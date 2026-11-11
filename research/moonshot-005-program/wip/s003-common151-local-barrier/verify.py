import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(p,s):
 if not p:raise ValueError(s)
def span(vs):
 x={0}
 for v in vs:x|={q^v for q in tuple(x)}
 return frozenset(x)
def run(source):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));n=w['public'];frames=list(map(span,w['frames']));cur=w['initial']+[None]*w['owned_fields'];value=[F(i==55) for i in range(n+w['owned_fields'])]
 need(w['program'][30773]==['MOVE',151,327,541,False],'source MOVE')
 for e in w['program'][:30774]:
  op,h=e[:2]
  if op=='INIT':need(cur[h] is None,'fresh');cur[h]=e[2];value[h]=F(0)
  elif op=='CLEAR':need(cur[h]==e[2],'clear chart');cur[h]=None;value[h]=F(0)
  elif op=='MOVE':need(cur[h]==e[2],'MOVE source');cur[h]=e[3]
  elif op=='SCALE':need(cur[h]==e[3],'SCALE chart');value[h]*=F(e[2])
  elif op in ['ADD','COPY']:
   need(cur[h] is not None and cur[e[2]] is not None and frames[cur[h]]==frames[cur[e[2]]]==frames[e[4]],'cochart')
   if op=='COPY':need(value[h]==0,'COPY zero');value[h]=F(0)
   value[h]+=F(e[3])*value[e[2]]
  else:raise ValueError(op)
 observers=[h for h,f in enumerate(cur) if f is not None and frames[f]==frames[541] and h!=151]
 need(observers==[130,472,745,899,1359],'complete actual cochart inventory')
 need(all(value[h]==0 for h in observers),'dual annihilates all observations')
 need(value[151]==F(1,2),'dual target value')
 need(cur[55]!=541 and frames[cur[55]]!=frames[541],'witness common input not locally exposed')
 return {'status':'PASS_COMMON151_IMMEDIATE_LOCAL_BARRIER','source_sha256':PIN,
         'cut':30774,'event_completed':30773,'common_input_domain':1480,
         'input_witness':{'55':'1'},'same_input_in_both_copies':True,'all_main_differences':0,
         'destination_chart':541,'excluded_borrowed_helper':151,'available_actual_cochart_roles':observers,
         'observer_values':{str(h):str(value[h]) for h in observers},'required_common151':'1/2',
         'positive_control_if_original_helper151_granted':'target observable has value1/2',
         'scope':'Immediate original cochart common/owned values excluding151 cannot determine common151, even when loan q payloads are given and allq=0. Additional cached history, changed routes, private escrow recovery, or later decoding are not excluded. No new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.source);a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(r['status'])
