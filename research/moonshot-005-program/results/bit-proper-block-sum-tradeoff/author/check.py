#!/usr/bin/env python3
import argparse,hashlib,json
from pathlib import Path
from itertools import combinations
from collections import Counter
PIN='012018d59ce8227282749100b26eef2d3a4013dbb04d48d0bca030f3c036c963'

def rank(rows):
 p={}
 for v in rows:
  while v:
   j=v.bit_length()-1
   if j not in p:p[j]=v;break
   v^=p[j]
 return len(p)
def dot(a,b):return (a&b).bit_count()%2
def inverse(rows):
 a=[v|(1<<(9+i))for i,v in enumerate(rows)]
 for j in range(9):
  p=next(i for i in range(j,9)if a[i]>>j&1);a[j],a[p]=a[p],a[j]
  for i in range(9):
   if i!=j and a[i]>>j&1:a[i]^=a[j]
 assert [x&511 for x in a]==[1<<i for i in range(9)]
 return [x>>9 for x in a]
def complete(D,P):
 k=len(D);ev=lambda v:sum(dot(v,d)<<i for i,d in enumerate(D))
 Q=[]
 for i in range(k):
  candidates=[v for v in P if ev(v)==1<<i]
  Q.append(candidates[0]if candidates else next(v for v in range(1,512)if ev(v)==1<<i))
 ker=[]
 for v in P+list(range(1,512)):
  if ev(v)==0 and rank(ker+[v])>len(ker):ker.append(v)
  if len(ker)==9-k:break
 Q+=ker;assert len(Q)==9 and rank(Q)==9
 inv=inverse(Q);fullD=[sum(((inv[j]>>i)&1)<<j for j in range(9))for i in range(9)]
 assert fullD[:k]==list(D)
 assert all(dot(x,y)==int(i==j)for i,x in enumerate(fullD)for j,y in enumerate(Q))
 return {'decoder_basis':fullD,'payload_basis':Q,'proper_decoders':sum(v in P for v in fullD),'proper_payloads':sum(v in P for v in Q)}
def main():
 p=argparse.ArgumentParser();p.add_argument('--support',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 raw=a.support.read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN
 words=json.loads(raw)['all_nonzero_words'];P=sorted(w['binary_code_mask']for w in words if w['real_support_rank']==7);assert len(P)==25
 pairs=[[dot(x,y)for y in P]for x in P];results=[]
 for k,ceiling in [(3,7),(4,7),(5,6),(6,5)]:
  hist=Counter();best=-1;witness=None;tested=0
  for ids in combinations(range(25),k):
   tested+=1;D=[P[i]for i in ids]
   if rank(D)!=k:continue
   singles=0;zero=[]
   for t,v in enumerate(P):
    z=sum(pairs[i][t]<<j for j,i in enumerate(ids))
    if not z:zero.append(v)
    elif z&(z-1)==0:singles|=z
   score=singles.bit_count()+rank(zero);hist[score]+=1
   assert score<=ceiling
   if score>best:best=score;witness=D
  assert best==ceiling
  result={'proper_decoder_subset_size':k,'all_subsets':tested,'independent_subsets':sum(hist.values()),'maximum_proper_payloads':best,'histogram':dict(sorted(hist.items())),'tight_completed_basis':complete(witness,P)}
  results.append(result);print(k,best,flush=True)
 assert any(r['tight_completed_basis']['proper_decoders']+r['tight_completed_basis']['proper_payloads']==11 for r in results)
 result={'status':'PASS_PROPER_DECODER_PAYLOAD_SUM_BOUND_ELEVEN','support_sha256':PIN,'proper_directions':P,'subset_certificates':results,'sharp_sum_bound':11,'scope':'One paid copy, exactly nine receiver-downset records, arbitrary positive V and characteristic-two vertex gauges. p counts nonzero-line events; q counts rank-seven payload supports. No b>1 scaling or formation tariff.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
