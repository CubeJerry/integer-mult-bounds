#!/usr/bin/env python3
"""Independent exact replay of the frozen rank-54 eight-ferry word.

Uses the separately written worker-c sparse Fraction interpreter. No author
builder, extractor, or source replay code is imported.
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


PARENT_SHA = "a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc"
WORD_SHA = "20a5c2c3eccd000b757f65e2cd6bed7f8a9ec39f0b8f88a66716e4b818a2521f"
NATIVE_SHA = "2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883"


def need(ok: bool, msg: str) -> None:
    if not ok:
        raise AssertionError(msg)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def readgz(path: Path) -> tuple[bytes, dict]:
    blob = path.read_bytes()
    return blob, json.loads(gzip.decompress(blob))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", type=Path, required=True)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    spec = importlib.util.spec_from_file_location(
        "worker_c_exact_replay",
        (Path(__file__).resolve().parent.parent / "funded-cross-pair-review" / "replay.py"),
    )
    rep = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rep)

    parent_blob, parent = readgz(args.package / "source-evidence/rail-consumer.json.gz")
    word_blob, word = readgz(args.package / "output/rail-cross-four.json.gz")
    source_blob = (args.source / "research/shared-wire-split-composition/data/final.json.gz").read_bytes()
    native = json.loads(gzip.decompress(source_blob))
    need(sha(parent_blob) == PARENT_SHA and sha(word_blob) == WORD_SHA and sha(source_blob) == NATIVE_SHA, "all source pins")
    need(parent["public"] == word["public"] == 400 and parent["frames"] == word["frames"], "same 400-direction chart domain")
    need(parent["initial"] == word["initial"] and parent["owned_fields"] == word["owned_fields"] == 93, "same initial interface and owner budget")

    before, before_loc, old_bill = rep.replay(parent)
    after, after_loc, new_bill = rep.replay(word)
    need(before_loc == after_loc, "all final charts exactly retained")
    metadata = word["funded_cross_pair"]
    pairs = metadata["pairs"]
    packet_events = metadata["packet_events"]
    need(len(pairs) == len(packet_events) == 8, "eight distinct directed ferries")
    need([p["target_port"] for p in pairs] == [1, 106, 2, 4, 11, 15, 23, 24], "source pair order")
    undirected = [(1, 106, F(-1)), (2, 4, F(1)), (11, 15, F(1)), (23, 24, F(1))]
    expected_coeff = {}
    for a, b, c in undirected:
        expected_coeff[a, b] = c
        expected_coeff[b, a] = F(1) / c
    need(
        [(p["target_port"], p["D_port"], F(p["coefficient"])) for p in pairs]
        == [(a, b, c) for (a, b), c in expected_coeff.items()],
        "four planned inverse-weighted port pairs",
    )

    roles = {int(k): int(v) for k, v in word["source_role_map"].items()}
    host = {native["live"][k]: (x, y) for k, x, y in zip(native["hosted"]["Dports"], native["hosted"]["X2"], native["hosted"]["Y2"])}
    need(
        all(roles[host[p["target_port"]][0]] == p["B"] and roles[host[p["D_port"]][1]] == p["D"] for p in pairs),
        "all eight B/D row labels match native port bindings",
    )

    # Reconstruct all eight native packet maps directly from the parent word.
    packets = []
    for k, op in enumerate(parent["program"]):
        if op != ["INIT", 451, 127]:
            continue
        down = next(i for i in range(k + 1, len(parent["program"])) if parent["program"][i] == ["MOVE", 451, 127, 3, True])
        end = next(i for i in range(down + 1, len(parent["program"])) if parent["program"][i] == ["CLEAR", 451, 3])
        alpha: dict[int, F] = {}
        for o in parent["program"][k + 1:down]:
            need(o[0] == "ADD" and o[1] == 451 and o[4] == 127, "old encoder event")
            alpha[o[2]] = alpha.get(o[2], F(0)) + F(o[3])
        beta: dict[int, F] = {}
        for o in parent["program"][down + 1:end]:
            need(o[0] == "ADD" and o[2] == 451 and o[4] == 3, "old decoder event")
            beta[o[1]] = beta.get(o[1], F(0)) + F(o[3])
        packets.append({"begin": k, "down": down, "end": end, "alpha": alpha, "beta": beta})
    need(len(packets) == 8, "eight actual old packet fields")
    for p, packet in zip(pairs, packets):
        recorded = p["packet"]
        need(
            (recorded["begin"], recorded["down"], recorded["end"])
            == (packet["begin"], packet["down"], packet["end"]),
            "each port pair is linked to the correct actual parent packet",
        )
        need(
            {int(k): F(v) for k, v in recorded["alpha"].items()} == packet["alpha"]
            and {int(k): F(v) for k, v in recorded["beta"].items()} == packet["beta"],
            "recorded packet maps equal maps independently extracted from parent operations",
        )

    # Exact precode from each actual decoder; exact literal D-only MOVE hoists.
    expected_precode = []
    for p, packet in zip(pairs, packets):
        for y, coefficient in packet["beta"].items():
            expected_precode.append(["ADD", y, p["D"], str(-coefficient), 3])
    start, stop = metadata["precode_range"]
    need((start, stop) == (40, 560) and word["program"][start:stop] == expected_precode, "520-term exact eight-mode Y precode")
    hoists = metadata["hoisted_D_events"]
    need(len(hoists) == 8 and [h["new_event"] for h in hoists] == list(range(560, 568)), "eight chronological donor hoists")
    for p in pairs:
        uses = [o for o in parent["program"] if o[1] == p["D"] or o[0] in ("ADD", "COPY") and o[2] == p["D"]]
        need(len(uses) == 1 and uses[0] == ["MOVE", p["D"], 3, p["facet"], False], f"D donor {p['D']} only has its old MOVE")
        old_index = next(i for i, o in enumerate(parent["program"]) if o == uses[0])
        need(old_index == p["old_D_MOVE"], "recorded donor event is the unique actual parent MOVE")
        h = next(h for h in hoists if h["old_event"] == p["old_D_MOVE"])
        need(h["op"] == uses[0] and word["program"][h["new_event"]] == uses[0], "literal donor MOVE retained")

    # Each packet performs its five-event, actual nested-chart handoff.
    for p, event in zip(pairs, packet_events):
        c = str(p["coefficient"])
        expected = [
            ["MOVE", 451, 127, p["facet"], True],
            ["ADD", 451, p["D"], "1", p["facet"]],
            ["MOVE", 451, p["facet"], p["line"], True],
            ["ADD", p["B"], 451, c, p["line"]],
            ["MOVE", 451, p["line"], 3, True],
        ]
        need(word["program"][event["begin"]:event["end"]] == expected, f"literal handoff itinerary {p['target_port']}<-{p['D_port']}")
        need(event["old_down"] == p["packet"]["down"], "replaces the right old packet descent")

    # Cleanup uses exactly the old packet encoder and only actual Hub X rows.
    cleanups = metadata["controller_cleanup"]
    need(len(cleanups) == 8, "eight controller cleanups")
    for p, packet, item in zip(pairs, packets, cleanups):
        c = F(p["coefficient"])
        expected = [["ADD", p["B"], src, str(-c * weight), 127] for src, weight in packet["alpha"].items()]
        need(word["program"][item["begin"]:item["end"]] == expected, "exact original X controller canceled")

    # Every parent operation is literal except the eight descents replaced by
    # the above handoffs. No other source/cost event is deleted or rewritten.
    lineage = word.get("parent_event_of_output")
    need(isinstance(lineage, list) and len(lineage) == len(word["program"]), "complete event lineage")
    seen = Counter(i for i in lineage if i is not None)
    need(all(v == 1 for v in seen.values()), "parent event lineage has no duplicates")
    removed = sorted(set(range(len(parent["program"]))) - set(seen))
    expected_removed = sorted(packet["down"] for packet in packets)
    need(removed == expected_removed, "only original packet descent MOVE events replaced")
    for i, old in enumerate(lineage):
        if old is not None:
            need(word["program"][i] == parent["program"][old], f"nonliteral original event {old}")

    live = native["live"]
    xrows = {roles[j] for j in live}
    yrows = {roles[j + 112] for j in live}
    need(len(xrows) == len(yrows) == 104, "104 first-X/first-Y rows")
    need(all(before[r] == after[r] for r in xrows | yrows), "all first-X and first-Y rows retained")
    need(
        all(
            set(packet["alpha"]) <= xrows
            and set(packet["beta"]) <= yrows
            for packet in packets
        ),
        "encoder/decoder supports are native X/Y rows",
    )
    expected_deltas = {p["B"]: {p["D"]: F(p["coefficient"])} for p in pairs}
    delta = {r: rep.plus(after[r], before[r], F(-1)) for r in range(400)}
    changed = {r: v for r, v in delta.items() if v}
    need(changed == expected_deltas, "only the eight promised B cross-D updates")

    # Independent all-suffix eight-tag transfer through the actual original
    # operation sequence, starting before the first B touch.
    first_touch = {}
    for i, op in enumerate(parent["program"]):
        for p in pairs:
            r = p["B"]
            if r not in first_touch and (op[1] == r or op[0] in ("ADD", "COPY") and op[2] == r):
                first_touch[r] = i
    need(all(first_touch[p["B"]] == p["first_old_B_use"] for p in pairs), "all recorded B first uses")
    tags = {i: {} for i in range(400)}
    tag_for = {p["B"]: 10000 + j for j, p in enumerate(pairs)}
    for row, tag in tag_for.items():
        tags[row] = {tag: F(1)}
    tag_events = 0
    for i, op in enumerate(parent["program"][530:], 530):
        kind, dst = op[:2]
        src = tags.get(op[2], {}) if kind in ("ADD", "COPY") else {}
        old_dst = tags.get(dst, {})
        if src or old_dst:
            tag_events += 1
        if kind == "INIT":
            tags[dst] = {}
        elif kind == "CLEAR":
            tags.pop(dst, None)
        elif kind == "MOVE":
            pass
        elif kind == "ADD":
            tags[dst] = rep.plus(tags.get(dst, {}), tags.get(op[2], {}), F(op[3]))
        elif kind == "COPY":
            need(not tags.get(dst, {}), f"tag COPY target not clear at parent event {i}")
            scale = F(op[3])
            tags[dst] = {k: scale * v for k, v in tags.get(op[2], {}).items() if scale * v}
        elif kind == "SCALE":
            scale = F(op[2])
            tags[dst] = {k: scale * v for k, v in tags.get(dst, {}).items() if scale * v}
    transfer = {r: v for r, v in tags.items() if v}
    expected_transfer = {p["B"]: {tag_for[p["B"]]: F(1)} for p in pairs}
    need(transfer == expected_transfer, "all eight suffix columns return to their own B outputs only")

    def residuals(rows: dict[int, dict[int, F]]) -> list[dict[int, F]]:
        return [rep.plus(rows[roles[b]], {roles[b]: F(1), roles[d]: F(-1)}, F(-1)) for b, d in host.values()]

    old_res, new_res = residuals(before), residuals(after)
    old_rank, new_rank = rep.rank(old_res), rep.rank(new_res)
    need((old_rank, new_rank) == (58, 54), "reverse residual rank 58->54")
    need(all(new_res[list(host).index(a)] == {k: c * v for k, v in new_res[list(host).index(b)].items()} for a, b, c in undirected), "four exact residual dependencies")
    zero_old = [h for h, r in zip(host, old_res) if not r]
    zero_new = [h for h, r in zip(host, new_res) if not r]
    need(zero_old == zero_new and len(zero_new) == 24, "all old completions retained")

    debt = 0
    for i in live:
        coeff = F(1) if i in host else F(1, 2)
        ideal = {roles[i]: coeff, roles[i + 112]: coeff}
        debt += len(rep.plus(after[roles[i + 112]], ideal, F(-1)))
    need(debt == 4920, "original-coordinate forward debt remains unchanged")

    old_raw = Counter((o[2], o[3], o[1]) for o in parent["program"] if o[0] == "MOVE" and not o[4])
    new_raw = Counter((o[2], o[3], o[1]) for o in word["program"] if o[0] == "MOVE" and not o[4])
    need(old_raw == new_raw, "all public/raw MOVE calls retained")
    need(
        new_bill["op_counts"]["ADD"] - old_bill["op_counts"]["ADD"] == 1056
        and new_bill["op_counts"]["MOVE"] - old_bill["op_counts"]["MOVE"] == 16
        and all(new_bill["op_counts"].get(k, 0) == old_bill["op_counts"].get(k, 0) for k in ("INIT", "CLEAR", "SCALE", "COPY")),
        "exact ordinary opcode delta, including no new scalar/COPY/owner operations",
    )
    move_delta = Counter(new_bill["move_ranks"])
    move_delta.subtract(old_bill["move_ranks"])
    move_delta = {k: v for k, v in move_delta.items() if v}
    need(move_delta == {1: 16, 7: 8, 9: -8}, "complete recursive MOVE-rank delta")
    need(new_bill["lifetimes"] == old_bill["lifetimes"] == 402 and new_bill["peak"] == old_bill["peak"] == 29, "all owners retire with no peak increase")

    result = {
        "status": "PASS_INDEPENDENT_FUNDED_CROSS_FOUR_REPLAY",
        "parent_sha256": sha(parent_blob),
        "word_sha256": sha(word_blob),
        "native_sha256": sha(source_blob),
        "input_directions": 400,
        "parent_instructions": old_bill["instructions"],
        "candidate_instructions": new_bill["instructions"],
        "candidate_op_counts": new_bill["op_counts"],
        "candidate_move_ranks": new_bill["move_ranks"],
        "lifetimes": new_bill["lifetimes"],
        "peak": new_bill["peak"],
        "move_rank_delta": move_delta,
        "only_changed_B_rows": {str(r): {str(k): str(v) for k, v in row.items()} for r, row in changed.items()},
        "suffix_tag_events": tag_events,
        "suffix_tag_transfer": {str(r): {str(k): str(v) for k, v in row.items()} for r, row in transfer.items()},
        "first_old_B_touches": {str(k): v for k, v in first_touch.items()},
        "replaced_parent_events": removed,
        "precode_terms": stop - start,
        "hoisted_D_moves": len(hoists),
        "reverse_rank": {"parent": old_rank, "candidate": new_rank},
        "completed_reverse_ports": zero_new,
        "original_coordinate_forward_debt": debt,
        "scope": "Exact partial source on all 400 directions; no completed endpoint or supplier inferred.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
