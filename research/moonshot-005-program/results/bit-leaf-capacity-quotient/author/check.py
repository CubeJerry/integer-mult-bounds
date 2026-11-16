#!/usr/bin/env python3
"""Check exact fixed-history hypotheses for the all-field leaf-capacity theorem."""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import argparse, hashlib, json
from sympy import Matrix
BASE_SHA='e4d451886a134c648f71fadac5b7f6f8693e5495b60416d137cfe0d0e563e050'
SOURCE_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
PORTS=[7,11,12,41,28,44,19,27]
WITNESSES=[[18],[26],[53,57,85],[24],[45],[29,62,63],[8,9,36,37],[42]]
SIDE_RANKS=[0,0,0,0,0,1,1,0]
@lru_cache(None)
def basis(rows):
    a=Matrix(rows) if rows else Matrix.zeros(0,8);r,p=a.rref()
    return tuple(tuple(r[i,j] for j in range(8)) for i in range(len(p)))
def chart(c):
    rows=tuple(tuple(r) for r in c['rows'])
    if c['kind']=='span':return basis(rows)
    assert c['kind']=='ann'
    return basis(tuple(tuple(z) for z in Matrix(rows).nullspace()))
@lru_cache(None)
def sub(a,b):return len(basis(a+b))==len(b)
def bb(rows):
    ans={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in ans:x^=ans[p]
            else:ans[p]=x;break
    return ans
def fits(rows,x):
    a=bb(rows)
    while x:
        p=x.bit_length()-1
        if p not in a:return False
        x^=a[p]
    return True
def sha(raw):return hashlib.sha256(raw).hexdigest()
def replay(w,roots):
    C={n:chart(c) for n,c in w['charts'].items()}
    for i,r in enumerate(roots):
        assert C[f'L{i}']==basis((tuple(r),))
        assert C[f'F{i}']==chart({'kind':'ann','rows':[r]})
    v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i) for i in range(111)}
    at={f'X{i}':f'L{i}' for i in range(111)}|{f'Y{i}':'zero' for i in range(111)}
    hist=[(0,n,at[n],z) for n,z in v.items()];owners=set();born=set();count=Counter();profile=Counter();dirty=peak=0
    for step,o in enumerate(w['operations'],1):
        op,n,*q=o;count[op]+=1
        if op=='INIT':
            assert n not in v and n not in born and q[0] in C
            v[n]=0;at[n]=q[0];owners.add(n);born.add(n);changed=n
        elif op=='ADD':
            assert n in v and q[0] in v and C[at[n]]==C[at[q[0]]],(step,o,'colocation')
            v[q[0]]^=v[n];changed=q[0]
        elif op=='MOVE':
            before,after=C[at[n]],C[q[0]]
            assert sub(after,before) if n in owners else sub(before,after),(step,o,'direction')
            d=abs(len(before)-len(after));assert d>0;profile[d]+=1;at[n]=q[0];changed=n
        elif op=='CLEAR':
            assert n in owners;dirty+=bool(v[n]);owners.remove(n);del v[n],at[n];continue
        else:raise AssertionError(o)
        peak=max(peak,len(owners));hist.append((step,changed,at[changed],v[changed]))
    assert not owners and len(v)==222
    for i in range(111):
        assert v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'
        assert v[f'Y{i}']==(1<<(111+i))^((1<<i) if i in w['targets'] else 0) and at[f'Y{i}']==f'F{i}'
    return C,hist,{'input_columns':222,'counts':dict(count),'movement_profile':dict(sorted(profile.items())),'dirty_CLEAR':dirty,'peak_owned':peak,'historical_record_states':len(hist)}
def make_banks(w):
    H0=[1<<i for i,h in enumerate(w['singular_h']) if h==0];E=set(w['history_extra_query_roles'])
    H1=[1<<i for i,h in enumerate(w['singular_h']) if h==1 and i not in E]
    g0=int(w['extra_source_delivery']['first_retention_hex'],16);g1=int(w['higher_source_delivery']['first_retention_hex'],16)
    return [H0+[g1],H0,H0,H1,H1,H1,[1<<i for i in sorted(E)]+[g0],H0+[g1]]
