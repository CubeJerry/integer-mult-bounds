#!/usr/bin/env python3
"""Source-preserving affine injection from six actual private acquisition charts."""
from pathlib import Path
import argparse,copy,hashlib,json
BASE='5566738ce7b2706c0094654fce0e4c1c438e82395dee2e6885ef917f2d4498f3'
def build(w,parameters):
 out=copy.deepcopy(w);out['base_word_sha256']=BASE;ops=[];stepmap={};spec=[]
 for z in range(6):
  if z<3:
   f=w['forks'][z];i,q=[3,76,80][z],[21,64,65][z];chart=f'D{i}_{q}';allowed=f['group'];targets=[i,q];ret=f'KEEP_C{z}'
  else:
   i=[4,74,78][z-3];chart=f'F{i}';allowed=w['h1_private_roles'][str(i)];targets=[i];ret=f'ZFIRST{z}'
  roles=parameters[z];assert len(set(roles))==len(roles)and set(roles)<=set(allowed)
  if not roles:continue
  name=f'AFF{z}';row=sum(1<<j for j in roles)
  spec.append({'packet':z,'owner':name,'chart':chart,'roles':sorted(roles),'allowed_roles':allowed,'row_hex':hex(row),'old_receivers':targets,'first_retention':ret})
  ops.append(['INIT',name,chart])
  dd=(out['multi_retention']if z<3 else out['m1_retention'])[z if z<3 else z-3]
  dd['first_retention_hex']=hex(int(dd['first_retention_hex'],16)^row)
 captured=set();queried=set();corrected=set()
 for oldstep,o in enumerate(w['operations'],1):
  op,n,*q=o
  if op=='MOVE'and n.startswith('Y'):
   i=int(n[1:])
   for s in spec:
    if s['packet']<3 and i in s['old_receivers']and q[0]==f'F{i}':
     ops.extend([['MOVE',n,s['chart']],['ADD',s['owner'],n]]);corrected.add((s['packet'],i))
  ops.append(o)
  if op=='MOVE':
   for s in spec:
    if q[0]!=s['chart']:continue
    if n.startswith('X')and int(n[1:])in s['roles']and(s['packet'],n)not in captured:
     ops.append(['ADD',n,s['owner']]);captured.add((s['packet'],n))
    if n==f"P{s['packet']}"and s['packet']not in queried:
     ops.append(['ADD',s['owner'],n]);queried.add(s['packet'])
    if s['packet']>=3 and n.startswith('Y')and int(n[1:])in s['old_receivers']:
     ops.append(['ADD',s['owner'],n]);corrected.add((s['packet'],int(n[1:])))
  stepmap[oldstep]=len(ops)
 for s in spec:ops.append(['CLEAR',s['owner']])
 assert len(captured)==sum(len(s['roles'])for s in spec)
 assert queried=={s['packet']for s in spec}
 assert corrected=={(s['packet'],i)for s in spec for i in s['old_receivers']}
 out['operations']=ops;out['milestones']={k:stepmap[v]for k,v in w['milestones'].items()};out['affine_injections']=spec
 out['affine_scope']='Actual higher-chart substitutions. First retention changes; old and new preload are not both freely available. No new endpoint or kappa.'
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--parameters',default='[[10],[],[],[25,51],[],[]]');a=p.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;w=build(json.loads(raw),json.loads(a.parameters));a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json').write_text(json.dumps(w,indent=2)+'\n');print(hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest())
if __name__=='__main__':main()
