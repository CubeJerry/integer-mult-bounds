#!/usr/bin/env python3
"""Three-root overlapping source encounters with an actual early E6 exit."""
import argparse,copy,hashlib,json
from pathlib import Path
ROOT='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
ROOT_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=ap.parse_args();raw=(a.repo/ROOT).read_bytes();assert hashlib.sha256(raw).hexdigest()==ROOT_SHA;R=json.loads(raw)['native_roots'];a.out.mkdir(parents=True,exist_ok=True)
 charts={'Hub':{'kind':'ann','rows':[]},'zero':{'kind':'span','rows':[]}}
 for i,r in enumerate(R):charts[f'L{i}']={'kind':'span','rows':[r]};charts[f'F{i}']={'kind':'ann','rows':[r]}
 charts.update({'H':{'kind':'span','rows':[R[52],R[54]]},'J':{'kind':'span','rows':[R[52],R[54],R[0]]},'C0':{'kind':'ann','rows':[R[0],R[31]]},'C1':{'kind':'ann','rows':[R[1],R[8]]}})
 ops=[['MOVE','X52','H'],['MOVE','X54','H'],['ADD','X54','X52'],['MOVE','X52','C0'],['MOVE','Y0','C0'],['ADD','X52','Y0'],['MOVE','Y0','F0'],['MOVE','X52','Hub'],['MOVE','X54','J'],['MOVE','X0','J'],['ADD','X0','X54'],['MOVE','X54','C1'],['MOVE','Y1','C1'],['ADD','X54','Y1'],['MOVE','Y1','F1'],['MOVE','X54','Hub'],['MOVE','X0','Hub'],['ADD','X0','X54'],['ADD','X54','X52']]
 ops += [['MOVE',f'X{i}','Hub']for i in range(111)if i not in [0,52,54]]+[['MOVE',f'Y{i}',f'F{i}']for i in range(2,111)]
 w={'schema':'overlapping-cohort-early-exit-v1','native_sha256':ROOT_SHA,'charts':charts,'operations':ops,'source_order':[52,54,0],'source_encoding_matrix':[[1,1,0],[0,1,1],[0,0,1]],'encoded_bank_destinations':{'X52':{'chart':'C0','receiver':0},'X54':{'chart':'C1','receiver':1}},'local_output_forms':{'0':[52,54],'1':[0,54]},'fully_completed_native_roles':[],'new_complete_kappa':False}
 (a.out/'WORD.json').write_text(json.dumps(w,indent=2,sort_keys=True)+'\n')
 c=copy.deepcopy(w);c['schema']='overlapping-cohort-paid-completion-control-v1';c['fully_completed_native_roles']=[0,1]
 for i,terms in [(0,[0,52,54]),(1,[0,1,54])]:
  n=f'K{i}';c['operations'] += [['INIT',n,'Hub']]+[['ADD',f'X{j}',n]for j in terms]+[['MOVE',n,f'F{i}'],['ADD',n,f'Y{i}'],['CLEAR',n]]
 (a.out/'COMPLETED-CONTROL-WORD.json').write_text(json.dumps(c,indent=2,sort_keys=True)+'\n');print('BUILT_OVERLAPPING_COHORT_PRECURSOR')
if __name__=='__main__':main()
