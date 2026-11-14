#!/usr/bin/env python3
"""Independent dense400-column review of the two target-relation words."""
import argparse,gzip,hashlib,json,importlib.util,math,copy
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
def need(x,s):
 if not x:raise ValueError(s)
def load(p,pin=None):
 b=p.read_bytes();need(pin is None or hashlib.sha256(b).hexdigest()==pin,'pin');return json.loads(gzip.decompress(b))
def rank(rows):
 b={}
 for row in rows:
  r=list(row)
  for p,v in sorted(b.items()):
   if r[p]:
    x,y=r[p],v[p];r=[y*a-x*c for a,c in zip(r,v)];g=math.gcd(*r)
    if g>1:r=[x//g for x in r]
  p=next((p for p,x in enumerate(r) if x),None)
  if p is not None:b[p]=r
 return len(b)
def main(a):
 need(hashlib.sha256(a.engine.read_bytes()).hexdigest()=='c4389c80322c875c4739af6ee558619f01da6112682c565e4f638a01750e5ec1','independent dense engine pin')
 spec=importlib.util.spec_from_file_location('independent_dense',a.engine);e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
 n=load(a.native,'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883');p=load(a.parent,'a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc');f=load(a.four,'20a5c2c3eccd000b757f65e2cd6bed7f8a9ec39f0b8f88a66716e4b818a2521f')
 q=dict(f);q['program']=[o for o,t in zip(f['program'],f['parent_event_of_output']) if t is None or t<p['consumer']['begin']]
 old,od,ol,ob,_=e.run(q,list(map(e.span,q['frames'])))
 roles={int(k):v for k,v in p['source_role_map'].items()};host={n['live'][i]:(roles[b],roles[d]) for i,b,d in zip(n['hosted']['Dports'],n['hosted']['X2'],n['hosted']['Y2'])}
 def residual(rr,d):
  out=[]
  for h,(b,z) in sorted(host.items()):
   row=list(rr[b]);row[b]-=d;row[z]+=d;out.append(row)
  return out
 need(rank(residual(old,od))==82,'baseline rank82');results={}
 for variant,sub in [('C6','output-shared6'),('C2','output')]:
  word=a.bundle/sub/'WORD.json.gz';w=load(word);cache=493;ops=w['program'];sp=list(map(e.span,w['frames']))
  need(w['public']==400 and w['initial']==q['initial'] and w['owned_fields']==94,'unchanged input interface')
  init=next(i for i,o in enumerate(ops) if o[:2]==['INIT',cache]);clear=next(i for i,o in enumerate(ops) if o[:2]==['CLEAR',cache]);own=[(i,o) for i,o in enumerate(ops) if o[1]==cache];moves=[(i,o) for i,o in own if o[0]=='MOVE'];need(len(moves)==1 and moves[0][1][3]==127,'one actual return')
  consume=[i for i,o in own if o[0]=='ADD' and o[2] in (209,298) and o[4]==127];need(len(consume)==2,'both actual current B subtractions')
  controller=[i for i,o in own if o[0]=='ADD' and o[2]<104 and o[4]==127];need(len(controller)==49,'49 actual controller adds')
  capture={max(controller):('target',[cache]),max(consume):('innovation',[cache])}
  new,nd,nl,nb,sn=e.run(w,sp,capture_after=capture)
  target={209:F(1),298:F(1),305:F(-1),394:F(-1)};innov={348:F(1),355:F(1),391:F(-1)}
  for label,want in [('target',target),('innovation',innov)]:
   d,rs,ls=sn[label];need(ls[cache]==127 and all(F(x,d)==want.get(j,0) for j,x in enumerate(rs[cache])),'actual '+label)
  need(nl==ol,'all original final charts');need(all(e.eqrow(new[i],nd,old[i],od) for i in range(400) if i!=209),'all399 unchanged public output rows')
  need(all(F(new[209][j],nd)==F(old[209][j],od)+innov.get(j,0) for j in range(400)),'only exact B1 shear')
  E=residual(new,nd);need(rank(E)==81,'new exact residual rank81');need(all(any(row) for row in E),'no individual B completed')
  i=list(sorted(host)).index(1);j=list(sorted(host)).index(106);need(all(x+y==0 for x,y in zip(E[i],E[j])),'exact target relation')
  debt=0
  for h in n['live']:
   c=F(1) if h in host else F(1,2);b=roles[h+112]
   debt+=sum(F(new[b][j],nd)!=c*int(j==roles[h])+c*int(j==b) for j in range(400))
  need(debt==4920,'remaining full forward debt')
  delta={j:nb['moves'].get(j,0)-ob['moves'].get(j,0) for j in set(nb['moves'])|set(ob['moves'])};delta={j:c for j,c in delta.items() if c}
  need(delta==({3:1} if variant=='C6' else {1:2,4:2,5:-2,7:1}),'full MOVE delta')
  need(nb['counts']['ADD']-ob['counts']['ADD']==54 and nb['lifetimes']==ob['lifetimes']+1 and nb['peak']==29,'all paid extras')
  controls=[]
  for name,t in [('missing_controller',controller[0]),('missing_current_B106',consume[1]),('missing_actual_return',moves[0][0]),('missing_second_snapshot_read',init+2)]:
   bad=dict(w);bad['program']=ops[:t]+ops[t+1:]
   try:
    rr,dd,ll,bb,_=e.run(bad,sp)
    need(ll==nl and all(e.eqrow(rr[r],dd,new[r],nd) for r in new),'changed all-column endpoint')
   except (AssertionError,ValueError):controls.append(name)
   else:raise ValueError('accepted corrupt word '+name)
  results[variant]=dict(word_sha256=hashlib.sha256(word.read_bytes()).hexdigest(),old_rank=82,new_rank=81,remaining_forward_coefficients=debt,individual_hosted_rows_completed=0,all399_other_public_rows_unchanged=True,full_bill=nb,move_delta=delta,new_ordered_pairs=sorted(set((o[2],o[3]) for o in ops if o[0]=='MOVE')-set((o[2],o[3]) for o in q['program'] if o[0]=='MOVE')),negative_controls=controls)
 out=dict(status='PASS_INDEPENDENT_ACTUAL_TARGET_RELATION',engine_sha256=hashlib.sha256(a.engine.read_bytes()).hexdigest(),results=results,scope='Finite exact scalar words and nested real binary-chart chronology; general compiler and remaining81 reverse rank/4920 forward coefficients open. Alternatives, not additive gains.',new_kappa=None)
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'ranks':{k:v['new_rank'] for k,v in results.items()}}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['native','parent','four','bundle','engine','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
