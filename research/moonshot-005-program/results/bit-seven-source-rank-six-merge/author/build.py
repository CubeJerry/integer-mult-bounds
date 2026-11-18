#!/usr/bin/env python3
"""Compile an exact seven-source complete-graph quotient gadget over F8.

The literal scheduling pattern is adapted, with attribution, from Worker A's
four-source tetrahedral compiler. All field dimensions/formulas are rebuilt.
"""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import gzip,json

LAYOUT_HASH='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
DONORS=[0,14,15,30,34,38,69]
RECEIVERS=[72,85,87,101,98,94,3]
N=7
RANK=5
DEGREE=3
POLYNOMIAL=11
PARAMETERS=list(range(N))

def need(value,message):
    if not value:raise ValueError(message)

def mul(a,b):
    z=0
    while b:
        if b&1:z^=a
        b>>=1;a<<=1
        if a&8:a^=POLYNOMIAL
    return z

def inv(a):
    need(a,'nonzero field denominator')
    return next(b for b in range(1,8)if mul(a,b)==1)

def dot(a,b):
    z=0
    for x,y in zip(a,b):z^=mul(x,y)
    return z

def powers(t):
    row=[1]
    for _ in range(RANK-1):row.append(mul(row[-1],t))
    return row

PHI=[powers(t)for t in PARAMETERS]

def lift(i,j,k):
    # Coefficients of product_(l outside {i,j,k}) (t+t_l).
    p=[1]
    for l in range(N):
        if l in(i,j,k):continue
        q=[0]*(len(p)+1)
        for c,x in enumerate(p):q[c]^=mul(x,PARAMETERS[l]);q[c+1]^=x
        p=q
    need(len(p)==RANK,'lift dimension')
    return p

def rank(rows):
    a=[r[:]for r in rows];p=0
    for c in range(len(a[0])if a else 0):
        z=next((z for z in range(p,len(a))if a[z][c]),None)
        if z is None:continue
        a[p],a[z]=a[z],a[p];q=inv(a[p][c]);a[p]=[mul(q,x)for x in a[p]]
        for z in range(len(a)):
            if z!=p and a[z][c]:
                q=a[z][c];a[z]=[x^mul(q,y)for x,y in zip(a[z],a[p])]
        p+=1
    return p

def names(prefix):return [prefix+'b'+str(c)for c in range(DEGREE)]

def build(w):
    A=[set(h)for h in w['A2']]
    planes={(j,k):next(h for h,H in enumerate(A)if{DONORS[j],DONORS[k]}<=H)for j,k in combinations(range(N),2)}
    def H(j,k):return 'H'+str(planes[tuple(sorted((j,k)))])
    events=[]
    def put(*a):events.append(list(a))
    def init(p,chart):
        for x in names(p):put('INIT',x,chart)
    def move(p,chart):
        for x in names(p):put('MOVE',x,chart)
    def clear(p):
        for x in names(p):put('CLEAR',x)
    def add(dst,src,c):
        for k in range(DEGREE):
            v=mul(c,1<<k)
            for r in range(DEGREE):
                if v>>r&1:put('ADD',names(dst)[r],names(src)[k])
    source_begin=len(events)
    for j in range(N):
        for k in range(N):
            if k==j:continue
            e=f'E{j}_{k}_';init(e,'L'+str(DONORS[j]))
            for c in range(RANK):add(e,f'X{j}_{c}_',PHI[k][c])
            move(e,H(j,k))
    source_end=len(events)
    for j in range(N):
        for c in range(RANK):move(f'X{j}_{c}_','Hub')
    for i in range(N):
        for c in range(RANK):move(f'Y{i}_{c}_','F'+str(RECEIVERS[i]))
    formulas=[]
    plane_add=0;receiver_add=0
    for j,k in combinations(range(N),2):
        for i in range(N):
            if i in(j,k):continue
            v=lift(i,j,k);a=inv(dot(PHI[k],v));b=inv(dot(PHI[j],v))
            z=f'Z{j}{k}_{i}_';init(z,H(j,k))
            t=len(events);add(z,f'E{j}_{k}_',a);add(z,f'E{k}_{j}_',b);plane_add+=len(events)-t
            move(z,'F'+str(RECEIVERS[i]))
            t=len(events)
            for c in range(RANK):add(f'Y{i}_{c}_',z,v[c])
            receiver_add+=len(events)-t
            clear(z)
            formulas.append({'plane':[j,k],'receiver':i,'lift':v,'plane_coefficients':[a,b]})
        clear(f'E{j}_{k}_');clear(f'E{k}_{j}_')
    return {'schema':'literal-binary-record-seven-source-F8-v1','native_donors':DONORS,'native_receivers':RECEIVERS,'plane_indices':[[j,k,h]for(j,k),h in sorted(planes.items())],'field_polynomial':POLYNOMIAL,'field_degree':DEGREE,'bank_field_dimension':RANK,'parameters':PARAMETERS,'source_forms':PHI,'plane_formulas':formulas,'ordinary_ADD_partition':{'source':sum(e[0]=='ADD'for e in events[source_begin:source_end]),'plane':plane_add,'receiver':receiver_add},'events':events}

