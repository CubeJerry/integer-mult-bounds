#!/usr/bin/env python3
"""Check the genuine weighted full-bank profile and bilateral S028 slice identities."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import numpy as np
import aggregate
import disjoint
import fastprice
import profile as algebra


def sha(value):
    return hashlib.sha256(value).hexdigest()


def load_module(path, name):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def read_blocks(cache, i, expected):
    matrix=np.load(cache/f'W{i:03}.npy',mmap_mode='r',allow_pickle=False)
    algebra.need(matrix.shape==(16,480,480) and sha(matrix)==expected,'actual aggregate coefficients')
    return matrix[0],matrix[1],list(matrix[2:9]),list(matrix[9:16])


def build_spaces(state,field,previous,null,widths,weights,cache,params):
    spaces={};forms=[]
    for i in range(111):
        blocks=read_blocks(cache,i,params['aggregate_sha256'][str(i)])
        V,Q=algebra.image_and_form(i,state,field,previous,widths,weights,blocks)
        X=algebra.preimage(field,null,blocks,V)
        receipt=params['facets'][str(i)]
        algebra.need((V.shape[1],X.shape[1])==(receipt['v'],receipt['x']),'native preimage dimensions')
        spaces[i]=V,X
        if len(Q):forms.append(Q)
    all_rows=np.vstack(forms)
    return spaces,all_rows[field.pivots(all_rows.T)]


def check_profile(args,author,temp):
    results=args.repo/'research/moonshot-005-program/results'
    earlier=args.bilateral_author or results/'bit-global-source-facet-row-column/author'
    flat=args.flat_author or results/'bit-global-facet-shared-coordinates/author'
    sys.path.insert(0,str(earlier.resolve()))
    previous=load_module(earlier/'check.py','bilateral_word')
    first,target,field,_,state,late=previous.setup(args,temp)
    fixed=json.loads((earlier/'output/PARAMETERS.json').read_text());widths=fixed['output_dimensions']
    weights=np.array(json.loads((flat/'output/PARAMETERS.json').read_text())['weights'],dtype=np.uint8)
    raw=(author/'output/PROFILE.json').read_bytes()
    algebra.need(sha(raw)=='d42fffe7164f7e053d901a881cc1bf8b329c757c0f54842c3ec476a1833ddd07','native profile parameter pin')
    params=json.loads(raw);cache=args.aggregate_cache or temp/'aggregate'
    if not all((cache/f'W{i:03}.npy').is_file() for i in range(111)):
        aggregate.prepare(previous,first,field,state,fixed,weights,late,cache)
    spaces,Q=build_spaces(state,field,previous,target.null_basis,widths,weights,cache,params)
    common=np.kron(np.eye(8,dtype=np.uint8),state['U'][:,:7]);tests=[common]+[M for pair in spaces.values() for M in pair]
    required=max(M.shape[1]-field.rank(field.mm(Q,M)) for M in tests)
    algebra.need(required==params['extra'] and len(Q)==params['q'],'computed number of compatibility rows and additional directions')
    plus=params['plus'];seed=params['seed']
    Z=np.vstack([Q,first.coefficients(f'common bilateral profile/{plus}/{seed}',(required+plus,3840))])
    algebra.need(sha(Z)==params['annihilator_sha256'] and field.rank(Z)==len(Z)==params['r'],'common profile annihilator')
    algebra.need(all(field.rank(field.mm(Z,M))==M.shape[1] for M in tests),'common transversality to every actual image and preimage')
    # Deleting compatibility rows cannot preserve the prescribed original output rows on this synchronization.
    arbitrary=first.coefficients('negative bilateral no target compatibility',(len(Z),3840))
    algebra.need(field.rank(np.vstack([arbitrary,Q]))>len(Z),'negative control lost an actual original output functional')
    prices=json.loads((author/'output/WORD-PRICES.json').read_text()) if (author/'output/WORD-PRICES.json').is_file() else {}
    compact=json.loads((author/'output/FAST-PRICES.json').read_text())
    W=target.null_basis(field,Z)
    for i,(V,_) in spaces.items():
        blocks=read_blocks(cache,i,params['aggregate_sha256'][str(i)]);record=params['facets'][str(i)]
        dual=algebra.preimage(field,target.null_basis,algebra.transpose(blocks),Z.T)
        ann_a=field.mm(dual,target.null_basis(field,field.mm(V.T,dual))).T
        ann_b=field.mm(target.null_basis(field,field.mm(Z,V).T).T,Z)
        d=len(Z)-V.shape[1]
        algebra.need(sha(ann_a.copy())==record['annA'] and sha(ann_b)==record['annB'] and len(ann_a)==len(ann_b)==record['d']==d,'actual dual annihilator of both candidate basis images')
        N=first.coefficients(f"bilateral facet common complement/{i}/{record['complement']}",(3840,d))
        algebra.need(field.rank(field.mm(ann_a,N))==d==field.rank(field.mm(ann_b,N)),'one actual common complement for both full dimension bases')
        bill=fastprice.compute(field,blocks,weights[i],Z,W,V,N)
        algebra.need(bill==compact[str(i)],'factored in-place native forward and inverse prices')
        if args.verify_prices:
            A=np.hstack([V,algebra.apply(field,blocks,W),N]);B=np.hstack([V,field.product[weights[i],W],N]);P=state['P'][:widths[i]]
            algebra.need(all(np.array_equal(field.mm(P,x),field.mm(P,y)) for x,y in zip(A.reshape(8,480,-1),B.reshape(8,480,-1))),'native measured rows are pointwise fixed')
            got={'raw_X':sha(A),'raw_Y':sha(B),'X':field.invert_and_price(A)[1],'Y':field.invert_and_price(B)[1]}
            algebra.need(got==prices[str(i)],'complete native binary forward/inverse ADD ledger')
    right=previous.bounds.target_kernel(field,state,state['U'][:,:7],state['tiers'],False)
    remaining=3840-len(Z);combined=right['forced_kernel']+remaining
    receipt={'status':'PASS_FULL_NATIVE_BILATERAL_TARGET_SLICES_AND_COMMON_BANK_RETURN_PROFILE',
             'native_proper_pairs':6470,'native_facets':len(spaces),'true_target_nonflat_blocks':len(state['terms']),
             'target_input_directions_by_donor':{str(8*n):state['tiers'].count(n) for n in sorted(set(state['tiers']))},
             'target_output_functionals_by_receiver':{str(8*n):widths.count(n) for n in sorted(set(widths))},
             'weighted_native_compatibility_rows':len(Q),'additional_common_annihilator_rows':required+plus,
             'profile_dimension':remaining,'target_input_kernel':right['forced_kernel'],'joint_return_kernel_lower':combined,
             'native_return_rank_upper':426240-combined,'new_INIT':0,'new_dirty_CLEAR':0,'new_MOVE':0,
             'native_aggregate_arrays':111,'new_complete_kappa':False}
    receipt['disjoint_roles_lower_bound']=disjoint.check(previous,first,field,state,fixed,late)
    receipt['native_return_rank_lower']=receipt['disjoint_roles_lower_bound']['full_return_lower_bound']
    forward=sum(x['native_forward_ADD']for x in compact.values())
    receipt.update({'native_extra_forward_binary_ADD':forward,'native_extra_pure_inverse_binary_ADD':forward,'native_extra_combined_binary_ADD':2*forward})
    if prices:
        algebra.need(set(prices)=={str(i) for i in range(111)},'one complete physical matrix ledger for each facet')
        forward=sum(x['X']+x['Y'] for x in prices.values())
        receipt['independent_dense_basis_compilation_combined_binary_ADD']=2*forward
    return receipt


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    for name in ('flat-author','target-author','bilateral-author','cache-dir','late-cache','aggregate-cache'):p.add_argument('--'+name,type=Path)
    p.add_argument('--verify-prices',action='store_true',help='also expand all 222 native 3,840-dimensional factors')
    args=p.parse_args();author=Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix='bilateral-profile-') as td:receipt=check_profile(args,author,Path(td))
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print('PASS',receipt['profile_dimension'],'profile dimensions;',receipt['joint_return_kernel_lower'],'joint return kernel')


if __name__=='__main__':main()
