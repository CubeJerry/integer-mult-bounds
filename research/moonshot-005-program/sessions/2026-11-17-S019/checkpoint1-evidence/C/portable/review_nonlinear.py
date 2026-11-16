#!/usr/bin/env python3
"""Independent full-coordinate audit of the symmetrized Petersen entropy dual.

No root checker is imported. Instead of collecting coefficients by canonical
orbit representatives, expand every inequality under every S5 permutation.
The conclusion must telescope in the original1024 subset coordinates.
"""
import argparse,copy,hashlib,json
from collections import defaultdict
from fractions import Fraction
from itertools import combinations,permutations
from pathlib import Path
from audit_cp6 import CP,sha,replay,insist,subset

def expanded_dual(d):
    P=list(combinations(range(5),2));index={p:i for i,p in enumerate(P)}
    insist(d['pair_labels']==[list(x)for x in P],'standard pair labels')
    neighbors=[{j for j,q in enumerate(P)if set(p).isdisjoint(q)}for p in P]
    actions=[[index[tuple(sorted((pi[a],pi[b])))]for a,b in P]for pi in permutations(range(5))]
    insist(len({tuple(x)for x in actions})==120,'120 distinct graph automorphisms')
    for action in actions:
        for i,N in enumerate(neighbors):insist({action[j]for j in N}==neighbors[action[i]],'automorphism preserves every neighbor set')
    def image(s,pi):return sum(1<<pi[i]for i in range(10)if s>>i&1)
    total=defaultdict(Fraction);rhs=Fraction();expanded=0
    for row in d['terms']:
        weight=Fraction(row['multiplier']);insist(weight>0,'nonnegative conic combination')
        kind,*z=row['inequality']
        if kind=='initialize':
            insist(z==[],'initialization shape');coeff={1023:-1};bound=-10
        else:
            insist(len(z)==(3 if kind=='submodularity'else 2),'elementary inequality arity')
            S,i,*q=z;insist(0<=S<1024 and 0<=i<10 and not S>>i&1,'elementary disjoint index');A=S|(1<<i)
            if kind=='slope':coeff={A:1,S:-1};bound=1
            elif kind=='monotonicity':coeff={S:1,A:-1};bound=0
            elif kind=='decode':
                insist(neighbors[i]<={j for j in range(10)if S>>j&1},'all raw decoder neighbors are granted');coeff={A:1,S:-1};bound=0
            elif kind=='submodularity':
                j=q[0];insist(i!=j and 0<=j<10 and not S>>j&1,'second distinct outside index');coeff={S:1,A|(1<<j):1,A:-1,S|(1<<j):-1};bound=0
            else:raise ValueError('unknown elementary Shannon inequality')
        insist(bound==row['rhs'],'declared right side')
        for pi in actions:
            for S,c in coeff.items():total[image(S,pi)]+=weight*c/Fraction(120)
            rhs+=weight*bound/Fraction(120);expanded+=1
    nz={S:c for S,c in total.items()if c}
    insist(nz=={0:Fraction(-1)}and rhs==-5,'full1024-coordinate exact telescope')
    return {'automorphisms':len(actions),'elementary_terms':len(d['terms']),'expanded_inequalities':expanded,'full_coordinate_nonzero_lhs':{S:str(c)for S,c in nz.items()},'rhs':str(rhs)}

def graph_check(repo,evidence):
    path=evidence/'A/local-canonical9-source/WORD.json';w=json.loads(path.read_text());src=repo/w['source_path'];source=json.loads(src.read_text());cut=w['carrier_interface_before_operation'];stats,snaps,C,_=replay(w,source,[cut]);values,loc=snaps[cut]
    J=[5,35,90,93,96,97,109,110];E=[31,32,55,56,57,58];W=sorted(J+E);isolates=[5,35,90,93]
    labels={96:(0,4),97:(1,4),109:(2,4),110:(3,4),31:(2,3),32:(0,1),55:(1,2),56:(0,2),57:(1,3),58:(0,3)}
    insist(set(labels.values())==set(combinations(range(5),2)),'bijection of actual ten roles to all pairs')
    actual={}
    for i in W:
        visible=set()
        for name,v in values.items():
            if subset(C[loc[name]],C[f'F{i}']):visible|=set(v)&set(W)
        want={j for j in W if i in labels and j in labels and set(labels[i]).isdisjoint(labels[j])}
        insist(visible==want,('actual nonlinear cut sideinformation',i));actual[i]=sorted(visible)
    insist(set(W)<=set(range(111))-set(w['targets']),'all14 demands unfinished')
    return {'word_sha256':sha(path),'source_sha256':sha(src),'cut':cut,'witness':W,'isolates':isolates,'pair_labels':labels,'actual_neighbor_sets':actual,'full_native_replay_and_lifetimes':True}

def main():
    p=argparse.ArgumentParser();p.add_argument('--dual',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--evidence',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();d=json.loads(a.dual.read_text())
    dual=expanded_dual(d);graph=graph_check(a.repo,a.evidence);controls=[]
    for label in ['negative_multiplier','false_decode','wrong_rhs','dropped_term']:
        bad=copy.deepcopy(d)
        if label=='negative_multiplier':bad['terms'][0]['multiplier']='-1'
        elif label=='false_decode':next(r for r in bad['terms']if r['inequality'][0]=='decode')['inequality'][1]=0
        elif label=='wrong_rhs':bad['terms'][0]['rhs']=-11
        else:bad['terms'].pop()
        try:expanded_dual(bad)
        except ValueError as exc:controls.append({'control':label,'rejected':str(exc)})
        else:raise ValueError('invalid dual accepted')
    result={'status':'PASS_INDEPENDENT_EXPANDED_NONLINEAR_PETERSEN_GATE','dual_sha256':sha(a.dual),'expanded_dual':dual,'actual_graph':graph,'negative_controls':controls,'scope':'Fixed schedule, deterministic zero-error, finite whole-record alphabet, all non-witness inputs fixed. Arbitrary nonlinear co-chart processing. Nine future whole-record descents after this exact cut; no uncharged schedule channel.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'NONLINEAR-REVIEW-RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status']);print(dual)
if __name__=='__main__':main()
