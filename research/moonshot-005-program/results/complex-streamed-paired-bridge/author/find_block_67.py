#!/usr/bin/env python3
"""Exact receiver-pair C6/D7 candidates with full raw-stop float preflight."""
import argparse,gzip,json,itertools,importlib.util,time
from pathlib import Path
from fractions import Fraction as F
s=importlib.util.spec_from_file_location('geometry',Path(__file__).with_name('find_block.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def main(a):
 start=time.monotonic();n=json.loads(gzip.decompress(a.native.read_bytes()));w=json.loads(gzip.decompress(a.seed.read_bytes()));ports=n['live'];host=sorted(n['live'][i]for i in n['hosted']['Dports']);vec={h:n['frames'][n['initial'][h]][0]for h in ports};roots={h:g.root(vec[h])for h in ports};G={(h,j):F(sum(x*y for x,y in zip(roots[h],roots[j])),18)for h in ports for j in ports};c3={h:tuple(z['C_frame'])for z in w['duplex']['groups']for h in z['ports']};best={};count=0;Ds=0;hist={}
 for i,j in itertools.combinations(host,2):
  db=g.basis(v for v in range(512)if (v&vec[i]).bit_count()%2==0 and (v&vec[j]).bit_count()%2==0);ds=g.span(db)
  if not all(z in ds for h in [i,j]for z in c3[h]):continue
  g.need(len(db)==7,'two distinct receiver normals');Ds+=1;T=[i,j];table=[]
  for mask in range(128):
   v=0
   for k,b in enumerate(db):
    if mask>>k&1:v^=b
   table.append(v)
  for normal in range(1,128):
   cs={v for mask,v in enumerate(table)if (normal&mask).bit_count()%2==0};J=[h for h in host if vec[h]in cs]
   if not J:continue
   mat=[[-G[h,k]for k in J]for h in T];r=g.rank(mat);g.need(r in(1,2),'nonzero two-row block');hist[r]=hist.get(r,0)+1;count+=1
   t=.995;inc=2*r+1+2*len(J)*(5**t+3**t-8**t)+2*len(T)*(4**t+1-5**t);pairs=sum(bool(x)for row in mat for x in row);score=(pairs,-inc)
   if inc<8.843518963022781 and(r not in best or score>tuple(best[r]['score'])):best[r]={'rank':r,'donors':J,'receivers':T,'C':list(g.basis(cs)),'D':list(db),'F':[[str(x)for x in row]for row in mat],'pairs':pairs,'raw_donor_count':len(J),'raw_receiver_count':len(T),'optimistic_increment_float':inc,'optimistic_remaining_float':8.843518963022781-inc,'score':score,'scope':'Finite native geometry candidate with raw-stop float preflight; source and exact interval invoice remain.'}
 out={'status':'FINITE_NATIVE_C6_D7_STREAMING_CANDIDATES','D_count':Ds,'C_D_blocks_examined':count,'rank_distribution':hist,'elapsed_seconds':time.monotonic()-start,'best_by_rank':best};a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--seed',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
