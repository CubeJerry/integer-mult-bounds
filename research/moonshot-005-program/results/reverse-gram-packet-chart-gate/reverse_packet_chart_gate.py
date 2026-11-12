#!/usr/bin/env python3
"""Exact all-chart availability gate for separate hosted reverse Gram packets.

All511 binary lines are checked. Modular nonzero minors certify rational lower
ranks; explicit rational root null vectors certify the24 rank-seven cases.
"""
import argparse,json
from itertools import combinations
from pathlib import Path
from fractions import Fraction as F
from cohort_geometry import SOURCE_PIN,root,space,require,rank
from check_cohort_word import load,sha,root_bounds

PRIME=101
def modular_basis(rows):
 pivots={};chosen=[]
 for label,row in rows:
  r=[int(v)%PRIME for v in row]
  for c,q in sorted(pivots.items()):
   t=r[c]
   if t:r=[(a-t*b)%PRIME for a,b in zip(r,q)]
  if any(r):
   c=next(i for i,v in enumerate(r) if v);u=pow(r[c],-1,PRIME)
   pivots[c]=[v*u%PRIME for v in r];chosen.append(label)
   if len(chosen)==8:break
 return chosen

def main(a):
 require(PRIME==101 and all(PRIME%d for d in range(2,11)),'prime used for exact modular minor certificates')
 s=load(a.source,True,SOURCE_PIN);xs=sorted(s['live']);H=[xs[i] for i in s['hosted']['Dports']]
 lines={x:s['frames'][s['initial'][x]][0] for x in H};V={x:root(lines[x]) for x in H};facets={x:space(s['frames'][s['final'][x+112]]) for x in H}
 for x in xs:
  line=s['frames'][s['initial'][x]][0]
  require(space(s['frames'][s['final'][x+112]])=={z for z in range(512) if (line&z).bit_count()%2==0},'all104 source facets are polar hyperplanes of initial lines')
 require(len(H)==len(set(lines.values()))==96 and rank(list(V.values()))==8,'96 distinct hosted lines and full root-row rank8')
 missing={z for z in range(1,512) if z.bit_count() in (3,7)}-set(lines.values())
 require(len(missing)==24,'all120 E8 root lines minus96 actual hosted lines')
 certificates=[];directions={}
 for z in range(1,512):
  unavailable=[x for x in H if z not in facets[x]];basis=modular_basis([(x,V[x]) for x in unavailable])
  if z in missing:
   w=root(z);require(len(basis)==7 and any(w) and all(sum(a*b for a,b in zip(w,V[x]))==0 for x in unavailable),'rank7 lower minor and exact upper null vector')
   sign=1 if next(v for v in w if v)>0 else -1;directions[z]=tuple(sign*v for v in w)
   certificate=dict(line=z,unavailable_hosted_count=len(unavailable),rational_rank=7,modular_basis= basis,available_root_functional=w,
                    nonzero_packet_terms=sum(bool(sum(a*b for a,b in zip(w,V[x]))) for x in H))
  else:
   require(len(basis)==8,'every other line has an exact nonzero rank8 modular minor')
   certificate=dict(line=z,unavailable_hosted_count=len(unavailable),rational_rank=8,modular_basis=basis)
  certificates.append(certificate)
 require(len(set(directions.values()))==24,'all24 line-available functional directions are distinct up to sign')
 # Every exceptional vector has norm8, so equality up to rational scaling
 # would be equality up to sign. Two distinct exceptional lines have no
 # common nonzero available Gram functional.
 for z,w in directions.items():require(sum(v*v for v in w)==8,'fixed root norm8')
 for z,t in combinations(directions,2):require(rank([directions[z],directions[t]])==2,'all276 exceptional-line pairs have zero common availability space')
 prior_pin='a0ad37e09f691e57128d0eda773aaeb3bea62a757759c7cba0059686cae9ea6e'
 prior=load(a.source.parents[2]/'moonshot-005-program/results/eight-packet-seven-corrections-fused/review/REVIEW-RESULT.json',pin=prior_pin)
 allowance=tuple(map(F,prior['conditional_remaining_exact_bounds']));price=tuple(8*v for v in root_bounds(8))
 require(price[0]>F(63) and allowance[1]<F(47) and price[0]>allowance[1],'strict separate-eight-packet target failure even at best nonzero acquisition lines')
 control_x=H[0];control_line=lines[control_x];w=V[control_x]
 require(control_line not in facets[control_x] and sum(a*b for a,b in zip(w,V[control_x]))==8,'own hosted diagonal prevents declaring its root line available')
 z=min(missing);wrong=root(z);wrong[0]+=1;bad=[x for x in H if z not in facets[x]]
 require(any(sum(a*b for a,b in zip(wrong,V[x])) for x in bad),'wrong exceptional functional rejected')
 result=dict(status='PASS_ALL511_LINE_GRAM_PACKET_AVAILABILITY_GATE',source_sha256=SOURCE_PIN,
             reviewer_sha256=sha(Path(__file__).read_bytes()),hosted_inputs=96,root_row_rank=8,field_scope='Rational coefficients and their characteristic-zero extensions.',
             proof_modulus=PRIME,polar_facet_identities=104,full_rank_lines=487,rank7_lines=24,exceptional_lines=sorted(missing),
             max_nonzero_acquisition_chart_dimension=1,exceptional_pair_checks=276,certificates=certificates,
             separate_global_packets_required=8,minimum_separate_packet_price_exact=[str(v) for v in price],minimum_separate_packet_price_approx=float(price[0]),
             parent_review_sha256=prior_pin,parent_remaining_native_moment_exact=[str(v) for v in allowance],
             optimistic_remaining_moment_upper=str(allowance[1]-price[0]),
             negative_controls=dict(own_hosted_root_line_has_unavailable_diagonal=True,wrong_exceptional_functional=True,two_distinct_exceptional_lines_have_no_shared_nonzero_functional=True),
             scope='Exact finite source availability theorem for separately formed complete Gram-rowspace packets, allowing every binary chart and free access to every unchanged original Y2 whose final facet contains that chart. It excludes an additional independent eight-packet return within the fixed parent invoice. Changed raw payloads, partial packet factors, shared already-funded carriers and changed common processing are outside this claim.')
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='certificates'},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
