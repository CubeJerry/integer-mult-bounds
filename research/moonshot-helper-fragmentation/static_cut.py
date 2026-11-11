#!/usr/bin/env python3
"""Exact static rank3/6 cut obstruction on selected#7000. No new kappa."""
import argparse
from collections import Counter,defaultdict
from fractions import Fraction as Q
import gzip,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
SHA='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
BLOB='74563a7867d9d762b6588f65362369668841bb3e'

def need(ok,msg):
    if not ok:raise ValueError(msg)

def put(v,k,x):
    if x:v[k]=x
    else:v.pop(k,None)

def add(v,w,c):
    for k,x in w.items():put(v,k,v.get(k,0)+c*x)

def kernel(images,allowed):
    """Transposed constraints: one equation per forbidden source coordinate."""
    n=len(images);eq={}
    for j,img in enumerate(images):
        for k,x in img.items():
            if k not in allowed:eq.setdefault(k,[Q(0)]*n)[j]=x
    pivots={}
    for k in sorted(eq,reverse=True):
        row=eq[k][:]
        for p,old in sorted(pivots.items()):
            if row[p]:
                c=row[p];row=[x-c*y for x,y in zip(row,old)]
        p=next((i for i,x in enumerate(row) if x),None)
        if p is None:continue
        c=row[p];row=[x/c for x in row]
        for op,old in list(pivots.items()):
            if old[p]:
                c=old[p];pivots[op]=[x-c*y for x,y in zip(old,row)]
        pivots[p]=row
    out=[]
    for free in range(n):
        if free in pivots:continue
        coeff=[Q(int(i==free)) for i in range(n)]
        for p,row in pivots.items():coeff[p]=-row[free]
        img={}
        for c,v in zip(coeff,images):
            if c:add(img,v,c)
        need(set(img)<=allowed,'kernel support');out.append((coeff,img))
    return out

def classify(A,B):
    if not any(img for c,img in A):return 'no_pure_prefix'
    if not any(img for c,img in B):return 'no_pure_suffix'
    if not any(sum(x*y for x,y in zip(a,b)) for a,c in A for b,d in B):return 'zero_local_pairing'
    raise ValueError('not excluded by zero-pairing certificate')

def compute(raw):
    need(hashlib.sha256(raw).hexdigest()==SHA,'source SHA256')
    need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==BLOB,'source Git blob')
    w=json.loads(gzip.decompress(raw));n=w['public'];N=n+w['owned_fields'];prog=w['program']
    G={i for i in range(n) if w['initial'][i]==3 and w['final'][i]==127}
    need(len(G)==595,'group size');dims=[];spaces=[]
    for basis in w['frames']:
        sp={0}
        for v in basis:
            need(type(v) is int and 0<v<512 and v not in sp,'independent binary frame');sp|={x^v for x in sp}
        dims.append(len(basis));spaces.append(sp)
    rows=[{i:Q(1)} if i<n else {} for i in range(N)]
    cur=w['initial']+[None]*w['owned_fields'];at=defaultdict(set)
    for i in range(n):at[cur[i]].add(i)
    counts=Counter();snaps={};total=0
    for i,e in enumerate(prog):
        op,r=e[:2]
        if op=='MOVE':
            u,v=e[2:4];need(cur[r]==u,'MOVE source')
            need(spaces[u]<=spaces[v] or spaces[v]<=spaces[u],'MOVE nesting')
            at[u].remove(r);at[v].add(r);cur[r]=v;touched={u,v}
        elif op=='INIT':
            need(cur[r] is None,'INIT active');cur[r]=e[2];at[cur[r]].add(r);rows[r]={};touched={cur[r]}
        elif op=='CLEAR':
            need(cur[r]==e[2],'CLEAR frame');touched={cur[r]};at[cur[r]].remove(r);cur[r]=None;rows[r]={}
        elif op=='SCALE':
            need(cur[r]==e[-1],'SCALE frame');c=Q(e[-2]);need(c!=0,'zero scale');rows[r]={j:c*x for j,x in rows[r].items()};touched={cur[r]}
        elif op in ('ADD','COPY'):
            s=e[2];need(cur[r]==cur[s]==e[-1],'contact frame')
            if op=='COPY':need(not rows[r],'COPY ideal-zero destination')
            add(rows[r],rows[s],Q(e[-2]));touched={cur[r]}
        else:raise ValueError('unknown opcode')
        for f in sorted(touched):
            if f is None or dims[f] not in (3,6) or not at[f]:continue
            roles=sorted(at[f]);total+=1;A=kernel([rows[r] for r in roles],G)
            if not any(img for c,img in A):counts['no_pure_prefix']+=1
            else:snaps.setdefault(i,[]).append((f,roles,A))
    need(all(rows[r]=={r:Q(1)} for r in G),'arbitrary helper identity')
    need(all(cur[r] is None and not rows[r] for r in range(n,N)),'owned final state')
    cols=[{i:Q(1)} if i<n else {} for i in range(N)];classes=[]
    for i in range(len(prog)-1,-1,-1):
        for f,roles,A in snaps.get(i,[]):
            B=kernel([cols[r] for r in roles],G);kind=classify(A,B);counts[kind]+=1
            classes.append({'cut_after':i,'frame':f,'rank':dims[f],'roles':roles,'prefix_dimension':len(A),'suffix_dimension':len(B),'kind':kind})
        e=prog[i];op,r=e[:2]
        if op in ('INIT','CLEAR'):cols[r]={}
        elif op=='SCALE':cols[r]={j:Q(e[-2])*x for j,x in cols[r].items()}
        elif op in ('ADD','COPY'):add(cols[e[2]],cols[r],Q(e[-2]))
    need(sum(counts.values())==total==4657,'cut coverage')
    need(dict(counts)=={'no_pure_prefix':4496,'no_pure_suffix':136,'zero_local_pairing':25},'source-specific result')
    try:classify(kernel([{0:Q(1)}],{0}),kernel([{0:Q(1)}],{0}))
    except ValueError as ex:need(str(ex)=='not excluded by zero-pairing certificate','positive control exception')
    else:raise ValueError('positive cut falsely excluded')
    need(classify([([Q(1),Q(0)],{0:Q(1)})],[([Q(0),Q(1)],{0:Q(1)})])=='zero_local_pairing','orthogonal control')
    return {'status':'PASS_STATIC_3_6_CUT_OBSTRUCTION','source_sha256':SHA,'frames':len(spaces),'events':len(prog),'group_size':len(G),'classes_count':total,'counts':dict(counts),'classes':sorted(classes,key=lambda c:(c['cut_after'],c['frame'])),'controls':['positive split not falsely excluded','orthogonal nonzero images excluded'],'scope':'All existing rank3/6 chart-touch cuts; all coframed public and owned roles; fixed selected source order; boundary support exactly595 current rank9 helpers; COPY-as-ADD. No new kappa.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--source',type=Path,default=HERE.parent/'shared-wire-split-composition/data/final.json.gz');a=p.parse_args()
    result=compute(a.source.read_bytes());path=HERE/'STATIC-RESULT.json'
    if a.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(json.loads(path.read_text())==result,'frozen static receipt mismatch')
    print('PASS_STATIC_3_6_CUT_OBSTRUCTION:4657 classes;4496/136/25 exclusions; No new kappa')

if __name__=='__main__':main()
