import argparse,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
import numpy as np
from basis import Basis,change
from native import arrivals

def unpack(folder,i):
    raw=(folder/f'F{i:03}.bin').read_bytes();b=np.frombuffer(raw,dtype=np.uint8).astype(np.uint32).reshape(-1,3)
    return raw,b[:,0]^(b[:,1]<<8)^(b[:,2]<<16)
def main(args):
    spec=importlib.util.spec_from_file_location('canonical_direct',args.canonical/'check.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    alg=m.load_replay(args.replay);engine=m.Engine(args.stream_lib);mm=engine.mm;alg.mm=mm
    nat=alg.Native(args);basis=Basis();sector=args.sector;w,d=(96,168)if sector=='small'else(384,672)
    receipts=json.loads(gzip.decompress((args.program/'output/TERMINAL-RECEIPTS.json.gz').read_bytes()))[sector]
    folder=args.program/sector;counts={};csha=hashlib.sha256()
    data,owners,zs=arrivals(nat,alg,mm,sector)
    np.savez_compressed(args.out/(sector+'-owners.npz'),**{f'{i}-{p}':np.array(v[idx],dtype=np.int64)for i,v in owners.items()for idx,p in enumerate(('X','Y'))})
    for i in range(111):
        e,y=owners[i];raw,F=unpack(folder,i);F=F.reshape(w,len(e)+len(y));r=receipts[i]
        assert r['facet']==i and r['early_count']==len(e) and r['late_count']==len(y)==w and r['preterminal_count']==F.shape[1]
        assert r['actual_GF24_terminal_word_SHA256']==hashlib.sha256(raw).hexdigest()and set(map(int,r['actual_foreign_nonzero_determinants']))==set(np.flatnonzero(nat.orth[i]))
        four=basis.matrix(F);src=data[e+y].reshape(len(e)+len(y),d,4);out=np.zeros((w,d,4),dtype=np.uint8)
        for u in range(4):
            for v in range(4):out[:,:,u]^=mm(four[:,:,u,v],src[:,:,v])
        target=zs[i].reshape(w,d,4);assert np.array_equal(out,target),(sector,i)
        h=hashlib.sha256(basis.wrap(target).tobytes()).hexdigest();assert h==r['all_mode_identity_SHA256']
        if i==0:
            fault=F.copy();fault[0,0]^=1
            assert np.any(src[0]) and not np.array_equal(out[0]^src[0],target[0])
        counts[i]={'early':len(e),'late':len(y),'matrix_sha256':hashlib.sha256(raw).hexdigest(),'identity_sha256':h}
        csha.update(raw)
        if i%20==0:print(sector,i,flush=True)
    result={'sector':sector,'facets':len(counts),'all_mode_columns_per_facet':d,'native_copy_limbs_rechecked':4,
            'matrix_stream_sha256':csha.hexdigest(),'all_receipts':counts,'changed_first_coefficient':'detected on true nonzero incoming data'}
    (args.out/(sector+'-action.json')).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for z in ('repo','canonical','replay','h-words','d-words','k-words','stream-lib','program','out'):p.add_argument('--'+z,type=Path,required=True)
    p.add_argument('--sector',choices=['small','large'],required=True)
    main(p.parse_args())
