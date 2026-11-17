"""Independent exact support certificate for three-round binary frame service."""
import argparse,hashlib,itertools,json
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
SOURCE='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
WORD_SHA='6f1bd8465c7a4fa5b7b59888fb5dbd9bbbb88dc3306c984bd71497fd4be7d980'
CUT_SHA='668af067842aed7bfd0e1a3ea403756d9aaf3cd3a0cd678c29d5ca344ad4adb8'
ROLES=[14,17,19,20,96,99,101,102]

def run(repo,parent,out):
 raw=(repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA
 roots=json.loads(raw)['native_roots']
 assert all(sum(x*y for x,y in zip(roots[i],roots[j]))==0 for i,j in itertools.combinations(ROLES,2))
 assert all(sum(x*x for x in roots[i])>0 for i in ROLES)
 assert hashlib.sha256((parent/'WORD.json').read_bytes()).hexdigest()==WORD_SHA
 rawcut=(parent/'CUT-INVENTORY.json').read_bytes();assert hashlib.sha256(rawcut).hexdigest()==CUT_SHA
 cut=json.loads(rawcut);fields={f['name']:f for f in cut['fields']}
 assert cut['word_sha256']==WORD_SHA and cut['cut_before_operation']==1893
 for i in ROLES:
  assert fields[f'NATIVE_{i}']['chart']==f'L{i}' and int(fields[f'NATIVE_{i}']['row_hex'],16)==1<<i
  assert fields[f'Y{i}']['chart']=='zero'
 # Independently enumerate all 8! native-seed permutations. Unlike make_cases,
 # this verifier does not derive allowed seed sets or backtrack on them.
 seeds=np.array(list(itertools.permutations(range(8))),dtype=np.int64)
 seedbits=1<<seeds
 pp=list(itertools.permutations(range(4)));cases=[];rank6=0
 for p2 in pp:
  for p3 in pp:
   masks=[1<<i for i in range(8)];history=[]
   for p in [tuple(range(4)),p2,p3]:
    for i,j in enumerate(p):masks[i]=masks[4+j]=masks[i]|masks[4+j]
    history.append(masks.copy())
   if any(m.bit_count()!=6 for m in masks):continue
   rank6+=1;valid=np.ones(len(seeds),dtype=bool)
   for i,j in enumerate(p3):
    inds=[k for k in range(8) if masks[i]>>k&1]
    actual=seedbits[:,inds].sum(axis=1)
    valid &= actual==(255^((1<<i)|(1<<(4+j))))
   for index in np.flatnonzero(valid):
    seed=seeds[index].tolist();before=[]
    for mask in history[1]:before.append(sum(1<<seed[k] for k in range(8) if mask>>k&1))
    witnesses=[]
    for i,j in enumerate(p3):
     need_a=15^(1<<i);need_b=(15^(1<<j))<<4;u,v=before[i],before[4+j]
     missing=[need_a&~u,need_a&~v,need_b&~u,need_b&~v]
     assert all(missing), ('uncovered final pair',p2,p3,seed,i,j)
     witnesses.append({'pair':[i,4+j],'incoming_chart_source_masks':[u,v],
       'required_source_masks':[need_a,need_b],'four_nonzero_missing_masks':missing})
    cases.append({'round2':p2,'round3':p3,'seed_permutation':seed,'final_pair_witnesses':witnesses})
 assert rank6==120 and len(cases)==192
 # Every invertible binary pair map has distinct nonzero coefficient rows.
 gl2=[(a,b) for a in [1,2,3] for b in [1,2,3] if a!=b]
 assert len(gl2)==6 and (3,3) not in gl2
 result={'status':'PASS_EXACT_THREE_ROUND_COMPLEMENTARY_FRAME_GATE',
   'physical_roles':ROLES,'native_source_sha256':SHA,'parent_word_sha256':WORD_SHA,'parent_cut_sha256':CUT_SHA,
   'all_eight_source_lines_independent_and_mutually_orthogonal':True,
   'normalized_matching_schedules':576,'rank6_final_schedules':rank6,'native_seed_permutations_checked_per_schedule':40320,
   'legal_schedule_seed_cases':len(cases),'final_pairs_certified':4*len(cases),
   'gate_coefficient_rows_that_both_outputs_would_need':[3,3],
   'binary_GL2_matrices':gl2,'cases':cases,
   'scope':'Eight public Y records, one native-unit seed each, three actual cochart cross-frame perfect-matching rounds including identity-map pairs, invertible binary local two-record maps, no additional X read or outside-record assistance. No general receiver or supplier exclusion.'}
 out.mkdir(parents=True,exist_ok=True);(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(result['status'],'192 legal cases, 768 exact final-pair witnesses')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--parent',type=Path,default=HERE.parent/'full-half-reservoir');p.add_argument('--out',type=Path,default=HERE/'output');a=p.parse_args();run(a.repo,a.parent,a.out)
