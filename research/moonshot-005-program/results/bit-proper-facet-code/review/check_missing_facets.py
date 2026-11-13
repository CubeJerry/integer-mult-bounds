#!/usr/bin/env python3
"""Independent replay of the frozen BIT missing-facet packet package.

This uses a second modular rank prime (1013), exact rational normal checks,
an independent reflection closure, and a local 222-input word interpreter.
It does not import the author's rank/census builder or retained interpreter.
"""
import argparse
import gzip
import hashlib
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from decimal import Decimal, localcontext
from pathlib import Path

NATIVE_SHA = "51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78"
MANIFEST_SHA = "6ff4c619fd0f37ea016e18f6657c2b32559f25a33d88a3b4aa7019f26805ec56"
P = 1013


def need(ok, msg):
    if not ok:
        raise AssertionError(msg)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def f2_insert(basis, value, witness=None):
    while value:
        pivot = value.bit_length() - 1
        if pivot not in basis:
            basis[pivot] = value
            return True
        value ^= basis[pivot]
    return False


def f2_rank(rows):
    basis = {}
    for row in rows:
        f2_insert(basis, row)
    return len(basis)


def f2_solve(rows, target):
    basis = {}
    for i, row in enumerate(rows):
        x = row
        coeff = 1 << i
        while x:
            pivot = x.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (x, coeff)
                break
            old, old_coeff = basis[pivot]
            x ^= old
            coeff ^= old_coeff
    x = target
    coeff = 0
    while x:
        pivot = x.bit_length() - 1
        if pivot not in basis:
            return None
        old, old_coeff = basis[pivot]
        x ^= old
        coeff ^= old_coeff
    return coeff


