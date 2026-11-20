#!/usr/bin/env python3
"""Independent rational source and four-space export-cut verification.

Reuses only the earlier independent review's sparse Fraction arithmetic and
authenticated original-source reader. No current or predecessor author
checker, graph class or surgery constructor is imported.
"""
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import gzip
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

PRIOR = 'research/moonshot-005-program/results/complex-native-static-route-cut/review-b/check.py'
PRIOR_HASH = '39aebe9941bd1b4551f0194f8ce010a76d682ac441d911cc0d1206efd573e04d'
SOURCE = 'research/moonshot-005-program/results/complex-native-contested-restoration/rail/sources'
PINS = {
    'DOUBLE-CANDIDATE.json.gz': '1b1b3294e86979f1f41076fb056f3c0a08ace6df7bf80f2886bc579a22962f4b',
    'DOUBLE-APPLICATION.json.gz': '69596ca0289d3164b0149cd7b0bbed8b8775243d6af8817088006df334c8962e',
}

def need(value, reason):
    if not value:
        raise ValueError(reason)

def load_module(path):
    spec = importlib.util.spec_from_file_location('prior_independent_static_review', path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

def evaluate(data, forms, routes, schedule, arithmetic):
    """Separate sparse evaluation with unlimited local histories and guards."""
    n = len(data['initial'])
    values = {~j: {j: Fraction(1)} for j in range(n)}
    places = {~j: c for j, c in enumerate(data['initial'])}
    outputs = {data['first_output']+j: c for j, c in enumerate(data['final'])}
    need(set(schedule) == set(forms) == set(routes) | set(outputs), 'complete changed inventory')
    need(len(schedule) == len(set(schedule)), 'unique changed schedule')
    spans = arithmetic.subspaces(data['frames'])
    for event in schedule:
        chart = routes[event][0] if event in routes else outputs[event]
        row = {}
        for operand, scalar in forms[event].items():
            need(operand in values and places[operand] == chart and scalar, 'literal changed stock ownership')
            arithmetic.axpy(row, scalar, values[operand])
        if event in routes:
            a, b = routes[event]
            need(spans[a] < spans[b] or spans[b] < spans[a], 'changed movement joins nested charts')
            places[event] = b
        else:
            places[event] = chart
        values[event] = row
    return [values[data['first_output']+j] for j in range(n)]

def surgery(data, shadow):
    """Explicit literal changes, checked against the full target by replay."""
    forms = {e: {o: Fraction(q) for o, q in row} for e, row in data['forms']}
    routes = {e: (u,v) for e,u,v in data['moves']}
    readers = lambda e: [r for r in data['schedule'] if e in forms[r]]
    need(readers(95914) == [88], 'retired channel sole original use')
    need(readers(94019) == [94034,156055], 'all retarget source duties')
    need(readers(90369) == [91110,98703,94251], 'all withdrawn observer duties')
    retarget_readers, observer_readers = readers(94019), readers(90369)
    old_observer = forms[90369].copy()
    old_observer_route = routes[90369]
    old_retarget = forms[94019].copy()
    retired = forms[95914].copy()
    schedule = [e for e in data['schedule'] if e != 95914]
    del forms[95914], routes[95914]
    routes[94019] = (3,278)
    routes[90369] = (3,304)
    routes[88] = (278,127)
    forms[94019] = {~1288: Fraction(1)}
    forms[90369] = old_retarget
    need(94019 not in retired, 'new outlet incidence is distinct')
    forms[88] = retired | {94019: Fraction(-845660160)}
    for event in retarget_readers:
        need(90369 not in forms[event], 'distinct replacement observer')
        forms[event][90369] = forms[event].pop(94019)
    extra = None
    if shadow:
        extra = max(schedule)+1
        need(extra not in forms, 'fresh real shadow channel')
        schedule.insert(schedule.index(90369)+1, extra)
        routes[extra] = old_observer_route
        forms[extra] = old_observer
        for event in observer_readers:
            forms[event][extra] = forms[event].pop(90369)
    else:
        for event in observer_readers:
            del forms[event][90369]
    return forms, routes, schedule, extra

def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--repo',type=Path,required=True)
    cli.add_argument('--out',type=Path,required=True)
    args = cli.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    raw = (args.repo/PRIOR).read_bytes()
    need(sha256(raw).hexdigest() == PRIOR_HASH, 'prior independent reader pin')
    arith = load_module(args.repo/PRIOR)
    objects = {}
    for name,pin in PINS.items():
        raw = (args.repo/SOURCE/name).read_bytes()
        need(sha256(raw).hexdigest() == pin, 'source pin '+name)
        objects[name] = json.loads(gzip.decompress(raw))
    data = objects['DOUBLE-CANDIDATE.json.gz']
    application = objects['DOUBLE-APPLICATION.json.gz']
    need(application['word_sha256'] == sha256(gzip.decompress((args.repo/SOURCE/'DOUBLE-CANDIDATE.json.gz').read_bytes())).hexdigest(), 'caller binds source bytes')
    full = arith.source_transfer(data, application)
    full_rank = arith.rank(full)
    need(full_rank == 1289, 'complete public target invertible')
    spans = arith.subspaces(data['frames'])
    inside = {frozenset({0}),frozenset({0,261}),frozenset({0,296}),frozenset({0,45,261,296})}
    aliases = [j for j,span in enumerate(spans) if span in inside]
    need(aliases == [3,11,58,278] and spans[282] not in inside, 'all four canonical chart spaces and outside destination')
    born = {j for j,c in enumerate(data['initial']) if spans[c] in inside}
    finished = {j for j,c in enumerate(data['final']) if spans[c] in inside}
    birth_counts = Counter(data['initial'][j] for j in born)
    need(birth_counts == {3:908,11:2,58:2} and not finished, 'actual independent inputs and no inside outputs')
    restricted = arith.block(full,range(1289),born)
    need(arith.rank(restricted) == 912, 'full target restricted to all inside originals')
    original = {e:(u,v) for e,u,v in data['moves']}
    four_forms,four,four_schedule,_ = surgery(data,False)
    five_forms,five,five_schedule,extra = surgery(data,True)
    four_endpoint = evaluate(data,four_forms,four,four_schedule,arith)
    five_endpoint = evaluate(data,five_forms,five,five_schedule,arith)
    need(five_endpoint == full and four_endpoint != full, 'authentic fifth-channel positive and incomplete four-channel negative controls')
    exports = lambda routes: {e for e,(u,v) in routes.items() if spans[u] in inside and spans[v] not in inside}
    old_exports,new_exports,five_exports = map(exports,(original,four,five))
    need((len(old_exports),len(new_exports),len(five_exports)) == (912,911,912), 'exact whole-field export capacities')
    changes = []
    for event in sorted(set(original)|set(four)):
        if original.get(event) != four.get(event):
            changes.append({'slot':event,'old':original.get(event),'new':four.get(event),'old_export':event in old_exports,'new_export':event in new_exports})
    need([v['slot'] for v in changes] == [88,90369,94019,95914], 'exact surgery route scope')
    need(sum(int(v['new_export'])-int(v['old_export']) for v in changes) == -1, 'one lost export')
    forms = {e:dict(row) for e,row in data['forms']}
    clock = {event:t for t,event in enumerate(data['schedule'])}
    first_use = next(event for event in data['schedule'] if 90369 in forms[event])
    grade = lambda route: abs(len(data['frames'][route[0]])-len(data['frames'][route[1]]))
    donors = [event for event in data['schedule'] if event in original and original[event][0] == 3 and clock[event] < clock[first_use] and grade(original[event]) >= 3 and event not in {94019,90369}]
    wide = [event for event,route in four.items() if route[0] == 3 and grade(route) >= 3]
    need(len(donors) == 181 and len(wide) == 182, 'complete early and unrestricted high-grade rosters')
    for event in wide:
        u,v = four[event]
        need(event in new_exports and spans[v] not in inside and spans[282] not in inside, 'each eligible old and new destination outside')
    simultaneous = four | {event:(3,282) for event in donors}
    need(exports(simultaneous) == new_exports, 'all simultaneous redirections preserve the export set')
    need(extra in five_exports and five[extra] == (3,282), 'genuine paid additional export')
    author_path = Path(__file__).resolve().parent.parent/'author/output/RESULT.json'
    author = json.loads(author_path.read_text())
    need(author['export_slots'] == sorted(new_exports) and author['eligible_donors'] == donors, 'independent literal export and donor lists match')
    need(author['actual_extra_channel'] == extra, 'positive-control channel identity')
    receipt = {
        'status':'PASS_INDEPENDENT_FULL_SOURCE_EXPORT_CUT',
        'full_public_columns':1289, 'full_target_rank':full_rank,
        'target_row_digest':arith.digest(full), 'inside_charts':aliases,
        'inside_input_counts':dict(sorted(birth_counts.items())),
        'inside_inputs':len(born), 'inside_outputs':len(finished),
        'restricted_target_rank':912, 'export_capacities':[912,911,912],
        'surgery_changes':changes, 'eligible_donors':donors,
        'eligible_grade_histogram':dict(sorted(Counter(grade(four[e]) for e in donors).items())),
        'all_high_grade_chart3_donors':len(wide),
        'new_export_slots':sorted(new_exports), 'genuine_shadow_slot':extra,
        'positive_control_exact_on_all_1289_columns':True,
        'four_channel_endpoint_differs':True,
        'all_subset_crossing_indicators_unchanged':True,
        'required_extra_export_per_positive_width':1,
        'prior_independent_reader_sha256':PRIOR_HASH,
        'source_pins':PINS, 'new_complete_kappa':False,
    }
    (args.out/'RESULT.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(receipt['status'],1289,912,911,181,flush=True)

if __name__ == '__main__':
    main()
