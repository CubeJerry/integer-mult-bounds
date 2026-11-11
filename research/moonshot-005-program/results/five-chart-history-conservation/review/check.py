#!/usr/bin/env python3
"""Independent all-input native replay and global terminal/history intersection.

No programme scientific code is imported. Exact rational sparse elimination.
Prepared for CubeJerry with OpenAI assistance, Apache-2.0.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path

Q = Fraction
PIN = "2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def axpy(out, source, scale=Q(1)):
    for key, value in source.items():
        next_value = out.get(key, Q(0)) + scale * value
        if next_value:
            out[key] = next_value
        else:
            out.pop(key, None)
    return out

def canonical_span(frame):
    values = {0}
    for vector in frame:
        values |= {vector ^ item for item in values}
    return tuple(sorted(values))

class Echelon:
    def __init__(self, rows=()):
        self.rows = {}
        for row in rows:
            self.insert(row)

    def residual(self, row):
        out = dict(row)
        for pivot in sorted(self.rows):
            if pivot in out:
                axpy(out, self.rows[pivot], -out[pivot])
        return out

    def insert(self, row):
        out = self.residual(row)
        if not out:
            return False
        pivot = min(out)
        leading = out[pivot]
        self.rows[pivot] = {key: value / leading for key, value in out.items()}
        return True

    def rank(self):
        return len(self.rows)

def intersect(left, right):
    """Kernel of quotient restriction; carry the original row in parallel."""
    independent_left = Echelon(left)
    images = {}
    output = []
    for original in independent_left.rows.values():
        image, lift = right.residual(original), dict(original)
        for pivot in sorted(images):
            if pivot in image:
                scale = -image[pivot]
                axpy(image, images[pivot][0], scale)
                axpy(lift, images[pivot][1], scale)
        if image:
            pivot = min(image)
            lead = image[pivot]
            images[pivot] = (
                {key: val / lead for key, val in image.items()},
                {key: val / lead for key, val in lift.items()},
            )
        else:
            require(lift, "independent source rows cannot have zero lift")
            require(not right.residual(lift), "intersection row not in right space")
            output.append(lift)
    require(len(output) + len(images) == independent_left.rank(), "rank nullity")
    require(Echelon(output).rank() == len(output), "intersection basis dependence")
    return output

def encode(row):
    return [[key, str(value)] for key, value in sorted(row.items())]

def run(source, output, donor=77, receiver=189, terminal=127):
    data = source.read_bytes()
    require(hashlib.sha256(data).hexdigest() == PIN, "source pin")
    word = json.loads(gzip.decompress(data))
    program = word["program"]
    frames = list(map(canonical_span, word["frames"]))
    n = word["public"]
    endpoint = frames[terminal]
    itinerary = {frames[word["initial"][receiver]]}
    itinerary.update(frames[event[3]] for event in program
                     if event[0] == "MOVE" and event[1] == receiver)
    values = {j: {j: Q(1)} for j in range(n)}
    locations = {j: frames[frame] for j, frame in enumerate(word["initial"])}
    initial_roles = [j for j in range(n) if locations[j] in itinerary]
    observations = [dict(values[j]) for j in initial_roles]
    keys = [[-1, j] for j in initial_roles]
    for index, event in enumerate(program):
        op, target = event[:2]
        if op == "INIT":
            require(target not in values, "double INIT")
            values[target] = {}
            locations[target] = frames[event[2]]
        elif op == "CLEAR":
            require(target >= n and target in values, "public/missing CLEAR")
            del values[target]
            del locations[target]
        elif op == "MOVE":
            require(locations[target] == frames[event[2]], "MOVE origin")
            locations[target] = frames[event[3]]
            if locations[target] in itinerary:
                observations.append(dict(values[target]))
                keys.append([index, target])
        elif op in ("ADD", "COPY"):
            other, scale = event[2], Q(event[3])
            require(locations[target] == locations[other], "noncochart scalar")
            if op == "COPY":
                require(not values[target], "nonzero COPY target")
                values[target] = {}
            axpy(values[target], values[other], scale)
        elif op == "SCALE":
            values[target] = {key: value * Q(event[2]) for key, value in values[target].items()}
        else:
            raise ValueError(op)
    require(set(values) == set(range(n)), "unretired owned field")
    require(all(locations[j] == frames[word["final"][j]] for j in range(n)), "final charts")
    final_roles = [j for j in range(n) if locations[j] == endpoint]
    stable_roles = [j for j in range(n) if locations[j] in itinerary and locations[j] != endpoint]
    stable_rows = [{j: Q(1)} for j in initial_roles] + [values[j] for j in stable_roles]
    stable = Echelon(stable_rows)
    history = Echelon(observations)
    terminal_space = Echelon(values[j] for j in final_roles)
    common = intersect(history.rows.values(), terminal_space)
    surviving = Echelon(stable.residual(row) for row in common)
    quotient = Echelon(stable.residual(row) for row in history.rows.values())
    growing_stable = Echelon(stable_rows)
    timed = []
    for key, row in zip(keys[len(initial_roles):], observations[len(initial_roles):]):
        before = growing_stable.rank()
        growing_stable.insert(row)
        timed.append({
            "after_event": key[0], "role": key[1],
            "baseline_row": encode(row),
            "stable_rank_before_observation": before,
            "stable_rank_after_observation": growing_stable.rank(),
            "history_quotient_rank_after_observation": history.rank() - growing_stable.rank(),
        })
    require(growing_stable.rank() == history.rank(), "all histories eventually stable")
    receipt = {
        "status": "PASS_GLOBAL_RECOVERY_INTERSECTION" if not surviving.rank() else "GLOBAL_RECOVERY_INTERSECTION_HAS_NONSTABLE_MODES",
        "source_sha256": PIN,
        "donor": donor, "receiver": receiver, "terminal_frame": terminal,
        "public_inputs": n, "instructions": len(program),
        "receiver_chart_spaces": len(itinerary),
        "receiver_initial_roles": initial_roles,
        "receiver_observations": len(observations),
        "history_rank": history.rank(),
        "terminal_roles": final_roles,
        "terminal_rank": terminal_space.rank(),
        "stable_endpoint_roles": stable_roles,
        "stable_rank": stable.rank(),
        "history_mod_stable_rank": quotient.rank(),
        "global_recoverable_history_rank": len(common),
        "global_recoverable_mod_stable_rank": surviving.rank(),
        "nonstable_recoverable_basis": [encode(row) for row in surviving.rows.values()],
        "history_quotient_basis": [encode(row) for row in quotient.rows.values()],
        "terminal_history_intersection_basis": [encode(row) for row in common],
        "history_observation_keys": keys,
        "timed_stable_quotient": timed,
        "no_new_kappa": True,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({k: v for k, v in receipt.items() if not isinstance(v, list)}, indent=2))
    print("nonstable recoverable basis", receipt["nonstable_recoverable_basis"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    run(args.source, args.output)
