#!/usr/bin/env python3
"""Exact actual-BIT nine-frame witness and attained binary fitting rank."""
import argparse, collections, gzip, hashlib, json
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
FRAMES=[[0,16,17,32,36,38,67,71],[0,16,17,32,36,39,68,72],
 [0,16,17,36,37,63,71,72],[0,16,17,36,38,39,62,63],
 [1,8,9,30,37,46,73,77],[1,8,9,30,37,47,74,78],
 [1,8,9,36,37,65,73,74],[1,8,9,37,46,47,64,65],
 [36,37,62,64,67,68,77,78]]
def need(ok,why):
 if not ok:raise ValueError(why)
def rank_basis(rows):
 basis={};selected=[]
 for index,row in enumerate(rows):
  while row:
   p=row.bit_length()-1
   if p not in basis:basis[p]=row;selected.append(index);break
   row^=basis[p]
 return basis,selected
def main(a):
 raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'Exact native pin')
 s=json.loads(gzip.decompress(raw));ff={int(k):v for k,v in s['frames'].items()};roots=[[F(x) for x in ff[s['start'][i]]['B'][0]] for i in range(111)];dot=lambda u,v:sum(x*y for x,y in zip(u,v))
 for i in range(111):
  facet=ff[s['final'][111+i]];need(ff[s['start'][i]]['dim']==1 and facet['dim']==7,'Line/facet dimensions');need(all(dot(roots[i],[F(x) for x in row])==0 for row in facet['B']),'Actual orthogonal final facet')
 normalized=[]
 for r in roots:
  n=dot(r,r);need(n in (1,4),'Source root norm');normalized.append([int(x*(2 if n==1 else 1)) for x in r])
 need(all(dot(r,r)==4 for r in normalized),'Doubled unit roots')
 def parity_check(frames):
  if len(frames)%2==0:return False
  counts=collections.Counter()
  for frame in frames:
   if len(frame)!=8 or len(set(frame))!=8 or any(i not in range(111) for i in frame):return False
   if any(dot(roots[i],roots[j])==0 for i in frame for j in frame):return False
   counts.update(frame)
  return all(x%2==0 for x in counts.values())
 need(parity_check(FRAMES),'Actual nonorthogonal parity witness');counts=collections.Counter(i for f in FRAMES for i in f);need(collections.Counter(counts.values())=={2:18,4:6,6:2},'Multiplicity histogram')
 rows=[];brows=[]
 for i in range(111):
  row=brow=0
  for j in range(111):
   inner=dot(normalized[i],normalized[j]);need(inner%2==0,'Even inner products');bit=(inner//2)&1;brow|=bit<<j;row|=(1^bit)<<j;need(i==j or (1^bit)==int(inner==0),'Fitting supported on actual contacts')
  need(row>>i&1,'Identity diagonal');rows.append(row);brows.append(brow)
 kb,selected=rank_basis(rows);bb,_=rank_basis(brows);need(len(kb)==9 and len(bb)==8,'Attained binary fitting ranks');columns=sorted(kb,reverse=True)
 minor=[sum(((rows[i]>>j)&1)<<k for k,j in enumerate(columns)) for i in selected];need(len(rank_basis(minor)[0])==9,'Explicit nonsingular9-minor')
 need(not parity_check(FRAMES[:-1]),'Even frame collection rejected');duplicate=[f[:] for f in FRAMES];duplicate[0][0]=duplicate[0][1];need(not parity_check(duplicate),'Duplicate role rejected')
 bad=next(i for i in range(111) if i not in FRAMES[0] and any(dot(roots[i],roots[j])==0 for j in FRAMES[0][1:]));orthogonal=[f[:] for f in FRAMES];orthogonal[0][0]=bad;need(not parity_check(orthogonal),'Hosted orthogonal replacement rejected')
 out={'status':'PASS_ACTUAL_BIT_ATTAINED_MINIMUM_RANK_NINE_CERTIFICATE','native_sha256':PIN,'source_ports':111,'frames_pairwise_REAL_NONorthogonal':FRAMES,'frames_source_start_charts':[[s['start'][i] for i in f] for f in FRAMES],'ordered_frame_inner_product_checks':576,'root_multiplicity_by_role':dict(sorted(counts.items())),'multiplicity_histogram':dict(sorted(collections.Counter(counts.values()).items())),'binary_Gram_rank':len(bb),'attained_fitting_rank':len(kb),'attaining_fitting_rows':rows,'nonsingular_minor_row_indices':selected,'nonsingular_minor_column_indices':columns,'negative_controls':{'deleted_frame':True,'duplicate_role':True,'orthogonal_replacement':True},'all_volume_theorem':'Minimum block fitting rank is exactly9V for every characteristic-two field and V>=1 on this actual BIT contact graph.','scope':'Fitting rank and stated monotone-network cut consequence only; no minimal physical price, complete native, supplier or new kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','source_ports','multiplicity_histogram','binary_Gram_rank','attained_fitting_rank','all_volume_theorem']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
