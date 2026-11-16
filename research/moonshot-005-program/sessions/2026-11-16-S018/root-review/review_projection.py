#!/usr/bin/env python3
"""Independent exact release-pool and simultaneous-ground-interface audit."""
from pathlib import Path
import argparse,copy,hashlib,json
from optimize_word import independent_replay
from review_source_families import trace
def rank(rs):
 b={}
 for x in rs:
  while x:
   k=x.bit_length()-1
   if k in b:x^=b[k]
   else:b[k]=x;break
 return len(b)
def main():
 p=argparse.ArgumentParser()
 for n in ['repo','word','out']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();base=a.repo/'research/moonshot-005-program/results/bit-canonical-mask-source/author/early-paid46/WORD.json';old=json.loads(base.read_bytes());w=json.loads(a.word.read_bytes());independent_replay(old);independent_replay(w)
 assert hashlib.sha256(base.read_bytes()).hexdigest()==w['base_word_sha256']=='27dc6c36eec067acd2fe4679a81c95ea9db8fd6377784a0bbfc060ca52a121fd';assert w['charts']==old['charts']and w['targets']==old['targets']
 S=set(old['targets']);mutable={int(o[2][1:])for o in old['operations']if o[0]=='ADD'and o[2].startswith('X')};B={int(k):v for k,v in w['protected_native_ground_backups'].items()};D=(set(range(111))-S-mutable)|set(B);assert sorted(D)==w['released_carriers']and len(D)==73;assert set(range(111))-S-(D-S)=={61,67};assert not any(o[0]=='ADD'and o[1].startswith('Y')for o in old['operations'])
 for d,b in B.items():
  assert d in S and d not in mutable
  assert[o for o in old['operations']if o[0]=='ADD'and o[2]==b]==[['ADD',f'X{d}',b]]
  assert[o for o in old['operations']if o[0]=='INIT'and o[1]==b]==[['INIT',b,f'L{d}']]
  assert[o for o in old['operations']if o[0]=='MOVE'and o[1]==b]==[['MOVE',b,'zero']]
 os,_=trace(old);ns,_=trace(w);oi=next(k for k,o in enumerate(old['operations'])if o[0]=='CLEAR');ni=w['carrier_interface_before_operation'];ov,oa=os[oi];nv,na=ns[ni]
 assert all(nv[f'X{i}']==1<<i and na[f'X{i}']==(f'L{i}'if i in D else'Hub')for i in range(111));assert all(nv[b]==1<<d and na[b]=='zero'for d,b in B.items())
 G=[v for n,v in ov.items()if oa[n]=='zero'and v>>111==0];H=[v for n,v in nv.items()if na[n]=='zero'and v>>111==0];E=[1<<d for d in B];dm=sum(1<<d for d in D);un=sum(1<<d for d in D-S)
 assert all(not(v&un)for v in G);assert rank(G)==rank(G+E)==rank(H)==rank(G+H)==25;assert rank(H)==rank(H+[v&~dm for v in G]+E)
 assert all(nv[f'IMPORT_E{i}']==0 for i in [8,9,36])
 controls=[]
 for op in [['MOVE','X5','Hub'],['ADD','X50','ADDED_RAW50']]:
  bad=copy.deepcopy(w);bad['operations'].remove(op)
  try:independent_replay(bad)
  except(AssertionError,KeyError):controls.append({'omitted':op,'rejected':True})
  else:raise AssertionError('negative control accepted')
 out={'status':'PASS_ROOT_INDEPENDENT_PROTECTED_PROJECTION_INTERFACE','word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'released_roles':sorted(D),'completed_backed':sorted(B),'unfinished_released':sorted(D-S),'mutable_unfinished_excluded':[61,67],'ground_rank':25,'ground_rowspace_identical':True,'ground_projection_plus_protected_space_formula':True,'old_ground_has_no_released_unfinished_coordinates':True,'actual_raw_native_carriers':73,'actual_raw_Hub_originals':38,'old_M1_imports_now_zero':[8,9,36],'controls':controls,'scope':'Written projection induction separately reviewed; exact full222 endpoint/native-geometry replay and current-source audit. Old higher/history contracts not inherited. No full supplier or new kappa.'};a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
