#!/usr/bin/env python3
"""Independent matrix/nullspace verification of the two-stage row supports."""
import argparse,gzip,hashlib,json,importlib.util
from collections import Counter,defaultdict
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
HERE=Path(__file__).resolve().parent
N=25
I=tuple(1<<i for i in range(N))
def need(c,m):
    if not c:raise ValueError(m)
def parity(x):return x.bit_count()%2
def mv(A,x):
    z=0
    for k,c in enumerate(A):
        if x>>k&1:z^=c
    return z
def trans(A,x):return sum(parity(c&x)<<k for k,c in enumerate(A))
def compose(first,second):
    A,b=first;C,d=second
    return tuple(mv(C,a)for a in A),mv(C,b)^d
def nullspace(vectors):
    rows=list(vectors);pivots=[];r=0
    for c in range(N):
        ix=next((i for i in range(r,len(rows))if rows[i]>>c&1),None)
        if ix is None:continue
        rows[r],rows[ix]=rows[ix],rows[r]
        for i in range(len(rows)):
            if i!=r and rows[i]>>c&1:rows[i]^=rows[r]
        pivots.append(c);r+=1
    ans=[]
    for f in range(N):
        if f in pivots:continue
        x=1<<f
        for row,c in zip(rows,pivots):
            if row>>f&1:x|=1<<c
        ans.append(x)
    need(all(parity(x&v)==0 for x in ans for v in vectors),'annihilator construction')
    return ans
def equation_rank(eqs):
    rows=[a|(b<<N)for a,b in eqs];r=0
    for c in range(N):
        ix=next((i for i in range(r,len(rows))if rows[i]>>c&1),None)
        if ix is None:continue
        rows[r],rows[ix]=rows[ix],rows[r]
        for i in range(len(rows)):
            if i!=r and rows[i]>>c&1:rows[i]^=rows[r]
        r+=1
    consistent=all(row!=(1<<N)for row in rows)
    return r,consistent
