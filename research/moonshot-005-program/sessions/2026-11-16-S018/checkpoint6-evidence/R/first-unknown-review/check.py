#!/usr/bin/env python3
import argparse,copy,hashlib,itertools,json,sys
from pathlib import Path
p=argparse.ArgumentParser()
for n in ['repo','work','out']:p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args();P=a.repo/'research/moonshot-005-program';sys.path.insert(0,str(P/'sessions/2026-11-16-S018/root-review'))
from optimize_word import independent_replay
from review_source_families import trace
from review_leaf_capacity import chart_basis,echelon
from price import invoice
bp=a.work/'C/canonical3-reset-source/LIBERATED-CACHED48-WORD.json';wp=a.work/'C/first-unknown49/WORD.json';b=json.loads(bp.read_text());w=json.loads(wp.read_text());sr=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(sr).hexdigest()==w['source_sha256'];R=json.loads(sr)['native_roots'];stats=independent_replay(w);bc=b['carrier_interface_before_operation'];wc=w['carrier_interface_before_operation'];assert(bc,wc)==(634,638)
bv,ba=trace(b)[0][bc];v,at=trace(w)[0][wc];owner='ASC_GROUP_4_74_78';H='CANONICAL_FIRST_UNKNOWN_MEET';chain=[['MOVE',owner,H],['MOVE','Y5',H],['ADD',owner,'Y5'],['MOVE','Y5','F5']]
tail=copy.deepcopy(b['operations'][bc:]);tail.remove(['MOVE','Y5','F5']);assert w['operations']==b['operations'][:bc]+chain+tail
assert set(w['targets'])==set(b['targets'])|{5};assert bv[owner]==1<<5 and chart_basis(b['charts'][ba[owner]])==chart_basis(b['charts']['M1'])
C={n:chart_basis(z)for n,z in w['charts'].items()};assert len(C[H])==4
assert len(echelon(C[H]+C['M1'])[0])==5 and len(echelon(C[H]+C['F5'])[0])==7
for n,z in bv.items():
 assert v[n]==(z^(1<<5)if n=='Y5'else z)
 assert at[n]==('F5'if n=='Y5'else H if n==owner else ba[n])
cover=json.loads((a.work/'C/first-unknown49/RESULT.json').read_text())['orthogonal_partition_of_U63'];flat=sum(cover,[]);U=set(range(111))-set(b['targets']);assert len(cover)==12 and len(flat)==len(set(flat))==63 and set(flat)==U
for i in U:assert any(z==1<<i and ba[n]==f'L{i}'for n,z in bv.items())
for g in cover:
 for i,j in itertools.combinations(g,2):
  assert sum(x*y for x,y in zip(R[i],R[j]))==0
  assert len(echelon(C[f'L{i}']+C[f'F{j}'])[0])==7 and len(echelon(C[f'L{j}']+C[f'F{i}'])[0])==7
for event in [chain[0],chain[2]]:
 bad=copy.deepcopy(w);bad['operations'].remove(event)
 try:independent_replay(bad)
 except AssertionError:pass
 else:raise AssertionError('omission not rejected')
report={'status':'PASS_ROOT_ACTUAL_FIRST_UNKNOWN49_AND_12_COVER_REVIEW','base_word_sha256':hashlib.sha256(bp.read_bytes()).hexdigest(),'word_sha256':hashlib.sha256(wp.read_bytes()).hexdigest(),'proof_sha256':hashlib.sha256((a.work/'C/FIRST-UNKNOWN49-AND-ACYCLIC-COVER.md').read_bytes()).hexdigest(),'all222_native_stats':stats,'literal_added_chain':chain,'every_other_cut_value_and_chart_unchanged':True,'actual_raw_ground_basis':48,'orthogonal_cover':cover,'acyclic_witness_size_upper_bound_at_fresh48':12,'two_independent_omission_controls':True,'price':invoice(stats['movement_profile']),'scope':'First unknown5 is physically decoded; raw ground source remains48. Pairwise actual local access within12 explicit groups bounds only the acyclic-witness method, not all information inequalities or feasibility. Fixed source-code static closure still49;62 receivers require new coded information or altered histories. All foundations and full supplier remain open.'}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
