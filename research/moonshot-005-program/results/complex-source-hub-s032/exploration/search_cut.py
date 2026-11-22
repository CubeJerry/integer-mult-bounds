"""Discovery only: cuts from mixed integer optimization, not solver certificates."""
from pathlib import Path
from collections import Counter,defaultdict
from fractions import Fraction
import importlib.util,json,time,sys
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import coo_matrix
HERE=Path(__file__).resolve().parent;R=HERE.parents[1]
src=R/'complex-native-funded-donor-cuts/inputs/7833-construction.py'
spec=importlib.util.spec_from_file_location('native',src);S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
g=S.compensated(S.load_word(src.with_name('DOUBLE-CANDIDATE.json.gz')),True)
def span(fr):
 a={0}
 for x in fr:a|={v^x for v in a}
 return tuple(sorted(a))
spaces=sorted({span(f)for f in g.frames});idx={s:i for i,s in enumerate(spaces)};canon={c:idx[span(f)]for c,f in enumerate(g.frames)};N=len(spaces)
rep={v:min(c for c,w in canon.items()if w==v)for v in range(N)}
D={86,89777,97232,97241,97320,97323,99064}
old=Counter((canon[a],canon[b])for e,(a,b)in g.routes.items()if e not in D and canon[a]!=canon[b])
pairs=json.loads((R/'complex-paid-export-s031-coupled-repair/endpoint-screen/EXPECTED-SURVIVORS.json').read_text())['pairs']
parts=json.loads((HERE/'TARGET-COMPONENTS.json').read_text())
# A matching in each nonsingular 1x1/2x2 target component certifies its cross rank.
dem=[]
for p in parts:
 for i,oc in enumerate(p['output_charts']):
  for j,ic in enumerate(p['input_charts']):
   if Fraction(p['matrix'][i][j]):dem.append((p['inputs'][j],p['outputs'][i],canon[ic],canon[oc]))
# Group identical singleton pairs for performance. Non-singletons keep row/column quotas.
print('N',N,'oldpairs',len(old),'dem',len(dem),flush=True)
cuts=[];pending=list(range(len(pairs)));rounds=0
maxsec=float(sys.argv[1])if len(sys.argv)>1 else 30
while pending and rounds<30:
 pi=pending[0];pair=pairs[pi];routes=old.copy()
 for a,b in pair:routes[canon[a],canon[b]]+=1
 edges=sorted(routes);num=N+len(edges)+len(dem);cost=np.zeros(num)
 cost[N:N+len(edges)]=[routes[e]for e in edges];cost[N+len(edges):]=-1
 rr=[];cc=[];vv=[];lo=[];hi=[]
 def row(d,l=-np.inf,h=0):
  k=len(lo);lo.append(l);hi.append(h)
  for j,v in d.items():rr.append(k);cc.append(j);vv.append(v)
 for k,(u,v)in enumerate(edges):row({u:1,v:-1,N+k:-1})
 ins=defaultdict(list);outs=defaultdict(list);ip={};op={}
 for k,(a,b,u,v)in enumerate(dem):ins[a].append(N+len(edges)+k);outs[b].append(N+len(edges)+k);ip[a]=u;op[b]=v
 for a,ks in ins.items():row({**{k:1 for k in ks},ip[a]:-1})
 for b,ks in outs.items():row({**{k:1 for k in ks},op[b]:1},h=1)
 mat=coo_matrix((vv,(rr,cc)),shape=(len(lo),num)).tocsc()
 start=time.time();r=milp(cost,integrality=np.r_[np.ones(N),np.zeros(num-N)],bounds=Bounds(np.zeros(num),np.ones(num)),constraints=LinearConstraint(mat,lo,hi),options={'time_limit':maxsec,'mip_rel_gap':0.0,'presolve':True})
 print('pair',pi,pair,'status',r.status,'fun',r.fun,'bound',getattr(r,'mip_dual_bound',None),'sec',time.time()-start,flush=True)
 if r.x is None or r.fun>-.5:
  rounds+=1;pending.remove(pi);continue
 A={i for i,x in enumerate(r.x[:N])if x>.5};oldout=[e for e,(u,v)in g.routes.items()if e not in D and canon[u]in A and canon[v]not in A]
 # Exact target cross rank, not rounded objective.
 rank=0;minors=[]
 for p in parts:
  js=[j for j,c in enumerate(p['input_charts'])if canon[c]in A];is_=[i for i,c in enumerate(p['output_charts'])if canon[c]not in A]
  if not js or not is_:continue
  M=[[Fraction(p['matrix'][i][j])for j in js]for i in is_]
  if len(js)==len(is_)==2:
   assert M[0][0]*M[1][1]!=M[0][1]*M[1][0];v=2
  else:v=int(any(any(row)for row in M))
  rank+=v
  if v:minors.append({'inputs':[p['inputs'][j]for j in js],'outputs':[p['outputs'][i]for i in is_],'rank':v})
 rej=[]
 for pj in pending:
  cap=len(oldout)+sum(canon[a]in A and canon[b]not in A for a,b in pairs[pj])
  if cap<rank:rej.append(pj)
 assert pi in rej
 cuts.append({'id':len(cuts),'rank':rank,'old_capacity':len(oldout),'old_exports':oldout,'raw_charts':sorted(c for c,v in canon.items()if v in A),'rejected_pair_indices':rej,'minors':minors})
 pending=[p for p in pending if p not in rej]
 (HERE/'DISCOVERED-CUTS.json').write_text(json.dumps({'cuts':cuts,'pending_pair_indices':pending},indent=2)+'\n')
 print('CUT rank',rank,'oldcap',len(oldout),'A',len(A),'reject',len(rej),'pending',len(pending),flush=True)
 rounds+=1
print('done',len(cuts),len(pending),flush=True)
