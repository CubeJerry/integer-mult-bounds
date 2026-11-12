#!/usr/bin/env python3
"""Exact response and nullspace of all scalar-unit helper departures."""
import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def check(x,s):
    if not x:raise ValueError(s)
def add(a,b,c=F(1)):
    for k,v in tuple(b.items()):
        z=a.get(k,F(0))+c*v
        if z:a[k]=z
        else:a.pop(k,None)
def enc(a):return [[k,str(v)] for k,v in sorted(a.items())]
def rank_null(columns):
    basis={};null=[];piv=[]
    for i,row in columns:
        z=dict(row);expr={i:F(1)}
        for p,(b,e) in basis.items():
            if p in z:
                c=z[p];add(z,b,-c);add(expr,e,-c)
        if z:
            p=min(z);c=z[p];basis[p]=({j:v/c for j,v in z.items()},{j:v/c for j,v in expr.items()});piv.append([i,p,str(c)])
        else:null.append(enc(expr))
    return dict(rank=len(basis),pivots=piv,nullspace=null)
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--census',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
raw=args.source.read_bytes();check(hashlib.sha256(raw).hexdigest()==PIN,'native pin');w=json.loads(gzip.decompress(raw));C=json.loads(args.census.read_text());check(C['source_sha256']==PIN,'census source');cuts=C['events'];idx={a['event']:i for i,a in enumerate(cuts)}
R=[{} for _ in range(w['public']+w['owned_fields'])];L=[];guards=[];coef={}
def scalar(s):
    if s not in coef:coef[s]=F(s)
    return coef[s]
for t,x in enumerate(w['program']):
    op,d,s=x[:3]
    if t in idx:
        i=idx[t];check(d==cuts[i]['helper'],'cut helper');L.append(dict(R[d]));R[d][i]=R[d].get(i,F(0))+1
    if op=='ADD':add(R[d],R[s],scalar(x[3]))
    elif op=='SCALE':R[d]={k:scalar(s)*v for k,v in R[d].items() if scalar(s)*v}
    elif op=='COPY':guards.append(enc(R[d]));R[d]={k:scalar(x[3])*v for k,v in R[s].items()}
    elif op in ('INIT','CLEAR'):R[d]={}
Z=[{} for _ in cuts]
for j in range(w['public']):
    if w['final'][j]!=127:
        for k,v in R[j].items():Z[k][j]=v
for a in cuts:
    i=idx[a['event']];a['own_final_Y_response']=str(Z[i].get(a['donor']+112,F(0)));a['offhub_support']=len(Z[i])
accessible=[i for i,a in enumerate(cuts) if a['donor_access']];nonzero=[i for i in accessible if Z[i]]
families={name:rank_null([(i,Z[i]) for i in I]) for name,I in [('all38',list(range(len(cuts)))),('accessible37',accessible),('accessible_nonzero',nonzero)]}
for f in families.values():
    for n in f['nullspace']:
        out={}
        for i,c in n:add(out,Z[i],F(c))
        check(not out,'nullspace check')
out=dict(schema='all-source-unit-helper-response-v1',source_sha256=PIN,census_sha256=hashlib.sha256(args.census.read_bytes()).hexdigest(),cuts=cuts,chronological_L=[enc(a) for a in L],offhub_columns=[enc(a) for a in Z],copy_guard_responses=guards,families=families,status='Exact complete scalar-unit helper family response, not a global controller obstruction.')
payload=(json.dumps(out,indent=2,sort_keys=True)+'\n').encode();args.output.write_bytes(gzip.compress(payload,mtime=0) if args.output.suffix=='.gz' else payload)
print(json.dumps(dict(ranks={k:v['rank'] for k,v in families.items()},accessible_nonzero=len(nonzero),zero_columns=[a['event'] for i,a in enumerate(cuts) if not Z[i]],nonzero_own_Y=sum(a['own_final_Y_response']!='0' for a in cuts),nullspace=families['accessible37']['nullspace']),sort_keys=True))
