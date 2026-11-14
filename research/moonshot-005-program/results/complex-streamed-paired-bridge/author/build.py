#!/usr/bin/env python3
"""One actual zero-restored carrier streams two native paired factors.

@CubeJerry, substantial OpenAI assistance, Apache-2.0. No complete supplier.
"""
from __future__ import annotations
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
NATIVE_PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
SEED_PIN='6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc'
ENGINE_PIN='045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e'
J=[1,6,32,33,48,49,50,73,74,75,82,83,84,85,98];T=[0,7]
C_FRAME=[263,135,71,32,19,13];D_FRAME=[256,128,64,32,19,10,7]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(x):return hashlib.sha256(x).hexdigest()
def load(path,pin):
 raw=path.read_bytes();need(sha(raw)==pin,'source pin '+str(path));return json.loads(gzip.decompress(raw))
def clean(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):clean(v)for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [clean(v)for v in x]
 return x

def main(a):
 need(sha(a.engine.read_bytes())==ENGINE_PIN,'retained replay engine pin');sp=importlib.util.spec_from_file_location('streamed_paired_replay',a.engine);e=importlib.util.module_from_spec(sp);sys.modules[sp.name]=e;sp.loader.exec_module(e)
 seed=load(a.seed,SEED_PIN);native=load(a.native,NATIVE_PIN);roles={int(k):v for k,v in seed['source_role_map'].items()};ports=native['live'];host={native['live'][i]:(roles[b],roles[d])for i,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2'])};X={j:roles[j]for j in ports};Y={j:roles[j+112]for j in ports};need(set(J+T)<=set(host),'all real hosted companions')
 frames=copy.deepcopy(seed['frames']);spaces=[e.span(f)for f in frames]
 def chart(f):
  ss=e.span(f)
  if ss not in spaces:spaces.append(ss);frames.append(f)
  return spaces.index(ss)
 C=chart(C_FRAME);D=chart(D_FRAME);Hub=127;facets={h:spaces.index(e.span(native['frames'][native['final'][h+112]]))for h in ports};group=next(z for z in seed['duplex']['groups']if set(T)<=set(z['hosted']));C3=group['C'];need(len(frames[C])==6 and len(frames[D])==7 and spaces[C]<spaces[D],'actual unit bridge')
 need(spaces[C3]<spaces[D] and all(spaces[D]<spaces[facets[h]]for h in T),'actual receiver chains');need(all(spaces[seed['initial'][X[j]]]<spaces[C]for j in J),'actual donor lines below C')
 def root(h):
  v=native['frames'][native['initial'][h]][0];on=[i for i in range(9)if v>>i&1]
  if len(on)==3:return [2 if i in on else -1 for i in range(9)]
  off=[i for i in range(9)if not(v>>i&1)];return [3*(int(i==off[0])-int(i==off[1]))for i in range(9)]
 roots={h:root(h)for h in ports};G=lambda h,j:F(sum(x*y for x,y in zip(roots[h],roots[j])),18);P=[[-G(h,j)for j in J]for h in T];need(e.exact_rank([{j:x for j,x in enumerate(row)if x}for row in P])==2,'actual target block rank2');need(all(abs(x)==F(1,2)for row in P for x in row),'all30 target coefficients, exact dyadic primitive')
 r,s=408,411;caches={T[0]:409,T[1]:410};selected_XB={X[j]for j in J}|{host[j][0]for j in J};selected_D={host[h][1]:h for h in T};selected_Y={Y[h]:h for h in T};out=[];marks={};phases=[];changed=[];oldmap={0:0}
 def emit(o):out.append(o)
 def add(dst,src,c,at):emit(['ADD',dst,src,str(c),at])
 def move(role,src,dst):emit(['MOVE',role,src,dst,True])
 def block():
  marks['begin']=len(out)
  for h in T:emit(['INIT',caches[h],D])
  if a.mode=='streaming':emit(['INIT',r,C])
  for i,h in enumerate(T):
   phase={'factor':i,'begin':len(out)}
   if a.mode=='independent':emit(['INIT',r,C]);emit(['INIT',s,D])
   for j,p in zip(J,P[i]):add(r,X[j],p,C)
   move(r,C,D);phase['arrival']=len(out)
   if a.mode=='streaming'and i:
    phase['previous_adjoint_subtraction']=len(out);add(r,host[T[i-1]][1],-1,D)
   phase['pure_primal']=len(out);add(caches[h],r,1,D);phase['output_stored']=len(out)
   add(r,caches[h],-1,D);phase['primal_zero']=len(out)
   carrier=r if a.mode=='streaming'else s;add(carrier,host[h][1],1,D);move(carrier,D,C)
   for j,p in zip(J,P[i]):add(host[j][0],carrier,-p,C)
   phase['adjoint_consumed']=len(out)
   if a.mode=='independent':
    move(s,C,D);add(s,host[h][1],-1,D);phase['zero_retirement']=len(out);emit(['CLEAR',r,D]);emit(['CLEAR',s,D])
   phases.append(phase)
  if a.mode=='streaming':
   marks['final_cleanup_move']=len(out);move(r,C,D);marks['final_cleanup_subtraction']=len(out);add(r,host[T[-1]][1],-1,D);marks['zero_retirement']=len(out);emit(['CLEAR',r,D])
  marks['end']=len(out)
  for h in T:emit(['MOVE',host[h][1],D,facets[h],False])
  for j in J:emit(['MOVE',X[j],C,Hub,False]);emit(['MOVE',host[j][0],C,Hub,False])
  marks['slot_end']=len(out)
 slotend=seed['duplex']['markers']['XB_slot_end']
 for t,o0 in enumerate(seed['program']):
  if t==slotend:block()
  o=copy.deepcopy(o0)
  if o[0]=='MOVE'and o[1]in selected_D and o[2]==C3 and o[3]==facets[selected_D[o[1]]]:o[3]=D;changed.append((t,'D_hold'))
  elif o[0]=='MOVE'and o[1]in selected_XB and o[3]==Hub:need(t<slotend,'only original XB ascent');o[3]=C;changed.append((t,'XB_hold'))
  elif o[0]=='MOVE'and o[1]in selected_Y and o[2]==C3 and o[3]==facets[selected_Y[o[1]]]:
   h=selected_Y[o[1]];emit(['MOVE',o[1],C3,D,False]);add(o[1],caches[h],1,D);emit(['CLEAR',caches[h],D]);o[2]=D;changed.append((t,'Y_read'))
  emit(o);oldmap[t+1]=len(out)
 need(len(changed)==34,'exact native route replacements')
 w={k:copy.deepcopy(v)for k,v in seed.items()if k not in('duplex','program')};w.update(schema='moonshot-S012-single-carrier-streamed-paired-bridge-v1',program=out,frames=frames,owned_fields=11 if a.mode=='streaming'else 12,streaming={'mode':a.mode,'donors':J,'receivers':T,'C':C,'D':D,'C3':C3,'P':clean(P),'Q':[['1','0'],['0','1']],'L':[['1','0'],['0','1']],'relay':r,'independent_return_relay':s if a.mode=='independent'else None,'cache_fields':caches,'phases':phases,'markers':marks,'seed_boundary_to_new':oldmap,'seed_sha256':SEED_PIN,'native_sha256':NATIVE_PIN})
 base,base_locs,base_bill=e.replay(seed,seed['program']);observations=[];boundary_rows=[]
 def capture(t,o,rows,loc):
  k=t+1
  if o is not None and o[0]=='MOVE' and o[1]in(r,s) and marks['begin']<=t<marks['end']:
   boundary_rows.append(copy.deepcopy(rows[o[1]]))
  for phase in phases:
   i=phase['factor'];h=T[i]
   if k==phase['pure_primal']:
    need(rows[r]=={X[j]:p for j,p in zip(J,P[i])},'actual current primal row after adjoint cancellation');need(loc[r]==D,'primal arrival at D');observations.append(('primal',i))
   if k==phase['output_stored']:
    for u in range(i+1):need(rows[caches[T[u]]]=={X[j]:p for j,p in zip(J,P[u])},'actual prefix output cache invariant')
   if k==phase['primal_zero']:need(rows[r]=={},'actual zero-output left-inverse cleanup')
   if k==phase['adjoint_consumed']:
    carrier=r if a.mode=='streaming'else s;need(rows[carrier]=={host[h][1]:F(1)} and loc[carrier]==C,'actual current adjoint carrier at C')
    for j in J:
     wanted={host[j][0]:F(1)}
     for u in range(i+1):wanted=e.add(wanted,{host[T[u]][1]:F(1)},-P[u][J.index(j)])
     need(rows[host[j][0]]==wanted,'actual accumulated B current rows')
   if k==phase.get('zero_retirement'):need(rows[r]=={}and rows[s]=={}and loc[r]==D and loc[s]==D,'independent actual zero retirements')
  if k==marks.get('zero_retirement'):need(rows[r]=={}and loc[r]==D,'actual final zero at D, not C')
 rows,loc,bill=e.replay(w,out,capture);want=copy.deepcopy(base)
 for h,prow in zip(T,P):
  for j,p in zip(J,prow):want[Y[h]]=e.add(want[Y[h]],{X[j]:F(1)},p);want[host[j][0]]=e.add(want[host[j][0]],{host[h][1]:F(1)},-p)
 need(rows==want and loc==base_locs,'complete400-column source map and final chart equality');need(e.exact_rank(rows.values())==400,'all400 original inputs retained');need(all(rows[host[h][0]].get(host[j][1],F(0))+rows[Y[j]].get(X[h],F(0))==0 for h in host for j in host),'all9216 paired transpose entries')
 raw=Counter();owned=Counter()
 for o in out:
  if o[0]=='MOVE':(owned if o[4]else raw)[abs(len(frames[o[3]])-len(frames[o[2]]))]+=1
 need(dict(raw)=={1:116,2:112,3:118,4:4,5:226,8:170},'complete original-route tariff');need(dict(owned)=={1:13 if a.mode=='streaming'else 14,8:16},'complete owned tariff');need(sum(k*v for k,v in raw.items())==3200,'public rank mass3200')
 debt=sum(len(e.add(rows[Y[h]],{X[h]:F(1)if h in host else F(1,2),Y[h]:F(1)if h in host else F(1,2)},F(-1)))for h in ports);rr=e.exact_rank([e.add(rows[b],{b:F(1),d:F(-1)},F(-1))for h,(b,d)in host.items()]);need(debt==5346,'expanded forward debt reduced by30')
 positive_observations=copy.deepcopy(observations);boundary_rank=e.exact_rank(boundary_rows);need(boundary_rank==4,'two independent primal and two adjoint transported modes')
 controls=[];mutants={'omit_output_cleanup':phases[0]['primal_zero']-1,'wrong_adjoint_consumer':phases[-1]['adjoint_consumed']-1}
 if a.mode=='streaming':mutants.update(omit_previous_adjoint_cancellation=phases[1]['previous_adjoint_subtraction'],omit_final_cleanup=marks['final_cleanup_subtraction'])
 for label,k in mutants.items():
  bad=copy.deepcopy(w);bad['program'][k][3]='0'
  try:mr,ml,_=e.replay(bad,bad['program'],capture);reject=mr!=rows or ml!=loc
  except ValueError:reject=True
  need(reject,'negative control '+label);controls.append(label)
 bad=copy.deepcopy(w);k=next(i for i,o in enumerate(out)if o[0]=='CLEAR'and o[1]==r);bad['program'][k][2]=C
 try:e.replay(bad,bad['program']);reject=False
 except ValueError:reject=True
 need(reject,'false home retirement');controls.append('false_home_retirement_at_C')
 payload=(json.dumps(clean(w),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0);a.output.mkdir(parents=True,exist_ok=True);(a.output/'WORD.json.gz').write_bytes(blob);result={'status':'PASS_ACTUAL_STREAMED_PAIRED_NATIVE_BLOCK','mode':a.mode,'word_sha256':sha(blob),'payload_sha256':sha(payload),'seed_word_sha256':SEED_PIN,'native_sha256':NATIVE_PIN,'replay_engine_sha256':ENGINE_PIN,'target_block_rank':2,'transported_boundary_rank':boundary_rank,'new_moving_owner_lifetimes':1 if a.mode=='streaming'else 4,'paired_coefficients_removed_each_side':30,'all400_input_rank':400,'all_final_charts_equal_seed':True,'all_original_D_restored':True,'hosted_R_plus_L_transpose_zero':True,'relay_zero_at_retirement':True,'relay_terminal_chart':'D','relay_return_to_birth_C_claimed':False,'source_bill':bill,'raw_histogram':dict(raw),'owned_histogram':dict(owned),'current_a_forward_offdiagonal_coefficients':4962,'original_coordinate_forward_debt':debt,'reverse_residual_rank':rr,'observed_phase_primal_rows':positive_observations,'negative_controls':controls,'new_scalar_denominators':[1,2],'all_source_scalar_denominators':sorted({F(o[3]if o[0]=='ADD'else o[2]).denominator for o in out if o[0]in('ADD','SCALE')}),'scope':'Two genuine paired source factors with actual changing carrier history and full caller price. Partial source only; no new complete kappa or foundation discharge.'};(a.output/'RESULT.json').write_text(json.dumps(clean(result),sort_keys=True,indent=2)+'\n');print(json.dumps(clean(result),indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seed',type=Path,required=True);p.add_argument('--native',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--mode',choices=['streaming','independent'],default='streaming');main(p.parse_args())
