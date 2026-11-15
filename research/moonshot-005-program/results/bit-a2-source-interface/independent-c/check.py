#!/usr/bin/env python3
import argparse,json,hashlib,itertools
from pathlib import Path
from collections import Counter,defaultdict
from functools import lru_cache
import sympy as sp
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);a=p.parse_args();out=Path(__file__).parent
raw=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];wb=a.word.read_bytes();assert hashlib.sha256(wb).hexdigest()=='1f9aa12022272c61f831b4fae4463168f927f2e1660f513051cd0af5842a84f1';w=json.loads(wb);cert=json.loads(a.certificate.read_text());dot=lambda x,y:sum(a*b for a,b in zip(x,y))
def basis(vs):
 b={}
 for v in vs:
  while v:
   k=v.bit_length()-1
   if k in b:v^=b[k]
   else:b[k]=v;break
 return list(b.values())
def rank(vs):return len(basis(vs))
def span(rows):
 s={0}
 for v in rows:s|={z^v for z in tuple(s)}
 return frozenset(s)
def partitions(n):
 if not n:yield [];return
 for old in partitions(n-1):
  yield old+[[n-1]]
  for i in range(len(old)):yield old[:i]+[old[i]+[n-1]]+old[i+1:]
def spaces(n):
 found={frozenset([0])};queue=list(found)
 for s in queue:
  for v in range(1,1<<n):
   if v in s:continue
   t=span(list(s)+[v])
   if t not in found:found.add(t);queue.append(t)
 return queue
charts={}
for name,d in w['charts'].items():
 m=sp.Matrix(d['rows'])if d['rows']else sp.zeros(0,8);charts[name]=tuple(tuple(z)for z in (m.rowspace()if d['kind']=='span'else m.nullspace()))
for j,r in enumerate(R):
 assert charts[f'L{j}']==tuple(tuple(z)for z in sp.Matrix([r]).rowspace())
 assert charts[f'F{j}']==tuple(tuple(z)for z in sp.Matrix([r]).nullspace())
assert len(charts['Hub'])==8 and not charts['zero']
@lru_cache(None)
def inside(x,y):return all(dot(u,v)==0 for u in charts[x]for v in sp.Matrix(charts[y]).nullspace())if charts[y]else not charts[x]
# Separate facet test uses chart basis dot products, not the author's normal-rank formula.
eligible={c:[i for i in range(111)if all(dot(u,R[i])==0 for u in bs)]for c,bs in charts.items()}
X=[f'X{j}_{k}'for j in range(111)for k in range(4)];Y=[f'Y{j}_{k}'for j in range(111)for k in range(4)];vals={n:1<<i for i,n in enumerate(X+Y)};loc={n:f'L{i//4}'for i,n in enumerate(X)}|{n:'zero'for n in Y};duals={n:1<<i for i,n in enumerate(X)};owned=set();born=set();history=defaultdict(set);cut=w['milestones']['canonical36_at_ground_before_all_Y_moves'];counts=Counter();moves=Counter();dirty=0;Xmask=(1<<444)-1;querydata={}
C=basis([sum(1<<(4*j+k)for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)for k in range(4)]);assert len(C)==36
def capture(n):
 if n in vals and not n.startswith('Y'):
  assert vals[n]&~Xmask==0;history[loc[n]].add(vals[n])
for pos,op in enumerate(w['operations'],1):
 tag=op[0];counts[tag]+=1
 if pos>cut:
  for n in op[1:]:capture(n)
 if tag=='INIT':
  _,n,c=op;assert n not in vals and n not in born;vals[n]=0;loc[n]=c;owned.add(n);born.add(n)
 elif tag=='ADD':
  _,s,t=op;assert s!=t and inside(loc[s],loc[t])and inside(loc[t],loc[s]);vals[t]^=vals[s]
  if s in duals and t in duals:duals[s]^=duals[t]
  elif t in duals:raise AssertionError('Non-X source modification of original X not modeled')
 elif tag=='MOVE':
  _,n,c=op;assert inside(c,loc[n])if n in owned else inside(loc[n],c);r=abs(len(charts[c])-len(charts[loc[n]]));assert r;moves[r]+=1;loc[n]=c
 elif tag=='CLEAR':
  _,n=op;assert n in owned;dirty+=bool(vals[n]);owned.remove(n);del vals[n],loc[n]
 else:raise AssertionError(tag)
 if pos==cut:
  assert all(vals[n]==1<<(444+i)and loc[n]=='zero'for i,n in enumerate(Y));assert all(loc[f'P{q}']=='zero'for q in range(36));P=[vals[f'P{q}']for q in range(36)];assert rank(P)==rank(P+C)==36
  H=[n for n in X if loc[n]=='Hub'];D=[n for n in X if loc[n]!='Hub'];assert len(H)==420 and len(D)==24
  assert all(((vals[x]&duals[z]).bit_count()%2)==int(x==z)for x in X for z in X)
  projected=[sum(((v&duals[n]).bit_count()%2)<<j for j,n in enumerate(D))for v in C];groups={c:[j for j,n in enumerate(D)if loc[n]==c]for c in sorted({loc[n]for n in D})};marginals={c:rank([sum(((v>>j)&1)<<k for k,j in enumerate(ids))for v in projected])for c,ids in groups.items()};assert len(groups)==12 and set(marginals.values())=={2} and rank(projected)==24
  querydata={'held_records':24,'actual_chart_groups':12,'marginal_ranks':marginals,'joint_projection_rank':rank(projected),'Delta':sum(marginals.values())-rank(projected)}
  for n in tuple(vals):capture(n)
 elif pos>cut:
  for n in op[1:]:capture(n)
