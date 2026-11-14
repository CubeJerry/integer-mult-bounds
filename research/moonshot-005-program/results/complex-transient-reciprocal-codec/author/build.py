#!/usr/bin/env python3
"""Literal receiver-side reciprocal codec with restored original D fields."""
from __future__ import annotations
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from fractions import Fraction as F
from pathlib import Path
from collections import Counter

def module(p):
 s=importlib.util.spec_from_file_location('transient_exact_engine',p);e=importlib.util.module_from_spec(s);sys.modules[s.name]=e;s.loader.exec_module(e);return e
def inv(o):
 ty,i,j,c=o
 return (ty,i,j,-c if ty=='ADD' else 1/c)
def dual(o):
 ty,i,j,c=o
 return ('ADD',j,i,-c) if ty=='ADD' else ('SCALE',i,i,1/c)
def gauss_ops(M):
 n=len(M);A=copy.deepcopy(M);ops=[]
 def emit(o):
  ty,i,j,c=o;ops.append(o)
  if ty=='ADD':A[i]=[x+c*y for x,y in zip(A[i],A[j])]
  else:A[i]=[c*x for x in A[i]]
 for j in range(n):
  k=next(i for i in range(j,n) if A[i][j])
  if k!=j:
   emit(('ADD',j,k,F(1)));emit(('ADD',k,j,F(-1)));emit(('ADD',j,k,F(1)));emit(('SCALE',k,k,F(-1)))
  if A[j][j]!=1:emit(('SCALE',j,j,1/A[j][j]))
  for i in range(n):
   if i!=j and A[i][j]:emit(('ADD',i,j,-A[i][j]))
 if A!=[[F(i==j) for j in range(n)] for i in range(n)]:raise ValueError('exact M elimination')
 return [inv(o) for o in reversed(ops)]
def clean(z):
 if isinstance(z,F):return str(z)
 if isinstance(z,dict):return {str(k):clean(v) for k,v in z.items()}
 if isinstance(z,(list,tuple)):return [clean(v) for v in z]
 return z

