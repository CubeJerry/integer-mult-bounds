"""Independent dense original-input review of the coordinated cross-D word."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import argparse,collections,copy,gzip,hashlib,json
from dense_engine import run,span,eqrow
if not __debug__:raise SystemExit('Assertions required; do not use -O')
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PARENT='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc'
WORD='787ae38760119ce9b628c3b9eff0244271b3c0ad65b646c725730a2142d6dc1a'
def load(p,pin):
 b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==pin;return json.loads(gzip.decompress(b))
def rank(rows):
 piv={}
 for raw in rows:
  row=list(raw)
  for i,b in sorted(piv.items()):
   if row[i]:
    x,y=row[i],b[i];row=[y*v-x*w for v,w in zip(row,b)]
    d=0
    for v in row:d=gcd(d,abs(v))
    if d>1:row=[v//d for v in row]
  non=[i for i,v in enumerate(row) if v]
  if non:piv[non[0]]=row
 return len(piv)
def main(a):
 s=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',PIN);q=load(a.bundle/'source-evidence/rail-consumer.json.gz',PARENT);w=load(a.bundle/'output/rail-cross-pair.json.gz',WORD)
 mb=(a.bundle/'MANIFEST.json').read_bytes();assert hashlib.sha256(mb).hexdigest()=='b5bfd431477d9d423961fd679b8c940273594530f11c2f6629d2ae523d6342ac'
 for row in json.loads(mb)['files']:assert hashlib.sha256((a.bundle/row['path']).read_bytes()).hexdigest()==row['sha256']
 assert all(w[k]==q[k] for k in ['public','owned_fields','initial','frames','source_role_map'])
 spaces=list(map(span,w['frames']));roles={int(k):v for k,v in q['source_role_map'].items()};rev={v:k for k,v in roles.items()}
 host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};live=s['live'];pairs=[(1,106,209,394,1,226),(106,1,298,305,99,129)]
 old,do,lo,bo,_=run(q,spaces);capture_before={};capture_after={};events=[]
 for port,dp,b,d,line,facet in pairs:
  assert (roles[host[port][0]],roles[host[dp][1]])==(b,d)
  assert q['initial'][b]==line and s['final'][rev[d]]==facet
  touches=[(i,o) for i,o in enumerate(q['program']) if o[1]==d or o[0] in ('ADD','COPY') and o[2]==d]
  assert len(touches)==1 and touches[0][1]==['MOVE',d,3,facet,False]
  assert all(old[r][b]==(do if r==b else 0) for r in range(400))
  start=next(i for i,o in enumerate(w['program']) if o==['MOVE',451,127,facet,True])
  assert w['program'][start:start+5]==[['MOVE',451,127,facet,True],['ADD',451,d,'1',facet],['MOVE',451,facet,line,True],['ADD',b,451,'-1',line],['MOVE',451,line,3,True]]
  capture_before[start]=(f'pre_{port}',[451,b,d]+[roles[j] for j in live]);capture_after[start+4]=(f'post_{port}',[451,b,d])
  events.append({'port':port,'D_port':dp,'start':start,'B':b,'D':d,'line':line,'facet':facet,'old_D_event':touches[0][0]})
 new,dn,ln,bn,sn=run(w,spaces,capture_before=capture_before,capture_after=capture_after)
 assert ln==lo=={i:s['final'][rev[i]] for i in range(400)}
 for r in range(400):
  delta=next((d for _,_,b,d,_,_ in pairs if r==b),None);want=[x*dn for x in old[r]]
  if delta is not None:want[delta]-=do*dn
  assert [x*do for x in new[r]]==want
 for ev in events:
  port=ev['port'];b=ev['B'];d=ev['D'];db,rb,lb=sn[f'pre_{port}'];da,ra,la=sn[f'post_{port}']
  assert lb[b]==ev['line'] and lb[d]==ev['facet'] and lb[451]==127
  assert rb[b]==[db*int(i==b) for i in range(400)] and rb[d]==[db*int(i==d) for i in range(400)]
  for j in live:assert lb[roles[j]]==127 and eqrow(rb[roles[j]],db,old[roles[j]],do)
  payload=rb[451].copy();payload[d]+=db
  assert eqrow(ra[451],da,payload,db) and la[451]==3
  bvalue=[-v for v in payload];bvalue[b]+=db
  assert eqrow(ra[b],da,bvalue,db) and la[b]==ev['line'];assert eqrow(ra[d],da,rb[d],db)
 def residual(rr,den):
  result=[]
  for b,d in host.values():
   row=rr[roles[b]].copy();row[roles[b]]-=den;row[roles[d]]+=den;result.append(row)
  return result
 ro,rn=residual(old,do),residual(new,dn);assert rank(ro)==58 and rank(rn)==57
 ports=list(host);i,j=ports.index(1),ports.index(106);assert rn[i]==[-v for v in rn[j]]
 complete=lambda rows:[p for p,row in zip(ports,rows) if not any(row)]
 assert complete(ro)==complete(rn) and len(complete(rn))==24
 debt=0
 for port in live:
  row=[F(v,dn) for v in new[roles[port+112]]];c=F(1) if port in host else F(1,2);row[roles[port]]-=c;row[roles[port+112]]-=c;debt+=sum(bool(v) for v in row)
 assert debt==4920
 delta={r:bn['moves'].get(r,0)-bo['moves'].get(r,0) for r in set(bn['moves'])|set(bo['moves'])};delta={r:n for r,n in delta.items() if n};assert delta=={1:4,7:2,9:-2}
 assert bn['counts']=={'ADD':3860,'CLEAR':402,'INIT':402,'MOVE':844,'SCALE':2}
 assert bn['instructions']==5510 and bn['lifetimes']==402 and bn['peak']==29
 controls=[]
 for label,typ in [('wrong_D_pickup',0),('wrong_B_deposit',1),('missing_Y_precode',2)]:
  bad=copy.deepcopy(w);ix=events[0]['start']+(1 if typ==0 else 3) if typ<2 else 40
  assert bad['program'][ix][0]=='ADD';bad['program'][ix][3]='0'
  rr,dr,lr,_,_=run(bad,spaces);rejected=lr!=ln or any(not eqrow(rr[r],dr,new[r],dn) for r in range(400));assert rejected;controls.append({'name':label,'event':ix,'rejected':True})
 Bcols={port:all(old[r][roles[b]]==(do if r==roles[b] else 0) for r in range(400)) for port,(b,d) in host.items()}
 Dpaths={}
 for port,(b,d) in host.items():
  dr=roles[d];writes=[(ix,o) for ix,o in enumerate(q['program']) if o[1]==dr];reads=[ix for ix,o in enumerate(q['program']) if o[0] in ['ADD','COPY'] and o[2]==dr]
  Dpaths[port]={'writes':writes,'read_count':len(reads),'all_reads_at_final_chart':all(q['program'][ix][4]==s['final'][d] for ix in reads)}
 out={'status':'PASS_INDEPENDENT_DENSE400_FUNDED_CROSS_D_WORD','native_sha256':PIN,'parent_sha256':PARENT,'word_sha256':WORD,'all400_original_input_columns':True,'only_final_changes':{'B1':'parent_B1-d106','B106':'parent_B106-d1'},'all_firstX_firstY_D_exact_parent':True,'actual_current_donors_and_packet_histories_checked':True,'whole_parent_B_transfer_columns_are_identity':True,'old_reverse_rank':58,'new_reverse_rank':57,'old_completed_reverse_ports_retained':complete(rn),'original_forward_debt':debt,'bill':bn,'movement_delta':delta,'events':events,'negative_controls':controls,'generalization_source_premises':{'B_identity_columns':Bcols,'D_paths':Dpaths},'independence':'No author builder/interpreter imported. Reuses B independently authored dense common-denominator engine from the admitted earlier exchange review; rank oracle uses fraction-free integer row elimination with gcd normalization.','scope':'Finite partial400-input source. Phase maps and literal m3 reviewed separately; no complete source, supplier, or new kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','new_reverse_rank','original_forward_debt','bill','negative_controls']},indent=2));print('B identities',sum(Bcols.values()),'pureD single moves',sum(len(z['writes'])==1 and z['writes'][0][1][0]=='MOVE' for z in Dpaths.values()),'D final-only reads',sum(z['all_reads_at_final_chart'] for z in Dpaths.values()))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--bundle',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
