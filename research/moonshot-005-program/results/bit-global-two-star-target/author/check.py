#!/usr/bin/env python3
"""Verify the complete S028 nonflat native endpoint stars and a 220-edge exact extension."""
import argparse
from collections import Counter,defaultdict
import importlib.util
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import numpy as np
import native
import slices


def need(x,msg):
    if not x:raise ValueError(msg)


def check(args,author,temp):
    results=args.repo/'research/moonshot-005-program/results';bilateral=args.bilateral_author or results/'bit-global-source-facet-row-column/author'
    sys.path.insert(0,str(bilateral.resolve()));ss=importlib.util.spec_from_file_location('previous_bilateral',bilateral/'check.py');prev=importlib.util.module_from_spec(ss);ss.loader.exec_module(prev)
    first,_,field,_,state,late=prev.setup(args,temp);params=json.loads((bilateral/'output/PARAMETERS.json').read_text());width=params['output_dimensions'];tier=state['tiers'];adj=state['adj'];terms=state['terms']
    core_donors=set(adj[80]);core_facets=set(adj[10]);core={(80,j)for j in core_donors}|{(i,10)for i in core_facets}
    need(core==set(terms) and len(core_donors)==62 and len(core_facets)==61 and 10 not in core_donors and 80 not in core_facets,'the 123 full target matrices form two disjoint actual native stars')
    need(all(terms[i,j][0]==0 for i,j in core if i==80) and all(terms[i,j][1]==0 for i,j in core if j==10),'common original source or target aperture is precisely raw bank zero')
    need(set(state['copy'][:64])=={0} and tier[10]==5 and width[80]==7,'true raw aperture belongs to native copy zero')
    source={j:[(80,j)] for j in core_donors};facet={i:[(i,10)] for i in core_facets};assigned=set(core)
    for j in sorted(set(range(111))-core_donors-{10}):
        i=min(i for i in core_facets.intersection(adj[j]) if width[i]==7)
        source[j]=[(i,j),(i,10)];assigned.add((i,j))
    for i in sorted(set(range(111))-core_facets-{80}):
        j=min(j for j in core_donors.intersection(adj[i]) if tier[j]==7)
        facet[i]=[(i,j),(80,j)];assigned.add((i,j))
    need(len(assigned)==220 and len(source)==len(facet)==110,'two spanning native endpoint trees')
    per=defaultdict(list)
    for i,j in sorted(assigned):per[j].append(i)
    pins=json.loads((author/'output/SOURCE-PINS.json').read_text());ledger={};fullU={m:np.kron(np.eye(8,dtype=np.uint8),state['U'][:,:m])for m in set(tier)};fullP={m:np.kron(np.eye(8,dtype=np.uint8),state['P'][:m]).T for m in set(width)}
    minor=np.eye(5760,dtype=np.uint8)
    for j in range(111):
        if args.source_cache:program=native.cached(args.source_cache/f'{j:03}.npz')
        else:_,program=prev.donor.verify_donor(j,field,first.coefficients,state,params,late,minor)
        need(native.source_pin(*program)==pins[str(j)],'actual bilateral distributed source coefficient pin')
        ls=np.load(late/f'L{j}.npy',mmap_mode='r',allow_pickle=False);need(hashlib.sha256(ls).hexdigest()==params['donors'][str(j)]['late_transfer_sha256'],'actual native late transfer')
        for i in per[j]:
            z=native.whole(field,state,i,j,ls[adj[j].index(i)],program);t=terms.get((i,j));U=fullU[tier[j]];P=fullP[width[i]]
            need(np.array_equal(native.apply(field,z,U),native.target(field,U,t,state)),'all original input anchor comparisons before full physical inversion')
            need(np.array_equal(native.apply(field,native.adjoint(z),P),native.target(field,P,t,state,True)),'all original dual anchor comparisons before full physical inversion')
            rec=native.price(field,z);rec['original_target_forward_or_inverse_ADD']=native.target_price(field,t);ledger[i,j]=rec
    def invoice(words):
        return sum(ledger[p]['native_forward_or_inverse_ADD']+ledger[p]['original_target_forward_or_inverse_ADD'] for path in words.values()for p in path)
    def dump(paths):return {str(k):[list(pair)for pair in values]for k,values in sorted(paths.items())}
    right=slices.target_kernel(field,state,state['U'][:,:5],[5]*111,False);left=slices.target_kernel(field,state,state['P'][:7].T,width,True)
    pure_source=invoice(source);pure_facet=invoice(facet);pair_count=sum(map(len,adj));base_lower=46690
    return {'status':'PASS_ALL_123_COMPLETE_ORIGINAL_NONFLAT_TARGETS_AND_97_COMPLETE_FLAT_FOREIGN_BLOCKS','native_proper_pairs':pair_count,
        'true_nonflat_complete_blocks':len(core),'true_flat_complete_blocks_certified':len(assigned-core),'true_complete_blocks_certified':len(assigned),
        'complete_original_field_columns_on_each_whole_block':3840,'full_target_equations_on_complete_blocks':3840*len(assigned),
        'native_proper_rank_everywhere':3840,'native_remaining_full_output_input_directions_per_donor':35,
        'native_remaining_full_input_output_probes_by_receiver':{str(7*x):v for x,v in Counter(width).items()},
        'whole_column_donor':10,'whole_column_exact_edges':61,'whole_row_receiver':80,'whole_row_exact_edges':62,
        'native_source_forward_ADD':pure_source,'native_pure_source_inverse_ADD':pure_source,'native_facet_forward_ADD':pure_facet,'native_pure_facet_inverse_ADD':pure_facet,
        'new_combined_binary_ADD':2*(pure_source+pure_facet),'new_MOVE':0,'new_INIT':0,'new_dirty_CLEAR':0,
        'actual_disjoint_role_lower':base_lower,'restricted_target_fitting_right':right,'restricted_target_fitting_left':left,
        'native_return_upper':426240-max(right['forced_kernel'],left['forced_kernel']),'complete_kappa':False,
        'source_gauge_paths':dump(source),'facet_gauge_paths':dump(facet),'primitive_edge_words':{f'{i},{j}':rec for (i,j),rec in sorted(ledger.items())}}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    for n in ('bilateral-author','target-author','flat-author','cache-dir','late-cache','source-cache'):p.add_argument('--'+n,type=Path)
    args=p.parse_args();author=Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix='actual-two-star-') as td:result=check(args,author,Path(td))
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print('PASS',result['true_complete_blocks_certified'],result['new_combined_binary_ADD'],result['native_return_upper'])

if __name__=='__main__':main()
