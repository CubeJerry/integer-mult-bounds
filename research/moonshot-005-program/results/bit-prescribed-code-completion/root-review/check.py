"""Independent source reconstruction and exact completion/feedback audit."""
from pathlib import Path
from collections import Counter
import argparse, hashlib, itertools, json

def basis(rows):
    out={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in out:x^=out[p]
            else:out[p]=x;break
    return list(out.values())
def rank(rows):return len(basis(rows))
def span(rows):
    s=[0]
    for x in basis(rows):s += [y^x for y in s]
    return s
def contains(rows,x):return rank(rows+[x])==rank(rows)
def mask(indices):return sum(1<<j for j in indices)
def load(path):return json.loads(path.read_text())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--seed',type=Path,required=True);p.add_argument('--closure',type=Path,required=True)
    p.add_argument('--threshold',type=Path,required=True);p.add_argument('--completion',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();seed=load(a.seed);native=a.repo/seed['native_source_path']
    assert digest(native)=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
    roots=load(native)['native_roots'];n=len(roots);assert n==111
    dot=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))
    local=[mask(j for j in range(n) if dot(i,j)==0) for i in range(n)]
    allbits=(1<<n)-1;nonlocal_masks=[allbits^v for v in local]
    canonical=[v^(1<<i) for i,v in enumerate(local)];assert rank(canonical)==9
    h=seed['h_values'];hraw=[int((i!=72 and dot(72,i)!=0)^(sum(x*y for x,y in zip([0,0,1,1,0,0,1,-1],r))!=0)) for i,r in enumerate(roots)]
    assert h==hraw
    fitting=[canonical[i]&mask(j for j in range(n) if h[j]==h[i]) for i in range(n)]
    S=[fitting[i] for i in [1,3,4,6,73,74,77,78]]
    supplied=[int(x,16) for x in seed['seed_rows']]
    assert rank(S)==rank(supplied)==rank(S+supplied)==8 and rank(fitting)==15
    P0=[1,6,73,75,77,79]
    Z=[1,3,4,6,18,21,61,64,65,73,74,75,76,77,78,79,80]
    def fit(B):return [i for i in range(n) if contains([v&nonlocal_masks[i] for v in B],1<<i)]
    assert fit(S+[1<<j for j in P0])==Z
    assert fit(S+[1<<j for j in Z])==Z
    assert rank(S+[1<<j for j in P0])==14 and rank(S+[1<<j for j in Z])==25
    closure=load(a.closure);assert closure['closed_point_set']==Z
    for w in closure['dual_witnesses']:
        i=w['receiver'];u=int(w['annihilator_hex'],16)
        assert u==mask(w['annihilator_support']) and u>>i&1
        assert not(u&mask(Z)) and not(u&local[i])
        assert all((u&s).bit_count()%2==0 for s in S)
    assert len(closure['dual_witnesses'])==94
    threshold=load(a.threshold);code=span(S);mins={};hist=[Counter(),Counter()]
    for rec in threshold['all94_exact_activation_records']:
        i=rec['receiver'];candidates=[s for s in code if s>>i&1]
        costs=[(s&nonlocal_masks[i]&~mask(Z+[i])).bit_count() for s in candidates]
        d=min(costs) if costs else None;mins[i]=d
        assert d==rec['minimum_external_points']
        if d is not None:
            assert len(rec['witness_points'])==d
            assert i in fit(S+[1<<j for j in Z+rec['witness_points']])
            hist[h[i]][d]+=1
    assert [i for i,d in mins.items() if d is None]==[19,20]
    assert [min(x) for x in hist]==[5,7]
    assert all(not(s&mask([19,20])) for s in S)
    S0=[s for s in code if not(s&mask(i for i in range(n) if h[i]))]
    S1=[s for s in code if not(s&mask(i for i in range(n) if not h[i]))]
    assert rank(S0)==rank(S1)==4
    points=sorted(Z+[26,34,35,47,72])
    while True:
        nxt=fit(S+[1<<j for j in points])
        if nxt==points:break
        points=nxt
    assert points==threshold['five_point_attainment_example']['closed_set'] and len(points)==24
    I=[0,14,22,23,30,31,59,60];lam=mask([0,24,32]);restriction=mask(I)
    assert all(dot(i,j)!=0 for i in I for j in I)
    assert not(restriction&mask(Z));assert rank([s&restriction for s in S])==4
    source_row=int('cc00cc6400097c0033000055',16)
    assert contains(S,source_row) and source_row&restriction==1
    assert not(lam&local[0]) and not(lam&mask(Z))
    assert all((s&lam).bit_count()%2==0 for s in S)
    for P in [[],P0,Z]:
        B=S+[1<<j for j in P]
        assert rank(B)+9-rank(B+canonical)==4
    completion=load(a.completion);S6=[fitting[i] for i in [3,76,80,4,74,78]]
    cases={'S8':S,'S8_plus_E6':S+[1<<j for j in P0],'S8_plus_all17_feedback':S+[1<<j for j in Z],
           'S6':S6,'S6_plus_E6':S6+[1<<j for j in P0],'S6_plus_all17_feedback':S6+[1<<j for j in Z]}
    assert set(cases)==set(completion['cases']);blockers=0
    for name,B in cases.items():
        rec=completion['cases'][name];constraints=[]
        assert rec['served']==fit(B)
        for c in rec['constraint_basis']:
            i=c['receiver'];v=int(c['row'],16)
            assert not(v&local[i]) and not(v>>i&1)
            assert all((v&s).bit_count()%2==0 for s in B)
            constraints.append(v)
        assert rank(constraints)==n-rank(B)
        for d in rec['blocking_witnesses']:
            i=d['receiver'];v=int(d['annihilator'],16);total=0
            for j in d['constraint_sum']:total^=constraints[j]
            assert total==v and v>>i&1 and not(v&local[i])
            assert all((v&s).bit_count()%2==0 for s in B);blockers+=1
        quotient=[int(x,16) for x in rec['canonical_quotient_rows']]
        assert rank(B+quotient)==rank(B)+len(quotient) and rank(B+quotient+canonical)==rank(B+quotient)
        forced=[]
        for d in rec['canonical_receiver_spaces']:
            if d['allowed_dimension']!=1 or len(d['good_directions'])!=1:continue
            i=d['receiver'];m=d['good_directions'][0];possible=[]
            for m2 in range(1,1<<len(quotient)):
                q2=0
                for k,row in enumerate(quotient):
                    if m2>>k&1:q2^=row
                if contains([v&nonlocal_masks[i] for v in B+[1<<i]],q2&nonlocal_masks[i]):possible.append(m2)
                if m2==m:assert contains([v&nonlocal_masks[i] for v in B+[q2]],1<<i)
            assert possible==[m];forced.append(m)
        assert rank(forced)==len(quotient)
    assert blockers==574
    J=[i for i in range(n) if not h[i] and i not in Z]
    assert len(J)==41 and rank([c&mask(J) for c in canonical])==8
    assert rank([s&mask(J) for s in S])==4 and rank([s&mask(J) for s in S6])==3
    hrow=mask(i for i in range(n) if h[i]);assert contains(canonical,hrow) and hrow>>19&1
    # Independent restricted-family check over F2 at V=1.
    fibers={}
    for u in itertools.product(range(2),repeat=8):
        for t in range(2):
            x=[0]*n
            for i,v in zip(I,u):x[i]=v
            for i in [0,24,32]:x[i]^=t
            b=tuple(sum(x[j] for j in range(n) if s>>j&1)%2 for s in S)
            value=sum(x[j] for j in range(n) if source_row>>j&1)%2
            assert value==u[0] and all(x[j]==0 for j in range(n) if local[0]>>j&1)
            assert all(x[j] in (0,t) for i in I[1:] for j in range(n) if local[i]>>j&1)
            fibers[b]=fibers.get(b,0)+1
    assert len(fibers)==16 and set(fibers.values())=={32}
    controls={'missing_own_lambda':not((lam^1)&1),'extra_free_point24':bool(lam&(1<<24)),
              'extra_local_point24':bool(lam&(local[0]|(1<<24))),
              'wrong_lambda_without32':any((s&(lam^(1<<32))).bit_count()%2 for s in S),
              'raw_grant_outside_closure':0 in fit(S+[1<<j for j in Z+[0]])}
    assert all(controls.values())
    out={'status':'PASS_INDEPENDENT_S8_COMPLETION_AND_FEEDBACK_REVIEW','native_sha256':digest(native),
         'seed_sha256':digest(a.seed),'closure_sha256':digest(a.closure),'threshold_sha256':digest(a.threshold),
         'closed_set':Z,'dual_witnesses':94,'activation_thresholds':[5,7],'mandatory_points':[19,20],
         'point_grants_lower_bound':14,'frame':I,'restriction_rank':4,'lambda_support':[0,24,32],
         'completion_dual_blockers':blockers,'canonical_envelope_forced_lines':True,'gauge_restriction_coordinates':J,
         'exact_linear_added_dimension_per_width':5,'nonlinear_F2_family_size':512,
         'nonlinear_F2_baseline_values':16,'nonlinear_F2_fiber_size':32,'scope_controls':controls,
         'new_complete_kappa':False}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])

if __name__=='__main__':main()
