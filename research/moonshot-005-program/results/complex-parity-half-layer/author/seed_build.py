#!/usr/bin/env python3
"""Actual reciprocal Gram seed through eight omitted-root lines."""
from __future__ import annotations
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
REPLAY='045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e'
FRAME=[7,25,42,52,76,82,97,127]
def need(c,m):
 if not c:raise ValueError(m)
def loadmod(p):
 need(hashlib.sha256(p.read_bytes()).hexdigest()==REPLAY,'retained replay SHA256');sp=importlib.util.spec_from_file_location('duplex_retained_replay',p);e=importlib.util.module_from_spec(sp);sys.modules[sp.name]=e;sp.loader.exec_module(e);return e
def inverse_op(o):
 ty,i,j,c=o;return ty,i,j,-c if ty=='ADD' else 1/c
def dual_op(o):
 ty,i,j,c=o;return ('ADD',j,i,-c) if ty=='ADD' else ('SCALE',i,i,1/c)
def encoder(M):
 A=copy.deepcopy(M);out=[];n=len(A)
 def emit(o):
  ty,i,j,c=o;out.append(o)
  if ty=='ADD':A[i]=[x+c*y for x,y in zip(A[i],A[j])]
  else:A[i]=[c*x for x in A[i]]
 for j in range(n):
  k=next(i for i in range(j,n) if A[i][j])
  if k!=j:
   emit(('ADD',j,k,F(1)));emit(('ADD',k,j,F(-1)));emit(('ADD',j,k,F(1)));emit(('SCALE',k,k,F(-1)))
  if A[j][j]!=1:emit(('SCALE',j,j,1/A[j][j]))
  for i in range(n):
   if i!=j and A[i][j]:emit(('ADD',i,j,-A[i][j]))
 need(A==[[F(i==j) for j in range(n)] for i in range(n)],'exact invertible encoder');return [inverse_op(o) for o in reversed(out)]
def basis(vs):
 d={}
 for v in vs:
  while v:
   p=v.bit_length()-1
   if p in d:v^=d[p]
   else:
    d[p]=v
    for j in d:
     if j!=p and d[j]>>p&1:d[j]^=v
    break
 return [d[p] for p in sorted(d,reverse=True)]
def root(v):
 one=[i for i in range(9) if v>>i&1]
 if len(one)==3:return [F(2 if i in one else -1) for i in range(9)]
 zero=[i for i in range(9) if i not in one];need(len(zero)==2,'E8 normal');return [F(3*(int(i==zero[0])-int(i==zero[1]))) for i in range(9)]
