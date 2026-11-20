#!/usr/bin/env python3
"""Verify true S028 rows and columns across all native foreign source/receiver pairs."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import numpy as np
import bounds
import donor
import late
import state as layers


def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result


def setup(args,temp):
    author=Path(__file__).resolve().parent;results=args.repo/'research/moonshot-005-program/results'
    flat=args.flat_author or results/'bit-global-facet-shared-coordinates/author';target=args.target_author or results/'bit-global-two-sided-facet-slices/author';up=results/'bit-spread-rs-physical-word/author'
    sys.path.insert(0,str(flat.resolve()));first=module(flat/'check.py','shared_facet');second=module(target/'check.py','true_target_slices');sys.path.insert(0,str(up.resolve()));import transfer
    lib=temp/'finite-field.so';subprocess.run(['cc','-O3','-march=native','-shared','-fPIC',str(flat/'field.c'),str(up/'gf64_matmul.c'),'-o',str(lib)],check=True)
    f=first.Field(lib,transfer);native=transfer.Atlas(args.repo,results/'bit-gf64-actual-k-atlas/author/output',results/'bit-minimum-cache-d-atlas/author/output/CHARTS.json.gz',lib);native.results=results
    cache=args.cache_dir or temp/'early';after=args.late_cache or temp/'late'
    if not all((cache/f'{p}{i}.npy').is_file() for i in range(111) for p in ('E','B')):first.prepare(native,cache)
    flat_params=json.loads((flat/'output/PARAMETERS.json').read_text());primal=json.loads((target/'output/PARAMETERS.json').read_text())
    state=layers.restore(f,first,second,flat_params,primal,native,cache);state['field']=f;state['P']=first.coefficients('globally shared native output rows 0',(8,480))
    if not all((after/f'{p}{i}.npy').is_file() for i in range(111) for p in ('IDs','L')):
        late.prepare(native,transfer,{i:state['VS'][i][0] for i in range(111)},after)
    return first,second,f,native,state,after


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--cache-dir',type=Path);p.add_argument('--late-cache',type=Path);p.add_argument('--flat-author',type=Path);p.add_argument('--target-author',type=Path)
    args=p.parse_args();author=Path(__file__).resolve().parent;raw=(author/'output/PARAMETERS.json').read_bytes()
    donor.need(hashlib.sha256(raw).hexdigest()=='058735201781330ed80758108d959684dd94580bc5c27da9bb48d158a9ee1ee1','literal native source seeds and true late owner certificates')
    params=json.loads(raw);widths=params['output_dimensions']
    with tempfile.TemporaryDirectory(prefix='dual-physical-') as td:
        prev,prior,f,native,s,cache=setup(args,Path(td));minor=np.eye(12*480,dtype=np.uint8);receipts={}
        for j in range(111):
            receipts[j],_=donor.verify_donor(j,f,prev.coefficients,s,params,cache,minor)
        pairs=sum(len(x) for x in s['adj']);donor.need(pairs==6470,'complete native adjacency')
        exercised=sum(any(np.any(donor.dual_N(i,j,g,h,s,widths)) for g in range(8) for h in range(8)) for i,j in s['terms'])
        donor.need(exercised==123,'all five internal and 118 cross-bank perturbations exercised by output probes')
        in_tiers=s['tiers'];right=bounds.target_kernel(f,s,s['U'][:,:max(in_tiers)],in_tiers,False)
        left=bounds.target_kernel(f,s,s['P'][:max(widths)].T,widths,True)
        pairings={m:f.rank(f.mm(s['P'][:m],s['U'][:,:m])) for m in sorted(set(widths))}
        rank=f.rank(minor);upper=426240-max(right['forced_kernel'],left['forced_kernel'])
        donor.need(7*rank>34688,'physical rim minor exceeds S028 target return')
        result={'status':'PASS_SIMULTANEOUS_ORIGINAL_ROWS_AND_COLUMNS_ON_EVERY_FOREIGN_EDGE',
                'native_foreign_pairs':pairs,'nonidentity_target_edges_seen_from_input_and_output':exercised,
                'input_directions_by_donors':{8*k:v for k,v in Counter(in_tiers).items()},'output_functionals_by_receivers':{8*k:v for k,v in Counter(widths).items()},
                'weighted_total_input_directions_over_pairs':8*sum(sum(in_tiers[j] for j in js) for js in s['adj']),
                'weighted_total_output_functionals_over_pairs':8*sum(len(js)*widths[i] for i,js in enumerate(s['adj'])),
                'pairing_ranks_of_leading_basis_directions':pairings,'right_restricted_target_fitting':right,'left_restricted_target_fitting':left,
                'first_twelve_roles_one_rim_copy_minor_rank':rank,'first_twelve_roles_one_rim_copy_minor_sha256':hashlib.sha256(minor).hexdigest(),
                'native_return_rank_lower':7*rank,'native_return_rank_upper':upper,'new_source_binary_ADD':sum(v['binary_add'] for v in receipts.values()),
                'new_source_INIT':0,'new_source_dirty_CLEAR':0,'new_pure_inverse_ADD':0,'new_MOVE':0,
                'actual_pair_blocks_requiring_nonzero_Schur_corrections':sum(v['native_schurs'] for v in receipts.values()),
                'complete_target':False,'new_complete_kappa':False,'per_donor':receipts}
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS',pairs,'both directional tests,',exercised,'nonflat blocks, return rank in',7*rank,upper)

if __name__=='__main__':main()
