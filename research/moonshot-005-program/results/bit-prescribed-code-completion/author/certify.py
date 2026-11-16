#!/usr/bin/env python3
"""Small explicit witnesses certifying the prescribed-code completion bounds."""
import argparse,hashlib,json
from pathlib import Path
from screen import basis,red,solve

def parity(v):return v.bit_count()&1
def xor(values):
    x=0
    for v in values:x^=v
    return x

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--seed',type=Path,required=True);p.add_argument('--screen',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();d=json.loads(a.seed.read_text());src=(a.repo/d['native_source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==d['native_source_sha256'];R=json.loads(src)['native_roots'];h=d['h_values'];dot=lambda a,b:sum(x*y for x,y in zip(a,b));K=[sum(1<<j for j in range(111)if i==j or not dot(R[i],R[j]))for i in range(111)];A=[K[i]&sum(1<<j for j in range(111)if h[i]==h[j])for i in range(111)];S8=[int(v,16)for v in d['seed_rows']];S6=[A[i]for i in [3,76,80,4,74,78]];E=[1,6,73,75,77,79];T=[1,3,4,6,18,21,61,64,65,73,74,75,76,77,78,79,80];L=[K[i]^(1<<i)for i in range(111)]
    assert len(basis(K))==9 and len(basis(S8))==8 and len(basis(S6))==6
    assert len(basis(S8+[A[i]for i in d['targets']]))==8
    frames={'S8':[0,14,22,23,30,31,59,60],'S6':[0,14,60,63,69,70,107,109]};frameproof=[]
    for name,S in [('S8',S8),('S6',S6)]:
        I=frames[name];assert len(set(I))==8 and not set(I)&set(T)
        assert all(dot(R[i],R[j])!=0 for i in I for j in I)
        cols=[sum(((v>>i)&1)<<j for j,v in enumerate(S))for i in I];rank=len(basis(cols));assert rank==(4 if name=='S8'else 3)
        frameproof.append({'code':name,'roles':I,'evaluation_columns':cols,'restriction_rank':rank,'added_dimension_lower_bound':8-rank,'all_granted_points_vanish':True})
    J=[j for j in range(111)if h[j]==0 and j not in T];jm=sum(1<<j for j in J);hv=sum(v<<j for j,v in enumerate(h));assert len(J)==41
    assert len(basis(v&jm for v in K))==8 and solve(K,hv)is not None
    assert h[19]==1 and 19 not in T and all(not(v>>19&1)for v in S8+S6)
    assert len(basis(v&jm for v in S8))==4 and len(basis(v&jm for v in S6))==3
    gauge={'J':J,'C9_restriction_rank':8,'S8_restriction_rank':4,'S6_restriction_rank':3,'kernel_generator_h':hex(hv),'h_from_canonical_rows':hex(solve(K,hv)),'separating_coordinate':19,'all_baseline_rows_zero_at_separating_coordinate':True}
    raw=a.screen.read_bytes();screen=json.loads(raw);cases={};negative=0
    for name,res in screen['cases'].items():
        S=S8 if name.startswith('S8')else S6
        points=T if 'all17'in name else E if 'E6'in name else[]
        B=S+[1<<j for j in points];dim=len(basis(B));assert dim==res['seed_dimension'];N=[int(v['row'],16)for v in res['constraint_basis']]
        for z,meta in zip(N,res['constraint_basis']):
            i=meta['receiver'];assert all(not parity(z&v)for v in B)and not(z&L[i])and not(z>>i&1)
        assert len(basis(N))==111-dim
        for v in res['intersection_basis']:assert red(int(v,16),basis(B))==0
        dual=[]
        for rec in res['blocking_witnesses']:
            i=rec['receiver'];z=int(rec['annihilator'],16)
            assert z>>i&1 and not(z&L[i])and all(not parity(z&v)for v in B)
            assert xor(N[j]for j in rec['constraint_sum'])==z
            dual.append(i)
            assert xor(N[j]for j in rec['constraint_sum'])!=(z^(1<<i));negative+=1
        assert dual==res['unserved']
        Q=[int(v,16)for v in res['canonical_quotient_rows']];assert len(Q)==(5 if name.startswith('S8')else 6)
        assert len(basis(B+Q))==dim+len(Q)and len(basis(B+Q+K))==dim+len(Q)
        forced=[];fb={}
        for r in res['canonical_receiver_spaces']:
            if r['allowed_dimension']!=1:continue
            i=r['receiver'];loc=[1<<j for j in range(111)if L[i]>>j&1];bi=basis(B+loc);ui=basis(B+loc+[1<<i]);masks=[]
            for m in range(1<<len(Q)):
                row=xor(Q[j]for j in range(len(Q))if m>>j&1)
                if red(row,ui)==0:masks.append(m)
            assert len(masks)==2 and masks[0]==0
            m=masks[1];v=xor(Q[j]for j in range(len(Q))if m>>j&1);assert red(v,bi)!=0
            if red(m,fb):forced.append({'receiver':i,'quotient_mask':m});fb=basis(v['quotient_mask']for v in forced)
        assert len(forced)==len(Q)
        omissions=[]
        for omit in range(len(Q)):
            bb=B+[v for j,v in enumerate(Q)if j!=omit]
            missed=[i for i in range(111)if red(1<<i,basis(bb+[1<<j for j in range(111)if L[i]>>j&1]))!=0]
            assert missed;omissions.append({'omitted_new_direction':omit,'unfitted_receivers':missed})
        cases[name]={'baseline_dimension':dim,'one_row_intersection_equals_baseline':True,'verified_dual_blockers':len(dual),'canonical_added_directions':len(Q),'independent_forced_quotient_lines':forced,'omission_controls':omissions,'added_dimension_bounds':[4,5]if name.startswith('S8')else[5,6]}
    out={'status':'PASS_PRESCRIBED_SEED_COMPLETION_CERTIFICATES','source_sha256':hashlib.sha256(src).hexdigest(),'seed_source_sha256':hashlib.sha256(a.seed.read_bytes()).hexdigest(),'screen_sha256':hashlib.sha256(raw).hexdigest(),'frames':frameproof,'gauge_certificate':gauge,'cases':cases,'mutated_dual_negative_controls':negative,'all_fields_and_widths':'By binary rank stability, identity block restriction and the proved injective restriction argument; no scalar-field search extrapolation','scope':'Fixed retained S8 or activeS6 ground-code extension, even with maximal geometric side information; no restriction on changed preload/chronological architectures; no new kappa'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k in ['status','frames','mutated_dual_negative_controls','scope']}))

if __name__=='__main__':main()
