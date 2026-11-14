#!/usr/bin/env python3
"""Actual canonical pivot: complete one target and retain its useful recoded global mode."""
import argparse,gzip,hashlib,json,runpy
from pathlib import Path
BASE_PIN='244bedc78693645fdd70ed4540689e7d047e0a6eb260c3d40403ac691d43b7e8'
REPLAY_PIN='f99bfc2896163e373224a4ce86608bf0452f49f0367db5d006aeca03a4180cbe'
def xor(rows):
 v=0
 for r in rows:v^=r
 return v
def main(a):
 need=lambda b,m:None if b else (_ for _ in ()).throw(ValueError(m))
 need(hashlib.sha256(a.geometry.read_bytes()).hexdigest()==BASE_PIN,'geometry pin');need(hashlib.sha256(a.replayer.read_bytes()).hexdigest()==REPLAY_PIN,'separate replayer pin')
 m=runpy.run_path(str(a.geometry));replay=runpy.run_path(str(a.replayer))['replay'];raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==m['PIN'],'native pin')
 n=json.loads(gzip.decompress(raw));c=m['analyse'](n);K=c['K'];i=0;Ki=K[i];Li=Ki^(1<<i);inds=[0,1,2,4,8,9,14,30,59];G=[K[j]for j in inds]
 coeff={xor(G[j]for j in range(9)if(mask>>j)&1):mask for mask in range(512)};need(len(coeff)==512 and set(K)<=set(coeff),'native canonical basis')
 H=[g^(((g>>i)&1)*Ki)for g in G[1:]];need(m['rank'](H)==8 and all(((h>>i)&1)==0 for h in H),'actual column-zero complement')
 B=[Li,*H[:2]];A=[((k>>i)&1)|((coeff[k]>>1&1)<<1)|((coeff[k]>>2&1)<<2)for k in K];R=[xor(b for t,b in enumerate(B)if(mask>>t)&1)for mask in A]
 residual=[k^(((k>>i)&1)<<i)for k in K]
 for j,k in enumerate(K):
  need(residual[j]==(((k>>i)&1)*Li)^xor(h for t,h in enumerate(H,1)if(coeff[k]>>t)&1),'exact global residual code')
  if j!=i:need((residual[j]>>j)&1 and residual[j]&~K[j]==0,'remaining receiver fitting')
 need(m['rank']([residual[j]for j in range(111)if j!=i])==9,'residual code rank9')
 need(m['rank'](H+[Ki,Li])==10,'extra actual history direction')
 s=m['Source'](n);Fi=n['final'][111+i];Yi=111+i;events={};meta={};points=[]
 for j in range(111):s.init(222+j,s.where[j]);points.append(s.add(222+j,j,s.where[j]))
 s.init(334,s.zero);cache_y=s.add(334,Yi,s.zero)
 precode=[]
 for j in range(111):
  if j!=i and(K[j]>>i)&1:precode.append(s.add(111+j,Yi,s.zero))
 s.move(Yi,Fi);local_reads=[];captures=[]
 for j in range(111):
  if(Li>>j)&1:
   s.move(j,Fi);local_reads.append(s.add(Yi,j,Fi));captures.append(j)
  s.move(j,s.hub)
 events['all_originals_Hub_Yi_has_local_form']=len(s.ops)-1
 s.init(333,s.hub);encoder=[]
 for j in range(111):
  if(Ki>>j)&1:encoder.append(s.add(333,j,s.hub))
 s.move(333,Fi);finish=s.add(Yi,333,Fi);feedback=s.add(333,Yi,Fi);events['pivot_completed_history_recoded']=len(s.ops)-1
 s.move(333,s.zero);deposits=[]
 for j in range(111):
  if j!=i and(K[j]>>i)&1:deposits.append(s.add(111+j,333,s.zero))
 purification=s.add(333,334,s.zero);s.clear(334);events['actual_Li_core_ready']=len(s.ops)-1
 other=[]
 for t,(packet,cache)in enumerate(((335,336),(337,338)),start=1):
  s.init(packet,s.hub);reads=[]
  for j in range(111):
   if(B[t]>>j)&1:reads.append(s.add(packet,j,s.hub))
  s.move(packet,s.zero);s.init(cache,s.zero);copy=s.add(cache,packet,s.zero);ds=[]
  for j,mask in enumerate(A):
   if j!=i and(mask>>t)&1:ds.append(s.add(111+j,packet,s.zero))
  s.clear(packet);other.append({'packet':packet,'cache':cache,'encoder':reads,'copy':copy,'deposits':ds})
 events['pivot_three_mode_prefix_complete']=len(s.ops)-1
 live=list(range(222,333))+[333,336,338]
 def word(scope):
  w=s.word(live,scope);w['schema']='BIT-native-canonical-pivot-core-v1';w['owned_fields']=117;w['directions']={str(p):'down'for p in(333,335,337)};return w
 pre=word('Actual nonterminal canonical pivot prefix: target0 completed, useful Li+2H ground core, six canonical complementary modes remain. No complete decoder.')
 for j in range(111):s.move(111+j,n['final'][111+j])
 for p in live:s.clear(p)
 close=word('Closed partial map only: X restored, Y0 correct, other110 Y have actual residual-code core preloads. No complete supplier.');close['end_owned']=[]
 pr=replay(pre,m);cr=replay(close,m);want=[1<<j for j in range(222)]
 for j,r in enumerate(R):want[111+j]^=(1<<j)if j==i else r
 need(pr['rows']==cr['rows']==want,'all222 independent input columns')
 need(pre['final'][:111]==n['final'][:111] and close['final']==n['final'][:222],'native actual endpoints')
 need(all(pre['final'][111+j]==(Fi if j==i else s.zero)for j in range(111)),'exact partial public locations')
 expect={str(222+j):hex(1<<j)for j in range(111)}|{str(p):hex(b)for p,b in zip((333,336,338),B)}
 need(pr['owned_rows']==expect,'every retained point and pure core row')
 need(pr['owned_where']==({str(222+j):n['start'][j]for j in range(111)}|{str(p):s.zero for p in(333,336,338)}),'every retained physical location')
 need(pr['paid_profile']=={1:808}and cr['paid_profile']=={1:1578},'literal rank length')
 need(pr['owned_lifetimes']==117 and pr['peak_owned']==115,'exact lifetime/peak count')
 need(pr['counts']=={'INIT':117,'ADD':575,'MOVE':808,'CLEAR':3}and cr['counts']=={'INIT':117,'ADD':575,'MOVE':1578,'CLEAR':117},'complete ordinary invoices')
 controls=[]
 for name,k in [('original_y_cache',cache_y),('ground_y_precode',precode[0]),('local_original_read',local_reads[0]),('Hub_encoder',encoder[0]),('pivot_completion',finish),('completed_Y_feedback',feedback),('dirty_history_deposit',deposits[0]),('ground_history_purification',purification),('retained_point',points[0]),('second_core_copy',other[0]['copy'])]:
  bad=json.loads(json.dumps(pre));del bad['program'][k]
  try:rr=replay(bad,m);rejected=rr['rows']!=want or rr['owned_rows']!=expect
  except ValueError:rejected=True
  need(rejected,'mutation missed '+name);controls.append(name)
 S=[4,8,9,14,30,73];roots=[m['rref'](n['frames'][str(n['start'][j])]['B'])[0]for j in range(111)]
 def inside(chart):return any(all(m['dot'](roots[j],v)==0 for v in m['rref'](pre['frames'][chart]['B']))for j in S)
 obs=[r for j,r in enumerate(pr['rows'])if inside(pre['final'][j])]+[int(r,16)for p,r in pr['owned_rows'].items()if inside(pr['owned_where'][p])];r0=m['rank'](obs);r1=m['rank'](obs+[(1<<j)^(1<<(111+j))for j in S]);need(r1-r0==6,'actual remaining six-channel cut')
 code={'pivot':i,'canonical_basis_indices':inds,'initial_pivot_row_hex':hex(Ki),'local_pivot_row_hex':hex(Li),'column_zero_complement_hex':[hex(h)for h in H],'core_basis_hex':[hex(b)for b in B],'receiver_core_coefficients':A,'receiver_preloads_hex':[hex(r)for r in R],'residual_fitting_rows_hex':[hex(r)for r in residual],'six_remaining_modes_hex':[hex(h)for h in H[2:]],'dimensions':{'canonical':9,'column_zero_complement':8,'residual_unfinished_fitting':9,'core':3,'remaining_complement':6,'actual_prefix_history_span':4,'prescribed_history_span_after_all_nine_modes':10},'natural_full_fitting_foreign_charge':sum(((r.bit_count()-1)>36)+((r.bit_count()-1)>52)for j,r in enumerate(residual)if j!=i),'qualification':'One target is already physically completed. Six-mode completion for all others is algebraic; their actual decoder remains open.'}
 meta={'captures':captures,'events':events,'original_y_cache':cache_y,'precode':precode,'local_reads':local_reads,'encoder':encoder,'pivot_completion':finish,'completed_Y_feedback':feedback,'dirty_deposits':deposits,'purification':purification,'other_core':other}
 a.output.mkdir(parents=True,exist_ok=True);pins={f:m['save_word'](a.output/f,w)for f,w in [('PREFIX.json.gz',pre),('CLOSED-PARTIAL.json.gz',close)]}
 for rec in(pr,cr):rec.pop('rows')
 out={'status':'PASS_ACTUAL_CANONICAL_PIVOT_RETAINS_GLOBAL_MODE','native_sha256':m['PIN'],'geometry_sha256':BASE_PIN,'replayer_sha256':REPLAY_PIN,'metadata':meta,'prefix_receipt':pr,'closed_receipt':cr,'word_pins':pins,'negative_controls':controls,'actual_receiver_cut':{'receivers':S,'observation_rank':r0,'augmented_rank':r1,'deficit':r1-r0},'complete_supplier':False,'new_kappa':False}
 (a.output/'CODE.json').write_text(json.dumps(code,indent=2,sort_keys=True)+'\n');(a.output/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'prefix':pr['counts'],'closed':cr['counts'],'peak':pr['peak_owned'],'cut':out['actual_receiver_cut'],'encoder_weights':[b.bit_count()for b in[Ki,*H[:2]]]}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for n in('native','geometry','replayer','output'):p.add_argument('--'+n,type=Path,required=True)
 main(p.parse_args())
