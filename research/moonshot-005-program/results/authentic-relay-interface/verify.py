#!/usr/bin/env python3
"""Source-exact conditional interface; no global oracle input is inserted."""
import argparse,bisect,collections,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,m):
 if not x:raise ValueError(m)
def add(a,b,c):
 z=a.copy()
 for i,v in b.items():
  x=z.get(i,F(0))+c*v
  if x:z[i]=x
  else:z.pop(i,None)
 return z
def scale(a,c):return {i:c*v for i,v in a.items() if c*v}
def span(a):
 S={0}
 for x in a:S.update(z^x for z in tuple(S))
 return frozenset(S)
def source_rows(w,M):
 R=[{i:F(1)} if i in M else {} for i in range(w['public']+w['owned_fields'])];snap={};want={30773:[130,151],30776:[399],30808:[1507],30824:[1481]};reads=[]
 for k,e in enumerate(w['program']):
  if k in want:
   for i in want[k]:snap[str(k)+':'+str(i)]=R[i].copy()
  tag,r=e[:2]
  if tag in ('ADD','COPY') and e[2]==1481:reads.append({'event':k,'receiver':r,'coefficient':str(F(e[3])),'chart':e[4],'row':{str(i):str(F(e[3])*v) for i,v in sorted(R[1481].items())}})
  if tag in ('INIT','CLEAR'):R[r]={}
  elif tag=='SCALE':R[r]=scale(R[r],F(e[2]))
  elif tag in ('ADD','COPY'):R[r]=add(R[r],R[e[2]],F(e[3]))
 return snap,reads

def quiet_starts(w,M,C):
 touch=collections.defaultdict(list);visits={};at={i:(-1,w['initial'][i]) for i in M};P=w['program'];end=len(P)
 for k,e in enumerate(P):
  touch[e[1]].append(k)
  if e[0] in ('ADD','COPY'):touch[e[2]].append(k)
  if e[0]=='MOVE' and e[1] in M:
   a,f=at[e[1]];need((e[1],C[f]) not in visits,'single main chart visit');visits[e[1],C[f]]=(a,k);at[e[1]]=(k,e[3])
 for i,(a,f) in at.items():visits[i,C[f]]=(a,end)
 starts=set();count=0
 for k,e in enumerate(P):
  if e[0]!='MOVE' or e[1] in M:continue
  h,s,d=e[1:4];ix=bisect.bisect_right(touch[h],k);deadline=touch[h][ix] if ix<len(touch[h]) else end
  for q in M:
   a,b=visits.get((q,C[s])),visits.get((q,C[d]))
   if a and b and a[0]<k<a[1] and k<b[0]<deadline:starts.add(k);count+=1
 need(count==354 and len(starts)==141,'quiet source census');return starts

def module(w,reads):
 # Four actual local ports:0=A,1=B,2=M,3=G, all at541.
 P=[['ADD',0,1,'1',541],['ADD',2,0,'1',541],['ADD',0,2,'-1/2',541],['SCALE',0,'-2',541],['ADD',0,3,'1',541],['INIT',4,541],['ADD',4,0,'1',541],['SCALE',4,'1/2',541],['MOVE',4,541,534,True],['INIT',5,534],['ADD',5,4,'4',534],['MOVE',4,534,117,True],['INIT',6,117],['ADD',6,4,'1',117],['MOVE',4,117,594,True]]
 rows={i:{i:F(1)} for i in range(4)};chart={i:541 for i in range(4)};C=list(map(span,w['frames']));bill=collections.Counter();hist=collections.Counter()
 for e in P:
  tag,r=e[:2];bill[tag]+=1
  if tag=='INIT':need(r>=4 and r not in chart,'fresh owned record');chart[r]=e[2];rows[r]={}
  elif tag=='MOVE':
   a,b,owned=e[2:];need(r>=4 and owned and chart[r]==a and (C[a]<C[b] or C[b]<C[a]),'legal complete-field owned route');chart[r]=b;hist[abs(len(w['frames'][a])-len(w['frames'][b]))]+=1
  elif tag=='SCALE':need(chart[r]==e[3],'SCALE chart');rows[r]=scale(rows[r],F(e[2]))
  else:need(chart[r]==chart[e[2]]==e[4],'cochart ADD');rows[r]=add(rows[r],rows[e[2]],F(e[3]))
 r={0:F(-1,2),1:F(-1,2),2:F(1,2),3:F(1,2)};need(rows[0]==scale(r,2) and rows[2]=={0:F(1),1:F(1),2:F(1)},'full two-output local block');need(rows[4]==rows[6]==r and rows[5]==scale(r,4),'three owned output records')
 observers=[]
 for q in reads:
  rec={534:5,117:6,594:4}[q['chart']];a=F(q['coefficient'])/(4 if rec==5 else 1);need(chart[rec]==q['chart'] and scale(rows[rec],a)==scale(r,F(q['coefficient'])),'all13 increments factor through cochart record');observers.append({'event':q['event'],'receiver':q['receiver'],'record':rec,'multiplier':str(a),'chart':q['chart']})
 return {'status':'CONDITIONAL_LOCAL_FOUR_PORT_PREFIX','input_ports':{'0':'A:actual delta151 before30776','1':'B:actual delta399 before30776','2':'M:actual delta130 before30777, not rawq130','3':'G:actual delta1507 before30808'},'input_chart':541,'program':P,'public_output_rows':{str(i):{str(j):str(v) for j,v in sorted(rows[i].items())} for i in range(4)},'owned_outputs':{'4':{'chart':594,'value':'r'},'5':{'chart':534,'value':'4r'},'6':{'chart':117,'value':'r'}},'observations':observers,'counts':dict(bill),'owned_MOVE_histogram':{str(k):v for k,v in sorted(hist.items())},'live_owned_outputs':3,'clear_operations_implemented':0,'required_retirement':'Caller must apply/replace receiver updates and retire all three owned outputs; no free cleanup is claimed.'}

