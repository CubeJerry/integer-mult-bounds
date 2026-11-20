#!/usr/bin/env python3
"""Independent source-hub interface; retained root reverse-DAG method, new completion checks."""
from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json


def need(ok, why):
    if not ok:
        raise ValueError(why)


def add(row, other, scale=F(1)):
    for j, x in other.items():
        y = row.get(j, 0) + scale*x
        if y:
            row[j] = y
        else:
            row.pop(j, None)


ap = ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--out', type=Path, required=True)
args = ap.parse_args()
pkg = Path(__file__).resolve().parent
for path, digest in json.loads((pkg/'SOURCE-PINS.json').read_text())['files'].items():
    need(sha256((args.repo/path).read_bytes()).hexdigest() == digest, 'pin '+path)
base = args.repo/'research/moonshot-005-program/results'
raw = gzip.decompress((base/'complex-native-funded-donor-cuts/inputs/DOUBLE-CANDIDATE.json.gz').read_bytes())
need(sha256(raw).hexdigest() == '7660985e0b618cdbee13e4190a4c6d5f91fbdf01a8f7a5186fdde8b980c19b48', 'unpacked source')
w = json.loads(raw)
n = len(w['initial'])
need(n == len(w['final']) == 1289, 'complete endpoint inventory')
old_forms = {e: {j: F(x) for j, x in row} for e, row in w['forms']}
forms = {e: row.copy() for e, row in old_forms.items()}
schedule = [e for e in w['schedule'] if e != 95914]
del forms[95914]
routes = {e: (u, v) for e, u, v in w['moves'] if e != 95914}
routes.update({94019: (3, 278), 90369: (3, 304), 88: (278, 127)})
observer = max(schedule)+1
schedule.insert(schedule.index(90369)+1, observer)
routes[observer] = (3, 282)
forms[94019] = {~1288: F(1)}
forms[90369] = old_forms[94019].copy()
forms[88] = {**old_forms[95914], 94019: F(-845660160)}
forms[observer] = old_forms[90369].copy()
for e in schedule:
    if e in (94019, 90369, 88, observer):
        continue
    if 94019 in forms[e]:
        forms[e][90369] = forms[e].pop(94019)
    if 90369 in old_forms[e]:
        forms[e][observer] = forms[e].pop(90369)
ends = [w['first_output']+i for i in range(n)]
terminal_chart = dict(zip(ends, w['final']))
holders = {~j: chart for j, chart in enumerate(w['initial'])}
for e in schedule:
    chart = routes[e][0] if e in routes else terminal_chart[e]
    need(all(holders.get(j) == chart for j in forms[e]), 'actual local operands '+str(e))
    if e in routes:
        holders[e] = routes[e][1]
candidates = [86, 97232, 97241, 97323, 99064]
pos = {e: j for j, e in enumerate(candidates)}


def backward(slot, rows, order, capture=True):
    weights = {slot: F(1)}
    exposures = [F(0)]*5
    for e in reversed(order):
        q = weights.pop(e, 0)
        if e in pos and capture:
            exposures[pos[e]] = q
        if q:
            add(weights, rows[e], q)
    need(all(j < 0 for j in weights), 'complete backwards source expansion')
    return {~j: q for j, q in weights.items()}, exposures


E, B = [], []
for slot in ends:
    row, response = backward(slot, forms, schedule)
    old, _ = backward(slot, old_forms, w['schedule'], False)
    need(row == old, 'compensated full target '+str(slot))
    E.append(row)
    B.append(response)
print('Reconstructed all 1289 endpoints by reverse DAG expansion.', flush=True)
# Sparse elimination of the complete target, without component inversion.
pivots = {}
for i, entry in reversed(list(enumerate(E))):
    row, right = entry.copy(), {i: F(1)}
    while row:
        j = min(row)
        q = row[j]
        if j not in pivots:
            pivots[j] = ({k: x/q for k, x in row.items()}, {k: x/q for k, x in right.items()})
            break
        left, previous = pivots[j]
        add(row, left, -q)
        add(right, previous, -q)
    else:
        raise ValueError('singular complete endpoint')
need(set(pivots) == set(range(n)), 'all source pivots')
inverse = [{} for _ in range(n)]
for j in reversed(range(n)):
    row, right = pivots[j]
    inverse[j] = right.copy()
    for k, x in row.items():
        if k != j:
            add(inverse[j], inverse[k], -x)


def product(left, right):
    out = []
    for row in left:
        value = {}
        for j, q in row.items():
            add(value, right[j], q)
        out.append(value)
    return out


identity = [{j: F(1)} for j in range(n)]
need(product(E, inverse) == product(inverse, E) == identity, 'two complete inverse identities')

