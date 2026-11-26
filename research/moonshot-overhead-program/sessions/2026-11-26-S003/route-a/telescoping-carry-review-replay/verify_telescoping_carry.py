#!/usr/bin/env python3
"""Formal coefficient comparison and actual unfolded-length checks."""
from pathlib import Path
from itertools import product
from functools import lru_cache
import importlib.util
import hashlib
import json
import sys

path=Path(__file__).with_name('verify_p_power_count_compiler.py')
spec=importlib.util.spec_from_file_location('count_compiler',path)
cc=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=cc
spec.loader.exec_module(cc)

def add(a,b,p):
    out=a.copy()
    for monomial,value in b.items():
        out[monomial]=(out.get(monomial,0)+value)%p
        if not out[monomial]:del out[monomial]
    return out

def mul(a,b,p):
    out={}
    for x,c in a.items():
        for y,d in b.items():
            monomial=tuple(i+j for i,j in zip(x,y))
            out[monomial]=(out.get(monomial,0)+c*d)%p
            if not out[monomial]:del out[monomial]
    return out

def run():
    report=dict(formal_polynomials=0,formal_nonzero_coefficients=0,
                ordinary_digit_values=0,checked_additions=0,
                negative_controls=0,profiles=[])
    for p in [2,3,5,7]:
        n=p+1
        f=cc.Formula(p)
        variables=[f.var(j) for j in range(n)]
        terms=[]
        for j in range(1,n):
            prefix=f.add(variables[:j],1)
            terms += [f.mul([f.binom(prefix,a,1),f.binom(variables[j],p-a,1)])
                      for a in range(1,p)]
        root=f.add(terms,p)
        assert root.length==p and root.size<=8*p**4
        report['checked_additions']+=cc.structural_check(root,p,p)
        zero=(0,)*n
        @lru_cache(None)
        def expand(node):
            if node.op=='const':return {zero:node.value} if node.value else {}
            if node.op=='var':
                exponent=list(zero);exponent[node.value]=1
                return {tuple(exponent):1}
            if node.op=='scale':
                return {key:value*node.value%p for key,value in expand(node.args[0]).items()
                        if value*node.value%p}
            value={} if node.op=='add' else {zero:1}
            operation=add if node.op=='add' else mul
            for arg in node.args:value=operation(value,expand(arg),p)
            return value
        actual=expand(root)
        # Independent formal definition; its reference circuit is not the
        # formula whose size and factor budgets are being claimed.
        states=[{} for _ in range(p+1)];states[0]={zero:1}
        for variable in variables:
            binomials=[expand(f.binom(variable,a,1)) for a in range(p)]
            new=[{} for _ in range(p+1)]
            for degree in range(p+1):
                for a in range(min(p-1,p-degree)+1):
                    new[degree+a]=add(new[degree+a],mul(states[degree],binomials[a],p),p)
            states=new
        assert actual==states[p]
        report['formal_polynomials']+=1
        report['formal_nonzero_coefficients']+=len(actual)
        assignments=(list(product(range(p),repeat=n)) if p<=3 else
                     [tuple((seed*(j+1)+j*j)%p for j in range(n)) for seed in range(5*p)] +
                     [tuple(min(p-1,max(0,total-j*(p-1))) for j in range(n))
                      for total in range(p*p)])
        for values in assignments:
            assert f.evaluator(values)(root)==sum(values)//p
            report['ordinary_digit_values']+=1
        ones=(1,)*n
        assert f.evaluator(ones)(root)==1
        assert cc.generalized_binom(sum(ones)%p,p)%p==0
        adjacent=sum(sum(cc.generalized_binom(ones[j-1],a)*
                            cc.generalized_binom(ones[j],p-a)
                            for a in range(1,p)) for j in range(1,n))%p
        assert adjacent!=1
        report['negative_controls']+=2
        report['profiles'].append(dict(p=p,unfolded_nodes=root.size,
                                       addition_budgets=[1,p],root_length=root.length))
    return report

if __name__=='__main__':
    result=dict(status='passed',checks=run(),
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                dependency_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                scope='Formal finite prime-ary carry formula and actual budgets; no complete physical compiler.')
    Path(__file__).with_name('telescoping-carry-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
