#!/usr/bin/env python3
"""Fresh sparse rational replay of the two closed 416-column handoffs.
No author replay or scientific-module imports. Nonzero owned CLEAR remains
an inherited erasure assumption; it is counted and never reported as proved.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import gzip,json,hashlib,argparse,copy
HERE=Path(__file__).resolve().parent
PINS={'complete-allhosted':'3dec380d820ed631636bdc77adb4a4c3e35abdb31d2b312f8f41edadff389d96',
 'gram':'721949af97ebb48344437477c99b7b1dcc8f1e52811a1ed80c8b683b3ef46f0d',
 'parity':'f212f5fb73979e4c9842883e84435805d3ea87147e53afe322015019f6d21d22'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def load(name):
 raw=(HERE/'source'/f'{name}.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==PINS[name],'source pin '+name)
 return json.loads(gzip.decompress(raw))
def basis(rows):
 B={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in B:x^=B[p]
   else:B[p]=x;break
 return B
def included(A,B):
 for x in A.values():
  while x:
   p=x.bit_length()-1
   if p not in B:return False
   x^=B[p]
 return True
def add(a,b,c):
 out=dict(a)
 for j,v in b.items():
  w=out.get(j,F(0))+c*v
  if w:out[j]=w
  else:out.pop(j,None)
 return out
def rank(rows):
 B={}
 for raw in rows:
  row=dict(raw)
  while row:
   p=min(row);a=row[p]
   if p in B:row=add(row,B[p],-a)
   else:B[p]={j:v/a for j,v in row.items()};break
 return len(B)
def run(w):
 n=w['public'];need(n==416,'416 independent inputs')
 rows={i:{i:F(1)}for i in range(n)};loc=dict(enumerate(w['initial']))
 charts=[basis(v)for v in w['frames']];moves=Counter();counts=Counter();dirty=0;lifetimes=0
 for op in w['program']:
  ty,d=op[:2];counts[ty]+=1
  if ty=='INIT':
   need(d>=n and d not in loc,'zero-owned birth');rows[d]={};loc[d]=op[2];lifetimes+=1
  elif ty=='CLEAR':
   need(d>=n and loc.get(d)==op[2],'owned retirement');dirty+=bool(rows[d]);del rows[d];del loc[d]
  elif ty=='MOVE':
   src,dst,owned=op[2:];need(loc.get(d)==src and owned==(d>=n),'move location/ownership')
   A,B=charts[src],charts[dst];up=included(A,B)and len(A)<len(B);down=included(B,A)and len(B)<len(A)
   need(up or owned and down,'literal nested source move');moves[abs(len(A)-len(B))]+=1;loc[d]=dst
  elif ty=='ADD':
   s,c,at=op[2:];need(d!=s and loc.get(d)==loc.get(s)==at,'cocharted add');rows[d]=add(rows[d],rows[s],F(c))
  elif ty=='SCALE':
   c,at=op[2:];need(loc.get(d)==at and F(c)!=0,'nonzero cocharted scale');rows[d]={j:F(c)*v for j,v in rows[d].items()}
  else:raise ValueError('unknown opcode '+ty)
 need(set(rows)==set(range(n)),'no live owners at closed handoff')
 need(loc==dict(enumerate(w['final'])),'literal public final charts')
 return rows,charts,dict(sorted(moves.items())),dict(counts),dirty,lifetimes
def endpoint(w,rows,charts,native):
 maprole={int(k):v for k,v in w['source_role_map'].items()};live=native['live']
 H=native['hosted'];need(H['Dports']==list(range(104)),'all actual ports hosted')
 X=[maprole[h]for h in live];Y=[maprole[112+h]for h in live]
 U=[maprole[h]for h in H['X2']];D=[maprole[h]for h in H['Y2']]
 need(len(set(X+Y+U+D))==416,'four independent role cohorts')
 for x,u,y,d in zip(X,U,Y,D):
  need(rows[x]=={x:F(1)}and rows[d]=={d:F(1)},'original X and D restored')
  need(len(charts[w['final'][x]])==len(charts[w['final'][u]])==9,'X/U at Hub')
  need(len(charts[w['final'][y]])==len(charts[w['final'][d]])==8,'Y/D at proper facets')
 K=[]
 for y in Y:
  row=dict(rows[y]);need(row.pop(y,None)==1 and set(row)<=set(X),'forward pure shear')
  K.append([row.get(x,F(0))for x in X])
 for j,u in enumerate(U):
  want={u:F(1)};want.update({d:-K[i][j]for i,d in enumerate(D)if K[i][j]})
  need(rows[u]==want,'all10816 paired transpose entries')
 R=[{j:F(i==j)-K[i][j]for j in range(104)if F(i==j)!=K[i][j]}for i in range(104)]
 r=rank(R);rt=rank([{i:R[i][j]for i in range(104)if j in R[i]}for j in range(104)])
 need(r==rt,'both directional cut ranks')
 return dict(roles={'X':X,'Y':Y,'U':U,'D':D},residual_rank_forward=r,residual_rank_reverse=rt,
  independent_public_rank=416,retained_owned_fields=0,complete_paired_entries=10816,
  residual_matrix_sha256=hashlib.sha256(json.dumps([[str(R[i].get(j,0))for j in range(104)]for i in range(104)],separators=(',',':')).encode()).hexdigest())
def main(out):
 native=load('complete-allhosted');receipts={};negative={}
 for name,want in [('gram',104),('parity',56)]:
  w=load(name);rows,charts,moves,counts,dirty,life=run(w);z=endpoint(w,rows,charts,native)
  need(z['residual_rank_forward']==want,'source-specific exact residual rank')
  z.update(source_sha256=PINS[name],moves=moves,operations=counts,dirty_erasure_retirements=dirty,lifetimes=life)
  receipts[name]=z
  bad=copy.deepcopy(w);i=next(i for i in range(len(bad['program'])-1,-1,-1)if bad['program'][i][0]=='ADD')
  bad['program'][i][3]=str(F(bad['program'][i][3])+1)
  try:
   rr,cc,*_=run(bad);endpoint(bad,rr,cc,native)
  except ValueError as e:negative[name+'_perturbed_last_add']=str(e)
  else:raise ValueError('paired negative control survived')
  bad=copy.deepcopy(w);i=next(i for i in range(len(bad['program'])-1,-1,-1)if bad['program'][i][0]=='CLEAR');bad['program'].pop(i)
  try:run(bad)
  except ValueError as e:negative[name+'_unretired_owned_record']=str(e)
  else:raise ValueError('live-owner negative control survived')
 R=dict(status='PASS_CLOSED_HANDOFF_SOURCE_REPLAY',sources=receipts,negative_controls=negative,
  scope='Exact finite rational replay on every public input. Dirty owned erasure remains an inherited assumption. The universal continuation theorem is in PROOF.md; no new kappa.')
 out.write_text(json.dumps(R,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v['residual_rank_forward']for k,v in receipts.items()}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=HERE/'REPLAY.json');main(p.parse_args().out)
