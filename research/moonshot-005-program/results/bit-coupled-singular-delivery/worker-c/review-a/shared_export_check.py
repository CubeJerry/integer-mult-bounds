#!/usr/bin/env python3
"""Independent source-frame/cut certificate audit, importing no Worker A code."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from check import SOURCE_SHA, dot, kernel, rank2, rref

here=Path(__file__).resolve().parent
repo=next(p for p in here.parents if (p/'AGENTS.md').exists())
source=repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
assert hashlib.sha256(source.read_bytes()).hexdigest()==SOURCE_SHA
roots=json.loads(source.read_text())['native_roots']
base=here.parent/'nine-output'
assert hashlib.sha256((base/'WORD.json').read_bytes()).hexdigest()=='d62e487fe2b191f4ecf6846696d17686061a6892b1bc4b0ed4d47612855b4e36'
assert hashlib.sha256((base/'CLOSED-WORD.json').read_bytes()).hexdigest()=='43814e1b64d7509d28fc8db7f728d3fc47fdef52387d94c67b8237826d7a9c6f'
word=json.loads((base/'WORD.json').read_text())
receipt=json.loads((base/'RESULT.json').read_text())['receipts']['WORD.json']
states=receipt['actual_handoff']
for name,expected in word['expected_owned_at_handoff'].items():
    assert states[name]['chart']==expected['chart']
    assert states[name]['coefficient_hex']==expected['value_hex']
for i in range(111):
    assert states[f'X{i}']['chart']=='Hub'
    assert int(states[f'X{i}']['coefficient_hex'],16)==1<<i
    expected=(1<<(111+i))^((1<<i) if i in receipt['completed_targets'] else 0)
    assert int(states[f'Y{i}']['coefficient_hex'],16)==expected
frame=[0,15,31,35,40,41,106,110]
assert not set(frame)&set(receipt['completed_targets'])
gram=[[dot(roots[i],roots[j]) for j in frame] for i in frame]
assert all(gram[i][j]==(4 if i==j else 2) for i in range(8) for j in range(8))
def project(row): return sum(((row>>j)&1)<<k for k,j in enumerate(frame))
donors=[16,19,38,49,50,56,57]
G=[int(states[f'P{i}']['coefficient_hex'],16) for i in range(8)]+[1<<j for j in donors]
restricted=[project(g) for g in G]
assert rank2(restricted)==5
static=json.loads((here.parent.parent/'worker-a/TWO-RECEIVER-STATIC-GATE.json').read_text())
feasible=[]
outside={i:sum(1<<j for j in range(111) if dot(roots[i],roots[j])!=0) for i in range(111)}
for i in range(111):
    rows=[g&outside[i] for g in G]
    if rank2(rows+[1<<i])==rank2(rows): feasible.append(i)
assert feasible==[16,17,19,38,49,50,56,57,59,60]==static['feasible_receivers']
assert len(static['infeasible_duals'])==101
for item in static['infeasible_duals']:
    i=item['role'];z=int(item['dual_hex'],16)
    assert i not in feasible and z>>i&1 and z&~outside[i]==0
    assert all((g&z).bit_count()%2==0 for g in G)
duals=[49,90,146]
assert rank2(duals)==3 and all((z&g).bit_count()%2==0 for z in duals for g in restricted)
charts={name:(kernel(v['rows']) if v['kind']=='ann' else rref(v['rows']))
        for name,v in word['charts'].items()}
in_downset={name:any(all(dot(row,roots[i])==0 for row in basis) for i in frame)
            for name,basis in charts.items()}
inside=[]
for name,state in states.items():
    if in_downset[state['chart']]:
        value=project(int(state['coefficient_hex'],16))
        assert rank2(restricted+[value])==5,(name,value)
        inside.append(name)
for i in range(111):
    state=states[f'Y{i}']
    if i in receipt['completed_targets']:
        assert not in_downset[state['chart']]
    else:
        assert state['chart']=='zero'
price=json.loads((base/'PRICE.json').read_text())
room=(Fraction(price['limiting_room']['lower']),Fraction(price['limiting_room']['upper']))
assert 0<room[0]<=room[1]<3
minimal_m2_upper=Fraction(price['finite_even_caller_controls'][0]['margin']['upper'])-54
minimal_margin_slope_upper=18*(room[1]-3)
assert minimal_m2_upper<0 and minimal_margin_slope_upper<0
bad=duals.copy();bad[0]^=1
assert any((z&g).bit_count()%2 for z in bad for g in restricted)
result={'status':'PASS_INDEPENDENT_THREE_EXPORT_CUT_REVIEW',
        'source_sha256':SOURCE_SHA,
        'word_sha256':hashlib.sha256((base/'WORD.json').read_bytes()).hexdigest(),
        'frame':frame,'frame_gram':gram,'restricted_G_rows':restricted,
        'restricted_rank':5,'independent_duals':duals,
        'static_no_export_feasible_roles':feasible,
        'static_no_export_failed_duals_independently_checked':101,
        'all_initial_downset_records_checked':len(inside),
        'completed_Y_outside_cut':True,'unserved_Y_at_ground':True,
        'required_extra_payload_dimension':'3V',
        'required_positive_rank_owned_ingresses':3,
        'limiting_room_lower':str(room[0]),'limiting_room_upper':str(room[1]),
        'strict_deficit_lower':str(3-room[1]),
        'minimal_completed_margin_at_m2_upper':str(minimal_m2_upper),
        'minimal_completed_margin_slope_upper':str(minimal_margin_slope_upper),
        'all_even_callers_m_at_least_2_excluded':True,
        'corrupt_dual_rejected':True,
        'classification':'exact source-bound certificate plus separately written universal cut proof',
        'new_kappa':False}
(here/'SHARED-EXPORT-REVIEW-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','restricted_rank','all_initial_downset_records_checked','strict_deficit_lower']}))
