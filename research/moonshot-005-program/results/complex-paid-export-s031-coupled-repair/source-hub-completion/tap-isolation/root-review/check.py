#!/usr/bin/env python3
"""Independent raw causal patch and complete rational endpoint/quotient replay."""
from argparse import ArgumentParser
from pathlib import Path
from hashlib import sha256
import json,runpy,sys
ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();here=Path(__file__).resolve().parent
for p,h in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():assert sha256((args.repo/p).read_bytes()).hexdigest()==h,p
baseline=here.parent.parent/'frozen-gates/root-review/check.py';sys.argv=[str(baseline),'--repo',str(args.repo),'--out',str(args.out/'baseline')];s=runpy.run_path(str(baseline));F=s['F'];D=set(s['D']);schedule=[e for e in s['schedule']if e not in D];routes={e:uv for e,uv in s['routes'].items()if e not in D};forms={e:{j:q for j,q in s['forms'][e].items()if j not in D}for e in schedule}
assert routes[48]==(3,117)and forms[48]=={~332:F(-3072)}
assert forms[155100]=={48:F(-1,3072)}
uses=[e for e in schedule if e!=155100 and 48 in forms[e]];assert len(uses)==11
for e in uses:del forms[e][48]
exports=[e for e,(a,b)in routes.items()if a==3];source_changes=[e for e in exports if e!=48 and ~332 in forms[e]];assert len(source_changes)==6
for e in source_changes:del forms[e][~332]
assert [e for e in schedule if 48 in forms[e]]==[155100]
assert [e for e in exports if ~332 in forms[e]]==[48]
holders={~j:c for j,c in enumerate(s['w']['initial'])}
for e in schedule:
 chart=routes[e][0]if e in routes else s['terminal_chart'][e]
 assert all(holders.get(j)==chart for j in forms[e]),('nonlocal patch',e)
 if e in routes:holders[e]=routes[e][1]
E1=[];v1={}
for i,e in enumerate(s['ends']):
 row,imp=s['backward'](e,forms,schedule);E1.append(row)
 if imp[-1]:v1[i]=imp[-1]
 expected=s['E0'][i].copy()
 if s['E'][i].get(332):expected[332]=s['E'][i][332]
 else:expected.pop(332,None)
 assert row==expected,('full endpoint patch mismatch',e)
assert v1==s['v0']
assert all(E1[i]==s['E0'][i]for i in s['A'])
cols=s['columns'](E1,1289);C=[cols[j]for j in s['X']]+[v1];basis={}
for c in C:s['basis_add'](basis,c)
assert len(basis)==909
Frows=[]
for e in exports:
 row={~j:q for j,q in forms[e].items()}
 if e==94019:row[1289]=F(1)
 Frows.append(row)
assert len(exports)==909 and s['rank'](Frows)==909
residuals=[];failed=[];pure=[];purefailed=[]
for i in s['eligible']:
 f={i:F(1)}
 for j,q in s['Rcols'][i].items():
  if j in s['Yset']:s['add'](f,cols[j],-q)
 r=s['residue'](basis,f);residuals.append(r)
 if r:failed.append(s['ends'][i])
 if not(set(s['Rcols'][i])&s['Yset']):
  pure.append(r)
  if r:purefailed.append(s['ends'][i])
assert len(pure)==272 and not purefailed
assert s['rank'](residuals)==5 and len(failed)==102
allbasis={j:v.copy()for j,v in basis.items()}
for j in s['Y']:s['basis_add'](allbasis,cols[j])
assert len(allbasis)==1288
CA=[{j:q for j,q in E1[i].items()if j in s['Xset']}for i in s['A']]
for row,i in zip(CA,s['A']):
 if v1.get(i):row[1289]=v1[i]
ca=s['rank'](CA);assert not s['TH'][332], 'T and h input332 rows vanish'
result={'status':'PASS_ROOT_EXACT_TAP_ISOLATION','retired_D1_routes':sorted(D),'changed_non_source_forms':uses,'changed_source_forms':source_changes,'new_routes':0,'complete_target_input_column_restored':332,'all_other_endpoint_columns_equal_frozen_D1':True,'all_outside_endpoint_rows_equal_frozen_D1':True,'actual_patched_word_local_and_causal':True,'natural_source_export_basis_rank':909,'C_rank_Q':909,'Ca_rank_Q':ca,'pure_source_pinned_count':272,'pure_source_pinned_failures':0,'full_pinned_quotient_rank':5,'remaining_pinned_failures':102,'control_external_input_rank':1288,'net_independent_obstruction_removed':False,'new_author_executable_imported':False,'retained_independent_root_reconstruction_reused':True,'complete_repaired_word':False,'new_complete_kappa':False}
args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],11,6,332,272,909,5,102,1288,flush=True)
