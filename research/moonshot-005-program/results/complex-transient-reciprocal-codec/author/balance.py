#!/usr/bin/env python3
"""Restore the exact hosted primal/dual Gram invariant in the stripped source."""
from __future__ import annotations
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
from fractions import Fraction as F
from collections import Counter

def mod(p):
 if hashlib.sha256(p.read_bytes()).hexdigest()!='045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e':raise ValueError('retained exact history replay pin')
 s=importlib.util.spec_from_file_location('balance_exact_engine',p);e=importlib.util.module_from_spec(s);sys.modules[s.name]=e;s.loader.exec_module(e);return e

def balanced(e,q,n):
 ops=q['program'][:q['consumer']['begin']];base,loc,bill=e.replay(q,ops);roles={int(k):v for k,v in q['source_role_map'].items()};H=sorted((n['live'][k],roles[b],roles[d]) for k,b,d in zip(n['hosted']['Dports'],n['hosted']['X2'],n['hosted']['Y2']));B={b for h,b,d in H};Ds={d for h,b,d in H}
 repairs=sum([r['ops'] for r in q['repair_manifest']],[]);e.need(len(repairs)==31 and ops[-31:]==repairs,'exact six one-way forward repair suffix, seven coefficients')
 cut=len(ops)-len(repairs);candidate=ops[:cut];fwd,floc,fbill=e.replay(q,candidate)
 def root(h):
  z=n['frames'][n['initial'][h]][0];ones=[i for i in range(9) if z>>i&1]
  if len(ones)==3:return [2 if i in ones else -1 for i in range(9)]
  zz=[i for i in range(9) if i not in ones];return [3*(int(i==zz[0])-int(i==zz[1])) for i in range(9)]
 roots={h:root(h) for h,b,d in H};G={(h,j):F(sum(x*y for x,y in zip(roots[h],roots[j])),18) for h,b,d in H for j,bj,dj in H}
 # D-only ADDs can be changed independently because no original D is written.
 adj={r:({r:F(1)} if r in B else {}) for r in range(400)};directions={d:[] for d in Ds}
 for t in range(len(candidate)-1,-1,-1):
  o=candidate[t];ty,r=o[:2]
  if ty=='ADD':
   src,c,at=o[2:]
   if src in Ds:
    e.need(r in B,'every old original-D read writes a public B');directions[src].append((t,dict(adj[r])))
   adj[src]=e.add(adj[src],adj[r],F(c))
  elif ty=='SCALE':adj[r]=e.scale(adj[r],F(o[2]))
  elif ty=='CLEAR':adj[r]={}
  elif ty=='INIT':del adj[r]
  elif ty=='MOVE':pass
  else:raise ValueError(ty)
 def solve(columns,target):
  basis={}
  for t,col in columns:
   row=dict(col);rep={t:F(1)}
   for j,(u,c) in basis.items():
    if j in row:
     a=row[j];row=e.add(row,u,-a);rep=e.add(rep,c,-a)
   if row:
    p=min(row);z=row[p];basis[p]=(e.scale(row,1/z),e.scale(rep,1/z))
  row=dict(target);rep={}
  for j,(u,c) in basis.items():
   if j in row:
    a=row[j];row=e.add(row,u,-a);rep=e.add(rep,c,a)
  e.need(not row,'old source D controls span reciprocal-alignment delta');return rep
 changes={};targetmap=copy.deepcopy(fwd);excess=[]
 for j,bj,dj in H:
  delta={}
  for h,b,d in H:
   wanted=G[h,j]-fwd[roles[j+112]].get(roles[h],F(0));z=wanted-fwd[b].get(dj,F(0))
   if z:delta[b]=z;targetmap[b]=e.add(targetmap[b],{dj:F(1)},z);excess.append([h,j,z])
  solution=solve(directions[dj],delta)
  for t,c in solution.items():changes[t]=changes.get(t,F(0))+c
 out=[];lineage=[];edits=[]
 for t,o in enumerate(candidate):
  if t in changes:
   v=copy.deepcopy(o);v[3]=str(F(o[3])+changes[t]);edits.append({'old_event':t,'old_op':o,'new_coefficient':v[3],'delta':str(changes[t])})
   if F(v[3]):out.append(v);lineage.append(t)
  else:out.append(copy.deepcopy(o));lineage.append(t)
 after,al,nbill=e.replay(q,out);e.need(after==targetmap and al==loc,'actual entire400-input reciprocal alignment')
 e.need(len(edits)==72 and all(F(z['new_coefficient'])==0 for z in edits),'exactly72 literal D reads removed; no replacement coefficient introduced')
 for h,b,d in H:
  for j,bj,dj in H:e.need(after[b].get(dj,F(0))+after[roles[j+112]].get(roles[h],F(0))==G[h,j],'complete hosted R+Ltranspose=G identity')
 # Every first-Y current-a expression is authenticated, including coupled inputs.
 for j in n['live']:
  y=roles[j+112];r=e.add(after[y],{y:F(1)},F(-1))
  for h in n['live']:r=e.add(r,after[roles[h]],-after[y].get(roles[h],F(0)))
  e.need(not r,'actual all104 first-Y = original y + L times actual first-X')
 gr=e.exact_rank([{j:G[h,j] for j,bj,dj in H if G[h,j]} for h,b,d in H]);e.need(gr==8,'actual hosted target Gram rank8')
 e.need(e.exact_rank(after.values())==400,'all original information retained')
 def debt(rr):return sum(len(e.add(rr[roles[j+112]],{roles[j]:F(1) if j in {h for h,b,d in H} else F(1,2),roles[j+112]:F(1) if j in {h for h,b,d in H} else F(1,2)},F(-1))) for j in n['live'])
 ranks=[e.exact_rank([e.add(rr[b],{b:F(1),d:F(-1)},F(-1)) for h,b,d in H]) for rr in [base,after]]
 move_delta={r:nbill['moves'].get(r,0)-bill['moves'].get(r,0) for r in set(nbill['moves'])|set(bill['moves'])};move_delta={r:v for r,v in move_delta.items() if v};e.need(move_delta=={1:-6},'only six one-way owned repair MOVEs removed')
 controls=[]
 for label,mutant in [('retain_one_removed_D_read',out+[copy.deepcopy(edits[0]['old_op'])]),('retain_one_forward_repair_packet',out+copy.deepcopy(q['repair_manifest'][0]['ops']))]:
  # The removed D read's old chart need not be its final chart. Reinsert it
  # at the original sequence position, using the preserved event lineage.
  if label=='retain_one_removed_D_read':
   at=next((k for k,t in enumerate(lineage) if t>edits[0]['old_event']),len(out));mutant=out[:at]+[copy.deepcopy(edits[0]['old_op'])]+out[at:]
  mr,ml,mb=e.replay(q,mutant)
  is_gram=all(mr[b].get(dj,F(0))+mr[roles[j+112]].get(roles[h],F(0))==G[h,j] for h,b,d in H for j,bj,dj in H)
  e.need(not is_gram,'reciprocal-alignment mutant '+label);controls.append(label)
 w=copy.deepcopy(q);w['schema']='moonshot-S011-reciprocal-aligned-stripped-source-v1';w['program']=out;w['consumer']={'begin':len(out),'end':len(out),'scope':'No coordinate returns. This marker preserves the standalone builder interface.'};w['parent_event_of_output']=lineage
 receipt={'status':'PASS_ACTUAL_HOSTED_RECIPROCAL_GRAM_INVARIANT','native_sha256':e.NATIVE,'parent_sha256':e.PARENT,'input_directions':400,'hosted_pairs':96,'full_public_map_rank':400,'all104_current_a_forward_identity':True,'hosted_R_plus_L_transpose_equals_Gram':True,'invariant_Gram_rank':gr,'forward_debt_before':debt(base),'forward_debt_after':debt(after),'reverse_rank_before':ranks[0],'reverse_rank_after':ranks[1],'removed_one_way_forward_repairs':q['repair_manifest'],'old_D_ADD_edits':edits,'old_unpaired_reverse_excess':excess,'changed_reverse_coefficients':len(excess),'source_bill':nbill,'parent_source_bill':bill,'move_delta':move_delta,'negative_controls':controls,'scope':'Reciprocity-aligned alternative baseline, not a better complete kappa. Six one-way forward repair packets, containing seven current-controller coefficients, and old reverse-only cyclic excess are deliberately reopened to obtain the exact composable invariant. Forward debt, coupled exceptions, physical compilation and a priced actual reverse-code supplier remain open.'}
 return w,after,al,nbill,receipt

def clean(z):
 if isinstance(z,F):return str(z)
 if isinstance(z,dict):return {str(k):clean(v) for k,v in z.items()}
 if isinstance(z,(list,tuple)):return [clean(v) for v in z]
 return z
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();e=mod(a.engine);q=e.load(a.parent,e.PARENT);n=e.load(a.native,e.NATIVE);w,r,l,b,res=balanced(e,q,n)
 payload=(json.dumps(clean(w),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0);res['word_sha256']=hashlib.sha256(blob).hexdigest();res['payload_sha256']=hashlib.sha256(payload).hexdigest();res['producer_engine_sha256']=hashlib.sha256(a.engine.read_bytes()).hexdigest();a.output.mkdir(parents=True,exist_ok=True);(a.output/'WORD.json.gz').write_bytes(blob);(a.output/'RESULT.json').write_text(json.dumps(clean(res),sort_keys=True,indent=2)+'\n');print(json.dumps({k:res[k] for k in ['status','word_sha256','forward_debt_after','reverse_rank_after','changed_reverse_coefficients','source_bill','move_delta']},indent=2))
