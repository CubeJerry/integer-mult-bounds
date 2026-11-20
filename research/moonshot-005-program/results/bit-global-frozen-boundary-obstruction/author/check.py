#!/usr/bin/env python3
"""Compute the exact fixed early-kernel / late-image invariant at every flat target edge."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import numpy as np


def check(args):
    results=args.repo/'research/moonshot-005-program/results'
    bilateral=args.bilateral_author or results/'bit-global-source-facet-row-column/author';sys.path.insert(0,str(bilateral.resolve()))
    spec=importlib.util.spec_from_file_location('original_frozen_transfer',bilateral/'check.py');prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
    with tempfile.TemporaryDirectory(prefix='frozen-native-') as td:
        _,target,field,_,state,after=prior.setup(args,Path(td));hist=Counter();edges={};sample=None
        late={j:np.load(after/f'L{j}.npy',mmap_mode='r',allow_pickle=False) for j in range(111)}
        sources=json.loads((bilateral/'output/PARAMETERS.json').read_text())['donors']
        for j,L in late.items():
            if hashlib.sha256(L).hexdigest()!=sources[str(j)]['late_transfer_sha256']:raise ValueError('genuine late image pin')
        for i,neighbours in enumerate(state['adj']):
            V,_=state['VS'][i]
            for index,j in enumerate(neighbours):
                if (i,j) in state['terms']:continue
                L=late[j][state['adj'][j].index(i)];E=state['E'][i][index];B=state['B'][i][index];W=target.null_basis(field,E)
                residual=field.mm(field.mm(V,B)^np.eye(480,dtype=np.uint8),W)
                r=field.rank(L);d=field.rank(np.hstack([L,residual]))-r;hist[d]+=1;edges[i,j]=d
                if (i,j)==(0,5):
                    # Both classes of allowed changes vanish in this quotient even after a nonzero injection.
                    X=np.zeros((480,E.shape[0]),dtype=np.uint8);X[0,0]=1;Y=np.zeros((L.shape[1],480),dtype=np.uint8);Y[0,0]=1
                    modified=field.mm(field.mm(V,B)^np.eye(480,dtype=np.uint8)^field.mm(X,E)^field.mm(L,Y),W)
                    if field.rank(np.hstack([L,modified]))-r!=d:raise ValueError('fixed double quotient was altered by an allowed adjustment')
                    sample={'receiver':i,'donor':j,'native_early_kernel':W.shape[1],'native_late_rank':r,'native_quotient_rank':d,'full_target_error_rank_lower':8*d,'largest_possible_exact_input_subspace':3840-8*d}
        if (len(edges),sample['native_early_kernel'],sample['native_late_rank'],sample['native_quotient_rank'])!=(6347,300,180,300):raise ValueError('complete canonical edge scan or original designated witness')
        ordered=np.array([edges[key] for key in sorted(edges)],dtype='<u2')
        return {'status':'PASS_FROZEN_EARLY_KERNEL_LATE_IMAGE_OBSTRUCTION','canonical_original_edges':len(edges),'native_quotient_rank_histogram':hist,
                'full_target_error_rank_lower_at_each_canonical_edge':8*min(hist),'canonical_rank_census_sha256':hashlib.sha256(ordered).hexdigest(),
                'maximizing_native_edge':sample,'complete_kappa_implication':False}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    for name in ('flat-author','target-author','bilateral-author','cache-dir','late-cache'):p.add_argument('--'+name,type=Path)
    args=p.parse_args();res=check(args);args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(res,sort_keys=True,indent=2)+'\n')
    print('PASS',res['canonical_original_edges'],'original flat blocks, designated obstruction',res['maximizing_native_edge']['full_target_error_rank_lower'])

if __name__=='__main__':main()
