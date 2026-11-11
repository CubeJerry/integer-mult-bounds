#!/usr/bin/env python3
"""Recompute the chronological single-encoder source screen from pinned bytes.
@CubeJerry with OpenAI assistance. Apache-2.0. No new kappa.
"""
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as Q
from pathlib import Path
from algebra import add,span,basis,put,reduce,intersection,serial,need,reps,solve,check,show
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
SOURCE='research/shared-wire-split-composition/data/final.json.gz'

def apply(e,rows,loc,C):
 op,j=e[:2]
 if op=='INIT':need(j not in rows,'INIT fresh');rows[j]={};loc[j]=e[2]
 elif op=='CLEAR':
  need(j in rows and C[loc[j]]==C[e[2]],'CLEAR actual chart');rows.pop(j);loc.pop(j)
 elif op=='MOVE':need(C[loc[j]]==C[e[2]],'MOVE actual source');loc[j]=e[3]
 elif op in ('ADD','COPY'):
  s=e[2];need(s!=j and C[loc[s]]==C[loc[j]],'arithmetic distinct and cochart')
  if op=='COPY':need(not rows[j],'COPY zero');rows[j]={}
  add(rows[j],rows[s],Q(e[3]))
 elif op=='SCALE':
  need(Q(e[2])!=0,'nonzero source SCALE');rows[j]={i:Q(e[2])*v for i,v in rows[j].items()}
 else:raise ValueError('unknown operation')

def replay(w,C,receiver):
 rows={j:{j:Q(1)} for j in range(w['public'])};loc=dict(enumerate(w['initial']));hist=[];keys=[];snap={}
 def record(t,j):
  if C[loc[j]] in receiver:hist.append(rows[j].copy());keys.append((t,j,loc[j]))
 for j in rows:record(-1,j)
 for t,e in enumerate(w['program']):
  apply(e,rows,loc,C)
  if e[0]=='MOVE':record(t,e[1])
  if t in (29530,42654):snap[t]={j:r.copy() for j,r in rows.items() if C[loc[j]]==C[232]}
 need(set(rows)==set(range(w['public'])),'all owned retired')
 need(all(C[loc[j]]==C[w['final'][j]] for j in rows),'all final charts')
 return rows,hist,keys,snap

def screen(w,C,route,receiver,hist,keys,final,I,S):
 rows={j:{j:Q(1)} for j in range(w['public'])};loc=dict(enumerate(w['initial']));at=collections.defaultdict(set)
 for j,c in loc.items():at[C[c]].add(j)
 canon={C[c]:c for c in route}
 pre=basis([r for r,k in zip(hist,keys) if k[0]<0]+[r for j,r in final.items() if C[w['final'][j]] in receiver])
 obs={t:(i,j) for i,(t,j,c) in enumerate(keys) if t>=0};last=max(obs);records=[]
 def calc(t,chart):
  E=[rows[j] for j in sorted(at[chart])];D=intersection(E,I)
  qs=basis(reduce(r,S) for r in D.values());qc=basis(reduce(r,pre) for r in D.values())
  records.append({'after_event':t,'chart':canon[chart],'local_fields':len(E),'D_rank':len(D),
                  'static_quotient_rank':len(qs),'causal_stable_rank':len(pre),'causal_quotient_rank':len(qc)})
 for chart in sorted(canon,key=canon.get):calc(-1,chart)
 for t,e in enumerate(w['program']):
  if t>last:break
  op,j=e[:2];old=C[loc[j]] if j in loc else None;apply(e,rows,loc,C)
  if op=='INIT':at[C[loc[j]]].add(j)
  elif op=='CLEAR':at[old].remove(j)
  elif op=='MOVE':
   new=C[loc[j]];at[old].remove(j);at[new].add(j)
   if t in obs:
    i,jj=obs[t];need(j==jj and rows[j]==hist[i],'timed history agrees in second replay');put(pre,rows[j])
   if old in canon:calc(t,old)
   if new in canon and new!=old:calc(t,new)
 need(len(pre)==len(basis(hist)),'eventual stable history is complete')
 return records,last