def run(source,packet,write=False):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));Mset=set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);S,reads=source_rows(w,Mset);A=S['30773:151'];B=S['30776:399'];M=S['30773:130'];G=S['30808:1507'];r=S['30824:1481'];b={55:F(1,2),101:F(-1,2)};U=add(add(add(M,B,F(-1)),G,F(1)),{130:F(1)},F(-1,2));W=add(add(M,B,F(1)),{130:F(1)},F(1,2));need(A==add(b,{130:F(1)},F(1,2)),'exact entry snapshot');need(r==scale(add(add(add(M,A,F(-1)),B,F(-1)),G,F(1)),F(1,2)),'actual carrier after all writes');need(r==scale(add(U,b,F(-1)),F(1,2)),'fused relay interface');need(len(A)==3 and len(M)==15 and len(B)==9 and len(G)==34 and len(r)==59 and len(U)==57 and len(W)==24,'support counts');need(len(reads)==13 and reads[-1]['event']==39544 and w['program'][40843]==['CLEAR',1481,594],'entire lifetime');need(all({int(i):F(v) for i,v in q['row'].items()}==scale(r,F(q['coefficient'])) for q in reads),'unchanged relay on every read');local=module(w,reads)
 C=list(map(span,w['frames']));quiet=quiet_starts(w,Mset,C);reach=collections.defaultdict(set)
 for i in Mset:reach[C[w['initial'][i]]].add(i)
 for k,e in enumerate(w['program'][:30824]):
  if e[0]=='MOVE' and (e[1] in Mset or e[4] or k in quiet):reach[C[e[3]]]|=reach[C[e[2]]]
 missing=sorted(set(U)-reach[C[541]]);need(len(missing)==50 and 4 in missing and 7 in missing,'source-cut absent information');det=U[7]*W[4]-U[4]*W[7];need(det==F(-1,2) and 4 not in b and 7 not in b,'independent missing observable minor');need(A[55]/2==F(1,4) and r[55]==F(-1,4),'false half-entry counterexample');need(r[7]==F(-1,4) and 7 not in A,'missing information counterexample')
 cert={'source_sha256':PIN,'snapshot_rows':{k:{str(i):str(v) for i,v in sorted(z.items())} for k,z in S.items()},'fused_U':{str(i):str(v) for i,v in sorted(U.items())},'fused_W_for_current_main130':{str(i):str(v) for i,v in sorted(W.items())},'all13_source_reads':reads,'retirement_event':40843,'missing_U_input_roles_in_funded_graph_at30824':missing,'two_observable_minor':{'columns':[7,4],'rows':['U','W'],'determinant':'-1/2'},'counterexamples':{'q55_only':{'incorrect_half_entry':'1/4','actual_carrier':'-1/4'},'q7_only':{'incorrect_half_entry':'0','actual_carrier':'-1/4'}}}
 for name,obj in [('SOURCE-ROWS.json',cert),('CONDITIONAL-PREFIX.json',local)]:
  text=json.dumps(obj,indent=2,sort_keys=True)+'\n';path=packet/name
  if write:path.write_text(text)
  else:need(path.read_text()==text,'exact '+name)
 return {'status':'PASS_EXACT_AUTHENTIC_RELAY_REDUCTION','source_sha256':PIN,'source_rows_sha256':hashlib.sha256((packet/'SOURCE-ROWS.json').read_bytes()).hexdigest(),'conditional_prefix_sha256':hashlib.sha256((packet/'CONDITIONAL-PREFIX.json').read_bytes()).hexdigest(),'actual_relay_support':59,'fused_U_support':57,'fused_W_support':24,'all_source_reads':13,'retirement_event':40843,'local_four_port_instruction_count':len(local['program']),'local_counts':local['counts'],'owned_output_records':3,'unproved_physical_input_ports':['actual B','actual M','actual G'],'unproved_reduced_supply':'U at541 before30824; W additionally if current delta130 must be realized','funded_graph_missing_U_coordinates':50,'two_observable_missing_minor':'-1/2','negative_controls':cert['counterexamples'],'scope':'Proved local reduction and full source lifetime audit. Conditional four-port prefix only; no oracle is inserted into a global1880-input word. Inputs, receiver-state continuation and retirement are unproved. No new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--output',type=Path);p.add_argument('--write-certificates',action='store_true');a=p.parse_args();r=run(a.source,a.packet,a.write_certificates);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(s,end='')