def replay(w,word):
    A=[set(h)for h in w['A2']];R=w['root_table'];fields={};original={};order=[]
    for prefix,roles in [('X',DONORS),('Y',RECEIVERS)]:
        for j,role in enumerate(roles):
            for c in range(RANK):
                for name in names(f'{prefix}{j}_{c}_'):
                    n=len(order);order.append(name);original[name]=1<<n
                    fields[name]=[1<<n,('L'+str(role))if prefix=='X'else'G',False]
    def chart_rank(chart):return 0 if chart=='G'else 8 if chart=='Hub'else 1 if chart[0]=='L'else 2 if chart[0]=='H'else 7
    def nested(a,b):
        if a=='G' or b=='Hub':return chart_rank(a)<chart_rank(b)
        if a[0]=='L'and b[0]=='H':return int(a[1:])in A[int(b[1:])]
        if a[0]=='H'and b[0]=='F':return all(sum(x*y for x,y in zip(R[j],R[int(b[1:])]))==0 for j in A[int(a[1:])])
        return False
    counts=Counter();profile=Counter();owned_profile=Counter();dirty=0;peak=0;owned=set();seen=set(fields)
    for t,event in enumerate(word['events']):
        op=event[0];counts[op]+=1
        if op=='INIT':
            _,name,chart=event;need(name not in seen,'fresh auxiliary name');seen.add(name);fields[name]=[0,chart,True];owned.add(name);peak=max(peak,len(owned))
        elif op=='ADD':
            _,dst,src=event;need(dst!=src and dst in fields and src in fields,'live distinct operands');need(fields[dst][1]==fields[src][1],f'ADD same chart at {t}');fields[dst][0]^=fields[src][0]
        elif op=='MOVE':
            _,name,chart=event;need(name in fields,'live move');old=fields[name][1];need(nested(old,chart),f'strict genuine inclusion {old}->{chart}');gap=chart_rank(chart)-chart_rank(old);profile[gap]+=1
            if fields[name][2]:owned_profile[gap]+=1
            fields[name][1]=chart
        elif op=='CLEAR':
            _,name=event;need(name in owned,'owned clear');dirty+=bool(fields[name][0]);owned.remove(name);del fields[name]
        else:raise ValueError(op)
    need(not owned and set(fields)==set(original),'helpers retired and originals retained')
    for j in range(N):
        for c in range(RANK):
            for bit,name in enumerate(names(f'X{j}_{c}_')):need(fields[name]==[original[name],'Hub',False],'original X restored')
    for i in range(N):
        for c in range(RANK):
            for bit,name in enumerate(names(f'Y{i}_{c}_')):
                wanted=original[name]
                for j in range(N):
                    if j!=i:wanted^=original[names(f'X{j}_{c}_')[bit]]
                need(fields[name]==[wanted,'F'+str(RECEIVERS[i]),False],'all-column exact receiver sum')
    return {'counts':dict(sorted(counts.items())),'movement_profile':dict(sorted(profile.items())),'owned_upward_profile':dict(sorted(owned_profile.items())),'dirty_CLEAR':dirty,'peak_owned_binary_records':peak,'original_binary_columns':len(original),'all_original_X_restored':True,'all_arbitrary_Y_baselines_preserved':True,'all_42_foreign_blocks_identity':True,'final_rows':{name:fields[name][0]for name in order}}

def main():
    ap=ArgumentParser();ap.add_argument('--layout',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();raw=gzip.decompress(a.layout.read_bytes());need(sha256(raw).hexdigest()==LAYOUT_HASH,'pinned native layout');w=json.loads(raw)
    need(all(rank([PHI[j]for j in S])==RANK for S in combinations(range(N),RANK)),'all five-row Vandermonde bases')
    geometry=[]
    for i,r in enumerate(RECEIVERS):
        dots=[sum(a*b for a,b in zip(w['root_table'][r],w['root_table'][j]))for j in DONORS]
        need([v==0 for v in dots]==[j!=i for j in range(N)],'native all-but-diagonal incidence');geometry.append(dots)
    word=build(w);res=replay(w,word)
    need(res['movement_profile']=={1:126,5:315,7:210},'complete paid movement invoice')
    for j,k in combinations(range(N),2):
        formulas=[p for p in word['plane_formulas']if p['plane']==[j,k]]
        need(rank([p['plane_coefficients']for p in formulas])==2,'private output map has rank two')
        for fa,fb in combinations(formulas,2):need(rank([fa['plane_coefficients'],fb['plane_coefficients']])==2,'all five private output lines distinct')
    a.out.mkdir(parents=True,exist_ok=True);wr=json.dumps(word,separators=(',',':')).encode()+b'\n';(a.out/'WORD.json').write_bytes(wr)
    out={'status':'PASS_PAID_NATIVE_SEVEN_SOURCE_QUOTIENT_GADGET','layout_uncompressed_sha256':LAYOUT_HASH,'word_sha256':sha256(wr).hexdigest(),'native_foreign_dots':geometry,'invoice':res,'ordinary_ADD_partition':word['ordinary_ADD_partition'],'field_inputs_per_donor':RANK,'field_outputs_per_receiver':RANK,'field_source_ports':42,'field_private_plane_ports':105,'field_polynomial':POLYNOMIAL,'full_balanced_source_constructed':False,'new_complete_kappa':False}
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],res['counts'],res['movement_profile'],'dirty',res['dirty_CLEAR'],'peak',res['peak_owned_binary_records'])

if __name__=='__main__':main()
