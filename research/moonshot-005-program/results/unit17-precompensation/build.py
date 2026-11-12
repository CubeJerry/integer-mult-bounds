"""Construct and verify a partial second-copy word on1880 independent inputs."""
import argparse
from collections import Counter,defaultdict
from fractions import Fraction as F
import gzip,hashlib,json
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(v,m):
 if not v:raise ValueError(m)
def add(a,b,c=F(1)):
 for k,v in list(b.items()):
  z=a.get(k,F(0))+c*v
  if z:a[k]=z
  else:a.pop(k,None)
def span(f):
 s={0}
 for b in f:s.update(x^b for x in tuple(s))
 return s
class Machine:
 def __init__(self,initial,frames,limit):
  self.rows={j:{j:F(1)} for j in range(1880)};self.loc=dict(enumerate(initial));self.frames=frames;self.spans=list(map(span,frames));self.limit=limit;self.peak=self.active=0;self.count=Counter();self.moves=Counter()
 def run(self,e):
  op,j=e[:2];self.count[op]+=1
  if op=='INIT':
   need(1880<=j<self.limit and j not in self.loc,'owned INIT');self.loc[j]=e[2];self.rows[j]={};self.active+=1;self.peak=max(self.peak,self.active)
  elif op=='CLEAR':
   need(j>=1880 and self.loc[j]==e[2],'owned CLEAR');del self.loc[j];del self.rows[j];self.active-=1
  elif op=='ADD':
   need(self.loc[j]==self.loc[e[2]]==e[4],'cochart ADD');add(self.rows[j],self.rows[e[2]],F(e[3]))
  elif op=='SCALE':
   need(self.loc[j]==e[3] and F(e[2]),'cochart SCALE');self.rows[j]={k:v*F(e[2]) for k,v in self.rows[j].items() if v*F(e[2])}
  elif op=='COPY':
   need(self.loc[j]==self.loc[e[2]]==e[4] and not self.rows[j],'COPY zero/cochart');self.rows[j]={k:v*F(e[3]) for k,v in self.rows[e[2]].items() if v*F(e[3])}
  elif op=='MOVE':
   need(self.loc[j]==e[2] and e[4]==(j>=1880),'MOVE location/ownership');a,b=self.spans[e[2]],self.spans[e[3]];need(a<=b or b<=a,'nested MOVE');r=abs(len(self.frames[e[2]])-len(self.frames[e[3]]));self.moves[r]+=1;self.loc[j]=e[3]
  else:raise ValueError(op)
def expected_common(w):
 R={j:{j:F(1)} for j in range(1480)};D=set(w['hosted']['Dports'])
 for i,x in enumerate(w['live']):
  y=x+112
  if i in D:R[y]={x:F(1),y:F(1)}
  else:R[x]={x:F(1),y:F(-1)};R[y]={x:F(1,2),y:F(1,2)}
 for x,y in zip(w['hosted']['X2'],w['hosted']['Y2']):R[x]={x:F(1),y:F(-1)}
 return R
