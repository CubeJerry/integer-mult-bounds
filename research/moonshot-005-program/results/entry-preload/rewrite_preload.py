"""Discharge five historical helper-difference observations by four paid entry loads.
Conditional reference difference rail; no full shared native admission.
"""
import argparse,gzip,hashlib,importlib.util,json
from collections import defaultdict,Counter
from fractions import Fraction as F
from pathlib import Path
BASE_PIN='aadcd3f2409cb2da80d52eefb44c2d950e4efd0a23de0a68014abf8ffb954cd7'
BASE=Path(__file__).resolve().parent.parent/'historical-accumulator'/'rewrite.py'
def load_base(path):
 if hashlib.sha256(path.read_bytes()).hexdigest()!=BASE_PIN:raise ValueError('base rewriter pin')
 spec=importlib.util.spec_from_file_location('accumulator_base',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def construct(w,cert,b):
 need=b.need;N=w['public']+w['owned_fields'];M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);mapping={r:r for r in range(N)};after=defaultdict(list);returns={};acc={};program=[];rebindings=[];loads=[]
 entry=next(i for i,vs in enumerate(w['frames']) if not vs)
 for j,c in enumerate(cert):
  z=N+j;acc[c['event']]=z;returns[c['event']]=c;row={};helper_terms=[]
  for term in c['witnesses']['all']:
   o=term['observation'];need(o['phase']=='after' and o['event']<c['event'] and o['chart']==c['to'],'historical observation pins')
   if o['kind']=='helper':
    b.add(row,{int(i):F(v) for i,v in o['row'].items()},F(term['coefficient']));helper_terms.append({'role':o['role'],'event':o['event'],'coefficient':term['coefficient']})
   else:
    need(o['kind']=='owned','remaining observation kind');after[o['event']].append((c,z,term))
  need(row and all(r in M and w['initial'][r]==entry for r in row),'preload uses cochart initial main differences only')
  program.append(['INIT',z,entry])
  for r,c0 in sorted(row.items()):program.append(['ADD',z,r,str(c0),entry])
  program.append(['MOVE',z,entry,c['to'],True])
  loads.append({'return_event':c['event'],'physical_owner':z,'entry_chart':entry,'destination':c['to'],'rank':len(w['frames'][c['to']]),'support':len(row),'row':[[r,str(c0)] for r,c0 in sorted(row.items())],'replaced_helper_observations':helper_terms})
 prelude=len(program)
 for k,e in enumerate(w['program']):
  op,r=e[:2]
  if op=='INIT':mapping[r]=r
  if k in returns:
   c=returns[k];z=acc[k];need(e==['MOVE',c['owner'],c['from'],c['to'],True],'owned return pin');old=mapping[r];at=len(program);program.append(['CLEAR',old,c['from']]);mapping[r]=z;rebindings.append({'physical_before_event':at,'event':k,'logical_owner':r,'old_physical_owner':old,'new_physical_owner':z,'destination':c['to']})
  else:
   x=e[:];x[1]=mapping[r]
   if op in ('ADD','COPY'):x[2]=mapping[e[2]]
   program.append(x)
  for c,z,term in after.get(k,()):program.append(['ADD',z,mapping[term['observation']['role']],term['coefficient'],c['to']])
 return program,rebindings,loads,prelude

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base-rewriter',type=Path,default=BASE);a0,_=ap.parse_known_args();b=load_base(a0.base_rewriter);ap.add_argument('--source',type=Path,default=b.default_source());ap.add_argument('--certificate',type=Path,default=b.default_certificate());ap.add_argument('--output',type=Path);ap.add_argument('--transcript',type=Path);a=ap.parse_args();raw=a.source.read_bytes();b.need(hashlib.sha256(raw).hexdigest()==b.PIN,'source SHA');w=json.loads(gzip.decompress(raw));cert=json.loads(a.certificate.read_text());ops,rebind,loads,prelude=construct(w,cert,b);rows,cur,bill=b.replay(w,ops,len(cert),rebind);base,bcur,bbill=b.replay(w,w['program'],0);b.need(rows[:w['public']]==base[:w['public']] and cur[:w['public']]==bcur[:w['public']],'all public difference endpoints');b.need(not bill['final_live_owned'],'complete cleanup')
 counts=Counter(bill['counts']);counts.subtract(bbill['counts']);added=Counter(x['rank'] for x in loads);removed=Counter(c['rank'] for c in cert);expected=Counter(bbill['move_histogram']);expected.subtract(removed);expected.update(added);b.need(dict(expected)==bill['move_histogram'],'exact paid histogram');b.need(dict(added)=={3:3,6:1} and dict(removed)=={2:3,5:1},'direct and skipped ranks');b.need([x['support'] for x in loads]==[44,44,44,49],'exact entry form supports');b.need(counts['ADD']==185 and counts['INIT']==4 and counts['CLEAR']==4 and counts['MOVE']==0 and all(v==0 for k,v in counts.items() if k not in ('ADD','INIT','CLEAR','MOVE')),'complete operation increments')
 controls=[]
 for name in ('wrong_preload_coefficient','wrong_preload_destination','wrong_preload_ownership'):
  bad=[e[:] for e in ops]
  if name=='wrong_preload_coefficient':bad[1][3]=str(-F(bad[1][3]))
  elif name=='wrong_preload_destination':next(e for e in bad[:prelude] if e[0]=='MOVE')[3]=3
  else:next(e for e in bad[:prelude] if e[0]=='MOVE')[4]=False
  try:
   rr,cc,bi=b.replay(w,bad,len(cert),rebind);b.need(rr[:w['public']]==base[:w['public']] and not bi['final_live_owned'],'mutated endpoint')
  except ValueError as ex:controls.append({'name':name,'rejected':str(ex)})
  else:raise ValueError('negative control accepted '+name)
 t={'schema':'moonshot-entry-preloaded-difference-rail-v1','source_sha256':b.PIN,'public':w['public'],'owned_fields':w['owned_fields']+len(cert),'initial':w['initial'],'frames':w['frames'],'main_roles':sorted(set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])),'initial_helper_differences':'zero, conditional reference rail; five selected helper observations discharged by paid entry loads','program':ops,'rebindings':rebind,'preloads':loads,'prelude_instructions':prelude};payload=(json.dumps(t,sort_keys=True,separators=(',',':'))+'\n').encode();result={'status':'PASS_ENTRY_PRELOADED_CONDITIONAL_DIFFERENCE_RAIL','source_sha256':b.PIN,'base_rewriter_sha256':BASE_PIN,'certificate_sha256':hashlib.sha256(a.certificate.read_bytes()).hexdigest(),'transcript_payload_sha256':hashlib.sha256(payload).hexdigest(),'public_difference_rows_checked':w['public'],'independent_main_difference_inputs':400,'helper_observations_discharged':5,'later_helper_observation_reads':0,'remaining_owned_observation_reads':4,'entry_form_supports':[x['support'] for x in loads],'entry_ADDs':sum(x['support'] for x in loads),'baseline':bbill,'rewritten':bill,'added_MOVE_histogram':dict(added),'removed_MOVE_histogram':dict(removed),'operation_changes':dict(counts),'preloads':loads,'rebindings':rebind,'negative_controls':controls,'scope':'Five helper observation obligations discharged using explicit paid entry loads from initial q. Four later owned differences and the rest of the reference difference rail remain conditioned; not a complete H4 lift or new kappa.'}
 if a.transcript:a.transcript.write_bytes(gzip.compress(payload,mtime=0))
 if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('preloads','rebindings')},indent=2))
if __name__=='__main__':main()
