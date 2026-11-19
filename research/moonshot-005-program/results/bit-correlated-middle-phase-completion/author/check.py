#!/usr/bin/env python3
"""Finite exact controls for the correlated proper-boundary phase theorem."""
from argparse import ArgumentParser
from hashlib import sha256
from itertools import product, combinations
from pathlib import Path
import json


def space(rows):
    values = {0}
    for row in rows:
        values |= {value ^ row for value in tuple(values)}
    return frozenset(values)


def dimension(values):
    assert len(values) and len(values) & (len(values) - 1) == 0
    return len(values).bit_length() - 1


def subspaces(values):
    result = {frozenset({0})}
    queue = [frozenset({0})]
    while queue:
        small = queue.pop()
        for value in values - small:
            larger = small | frozenset(value ^ x for x in small)
            if larger not in result:
                result.add(larger)
                queue.append(larger)
    return sorted(result, key=lambda x: (len(x), tuple(sorted(x))))


def combine(mask, rows):
    result = 0
    for k, row in enumerate(rows):
        if mask >> k & 1:
            result ^= row
    return result


def sumspace(spaces):
    return space(value for values in spaces for value in values)


def independent_selection(allowed):
    # Direct enumeration of row choices; this is not the Hall test.
    def visit(k, chosen):
        if k == len(allowed):
            return True
        for value in allowed[k] - chosen:
            if visit(k + 1, chosen | frozenset(value ^ x for x in chosen)):
                return True
        return False
    return visit(0, frozenset({0}))


def check_lifts():
    cases = families = individual = 0
    histogram = {}
    for b in (1, 2, 3):
        for ne in range(1, min(b, 2) + 1):
            early = tuple(1 << k for k in range(ne))
            W = space(early)
            for nl in range(3):
                for late in product(range(1 << b), repeat=nl):
                    R = space(early + late)
                    rho = dimension(R) - ne
                    kernel = frozenset(beta for beta in range(1 << nl)
                                       if combine(beta, late) in W)
                    assert dimension(kernel) == nl - rho
                    Qs = subspaces(R)
                    preimages = []
                    for Q in Qs:
                        QW = sumspace([Q, W])
                        P = frozenset(beta for beta in range(1 << nl)
                                      if combine(beta, late) in QW)
                        assert dimension(P) == nl - rho + dimension(QW) - ne
                        for beta in P:
                            assert any((combine(alpha, early) ^ combine(beta, late)) in Q
                                       for alpha in range(1 << ne))
                        preimages.append(P)
                        individual += 1
                    # All pairs test sums of preimages, including zero Q.
                    for k, Q in enumerate(Qs):
                        for j, T in enumerate(Qs):
                            expected = frozenset(beta for beta in range(1 << nl)
                                if combine(beta, late) in sumspace([Q, T, W]))
                            assert sumspace([preimages[k], preimages[j]]) == expected
                    # Exhaustive local late feasibility for at most two slots;
                    # selected three-slot families stress subset obstructions.
                    for s in range(min(ne, 1) + 1):
                        count = nl + s
                        if count <= 2:
                            selections = product(range(len(Qs)), repeat=count)
                        else:
                            selections = product(range(min(len(Qs), 5)), repeat=count)
                        for ids in selections:
                            allowed = [frozenset(beta | (gamma << nl)
                                for beta in preimages[k] for gamma in range(1 << s))
                                for k in ids]
                            hall = True
                            for size in range(1, count + 1):
                                for subset in combinations(range(count), size):
                                    quotient_dim = dimension(sumspace([W] + [Qs[ids[a]] for a in subset])) - ne
                                    if quotient_dim + nl - rho + s < size:
                                        hall = False
                            assert hall == independent_selection(allowed)
                            families += 1
                    cases += 1
                    key = f"nE={ne},nL={nl},rho={rho}"
                    histogram[key] = histogram.get(key, 0) + 1
    return {"boundary_matrices": cases, "individual_preimages": individual,
            "late_families": families, "boundary_histogram": histogram}


def example_controls():
    # Full actual state includes independent original Y, not only proper zero.
    states = 0
    for x1, x2, z in product(range(2), repeat=3):
        incoming_y = z ^ x1
        output_y = incoming_y ^ x1 ^ x2
        assert output_y == z ^ x2
        states += 1
    # Wrongly imposing independent proper late x3 has no invertible 1Y solution.
    independent_solutions = []
    for alpha1, alpha2 in product(range(2), repeat=2):
        if all((alpha1*x1 ^ alpha2*x2 ^ x3) == x2
               for x1, x2, x3 in product(range(2), repeat=3)):
            independent_solutions.append((alpha1, alpha2))
    assert not independent_solutions
    # Total-span-only testing misses a deficient two-slot subfamily.
    Q = [frozenset({0}), frozenset({0}), space([1, 2, 4])]
    assert dimension(sumspace(Q)) == 3
    assert not independent_selection(Q)
    # Two scalar proper messages need not be linearly relabeled. Exhaust all
    # permutations on two actual Y bits and verify the projection fibre bound.
    import itertools
    nonlinear_cases = 0
    for permutation in itertools.permutations(range(4)):
        for proper_slice in (frozenset({0}), space([1]), space([2]), space([3]), space([1, 2])):
            rho = dimension(proper_slice)
            for projection in (1, 2, 3):
                size = projection.bit_count()
                values = {permutation[x] & projection for x in proper_slice}
                assert len(values) * (1 << (2-size)) >= 1 << rho
                nonlinear_cases += 1
    return {"arbitrary_Y_states": states,
            "independent_late_target_solutions": len(independent_solutions),
            "total_span_false_positive_rejected": True,
            "nonlinear_projection_cases": nonlinear_cases,
            "nL_minus_rho_positive_control": 1,
            "sufficient_field_threshold_not_inferred_from_binary_tests": True}


def main():
    parser = ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = {"status": "PASS_CORRELATED_PROPER_PHASE_LIFT",
              "scope": "finite exact support for the written all-dimension theorem",
              "lifts": check_lifts(), "controls": example_controls(),
              "new_complete_kappa": False,
              "proof_sha256": sha256(Path(__file__).with_name("PROOF.md").read_bytes()).hexdigest()}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print(json.dumps({k: v for k, v in result["lifts"].items() if k != "boundary_histogram"}))


if __name__ == "__main__":
    main()
