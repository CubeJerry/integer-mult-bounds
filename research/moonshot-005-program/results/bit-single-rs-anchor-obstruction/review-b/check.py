#!/usr/bin/env python3
"""Independent finite witness and physical-capacity audit for all 99 anchors.

The separately authored prior independent review supplies field arithmetic,
synthetic polynomial division and descending-pivot elimination. No author
module from either source-fibre package is imported. The nonlinear proof is
reviewed separately in REVIEW.md; this executable checks its finite premises.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import gzip
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

PINS = {
    'geometry': ('bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',
                 '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'),
    'routes': ('bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz',
               '6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'),
    'phases': ('bit-asymmetric-balanced-atlas/author/output/PLANE-PHASES.json',
               'bae4a03a923abfc840e0d030093bdb635eb948de312697b5a08d0338bcc83cf6'),
    'target': ('bit-two-sided-covariant-target/author/output/ASSIGNMENT.json',
               'deabb7ac9cf8429981b4f28de015723c33399f9ea5c838a34621886ea5c74601'),
    'target_proof': ('bit-two-sided-covariant-target/author/PROOF.md',
                     '2c2e9b1cbbe3dee1c15f69697c6b01da1b653c82fc18f3c0d452a99633038468'),
    'RS_source': ('bit-spread-rs-physical-word/author/rs_source.py',
                  'a51189b6d5422ec07fb2fedc822dc856e3277ea8ae0631894c34464419b8c7f9'),
    'RS_proof': ('bit-spread-rs-physical-word/author/RS-SOURCE.md',
                 '432e19d4d11e6068eac7bea94dba459464e804b539634be54824c30f25f7fcae'),
    'prior_independent_checker': ('bit-rs-source-fibre-census/review-large-kappa/check.py',
                                  '2408c2321a112d6aff8d2ca9d0a54ea235572cf54cf9da6886cd9c60f8cfc489'),
    'prior_independent_result': ('bit-rs-source-fibre-census/review-large-kappa/RESULT.json',
                                 '90edc4023d98b4282ce72450d0bd1832414b9c9ffa30201c0dd08ddde77fc1c0'),
    'witnesses': ('bit-single-rs-anchor-obstruction/author/WITNESSES.json.gz',
                  'c74e4cd954ed1d68d7be46dc35290241558c785ff22c37e25061ecb379f26798'),
}

def need(value, message):
    if not value:
        raise ValueError(message)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    base = args.repo / 'research/moonshot-005-program/results'
    payload = {}
    for key, (name, expected) in PINS.items():
        raw = (base / name).read_bytes()
        if name.endswith('.gz'):
            raw = gzip.decompress(raw)
        need(sha256(raw).hexdigest() == expected, 'source hash ' + key)
        payload[key] = raw
    spec = importlib.util.spec_from_file_location('independent_predecessor', base / PINS['prior_independent_checker'][0])
    field = importlib.util.module_from_spec(spec); spec.loader.exec_module(field)
    geometry = json.loads(payload['geometry'])
    roots = geometry['root_table']; planes = list(map(frozenset, geometry['A2']))
    middles = list(map(frozenset, geometry['D4'])); dual = geometry['dual_D4']
    native = set(range(111))
    perp = [{k for k, y in enumerate(roots) if sum(a*b for a, b in zip(x, y)) == 0} for x in roots]
    stars = {j: [h for h, H in enumerate(planes) if j in H] for j in native}
    nodes = {j: {h: n+1 for n, h in enumerate(stars[j])} for j in native}
    audience = [native.intersection(*(perp[j] for j in H)) for H in planes]
    singleton = {next(iter(H & native)) for H in planes if len(H & native) == 1}
    anchors = native - singleton - {10}
    views = {(j, i): [h for h in stars[j] if i in audience[h]] for j in native for i in perp[j] & native}
    need(len(anchors) == 99 and len(singleton) == 11, 'ordinary anchor universe')
    need(all(len(v) == 28 for v in stars.values()), 'all native 28-plane stars')
    need(len(views) == 6470 and all(len(v) == 16 for v in views.values()), 'all real 16-plane receiver views')
    signed_roots = {tuple(x): j for j, x in enumerate(roots)}
    signed_roots.update({tuple(-a for a in x): j for j, x in enumerate(roots)})
    need(len(signed_roots) == 240 and all(sum(a*a for a in x) == 4 for x in roots), '120 norm-four root lines')
    reflections = []
    for c in roots:
        permutation = []
        for x in roots:
            dot = sum(a*b for a, b in zip(c, x))
            twice_image = [2*a-dot*b for a, b in zip(x, c)]
            need(all(a % 2 == 0 for a in twice_image), 'integral native reflection')
            image = tuple(a//2 for a in twice_image)
            need(image in signed_roots, 'reflection closes on actual root lines')
            permutation.append(signed_roots[image])
        need(len(set(permutation)) == 120 and all(permutation[permutation[j]] == j for j in range(120)),
             'literal root-line reflection involution')
        reflections.append(permutation)
    target = json.loads(payload['target'])
    modified = {tuple(x[:2]) for x in target['row_transfers'] + target['column_transfers']}
    modified |= {tuple(x) for x in target['internal_edges']}
    need(len(modified) == 123 and all(i == 80 or j == 10 for i, j in modified), 'actual exact-identity target domain')
    need(all(i in perp[j] for i, j in modified), 'modified targets are actual foreign pairs')

    # Independently recheck the source and H cut widths actually needed by the
    # generalized tightness lemma, including the two chronological phases.
    phases = json.loads(payload['phases'])
    routes = [json.loads(line) for line in payload['routes'].splitlines()]
    seen_owners = set(); outgoing = defaultdict(Counter); incoming = Counter()
    for kind, role, local, h, d, k, line, terminal in routes:
        owner = (kind, role, local)
        need(owner not in seen_owners and kind in {'X', 'Y'} and role in native and 0 <= local < 480,
             'one actual route for each original field owner')
        seen_owners.add(owner)
        if h is not None:
            need(planes[h] <= middles[d], 'source H to D containment')
            outgoing[h, d][kind] += 1
            if line is not None:
                need(line in planes[h] & native, 'actual source donor line')
                incoming[line, h, kind] += 1
        if k is not None:
            need(planes[k] <= middles[dual[d]], 'D to K perpendicular containment')
            if terminal is not None:
                need(terminal in planes[k] & native, 'actual native receiver line')
    need(len(seen_owners) == 106560, 'all physical owners covered')
    for d, D in enumerate(middles):
        need(set.intersection(*(perp[j] for j in D)) == set(middles[dual[d]]), 'exact real D perpendicular')
    cut_counts = 0
    for h, H in enumerate(planes):
        ports = [d for d, D in enumerate(middles) if H <= D]
        need(len(ports) == 45, '45 actual H output ports')
        phase = phases[str(h)]
        for d in ports:
            need(outgoing[h, d]['X'] == phase['early'] and outgoing[h, d]['Y'] == phase['late'],
                 'actual two-phase port owners')
            need(sum(outgoing[h, d].values()) == 2, 'two total fields per port')
        for i in audience[h]:
            visible = [d for d in ports if middles[d] <= perp[i]]
            need(len(visible) == 15 and sum(sum(outgoing[h, d].values()) for d in visible) * 8 == 240,
                 'tight whole H-to-receiver cut')
            cut_counts += 1
    for j in anchors:
        need(sum(incoming[j, h, 'X'] for h in stars[j]) == 480, 'one original early donor bank')
        need(all(incoming[j, h, 'X'] + incoming[j, h, 'Y'] == 30 for h in stars[j]),
             'each ordinary source quotient has exactly 240 field slots at eight copies')
    print('PASS_PHYSICAL_SOURCE_AND_MIXED_PHASE_TIGHT_CAPACITIES', cut_counts, flush=True)

    @lru_cache(None)
    def fibre(j, h, i):
        need(h in views[j, i], 'shared plane actually visible to anchor receiver')
        full = field.annihilator([nodes[j][q] for q in views[j, i]])
        value = field.divide_linear(full, nodes[j][h])
        need(len(value) == 16 and value[-1] == 1, 'actual monic degree-15 anchor fibre')
        need(all(bool(field.evaluate(value, nodes[j][q])) == (q == h) for q in views[j, i]),
             'exact 15-node fibre zero set')
        return value

    witnesses = json.loads(payload['witnesses'])['witnesses']
    seen = set(); summaries = []; propagation_count = 0; intersection_histogram = Counter(); controls = {}
    for witness in witnesses:
        anchor = witness['anchor']; left, right = witness['leaf_donors']
        h_left, h_right, h_final = witness['centres']; final_receiver = witness['final_receiver']
        need(anchor in anchors and anchor not in seen, 'one exact witness per ordinary anchor')
        need(left in anchors and right in anchors and len({anchor, left, right}) == 3, 'three distinct ordinary nonexceptional donors')
        need(len({h_left, h_right, h_final}) == 3, 'three distinct native triangle planes')
        need({anchor, left} <= planes[h_left] and {anchor, right} <= planes[h_right]
             and {left, right} <= planes[h_final], 'literal triangle incidences')
        need(final_receiver != 80 and final_receiver in audience[h_final] and final_receiver not in perp[anchor],
             'final receiver sees both leaves but not the anchor')
        branches = witness['propagations']; need(len(branches) == 2, 'both propagation arms')
        mapped_sets = []
        for branch, leaf, centre in zip(branches, [left, right], [h_left, h_right]):
            need(branch['leaf'] == leaf and branch['centre'] == centre, 'propagation arm binding')
            third = planes[centre] - {anchor, leaf}
            need(len(third) == 1, 'unique third root of centre')
            permutation = reflections[next(iter(third))]
            need(permutation[anchor] == leaf and permutation[leaf] == anchor, 'reflection exchanges the two source lines')
            need({permutation[x] for x in planes[centre]} == planes[centre], 'reflection preserves the centre plane')
            expected = set(views[leaf, final_receiver]) - {h_final}
            need(len(expected) == 15 and centre not in expected, '15 actual off-final quotients avoid anchor centre')
            records = branch['quotient_propagations']; need(len(records) == 15, 'exactly 15 needed propagations')
            used = set(); mapped = []
            for record in records:
                q = record['leaf_plane']; r = record['anchor_plane']; receivers = record['receivers']
                need(q in expected and q not in used and q != centre, 'each needed leaf quotient exactly once')
                need(r in stars[anchor] and r != centre, 'genuine off-centre anchor quotient')
                need({permutation[x] for x in planes[q]} == planes[r], 'actual reflected source-plane map')
                need(len(receivers) == len(set(receivers)) == 15 and 80 not in receivers,
                     '15 distinct nonexceptional propagation receivers')
                need(set(receivers) <= audience[centre] & audience[q], 'actual simultaneous centre/leaf visibility')
                need(all(permutation[i] == i and i in audience[r] for i in receivers),
                     'propagation receivers fixed by reflection and see the anchor plane')
                vectors = [fibre(anchor, centre, i) for i in receivers]
                need(field.row_rank(vectors) == record['rank'] == 15, 'independent rank-15 propagation span')
                need(all(field.evaluate(v, nodes[anchor][r]) == 0 for v in vectors), 'span lies in claimed evaluation kernel')
                if not controls:
                    duplicate_rank = field.row_rank(vectors[:-1] + [vectors[0]])
                    need(duplicate_rank == 14, 'duplicated propagation receiver loses rank')
                    wrong_kernel = all(field.evaluate(v, nodes[anchor][centre]) == 0 for v in vectors)
                    need(not wrong_kernel, 'central evaluation cannot replace propagated kernel')
                    controls = {'duplicate_receiver_rank': duplicate_rank, 'wrong_central_kernel_rejected': True}
                used.add(q); mapped.append(r); propagation_count += 1
            need(used == expected and len(set(mapped)) == 15, 'exact off-final coverage and 15 distinct forced anchor quotients')
            mapped_sets.append(set(mapped))
        reported = list(map(set, witness['distinct_anchor_plane_sets']))
        need(mapped_sets == reported and mapped_sets[0] != mapped_sets[1], 'two different actual anchor plane sets')
        final_polynomials = [field.annihilator([nodes[anchor][q] for q in sorted(S)]) for S in mapped_sets]
        need(all(len(v) == 16 and v[-1] == 1 for v in final_polynomials), 'two monic degree-15 final fibres')
        need(field.row_rank(final_polynomials) == witness['final_fibre_rank'] == 2, 'distinct final fibre directions')
        need(field.row_rank([final_polynomials[0], final_polynomials[0]]) == 1, 'equal plane-set control removes contradiction')
        overlap = len(mapped_sets[0] & mapped_sets[1]); intersection_histogram[overlap] += 1
        summaries.append({'anchor': anchor, 'leaves': [left, right], 'centres': [h_left, h_right, h_final],
                          'final_receiver': final_receiver, 'mapped_set_intersection': overlap,
                          'final_fibres': [list(v) for v in final_polynomials]})
        seen.add(anchor)
    need(seen == anchors and len(witnesses) == 99 and propagation_count == 2970, 'complete 99-anchor finite census')
    author_path = Path(__file__).resolve().parent.parent / 'author/output/RESULT.json'
    author_raw = author_path.read_bytes(); author = json.loads(author_raw)
    need(author['actual_ordinary_anchor_ids'] == sorted(seen) and author['source_kernel_rank_counts'] == {'15': 2970},
         'author receipt agrees with independently reconstructed census')
    expected_triangles = [{'anchor': row['anchor'], 'leaves': row['leaves'], 'centres': row['centres'],
                          'receiver': row['final_receiver'], 'common_final_plane_count': row['mapped_set_intersection']}
                         for row in summaries]
    need(author['triangle_witnesses'] == expected_triangles, 'all 99 author triangle summaries independently matched')
    prior = json.loads(payload['prior_independent_result'])
    packing_counts = [{'centres': row['charts'], 'changed_in_J': row['special_in_J'],
                       'retained_in_J': row['retained_in_J'],
                       'further_changes_required': row['retained_in_J']}
                      for row in prior['packing_counts']]
    need([row['further_changes_required'] for row in packing_counts] == [31, 32, 24, 29],
         'new consequence for independently reviewed retained source sets')
    result = {'status': 'PASS_INDEPENDENT_FINITE_SINGLE_ANCHOR_CENSUS',
              'proof_admission': 'See separate REVIEW.md; executable checks finite premises only.',
              'new_author_python_imported': False, 'prior_independent_review_reused': PINS['prior_independent_checker'][0],
              'anchors': sorted(seen), 'singleton_exclusions': sorted(singleton), 'exceptional_donor': 10,
              'exceptional_receiver': 80, 'propagation_rank_15_checks': propagation_count,
              'final_rank_2_checks': len(witnesses), 'physical_H_receiver_cuts': cut_counts,
              'all_source_receiver_views': len(views), 'mapped_set_intersection_histogram': dict(intersection_histogram),
              'source_payload_hashes': {key: sha256(raw).hexdigest() for key, raw in payload.items()},
              'controls': controls, 'witness_summaries': summaries, 'complete_kappa_claimed': False}
    result['all_native_reflections_checked'] = len(reflections)
    result['author_result_sha256'] = sha256(author_raw).hexdigest()
    result['packing_source_change_counts'] = packing_counts
    (args.out / 'RESULT.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(result['status'], len(seen), propagation_count, dict(intersection_histogram), flush=True)

if __name__ == '__main__':
    main()
