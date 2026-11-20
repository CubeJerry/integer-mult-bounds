#!/usr/bin/env python3
"""Verify every ordinary RS anchor's forced quotient triangle, without discovery search."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations
import gzip,json
from pathlib import Path
import numpy as np

def need(ok,why):
 if not ok:raise ValueError(why)
def multiply(a,b):
 v=0
 while b:
  if b&1:v^=a
  a<<=1
  if a&64:a^=67
  b>>=1
 return v
M=np.array([[multiply(a,b)for b in range(64)]for a in range(64)],dtype=np.uint8)
INV=np.array([0]+[next(b for b in range(1,64)if M[a,b]==1)for a in range(1,64)],dtype=np.uint8)
def rank(matrix):
 a=np.asarray(matrix,dtype=np.uint8).copy();r=0
 for c in range(a.shape[1]):
  if r==len(a):break
  nz=np.flatnonzero(a[r:,c])
  if not len(nz):continue
  p=r+int(nz[0]);a[[r,p]]=a[[p,r]];a[r]=M[INV[a[r,c]],a[r]]
  a[r+1:]^=M[a[r+1:,c,None],a[r][None,:]];r+=1
 return r
def polynomial(nodes):
 p=np.array([1],dtype=np.uint8)
 for x in nodes:
  q=np.zeros(len(p)+1,dtype=np.uint8);q[:-1]^=M[x,p];q[1:]^=p;p=q
 return p
def evaluate(p,x):
 y=0
 for a in reversed(p):y=int(M[y,x])^int(a)
 return y

def main():
 cli=ArgumentParser(description=__doc__);cli.add_argument('--repo',type=Path,required=True);cli.add_argument('--out',type=Path,required=True);args=cli.parse_args()
 here=Path(__file__).resolve().parents[1];pins=json.loads((here/'SOURCE-PINS.json').read_text())
 for path,entry in pins['sources'].items():
  data=(args.repo/path).read_bytes();need(len(data)==entry['bytes']and sha256(data).hexdigest()==entry['sha256'],'source pin '+path)
 geometry=args.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
 g=json.loads(gzip.decompress(geometry.read_bytes()));roots=np.array(g['root_table'],dtype=np.int16);planes=[frozenset(p)for p in g['A2']];hid={p:h for h,p in enumerate(planes)}
 orth=roots@roots.T==0;stars=[[h for h,p in enumerate(planes)if j in p]for j in range(111)];nodes=[{h:q+1 for q,h in enumerate(star)}for star in stars]
 singleton={next(j for j in p if j<111)for p in planes if sum(j<111 for j in p)==1};ordinary=set(range(111))-singleton-{10}
 need(len(singleton)==11 and len(ordinary)==99 and all(len(v)==28 for v in stars),'actual source domain')
 need(set(np.sum(roots*roots,axis=1))=={4},'native root norm')
 root_id={tuple(map(int,r)):i for i,r in enumerate(roots)};root_id.update({tuple(map(int,-r)):i for i,r in enumerate(roots)})
 reflections={}
 for c in range(120):
  perm=[]
  for r in roots:
   dot=int(r@roots[c]);need(dot%2==0,'integral root reflection');image=r-(dot//2)*roots[c];need(tuple(map(int,image))in root_id,'reflected root exists');perm.append(root_id[tuple(map(int,image))])
  need(len(set(perm))==120 and all(perm[perm[t]]==t for t in range(120)),'true root-line involution');reflections[c]=perm
 visible=[[i for i in range(111)if all(orth[i,j]for j in p)]for p in planes]
 payload=gzip.decompress((here/'author/WITNESSES.json.gz').read_bytes());need(sha256(payload).hexdigest()==pins['witness_payload_sha256'],'exact compact witness payload');certificate=json.loads(payload)['witnesses']
 seen=set();propagations=0;span_hist=Counter();control=None;triangle_rows=[]
 def fibre(j,h,i):
  other=[q for q in stars[j]if q!=h and i in visible[q]];need(len(other)==15,'actual tight off-plane source fibre');return polynomial([nodes[j][q]for q in other])
 for row in certificate:
  j=row['anchor'];k,l=row['leaf_donors'];h1,h2,h3=row['centres'];i=row['final_receiver']
  need(j in ordinary and j not in seen and k in ordinary and l in ordinary and len({j,k,l})==3,'distinct eligible anchor and arbitrary leaf sources');seen.add(j)
  need({j,k}<=planes[h1]and{j,l}<=planes[h2]and{k,l}<=planes[h3]and len({h1,h2,h3})==3,'literal native triangle')
  need(i!=80 and i in visible[h3]and not orth[i,j]and i not in visible[h1]and i not in visible[h2],'final receiver avoids both anchor centres')
  final_sets=[]
  need(len(row['propagations'])==2,'both forced leaf stars')
  for block,(leaf,h)in zip(row['propagations'],[(k,h1),(l,h2)]):
   need(block['leaf']==leaf and block['centre']==h,'consistent propagation edge')
   expected={q for q in stars[leaf]if q!=h3 and i in visible[q]};need(len(expected)==15 and h not in expected,'fifteen known final off-plane quotients')
   entries=block['quotient_propagations'];need({e['leaf_plane']for e in entries}==expected and len(entries)==15,'every required final quotient certified')
   mapped=[];c=next(v for v in planes[h]if v not in(j,leaf));perm=reflections[c];need(perm[leaf]==j,'centre reflection exchanges donors')
   for e in entries:
    q,r=e['leaf_plane'],e['anchor_plane'];aud=e['receivers'];need(r in stars[j]and r!=h and q!=h,'ordinary off-centre quotient')
    need(hid[frozenset(perm[x]for x in planes[q])]==r,'native reflection transport of the plane')
    need(len(aud)==len(set(aud))==15 and 80 not in aud,'fifteen distinct admissible propagation receivers')
    need(all(a in visible[h]and a in visible[q]and a in visible[r]for a in aud),'all three genuine plane incidences')
    a=np.array([fibre(j,h,t)for t in aud],dtype=np.uint8)
    need(all(evaluate(p,nodes[j][r])==0 for p in a),'common anchor evaluation kernel')
    rho=rank(a);need(rho==e['rank']==15,'span is the complete fifteen-dimensional anchor quotient kernel');span_hist[rho]+=1;propagations+=1
    if control is None:
     fault=a.copy();fault[-1]=fault[0];need(rank(fault)==14,'duplicate propagation row loses rank');control={'anchor':j,'centre':h,'leaf_plane':q,'rank_after_duplicate':14}
    mapped.append(r)
   need(len(set(mapped))==15,'fifteen distinct anchor evaluation nodes');final_sets.append(mapped)
  need(final_sets==row['distinct_anchor_plane_sets'],'literal final source-plane sets')
  final=[polynomial([nodes[j][r]for r in v])for v in final_sets]
  need(rank(np.array(final))==row['final_fibre_rank']==2,'forced final fibre partitions are different')
  need(set(final_sets[0])!=set(final_sets[1]),'distinct monic annihilators')
  triangle_rows.append({'anchor':j,'leaves':[k,l],'centres':[h1,h2,h3],'receiver':i,'common_final_plane_count':len(set(final_sets[0])&set(final_sets[1]))})
 need(seen==ordinary and propagations==2970,'complete99-anchor and2970-propagation census')
 result={'status':'PASS_SINGLE_RS_ANCHOR_TRIANGLE_CENSUS','anchors':len(seen),'source_quotient_propagations':propagations,'independent_fibre_rows':15*propagations,'source_kernel_rank_counts':dict(span_hist),'actual_ordinary_anchor_ids':sorted(seen),'singleton_donors_excluded':sorted(singleton),'target_exceptional_donor_excluded':10,'target_exceptional_receiver_excluded':80,'triangle_witnesses':triangle_rows,'controls':[control],'all99_sources_must_change_under_stated_contract':True,'new_complete_kappa':False}
 args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],len(seen),propagations,flush=True)
if __name__=='__main__':main()
