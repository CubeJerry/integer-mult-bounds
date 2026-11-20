#!/usr/bin/env python3
"""Independent source cuts, common fibres, owner words and complete invoice."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import numpy as np

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec); spec.loader.exec_module(value)
    return value

source = load(Path(__file__).with_name('construct.py'), 'independent_chain_reconstruction')
need = source.need

def powers(field, nodes, width):
    nodes = np.array(nodes, dtype=np.uint8)
    result = np.ones((len(nodes), width), dtype=np.uint8)
    for c in range(1, width):
        result[:, c] = field.product[result[:, c-1], nodes]
    return result

def source_cuts(ctx):
    F = ctx.field; geometric = Counter(); native = Counter(); deficient = Counter()
    non_rs = json.loads(ctx.payload['non_RS'])
    need(set(map(int, non_rs)) == set(ctx.donors), 'all seven information-change witnesses')
    for (j, k), rows in sorted(ctx.maps.items()):
        need(set(rows) == set(ctx.stars[j]), 'one complete 28-plane source at every donor')
        for i in sorted(ctx.perp[j]):
            stack = np.vstack([rows[h] for h in ctx.views[j, i]])
            need(stack.shape == (16*k, 16*k) and F.rank(stack) == 16*k, 'entire geometric source cut')
            geometric[k] += 1; native[k] += (i < 111)
        if k == 3:
            witness = non_rs[str(j)]; hs = witness['planes']
            need(len(hs) == len(set(hs)) == 16 and set(hs) <= set(rows), '16 actual ordinary observation planes')
            rank = F.rank(np.vstack([rows[h] for h in hs]))
            need(rank == witness['rank'] and rank < 48, 'new marked observation is noninjective')
            deficient[rank] += 1
    need(geometric == {3: 441, 12: 441} and native == {3: 408, 12: 408}, 'all geometric and native source cuts')
    need(deficient == {47: 6, 46: 1}, 'seven genuine nonlinear-invariant source changes')
    j = 0; i = min(ctx.perp[j] & set(range(111)))
    original = np.vstack([ctx.maps[j, 3][h] for h in ctx.views[j, i]])
    broken = original.copy(); broken[:3] = 0
    need(F.rank(broken) == 45, 'deleting a genuine quotient destroys a native source cut')
    return {'geometric': dict(geometric), 'native': dict(native), 'non_RS_ranks': dict(deficient),
            'deleted_quotient_control': {'donor': j, 'receiver': i, 'original': 48, 'damaged': 45}}

def inverse_fibres(ctx):
    F = ctx.field; counts = Counter(); native_counts = Counter(); hashes = {}; control = None
    for h in ctx.centres:
        need(10 not in ctx.H[h] and not ctx.H[h] <= ctx.perp[80], 'designated interfaces avoid both target perturbations')
        for k in (3, 12):
            chart = ctx.charts[h, k]; donors = sorted(ctx.H[h]); digest = sha256()
            points = {p: ctx.maps[donors[0], k][q] for q, p in chart.point[donors[0]].items()}
            for j in donors:
                need(all(np.array_equal(ctx.maps[j, k][q], points[p]) for q, p in chart.point[j].items()),
                     'one identical point quotient across all centre donors')
            for i in chart.receivers:
                pos = [ordinal for ordinal, d in enumerate(chart.ports) if ctx.D[d] <= ctx.perp[i]]
                need(len(pos) == k, 'actual receiver component port count')
                V = powers(F, [q+1 for q in pos], 3*k)
                first = donors[0]; rows = ctx.maps[first, k]
                off = [q for q in ctx.views[first, i] if q != h]
                point_view = {chart.point[first][q] for q in off}
                need(len(point_view) == 15, '15 actual off-centre point quotients')
                for ordinal, port in enumerate(chart.ports):
                    need(len(point_view & ctx.native.rad[port]) == (3 if ordinal in pos else 1),
                         'actual full-or-single radical intersection')
                annihilator = np.vstack([rows[q] for q in off])
                need(F.rank(annihilator) == 15*k, 'entire off-centre fibre has dimension k')
                readout = F.mm(V[:, :k], rows[h])
                stack = np.vstack([readout, annihilator])
                rhs = np.zeros((16*k, k), dtype=np.uint8); rhs[:k] = np.eye(k, dtype=np.uint8)
                lift = F.solve(stack, rhs); digest.update(lift.tobytes())
                for ordinal, j in enumerate(donors):
                    rows = ctx.maps[j, k]
                    off = [q for q in ctx.views[j, i] if q != h]
                    need(not np.any(F.mm(np.vstack([rows[q] for q in off]), lift)), 'all true off-centre information vanishes')
                    minor = V[:, ordinal*k:(ordinal+1)*k]
                    need(F.rank(minor) == k, 'physical H donor block is invertible')
                    readout = F.mm(minor, rows[h])
                    need(np.array_equal(F.mm(readout, lift), np.eye(k, dtype=np.uint8)), 'same complete canonical inverse lift for every donor')
                    if control is None and ordinal == 1 and i < 111:
                        changed = F.product[2, readout]
                        need(F.rank(changed) == k and not np.array_equal(F.mm(changed, lift), np.eye(k, dtype=np.uint8)),
                             'rank-preserving donor relabel breaks the common readout')
                        control = {'H': h, 'receiver': i, 'donor': j, 'k': k}
                counts[k] += 1; native_counts[h, k] += (i < 111)
            hashes[f'{h}/{k}'] = digest.hexdigest()
    need(counts == {3: 108, 12: 108}, 'all geometric common inverse fibres')
    need(all(native_counts[h, k] == ({263: 33, 642: 34, 135: 34}[h]) for h, k in native_counts), 'all 101 native inverse fibres')
    return {'geometric_per_component': dict(counts), 'native_per_centre': {str(h): native_counts[h, 3] for h in ctx.centres},
            'native_per_component': 101, 'native_donor_fibres_per_component': 303,
            'hashes': hashes, 'rank_preserving_control': control}

def source_word(ctx):
    F = ctx.field; cost = json.loads(ctx.payload['cost'])
    total = Counter(); by_donor = {}; word_hashes = {}; all_y = set(); early_count = 0; half_frames = 0
    for j in ctx.donors:
        local = Counter(); mapping = {}; records = {}; hashes = {}
        for k in (3, 12):
            rows = ctx.maps[j, k]; centre = next(h for h in ctx.centres if j in ctx.H[h])
            seed = ctx.parameters[str(k)]['early'][str(j)]
            prefix = 0 if k == 3 else 3; offset = 0 if k == 3 else 768; n = 16*k
            early = []; positions = []; jobs = []
            for h, A in sorted(rows.items()):
                xs = ctx.wires[j, h, 'X']; ys = ctx.wires[j, h, 'Y']; quota = len(xs)//120
                need(quota in (1, 2) and len(xs) == 120*quota and len(ys) == 120*(2-quota), 'actual ordinary early/late quota')
                doubled = np.kron(np.eye(2, dtype=np.uint8), A)
                if quota == 2:
                    early.append(doubled)
                    if ctx.xcount[h] == 90:
                        positions.extend((h, 16*prefix+16*d+8*b) for b in range(2) for d in range(k))
                    else:
                        need(ctx.xcount[h] == 45, 'actual large early donor at a two-donor plane')
                        positions.extend((h, 16*prefix+8*d) for d in range(2*k))
                else:
                    frame = np.eye(2*k, dtype=np.uint8)[:k] if h in ctx.centres else source.pseudo(f'early/{centre}/{k}/{j}/{h}/{seed}', k, 2*k)
                    rank, _, pivots = F.reduce(frame, full=True)
                    need(rank == k, 'independent physical early half frame')
                    complementary = [c for c in range(2*k) if c not in pivots]
                    need(F.rank(np.vstack([frame, np.eye(2*k, dtype=np.uint8)[complementary]])) == 2*k, 'exact late complement')
                    early.append(F.mm(frame, doubled)); half_frames += 1
                    positions.extend((h, 8*prefix+8*d) for d in range(k))
                    for d, c in enumerate(complementary):
                        half, power = divmod(c, k)
                        jobs.append({'h': h, 'coefficients': A[power].tolist(),
                                     'dest_and_first_X': [(ys[8*(prefix+d)+lane], j*3840+offset+8*half+lane) for lane in range(8)]})
            early = np.vstack(early)
            need(early.shape == (32*k, 32*k) and F.rank(early) == 32*k, 'complete chronological source basis')
            stream, price = F.compile(early); early_count += 1
            hashes[str(k)] = sha256(stream).hexdigest()
            need(hashes[str(k)] == cost['all_word_hashes'][str(j)][str(k)], 'literal independently compiled source word')
            placements = []
            for lane in range(8):
                bank = [j*3840+offset+16*c+8*b+lane for b in range(2) for c in range(n)]
                placements.append(bank)
                for index, (h, pos) in enumerate(positions):
                    owner = ctx.wires[j, h, 'X'][pos+lane]
                    need(owner not in mapping, 'unique original X output placement')
                    mapping[owner] = bank[index]
            late = [dest for job in jobs for dest, first in job['dest_and_first_X']]
            need(len(set(late)) == len(late) and not all_y.intersection(late), 'one actual late parity cache per field')
            need(all(any(job['coefficients']) for job in jobs), 'late parities genuinely depend on original input')
            all_y.update(late)
            local['basis_ADD'] += 8*price
            local['write_ADD'] += 8*sum(int(F.weights[job['coefficients']].sum()) for job in jobs)
            local['read_ADD'] += 6*len(late); local['INIT'] += 6*len(late); local['dirty_CLEAR'] += 6*len(late)
            records[f'{j}-{k}'] = {'reduce_file': f'REDUCE-{j}-{k}.bin.gz', 'original_field_placements': placements,
                                  'before_departure_late_parities': jobs}
        original = set(range(3840*j, 3840*(j+1)))
        need(set(mapping) == set(mapping.values()) == original, 'one permutation of all 3840 original donor fields')
        seen = set(); swaps = []
        for first in sorted(mapping):
            if first in seen:
                continue
            cycle = []; at = first
            while at not in seen:
                seen.add(at); cycle.append(at); at = mapping[at]
            need(at == first, 'owner permutation cycle closes')
            swaps.extend(zip(cycle, cycle[1:]))
        moved = {u: u for u in original}
        for a, b in swaps:
            moved[a], moved[b] = moved[b], moved[a]
        need(moved == mapping, 'literal owner swaps replayed')
        records[f'{j}-swaps'] = swaps
        hashes['holder'] = sha256(json.dumps(records, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        need(hashes['holder'] == cost['all_word_hashes'][str(j)]['holder'], 'independent actual holder dictionary')
        local['permutation_ADD'] = 18*len(swaps)
        local['inverse_ADD'] = local['basis_ADD']+local['permutation_ADD']
        local['forward_ADD'] = local['inverse_ADD']+local['write_ADD']+local['read_ADD']
        local['total_ADD'] = local['forward_ADD']+local['inverse_ADD']
        need(dict(local) == cost['special_donor_costs'][str(j)], 'all source charges for one changed donor')
        total.update(local); by_donor[str(j)] = dict(local); word_hashes[str(j)] = hashes
    need(dict(total) == cost['special'] and total['INIT'] == 6*len(all_y) == 120960, 'complete seven-source physical invoice')
    need(early_count == 14 and half_frames == 336, 'all actual early component bases and half frames')
    return dict(total), by_donor, word_hashes

def background_invoice(ctx):
    # Reconstruct every predecessor donor's source descriptors and actual owner
    # permutation, then retain exactly the 104 banks not replaced by the chain.
    # The prior independent review's bit-level compiler replays each distinct
    # 96-dimensional binary word forward and backward on the whole basis.
    old = source.module(ctx.base/source.PINS['RS_review'][0], 'previous_independent_RS_word_audit')
    F = ctx.field
    need(np.array_equal(old.G, F.product), 'background field representation agrees')
    expected = json.loads(ctx.payload['background_costs'])
    rs_result = json.loads(ctx.payload['RS_result'])
    scales = {int(j): value for j, value in rs_result['chosen_singleton_scales'].items()}
    all_costs = Counter(); retained = Counter(); per_donor = {}
    row_costs = [int(F.weights[powers(F, [x], 16)[0]].sum()) for x in range(29)]
    for j in range(111):
        node = {h: q+1 for q, h in enumerate(ctx.stars[j])}
        partial = sorted(h for h in ctx.stars[j] if len(ctx.wires[j, h, 'X']) == 120)
        first_half = set(partial[:12])
        need(len(partial) in (24, 25), 'actual old RS ordinary/singleton half phases')
        bindings = defaultdict(list); local = Counter()
        for h in ctx.stars[j]:
            xs = ctx.wires[j, h, 'X']; ys = ctx.wires[j, h, 'Y']; quota = len(xs)//120
            need(quota in (1, 2, 3) and len(xs) == 120*quota and len(ys) == 120*max(2-quota, 0), 'true predecessor phase capacities')
            local['late_evaluation_ADD'] += len(ys)*row_costs[node[h]]
            used = set()
            for k in (3, 12):
                prefix = 0 if k == 3 else 3
                if quota == 1:
                    slots = [(d+(0 if h in first_half else k), 0, 1, 8*prefix+8*d) for d in range(k)]
                elif quota == 2:
                    if ctx.xcount[h] == 90:
                        slots = [(d+b*k, 0, 1, 16*prefix+16*d+8*b) for b in range(2) for d in range(k)]
                    else:
                        need(ctx.xcount[h] == 45, 'old large early two-donor allocation')
                        slots = [(d, 0, 1, 16*prefix+8*d) for d in range(2*k)]
                else:
                    need(j in scales, 'actual singleton derivative scale')
                    delta = scales[j][int(k == 12)]
                    slots = [(d if d < 2*k else d-2*k, int(d >= 2*k), delta if d >= 2*k else 1,
                              24*prefix+8*d) for d in range(3*k)]
                for c, derivative, scalar, first in slots:
                    for stripe in range(8):
                        owner = xs[first+stripe]
                        need(owner not in used, 'one predecessor early row per real owner')
                        used.add(owner)
                        bindings[k, stripe, c].append((h, derivative, scalar, owner))
            need(used == set(xs), 'every predecessor source-plane X holder assigned')
        permutation = [-1]*3840; serial = 0
        for k in (3, 12):
            for stripe in range(8):
                for channel in range(2*k):
                    rows = sorted(bindings[k, stripe, channel])
                    need(len(rows) == 16, 'all 16 predecessor evaluation/jet constraints')
                    descriptors = tuple((node[h], derivative, scalar) for h, derivative, scalar, owner in rows)
                    local['early_basis_ADD'] += old.rsword(descriptors, False)
                    for h, derivative, scalar, owner in rows:
                        destination = owner-j*3840
                        need(0 <= destination < 3840 and permutation[destination] == -1, 'predecessor physical permutation span')
                        permutation[destination] = serial; serial += 1
        need(serial == 3840, 'all predecessor original source coordinates')
        local['source_owner_permutation_ADD'] = old.permcost(permutation)
        local['snapshot_copy_ADD_INIT_dirty_CLEAR'] = 3840*6
        need(dict(local) == expected[str(j)], 'independently rebuilt predecessor per-donor invoice')
        all_costs.update(local); per_donor[str(j)] = dict(local)
        if j not in ctx.donors:
            retained.update(local)
    previous = json.loads(ctx.payload['RS_review_result'])['RS_source']
    need(all_costs['early_basis_ADD'] == previous['early_basis_ADD']
         and all_costs['source_owner_permutation_ADD'] == previous['permutation_ADD']
         and all_costs['late_evaluation_ADD'] == previous['late_evaluation_ADD']
         and all_costs['snapshot_copy_ADD_INIT_dirty_CLEAR'] == previous['cache_bits'],
         'full independent predecessor invoice agrees with prior reviewed total')
    need(dict(retained) == json.loads(ctx.payload['cost'])['background'], 'exactly the 104 unmodified source charges')
    return dict(retained), per_donor

def main():
    cli = ArgumentParser(description=__doc__)
    cli.add_argument('--repo', type=Path, required=True)
    cli.add_argument('--out', type=Path, required=True)
    args = cli.parse_args()
    ctx = source.context(args.repo, args.out)
    print('PASS_INDEPENDENT_34_CLASS_CONNECTED_SOURCE', flush=True)
    cuts = source_cuts(ctx)
    print('PASS_ALL_441_GEOMETRIC_AND_408_NATIVE_SOURCE_CUTS_PER_COMPONENT', flush=True)
    fibres = inverse_fibres(ctx)
    print('PASS_ALL_108_GEOMETRIC_AND_101_NATIVE_COMMON_FIBRES_PER_COMPONENT', flush=True)
    special, per_donor, hashes = source_word(ctx)
    print('PASS_ALL_14_EARLY_WORDS_AND_SEVEN_PHYSICAL_HOLDER_DICTIONARIES', flush=True)
    background, old_donors = background_invoice(ctx)
    inverse = background['early_basis_ADD'] + background['source_owner_permutation_ADD']
    cache = background['snapshot_copy_ADD_INIT_dirty_CLEAR']
    forward = inverse + cache + background['late_evaluation_ADD']
    combined = {'donors': 111, 'source_forward_ADD': forward+special['forward_ADD'],
                'source_pure_inverse_ADD': inverse+special['inverse_ADD'],
                'source_forward_and_inverse_ADD': forward+inverse+special['total_ADD'],
                'source_INIT': cache+special['INIT'], 'source_dirty_CLEAR': cache+special['dirty_CLEAR'],
                'source_extra_MOVE': 0, 'new_complete_kappa': False}
    need(combined == json.loads(ctx.payload['cost'])['combined'], 'complete 111-source invoice with no double counting')
    need(combined['source_forward_and_inverse_ADD'] == 592316904, 'published complete source ADD total')
    components = {}
    for k, c in ctx.components.items():
        components[str(k)] = {'constraint_shape': list(c['relation'].shape),
                              'constraint_sha256': sha256(c['relation'].tobytes()).hexdigest(),
                              'embedding_shape': list(c['embedding'].shape),
                              'embedding_sha256': sha256(c['embedding'].tobytes()).hexdigest(),
                              'point_coefficient_rank_census': c['point_coefficient_rank_census'],
                              'quotient_classes': c['classes']}
    result = {'status': 'PASS_INDEPENDENT_CONNECTED_THREE_CENTRE_SOURCE',
              'new_author_code_imported': False, 'donors': ctx.donors, 'centres': ctx.centres,
              'source_payload_pins': {name: digest for name, digest in source.PINS.values()},
              'components': components, 'source_cuts': cuts, 'common_fibres': fibres,
              'literal_reduction_streams_matched': 14, 'holder_dictionaries_matched': 7,
              'special_source_costs': special, 'special_per_donor': per_donor, 'word_hashes': hashes,
              'retained_background_sources': 104, 'background_source_costs': background,
              'independently_rebuilt_old_per_donor_costs': old_donors, 'combined_source_costs': combined,
              'scope': 'Seven-source connected construction and complete 111-source invoice; no common D/K/F or complete target/return.',
              'new_complete_kappa': False}
    (args.out/'RESULT.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(result['status'], combined, flush=True)

if __name__ == '__main__':
    main()
