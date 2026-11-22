#!/usr/bin/env python3
"""Reproduce the source-valid t=26 specialization and its local physical bill."""
from pathlib import Path
import argparse,sys,importlib.util,hashlib,json,gzip,time
HERE=Path(__file__).resolve().parent

def mod(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def need(v,msg):
 if not v:raise ValueError(msg)

def main(repo,out,skip_compile):
 started=time.time();reads=set()
 def audit(event,args):
  if event!='open' or not args or not isinstance(args[0],(str,bytes)):return
  try:p=Path(args[0]).resolve()
  except (OSError,ValueError):return
  if not p.is_relative_to(repo):return
  if p.suffix=='.pyc':
   try:p=Path(importlib.util.source_from_cache(str(p)))
   except ValueError:return
  mode=args[1]if len(args)>1 else None
  if isinstance(mode,str)and all(x not in mode for x in 'wax+'):reads.add(p)
 sys.addaudithook(audit)
 out.mkdir(parents=True,exist_ok=True)
 pins=HERE/'SOURCE-PINS.json'
 if pins.exists():
  for path,digest in json.loads(pins.read_text()).items():need(hashlib.sha256((repo/path).read_bytes()).hexdigest()==digest,'source pin '+path)
 build=mod(HERE/'build.py','s033_build');check=mod(HERE/'check.py','s033_check');interfaces=mod(HERE/'interfaces.py','s033_interfaces');controls=mod(HERE/'controls.py','s033_controls');compiler=mod(HERE/'compile.py','s033_compile')
 candidate=out/'CANDIDATE.json.gz';build.build(repo,26,candidate);need(gzip.decompress(candidate.read_bytes())==gzip.decompress((HERE/'CANDIDATE.json.gz').read_bytes()),'exact t26 coefficient reproduction')
 source=check.run(repo,out,candidate,True);need(len(source['source_views'])==11 and all(z['all_protected_rank96']and len(z['views'])==63 for z in source['source_views'].values()),'all693 geometric source views');need(sum(z['native_views']for z in source['source_views'].values())==639,'all639 native source views');need(all(z['full_rank']==480 for z in source['early'].values()),'all11 actual early bases');need({str(j):z['maximum']for j,z in source['propagation'].items()}=={'0':84,'32':60,'35':60},'complete source propagation maxima');need(all(z['maximum']+z['complement_bound']<450 for z in source['propagation'].values()),'strict paired source nonsaturation')
 inter=interfaces.check(repo,candidate,out);need(inter['retained_geometric_H_interfaces']==72 and inter['retained_native_H_interfaces']==67 and len(inter['whole_D_identity_readouts'])==44 and len(inter['D_sections'])==144,'whole retained interfaces');controls.run(repo,out)
 if not skip_compile:
  c=compiler.run(repo,candidate,out);need(c['fullbank_source_H_D_ADD']==454510288 and c['fullbank_ADD_delta']==572680 and c['fullbank_INIT']==279648 and c['fullbank_dirty_CLEAR']==279648,'exact full local replacement bill')
 inherited={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(reads)if p.is_file()and not p.is_relative_to(HERE)}
 (out/'OBSERVED-SOURCE-PINS.json').write_text(json.dumps(inherited,sort_keys=True,indent=2)+'\n')
 result={'status':'PASS_SOURCE_VALID_T26_COUPLED_LOCAL_CONSTRUCTION','geometric_source_views':693,'native_source_views':639,'actual_early_bases':11,'geometric_H_interfaces':72,'native_H_interfaces':67,'whole_D_fibre_identity_pairs':44,'geometric_D_sections':144,'compiler_reproduced':not skip_compile,'seconds':time.time()-started,'independent_implementation':False,'fifth_receiver_complete':False,'complete_supplier':False,'new_complete_kappa':False};(out/'REPLAY-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--out',type=Path,required=True);p.add_argument('--skip-compile',action='store_true');q=p.parse_args();main(q.repo.resolve(),q.out.resolve(),q.skip_compile)
