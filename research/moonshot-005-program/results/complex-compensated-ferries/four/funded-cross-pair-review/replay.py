#!/usr/bin/env python3
"""Independent exact replay for the frozen funded-cross-pair word.

This uses its own sparse Fraction interpreter and endpoint linear algebra. It
does not import the author's extractor, builder, or replay engine.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path


PARENT_SHA = "a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc"
WORD_SHA = "787ae38760119ce9b628c3b9eff0244271b3c0ad65b646c725730a2142d6dc1a"
NATIVE_SHA = "2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883"


def need(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_gz(path: Path) -> tuple[bytes, dict]:
    blob = path.read_bytes()
    return blob, json.loads(gzip.decompress(blob))


def span(frame: list[int]) -> frozenset[int]:
    out = {0}
    for v in frame:
        out |= {x ^ v for x in tuple(out)}
    return frozenset(out)


def plus(dst: dict[int, F], src: dict[int, F], scale: F = F(1)) -> dict[int, F]:
    out = dict(dst)
    for k, v in src.items():
        z = out.get(k, F(0)) + scale * v
        if z:
            out[k] = z
        else:
            out.pop(k, None)
    return out


def replay(word: dict, *, basis: bool = True) -> tuple[dict[int, dict[int, F]], dict[int, int], dict]:
    n = word["public"]
    owneds = word["owned_fields"]
    frames = word["frames"]
    spaces = [span(frame) for frame in frames]
    dims = [len(frame) for frame in frames]
    loc = dict(enumerate(word["initial"]))
    rows = {i: ({i: F(1)} if basis else {}) for i in range(n)}
    op_counts: Counter[str] = Counter()
    all_moves: Counter[tuple[int, int, int, bool]] = Counter()
    raw_moves: Counter[tuple[int, int, int]] = Counter()
    move_ranks: Counter[int] = Counter()
    life = peak = 0

    for t, op in enumerate(word["program"]):
        kind, dst = op[:2]
        need(dst in range(n + owneds), f"event {t}: destination out of declaration")
        op_counts[kind] += 1
        if kind == "INIT":
            need(dst >= n and dst not in loc, f"event {t}: invalid owner INIT {op}")
            need(op[2] in range(len(frames)), f"event {t}: invalid INIT chart")
            loc[dst] = op[2]
            rows[dst] = {}
            life += 1
        elif kind == "CLEAR":
            need(dst >= n and loc.get(dst) == op[2], f"event {t}: invalid owner CLEAR {op}")
            del loc[dst]
            del rows[dst]
        elif kind == "MOVE":
            a, b, owned = op[2:]
            need(type(owned) is bool and owned == (dst >= n), f"event {t}: owner bit mismatch")
            need(loc.get(dst) == a, f"event {t}: stale MOVE source {op}")
            need(a in range(len(frames)) and b in range(len(frames)), f"event {t}: bad MOVE chart")
            ascends = spaces[a] < spaces[b]
            descends = spaces[b] < spaces[a]
            need(ascends or owned and descends, f"event {t}: nonnested MOVE {a}->{b}")
            rank = abs(dims[a] - dims[b])
            move_ranks[rank] += 1
            all_moves[a, b, dst, owned] += 1
            if not owned:
                raw_moves[a, b, dst] += 1
            loc[dst] = b
        elif kind in ("ADD", "COPY"):
            src, coeff, chart = op[2:]
            need(src != dst, f"event {t}: aliased ADD/COPY")
            need(loc.get(dst) == loc.get(src) == chart, f"event {t}: cochart failure {op}")
            scale = F(coeff)
            if kind == "COPY":
                need(not rows[dst], f"event {t}: COPY into nonzero destination")
                rows[dst] = {k: scale * v for k, v in rows[src].items() if scale * v}
            else:
                rows[dst] = plus(rows[dst], rows[src], scale)
        elif kind == "SCALE":
            coeff, chart = op[2:]
            need(loc.get(dst) == chart and F(coeff) != 0, f"event {t}: invalid SCALE {op}")
            c = F(coeff)
            rows[dst] = {k: c * v for k, v in rows[dst].items() if c * v}
        else:
            raise AssertionError(f"event {t}: unknown opcode {kind}")
        peak = max(peak, len(loc) - n)

    need(set(loc) == set(range(n)), "final live set is not exactly public rows")
    bill = {
        "instructions": len(word["program"]),
        "op_counts": dict(sorted(op_counts.items())),
        "move_ranks": dict(sorted(move_ranks.items())),
        "lifetimes": life,
        "peak": peak,
        "final_owned": len(loc) - n,
        "all_move_pairs": all_moves,
        "raw_move_pairs": raw_moves,
    }
    return rows, loc, bill


def rank(rows: list[dict[int, F]]) -> int:
    basis: dict[int, dict[int, F]] = {}
    for row0 in rows:
        row = dict(row0)
        while row:
            pivot = min(row)
            if pivot not in basis:
                c = row[pivot]
                basis[pivot] = {k: v / c for k, v in row.items()}
                break
            c = row[pivot]
            row = plus(row, basis[pivot], -c)
    return len(basis)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", type=Path, required=True)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    parent_blob, parent = load_gz(args.package / "source-evidence/rail-consumer.json.gz")
    word_blob, word = load_gz(args.package / "output/rail-cross-pair.json.gz")
    native_blob = (args.source / "research/shared-wire-split-composition/data/final.json.gz").read_bytes()
    need(sha(parent_blob) == PARENT_SHA, "parent Q pin")
    need(sha(word_blob) == WORD_SHA, "candidate word pin")
    need(sha(native_blob) == NATIVE_SHA, "native source pin")
    need(parent["public"] == word["public"] == 400, "400 public domain")
    need(parent["frames"] == word["frames"] and parent["initial"] == word["initial"], "same chart interface")
    need(parent["owned_fields"] == word["owned_fields"] == 93, "same owner declaration")
    native = json.loads(gzip.decompress(native_blob))

    before, before_loc, old_bill = replay(parent)
    after, after_loc, new_bill = replay(word)
    need(before_loc == after_loc, "all final chart locations unchanged")

    # Every original opcode is retained exactly except the two packet descents;
    # inserted operations have no parent lineage.
    lineage = word.get("parent_event_of_output")
    need(isinstance(lineage, list) and len(lineage) == len(word["program"]), "event lineage table")
    seen_parent = Counter(i for i in lineage if i is not None)
    need(all(count == 1 for count in seen_parent.values()), "duplicate parent event lineage")
    removed = sorted(set(range(len(parent["program"]))) - set(seen_parent))
    need(removed == [3528, 3661], f"unexpected removed parent events {removed}")
    for k, old in enumerate(lineage):
        if old is not None:
            need(word["program"][k] == parent["program"][old], f"nonliteral inherited event at output {k}")

    # The exact precode is derived from the first two original packet decoders.
    packets = []
    for k, op in enumerate(parent["program"]):
        if op != ["INIT", 451, 127]:
            continue
        down = next(i for i in range(k + 1, len(parent["program"])) if parent["program"][i] == ["MOVE", 451, 127, 3, True])
        end = next(i for i in range(down + 1, len(parent["program"])) if parent["program"][i] == ["CLEAR", 451, 3])
        alpha: dict[int, F] = {}
        for o in parent["program"][k + 1:down]:
            need(o[0] == "ADD" and o[1] == 451 and o[4] == 127, "packet encoder shape")
            alpha[o[2]] = alpha.get(o[2], F(0)) + F(o[3])
        beta: dict[int, F] = {}
        for o in parent["program"][down + 1:end]:
            need(o[0] == "ADD" and o[2] == 451 and o[4] == 3, "packet decoder shape")
            beta[o[1]] = beta.get(o[1], F(0)) + F(o[3])
        packets.append({"begin": k, "down": down, "end": end, "alpha": alpha, "beta": beta})
    need(len(packets) == 8, "eight old packets")
    pair_specs = [(1, 106, 209, 394, 226, 1), (106, 1, 298, 305, 129, 99)]
    precode = word["program"][40:170]
    expected_precode = []
    for (_, dport, _b, _drole, _facet, _line), packet in zip(pair_specs, packets[:2]):
        for r, c in packet["beta"].items():
            expected_precode.append(["ADD", r, _drole, str(-c), 3])
    need(precode == expected_precode and len(precode) == 130, "actual beta precode formula/order")
    need(word["program"][170:172] == [["MOVE", 394, 3, 226, False], ["MOVE", 305, 3, 129, False]], "literal D hoists")

    # Reconstruct the two funded carrier handoffs and the actual cleanup, not
    # just their net endpoint effect.
    pair_events = word["funded_cross_pair"]["packet_events"]
    expected_handoffs = [
        [
            ["MOVE", 451, 127, 226, True],
            ["ADD", 451, 394, "1", 226],
            ["MOVE", 451, 226, 1, True],
            ["ADD", 209, 451, "-1", 1],
            ["MOVE", 451, 1, 3, True],
        ],
        [
            ["MOVE", 451, 127, 129, True],
            ["ADD", 451, 305, "1", 129],
            ["MOVE", 451, 129, 99, True],
            ["ADD", 298, 451, "-1", 99],
            ["MOVE", 451, 99, 3, True],
        ],
    ]
    for event, expected_ops, expected_begin, old_down in zip(
        pair_events, expected_handoffs, (2016, 2153), (3528, 3661)
    ):
        need(event["begin"] == expected_begin and event["old_down"] == old_down, "handoff event boundary")
        need(word["program"][event["begin"]:event["end"]] == expected_ops, "literal causal handoff itinerary")
    need(word["funded_cross_pair"]["precode_range"] == [40, 170], "precode chronology")
    need(word["funded_cross_pair"]["primal_end"] == 3201, "primal bank endpoint")
    cleanup = word["funded_cross_pair"]["controller_cleanup"]
    for item, packet, target in zip(cleanup, packets[:2], (209, 298)):
        expected_ops = [["ADD", target, src, str(c), 127] for src, c in packet["alpha"].items()]
        need(word["program"][item["begin"]:item["end"]] == expected_ops, "controller uses exact old encoder")

    # An independent two-tag suffix trace begins at the actual untouched B
    # boundaries in the original word. It catches any feedback/spreading into
    # a foreign final output, including intermediate owner records.
    first_touch = {}
    for i, op in enumerate(parent["program"]):
        for row in (209, 298):
            if row not in first_touch and (op[1] == row or op[0] in ("ADD", "COPY") and op[2] == row):
                first_touch[row] = i
    need(first_touch == {209: 530, 298: 534}, "B rows are untouched before actual boundary")
    tags = {i: {} for i in range(400)}
    tags[209] = {10000: F(1)}
    tags[298] = {10001: F(1)}
    tag_events = 0
    for i, op in enumerate(parent["program"][530:], 530):
        kind, dst = op[:2]
        src_tags = tags.get(op[2], {}) if kind in ("ADD", "COPY") else {}
        dst_tags = tags.get(dst, {})
        if src_tags or dst_tags:
            tag_events += 1
        if kind == "INIT":
            tags[dst] = {}
        elif kind == "CLEAR":
            tags.pop(dst, None)
        elif kind == "MOVE":
            pass
        elif kind == "ADD":
            tags[dst] = plus(tags.get(dst, {}), tags.get(op[2], {}), F(op[3]))
        elif kind == "COPY":
            need(not tags.get(dst, {}), f"tag COPY into live record at old event {i}")
            tags[dst] = {k: F(op[3]) * v for k, v in tags.get(op[2], {}).items() if F(op[3]) * v}
        elif kind == "SCALE":
            c = F(op[2])
            tags[dst] = {k: c * v for k, v in tags.get(dst, {}).items() if c * v}
    tag_transfer = {r: vals for r, vals in tags.items() if vals}
    need(tag_transfer == {209: {10000: F(1)}, 298: {10001: F(1)},}, "two exact original suffix columns")

    # Unique D use and true initial B input boundaries.
    for drow, move in [(394, ["MOVE", 394, 3, 226, False]), (305, ["MOVE", 305, 3, 129, False])]:
        uses = [o for o in parent["program"] if o[1] == drow or o[0] in ("ADD", "COPY") and o[2] == drow]
        need(uses == [move], f"D row {drow} has other old use/write")

    # Exact endpoint deltas and untouched first-X/first-Y duties.
    roles = {int(k): int(v) for k, v in word["source_role_map"].items()}
    host = {
        native["live"][k]: (x, y)
        for k, x, y in zip(native["hosted"]["Dports"], native["hosted"]["X2"], native["hosted"]["Y2"])
    }
    need(
        (roles[host[1][0]], roles[host[106][0]], roles[host[106][1]], roles[host[1][1]])
        == (209, 298, 394, 305),
        "logical ports map to the claimed B and D rows",
    )
    live = native["live"]
    xrows = {roles[j] for j in live}
    yrows = {roles[j + 112] for j in live}
    need(len(xrows) == len(yrows) == 104, "104 original first-X/first-Y rows")
    need(set(packets[0]["alpha"]) <= xrows and set(packets[1]["alpha"]) <= xrows, "both controllers use first-X rows")
    need(set(packets[0]["beta"]) <= yrows and set(packets[1]["beta"]) <= yrows, "both decoders write first-Y rows")
    need(all(before[r] == after[r] for r in xrows | yrows), "first-X/first-Y endpoints changed")

    # Causal checkpoints: every old primal record is restored before the dual
    # suffix, and the cleanup reconstructs each controller from live Hub rows.
    p_end = word["funded_cross_pair"]["primal_end"]
    c0, loc0, _ = replay({**word, "program": word["program"][:p_end]})
    need(all(c0[r] == before[r] for r in xrows | yrows), "first-X/first-Y map at primal boundary")
    need(all(loc0[r] == before_loc[r] for r in xrows | yrows), "first-X/first-Y chart at primal boundary")
    clean_begin = cleanup[0]["begin"]
    c1, loc1, _ = replay({**word, "program": word["program"][:clean_begin]})
    for packet in packets[:2]:
        for src in packet["alpha"]:
            need(c1[src] == before[src] and loc1[src] == 127, "live unchanged Hub controller source before cleanup")
    delta = {r: plus(after[r], before[r], F(-1)) for r in range(400)}
    changed = {r: row for r, row in delta.items() if row}
    need(set(changed) == {209, 298}, f"unexpected changed public endpoints {sorted(changed)}")
    need(changed[209] == {394: F(-1)} and changed[298] == {305: F(-1)}, "cross-D endpoint changes")

    def residuals(rows: dict[int, dict[int, F]]) -> list[dict[int, F]]:
        out = []
        for b, d in host.values():
            out.append(plus(rows[roles[b]], {roles[b]: F(1), roles[d]: F(-1)}, F(-1)))
        return out

    old_res = residuals(before)
    new_res = residuals(after)
    need(rank(old_res) == 58 and rank(new_res) == 57, "reverse residual rank 58->57")
    zero_old = [h for h, r in zip(host, old_res) if not r]
    zero_new = [h for h, r in zip(host, new_res) if not r]
    need(zero_old == zero_new and len(zero_new) == 24, "previous 24 reverse completions retained")
    i1, i106 = list(host).index(1), list(host).index(106)
    need(new_res[i1] == {k: -v for k, v in new_res[i106].items()}, "new residual rows 1/106 are negatives")

    # Original-coordinate forward debt is explicitly unchanged.
    debt = 0
    for i in live:
        coeff = F(1) if i in host else F(1, 2)
        ideal = {roles[i]: coeff, roles[i + 112]: coeff}
        debt += len(plus(after[roles[i + 112]], ideal, F(-1)))
    need(debt == 4920, f"forward debt {debt}")

    # Public raw moves are exactly the original moves; added routes are owned.
    old_raw = Counter((o[2], o[3], o[1]) for o in parent["program"] if o[0] == "MOVE" and not o[4])
    new_raw = Counter((o[2], o[3], o[1]) for o in word["program"] if o[0] == "MOVE" and not o[4])
    need(old_raw == new_raw, "raw source routes changed")
    new_pairs = {(o[2], o[3]) for o in word["program"] if o[0] == "MOVE"} - {
        (o[2], o[3]) for o in parent["program"] if o[0] == "MOVE"
    }
    need(new_pairs == {(127, 129), (127, 226), (226, 1), (129, 99), (1, 3), (99, 3)}, "six actual new chart pairs")
    move_delta = Counter(new_bill["move_ranks"])
    move_delta.subtract(old_bill["move_ranks"])
    move_delta = {k: v for k, v in move_delta.items() if v}
    need(move_delta == {1: 4, 7: 2, 9: -2}, f"movement delta {move_delta}")
    need(new_bill["lifetimes"] == old_bill["lifetimes"] == 402 and new_bill["peak"] == old_bill["peak"] == 29, "owner bill")

    report = {
        "status": "PASS_INDEPENDENT_FUNDED_CROSS_PAIR_REPLAY",
        "parent_sha256": sha(parent_blob),
        "word_sha256": sha(word_blob),
        "native_sha256": sha(native_blob),
        "parent_bill": {
            k: (dict(v) if isinstance(v, Counter) else v)
            for k, v in old_bill.items()
            if k not in ("all_move_pairs", "raw_move_pairs")
        },
        "candidate_bill": {
            k: (dict(v) if isinstance(v, Counter) else v)
            for k, v in new_bill.items()
            if k not in ("all_move_pairs", "raw_move_pairs")
        },
        "lineage_missing_parent_events": removed,
        "raw_public_move_multiset_unchanged": True,
        "move_rank_delta": move_delta,
        "hoisted_D_single_use_rows": [394, 305],
        "precode_terms": len(precode),
        "handoff_event_ranges": [[x["begin"], x["end"]] for x in pair_events],
        "controller_cleanup_ranges": [[x["begin"], x["end"]] for x in cleanup],
        "first_old_B_touches": first_touch,
        "independent_suffix_tag_events": tag_events,
        "independent_suffix_tag_transfer": {
            str(r): {str(k): str(v) for k, v in vals.items()} for r, vals in tag_transfer.items()
        },
        "new_chart_pairs": sorted([list(x) for x in new_pairs]),
        "x_rows_unchanged": len(xrows),
        "y_rows_unchanged": len(yrows),
        "changed_endpoints": {str(k): {str(j): str(v) for j, v in sorted(row.items())} for k, row in changed.items()},
        "reverse_rank": {"parent": rank(old_res), "candidate": rank(new_res)},
        "completed_reverse_ports": zero_new,
        "original_coordinate_forward_debt": debt,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
