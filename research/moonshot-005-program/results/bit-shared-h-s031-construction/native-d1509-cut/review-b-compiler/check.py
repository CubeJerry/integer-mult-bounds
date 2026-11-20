#!/usr/bin/env python3
"""Independent literal compiler/accounting review; no author executable imported."""
from pathlib import Path
from array import array
from hashlib import sha256
from collections import defaultdict
import gzip,json,sys,time
import numpy as np
HERE=Path(__file__).resolve().parent;PACKAGE=HERE.parent;BASE=HERE.parents[2]
def read(p):return json.loads(gzip.decompress(p.read_bytes()))
manifest=json.loads((PACKAGE/'MANIFEST.json').read_text())
for name,digest in manifest.items():assert sha256((PACKAGE/name).read_bytes()).hexdigest()==digest
s=read(PACKAGE/'output/SOURCES.json.gz');early=read(PACKAGE/'output/EARLY.json.gz');hs=read(PACKAGE/'output/H-PHYSICAL.json.gz');dw=read(PACKAGE/'output/D-WORD.json.gz');expected=read(PACKAGE/'output/PHASE-COMPILER-RECEIPTS.json.gz');bill=json.loads((PACKAGE/'output/COMPILER-RESULT.json').read_text())
old=read(BASE/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/COEFFICIENTS.json.gz')
routefile=BASE/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz';routes=[json.loads(x)for x in gzip.decompress(routefile.read_bytes()).splitlines()]
orderkey=lambda r:(r[1],r[2]);HX=defaultdict(list);HY=defaultdict(list);SX=defaultdict(list);SY=defaultdict(list)
for r in routes:
 if r[3]is not None:
  (HX if r[0]=='X'else HY)[r[3]].append(r)
  if r[0]=='X':SX[r[1],r[3]].append(r)
  elif r[6]is not None:SY[r[6],r[3]].append(r)
for groups in [HX,HY,SX,SY]:
 for k in groups:groups[k].sort(key=orderkey)
def rem(value):
 while value.bit_length()>6:value^=67<<(value.bit_length()-7)
 return value
monomial=[[rem(a<<k)for k in range(6)]for a in range(64)]
pattern=[[sum(((monomial[a][k]>>b)&1)<<k for k in range(6))for b in range(6)]for a in range(64)]
product=np.zeros((64,64),dtype=np.uint8)
for a in range(64):
 for b in range(64):
  v=0
  for k in range(6):
   if b>>k&1:v^=a<<k
  product[a,b]=rem(v)
def mat(values,shape=None):
 A=np.array(values,dtype=np.uint8)
 if shape is not None:A=A.reshape(shape)
 assert all(isinstance(v,int)and 0<=v<64 for row in values for v in row)
 return A
def mm(A,B):
 C=np.zeros((len(A),B.shape[1]),dtype=np.uint8)
 for k in range(A.shape[1]):C^=product[A[:,k,None],B[k,None,:]]
 return C
def lift(A):
 result=[]
 for row in A:
  bits=[0]*6
  for c,a in enumerate(row):
   for b in range(6):bits[b]|=pattern[int(a)][b]<<(6*c)
  result.extend(bits)
 return result
def apply(state,ops,forward):
 state=state.copy();indices=range(len(ops)-2,-1,-2)if forward else range(0,len(ops),2)
 for k in indices:
  t,u=ops[k],ops[k+1];assert t!=u and t<len(state)and u<len(state);state[t]^=state[u]
 return state
def compile_matrix(A):
 binary=lift(A);n=len(binary);assert A.shape==(n//6,n//6);work=binary.copy();ops=array('I');swaps=0
 for j in range(n):
  k=next(i for i in range(j,n)if work[i]>>j&1)
  if j!=k:
   swaps+=1
   for t,u in [(j,k),(k,j),(j,k)]:work[t]^=work[u];ops.extend([t,u])
  clear=[i for i,v in enumerate(work)if i!=j and v>>j&1]
  for i in clear:work[i]^=work[j];ops.extend([i,j])
 identity=[1<<j for j in range(n)];assert work==identity
 forward=apply(identity,ops,True);assert forward==binary and apply(forward,ops,False)==identity
 encoded=ops.tobytes()if sys.byteorder=='little'else b''.join(int(v).to_bytes(4,'little')for v in ops)
 receipt={'field_dimension':len(A),'binary_dimension':n,'ADD_per_direction':len(ops)//2,'elimination_word_uint32le_sha256':sha256(encoded).hexdigest()}
 return receipt,ops,binary,swaps
started=time.time();phase=0;parity_add=0;parity_fields=0;H_cache_fields=0;H_cross_add=0;H_cache_modules=[];all_cache_labels=set();Ytargets=set();source_receipts=[];H_receipts=[]
for js,e in sorted(early.items(),key=lambda x:int(x[0])):
 j=int(js);A=mat(e['physical_matrix']);assert A.shape==(480,480)
 assigned={};labels_to_row={tuple(label):row for label,row in zip(e['row_owners'],e['matrix'])};assert len(labels_to_row)==480
 source_parity_count=source_parity_add=0;actual_bindings=[]
 for hstr,Fvalue in s['maps'][js].items():
  h=int(hstr);F=mat(Fvalue);assert F.shape==(15,240);Q=mat(s['frames'][f'{j}/{h}']);assert Q.shape==(30,30)
  B=np.zeros((30,480),dtype=np.uint8);B[:15,:240]=F;B[15:,240:]=F;R=mm(Q,B);xs=SX[j,h];ys=SY[j,h];quota=len(xs);assert quota in [15,30]and len(ys)==30-quota
  P=mat(s['late_parities'][js][hstr],(30-quota,480));assert np.array_equal(P,R[quota:])
  for k,r in enumerate(xs):
   assert r[6]==j and r[2]not in assigned and labels_to_row[h,r[2]]==R[k].tolist();assigned[r[2]]=R[k]
  binaryP=lift(P);source_parity_add+=sum(v.bit_count()for v in binaryP);source_parity_count+=len(P)
  # Cache each complete parity on original inputs before the early map. Each
  # one-bit coefficient costs one ADD into an initialized stationary bit.
  cache=[]
  for targetmask in binaryP:
   actual=0;remaining=targetmask
   while remaining:
    low=remaining&-remaining;actual^=low;remaining-=low
   assert actual==targetmask;cache.append(actual)
  for q,r in enumerate(ys):
   target=('Y',r[1],r[2]);assert target not in Ytargets;Ytargets.add(target)
   binding={'H':h,'Y_owner':[r[1],r[2]],'row':q,'cache_label':f'source-parity/{j}/{h}/{q}'};actual_bindings.append(binding)
   for bit in range(6):
    label=('source',j,h,q,bit);assert label not in all_cache_labels;all_cache_labels.add(label)
    yy=1<<(2880+6*q+bit);injected=yy^cache[6*q+bit]
    assert injected>>(2880+6*q+bit)&1
  # Clearing the additional cache never overwrites an original Y owner.
 assert set(assigned)==set(range(480))and np.array_equal(A,np.vstack([assigned[x]for x in range(480)]))
 assert source_parity_count==360
 got,ops,binary,swaps=compile_matrix(A);assert got==expected['sources'][js]['early'];phase+=2*got['ADD_per_direction'];parity_add+=source_parity_add;parity_fields+=source_parity_count
 exp=expected['sources'][js];assert exp['actual_late_field_parities']==360 and exp['stationary_parity_bits']==2160 and exp['exact_parity_form_ADD']==source_parity_add and exp['actual_Y_injection_ADD']==2160
 key=lambda z:(z['H'],z['row']);assert sorted(actual_bindings,key=key)==sorted(exp['cache_bindings'],key=key)
 source_receipts.append({'source':j,'phase':got,'three_ADD_swaps':swaps,'parity_fields':360,'parity_form_ADDs':source_parity_add,'actual_Y_owner_bindings_checked':360})
 print('INDEPENDENT_NATIVE_SOURCE',j,got['ADD_per_direction'],source_parity_add,round(time.time()-started,2),flush=True)
assert parity_fields==1800 and len(Ytargets)==1800
for number,(hstr,z)in enumerate(sorted(hs.items(),key=lambda x:int(x[0]))):
 h=int(hstr);xs=HX[h];ys=HY[h];assert z['X_owners']==xs and z['Y_owners']==ys;nx=len(xs);ny=len(ys)
 E=mat(z['early']);B=mat(z['late'],(ny,ny));G=mat(z['cross'],(ny,nx));assert E.shape==(nx,nx)
 paid=h==642
 if paid:
  ph=old['H']['642']['physical'];assert ph['input_owners']==[[r[1],r[2]]for r in xs]and np.array_equal(E,mat(ph['word']))
  Extension=mat(ph['extension']);assert Extension.shape==(92,92)and np.array_equal(Extension[:90,:90],E)
  er,eo,eb,es=compile_matrix(Extension);initial=[1<<k for k in range(540)]+[0]*12;out=apply(initial,eo,True)
  assert out[:540]==lift(E)and out[540:]==lift(mat(ph['complements']))and apply(out,eo,False)==initial
  for bit in range(12):all_cache_labels.add(('H642-complement',bit))
 else:er,eo,eb,es=compile_matrix(E)
 br=bo=bb=None
 if ny:br,bo,bb,bs=compile_matrix(B)
 assert er==expected['H'][hstr]['early']and br==expected['H'][hstr]['late'];phase+=2*(er['ADD_per_direction']+(br['ADD_per_direction']if br else 0))
 has_cross=bool(np.any(G));Gbits=lift(G);weight=sum(v.bit_count()for v in Gbits);ncache=nx if has_cross else 0
 if has_cross:
  assert nx==45;H_cache_modules.append(h)
  for r in xs:
   for bit in range(6):
    label=('H',h,r[1],r[2],bit);assert label not in all_cache_labels;all_cache_labels.add(label)
 if not paid:
  X=[1<<k for k in range(6*nx)];Y=[1<<(6*nx+k)for k in range(6*ny)];saved=X.copy()if has_cross else []
  XX=apply(X,eo,True);YY=apply(Y,bo,True)if ny else[]
  for t,mask in enumerate(Gbits):
   while mask:
    low=mask&-mask;YY[t]^=saved[low.bit_length()-1];mask-=low
  block=np.zeros((nx+ny,nx+ny),dtype=np.uint8);block[:nx,:nx]=E;block[nx:,nx:]=B;block[nx:,:nx]=G
  assert XX+YY==lift(block)
 H_cache_fields+=ncache;H_cross_add+=weight;ex=expected['H'][hstr];assert ex['stationary_original_early_cache_bits']==6*ncache and ex['exact_late_cross_ADD']==weight and ex['paid_H642_extension']==paid
 assert ex['cache_bindings']==([[r[1],r[2]]for r in xs]if ncache else[])
 H_receipts.append({'H':h,'early':er,'late':br,'cache_fields':ncache,'cross_ADDs':weight,'actual_owners_and_all_input_bits_checked':True})
 if number%30==0:print('INDEPENDENT_NATIVE_H',number+1,len(hs),h,round(time.time()-started,2),flush=True)
assert len(hs)==136 and len(H_cache_modules)==22 and H_cache_fields==990
owners=sorted([r for r in routes if r[0]=='X'and r[4]==1509],key=orderkey)+sorted([r for r in routes if r[0]=='Y'and r[4]==1509],key=orderkey);assert owners==dw['owners']and len(owners)==35 and sum(r[0]=='X'for r in owners)==19
T=mat(dw['matrix']);assert T.shape==(35,35)and not np.any(T[:19,19:]);E=T[:19,:19];B=T[19:,19:];G=T[19:,:19]
er,eo,eb,_=compile_matrix(E);br,bo,bb,_=compile_matrix(B);gb=lift(G);cross=[]
for t,mask in enumerate(gb):
 for k in range(114):
  if mask>>k&1:cross.append([t,k])
dc=dw['compiler'];assert dc['early_elimination_ADDs']==[list(eo[k:k+2])for k in range(0,len(eo),2)]and dc['late_elimination_ADDs']==[list(bo[k:k+2])for k in range(0,len(bo),2)]and dc['late_cross_from_cache_ADDs']==cross
labels=[f'D1509-X-cache/{r[1]}/{r[2]}/{bit}'for r in owners[:19]for bit in range(6)];assert dc['cache_labels']==labels
X=[1<<k for k in range(114)];Y=[1<<(114+k)for k in range(96)];cache=X.copy();XX=apply(X,eo,True);YY=apply(Y,bo,True)
for t,k in cross:YY[t]^=cache[k]
assert XX+YY==lift(T)
for r in owners[:19]:
 for bit in range(6):all_cache_labels.add(('D',1509,r[1],r[2],bit))
assert(er['ADD_per_direction'],br['ADD_per_direction'],len(cross))==(6543,4721,4354)
Dadd=2*(er['ADD_per_direction']+br['ADD_per_direction'])+114+len(cross);assert Dadd==26996
assert dc['INIT']==dc['dirty_CLEAR']==dc['cache_copy_ADDs']==114 and dc['extra_MOVE']==0 and dc['forward_ADDs']==15732 and dc['including_pure_inverse_ADDs']==Dadd
base={'phase_forward_inverse_ADD':phase,'source_parity_cache_INIT':6*parity_fields,'source_parity_form_ADD':parity_add,'source_parity_inject_ADD':6*parity_fields,'source_parity_dirty_CLEAR':6*parity_fields,'H_early_cache_INIT':6*H_cache_fields,'H_early_cache_copy_ADD':6*H_cache_fields,'H_late_cross_ADD':H_cross_add,'H_early_cache_dirty_CLEAR':6*H_cache_fields};assert base==bill['base_counts']
ADD=8*(phase+parity_add+6*parity_fields+6*H_cache_fields+H_cross_add+Dadd);initial=8*(6*(parity_fields+H_cache_fields+19+2));assert ADD==313198856 and initial==134928 and len(all_cache_labels)==16866
assert bill['fullbank_ADD_including_phase_inverses']==ADD and bill['fullbank_INIT']==bill['fullbank_dirty_CLEAR']==initial and bill['fullbank_extra_field_exports']==16 and bill['fullbank_extra_MOVE_binary_records']==96 and bill['extra_MOVE_gap']==6
result={'status':'PASS_INDEPENDENT_NATIVE_D1509_COMPILER_AND_GROSS_BILL','source_phases':source_receipts,'H_phases':H_receipts,'H_cache_modules':H_cache_modules,'base_field_holders':{'source_parity':1800,'H_early':990,'D_early':19,'H642_complement':2},'distinct_base_holder_bits':len(all_cache_labels),'base_counts':base,'D_base_counts':{'early_ADD_per_direction':6543,'late_ADD_per_direction':4721,'copy_ADD':114,'cross_ADD':4354,'forward_ADD':15732,'including_pure_inverse_ADD':26996,'INIT':114,'dirty_CLEAR':114},'fullbank_ADD':ADD,'fullbank_INIT':initial,'fullbank_dirty_CLEAR':initial,'retained_gap6_field_exports':16,'retained_gap6_binary_MOVE':96,'every_source_H_D_phase_forward_and_pure_inverse_replayed':True,'all_chronological_cross_blocks_replayed_on_independent_early_late_inputs':True,'source_parity_rows_and_Y_bindings_reconstructed':True,'pure_phase_inverses_are_not_full_global_inverse':True,'whole_geometry_review_separate':True,'complete_global_supplier_invoice':False,'new_kappa':False,'input_sha256':{str(p.relative_to(BASE)):sha256(p.read_bytes()).hexdigest()for p in [routefile,PACKAGE/'PROOF.md',PACKAGE/'compile_prefix.py',PACKAGE/'output/SOURCES.json.gz',PACKAGE/'output/EARLY.json.gz',PACKAGE/'output/H-PHYSICAL.json.gz',PACKAGE/'output/D-WORD.json.gz',PACKAGE/'output/PHASE-COMPILER-RECEIPTS.json.gz',PACKAGE/'output/COMPILER-RESULT.json']}}
(HERE/'output').mkdir(exist_ok=True);(HERE/'output/RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],ADD,initial,16,round(time.time()-started,2),flush=True)
