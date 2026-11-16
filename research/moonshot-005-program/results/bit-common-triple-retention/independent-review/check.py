#!/usr/bin/env python3
"""Independent full-column review of the source-aware41-output clique chain."""
from pathlib import Path
from fractions import Fraction
import argparse,copy,hashlib,importlib.util,json
PINS={
 'reprogram36':'af51d0d7c872dbf3fa3744b582769d4c7763e0747e57c74005d091d19b7da474',
 'common38':'b30cca73a0aafcc98dd98440ba2597119bf79401751f2fc5022dcbd1c22b1059',
 'common39':'c7c8eb65cdc69d01d61cb82949ad85ff4de675606462ae7d3ce772fc885eb757',
 'clique39':'0ce7ccb671300c1af9548f091e972e81feb09f7f8d8cf115d0e46b3bb0762bc2',
 'clique41':'07ed37cf9dfa1da24d3518e25e46d7b29141582f71f32da1191f13fbc9b1971f'}
SOURCE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--stages',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--price-engine',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();e=load(a.engine,'independent_geometry');price=load(a.price_engine,'independent_prices');stages=[];parent=None;words={};runs={};cuts={}
 for name,pin in PINS.items():
  path=a.stages/name/'WORD.json';assert sha(path)==pin;w=json.loads(path.read_text());assert w['source_sha256']==SOURCE
  if parent:assert w['base_word_sha256']==parent
  src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==SOURCE;R=json.loads(src)['native_roots'];C,H,report=e.replay(w,R);cut,events=price.cut(w)
  words[name]=w;runs[name]=(C,H,report);cuts[name]=cut;stages.append({'stage':name,'word_sha256':pin,'parent_sha256':w['base_word_sha256'],'targets':len(w['targets']),'independent_replay':report});parent=pin
 w=words['clique41'];old=words['clique39'];C,H,report=runs['clique41'];v,at=cuts['clique41']['seed'];ov,oa=cuts['clique39']['seed']
 assert len(w['targets'])==41 and set(w['targets'])-set(old['targets'])=={40,49} and set(old['targets'])<=set(w['targets'])
 assert report['counts']=={'INIT':129,'ADD':948,'MOVE':460,'CLEAR':129} and report['dirty_CLEAR']==129
 triples=[[29,40,42],[41,43,46],[45,48,49]];dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));assert all(dot(i,j)==0 for T in triples for i in T for j in T if i!=j)
 assert v['P4']^v['E75']==sum(1<<i for i in triples[0])
 assert v['P3']^v['E6']==sum(1<<i for i in triples[1])
 assert v['P5']^v['E79']^v['ZRAW0']^v['ZRAW44']==sum(1<<i for i in triples[2])
 masks={'P4_RET':[29,42],'P5_RET':[0,44,45,48],'RAW40':[40],'RAW49':[49],'P4_RAW29':[29],'P4_RAW42':[42],'P5_RAW45':[45],'P5_RAW48':[48],'CAP2942':[29,42],'CAP46':[43,46]}
 for field,roles in masks.items():assert v[field]==sum(1<<i for i in roles),(field,hex(v[field]))
 assert 'ZCORR2'not in v and not any('ZCORR2'in o for o in w['operations'])
 assert not any(o==['MOVE','X29','Jnew2']for o in w['operations'])
 assert ['MOVE','Y2','L29']in w['operations']and ['ADD','RAW29','Y2']in w['operations']
 assert e.sub(C['L29'],C['Jnew2']) and e.sub(C['Jnew2'],C['F2'])
 assert not e.sub(C['Jnew2'],C['P4_A']) and not e.sub(C['P4_A'],C['Jnew2'])
 proper=[]
 for name,receiver in [('P4_K',42),('P4_A',40),('P4_B',29),('P5_K',48),('P5_A',49),('P5_B',45),('K46_PAIR',46),('J41_PAIR',41),('J43_PAIR',43)]:
  assert e.sub(C[name],C[f'F{receiver}']) and e.sub(C[name],C['M1']);proper.append({'chart':name,'rank':len(C[name]),'receiver':receiver,'source_chart':'M1'})
 ground=[z for n,z in v.items()if at[n]=='zero'and z>>111==0];assert len(e.bb(ground))==17
 delta={1:17,2:-1,3:5,4:-3,5:4,6:-4,7:-2};expected=runs['clique39'][2]['movement_profile'].copy()
 for d,n in delta.items():expected[d]+=n
 assert report['movement_profile']==expected
 assert sum(d*n for d,n in delta.items())==0
 Q=price.moment(report['movement_profile']);B={127:37,64:74,1:-74}
 for j in range(1,9):B[1+7*j]=B.get(1+7*j,0)+74;B[7*j]=B.get(7*j,0)-74
 allowance=tuple(x/6 for x in price.moment(B));room=(allowance[0]-Q[1],allowance[1]-Q[0]);ap=json.loads((a.stages/'clique41/PRICE.json').read_text())
 for tag,interval in [('moment',Q),('limiting_allowance',allowance),('limiting_room',room)]:assert interval[0]<=Fraction(ap[tag]['lower_fraction'])<=Fraction(ap[tag]['upper_fraction'])<=interval[1],tag
 assert room[0]>0 and room[1]<1
 cert=json.loads((a.stages/'clique41/CLOSURE.json').read_text());assert cert['word_sha256']==PINS['clique41'];assert set(cert['optimistic_closure'])==set(w['targets']);assert len(cert['outsider_duals'])==70 and {d['receiver']for d in cert['outsider_duals']}==set(range(111))-set(w['targets'])
 duals=[];xmask=(1<<111)-1
 for d in cert['outsider_duals']:
  i=d['receiver'];z=int(d['dual_hex'],16);assert z>>i&1 and not z>>111
  rows=[value&xmask for _,_,ch,value in H if e.sub(C[ch],C[f'F{i}'])]+[1<<j for j in range(111)if dot(i,j)==0]+[1<<j for j in w['targets']]
  assert all((x&z).bit_count()%2==0 for x in rows),(i,'all-history dual')
  duals.append({'receiver':i,'dual_hex':hex(z),'checked_measurements':len(rows)})
 tests=[['ADD','X40','RAW40'],['ADD','X49','RAW49'],['ADD','RAW40','P4'],['ADD','RAW49','P5'],['ADD','P4','P4_RET'],['ADD','P5','P5_RET'],['MOVE','Y2','L29'],['ADD','RAW29','Y2'],['ADD','X29','P4_RAW29'],['ADD','X42','P4_RAW42'],['ADD','X45','P5_RAW45'],['ADD','X48','P5_RAW48'],['ADD','P4_RET','Y42'],['ADD','P5_RET','Y48'],['ADD','P4_RAW29','Y40'],['ADD','P5_RAW45','Y49'],['MOVE','Y29','P4_B'],['MOVE','Y45','P5_B'],['CLEAR','P5_RET']];rejected=[]
 for op in tests:
  bad=copy.deepcopy(w);bad['operations'].remove(op)
  try:e.replay(bad,R)
  except (AssertionError,KeyError)as ex:rejected.append({'removed':op,'failure':str(ex)})
  else:raise AssertionError(('accepted omission',op))
 # Restore the obsolete source stop: it is incomparable with the new pair chart.
 bad=copy.deepcopy(w);ix=bad['operations'].index(['MOVE','X29','P4_A']);bad['operations'].insert(ix,['MOVE','X29','Jnew2'])
 try:e.replay(bad,R)
 except AssertionError as ex:rejected.append({'inserted':['MOVE','X29','Jnew2'],'before':['MOVE','X29','P4_A'],'failure':str(ex)})
 else:raise AssertionError('accepted incomparable source itinerary')
 out={'status':'PASS_INDEPENDENT_ACTUAL41_CHAIN_AND_PRICE','word_sha256':PINS['clique41'],'native_source_sha256':SOURCE,'dependency_hashes':{'geometry_engine':sha(a.engine),'price_engine':sha(a.price_engine)},'all_stages_independently_replayed':stages,'common_rank':17,'common_codes':triples,'partial_rows':{n:hex(v[n])for n in masks},'new_chart_inclusions':proper,'old_Y2_raw29_repair_verified':True,'incomparable_old_X29_itinerary_excluded':True,'signed_movement_profile_difference_from39':delta,'zero_linear_rank_volume_increment':True,'independent_price':{'method':'Exact integer200th roots at scale10^32, independently recomputed fractions','moment':price.display(Q),'limiting_allowance':price.display(allowance),'limiting_room':price.display(room),'increment_from39':price.display(price.moment(delta))},'author_price_intervals_contained':True,'independently_checked_all_history_closure_duals':duals,'frozen_closure_scope':'All record histories (including original-Y X-parts), raw geometric locals and free decoded-point feedback close at41.','semantic_controls_without_invoice_metadata_or_milestones':rejected,'scope':'Exact formal source/decoder identities over all characteristic-two fields and record widths; complete111 source, ordinary and recursive supplier costs and all five foundations remain open. No new kappa.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'counts':report['counts'],'history_states':len(H),'common_rank':17,'Q':price.display(Q),'room':price.display(room),'closure_duals':len(duals),'controls':len(rejected)}))
if __name__=='__main__':main()
