#!/usr/bin/env python3
"""Finite supplements to the any-field paired-encoder and alias proofs."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

def need(b,s):
    if not b: raise ValueError(s)

def inverse(a,p):
    n=len(a); z=[list(r)+[int(i==j) for j in range(n)] for i,r in enumerate(a)]
    for c in range(n):
        k=next((k for k in range(c,n) if z[k][c]%p),None)
        if k is None:return None
        z[k],z[c]=z[c],z[k];d=pow(z[c][c],-1,p);z[c]=[v*d%p for v in z[c]]
        for k in range(n):
            if k!=c:
                d=z[k][c];z[k]=[(v-d*w)%p for v,w in zip(z[k],z[c])]
    return [r[n:] for r in z]

def mv(a,x,p):return [sum(v*w for v,w in zip(r,x))%p for r in a]

def aliases(n,p):
    matrices=cases=assignments=0;valid=Counter()
    for flat in product(range(p),repeat=n*n):
        M=[list(flat[n*i:n*i+n]) for i in range(n)];inv=inverse(M,p)
        if inv is None:continue
        matrices+=1;dual=list(zip(*inv))
        for mask in range(1<<n):
            U=[i for i in range(n) if mask>>i&1];H=[i for i in range(n) if not mask>>i&1]
            criterion=all(M[i][j]==M[j][i]==0 for i in U for j in H) and all(sum(M[i][k]*M[j][k] for k in U)%p==int(i==j) for i in U for j in U)
            actual=True
            for v in product(range(p),repeat=2*n-len(U)):
                a=list(v[:n]);b=a.copy()
                for k,i in enumerate(H):b[i]=v[n+k]
                x,y=mv(M,a,p),mv(dual,b,p);assignments+=1
                if any(x[i]!=y[i] for i in U):actual=False;break
            need(actual==criterion,'alias theorem finite counterexample');cases+=1
            if actual:valid[len(U)]+=1
    return dict(field=p,dimension=n,invertible_matrices=matrices,interfaces=cases,input_assignments_until_decision=assignments,valid_by_size=dict(valid))

def span(basis):
    out={0}
    for b in basis:out|={v^b for v in out}
    return out

CHARTS=[[1],[2],[1,2],[1,2,4],[1,2,4,8]]
INITIAL=[0,1,0,1,3,3]
WORD=[['MOVE',0,0,2],['MOVE',1,1,2],['MOVE',2,0,2],['MOVE',3,1,2],['ADD',0,1,'1',2],['ADD',3,2,'-1',2],['MOVE',0,2,3],['MOVE',2,2,3],['ADD',4,0,'1',3],['ADD',2,5,'-1',3],['MOVE',0,3,4],['MOVE',2,3,4],['MOVE',1,2,4],['MOVE',3,2,4],['ADD',0,1,'-1',4],['ADD',3,2,'1',4]]

def execute(word):
    loc=INITIAL.copy();rows=[[F(i==j) for j in range(6)] for i in range(6)];ranks=Counter();counts=Counter()
    for e,o in enumerate(word):
        counts[o[0]]+=1
        if o[0]=='MOVE':
            _,j,s,t=o;need(loc[j]==s,'wrong MOVE source');need(span(CHARTS[s])<span(CHARTS[t]),'nonnested public route');loc[j]=t;ranks[len(CHARTS[t])-len(CHARTS[s])]+=1
        else:
            _,j,i,c,f=o;need(loc[j]==loc[i]==f,'missing actual cochart');rows[j]=[a+F(c)*b for a,b in zip(rows[j],rows[i])]
    return rows,loc,counts,ranks

def typed():
    out,loc,counts,ranks=execute(WORD);want=[[F(i==j) for j in range(6)] for i in range(6)];want[2][5]=want[3][5]=-1;want[4][0]=want[4][1]=1
    need(out==want and loc==[4,4,4,4,3,3],'complete six-input reciprocal map');need(counts=={'MOVE':10,'ADD':6} and ranks=={1:8,2:2},'complete recursive and ordinary profile')
    bad=[o.copy() for o in WORD];bad[5]=['ADD',2,3,'1',2];need(execute(bad)[0]!=want,'same-M mutant undetected')
    bad=[o.copy() for o in WORD];bad[-1][3]='-1';need(execute(bad)[0]!=want,'wrong inverse mutant undetected')
    failures=[]
    for bad in [[o.copy() for i,o in enumerate(WORD) if i!=7], [o.copy() for o in WORD]]:
        if len(bad)==len(WORD):bad[8][2]=1
        try:execute(bad)
        except ValueError as e:failures.append(str(e))
    need(failures==['missing actual cochart']*2,'route/availability mutants not rejected')
    return dict(independent_inputs=6,word=WORD,final_rows=[[str(x) for x in r] for r in out],counts=dict(counts),histogram=dict(ranks),direct_baseline={3:4},increment='8+2*2^t-4*3^t',negative_controls=['same M instead of inverse transpose','wrong hub inverse','omitted dual facet MOVE','read at unavailable donor chart'])

def main():
    result=dict(status='PASS_PAIRED_ENCODER_AND_EXACT_ALIAS_GATE',finite_checks=[aliases(3,2),aliases(2,3)],typed_example=typed(),scope='Proof is universal; finite checks supplement it. No complete supplier or kappa.')
    Path(__file__).with_name('PAIRED-INTERFACE-CHECK.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='typed_example'},indent=2))

if __name__=='__main__':main()
