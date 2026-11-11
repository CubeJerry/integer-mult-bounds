#!/usr/bin/env python3
import argparse,collections,gzip,hashlib,json
from pathlib import Path
from fractions import Fraction as Q
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883';EVENTS=(28141,33554,34467,37597)
def need(c,m):
 if not c:raise ValueError(m)
def plus(a,b,c):
 o=a.copy()
 for j,v in b.items():
  x=o.get(j,Q(0))+c*v
  if x:o[j]=x
  else:o.pop(j,None)
 return o
def span(xs):
 z={0}
 for x in xs:z.update(v^x for v in tuple(z))
 return frozenset(z)
def rank(vs):
 B={}
 for v in vs:
  v=v.copy()
  for p,b in sorted(B.items(),reverse=True):
   if p in v:v=plus(v,b,-v[p])
  if v:
   p=max(v);c=v[p];B[p]={i:x/c for i,x in v.items()}
 return len(B)
def determinant(A):
 A=[list(map(Q,r)) for r in A];d=Q(1)
 for i in range(len(A)):
  j=next((j for j in range(i,len(A)) if A[j][i]),None)
  if j is None:return Q(0)
  if j!=i:A[i],A[j]=A[j],A[i];d=-d
  a=A[i][i];d*=a
  for j in range(i+1,len(A)):
   c=A[j][i]/a
   for k in range(i,len(A)):A[j][k]-=c*A[i][k]
 return d
def replay(w,ops,owned,checks=()):
 P=w['public'];M=set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);cur={i:w['initial'][i] for i in range(P)};rows={i:({i:Q(1)} if i in M else {}) for i in range(P)};spaces=list(map(span,w['frames']));bills=collections.Counter();hist=collections.Counter();peak=life=0;record={};check={x['physical_before_event']:x for x in checks}
 for k,e in enumerate(ops):
  tag,a=e[:2];need(0<=a<P+owned,'owner range')
  if k in check:
   z=check[k];need(rows[z['old_physical_owner']]==rows[z['new_physical_owner']],'exact400-column rebind');need(cur[z['new_physical_owner']]==z['destination'],'rebind destination')
  if ops is w['program'] and k in EVENTS:record[k]=rows[a].copy()
  bills[tag]+=1
  if tag=='INIT':need(a>=P and a not in cur,'INIT');cur[a]=e[2];rows[a]={};life+=1
  elif tag=='CLEAR':need(a>=P and cur.get(a)==e[2],'CLEAR');del cur[a];del rows[a]
  elif tag=='MOVE':
   s,t,o=e[2:];need(cur.get(a)==s and type(o) is bool and o==(a>=P),'typed MOVE');need(spaces[s]<spaces[t] or o and spaces[t]<spaces[s],'nested MOVE');cur[a]=t;hist[abs(len(w['frames'][s])-len(w['frames'][t]))]+=1
  elif tag in ('ADD','COPY'):
   b,c,f=e[2:];need(a!=b and cur.get(a)==cur.get(b)==f and a in cur and b in cur,'live cochart scalar');c=Q(c);need(c!=0,'nonzero ADD')
   if tag=='COPY':need(not rows[a],'COPY zero')
   rows[a]=plus(rows[a],rows[b],c)
  elif tag=='SCALE':need(cur.get(a)==e[3] and Q(e[2])!=0,'SCALE');rows[a]={i:Q(e[2])*v for i,v in rows[a].items()}
  else:raise ValueError(tag)
  peak=max(peak,len(cur)-P)
 return rows,cur,{'counts':dict(bills),'move_histogram':{str(k):v for k,v in sorted(hist.items())},'peak_owned':peak,'owned_lifetimes':life,'final_live_owned':len(cur)-P},record

