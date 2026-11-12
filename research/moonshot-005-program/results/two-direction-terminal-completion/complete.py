#!/usr/bin/env python3
"""Exact416-field terminal completion. Reuses disclosed S008 interpreter."""
import argparse,gzip,hashlib,importlib.util,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
def need(b,m):
 if not b:raise ValueError(m)
def load(p):
 need(hashlib.sha256(p.read_bytes()).hexdigest()=='fa5d7f3c84a4dcd9aee70240dc8592865ea8baaaf02f3d3a4a3228d0e331bd21','S008 interpreter pin')
 s=importlib.util.spec_from_file_location('endpoint_reconstruction',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def rank(rows):
 piv={}
 for original in rows:
  row=original.copy()
  while row:
   j=min(row)
   if j not in piv:
    c=row[j];piv[j]={k:v/c for k,v in row.items()};break
   c=row[j]
   for k,v in piv[j].items():
    z=row.get(k,Q(0))-c*v
    if z:row[k]=z
    else:row.pop(k,None)
 return len(piv)
def original_Y(e,w):
 xs,fy,rx,ry,xa,ya,mains,U,roots,P=e.sets(w);H=sorted(set(range(104))-set(U))
 P0=[[P[i][j] for j in U] for i in U]
 S=[[Q(i==j)+sum(P0[i][k]*P0[k][j] for k in range(8)) for j in range(8)] for i in range(8)]
 inv,det=e.inverse(S);A=[];B=[]
 for i in U:
  ar={xs[i]:Q(1)};br={fy[i]:Q(2)}
  for j in H:
   if P[i][j]:e.addto(ar,{ry[j]:Q(1)},P[i][j]);e.addto(br,{xs[j]:Q(1)},-P[i][j])
  A.append(ar);B.append(br)
 rhs=[]
 for i in range(8):
  r=B[i].copy()
  for j in range(8):
   if P0[i][j]:e.addto(r,A[j],-P0[i][j])
  rhs.append(r)
 out={}
 for i,port in enumerate(U):
  r={}
  for j in range(8):
   if inv[i][j]:e.addto(r,rhs[j],inv[i][j])
  out[port]=r
 return out,det
def build(e,w,private):
 xs,fy,rx,ry,xa,ya,mains,U,roots,P=e.sets(w);Y,det=original_Y(e,w);ops=[];marks=[];banks=[]
 def emit(op,purpose):marks.append({'event':len(ops),'purpose':purpose});ops.append(op)
 for bank in (0,1):
  physical=lambda r:r if bank==0 else private[r]
  cache={r:1880+i for i,r in enumerate(ry)};exactY={p:1984+i for i,p in enumerate(U)};start=len(ops)
  for r in ry:
   at=w['final'][r];h=cache[r]
   emit(['INIT',h,at],'incoming_init');emit(['ADD',h,physical(r),'1',at],'incoming_copy');emit(['MOVE',h,at,127,True],'incoming_rank1')
  for port in U:
   h=exactY[port];emit(['INIT',h,127],'original_Y_init')
   for r,c in sorted(Y[port].items()):emit(['ADD',h,physical(r) if r in xa else cache[r],str(c),127],'original_Y_decode')
  for i,r in enumerate(rx):
   for j in range(104):
    c=P[i][j]-Q(i==j)
    if c:emit(['ADD',physical(r),exactY[j] if j in exactY else cache[ry[j]],str(c),127],'reverse_correction')
  for i,y in enumerate(fy):
   h=1992;emit(['INIT',h,127],'outgoing_init');c0=Q(1,2) if i in U else Q(1)
   for j,x in enumerate(xs):
    c=-c0*(P[i][j]-Q(i==j))
    if c:
     emit(['ADD',h,physical(x),str(c),127],'outgoing_current_X')
     if j in exactY:emit(['ADD',h,exactY[j],str(c),127],'outgoing_original_X')
   at=w['final'][y];emit(['MOVE',h,127,at,True],'outgoing_rank1');emit(['ADD',physical(y),h,'1',at],'forward_correction');emit(['CLEAR',h,at],'outgoing_retirement')
  for h in cache.values():emit(['CLEAR',h,127],'incoming_retirement')
  for h in exactY.values():emit(['CLEAR',h,127],'original_Y_retirement')
  banks.append({'bank':'common' if bank==0 else 'second','start':start,'stop':len(ops)})
 return {'schema':'moonshot-two-direction-terminal-suffix-v1','public':1880,'owned_fields':113,'program':ops,'marks':marks,'bank_passes':banks,'coupled_inverse_determinant':str(det)}
def main(a):
 e=load(a.helper);source=a.source.read_bytes();need(hashlib.sha256(source).hexdigest()==e.SOURCE_PIN,'source pin');w=json.loads(gzip.decompress(source));wb=a.word.read_bytes();payload=gzip.decompress(wb);need(hashlib.sha256(payload).hexdigest()=='d77b09caae740cd3e0d8ecae92fcebc0b49d8a5f7905d9b425d9d1552748667e','candidate canonical payload pin');word=json.loads(payload);private={int(k):v for k,v in word['difference_role_map'].items()}
 xs,fy,rx,ry,xa,ya,mains,U,roots,P=e.sets(w);rows,loc,bill=e.symbolic_walk(w,word);desired=e.exact_native_target(w);target=desired.copy()
 for r,physical in private.items():target[physical]={private[j]:c for j,c in desired[r].items()}
 AtA=[[sum(v[i]*v[j] for v in roots) for j in range(8)] for i in range(8)];need(AtA==[[104*int(i==j) for j in range(8)] for i in range(8)],'retained104 tight-frame identity')
 E=[[P[i][j]-Q(i==j) for j in range(104)] for i in range(104)];Ei=[[-Q(i==j)+P[i][j]/12 for j in range(104)] for i in range(104)]
 need(all(sum(E[i][k]*Ei[k][j] for k in range(104))==Q(i==j) for i in range(104) for j in range(104)),'exact104 residual inverse')
 mainphys=set(mains)|set(private.values());helperphys=set(range(1480))-set(mains);need(all(rows[r]==target[r]=={r:Q(1)} for r in helperphys),'helper identities')
 charts=sorted({127}|{w['final'][r] for r in fy});spaces={j:e.span(w['frames'][j]) for j in charts};need(len(charts)==len(set(spaces.values()))==105,'105 different binary subspaces')
 need(len(spaces[127])==512 and all(len(spaces[j])==256 for j in charts if j!=127),'hub and104 facets')
 cuts=[]
 for chart in charts:
  fields=sorted(r for r in mainphys if loc[r]==chart);current=[rows[r] for r in fields];want=[target[r] for r in fields];old=rank(current);joint=rank(current+want);deficit=joint-old
  need(deficit==(208 if chart==127 else 2),'actual destination quotient deficit')
  cuts.append({'chart':chart,'binary_basis':w['frames'][chart],'main_fields':fields,'current_main_rank':old,'joint_rank':joint,'independent_helpers_at_chart':sum(loc[r]==chart for r in helperphys),'new_field_unit_lower_bound':deficit})
 need(sum(c['new_field_unit_lower_bound'] for c in cuts)==416,'sum of separate destination arrival charges')
 S=build(e,w,private);complete=dict(word,schema='moonshot-two-direction-complete-source-map-S008-v1',scope='Exact finite normalized completion of all1880 pinned source outputs. The complete fixed H4 recursive target budget fails; physical scalar admission, uniform suppliers and the five foundations remain unresolved. No new kappa.',owned_fields=S['owned_fields'],program=word['program']+S['program'])
 complete['prefix_provenance']={'schema':word['schema'],'scope':word['scope'],'canonical_payload_sha256':hashlib.sha256(payload).hexdigest(),'instruction_count':len(word['program']),'bank_passes':word['bank_passes']}
 complete['marks']=word['marks']+[dict(m,event=len(word['program'])+m['event']) for m in S['marks']]
 complete['bank_passes']=[dict(b,stage='partial_prefix') for b in word['bank_passes']]+[dict(b,stage='exact_terminal_completion',start=len(word['program'])+b['start'],stop=len(word['program'])+b['stop']) for b in S['bank_passes']]
 out,at,whole=e.symbolic_walk(w,complete)
 need(out==target and at==dict(enumerate(word['final'])),'all1880 authentic source endpoints')
 need(Counter(whole['move_histogram'])-Counter(bill['move_histogram'])==Counter({1:416}),'attaining416rank1suffix')
 scount=Counter(op[0] for op in S['program']);need(scount['MOVE']==416 and whole['peak_owned']==113,'suffix cost and storage')
 controls=[]
 for name,purpose,kind in [('omitted_inbound_MOVE','incoming_rank1','omit'),('omitted_forward_correction','forward_correction','omit'),('wrong_reverse_correction','reverse_correction','sign'),('broken_coupled_inverse','original_Y_decode','omit')]:
  k=next(m['event'] for m in S['marks'] if m['purpose']==purpose);bad=[o.copy() for o in S['program']]
  if kind=='omit':bad.pop(k)
  else:bad[k][3]=str(-Q(bad[k][3]))
  try:
   rr,ll,_=e.symbolic_walk(w,dict(complete,program=word['program']+bad));need(rr==target and ll==at,'source target mismatch')
  except ValueError as error:controls.append({'mutation':name,'rejection':str(error)})
  else:raise ValueError('accepted mutant '+name)
 invbytes=a.invoice.read_bytes();need(hashlib.sha256(invbytes).hexdigest()==e.INVOICE_PIN,'invoice pin');cost=e.complete_invoice(w,word,json.loads(invbytes),bill);after=[Q(x)-416 for x in cost['remaining_paid_moment_per_native_bounds']];need(after[1]<0,'full target excluded')
 paid={int(r):n for r,n in cost['paid_histogram'].items()};paid[1]+=18*416;T={int(r):n for r,n in cost['target_histogram'].items()}
 a.outdir.mkdir(parents=True,exist_ok=True)
 for name,data in [('SUFFIX.json.gz',S),('COMPLETE-WORD.json.gz',complete)]:
  payload=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode();(a.outdir/name).write_bytes(gzip.compress(payload,mtime=0))
 result={'status':'PASS_SHARP416_TERMINAL_COMPLETION','source_sha256':e.SOURCE_PIN,'candidate_word_sha256':hashlib.sha256(wb).hexdigest(),'interpreter_sha256':hashlib.sha256(a.helper.read_bytes()).hexdigest(),'tight_frame_identity':'A^T A=104I; credited reuse of eight-packet-prefix/review-algebra/CORRECTION-STRUCTURE.md','residual_inverse':'(P-I)^(-1)=-I+P/12; P^2=13P','terminal_cuts':cuts,'hub_inbound_field_units':208,'facet_inbound_field_units':208,'new_positive_rank_field_units':416,'attaining_MOVE_histogram':{1:416},'suffix_instructions':len(S['program']),'suffix_counts':dict(sorted(scount.items())),'complete_instructions':len(complete['program']),'complete_physical_word':whole,'all1880_source_targets_correct':True,'complete_paid_histogram':dict(sorted(paid.items())),'complete_paid_positions':sum(paid.values()),'complete_target_positions':sum(T.values()),'complete_rank_surplus':sum(r*(T.get(r,0)-paid.get(r,0)) for r in T.keys()|paid.keys()),'remaining_moment_bounds':list(map(str,after)),'remaining_moment_approximate':float(after[0]),'negative_controls':controls,'scope':'Sharp append-only field-linear completion from this exact terminal state, no unrecorded histories or unexecuted funded routes. Arbitrary local recoding/interbank feedback allowed; each wholeVfield MOVE charged at destination. Earlier route/encoding changes remain open.','classification':'Exact finite normalized completion and scoped recursive-cost exclusion; five foundations and physical scalar/precision admission remain. No new kappa.'}
 (a.outdir/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['status','new_positive_rank_field_units','suffix_instructions','complete_instructions','complete_paid_positions','complete_rank_surplus','remaining_moment_approximate']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for name in ['helper','source','word','invoice','outdir']:p.add_argument('--'+name,type=Path,required=True)
 main(p.parse_args())

