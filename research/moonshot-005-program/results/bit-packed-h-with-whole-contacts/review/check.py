#!/usr/bin/env python3
"""Source-first native replay of 51 original full contacts in the packed-H word."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
import numpy as np
def target(i,j):
    A=np.eye(480,dtype=np.uint8)
    if (i,j)in ((80,2),(0,10)):
        dest,src=(0,2)if i==80 else(1,0)
        for h in range(2):
            A[h*48+4*dest:h*48+4*dest+4,h*48+4*src:h*48+4*src+4]=np.eye(4,dtype=np.uint8)
    return A
def review(a):
    spec=importlib.util.spec_from_file_location('forward_cascade',a.engine/'check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    alg=m.load_replay(a.forward);eng=m.Engine(a.stream);alg.mm=eng.mm;n=alg.Native(a);g=np.load(a.gauges);ass={int(j):ii for j,ii in json.loads(a.assignment.read_text()).items()};ass[10]=[0];ass[2]=ass[2]+[80];dig=hashlib.sha256();checks=0
    for j,receivers in sorted(ass.items()):
        dv=n.through_d(j,receivers)
        for i in receivers:
            _,_,B,_=n.facet(dv,i,'spread');reconstructed=np.empty_like(B)
            for a0,k in ((slice(0,96),3),(slice(96,480),12)):
                for q0,k0 in ((slice(0,96),3),(slice(96,480),12)):
                    reconstructed[a0,q0]=eng.mm(eng.mm(g[f'O{i}-{k}'],B[a0,q0]),g[f'G{j}-{k0}'])
            E=target(i,j);assert np.array_equal(reconstructed,E)
            dig.update(bytes([i,j]));dig.update(reconstructed.tobytes());checks+=1
    assert checks==51
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps({'full_source_first_body_matrices':51,'actual_body_coefficients_checked':51*480*480,'physical_copy_factor':8,'true_result_stream_sha256':dig.hexdigest()},indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for s in ('repo','engine','forward','h-words','d-words','k-words','f-words','stream','gauges','assignment','out'):p.add_argument('--'+s,type=Path,required=True)
 review(p.parse_args())
