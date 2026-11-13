#!/usr/bin/env python3
"""Independent audit of the frozen BIT rank-nine partial rail and m=4 lift.

Uses only exact source/artifact replay. Does not import the author builder or
the source screen. The paired caller profile is cross-checked against its
frozen, independently reviewed RESULT receipt.
"""
import argparse
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

NATIVE_SHA = "51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78"
BASELINE_SHA = "3fb13f8072e0d8b2ff9cead7754533cf95fe5079f144857e558da719d3a533f0"


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def qrank(rows):
    if not rows:
        return 0
    a = [[Fraction(x) for x in row] for row in rows]
    nrow, ncol = len(a), len(a[0])
    pivot_row = 0
    for col in range(ncol):
        pivot = next((i for i in range(pivot_row, nrow) if a[i][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        z = a[pivot_row][col]
        a[pivot_row] = [x / z for x in a[pivot_row]]
        for i in range(nrow):
            if i != pivot_row and a[i][col]:
                z = a[i][col]
                a[i] = [x - z * y for x, y in zip(a[i], a[pivot_row])]
        pivot_row += 1
        if pivot_row == nrow:
            break
    return pivot_row


def f2rank(rows):
    basis = {}
    for value in rows:
        while value:
            pivot = value.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = value
                break
            value ^= basis[pivot]
    return len(basis)


def f2basis(rows):
    basis = {}
    source_indices = []
    for i, original in enumerate(rows):
        value = original
        witness = 0
        while value:
            pivot = value.bit_length() - 1
            if pivot not in basis:
                witness ^= 1 << len(source_indices)
                basis[pivot] = (value, witness)
                source_indices.append(i)
                break
            old, old_witness = basis[pivot]
            value ^= old
            witness ^= old_witness
    return basis, source_indices


def f2solve(basis, value):
    mask = 0
    while value:
        pivot = value.bit_length() - 1
        if pivot not in basis:
            return None
        old, witness = basis[pivot]
        value ^= old
        mask ^= witness
    return mask


def normalize_line(v):
    for x in v:
        if x:
            return tuple(v) if x > 0 else tuple(-z for z in v)
    raise ValueError("zero root vector")


def validate_frames(frames):
    for frame_id, frame in frames.items():
        B = [[Fraction(x) for x in row] for row in frame["B"]]
        A = [[Fraction(x) for x in row] for row in frame["A"]]
        d = frame["dim"]
        need(len(B) == d and len(A) == 8 - d, ("frame cardinality", frame_id))
        need(qrank(B) == d and qrank(A) == 8 - d, ("frame basis ranks", frame_id))
        need(all(dot(b, a) == 0 for b in B for a in A), ("frame orthogonality", frame_id))
        need(qrank(B + A) == 8, ("frame complement", frame_id))


def nested(frames, source, target):
    fs, ft = frames[source], frames[target]
    if fs["dim"] <= ft["dim"]:
        small, large = fs, ft
    else:
        small, large = ft, fs
    return all(
        dot([Fraction(x) for x in b], [Fraction(x) for x in a]) == 0
        for b in small["B"] for a in large["A"]
    )


def replay(word, frames):
    public = word["public"]
    rows = {i: 1 << i for i in range(public)}
    where = dict(enumerate(word["start"]))
    count = Counter()
    paid = Counter()
    active_peak = 0
    lifetimes = 0
    move_pairs = set()
    swap_log = []
    for event, ins in enumerate(word["program"]):
        op, a = ins[:2]
        count[op] += 1
        if op == "INIT":
            need(a >= public and a not in rows, ("INIT ownership", event, ins))
            rows[a] = 0
            where[a] = ins[2]
            lifetimes += 1
            active_peak = max(active_peak, len(rows) - public)
        elif op == "CLEAR":
            need(a >= public and where.get(a) == ins[2], ("CLEAR chart", event, ins))
            del rows[a]
            del where[a]
        elif op == "ADD":
            b, chart = ins[2:]
            need(a != b and a in rows and b in rows, ("ADD lifetime", event, ins))
            need(where[a] == where[b] == chart, ("ADD cochart", event, ins))
            rows[a] ^= rows[b]
        elif op == "SWAP":
            b = ins[2]
            need(a != b and a in rows and b in rows, ("SWAP lifetime", event, ins))
            swap_log.append((event, a, b, where[a], where[b]))
            rows[a], rows[b] = rows[b], rows[a]
            where[a], where[b] = where[b], where[a]
        elif op == "MOVE":
            source, target = ins[2:]
            need(where.get(a) == source, ("MOVE entrance", event, ins))
            need(source in frames and target in frames and source != target,
                 ("MOVE frames", event, ins))
            rank = abs(frames[target]["dim"] - frames[source]["dim"])
            need(rank > 0 and nested(frames, source, target), ("MOVE nested/rank", event, ins))
            paid[rank] += 1
            move_pairs.add((source, target))
            where[a] = target
        else:
            raise ValueError(("unknown op", event, ins))
    need(set(rows) == set(range(public)), "owned fields all retired")
    need([where[i] for i in range(public)] == word["final"], "public final chart list")
    return [rows[i] for i in range(public)], {
        "operations": len(word["program"]),
        "instruction_counts": dict(sorted(count.items())),
        "paid_profile": dict(sorted(paid.items())),
        "move_count": sum(paid.values()),
        "retired_lifetimes": lifetimes,
        "peak_owned": active_peak,
        "public_inputs_replayed": public,
        "distinct_nested_move_pairs": len(move_pairs),
        "swaps": swap_log,
    }


def rank_power_interval(rank, bits=128):
    den = 1 << bits
    target = rank ** 199 * den ** 200
    lo, hi = 0, rank * den + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** 200 <= target:
            lo = mid
        else:
            hi = mid
    need(lo ** 200 <= target < (lo + 1) ** 200, ("200th-root bracket", rank))
    upper = lo if lo ** 200 == target else lo + 1
    return Fraction(lo, den), Fraction(upper, den)


def moment(profile):
    low = high = Fraction(0)
    for r, coefficient in profile.items():
        if not coefficient:
            continue
        a, b = rank_power_interval(r)
        if coefficient >= 0:
            low += coefficient * a
            high += coefficient * b
        else:
            low += coefficient * b
            high += coefficient * a
    return low, high


def profile_add(*terms):
    out = defaultdict(Fraction)
    for scale, profile in terms:
        for r, n in profile.items():
            out[r] += scale * n
    return {r: n for r, n in out.items() if n}


def interval_strings(interval):
    return [str(interval[0]), str(interval[1])]


def main(args):
    workspace = args.repo
    repository = workspace / "programme" if (workspace / "programme/research").exists() else workspace
    package = workspace / "root-work/bit-nine" if (workspace / "root-work/bit-nine").exists() else workspace / "bit-nine"
    manifest = json.loads((package / "MANIFEST.json").read_text())
    pinned_hashes = manifest["files"]
    for name, expected in pinned_hashes.items():
        need(sha((package / name).read_bytes()) == expected, ("frozen package pin", name))

    native_path = repository / "research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz"
    native_raw = native_path.read_bytes()
    need(sha(native_raw) == NATIVE_SHA, "BIT native source pin")
    native = json.loads(gzip.decompress(native_raw))
    frames = {int(k): v for k, v in native["frames"].items()}
    validate_frames(frames)
    need(native["public"] == 659 and native["owned_fields"] == 237,
         "native public/owned cardinalities")
    need(len(native["start"]) == len(native["final"]) == 659,
         "native endpoint arrays")

    # Recover the 111 source lines and close them under their exact reflections.
    raw_lines = [[Fraction(x) for x in frames[native["start"][i]]["B"][0]]
                 for i in range(111)]
    need(all(frames[native["start"][i]]["dim"] == 1 and
             len(frames[native["start"][i]]["B"]) == 1 for i in range(111)),
         "all 111 X inputs start on their actual root line")
    g2 = []
    raw_norms = Counter()
    for r in raw_lines:
        n2 = dot(r, r)
        raw_norms[n2] += 1
        need(n2 in (1, 4), ("source root norm", n2))
        v = [x * (2 if n2 == 1 else 1) for x in r]
        need(all(x.denominator == 1 for x in v), "doubled roots integral")
        need(dot(v, v) == 4, "common scaled root norm")
        g2.append(tuple(int(x) for x in v))
    gram_values = {dot(a, b) for a in g2 for b in g2}
    need(gram_values == {-2, 0, 2, 4}, "common scaled E8 inner products")
    need(all(dot(g2[i], g2[j]) in (-2, 0, 2) for i in range(111)
             for j in range(i)), "distinct source lines")
    need(qrank(g2) == 8, "111 source lines span rank eight")

    generators = {normalize_line(v) for v in g2}
    closure = set(generators)
    todo = list(generators)
    while todo:
        beta = todo.pop()
        for alpha in generators:
            d = dot(beta, alpha)
            need(d % 2 == 0, "root reflection coefficient integral")
            reflected = normalize_line(tuple(beta[j] - (d // 2) * alpha[j]
                                             for j in range(8)))
            need(dot(reflected, reflected) == 4, "reflected root norm")
            if reflected not in closure:
                closure.add(reflected)
                todo.append(reflected)
    need(len(closure) == 120, "source lines generate 120 E8 projective roots")
    need(all(dot(a, b) in (-2, 0, 2, 4) for a in closure for b in closure),
         "closed E8 root-line angle set")
    for alpha in closure:
        for beta in closure:
            d = dot(alpha, beta)
            reflected = normalize_line(tuple(beta[j] - (d // 2) * alpha[j]
                                             for j in range(8)))
            need(reflected in closure, "full root reflection closure")

    # Rebuild the binary Gram and the real-orthogonality contact-plus-identity K.
    b_rows = []
    k_rows = []
    for i in range(111):
        b = k = 0
        for j in range(111):
            inner = dot(g2[i], g2[j])
            need(inner % 2 == 0, "even doubled Gram")
            bit = (inner // 2) & 1
            if bit:
                b |= 1 << j
            else:
                k |= 1 << j
            need((i == j and bit == 0) or
                 (i != j and bool(bit) == (inner != 0)), "Gram/contact sign interpretation")
            if i != j:
                need(bool(k >> j & 1) == (inner == 0), "off-diagonal K contact")
        need((b >> i) & 1 == 0 and ((k >> i) & 1) == 1,
             "binary Gram/contact diagonal control")
        b_rows.append(b)
        k_rows.append(k)
    need(f2rank(b_rows) == 8 and f2rank(k_rows) == 9, "F2 Gram and fitting ranks")

    # Verify the geometric contact relation directly in each actual receiver
    # facet, rather than inferring it only from the normal inner product.
    for i in range(111):
        facet = frames[native["final"][111 + i]]
        need(facet["dim"] == 7 and qrank(facet["B"]) == 7,
             ("receiver facet rank", i))
        need(all(dot(g2[i], [Fraction(x) for x in row]) == 0
                 for row in facet["B"]), ("receiver normal", i))
        for j in range(111):
            contained = qrank(facet["B"] + [g2[j]]) == 7
            if i == j:
                need(not contained and (k_rows[i] >> j) & 1,
                     "K diagonal is identity augmentation, not a self-contact")
            else:
                need(contained == bool((k_rows[i] >> j) & 1),
                     ("actual line-to-facet contact", i, j))

    basis, selected = f2basis(k_rows)
    decoder = [f2solve(basis, row) for row in k_rows]
    need(len(selected) == 9 and all(x is not None for x in decoder),
         "nine-row exact fitting factorization")
    encoder_rows = [k_rows[i] for i in selected]
    for i, mask in enumerate(decoder):
        row = 0
        for j, enc in enumerate(encoder_rows):
            if (mask >> j) & 1:
                row ^= enc
        need(row == k_rows[i], ("K decoder", i))
    residual = [k_rows[i] ^ (1 << i) for i in range(111)]
    need(f2rank(residual) == 108, "K+I residual rank")
    residual_coefficients = sum(r.bit_count() for r in residual)
    need(residual_coefficients == 6470, "K+I residual coefficient count")
    nonzero_residual_rows = sum(bool(r) for r in residual)

    # Independently replay the authenticated native endpoint and charged routes.
    native_rows, native_info = replay(native, frames)
    expected_native = [1 << i for i in range(659)]
    for i in range(111):
        expected_native[111 + i] ^= 1 << i
    need(native_rows == expected_native, "native X=x, Y=y+x, H=h endpoint")
    native_paid = Counter(native_info["paid_profile"])
    need(sum(native_paid.values()) == 2871, "native MOVE count")
    helper_target = Counter()
    for field in range(222, 659):
        start_dim = frames[native["start"][field]]["dim"]
        final_dim = frames[native["final"][field]]["dim"]
        helper_target[abs(final_dim - start_dim)] += 1
    need(helper_target == Counter({2: 1, 4: 25, 6: 1, 8: 410}),
         "437-helper target histogram")

    # Source-history contamination control: the X-only subsequence is a valid
    # *new* circuit, but its rows are generally not the native's actual values.
    full_rows = {i: 1 << i for i in range(659)}
    full_rows.update({i: 0 for i in range(659, 896)})
    x_rows = [1 << i for i in range(111)]
    x_where = native["start"][:111].copy()
    seen = set()
    pure_histories = []

    def record_x_history(event, field):
        key = (x_where[field], x_rows[field])
        if key in seen:
            return
        seen.add(key)
        actual = full_rows[field]
        pure_histories.append({
            "event": event,
            "field": field,
            "pure_row": x_rows[field],
            "actual_x_row": actual & ((1 << 111) - 1),
            "foreign_inputs": actual >> 111,
        })

    for i in range(111):
        record_x_history(-1, i)
    x_adds = 0
    x_moves = Counter()
    x_to_nonx_adds = 0
    for event, ins in enumerate(native["program"]):
        op, a = ins[:2]
        # Full actual public/owned F2 coefficient replay.
        if op == "ADD":
            b = ins[2]
            full_rows[a] ^= full_rows[b]
            if a < 111 and b >= 111:
                x_to_nonx_adds += 1
        elif op == "SWAP":
            b = ins[2]
            full_rows[a], full_rows[b] = full_rows[b], full_rows[a]
        elif op in ("INIT", "CLEAR"):
            full_rows[a] = 0

        # The extracted X-only subword deliberately omits every non-X operand.
        if a >= 111:
            continue
        if op in ("ADD", "SWAP"):
            b = ins[2]
            if b >= 111:
                continue
            if op == "ADD":
                x_rows[a] ^= x_rows[b]
                x_adds += 1
            else:
                x_rows[a], x_rows[b] = x_rows[b], x_rows[a]
                x_where[a], x_where[b] = x_where[b], x_where[a]
            record_x_history(event, a)
            if op == "SWAP":
                record_x_history(event, b)
        elif op == "MOVE":
            source, target = ins[2:]
            need(x_where[a] == source, ("X-subword route source", event, ins))
            x_moves[abs(frames[target]["dim"] - frames[source]["dim"])] += 1
            x_where[a] = target
            record_x_history(event, a)
    need(all(x_rows[i] == 1 << i for i in range(111)), "extracted X-only word identity")
    need(x_where == native["final"][:111], "extracted X-only final charts")
    need(x_adds == 628 and x_moves == Counter({1: 289, 2: 244}),
         "extracted X-only operation profile")
    need(len(pure_histories) == 1027 and x_to_nonx_adds == 1702,
         "source contamination control cardinalities")
    history_mismatches = sum(h["pure_row"] != h["actual_x_row"] for h in pure_histories)
    history_contaminated = sum(bool(h["foreign_inputs"]) for h in pure_histories)
    history_clean_equal = sum(h["pure_row"] == h["actual_x_row"] and
                              not h["foreign_inputs"] for h in pure_histories)
    need((history_mismatches, history_contaminated, history_clean_equal) == (670, 914, 111),
         "full-native history contamination negative control")

    # Replay the frozen 222-input Q and its m=4 shared-native word.
    rail_bytes = (package / "RAIL.json.gz").read_bytes()
    m4_bytes = (package / "M4-WORD.json.gz").read_bytes()
    rail = json.loads(gzip.decompress(rail_bytes))
    m4 = json.loads(gzip.decompress(m4_bytes))
    rail_receipt = json.loads((package / "RAIL-RESULT.json").read_text())
    m4_receipt = json.loads((package / "M4-RESULT.json").read_text())
    rail_rows, rail_info = replay(rail, frames)
    need(rail["public"] == 222 and rail["start"] == native["start"][:222]
         and rail["final"] == native["final"][:222], "Q source/target charts")
    expected_rail = [1 << i for i in range(111)]
    expected_rail += [(1 << (111 + i)) ^ k_rows[i] for i in range(111)]
    need(rail_rows == expected_rail, "Q exact partial map (X,Y+KX)")
    need(rail_info["operations"] == 1267 and
         rail_info["paid_profile"] == {7: 222, 8: 9} and
         rail_info["retired_lifetimes"] == 9 and rail_info["peak_owned"] == 1,
         "Q physical/owned ledger")
    need(rail_info["distinct_nested_move_pairs"] == 223,
         "Q nested MOVE pair census")
    need(rail_receipt["status"] == "PASS_EXACT_PARTIAL_RAIL_NOT_COMPLETE_Q" and
         rail_receipt["word_sha256"] == sha(rail_bytes) and
         rail_receipt["fitting_rows"] == k_rows and
         rail_receipt["encoder_source_rows"] == selected and
         rail_receipt["encoder_rows"] == encoder_rows and
         rail_receipt["decoder_masks"] == decoder and
         rail_receipt["residual_rank"] == 108 and
         rail_receipt["residual_nonzero_coefficients"] == 6470,
         "author rail receipt agrees with independent reconstruction")

    m4_rows, m4_info = replay(m4, frames)
    m = m4["multiplicity"]
    need(m == 4 and m4["public"] == 659 + 222 * (m - 1), "m4 dimensions")
    base_private = 659
    expected_m4 = [1 << i for i in range(m4["public"])]
    # Common main outputs: one correct native result plus each private Q error.
    for i in range(111):
        common_y = 111 + i
        expected_m4[common_y] ^= 1 << i
        for k in range(m - 1):
            base = base_private + 222 * k
            residual_block = sum(1 << (base + j) for j in range(111)
                                 if (residual[i] >> j) & 1)
            expected_m4[common_y] ^= residual_block
            expected_m4[base + 111 + i] ^= k_rows[i] << base
    need(m4_rows == expected_m4, "m4 exact common/private partial endpoint")
    need(all(m4_rows[i] == 1 << i for i in range(222, 659)),
         "m4 common helper inputs/outputs unchanged")
    need(m4_info["operations"] == 39270 and m4_info["move_count"] == 3564 and
         m4_info["retired_lifetimes"] == 264 and m4_info["peak_owned"] == 237,
         "m4 literal operation and ownership ledger")
    expected_m4_paid = Counter(native_paid)
    for rank, count in rail_info["paid_profile"].items():
        expected_m4_paid[rank] += (m - 1) * count
    need(Counter(m4_info["paid_profile"]) == expected_m4_paid,
         "m4 paid profile is one native plus three Q rails")
    need(len(m4_info["swaps"]) == 3 and
         all(frames[b]["dim"] != frames[d]["dim"] for _, _, _, b, d in m4_info["swaps"]),
         "m4 retained role swaps include unequal-chart examples")
    need(m4_receipt["status"] == "PASS_EXACT_SHARED_NATIVE_PARTIAL_WORD" and
         m4_receipt["word_sha256"] == sha(m4_bytes) and
         m4_receipt["operations"] == m4_info["operations"] and
         m4_receipt["paid_profile"] == {str(r): c for r, c in m4_info["paid_profile"].items()} and
         m4_receipt["retired_lifetimes"] == m4_info["retired_lifetimes"] and
         m4_receipt["peak_owned"] == m4_info["peak_owned"],
         "author m4 receipt agrees with independent replay")

    # Cross-check caller profiles and the exact even-m formula.
    baseline_path = repository / "research/moonshot-005-program/results/bit-query-budget/RESULT.json"
    baseline_raw = baseline_path.read_bytes()
    need(sha(baseline_raw) == BASELINE_SHA, "reviewed paired caller profile pin")
    baseline = json.loads(baseline_raw)
    need(baseline["source_pins"]["research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz"] == NATIVE_SHA,
         "paired caller ledger pins this native")
    ledger_N = Counter({int(k): v for k, v in baseline["native_paid"].items()})
    ledger_H = Counter({int(k): v for k, v in baseline["native_helpers"].items()})
    need(ledger_N == native_paid and ledger_H == helper_target,
         "caller ledger native paid/helper profiles independently rederived")
    P2 = Counter({r: 36 * c for r, c in native_paid.items()})
    T2 = Counter({r: 36 * c for r, c in helper_target.items()})
    P2[1] += 444
    for j in range(1, 9):
        P2[7 * j] += 444
    T2[127] += 222
    for j in range(1, 10):
        T2[1 + 7 * j] += 444
    ledger_P = Counter({int(k): v for k, v in baseline["paid"].items()})
    ledger_T = Counter({int(k): v for k, v in baseline["targets"].items()})
    need(P2 == ledger_P and T2 == ledger_T, "paired P2/T2 caller profile identities")

    Q_paid = Counter(rail_info["paid_profile"])
    Pm = Counter({r: (m // 2) * c for r, c in P2.items()})
    Tm = Counter({r: (m // 2) * c for r, c in T2.items()})
    for r, c in native_paid.items():
        Pm[r] -= 18 * (m - 1) * c
    for r, c in Q_paid.items():
        Pm[r] += 18 * (m - 1) * c
    for r, c in helper_target.items():
        Tm[r] -= 18 * (m - 1) * c
    need(min(Pm.values()) >= 0 and min(Tm.values()) >= 0,
         "conditional histogram nonnegative")
    budget = json.loads((package / "BUDGET.json").read_text())
    profile_json = lambda x: {str(r): c for r, c in sorted(x.items()) if c}
    need(profile_json(Pm) == budget["conditional_complete_paid"] and
         profile_json(Tm) == budget["conditional_complete_target"],
         "frozen conditional m4 caller histograms")

    M2 = profile_add((1, T2), (-1, P2))
    NH = profile_add((1, native_paid), (-1, helper_target))
    q_partial = dict(Q_paid)
    limiting = profile_add((1, NH), (Fraction(1, 36), M2))
    limiting_room = profile_add((1, limiting), (-1, q_partial))
    exact_intervals = {
        "original_paired_margin": moment(M2),
        "Q_moment": moment(q_partial),
        "limiting_Q_allowance": moment(limiting),
        "limiting_remaining_completion_room": moment(limiting_room),
    }
    m_rooms = {}
    for mm in (2, 4, 6, 8, 16, 32):
        allowance = profile_add((1, NH), (Fraction(mm, 36 * (mm - 1)), M2))
        m_rooms[str(mm)] = moment(profile_add((1, allowance), (-1, q_partial)))
    exact_intervals["fixed_even_m_remaining_completion_room"] = m_rooms
    exact_intervals["mcopy_conditional_complete_margin"] = moment(profile_add((1, Tm), (-1, Pm)))
    stored = budget["at_t_199_over_200"]
    for key in ("original_paired_margin", "Q_moment", "limiting_Q_allowance",
                "limiting_remaining_completion_room", "mcopy_conditional_complete_margin"):
        need(interval_strings(exact_intervals[key]) ==
             [stored[key]["exact_lower"], stored[key]["exact_upper"]],
             ("exact budget interval", key))
    for mm, interval in m_rooms.items():
        need(interval_strings(interval) ==
             [stored["fixed_even_m_remaining_completion_room"][mm]["exact_lower"],
              stored["fixed_even_m_remaining_completion_room"][mm]["exact_upper"]],
             ("fixed-m exact room", mm))
    old_m2 = baseline["margin_intervals_by_free_queries_removed"]["0"]
    need(exact_intervals["original_paired_margin"][0] >= Fraction(old_m2[0]) and
         exact_intervals["original_paired_margin"][1] <= Fraction(old_m2[1]),
         "independent 128-bit M2 enclosure is inside old 88-bit interval")
    need(exact_intervals["original_paired_margin"][1] < 0,
         "paired baseline margin negative")
    need(m_rooms["2"][1] < 0 < m_rooms["4"][0],
         "m2 fails and m4 provisional completion allowance is positive")

    # Wrong-chart SWAP mutant: changing values but retaining fixed charts must
    # disagree with the pinned endpoint. Source swaps are role permutations.
    fixed_chart_where = dict(enumerate(native["start"]))
    fixed_chart_rows = {i: 1 << i for i in range(659)}
    fixed_chart_rows.update({i: 0 for i in range(659, 896)})
    for ins in native["program"]:
        op, a = ins[:2]
        if op == "ADD":
            fixed_chart_rows[a] ^= fixed_chart_rows[ins[2]]
        elif op == "SWAP":
            b = ins[2]
            fixed_chart_rows[a], fixed_chart_rows[b] = fixed_chart_rows[b], fixed_chart_rows[a]
            # Deliberately retain each field's old chart as the bad mutant.
        elif op == "MOVE":
            fixed_chart_where[a] = ins[3]
        elif op == "INIT":
            fixed_chart_rows[a] = 0
            fixed_chart_where[a] = ins[2]
        elif op == "CLEAR":
            fixed_chart_rows[a] = 0
            fixed_chart_where.pop(a, None)
    wrong_swap_endpoint_mismatches = sum(
        fixed_chart_rows[i] != expected_native[i] for i in range(659)
    )
    wrong_swap_chart_mismatches = sum(
        fixed_chart_where.get(i) != native["final"][i] for i in range(659)
    )
    need(wrong_swap_endpoint_mismatches == 0 and wrong_swap_chart_mismatches == 6,
         "fixed-chart swap mutant preserves values but fails six endpoint charts")

    result = {
        "status": "PASS_INDEPENDENT_BIT_NINE_RAIL_AND_M4_AUDIT",
        "source_sha256": NATIVE_SHA,
        "frozen_author_manifest_sha256": sha((package / "MANIFEST.json").read_bytes()),
        "baseline_profile_receipt_sha256": BASELINE_SHA,
        "source_root_norms_before_common_scaling": {str(k): v for k, v in sorted(raw_norms.items())},
        "source_projective_roots": 111,
        "generated_full_E8_root_lines": len(closure),
        "source_root_span_rank": 8,
        "binary_gram_rank": f2rank(b_rows),
        "contact_plus_identity_rank": f2rank(k_rows),
        "fitting_encoder_source_rows": selected,
        "all_111_decoder_masks_exact": True,
        "receiver_facet_checks": 111,
        "off_diagonal_contact_identity": True,
        "contact_plus_identity_diagonal_is_not_a_self_contact": True,
        "residual_rank": f2rank(residual),
        "residual_nonzero_coefficients": residual_coefficients,
        "residual_nonzero_receiver_rows": nonzero_residual_rows,
        "native_endpoint_replay": native_info,
        "rail_replay": rail_info,
        "m4_replay": m4_info,
        "m4_exact_map": "common=(F u0)+sum_{k=1..3}(F-Q)u_k; private_k=Q u_k; helpers=h",
        "screen_history_negative_control": {
            "X_to_nonX_ADD_count": x_to_nonx_adds,
            "distinct_pure_X_history_count": len(pure_histories),
            "history_X_row_mismatches_vs_actual_native": history_mismatches,
            "histories_with_foreign_input_contamination": history_contaminated,
            "histories_clean_and_equal": history_clean_equal,
            "scope": "The screen's X-only subword is a valid new independent circuit; its recorded intermediate rows are not generally actual native field values. The emitted Q does not reuse them."
        },
        "paired_caller_profile_crosscheck": {
            "native_paid": dict(sorted(native_paid.items())),
            "helper_target": dict(sorted(helper_target.items())),
            "paired_paid_formula_matches_reviewed_receipt": True,
            "paired_target_formula_matches_reviewed_receipt": True,
            "caller_event_replay": "Not repeated: EFREE-CALLER.json.gz is absent from this checkout. The independently reviewed hash-pinned RESULT profile was checked exactly against N/H and the stated histogram formulas."
        },
        "moment_intervals_199_over_200": {
            k: interval_strings(v) for k, v in exact_intervals.items()
            if k != "fixed_even_m_remaining_completion_room"
        },
        "fixed_even_m_remaining_completion_room": {
            k: interval_strings(v) for k, v in m_rooms.items()
        },
        "negative_controls": {
            "K_diagonal": "1 by J augmentation, but g_i is not orthogonal to itself; RAIL removes I before calling K+I the residual.",
            "value_only_swap": {"native_endpoint_mismatches": wrong_swap_endpoint_mismatches,
                                "wrong_endpoint_chart_count": wrong_swap_chart_mismatches,
                                "source_swaps": native_info["swaps"]},
            "partial_Q": "6470 missing K+I coefficients and residual rank108 remain; no completion credit is included."
        },
        "scope": "Exact scalar source/rail and m4 partial map plus conditional even-m profile arithmetic. No completed Q, supplier, ordinary/compiler/precision bill, physical all-width admission, or new kappa."
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "source_projective_roots": result["source_projective_roots"],
        "generated_full_E8_root_lines": result["generated_full_E8_root_lines"],
        "binary_gram_rank": result["binary_gram_rank"],
        "fitting_rank": result["contact_plus_identity_rank"],
        "rail_paid": rail_info["paid_profile"],
        "m4_operations": m4_info["operations"],
        "m4_paid_moves": m4_info["move_count"],
        "residual_rank_and_ones": [f2rank(residual), residual_coefficients],
        "m4_room": interval_strings(m_rooms["4"]),
        "limiting_room": interval_strings(exact_intervals["limiting_remaining_completion_room"]),
        "screen_history_negative_control": [history_mismatches, history_contaminated, history_clean_equal],
    }, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    main(parser.parse_args())
