#!/usr/bin/env python3
"""Independent exact compact Toffoli interpreter, written from retained primitives."""
import argparse, itertools, json, random
from collections import Counter
from pathlib import Path


def program(f, K, G, rho=0):
    n=f-1; B=1<<G; js=[rho+i*K for i in range(n)]
    def digit(s,v,i):return (s[v]>>(i*G))&(B-1)
    def q(s,i):return (digit(s,'u',i)&1)*(digit(s,'v',i)&1)
    def pack(s,v):return sum(((s[v]>>j)&1)<<(i*G) for i,j in enumerate(js))
    ops=[]
    def swap(a,b):ops.append(('swap',a,b))
    def rotate(v,controls,fun):ops.append(('rotate',v,tuple(controls),fun))
    def earlier():
        rotate('y',('u','v','t'),lambda s:sum(2*q(s,i)*digit(s,'t',i)*(1<<j) for i,j in enumerate(js)))
        swap('t','b')
        rotate('b',('y',),lambda s:pack(s,'y'))
        swap('t','b')
        rotate('y',('u','v','t'),lambda s:sum(q(s,i)*(1-2*digit(s,'t',i))*(1<<j) for i,j in enumerate(js)))
        swap('t','b')
        rotate('b',('u','v','y'),lambda s:-sum((((s['y']>>j)&1)^q(s,i))<<(i*G) for i,j in enumerate(js)))
        swap('t','b')
    def load(v,source,sign):
        swap(v,'b');rotate('b',(source,),lambda s:sign*pack(s,source));swap(v,'b')
    earlier();load('u','x',1);earlier();load('v','z',1)
    earlier();load('u','x',-1);earlier();load('v','z',-1)
    widths={'u':n*G,'v':n*G,'t':n*G,'b':n*G,'x':f*K,'y':f*K,'z':f*K}
    masks={v:(1<<w)-1 for v,w in widths.items()}
    def apply(s, inverse=False, omit=None):
        s=s.copy()
        chosen=list(enumerate(ops))
        if inverse:chosen.reverse()
        for i,o in chosen:
            if i==omit:continue
            if o[0]=='swap':s[o[1]],s[o[2]]=s[o[2]],s[o[1]]
            else:s[o[1]]=(s[o[1]]+(-1 if inverse else 1)*o[3](s))&masks[o[1]]
        return s
    def ideal(s):
        s=s.copy()
        for j in js:s['y']^=(((s['x']>>j)&1)*((s['z']>>j)&1))<<j
        return s
    def bad(s):
        return any(digit(s,v,i)==B-1 for v in ['u','v','t'] for i in range(n)) or any(not(2*B<=((s['y']>>j)&((1<<K)-1))//2<(1<<(K-1))-2*B)for j in js)
    for order in itertools.permutations(['x','y','z']):
        layout=['u','v','t',*order,'b']
        for o in ops:
            if o[0]=='rotate':
                assert o[1] not in o[2]
                assert all(layout.index(c)<layout.index(o[1])for c in o[2])
    return ops,widths,apply,ideal,bad


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    total=good=badcount=actual_bad_diff=0
    profiles=set();inverse_cases=0;repair_cases=0
    # Exhaust the complete transformed rectangle for n=1, including every
    # target bit and all arbitrary dirty fields. Source irrelevant bits are
    # untouched spectators; the four low control pairs exhaust their action.
    ops,widths,apply,ideal,bad=program(2,5,1)
    names=['u','v','t','b','y']
    for x,z in itertools.product(range(2),repeat=2):
        images=set();repair_images=set()
        for vals in itertools.product(range(2),range(2),range(2),range(2),range(1024)):
            s=dict(zip(names,vals))|{'x':x,'z':z}
            out=apply(s);want=ideal(s);isbad=bad(s)
            assert apply(out,True)==s
            assert bad(out)==isbad
            if not isbad:assert out==want;good+=1
            else:
                badcount+=1;actual_bad_diff+=out!=want
                repaired=ideal(apply(out,True))
                assert repaired==want and bad(repaired)
                repair_images.add(tuple(repaired[k]for k in names));repair_cases+=1
            images.add(tuple(out[k]for k in names));total+=1;inverse_cases+=1
        assert len(images)==2**14
        assert len(repair_images)==sum(bad(dict(zip(names,v))|{'x':x,'z':z})for v in itertools.product(range(2),range(2),range(2),range(2),range(1024)))
    rng=random.Random(0x00515)
    mutants={}
    # Extreme rho, compact carry boundaries, multi-digit carries, and three
    # independent control layouts. The universal proof is still the digit
    # identity and invariant-set repair, not this finite sample.
    for f,K,G,rho in [(3,6,1,0),(3,7,2,6),(4,8,2,7),(2,8,3,7),(5,10,3,9)]:
        ops,widths,apply,ideal,bad=program(f,K,G,rho)
        counts=Counter(o[0]for o in ops);profiles.add((counts['swap'],counts['rotate']))
        n=f-1;B=1<<G
        for index in range(2048):
            s={v:rng.randrange(1<<w)for v,w in widths.items()}
            if index%2==0:
                for v in ['u','v','t']:s[v]=sum(rng.randrange(B-1)<<(i*G)for i in range(n))
                for i in range(n):
                    j=rho+i*K;seg=(rng.randrange(2*B,(1<<(K-1))-2*B)<<1)|rng.randrange(2)
                    s['y']=(s['y']&~(((1<<K)-1)<<j))|(seg<<j)
            out=apply(s);want=ideal(s);isbad=bad(s)
            assert apply(out,True)==s and bad(out)==isbad
            if not isbad:
                assert out==want;good+=1
                for mi in [0,8,11,19,22,30,33,41]:
                    if mi not in mutants and apply(s,omit=mi)!=want:mutants[mi]={'f':f,'K':K,'G':G,'rho':rho,'state':s}
            else:badcount+=1;actual_bad_diff+=out!=want
            total+=1;inverse_cases+=1
    assert profiles=={(24,20)}
    assert actual_bad_diff>0 and len(mutants)==8
    # The raw two-source dirty-control parity identity holds on all16 inputs.
    for u,v,x,z in itertools.product(range(2),repeat=4):
        assert (u*v)^((u^x)*v)^((u^x)*(v^z))^(u*(v^z))==x*z
    result={'status':'PASS_INDEPENDENT_COMPACT_TOFFOLI',
            'exact_small_rectangle_cases':65536,'total_cases':total,
            'good_cases':good,'bad_cases':badcount,
            'bad_cases_needing_repair':actual_bad_diff,
            'inverse_cases':inverse_cases,'exact_bad_repair_cases':repair_cases,
            'swap_rotation_counts':[24,20],
            'all_six_source_target_orders_verified':True,
            'omission_negative_controls':mutants,
            'scope':'Checks literal address permutation, inverses, good-set identity and exact repair keys; asymptotic physical cost requires retained primitive and reservation proof review.'}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k!='omission_negative_controls'}))

if __name__=='__main__':main()
