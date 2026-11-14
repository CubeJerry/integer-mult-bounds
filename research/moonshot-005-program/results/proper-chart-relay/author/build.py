#!/usr/bin/env python3
"""Literal dyadic preload and proper-chart dirty relay for 20 or 44 original D rows."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,copy,gzip,hashlib,json
import seed as s
need=s.need;clean=s.clean;root=s.root;basis=s.basis
CYCLES={44:[4,20,37,111,50,103,18,53,58,110,51,78,48,28,63,62,5,59,46,79,86,85,87,88,36,33,77,29,49,32,92,98,13,99,15,68,94,69,9,81,80,10,11,67],20:[4,78,28,110,58,99,81,63,88,37,80,9,11,68,49,87,98,33,92,85]}
COMPLEMENT={44:[0,91,27,2,71,89,90,70,72,25,101,96,83,6,73,75,1,74,31,26,44,95,100,22,23,45,97,24,102,84,7,82,8,66,64,65,104,105,106,42,43,41,107,12,108,109,56,16,57,54,35,55],20:[0,5,15,67,48,51,111,53,50,69,13,32,18,103,72,59,70,27,89,36,104,106,91,55,71,29,74,23,65,107,95,100,82,2,109,84,97,42,8,10,77,6,12,102,45,86,41,43,7,79,57,44,94,25,16,20,62,46,56,66,1,83,75,31,26,73,54,64,35,22,96,101,24,105,108,90]}
def coordinates(rows,target):
 n=len(rows);A=[[F(rows[j][i]) for j in range(n)]+[F(target[i])] for i in range(len(target))];r=0
 for c in range(n):
  k=next((k for k in range(r,len(A)) if A[k][c]),None);need(k is not None,'independent real mode basis');A[r],A[k]=A[k],A[r];a=A[r][c];A[r]=[x/a for x in A[r]]
  for k in range(len(A)):
   if k!=r and A[k][c]:
    a=A[k][c];A[k]=[x-a*y for x,y in zip(A[k],A[r])]
  r+=1
 need(all(not any(row[:-1]) and row[-1]==0 for row in A[r:]),'root lies in real mode span');return [A[k][-1] for k in range(n)]
def determinant(A):
 A=[row[:] for row in A];value=F(1)
 for i in range(len(A)):
  k=next((k for k in range(i,len(A)) if A[k][i]),None)
  if k is None:return F(0)
  if k!=i:A[k],A[i]=A[i],A[k];value=-value
  pivot=A[i][i];value*=pivot;A[i]=[x/pivot for x in A[i]]
  for j in range(i+1,len(A)):
   c=A[j][i];A[j]=[x-c*y for x,y in zip(A[j],A[i])]
 return value
def main(a):
 e=s.loadmod(a.engine);n=e.load(a.native,e.NATIVE);q=e.load(a.parent,e.PARENT);role={int(k):v for k,v in q['source_role_map'].items()};P=list(n['live']);host={P[k]:(role[b],role[d]) for k,b,d in zip(n['hosted']['Dports'],n['hosted']['X2'],n['hosted']['Y2'])};H=list(host);U=sorted(set(P)-set(H));X={h:role[h] for h in P};Y={h:role[h+112] for h in P};v={h:n['frames'][n['initial'][h]][0] for h in P};roots={h:root(v[h]) for h in P};fr=[root(z) for z in s.FRAME];g={h:[sum(x*y for x,y in zip(r,roots[h]))/18 for r in fr] for h in P};G={(h,j):sum(g[h][i]*g[j][i] for i in range(8)) for h in P for j in P};need(all(G[h,j]==sum(x*y for x,y in zip(roots[h],roots[j]))/18 for h in P for j in P),'Gram factorization');T=CYCLES[a.size];other=COMPLEMENT[a.size];need(sorted(T+other)==sorted(H),'cycles partition96');need(all((v[cy[i]]&v[cy[(i+1)%len(cy)]]).bit_count()%2==0 for cy in (T,other) for i in range(len(cy))),'all cycle edges actual line/facet contacts');perm={cy[i]:cy[(i+1)%len(cy)] for cy in (T,other) for i in range(len(cy))};ip={p:h for h,p in perm.items()};modes=[u for u in U if u!=17];beta={h:coordinates([roots[u] for u in modes],roots[h]) for h in T};need(all(x.denominator&(x.denominator-1)==0 for row in beta.values() for x in row),'dyadic coefficients')
 frames=copy.deepcopy(q['frames']);where={frozenset(e.span(f)):i for i,f in enumerate(frames)}
 def chart(vs):
  b=basis(vs);S=frozenset(e.span(b))
  if S not in where:where[S]=len(frames);frames.append(b)
  return where[S]
 O=chart([]);Hub=chart([1<<i for i in range(9)]);facets={h:chart(x for x in range(512) if not (x&v[h]).bit_count()%2) for h in P};lines={h:chart([v[h]]) for h in P};C=chart((x for x in range(512) if not (x&63).bit_count()%2) if a.size==44 else [v[u] for u in U]);need(len(frames[C])==(8 if a.size==44 else 7),'bank dimension');CS=e.span(frames[C]);need(all(v[h] in CS for h in T),'target lines in bank');stops={h:chart(x for x in CS if not (x&v[h]).bit_count()%2) for h in T};need(all(len(frames[stops[h]])==len(frames[C])-1 and e.span(frames[lines[perm[h]]])<e.span(frames[stops[h]])<e.span(frames[facets[h]]) for h in T),'proper monotone routes');need(all(C!=facets[h] for h in H) and all(stops[h]!=facets[j] for h in T for j in H),'no bank/stop equals final hosted facet');need(a.size!=44 or sorted(T)==sorted(h for h in H if sum(x*y for x,y in zip(roots[h],root(448)))==0),'actual44 E7 set')
 local_g_ranks={h:e.exact_rank([{i:x for i,x in enumerate(g[j]) if x} for j in H if j!=h and v[j] not in e.span(frames[stops[h]])]) for h in T};need(all(r==8 for r in local_g_ranks.values()),'no local-initial-record proper-stop decoder');det8=determinant([[F(i==j)-sum(g[h][i]*g[h][j] for h in other) for j in range(8)] for i in range(8)]);need(det8==(480000 if a.size==44 else 24387048),'exact residual D determinant');out=[];marks={};events={};captures={}
 def emit(o):out.append(o)
 def swap(i,j,c):
  emit(['ADD',i,j,'1',c]);emit(['ADD',j,i,'-1',c]);emit(['ADD',i,j,'1',c]);emit(['SCALE',j,'-1',c])
 for h in U:
  emit(['INIT',400,O]);emit(['ADD',400,Y[h],'1',O]);emit(['MOVE',400,O,lines[h],True]);emit(['ADD',X[h],400,'-1',lines[h]]);emit(['CLEAR',400,lines[h]])
 marks['entry_end']=len(out)
 for i in range(8):
  emit(['INIT',400+i,O])
  for h,(b,d) in host.items():
   if g[h][i]:emit(['ADD',400+i,d,str(g[h][i]),O])
 for h,(b,d) in host.items():
  emit(['SCALE',d,'-1',O])
  for i in range(8):
   if g[h][i]:emit(['ADD',d,400+i,str(g[h][i]),O])
 for k,u in enumerate(modes):
  emit(['INIT',408+k,O])
  for i in range(8):
   if g[u][i]:emit(['ADD',408+k,400+i,str(g[u][i]),O])
 marks['ground_preload']=len(out)
 for i in range(8):emit(['CLEAR',400+i,O])
 for cy in (T,other):
  for h,j in zip(cy,cy[1:]):swap(host[h][1],host[j][1],O)
 marks['permuted_preload']=len(out)
 for h,(b,d) in host.items():
  p=perm[h];emit(['MOVE',d,O,lines[p],False]);emit(['ADD',host[p][0],d,'1',lines[p]])
 for h,(b,d) in host.items():emit(['MOVE',b,lines[h],Hub,False])
 marks['all_B_reads']=len(out)
 for k,u in enumerate(modes):emit(['MOVE',408+k,O,C,True])
 emit(['INIT',400,lines[T[0]]]);emit(['ADD',400,host[ip[T[0]]][1],'1',lines[T[0]]]);emit(['MOVE',400,lines[T[0]],C,True]);marks['relay_start']=len(out)
 for k,h in enumerate(T):
  d=host[h][1];emit(['SCALE',400,'-1',C])
  for j,c in enumerate(beta[h]):
   if c:emit(['ADD',400,408+j,str(c),C])
  events.setdefault('decoded_owner',[]).append({'port':h,'step':len(out)});stop=stops[h];emit(['MOVE',d,lines[perm[h]],stop,False]);emit(['MOVE',400,C,stop,True]);events.setdefault('first_swap',[]).append(len(out));swap(d,400,stop);events.setdefault('restored_public',[]).append({'port':h,'step':len(out),'next_payload':perm[h]});emit(['MOVE',d,stop,facets[h],False])
  if k+1<len(T):emit(['MOVE',400,stop,C,True])
 emit(['CLEAR',400,stops[T[-1]]])
 for k,u in enumerate(modes):emit(['CLEAR',408+k,C])
 marks['relay_end']=len(out)
 for h in other:emit(['MOVE',host[h][1],lines[perm[h]],facets[h],False])
 for h in P:emit(['MOVE',X[h],lines[h],Hub,False]);emit(['MOVE',Y[h],O,facets[h],False])
 w={'schema':'moonshot-S011-dyadic-preload-proper-chart-relay-v1','public':400,'owned_fields':15,'initial':q['initial'],'frames':frames,'source_role_map':q['source_role_map'],'program':out,'source_pins':{'native':e.NATIVE,'interface_parent':e.PARENT},'relay':{'restored_ports':T,'unrestored_ports':other,'permutation':perm,'bank':C,'bank_frame':frames[C],'stops':stops,'mode_ports':modes,'beta':clean(beta),'preload':'r_h=-d_h+G_hH*d; r_u=G_uH*d','ground_Gram_frame':s.FRAME,'markers':marks,'events':events,'old_seed_or_parity_progress_retained':False}}
 bounds=set(marks.values())|{z['step'] for name in ('decoded_owner','restored_public') for z in events[name]}
 previous_owned={};dirty_retirements=[]
 def capture(t,o,rr,ll):
  nonlocal previous_owned
  if o and o[0]=='CLEAR':
   need(bool(previous_owned.get(o[1])),'each recorded retirement is truly dirty');dirty_retirements.append({'step':t,'field':o[1],'chart':o[2]})
  previous_owned={j:row for j,row in rr.items() if j>=400}
  if t+1 in bounds:captures[t+1]=copy.deepcopy(rr)
 rr,ll,bill=e.replay(w,out,capture);want={j:{j:F(1)} for j in range(400)};wantloc={};rp={p:e.add({host[p][1]:F(-1)},{d:G[p,j] for j,(b,d) in host.items() if G[p,j]},F(1)) for p in H}
 for h in P:
  wantloc[X[h]]=Hub;wantloc[Y[h]]=facets[h]
  if h in U:want[X[h]][Y[h]]=F(-1)
 for h,(b,d) in host.items():
  wantloc[b]=Hub;wantloc[d]=facets[h];want[b]=e.add({b:F(1)},rp[h],F(1));want[d]={d:F(1)} if h in T else rp[perm[h]]
 need(rr==want and ll==wantloc,'all400 exact endpoint rows/locations');forward_debt=sum(len(e.add(rr[Y[h]],{X[h]:F(1) if h in host else F(1,2),Y[h]:F(1) if h in host else F(1,2)},F(-1))) for h in P);need(forward_debt==112,'exact unfinished forward endpoint debt');_,native_final,_=e.replay(q,q['program'][:q['consumer']['begin']]);need(ll==native_final,'all400 exact retained final chart identifiers');need(e.exact_rank(rr.values())==400,'all400 input directions survive dirty retirement');need(e.exact_rank([e.add(rr[b],{b:F(1),d:F(-1)},F(-1)) for h,(b,d) in host.items()])==8,'reverse residual8');need(all(captures[z['step']][400]=={host[z['port']][1]:F(1)} for z in events['decoded_owner']),'actual active owner original d_h before import');need(all(captures[z['step']][host[z['port']][1]]=={host[z['port']][1]:F(1)} and captures[z['step']][400]==rp[z['next_payload']] for z in events['restored_public']),'each swap restores D and keeps next payload')
 raw=Counter();owned=Counter();public_down=[];owner_facets=[]
 for k,o in enumerate(out):
  if o[0]=='MOVE':
   dr=len(frames[o[3]])-len(frames[o[2]]);(owned if o[4] else raw)[abs(dr)]+=1
   if not o[4] and dr<0:public_down.append(k)
   if o[4] and o[3] in set(facets[h] for h in H):owner_facets.append(k)
 need(not public_down and not owner_facets,'public monotonicity and zero owned final-facet visits');need(sum(k*v for k,v in raw.items())==3200,'public rankmass3200');need(sum(rr[d]=={d:F(1)} for b,d in host.values())==a.size,'exact D restoration count');scalars=[F(o[3] if o[0]=='ADD' else o[2]) for o in out if o[0] in ('ADD','SCALE')];need(all(x.denominator&(x.denominator-1)==0 for x in scalars),'dyadic scalars')
 controls=[];choices=[('wrong_active_sign',marks['relay_start']),('wrong_swap_sign',events['first_swap'][0]+1),('omit_first_B_read',marks['permuted_preload']+1),('omit_coupled_entry',3),('wrong_mode_preload',next(k for k,o in enumerate(out) if o[0]=='ADD' and o[1]==408))]
 for label,k in choices:
  bad=copy.deepcopy(w);o=bad['program'][k]
  if o[0]=='ADD':o[3]='0' if 'omit' in label else str(-F(o[3]))
  else:o[2]='1'
  try:br,bl,_=e.replay(bad,bad['program']);rejected=br!=rr or bl!=ll
  except ValueError:rejected=True
  need(rejected,'semantic control '+label);controls.append(label)
 payload=(json.dumps(clean(w),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0);a.output.mkdir(parents=True,exist_ok=True);(a.output/'WORD.json.gz').write_bytes(blob);receipt={'status':'PASS_LITERAL_PROPER_CHART_DIRTY_RELAY','size':a.size,'native_sha256':e.NATIVE,'interface_parent_sha256':e.PARENT,'producer_replay_sha256':s.REPLAY,'seed_helper_sha256':hashlib.sha256(Path(s.__file__).read_bytes()).hexdigest(),'word_sha256':hashlib.sha256(blob).hexdigest(),'payload_sha256':hashlib.sha256(payload).hexdigest(),'all400_input_rank':400,'all400_final_chart_ids_match_retained_interface':True,'all_actual_scalars_dyadic':True,'public_downward_moves':public_down,'owned_hosted_facet_visits':owner_facets,'original_D_restored':a.size,'D_unrestored':96-a.size,'reverse_residual_rank':8,'forward_endpoint_debt':112,'all_forward_corrections_unfinished':True,'paired_forward_required':'I-G on hosted block; unchanged Y is not paired','coupled_current_a_entry_retained':True,'ground_preload_was_actually_acquired':True,'dirty_retirements':dirty_retirements,'local_initial_record_decoder_exclusion_ranks':local_g_ranks,'remaining_D_small_determinant':str(det8),'mode_bank_dimension':len(frames[C]),'restoration_chart_dimension':len(frames[C])-1,'source_bill':bill,'raw_histogram':dict(raw),'owned_histogram':dict(owned),'semantic_negative_controls':controls,'exact_scope':'New dyadic preload, actual partial400 source,20 or44 original D restored at proper charts by nonlocal dirty import. Remaining D and all forward obligations open. No supplier/kappa; no old source progress retained.'};(a.output/'RESULT.json').write_text(json.dumps(clean(receipt),sort_keys=True,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--size',type=int,choices=[20,44],required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
