#!/usr/bin/env python3
"""Paid rectangular paired echo on the pinned omitted-line Gram seed.

@CubeJerry, with OpenAI assistance. Apache-2.0. No complete supplier claim.
"""
from __future__ import annotations
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
SEED_PIN='6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc'
NATIVE_PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
ENGINE_PIN='045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e'
DONORS=[32,48,85,98];RECEIVERS=[0,7,87,92]
C_FRAME=[426,74,25,7];D_FRAME=[384,74,42,25,7]
P=[F(1,2),F(-1,2),F(1,2),F(1,2)];Q=[F(-1),F(1),F(-1),F(1)]
def need(v,m):
 if not v:raise ValueError(m)
def digest(b):return hashlib.sha256(b).hexdigest()
def load(p,pin):
 b=p.read_bytes();need(digest(b)==pin,'source pin: '+str(p));return json.loads(gzip.decompress(b))
def clean(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):clean(v)for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(y)for y in x]
 return x

def main(a):
 need(digest(a.engine.read_bytes())==ENGINE_PIN,'replay engine pin');spec=importlib.util.spec_from_file_location('retained_echo_replay',a.engine);e=importlib.util.module_from_spec(spec);sys.modules[spec.name]=e;spec.loader.exec_module(e)
 native=load(a.native,NATIVE_PIN);seed=load(a.seed,SEED_PIN);role={int(k):v for k,v in seed['source_role_map'].items()};ports=native['live'];host={native['live'][i]:(role[b],role[d]) for i,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2'])};X={h:role[h]for h in ports};Y={h:role[h+112]for h in ports}
 need(set(DONORS+RECEIVERS)<=set(host),'actual independent hosted banks')
 frames=copy.deepcopy(seed['frames']);spaces=[e.span(f)for f in frames]
 def chart(f):
  s=e.span(f)
  if s not in spaces:spaces.append(s);frames.append(f)
  return spaces.index(s)
 C=chart(C_FRAME);D=chart(D_FRAME);Hub=127;O=3
 group=next(z for z in seed['duplex']['groups']if set(RECEIVERS)<=set(z['hosted']));C3=group['C'];facets={h:native['final'][h+112]for h in ports}
 # Native chart identifiers and source-interface frame identifiers may differ;
 # resolve by exact subspace, never by a guessed numerical alias.
 facets={h:spaces.index(e.span(native['frames'][facets[h]]))for h in ports}
 need(len(frames[C])==4 and len(frames[D])==5 and spaces[C]<spaces[D],'proper rank-one bridge')
 need(spaces[C3]<spaces[D] and all(spaces[D]<spaces[facets[h]]for h in RECEIVERS),'actual receiver C3-D-facet chains')
 need(all(spaces[seed['initial'][X[j]]]<spaces[C]for j in DONORS),'actual original donor access at C')
 def root(h):
  v=native['frames'][native['initial'][h]][0];on=[i for i in range(9)if v>>i&1]
  if len(on)==3:return [2 if i in on else -1 for i in range(9)]
  off=[i for i in range(9)if not(v>>i&1)];return [3*(int(i==off[0])-int(i==off[1]))for i in range(9)]
 roots={h:root(h)for h in ports};gram=lambda h,j:F(sum(x*y for x,y in zip(roots[h],roots[j])),18)
 need(all(Q[ii]*P[jj]==-gram(h,j)for ii,h in enumerate(RECEIVERS)for jj,j in enumerate(DONORS)),'exact rank-one sixteen-coefficient source rectangle')
 dirty=a.mode=='dirty_echo';r,s=(400,401) if dirty else (408,409);cache_base=408 if dirty else 410;caches={h:cache_base+i for i,h in enumerate(RECEIVERS)};xroles=[X[j]for j in DONORS];broles=[host[j][0]for j in DONORS];droles={host[h][1]:h for h in RECEIVERS};yroles={Y[h]:h for h in RECEIVERS}
 out=[];marks={};old_boundary_to_new={0:0};changed=[]
 def emit(o):out.append(o)
 def aa(sign):
  for j,p in zip(DONORS,P):
   emit(['ADD',r,X[j],str(sign*p),C]);emit(['ADD',host[j][0],s,str(-sign*p),C])
 def bb(sign):
  for h,q in zip(RECEIVERS,Q):
   emit(['ADD',caches[h],r,str(sign*q),D]);emit(['ADD',s,host[h][1],str(-sign*q),D])
 def move_relays(src,dst):
  emit(['MOVE',r,src,dst,True]);emit(['MOVE',s,src,dst,True])
 def echo():
  marks['echo_begin']=len(out)
  if dirty:
   for owner,line in zip((r,s),seed['duplex']['lines'][:2]):
    need(spaces[line]<spaces[C],'actual dirty reverse-owner access at C')
    emit(['MOVE',owner,line,C,True])
  elif a.mode=='zero_echo':
   emit(['INIT',r,C]);emit(['INIT',s,C])
  else:
   emit(['INIT',r,C]);emit(['INIT',s,D])
  for h in RECEIVERS:emit(['INIT',caches[h],D])
  marks['relay_entry']=len(out)
  if a.mode in ('dirty_echo','zero_echo'):
   aa(1);marks['A_end']=len(out);move_relays(C,D);bb(1);marks['B_end']=len(out)
   move_relays(D,C);aa(-1);marks['A_inverse_end']=len(out);move_relays(C,D);bb(-1);marks['relay_restoration']=len(out)
   if not dirty:emit(['CLEAR',r,D]);emit(['CLEAR',s,D])
  else:
   for j,p in zip(DONORS,P):emit(['ADD',r,X[j],str(p),C])
   marks['A_end']=len(out);emit(['MOVE',r,C,D,True])
   for h,q in zip(RECEIVERS,Q):
    emit(['ADD',caches[h],r,str(q),D]);emit(['ADD',s,host[h][1],str(q),D])
   marks['B_end']=len(out);emit(['MOVE',s,D,C,True])
   for j,p in zip(DONORS,P):emit(['ADD',host[j][0],s,str(-p),C])
   marks['A_inverse_end']=len(out)
   if a.mode in ('zero_roundtrip','zero_output_cleanup'):
    if a.mode=='zero_roundtrip':emit(['MOVE',r,D,C,True])
    if a.mode=='zero_roundtrip':
     for j,p in zip(DONORS,P):emit(['ADD',r,X[j],str(-p),C])
    else:
     # Genuine zero-born output cache is a left-invertible observation of r.
     emit(['ADD',r,caches[RECEIVERS[0]],str(-1/Q[0]),D])
    emit(['MOVE',s,C,D,True])
    for h,q in zip(RECEIVERS,Q):emit(['ADD',s,host[h][1],str(-q),D])
    marks['relay_restoration']=len(out)
    emit(['CLEAR',r,C if a.mode=='zero_roundtrip'else D]);emit(['CLEAR',s,D])
   else:
    marks['relay_retirement']=len(out)
    emit(['CLEAR',r,D]);emit(['CLEAR',s,C])
  marks['echo_end']=len(out)
  for h in RECEIVERS:emit(['MOVE',host[h][1],D,facets[h],False])
  for j in DONORS:
   emit(['MOVE',X[j],C,Hub,False]);emit(['MOVE',host[j][0],C,Hub,False])
  marks['slot_restored']=len(out)
 slotend=seed['duplex']['markers']['XB_slot_end']
 for t,o0 in enumerate(seed['program']):
  if t==slotend:echo()
  o=copy.deepcopy(o0)
  if dirty and o[0]=='MOVE' and o[1]in(r,s) and o[3]==Hub:
   need(t>=slotend,'actual later reverse-owner ascent');o[2]=D
  if o[0]=='MOVE' and o[1] in droles and o[2]==C3 and o[3]==facets[droles[o[1]]]:
   o[3]=D;changed.append({'old_event':t,'kind':'D_wait_at_D'})
  elif o[0]=='MOVE' and o[1]in xroles+broles and o[3]==Hub:
   need(t<slotend,'single original-X/B ascent');o[3]=C;changed.append({'old_event':t,'kind':'X_B_wait_at_C'})
  elif o[0]=='MOVE' and o[1]in yroles and o[2]==C3 and o[3]==facets[yroles[o[1]]]:
   h=yroles[o[1]];emit(['MOVE',o[1],C3,D,False]);emit(['ADD',o[1],caches[h],'1',D]);emit(['CLEAR',caches[h],D]);o[2]=D;changed.append({'old_event':t,'kind':'Y_actual_cache_read'})
  emit(o);old_boundary_to_new[t+1]=len(out)
 need(len(changed)==16,'exact eight donor and eight receiver route replacements')
 word={k:copy.deepcopy(v)for k,v in seed.items()if k not in('duplex','program')};word.update(schema='moonshot-S012-paid-paired-relay-echo-v1',owned_fields=12 if dirty else 14,frames=frames,program=out,echo={'donors':DONORS,'receivers':RECEIVERS,'C':C,'D':D,'C3':C3,'P':clean(P),'Q':clean(Q),'relay_fields':[r,s],'cache_fields':caches,'markers':marks,'seed_event_boundary_to_new':old_boundary_to_new,'changed_original_moves':changed,'seed_word_sha256':SEED_PIN,'native_sha256':NATIVE_PIN,'mode':a.mode,'relay_values_restored':a.mode!='zero_erasure','relay_terminal_chart':{'dirty_echo':'D','zero_echo':'D','zero_roundtrip':'r:C,s:D','zero_erasure':'r:D,s:C','zero_output_cleanup':'r:D,s:D'}[a.mode],'relay_home_return_claimed':a.mode=='zero_roundtrip'})
 parent_rows,parent_locs,parent_bill=e.replay(seed,seed['program']);observed={}
 def capture(t,o,rr,ll):
  if t+1==marks['relay_entry']:
   observed['relay_entry_rows']={r:copy.deepcopy(rr[r]),s:copy.deepcopy(rr[s])}
  if t+1==marks.get('relay_restoration'):
   need(rr[r]==observed['relay_entry_rows'][r] and rr[s]==observed['relay_entry_rows'][s],'actual relay contents restored')
   wanted={r:C,s:D}if a.mode=='zero_roundtrip'else {r:D,s:D}
   need(ll[r]==wanted[r] and ll[s]==wanted[s],'actual restored relay charts')
   observed['relay_contents_restored']=True
   for h,q in zip(RECEIVERS,Q):need(rr[caches[h]]=={X[j]:q*p for j,p in zip(DONORS,P)},'actual acquired rectangular cache row')
  if t+1==marks['slot_restored']:
   need(all(rr[X[j]]=={X[j]:F(1)}for j in DONORS),'all acquisition originals restored')
   need(all(rr[host[h][1]]=={host[h][1]:F(1)}for h in RECEIVERS),'all D sources restored')
   observed['originals_restored']=True
 rows,locs,bill=e.replay(word,out,capture);want=copy.deepcopy(parent_rows)
 for h,q in zip(RECEIVERS,Q):
  for j,p in zip(DONORS,P):
   want[Y[h]]=e.add(want[Y[h]],{X[j]:F(1)},q*p)
   want[host[j][0]]=e.add(want[host[j][0]],{host[h][1]:F(1)},-q*p)
 need(rows==want and locs==parent_locs,'all400 exact coefficients and final source charts')
 need(e.exact_rank(rows.values())==400,'all400 independent original directions retained')
 need(all(rows[host[h][0]].get(host[j][1],F(0))+rows[Y[j]].get(X[h],F(0))==0 for h in host for j in host),'hosted paired transpose invariant')
 raw=Counter();owned=Counter()
 for o in out:
  if o[0]=='MOVE':(owned if o[4]else raw)[abs(len(frames[o[3]])-len(frames[o[2]]))]+=1
 need(dict(raw)=={1:112,2:120,3:104,5:200,8:192},'full actual raw profile')
 expected_owned={'dirty_echo':{1:14,3:2,4:2,8:14},'zero_echo':{1:14,8:16},'zero_roundtrip':{1:12,8:16},'zero_erasure':{1:10,8:16},'zero_output_cleanup':{1:11,8:16}}[a.mode]
 need(dict(owned)==expected_owned,'full actual owned profile')
 need(sum(k*v for k,v in raw.items())==3200,'all original public rank mass')
 forward_debt=sum(len(e.add(rows[Y[h]],{X[h]:F(1)if h in host else F(1,2),Y[h]:F(1)if h in host else F(1,2)},F(-1)))for h in ports)
 reverse_rank=e.exact_rank([e.add(rows[b],{b:F(1),d:F(-1)},F(-1))for h,(b,d)in host.items()])
 prior_complete={('Y',h)for h in ports if parent_rows[Y[h]]=={X[h]:F(1)if h in host else F(1,2),Y[h]:F(1)if h in host else F(1,2)}}|{('B',h)for h,(b,d)in host.items()if parent_rows[b]=={b:F(1),d:F(-1)}}
 now_complete={('Y',h)for h in ports if rows[Y[h]]=={X[h]:F(1)if h in host else F(1,2),Y[h]:F(1)if h in host else F(1,2)}}|{('B',h)for h,(b,d)in host.items()if rows[b]=={b:F(1),d:F(-1)}}
 need(not now_complete-prior_complete,'honest partial-source endpoint status')
 controls=[]
 control_indices={'omit_last_source_feedback':marks['A_inverse_end']-1,'wrong_receiver_pair_sign':marks['B_end']-1}
 if 'relay_restoration'in marks:control_indices['omit_relay_restoration']=marks['relay_restoration']-1
 if a.mode=='zero_output_cleanup':control_indices['omit_forward_output_cleanup']=next(i for i,o in enumerate(out)if o[0]=='ADD'and o[1]==r and o[2]==caches[RECEIVERS[0]])
 for name,idx in control_indices.items():
  bad=copy.deepcopy(word);op=bad['program'][idx]
  need(op[0]=='ADD','negative-control ADD target')
  op[3]='0' if name.startswith('omit')else str(-F(op[3]))
  try:
   rr,ll,bbill=e.replay(bad,bad['program'],capture);rejected=rr!=rows or ll!=locs
  except ValueError:rejected=True
  need(rejected,'negative control '+name);controls.append(name)
 # Restored content does not grant a different owner location.
 bad=copy.deepcopy(word)
 if dirty:
  idx=next(i for i,o in enumerate(bad['program'])if i>=marks['echo_end']and o[0]=='MOVE'and o[1]==r and o[3]==Hub);bad['program'][idx][2]=C
 else:
  idx=next(i for i,o in enumerate(bad['program'])if i>=marks['echo_begin']and o[0]=='CLEAR'and o[1]==r);bad['program'][idx][2]=D if bad['program'][idx][2]==C else C
 try:e.replay(bad,bad['program']);rejected=False
 except ValueError:rejected=True
 need(rejected,'wrong relay terminal/home chart rejected');controls.append('wrong_relay_terminal_chart')
 # Premature D departure is a chronology control, not just coefficient mutation.
 bad=copy.deepcopy(word);idx=next(i for i,o in enumerate(bad['program'])if o[0]=='MOVE'and o[1]==host[RECEIVERS[0]][1]and o[3]==D);bad['program'][idx][3]=facets[RECEIVERS[0]]
 try:e.replay(bad,bad['program']);rejected=False
 except ValueError:rejected=True
 need(rejected,'premature D departure rejected');controls.append('premature_D_departure')
 payload=(json.dumps(clean(word),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0);a.output.mkdir(parents=True,exist_ok=True);(a.output/'WORD.json.gz').write_bytes(blob)
 result={'status':'PASS_ACTUAL_NATIVE_PAIRED_ECHO_RECTANGLE','seed_word_sha256':SEED_PIN,'native_sha256':NATIVE_PIN,'replay_engine_sha256':ENGINE_PIN,'word_sha256':digest(blob),'payload_sha256':digest(payload),'donors':DONORS,'receivers':RECEIVERS,'rank_one_coefficients_removed_each_side':16,'all400_input_rank':400,'all_final_charts_equal_seed':True,'all_original_D_restored':True,'hosted_R_plus_L_transpose_zero':True,'mode':a.mode,'relay_contents_restored':observed.get('relay_contents_restored',False),'relay_initial_rows':clean(observed['relay_entry_rows']),'relay_final_location_contract':word['echo']['relay_terminal_chart'],'relay_home_return_claimed':word['echo']['relay_home_return_claimed'],'source_bill':bill,'raw_histogram':dict(raw),'owned_histogram':dict(owned),'raw_rank_mass':sum(k*v for k,v in raw.items()),'current_a_forward_offdiagonal_coefficients':sum(h!=j and bool(gram(h,j))for h in ports for j in ports)-16,'original_coordinate_forward_debt':forward_debt,'reverse_residual_rank':reverse_rank,'new_complete_public_target_rows':len(now_complete-prior_complete),'negative_controls':controls,'scope':'Actual partial complex source with a paid rectangular rank-one bridge; exact owner-restoration and terminal-chart status stated per mode. Sixteen paired coefficients removed; no new full target endpoint, complete supplier, new kappa or foundational discharge.'};(a.output/'RESULT.json').write_text(json.dumps(clean(result),sort_keys=True,indent=2)+'\n');print(json.dumps(clean(result),indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seed',type=Path,required=True);p.add_argument('--native',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--mode',choices=['dirty_echo','zero_echo','zero_roundtrip','zero_erasure','zero_output_cleanup'],default='dirty_echo');main(p.parse_args())
