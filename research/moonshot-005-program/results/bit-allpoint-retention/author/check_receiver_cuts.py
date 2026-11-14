#!/usr/bin/env python3
"""Exact exhaustive receiver-union cut certificate after all111 point copies.
The all-subsets reduction is proved in PROOF.md; this checks its finite domain.
"""
import argparse,gzip,hashlib,json,runpy
from collections import Counter
from fractions import Fraction
from pathlib import Path

def rank(rows):
    piv={}
    for row in rows:
        while row:
            p=row.bit_length()-1
            if p not in piv:
                piv[p]=row;break
            row^=piv[p]
    return len(piv)

def enumerate_cuts(N,B):
    allmask=(1<<111)-1;noncoord=allmask^255
    adj=[v&~(1<<i) for i,v in enumerate(N)]
    labels=[sum(((b>>j)&1)<<t for t,b in enumerate(B)) for j in range(111)]
    label_masks=[sum(1<<j for j in range(111) if labels[j]==b) for b in range(8)]
    ranklookup=[rank([b for b in range(1,8) if (s>>(b-1))&1]) for s in range(128)]
    def info_rank(mask):
        return ranklookup[sum(1<<(b-1) for b in range(1,8) if mask&label_masks[b])]
    result={'maximum_conditional_target_deficit':0,'cliques_visited':0,'maximum_noncoordinate_clique_size':0,
            'nontrivial_cuts_checked':0,'witness':None}
    counts=Counter()
    def visit(L,k,P,U,coord):
        result['cliques_visited']+=1
        result['maximum_noncoordinate_clique_size']=max(k,result['maximum_noncoordinate_clique_size'])
        choices=[0] if k>=7 else []
        if k>=6:
            choices += [1<<i for i in range(8) if (coord>>i)&1]
        for T in choices:
            u=U
            if T:u&=N[T.bit_length()-1]
            d=k+T.bit_count()-info_rank(u)+info_rank(u&~L)
            result['nontrivial_cuts_checked']+=1;counts[d]+=1
            if d>result['maximum_conditional_target_deficit']:
                result['maximum_conditional_target_deficit']=d
                result['witness']={'noncoordinate_clique':[j for j in range(8,111) if (L>>j)&1],
                    'coordinates':[j for j in range(8) if (T>>j)&1],
                    'outside_nuisance_inputs':[j for j in range(8,111) if ((u&~L)>>j)&1],
                    'outside_core_rank':info_rank(u),'outside_nuisance_core_rank':info_rank(u&~L),
                    'deficit':d}
        while P:
            bit=P&-P;v=bit.bit_length()-1;P^=bit
            visit(L|bit,k+1,P&adj[v],U&N[v],coord&(N[v]&255))
    visit(0,0,noncoord,noncoord,255)
    result['deficit_counts']=dict(sorted(counts.items()))
    return result

def main(a):
    raw=a.native.read_bytes();m=runpy.run_path(str(a.builder))
    if hashlib.sha256(raw).hexdigest()!=m['PIN']:raise ValueError('native source pin')
    native=json.loads(gzip.decompress(raw));c=m['analyse'](native)
    roots=[[Fraction(x) for x in native['frames'][str(native['start'][j])]['B'][0]] for j in range(111)]
    N=[sum(1<<j for j in range(111) if sum(x*y for x,y in zip(roots[i],roots[j]))!=0) for i in range(111)]
    result=enumerate_cuts(N,c['B'])
    if result['maximum_conditional_target_deficit']!=6:raise ValueError('cut condition failed')
    if (result['cliques_visited'],result['nontrivial_cuts_checked'])!=(305073,62003):raise ValueError('domain count changed')
    # A changed pivot gauge is a meaningful negative control, not a search failure.
    old=[]
    for k in c['K']:
        row=k&~255
        for g in c['groups']:
            if (k>>min(g['indices']))&1:row^=g['row']
        old.append(row)
    oldbasis=[]
    for row in old:
        if rank(oldbasis+[row])>len(oldbasis):oldbasis.append(row)
    if len(oldbasis)!=3:raise ValueError('old gauge rank changed')
    oldresult=enumerate_cuts(N,oldbasis)
    if oldresult['maximum_conditional_target_deficit']<8:raise ValueError('old pivot failure not detected')
    zeroresult=enumerate_cuts(N,[0,0,0])
    if zeroresult['maximum_conditional_target_deficit']!=8:raise ValueError('no-core control')
    out={'status':'PASS_EXACT_ALL_RECEIVER_SUBSET_REDUCTION_NO_LOCAL_DROPS',
         'native_sha256':hashlib.sha256(raw).hexdigest(),'builder_sha256':hashlib.sha256(a.builder.read_bytes()).hexdigest(),
         'model':'All111 pure input copies at original source lines; three pure B caches at zero; arbitrary independent Y preloaded by E; original halfbanks at exact local spans.',
         'exact_reduced_enumeration':result,
         'negative_controls':{'minimum_index_pivots':oldresult,'zero_core':zeroresult},
         'universal_scope':'The proof reduces every receiver subset to the enumerated clique domain or a demand set of at most6. This is necessary communication-cut feasibility only.',
         'completed_decoder':False,'new_kappa':False}
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':out['status'],'maximum_deficit':6,'checks':result['nontrivial_cuts_checked'],'negative_maxima':[oldresult['maximum_conditional_target_deficit'],zeroresult['maximum_conditional_target_deficit']]}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--builder',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
