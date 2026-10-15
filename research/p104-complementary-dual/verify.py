#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact finite P104 companion replay, including dirty state and native phases.

Default replay is read-only and does not need Git, network, or a solver.
Prepared for @CubeJerry with substantial OpenAI Codex assistance.
"""
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from functools import lru_cache
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("p104_dual_verify_sources", HERE / "sources.py")
S = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(S)
require = S.require
PROFILE = {1: 2429, 2: 557, 3: 389, 4: 112, 5: 108, 6: 16, 7: 13, 9: 1}
PRIVATE_PROFILE = {1: 2, 2: 1, 3: 1, 7: 7}
SELECTED_KAPPA = Q(836330098538459, 500000000000000000)


class EndpointError(ValueError):
    def __init__(self, registers):
        self.registers = registers
        super().__init__("endpoint: " + ",".join(map(str, registers)))


@lru_cache(None)
def frame(basis):
    require(all(type(x) is int and 0 < x < 512 for x in basis), "frame vector")
    values = {0}
    for x in basis:
        require(x not in values, "dependent frame basis")
        values |= {x ^ y for y in tuple(values)}
    return frozenset(values)


@lru_cache(None)
def perpendicular(basis):
    # Exhaust all 512 labels; the generator instead computes a binary nullspace.
    return frozenset(x for x in range(512)
                     if all((x & y).bit_count() % 2 == 0 for y in basis))


def dim(subspace):
    return len(subspace).bit_length() - 1


def profile(counter):
    return {str(rank): count for rank, count in sorted(counter.items()) if count}


def add(destination, source, coefficient):
    for column, value in source.items():
        value = destination.get(column, Q(0)) + coefficient * value
        if value:
            destination[column] = value
        else:
            destination.pop(column, None)


def replay(word):
    require(set(word) == {"schema", "orientation", "public_registers", "port_pairs",
                          "initial", "final", "events"}, "word schema fields")
    require(word["schema"] == "p104-framed-word-v1" and word["public_registers"] == 735,
            "word schema or public register count")
    backward = word["orientation"] == "backward"
    require(backward or word["orientation"] == "forward", "orientation")
    n = word["public_registers"]
    pairs = word["port_pairs"]
    require(len(pairs) == 104 and all(len(p) == 3 for p in pairs), "104 port pairs")
    public_ports = [r for x, y, _ in pairs for r in (x, y)]
    require(len(set(public_ports)) == 208
            and all(type(r) is int and 0 <= r < n for r in public_ports), "distinct data registers")
    require(len({p for _, _, p in pairs}) == 104, "distinct physical labels")
    require(len(word["initial"]) == len(word["final"]) == n, "public frame inventory")
    initial = [frame(tuple(f)) for f in word["initial"]]
    final = [frame(tuple(f)) for f in word["final"]]
    for x, y, port in pairs:
        require(type(port) is int and 0 < port < 512 and port.bit_count() % 2 == 1,
                "odd physical port")
        src, dst = (y, x) if backward else (x, y)
        require(initial[src] == frozenset((0, port)) and final[src] == frozenset(range(512))
                and initial[dst] == frozenset((0,)) and final[dst] == perpendicular((port,)),
                "intrinsic data boundary")
    require(all(a <= b for a, b in zip(initial, final)), "public boundary inclusion")
    rows = {i: {i: Q(1)} for i in range(n)}
    current = dict(enumerate(initial))
    counts, paid, private_paid = Counter(), Counter(), Counter()
    live_private, peak, paths, active_path = set(), 0, [], None
    for index, event in enumerate(word["events"]):
        require(isinstance(event, list) and event, "event schema")
        kind, r = event[:2]
        require(type(r) is int and 0 <= r < n + 8, "register namespace")
        counts[kind] += 1
        if kind == "zero":
            require(len(event) == 3 and r >= n and r not in rows and not live_private,
                    "private zero lifetime")
            current[r], rows[r] = frame(tuple(event[2])), {}
            require(dim(current[r]) == 8, "private entry dimension")
            live_private.add(r)
            peak = max(peak, len(live_private))
            active_path = []
        elif kind == "drop":
            require(len(event) == 3 and r in live_private and current[r] == frame(tuple(event[2])),
                    "private drop lifetime")
            require(dim(current[r]) == 1 and active_path, "private exit dimension")
            paths.append(active_path)
            active_path = None
            live_private.remove(r)
            del current[r], rows[r]
        elif kind == "transport":
            require(len(event) == 6 and r in rows, "transport live register")
            old, new = frame(tuple(event[2])), frame(tuple(event[3]))
            private = r >= n
            require(type(event[5]) is bool and event[5] == private, "transport private classification")
            require(current[r] == old, "transport entry frame")
            require(new < old if private else old < new, "transport direction")
            rank = abs(dim(new) - dim(old))
            require(type(event[4]) is int and event[4] == rank, "transport rank charge")
            current[r] = new
            paid[rank] += 1
            if private:
                require(r in live_private and active_path is not None, "private transport lifetime")
                private_paid[rank] += 1
                active_path.append(rank)
        elif kind == "scale":
            require(len(event) == 4 and r in rows, "scale live register")
            require(current[r] == frame(tuple(event[3])), "scalar frame")
            coefficient = Q(event[2])
            require(bool(coefficient), "zero scalar scale")
            rows[r] = {i: coefficient * x for i, x in rows[r].items()}
        else:
            require(kind in ("add", "copy") and len(event) == 5, "scalar operation kind")
            src = event[2]
            require(type(src) is int and r != src and r in rows and src in rows, "scalar live operands")
            require(current[r] == current[src] == frame(tuple(event[4])), "scalar frame")
            coefficient = Q(event[3])
            require(bool(coefficient), "zero scalar addition")
            if kind == "copy":
                require(not backward and r in live_private and not rows[r], "copy zero destination")
            add(rows[r], rows[src], coefficient)
    require(not live_private and active_path is None and set(rows) == set(range(n)),
            "unclosed private lifetime")
    require([current[r] for r in range(n)] == final, "public final frame")
    expected = {r: {r: Q(1)} for r in range(n)}
    for x, y, _ in pairs:
        expected[x if backward else y][y if backward else x] = Q(-1 if backward else 1)
    failures = [r for r in range(n) if rows[r] != expected[r]]
    if failures:
        raise EndpointError(failures)
    require(dict(paid) == PROFILE and dict(private_paid) == PRIVATE_PROFILE, "complete paid profile")
    wanted = dict(add=20955 if backward else 20947, transport=3625, scale=715, zero=8, drop=8)
    if not backward:
        wanted["copy"] = 8
    require(dict(counts) == wanted and peak == 1 and len(paths) == 8, "complete operation inventory")
    widths = [dim(b) - dim(a) for a, b in zip(initial, final)]
    require(sum(widths) == 5838 and sum(r * c for r, c in private_paid.items()) == 56,
            "public/private rank mass")
    endpoint = [[[i, str(v)] for i, v in sorted(rows[r].items())] for r in range(n)]
    return dict(public_columns=n, dirty_helpers=n-208, orientation=word["orientation"],
                endpoint_sha256=S.sha(S.canonical(endpoint)),
                paid_profile=profile(paid), public_rank_mass=sum(widths), private_rank_mass=56,
                total_rank_mass=5894, counts=dict(sorted(counts.items())), private_paths=paths,
                peak_private_registers=peak, public_widths_sha256=S.sha(S.canonical(widths)))


def correspondence(original, backward):
    require(original["port_pairs"] == backward["port_pairs"], "port correspondence")
    require(len(original["events"]) == len(backward["events"]), "event correspondence count")
    for a, b in zip(original["initial"], backward["final"]):
        require(frame(tuple(b)) == perpendicular(tuple(a)), "complementary final boundary")
    for a, b in zip(original["final"], backward["initial"]):
        require(frame(tuple(b)) == perpendicular(tuple(a)), "complementary initial boundary")
    signed = {x for x, _, _ in original["port_pairs"]}
    for a, b in zip(reversed(original["events"]), backward["events"]):
        kind = a[0]
        if kind == "transport":
            require(b[:2] == a[:2] and b[4:] == a[4:]
                    and frame(tuple(b[2])) == perpendicular(tuple(a[3]))
                    and frame(tuple(b[3])) == perpendicular(tuple(a[2])), "dual transport correspondence")
        elif kind in ("zero", "drop"):
            require(b[:2] == ["drop" if kind == "zero" else "zero", a[1]]
                    and frame(tuple(b[2])) == perpendicular(tuple(a[2])), "dual private correspondence")
        elif kind == "scale":
            require(b[:2] == a[:2] and Q(b[2]) == Q(a[2])
                    and frame(tuple(b[3])) == perpendicular(tuple(a[3])), "dual scale correspondence")
        else:
            sign = -1 if (a[1] in signed) != (a[2] in signed) else 1
            require(b[:3] == ["add", a[2], a[1]] and Q(b[3]) == sign * Q(a[3])
                    and frame(tuple(b[4])) == perpendicular(tuple(a[4])), "dual addition correspondence")
    return len(backward["events"])


def reject(word, edit, reason, helper_only=False):
    bad = deepcopy(word)
    edit(bad)
    try:
        replay(bad)
    except ValueError as error:
        require(reason in str(error), "unexpected negative-control rejection: " + str(error))
        if helper_only:
            ports = {r for x, y, _ in word["port_pairs"] for r in (x, y)}
            require(isinstance(error, EndpointError) and set(error.registers).isdisjoint(ports),
                    "dirty-helper control also corrupts a data endpoint")
        return "rejected: " + reason
    raise ValueError("negative control accepted: " + reason)


def controls(backward):
    events = backward["events"]
    n = backward["public_registers"]
    accumulating = next(i for i, e in enumerate(events) if e[0] == "add" and e[1] >= n)
    scattering = next(i for i, e in enumerate(events) if e[0] == "add" and e[2] >= n)
    private_scale = next(i for i, e in enumerate(events) if e[0] == "scale" and e[1] >= n
                         and abs(Q(e[2])) != 1)
    helper_cleanup = max(i for i, e in enumerate(events) if e[0] == "add" and 224 <= e[1] < n)
    transport = next(i for i, e in enumerate(events) if e[0] == "transport")
    unused = next(i for i, e in enumerate(events) if e[0] == "transport" and e[1] == 711)
    zero = next(i for i, e in enumerate(events) if e[0] == "zero")
    result = {}
    result["missing_private_accumulation"] = reject(backward, lambda w: w["events"].pop(accumulating), "endpoint")
    result["wrong_private_scatter_sign"] = reject(
        backward, lambda w: w["events"][scattering].__setitem__(3, str(-Q(events[scattering][3]))), "endpoint")
    result["inverse_instead_of_transposed_scale"] = reject(
        backward, lambda w: w["events"][private_scale].__setitem__(2, str(1/Q(events[private_scale][2]))), "endpoint")
    result["dirty_helper_cleanup_omitted"] = reject(
        backward, lambda w: w["events"].pop(helper_cleanup), "endpoint", helper_only=True)
    result["wrong_common_chart"] = reject(
        backward, lambda w: w["events"][accumulating].__setitem__(4, []), "scalar frame")
    result["undercharged_transport"] = reject(
        backward, lambda w: w["events"][transport].__setitem__(4, events[transport][4]-1), "transport rank charge")
    result["unpaid_unused_helper_boundary"] = reject(
        backward, lambda w: w["events"].pop(unused), "public final frame")
    result["missing_private_zero"] = reject(
        backward, lambda w: w["events"].pop(zero), "scalar live operands")
    result["public_reset_as_private_zero"] = reject(
        backward, lambda w: w["events"][zero].__setitem__(1, 711), "private zero lifetime")
    def remove_gauge(word):
        signed = {x for x, _, _ in word["port_pairs"]}
        for e in word["events"]:
            if e[0] == "add" and (e[1] in signed) != (e[2] in signed):
                e[3] = str(-Q(e[3]))
    result["positive_transpose_instead_of_inverse_transpose"] = reject(backward, remove_gauge, "endpoint")
    return result


def native_witness(word):
    edges, paths, path = [], [], None
    for event in word["events"]:
        if event[0] == "zero":
            path = []
        elif event[0] == "drop":
            paths.append(path)
            path = None
        elif event[0] == "transport":
            edge = dict(register=str(event[1]), old=event[2], new=event[3], rank=event[4],
                        private=event[5], occurrence=len(edges))
            edges.append(edge)
            if event[5]:
                path.append(edge)
    return dict(transports=edges, private_paths=paths, ports=[p for _, _, p in word["port_pairs"]])


def pricing():
    engine = S.module("ceiling", S.ROOT / "research/complex-local-word-ceiling/ceiling.py")
    a = SELECTED_KAPPA / (1-SELECTED_KAPPA)
    lower, upper = engine.relax(PROFILE, 73, 832, 9, 56, a)
    require(upper < 1, "hypothetical fractional-idle budget fails selected threshold")
    alo, ahi = engine.ceiling(PROFILE, 73, 832, 9, 56)
    return dict(model="Hypothetical inherited m73, 832/9 families per call, COPY56, fractional rank51 idle",
                local_mass=5894, idle_mass=818, selected_kappa=str(SELECTED_KAPPA),
                selected_threshold_moment=[str(lower), str(upper)],
                primitive_ceiling_bracket=[str(alo), str(ahi)],
                kappa_upper_cap=str(ahi/(1+ahi)),
                actual_backward_hosting_verified=False,
                scope="A favorable necessary relaxation only. Equal widths do not prove owner windows or global admission.")


def verify(scalar_only=False):
    S.live_inputs()
    original, backward = S.word("FORWARD.json.gz"), S.word("BACKWARD.json.gz")
    forward_result, backward_result = replay(original), replay(backward)
    count = correspondence(original, backward)
    require(forward_result["public_widths_sha256"] == backward_result["public_widths_sha256"],
            "public width vector changed")
    generator = S.module("builder", HERE / "build.py")
    with S.predecessor() as root:
        regenerated = generator.forward(root)
        require(regenerated == original and generator.dual(regenerated) == backward,
                "regenerated complete word differs")
        normalized = deepcopy(original)
        for event in normalized["events"]:
            if event[0] == "copy":
                event[0] = "add"
        require(generator.dual(backward) == normalized, "double-dual positive control")
        print("PASS both 735-column endpoints, 25,311 event correspondences and complete regeneration", flush=True)
        negative = controls(backward)
        budget = pricing()
        print("PASS ten semantic/accounting controls and exact conditional budget", flush=True)
        if scalar_only:
            return dict(status="PASS_SCALAR_ONLY_NATIVE_NOT_RUN", forward=forward_result,
                        backward=backward_result, controls=negative, pricing=budget)
        checker = S.module("native_checker", root / "research/p104-interleaved-search/native_checks.py")
        native = checker.verify(native_witness(backward))
        require(native["paid_profile"] == profile(PROFILE) and native["native_rank_mass"] == 5894
                and native["literal_transport_occurrences"] == 3625
                and native["distinct_transport_recipes"] == 2942
                and native["private_path_gaussian_columns"] == 4096
                and native["intrinsic_monomial_endpoint_adapters"] == 208
                and native["wrong_global_phase_control_rejected"], "native replay coverage")
        # The unchanged generic native checker's original prose says "forward".
        # Its input here is explicitly bound to BACKWARD, with separately checked endpoints.
        native["scope"] = "Native operators of BACKWARD.json.gz, including exact phases; public caller wrappers are outside scope."
        print("PASS 2,942 native recipes, 208 endpoint adapters, 4,096 private-path columns and phase control", flush=True)
    return dict(status="PASS_P104_COMPLEMENTARY_DUAL", forward=forward_result,
                backward=backward_result, event_correspondences=count,
                complete_source_regeneration=True, double_dual_control=True,
                native=native, negative_controls=negative, pricing=budget,
                scope="Finite complementary-frame inverse-transpose companion; no global supplier or new kappa.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scalar-only", action="store_true", help="Development check; explicitly omits native verification")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write-result", action="store_true", help="Explicitly replace the checked receipt")
    group.add_argument("--out", type=Path, help="Write a receipt to a new file only")
    args = parser.parse_args()
    require(not (args.scalar_only and args.write_result), "partial replay cannot replace full receipt")
    if args.out:
        require(not args.out.exists(), "output already exists")
    result = verify(args.scalar_only)
    if args.write_result:
        (HERE / "RESULT.json").write_bytes(S.canonical(result))
    elif not args.scalar_only:
        require(result == json.loads((HERE / "RESULT.json").read_bytes()), "recorded receipt differs")
    if args.out:
        with args.out.open("xb") as handle:
            handle.write(S.canonical(result))
    print(result["status"], "receipt=" + S.sha(S.canonical(result)))


if __name__ == "__main__":
    main()
