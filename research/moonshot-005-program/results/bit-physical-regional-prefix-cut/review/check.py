#!/usr/bin/env python3
"""Audit the submitted pre-K square minors in reversed field coordinate order."""
import argparse,ctypes,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
import numpy as np

def main():
    p=argparse.ArgumentParser()
    for name in ('repo','transfer','engine','k-words','d-words','stream-lib','mult','cut','out'):
        p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--sector',choices=('small','large'),required=True)
    a=p.parse_args();sys.path.insert(0,str(a.transfer.resolve()))
    from transfer import Atlas
    spec=importlib.util.spec_from_file_location('reverse_stream',a.engine/'check.py')
    eng=importlib.util.module_from_spec(spec);spec.loader.exec_module(eng);e=eng.Engine(a.stream_lib)
    at=Atlas(a.repo,a.k_words,a.d_words,a.mult)
    record=json.loads((a.cut/(a.sector.upper()+'.json')).read_text())
    raw=gzip.decompress((a.cut/(a.sector.upper()+'-PIVOTS.json.gz')).read_bytes())
    assert hashlib.sha256(raw).hexdigest()==record['selected_columns_sha256']
    chosen=set(json.loads(raw));small=a.sector=='small';n=record['rank'];w=record['source_width']
    ks={k for i in record['rows'] for k in at.ks[i]};start=0 if small else 96
    owners=sorted([u for u,r in at.route.items() if r[5] in ks and (r[4] in at.marked)==small],reverse=True)
    assert len(owners)==n==len(chosen)
    index={u:t for t,u in enumerate(owners)}
    used={j:sorted([t for t in range(w) if s*w+t in chosen],reverse=True) for s,j in enumerate(record['donors'])}
    st=e.lib.begin(n);ops=e.lib;cnt=0;h=hashlib.sha256()
    try:
        for j,cols in reversed(list(used.items())):
            if not cols:continue
            source=at.left(j);packet=np.zeros((len(cols),n),dtype=np.uint8)
            inds=np.array(cols)+start
            for d,roots in enumerate(at.D):
                if j not in roots or ((d in at.marked)!=small):continue
                M,oo=at.middle_matrix(d)
                dst=[p for p,u in enumerate(oo) if u in index]
                if not dst:continue
                src=[p for p,u in enumerate(oo) if u in source]
                assert len(src)==8
                block=at.ops.matmul(M[np.ix_(dst,src)],np.array([source[oo[p]][inds] for p in src]))
                packet[:,[index[oo[p]] for p in dst]]=block.T
            h.update(memoryview(packet)); cnt+=len(packet)
            for pos in range(0,len(packet),64):
                blk=packet[pos:pos+64]
                assert ops.consume(st,blk.ctypes.data,len(blk))
            if cnt//w%15==0:print(a.sector,cnt,ops.present_rank(st),flush=True)
        rank=ops.present_rank(st);det=ops.determinant(st)
        assert cnt==rank==n and det==record['certificate_minor_determinant']
        a.out.mkdir(exist_ok=True,parents=True)
        out={'sector':a.sector,'submitted_square_minor_rank':rank,'independent_determinant':det,
             'reversed_coordinates_square_hash':h.hexdigest(),'mode':'H left-owner factor, literal D minor; reversed source and receiver order'}
        (a.out/(a.sector.upper()+'.json')).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
        print(out,flush=True)
    finally:ops.finish(st)
if __name__=='__main__':main()
