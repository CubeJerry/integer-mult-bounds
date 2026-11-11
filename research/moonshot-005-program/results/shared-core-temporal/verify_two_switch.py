#!/usr/bin/env python3
"""Exact modular source certificate covering every pair of two-switch cuts."""
import argparse,bisect,gzip,hashlib,json,math
from fractions import Fraction as F
from pathlib import Path
P=1000003
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
SOURCE='research/shared-wire-split-composition/data/final.json.gz'
CUTS=[0,3625,5000,7000,8501,9539,10488,12000,12382,13000,14404,15493,16000,17000,19000,20000,20588,21000,22000,23000,24000,26000,27000,27416,29000,29918,32000,33530,35000,35857,37263,39000,40842,42000,42800,44661,45489,47000,49000,50000,50534,52000,53000,54000,55000,55325,56000,56404,57000,57494,58000,71261]
def need(p,m):
 if not p:raise ValueError(m)
def field(x):
 q=F(x);need(q.denominator%P!=0,'denominator prime');return q.numerator%P*pow(q.denominator,-1,P)%P
def add(a,b,q):
 for k,x in b.items():
  y=(a.get(k,0)+q*x)%P
  if y:a[k]=y
  else:a.pop(k,None)
def rank(rows):
 basis={}
 for original in rows:
  row=original.copy()
  while row:
   c=min(row);q=row[c]
   if c not in basis:
    iv=pow(q,-1,P);basis[c]={k:x*iv%P for k,x in row.items()};break
   add(row,basis[c],-q)
 return len(basis)
def run(path):
 raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin')
 need(all(P%d for d in range(2,math.isqrt(P)+1)),'prime proof')
 w=json.loads(gzip.decompress(raw));prog=w['program'];mains=sorted(set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));mi={r:i for i,r in enumerate(mains)};M=set(mains);n=w['public']+w['owned_fields'];N=len(mains)
 need(N==400 and len(prog)==CUTS[-1],'source domain')
 need(not any(e[1]in M and e[0]in('INIT','CLEAR','COPY') for e in prog),'invertible skeleton opcodes')
 need([i for i,e in enumerate(prog) if e[0]=='COPY']==[31737],'source COPY occurrence')
 need(prog[31736][0]=='INIT' and prog[31736][1]==prog[31737][1],'COPY immediately follows same-owner INIT')
 need(all(field(e[2])!=0 for e in prog if e[0]=='SCALE'and e[1]in M),'invertible skeleton scales')
 enc=[]
 for e in prog:
  q=field(e[2])if e[0]=='SCALE'else field(e[3])if e[0]in('ADD','COPY')else None
  enc.append((e,q))
 E=[{i:1}for i in range(N)];D=set(w['hosted']['Dports'])
 for i,x in enumerate(w['live']):
  y=x+112
  if i in D:E[mi[y]][mi[x]]=1
  else:E[mi[x]][mi[y]]=P-1;E[mi[y]]={mi[x]:field('1/2'),mi[y]:field('1/2')}
 for x,y in zip(w['hosted']['X2'],w['hosted']['Y2']):E[mi[x]][mi[y]]=P-1
 need(rank(E)==N,'target invertible');cutset=set(CUTS)
 def sweep(reverse=False,skeleton=False):
  a=[{}for _ in range(n)]
  for r,i in mi.items():a[r]={i:1}
  samples={len(prog)if reverse else 0:N}
  it=range(len(prog)-1,-1,-1)if reverse else range(len(prog))
  for i in it:
   e,q=enc[i];op=e[0];r=e[1]
   if skeleton and (r not in M or(op in('ADD','COPY')and e[2]not in M)):continue
   if op in('INIT','CLEAR'):a[r]={}
   elif op=='SCALE':a[r]={k:x*q%P for k,x in a[r].items()}
   elif op in('ADD','COPY'):
    if reverse:add(a[e[2]],a[r],q)
    else:add(a[r],a[e[2]],q)
   c=i if reverse else i+1
   if not skeleton and c in cutset:samples[c]=rank([a[r]for r in mains])
  return samples,[a[r]for r in mains]
 pre,full=sweep();post,back=sweep(True);_,R=sweep(skeleton=True)
 need(full==E,'whole-source main endpoint')
 ET=[{i:E[i][j]for i in range(N)if j in E[i]}for j in range(N)]
 need(back==ET,'reverse whole-source endpoint')
 residual=[]
 for e,r in zip(E,R):z=e.copy();add(z,r,-1);residual.append(z)
 rr=rank(residual);need(rr==275,'residual rank');need(rank(R)==N,'skeleton invertible')
 bounds={};coverage={}
 for name,reverse,samples in [('prefix',False,pre),('suffix',True,post)]:
  relevant=[i+1 for i,e in enumerate(prog)if e[0]in('ADD','COPY')and((e[2]in M and e[1]not in M)if reverse else(e[1]in M and e[2]not in M))]
  rows=[]
  for c,d in zip(CUTS,CUTS[1:]):
   count=bisect.bisect_right(relevant,d)-bisect.bisect_right(relevant,c)
   lower=(samples[c]+samples[d]-count+1)//2
   rows.append({'left':c,'right':d,'rank_left':samples[c],'rank_right':samples[d],'rank_changing_events':count,'all_cut_rank_lower':lower})
  bounds[name]=min(z['all_cut_rank_lower']for z in rows);coverage[name]=rows
 need(bounds['prefix']>=270 and bounds['suffix']>=270,'all-cut rank lower bounds')
 nullity_sum=2*N-bounds['prefix']-bounds['suffix'];need(nullity_sum<rr,'strict two-switch exclusion')
 need(rank([{0:1},{1:1}])==2 and rank([{}, {1:1}])==1,'rank-drop control')
 need((2+2-2+1)//2==1,'two-sided interpolation control')
 return {'status':'PASS_ALL_CUT_TWO_SWITCH_EXCLUSION','source_sha256':PIN,'prime':P,'prime_verified_by_trial_division':True,'main_dimension':N,'source_cuts_covered':len(prog)+1,'sample_cuts':CUTS,'prefix_ranks':pre,'suffix_ranks':post,'residual_rank_mod_p':rr,'all_cut_rank_lower_bounds':bounds,'all_pair_nullity_sum_upper':nullity_sum,'interval_coverage':coverage,'scope':'Rational rank lower bounds from exact modular arithmetic plus universal block proof; no H4 native and no new kappa.'}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--source',type=Path);args=a.parse_args();src=args.source
 if src is None:src=next((d/SOURCE for d in Path(__file__).resolve().parents if(d/SOURCE).is_file()),None)
 need(src is not None,'provide source path');print(json.dumps(run(src),indent=2))
