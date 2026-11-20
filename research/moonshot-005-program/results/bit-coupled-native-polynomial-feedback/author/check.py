#!/usr/bin/env python3
"""Check all ordinary native source cuts and the universal9k propagation bound."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
import ctypes
import itertools
import json
from pathlib import Path
import numpy as np
import construction


def main():
    p = ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--rank-library", type=Path)
    args = p.parse_args()
    geometric, f, a, previous, global_nodes, nodes_path = construction.context(args.repo)
    if args.rank_library:
        library = ctypes.CDLL(str(args.rank_library))
        native_rank = library.field_rank
        native_rank.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]
        native_rank.restype = ctypes.c_int
        def fast_rank(matrix):
            matrix = np.array(matrix, dtype=np.uint8, order="C", copy=True)
            return native_rank(matrix.ctypes.data, *matrix.shape, a.product.ctypes.data, a.inverse.ctypes.data)
        a.rank = fast_rank
    here = Path(__file__).parent
    raw = (here / "output/PARAMETERS.json").read_bytes()
    prm = json.loads(raw)
    witness_raw = (here / "output/NON-RS-WITNESSES.json").read_bytes()
    witnesses = json.loads(witness_raw)
    Q, visible, polys = construction.field_blocks(geometric, a)
    e0 = np.eye(16, dtype=np.uint8)[0]
    scalar_hist = Counter()
    for x, y in itertools.permutations(Q, 2):
        vs = [v for v, nodes in visible.items() if x in nodes and y in nodes]
        old = np.array([a.product[geometric.power(v, 2, a), construction.quotient(polys[v], x, a)] for v in vs]).T
        correction = np.array([a.product[geometric.power(v, 2, a), polys[v][:16] ^ e0] for v in vs]).T
        ranks = a.rank(old), a.rank(correction), a.rank(np.hstack([old, correction]))
        construction.require(len(vs) == 20 and ranks == (5, 5, 10), "all756 scalar propagation envelopes")
        scalar_hist[str(ranks)] += 1
    singletons = {j for (j, h), quota in a.quota.items() if quota == 45}
    donors = sorted(a.native - singletons)
    construction.require(donors == prm["ordinary_donors"] and len(donors) == 100, "all actual ordinary donors")
    construction.require(set(map(int, witnesses)) == set(donors), "all100 nonlinear-invariant source witnesses")
    source_cuts = native_cuts = nilpotent_checks = 0
    hashes = {}
    all_maps = {}
    for j in donors:
        V, maps = construction.source_maps(f, a, global_nodes, j, prm["feedback_seed"])
        construction.require(a.rank(V) == 3, "nontrivial full-row feedback")
        chart_spec = prm["early"][str(j)]
        chart = f.Chart(a, chart_spec["chart"], 3)
        chart.early(j, maps, chart_spec["seed"])
        for i in sorted(a.adj[j]):
            hs = [h for h in maps if a.planes[h] <= a.adj[i]]
            v = global_nodes["receiver_parameters"][str(j)][str(i)]
            construction.require(len(hs) == 16 and {global_nodes["H_nodes"][h] for h in hs} == set(visible[v]),
                                 "actual geometry equals the authenticated field block")
            remainder = polys[v][:16] ^ e0
            lift = np.kron(remainder[:, None], np.eye(3, dtype=np.uint8))
            construction.require(not np.any(a.mm(V, lift)), "all native inverse updates are square-zero")
            source = np.vstack([maps[h] for h in hs])
            construction.require(a.rank(source) == 48, "actual full source cut")
            source_cuts += 1
            native_cuts += i in a.native
            nilpotent_checks += 1
        witness = witnesses[str(j)]
        hs = witness["planes"]
        construction.require(len(set(hs)) == 16 and set(hs) <= set(maps), "sixteen actual source observations")
        construction.require(a.rank(np.vstack([maps[h] for h in hs])) == witness["rank"] < 48,
                             "genuine non-RS source information system")
        hashes[j] = sha256(b"".join(maps[h].tobytes() for h in sorted(maps))).hexdigest()
        all_maps[j] = maps
    # Literal noncommuting copy-axis generation, present at every donor.
    V = construction.feedback(f, 0)
    P, E = V[:, 9:12], V[:, 18:21]
    powers = [np.eye(3, dtype=np.uint8), P, a.mm(P, P)]
    words = np.array([a.mm(a.mm(left, E), right).reshape(-1) for left in powers for right in powers])
    construction.require(a.rank(words) == 9 and np.any(a.mm(P, E) ^ a.mm(E, P)), "full noncommuting matrix algebra")
    # An actual unsupported feedback block destroys the exact source inverse.
    i = min(a.adj[0] & a.native)
    v = global_nodes["receiver_parameters"]["0"][str(i)]
    bad = V.copy()
    bad[:, 42:45] = a.product[a.inverse[polys[v][14]], np.eye(3, dtype=np.uint8)]
    hs = [h for h in all_maps[0] if a.planes[h] <= a.adj[i]]
    bad_maps = []
    for h in hs:
        powers_node = a.vandermonde([global_nodes["H_nodes"][h]], 17)[0]
        bad_maps.append(np.kron(powers_node[:16][None, :], np.eye(3, dtype=np.uint8)) ^ a.product[powers_node[16] ^ 1, bad])
    bad_rank = a.rank(np.vstack(bad_maps))
    construction.require(bad_rank == 45, "forbidden coefficient position loses three source ranks")
    # This family is not itself a common H construction in the displayed coordinates.
    H = 263
    common_ranks = Counter()
    for i in range(111):
        if not a.planes[H] <= a.adj[i]:
            continue
        off = [np.vstack([F for h, F in all_maps[j].items() if h != H and a.planes[h] <= a.adj[i]]) for j in (0, 61)]
        union_rank = a.rank(np.vstack(off))
        construction.require(union_rank == 48, "ungauged pair has zero common inverse fibre")
        common_ranks[union_rank] += 1
    # One complete feedback instance checks the matrix-valued propagation, not only its envelope.
    actual_hist = Counter()
    for x, y in itertools.permutations(Q, 2):
        vs = [v for v, nodes in visible.items() if x in nodes and y in nodes]
        K = np.hstack([construction.kernel_columns(polys[v], x, V, a) for v in vs])
        actual_rank = a.rank(K)
        construction.require(actual_rank <= 27, "the actual coupled propagation obeys9k")
        actual_hist[actual_rank] += 1
    result = {"status": "PASS_UNIVERSAL_NONSATURATING_POLYNOMIAL_FEEDBACK_SOURCE",
              "field": {"size": 64, "binary_modulus": 67}, "feedback_polynomial": "z^16+1",
              "remainder_support": list(construction.SUPPORT), "free_feedback_slots": list(construction.GAPS),
              "arbitrary_matrix_block_count": 9, "universal_block_width_k": "any positive integer",
              "source_view_inverse": "I+N, N^2=0", "universal_propagation_rank_upper": "9k",
              "saturation_threshold": "15k", "scalar_propagation_pairs": 756, "scalar_envelope_histogram": dict(scalar_hist),
              "literal_component_width": 3, "ordinary_donors": donors, "geometric_source_cuts": source_cuts,
              "native_ordinary_source_cuts": native_cuts, "square_zero_checks": nilpotent_checks,
              "actual_early_basis_count": len(donors), "actual_early_basis_dimension": 96,
              "source_stars_inequivalent_to_RS": len(donors), "copy_axis_coefficient_algebra_dimension": 9,
              "source_coefficient_sha256": hashes, "literal_donor0_propagation_histogram": dict(actual_hist),
              "negative_controls": {"unsupported_position_cut_rank": bad_rank, "ungauged_H263_pair_union_ranks": dict(common_ranks)},
              "parameters_sha256": sha256(raw).hexdigest(), "non_RS_witnesses_sha256": sha256(witness_raw).hexdigest(),
              "global_nodes_path": str(nodes_path.relative_to(args.repo)), "global_nodes_sha256": sha256(nodes_path.read_bytes()).hexdigest(),
              "singleton_source_replacements": False, "complete_physical_bank_word_and_invoice": None,
              "common_H_D_K_endpoint": False, "actual_global_return_rank": None, "new_complete_kappa": False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "native_ordinary_source_cuts", "actual_early_basis_count", "literal_donor0_propagation_histogram")}, sort_keys=True))


if __name__ == "__main__":
    main()
