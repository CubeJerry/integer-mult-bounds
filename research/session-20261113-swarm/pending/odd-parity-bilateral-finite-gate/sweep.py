#!/usr/bin/env python3
"""Odd-parity H4/2 rounding with bilateral radial slack at most one half."""

from __future__ import annotations

import itertools
import json
from collections import deque
from math import factorial


H = (
    (1, 1, 1, 1),
    (1, -1, 1, -1),
    (1, 1, -1, -1),
    (1, -1, -1, 1),
)
RADII = (5, 9, 11)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def norm_squared(point):
    return sum(value * value for value in point)


def encode_key(key):
    pattern, sign = key
    return [list(pattern), sign]


def orbit_key(point):
    pattern = tuple(sorted(abs(value) for value in point))
    if 0 in point:
        return pattern, None
    product = 1
    for value in point:
        product *= 1 if value > 0 else -1
    return pattern, product


def orbit_capacity(key):
    pattern, sign_class = key
    multiplicities = {}
    for value in pattern:
        multiplicities[value] = multiplicities.get(value, 0) + 1
    zero_count = multiplicities.pop(0, 0)
    denominator = factorial(zero_count)
    for multiplicity in multiplicities.values():
        denominator *= factorial(multiplicity)
    placements = factorial(4) // denominator
    signs = 1 << (4 - zero_count)
    if zero_count == 0:
        require(sign_class in (-1, 1), "nonzero orbit needs a sign-product label")
        signs //= 2
    else:
        require(sign_class is None, "zero-containing orbit has no sign-product label")
    return placements * signs


def canonical_rep(key):
    pattern, sign_class = key
    if sign_class is None or sign_class == 1:
        return pattern
    return (-pattern[0], pattern[1], pattern[2], pattern[3])


def matrix_multiply(left, right):
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(4))
              for j in range(4))
        for i in range(4)
    )


def matrix_transpose(matrix):
    return tuple(tuple(matrix[i][j] for i in range(4)) for j in range(4))


def is_signed_permutation(matrix):
    return (
        len(matrix) == 4
        and all(len(row) == 4 for row in matrix)
        and all(sum(abs(value) for value in row) == 1 for row in matrix)
        and all(sum(abs(matrix[i][j]) for i in range(4)) == 1
                for j in range(4))
    )


def signed_permutations(even_signs_only=False):
    result = []
    for permutation in itertools.permutations(range(4)):
        for signs in itertools.product((-1, 1), repeat=4):
            if even_signs_only and signs[0] * signs[1] * signs[2] * signs[3] != 1:
                continue
            matrix = [[0] * 4 for _ in range(4)]
            for row, column in enumerate(permutation):
                matrix[row][column] = signs[row]
            result.append(tuple(tuple(row) for row in matrix))
    return result