def run(repo):
 raw=(repo/SOURCE).read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native source pin')
 w=json.loads(gzip.decompress(raw));C=list(map(span,w['frames']));P=w['program']
 need(w['public']==1480 and len(P)==71261,'source census')
 route=[w['initial'][77]]+[e[3] for e in P if e[0]=='MOVE' and e[1]==77]
 receiver={C[w['initial'][189]]}|{C[e[3]] for e in P if e[0]=='MOVE' and e[1]==189}
 need(route==[71,312,324,232,127],'actual donor itinerary')
 need(not {C[c] for c in route}&receiver,'disjoint donor/receiver charts')
 final,hist,keys,snap=replay(w,C,receiver)
 terminal={j:r for j,r in final.items() if C[w['final'][j]]==C[127]}
 rend={j:r for j,r in final.items() if C[w['final'][j]] in receiver}
 H=basis(hist);W=basis(terminal.values());S=basis([r for r,k in zip(hist,keys) if k[0]<0]+list(rend.values()))
 QH=basis(reduce(r,S) for r in H.values());I=intersection(H.values(),W);QI=basis(reduce(r,S) for r in I.values())
 need((len(hist),len(H),len(W),len(S),len(QH),len(I),len(QI))==(1065,1056,1022,1047,9,605,9),'global quotient ranks')
 need(sorted(rend)==[189,953] and all(not reduce(r,H) for r in rend.values()),'actual receiver endpoints')
 records,last=screen(w,C,route,receiver,hist,keys,final,I,S)
 need(last==41670 and len(records)==154,'MOVE-boundary census')
 nonhub=[r for r in records if r['chart']!=127 and r['causal_quotient_rank']]
 hub=[r for r in records if r['chart']==127 and r['causal_quotient_rank']]
 need(len(nonhub)==1 and nonhub[0]['after_event']==29530 and nonhub[0]['chart']==232 and nonhub[0]['D_rank']==nonhub[0]['causal_quotient_rank']==1,'sole nonhub candidate')
 need(len(hub)==67 and max(r['causal_quotient_rank'] for r in hub)==1,'hub candidate census')
 nxt=min(t for t,e in enumerate(P) if t>29530 and e[0]=='MOVE' and C[232] in (C[e[2]],C[e[3]]))
 need(nxt==29637,'candidate interval end')
 E=snap[29530];D=intersection(E.values(),I);need(len(D)==1,'candidate dimension');r=next(iter(D.values()))
 eco=solve(r,reps(E));wco=solve(r,reps(terminal));hco=solve(r,reps(dict(enumerate(hist))))
 for co,src in [(eco,E),(wco,terminal),(hco,dict(enumerate(hist)))]:check(r,co,src)
 need(eco=={103:Q(1,4),273:Q(-1,4),275:Q(-1,4),277:Q(-1,2),282:Q(1,2)},'five-term encoder')
 St=basis([h for h,k in zip(hist,keys) if k[0]<=29530]+list(rend.values()));cr=reduce(r,St)
 need(cr=={17:Q(-1,8),38:Q(-1,8)},'surviving causal mode')
 terms=[{'after_event':keys[i][0],'role':keys[i][1],'chart':keys[i][2],'coefficient':str(c)} for i,c in sorted(hco.items())]
 later=[t for t in terms if t['after_event']>29530]
 need([(t['after_event'],t['role'],t['coefficient']) for t in later]==[(40811,383,'1/2'),(40836,484,'1/4'),(41625,622,'1'),(41670,620,'1')],'later decoder observations')
 late=snap[42654][12];need(late=={12:Q(1),31:Q(1)} and bool(reduce(late,S)) and not reduce(late,H),'late static false positive')
 wrong=eco.copy();wrong[103]+=Q(1,4);wr={}
 for j,c in wrong.items():add(wr,E[j],c)
 need(wr!=r and (reduce(wr,H) or reduce(wr,W)),'wrong coefficient must leave admissible intersection')
 return {'status':'PASS_CAUSAL_RECOVERABLE_ENCODER_SCREEN','source_path':SOURCE,'source_sha256':PIN,
 'donor':77,'receiver':189,'donor_chart_ids':route,'receiver_final_roles':sorted(rend),
 'ranks':{'history_count':len(hist),'history_rank':len(H),'terminal_rank':len(W),'static_stable_rank':len(S),'history_quotient_rank':len(QH),'history_terminal_intersection_rank':len(I),'recoverable_quotient_rank':len(QI)},
 'static_quotient_basis':serial(QH.values()),'recoverable_quotient_basis':serial(QI.values()),
 'screened_move_boundary_states':len(records),'states_per_chart':dict(sorted(collections.Counter(z['chart'] for z in records).items())),
 'last_receiver_arrival':last,'hub_candidate_states':len(hub),'records':records,
 'sole_nonhub_candidate':{'first_cut_after_event':29530,'last_cut_before_event':29637,'chart':232,'cochart_roles':sorted(E),'common_row':show(r),'encoder_coefficients':show(eco),'terminal_coefficients':show(wco),'history_coefficients':terms,'causal_quotient_row':show(cr),'later_history_coefficients':later},
 'negative_controls':['late u12+u31 survives static gate but all its observations precede encoder','wrong local103 coefficient leaves admissible intersection'],
 'scope':'Finite pinned-source reduction for a single recoverable encoder on donor77 original route. Nonzero causal quotient is necessary not sufficient. Control gain, physical realization, composition, suppliers and foundations remain unproved here.','new_complete_kappa':None}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repository',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.repository);a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(r['status']);print(r['ranks']);print('Sole nonhub candidate: chart232 after29530, before29637. No positive channel asserted.')