def verify_witness(J,k,w,R,C,hist,banks,expected_side_rank=None):
    dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));mask=sum(1<<i for i in J)
    assert set(J).isdisjoint(w['targets'])
    vis={i:[p for p,j in enumerate(PORTS) if dot(i,j)==0] for i in J}
    counts={};side=[];old=[]
    for i in J:
        assert k in vis[i]
        visible=[x for x in hist if sub(C[x[2]],C[f'F{i}'])];counts[str(i)]=len(visible)
        old +=[value&mask for _,_,_,value in visible]
        side +=[value&mask for _,_,_,value in visible]
        side +=[(1<<j)&mask for j in range(111) if dot(i,j)==0]
        for p in vis[i]:
            if p!=k:side +=[row&mask for row in banks[p]]
    side +=[(1<<j)&mask for j in w['targets']]
    basis_rows=list(bb(side).values());r=len(basis_rows)
    if expected_side_rank is not None:assert r==expected_side_rank,(J,r,expected_side_rank,'external-information rank changed')
    kernel=[]
    for bits in range(1<<len(J)):
        z=sum(((bits>>t)&1)<<j for t,j in enumerate(J))
        if all((z&row).bit_count()%2==0 for row in basis_rows) and not fits(kernel,z):kernel.append(z)
    assert len(kernel)==len(J)-r
    assert len(bb(row&mask for row in banks[k]))==len(J)
    return {'port':PORTS[k],'demands':J,'external_projected_rank':r,'external_projected_basis_hex':[hex(z) for z in basis_rows],'input_kernel_basis_hex':[hex(z) for z in kernel],'required_capacity_in_whole_records':len(J)-r,'gram_matrix':[[dot(i,j) for j in J] for i in J],'visible_ports':{str(i):[PORTS[p] for p in vis[i]] for i in J},'visible_old_history_counts':counts,'old_history_projected_rank':len(bb(old)),'designated_bank_projection_rank':len(J)}
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--expected-word-sha',default=BASE_SHA);a=p.parse_args()
    raw=a.word.read_bytes();assert sha(raw)==a.expected_word_sha;w=json.loads(raw);source=(a.repo/w['source_path']).read_bytes();assert sha(source)==SOURCE_SHA==w['source_sha256'];R=json.loads(source)['native_roots']
    C,hist,replay_report=replay(w,R);banks=make_banks(w);cases=[verify_witness(J,k,w,R,C,hist,banks,SIDE_RANKS[k]) for k,J in enumerate(WITNESSES)]
    dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));known=set(w['targets']);waves=[]
    while True:
        nxt=set(known)
        for i in range(111):
            rows=[1<<j for j in known]+[1<<j for j in range(111) if dot(i,j)==0]
            for k,j in enumerate(PORTS):
                if dot(i,j)==0:rows+=banks[k]
            if fits(rows,1<<i):nxt.add(i)
        if nxt==known:break
        waves.append(sorted(nxt-known));known=nxt
    assert len(known)==111
    controls=[]
    try:verify_witness(WITNESSES[2],2,w,R,C,hist+[(-1,'leak_X53','zero',1<<53)],banks,0)
    except AssertionError:controls.append('New common X53 information invalidates the frozen-history witness.')
    else:raise AssertionError('accepted common-information mutation')
    altered=[list(b) for b in banks];altered[5].append(1<<53)
    try:verify_witness(WITNESSES[2],2,w,R,C,hist,altered,0)
    except AssertionError:controls.append('New X53 source at port44 invalidates the fixed-bank witness.')
    else:raise AssertionError('accepted source-bank mutation')
    short=verify_witness([53,57],2,w,R,C,hist,banks);assert short['required_capacity_in_whole_records']==2
    controls.append('Removing demand85 lowers the port12 witness floor from3 to2.')
    result={'status':'PASS_EXACT_LEAF_CAPACITY_THIRTEEN_QUOTIENT','word_sha256':sha(raw),'native_source_sha256':sha(source),'replay':replay_report,'fixed_history_scope':'Every initial record and every post-INIT/ADD/MOVE record at its actual chart across the complete fixed operation word; even original-Y X-parts are granted.','ports':PORTS,'source_banks':[{'port':j,'binary_rank':len(bb(b)),'rows_hex':[hex(r) for r in b]} for j,b in zip(PORTS,banks)],'initial_free_points':w['targets'],'witnesses':cases,'componentwise_capacity_floor':[c['required_capacity_in_whole_records'] for c in cases],'sum_of_capacity_floors':sum(c['required_capacity_in_whole_records'] for c in cases),'one_record_per_port_deficit':{str(c['port']):c['required_capacity_in_whole_records']-1 for c in cases if c['required_capacity_in_whole_records']>1},'whole_bank_feedback_closure_count':len(known),'whole_bank_feedback_waves':waves,'negative_and_boundary_controls':controls,'scope':'Necessary fixed-history/full-source-bank leaf-capacity gate, including free decoded-raw-point feedback. No movement-price conclusion without an additional physical cut proof. Changed higher memories, source banks, ports or common coded data may escape.','no_new_kappa':True}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'word_sha256':sha(raw),'history_states':len(hist),'capacity_floor':result['componentwise_capacity_floor'],'whole_bank_closure':len(known),'controls':len(controls)}))
if __name__=='__main__':main()
