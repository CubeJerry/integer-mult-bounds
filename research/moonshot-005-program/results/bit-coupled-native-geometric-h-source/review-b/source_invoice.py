"""Adapted from the pinned independent three-chain physical-word review.
Only source count, receipt key, and dependency lookup are changed.
No author compiler is imported.
"""
from collections import Counter, defaultdict
from hashlib import sha256
import json
import numpy as np
import importlib.util
from pathlib import Path
_spec=importlib.util.spec_from_file_location('new_geometric_review_constructor',Path(__file__).with_name('construct.py'))
source=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(source)
need=source.need
powers=source.powers

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
            need(hashes[str(k)] == cost['all_source_word_hashes'][str(j)][str(k)], 'literal independently compiled source word')
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
        need(hashes['holder'] == cost['all_source_word_hashes'][str(j)]['holder'], 'independent actual holder dictionary')
        local['permutation_ADD'] = 18*len(swaps)
        local['inverse_ADD'] = local['basis_ADD']+local['permutation_ADD']
        local['forward_ADD'] = local['inverse_ADD']+local['write_ADD']+local['read_ADD']
        local['total_ADD'] = local['forward_ADD']+local['inverse_ADD']
        need(dict(local) == cost['special_donor_costs'][str(j)], 'all source charges for one changed donor')
        total.update(local); by_donor[str(j)] = dict(local); word_hashes[str(j)] = hashes
    need(dict(total) == cost['special'] and total['INIT'] == 6*len(all_y) == 51840, 'complete three-source physical invoice')
    need(early_count == 6 and half_frames == 144, 'all actual early component bases and half frames')
    return dict(total), by_donor, word_hashes

def background_invoice(ctx):
    # Reconstruct every predecessor donor's source descriptors and actual owner
    # permutation, then retain exactly the 108 banks not replaced by the chain.
    # The prior independent review's bit-level compiler replays each distinct
    # 96-dimensional binary word forward and backward on the whole basis.
    old = source.module(ctx.base/ctx.pins['RS_review']['path'], 'previous_independent_RS_word_audit')
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
    need(dict(retained) == json.loads(ctx.payload['cost'])['background'], 'exactly the 108 unmodified source charges')
    return dict(retained), per_donor