def main(output):
    pins=json.loads((HERE/'SOURCES.json').read_text())['pins']
    for p,s in pins.items():need(hashlib.sha256((HERE/p).read_bytes()).hexdigest()==s,'pin '+p)
    w=json.loads(gzip.decompress((HERE/'source/FORWARD.json.gz').read_bytes()));d=w['logical_involution']
    P=d['ports'];q={int(h):v for h,v in d['normals'].items()};R={int(h):{int(j):F(v)for j,v in row.items()}for h,row in d['R_rows'].items()}
    rr={(r['stage'],r['port']):r for r in json.loads((HERE/'source/ROUTES.json').read_text())['route_records']}
    report=json.loads((HERE/'source/ROOT-SUPPORT.json').read_text());author={r['output_port']:r for r in report['certificates']}
    for h in P:
        acc=defaultdict(F)
        for k,a in R[h].items():
            for j,b in R[k].items():acc[j]+=a*b
        need({j:v for j,v in acc.items()if v}=={h:F(1)},'actual R involution')
    perms={}
    for (s,h),row in rr.items():
        B=row['orthogonal_complement'];start=9+8*(s-1)
        basis=[q[h]]+B
        need(all(parity(a&b)==int(i==j)for i,a in enumerate(basis)for j,b in enumerate(basis)),'actual orthonormal head frame')
        cols=[]
        for j in range(N):
            if j<9:col=(q[h]if q[h]>>j&1 else 0)^sum((1<<(start+k))for k,b in enumerate(B)if b>>j&1)
            elif start<=j<start+8:col=B[j-start]
            else:col=1<<j
            cols.append(col)
        A=tuple(cols);need(all(mv(A,c)==1<<i for i,c in enumerate(A)),'actual swap involution');perms[s,h]=A
    def atom(tag,s,h,inv=False):
        A=perms[s,h];tau=rr[s,h]['input_translation'if tag=='M'else'output_translation']
        return A,tau if inv else mv(A,tau)
    def fourier(ops,z):
        phase=0
        for tag,s,h,inv in reversed(ops):
            if tag=='Q2':phase+=2*parity(q[h]&z);continue
            tau=rr[s,h]['input_translation'if tag=='M'else'output_translation'];A=perms[s,h]
            if inv:phase+=2*parity(tau&z);z=mv(A,z)
            else:z=mv(A,z);phase+=2*parity(tau&z)
        return z,phase%4
    blocks=defaultdict(lambda:defaultdict(F));core_count=0;wrong_translation=None
    for h in P:
        for k,a in R[h].items():
            for j,b in R[k].items():
                ops=[('O',2,h,False),('O',2,k,True),('Q2',0,k,False),('M',1,k,True),('M',1,j,False)]
                core=(I,0)
                for tag,s,l,iv in ops:core=compose(core,(I,q[l])if tag=='Q2'else atom(tag,s,l,iv))
                A,offset=core
                for z in(0,)+I:need(fourier(ops,z)==(trans(A,z),2*parity(offset&z)),'actual core matrix / Fourier order')
                if wrong_translation is None:
                    bad=[op for op in ops if op[0]!='Q2']
                    witness=next((z for z in I if fourier(bad,z)!=fourier(ops,z)),None)
                    if witness is not None:wrong_translation={'h':h,'k':k,'j':j,'frequency':witness}
                blocks[h,j][core]+=a*b;core_count+=1
    blocks={ij:{c:v for c,v in rows.items()if v}for ij,rows in blocks.items()if any(rows.values())}
    need(len(blocks)==448 and all(len(z)==4 and all(abs(c)==F(1,4)for c in z.values())for z in blocks.values()),'complete1792 path sums')
    need(wrong_translation is not None,'omitted Q2 translation detected')
    codims=Counter();pair_count=0;row_separator_count=0;bad_uniform_row=None;tensor_checks=0
    for h in P:
        receipt=author[h];x=receipt['spatial_row'];actual_blocks=[];actual_collisions=[]
        for (hh,j),terms in blocks.items():
            if hh!=h:continue
            def plane(core,x):
                A,b=core;base=mv(A,x)^b;u=mv(A,q[h]);v=q[j]
                S={base,base^u,base^v,base^u^v};need(len(S)==4,'genuine independent Gaussian directions');return S
            corelist=list(terms);sets=[plane(c,x)for c in corelist]
            need(len(set.union(*sets))==16,'actual separator has all16 block entries')
            actual_blocks.append({'input_port':j,'planes':sorted((sorted(plane(c,x)),str(v))for c,v in terms.items())})
            zero_sets=[plane(c,0)for c in corelist]
            if len(set.union(*zero_sets))<16 and bad_uniform_row is None:bad_uniform_row={'output_port':h,'input_port':j,'row':0,'union_size':len(set.union(*zero_sets))}
            for ii,jj in((i,j)for i in range(4)for j in range(i)):
                A,b=corelist[ii];C,e=corelist[jj]
                ann=nullspace([mv(A,q[h]),mv(C,q[h]),q[j]])
                eqs=[(trans(tuple(a^c for a,c in zip(A,C)),z),parity(z&(b^e)))for z in ann]
                codim,consistent=equation_rank(eqs);need(consistent and codim>=3,'proper affine collision locus')
                codims[str(codim)]+=1;pair_count+=1
                actual_collisions.append({'input_port':j,'term_pair':[ii,jj],'codimension':codim,'consistent':consistent})
                # Cartesian products intersect iff both coordinate factors intersect.
                s0=zero_sets[ii];t0=zero_sets[jj];s1=sets[ii];t1=sets[jj]
                need(set(product(s0,s1))&set(product(t0,t1))==set(product(s0&t0,s1&t1)),'two-column product intersection')
                need(not(set(product(s0,s1))&set(product(t0,t1))),'one separating column suffices');tensor_checks+=1
        canon=lambda z:sorted((r['input_port'],tuple(sorted((tuple(p),v)for p,v in r['planes'])))for r in z)
        need(canon(actual_blocks)==canon(receipt['input_blocks']),'independent source planes match every published separator')
        need(actual_collisions==receipt['collision_pairs'],'independent linear-equation collision codimensions')
        row_separator_count+=1
    need(dict(codims)==report['collision_codimension_histogram'],'global collision census')
    need(bad_uniform_row is not None,'false every-row assertion rejected')
    def power(r):
        den=10**40;target=r**199*den**200;lo=0;hi=r*den+1
        while hi-lo>1:
            mid=(hi+lo)//2
            if mid**200<=target:lo=mid
            else:hi=mid
        need(lo**200<=target<(lo+1)**200,'fresh directed power bracket')
        return F(lo,den),F(lo if lo**200==target else lo+1,den)
    def moment(profile):
        lo=hi=F(0)
        for r,c in profile.items():
            a,b=power(r);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
        return lo,hi
    room=moment({17:448,1:-224,2:-448,3:-448,5:-448,6:-448});lower=power(448)
    need(lower[0]>room[1]>0,'joint two-bank entropy tariff exceeds optimistic allowance')
    result={'status':'PASS_INDEPENDENT_TWO_STAGE_SUPPORT_REVIEW','source_pins':pins,'actual_core_paths':core_count,
       'nonzero_blocks':len(blocks),'actual_separating_rows':row_separator_count,'collision_equation_systems':pair_count,
       'collision_codimension_histogram':dict(codims),'two_column_product_intersections_checked':tensor_checks,
       'negative_controls':{'omit_middle_Q_squared':wrong_translation,'claim_every_spatial_row_separates':bad_uniform_row},
       'proved_fraction_at_least':'max(0,1-24*2^(-3V))','weaker_author_bound_valid':True,
       'per_good_row_support':'16*4^V','per_good_entry_magnitude':'2^(-V-2)',
       'normalized_entropy_lower_bound':'112*b*max(0,1-24*2^(-3V))*(2V+4)',
       'optimistic_two_call_two_query_allowance_interval':[str(z)for z in room],
       'unitary_joint_two_bank_moment_lower_bound_interval':[str(z)for z in lower],
       'universal_tensor_claim_depends_on_review_proof_not_finite_tests':True,'no_general_nonunitary_exclusion':True,'new_kappa':False}
    output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print({k:v for k,v in result.items()if k not in('source_pins','negative_controls')})
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'RESULT.json');a=p.parse_args();main(a.output)
