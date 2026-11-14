#!/usr/bin/env python3
"""Independent all-input, actual-chart, history and residual-cut braid review."""
import argparse,copy,gzip,hashlib,importlib.util,json
from pathlib import Path
from fractions import Fraction as F
def load_module(p):
 s=importlib.util.spec_from_file_location('independent_occurrences',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main(a):
 e=load_module(a.engine);need=e.need
 need(e.digest(a.native)=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin')
 n=e.read(a.native);roots=[tuple(map(F,n['frames'][str(c)]['B'][0])) for c in n['start'][:111]]
 groups={}
 for i,v in enumerate(roots[8:],8):groups.setdefault((tuple(j for j,x in enumerate(v) if x),sum(x<0 for x in v)%2),[]).append(i)
 piv=[10,11,20,21,28,24,36,37,38,39,50,49,55,54,59,65,67,70,79,74,81,84,88,92,101,97,108,107]
 need(len(groups)==28 and all(p in g for p,g in zip(piv,groups.values())),'native halfclass pivots')
 K=[sum(1<<j for j,u in enumerate(roots) if i==j or sum(x*y for x,y in zip(v,u))==0) for i,v in enumerate(roots)]
 E=[]
 for row in K:
  z=row&~255
  for p,g in zip(piv,groups.values()):
   if row>>p&1:z^=sum(1<<j for j in g)
  E.append(z)
 B=[E[i] for i in (8,14,30)];need(e.rank(E)==e.rank(B)==3,'core rank')
 S=[92,36,54,38,55];need(e.rref([roots[i] for i in S]).__len__()==5,'independent five roots')
 for j,i in enumerate(S):
  for k,h in enumerate(S):
   if j!=k:need((sum(x*y for x,y in zip(roots[i],roots[h]))==0)==((j-k)%5 in [1,4]),'actual orthogonality C5')
 need(all(not (row>>i&1) for row in E for i in S),'core has no selected source columns')
 pins={'PARTIAL-WORD.json.gz':'6fce4f192725a564acde67081570f1cc0bc96ded56695a1197e6bee70ab0313a','CLOSED-WORD.json.gz':'2d533e3c061f829e67e5611d05a5e2297ec9a298a35b45f9d1cb221b983f126b'}
 words={};replays={};receipts={}
 def expected(w,re,closed):
  values={i:1<<i for i in range(222)}
  for i,row in enumerate(E):values[111+i]^=(1<<i) if i in S else row
  if not closed:
   for p,g in zip(piv,groups.values()):
    if p not in S:values[p]=sum(1<<j for j in g)
   values.update({222+j:1<<j for j in range(111)})
   values.update({336+j:row for j,row in enumerate(B)})
  need(re['val']==values,'complete public/owned output coefficient matrix')
  need(re['peak']==117,'actual peak117')
  need(dict(re['counts'])==({'INIT':122,'ADD':616,'MOVE':1598,'CLEAR':122} if closed else {'INIT':122,'ADD':555,'MOVE':756,'CLEAR':8}),'exact complete known invoice')
  if closed:need(w['final']==n['final'][:222] and len(re['loc'])==222,'native final charts and closure')
  else:
   need(all(re['loc'][222+j]==n['start'][j] for j in range(111)),'all111 pure point copies retained in place')
   need(all(re['loc'][336+j]==0 for j in range(3)),'three pure cores retained at ground')
   for i in S:need(re['loc'][i]==1 and re['loc'][111+i]==n['final'][111+i],'selected actual endpoints')
  need([(z[1],len(re['frames'][z[2]])) for z in re['clears'] if z[1] in [339,340,343]]==[(339,2),(340,2),(343,5)],'proper paid clone and reflection erasures')
 for name,pin in pins.items():
  p=a.bundle/name;need(e.digest(p)==pin,'frozen word pin');w=e.read(p);re=e.replay(w,n);closed=name.startswith('CLOSED');expected(w,re,closed)
  norm,G=e.normalize(w,n,re);need(norm['historical_x_rank']==8 and norm['historical_coordinates']==8,'actual eight-history rank')
  need(e.rank([z&((1<<111)-1) for z in G]+B+[1<<i for i in S])==8,'history X span is exactly three core plus five target coordinates')
  need(norm['owned_moves']==44 and norm['owned_downward_moves']==41 and norm['ground_arrivals']==5,'actual paid owned routes')
  receipts[name]=dict(counts=dict(re['counts']),peak_owned=re['peak'],live_owned=len(re['loc'])-222,normalization=norm)
  words[name]=w;replays[name]=re
 partial=replays['PARTIAL-WORD.json.gz'];word=words['PARTIAL-WORD.json.gz'];Cset=[8,9,14,15,30,31,59]
 facets=[e.rref(n['frames'][str(n['final'][111+i])]['B']) for i in Cset]
 inside=[row for i,row in partial['val'].items() if any(e.contained(partial['frames'][partial['loc'][i]],f) for f in facets)]
 target=[(1<<i)^(1<<(111+i)) for i in Cset]
 cut_before=e.rank(inside);cut_after=e.rank(inside+target)
 need((cut_before,cut_after)==(211,217),'actual residual conditional-information cut')
 y=[1<<i for i in range(111,222)];need(e.rank(inside+y+target)-e.rank(inside+y)==6,'same deficit even granting every original Y')
 controls=[]
 predicates=[('missing_reflection_copy',lambda o:o[:3]==['ADD',343,342]),('missing_return_swap',lambda o:o[:3]==['ADD',342,343]),('missing_local_mask_clone',lambda o:o[:3]==['ADD',339,258]),('missing_up_reflection',lambda o:o[0]=='MOVE' and o[1]==343 and len(partial['frames'][o[3]])>len(partial['frames'][o[2]])),('missing_down_reflection',lambda o:o[0]=='MOVE' and o[1]==343 and len(partial['frames'][o[3]])<len(partial['frames'][o[2]]))]
 for label,predicate in predicates:
  w=copy.deepcopy(words['CLOSED-WORD.json.gz']);k=next(j for j,o in enumerate(w['program']) if predicate(o));del w['program'][k]
  try:expected(w,e.replay(w,n),True)
  except (ValueError,KeyError):controls.append(label)
  else:raise ValueError('mutant accepted '+label)
 out=dict(status='PASS_INDEPENDENT_NATIVE_REFLECTED_C5_WORD_AND_RESIDUAL_CUT',native_sha256=e.digest(a.native),word_pins=pins,independent_engine_sha256=e.digest(a.engine),all_original_columns=222,all_native_final_chart_ids=222,receipts=receipts,remaining_cut=dict(receivers=Cset,inside_rank=cut_before,with_targets_rank=cut_after,deficit=6,all_original_Y_granted_deficit=6),negative_controls=controls,classification='Proved explicit partial scalar characteristic-two source with tensor identity lift; all222 endpoints checked against its stated partial map. No complete six-packet decoder.',new_kappa=None)
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(dict(status=out['status'],controls=len(controls),remaining_deficit=6,historical_rank=8)))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['native','bundle','engine','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
