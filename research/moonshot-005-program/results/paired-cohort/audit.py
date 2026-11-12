#!/usr/bin/env python3
"""Exact source residual rank and real-word mutation checks."""
import argparse,sys,copy
from pathlib import Path
def main(a):
 sys.path.insert(0,str(a.reconstruction));from common import F,need,load_inputs,sha,gzip,json,rank,mul
 import build as b
 s,_,_=load_inputs(a.repo);wb=(a.output/'WORD.json.gz').read_bytes();w=json.loads(gzip.decompress(wb));raw={int(x):r for x,r in w['private_role_map'].items()};actual,_=b.interpret_prefix(s,w);X=s['hosted']['X2'];Y=s['hosted']['Y2'];idx={r:i for i,r in enumerate(Y)};R=[[F(0) for _ in Y] for _ in X]
 for i,x in enumerate(X):
  for y,c in w['paired_reverse_corrections'].get(str(x),[]):R[i][idx[y]]=F(c)
 need(not any(v for row in mul(R,R) for v in row),'reverse addition matrix square zero');residual=[[F(i==j)+R[i][j] for j in range(96)] for i in range(96)];need(rank(residual)==96,'no reverse debt-rank reduction from partial frame')
 mutants={}
 def reject(name,m):
  try:
   rows,_=b.interpret_prefix(s,m);need(rows==actual,'wrong exact1880-coordinate prefix');b.typed(s,m)
  except (ValueError,KeyError) as e:mutants[name]=str(e)
  else:raise ValueError('mutant survived: '+name)
 g=next(g for g in w['paired_collection']['groups'] if g['kind']=='inverse_transpose')
 for name,event,value in [('encoder_original_not_cleared',g['encoder_snapshots'][-1]+1,'0'),('wrong_facet_injection',g['injections'][0]['event'],'1'),('decoder_original_not_cleared',g['decoder_snapshots'][-1]+1,'0')]:
  m=copy.deepcopy(w);m['program'][event][3]=value;reject(name,m)
 defect=w['paired_collection']['groups'][0];first=defect['reads'][0]['event'];source=w['program'][first][2];moves=[i for i,e in enumerate(w['program'][:first]) if e[0]=='MOVE' and e[1]==source];m=copy.deepcopy(w);m['program'][moves[-1]][3]=s['final'][next(r for r,j in raw.items() if j==source)];reject('Y2_skips_required_defect_cochart',m)
 result={'status':'PASS_PAIRED_SOURCE_RESIDUAL_RANK_AND_MUTANTS','word_sha256':sha(wb),'reverse_addition_rank':rank(R),'reverse_addition_square_zero':True,'remaining_reverse_target_rank':96,'ordinary_reverse_pairs_completed':0,'mutants':mutants,'scope':'The source partial code has not reduced global reverse residual rank. No free completion or new kappa is claimed.'};(a.output/'AUDIT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--reconstruction',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
