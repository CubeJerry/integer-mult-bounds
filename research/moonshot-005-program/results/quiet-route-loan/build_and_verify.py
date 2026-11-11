#!/usr/bin/env python3
"""Literal source-bound quiet helper loan; arbitrary dirty inputs, exact rows."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
START=28048;CLOSE=30653;HELPER=449;DONOR=907;RECEIVER=977

def need(c,msg):
 if not c:raise ValueError(msg)
def add(a,b,c):
 for k,v in b.items():
  z=a.get(k,Q(0))+c*v
  if z:a[k]=z
  else:a.pop(k,None)
def span(vs):
 s={0}
 for v in vs:s|={x^v for x in s}
 return frozenset(s)
def source(path):
 b=path.read_bytes();need(hashlib.sha256(b).hexdigest()==PIN,'source hash');return json.loads(gzip.decompress(b))
def layout(w):
 M=sorted(set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));n=w['public'];need(len(M)==400 and n==1480,'public source inventory');return M,{r:n+i for i,r in enumerate(M)}
def construct(w):
 M,C=layout(w);n=w['public'];p=n+len(M);ops=[['ADD',C[r],r,'-1',w['initial'][r]] for r in M];q=C[DONOR];z=C[RECEIVER];loan_indices=[]
 def loan(e):loan_indices.append(len(ops));ops.append(e)
 def physical(e):
  x=e[:];x[1]=x[1]+400 if x[1]>=n else x[1]
  if x[0] in ('ADD','COPY'):x[2]=x[2]+400 if x[2]>=n else x[2]
  return x
 need(w['program'][START]==['MOVE',HELPER,3,594,False],'start route');need(w['program'][CLOSE]==['MOVE',DONOR,3,594,False],'closure route')
 for i,e in enumerate(w['program']):
  if i==START:
   loan(['ADD',HELPER,q,'1',3]);loan(['ADD',q,HELPER,'-1',3]);loan(['ADD',HELPER,q,'1',3])
  ops.append(physical(e))
  if e[0]=='MOVE' and e[1] in C:ops.append(['MOVE',C[e[1]],e[2],e[3],False])
  if i==START:loan(['ADD',z,HELPER,'1',594])
  if i==CLOSE:
   loan(['ADD',HELPER,q,'-1',594]);loan(['ADD',q,HELPER,'1',594]);loan(['ADD',HELPER,q,'-1',594])
 return {'schema':'moonshot-quiet-helper-loan-v1','source_sha256':PIN,'public':p,'owned_fields':w['owned_fields'],'initial':w['initial']+[w['initial'][r] for r in M],'final':w['final']+[w['final'][r] for r in M],'frames':w['frames'],'carrier_map':{str(r):q for r,q in C.items()},'program':ops,'loan_instruction_indices':loan_indices,'loan':{'helper':HELPER,'donor_main':DONOR,'receiver_main':RECEIVER,'start_source_event':START,'close_source_event':CLOSE},'scope':'Exact complete reference source with raw difference carriers; final difference bank is one elementary shear, not the required second native action.'}
def replay(ops,initial,frames,public,owned):
 rows=[{r:Q(1)} if r<public else {} for r in range(public+owned)];cur=initial+[None]*owned;live=set(range(public));life=peak=0;counts=Counter();hist=Counter();ownedhist=Counter();spans=list(map(span,frames))
 for i,e in enumerate(ops):
  op,r=e[:2];need(0<=r<public+owned,'holder index');counts[op]+=1
  if op=='INIT':need(r>=public and r not in live and cur[r] is None,'owned init');rows[r]={};cur[r]=e[2];live.add(r);life+=1
  elif op=='CLEAR':need(r>=public and r in live and cur[r]==e[2],'owned clear');rows[r]={};cur[r]=None;live.remove(r)
  elif op=='MOVE':
   need(r in live and cur[r]==e[2],'move source frame');need(type(e[4]) is bool and e[4]==(r>=public),'move ownership');a,b=spans[e[2]],spans[e[3]];need(a<b if r<public else a<b or b<a,'nested transport');rank=abs(len(frames[e[2]])-len(frames[e[3]]));hist[rank]+=1
   if r>=public:ownedhist[rank]+=1
   cur[r]=e[3]
  elif op in ('ADD','COPY'):
   s=e[2];need(r in live and s in live and r!=s and cur[r]==cur[s]==e[4],'current cochart add');c=Q(e[3]);need(c!=0,'nonzero add')
   if op=='COPY':need(not rows[r],'all-input COPYzero')
   add(rows[r],rows[s],c)
  elif op=='SCALE':need(r in live and cur[r]==e[3] and Q(e[2])!=0,'nonzero current scale');rows[r]={j:v*Q(e[2]) for j,v in rows[r].items()}
  else:raise ValueError(op)
  peak=max(peak,sum(q>=public for q in live))
 return rows,cur,{'counts':dict(counts),'move_histogram':dict(sorted(hist.items())),'owned_move_histogram':dict(sorted(ownedhist.items())),'owned_lifetimes':life,'peak_owned':peak,'final_live_owned':sum(q>=public for q in live)}
def verify(w,t):
 M,C=layout(w);n=w['public'];p=t['public'];need(p==1880 and t['owned_fields']==w['owned_fields'],'physical inventory');need(t['frames']==w['frames'] and t['initial']==w['initial']+[w['initial'][r] for r in M],'literal input frames');need(t['source_sha256']==PIN,'transcript source pin')
 # Check the actual helper blackout, rather than presuming a value-only silence.
 touches=[]
 for i in range(START+1,CLOSE+1):
  e=w['program'][i]
  if e[1]==HELPER or e[0] in ('ADD','COPY') and e[2]==HELPER:touches.append(i)
 need(not touches,'quiet helper window')
 nextuse=next(i for i in range(CLOSE+1,len(w['program'])) if w['program'][i][1]==HELPER or w['program'][i][0] in ('ADD','COPY') and w['program'][i][2]==HELPER)
 need(nextuse==30837,'next helper use')
 rows,cur,bill=replay(t['program'],t['initial'],t['frames'],p,t['owned_fields']);base,bcur,baseline=replay(w['program'],w['initial'],w['frames'],n,w['owned_fields'])
 def maprole(r):return r if r<n else r+400
 for r in range(n+w['owned_fields']):need(rows[maprole(r)]==base[r] and cur[maprole(r)]==bcur[r],'exact full first-copy source output')
 for r in M:
  want={C[r]:Q(1),r:Q(-1)}
  if r==RECEIVER:add(want,{C[DONOR]:Q(1),DONOR:Q(-1)},Q(1))
  need(rows[C[r]]==want and cur[C[r]]==w['final'][r],'exact final elementary difference shear')
 need(cur[:p]==t['final'],'full final public frames');need(bill['final_live_owned']==0,'original cleanup')
 funded=Counter(abs(len(w['frames'][e[2]])-len(w['frames'][e[3]])) for e in w['program'] if e[0]=='MOVE' and e[1] in C)
 expected=Counter(baseline['move_histogram']);expected.update(funded);need(dict(sorted(expected.items()))==bill['move_histogram'],'no added transport beyond second main itineraries');need(bill['owned_move_histogram']==baseline['owned_move_histogram'],'unchanged owned route invoice');need(bill['owned_lifetimes']==baseline['owned_lifetimes'] and bill['peak_owned']==baseline['peak_owned'],'no extra lifecycle')
 extra=Counter(bill['counts']);extra.subtract(Counter(baseline['counts']));need(extra['ADD']==407 and extra['MOVE']==sum(funded.values()) and all(v==0 for k,v in extra.items() if k not in ('ADD','MOVE')),'exact scalar and funded route counts')
 return {'status':'PASS_EXACT_SOURCE_QUIET_LOAN','source_sha256':PIN,'formal_input_columns':p,'physical_events':len(t['program']),'loan_ADDs':7,'difference_formation_ADDs':400,'extra_MOVEs':0,'funded_second_main_MOVEs':sum(funded.values()),'extra_owners':0,'extra_lifetimes':0,'quiet_interval':[START+1,CLOSE],'next_helper_use':nextuse,'first_copy_roles_checked':n+w['owned_fields'],'difference_outputs_checked':len(M),'first_copy_source_bill':baseline,'physical_bill':bill,'final_difference_effect':'q977 <- q977 + q907; every other q is unchanged','scope':t['scope']}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--transcript',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args();w=source(a.source);t=construct(w);payload=(json.dumps(t,sort_keys=True,separators=(',',':'))+'\n').encode();r=verify(w,t);r['transcript_payload_sha256']=hashlib.sha256(payload).hexdigest();controls=[]
 for name in ('wrong_restore_sign','wrong_delivery_chart','wrong_public_MOVE_flag'):
  z=json.loads(payload)
  if name=='wrong_restore_sign':z['program'][z['loan_instruction_indices'][-1]][3]='1'
  elif name=='wrong_delivery_chart':z['program'][z['loan_instruction_indices'][3]][4]=3
  else:
   donor=z['carrier_map'][str(DONOR)];e=next(e for e in z['program'] if e[0]=='MOVE' and e[1]==donor);e[4]=True
  try:verify(w,z)
  except ValueError as ex:controls.append({'mutation':name,'rejection':str(ex)})
  else:raise ValueError('negative control accepted '+name)
 r['negative_controls']=controls
 if a.transcript:a.transcript.write_bytes(gzip.compress(payload,mtime=0))
 s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(s)
if __name__=='__main__':main()
