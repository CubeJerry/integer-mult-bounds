import argparse,gzip,hashlib,json
from collections import Counter
from decimal import Decimal,localcontext
from fractions import Fraction as F
from pathlib import Path
NATIVE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
CERT='7b915321a6e9afc2a83fd79f95e0c9605d28dc578d69d4b0700ee6fd37f739b9'
INVOICE='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
PREPAID='6a1d608dc4b0947cd1d47e2869ceafc72498813a8ceba5d7a09cc1e7ec5bad51'
def need(b,s):
 if not b:raise ValueError(s)
def read(p,pin):
 b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==pin,'dependency pin '+p.name);return b
def span(f):
 s={0}
 for q in f:s|={x^q for x in s}
 return s
def replay(w,ops,M,capture=None,dirty=None):
 p=w['public'];n=p+w['owned_fields'];x=[{i:F(1)} if i in M or i==dirty else {} for i in range(n)];loc=w['initial'][:]+[None]*(n-p);live=set(range(p));frames=list(map(span,w['frames']));counts=Counter();moves=Counter();peak=life=0;out={}
 for i,e in enumerate(ops):
  if capture and i in capture:out[i]=({r:x[r].copy() for r in live}, {r:loc[r] for r in live})
  op,r=e[:2];need(0<=r<n,'field bound');counts[op]+=1
  if op=='INIT':need(r>=p and r not in live,'INIT owned fresh');live.add(r);loc[r]=e[2];x[r]={};life+=1
  elif op=='CLEAR':need(r>=p and r in live and loc[r]==e[2],'CLEAR owned chart');live.remove(r);loc[r]=None;x[r]={}
  elif op=='MOVE':
   need(r in live and loc[r]==e[2] and type(e[4]) is bool and e[4]==(r>=p),'MOVE actual ownership/chart');a,b=frames[e[2]],frames[e[3]];need(a<b or r>=p and b<a,'MOVE strict legal nesting');loc[r]=e[3];moves[abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]))]+=1
  elif op=='SCALE':need(r in live and loc[r]==e[3] and F(e[2])!=0,'SCALE');x[r]={j:v*F(e[2]) for j,v in x[r].items()}
  elif op in ('ADD','COPY'):
   q=e[2];need(0<=q<n and r!=q and r in live and q in live and loc[r]==loc[q]==e[4],'actual live cochart operands');c=F(e[3]);need(c!=0,'nonzero coefficient')
   if op=='COPY':need(not x[r],'zero COPY')
   for j,v in x[q].items():
    x[r][j]=x[r].get(j,F(0))+c*v
    if not x[r][j]:del x[r][j]
  else:raise ValueError(op)
  peak=max(peak,len(live)-p)
 need(live==set(range(p)) and loc[:p]==w['final'],'final chart cleanup');return x,{'counts':dict(counts),'MOVE_histogram':{str(r):c for r,c in sorted(moves.items())},'owned_lifetimes':life,'peak_live_owned':peak,'final_live_owned':0,'declared_owned_labels':w['owned_fields'],'owned_labels_used':len({e[1] for e in ops if e[0]=='INIT'})},out
def power(r):
 D=2**88;N=r**199*D**200
 with localcontext() as c:c.prec=100;a=int(Decimal(r)**(Decimal(199)/200)*D)
 while a**200>N:a-=1
 while(a+1)**200<=N:a+=1
 need(a**200<=N<(a+1)**200,'exact power enclosure');return F(a,D),F(a if a**200==N else a+1,D)

