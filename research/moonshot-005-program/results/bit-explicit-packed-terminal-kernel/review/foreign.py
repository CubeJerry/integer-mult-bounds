import argparse,gzip,hashlib,importlib.util,json
from pathlib import Path
import numpy as np
from recfield import Field
from basis import change
from action import unpack
def main(args):
    spec=importlib.util.spec_from_file_location('canonical_direct',args.canonical/'check.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    alg=mod.load_replay(args.replay);engine=mod.Engine(args.stream_lib);alg.mm=engine.mm
    nat=alg.Native(args);f=Field(args.lib);sector=args.sector;w,lo,n=(96,0,9)if sector=='small'else(384,96,36)
    receipts=json.loads(gzip.decompress((args.program/'output/TERMINAL-RECEIPTS.json.gz').read_bytes()))[sector]
    ownerfile=np.load(args.owner_dir/(sector+'-owners.npz'));owners={i:np.concatenate([ownerfile[f'{i}-X'],ownerfile[f'{i}-Y']]).tolist()for i in range(111)}
    cascade=mod.Cascade(nat,alg,engine,sector=='small')
    F={};digest=hashlib.sha256();checked=0
    for i in range(111):
        _,raw=unpack(args.program/sector,i);rows=raw.reshape(w,len(owners[i]));limbs=f.b.limbs(rows);F[i]=np.ascontiguousarray(limbs.transpose(2,0,1)).reshape(4*w,-1)
    for j in range(args.start,args.stop):
        dv=nat.through_d(j,range(111),sector=='small');zero=np.zeros(w,dtype=np.uint8);physical={}
        for h in cascade.by_donor[j]:
            strips,cross=cascade.word[h]
            for src,dst in strips:
                vals=np.stack([dv[t][lo:lo+w]if t in dv else zero for t in src])
                if vals.any():physical.update(zip(dst,engine.mm(cascade.vandermonde,vals)))
            for x,y in cross:
                if x in physical:
                    if y in physical:physical[y]^=physical[x]
                    else:physical[y]=physical[x].copy()
        for i in np.flatnonzero(nat.orth[:,j]):
            i=int(i);M=np.stack([physical.get(t,zero)for t in owners[i]]);P=engine.mm(F[i],M).reshape(4,w,w).transpose(1,2,0)
            A=change(f.b.wrap(P),f.b.rec);rank,det=f.det(A)
            actual=receipts[i]['actual_foreign_nonzero_determinants'][str(j)];expected=int(change(np.uint32(actual),f.b.rec))
            assert rank==w and det==expected,(i,j,rank,det,expected)
            if i==int(np.flatnonzero(nat.orth[:,j])[0])and j==args.start:
                fault=A.copy();fault[0]=0;assert f.det(fault)[0]==w-1
            checked+=1;digest.update(bytes([i,j]));digest.update(det.to_bytes(3,'little'))
        if j%10==0:print(sector,j,checked,flush=True)
    args.out.mkdir(exist_ok=True,parents=True)
    (args.out/f'{sector}-foreign-{args.start}-{args.stop}.json').write_text(json.dumps({'sector':sector,'start':args.start,'stop':args.stop,'descending_reciprocal_field_determinants':checked,'determinant_stream_sha256':digest.hexdigest()},indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for z in ('repo','canonical','replay','h-words','d-words','k-words','stream-lib','program','lib','owner-dir','out'):p.add_argument('--'+z,type=Path,required=True)
    p.add_argument('--sector',choices=['small','large'],required=True);p.add_argument('--start',default=0,type=int);p.add_argument('--stop',default=111,type=int)
    main(p.parse_args())