def run(source,packet):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));original,och,ob,trs=replay(w,w['program'],w['owned_fields']);T=[trs[k] for k in EVENTS];dest=[w['program'][k][3] for k in EVENTS];C=list(map(span,w['frames']));G=collections.defaultdict(set)
 for row in T:
  for i in row:G[C[w['initial'][i]]].add(i)
 cuts={f:rank([{i:a for i,a in row.items() if i in S} for row,d in zip(T,dest) if C[d]!=f]) for f,S in G.items()};empty=frozenset({0});need(len(G)==102 and cuts[empty]==4 and sum(cuts.values())==105 and all(v==1 for f,v in cuts.items() if f!=empty),'exact initial chart cuts')
 X=[{i:a for i,a in row.items() if C[w['initial'][i]]!=empty} for row in T];Y=[{i:a for i,a in row.items() if C[w['initial'][i]]==empty} for row in T];need(rank(X)==rank(Y)==4,'block ranks');dx=determinant([[row.get(i,Q(0)) for i in (4,2,1,0)] for row in T]);dy=determinant([[row.get(i,Q(0)) for i in (131,129,142,150)] for row in T]);need(dx==Q(-3,4) and dy==Q(-495,64),'independent minors')
 # Reconstruct every instruction from independently replayed return rows.
 N=w['public']+w['owned_fields'];ops=[['INIT',N+j,3] for j in range(4)]
 for j,row in enumerate(T):ops.extend(['ADD',N+j,i,str(a),3] for i,a in sorted(row.items()) if C[w['initial'][i]]==empty)
 donors=sorted(set().union(*(set(x) for x in X)))
 for i in donors:
  f=w['initial'][i];need(len(w['frames'][f])==1,'gathering rank1');ops.extend([['INIT',N+4,f],['ADD',N+4,i,'1',f],['MOVE',N+4,f,3,True]]);ops.extend(['ADD',N+j,N+4,str(row[i]),3] for j,row in enumerate(T) if i in row);ops.append(['CLEAR',N+4,3])
 ops.extend(['MOVE',N+j,3,d,True] for j,d in enumerate(dest));pre=len(ops);mapping={i:i for i in range(N)};bind=[]
 for k,e in enumerate(w['program']):
  a=e[1]
  if e[0]=='INIT':mapping[a]=a
  if k in EVENTS:
   j=EVENTS.index(k);bind.append({'physical_before_event':len(ops),'event':k,'logical_owner':a,'old_physical_owner':mapping[a],'new_physical_owner':N+j,'destination':dest[j]});ops.append(['CLEAR',mapping[a],e[2]]);mapping[a]=N+j
  else:
   q=e[:];q[1]=mapping[a]
   if e[0] in ('ADD','COPY'):q[2]=mapping[e[2]]
   ops.append(q)
 payload=gzip.decompress((packet/'whole-preload.json.gz').read_bytes());t=json.loads(payload);a=json.loads((packet/'WHOLE-RESULT.json').read_text());need(t['program']==ops and t['rebindings']==bind,'entire literal word');need(t['initial']==w['initial'] and t['frames']==w['frames'] and t['owned_fields']==56,'physical interface');out,ch,bill,_=replay(w,ops,56,bind);P=w['public'];need(all(out[i]==original[i] and ch[i]==och[i] for i in range(P)),'all1480 public endpoints');need(bill==a['rewritten'],'complete typed bill');need(pre==812 and len(ops)==72073 and bill['owned_lifetimes']==159 and bill['peak_owned']==44 and bill['final_live_owned']==0,'exact lifecycle/instruction census');delta=collections.Counter(bill['counts']);delta.subtract(ob['counts']);need({k:v for k,v in delta.items() if v}=={'ADD':501,'INIT':105,'MOVE':101,'CLEAR':105},'operation delta')
 controls=[]
 for name in ('wrong_preload_coefficient','owned_gather_marked_public','retired_owner_reference'):
  bad=[q[:] for q in ops]
  if name=='wrong_preload_coefficient':next(q for q in bad if q[0]=='ADD')[3]='999'
  elif name=='owned_gather_marked_public':next(q for q in bad if q[0]=='MOVE')[4]=False
  else:
   b=bind[0]
   for q in bad[b['physical_before_event']+1:]:
    if q[0] in ('ADD','COPY') and q[2]==b['new_physical_owner']:q[2]=b['old_physical_owner'];break
    if q[1]==b['new_physical_owner']:q[1]=b['old_physical_owner'];break
  try:
   o,c,bb,_=replay(w,bad,56,bind);need(all(o[i]==original[i] for i in range(P)),'mutated endpoint')
  except ValueError as e:controls.append({'mutation':name,'rejection':str(e)})
  else:raise ValueError('accepted mutant '+name)
 need(T[0].get(4)==Q(-3,4) and 4 not in Y[0],'nonentry counterexample');need(rank([{}]*4)==0 and rank([T[0]]*4)==1,'zero/duplicate rank controls')
 return {'status':'PASS_INDEPENDENT_SHARP_105_PREPROCESSING','source_sha256':PIN,'author_result_sha256':hashlib.sha256((packet/'WHOLE-RESULT.json').read_bytes()).hexdigest(),'transcript_payload_sha256':hashlib.sha256(payload).hexdigest(),'initial_chart_groups':len(G),'distributed_chart_cuts':len(G)-1,'empty_chart_cut_rank':cuts[empty],'minimum_added_arrivals':sum(cuts.values()),'distributed_minor':str(dx),'entry_minor':str(dy),'independent_difference_inputs':400,'public_endpoint_rows':P,'instructions':len(ops),'prelude_instructions':pre,'added_rank_one_gathering_MOVEs':len(donors),'declared_owned_labels':56,'operation_changes':dict(delta),'typed_bill':bill,'negative_controls':controls,'scope':'Exact initial-only minimum and literal reference-rail upper witness. Dynamic funded routes, joint common/difference codes, weighted-price optimality and global kappa contracts remain outside.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args();r=run(a.source,a.packet);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(s,end='')
