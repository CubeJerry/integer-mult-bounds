#!/usr/bin/env python3
"""Finite exact basis-walk, intersection and invoice checks."""
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import comb, isqrt
from pathlib import Path
import json
import runpy
ROOT=Path(__file__).resolve().parent
h=runpy.run_path(str(ROOT/'ROUTING-verify-destination-gauge.py'))
rank=h['rank']; subspaces=h['subspaces']; perpendicular=h['perpendicular']; representatives=h['representatives']; parity=h['parity']

def basis(U,d):
    result=[]
    for c in representatives(U,d):
        for xi in representatives(perpendicular(U,d),d):
            col=[0]*(1<<d)
            for u in U:col[c^u]=(-1)**parity(xi&u)
            result.append(col)
    return result

def transition_bases():
    pairs=entries=nonzero=0
    for d in range(1,5):
        spaces=subspaces(d); cache={U:basis(U,d) for U in spaces}
        for U,V in product(spaces,repeat=2):
            intersection=len(set(U)&set(V))
            support_size=len(U)*len(V)//(intersection*intersection)
            for source in cache[U]:
                values=[sum(a*b for a,b in zip(destination,source)) for destination in cache[V]]
                assert sum(value!=0 for value in values)==support_size
                assert all(Fraction(value*value,len(U)*len(V))==Fraction(1,support_size) for value in values if value)
                entries+=len(values); nonzero+=support_size
            pairs+=1
    return {'subspace_pairs':pairs,'matrix_entries':entries,'nonzero_entries':nonzero}

def span_basis(rows):
    pivots={}
    for row in rows:
        while row:
            bit=row.bit_length()-1
            if bit not in pivots:pivots[bit]=row; break
            row^=pivots[bit]
    return tuple(pivots.values())

def letter_set(letter,b,t,source):
    if b==0:return (letter,)
    width=t-b; size=1<<width; prefix=letter>>width
    if source:prefix^=1
    return tuple((prefix<<width)+a for a in range(size))

def cost(s,z,t):
    if s==z:return 0
    a=lambda b:1 if b==0 else 1<<(t-b)
    return 1+sum(max(a(x),a(y))-1 for x,y in zip(s,z) if x!=y)

def gray(t,j):
    if j==0:return [()]
    suffix=gray(t,j-1); result=[]
    for i,b in enumerate(range(t,0,-1)):
        result.extend((b,)+s for s in (suffix if i%2==0 else reversed(suffix)))
    return result

def gray_walk(t,L):
    walk=[]; processed=[]
    for mask in range(1,1<<L):
        if mask.bit_count()%2==0:continue
        support=[i for i in range(L) if (mask>>i)&1]
        forward=[]
        for local in gray(t,len(support)):
            state=[0]*L
            for i,b in zip(support,local):state[i]=b
            forward.append(tuple(state))
        processed.extend(forward)
        walk.extend(forward+list(reversed(forward[:-1])))
    assert len(set(processed))==len(processed)
    return walk,processed

