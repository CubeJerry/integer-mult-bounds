#!/usr/bin/env python3
"""Authenticate actual R0 words and enclose the remaining two-bank moment."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from collections import Counter
import argparse,gzip,hashlib,json,sys
sys.dont_write_bytecode=True
import check_routes as routes
HERE=Path(__file__).resolve().parent;DEN=10**45
PINS={'R0-WORD.json.gz':'d27892c4934f9b6fa08fd10b53a665f455020e6711db9378ab01f439ede2c56c','R0-MINIMAL-WORD.json.gz':'c06724af5a2c414e62887ea78124d268cad2cabf500f9963ad5d0e9758c8a336'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
@lru_cache(None)
def p(r):
 if r in(0,1):return F(r),F(r)
 z=r**199*DEN**200;x=1<<((z.bit_length()+199)//200)
 while True:
  y=(199*x+z//x**199)//200
  if y>=x:break
  x=y
 while x**200>z:x-=1
 while(x+1)**200<=z:x+=1
 need(x**200<=z<(x+1)**200,'root enclosure')
 return F(x,DEN),F(x+1,DEN)
def add(*xs):return sum(x[0]for x in xs),sum(x[1]for x in xs)
def mul(a,x):
 a=F(a);return(a*x[0],a*x[1])if a>=0 else(a*x[1],a*x[0])
def sub(x,y):return add(x,mul(-1,y))
def show(x):return {'rational_interval':list(map(str,x)),'approximate':[float(y)for y in x]}
def W(a):return add(mul(2,p(1+16*a)),*(mul(4,p(1+8*j))for j in range(1,a+1)),mul(-4,p(1)),*(mul(-4,p(8*j))for j in range(1,a)))
def basis(vs):
 B={}
 for v in vs:
  while v:
   k=v.bit_length()-1
   if k in B:v^=B[k]
   else:B[k]=v;break
 return B
def inside(v,B):
 while v:
  k=v.bit_length()-1
  if k not in B:return False
  v^=B[k]
 return True
def invoice(w):
 need(w['public']==448 and w['owned_fields']==0,'four arbitrary public banks and no owners')
 loc=list(w['initial']);profile=Counter();adds=0
 for e in w['program']:
  if e[0]=='MOVE':
   _,h,old_id,f,owned=e;need(old_id==loc[h] and not owned,'actual source location and raw move');old=w['frames'][old_id];new=w['frames'][f]
   a,b=(old,new)if len(old)<=len(new)else(new,old)
   need(all(inside(x,basis(b))for x in a),'nested actual move')
   r=abs(len(old)-len(new));need(r>0,'positive actual move rank')
   profile[r]+=1;loc[h]=f
  else:
   need(e[0]=='ADD','source alphabet');need(loc[e[1]]==loc[e[2]],'actual cocharted ADD');adds+=1
 need(loc==w['final']and adds==896,'full endpoints and ADD count')
 return dict(sorted(profile.items()))
def main(out):
 source={};words={}
 expected={'R0-WORD.json.gz':{3:224,4:448,5:224},'R0-MINIMAL-WORD.json.gz':{2:224,3:224,5:224,6:224}}
 allowance=mul(F(112,12),W(6))
 need(sub(mul(5,W(6)),mul(6,W(5)))[0]>0 and sub(mul(6,W(7)),mul(7,W(6)))[1]<0,'all-arm unique maximum at a6, with concavity proof')
 for name,sha in PINS.items():
  raw=(HERE/'source'/name).read_bytes();need(hashlib.sha256(raw).hexdigest()==sha,'actual word pin')
  w=json.loads(gzip.decompress(raw));words[name]=w;H=invoice(w);need(H==expected[name],'exact actual invoice')
  Q=add(*(mul(n,p(r))for r,n in H.items()));slack=sub(allowance,Q);need(slack[0]>0,'positive conditional room')
  source[name]={'sha256':sha,'profile':H,'moment':show(Q),'two_bank_ceiling':show(slack),'single_bank_ceiling':show(mul(F(1,2),slack))}
 x,y=words.values();need(routes.actual_R(x)==routes.actual_R(y),'same literal paired R0 rows')
 need(x['logical_involution']['role_map']==y['logical_involution']['role_map'],'same public roles')
 for key in ['initial','final']:
  need([x['frames'][f]for f in x[key]]==[y['frames'][f]for f in y[key]],'same actual boundary frames')
 R={'status':'PASS_ACTUAL_R0_TWO_NORMALIZER_TARGET_BUDGET','t':'199/200','best_stages':12,'per_native_allowance':show(allowance),'sources':source,
 'strict_requirement':'two independent N-bank implementation moments plus every other new net expense < source-specific two_bank_ceiling',
 'service':'N=Q^-1 R0 Q on112 arbitrary coindexed arrays; no service constructed',
 'scope':'Exact source invoices and conditional raw target budget. Uniform compiler, ordinary service, precision, BIT compatibility and all foundational assumptions remain. No new kappa.'}
 out.write_text(json.dumps(R,indent=2,sort_keys=True)+'\n');print(R['status'])
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=HERE/'BUDGET.json');main(a.parse_args().out)
