#!/usr/bin/env python3
"""Exact threshold graphs, spanning trees and shared-state invoices."""
from hashlib import sha256
from itertools import groupby, product
from math import factorial
from pathlib import Path
import json
import runpy
ROOT=Path(__file__).resolve().parent
h=runpy.run_path(str(ROOT/'ROUTING-verify-state-walk.py'))
cost=h['cost']

def C(L,h):return (h+1)**L-(h**L if L%2==0 else 0)

def formula(t,L):
    lam=((t+1)**L-(1-t)**L)//2
    return lam-C(L,t-1)+sum((1<<(t-1-h))*(C(L,h+1)-C(L,h)) for h in range(t-1))

def graph_case(t,L):
    q=1<<t; D=2+L*(q-2)
    states=[s for s in product(range(t+1),repeat=L) if sum(b!=0 for b in s)%2]
    N=len(states); parent=list(range(N)); sizes=[1]*N
    def root(v):
        while parent[v]!=v:
            parent[v]=parent[parent[v]]; v=parent[v]
        return v
    def merge(a,b):
        a,b=root(a),root(b)
        if a==b:return False
        if sizes[a]<sizes[b]:a,b=b,a
        parent[b]=a; sizes[a]+=sizes[b]; return True
    edges=sorted((cost(states[i],states[j],t),i,j) for i in range(N) for j in range(i))
    tree=[]; weight=0; threshold_groups=0; components=N
    for w,group in groupby(edges,key=lambda e:e[0]):
        for _,a,b in group:
            if merge(a,b):
                tree.append((a,b,w)); weight+=w; components-=1
                assert w&(w-1)==0
        high={b for b in range(1,t+1) if (1<<(t-b))>w}
        patterns={}; roots={}
        for i,s in enumerate(states):
            pattern=tuple(b if b in high else 0 for b in s); r=root(i)
            assert r not in roots or roots[r]==pattern
            assert pattern not in patterns or patterns[pattern]==r
            roots[r]=pattern; patterns[pattern]=r
        assert components==len(patterns)==C(L,len(high))
        threshold_groups+=1
        if components==1:break
    assert len(tree)==N-1 and weight==formula(t,L)
    adjacency=[[] for _ in states]
    for a,b,w in tree:adjacency[a].append((b,w)); adjacency[b].append((a,w))
    start=states.index((0,)*(L-1)+(t,)); path=[start]
    def walk(v,p):
        for z,w in adjacency[v]:
            if z==p:continue
            path.append(z); walk(z,v); path.append(v)
    walk(start,-1)
    assert len(path)==2*N-1 and path[-1]==start and len(set(path))==N
    traversal=sum(cost(states[a],states[b],t) for a,b in zip(path,path[1:]))
    assert traversal==2*weight
    F=2*D+8*weight
    B=1<<(L-1)
    gray=2*D+4*(B-1)+8*(q-2)*(N-B)//(t-1)
    return {'t':t,'L':L,'states':N,'complete_edges':len(edges),'threshold_groups':threshold_groups,
            'tree_edges':len(tree),'tree_weight':weight,'closed_visits':len(path),
            'tree_free_calls':F,'support_gray_free_calls':gray}

def main():
    parameters=[(2,L) for L in range(2,7)]+[(3,L) for L in range(2,5)]+[(4,L) for L in range(2,5)]+[(t,3) for t in range(5,9)]
    cases=[graph_case(t,L) for t,L in parameters]
    guards=0
    for t in range(2,81):
        q=1<<t
        for L in range(2,81):
            lam=((t+1)**L-(1-t)**L)//2; D=2+L*(q-2); M=formula(t,L)
            assert M>=lam-1
            assert M<=2*q*(1<<L)*factorial(L)<=2*q*(2*L)**L
            assert 2*D+8*M>=D+lam
            guards+=1
    assert C(2,1)==3 and C(2,1)!=(1+1)**2
    result={'status':'pass','scope':'Exact complete graphs of the declared state metric, threshold components, minimum spanning trees and closed traversals; parameter guards, not a full source pencil or tape multiplier.',
            'proof_sha256':sha256((ROOT/'ROUTING-STATE-TREE-SHARING.md').read_bytes()).hexdigest(),
            'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'state_helper_sha256':sha256((ROOT/'ROUTING-verify-state-walk.py').read_bytes()).hexdigest(),
            'cases':cases,'total_states':sum(c['states'] for c in cases),
            'total_complete_edges':sum(c['complete_edges'] for c in cases),
            'total_tree_edges':sum(c['tree_edges'] for c in cases),
            'total_closed_visits':sum(c['closed_visits'] for c in cases),
            'integer_guards':guards,
            'negative_controls':['counting all-high patterns at even L is rejected'],
            'first_visit_rule':'Each distinct state contributes once; repeat visits are basis transitions only.'}
    (ROOT/'ROUTING-state-tree-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('cases','scope')},indent=2))

if __name__=='__main__':main()