def main(a):
 if hashlib.sha256(a.engine.read_bytes()).hexdigest()!='045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e':raise ValueError('retained exact history replay pin')
 e=module(a.engine);q=e.load(a.parent,e.PARENT);native=e.load(a.native,e.NATIVE);baseline_pin=e.PARENT;balance_receipt=None
 if a.balanced_module:
  sp=importlib.util.spec_from_file_location('reciprocal_alignment_module',a.balanced_module);ba=importlib.util.module_from_spec(sp);sys.modules[sp.name]=ba;sp.loader.exec_module(ba);q,_,_,_,balance_receipt=ba.balanced(e,q,native);baseline_pin=hashlib.sha256(gzip.compress((json.dumps(clean(q),sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0)).hexdigest()
 old=q['program'][:q['consumer']['begin']];base,base_loc,base_bill=e.replay(q,old)
 roles={int(k):v for k,v in q['source_role_map'].items()};host={native['live'][k]:(roles[b],roles[d]) for k,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2'])}
 I=[0,6];J=[12,13,15,25,68,70,71,72,73,74,75,80,81,82,83,84,85,98,99,101]
 Cframe=[13,6];Cspace=e.span(Cframe);frames=copy.deepcopy(q['frames']);C=next((i for i,f in enumerate(frames) if e.span(f)==Cspace),None)
 if C is None:C=len(frames);frames.append(Cframe)
 Cframe=frames[C];dim=len(Cframe);e.need(dim==2,'selected common plane')
 Bs=[host[i][0] for i in I];Xs=[roles[i] for i in I];Ys=[roles[j+112] for j in J];Ds=[host[j][1] for j in J];facets=[base_loc[d] for d in Ds]
 e.need(all(e.span(frames[q['initial'][b]])<Cspace for b in Bs),'two actual receiver initial lines below C')
 e.need(all(Cspace<e.span(frames[f]) and len(frames[f])==8 for f in facets),'C below every true original endpoint facet')
 old_Y_moves={};old_D_moves={}
 for j,y,d,f in zip(J,Ys,Ds,facets):
  dt=[(t,o) for t,o in enumerate(old) if o[1]==d or o[0]=='ADD' and o[2]==d]
  yt=[(t,o) for t,o in enumerate(old) if o[1]==y or o[0]=='ADD' and o[2]==y]
  ym=[(t,o) for t,o in yt if o[0]=='MOVE']
  e.need(len(dt)==len(ym)==1 and dt[0][1]==['MOVE',d,3,f,False] and ym[0][1]==['MOVE',y,3,f,False],'selected actual direct source routes')
  e.need(all(o[0]=='MOVE' or o[0]=='ADD' and o[1]==y and o[4]==3 for t,o in yt),'selected Y has no old input or facet use')
  old_Y_moves[ym[0][0]]=y;old_D_moves[dt[0][0]]=d
 # Derive the actual missing forward columns, instead of presuming a Gram formula.
 A=[[-base[y].get(x,F(0)) for y in Ys] for x in Xs]
 e.need(all(v in (F(1,2),F(-1,2)) for row in A for v in row),'forty actual unwanted half coefficients')
 _,piv=e.select([[int(v.numerator)*pow(v.denominator,-1,e.PRIME)%e.PRIME for v in row] for row in A]);e.need(len(piv)==2,'rank-two requested paired patch')
 n=len(J);M=[[F(i==j) for j in range(n)] for i in range(n)]
 for row,p in zip(A,piv):M[p]=list(row)
 enc=gauss_ops(M);dec=[inv(o) for o in reversed(enc)];dual_enc=[dual(o) for o in enc];dual_dec=[inv(o) for o in reversed(dual_enc)]
 # Literal lifetime-colour separation, independently regenerated from the source.
 uf=list(range(400));cur={i:i for i in range(400)};nodes=[]
 def find(x):
  while uf[x]!=x:uf[x]=uf[uf[x]];x=uf[x]
  return x
 def union(x,y):
  x,y=find(x),find(y)
  if x!=y:uf[y]=x
 for o in old:
  ty,r=o[:2]
  if ty=='INIT':cur[r]=len(uf);uf.append(len(uf))
  nodes.append(cur[r])
  if ty=='ADD':union(cur[r],cur[o[2]])
  if ty=='CLEAR':del cur[r]
 colours={}
 for i in range(400):colours.setdefault(find(i),set()).add('D' if i>=208 else 'P')
 e.need(all(len(z)==1 for z in colours.values()),'whole-lifetime primal/dual separation')
 def colour(n):return next(iter(colours.get(find(n),{'P'})))
 P=[(t,o) for t,o in enumerate(old) if colour(nodes[t])=='P'];D=[(t,o) for t,o in enumerate(old) if colour(nodes[t])=='D']
 downs=[t for t,o in P if o==['MOVE',451,127,3,True]];e.need(len(downs)==8,'all eight old forward packets retained')
 last_clear=next(t for t,o in P if t>downs[-1] and o==['CLEAR',451,3]);e.need(all(t>last_clear for t in old_Y_moves),'all selected Y still at ground after all packets')
 out=[];lineage=[];markers={};cache=[400+q['owned_fields']+k for k in range(len(I))]
 def emit(o,old_t=None):out.append(o);lineage.append(old_t)
 def bank_ops(bank,ops,chart):
  for ty,i,j,c in ops:
   emit(['ADD',bank[i],bank[j],str(c),chart] if ty=='ADD' else ['SCALE',bank[i],str(c),chart])
 for c,x,b in zip(cache,Xs,Bs):
  line=q['initial'][b];e.need(q['initial'][x]==line,'actual paired X/B initial cochart');emit(['INIT',c,line]);emit(['ADD',c,x,'1',line])
 def gadget():
  markers['gadget_begin']=len(out);bank_ops(Ds,enc,3);bank_ops(Ys,dual_enc,3);markers['ground_encoding_end']=len(out)
  branches={p:k for k,p in enumerate(piv)}
  for j,(y,d) in enumerate(zip(Ys,Ds)):
   if j in branches:
    k=branches[j];line=q['initial'][Bs[k]]
    emit(['MOVE',y,3,line,False]);emit(['MOVE',d,3,line,False]);markers['branch_'+str(k)+'_before_read']=len(out)
    emit(['ADD',y,cache[k],'1',line]);emit(['ADD',Bs[k],d,'-1',line]);emit(['CLEAR',cache[k],line])
    emit(['MOVE',y,line,C,False]);emit(['MOVE',d,line,C,False])
   else:
    emit(['MOVE',y,3,C,False]);emit(['MOVE',d,3,C,False])
  markers['all_at_common_plane']=len(out);bank_ops(Ds,dec,C);bank_ops(Ys,dual_dec,C);markers['common_decode_end']=len(out)
  for y,d,f in zip(Ys,Ds,facets):emit(['MOVE',y,C,f,False]);emit(['MOVE',d,C,f,False])
  markers['gadget_end']=len(out)
 for t,o in P:
  if t not in old_Y_moves:emit(copy.deepcopy(o),t)
  if t==last_clear:gadget()
 for t,o in D:
  if t not in old_D_moves:emit(copy.deepcopy(o),t)
 w=copy.deepcopy(q);w['schema']='moonshot-S011-receiver-side-transient-paired-D-codec-v1';w['frames']=frames;w['owned_fields']=q['owned_fields']+len(cache);w['program']=out;w.pop('consumer',None);w.pop('parent_event_of_output',None);w['baseline_event_of_output']=lineage
 w['transient_codec']={'native_sha256':e.NATIVE,'parent_sha256':e.PARENT,'actual_baseline_sha256':baseline_pin,'reciprocal_aligned_baseline':bool(a.balanced_module),'parent_31_returns_stripped':True,'I_ports':I,'J_ports':J,'X_roles':Xs,'B_roles':Bs,'Y_roles':Ys,'D_roles':Ds,'C':C,'C_frame':Cframe,'encoder_M':clean(M),'desired_A':clean(A),'pivot_positions':piv,'D_encoder_elementary_ops':clean(enc),'X_stationary_caches':cache,'markers':markers,'replaced_Y_MOVE_events':sorted(old_Y_moves),'replaced_D_MOVE_events':sorted(old_D_moves)}
 captures={}
 def capture(t,o,rows,loc):
  if t+1 in (markers['ground_encoding_end'],markers['common_decode_end']):captures[t+1]={r:dict(rows[r]) for r in Ds+Ys}
 new,floc,bill=e.replay(w,out,capture)
 want=copy.deepcopy(base)
 for k,b in enumerate(Bs):
  for j,d in enumerate(Ds):want[b]=e.add(want[b],{d:F(1)},-A[k][j])
 for j,y in enumerate(Ys):
  for k,x in enumerate(Xs):want[y]=e.add(want[y],{x:F(1)},A[k][j])
 e.need(new==want and floc==base_loc,'exact entire400-input paired patch and all endpoint charts')
 e.need(all(captures[markers['common_decode_end']][d]=={d:F(1)} for d in Ds),'all original D restored at the common predecessor before final facets')
 e.need(any(captures[markers['ground_encoding_end']][d]!={d:F(1)} for d in Ds),'genuine temporary D recoding')
 e.need(e.exact_rank(new.values())==400,'all original independent input directions retained')
 def debt(rr):
  return sum(len(e.add(rr[roles[h+112]],{roles[h]:F(1) if h in host else F(1,2),roles[h+112]:F(1) if h in host else F(1,2)},F(-1))) for h in native['live'])
 before_debt=4928 if a.balanced_module else 4920;e.need(debt(base)==before_debt and debt(new)==before_debt-40,'exact forty original forward coefficients removed')
 for h,(b,d) in host.items():
  for j,(bj,dj) in host.items():e.need(new[b].get(dj,F(0))+new[roles[j+112]].get(roles[h],F(0))==base[b].get(dj,F(0))+base[roles[j+112]].get(roles[h],F(0)),'all9216 hosted reciprocal invariant entries unchanged')
 E0=[e.add(base[b],{b:F(1),d:F(-1)},F(-1)) for b,d in host.values()];E1=[e.add(new[b],{b:F(1),d:F(-1)},F(-1)) for b,d in host.values()]
 ranks=[e.exact_rank(z) for z in [E0,E1]]
 delta={r:bill['moves'].get(r,0)-base_bill['moves'].get(r,0) for r in set(bill['moves'])|set(base_bill['moves'])};delta={r:v for r,v in delta.items() if v};e.need(delta=={1:8,2:36,6:40,8:-40},'complete two-bank source movement invoice')
 e.need(all(o[0]!='MOVE' or not o[4] for o,old_t in zip(out,lineage) if old_t is None),'no added owned transport')
 controls=[]
 for control in ['omit_D_uncompute','omit_Y_transpose_uncompute','wrong_reverse_sign','forget_actual_X_cache','wrong_branch_chart']:
  bad=copy.deepcopy(w)
  if control=='omit_D_uncompute':
   o=bad['program'][markers['all_at_common_plane']];o[3 if o[0]=='ADD' else 2]='0' if o[0]=='ADD' else '1'
  elif control=='omit_Y_transpose_uncompute':
   ix=markers['all_at_common_plane']+len(dec);o=bad['program'][ix];o[3 if o[0]=='ADD' else 2]='0' if o[0]=='ADD' else '1'
  elif control=='wrong_reverse_sign':bad['program'][markers['branch_0_before_read']+1][3]='1'
  elif control=='forget_actual_X_cache':bad['program'][1][3]='0'
  else:bad['program'][markers['branch_0_before_read']][4]=C
  rejected=False
  try:rr,ll,bb=e.replay(bad,bad['program']);rejected=rr!=new or ll!=floc
  except ValueError:rejected=True
  e.need(rejected,'meaningful transient-codec mutant '+control);controls.append(control)
 payload=(json.dumps(clean(w),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0);a.output.mkdir(parents=True,exist_ok=True);(a.output/'WORD.json.gz').write_bytes(blob)
 receipt={'status':'PASS_ACTUAL_TRANSIENT_PAIRED_CODEWORD_40_FORWARD_AND40_REVERSE_TERMS','native_sha256':e.NATIVE,'parent_sha256':e.PARENT,'producer_engine_sha256':hashlib.sha256(a.engine.read_bytes()).hexdigest(),'word_sha256':hashlib.sha256(blob).hexdigest(),'payload_sha256':hashlib.sha256(payload).hexdigest(),'input_directions':400,'full_public_map_rank':400,'actual_baseline_sha256':baseline_pin,'reciprocal_aligned_baseline':bool(a.balanced_module),'forward_debt_before':debt(base),'forward_debt_after':debt(new),'all_hosted_reciprocal_invariant_entries_preserved':True,'hosted_R_plus_L_transpose_equals_Gram':bool(a.balanced_module),'paired_reverse_added_coefficients':40,'reverse_rank_before':ranks[0],'reverse_rank_after':ranks[1],'all_original_D_exactly_restored_before_final_departures':True,'all_firstX_exact_parent':True,'every_other_public_row_exact_parent':True,'completed_forward_ports_before':[h for h in native['live'] if not e.add(base[roles[h+112]],{roles[h]:F(1) if h in host else F(1,2),roles[h+112]:F(1) if h in host else F(1,2)},F(-1))],'completed_forward_ports_after':[h for h in native['live'] if not e.add(new[roles[h+112]],{roles[h]:F(1) if h in host else F(1,2),roles[h+112]:F(1) if h in host else F(1,2)},F(-1))],'source_bill':bill,'parent_source_bill':base_bill,'move_delta':delta,'added_owned_moves':0,'ordinary_delta':{k:bill['counts'].get(k,0)-base_bill['counts'].get(k,0) for k in set(bill['counts'])|set(base_bill['counts'])},'codec':w['transient_codec'],'negative_controls':controls,'scope':'Actual paired local-source codec, with all original D restored and no new owned transport; forty forward debt coefficients removed and matching transpose B update. Global compatible composition, complete forward/reverse endpoints, uniform supplier and kappa target remain unresolved.'}
 (a.output/'RESULT.json').write_text(json.dumps(clean(receipt),sort_keys=True,indent=2)+'\n');print(json.dumps({k:receipt[k] for k in ['status','word_sha256','forward_debt_after','reverse_rank_after','source_bill','move_delta','ordinary_delta']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--balanced-module',type=Path);main(p.parse_args())
