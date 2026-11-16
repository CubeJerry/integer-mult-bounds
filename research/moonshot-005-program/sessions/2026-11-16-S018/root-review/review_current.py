#!/usr/bin/env python3
"""S018 root review with pinned independent predecessor geometry/price engines.
No S018 construction module is imported. Written proof is reviewed separately.
"""
from pathlib import Path
import argparse,hashlib,json
from optimize_word import independent_replay
from review_leaf_capacity import chart_basis,echelon
from price import invoice
def main():
 p=argparse.ArgumentParser()
 for n in ['repo','word','out']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();raw=a.word.read_bytes();w=json.loads(raw);source=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==w['source_sha256']=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
 roots=json.loads(source)['native_roots'];C={n:chart_basis(s)for n,s in w['charts'].items()}
 assert len(C['zero'])==0 and len(C['Hub'])==8
 for i,r in enumerate(roots):
  assert len(C[f'L{i}'])==1 and len(echelon(C[f'L{i}']+[r])[0])==1
  assert len(C[f'F{i}'])==7 and all(sum(x*y for x,y in zip(row,r))==0 for row in C[f'F{i}'])
 for o in w['operations']:
  assert o[0] in ['INIT','ADD','MOVE','CLEAR'];assert len(o)==(2 if o[0]=='CLEAR'else 3)
  if o[0]=='ADD':assert o[1]!=o[2]
  if o[0] in ['INIT','MOVE']:assert o[2]in C
 assert len(w['targets'])==len(set(w['targets']))
 stats=independent_replay(w);out={'status':'PASS_ROOT_NATIVE_SOURCE_GEOMETRY_ENDPOINTS_PRICE','word_sha256':hashlib.sha256(raw).hexdigest(),'native_source_sha256':w['source_sha256'],'stats':stats,'price':invoice(stats['movement_profile']),'new_complete_kappa':False,'method':'Root separate mathematical review plus independently implemented predecessor Fraction geometry and222-column replay; no S018 author module imported. Exact predecessor price engine is explicitly reused.'}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status']);print(json.dumps({'stats':stats,'price':out['price']},indent=2))
if __name__=='__main__':main()
