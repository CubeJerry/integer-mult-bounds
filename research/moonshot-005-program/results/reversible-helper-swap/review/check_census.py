#!/usr/bin/env python3
"""Independent certificate join and source-route reconstruction; no author imports."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
RESULTS = ROOT / 'research/moonshot-005-program/results'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    raw = path.read_bytes()
    payload = gzip.decompress(raw) if path.suffix == '.gz' else raw
    return json.loads(payload), hashlib.sha256(raw).hexdigest(), hashlib.sha256(payload).hexdigest()


def span(frame):
    result = [0]
    for vector in frame:
        result = list(set(result + [a ^ vector for a in result]))
    return tuple(sorted(result))


def main():
    source, source_hash, _ = load(ROOT / 'research/shared-wire-split-composition/data/final.json.gz')
    edges, _, edge_payload_hash = load(RESULTS / 'endpoint-side-information/RESULT.json.gz')
    losses, loss_hash, loss_payload_hash = load(RESULTS / 'single-overwrite-loss/CERTIFICATE.json.gz')
    need(source_hash == '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883', 'source pin')
    need(edge_payload_hash == '58186c21ef28a9ae71e8c14dd82c12a01bf50f33db28e23eadc23755e905b139', 'neutral payload pin')
    need(loss_hash == '8a500a84ec0b1dd3a10c38278d522908ccfc8f999625edff4d02fa1a898e7181', 'reviewed overwrite certificate pin')
    first = {}
    canonical = []
    for index, frame in enumerate(source['frames']):
        key = span(frame)
        first.setdefault(key, index)
        canonical.append(first[key])
    routes = [[canonical[start]] for start in source['initial']]
    for operation in source['program']:
        if operation[0] == 'MOVE' and operation[1] < source['public']:
            routes[operation[1]].append(canonical[operation[3]])
    for role, recorded in edges['raw_itineraries'].items():
        need(routes[int(role)] == recorded, 'independently reconstructed raw route')
    xs = set(source['live'])
    ys = {i + 112 for i in xs}
    need(set(edges['column_order_donor_X']) == xs, 'active X census')
    flags = {record['event']: record for record in losses['records']}
    neutral = edges['edge_certificate']['public_neutral']
    need(len(neutral) == len(flags) == 1472, 'neutral cardinality')
    keep = [edge for edge in neutral if flags[edge['event']]['hub_recoverable_payload']]
    target_counts = Counter(edge['target'] for edge in keep)
    need(len(keep) == 824 and target_counts == Counter({127: 822, 246: 2}), '824/822/2 census')
    direct_pairs = []
    for edge in keep:
        op = source['program'][edge['event']]
        need(op[0] == 'MOVE' and op[1] == edge['role'], 'source event and helper identity')
        need(canonical[op[2]] == edge['source'] and canonical[op[3]] == edge['target'], 'source charts')
        for donor in xs:
            if edge['source'] in routes[donor]:
                for receiver in ys:
                    if edge['target'] in routes[receiver]:
                        direct_pairs.append([edge['event'], donor, receiver])
    need(not direct_pairs, 'no direct active X to active Y swap candidate')
    chart_membership = {}
    for chart in [127, 246, 902, 930]:
        chart_membership[str(chart)] = {'X': sorted(i for i in xs if chart in routes[i]), 'Y': sorted(i for i in ys if chart in routes[i])}
    need(chart_membership['246'] == {'X': [54, 69], 'Y': []}, 'target246 roles')
    need(chart_membership['902'] == {'X': [], 'Y': [129, 150]}, 'source902 roles')
    need(chart_membership['930'] == {'X': [], 'Y': [117, 181]}, 'source930 roles')
    result = {'status': 'PASS_INDEPENDENT_NEUTRAL_HUB_PAYLOAD_CENSUS', 'source_sha256': source_hash, 'neutral_payload_sha256': edge_payload_hash, 'loss_certificate_sha256': loss_hash, 'loss_certificate_payload_sha256': loss_payload_hash, 'source_raw_routes_checked': len(edges['raw_itineraries']), 'hub_recoverable_count': len(keep), 'target_counts': dict(target_counts), 'nonhub_events': [edge for edge in keep if edge['target'] != 127], 'chart_membership': chart_membership, 'direct_X_to_Y_candidates': direct_pairs, 'scope': 'Joins reviewed exact neutral/payload certificates and independently rebuilds source routes. Excludes only a direct one-neutral-MOVE active-X to active-Y swap with hub-recoverable displaced payload. Does not reprove the complete pulse census or exclude changed receiver modules, other records or paid routes.'}
    Path(__file__).with_name('CENSUS-CHECK.json').write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'])
    print(json.dumps({key: result[key] for key in ['hub_recoverable_count', 'target_counts', 'source_raw_routes_checked', 'nonhub_events', 'direct_X_to_Y_candidates']}, indent=2))


if __name__ == '__main__':
    main()
