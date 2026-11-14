#!/usr/bin/env python3
"""Exact independent formal-stage replay; no constructor imports.
Four characters of Q^4-1 are faithful over Q(i); D exponents stay formal.
"""
from pathlib import Path
from collections import Counter
import argparse,gzip,json,hashlib

def need(ok,msg):
    if not ok:raise ValueError(msg)
def cmul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def cadd(a,b):return a[0]+b[0],a[1]+b[1]
def scale(row,c):return {k:cmul(v,c)for k,v in row.items()if cmul(v,c)!=(0,0)}
def add(a,b,c=(1,0)):
    a=a.copy()
    for k,v in b.items():
        w=cadd(a.get(k,(0,0)),cmul(v,c))
        if w!=(0,0):a[k]=w
        else:a.pop(k,None)
    return a
def dmul(row,stages):
    ans={}
    for (col,ex),v in row.items():
        ex=list(ex)
        for s in stages:ex[s-1]+=1
        ans[col,tuple(ex)]=v
    return ans
ROOTS=[(1,0),(0,1),(-1,0),(0,-1)]
def replay(C,ch,skip=None):
    n=C['roles'];s=C['stages'];z=(0,)*s
    rows=[{(i,z):(1,0)}for i in range(n)];q=ROOTS[ch];qi=ROOTS[-ch%4];peak=n;maxdeg=0
    for idx,e in enumerate(C['events']):
        if idx==skip:continue
        op=e[0]
        if op=='ADD':
            c=int(e[3]);need(str(c)==e[3],'integral ADD');rows[e[1]]=add(rows[e[1]],rows[e[2]],(c,0))
        elif op=='SCALE':
            c=int(e[2]);need(c==-1,'unit integer SCALE');rows[e[1]]=scale(rows[e[1]],(c,0))
        elif op=='SWAP':rows[e[1]],rows[e[2]]=rows[e[2]],rows[e[1]]
        elif op=='LAMBDA':
            need(e[2]in(-1,1),'phase sign');c=(1,0)if ch%2==0 else(0,e[2]);rows[e[1]]=scale(rows[e[1]],c)
        elif op=='QUERY':
            need(e[1]!=e[2]and e[3]in(-1,1),'literal nonself query');rows[e[1]]=add(rows[e[1]],rows[e[2]],ROOTS[ch*e[3]%4])
        elif op=='HOST2':
            stage,x,y,u,v=e[1:];need(len({x,y,u,v})==4,'four distinct native mains')
            rows[y]=add(rows[y],rows[x],qi);rows[u]=add(rows[u],rows[v],(-q[0],-q[1]))
            for r in(x,y,u,v):rows[r]=dmul(rows[r],[stage])
        elif op=='IDLE_ONE':
            need(len(set(e[2]))==len(e[2]),'distinct whole-idle axes');rows[e[1]]=dmul(rows[e[1]],e[2])
        else:raise ValueError('unknown opcode '+op)
        peak=max(peak,sum(map(len,rows)))
    bad=[]
    for row,target in zip(rows,C['endpoint']):
        ex=[0]*s
        for j in target['stages']:ex[j-1]+=1
        expect={(target['role'],tuple(ex)):ROOTS[ch*target['head_exponent']%4]}
        if row!=expect:bad.append(target['role'])
        maxdeg=max(maxdeg,max((max(ex)for _,ex in row),default=0))
    return dict(bad_outputs=bad,peak_terms=peak,final_max_stage_degree=maxdeg)

def main(src,out):
    C=json.loads(gzip.decompress(src.read_bytes()));checks=[replay(C,ch)for ch in range(4)]
    need(all(not x['bad_outputs']for x in checks),'complete polynomial caller endpoint')
    need(all(x['final_max_stage_degree']==1 for x in checks),'each final stage appears once')
    counts=Counter(e[0]for e in C['events']);a=C['arms'];b=C['body_dimension']
    need(counts==C['counts'],'literal operation inventory')
    need(counts['HOST2']==2*a and counts['QUERY']==4 and counts['IDLE_ONE']==4*(a-1),'source profile')
    T=Counter(1+b*len(x['stages'])for x in C['endpoint']);P=Counter({1:4})
    for e in C['events']:
        if e[0]=='IDLE_ONE':P[b*len(e[2])]+=1
    need(T=={int(k):v for k,v in C['wrapper_invoice_per_port']['T'].items()}and P=={int(k):v for k,v in C['wrapper_invoice_per_port']['P'].items()},'recounted whole jobs')
    controls={}
    for op in('HOST2','QUERY','IDLE_ONE','LAMBDA','ADD'):
        where=next((i for i,e in enumerate(C['events'])if e[0]==op),None)
        if where is None:continue
        bad=[replay(C,ch,skip=where)['bad_outputs']for ch in range(4)]
        need(any(bad),'deleted actual '+op+' must fail');controls[op]=dict(event=where,bad_counts=list(map(len,bad)))
    result=dict(status='PASS_EXACT_SHORT_CALLER',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
                arms=a,stages=2*a,native_dimension=b+1,ambient_cap=C['ambient_cap'],roles=C['roles'],
                literal_counts=dict(sorted(counts.items())),formal_character_checks=checks,controls=controls,
                wrapper_invoice_per_port=dict(T=dict(sorted(T.items())),P=dict(sorted(P.items()))),
                scope='Formal complete caller on arbitrary independent arrays conditional on each exact HOST2 macro, ordinary LAMBDA and full-job physical contracts. No higher-label native source or new kappa.')
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:result[k]for k in('status','stages','roles','literal_counts')},sort_keys=True))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('caller',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();main(a.caller,a.out)
