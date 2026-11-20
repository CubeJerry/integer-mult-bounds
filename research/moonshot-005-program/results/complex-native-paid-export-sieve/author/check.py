#!/usr/bin/env python3
"""Exact circulation and target-support sieve for paid chart-282 restorations.

No LP/MIP/flow optimizer is used. All target arithmetic is rational, and all
reachability/cycle statements are checked directly in the literal route graph.
"""
import argparse,hashlib,importlib.util,json,sys
from collections import Counter,defaultdict
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

def need(q,msg):
 if not q:raise ValueError(msg)

ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
package=Path(__file__).resolve().parent.parent;pins=json.loads((package/'SOURCE-PINS.json').read_text())
for name,h in pins['files'].items():need(hashlib.sha256((a.repo/name).read_bytes()).hexdigest()==h,'source pin '+name)
base=a.repo/'research/moonshot-005-program/results';source=base/'complex-native-funded-donor-cuts/inputs'
spec=importlib.util.spec_from_file_location('sieve_native_source',source/'7833-construction.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
w=S.load_word(source/'DOUBLE-CANDIDATE.json.gz');four=S.compensated(w);five=S.compensated(w,True)

def span(b):
 out={0}
 for x in b:out|={x^y for y in out}
 need(len(out)==1<<len(b),'independent canonical frame')
 return tuple(sorted(out))

spaces={};canon={};aliases=defaultdict(list)
for c,F in enumerate(w.frames):
 d=spaces.setdefault(span(F),len(spaces));canon[c]=d;aliases[d].append(c)
N=len(spaces);need(N==1102 and len(w.frames)==1103,'canonical atlas inventory')

def graph(routes,removed=()):
 adj=[set()for _ in range(N)];rev=[set()for _ in range(N)]
 for e,(a0,b0)in routes.items():
  if e in removed:continue
  u,v=canon[a0],canon[b0];adj[u].add(v);rev[v].add(u)
 return adj,rev

def reach(adj,start):
 seen={start};todo=[start]
 while todo:
  for v in adj[todo.pop()]-seen:seen.add(v);todo.append(v)
 return seen

def all_reach(adj):return [reach(adj,v)for v in range(N)]
def raw_charts(vertices):return sorted(c for v in vertices for c in aliases[v])
def balance(g):
 b=Counter(canon[c]for c in g.inputs.values());b.subtract(Counter(canon[c]for c in g.terminals.values()))
 for u,v in g.routes.values():b[canon[u]]-=1;b[canon[v]]+=1
 return {v:q for v,q in b.items()if q}
need(not balance(w),'original graph is balanced at every canonical chart')
need(balance(four)=={canon[278]:1,canon[282]:-1},'four-channel imbalance')
need(balance(five)=={canon[3]:-1,canon[278]:1},'one paid observer imbalance')
shadow,=set(five.routes)-set(w.routes);need(five.routes[shadow]==(3,282),'the paid observer route')

# Exact literal target replay, including all 889 helpers and all 400 main inputs.
V=S.all_public_rows(w);VF=S.all_public_rows(five);ends=sorted(w.terminals)
E=[{j:Q(x,den)for j,x in row.items()}for den,row in (V[e]for e in ends)]
need(all(V[e]==VF[e]for e in ends),'authentic fifth channel restores every target column')
R=S.IntegerElimination({j:j for j in range(1289)})
for e in ends:R.add(V[e][1])
need(len(R.rows)==1289,'full target is invertible')
need(sum(len(row)>1 for row in E)==208,'literal coupled endpoint support')

adj,rev=graph(four.routes);reachable=all_reach(adj)
cycles=sorted(e for e,(u,v)in four.routes.items()if canon[u]in reachable[canon[v]])
wide=sorted(e for e,r in four.routes.items()if four.grade(r)>=3)
wide_cycles=sorted(set(wide)&set(cycles))
expected=[43,86,89777,96404,96513,97232,97241,97320,97323,99064,100120]
need(wide_cycles==expected and len(cycles)==144 and len(wide)==1076,'exact cycle and high-grade roster')
regions={};path_slots=set()
for target,wanted in [(278,[3,11,58,278]),(282,[3,11,57,66,85,273,276,282])]:
 verts=reachable[canon[3]]&reach(rev,canon[target]);old=[e for e,(u,v)in four.routes.items()if canon[u]in verts and canon[v]in verts]
 need(raw_charts(verts)==wanted,'complete source-to-target path region')
 need(all(four.grade(four.routes[e])<=2 for e in old),'no high-grade old edge lies on an allowed unused path')
 regions[str(target)]={'charts':wanted,'old_occurrences':sorted(old),'old_grade_histogram':dict(sorted(Counter(four.grade(four.routes[e])for e in old).items()))}
 path_slots.update(old)
need(canon[3]not in set.union(set(),*adj),'no return to source3; new parallel exports create no cycle')
need(canon[278]not in reachable[canon[282]],'new exports create no path into278')

# For each high-grade pair, certify every lost target dependency by a literal
# reachable set. Parallel copies of the new edge have identical reachability.
forbidden=[]
for d,e in combinations(wide_cycles,2):
 A,_=graph(five.routes,{d,e});by_source={};witness=None
 for i,row in enumerate(E):
  if witness is not None:break
  dst=canon[w.terminals[ends[i]]]
  for j,q in row.items():
   src=canon[w.inputs[~j]]
   if src not in by_source:by_source[src]=reach(A,src)
   if dst not in by_source[src]:
    C=by_source[src]
    need(all(not(u in C and v not in C)for f,(aa,bb)in five.routes.items()if f not in{d,e}for u,v in[(canon[aa],canon[bb])]),'literal zero-capacity closed cut')
    witness={'deleted':[d,e],'input_axis':j,'input_chart':w.inputs[~j],'terminal_axis':i,'terminal_slot':ends[i],'terminal_chart':w.terminals[ends[i]],'target_coefficient':str(q),'closed_charts':raw_charts(C)};break
 if witness is not None:forbidden.append(witness)
expected_pairs=[[43,96404],[43,97320],[43,100120],[89777,96404],[89777,96513],[89777,100120],[96404,96513],[96404,100120],[96513,97320],[96513,100120],[97320,100120]]
need([r['deleted']for r in forbidden]==expected_pairs,'eleven forbidden pairs')

# Exhaust all 2^11 deletion subsets using closure in the graph with all eleven
# removed. This checks that the clauses classify support feasibility exactly.
B,_=graph(five.routes,set(wide_cycles));BR=all_reach(B);BRbits=[sum(1<<v for v in z)for z in BR]
needed=[]
for i,row in enumerate(E):
 dst=canon[w.terminals[ends[i]]]
 for j in row:
  src=canon[w.inputs[~j]]
  if dst not in BR[src]:needed.append((src,dst,i,j))
need(len(needed)==40,'forty dependencies affected by the full deletion family')
routes=[tuple(canon[c]for c in five.routes[e])for e in wide_cycles];valid=[]
for mask in range(1<<len(wide_cycles)):
 D={e for k,e in enumerate(wide_cycles)if(mask>>k)&1};rows=[BRbits[src]for src,dst,i,j in needed]
 for _ in range(len(wide_cycles)):
  changed=False
  for k,(u,v)in enumerate(routes):
   if(mask>>k)&1:continue
   for h in range(len(rows)):
    if(rows[h]>>u)&1:
     new=rows[h]|BRbits[v]
     if new!=rows[h]:rows[h]=new;changed=True
  if not changed:break
 good=all((rows[h]>>dst)&1 for h,(src,dst,i,j)in enumerate(needed))
 clauses=all(not set(q['deleted'])<=D for q in forbidden)
 need(good==clauses,'pair clauses are exact for target-support reachability')
 if good:valid.append((sorted(D),Counter(four.grade(four.routes[e])for e in D)))
max_volume=max(sum(r*n for r,n in hist.items())for D,hist in valid)
max_sets=[D for D,hist in valid if sum(r*n for r,n in hist.items())==max_volume]
need(max_volume==28 and max_sets==[[86,89777,97232,97241,97320,97323,99064],[86,96404,97232,97241,97320,97323,99064]],'maximum support-feasible high-grade saving volume')

# Complete caller prices are outward dyadic intervals from the pinned engine.
rail=base/'complex-native-contested-restoration/rail';sys.path.insert(0,str(rail));import price
from graph import Graph
G=Graph();pricing={}
for kappa in [Q(43,10000),Q(1,200)]:
 t=1-kappa;best_hist=Counter({4:5,5:1,3:1});best=price.moment(best_hist,t)
 for D,hist in valid:
  z=price.moment(hist,t)
  need(hist==best_hist or z[1]<best[0],'exact best profile among all support-feasible subsets')
 # four-vs-native gross saving = 3^t+5^t-7^t; one new paid observer costs3^t.
 old=Counter(four.grade(r)for r in w.routes.values());four_hist=Counter(four.grade(r)for r in four.routes.values());need(price.add_profiles((1,old),(-1,four_hist))=={3:1,5:1,7:-1},'literal changed-route tariff')
 gain_hist=price.add_profiles((1,old),(-1,four_hist),(1,best_hist),(-1,{3:1}));gain=price.moment(gain_hist,t)
 required=price.moment(price.add_profiles((1,G.native),(-1,G.helpers),(-Q(1,G.calls),G.fixed_root),(Q(1,G.calls),G.fixed_paid)),t)
 pricing[str(kappa)]={'maximum_high_grade_deleted_moment':price.pretty(best),'maximum_net_saving_with_one_paid_observer':price.pretty(gain),'complete_caller_required_saving':price.pretty(required),'unallocated_margin_for_additional_costs':price.pretty((gain[0]-required[1],gain[1]-required[0]))}

receipt={'status':'PASS_PAID_EXPORT_CIRCULATION_AND_SUPPORT_SIEVE','complete_kappa_claimed':False,'source_columns':1289,'original_paid_occurrences':len(w.routes),'four_channel_paid_occurrences':len(four.routes),'canonical_charts':N,'paid_parallel_observers':'arbitrary integer k >= 1, each route3->282, charged at grade3','all_high_grade_retained_occurrences':len(wide),'mandatory_high_grade_retained_occurrences':len(wide)-len(wide_cycles),'eligible_high_grade_donors_excluding_protected_three':len([e for e in wide if e not in(S.RETARGET,S.OBSERVER,S.OUTLET)]),'wide_cycles':[{'slot':e,'route':four.routes[e],'grade':four.grade(four.routes[e]),'native_clock':w.clock[e]}for e in wide_cycles],'cycle_occurrences':cycles,'cycle_grade_histogram':dict(sorted(Counter(four.grade(four.routes[e])for e in cycles).items())),'path_regions':regions,'noncyclic_old_occurrences_eligible_for_unused_paths':sorted(path_slots-set(cycles)),'forbidden_pairs':forbidden,'support_feasible_subsets':len(valid),'maximum_high_grade_saved_volume':max_volume,'maximizing_subsets':max_sets,'best_high_grade_deleted_profile':{3:1,4:5,5:1},'prices':pricing,'scope':'Only retained four-channel routes may be deleted; additional arcs are parallel3->282 exports. All retained payloads, local operations, histories and timing may change. Original1289 input/output roles and full target remain fixed. Additional endpoint rewrites or other new routes change the premises.'}
(a.out/'RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'],len(wide_cycles),len(forbidden),len(valid),flush=True)
