#!/usr/bin/env python3
"""All-class reciprocal parity-half correction with literal coupled inputs."""
from __future__ import annotations
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
seed_path=Path(__file__).with_name('seed_build.py')
if hashlib.sha256(seed_path.read_bytes()).hexdigest()!='4cb31f8f1c5b2e069afbbb3a3f028c787b677684a558bc12c2f31f51a4871297':raise ValueError('retained omitted-line builder dependency pin')
seed_spec=importlib.util.spec_from_file_location('retained_seed_builder',seed_path);s=importlib.util.module_from_spec(seed_spec);sys.modules[seed_spec.name]=s;seed_spec.loader.exec_module(s)

def match_anchors(halfclasses):
 out={}
 def visit(k,used):
  if k==len(halfclasses):return True
  j,z=halfclasses[k]
  for i in z['modes']:
   if i not in used:
    out[j]=i
    if visit(k+1,used|{i}):return True
  out.pop(j,None);return False
 s.need(visit(0,set()),'distinct anchor-mode matching');return out

def main(a):
 e=s.loadmod(a.engine);n=e.load(a.native,e.NATIVE);q=e.load(a.parent,e.PARENT)
 role={int(k):v for k,v in q['source_role_map'].items()};ports=list(n['live']);host={n['live'][k]:(role[b],role[d]) for k,b,d in zip(n['hosted']['Dports'],n['hosted']['X2'],n['hosted']['Y2'])};U=sorted(set(ports)-set(host));X={h:role[h] for h in ports};Y={h:role[h+112] for h in ports};v={h:n['frames'][n['initial'][h]][0] for h in ports};r={h:s.root(v[h]) for h in ports};fr=[s.root(z) for z in s.FRAME]
 g={h:[sum(x*y for x,y in zip(f,r[h]))/18 for f in fr] for h in ports};G={(h,j):sum(g[h][i]*g[j][i] for i in range(8)) for h in ports for j in ports};patterns={}
 for h in ports:
  pat=tuple(i for i,x in enumerate(g[h]) if x);s.need(len(pat)==4,'four modes');patterns.setdefault(pat,[]).append(h)
 frames=copy.deepcopy(q['frames']);where={frozenset(e.span(f)):k for k,f in enumerate(frames)}
 def chart(f):
  f=s.basis(f);sp=frozenset(e.span(f))
  if sp not in where:where[sp]=len(frames);frames.append(f)
  return where[sp]
 def perp(vs):return chart(w for w in range(512) if all(not (w&z).bit_count()%2 for z in vs))
 O=chart([]);Hub=chart([1<<i for i in range(9)]);lines=[chart([z]) for z in s.FRAME];facets={h:perp([v[h]]) for h in ports}
 groups=[];halves=[];halfof={};classof={}
 for gi,(pat,allh) in enumerate(sorted(patterns.items())):
  hs=sorted(h for h in allh if h in host);A=[[g[h][i] for h in hs] for i in pat];_,piv=e.select([[int(x.numerator)*pow(x.denominator,-1,e.PRIME)%e.PRIME for x in row] for row in A]);s.need(len(piv)==4,'hosted full class rank4');Md=[[F(i==j) for j in range(len(hs))] for i in range(len(hs))]
  for i,p in zip(pat,piv):Md[p]=[g[h][i] for h in hs]
  C=chart([s.FRAME[i] for i in pat]);s.need(len(frames[C])==3,'class C3');z={'index':gi,'modes':list(pat),'ports':sorted(allh),'hosted':hs,'pivots':piv,'M_D':Md,'D_encoder':s.encoder(Md),'C3':C,'markers':{}}
  part={-1:[],1:[]}
  for h in allh:
   sg=1
   for i in pat:sg*=1 if g[h][i]>0 else -1
   part[sg].append(h);classof[h]=gi
  z['halves']=[]
  for sg,hh in sorted(part.items()):
   hh=sorted(hh);C6=perp([v[h] for h in hh]);s.need(len(hh) in (3,4) and len(frames[C6])==6,'actual full-Y half size3/4 and C6');s.need(e.span(frames[C])<e.span(frames[C6]),'C3 below half C6');s.need(all(G[h,j]==int(h==j) for h in hh for j in hh),'each half is real orthogonal')
   k=len(halves);z['halves'].append(k);halves.append({'index':k,'class':gi,'sign':sg,'modes':list(pat),'ports':hh,'hosted':[h for h in hh if h in host],'coupled':[h for h in hh if h not in host],'C3':C,'C6':C6,'markers':{}})
   for h in hh:halfof[h]=k
  for k in z['halves']:
   other=z['halves'][1] if k==z['halves'][0] else z['halves'][0];halves[k]['opposite']=other
   s.need(all(v[h] in e.span(frames[halves[k]['C6']]) for h in halves[other]['ports']),'all opposite source lines below C6')
  groups.append(z)
 deficient=[(k,z) for k,z in enumerate(halves) if len(z['ports'])==3];s.need(len(deficient)==8,'eight deficient full-Y halves');anchors=match_anchors(deficient);s.need(len(set(anchors.values()))==8,'every forward mode serves exactly one anchor')
 s.need(len(groups)==14 and all(sum(i in z['modes'] for z in groups)==7 for i in range(8)),'fourteen class-mode embeddings satisfy E E^T=7I')
 for k,z in enumerate(halves):
  hh=z['ports'];modes=z['modes'];anchor=anchors.get(k);basis_modes=[i for i in modes if i!=anchor];M=[[g[h][i]*(1 if h in host else F(1,2)) for h in hh] for i in basis_modes];enc=s.encoder(M);z.update({'anchor':anchor,'basis_modes':basis_modes,'M_Y':M,'Y_encoder':enc})
  if anchor is not None:
   # A_anchor is the stated exact combination of the three nonanchor rows.
   # Rows of M inverse are obtained by applying its inverse elementary word.
   inv=[[F(i==j) for j in range(3)] for i in range(3)]
   for ty,i,j,c in [s.inverse_op(o) for o in reversed(enc)]:
    if ty=='ADD':inv[i]=[x+c*y for x,y in zip(inv[i],inv[j])]
    else:inv[i]=[c*x for x in inv[i]]
   ar=[g[h][anchor]*(1 if h in host else F(1,2)) for h in hh];co=[sum(ar[j]*inv[j][i] for j in range(3)) for i in range(3)];s.need(all(sum(co[i]*M[i][j] for i in range(3))==ar[j] for j in range(3)),'exact anchor dependence');s.need(all(abs(x)==1 for x in co),'anchor signs');z['anchor_coefficients']=co;z['anchor_cache']=512+anchor
 out=[];markers={};events={};captures={}
 def emit(o):out.append(o)
 def bop(bank,ops,C):
  for ty,i,j,c in ops:emit(['ADD',bank[i],bank[j],str(c),C] if ty=='ADD' else ['SCALE',bank[i],str(c),C])
 for h in U:
  emit(['INIT',400,O]);emit(['ADD',400,Y[h],'1',O]);emit(['MOVE',400,O,q['initial'][X[h]],True]);emit(['ADD',X[h],400,'-1',q['initial'][X[h]]]);emit(['CLEAR',400,q['initial'][X[h]]])
 for i,L in enumerate(lines):emit(['INIT',400+i,L])
 for z in groups:
  bank=[host[h][1] for h in z['hosted']];C=z['C3'];enc=z['D_encoder'];bop(bank,enc,O);pmap={p:i for p,i in zip(z['pivots'],z['modes'])}
  for j,d in enumerate(bank):
   if j in pmap:
    i=pmap[j];emit(['MOVE',d,O,lines[i],False]);emit(['ADD',400+i,d,'1',lines[i]]);emit(['MOVE',d,lines[i],C,False])
   else:emit(['MOVE',d,O,C,False])
  bop(bank,[s.inverse_op(o) for o in reversed(enc)],C);z['markers']['D_restored_C3']=len(out)
  for h,d in zip(z['hosted'],bank):emit(['MOVE',d,C,halves[halfof[h]]['C6'],False])
 markers['D_waiting_at_C6']=len(out)
 for z in halves:
  C=z['C6'];opp=halves[z['opposite']]['ports'];z['markers']['compiler_begin']=len(out)
  for h in opp:
   emit(['MOVE',X[h],q['initial'][X[h]],C,False])
   if h in host:emit(['MOVE',host[h][0],q['initial'][host[h][0]],C,False])
  for h in z['ports']:
   ca=408+ports.index(h);emit(['INIT',ca,C])
   for j in opp:
    c=-G[h,j]*(1 if h in host else F(1,2));s.need(c,'opposite parity coefficient');emit(['ADD',ca,X[j],str(c),C])
  for j in opp:
   if j in host:
    for h in z['hosted']:emit(['ADD',host[j][0],host[h][1],str(G[j,h]),C])
  z['markers']['compiler_cache_ready']=len(out)
  for h in opp:
   emit(['MOVE',X[h],C,Hub,False])
   if h in host:emit(['MOVE',host[h][0],C,Hub,False])
 for h,(b,d) in host.items():emit(['MOVE',d,halves[halfof[h]]['C6'],facets[h],False])
 markers['compiler_end']=len(out)
 for i,L in enumerate(lines):
  emit(['MOVE',400+i,L,Hub,True]);events.setdefault('reverse_moves',[]).append(len(out)-1)
  for h,(b,d) in host.items():
   if g[h][i]:emit(['ADD',b,400+i,str(-g[h][i]),Hub])
  emit(['CLEAR',400+i,Hub])
 for i,L in enumerate(lines):
  emit(['INIT',400+i,Hub])
  for h in ports:
   if g[h][i]:emit(['ADD',400+i,X[h],str(g[h][i]),Hub])
  k=next(k for k,x in anchors.items() if x==i);C=halves[k]['C3'];emit(['MOVE',400+i,Hub,C,True]);emit(['INIT',512+i,C]);emit(['ADD',512+i,400+i,'1',C]);emit(['MOVE',400+i,C,L,True])
 markers['forward_modes_ready']=len(out)
 for z in halves:
  bank=[Y[h] for h in z['ports']];C=z['C6'];enc=[s.dual_op(o) for o in z['Y_encoder']];bop(bank,enc,O)
  for j,y in enumerate(bank):
   i=z['basis_modes'][j];emit(['MOVE',y,O,lines[i],False]);events.setdefault('forward_reads',[]).append(len(out));emit(['ADD',y,400+i,'1',lines[i]])
   if z['anchor'] is None:emit(['MOVE',y,lines[i],C,False])
   else:
    C3=z['C3'];emit(['MOVE',y,lines[i],C3,False]);events.setdefault('anchor_reads',[]).append(len(out));emit(['ADD',y,z['anchor_cache'],str(z['anchor_coefficients'][j]),C3]);emit(['MOVE',y,C3,C,False])
  bop(bank,[s.inverse_op(o) for o in reversed(enc)],C);z['markers']['Y_decode_end']=len(out)
  for h,y in zip(z['ports'],bank):
   ca=408+ports.index(h);events.setdefault('correction_reads',[]).append(len(out));emit(['ADD',y,ca,'1',C]);emit(['CLEAR',ca,C]);emit(['MOVE',y,C,facets[h],False])
  if z['anchor'] is not None:emit(['CLEAR',z['anchor_cache'],z['C3']])
 for i,L in enumerate(lines):emit(['CLEAR',400+i,L])
 w={'schema':'moonshot-S011-parity-half-paired-compiler-v1','public':400,'owned_fields':120,'initial':q['initial'],'frames':frames,'source_role_map':q['source_role_map'],'program':out,'source_pins':{'native':e.NATIVE,'interface_parent':e.PARENT},'parity_compiler':{'omitted_frame':s.FRAME,'lines':lines,'groups':s.clean(groups),'halves':s.clean(halves),'anchors':anchors,'markers':markers,'events':events,'standalone_rebuilt_source':True}}
 boundaries={z['markers']['D_restored_C3'] for z in groups}|{markers['D_waiting_at_C6'],markers['forward_modes_ready']}
 def capture(t,o,rr,ll):
  if t+1 in boundaries:captures[t+1]=copy.deepcopy(rr)
 rr,ll,bill=e.replay(w,out,capture);_,source_final_locations,_=e.replay(q,q['program'][:q['consumer']['begin']]);s.need(ll==source_final_locations,'all literal400 endpoint chart IDs')
 aa={h:{X[h]:F(1)} if h in host else {X[h]:F(1),Y[h]:F(-1)} for h in ports};want={j:{j:F(1)} for j in range(400)};cross={(h,j):G[h,j] if classof[h]!=classof[j] else F(0) for h in ports for j in ports}
 for h in ports:
  want[X[h]]=aa[h]
  for j in ports:want[Y[h]]=e.add(want[Y[h]],aa[j],(int(h==j)+cross[h,j])*(1 if h in host else F(1,2)))
 for h,(b,d) in host.items():
  for j,(bj,dj) in host.items():want[b]=e.add(want[b],{dj:F(1)},-int(h==j)-cross[h,j])
 s.need(rr==want,'complete400 exact parity-paired endpoint map');s.need(e.exact_rank(rr.values())==400,'all400 private input directions preserved')
 for z in groups:s.need(all(captures[z['markers']['D_restored_C3']][host[h][1]]=={host[h][1]:F(1)} for h in z['hosted']),'all original D restored at class C3')
 for i in range(8):
  need={d:g[h][i] for h,(b,d) in host.items() if g[h][i]};s.need(captures[markers['D_waiting_at_C6']][400+i]==need,'actual reverse Gram records');expect={}
  for h in ports:expect=e.add(expect,aa[h],g[h][i])
  s.need(captures[markers['forward_modes_ready']][400+i]==expect and captures[markers['forward_modes_ready']][512+i]==expect,'actual forward mode and its stationary anchor cache')
 s.need(all(rr[b].get(dj,F(0))+rr[Y[j]].get(X[h],F(0))==0 for h,(b,d) in host.items() for j,(bj,dj) in host.items()),'all9216 actual transpose equalities')
 raw=Counter();owned=Counter()
 for o in out:
  if o[0]=='MOVE':(owned if o[4] else raw)[abs(len(frames[o[3]])-len(frames[o[2]]))]+=1
 s.need(dict(raw)=={1:160,2:280,3:360,5:280},'exact all-original profile');s.need(dict(owned)=={1:8,2:8,6:8,8:8},'exact complete owned profile');s.need(sum(k*z for k,z in raw.items())==3200,'public rank mass3200')
 scalars=[F(o[3] if o[0]=='ADD' else o[2]) for o in out if o[0] in ('ADD','SCALE')];s.need(all(z.denominator&(z.denominator-1)==0 for z in scalars),'all introduced scalars exactly dyadic')
 fwd=sum(len(e.add(rr[Y[h]],{X[h]:F(1) if h in host else F(1,2),Y[h]:F(1) if h in host else F(1,2)},F(-1))) for h in ports);rev=e.exact_rank([e.add(rr[b],{b:F(1),d:F(-1)},F(-1)) for h,(b,d) in host.items()]);current=sum(bool(cross[h,j]) for h in ports for j in ports)
 negative=[]
 for label,k in [('wrong_anchor_sign',events['anchor_reads'][0]),('wrong_correction_sign',events['correction_reads'][0]),('wrong_Gram_sign',events['forward_reads'][0]),('omit_D_inverse',groups[0]['markers']['D_restored_C3']-1),('omit_half_Y_inverse',halves[0]['markers']['Y_decode_end']-1)]:
  bad=copy.deepcopy(w);o=bad['program'][k]
  if o[0]=='ADD':o[3]='0' if label.startswith('omit') else str(-F(o[3]))
  elif o[0]=='SCALE':o[2]='1'
  else:raise ValueError('negative-control opcode')
  try:mr,ml,_=e.replay(bad,bad['program']);rejected=mr!=rr or ml!=ll
  except ValueError:rejected=True
  s.need(rejected,'negative control '+label);negative.append(label)
 payload=(json.dumps(s.clean(w),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0);a.output.mkdir(parents=True,exist_ok=True);(a.output/'WORD.json.gz').write_bytes(blob)
 result={'status':'PASS_ACTUAL_PARITY_HALF_PAIRED_COMPILER','word_sha256':hashlib.sha256(blob).hexdigest(),'payload_sha256':hashlib.sha256(payload).hexdigest(),'native_sha256':e.NATIVE,'interface_parent_sha256':e.PARENT,'all400_input_rank':400,'all_D_restored_at_C3':True,'hosted_R_plus_L_transpose_zero':True,'actual_reverse_and_forward_Gram_modes':True,'current_a_forward_offdiagonal_coefficients':current,'within_class_coefficients_removed':4992-current,'original_coordinate_forward_debt':fwd,'reverse_residual_rank':rev,'source_bill':bill,'raw_histogram':dict(raw),'owned_histogram':dict(owned),'anchors':anchors,'halfclass_size_census':dict(Counter(len(z['ports']) for z in halves)),'groups':s.clean(groups),'halves':s.clean(halves),'negative_controls':negative,'scope':'Actual full400 paired local correction and original restoration. Cross-class compiler, completed endpoint source and uniform supplier remain open; no new kappa.'}
 (a.output/'RESULT.json').write_text(json.dumps(s.clean(result),sort_keys=True,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','word_sha256','current_a_forward_offdiagonal_coefficients','original_coordinate_forward_debt','reverse_residual_rank','source_bill','raw_histogram','owned_histogram']},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
