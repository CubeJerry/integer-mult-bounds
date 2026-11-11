#!/usr/bin/env python3
"""Sharp105-arrival full-return preprocessing, deliberately outside the target budget."""
import argparse,gzip,hashlib,importlib.util,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
BASE_PIN='aadcd3f2409cb2da80d52eefb44c2d950e4efd0a23de0a68014abf8ffb954cd7'
CERT_PIN='d46db515a5fead49b752b8d798472c883aff7698d7e5e948f0d4e336ec99054b'
def base(path):
 if hashlib.sha256(path.read_bytes()).hexdigest()!=BASE_PIN:raise ValueError('base pin')
 s=importlib.util.spec_from_file_location('retained_replay',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def build(w,cert,b):
 n=w['public']+w['owned_fields'];entry=3;temporary=n+4;rows=[{int(k):Q(v) for k,v in c['target_row'].items()} for c in cert];nonentry=sorted({k for row in rows for k in row if w['initial'][k]!=entry});entry_terms=sum(sum(w['initial'][k]==entry for k in row) for row in rows);mapping={r:r for r in range(n)};ops=[];bind=[];returns={c['event']:(j,c) for j,c in enumerate(cert)}
 for j in range(4):ops.append(['INIT',n+j,entry])
 for j,row in enumerate(rows):
  for k,v in sorted(row.items()):
   if w['initial'][k]==entry:ops.append(['ADD',n+j,k,str(v),entry])
 for k in nonentry:
  at=w['initial'][k];b.need(len(w['frames'][at])==1,'rank-one initial gather');ops.extend([['INIT',temporary,at],['ADD',temporary,k,'1',at],['MOVE',temporary,at,entry,True]])
  for j,row in enumerate(rows):
   if k in row:ops.append(['ADD',n+j,temporary,str(row[k]),entry])
  ops.append(['CLEAR',temporary,entry])
 for j,c in enumerate(cert):ops.append(['MOVE',n+j,entry,c['to'],True])
 prelude=len(ops)
 for k,e in enumerate(w['program']):
  tag,r=e[:2]
  if tag=='INIT':mapping[r]=r
  if k in returns:
   j,c=returns[k];b.need(e==['MOVE',c['owner'],c['from'],c['to'],True],'owned return');old=mapping[r];idx=len(ops);ops.append(['CLEAR',old,c['from']]);mapping[r]=n+j;bind.append({'physical_before_event':idx,'event':k,'logical_owner':r,'old_physical_owner':old,'new_physical_owner':n+j,'destination':c['to']})
  else:
   z=e[:];z[1]=mapping[r]
   if tag in ('ADD','COPY'):z[2]=mapping[e[2]]
   ops.append(z)
 return ops,bind,prelude,rows,nonentry,entry_terms
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--base-rewriter',type=Path,required=True);p.add_argument('--output',type=Path);p.add_argument('--transcript',type=Path);a=p.parse_args();b=base(a.base_rewriter);raw=a.source.read_bytes();b.need(hashlib.sha256(raw).hexdigest()==b.PIN,'source pin');cr=a.certificate.read_bytes();b.need(hashlib.sha256(cr).hexdigest()==CERT_PIN,'certificate pin');w=json.loads(gzip.decompress(raw));cs=json.loads(cr);ops,bind,prelude,rows,nonentry,entry_terms=build(w,cs,b);out,charts,bill=b.replay(w,ops,5,bind);orig,origcharts,origbill=b.replay(w,w['program'],0);b.need(out[:w['public']]==orig[:w['public']] and charts[:w['public']]==origcharts[:w['public']],'public endpoint equality');b.need(not bill['final_live_owned'],'cleanup');delta=Counter(bill['counts']);delta.subtract(origbill['counts']);added=Counter({1:len(nonentry),3:3,6:1});removed=Counter({2:3,5:1});hist=Counter(origbill['move_histogram']);hist.update(added);hist.subtract(removed);b.need(dict(hist)==bill['move_histogram'],'exact MOVE histogram');b.need(len(nonentry)==101 and entry_terms==192,'source support census');b.need(delta['ADD']==501 and delta['INIT']==105 and delta['CLEAR']==105 and delta['MOVE']==101,'complete primitive increments')
 controls=[]
 for name in ('wrong_preload_coefficient','wrong_temporary_ownership','stale_after_rebinding'):
  bad=[e[:] for e in ops]
  if name=='wrong_preload_coefficient':next(e for e in bad[:prelude] if e[0]=='ADD')[3]='999'
  elif name=='wrong_temporary_ownership':next(e for e in bad[:prelude] if e[0]=='MOVE')[4]=False
  else:
   c=bind[0]
   for e in bad[c['physical_before_event']+1:]:
    if e[1]==c['new_physical_owner']:e[1]=c['old_physical_owner'];break
    if e[0] in ('ADD','COPY') and e[2]==c['new_physical_owner']:e[2]=c['old_physical_owner'];break
  try:
   o,ch,bi=b.replay(w,bad,5,bind);b.need(o[:w['public']]==orig[:w['public']] and not bi['final_live_owned'],'mutant endpoint')
  except ValueError as ex:controls.append({'mutation':name,'rejection':str(ex)})
  else:raise ValueError('accepted mutation '+name)
 t={'schema':'moonshot-whole-return-preprocessing-v1','source_sha256':b.PIN,'public':w['public'],'owned_fields':w['owned_fields']+5,'initial':w['initial'],'frames':w['frames'],'main_roles':sorted(set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])),'program':ops,'rebindings':bind,'prelude_instructions':prelude,'scope':'Supplied400-input difference rail only. Four entire returns use actual initial q holders; no later helper or owned observations. The105 added arrivals exceed the target budget.'};payload=(json.dumps(t,sort_keys=True,separators=(',',':'))+'\n').encode();result={'status':'PASS_SHARP_105_ARRIVAL_INITIAL_PREPROCESSING','source_sha256':b.PIN,'historical_certificate_sha256':CERT_PIN,'base_rewriter_sha256':BASE_PIN,'transcript_payload_sha256':hashlib.sha256(payload).hexdigest(),'instructions':len(ops),'prelude_instructions':prelude,'independent_difference_inputs':400,'public_endpoints':w['public'],'preload_supports':[len(x) for x in rows],'distinct_q_inputs_used':len(set().union(*(set(x) for x in rows))),'nonentry_inputs':len(nonentry),'entry_ADDs':entry_terms,'gather_input_ADDs':len(nonentry),'distributed_accumulation_ADDs':sum(len([k for k in row if w['initial'][k]!=3]) for row in rows),'added_MOVEs':dict(added),'removed_MOVEs':dict(removed),'operation_changes':dict(delta),'baseline':origbill,'rewritten':bill,'declared_owned_labels':w['owned_fields']+5,'later_observation_reads':0,'rebindings':bind,'negative_controls':controls,'scope':'Exact minimum105 added-arrival preprocessing before unchanged source calendar, not a target-feasible shared native. All q input formation and reference rail costs remain explicit.'}
 if a.transcript:a.transcript.write_bytes(gzip.compress(payload,mtime=0))
 if a.output:a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('rebindings',)},sort_keys=True,indent=2))