def rref(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    if not a:
        return [], []
    nr, nc = len(a), len(a[0])
    p = 0
    pivots = []
    for c in range(nc):
        q = next((i for i in range(p, nr) if a[i][c]), None)
        if q is None:
            continue
        a[p], a[q] = a[q], a[p]
        z = a[p][c]
        a[p] = [v / z for v in a[p]]
        for i in range(nr):
            if i != p and a[i][c]:
                z = a[i][c]
                a[i] = [v - z * w for v, w in zip(a[i], a[p])]
        pivots.append(c)
        p += 1
        if p == nr:
            break
    return a[:p], pivots


def mod_rank(rows, prime=P):
    a = [[int(x) % prime for x in row] for row in rows]
    if not a:
        return 0
    nr, nc = len(a), len(a[0])
    p = 0
    for c in range(nc):
        q = next((i for i in range(p, nr) if a[i][c]), None)
        if q is None:
            continue
        a[p], a[q] = a[q], a[p]
        zinv = pow(a[p][c], -1, prime)
        a[p] = [(v * zinv) % prime for v in a[p]]
        for i in range(nr):
            if i != p and a[i][c]:
                z = a[i][c]
                a[i] = [(v - z * w) % prime for v, w in zip(a[i], a[p])]
        p += 1
        if p == nr:
            break
    return p


def canonical(v):
    first = next(x for x in v if x)
    return tuple(v) if first > 0 else tuple(-x for x in v)


def exact_normal(support, roots):
    rows, pivots = rref([roots[i] for i in support])
    need(len(pivots) == 7, ("exact rank-seven normal", len(support), len(pivots)))
    free = next(c for c in range(8) if c not in pivots)
    normal = [Fraction(0)] * 8
    normal[free] = 1
    for ri, c in enumerate(pivots):
        normal[c] = -rows[ri][free]
    den = math.lcm(*(x.denominator for x in normal))
    ints = [int(x * den) for x in normal]
    g = math.gcd(*ints)
    ints = [x // g for x in ints]
    ints = list(canonical(ints))
    return ints


def chart_rank(frames, chart):
    return len(rref(frames[chart]["B"])[1])


def subchart(frames, small, large):
    bs = frames[small]["B"]
    bl = frames[large]["B"]
    return len(rref(bs + bl)[1]) == len(rref(bl)[1])


def nested_pair(frames, a, b):
    return subchart(frames, a, b) or subchart(frames, b, a)


def interval_rank_power(rank, bits=128):
    den = 1 << bits
    target = rank ** 199 * den ** 200
    lo, hi = 0, rank * den + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** 200 <= target:
            lo = mid
        else:
            hi = mid
    need(lo ** 200 <= target < (lo + 1) ** 200, ("directed 200th root", rank))
    upper = lo if lo ** 200 == target else lo + 1
    return Fraction(lo, den), Fraction(upper, den)


def decimal_string(x, places=50):
    with localcontext() as context:
        context.prec = places + 12
        value = Decimal(x.numerator) / Decimal(x.denominator)
        return f"{value:.{places}f}"


def moment(profile):
    lo = hi = Fraction(0)
    for r, count in profile.items():
        if not count:
            continue
        x, y = interval_rank_power(r)
        if count > 0:
            lo += count * x
            hi += count * y
        else:
            lo += count * y
            hi += count * x
    return lo, hi


def replay_word(word, frames, krows):
    public = word["public"]
    rows = {i: 1 << i for i in range(public)}
    where = dict(enumerate(word["start"]))
    counts = Counter()
    paid = Counter()
    seen_pairs = set()
    active = set()
    peak = 0
    lifetimes = 0
    packet_deliveries = []
    for event, ins in enumerate(word["program"]):
        op, a = ins[:2]
        counts[op] += 1
        if op == "INIT":
            c = ins[2]
            need(a >= public and a not in rows and c in frames, ("INIT ownership", event, ins))
            rows[a] = 0
            where[a] = c
            active.add(a)
            lifetimes += 1
            peak = max(peak, len(active))
        elif op == "CLEAR":
            c = ins[2]
            need(a in active and where[a] == c, ("CLEAR lifetime/chart", event, ins))
            del rows[a]
            del where[a]
            active.remove(a)
        elif op == "ADD":
            b, c = ins[2:]
            need(a in rows and b in rows and a != b, ("ADD live fields", event, ins))
            need(where[a] == where[b] == c, ("ADD cochart", event, ins))
            rows[a] ^= rows[b]
        elif op == "MOVE":
            src, dst = ins[2:]
            need(a in rows and where[a] == src, ("MOVE source chart", event, ins))
            need(src in frames and dst in frames and src != dst, ("MOVE frames", event, ins))
            r = abs(frames[dst]["dim"] - frames[src]["dim"])
            need(r > 0 and nested_pair(frames, src, dst), ("MOVE nested/rank", event, ins))
            paid[r] += 1
            seen_pairs.add((src, dst))
            where[a] = dst
            if a >= public and frames[src]["dim"] >= 7 and frames[dst]["dim"] == 0:
                packet_deliveries.append({"field": a, "source_chart": src,
                                          "row": rows[a]})
        elif op == "SWAP":
            b = ins[2]
            need(a in rows and b in rows and a != b, ("SWAP live fields", event, ins))
            rows[a], rows[b] = rows[b], rows[a]
            where[a], where[b] = where[b], where[a]
        else:
            raise AssertionError(("unknown op", event, ins))
    need(not active, "all owned fields retired")
    need(set(rows) == set(range(public)), "only public rows remain")
    need([where[i] for i in range(public)] == word["final"], "all public endpoint charts")
    expected = [1 << i for i in range(111)] + [
        (1 << (111 + i)) ^ krows[i] for i in range(111)]
    need([rows[i] for i in range(public)] == expected, "exact X=x,Y=y+Kx map")
    return {
        "operations": sum(counts.values()),
        "counts": dict(sorted(counts.items())),
        "paid_profile": dict(sorted(paid.items())),
        "moves": sum(paid.values()),
        "distinct_nested_move_pairs": len(seen_pairs),
        "retired_lifetimes": lifetimes,
        "peak_owned": peak,
        "all_222_input_directions_replayed": True,
        "packet_delivery_rows": [x["row"] for x in packet_deliveries],
        "packet_delivery_records": packet_deliveries,
    }


def main(args):
    workspace = args.repo
    if (workspace / "programme/research").exists():
        programme = workspace / "programme"
        root_work = workspace / "root-work"
    else:
        programme = workspace
        root_work = workspace.parent / "root-work"
    package = args.package if args.package else root_work / "bit-missing-facets"
    manifest_raw = (package / "MANIFEST.json").read_bytes()
    need(sha(manifest_raw) == MANIFEST_SHA, "frozen author manifest hash")
    manifest = json.loads(manifest_raw)
    for name, expected_hash in manifest["files"].items():
        need(sha((package / name).read_bytes()) == expected_hash, ("frozen author file", name))

    native_path = programme / "research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz"
    native_raw = native_path.read_bytes()
    need(sha(native_raw) == NATIVE_SHA, "native source hash")
    native = json.loads(gzip.decompress(native_raw))
    frames = {int(k): v for k, v in native["frames"].items()}
    source_lines = []
    for chart in native["start"][:111]:
        raw = [Fraction(x) for x in frames[chart]["B"][0]]
        raw_norm = dot(raw, raw)
        need(raw_norm in (1, 4), ("raw E8 source norm", chart, raw_norm))
        scale = 2 if raw_norm == 1 else 1
        v = [x * scale for x in raw]
        need(all(x.denominator == 1 for x in v), ("integral norm-four source", chart))
        v = tuple(int(x) for x in v)
        need(dot(v, v) == 4, ("norm-four source", chart))
        source_lines.append(v)

    # Rebuild the actual F2 fitting matrix and its greedy encoder basis.
    krows = []
    for i in range(111):
        row = 0
        for j in range(111):
            if i == j or dot(source_lines[i], source_lines[j]) == 0:
                row |= 1 << j
        krows.append(row)
    row_basis = {}
    encoder_roles = []
    for i, row in enumerate(krows):
        x = row
        while x:
            pivot = x.bit_length() - 1
            if pivot not in row_basis:
                row_basis[pivot] = x
                encoder_roles.append(i)
                break
            x ^= row_basis[pivot]
    need(encoder_roles == [0, 1, 2, 4, 8, 9, 14, 30, 59], "actual greedy rank-nine encoder basis")
    encoders = [krows[i] for i in encoder_roles]
    need(f2_rank(krows) == 9, "actual K rank nine")

    # Exhaust all 511 words. Lower ranks use a prime different from the
    # author verifier's 1009. Rank-seven upper bounds use independent exact
    # rational normals; rank-eight words are certified full by mod 1013.
    words = []
    census = Counter()
    proper = []
    for mask in range(1, 512):
        word_row = 0
        for q, enc in enumerate(encoders):
            if (mask >> q) & 1:
                word_row ^= enc
        support = [j for j in range(111) if (word_row >> j) & 1]
        rank_1013 = mod_rank([source_lines[j] for j in support], P)
        need(rank_1013 in (7, 8), ("second-prime support rank", mask, rank_1013))
        census[(rank_1013, len(support))] += 1
        rec = {"mask": mask, "word": word_row, "weight": len(support), "rank_mod_1013": rank_1013}
        if rank_1013 == 7:
            normal = exact_normal(support, source_lines)
            need(dot(normal, normal) == 4, ("rank-seven root normal", mask, normal))
            exact_support = [j for j, v in enumerate(source_lines) if dot(normal, v) == 0]
            need(exact_support == support, ("facet support equality", mask))
            need(rank_1013 == 7, ("modular lower rank", mask))
            rec["normal"] = normal
            proper.append(rec)
        words.append(rec)
    proper.sort(key=lambda x: x["mask"])
    need(len(words) == 511 and len(proper) == 9, "exact 511-word census and nine proper words")
    proper_masks = [x["mask"] for x in proper]
    proper_weights = [x["weight"] for x in proper]
    need(proper_masks == [38, 44, 223, 241, 254, 296, 314, 367, 419], "proper word masks")
    need(proper_weights == [56, 60, 59, 58, 58, 59, 58, 56, 59], "proper word weights")
    proper_rows = [x["word"] for x in proper]
    need(f2_rank(proper_rows) == 9, "proper words form a basis of C")
    overlaps = []
    pair_union_ranks = []
    for a, b in itertools.combinations(proper, 2):
        overlaps.append((a["word"] & b["word"]).bit_count())
        union = a["word"] | b["word"]
        pair_union_ranks.append(mod_rank([source_lines[j] for j in range(111) if (union >> j) & 1], P))
    need((min(overlaps), max(overlaps)) == (25, 34), "proper support overlaps")
    need(set(pair_union_ranks) == {8}, "each distinct proper support union spans R8")

    # Independently close the source E8 reflection orbit and identify the
    # nine rank-seven normals as precisely the missing projective roots.
    closure = {canonical(v) for v in source_lines}
    while True:
        next_closure = set(closure)
        for x in closure:
            for y in closure:
                inner = dot(x, y)
                need(inner % 2 == 0, "even E8 inner product")
                reflected = canonical(tuple(a - (inner // 2) * b for a, b in zip(x, y)))
                need(dot(reflected, reflected) == 4, "reflection preserves norm-four roots")
                next_closure.add(reflected)
        need(len(next_closure) <= 120, "finite E8 line closure")
        if next_closure == closure:
            break
        closure = next_closure
    missing = closure - {canonical(v) for v in source_lines}
    proper_normals = {canonical(x["normal"]) for x in proper}
    need(len(closure) == 120 and missing == proper_normals and len(missing) == 9,
         "exactly nine proper normals are the nine omitted roots")

    # Cross-check the author's frozen finite table only after the independent
    # census has been completed with the second prime.
    cert = json.loads((package / "CERTIFICATE.json").read_text())
    author_words = cert["all_511_nonzero_words"]
    need(len(author_words) == len(words), "author certificate contains 511 rows")
    for own, author in zip(words, author_words):
        need((own["mask"], own["word"], own["weight"], own["rank_mod_1013"])
             == (author["mask"], author["row"], author["weight"], author["real_rank"]),
             ("full census agrees", own["mask"]))

    # All-field/block theorem data: K has rank 9 over F2, proper word supports
    # individually span facets, and every pair union has rank 8.
    # The accompanying report supplies the coefficient-field decomposition
    # argument; this exact finite data is the only source-specific premise.

    # Reconstruct the changed one-facet word without importing the retained
    # interpreter. The certificate package pins its compressed bytes.
    word_raw = (package / "PARTIAL-WORD.json.gz").read_bytes()
    need(sha(word_raw) == cert["partial_word_sha256"], "partial word pin")
    partial = json.loads(gzip.decompress(word_raw))
    normal_word = proper[0]
    need(cert["one_facet_mask"] == normal_word["mask"] == 38, "literal proper word is mask 38")
    packet_basis = [normal_word["word"]]
    for enc in encoders:
        if f2_rank(packet_basis + [enc]) > len(packet_basis):
            packet_basis.append(enc)
    need(len(packet_basis) == 9 and f2_rank(packet_basis) == 9,
         "independent packet basis completion")
    need(packet_basis == cert["partial_packet_rows"], "packet word uses proper word plus eight Hub rows")
    need(all(f2_solve(packet_basis, row) is not None for row in krows),
         "all 111 K rows decode from the nine packets")
    result_frames = {int(k): v for k, v in partial["frames"].items()}
    facet_candidates = [c for c, fr in result_frames.items()
                        if fr["dim"] == 7 and all(dot(normal_word["normal"], [Fraction(x) for x in b]) == 0
                                                   for b in fr["B"])]
    facet_chart = partial["program"][0][3]
    need(facet_chart in facet_candidates and len(facet_candidates) == 2,
         "literal missing-root facet and equivalent retained frame")
    candidate_spaces = [rref(result_frames[c]["B"])[0] for c in facet_candidates]
    need(candidate_spaces[0] == candidate_spaces[1], "the two frame IDs describe the same rational chart")
    need(result_frames[facet_chart]["A"] == [normal_word["normal"]], "literal facet normal")
    need(all(dot(normal_word["normal"], source_lines[j]) == 0
             for j in range(111) if (normal_word["word"] >> j) & 1),
         "all mask38 donors lie in proper facet")
    bill = replay_word(partial, result_frames, krows)
    need(bill["operations"] == 1307, "literal operation count")
    need(bill["counts"] == {"ADD": 1002, "CLEAR": 9, "INIT": 9, "MOVE": 287},
         "literal instruction counts")
    need(bill["paid_profile"] == {1: 56, 6: 56, 7: 167, 8: 8}, "literal paid profile")
    need(bill["retired_lifetimes"] == 9 and bill["peak_owned"] == 1,
         "literal owned ledger")
    need(bill["distinct_nested_move_pairs"] == 225, "literal nested MOVE pairs")
    need(bill["packet_delivery_rows"] == packet_basis, "delivered packet payloads equal the stated basis")

    old_profile = {7: 222, 8: 9}
    difference = {8: 1, 7: 55, 6: -56, 1: -56}
    gain = moment(difference)
    partial_price = moment({1: 56, 6: 56, 7: 167, 8: 8})
    old_price = moment(old_profile)
    need(gain[0] > 0, "strict exact one-facet movement saving at t=199/200")
    derived_gain = (old_price[0] - partial_price[1], old_price[1] - partial_price[0])
    need(derived_gain[0] <= gain[0] <= gain[1] <= derived_gain[1],
         "combined profile difference is consistent with separately rounded price intervals")

    result = {
        "status": "PASS_INDEPENDENT_SECOND_PRIME_AND_EXACT_WORD_REPLAY",
        "author_manifest_sha256": MANIFEST_SHA,
        "native_sha256": NATIVE_SHA,
        "author_certificate_sha256": sha((package / "CERTIFICATE.json").read_bytes()),
        "author_partial_word_sha256": sha(word_raw),
        "independent_rank_prime": P,
        "canonical_encoder_roles": encoder_roles,
        "all_511_nonzero_words_recomputed": len(words),
        "rank_weight_census": [{"rank_mod_1013": r, "weight": w, "count": n}
                                for (r, w), n in sorted(census.items())],
        "proper_word_masks": proper_masks,
        "proper_word_weights": proper_weights,
        "proper_normals": [x["normal"] for x in proper],
        "proper_word_basis_rank": f2_rank(proper_rows),
        "proper_support_overlap_range": [min(overlaps), max(overlaps)],
        "all_distinct_proper_union_ranks_mod_1013": sorted(set(pair_union_ranks)),
        "reflection_closure_size": len(closure),
        "missing_root_count": len(missing),
        "missing_roots_equal_proper_normals": True,
        "fresh_packet_support_theorem": {
            "scope": "Nine volume-V packets whose direct sum is the canonical rank-9 K tensor block code; each born at one chart; unchanged raw X inputs each follow one upward nested path; no informative moving copies or multi-chart packet assembly.",
            "maximum_proper_born_packets": 1,
            "reason": "same-facet shortenings coincide; distinct proper supports overlap in at least25 unchanged donors but their rank-7 facets are incomparable",
        },
        "literal_word_bill": bill,
        "old_profile": old_profile,
        "new_profile": {1: 56, 6: 56, 7: 167, 8: 8},
        "old_partial_price_interval": [str(x) for x in old_price],
        "new_partial_price_interval": [str(x) for x in partial_price],
        "separate_price_difference_interval": [str(x) for x in derived_gain],
        "saving_at_t_199_200_interval": [str(x) for x in gain],
        "saving_decimal_interval": [decimal_string(x) for x in gain],
        "scope": "Independent finite source/code census and scalar literal partial-word replay. The shortening theorem is valid for every characteristic-two field and block volume by the proof in REVIEW.md. All6470 K+I residual coefficients remain; no complete Q, physical all-width admission, supplier or new kappa.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in [
        "status", "independent_rank_prime", "all_511_nonzero_words_recomputed",
        "proper_word_masks", "proper_word_weights", "proper_support_overlap_range",
        "all_distinct_proper_union_ranks_mod_1013", "reflection_closure_size",
        "fresh_packet_support_theorem", "literal_word_bill",
        "old_partial_price_interval", "new_partial_price_interval",
        "saving_at_t_199_200_interval", "saving_decimal_interval",
    ]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--package", type=Path)
    parser.add_argument("--output", type=Path,
                        default=Path("worker-c/bit-missing-facets-review/RESULT.json"))
    main(parser.parse_args())