# New source-hub interface checks, using the complete independently inverted E.
X=[j for j,c in enumerate(w['initial']) if c==3];Y=[j for j,c in enumerate(w['initial']) if c!=3]
A=[i for i,c in enumerate(w['final']) if c!=127];Z=[i for i,c in enumerate(w['final']) if c==127]
need((len(X),len(Y),len(A),len(Z))==(908,381,387,902),'exact source and terminal populations')
need(w['initial'].count(127)==0,'final chart127 has no original source fields')
need(not any(a==127 for a,b in routes.values()) and not any(b==3 for a,b in routes.values()),'baseline chart boundary')
need(sum(b==127 for a,b in routes.values())==902,'all final chart127 stock fields')
Xset=set(X);Aset=set(A);Zset=set(Z);eligible=[];fixed=[]
for i in A:
    rows=[j for j in X if inverse[j].get(i)]
    need(len(rows)<=1,'one own-input row per outside inverse column')
    if rows:eligible.append({'outside_coordinate':i,'terminal':ends[i],'input_axis':rows[0],'inverse_coefficient':str(inverse[rows[0]][i])})
    else:fixed.append({'outside_coordinate':i,'terminal':ends[i]})
need(len(eligible)==376 and len(fixed)==11 and len({e['input_axis'] for e in eligible})==376,'distinct pinned source columns')
free=sorted(Xset-{e['input_axis'] for e in eligible});free_inside=[]
for j in free:
    need(len(inverse[j])==1,'free input is an output singleton')
    i=next(iter(inverse[j]));need(i in Zset and all(not E[a].get(j) for a in A),'free singleton affects no outside target')
    need({k for k in range(n) if inverse[k].get(i)}=={j},'free stock column has no pinned or external baseline')
    free_inside.append({'input_axis':j,'inside_coordinate':i,'terminal':ends[i],'inverse_coefficient':str(inverse[j][i])})
need(len(free)==532 and len({e['inside_coordinate'] for e in free_inside})==532,'independent free singleton stock coordinates')
fixed_inside=sorted(Zset-{e['inside_coordinate'] for e in free_inside});need(len(fixed_inside)==370,'fixed stock columns')
# Sparse rank independently certifies the actual export basis.
def sparse_rank(rows):
    piv={}
    for input_row in rows:
        r=input_row.copy()
        while r:
            j=max(r);value=r[j]
            if j not in piv:piv[j]={k:v/value for k,v in r.items()};break
            add(r,piv[j],-value)
    return len(piv)
need(sparse_rank([{j:v for j,v in E[i].items() if j in Xset} for i in A])==376,'exact outside-target own-input rank for the corollary')
old_exports=sorted(e for e,a,b in w['moves'] if a==3);exports=sorted(e for e,(a,b) in routes.items() if a==3)
need(len(old_exports)==908 and len(exports)==909 and observer==156057,'actual original and paid source export count')
perm={e:e for e in exports if e!=94019};perm[90369]=94019;perm[observer]=90369
need(set(perm.values())==set(old_exports) and len(perm)==908,'exact payload row permutation')
need(all(forms[e]==old_forms[f] for e,f in perm.items()),'literal original payloads retained')
need(all(all(j<0 and ~j in Xset for j in forms[e]) for e in exports),'all baseline source exports are local original inputs')
need(sparse_rank([forms[e] for e in perm])==908,'actual square original payload matrix full rank')
Frows=[]
for e in exports:
    r={~j:v for j,v in forms[e].items()}
    if e==94019:r[n]=F(1,845660160)
    Frows.append(r)
need(sparse_rank(Frows)==909,'full formal control basis')
need(sparse_rank([{k:v for k,v in r.items() if k!=n} for r in Frows])==908,'deleted formal coordinate loses one basis dimension')
source=json.loads((pkg.parent/'author/output/RESULT.json').read_text())
for key,value in [('input_chart_3_axes',X),('other_input_axes',Y),('outside_127_terminal_slots',[ends[i] for i in A]),('chart_127_terminal_slots',[ends[i] for i in Z]),('outside_coordinates_with_one_chart_3_input',eligible),('outside_coordinates_without_chart_3_input',fixed),('free_chart_3_singleton_columns',free_inside),('fixed_inside_coordinates',fixed_inside)]:need(source[key]==value,'literal source-interface agreement '+key)
result={'status':'PASS_ROOT_SOURCE_HUB_COMPLETION_INTERFACE','complete_endpoint_fields':1289,'source_chart3_inputs':908,'other_inputs':381,'outside_outputs':387,'chart127_outputs':902,'pinned_source_columns':376,'outside_target_own_input_rank':376,'free_source_columns':532,'fixed_stock_columns':370,'original_export_basis_rank':908,'formal_export_basis_rank':909,'new_author_code_imported':False,'retained_independent_reverse_DAG_method_reused':True,'conditional_full_rank_C_criterion_reviewed':True,'candidate_surrounding_C_rank_verified':False,'complete_repaired_word':False,'new_complete_kappa':False}
args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],908,381,387,902,376,532,370,flush=True)
