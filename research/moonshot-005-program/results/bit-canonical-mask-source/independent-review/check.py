#!/usr/bin/env python3
"""Independent live-source, mask-reader, restoration and invoice audit."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import argparse, copy, hashlib, importlib.util, json

EARLY='509fe171db1fb0f82d9452c52e53166cae41da6f0c1700b10d8ef5db00ad28f2'
BASE='27dc6c36eec067acd2fe4679a81c95ea9db8fd6377784a0bbfc060ca52a121fd'
WORD='7d2fea44d7bdf8b3a63807f88371cad28f9303649db66b7d4ccbb56e9c180ada'
CASES=[('P3','ZFIRST3','X6','F4','Y4'),('P4','ZFIRST4','X75','F74','Y74'),('P5','ZFIRST5','X79','F78','Y78')]

def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def initial():
 return ({f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)},
         {f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)})
def step(v,at,o):
 op,n,*q=o
 if op=='INIT':v[n]=0;at[n]=q[0]
 elif op=='ADD':v[q[0]]^=v[n]
 elif op=='MOVE':at[n]=q[0]
 elif op=='CLEAR':del v[n],at[n]
 else:raise AssertionError(o)
def old_cuts(w):
 v,at=initial();cases={p:{'packet':p,'retained':z,'held':h,'facet':f,'receiver':y}for p,z,h,f,y in CASES};live=None
 for k,o in enumerate(w['operations']):
  if o[0]=='CLEAR'and live is None:live=(v.copy(),at.copy())
  for p,d in cases.items():
   if o[0]=='ADD'and o[2]==p and at[p]=='Hub'and 'source'not in d:d.update(source=k,source_values=v.copy(),source_charts=at.copy())
   if o==['ADD',p,d['retained']]:d.update(capture=k,old_retained_row=v[p]);assert at[p]=='M1'
   if o==['MOVE',p,d['facet']]:d['coupling']=k
  step(v,at,o)
  for p,d in cases.items():
   h=d['held']
   if 'coupling'in d and 'restoration'not in d and v[h]==1<<int(h[1:])and at[h]=='Hub':d.update(restoration=k,restore_values=v.copy(),restore_charts=at.copy())
 assert live is not None
 return cases,live
def xor(rows):
 z=0
 for r in rows:z^=r
 return z
def rank_intersection(e,left,right):return len(e.bb(left))+len(e.bb(right))-len(e.bb(left+right))

def main():
 p=argparse.ArgumentParser()
 for n in ['repo','early-word','base','word','author-result','engine','price-engine','out']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();assert sha(a.early_word)==EARLY and sha(a.base)==BASE and sha(a.word)==WORD
 early=json.loads(a.early_word.read_text());old=json.loads(a.base.read_text());w=json.loads(a.word.read_text())
 assert old['base_word_sha256']==EARLY and w['base_word_sha256']==BASE and old['targets']==w['targets']and w['charts']==old['charts']==early['charts']
 src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256']==old['source_sha256']==early['source_sha256'];R=json.loads(src)['native_roots']
 e=load(a.engine,'canonical_review_e');price=load(a.price_engine,'canonical_review_price')
 CE,HE,re=e.replay(early,R);C0,H0,r0=e.replay(old,R);C,H,r=e.replay(w,R)
 added={f'ADDED_RAW{i}'for i in [8,9,36,37,50]};assert [o for o in old['operations']if not any(n in added for n in o[1:])]==early['operations']
 assert set(old['targets'])==set(early['targets'])|{8,9,36,37,50}
 assert r0['movement_profile']=={**re['movement_profile'],1:re['movement_profile'][1]+5}
 cases,oldlive=old_cuts(old);before={};after={};records=[]
 claimed={d['packet']:d for d in w['canonical_retention_couplings']};assert set(claimed)==set(cases)
 canonical=[(1<<i)^sum(1<<j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0)for i in range(111)]
 cb=list(e.bb(canonical).values());assert len(cb)==9
 for P,d in cases.items():
  m=claimed[P];aux='CANON_AUX_'+P;h=d['held'];assert m['auxiliary']==aux and m['retained_field']==d['retained']and m['held_original']==h and m['coupling_chart']==d['facet']
  assert (m['source_old_index'],m['coupling_after_old_index'],m['restoration_after_old_index'])==(d['source'],d['coupling'],d['restoration'])
  donor=m['Hub_source_originals'];restore=m['Hub_restoration_originals'];assert len(set(donor))==len(donor)and len(set(restore))==len(restore)and h not in restore
  for names,v,at in [(donor,d['source_values'],d['source_charts']),(restore,d['restore_values'],d['restore_charts'])]:
   assert all(n.startswith('X')and at[n]=='Hub'and v[n]==1<<int(n[1:])for n in names)
  u=xor(d['source_values'][n]for n in donor);assert u and u==xor(d['restore_values'][n]for n in restore)==int(m['mask_row_hex'],16)
  c=d['old_retained_row']^u;assert c==int(m['canonical_row_hex'],16)and e.fits(cb,c)and d['old_retained_row']==int(m['old_retained_row_hex'],16)
  before[d['source']]=[(['INIT',aux,'Hub'],P,'source_birth')]+[(['ADD',n,aux],P,'source_read')for n in donor]+[(['MOVE',aux,d['facet']],P,'aux_move')]
  after[d['coupling']]=[(['ADD',aux,P],P,'packet_mask'),(['ADD',aux,h],P,'held_mask')]
  after[d['restoration']]=[(['ADD',n,h],P,'restore_read')for n in restore]
  d.update(mask=u,canonical=c,auxiliary=aux,source_donors=donor,restore_donors=restore)
  # Recompute feasible canonical rows from both actual old source cuts.
  srcrows=[v for n,v in d['source_values'].items()if n.startswith('X')and d['source_charts'][n]=='Hub']
  restrows=[v for n,v in d['restore_values'].items()if n.startswith('X')and n!=h and d['restore_charts'][n]=='Hub']
  choices=[]
  for bits in range(1,512):
   z=xor(cb[j]for j in range(9)if bits>>j&1)
   if e.fits(srcrows,z^d['old_retained_row'])and e.fits(restrows,z^d['old_retained_row']):choices.append(z)
  assert len(choices)==m['available_canonical_choices']
  records.append({'packet':P,'retained_field':d['retained'],'held_original':h,'receiver':d['receiver'],'auxiliary':aux,'coupling_chart':d['facet'],'old_row_hex':hex(d['old_retained_row']),'canonical_row_hex':hex(c),'mask_row_hex':hex(u),'source_donors':donor,'restoration_donors':restore,'source_old_index':d['source'],'capture_old_index':d['capture'],'coupling_after_old_index':d['coupling'],'restoration_after_old_index':d['restoration'],'actual_raw_Hub_source_count':sum(n.startswith('X')and d['source_charts'][n]=='Hub'and v==1<<int(n[1:])for n,v in d['source_values'].items()),'feasible_nonzero_canonical_choices':len(choices),'unfinished_support':[i for i in range(111)if i not in w['targets']and c>>i&1]})
 tagged=[]
 for k,o in enumerate(old['operations']):tagged+=before.get(k,[])+[(o,k,'old')]+after.get(k,[])
 tagged +=[(['CLEAR',d['auxiliary']],P,'aux_clear')for P,d in cases.items()]
 assert [o for o,_,_ in tagged]==w['operations']
 ov,oa=initial();v,at=initial();changed_reads=[];changed_states=[];newlive=None;joint=None;restore_seen=set();source_checks=[]
 permitted={n for P,d in cases.items()for n in [P,d['retained'],d['held'],d['receiver']]}
 for nk,(o,who,kind)in enumerate(tagged):
  if kind=='source_birth':
   d=cases[who];source_checks.append({'packet':who,'new_operation_index':nk,'actual_raw_donors':{n:hex(v[n])for n in d['source_donors']}})
   assert all(at[n]=='Hub'and v[n]==1<<int(n[1:])for n in d['source_donors'])
  if kind=='source_read':assert at[o[1]]==at[o[2]]=='Hub'and v[o[1]]==1<<int(o[1][1:])
  if kind in ['packet_mask','held_mask']:assert v[o[1]]==cases[who]['mask']and at[o[1]]==at[o[2]]==cases[who]['facet']
  if kind=='restore_read':
   d=cases[who];assert at[o[1]]==at[o[2]]=='Hub'and v[o[1]]==1<<int(o[1][1:])
   if who not in restore_seen:
    restore_seen.add(who);assert ov[d['held']]==1<<int(d['held'][1:])and v[d['held']]==ov[d['held']]^d['mask']
  if kind=='old':
   assert o==old['operations'][who]
   if o[0]=='CLEAR'and newlive is None:newlive=(v.copy(),at.copy())
   if o[0]=='ADD':
    n,t=o[1:];ds=v[n]^ov[n];dd=v[t]^ov[t]
    if ds:changed_reads.append({'old_operation_index':who,'new_operation_index':nk,'operation':o,'source_difference_hex':hex(ds),'destination_difference_before_hex':hex(dd),'destination_difference_after_hex':hex(dd^ds)})
   step(ov,oa,o)
  step(v,at,o)
  assert all(at[n]==oa[n]for n in ov)
  differences={n:hex(v[n]^z)for n,z in ov.items()if v[n]!=z};assert set(differences)<=permitted
  if kind=='old'and differences:changed_states.append({'old_operation_index':who,'differences':differences})
  if kind=='restore_read'and o[1]==cases[who]['restore_donors'][-1]:assert v[cases[who]['held']]==ov[cases[who]['held']]
  if kind=='old'and o==['ADD','ZFIRST5','P5']:
   joint={'after_new_operation_index':nk,'fields':{n:hex(z)for n,z in v.items()if not z>>111 and at[n]=='M1'},'packet_value_hex':hex(v['P5'])}
 assert newlive is not None and joint is not None and v==ov and at==oa
 expected_reads=[]
 for P,d in cases.items():
  for o in [['ADD',P,d['retained']],['ADD',d['retained'],P],['ADD',d['retained'],d['receiver']],['ADD',d['held'],d['receiver']]]:expected_reads.append((tuple(o),hex(d['mask'])))
 assert Counter((tuple(z['operation']),z['source_difference_hex'])for z in changed_reads)==Counter(expected_reads)
 for d in cases.values():
  rr=[z for z in changed_reads if z['operation'][2]==d['receiver']]
  assert len(rr)==2 and rr[0]['destination_difference_before_hex']=='0x0'and rr[0]['destination_difference_after_hex']==hex(d['mask'])and rr[1]['destination_difference_after_hex']=='0x0'
  reset=next(z for z in changed_reads if z['operation']==['ADD',d['retained'],d['packet']]);assert reset['destination_difference_after_hex']=='0x0'
  assert joint['fields'][d['retained']]==hex(d['canonical'])
 oldvalues,oldcharts=oldlive;newvalues,newcharts=newlive;changed={d['retained']for d in cases.values()}
 assert all(newvalues[n]==z and newcharts[n]==oldcharts[n]for n,z in oldvalues.items()if n not in changed)
 assert all(newvalues[d['retained']]==d['canonical']and newcharts[d['retained']]=='M1'for d in cases.values())
 inv=lambda values,charts:{n:z for n,z in values.items()if not z>>111 and charts[n]=='M1'}
 oldinv=inv(oldvalues,oldcharts);newinv=inv(newvalues,newcharts);assert rank_intersection(e,list(oldinv.values()),cb)==0 and rank_intersection(e,list(newinv.values()),cb)==3
 assert len(e.bb(d['canonical']for d in cases.values()))==3
 contracts={n:{'value_hex':hex(newvalues[n]),'chart':newcharts[n]}for n in old['protected_source_contracts']};assert contracts==old['protected_source_contracts']
 probe=copy.deepcopy(w);ix=next(k for k,o in enumerate(probe['operations'])if o==['ADD','ZFIRST5','P5'])+1
 probe['operations'][ix:ix]=[o for d in cases.values()for o in [['ADD',d['retained'],'P5'],['ADD',d['retained'],'P5']]];e.replay(probe,R)
 controls=[]
 for P,d in cases.items():
  for kind in ['aux_move','packet_mask','held_mask','source_read','restore_read','aux_clear']:
   j=next(k for k,(_,who,t)in enumerate(tagged)if who==P and t==kind);bad=copy.deepcopy(w);bad['operations']=[o for k,(o,_,_)in enumerate(tagged)if k!=j]
   try:e.replay(bad,R)
   except (AssertionError,KeyError)as ex:controls.append({'packet':P,'omitted_new_operation':tagged[j][0],'rejected':str(ex)})
   else:raise AssertionError(('accepted essential omission',P,kind))
  for mode in ['remove_both_masks_and_restoration','omit_matching_source_and_restoration_donor']:
   donor=d['source_donors'][0];assert donor in d['restore_donors'];skip=lambda o,who,t:who==P and ((t in ['packet_mask','held_mask','restore_read'])if mode.startswith('remove_both')else(t in ['source_read','restore_read']and o[1]==donor))
   bad=copy.deepcopy(w);bad['operations']=[o for o,who,t in tagged if not skip(o,who,t)];_,BH,_=e.replay(bad,R)
   value=next(z for _,n,_,z in reversed(BH)if n==d['retained']);assert not e.fits(cb,value)
   controls.append({'packet':P,'mutation':mode,'all46_endpoints_and_originals_still_pass':True,'retained_field_value_hex':hex(value),'claimed_canonical_source_contract_rejected':True})
 delta={k:r['movement_profile'].get(k,0)-r0['movement_profile'].get(k,0)for k in set(r['movement_profile'])|set(r0['movement_profile'])};delta={k:z for k,z in delta.items()if z};assert delta=={1:3}
 assert r['counts']=={'INIT':130,'ADD':1093,'MOVE':484,'CLEAR':130}and r['dirty_CLEAR']==130 and r['peak_owned']==130
 B={127:37,64:74,1:-74}
 for j in range(1,9):B[1+7*j]=B.get(1+7*j,0)+74;B[7*j]=B.get(7*j,0)-74
 Q=price.moment(r['movement_profile']);allowance=tuple(z/6 for z in price.moment(B));room=(allowance[0]-Q[1],allowance[1]-Q[0]);author=json.loads(a.author_result.read_text())
 for key,z in [('moment',Q),('limiting_room',room)]:assert Fraction(author['price'][key]['lower_fraction'])<=z[0]<=z[1]<=Fraction(author['price'][key]['upper_fraction'])
 xm=(1<<111)-1;targets=set(w['targets']);visible=[];own_nonzero=[];nonlocal_rows=[]
 for i in range(111):
  rows=[z&xm for _,_,c,z in H if e.sub(C[c],C[f'F{i}'])];visible.append(rows)
  if i in targets:continue
  leaks=[(st,n,c,hex(z&xm))for st,n,c,z in H if e.sub(C[c],C[f'F{i}'])and z>>i&1]
  if leaks:own_nonzero.append({'receiver':i,'rows':leaks})
  local={j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0};keep=xm^sum(1<<j for j in targets|local);qrank=len(e.bb(z&keep for z in rows))
  if qrank:nonlocal_rows.append({'receiver':i,'quotient_rank':qrank})
 def closure(extra):
  known=targets.copy();waves=[]
  while True:
   nxt={i for i,rows in enumerate(visible)if e.fits(rows+extra+[1<<j for j in known],1<<i)};assert known<=nxt
   if nxt==known:break
   waves.append(sorted(nxt-known));known=nxt
  duals=[{'receiver':i,'dual_hex':hex(price.outsider_dual(visible[i]+extra+[1<<j for j in known],i))}for i in range(111)if i not in known]
  return {'closure':sorted(known),'waves':waves,'remaining_duals':duals}
 frozen=closure([]);relaxed=closure([d['canonical']for d in cases.values()]);assert len(frozen['closure'])==46 and not own_nonzero and not nonlocal_rows
 out={'status':'PASS_INDEPENDENT_CANONICAL_M1_COUPLED_SOURCE_REVIEW','word_sha256':WORD,'base_word_sha256':BASE,'early_release_word_sha256':EARLY,'source_sha256':w['source_sha256'],'early_replay':re,'base_replay':r0,'replay':r,'early_paid_ancestry_all_old_operations_preserved_in_order':True,'exact_expected_insertions_match_entire_word':True,'canonical_code_rank':len(cb),'canonical_basis_hex':[hex(z)for z in cb],'couplings':records,'actual_new_source_cut_donor_checks':source_checks,'all_changed_inherited_source_reads':changed_reads,'every_other_inherited_ADD_source_unchanged':True,'changed_old_record_states':changed_states,'all_other_old_final_live_values_and_charts_identical':True,'actual_M1_inventory_before':{n:hex(z)for n,z in oldinv.items()},'actual_M1_inventory_after':{n:hex(z)for n,z in newinv.items()},'M1_rank_before':len(e.bb(oldinv.values())),'M1_rank_after':len(e.bb(newinv.values())),'canonical_intersection_before':0,'canonical_intersection_after':3,'joint_actual_M1_cut':joint,'joint_read_unread_probe_passes':True,'three_protected_raw_import_contracts':contracts,'negative_and_source_only_controls':controls,'movement_delta':delta,'price':{'moment':price.display(Q),'limiting_room':price.display(room)},'M1_visible_native_facets':[i for i in range(111)if e.sub(C['M1'],C[f'F{i}'])],'fresh_outsider_own_coordinate_nonzero_rows':own_nonzero,'fresh_outsider_history_mod_rawlocals_and_targets_nonzero_quotients':nonlocal_rows,'fresh_fixed_history_feedback':frozen,'diagnostic_if_three_canonical_rows_were_globally_granted':relaxed,'scope':'Actual three-dimensional canonical source at M1; all46 endpoints preserved. Old source-bank restrictions cannot be inherited. Fresh replay nevertheless leaves all65 outsiders with no visible own-coordinate history. The global-three-row diagnostic is only an information grant, not a delivery construction.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'status':out['status'],'replay':r,'M1_rank_before':out['M1_rank_before'],'M1_rank_after':out['M1_rank_after'],'canonical_intersection_after':3,'changed_inherited_source_read_count':len(changed_reads),'controls':len(controls),'price':out['price'],'fresh_closure_count':len(frozen['closure']),'global_three_rows_diagnostic_closure_count':len(relaxed['closure']),'global_three_rows_diagnostic_waves':relaxed['waves']}))
if __name__=='__main__':main()
