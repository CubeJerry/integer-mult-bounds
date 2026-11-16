#!/usr/bin/env python3
from pathlib import Path
import argparse,copy,hashlib,json
from private_builder import build as private_build,BASE
DEFAULT='[[10],[],[],[25,51],[],[],[60],[13],[59],[20]]'
def build(base,parameters):
 assert len(parameters)==10;w=private_build(base,parameters[:6]);out=copy.deepcopy(w);ops=[];spec=[];stepmap={}
 for k,(z,ch)in enumerate([(3,'C1'),(4,'C4'),(5,'C3'),(6,'Extra6')],6):
  roles=parameters[k];allowed=(next(d['roles']for d in w['cache_metadata']if d['chart']==ch)if k<9 else w['history_extra_query_roles'])
  assert len(roles)==len(set(roles))and set(roles)<=set(allowed)
  if not roles:continue
  name=f'PAIR{z}'if k<9 else'EXTRA_AFF';row=sum(1<<j for j in roles);receivers=[[4],[74],[78],[]][k-6]
  s={'parameter_group':k,'packet':z,'owner':name,'chart':ch,'roles':sorted(roles),'allowed_roles':allowed,'row_hex':hex(row),'old_receivers':receivers,'first_retention':f'ZFIRST{z}'if k<9 else None};spec.append(s);ops.append(['INIT',name,ch])
  if k<9:
   d=out['m1_retention'][z-3];d['first_retention_hex']=hex(int(d['first_retention_hex'],16)^row)
  else:out['seed_rows_hex'][6]=hex(int(out['seed_rows_hex'][6],16)^row)
 captured=set();queried=set();corrected=set()
 for oldstep,o in enumerate(w['operations'],1):
  op,n,*q=o
  if op=='MOVE'and n.startswith('Y'):
   i=int(n[1:])
   for s in spec:
    if i in s['old_receivers']and q[0]==f'F{i}':ops.extend([['MOVE',n,s['chart']],['ADD',s['owner'],n]]);corrected.add((s['packet'],i))
  ops.append(o)
  if op=='MOVE':
   for s in spec:
    if q[0]!=s['chart']:continue
    if n.startswith('X')and int(n[1:])in s['roles']and(s['packet'],n)not in captured:ops.append(['ADD',n,s['owner']]);captured.add((s['packet'],n))
    if n==f"P{s['packet']}"and s['packet']not in queried:ops.append(['ADD',s['owner'],n]);queried.add(s['packet'])
  stepmap[oldstep]=len(ops)
 for s in spec:ops.append(['CLEAR',s['owner']])
 assert len(captured)==sum(len(s['roles'])for s in spec)and queried=={s['packet']for s in spec}
 assert corrected=={(s['packet'],i)for s in spec for i in s['old_receivers']}
 out['operations']=ops;out['milestones']={k:stepmap[v]for k,v in w['milestones'].items()};out['higher_shared_injections']=spec
 out['base_ground_code_metadata']=out.pop('ground_code');out['ground_code']='Actual terminal rows in seed_rows_hex; P6 changes by the acquired Extra6 row. The old canonical code is not also granted.'
 out['affine_scope']='Actual72-parameter higher-chart family. Preserves30 endpoints; no complete supplier or newkappa.'
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--parameters',default=DEFAULT);a=p.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;w=build(json.loads(raw),json.loads(a.parameters));a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json').write_text(json.dumps(w,indent=2)+'\n');print(hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest())
if __name__=='__main__':main()