def reconstruct(w):
 main=sorted(set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));qm={r:1480+i for i,r in enumerate(main)};K=1880+w['owned_fields'];H=151;D=qm[101];Y=qm[213];start=30773;stop=43452;P=w['program'];need(P[start]==['MOVE',151,327,541,False] and P[stop]==['MOVE',101,233,127,False],'source loan anchors')
 def old(r):return r if r<1480 else r+400
 def common(e):
  x=e[:];x[1]=old(x[1])
  if x[0] in ('ADD','COPY'):x[2]=old(x[2])
  return x
 def rawmove(e):return ['MOVE',qm[e[1]],e[2],e[3],False]
 def ismainmove(e):return e[0]=='MOVE' and e[1] in qm
 incoming=[['ADD',qm[r],r,'-1',w['initial'][r]] for r in main];outgoing=[['ADD',qm[r],r,'1',w['final'][r]] for r in main]
 base=incoming[:];basecut=None
 for t,e in enumerate(P):
  base.append(common(e))
  if ismainmove(e):base.append(rawmove(e))
  if t==start:basecut=len(base)
 base.extend(outgoing)
 ops=incoming[:];marks={}
 for t,e in enumerate(P[:start+1]):
  if t==start:
   marks['opening']=len(ops);ops.extend([['ADD',H,D,'1',327],['ADD',D,H,'-1',327],['ADD',H,D,'1',327]])
  ops.append(common(e))
  if ismainmove(e):ops.append(rawmove(e))
 ops.extend([['INIT',K,541],['ADD',K,H,'1',541]])
 routes=[];retimed=0
 for t in range(start+1,stop+1):
  e=P[t]
  if ismainmove(e):ops.append(rawmove(e));retimed+=1
  if t in (30824,30826,30830):
   need(e[0]=='MOVE' and e[1]==1481 and e[4] is True,'reserved source owned1481 leg');routes.append([t,e[2],e[3],abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]))]);marks['leg'+str(t)]=len(ops);ops.append(['MOVE',K,e[2],e[3],True])
  if t==30832:
   need(e==['MOVE',213,3,594,False],'receiver timing');marks['receiver']=len(ops);ops.extend([['ADD',Y,K,'1',594],['CLEAR',K,594]])
 marks['repair']=len(ops);ops.extend([['INIT',K,127],['ADD',K,D,'1',127],['MOVE',K,127,541,True],['ADD',H,K,'-1',541],['ADD',K,H,'1',541],['ADD',H,K,'-1',541],['ADD',K,H,'1',541],['MOVE',K,541,127,True],['ADD',D,K,'1',127],['CLEAR',K,127]])
 loancut=len(ops)
 for t in range(start+1,len(P)):
  e=P[t];ops.append(common(e))
  if t>stop and ismainmove(e):ops.append(rawmove(e))
 marks['output_boundary']=len(ops);ops.extend(outgoing)
 meta={'public':1880,'owned_fields':w['owned_fields']+1,'frames':w['frames'],'initial':w['initial']+[w['initial'][r] for r in main],'final':w['final']+[w['final'][r] for r in main]}
 return meta,base,ops,qm,basecut,loancut,marks,routes,retimed

def normalize_bill(b):
 return {'counts':b['counts'],'move_histogram':b['MOVE_histogram'],'owned_lifetimes':b['owned_lifetimes'],'peak_owned':b['peak_live_owned'],'owned_labels_used':b['owned_labels_used'],'final_owned':b['final_live_owned']}

