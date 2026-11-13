#!/usr/bin/env python3
"""Independent exact audit of the restored-cut ferry census and price.

This checker uses the separately written Worker C Fraction interpreter and a
small direct E8 root-coordinate constructor. It does not import the author's
extractor, checker, or root-coordinate engine.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path


Q_SHA = "a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc"
SOURCE_SHA = "2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883"
FULL_SHA = "d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7"
RESULT_SHA = "2b5eea66dfec83eef38090818f3241456250430dbb624c6797f88f8b7de8cd27"
FRAME = [0, 7, 20, 27, 36, 46, 57, 111]


def need(ok: bool, msg: str) -> None:
    if not ok:
        raise AssertionError(msg)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_gz(path: Path) -> tuple[bytes, dict]:
    blob = path.read_bytes()
    return blob, json.loads(gzip.decompress(blob))


def root9(v: int) -> tuple[F, ...]:
    """Exact norm-squared-2 E8 root vector encoded by a chart line."""
    support = {i for i in range(9) if (v >> i) & 1}
    if len(support) == 3:
        return tuple(F(int(i in support)) - F(1, 3) for i in range(9))
    need(len(support) == 7, f"line {v} has weight neither 3 nor 7")
    a, b = sorted(set(range(9)) - support)
    return tuple(F(int(i == a) - int(i == b)) for i in range(9))


def inner(a: tuple[F, ...], b: tuple[F, ...]) -> F:
    return sum((x * y for x, y in zip(a, b)), F(0))


def moment(profile: dict[int, F], places: int = 30) -> tuple[F, F]:
    den = 10**places
    lo = hi = F(0)
    for rank, coef in profile.items():
        if not rank or not coef:
            continue
        value = rank**199 * den**200
        left, right = 0, 1 << ((value.bit_length() + 199) // 200)
        while right - left > 1:
            mid = (left + right) // 2
            if mid**200 <= value:
                left = mid
            else:
                right = mid
        exact = left**200 == value
        low = F(left, den)
        high = low if exact else F(left + 1, den)
        if coef > 0:
            lo += coef * low
            hi += coef * high
        else:
            lo += coef * high
            hi += coef * low
    return lo, hi


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True, help="programme checkout")
    ap.add_argument("--lemma", type=Path, required=True, help="frozen author lemma package")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    interp_path = Path(__file__).resolve().parent / "interpreter.py"
    spec = importlib.util.spec_from_file_location("worker_c_ferry_interpreter", interp_path)
    interp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(interp)

    qb, q = read_gz(args.lemma / "source-evidence/rail-consumer.json.gz")
    sb, source = read_gz(args.repo / "research/shared-wire-split-composition/data/final.json.gz")
    fb = (args.repo / "research/shared-wire-split-composition/FULL-RESULT.json").read_bytes()
    full = json.loads(fb)
    rb = (args.lemma / "RESULT.json").read_bytes()
    author_result = json.loads(rb)
    need(sha(qb) == Q_SHA and sha(sb) == SOURCE_SHA and sha(fb) == FULL_SHA, "pinned parent/source/caller")
    need(sha(rb) == RESULT_SHA, "pinned author result for comparison only")

    roles = {int(k): int(v) for k, v in q["source_role_map"].items()}
    need(len(roles) == 400 and set(roles.values()) == set(range(400)), "private role map is a 400-row bijection")
    host = {
        source["live"][k]: (x, y)
        for k, x, y in zip(source["hosted"]["Dports"], source["hosted"]["X2"], source["hosted"]["Y2"])
    }
    H = list(host)
    need(len(H) == len(set(H)) == 96, "96 distinct hosted ports")
    rows, loc, bill = interp.replay(q)
    spans = [interp.span(frame) for frame in q["frames"]]

    census: dict[int, dict] = {}
    pure: list[int] = []
    B_roles, D_roles = {}, {}
    for h, (x, y) in host.items():
        b, d = roles[x], roles[y]
        B_roles[h], D_roles[h] = b, d
        need(all(rows[r].get(b, F(0)) == F(r == b) for r in range(400)), f"B column {h} is the isolated identity column")
        need(rows[d] == {d: F(1)}, f"D value {h} is unchanged")
        writes = [(i, op) for i, op in enumerate(q["program"]) if op[1] == d]
        need(all(op[0] == "MOVE" for _, op in writes), f"D {h} has only destination MOVE operations")
        reads = [
            {"event": i, "op": op}
            for i, op in enumerate(q["program"])
            if op[0] in ("ADD", "COPY") and op[2] == d
        ]
        single = len(writes) == 1 and writes[0][1] == ["MOVE", d, 3, loc[d], False]
        if single:
            need(all(r["op"][4] == loc[d] for r in reads), f"single-MOVE D {h} is read only at final facet")
            pure.append(h)
        census[h] = {
            "B_role": b,
            "D_role": d,
            "final_D_chart": loc[d],
            "D_writes": [{"event": i, "op": op} for i, op in writes],
            "D_reads": reads,
            "single_move_final_facet_only_reads": single,
        }
    need(len(pure) == 74 and len(H) - len(pure) == 22, "74 pure one-MOVE donors and 22 distinct-history donors")

    Bset, Dset = set(B_roles.values()), set(D_roles.values())
    first_xy = set(range(400)) - Bset - Dset
    need(len(first_xy) == 208 and len(Bset) == len(Dset) == 96, "public roles partition into 208 first-X/Y, 96 B, 96 D")
    need(all(not any(rows[r].get(D_roles[h], F(0)) for h in H) for r in first_xy), "all other public rows are D-independent")
    need(all(loc[B_roles[h]] == 127 for h in H), "all 96 B records are at the Hub in the restored cut")
    need(len({loc[D_roles[h]] for h in H}) == 96, "96 original D records occupy distinct restored facets")

    J = set(q["consumer"]["selected_return_ports"])
    M: list[list[F]] = []
    for h in H:
        row = [rows[B_roles[h]].get(D_roles[k], F(0)) + F(h == k) for k in H]
        M.append(row)
    M_rank = interp.rank([dict(enumerate(row)) for row in M])
    need(M_rank == 58 and len(J) == 31, "independently reconstructed M58 and J31")
    completed = {h for i, h in enumerate(H) if not any(M[i])}
    need(len(completed) == 24 and completed <= J, "24 zero rows remain inside the 31 returned ports")
    for i, h in enumerate(H):
        need(M[i][i] == F(h not in J), f"correct zero/nonzero diagonal on port {h}")

    # Direct reconstruction of the root Gram matrix from the frozen source's
    # 9-bit line encodings, without importing the author's root9 helper.
    roots = {h: root9(source["frames"][source["initial"][h]][0]) for h in H}
    G = [[inner(roots[h], roots[k]) / 2 for k in H] for h in H]
    frame_index = [H.index(h) for h in FRAME]
    need(set(FRAME) <= set(H) - J, "the selected eight ports are unreturned")
    need(
        all(G[frame_index[i]][frame_index[j]] == F(i == j) for i in range(8) for j in range(8)),
        "selected real-root frame is orthonormal",
    )

    # The contact at (i,j) means the initial B_i line is literally contained
    # in the final donor-D_j chart; direct GF(2) subspace membership is used.
    contact = [[source["frames"][source["initial"][h]][0] in spans[loc[D_roles[k]]] for k in H] for h in H]
    need(all(not contact[i][i] for i in range(96)), "self-facet contacts are forbidden for all 96 ports")
    need(all(contact[H.index(i)][H.index(j)] is False for i in FRAME for j in FRAME), "every contact in the selected 8x8 frame is forbidden")
    actual_minor = [[M[i][j] for j in frame_index] for i in frame_index]
    need(actual_minor == [[F(i == j) for j in range(8)] for i in range(8)], "actual M58 has the exact I8 principal minor")
    frame_contacts = [[contact[i][j] for j in frame_index] for i in frame_index]
    need(not any(any(row) for row in frame_contacts), "8x8 binary line-to-donor-facet contact matrix is zero")

    # Optimistic FREE completion: retain the selected 31 returned columns and
    # 24 completed rows, set every other entry to the full root Gram value.
    optimum = [[G[i][j] if H[i] not in completed and H[j] not in J else F(0) for j in range(96)] for i in range(96)]
    L = [[optimum[i][j] - M[i][j] for j in range(96)] for i in range(96)]
    for i, h in enumerate(H):
        for j, k in enumerate(H):
            if L[i][j]:
                need(i != j and contact[i][j], f"free difference at ({h},{k}) is an allowed off-diagonal contact")
    opt_rank = interp.rank([dict(enumerate(row)) for row in optimum])
    need(opt_rank == 8, "the explicit optimistic free matrix has rank 8")
    unreturned = [j for j, h in enumerate(H) if h not in J]
    need(len(unreturned) == 65 and all(optimum[j][j] == 1 for j in unreturned), "65 unreturned diagonal columns stay nonzero")
    opt_minor = [[optimum[i][j] for j in frame_index] for i in frame_index]
    need(opt_minor == [[F(i == j) for j in range(8)] for i in range(8)], "the free matrix also retains the exact I8 minor")

    # Recompute the complete-caller's limiting movement room and finite-m
    # correction from the already selected full-invoice formula.  Integer root
    # enclosures are evaluated here, not read from the author result.
    T = {int(k): F(v) for k, v in full["invoice"]["T"].items()}
    P = {int(k): F(v) for k, v in full["invoice"]["P"].items()}
    Hprof = {int(k): F(v) for k, v in full["native"]["helpers"].items()}
    N = {int(k): F(v) for k, v in full["native"]["paid"].items()}
    Q = {int(k): F(v) for k, v in bill["move_ranks"].items()}
    ranks = set(T) | set(P) | set(Hprof) | set(N) | set(Q) | {1}
    allowance = {r: (T.get(r, 0) - P.get(r, 0)) / 18 - Hprof.get(r, 0) + N.get(r, 0) - Q.get(r, 0) for r in ranks}
    terminal = dict(allowance)
    terminal[1] -= 65
    finite_slope = {r: (T.get(r, 0) - P.get(r, 0)) / 18 for r in ranks}
    free_bounds, terminal_bounds, slope_bounds = moment(allowance), moment(terminal), moment(finite_slope)
    need(slope_bounds[1] < 0, "exact finite-m correction coefficient is negative")
    need(terminal_bounds[1] < 0, "65 required rank-one departures strictly exceed limiting room")
    need(sha(rb) == RESULT_SHA, "result comparison source remains pinned")
    for actual, field, label in (
        (free_bounds, "limiting_free_ferry_margin_bounds", "limiting room"),
        (terminal_bounds, "limiting_after_terminal_bounds", "terminal deficit"),
        (slope_bounds, "finite_m_slope_bounds", "finite-m slope"),
    ):
        published = tuple(F(x) for x in author_result[field])
        need(published[0] <= actual[0] <= actual[1] <= published[1], f"published {label} enclosure contains independent interval")

    result = {
        "status": "PASS_INDEPENDENT_RESTORED_CUT_AND_FERRY_GEOMETRY_REVIEW",
        "pins": {"Q": sha(qb), "source": sha(sb), "full_caller": sha(fb), "author_result_for_comparison": sha(rb)},
        "parent_400_input_replay": {"input_directions": 400, "public_rows": 400, "B_identity_columns": 96, "unchanged_D_rows": 96, "rank_M58": M_rank},
        "restored_cut_public_partition": {"D_independent_first_XY_rows": len(first_xy), "B_rows_at_Hub": len(Bset), "D_rows_at_distinct_facets": len(Dset)},
        "D_census": {"pure_single_MOVE_donors": len(pure), "other_D_histories": 96 - len(pure)},
        "returned_ports": len(J),
        "completed_rows": len(completed),
        "frame_ports": FRAME,
        "actual_M58_frame_minor": [[str(x) for x in row] for row in actual_minor],
        "frame_contact_matrix": frame_contacts,
        "all_96_self_contacts_forbidden": True,
        "free_optimum_rank": opt_rank,
        "free_optimum_minor": [[str(x) for x in row] for row in opt_minor],
        "free_L_only_uses_allowed_offdiag_contacts": True,
        "unreturned_columns_nonzero": len(unreturned),
        "minimum_distinct_facet_departures_per_rail": len(unreturned),
        "width_V_interpretation": "For full-rank V-dimensional unreturned columns, each facet exports V independent information dimensions via at least one whole-V record departure; at least 65 whole-V departures per rail, each MOVE costing >=V rank-one units. This is 65 normalized movement atoms per rail, not 65V MOVE events.",
        "limiting_free_room_bounds": [str(x) for x in free_bounds],
        "terminal_room_after_65_unit_departures_bounds": [str(x) for x in terminal_bounds],
        "finite_m_correction_coefficient_bounds": [str(x) for x in slope_bounds],
        "finite_m_margin_identity": "terminal_limit + ((T-P)/18)_t/(m-1), for admissible fixed m>=2",
        "terminal_departure_claim_scope": "Restored cut with first-X/first-Y independent of D, all D_j at distinct original facets, only Hub state plus those facets carrying D, and each required unreturned D_j column nonzero (full column rank V for whole-record blocks); no surviving informative D-bearing record elsewhere. A first departure can move either upward or downward, but must be a strict chart move of positive rank.",
        "limitations": [
            "Rank-8 free optimum is proved only for the larger-than-physical algebraic class of zero-cost off-diagonal orthogonal line-deposit changes.",
            "The 65-departure argument is a distinct restored-cut theorem; it uses nonzero target columns and no retained D-bearing records, and does not rely on rank 8.",
            "For actual intermediate-line handoffs, a complete suffix-transfer column must vanish outside the intended B bank; B-bank projection alone does not suffice. The frozen rank54 word uses initial-line handoffs, and its eight-tag full-400 suffix check passes.",
            "This does not exclude preterminal informative retention, a changed current-row representation, or other architectures outside the stated cut.",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