assert not owned and counts==Counter(INIT=40,ADD=5012,MOVE=1416,CLEAR=40)and dirty==40
for j in range(111):
 for k in range(4):assert vals[f'X{j}_{k}']==1<<(4*j+k)and loc[f'X{j}_{k}']=='Hub';assert vals[f'Y{j}_{k}']==((1<<(444+4*j+k))^((1<<(4*j+k))if j in[3,76,80]else 0))and loc[f'Y{j}_{k}']==f'F{j}'
byreceiver=[set()for i in range(111)]
for c,vs in history.items():
 for i in eligible[c]:byreceiver[i].update(vs)
results=[];dualchecks=0
for i in range(111):
 grant=C+list(byreceiver[i]);r=rank(grant);E=[1<<(4*i+k)for k in range(4)];gap=rank(grant+E)-r;claim=cert['all_receivers'][i];assert claim['receiver']==i and claim['source_grant_rank']==r and claim['target_quotient_rank']==gap
 ds=[int(z,16)for z in claim['dual_witnesses_hex']]
 if i in[3,76,80]:assert gap==0 and not ds
 else:
  assert gap==4 and len(ds)==4
  for k,d in enumerate(ds):
   assert d>>444==0;assert all((v&d).bit_count()%2==0 for v in grant);assert[(e&d).bit_count()%2 for e in E]==[int(l==k)for l in range(4)];dualchecks+=1
 results.append({'receiver':i,'rank':r,'gap':gap})
# New source information changes the premise: each extra coordinate removes exactly one missing direction.
grant=C+list(byreceiver[0]);base=rank(grant)
assert [rank(grant+[1<<k for k in range(t)]+[1<<k for k in range(4)])-rank(grant+[1<<k for k in range(t)])for t in range(5)]==[4,3,2,1,0]
querycases=0
for n in range(1,5):
 for P in spaces(n):
  for part in partitions(n):
   ms=[sum(1<<j for j in b)for b in part];marg=[len({v&m for v in P}).bit_length()-1 for m in ms];Delta=sum(marg)-(len(P).bit_length()-1);local=span([v for v in P if any(v&~m==0 for m in ms)]);assert Delta>=0 and(Delta==0)==(local==P);querycases+=1
assert (len({v&1 for v in[0,3]}).bit_length()-1)+(len({v&2 for v in[0,3]}).bit_length()-1)-1==1
outdata={'status':'INDEPENDENT_PASS_FROZEN_SOURCE_CONTINUATION_AND_ONE_CHART_QUERY','source_sha256':hashlib.sha256(wb).hexdigest(),'columns':888,'own_inverse_columns_checked':444,'own_suffix_grant_ranks':dict(sorted(Counter(z['rank']for z in results).items())),'all_receivers':results,'independently_checked_explicit_duals':dualchecks,'excluded_receivers':108,'source_count_check':dict(counts),'movement_profile':dict(sorted(moves.items())),'actual_query_projection':querydata,'one_chart_all_subspace_partition_cases':querycases,'controls':{'three_actual_targets_have_zero_gap':True,'new_point_imports_reduce_gap_4_3_2_1_0':True,'diagonal_projection_two_chart_Delta1':True},'scope':'Frozen source; arbitrary monotone linear Y relays. Separate exact one-chart canonical acquisition criterion. Not general impossibility.','new_complete_kappa':False};(out/'RESULT.json').write_text(json.dumps(outdata,indent=2)+'\n');print({k:outdata[k]for k in['status','own_suffix_grant_ranks','independently_checked_explicit_duals','excluded_receivers','one_chart_all_subspace_partition_cases']})