def graph_group_check():
    w_d4 = set(signed_permutations(even_signs_only=True))
    all_signed = set(signed_permutations(even_signs_only=False))
    ht = matrix_transpose(H)
    input_projection = set()
    output_projection = set()
    pair_count = 0
    for a in all_signed:
        numerator = matrix_multiply(matrix_multiply(H, a), ht)
        if not all(value % 4 == 0 for row in numerator for value in row):
            continue
        b = tuple(tuple(value // 4 for value in row) for row in numerator)
        if not is_signed_permutation(b):
            continue
        require(matrix_multiply(b, H) == matrix_multiply(H, a),
                "paired action fails B H=H A")
        input_projection.add(a)
        output_projection.add(b)
        pair_count += 1
    require(len(all_signed) == 384 and len(w_d4) == 192,
            "signed-permutation group order changed")
    require(input_projection == w_d4 and output_projection == w_d4,
            "paired projections are not W(D4)")
    require(pair_count == 192, "paired signed-permutation count changed")
    return {
        "all_signed_permutations_examined": len(all_signed),
        "paired_group_order": pair_count,
        "input_projection_order": len(input_projection),
        "output_projection_order": len(output_projection),
    }


def odd_input_orbits(radius):
    patterns = {
        tuple(sorted(values))
        for values in itertools.product(range(radius + 1), repeat=4)
        if sum(value * value for value in values) <= radius * radius
        and sum(values) % 2 == 1
    }
    result = []
    for pattern in sorted(patterns):
        keys = [(pattern, None)] if 0 in pattern else [
            (pattern, 1), (pattern, -1)
        ]
        for key in keys:
            rep = canonical_rep(key)
            require(sum(rep) % 2 == 1, "input orbit representative is not odd")
            capacity = orbit_capacity(key)
            result.append({
                "key": key,
                "representative": rep,
                "capacity": capacity,
                "norm_squared": norm_squared(rep),
            })
    return result


def parity_preserving_corners(point):
    require(sum(point) % 2 == 1, "corner generator requires odd input")
    hx = tuple(sum(H[i][j] * point[j] for j in range(4)) for i in range(4))
    require(all(value % 2 == 1 for value in hx),
            "odd input must have half-integral H4/2 image")
    lower = tuple(value // 2 for value in hx)
    all_corners = {
        tuple(lower[i] + bits[i] for i in range(4))
        for bits in itertools.product((0, 1), repeat=4)
    }
    require(len(all_corners) == 16, "half-integral image must have 16 corners")
    corners = sorted(point for point in all_corners if sum(point) % 2 == 1)
    require(len(corners) == 8, "exactly eight corners must preserve odd parity")
    for output in corners:
        error_numerator = sum((2 * output[i] - hx[i]) ** 2 for i in range(4))
        require(error_numerator == 4, "a nearest corner must have error exactly one")
    return corners


def bilateral_half_ok(output_norm_squared, input_norm_squared):
    """Decide |sqrt(m)-sqrt(n)| <= 1/2 using integers only."""
    value = 4 * output_norm_squared + 4 * input_norm_squared - 1
    if value <= 0:
        return True
    return value * value <= 64 * output_norm_squared * input_norm_squared


class Dinic:
    def __init__(self, size):
        self.graph = [[] for _ in range(size)]

    def add_edge(self, source, target, capacity):
        forward = [target, capacity, len(self.graph[target])]
        reverse = [source, 0, len(self.graph[source])]
        self.graph[source].append(forward)
        self.graph[target].append(reverse)
        return forward

    def max_flow(self, source, sink):
        total = 0
        size = len(self.graph)
        while True:
            level = [-1] * size
            level[source] = 0
            queue = deque([source])
            while queue:
                node = queue.popleft()
                for target, capacity, _ in self.graph[node]:
                    if capacity > 0 and level[target] < 0:
                        level[target] = level[node] + 1
                        queue.append(target)
            if level[sink] < 0:
                return total
            next_edge = [0] * size

            def push(node, available):
                if node == sink:
                    return available
                while next_edge[node] < len(self.graph[node]):
                    index = next_edge[node]
                    target, capacity, reverse = self.graph[node][index]
                    if capacity > 0 and level[target] == level[node] + 1:
                        sent = push(target, min(available, capacity))
                        if sent:
                            self.graph[node][index][1] -= sent
                            self.graph[target][reverse][1] += sent
                            return sent
                    next_edge[node] += 1
                return 0

            while True:
                sent = push(source, 1 << 60)
                if not sent:
                    break
                total += sent

    def maximal_source_side(self, sink):
        reverse_residual = [[] for _ in self.graph]
        for source, edges in enumerate(self.graph):
            for target, capacity, _ in edges:
                if capacity > 0:
                    reverse_residual[target].append(source)
        can_reach_sink = {sink}
        queue = deque([sink])
        while queue:
            node = queue.popleft()
            for previous in reverse_residual[node]:
                if previous not in can_reach_sink:
                    can_reach_sink.add(previous)
                    queue.append(previous)
        return set(range(len(self.graph))) - can_reach_sink


def prepare_radius(radius):
    inputs = odd_input_orbits(radius)
    output_caps = {}
    pair_degree = {}
    input_corner_total = 0
    input_accepted_total = 0
    corner_output_edge_keys = set()
    accepted_edge_keys = set()
    per_representative = []

    for i, orbit in enumerate(inputs):
        rep = orbit["representative"]
        corners = parity_preserving_corners(rep)
        input_corner_total += orbit["capacity"] * len(corners)
        accepted = []
        for output in corners:
            key = orbit_key(output)
            corner_output_edge_keys.add(key)
            m = norm_squared(output)
            if bilateral_half_ok(m, orbit["norm_squared"]):
                accepted.append(output)
                accepted_edge_keys.add(key)
                output_caps[key] = orbit_capacity(key)
                pair_degree[(i, key)] = pair_degree.get((i, key), 0) + 1
        input_accepted_total += orbit["capacity"] * len(accepted)
        per_representative.append({
            "input_orbit": encode_key(orbit["key"]),
            "representative": list(rep),
            "input_capacity": orbit["capacity"],
            "preserving_corner_count": len(corners),
            "accepted_corner_count": len(accepted),
        })

    output_keys = sorted(output_caps)
    output_index = {key: j for j, key in enumerate(output_keys)}
    outputs = [
        {"key": key, "capacity": output_caps[key],
         "norm_squared": norm_squared(canonical_rep(key))}
        for key in output_keys
    ]
    pair_degree_indexed = {}
    quotient_edges = []
    for (i, key), degree in sorted(
        pair_degree.items(), key=lambda item: (item[0][0], output_index[item[0][1]])
    ):
        j = output_index[key]
        quotient_edges.append((i, j))
        pair_degree_indexed[(i, j)] = degree
        require(inputs[i]["capacity"] * degree % outputs[j]["capacity"] == 0,
                "filtered orbit-pair relation is not biregular")

    input_count = sum(orbit["capacity"] for orbit in inputs)
    all_corner_output_count = sum(orbit_capacity(key) for key in corner_output_edge_keys)
    accepted_output_count = sum(orbit["capacity"] for orbit in outputs)
    return {
        "radius": radius,
        "inputs": inputs,
        "outputs": outputs,
        "pair_degree": pair_degree_indexed,
        "quotient_edges": quotient_edges,
        "input_count": input_count,
        "input_orbit_count": len(inputs),
        "all_corner_output_count": all_corner_output_count,
        "all_corner_orbit_count": len(corner_output_edge_keys),
        "accepted_output_count": accepted_output_count,
        "accepted_output_orbit_count": len(outputs),
        "preserving_corner_edge_count": input_corner_total,
        "accepted_error_slack_edge_count": input_accepted_total,
        "representatives": per_representative,
        "corner_output_keys": sorted(corner_output_edge_keys),
        "accepted_output_keys": sorted(accepted_edge_keys),
    }


def solve_radius(radius):
    data = prepare_radius(radius)
    input_count = len(data["inputs"])
    output_count = len(data["outputs"])
    source = 0
    input_offset = 1
    output_offset = input_offset + input_count
    sink = output_offset + output_count
    network = Dinic(sink + 1)
    inf = data["input_count"] + data["accepted_output_count"] + 1

    source_edges = []
    for i, orbit in enumerate(data["inputs"]):
        edge = network.add_edge(source, input_offset + i, orbit["capacity"])
        source_edges.append((orbit["capacity"], edge))
    pair_edges = []
    for i, j in data["quotient_edges"]:
        edge = network.add_edge(input_offset + i, output_offset + j, inf)
        pair_edges.append((i, j, edge))
    sink_edges = []
    for j, orbit in enumerate(data["outputs"]):
        edge = network.add_edge(output_offset + j, sink, orbit["capacity"])
        sink_edges.append((orbit["capacity"], edge))

    flow = network.max_flow(source, sink)
    source_loads = [capacity - edge[1] for capacity, edge in source_edges]
    output_loads = [capacity - edge[1] for capacity, edge in sink_edges]
    row_sums = [0] * input_count
    column_sums = [0] * output_count
    pair_flows = []
    for i, j, edge in pair_edges:
        amount = inf - edge[1]
        if amount > 0:
            pair_flows.append([i, j, amount])
            row_sums[i] += amount
            column_sums[j] += amount
    require(row_sums == source_loads, "input-orbit flow conservation failed")
    require(column_sums == output_loads, "output-orbit flow conservation failed")
    require(sum(source_loads) == flow == sum(output_loads),
            "total quotient flow does not conserve")
    require(all(output_loads[j] <= data["outputs"][j]["capacity"]
                for j in range(output_count)),
            "quotient flow exceeds output capacity")

    source_side = network.maximal_source_side(sink)
    selected_inputs = {
        i for i in range(input_count) if input_offset + i in source_side
    }
    selected_outputs = {
        j for j in range(output_count) if output_offset + j in source_side
    }
    actual_neighbors = {
        j for i, j in data["quotient_edges"] if i in selected_inputs
    }
    require(actual_neighbors == selected_outputs,
            "cut output orbits are not the complete neighborhood")
    t_mass = sum(data["inputs"][i]["capacity"] for i in selected_inputs)
    n_mass = sum(data["outputs"][j]["capacity"] for j in selected_outputs)
    cut_capacity = data["input_count"] - t_mass + n_mass
    require(cut_capacity == flow, "cut and max-flow values disagree")
    deficiency = t_mass - n_mass
    require(deficiency == data["input_count"] - flow,
            "Hall cut deficiency disagrees with flow")

    feasible = flow == data["input_count"]
    if feasible:
        require(source_loads == [orbit["capacity"] for orbit in data["inputs"]],
                "feasible flow does not saturate every input orbit")
    return {
        "radius": radius,
        "radial_slack_filter": "abs(sqrt(m)-sqrt(n)) <= 1/2",
        "parity_restriction": "sum(x) and sum(y) odd",
        "domain": {
            "input_count": data["input_count"],
            "input_orbit_count": data["input_orbit_count"],
            "all_parity_preserving_corners_over_input_domain":
                data["preserving_corner_edge_count"],
            "all_corner_output_count": data["all_corner_output_count"],
            "all_corner_output_orbit_count": data["all_corner_orbit_count"],
            "accepted_output_count": data["accepted_output_count"],
            "accepted_output_orbit_count": data["accepted_output_orbit_count"],
            "quotient_adjacencies": len(data["quotient_edges"]),
            "accepted_error_slack_edge_count": data["accepted_error_slack_edge_count"],
        },
        "max_flow": flow,
        "feasible": feasible,
        "flow_certificate": {
            "positive_orbit_pair_flows": pair_flows,
            "input_supplies": source_loads,
            "output_loads": output_loads,
        },
        "hall_cut": {
            "input_capacity": t_mass,
            "neighbor_capacity": n_mass,
            "deficiency": deficiency,
            "input_orbit_count": len(selected_inputs),
            "output_orbit_count": len(selected_outputs),
            "input_orbits": [
                {"key": encode_key(data["inputs"][i]["key"]),
                 "capacity": data["inputs"][i]["capacity"]}
                for i in sorted(selected_inputs)
            ],
            "neighbor_orbits": [
                {"key": encode_key(data["outputs"][j]["key"]),
                 "capacity": data["outputs"][j]["capacity"]}
                for j in sorted(selected_outputs)
            ],
        },
        "input_orbit_capacities": [
            {"key": encode_key(o["key"]),
             "representative": list(o["representative"]),
             "capacity": o["capacity"], "norm_squared": o["norm_squared"]}
            for o in data["inputs"]
        ],
        "accepted_output_orbit_capacities": [
            {"key": encode_key(o["key"]),
             "capacity": o["capacity"], "norm_squared": o["norm_squared"]}
            for o in data["outputs"]
        ],
        "representatives": data["representatives"],
    }


def main():
    group = graph_group_check()
    records = []
    stopped = False
    for radius in RADII:
        record = solve_radius(radius)
        records.append(record)
        if not record["feasible"]:
            stopped = True
            break
    completed_radii = [record["radius"] for record in records]
    print(json.dumps({
        "status": "PASS",
        "scope": "only odd-parity inputs, odd-parity outputs, radii 5, 9, 11, error cap one",
        "operator": [list(row) for row in H],
        "group": {
            **group,
            "identified_as": "paired W(D4) signed-permutation action",
        },
        "exact_filter": {
            "formula": "let D=4m+4n-1; accept iff D<=0 or D^2<=64mn",
            "derivation": "abs(sqrt(m)-sqrt(n))<=1/2 iff m+n-2sqrt(mn)<=1/4",
            "floating_point_used": False,
        },
        "matching_lift": (
            "uniform quotient flow on each biregular orbit-pair edge set gives "
            "a fractional matching; Hall's inequality follows for every input "
            "subset, so Hall's theorem gives a full finite injection"
        ),
        "completed_radii": records,
        "stop_rule": "stop at the first deficient radius",
        "stopped_on_obstruction": stopped,
        "untouched_radii": [r for r in RADII if r not in completed_radii],
        "limits": "finite evidence only; no global construction or extrapolation",
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
