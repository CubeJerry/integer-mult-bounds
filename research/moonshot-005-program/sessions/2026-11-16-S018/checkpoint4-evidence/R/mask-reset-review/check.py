#!/usr/bin/env python3
"""Independent literal unknown-mask source/reset and released-carrier review."""
import argparse,copy,hashlib,json,sys
from fractions import Fraction
from pathlib import Path
p=argparse.ArgumentParser()
for n in ['repo','work','out']:p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args();P=a.repo/'research/moonshot-005-program';sys.path.insert(0,str(P/'sessions/2026-11-16-S018/root-review'))
from optimize_word import independent_replay
from review_source_families import trace
from review_leaf_capacity import chart_basis,echelon
from price import invoice
paths={'base':'A/m0-masked19-pure-pruned55/WORD.json','pair55':'C/m0-pair55/WORD.json',**{k:'C/mask-preserving-reset/'+n+'.json'for k,n in [('old','OLD-WORD'),('reset','RESET-WORD'),('source','SOURCE-WORD'),('liberated','LIBERATED-SOURCE-WORD'),('unprepared','UNPREPARED-WORD')]}}
raw={k:(a.work/v).read_bytes()for k,v in paths.items()};ws={k:json.loads(v)for k,v in raw.items()};b=ws['base'];new=ws['reset'];old=ws['old'];lib=ws['liberated']
pins={'base':'fd9ce4903aab198d234e6956a877e97241ed7268c7dba657064fa8ebf8cba84c','pair55':'12ccd57ba43a8d4902c04724c70489a348266690d20ce2269ff68eec34b4835e','old':'223382855493515b08f71a4288745ffc6842ea6d056da0545f425b1d5b86424b','reset':'637709a135ee93a2c8e60ca2e095495bfd784506b5a241466d4d0b8671f30cbf','source':'5d291862ad2dba74e5f4dd7e3d432ab69d54febde9934209ecf3d46986a442c7','liberated':'4fe64237569a99a41578a378145a7df7ceac8394d33c82ca4f5e1be166b8859c','unprepared':'d9f980ce5d215e2da5df788c65facad651b6b1824e18da47a2e9d822eabd46cb'}
assert{n:hashlib.sha256(v).hexdigest()for n,v in raw.items()}==pins
src=(a.repo/b['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==b['source_sha256']=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';roots=json.loads(src)['native_roots'];charts={n:chart_basis(v)for n,v in b['charts'].items()}
for i,r in enumerate(roots):
 assert len(charts[f'L{i}'])==1 and len(echelon(charts[f'L{i}']+[r])[0])==1
 assert len(charts[f'F{i}'])==7 and all(sum(x*y for x,y in zip(v,r))==0 for v in charts[f'F{i}'])
for k,w in ws.items():
 assert w['source_sha256']==b['source_sha256']and w['targets']==b['targets']
 if k!='pair55':assert w['charts']==b['charts']
stats={k:independent_replay(w)for k,w in ws.items()if k!='unprepared'};tr={k:trace(w)for k,w in ws.items()if k!='pair55'}
N=111;xm=(1<<N)-1;originals={f'{p}{i}'for p in 'XY'for i in range(N)};S=set(b['targets'])|{61,67};sm=sum(1<<i for i in S);assert len(S)==57
parts=[[31,57,58,82,87,97,105],[13,33,59,83,96,109],[14,52,60,86,100,101]];U=set(i for part in parts for i in part);assert len(U)==19 and not S&U;masks=[sum(1<<i for i in part)for part in parts]
bc=b['masked_feedback']['continuation_before_operation'];nc=new['mask_reset']['continuation_before_operation'];lc=lib['carrier_interface_before_operation'];assert(bc,nc,lc)==(950,519,350)
bv,ba=tr['base'][0][bc];nv,na=tr['reset'][0][nc];lv,la=tr['liberated'][0][lc];owners=set(bv)-originals;assert len(owners)==133
for n in bv:
 assert charts[ba[n]]==charts[na[n]]and(bv[n]^nv[n])>>N==0 and(bv[n]^nv[n])&xm&~sm==0
for i in S:
 n=f'MASK_RESET_RAW_{i}';assert nv[n]==lv[n]==1<<i and na[n]==la[n]=='zero'
 for w in [new,lib]:
  for op in [['INIT',n,f'L{i}'],['ADD',f'X{i}',n],['MOVE',n,'zero'],['CLEAR',n]]:assert w['operations'].count(op)==1
fields=['KEEP_C0','KEEP_C1','KEEP_C2'];common=b['masked_feedback']['common'];assert len(charts[common])==4
for j,mask in enumerate(masks):
 loc=f'MASK_CORRECTION_{j}';own=f'MASK_SOURCE_{j}';assert len(charts[loc])==6
 for name,at in [(own,loc),(fields[j],common)]:assert nv[name]==lv[name]==mask and na[name]==la[name]==at
 for i in parts[j]:
  for w in [new,lib]:
   for op in [['MOVE',f'X{i}',loc],['ADD',f'X{i}',own],['MOVE',f'X{i}','Hub']]:assert w['operations'].count(op)==1
 for op in [['INIT',fields[j],loc],['ADD',own,fields[j]],['MOVE',fields[j],common]]:assert lib['operations'].count(op)==1
free=set(range(N))-U;assert len(free)==92
for i in range(N):assert lv[f'X{i}']==1<<i and la[f'X{i}']==(f'L{i}'if i in free else'Hub')
for i in range(N):assert lv[f'Y{i}']==(1<<(N+i))^((1<<i)if i in b['targets']else 0)and la[f'Y{i}']==(f'F{i}'if i in b['targets']else'zero')
def brank(vals):
 piv={}
 for row in vals:
  while row:
   j=row.bit_length()-1
   if j in piv:row^=piv[j]
   else:piv[j]=row;break
 return len(piv)
live=set(lv)-originals;assert len(live)==63 and brank(lv[n]for n in live)==60 and all(lv[n]>>N==0 for n in live)
assert set(lib['source_interface']['omitted_unused_zero_owners'])=={n for n in owners if nv[n]==0}and len(lib['source_interface']['omitted_unused_zero_owners'])==127
assert stats['liberated']['counts']=={'INIT':63,'ADD':134,'MOVE':301,'CLEAR':63}and stats['liberated']['dirty_CLEAR']==63
assert stats['liberated']['movement_profile']=={1:57,2:22,5:19,7:203}
assert stats['source']['movement_profile']==stats['liberated']['movement_profile']
F=old['operations'][bc:];length=len(F);assert length==244 and new['operations'][nc:nc+length]==F
assert old['operations'][:bc]==b['operations'][:bc]
assert tr['old'][0][bc+2][0]['X7']==(1<<7)^(1<<34)^masks[0]
M=[(1<<i)^((1<<34)if i==7 else 0)for i in range(N)]
ufinal=tr['unprepared'][1][0];assert[ufinal[f'X{i}']for i in range(N)]==M
corrections=[ufinal[f'Y{i}']^(1<<(N+i))^((1<<i)if i in b['targets']else 0)for i in range(N)];assert all(z&~sm==0 for z in corrections)
ps,pe=new['mask_reset']['preload_range'];assert pe-ps==55
before_inverse,at_inverse=tr['reset'][0][nc+length];assert[before_inverse[f'X{i}']for i in range(N)]==M and all(at_inverse[f'X{i}']=='Hub'for i in range(N))
assert new['operations'][nc+length]==['ADD','X34','X7']
controls=[]
for op in [['ADD','MASK_SOURCE_0','KEEP_C0'],['ADD','X34','MASK_RESET_RAW_34']]:
 bad=copy.deepcopy(new);bad['operations'].remove(op)
 try:independent_replay(bad)
 except(AssertionError,KeyError):controls.append({'omitted':op,'rejected':True})
 else:raise AssertionError('omission survived')
bad=copy.deepcopy(new);del bad['operations'][nc+length]
try:independent_replay(bad)
except AssertionError:controls.append({'omitted':'actual final Hub inverse','rejected':True})
else:raise AssertionError('inverse omitted')
bad=copy.deepcopy(new);bad['operations'].remove(['ADD','X31','MASK_SOURCE_0']);independent_replay(bad)
lost,_=trace(bad)[0][nc-1];assert lost['KEEP_C0']^nv['KEEP_C0']==1<<31 and lost['MASK_SOURCE_0']^nv['MASK_SOURCE_0']==1<<31
controls.append({'mutation':'omit unknown source X31 from both proper copies','all_endpoints_still_pass':True,'actual_cut_source_rejects':True})
bad=copy.deepcopy(lib);op=['MOVE','X7','Hub'];ix=bad['operations'].index(op);assert ix>=lc;bad['operations'].pop(ix);bad['operations'].insert(lc-1,op);independent_replay(bad)
_,early=trace(bad)[0][lc+1];assert early['X7']=='Hub'
controls.append({'mutation':'postponed X7 closure performed before source cut','all_endpoints_still_pass':True,'92_native_contract_rejects':True})
prices={k:invoice(stats[k]['movement_profile'])for k in ['base','source','liberated','reset']}
author=json.loads((a.work/'C/mask-preserving-reset/RESULT.json').read_text())
for key,who in [('source_moment','source'),('nontrivial_control_moment','reset')]:
 lo,hi=map(Fraction,author[key]['rational']);pr=prices[who]['moment'];assert lo<=Fraction(pr['lower_fraction'])<=Fraction(pr['upper_fraction'])<=hi
r={'status':'PASS_ROOT_ACTUAL_MASK_PRESERVING_RESET_AND_LIBERATED_SOURCE','proof_sha256':hashlib.sha256((a.work/'C/MASK-PRESERVING-RESET.md').read_bytes()).hexdigest(),'word_hashes':pins,'stats':stats,'known_ground_sources':57,'unknown_source_inputs':19,'unknown_independent_modes':3,'total_owned_rank':60,'liberated_native_originals':92,'remaining_raw_ground_Y':56,'old_cut':bc,'reset_cut':nc,'liberated_cut':lc,'same_cut_Y_and_all_unknown_X_columns':True,'actual_known_preloads':55,'literal_continuation_length':length,'actual_final_Hub_inverse':[['ADD','X34','X7']],'source_price_identity':'222[7]+57+19([5]+[2]-[7])+3[2]','prices':prices,'controls':controls,'scope':'Independent retained root native/geometry/full222 engine; no C/A execution code imported. Same-interface reset and liberated distinct contract separately checked. Universal linear identities do not discharge global foundations; no complete supplier or kappa.'}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
