#!/usr/bin/env python3
"""Fresh Q replay, different-prime ROW ranks, direct witness cross-check."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from hashlib import sha256
import gzip,json,math,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
P=65521
def check(x,label):
    if not x:raise ValueError(label)
def axpy(a,b,c):
    for j,v in b.items():
        z=a.get(j,F(0))+c*v
        if z:a[j]=z
        else:a.pop(j,None)
def main():
    start=time.monotonic();data=json.loads((HERE/'RESULT.json').read_bytes());raw=(ROOT/'reference/pr7481/WORD.json.gz').read_bytes()
    check(sha256(raw).hexdigest()==data['source_sha256']=='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9','source')
    w=json.loads(gzip.decompress(raw));n=w['public'];values=[{i:F(1)} for i in range(n)]+[None]*w['owned_fields'];location=w['initial'].copy()+[None]*w['owned_fields'];banks=defaultdict(list);lookup={};targets={}
    def observe(t,a,f):
        row=values[a].copy();banks[f].append((t,a,row));lookup[t,a,f]=row
    for a,f in enumerate(w['initial']):observe(-1,a,f)
    for t,e in enumerate(w['program']):
        op,a=e[:2]
        if op=='MOVE':
            check(location[a]==e[2] and values[a] is not None,'MOVE state');targets[t]=values[a].copy();location[a]=e[3];observe(t,a,e[3])
        elif op=='INIT':check(location[a] is None,'INIT state');values[a]={};location[a]=e[2]
        elif op=='CLEAR':check(a>=n and location[a]==e[2],'CLEAR state');values[a]=None;location[a]=None
        elif op=='SCALE':check(location[a]==e[3],'SCALE state');values[a]={j:v*F(e[2]) for j,v in values[a].items()}
        else:
            b=e[2];check(op in ['ADD','COPY'] and location[a]==location[b]==e[4],'contact state')
            if op=='COPY':check(not values[a],'COPY zero')
            axpy(values[a],values[b],F(e[3]))
    check(location==w['final']+[None]*w['owned_fields'] and len(targets)==6279,'complete source')
    check(all(P%d for d in range(2,math.isqrt(P)+1)),'distinct prime')
    inverses={};membership={h:set() for h in data['helpers_tested']};rank_sum=0;misses=0
    def residue(q):
        if q.denominator not in inverses:
            check(q.denominator%P,'denominator');inverses[q.denominator]=pow(q.denominator,P-2,P)
        return q.numerator*inverses[q.denominator]%P
    for f,bank in banks.items():
        basis={}
        for t,a,row in bank:
            v={j:residue(q) for j,q in row.items() if residue(q)}
            while v:
                p=min(v)
                if p not in basis:
                    inv=pow(v[p],P-2,P);basis[p]={j:q*inv%P for j,q in v.items()};break
                q=v[p]
                for j,r in basis[p].items():
                    z=(v.get(j,0)-q*r)%P
                    if z:v[j]=z
                    else:v.pop(j,None)
        check(len(basis)==len(bank),'independent ROW rank reaches rational row-count upper bound');rank_sum+=len(basis)
        for h in membership:
            v={h:1}
            for p in sorted(basis):
                if v.get(p):
                    q=v[p]
                    for j,r in basis[p].items():
                        z=(v.get(j,0)-q*r)%P
                        if z:v[j]=z
                        else:v.pop(j,None)
            if not v:membership[h].add(f)
            else:misses+=1
    witness_count=0;target_checks=[]
    for c in data['cases']:
        h=c['helper'];inside={d['frame'] for d in c['coframes'] if d['relation_in_final_span']};check(membership[h]==inside,'different-prime memberships agree')
        for d in c['coframes']:
            if not d['relation_in_final_span']:continue
            total={}
            for p in d['unique_expression']:
                o=p['observation'];axpy(total,lookup[o['event'],o['owner'],o['frame']],F(p['coefficient']))
            check(total=={h:F(1)},'direct fresh exact final-bank unit witness');witness_count+=1
        check([e for e,row in targets.items() if set(row)=={h}]==c['zero_MOVE_events'],'fresh exact all-zero MOVE list')
        for hit in c['hits']:
            residual=targets[hit['event']].copy()
            for p in hit['providers']:
                o=p['observation'];check(o['event']<hit['event'],'strict provider');axpy(residual,lookup[o['event'],o['owner'],o['frame']],-F(p['coefficient']))
            check(residual=={h:F(hit['relation_coefficient'])},'fresh exact target identity');target_checks.append(hit['event'])
    check(rank_sum==7780 and misses==5862 and witness_count==12 and len(target_checks)==6,'complete independent domain')
    out={'status':'PASS_FRESH_DISTINCT_PRIME_ROW_AND_EXACT_WITNESS_REVIEW','source_sha256':data['source_sha256'],'prime':P,'original_rank_sum':rank_sum,'coframe_unit_decisions':5874,'full_augmented_row_count_miss_certificates':misses,'exact_Q_unit_expressions':witness_count,'exact_Q_target_identities':target_checks,'seconds':time.monotonic()-start,'scope':'Separate implementation and distinct prime; fresh full Q rows, not saved target/history matrices. No physical construction or kappa claim.'}
    (HERE/'INDEPENDENT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
