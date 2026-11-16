#!/usr/bin/env python3
"""Actual canonical K34 delivery and a paid stationary receiver correction."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
BASE='72317dffe82063e4db958c7b4025c490276d8339cbf11fd7041bc183ba991155'
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def scan(w):
 v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};before34=None;live=None;joint=None
 for k,o in enumerate(w['operations']):
  op,n,*q=o
  if o==['MOVE','Y34','F34']:before34=(k,v.copy(),at.copy())
  if op=='CLEAR'and live is None:live=(k,v.copy(),at.copy())
  if o==['MOVE','P5','P5_K']:joint=(k,v.copy(),at.copy())
  if op=='INIT':v[n]=0;at[n]=q[0]
  elif op=='ADD':v[q[0]]^=v[n]
  elif op=='MOVE':at[n]=q[0]
  elif op=='CLEAR':del v[n],at[n]
 return before34,live,joint
def main():
 p=argparse.ArgumentParser()
 for n in ['repo','base','engine','price-engine','out']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();blob=a.base.read_bytes();assert hashlib.sha256(blob).hexdigest()==BASE;old=json.loads(blob);src=(a.repo/old['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==old['source_sha256'];R=json.loads(src)['native_roots'];e=load(a.engine,'decoder34_e');price=load(a.price_engine,'decoder34_p');C0,H0,r0=e.replay(old,R)
 neighbours=[j for j in range(111)if sum(x*y for x,y in zip(R[34],R[j]))==0];N=sum(1<<j for j in neighbours);K=N^(1<<34);assert len(neighbours)==60
 rows=[int(d['canonical_row_hex'],16)for d in old['canonical_retention_couplings']];assert rows[0]^rows[1]^rows[2]==K
 s0,l0,j0=scan(old);assert all(s0[1][f'X{i}']==1<<i and s0[2][f'X{i}']=='Hub'for i in range(111));assert j0[1]['P5']==rows[2]
 for n,z in zip(['ZFIRST3','ZFIRST4','ZFIRST5'],rows):assert j0[1][n]==z and j0[2][n]=='M1'
 assert s0[1]['Y34']==1<<(111+34)and s0[2]['Y34']=='zero'
 aux='CANON_SIDE34';ops=[];new_indices={};introduced=[]
 for o in old['operations']:
  if o==['MOVE','P5','P5_K']:
   extra=[['ADD','ZFIRST3','P5'],['ADD','ZFIRST4','P5']];new_indices['M1_common_combination']=list(range(len(ops),len(ops)+len(extra)));ops+=extra;introduced+=extra
  if o==['MOVE','Y34','F34']:
   extra=[['INIT',aux,'Hub']]+[['ADD',f'X{j}',aux]for j in neighbours]+[['MOVE',aux,'F34'],['ADD','P5','Y34']];new_indices['source_and_common_read']=list(range(len(ops),len(ops)+len(extra)));ops+=extra;introduced+=extra
   ops.append(o);new_indices['facet_correction_read']=[len(ops)];ops.append(['ADD',aux,'Y34']);introduced.append(['ADD',aux,'Y34'])
  else:ops.append(o)
 new_indices['clear']=[len(ops)];ops.append(['CLEAR',aux]);introduced.append(['CLEAR',aux])
 w=copy.deepcopy(old);w.update(operations=ops,targets=sorted(old['targets']+[34]),schema='actual-canonical-K34-common-and-paid-facet-correction-v1',base_word_sha256=BASE,
  canonical_decoder34={'common_packet':'P5','common_row_hex':hex(K),'source_fields':['ZFIRST3','ZFIRST4','ZFIRST5'],'correction_field':aux,'correction_chart':'F34','correction_row_hex':hex(N),'actual_Hub_raw_donors':neighbours,'movement_increment':'1[1]'},
  scope='Actual47 endpoints with K34 carried to common by P5 and a paid Hub-to-F34 neighbour-sum correction. Retains three canonical M1 fields and three raw M1 imports. A source/delivery mechanism witness, not a cheaper endpoint frontier than raw point returns or a full supplier.')
 C,H,r=e.replay(w,R);s,l,j=scan(w);assert j[1]['P5']==K and j[2]['P5']=='M1'and s[1]['P5']==K and s[2]['P5']=='zero'and s[1][aux]==N and s[2][aux]=='F34'
 ov,oa=l0[1:];nv,na=l[1:];changed={n for n in ov if ov[n]!=nv[n]or oa[n]!=na[n]};assert changed=={'P5','P5_RET','Y34'}
 for n,z in zip(['ZFIRST3','ZFIRST4','ZFIRST5'],rows):assert nv[n]==z and na[n]=='M1'
 contracts={n:{'value_hex':hex(nv[n]),'chart':na[n]}for n in old['protected_source_contracts']};assert contracts==old['protected_source_contracts']
 profile=r0['movement_profile'].copy();profile[1]+=1;assert r['movement_profile']==profile
 assert r['counts']=={k:z+{'INIT':1,'ADD':64,'MOVE':1,'CLEAR':1}[k]for k,z in r0['counts'].items()}and r['dirty_CLEAR']==r0['dirty_CLEAR']+1
 controls=[]
 for badop in [['ADD','ZFIRST3','P5'],['ADD','ZFIRST4','P5'],['ADD',f'X{neighbours[0]}',aux],['MOVE',aux,'F34'],['ADD','P5','Y34'],['ADD',aux,'Y34'],['CLEAR',aux]]:
  bad=copy.deepcopy(w);bad['operations'].remove(badop)
  try:e.replay(bad,R)
  except(AssertionError,KeyError)as ex:controls.append({'omitted':badop,'rejected':str(ex)})
  else:raise AssertionError(('accepted omission',badop))
 # Taking only the new receiver reads away keeps all46 old endpoints valid.
 bad=copy.deepcopy(w);bad['targets']=old['targets'];bad['operations'].remove(['ADD','P5','Y34']);bad['operations'].remove(['ADD',aux,'Y34']);e.replay(bad,R)
 controls.append({'removed':'both new receiver reads and point34 target','all46_old_endpoints_still_pass':True})
 Q=price.moment(profile);B={127:37,64:74,1:-74}
 for q in range(1,9):B[1+7*q]=B.get(1+7*q,0)+74;B[7*q]=B.get(7*q,0)-74
 lim=tuple(z/6 for z in price.moment(B));room=(lim[0]-Q[1],lim[1]-Q[0])
 a.out.mkdir(parents=True,exist_ok=True);raw=(json.dumps(w,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(raw)
 out={'status':'PASS_ACTUAL_CANONICAL_DECODER34_WITH_PAID_FACET_CORRECTION','word_sha256':hashlib.sha256(raw).hexdigest(),'base_word_sha256':BASE,'source_sha256':old['source_sha256'],'before':r0,'after':r,'target_count':len(w['targets']),'new_target':34,'canonical_row_equals_K34':True,'K34_hex':hex(K),'N34_hex':hex(N),'neighbours':neighbours,'actual_Hub_source_cut_all111_raw':True,'actual_M1_combination_cut':{'old_operation_index':j0[0],'actual_fields':{n:hex(j0[1][n])for n in ['ZFIRST3','ZFIRST4','ZFIRST5']},'packet_value_after_combination_hex':hex(j[1]['P5'])},'actual_receiver_cut':{'new_MOVE_Y34_index':s[0],'common_packet_row_hex':hex(s[1]['P5']),'facet_correction_row_hex':hex(s[1][aux]),'Y34_before_move_hex':hex(s[1]['Y34'])},'old_final_live_fields_changed':sorted(changed),'all_other_old_final_live_values_and_charts_preserved':True,'protected_raw_M1_contracts':contracts,'canonical_M1_rows_unchanged':True,'introduced_operations':introduced,'new_operation_indices_by_role':new_indices,'exact_movement_increment':'1[1]','price':{'moment':price.display(Q),'limiting_room':price.display(room)},'controls':controls,'scope':w['scope']}
 (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['status','word_sha256','after','target_count','price']}))
if __name__=='__main__':main()
