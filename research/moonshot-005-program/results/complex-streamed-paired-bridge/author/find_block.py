#!/usr/bin/env python3
"""Find an actual native C5/D6 bridge block, preserving all source interfaces."""
from pathlib import Path
from fractions import Fraction as F
import argparse,gzip,json,itertools,time

def need(ok,msg):
 if not ok:raise ValueError(msg)
def span(bs):
 s={0}
 for b in bs:s|={v^b for v in tuple(s)}
 return s
def basis(vs):
 d={}
 for v in vs:
  for j in sorted(d,reverse=True):
   if v>>j&1:v^=d[j]
  if v:
   j=v.bit_length()-1
   for k in d:
    if d[k]>>j&1:d[k]^=v
   d[j]=v
 return tuple(d[j]for j in sorted(d,reverse=True))
def rank(A):
 rows={}
 for row in A:
  r=list(map(F,row))
  for i,v in rows.items():
   if r[i]:
    c=r[i];r=[x-c*y for x,y in zip(r,v)]
  if any(r):
   p=next(i for i,x in enumerate(r)if x);c=r[p];rows[p]=[x/c for x in r]
 return len(rows)
def root(v):
 on=[i for i in range(9)if v>>i&1]
 if len(on)==3:return [2 if i in on else -1 for i in range(9)]
 off=[i for i in range(9)if not(v>>i&1)];need(len(off)==2,'native root');return [3*(int(i==off[0])-int(i==off[1]))for i in range(9)]
def main(a):
 start=time.monotonic();n=json.loads(gzip.decompress(a.native.read_bytes()));w=json.loads(gzip.decompress(a.seed.read_bytes()));ports=n['live'];host=sorted(n['live'][i]for i in n['hosted']['Dports']);vec={h:n['frames'][n['initial'][h]][0]for h in ports};roots={h:root(vec[h])for h in ports};gram={(h,j):F(sum(x*y for x,y in zip(roots[h],roots[j])),18)for h in ports for j in ports};c3={h:tuple(g['C_frame'])for g in w['duplex']['groups']for h in g['ports']}
 subspaces={basis(vs)for vs in itertools.combinations(range(1,64),3)};subspaces={bs for bs in subspaces if len(bs)==3};need(len(subspaces)==1395,'complete quotient three-flat census')
 Ds=set()
 for group in w['duplex']['groups']:
  base=group['C_frame'];known=span(base);ext=[]
  for v in range(1,512):
   if v not in known:ext.append(v);known|={x^v for x in tuple(known)}
  need(len(ext)==6,'six-dimensional quotient')
  def lift(q):
   r=0
   for i,x in enumerate(ext):
    if q>>i&1:r^=x
   return r
  for bs in subspaces:Ds.add(basis([*base,*[lift(x)for x in bs]]))
 best={};eligible_D=0;candidate_count=0;rank_hist={}
 for db in sorted(Ds):
  ds=span(db);T=[h for h in host if all(z in ds for z in c3[h])and all((vec[h]&z).bit_count()%2==0 for z in db)]
  if len(T)<2:continue
  eligible_D+=1
  # Every codimension-one subspace of this D, with no repeated normal.
  table=[]
  for mask in range(64):
   v=0
   for j,x in enumerate(db):
    if mask>>j&1:v^=x
   table.append(v)
  for normal in range(1,64):
   cs={v for mask,v in enumerate(table)if (normal&mask).bit_count()%2==0};J=[j for j in host if vec[j]in cs]
   if not J:continue
   Fmat=[[-gram[h,j]for j in J]for h in T];r=rank(Fmat);candidate_count+=1;rank_hist[r]=rank_hist.get(r,0)+1
   if not(1<=r<=3):continue
   pairs=sum(bool(x)for row in Fmat for x in row)
   # Complete optimistic per-source movement relative to the seed, with all
   # raw stop refinements and the 2r+1 single-carrier bridge included.
   t=.995;increment=(2*r+1)+2*len(J)*(2*4**t-8**t)+2*len(T)*(3**t+2**t-5**t)
   if increment>=8.843518963022781:continue
   score=(pairs,-increment)
   if r not in best or score>tuple(best[r]['score']):best[r]={'rank':r,'donors':J,'receivers':T,'C':list(basis(cs)),'D':list(db),'F':[[str(x)for x in row]for row in Fmat],'pairs':pairs,'raw_donor_count':len(J),'raw_receiver_count':len(T),'optimistic_increment_float':increment,'optimistic_remaining_float':8.843518963022781-increment,'score':score,'scope':'Finite explicit geometry candidate and float screen; exact word, caller intervals and source obligations remain.'}
 out={'status':'FINITE_NATIVE_STREAMING_BRIDGE_CANDIDATES','all_D_count':len(Ds),'eligible_D_count':eligible_D,'C_D_blocks_examined':candidate_count,'rank_distribution':rank_hist,'elapsed_seconds':time.monotonic()-start,'best_by_rank':best};a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--seed',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
