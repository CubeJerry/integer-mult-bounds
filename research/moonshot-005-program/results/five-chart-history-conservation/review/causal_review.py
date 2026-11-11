#!/usr/bin/env python3
"""Independent154-boundary causal screen from raw native source."""
import argparse,collections,gzip,hashlib,json
from pathlib import Path
from check import Q,PIN,Echelon,intersect,canonical_span,axpy,require,encode

def execute(e,v,loc,F,n):
 op,j=e[:2]
 if op=='INIT':require(j not in v,'INIT absent');v[j]={};loc[j]=F[e[2]]
 elif op=='CLEAR':require(j>=n and j in v,'owned CLEAR');del v[j];del loc[j]
 elif op=='MOVE':require(loc[j]==F[e[2]],'MOVE source');loc[j]=F[e[3]]
 elif op=='ADD':require(j!=e[2] and loc[j]==loc[e[2]],'invertible cochart ADD');axpy(v[j],v[e[2]],Q(e[3]))
 elif op=='COPY':require(not v[j] and loc[j]==loc[e[2]],'COPY guard/cochart');v[j]={k:x*Q(e[3]) for k,x in v[e[2]].items()}
 elif op=='SCALE':require(Q(e[2]),'SCALE nonzero');v[j]={k:x*Q(e[2]) for k,x in v[j].items()}
 else:raise ValueError(op)

def run(src,out):
 raw=src.read_bytes();require(hashlib.sha256(raw).hexdigest()==PIN,'source pin')
 w=json.loads(gzip.decompress(raw));P=w['program'];F=list(map(canonical_span,w['frames']));n=w['public']
 R={F[w['initial'][189]]}|{F[e[3]] for e in P if e[0]=='MOVE' and e[1]==189}
 C={F[w['initial'][77]]}|{F[e[3]] for e in P if e[0]=='MOVE' and e[1]==77}
 require(not C&R,'disjoint charts');names={x:F.index(x) for x in C}
 v={j:{j:Q(1)} for j in range(n)};loc={j:F[f] for j,f in enumerate(w['initial'])}
 initial=[v[j].copy() for j in v if loc[j] in R];history=list(initial);arrivals={}
 for i,e in enumerate(P):
  execute(e,v,loc,F,n)
  if e[0]=='MOVE' and loc[e[1]] in R:arrivals[i]=v[e[1]].copy();history.append(arrivals[i])
 require(set(v)==set(range(n)),'owned retired')
 require(all(loc[j]==F[w['final'][j]] for j in v),'final charts')
 H=Echelon(history);W=Echelon(row for j,row in v.items() if loc[j]==F[127])
 S=Echelon(initial+[row for j,row in v.items() if loc[j] in R and loc[j]!=F[127]])
 I=Echelon(intersect(H.rows.values(),W))
 require((H.rank(),W.rank(),S.rank(),I.rank())==(1056,1022,1047,605),'source ranks')
 v={j:{j:Q(1)} for j in range(n)};loc={j:F[f] for j,f in enumerate(w['initial'])}
 checks=[];survivors=[];schedule=[];local_mode=None;candidate=None
 def inspect(i,c):
  roles=sorted(j for j in v if loc[j]==c);D=intersect([v[j] for j in roles],I);qr=Echelon(S.residual(x) for x in D)
  r=dict(after_event=i,chart=names[c],D_rank=len(D),stable_rank=S.rank(),causal_rank=qr.rank());checks.append(r)
  if qr.rank():survivors.append({**r,'D_basis':[encode(x) for x in D],'quotient_basis':[encode(x) for x in qr.rows.values()]})
 for c in sorted(C):inspect(-1,c)
 for i,e in enumerate(P[:41671]):
  touch={loc[e[1]],F[e[3]]}&C if e[0]=='MOVE' else set()
  execute(e,v,loc,F,n)
  if i in arrivals:
   require(v[e[1]]==arrivals[i],'second-pass observation');S.insert(arrivals[i]);schedule.append(dict(after_event=i,stable_rank=S.rank()))
  for c in sorted(touch):inspect(i,c)
  if i==29530:
   co={103:Q(1,4),273:Q(-1,4),275:Q(-1,4),277:Q(-1,2),282:Q(1,2)}
   require(all(loc[j]==F[232] for j in co),'literal encoder cochart');local_mode={}
   for j,x in co.items():axpy(local_mode,v[j],x)
   require(not I.residual(local_mode),'candidate in H intersect W')
   quotient=S.residual(local_mode)
   candidate=dict(local_coefficients=encode(co),row=encode(local_mode),causal_residual=encode(quotient))
   require(quotient=={17:Q(-1,8),38:Q(-1,8)},'exact causal quotient candidate')
   mutant=local_mode.copy();axpy(mutant,v[103],Q(1,4));require(I.residual(mutant),'mutated coefficient rejected')
 require(len(checks)==154,'all154 boundary snapshots')
 counts=collections.Counter(x['chart'] for x in checks);require(counts=={71:11,312:9,324:13,232:26,127:95},'source checkpoint census')
 nonterminal=[x for x in survivors if x['chart']!=127]
 require(len(nonterminal)==1 and nonterminal[0]['after_event']==29530 and nonterminal[0]['chart']==232 and nonterminal[0]['D_rank']==1 and nonterminal[0]['causal_rank']==1,'sole nonterminal interval')
 require(len(survivors)==68 and all(x['causal_rank']==1 for x in survivors),'surviving dimensions')
 require(S.rank()==H.rank(),'entirehistory stable at final receiver observation')
 require(next(x['after_event'] for x in schedule if x['stable_rank']==H.rank())==41625,'earlier full stability cutoff')
 require(not any(e[0]=='CLEAR' and e[1] in [17,77,103,272,273,275,277,282] for e in P[29531:29637]),'no interval local CLEAR')
 result=dict(status='PASS_INDEPENDENT_CAUSAL154_SOURCE_SCREEN',source_sha256=PIN,history_rank=H.rank(),terminal_rank=W.rank(),intersection_rank=I.rank(),checked_snapshots=len(checks),by_chart=dict(counts),survivor_count=len(survivors),nonterminal_survivor_count=len(nonterminal),all_history_stable_after_event=41625,checks=checks,survivors=survivors,candidate=candidate,stable_schedule=schedule,negative_controls=['local common103 coefficient changed from1/4 to1/2 leaves H intersect W'],new_complete_kappa=None)
 out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:x for k,x in result.items() if k not in ['checks','survivors','candidate','stable_schedule']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.source,a.output)
