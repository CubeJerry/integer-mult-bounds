#!/usr/bin/env python3
"""Independent finite controls for the universal quotient proof and seed gate."""
import argparse, copy, importlib.util, itertools, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('review',HERE/'check_independent.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)

def vectors(S):return [i for i in range(8)if S>>i&1]
def span(vs):
    out={0}
    for v in vs:out|={a^v for a in list(out)}
    return sum(1<<a for a in out)
def dim(S):return S.bit_count().bit_length()-1
def inside(A,B):return A&B==A
def add(A,B):return span(vectors(A)+vectors(B))

def quotient_control():
    spaces=sorted({span(S)for k in range(4)for S in itertools.combinations(range(1,8),k)})
    assert len(spaces)==16
    checked=feasible=0;counterexample=None
    for D,W,N,E in itertools.product(spaces,repeat=4):
        if not inside(N,D):continue
        n=dim(N);r=dim(add(D,W))-dim(D);k=dim(N&E)
        z=dim(E&add(D,W))-dim(E&D)
        for q in range(4):
            checked+=1
            good=[T for T in spaces if dim(T)<=q and inside(N,T)and inside(W,add(D,T))]
            actual=max((dim(T&E)for T in good),default=None)
            expected=None if q<n+r else min(dim(E),k+z+q-n-r)
            assert actual==expected,(D,W,N,E,q,actual,expected)
            if good:feasible+=1
            bad=None if q<n+r else min(dim(E),z+q-r)
            if counterexample is None and actual is not None and bad!=actual:
                counterexample={'D':vectors(D),'W':vectors(W),'N':vectors(N),'E':vectors(E),'q':q,'actual_maximum':actual,'incorrect_without_N_kernel_term':bad}
    assert counterexample is not None
    return {'ambient':'F2^3','all_subspaces':16,'all_valid_D_W_N_E_q_cases':checked,
            'feasible_cases':feasible,'omitting_N_kernel_term_rejected_by':counterexample,
            'scope':'finite control; universal statement follows from the written rank-nullity/lifting proof'}

def row_history(w):
    values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
    places={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    history=[];terminal=None
    for step,op in enumerate(w['operations'],1):
        kind,n,*rest=op
        if kind=='INIT':values[n]=0;places[n]=rest[0]
        elif kind=='ADD':values[rest[0]]^=values[n]
        elif kind=='MOVE':places[n]=rest[0]
        elif kind=='CLEAR':del values[n];del places[n]
        for i in range(8):
            name=f'P{i}'
            if name in values and places[name]!='Hub':history.append(values[name])
        if step==w['markers']['handoff']:terminal=[values[f'P{i}']for i in range(8)]
    for i in range(111):
        assert values[f'X{i}']==1<<i
        assert values[f'Y{i}']==(1<<(111+i))^((1<<i)if i in[9,17,34]else 0)
    return history,terminal

def sixth_canonical_control(repo,package):
    roots=json.loads((repo/c.ROOT_PATH).read_text())['native_roots']
    omitted=[0,0,1,1,0,0,1,-1]
    h=[(c.dot(roots[72],r)//2+c.dot(omitted,r)//2)%2 for r in roots]
    C=[sum(1<<j for j,r in enumerate(roots)if j==i or c.dot(r,roots[i])==0)for i in range(111)]
    W=[row&sum(1<<j for j in range(111)if h[j]==h[i])for i,row in enumerate(C)]
    word=copy.deepcopy(json.loads((package/'WORD.json').read_text()))
    target=C[5];seed=target^int(word['proper_mode_rows_hex'][6],16)
    old=word['operations'];a=old.index(['INIT','P6','Hub'])+1;b=a
    while b<len(old)and old[b][0]=='ADD'and old[b][2]=='P6'and old[b][1].startswith('X'):b+=1
    replacement=[['ADD',f'X{i}','P6']for i in c.support(seed)]
    word['operations']=old[:a]+replacement+old[b:];change=len(replacement)-(b-a)
    for name,count in word['markers'].items():
        assert count<=a or count>=b
        if count>=b:word['markers'][name]=count+change
    for name,index in word['exchange'].items():
        if name.endswith('_index')and index is not None and index>=b:word['exchange'][name]=index+change
    word['initial_seed_rows_hex'][6]=hex(seed)
    word['expected_owned_at_handoff']['P6']['value_hex']=hex(target)
    H,T=row_history(word);rank=lambda rows:len(c.binary_basis(rows))
    receipt={'actual_original_endpoints_preserved':True,'terminal_rank':rank(T),
             'terminal_C_intersection':rank(T)+9-rank(T+C),
             'history_W_intersection':rank(H)+15-rank(H+W),
             'scope':'correct original endpoints, but fails the explicitly retained full-W history contract'}
    assert receipt['terminal_rank']==8 and receipt['terminal_C_intersection']==6 and receipt['history_W_intersection']==14
    try:c.replay(word,roots)
    except ValueError as error:
        assert 'native W missing' in str(error),str(error)
        receipt['retained_W_reviewer_rejects']=str(error)
    else:raise AssertionError('sixth-canonical mutant incorrectly retained W15')
    return receipt

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    result={'status':'PASS_INDEPENDENT_SATURATED_QUOTIENT_CONTROLS',
            'universal_lemma_finite_control':quotient_control(),
            'sixth_canonical_source_control':sixth_canonical_control(a.repo,a.package),
            'new_complete_kappa':False}
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
