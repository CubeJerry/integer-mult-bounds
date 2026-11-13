#!/usr/bin/env python3
"""Independent exact dual checker: no Gaussian elimination or price imports."""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import gzip,json
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
PIN='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9'
def need(ok,label):
    if not ok:raise ValueError(label)
def key(frame):
    values={0}
    for v in frame:values|={x^v for x in values}
    return frozenset(values)
def pair(row,probe):return sum((Q(v)*probe.get(int(j),0) for j,v in row.items()),Q(0))
def run():
    raw=(ROOT/'reference/pr7481/WORD.json.gz').read_bytes();need(sha256(raw).hexdigest()==PIN,'actual source bytes');w=json.loads(gzip.decompress(raw));classes=list(map(key,w['frames']))
    result=json.loads((HERE/'RESULT.json').read_text());cold=set(result['cold_helpers']);need(len(cold)==72,'cold set')
    paths={'targets':ROOT/'independent-temporal-result.json','history':ROOT/'worker-b/history-cache/FILTER.json','two':ROOT/'worker-b/two-cache/FILTER.json','joint':ROOT/'worker-a/cold-compose/JOINT72-ZERO-CONTACTS.json','single':ROOT/'worker-b/cold-single/SCAN.json','projected':ROOT/'projected-temporal-result.json'}
    data={}
    for name,path in paths.items():
        raw=path.read_bytes();need(sha256(raw).hexdigest()==result['input_sha256'][name],'frozen source receipt '+name);data[name]=json.loads(raw);need(data[name]['source_sha256']==PIN,'source pin '+name)
    targets={r['event']:r for r in data['targets']['records']};two={r['event'] for r in data['two']['records']};events={r['event'] for r in data['projected']['records'] if r['earlier_B_hit']}
    need(events=={r['event'] for r in result['records']} and len(events)==14,'all14 projected candidates')
    checked=0;controls=0
    for record in result['records']:
        event=record['event'];t=targets[event];probe={int(j):Q(v) for j,v in record['integer_retained_input_dual'].items()}
        need(not set(probe)&cold,'cold coordinates zero');need(w['program'][event]==['MOVE',t['owner'],t['source'],t['destination'],True],'actual owned cut')
        origin=data['two'] if event in two else data['history'];field='earlier_generators' if event in two else 'generators'
        rows=[g for g in origin[field] if g['event']<event and classes[g['frame']]==classes[t['destination']]]
        need(len(rows)==record['history_generator_count'],'complete strict history coverage')
        need(all(pair(g['row'],probe)==0 for g in rows),'every complete history row annihilated')
        v=pair(t['target'],probe);need(v and v==Q(record['dual_target_value']),'target separated')
        # Contamination with the target itself must fail the zero-history rule.
        need(not all(pair(row,probe)==0 for row in [g['row'] for g in rows]+[t['target']]),'inserted-target negative control');controls+=1;checked+=1
    single=[r for r in data['single']['records'] if r['removed_paid']=={str(r['target_rank']):1}]
    union={m['event'] for r in single for m in r['pure_move_events']};need(len(union)==72 and union==set(result['zero_MOVE_events']),'singleton/joint zero event equality')
    need(result['target_debit_histogram']==result['zero_MOVE_credit_histogram'],'histogram cancellation')
    out={'status':'PASS_INDEPENDENT_PROJECTED_HISTORY_DUALS','dual_certificates_checked':checked,'inserted_target_negative_controls':controls,'joint72_zero_events_equal_singleton_union':True,'no_gaussian_elimination':True,'no_price_engine_import':True}
    (HERE/'CERTIFICATE-VALIDATION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
