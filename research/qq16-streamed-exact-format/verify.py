#!/usr/bin/env python3
"""Exact numerical envelopes for the frozen PR4015 recovery word.

@CubeJerry, with substantial OpenAI Codex assistance.
Apache-2.0. Reference arithmetic, not supplier admission.
"""
import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import re
import stat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RETAINED_SHA256 = "1fb806b834d5d56cf094f433601a13aa81ded2338b5f0dd986f2e160b27b92f5"
SOURCES_SHA256 = "837f5d9dc0121369714bb18d4b6bd8db41bd1847e2f84daaf12be337906cf21a"
OLD_WORD = "research/qq16-line-normalized-decoder/WORD.json"
REGISTER = re.compile(r"([XYZWFG])(0|[1-9][0-9]*)\Z")


def need(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def read(path, limit=1_000_000):
    need(stat.S_ISREG(path.lstat().st_mode), "regular file required: " + str(path))
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    need(len(raw) <= limit, "input size limit")
    return raw


def authenticate():
    raw = read(HERE / "RETAINED.json")
    need(hashlib.sha256(raw).hexdigest() == RETAINED_SHA256, "retained manifest changed")
    retained = json.loads(raw)
    for row in retained["files"]:
        raw = read(HERE / row["path"])
        need(hashlib.sha256(raw).hexdigest() == row["sha256"], "retained source hash: " + row["path"])
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        need(blob == row["git_blob"], "retained Git blob: " + row["path"])
    source_bytes = read(HERE / "SOURCES.json")
    need(hashlib.sha256(source_bytes).hexdigest() == SOURCES_SHA256, "source manifest changed")
    pins = json.loads(source_bytes)
    for row in pins["files"]:
        if row["usage"] == "input":
            raw = read(ROOT / row["path"])
            need(hashlib.sha256(raw).hexdigest() == row["sha256"], "canonical source hash: " + row["path"])
    return {r["path"]: r["sha256"] for r in retained["files"]}


def valid_register(name):
    need(type(name) is str, "register string")
    match = REGISTER.fullmatch(name)
    need(match is not None, "register spelling")
    kind, number = match.groups()
    need(int(number) < (8 if kind in "FG" else 112), "register range")
    return kind


def validate_word(word):
    """Typed initialization/borrowed-return and owner-private lifetime checks."""
    need(type(word) is list and 0 < len(word) <= 4100, "bounded word")
    initialized = {f"{k}{p}" for k in "XY" for p in range(112)}
    private = None
    zero = set()
    counts = Counter()
    for event in word:
        need(type(event) is list and event and type(event[0]) is str, "event list")
        op = event[0]
        counts[op] += 1
        if op in ("begin", "end"):
            need(len(event) == 3 and type(event[1]) is str and type(event[2]) is int,
                 "private delimiter schema")
            need(event[2] in (8, 16), "private field capacity")
            if op == "begin":
                need(private is None, "nested private scope")
                private = (event[1], event[2])
                initialized -= {f"{k}{p}" for k in "FG" for p in range(8)}
                zero -= {f"{k}{p}" for k in "FG" for p in range(8)}
            else:
                need(private == (event[1], event[2]), "matching private scope")
                expected = {f"F{p}" for p in range(8)}
                if event[2] == 16:
                    expected |= {f"G{p}" for p in range(8)}
                need(expected <= zero, "private zero return")
                private = None
                initialized -= {f"{k}{p}" for k in "FG" for p in range(8)}
            continue
        if op == "checkpoint":
            need(event == ["checkpoint", "original_F0_outputs"] and private is None,
                 "checkpoint schema")
            continue
        need(op in ("clear", "add", "map", "line"), "unknown operation")
        need(len(event) == {"clear": 3, "add": 4, "map": 5, "line": 4}[op], "event arity")
        destination = event[1]
        kind = valid_register(destination)
        need(kind not in "XY", "borrowed input write")
        if kind in "FG":
            need(private is not None, "private use outside its owner sweep")
            need(kind == "F" or private[1] == 16, "private scope capacity")
        if op == "clear":
            need(type(event[2]) is str, "clear frame")
            initialized.add(destination)
            zero.add(destination)
            continue
        need(destination in initialized, "uninitialized destination")
        if op == "add":
            source = event[2]
            source_kind = valid_register(source)
            need(source != destination and source in initialized, "uninitialized/aliased source")
            if source_kind in "FG":
                need(private is not None, "private read outside scope")
            need(type(event[3]) is str and event[3] in ("1", "-1", "1/4", "-1/4"),
                 "scalar alphabet")
            if source not in zero:
                zero.discard(destination)
        else:
            need(private is None, "native/map cannot carry owner-private state")
            if op == "line":
                need(type(event[2]) is int and 0 <= event[2] < 112, "native port")
                need(type(event[3]) is int and event[3] in (-1, 1), "native sign")
            else:
                need(type(event[2]) is int and event[2] in (1, 2), "map stage")
                need(type(event[3]) is int and 0 <= event[3] < 112 and type(event[4]) is bool,
                     "map port/direction")
    need(private is None, "unterminated private scope")
    need({f"{k}{p}" for k in "ZW" for p in range(112)} <= initialized, "all owned outputs defined")
    return counts


def frontier(pairs):
    """Max-affine denominator envelope: (intercept, t-slope)."""
    pairs = set(pairs)
    return tuple(sorted(p for p in pairs if not any(
        p != q and q[0] >= p[0] and q[1] >= p[1] for q in pairs)))


@dataclass(frozen=True)
class Bound:
    # Magnitude / (2**P * h) <= polynomial(2**(ceil(lambda/2)-1)).
    poly: tuple
    grids: tuple

    def scaled(self, coefficient):
        if not self.poly:
            return self
        coefficient = abs(Q(coefficient))
        need(coefficient in (Q(1), Q(1, 4)), "bound coefficient")
        extra = 2 if coefficient == Q(1, 4) else 0
        return Bound(tuple(x * coefficient for x in self.poly),
                     tuple((c + extra, a) for c, a in self.grids))

    def plus(self, other):
        if not self.poly:
            return other
        if not other.poly:
            return self
        n = max(len(self.poly), len(other.poly))
        p = tuple((self.poly[i] if i < len(self.poly) else 0) +
                  (other.poly[i] if i < len(other.poly) else 0) for i in range(n))
        return Bound(p, frontier(self.grids + other.grids))

    def tensor(self, numerator=False):
        if not self.poly:
            return self
        # All native interiors are <= 4 times the complete tensor row bound.
        # The exact tensor coefficient lemma gives factor 2**ceil(lambda/2).
        m = 8 if numerator else 2
        p = (Q(0),) + tuple(m * x for x in self.poly)
        # At even depth the penultimate factor already uses the final grid.
        g = tuple((c + 1, a + 1) for c, a in self.grids)
        return Bound(p, g)

    def wire(self):
        return {"poly": [str(x) for x in self.poly], "grid": [list(x) for x in self.grids]}

    def at(self, depth):
        t = (depth + 1) // 2 - 1
        return (sum(x * 2 ** (a * t) for a, x in enumerate(self.poly)),
                max((c + a * t for c, a in self.grids), default=0))


ZERO = Bound((), ())
ENTRY = Bound((Q(1),), ((0, 0),))


def analyze(word):
    counts = validate_word(word)
    state = {f"{k}{p}": ENTRY for k in "XY" for p in range(112)}
    trace = []
    peak_at_one, peak_degree, peak_event = Q(1), 0, None
    global_grid = ((0, 0),)
    grid_events = []
    for index, event in enumerate(word):
        op = event[0]
        if op in ("begin", "end", "checkpoint"):
            continue
        d = event[1]
        if op == "clear":
            value = ZERO
        elif op == "add":
            value = state[d].plus(state[event[2]].scaled(event[3]))
        elif op == "line":
            interior = state[d].tensor(numerator=True)
            trace.append([index, "cross_numerator", interior.wire()])
            value = state[d].tensor()
        else:
            value = state[d]
        state[d] = value
        trace.append([index, "completed", value.wire()])
        observations = [("completed", value)]
        if op == "line":
            observations.append(("cross_numerator", interior))
        for where, observation in observations:
            at_one = sum(observation.poly)
            if at_one > peak_at_one:
                peak_at_one = at_one
                peak_event = [index, where, event, observation.wire()]
            peak_degree = max(peak_degree, len(observation.poly) - 1)
            new_grid = frontier(global_grid + observation.grids)
            if new_grid != global_grid:
                grid_events.append([index, where, [list(x) for x in new_grid]])
            global_grid = new_grid
    need(len(global_grid) == 1, "one global affine grid required")
    intercept, slope = global_grid[0]
    range_bits = 0
    while peak_at_one >= 2 ** range_bits:
        range_bits += 1
    quarter = sum(e[0] == "add" and abs(Q(e[3])) == Q(1, 4) for e in word)
    unit = counts["add"] - quarter
    summary = {
        "events": len(word), "operation_counts": dict(sorted(counts.items())),
        "unit_adds": unit, "quarter_adds": quarter,
        "native_wrappers": 2 * counts["line"],
        "inherited_scalar_allowance": 8 * unit + 12 * quarter + 2 * counts["clear"],
        "observations": len(trace), "trace_sha256": sha(trace),
        "max_component_multiplier_at_depth_one": str(peak_at_one),
        "max_magnitude_polynomial_degree": peak_degree,
        "peak_witness": peak_event, "global_grid": [intercept, slope],
        "grid_frontier_changes": grid_events,
        "range_bits": [range_bits, peak_degree],
        "signed_width_above_P": [intercept + range_bits + 1, slope + peak_degree],
        "final_outputs": {f"{k}{p}": state[f"{k}{p}"].wire() for k in "ZW" for p in range(112)},
        "borrowed_inputs_unchanged": all(state[f"{k}{p}"] == ENTRY for k in "XY" for p in range(112)),
        "private_fields_zero": all(v == ZERO for k, v in state.items() if k[0] in "FG"),
    }
    need(summary["borrowed_inputs_unchanged"] and summary["private_fields_zero"], "endpoint ownership")
    return summary, trace


def typed(value):
    if type(value) is dict:
        return ("dict", tuple((k, typed(v)) for k, v in sorted(value.items())))
    if type(value) is list:
        return ("list", tuple(map(typed, value)))
    return (type(value).__name__, value)


def build(with_trace=False):
    source_hashes = authenticate()
    word = json.loads(read(HERE / "retained/PR4015-WORD.json"))
    old = json.loads(read(ROOT / OLD_WORD))
    current, current_trace = analyze(word)
    predecessor, old_trace = analyze(old)
    need(current["events"] == 3813 and current["operation_counts"]["line"] == 224, "PR4015 source identity")
    need(predecessor["events"] == 3823 and predecessor["operation_counts"]["line"] == 336, "PR2707 source identity")
    result = {"schema_version": 1, "status": "SCOPED_EXACT_NUMERICAL_FORMAT_NO_NEW_KAPPA",
            "source_hashes": source_hashes, "streamed": current, "original": predecessor,
            "input_contract": "Every borrowed real/imaginary component is in h Z and has absolute value < 2^P h, P>=0; owned dirt is cleared before use.",
            "depth_parameter": "t=ceil(lambda/2)-1>=0, lambda positive integer",
            "native_contract": "Each signed rank-one native line is its exact Gaussian pair kernel on each of lambda tensor layers, with exact component-permutation wrappers; covers are exact full-owner permutations.",
            "limits": "Numerical reference only. No native semantic reproof, physical memory/bit-tape tariff, actual caller admission, minimum precision, or multiplication theorem."}
    return (result, {"streamed": current_trace, "original": old_trace}) if with_trace else result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="create an absent RESULT.json")
    args = parser.parse_args()
    result, trace = build(with_trace=True)
    path = HERE / "RESULT.json"
    if args.write:
        need(not path.exists() and not (HERE / "TRACE.json").exists(), "generation refuses overwrite")
        with (HERE / "TRACE.json").open("xb") as stream:
            stream.write(canonical(trace) + b"\n")
        with path.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, indent=2)
            stream.write("\n")
    else:
        need(typed(result) == typed(json.loads(read(path))), "complete typed result differs")
        need(typed(trace) == typed(json.loads(read(HERE / "TRACE.json", 2_000_000))),
             "complete typed cut trace differs")
    row = result["streamed"]
    print("PASS_QQ16_STREAMED_EXACT_FORMAT", "events=" + str(row["events"]),
          "grid=" + str(row["global_grid"]), "width_above_P=" + str(row["signed_width_above_P"]),
          "native_calls=224 no_new_kappa")


if __name__ == "__main__":
    main()