def clean(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 return x

def main(a):
 e=loadmod(a.engine);n=e.load(a.native,e.NATIVE);q=e.load(a.parent,e.PARENT);role={int(k):v for k,v in q['source_role_map'].items()};ports=list(n['live']);host={n['live'][k]:(role[b],role[d]) for k,b,d in zip(n['hosted']['Dports'],n['hosted']['X2'],n['hosted']['Y2'])};U=sorted(set(ports)-set(host));X={h:role[h] for h in ports};Y={h:role[h+112] for h in ports};v={h:n['frames'][n['initial'][h]][0] for h in ports};r={h:root(v[h]) for h in ports};fr=[root(z) for z in FRAME]
 need(not set(FRAME)&set(v.values()),'entire orthogonal frame omitted from full104 source');need(all(sum(x*y for x,y in zip(fr[i],fr[j]))==18*int(i==j) for i in range(8) for j in range(8)),'orthogonal frame exact')
 g={h:[sum(x*y for x,y in zip(f,r[h]))/18 for f in fr] for h in ports};G={(h,j):sum(g[h][i]*g[j][i] for i in range(8)) for h in ports for j in ports};need(all(G[h,j]==sum(x*y for x,y in zip(r[h],r[j]))/18 for h in ports for j in ports),'all104 Gram factorization')
 patterns={}
 for h in ports:
  pat=tuple(i for i,z in enumerate(FRAME) if (v[h]&z).bit_count()%2==0);need(len(pat)==4 and tuple(i for i,x in enumerate(g[h]) if x)==pat,'actual four-mode pattern');patterns.setdefault(pat,[]).append(h)
 need(len(patterns)==14,'fourteen actual classes')
 frames=copy.deepcopy(q['frames']);where={frozenset(e.span(f)):k for k,f in enumerate(frames)}
 def chart(f):
  f=basis(f);s=frozenset(e.span(f))
  if s not in where:where[s]=len(frames);frames.append(f)
  return where[s]
 O=chart([]);Hub=chart([1<<i for i in range(9)]);lines=[chart([z]) for z in FRAME];facets={h:chart(basis(w for w in range(512) if not (w&v[h]).bit_count()%2)) for h in ports};need(O==3 and Hub==127,'retained ground/Hub roles')
 groups=[]
 for pat,allh in sorted(patterns.items()):
  hs=sorted(h for h in allh if h in host);us=sorted(h for h in allh if h not in host);ys=hs+us;A=[[g[h][i] for h in hs] for i in pat];_,piv=e.select([[int(x.numerator)*pow(x.denominator,-1,e.PRIME)%e.PRIME for x in row] for row in A]);need(len(piv)==4,'hosted class rank4')
  Md=[[F(i==j) for j in range(len(hs))] for i in range(len(hs))];My=[[F(i==j) for j in range(len(ys))] for i in range(len(ys))]
  for mode,p in zip(pat,piv):
   Md[p]=[g[h][mode] for h in hs];My[p]=[g[h][mode]*(1 if h in host else F(1,2)) for h in ys]
  ed=encoder(Md);ey=encoder(My);C=chart([FRAME[i] for i in pat]);need(len(frames[C])==3,'class C3');need(all(e.span(frames[C])<e.span(frames[facets[h]]) for h in ys),'all actual class facets contain C3');need(all(e.span(frames[lines[i]])<e.span(frames[C]) for i in pat),'all four mode lines below C3')
  groups.append({'modes':list(pat),'ports':ys,'hosted':hs,'coupled':us,'D_roles':[host[h][1] for h in hs],'Y_roles':[Y[h] for h in ys],'pivots':piv,'C':C,'C_frame':frames[C],'M_D':Md,'M_Y':My,'D_encoder':ed,'Y_encoder':ey,'markers':{}})
 out=[];markers={};events={}
 def emit(o):out.append(o)
 def bop(bank,ops,C):
  for ty,i,j,c in ops:emit(['ADD',bank[i],bank[j],str(c),C] if ty=='ADD' else ['SCALE',bank[i],str(c),C])
 for h in U:
  emit(['INIT',400,O]);emit(['ADD',400,Y[h],'1',O]);emit(['MOVE',400,O,q['initial'][X[h]],True]);emit(['ADD',X[h],400,'-1',q['initial'][X[h]]]);emit(['CLEAR',400,q['initial'][X[h]]])
 markers['entry_end']=len(out)
 for i,L in enumerate(lines):emit(['INIT',400+i,L])
 for gi,z in enumerate(groups):
  bank=z['D_roles'];C=z['C'];enc=z['D_encoder'];z['markers']['D_encode_begin']=len(out);bop(bank,enc,O);z['markers']['D_encode_end']=len(out);pmap={p:i for p,i in zip(z['pivots'],z['modes'])}
  for j,d in enumerate(bank):
   if j in pmap:
    i=pmap[j];emit(['MOVE',d,O,lines[i],False]);emit(['ADD',400+i,d,'1',lines[i]]);emit(['MOVE',d,lines[i],C,False])
   else:emit(['MOVE',d,O,C,False])
  bop(bank,[inverse_op(o) for o in reversed(enc)],C);z['markers']['D_restored_at_C3']=len(out)
  for h,d in zip(z['hosted'],bank):emit(['MOVE',d,C,facets[h],False])
 markers['D_all_restored']=len(out);markers['XB_slot_begin']=len(out)
 for h in ports:emit(['MOVE',X[h],q['initial'][X[h]],Hub,False])
 for h,(b,d) in host.items():emit(['MOVE',b,q['initial'][b],Hub,False])
 markers['XB_slot_end']=len(out)
 for i,L in enumerate(lines):
  emit(['MOVE',400+i,L,Hub,True]);events.setdefault('reverse_returns',[]).append(len(out)-1)
  for h,(b,d) in host.items():
   if g[h][i]:emit(['ADD',b,400+i,str(-g[h][i]),Hub])
  emit(['CLEAR',400+i,Hub])
 markers['reverse_consumed']=len(out)
 for i,L in enumerate(lines):
  emit(['INIT',400+i,Hub])
  for h in ports:
   if g[h][i]:emit(['ADD',400+i,X[h],str(g[h][i]),Hub])
  emit(['MOVE',400+i,Hub,L,True]);events.setdefault('forward_descents',[]).append(len(out)-1)
 markers['forward_modes_at_lines']=len(out)
 for gi,z in enumerate(groups):
  bank=z['Y_roles'];C=z['C'];enc=[dual_op(o) for o in z['Y_encoder']];z['markers']['Y_encode_begin']=len(out);bop(bank,enc,O);z['markers']['Y_encode_end']=len(out);pmap={p:i for p,i in zip(z['pivots'],z['modes'])}
  for j,y in enumerate(bank):
   if j in pmap:
    i=pmap[j];emit(['MOVE',y,O,lines[i],False]);events.setdefault('forward_reads',[]).append(len(out));emit(['ADD',y,400+i,'1',lines[i]]);emit(['MOVE',y,lines[i],C,False])
   else:emit(['MOVE',y,O,C,False])
  bop(bank,[inverse_op(o) for o in reversed(enc)],C);z['markers']['Y_decode_end']=len(out)
  for h,y in zip(z['ports'],bank):emit(['MOVE',y,C,facets[h],False])
 for i,L in enumerate(lines):emit(['CLEAR',400+i,L])
 w={'schema':'moonshot-S011-eight-line-Gram-duplex-seed-v1','public':400,'owned_fields':8,'initial':q['initial'],'frames':frames,'source_role_map':q['source_role_map'],'program':out,'source_pins':{'native':e.NATIVE,'interface_parent':e.PARENT},'duplex':{'omitted_frame':FRAME,'lines':lines,'groups':clean(groups),'markers':markers,'events':events,'standalone_rebuilt_source':True,'old_compensated_word_progress_not_retained':True}}
 captures={};boundaries={z['markers']['D_restored_at_C3'] for z in groups}|{markers['D_all_restored'],markers['forward_modes_at_lines'],markers['entry_end']}
 def capture(t,o,rr,ll):
  if t+1 in boundaries:captures[t+1]=copy.deepcopy(rr)
 rr,ll,bill=e.replay(w,out,capture);_,source_final_locations,_=e.replay(q,q['program'][:q['consumer']['begin']]);need(ll==source_final_locations,'all400 literal source-prescribed final chart identifiers');aa={h:{X[h]:F(1)} if h in host else {X[h]:F(1),Y[h]:F(-1)} for h in ports};want={j:{j:F(1)} for j in range(400)};wantloc={}
 for h in ports:
  want[X[h]]=aa[h];wantloc[X[h]]=Hub;wantloc[Y[h]]=facets[h]
  for j in ports:want[Y[h]]=e.add(want[Y[h]],aa[j],G[h,j]*(1 if h in host else F(1,2)))
 for h,(b,d) in host.items():
  wantloc[b]=Hub;wantloc[d]=facets[h]
  for j,(bj,dj) in host.items():want[b]=e.add(want[b],{dj:F(1)},-G[h,j])
 need(rr==want and ll==wantloc,'exact complete400-column Gram-duplex source map');need(e.exact_rank(rr.values())==400,'all400 input directions retained')
 for z in groups:need(all(captures[z['markers']['D_restored_at_C3']][d]=={d:F(1)} for d in z['D_roles']),'each original D restored at its actual C3')
 for i in range(8):
  expect={d:g[h][i] for h,(b,d) in host.items() if g[h][i]};need(captures[markers['D_all_restored']][400+i]==expect,'eight actual full Gram records before any return')
  expect={}
  for h in ports:expect=e.add(expect,aa[h],g[h][i])
  need(captures[markers['forward_modes_at_lines']][400+i]==expect,'actual original coupled-current-a forward mode')
 need(all(rr[b].get(dj,F(0))+rr[Y[j]].get(X[h],F(0))==0 for h,(b,d) in host.items() for j,(bj,dj) in host.items()),'actual R+L_HHtranspose=0, all9216 entries')
 raw=Counter();owned=Counter()
 for o in out:
  if o[0]=='MOVE':(owned if o[4] else raw)[abs(len(frames[o[3]])-len(frames[o[2]]))]+=1
 need(dict(raw)=={1:112,2:112,3:88,5:200,8:200},'complete raw profile');need(dict(owned)=={1:8,8:16},'complete owned profile including coupled entries');need(sum(r*v for r,v in raw.items())==3200,'original public rank mass3200')
 scalars=[F(o[3] if o[0]=='ADD' else o[2]) for o in out if o[0] in ('ADD','SCALE')];need(all(z.denominator&(z.denominator-1)==0 for z in scalars),'every introduced scalar is exactly dyadic')
 fwd=sum(len(e.add(rr[Y[h]],{X[h]:F(1) if h in host else F(1,2),Y[h]:F(1) if h in host else F(1,2)},F(-1))) for h in ports);rev=e.exact_rank([e.add(rr[b],{b:F(1),d:F(-1)},F(-1)) for h,(b,d) in host.items()]);need(fwd==5376 and rev==96,'honest unfinished endpoint debt')
 controls=[];choices={'omit_D_inverse':groups[0]['markers']['D_restored_at_C3']-1,'omit_Y_inverse':groups[0]['markers']['Y_decode_end']-1,'wrong_forward_read_sign':events['forward_reads'][0],'wrong_coupled_entry_sign':3,'wrong_reverse_consumer_sign':events['reverse_returns'][0]+1,'wrong_forward_line':events['forward_descents'][0]}
 for label,k in choices.items():
  bad=copy.deepcopy(w);o=bad['program'][k]
  if label=='wrong_forward_line':o[3]=Hub
  elif o[0]=='ADD':o[3]=str(-F(o[3])) if label not in ('omit_D_inverse','omit_Y_inverse') else '0'
  elif o[0]=='SCALE':o[2]='1'
  else:raise ValueError('negative-control opcode')
  try:mr,ml,mb=e.replay(bad,bad['program']);rejected=(mr!=rr or ml!=ll)
  except ValueError:rejected=True
  need(rejected,'negative control '+label);controls.append(label)
 payload=(json.dumps(clean(w),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0);a.output.mkdir(parents=True,exist_ok=True);(a.output/'WORD.json.gz').write_bytes(blob);result={'status':'PASS_ACTUAL_EIGHT_LINE_GRAM_DUPLEX_SOURCE','native_sha256':e.NATIVE,'interface_parent_sha256':e.PARENT,'word_sha256':hashlib.sha256(blob).hexdigest(),'payload_sha256':hashlib.sha256(payload).hexdigest(),'producer_replay_sha256':REPLAY,'all400_input_rank':400,'all_D_restored_at_C3':True,'actual_eight_reverse_Gram_records_at_lines':True,'actual_eight_forward_Gram_records_at_lines':True,'hosted_R_plus_L_transpose_zero':True,'old_compensated_progress_retained':False,'current_a_forward_offdiagonal_coefficients':sum(h!=j and bool(G[h,j]) for h in ports for j in ports),'original_coordinate_forward_debt':fwd,'reverse_residual_rank':rev,'source_bill':bill,'raw_histogram':dict(raw),'owned_histogram':dict(owned),'groups':clean(groups),'frame':FRAME,'negative_controls':controls,'scope':'Actual reconstructed400-coordinate Gram forward/reverse seed with all D restored and full input rank. Paired global offdiagonal compiler, chronology with its actual caches/routes, complete endpoints, uniform supplier, physical costs and kappa remain open.'};(a.output/'RESULT.json').write_text(json.dumps(clean(result),sort_keys=True,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','word_sha256','original_coordinate_forward_debt','reverse_residual_rank','source_bill','raw_histogram','owned_histogram']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