def run(source,packet,lifetime,invoice):
 w=json.loads(gzip.decompress(read(source,NATIVE)));a=json.loads((packet/'RESULT.json').read_text());need(hashlib.sha256((packet/'RESULT.json').read_bytes()).hexdigest()=='e115789257883fdcb09f67fbb47ee305371982a179ce74a8ebb6f82d48e84c0a','frozen paused author receipt');payload=gzip.decompress((packet/'paused-common-word.json.gz').read_bytes());published=json.loads(payload);meta,base,ops,qm,bc,lc,marks,routes,retimed=reconstruct(w)
 need(ops==published['program'],'all73791 independently reconstructed instructions');need(all(meta[k]==published[k] for k in meta),'full metadata');need(published['difference_role_map']=={str(k):v for k,v in qm.items()},'actual400 role map');need(len(ops)==73791 and len(base)==73771 and retimed==1387,'instruction/schedule census');need(published['restoration_checkpoint']=={'baseline_physical_event':bc-1,'loan_physical_event':lc-1,'source_common_cut_after':30773,'difference_calendar_advanced_through':43452},'cut locations')
 allinputs=set(range(1880));b,bb,br=replay(meta,base,allinputs,{bc:None});x,xb,xr=replay(meta,ops,allinputs,{lc:None});expected=[r.copy() for r in b]
 for j,c in {qm[101]:F(1),101:F(-1)}.items():
  expected[qm[213]][j]=expected[qm[213]].get(j,F(0))+c
  if not expected[qm[213]][j]:del expected[qm[213]][j]
 need(x[:1880]==expected[:1880],'all1880 exact endpoint rows');need(x[213]=={213:F(1),101:F(1)} and x[qm[213]]=={qm[213]:F(1),qm[101]:F(1)},'both complete selected native213 endpoints')
 rv,rl=xr[lc];bv,bl=br[bc];common={r for r in bv if r<1480 or r>=1880};need(len(common)==1492 and all(rv[r]==bv[r] and rl[r]==bl[r] for r in common),'all1480 common public and12live owned restored atcut');need(set(r for r in rv if r<1480 or r>=1880)==common,'no leaked common/repair owned role');need(rv[qm[101]]=={qm[101]:F(1),101:F(-1)} and rl[qm[101]]==127,'donor original raw difference restored at127')
 need(normalize_bill(bb)==a['baseline_bill'] and normalize_bill(xb)==a['loan_bill'],'complete independent primitive bill');delta=Counter(xb['counts']);delta.subtract(bb['counts']);need({k:v for k,v in delta.items() if v}=={'ADD':11,'MOVE':5,'INIT':2,'CLEAR':2},'11ADD5MOVE2lifetimes');need(routes==[[30824,541,534,1],[30826,534,117,1],[30830,117,594,4]],'source1,1,4 funding lineage');need(sum(e[0]=='ADD' for e in ops[:400])==400 and len(ops)-marks['output_boundary']==400,'all800 boundary ADDs')
 # Arithmetic compatibility only. Verify that the three reserved routes survive
 # in the eight-current reference; no simultaneous delta1481 claim is made.
 lp=lifetime/'RESULT.json';lr=lp.read_bytes();need(hashlib.sha256(lr).hexdigest()=='594999b1ba54a5dd5ef12a397acf9bc642edf347697042f9ed89ff07b3c9e7ea','lifetime result pin');eight=json.loads(lr)['variants']['eight'];ew=json.loads(gzip.decompress((lifetime/'eight.json.gz').read_bytes()));need(all([t,'source'] in ew['source_map'] for t,_,_,_ in routes),'all three paid slots retained by eight profile')
 iv=json.loads(read(invoice,INVOICE));T=Counter({int(k):v for k,v in iv['T4'].items()});P=Counter({int(k):v for k,v in eight['new_P'].items()});P[2]+=36;powers={r:power(r) for r in set(T)|set(P)};lo=hi=F(0)
 for r in set(T)|set(P):
  c=T[r]-P[r];u,v=powers[r];lo+=c*(u if c>=0 else v);hi+=c*(v if c>=0 else u)
 need(lo>0,'arithmetic eight plus two rank2 repairs remains positive');repair=tuple(2*z for z in power(2));controls=[]
 cases={'omit_donor_restore':('omit',marks['repair']+8),'omit_common_restore_step':('omit',marks['repair']+4),'false_public_descent':('flag',marks['repair']+2),'omit_funded_middle_leg':('omit',marks['leg30826']),'wrong_receiver_shear':('sign',marks['receiver']),'omit_donor_input_conversion':('omit',next(k for k,e in enumerate(ops[:400]) if e[1]==qm[101])),'omit_receiver_output_recoupling':('omit',next(k for k in range(marks['output_boundary'],len(ops)) if ops[k][1]==qm[213]))}
 for name,(how,j) in cases.items():
  bad=[e[:] for e in ops]
  if how=='omit':bad.pop(j)
  elif how=='flag':bad[j][4]=False
  else:bad[j][3]='-1'
  try:y,_,_=replay(meta,bad,allinputs);need(y[:1880]==expected[:1880],'mutant full1880 endpoint')
  except (ValueError,TypeError) as exc:controls.append({'mutation':name,'rejection':str(exc)})
  else:raise ValueError('accepted mutation '+name)
 return {'status':'PASS_INDEPENDENT_1880_PAUSED_COMMON_LOAN','source_sha256':NATIVE,'author_result_sha256':hashlib.sha256((packet/'RESULT.json').read_bytes()).hexdigest(),'word_payload_sha256':hashlib.sha256(payload).hexdigest(),'independent_input_columns':1880,'public_output_rows':1880,'boundary_ADDs':800,'instructions':len(ops),'retimed_raw_main_MOVEs':retimed,'common_rows_restored_at_cut':{'public':1480,'live_owned':12},'selected_output':213,'exact_first_output':{str(k):str(v) for k,v in x[213].items()},'exact_second_output':{str(k):str(v) for k,v in x[qm[213]].items()},'independent_bill':normalize_bill(xb),'funded_second_owned_lineage':routes,'new_paid_ranks':[2,2],'new_paid_moment_per_native_bounds':[str(z) for z in repair],'eight_plus_repairs_paid_positions':sum(P.values()),'eight_plus_repairs_rank_surplus':sum(r*(T[r]-P[r]) for r in set(T)|set(P)),'eight_plus_repairs_headroom_per_native_bounds':[str(lo/18),str(hi/18)],'negative_controls':controls,'scope':'One exact second-native endpoint with all arbitrary common inputs restored; three reserved second-owned1481 payload duties are repurposed and not simultaneously discharged. Arithmetic coexistence with eight-profile is not composition or supplier admission. All other native, precision, compiler, ordinary and foundational duties remain.'}
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for s in ('source','packet','lifetime','invoice'):p.add_argument('--'+s,type=Path,required=True)
 p.add_argument('--output',type=Path,required=True);a=p.parse_args();d=run(a.source,a.packet,a.lifetime,a.invoice);a.output.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n');print(d['status'])