def span_checks():
    cases=[]; endpoint_ranks=adjacent_pairs=all_state_pairs=0
    for t,L in ((1,2),(1,3),(1,4),(1,5),(1,6),(2,2),(2,3),(2,4),(3,2),(3,3),(4,2)):
        q=1<<t; D=2+L*(q-2)
        words=list(product(range(q),repeat=L)); lookup={w:i for i,w in enumerate(words)}
        gram=[sum(1<<j for j,v in enumerate(words) if sum(a!=b for a,b in zip(w,v))%2==0) for w in words]
        states=[s for s in product(range(t+1),repeat=L) if sum(b!=0 for b in s)%2]
        lam=((1+t)**L-(1-t)**L)//2; assert len(states)==lam
        sizes={s:tuple(1 if b==0 else 1<<(t-b) for b in s) for s in states}
        state_rank={s:1+sum(a-1 for a in sizes[s]) for s in states}
        exact=4 if q==2 else q+2*(D-1)+4*sum(cost(s,z,t) for s,z in zip(states,states[1:]))
        gpath,processed=gray_walk(t,L)
        assert set(processed)==set(states)
        B=1<<(L-1)
        gray_exact=4 if q==2 else 2*D+4*(B-1)+8*(q-2)*(lam-B)//(t-1)
        if q>=4:assert 2*D+4*sum(cost(s,z,t) for s,z in zip(gpath,gpath[1:]))==gray_exact
        for number,w in enumerate(words):
            cache=[]
            for source in (True,False):
                mapping={}
                for s in states:
                    side=product(*(letter_set(letter,b,t,source) for letter,b in zip(w,s)))
                    rows=span_basis(gram[lookup[v]] for v in side)
                    assert len(rows)==state_rank[s]
                    mapping[s]=rows; endpoint_ranks+=1
                cache.append(mapping)
            total=2*state_rank[states[0]]+2*(D-state_rank[states[-1]])
            pairs=list(product(states,repeat=2)) if number==0 else list(zip(states,states[1:]))
            for s,z in pairs:
                ds=2*rank(cache[0][s]+cache[0][z])-len(cache[0][s])-len(cache[0][z])
                dd=2*rank(cache[1][s]+cache[1][z])-len(cache[1][s])-len(cache[1][z])
                expected_d=sum(abs(a-b) for a,b in zip(sizes[s],sizes[z]))
                expected_s=0 if q==2 or s==z else 2+sum(a+b-2 for i,(a,b) in enumerate(zip(sizes[s],sizes[z])) if s[i]!=z[i])
                assert ds==expected_s and dd==expected_d
                if number==0:all_state_pairs+=1
                else:adjacent_pairs+=1
            for s,z in zip(states,states[1:]):
                ds=2*rank(cache[0][s]+cache[0][z])-len(cache[0][s])-len(cache[0][z])
                dd=2*rank(cache[1][s]+cache[1][z])-len(cache[1][s])-len(cache[1][z])
                total+=2*(ds+dd)
            assert total==exact
            gray_total=2*D
            for s,z in zip(gpath,gpath[1:]):
                ds=2*rank(cache[0][s]+cache[0][z])-len(cache[0][s])-len(cache[0][z])
                dd=2*rank(cache[1][s]+cache[1][z])-len(cache[1][s])-len(cache[1][z])
                gray_total+=2*(ds+dd)
            assert gray_total==gray_exact
        assert exact<=20*q*(t+1)**(L-1)
        derivative=sum(j*comb(L,j)*t**(j-1) for j in range(1,L+1,2))
        mu=lam+(q-1-t)*derivative
        cases.append({'t':t,'L':L,'D':D,'labels':len(words),'states':lam,
                      'old_free_calls':2*D*lam,'destination_free_calls':4*mu-2*lam+2*(D-1),
                      'walk_free_calls':exact,'gray_free_calls':gray_exact,'gray_visits':len(gpath),
                      'safe_walk_bound':20*q*(t+1)**(L-1)})
    return {'cases':cases,'endpoint_ranks':endpoint_ranks,'adjacent_pairs':adjacent_pairs,'all_state_pairs':all_state_pairs}

def walk_arithmetic():
    lex_checks=log_guards=0
    for t in range(1,7):
        q=1<<t
        for L in range(2,7):
            all_states=list(product(range(t+1),repeat=L))
            odd=[s for s in all_states if sum(b!=0 for b in s)%2]
            full=sum(cost(s,z,t) for s,z in zip(all_states,all_states[1:]))
            sub=sum(cost(s,z,t) for s,z in zip(odd,odd[1:]))
            assert full==Fraction((3*q//2-2)*((t+1)**L-1),t)
            assert sub<=full
            lex_checks+=1
    for a in range(4,11):
        x=1<<a; m=1<<x; target=isqrt(x*a)//2
        for L in range(2,41):
            for t in (2,3,4,6,8,12,16,24,32,48,64):
                q=1<<t; D=2+L*(q-2)
                lam=((1+t)**L-(1-t)**L)//2
                J=Fraction(D+lam)+Fraction(m*D*comb(L,L//2),q**((L+1)//2))
                assert J>=1<<target
                log_guards+=1
    return {'lexicographic_variation_checks':lex_checks,'rounded_logarithmic_bound_checks':log_guards}

def main():
    transitions=transition_bases(); spans=span_checks(); arithmetic=walk_arithmetic()
    result={'status':'pass','scope':'Exact partial-basis transition matrices, label span intersections, literal walk invoices and finite lower-bound guards; no physical timing or full multiplication execution.',
            'proof_sha256':sha256((ROOT/'ROUTING-STATE-WALK-SHARING.md').read_bytes()).hexdigest(),
            'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'helper_sha256':sha256((ROOT/'ROUTING-verify-destination-gauge.py').read_bytes()).hexdigest(),
            'basis_transitions':transitions,'span_checks':spans,'arithmetic':arithmetic,
            'negative_controls':['q=2 rejects the q>=4 source transition formula'],
            'gray_schedule':'Each state contributes only on its first forward visit; reverse visits only change bases, and the final endpoint is included.'}
    (ROOT/'ROUTING-state-walk-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'pass','basis_transitions':transitions,
                      'span_counts':{k:v for k,v in spans.items() if k!='cases'},'arithmetic':arithmetic},indent=2))

if __name__=='__main__':main()
