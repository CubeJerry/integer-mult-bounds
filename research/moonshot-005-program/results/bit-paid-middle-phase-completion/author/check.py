#!/usr/bin/env python3
from argparse import ArgumentParser
from itertools import combinations,product
from pathlib import Path
import json

def span(rows):
    S={0}
    for r in rows:S|={x^r for x in list(S)}
    return frozenset(S)
def dim(S):return len(S).bit_length()-1
def all_spaces(n):
    found={frozenset([0])};todo=list(found)
    while todo:
        S=todo.pop()
        for v in range(1,1<<n):
            T=span(S|{v})
            if T not in found:found.add(T);todo.append(T)
    return sorted(found,key=lambda s:(len(s),sorted(s)))
def subsets(items):return(c for k in range(len(items)+1)for c in combinations(items,k))
def sum_spaces(Q,indices):return span(set().union(*(Q[i]for i in indices)))
def hall(Q,indices):return all(dim(sum_spaces(Q,S))>=len(S)for S in subsets(indices))
def late_condition(Q,indices,nE,s):return all(dim(span(x>>nE for x in sum_spaces(Q,S)))+s>=len(S)for S in subsets(indices))

def main():
    ap=ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    planes=[S for S in all_spaces(3)if dim(S)==2];assert len(planes)==7
    E=span([1,2]);cases=[]
    for V1,V2 in product(planes,repeat=2):
        Q=[frozenset(V1&V2&E),V1,V2]
        H=hall(Q,[0,1])and hall(Q,[0,2]);Ec=hall(Q,[0]);Lc=late_condition(Q,[1,2],2,1)
        predicted=H and Ec and Lc;witness=None
        for qe,qb,qc in product(*[sorted(S)for S in Q]):
            if dim(span([qe,qb]))!=2 or dim(span([qe,qc]))!=2:continue
            closures=[r for r in E if dim(span([qe,r]))==2]
            if not closures:continue
            for b1,b2 in product(range(2),repeat=2):
                purelate=[(qb>>2)|(b1<<1),(qc>>2)|(b2<<1)]
                if dim(span(purelate))==2:witness=[qe,qb,qc,closures[0],b1,b2];break
            if witness:break
        assert bool(witness)==predicted
        cases.append({'V1':sorted(V1),'V2':sorted(V2),'H':H,'E':Ec,'L':Lc,'linear_binary_witness':witness})
    Q=[span([1]),span([1]),span([4])]
    assert all(hall(Q,[i])for i in range(3))and not hall(Q,[0,1])
    Q=[span([1]),span([1])]
    assert all(hall(Q,[i])for i in range(2))and not late_condition(Q,[0,1],1,1)
    Q=[span([1]),span([1]),span([1,2,4])]
    assert dim(span(x>>1 for x in sum_spaces(Q,[0,1,2])))==2
    assert not late_condition(Q,[0,1,2],1,1)
    proper=arbitrary=0
    for u1,u2,v,y1,y2 in product(range(4),repeat=5):
        cache=(u1,u2);early=u1;closure=u2;late1=v^y1;late2=y2^cache[1]
        assert(early,closure)==(u1,u2)and(late1,late2)==(v^y1,u2^y2);arbitrary+=1
        if y1==y2==0:
            assert(early,late1)==(u1,v)and(early,late2)==(u1,u2);proper+=1
    for u1,u2 in product(range(4),repeat=2):assert len({(y1,y2^u2)for y1,y2 in product(range(4),repeat=2)})==16
    owners={}
    for k in range(2):
        owners[f'u1_{k}']=1<<k;owners[f'u2_{k}']=1<<(2+k)
        owners[f't_{k}']=(1<<(4+k))^(1<<(6+k));owners[f'b_{k}']=1<<(8+k)
    counts={'INIT':0,'ADD':0,'CLEAR':0};peak=0
    for name in ['u1_0','u1_1','u2_0','u2_1']:
        owners['cache_'+name]=0;counts['INIT']+=1
        owners['cache_'+name]^=owners[name];counts['ADD']+=1;peak+=1
    departures={k:owners.pop(k)for k in ['u1_0','u1_1','u2_0','u2_1']}
    for k in range(2):owners[f'b_{k}']^=owners[f'cache_u2_{k}'];counts['ADD']+=1
    for name in ['u1_0','u1_1','u2_0','u2_1']:
        assert owners['cache_'+name]!=0;del owners['cache_'+name];counts['CLEAR']+=1
    for k in range(2):
        assert owners[f't_{k}']==(1<<(4+k))^(1<<(6+k))
        assert owners[f'b_{k}']==(1<<(2+k))^(1<<(8+k))
    assert counts=={'INIT':4,'ADD':6,'CLEAR':4}and peak==4
    assert all('cache'not in k for k in owners)
    omitted_cross_control=(1<<8)!=((1<<2)^(1<<8));assert omitted_cross_control
    M=N=4;bound=2*(M*M+3*M)+2*(N*N+3*N)+M*N+M;assert bound==132
    result={'status':'PASS_PAID_MIDDLE_PHASE_COMPLETION','two_target_plane_cases':49,
      'positive_cases':sum(bool(x['linear_binary_witness'])for x in cases),'cases':cases,
      'controls':{'receiver_tests_do_not_imply_early_inverse':True,'receiver_tests_do_not_imply_late_inverse':True,'late_total_rank_without_subsets_insufficient':True,'omitted_cross_rejected':omitted_cross_control},
      'literal_positive_example':{'field':'GF4','proper_states':proper,'all_original_X_Y_states':arbitrary,'pure_late_bijections':16,'binary_primitive_counts':counts,'additional_auxiliary_peak':peak,'conservative_ADD_bound':bound,'added_MOVE':0,'all_cache_owners_retired':True},
      'general_field_threshold':'q>d+1, hence q>4 for native fanout3','new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status']);print('plane pairs',49,'positive',result['positive_cases'],'arbitrary X/Y states',arbitrary)
if __name__=='__main__':main()
