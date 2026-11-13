#!/usr/bin/env python3
"""Direct polynomial replay of a supplied separator; no row elimination.

Prepared for CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import importlib.util
import json
import sys

PIN = "acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9"
CPIN = "2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962"
CUT, INJECT = 40710, 35426
ZERO, ONE = (Q(0), Q(0)), (Q(1), Q(0))


def need(ok, why):
    if not ok:
        raise ValueError(why)


def plus(a, b, q=Q(1)):
    return a[0]+q*b[0], a[1]+q*b[1]


def span(basis):
    result = {0}
    for v in basis:
        need(v not in result and 0 < v < 512, "independent actual frame basis")
        result |= {v ^ t for t in tuple(result)}
    return frozenset(result)


def verify(source, certificate, compiler):
    raw = Path(source).read_bytes()
    need(sha256(raw).hexdigest() == PIN, "exact source pin")
    need(sha256(Path(compiler).read_bytes()).hexdigest() == CPIN, "actual frame constructor pin")
    w = json.loads(gzip.decompress(raw))
    author_raw = Path(certificate).read_bytes()
    x = {int(h): Q(v) for h, v in json.loads(author_raw)["dual_functional"].items()}
    need(len(x) == 52 and all(0 <= h < w["public"] for h in x), "52-coordinate separator input")
    spec = importlib.util.spec_from_file_location("review_carrier943_clifford", compiler)
    c = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = c
    spec.loader.exec_module(c)
    need(w["program"][CUT] == ["MOVE", 885, 3, 189, False], "literal target cut")
    need(w["program"][INJECT] == ["MOVE", 943, 3, 105, False], "literal latest injection cut")
    need(all(e[1] != 1459 and not (e[0] in ("ADD", "COPY") and e[2] == 1459)
             for e in w["program"][:CUT]), "demoted1459 has no original prefix contact")
    observed_ids = set(w["initial"]) | {e[3] for e in w["program"][:CUT] if e[0] == "MOVE"}
    # Enumerate ACTUAL frame IDs, not a preselected list of representatives.
    ops = {f: c.canonical_frame(9, w["frames"][f]) for f in sorted(observed_ids | {189})}
    spaces = {f: span(w["frames"][f]) for f in ops}
    rank_by_id, geometry = {}, []
    for f in sorted(observed_ids):
        op = ops[f].adjoint().then(ops[189])
        r = c.rank([a for a, b, phase in op.tab[9:]])
        expected = len(w["frames"][f])+8-2*((len(spaces[f] & spaces[189])).bit_length()-1)
        need(r == expected, "actual interface B-rank/geometric distance")
        rank_by_id[f] = r
        geometry.append({"frame": f, "rank_to_189": r, "dimension": len(w["frames"][f]),
                         "span": sorted(spaces[f])})
    cheap = {f for f, r in rank_by_id.items() if r <= 3}
    positive = {f for f in cheap if rank_by_id[f] > 0}
    positive_classes = {spaces[f] for f in positive}
    need(len(positive_classes) == 67, "complete67 positive cheap history classes")
    need(189 in cheap and rank_by_id[3] == 8, "destination and excluded source distance")

    def replay(dual, free_1459=False):
        n = w["public"]
        value = [(Q(h in (885, 1459)), -dual.get(h, Q(0))) for h in range(n)]
        value += [ZERO]*w["owned_fields"]
        cur = list(w["initial"]) + [None]*w["owned_fields"]
        promise = plus(plus(value[885], value[705], -1), value[1459], -1)
        need(promise == ZERO, "promised input polynomial")
        observations, current_checks = [], 0

        def observe(event, owner, frame):
            if frame in cheap and not (event == -1 and owner == 1459 and not free_1459):
                need(value[owner] == ZERO, "nonzero cheap history at " + str((event, owner, frame)))
                observations.append({"event": event, "owner": owner, "frame": frame})

        for owner, f in enumerate(w["initial"]):
            observe(-1, owner, f)
        for event, e in enumerate(w["program"][:CUT]):
            if event == INJECT:
                need(value[885] == ONE, "injected current885 is constant1; no quadratic alpha term")
                need(cur[885] == cur[943] == 3, "legal empty-frame injection")
                value[943] = plus(value[943], (Q(0), value[885][0]))
            op, a = e[:2]
            if op == "MOVE":
                need(cur[a] == e[2] and bool(e[4]) == (a >= n), "MOVE source/ownership")
                cur[a] = e[3]
                observe(event, a, e[3])
            elif op == "INIT":
                need(a >= n and cur[a] is None, "fresh owned INIT")
                cur[a], value[a] = e[2], ZERO
            elif op == "CLEAR":
                need(a >= n and cur[a] == e[2], "owned CLEAR; no zero-before-CLEAR premise")
                cur[a], value[a] = None, ZERO
            elif op == "SCALE":
                need(cur[a] == e[-1], "SCALE physical frame")
                q = Q(e[2])
                value[a] = value[a][0]*q, value[a][1]*q
            else:
                need(op in ("ADD", "COPY"), "known native scalar opcode")
                b, q = e[2], Q(e[3])
                need(a != b and cur[a] == cur[b] == e[-1], "same-frame scalar contact")
                if op == "COPY":
                    need(a >= n and value[a] == ZERO, "COPY fresh owned zero")
                    value[a] = ZERO
                value[a] = plus(value[a], value[b], q)
            if cur[a] in cheap:
                need(value[a] == ZERO, "cheap current value after " + str(event))
                current_checks += 1
        need(cur[885] == 3 and value[885] == ONE, "nonzero constant target at actual cut")
        need(len(observations) == 294, "all294 cheap observations directly checked")
        need(len({(o["event"], o["owner"], o["frame"]) for o in observations}) == 294,
             "no observation duplicate or representative omission")
        return {"observations": observations, "current_cheap_values_checked": current_checks,
                "target_polynomial": ["1", "0"], "input_promise_polynomial": ["0", "0"]}

    result = replay(x)
    controls = []
    wrong = x.copy()
    wrong[1196] += 1
    for name, dual, free in (("wrong_dual1196_coefficient", wrong, False),
                             ("unavailable_initial1459_supplied_free", x, True)):
        try:
            replay(dual, free)
        except ValueError as error:
            controls.append({"control": name, "rejected": True, "reason": str(error)})
        else:
            raise ValueError("failure control accepted: " + name)
    return {"status": "PASS_INDEPENDENT_POLYNOMIAL_ALL_ALPHA_HISTORY_SEPARATOR",
            "source_sha256": PIN, "compiler_sha256": CPIN,
            "author_certificate_sha256": sha256(author_raw).hexdigest(),
            "elimination_or_author_row_engine_used": False,
            "source_events_replayed": CUT,
            "demoted1459_no_prefix_contact_verified": True,
            "actual_observed_frame_ID_count": len(observed_ids),
            "actual_cheap_frame_IDs": sorted(cheap),
            "positive_cheap_actual_frame_IDs": sorted(positive),
            "positive_cheap_span_classes": len(positive_classes),
            "positive_cheap_rank_histogram": dict(Counter(rank_by_id[f] for f in positive)),
            "geometry": geometry, "direct_replay": result, "controls": controls,
            "limits": "Latest single943 injection only, demoted1459 original entrance unavailable, otherwise fixed original prefix. No original paid-payload augmentation or uncharged cross-frame ordinary algorithm. No supplier or kappa claim."}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("certificate", type=Path)
    p.add_argument("compiler", type=Path)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    result = verify(a.source, a.certificate, a.compiler)
    a.out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "cheap_classes": result["positive_cheap_span_classes"],
                      "observations": len(result["direct_replay"]["observations"]),
                      "controls": len(result["controls"])}))
