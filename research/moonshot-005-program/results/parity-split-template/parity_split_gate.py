#!/usr/bin/env python3
"""Exact parity-complement geometry and one-arrival rigidity checks."""
import argparse,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from cohort_geometry import SOURCE_PIN,space,root,rank,require
from check_cohort_word import load,sha,PARENT_PIN,PARENT_PAYLOAD

def binary_basis(values):
 pivots={};chosen=[]
 for label,value in values:
  x=value
  while x:
   bit=x.bit_length()-1
   if bit in pivots:x^=pivots[bit]
   else:pivots[bit]=x;chosen.append(label);break
 return chosen

def main(a):
 source=load(a.source,True,SOURCE_PIN);parent=load(a.source.parents[2]/'moonshot-005-program/results/eight-packet-seven-corrections-fused/WORD.json.gz',True,PARENT_PIN,PARENT_PAYLOAD)
 X=sorted(source['live']);L={i:source['frames'][source['initial'][i]][0] for i in X};V={i:root(L[i]) for i in X};ell=511
 hosted={X[i] for i in source['hosted']['Dports']};counts=Counter();residual_counts=Counter();sizes=Counter();cases=[];packet_checks=[]
 for i in X:
  Fi=space(source['frames'][source['final'][i+112]]);require(len(Fi)==256 and Fi=={z for z in range(512) if (L[i]&z).bit_count()%2==0},'actual polar final facet')
  require(all(L[j].bit_count()%2==1 for j in X),'all source donor lines are odd')
  gram=lambda j:sum(x*y for x,y in zip(V[i],V[j]))
  N=[j for j in X if L[j] in Fi]
  require(len(N)==48 and set(N)=={j for j in X if j!=i and gram(j)},'48 exact residual support lines')
  forbidden=[j for j in X if L[j] not in Fi and j!=i]
  require(rank([V[j] for j in forbidden])==7 and all(gram(j)==0 for j in forbidden) and sum(v*v for v in V[i])==8,'forced global Gram decoder from forbidden-source constraints')
  packet_checks.append(dict(receiver=i+112,forbidden_source_count=len(forbidden),forbidden_root_rank=7))
  corrections=parent['corrections'].get(str(i+112),[]);scale=F(1) if i in hosted else F(1,2)
  for j,c in corrections:require(j in N and F(c)==-scale*F(gram(j),8),'every inherited paid cancellation is an exact source residual term')
  omitted={j for j,c in corrections};remaining=[j for j in N if j not in omitted]
  require(len(binary_basis([(j,L[j]) for j in N]))==8,'entire residual support spans the full final facet')
  checked=0
  for f in range(1,512):
   if f==L[i] or f>(f^L[i]):continue
   checked+=1;outside=[j for j in N if (f&L[j]).bit_count()%2];after=[j for j in remaining if (f&L[j]).bit_count()%2]
   b=binary_basis([(j,L[j]) for j in outside]);r=binary_basis([(j,L[j]) for j in after]);even=f in (ell,ell^L[i]);wanted=8 if even else 7
   require(len(b)==len(r)==wanted,'all full and paid-corrected complementary span ranks')
   if not even:require(all(((f^ell)&L[j]).bit_count()%2==0 for j in outside),'actual parity-complement containing every outside line')
   counts[len(b)]+=1;residual_counts[len(r)]+=1;sizes[len(outside)]+=1
   cases.append([i,f,even,b,r])
  require(checked==255,'all255 distinct hyperplanes of each final facet')
 # The source-dependent triple is the concrete complementary pair instance.
 require(L[0]^L[1]^L[98]==ell,'dependent triple binary parity identity')
 for i,j,k in ((0,1,98),(1,0,98),(98,0,1)):
  require(((L[j]^ell)^L[k])==L[i],'the two pair charts are parity complements inside the selected facet')
 # An explicit counterexample to the rejected full-span claim.
 i=0;f=L[1];outside=[j for j in X if L[j] in space(source['frames'][source['final'][112]]) and (f&L[j]).bit_count()%2]
 require(len(outside)==24 and len(binary_basis([(j,L[j]) for j in outside]))==7,'actual24-donor counterexample to universal rank8 outside every hyperplane')
 result=dict(status='PASS_ALL104_FACET_PARITY_COMPLEMENT_TEMPLATES',source_sha256=SOURCE_PIN,parent_sha256=PARENT_PIN,
             checker_sha256=sha(Path(__file__).read_bytes()),facets=104,hyperplanes_per_facet=255,total_hyperplane_cases=len(cases),
             full_residual_outside_rank_histogram=dict(counts),after_seven_paid_corrections_rank_histogram=dict(residual_counts),outside_population_histogram=dict(sizes),
             case_certificate_sha256=sha(json.dumps(cases,separators=(',',':')).encode()),forced_packet_decoder_checks=packet_checks,
             concrete_counterexample=dict(receiver_firstX=0,last_Y_chart_normal=L[1],complementary_chart_normal=L[98],outside_donors=outside,outside_rank=7),
             negative_controls=dict(false_universal_rank8_claim_rejected=True,even_hyperplane_is_rank8_exception=True,seven_inherited_corrections_do_not_change_rigidity=True),
             scope='Exact finite source support geometry. Under only monotone X carriers, local stationary caches, one Y accumulator per receiver and fixed paid Gram information, a one-X-arrival completion forces complementary dimension7 last charts. It is a necessary template, not a construction or an impossibility of all coded networks.')
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('forced_packet_decoder_checks','concrete_counterexample')},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
