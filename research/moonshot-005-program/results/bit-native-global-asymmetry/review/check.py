#!/usr/bin/env python3
"""Independent C review: geometric reconstruction and exact dual arithmetic."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction
from pathlib import Path

def reduce_rows(rows,n):
    rows=list(rows);piv=[];r=0
    for c in range(n):
        ix=next((i for i in range(r,len(rows)) if rows[i]>>c&1),None)
        if ix is None:continue
        rows[r],rows[ix]=rows[ix],rows[r]
        for i in range(len(rows)):
            if i!=r and rows[i]>>c&1:rows[i]^=rows[r]
        piv.append(c);r+=1
    return rows[:r],piv
def basis_null(rows,n):
    rr,piv=reduce_rows(rows,n)
    return [(1<<c)|sum((1<<p) for p,row in zip(piv,rr) if row>>c&1) for c in range(n) if c not in piv]
def rank(rows,n=4):return len(reduce_rows(rows,n)[0])
def span(basis):
    out={0}
    for x in basis:out|={y^x for y in out}
    return out
def lin(M,x):
    y=0
    for i,c in enumerate(M):
        if x>>i&1:y^=c
    return y
def projection(L,K):
    table={l^k:l for l in L for k in K}
    assert len(table)==16
    return [table[1<<i] for i in range(4)]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);pg=a.repo/'research/moonshot-005-program'
    lp=pg/'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';raw=gzip.decompress(lp.read_bytes())
    assert hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
    layout=json.loads(raw);roots=layout['root_table'];dots=[[sum(x*y for x,y in zip(u,v)) for v in roots] for u in roots]
    native_raw=(pg/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes()
    factor_raw=(pg/'results/bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json').read_bytes()
    assert hashlib.sha256(native_raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
    assert hashlib.sha256(factor_raw).hexdigest()=='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7'
    assert roots[:111]==json.loads(native_raw)['native_roots']
    increments=dict(json.loads(factor_raw)['factors'])
    assert all(dots[i][i]==4 for i in range(120))
    reconstructed=set()
    for i,j in itertools.combinations(range(120),2):
        s=dots[i][j]
        if not s:continue
        assert abs(s)==2
        H=tuple(k for k in range(120) if 48-4*dots[i][k]**2+2*s*dots[i][k]*dots[j][k]-4*dots[j][k]**2==0)
        assert len(H)==3;reconstructed.add(H)
    assert reconstructed==set(map(tuple,layout['A2'])) and len(reconstructed)==1120
    planes=[set(H) for H in layout['A2']];native=set(range(111));singletons=[(next(iter(H&native)),H) for H in planes if len(H&native)==1]
    assert len(singletons)==11
    ordinary={h for h,H in enumerate(planes) if len(H&native)>1}
    early=[]
    for h,H in enumerate(planes):
        m=len(H&native);x=12//m+increments.get(h,0) if m else 0;early.append(x)
        assert (not m and x==0) or (m==1 and x==12) or (m>=2 and max(8,x)==8)
    assert all(sum(45*early[h] for h,H in enumerate(planes) if j in H)==5760 for j in native)
    pair_flags={(h,j,k) for h in ordinary for j,k in itertools.combinations(sorted(planes[h]&native),2)}
    assert len(ordinary)==1108 and len(pair_flags)==2870
    own={};hist=Counter();details=[];tight_sets={}
    for i in range(111):
        F={j for j in range(120) if dots[i][j]==0};tight=(F&native)-{j for j,H in singletons if H<=F};tight_sets[i]=tight
        order=sorted(tight);position={j:t for t,j in enumerate(order)};visible=[h for h,H in enumerate(planes) if H<=F]
        assert all(len([h for h in visible if j in planes[h]])==16 for j in tight)
        matrix=[sum(1<<position[j] for j in planes[h]&tight) for h in visible]
        nb=basis_null(matrix,len(order));vectors=span(nb);assert len(vectors)==2**len(nb)
        odd=[v for v in vectors if v.bit_count()%2];hist[len(odd)]+=1
        for v in odd:
            S=tuple(order[t] for t in range(len(order)) if v>>t&1);ss=set(S);paired=[]
            for h in visible:
                cut=sorted(ss&planes[h]);assert len(cut) in (0,2)
                if cut:paired.append((h,*cut))
            assert len(paired) in (216,280) and 2*len(paired)==16*len(S)
            own[i,S]=paired
        details.append({'receiver':i,'tight_count':len(tight),'nullity':len(nb),'odd_count':len(odd)})
    assert len(own)==421
    committed=json.loads(gzip.decompress((a.author/'output/WITNESSES.json.gz').read_bytes()))['witnesses']
    assert len(committed)==len(own) and len({(w['receiver'],tuple(w['donors'])) for w in committed})==421
    for w in committed:
        assert own[w['receiver'],tuple(w['donors'])]==[(h,*jk) for h,jk in w['paired_planes']]
    certificates={}
    for name,pair in [('PLANE-DUAL.json',False),('PAIR-DUAL.json',True)]:
        cert=json.loads((a.author/name).read_text());D=cert['scale'];weights=cert['weights']
        assert isinstance(D,int) and D>0 and len(weights)==421 and all(type(w) is int and w>=0 for w in weights)
        loads=Counter();weighted_rank=Fraction()
        for w,u in zip(committed,weights):
            flags=own[w['receiver'],tuple(w['donors'])];m=len(flags)
            for flag in flags:loads[flag if pair else flag[0]]+=u
            weighted_rank+=Fraction(u*16*m,m-1)
        assert max(loads.values())<=D
        value=Fraction(17*sum(weights),D)
        certificates[name]={'weight_sum':sum(weights),'scale':D,'max_load':max(loads.values()),'count_bound':str(value),'integer_count_bound':(value.numerator+value.denominator-1)//value.denominator,'weighted_rank_bound_per_p':str(weighted_rank/D) if pair else None}
    assert certificates['PLANE-DUAL.json']['integer_count_bound']==71
    assert certificates['PAIR-DUAL.json']['integer_count_bound']==152
    rank_bound=Fraction(certificates['PAIR-DUAL.json']['weighted_rank_bound_per_p']);assert rank_bound==Fraction(134487693944,937265625)
    lpair=Counter(flag for (i,S),flags in own.items() if i==80 for flag in flags)
    assert Counter(lpair.values())=={8:960,16:16}
    lp=Counter(flag[0] for (i,S),flags in own.items() if i==80 for flag in flags)
    assert Counter(lp.values())=={24:320,16:16}
    # Independent controls: all binary 2-subspaces and every pair of kernels
    # complementary to one fixed image, repeated for every image.
    spaces={frozenset(span([u,v])) for u in range(1,16) for v in range(u+1,16) if rank([u,v])==2};assert len(spaces)==35
    count=0
    for L in spaces:
        complements=[K for K in spaces if L&K=={0}];assert len(complements)==16
        for K in complements:
            E=projection(L,K)
            for K2 in complements:
                F=projection(L,K2);N=[u^v for u,v in zip(E,F)]
                assert all(lin(E,lin(E,x))==lin(E,x) and lin(F,lin(F,x))==lin(F,x) for x in range(16))
                assert all(lin(N,lin(N,x))==0 for x in range(16))
                intersection_dimension=(len(K&K2)).bit_length()-1
                assert rank(N)==2-intersection_dimension
                count+=1
    assert count==8960
    bad_found=False
    for (i,S),flags in own.items():
        for add in tight_sets[i]-set(S):
            bad=set(S);bad.remove(S[0]);bad.add(add)
            if any(len(H&bad)%2 for H in planes if all(dots[i][j]==0 for j in H)):
                bad_found=True;break
        if bad_found:break
    assert bad_found
    result={'status':'PASS_INDEPENDENT_GLOBAL_ASYMMETRY_REVIEW','A2_planes_reconstructed_from_exact_Gram_determinants':1120,'odd_witnesses_independently_reconstructed':421,'receiver_histogram':dict(sorted(hist.items())),'ordinary_planes':1108,'ordinary_pair_flags':2870,'dual_certificates':certificates,'rank_sum_ceiling_at_p360':(360*rank_bound.numerator+rank_bound.denominator-1)//rank_bound.denominator,'receiver80_pair_multiplicities':dict(Counter(lpair.values())),'receiver80_plane_multiplicities':dict(Counter(lp.values())),'projection_controls':count,'odd_cardinality_preserving_witness_mutation_rejected':bad_found,'retained_scope_only':True,'changed_return_bank_or_extra_repair_not_covered':True,'author_code_imported':False}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    pins=[]
    for p in [a.author/'PROOF.md',a.author/'PLANE-DUAL.json',a.author/'PAIR-DUAL.json']:
        pins.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    (a.out/'REVIEW-PINS.json').write_text(json.dumps(pins,indent=2)+'\n')
    print(result['status'])

if __name__=='__main__':main()
