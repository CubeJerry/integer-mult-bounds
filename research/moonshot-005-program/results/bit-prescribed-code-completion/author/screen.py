#!/usr/bin/env python3
import argparse,hashlib,json
from pathlib import Path

def basis(rows):
    b={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in b:x^=b[p]
            else:b[p]=x;break
    return b
def red(x,b):
    while x:
        p=x.bit_length()-1
        if p not in b:return x
        x^=b[p]
    return 0
def orth(rows,n=111):
    b=basis(rows);out=[]
    for j in range(n):
        if j in b:continue
        x=1<<j
        for p in sorted(b):
            if (b[p]&x).bit_count()%2:x^=1<<p
        assert all((x&r).bit_count()%2==0 for r in b.values());out.append(x)
    return out
def solve(rows,x):
    b={}
    for j,v in enumerate(rows):
        c=1<<j
        while v:
            p=v.bit_length()-1
            if p in b:v^=b[p][0];c^=b[p][1]
            else:b[p]=(v,c);break
    c=0
    while x:
        p=x.bit_length()-1
        if p not in b:return None
        v,m=b[p];x^=v;c^=m
    return c

def analyze(S,L,C):
    sb=basis(S);S=list(sb.values());B=[basis(S+loc)for loc in L]
    good=[i for i,b in enumerate(B)if red(1<<i,b)==0];bad=[i for i in range(111)if i not in good]
    N=[];Nmeta=[];nb={}
    for i in bad:
        for z in orth(list(B[i].values())+[1<<i]):
            if red(z,nb):N.append(z);Nmeta.append(i);nb=basis(N)
    H=orth(N);failure=[i for i in bad if all(red(v,B[i])==0 for v in H)]
    witness=[]
    for i in failure:
        z=next(v for v in orth(list(B[i].values()))if v>>i&1);coef=solve(N,z);assert coef is not None
        witness.append({'receiver':i,'annihilator':hex(z),'constraint_sum':[j for j in range(len(N))if coef>>j&1]})
    canonical=basis(S+C);Q=[];span=S.copy()
    for v in C:
        if red(v,basis(span)):Q.append(v);span.append(v)
    qrows=[0]
    for v in Q:qrows +=[z^v for z in qrows]
    R=[];forced=[]
    for i in bad:
        U=basis(list(B[i].values())+[1<<i]);ri=[mask for mask,row in enumerate(qrows)if red(row,U)==0]
        hit=[mask for mask in ri if red(qrows[mask],B[i])!=0]
        rrank=len(basis(ri));R.append({'receiver':i,'allowed_dimension':rrank,'good_directions':hit})
        if rrank==1:assert len(hit)==1;forced.append(hit[0])
    return {'seed_dimension':len(S),'served':good,'unserved':bad,'intersection_dimension':len(H),'intersection_basis':[hex(v)for v in H],
            'one_row_blocking_receivers':failure,'constraint_basis':[{'receiver':i,'row':hex(v)}for i,v in zip(Nmeta,N)],'blocking_witnesses':witness,
            'canonical_joint_dimension':len(canonical),'canonical_added_dimension':len(Q),'canonical_quotient_rows':[hex(v)for v in Q],
            'canonical_receiver_spaces':R,'forced_canonical_direction_span':len(basis(forced)),
            'all_extension_fields_one_row_possible':not failure}

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--seed',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();d=json.loads(a.seed.read_text());raw=(a.repo/d['native_source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==d['native_source_sha256'];R=json.loads(raw)['native_roots'];dot=lambda a,b:sum(x*y for x,y in zip(a,b));L=[[1<<j for j in range(111)if not dot(R[i],R[j])]for i in range(111)];C=[(1<<i)^sum(L[i])for i in range(111)];S=[int(v,16)for v in d['seed_rows']];E=[1,6,73,75,77,79];closure=[1,3,4,6,18,21,61,64,65,73,74,75,76,77,78,79,80]
    A=[C[i]&sum(1<<j for j in range(111)if d['h_values'][i]==d['h_values'][j])for i in range(111)];S6=[A[i]for i in [3,76,80,4,74,78]]
    results={}
    for name,extra in [('S8',[]),('S8_plus_E6',E),('S8_plus_all17_feedback',closure)]:
        res=analyze(S+[1<<j for j in extra],L,C);results[name]=res
        print(name,{k:v for k,v in res.items()if k in ['seed_dimension','served','intersection_dimension','canonical_joint_dimension','canonical_added_dimension','forced_canonical_direction_span','all_extension_fields_one_row_possible']},'blockers',len(res['one_row_blocking_receivers']))
    for name,extra in [('S6',[]),('S6_plus_E6',E),('S6_plus_all17_feedback',closure)]:
        res=analyze(S6+[1<<j for j in extra],L,C);results[name]=res
        print(name,{k:v for k,v in res.items()if k in ['seed_dimension','served','intersection_dimension','canonical_joint_dimension','canonical_added_dimension','forced_canonical_direction_span','all_extension_fields_one_row_possible']},'blockers',len(res['one_row_blocking_receivers']))
    out={'status':'EXACT_PRESCRIBED_SEED_COMPLETION_SCREEN','source_sha256':hashlib.sha256(raw).hexdigest(),'seed_source_sha256':hashlib.sha256(a.seed.read_bytes()).hexdigest(),'local_space':'All geometrically permitted raw foreign coordinates, granted freely and ignoring actual acquisition','cases':results}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