def main(a):
 raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));ob=json.load(open(a.observations));joint=json.loads(gzip.decompress(a.joint.read_bytes()));mat=json.load(open(a.matrices));donors=mat['donors'];need(len(donors)==17 and len(set(donors))==17,'distinct unit donors');obs=[next(o for o in ob['observations'] if o['donor']==j) for j in donors]
 M=sorted(set(w['live'])|{x+112 for x in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));q={j:1480+i for i,j in enumerate(M)};initial=w['initial']+[w['initial'][j] for j in M];Fc=expected_common(w)
 Ti=[[F(v) for v in r] for r in mat['T_inverse']];E=[[F(v) for v in r] for r in mat['raw_initial_gain_correction_I_minus_B_Tinv']];cols=[{int(j):F(v) for j,v in joint['offhub_columns'][k]} for k in mat['selected_cut_indices']]
 debt={role:[sum((cols[k].get(role,F(0))*Ti[k][j] for k in range(17)),F(0)) for j in range(17)] for role in sorted(set().union(*(set(c) for c in cols)))};K={}
 for role,row in debt.items():
  need(w['initial'][role]==3,'initial3 support');diag=Fc[role].get(role,F(0));need(diag,'same-role inverse');K[role]=[-v/diag for v in row]
 native_role=lambda j:j if j<1480 else j+400
 nextlabel=1931;vc={}
 for x in donors:vc[x]=nextlabel;nextlabel+=1
 packet=nextlabel;temp=nextlabel+1;nextlabel+=2;hist=[];after=defaultdict(list)
 for i,o in enumerate(obs):
  need(o['hrow']=={str(o['donor']):'1'},'unit payload');need(w['program'][o['event']][2]==w['initial'][o['donor']],'initial-line cache access');need(Fc[o['donor']]=={o['donor']:F(1)},'ordinary donor output')
  route={w['initial'][o['donor']+112]}|{e[3] for e in w['program'] if e[:2]==['MOVE',o['donor']+112]}
  for t in o['historical_decoder']:
   need(t['chart'] in route,'literal decoder chart on funded route');h={**t,'label':nextlabel,'receiver':o['donor']+112,'coefficient':str(F(t['coefficient']))};nextlabel+=1;hist.append(h);after[t['after_event']].append(h)
 m=Machine(initial,w['frames'],nextlabel);program=[];marks=[];reservations=[]
 def emit(e,purpose):m.run(e);program.append(e);marks.append(purpose)
 def snapshot(h):
  emit(['INIT',h['label'],h['chart']],'history_INIT');emit(['ADD',h['label'],native_role(h['role']),'1',h['chart']],'initial_history_snapshot' if h['after_event']==-1 else 'timed_history_snapshot')
 def rawmove(t,e):
  reservations.append({'physical_event':len(program),'source_event':t,'logical_role':e[1]});emit(['MOVE',q[e[1]],e[2],e[3],False],'funded_raw_MOVE')
 for x in donors:
  ch=w['initial'][x];emit(['INIT',vc[x],ch],'cache_actual_v');emit(['ADD',vc[x],q[x],'1',ch],'cache_actual_v');emit(['ADD',q[x],x,'-1',ch],'form_actual_q')
 for j,x in enumerate(donors):
  ch=w['initial'][x];emit(['INIT',packet,ch],'debt_packet_INIT');emit(['ADD',packet,q[x],'1',ch],'debt_packet_copy');emit(['MOVE',packet,ch,3,True],'new_rank1_debt_packet')
  for role,row in K.items():
   if row[j]:emit(['ADD',role,packet,str(row[j]),3],'common_initial_precorrection')
  for i,y in enumerate(donors):
   if E[i][j]:emit(['ADD',q[y+112],packet,str(E[i][j]),3],'raw_initial_gain_correction')
  emit(['CLEAR',packet,3],'debt_packet_CLEAR')
  for t,e in enumerate(w['program']):
   if e[:2]==['MOVE',x]:rawmove(t,e)
 for h in after[-1]:snapshot(h)
 cut={o['event']:o for o in obs}
 for t,e0 in enumerate(w['program']):
  if t in cut:
   o=cut[t];x=o['donor'];h=o['helper'];ch=w['initial'][x];g=F(o['gain']);emit(['INIT',temp,ch],'encoder_INIT');emit(['ADD',temp,h,'1',ch],'encoder_old_payload');emit(['ADD',h,vc[x],str(g),ch],'encoder_add_v');emit(['ADD',h,temp,str(-g),ch],'encoder_subtract_old');emit(['CLEAR',temp,ch],'encoder_CLEAR');emit(['CLEAR',vc[x],ch],'v_cache_CLEAR')
  e=list(e0);e[1]=native_role(e[1])
  if e[0] in ['ADD','COPY']:e[2]=native_role(e[2])
  emit(e,'original_common_word')
  for h in after[t]:snapshot(h)
 hub_repair={}
 for j in range(1480):
  err=dict(m.rows[j]);add(err,Fc[j],-1)
  if not err:continue
  need(w['final'][j]==127,'offhub already exactly corrected at '+str(j));coef={x:err.get(q[x],F(0)) for x in donors};rem=dict(err)
  for x,c in coef.items():add(rem,{q[x]:F(1),x:F(-1)},-c)
  need(not rem,'hub error is known q only');hub_repair[j]={x:str(c) for x,c in coef.items() if c}
  for x,c in coef.items():
   if c:emit(['ADD',j,q[x],str(-c),127],'common_hub_correction')
 for x in donors:emit(['ADD',q[x],x,'1',127],'restore_second_donor_v')
 pending=defaultdict(list)
 for h in hist:pending[(h['receiver'],h['chart'])].append(h)
 def consume(role,ch):
  for h in pending.pop((role,ch),[]):emit(['ADD',q[role],h['label'],h['coefficient'],ch],'receiver_history_accumulation');emit(['CLEAR',h['label'],ch],'history_CLEAR')
 for x in donors:consume(x+112,3)
 for t,e in enumerate(w['program']):
  if e[0]=='MOVE' and e[1] in q and e[1] not in donors:rawmove(t,e);consume(e[1],e[3])
 need(not pending,'all real historical caches consumed');need(m.active==0,'all owned lifetimes closed')
 expected={**Fc,**{q[j]:{q[j]:F(1)} for j in M}}
 for x in donors:expected[q[x+112]]={q[x+112]:F(1),q[x]:F(1)}
 bad=[j for j in range(1880) if m.rows[j]!=expected[j]];need(not bad,'full1880 endpoint comparison '+str(bad[:12]))
 need(all(m.loc[j]==w['final'][j] for j in range(1480)) and all(m.loc[q[j]]==w['final'][j] for j in M),'all final charts')
 need(len(reservations)==1710 and len({r['source_event'] for r in reservations})==1710,'exact funded raw reservations')
 recipe={'schema':'unit17-precompensated-partial-second-copy/1','source_sha256':PIN,'initial':initial,'public':1880,'owned_fields':nextlabel-1880,'program':program,'marks':marks,'funded_raw_reservations':reservations,'difference_role_map':q,'completed_second_shear_donors':donors,'common_initial_precorrection':{j:list(map(str,r)) for j,r in K.items()},'raw_initial_gain_correction':mat['raw_initial_gain_correction_I_minus_B_Tinv'],'hub_correction':hub_repair,'entry_contract':'1480 independent first-copy inputs u and400 independent actual second-copy main inputs v; common helpers shared','exit_contract':'Complete original common native F(u);17 selected second-copy shears vY+=vX; other second-copy main values unchanged; all public fields at native final charts. This is a partial map.'}
 a.output.mkdir(parents=True,exist_ok=True);payload=(json.dumps(recipe,sort_keys=True,separators=(',',':'))+'\n').encode();a.output.joinpath('WORD.json.gz').write_bytes(gzip.compress(payload,mtime=0));result={'status':'PASS_TYPED_1880_INPUT_PRECOMPENSATED_UNIT17_PARTIAL_WORD','source_sha256':PIN,'word_payload_sha256':hashlib.sha256(payload).hexdigest(),'word_compressed_sha256':hashlib.sha256(a.output.joinpath('WORD.json.gz').read_bytes()).hexdigest(),'donors':donors,'public_rows_checked':1880,'complete_common_output_rows':1480,'completed_second_shear_pairs':17,'remaining_second_cross_dependencies':191,'original_common_instructions':len(w['program']),'physical_instructions':len(program),'operation_counts':dict(sorted(m.count.items())),'MOVE_histogram':dict(sorted(m.moves.items())),'common_MOVEs':6310,'funded_raw_MOVEs':1710,'new_owned_rank1_debt_MOVEs':17,'declared_owned_labels':nextlabel-1880,'peak_live_owned':m.peak,'purpose_counts':dict(sorted(Counter(marks).items())),'dependency_pins':{'observations_sha256':hashlib.sha256(a.observations.read_bytes()).hexdigest(),'joint_receipt_compressed_sha256':hashlib.sha256(a.joint.read_bytes()).hexdigest(),'matrices_sha256':hashlib.sha256(a.matrices.read_bytes()).hexdigest()},'scope':'Fully typed partial construction: complete common restoration and17 second-copy shears. Not a complete supplier or price improvement over direct17-channel delivery. No new kappa.'};a.output.joinpath('RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status']);print(result['operation_counts']);print('peak',m.peak,'instructions',len(program),'snapshots',len(hist))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--observations',type=Path,required=True);p.add_argument('--joint',type=Path,required=True);p.add_argument('--matrices',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
