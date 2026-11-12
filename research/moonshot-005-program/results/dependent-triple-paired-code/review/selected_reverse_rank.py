#!/usr/bin/env python3
"""Independent source geometry and terminal-rank gate for selected reverse columns.

This proves an interface consequence, not existence of a source word realizing it.
"""
import argparse,json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
from cohort_geometry import SOURCE_PIN,FRAME,space,root,rank,bit_basis,require
from check_cohort_word import load,sha

def gram(roots,x,y):return sum(a*b for a,b in zip(roots[x],roots[y]))

def examine(source,selected):
 xs=sorted(source['live']);hosted=[xs[i] for i in source['hosted']['Dports']]
 require(set(selected)<=set(hosted),'all selected receivers have independent hosted dual roles')
 roots={x:root(source['frames'][source['initial'][x]][0]) for x in xs}
 S=list(selected);C=[x for x in hosted if x not in S]
 GSS=[[F(gram(roots,x,y)) for y in S] for x in S]
 A=[[F(x==y)-F(gram(roots,x,y),8) for y in hosted] for x in S]
 R=[[(-A[S.index(y)][hosted.index(x)] if y in S else F(0)) for y in hosted] for x in hosted]
 B=[[F(x==y)+R[i][j] for j,y in enumerate(hosted)] for i,x in enumerate(hosted)]
 require(all(B[hosted.index(x)][hosted.index(y)]==(F(gram(roots,x,y),8) if y in S else F(x==y)) for x in hosted for y in hosted),'exact selected-column residual interface')
 actual_rank=rank(B);formula=96-len(S)+rank(GSS)
 require(actual_rank==formula,'direct96-row rank agrees with block-elimination theorem')
 reduced=[row.copy() for row in B]
 for y in S:
  for x in C:
   c=B[hosted.index(x)][hosted.index(y)]
   if c:
    for i in range(96):reduced[i][hosted.index(y)]-=c*B[i][hosted.index(x)]
 for x in hosted:
  for y in hosted:
   want=F(gram(roots,x,y),8) if x in S and y in S else F(x==y) if x in C and y in C else F(0)
   require(reduced[hosted.index(x)][hosted.index(y)]==want,'explicit block diagonal column elimination')
 groups=defaultdict(list)
 for donor in xs:
  support=tuple(x for x in S if x!=donor and gram(roots,x,donor))
  if support:groups[support].append(donor)
 spans=[space(b) for b in source['frames']];geometry=[]
 for support,donors in sorted(groups.items()):
  Cspan=set.intersection(*(set(spans[source['final'][x+112]]) for x in support));basis=bit_basis(Cspan)
  require(all(spans[source['initial'][x]]<Cspan for x in donors),'each actual donor fits source acquisition intersection')
  hosts=[x for x in donors if x in hosted]
  rows=[[-F(gram(roots,x,d),8) for d in donors] for x in support]
  hrows=[[-F(gram(roots,x,d),8) for d in hosts] for x in support]
  geometry.append(dict(receivers=[x+112 for x in support],firstX_receivers=list(support),donors=donors,
                       hosted_donors=hosts,coupled_donors=sorted(set(donors)-set(hosts)),
                       intersection_basis=basis,intersection_dimension=len(basis),
                       source_chart_ids=[i for i,span in enumerate(spans) if span==Cspan],
                       full_aggregate_rank=rank(rows),hosted_aggregate_rank=rank(hrows)))
 result=dict(selected_firstX=S,selected_firstY=[x+112 for x in S],selected_gram=[[str(v) for v in row] for row in GSS],
             selected_root_rank=rank([roots[x] for x in S]),selected_gram_rank=rank(GSS),reverse_residual_rank=actual_rank,
             reverse_residual_nullity=96-actual_rank,groups=geometry,
             residual_matrix_sha256=sha(json.dumps([[str(v) for v in row] for row in B],separators=(',',':')).encode()))
 return result,B,hosted,roots

def main(a):
 source=load(a.source,True,SOURCE_PIN)
 prior_pin='a0ad37e09f691e57128d0eda773aaeb3bea62a757759c7cba0059686cae9ea6e'
 prior=load(a.source.parents[2]/'moonshot-005-program/results/eight-packet-seven-corrections-fused/review/REVIEW-RESULT.json',pin=prior_pin)
 remaining=tuple(map(F,prior['conditional_remaining_exact_bounds']))
 require(F(46)<remaining[0]<=remaining[1]<F(47),'exact admitted complete parent margin is between46 and47')
 triple,B,H,roots=examine(source,[0,1,98]);frame,_,_,_=examine(source,FRAME)
 relation={0:F(1),1:F(-1),98:F(-1)}
 require(all(sum(c*roots[x][i] for x,c in relation.items())==0 for i in range(8)),'source root0-root1-root98 relation')
 v=[relation.get(x,F(0)) for x in H]
 require(all(sum(c*w for c,w in zip(row,v))==0 for row in B),'exact residual null vector')
 require(triple['reverse_residual_rank']==95 and frame['reverse_residual_rank']==96,'dependent-triple95 versus orthogonal-frame96')
 require(len(triple['groups'])==3 and all(len(g['donors'])==24 and g['full_aggregate_rank']==g['hosted_aggregate_rank']==2 for g in triple['groups']),'three actual rank-two pair cohorts')
 negative={}
 wrong=[relation.get(x,F(0)) if x!=98 else F(1) for x in H]
 negative['wrong_root_relation_sign_rejected']=any(sum(c*w for c,w in zip(row,wrong)) for row in B)
 broken=[row.copy() for row in B]
 for x in relation:
  for y in relation:
   if x!=y:broken[H.index(x)][H.index(y)]=0
 negative['omitting_mutual_selected_terms_restores_rank96']=rank(broken)==96
 negative['orthogonal_frame_does_not_lower_rank']=frame['reverse_residual_nullity']==0
 require(all(negative.values()),'meaningful rank negative controls')
 result=dict(status='PASS_INDEPENDENT_SELECTED_COLUMN_RANK_AND_TRIPLE_GEOMETRY',source_sha256=SOURCE_PIN,
             independent_checker_sha256=sha(Path(__file__).read_bytes()),dependent_triple=triple,
             orthogonal_frame=dict(selected_firstX=FRAME,selected_gram_rank=frame['selected_gram_rank'],reverse_residual_rank=frame['reverse_residual_rank']),
             exact_null_vector=[[x,str(c)] for x,c in relation.items()],negative_controls=negative,
             budget_gate=dict(parent_review_sha256=prior_pin,parent_remaining_native_moment_upper=str(remaining[1]),max_affordable_integer_terminal_arrivals=46,
                              necessary_selected_nullity=50,necessary_inequality='|S|-rank(G[S,S]) >= 50',
                              scope='Necessary only if common/packet invoices are fixed, all new raw routes refine direct parent routes, and residual is repaired through extra terminal field arrivals.'),
             scope='Proved interface rank theorem and exact finite source geometry. Existence, typing, cost and current-row availability of a realizing triple word are separate obligations.')
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('dependent_triple',)},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
