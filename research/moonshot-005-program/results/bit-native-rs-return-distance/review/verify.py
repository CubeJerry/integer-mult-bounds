#!/usr/bin/env python3
"""Independent native propagation and reciprocal-field rank on the disjoint 55-role restriction."""
import argparse,ctypes,hashlib,importlib.util,json
from pathlib import Path
import numpy as np

def main(args):
    spec=importlib.util.spec_from_file_location('streamed_cascade',args.canonical/'check.py')
    runner=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    alg=runner.load_replay(args.replay)
    engine=runner.Engine(args.stream_lib)
    alg.mm=engine.mm
    native=alg.Native(args)
    cascade=runner.Cascade(native,alg,engine,args.sector=='small')
    width=cascade.width
    n=55*width
    state=engine.lib.begin(n)
    assert state
    digest=hashlib.sha256()
    checks={}
    try:
        for j in range(56,111):
            data=np.ascontiguousarray(cascade.columns(j)[:,:n])
            assert data.shape==(width,n)
            digest.update(memoryview(data))
            for lo in range(0,width,32):
                small=data[lo:lo+32]
                assert engine.lib.consume(state,small.ctypes.data,len(small))
            if (j-55)%10==0 or j==110:
                checks[j]=engine.lib.present_rank(state)
                print(args.sector,j,checks[j],flush=True)
        det=engine.lib.determinant(state);rank=engine.lib.present_rank(state)
        expected=41 if args.sector=='small' else 52
        assert rank==n and det==expected
        info={"receiver_role_interval":[0,54],"donor_role_interval":[56,110],"sector":args.sector,"width":width,"rank":rank,
              "determinant_in_native_GF64":det,"basis_polynomials":[67,97],"orientation":"column-ordered transpose",
              "native_input_column_sha256":digest.hexdigest(),"checkpoints_after_original_donor":checks}
        args.out.mkdir(parents=True,exist_ok=True)
        (args.out/(args.sector.upper()+'.json')).write_text(json.dumps(info,sort_keys=True,indent=2)+'\n')
        print(info,flush=True)
    finally:engine.lib.finish(state)
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('repo','canonical','replay','h-words','d-words','k-words','stream-lib','out'):
        p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--sector',choices=['small','large'],required=True)
    main(p.parse_args())
