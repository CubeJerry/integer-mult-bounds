#!/usr/bin/env python3
"""Exact native premises for the universal all-width canonical pair gate.

Credits the separately pinned quadratic/exterior checker for source loading
and elementary Gaussian elimination.  The mathematical proof is PROOF.md.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

HELPER_PIN = "7f56cda7898ec290b2c588a22a48e5ce7eb7437cf3f7e9baf51ad6e77d887045"
MATCHING = [[25,51],[3,85],[31,36],[35,40],[73,11],[74,24],[75,86],[97,63],
 [93,20],[49,37],[98,59],[106,0],[105,44],[8,4],[21,68],[22,18],
 [30,96],[67,64],[38,34],[15,82],[79,10],[57,89],[28,62],[43,32],
 [58,29],[69,14],[55,26],[101,81],[46,100],[78,9],[84,76],
 [87,103],[110,41],[92,45],[33,17],[94,66],[19,16],[104,42],
 [5,95],[1,12],[50,23],[61,109],[99,83],[6,107],[53,72],[88,39],
 [7,70],[90,56],[2,13],[27,47],[54,91],[52,71],[65,48],[108,80],[60,102]]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def helper(path):
    need(hashlib.sha256(path.read_bytes()).hexdigest() == HELPER_PIN, "credited geometry-helper pin")
    spec = importlib.util.spec_from_file_location("credited_quadratic_geometry", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(repo, helper_path):
    g = helper(helper_path)
    R, K = g.load_native(repo)
    C = g.basis(K)
    n = len(R)
    need(n == 111 and len(C) == 9, "native count and canonical dimension")
    allbits = (1 << n)-1
    dot = lambda a, b: sum(x*y for x, y in zip(a,b))
    exclusive = {}
    restrictions = Counter()
    real_ranks = Counter()
    canonical_quadratic = Counter()
    max_orthogonal_common = 0
    def lift(i, support):
        pivot = next(j for j,x in enumerate(R[i]) if x)
        coords = [j for j in range(8) if j != pivot]
        return [[R[t][a]*R[t][b] for a,b in itertools.combinations_with_replacement(coords,2)] for t in support]
    for i in range(n):
        need(len(g.basis(c & (allbits ^ K[i]) for c in C)) == 8, "one-row canonical restriction rank")
        foreign = list(g.members(K[i] & ~(1 << i)))
        rank = g.mod_rank(lift(i,foreign),101)
        need(rank == 28, "canonical foreign support has no vanishing quadratic")
        canonical_quadratic[rank] += 1
    for i,j in itertools.combinations(range(n),2):
        forbidden = allbits ^ (K[i] | K[j])
        rank = len(g.basis(c & forbidden for c in C))
        need(rank == 7 and len(g.basis([K[i],K[j]])) == 2, "two-row canonical restriction kernel")
        restrictions[rank] += 1
        if dot(R[i],R[j]) == 0:
            max_orthogonal_common = max(max_orthogonal_common,(K[i]&K[j]).bit_count())
            continue
        need(abs(dot(R[i],R[j])) == 2, "nonorthogonal root angle")
        for a,b in ((i,j),(j,i)):
            support = list(g.members(K[a] & ~K[b] & ~(1 << a)))
            exclusive[a,b] = support
            rank = g.mod_rank([R[t] for t in support],101)
            need(rank == 7 and all(dot(R[a],R[t]) == 0 for t in support), "ordered exclusive support spans facet")
            real_ranks[rank] += 1
    need(sum(restrictions.values()) == 6105 and sum(real_ranks.values()) == 5740, "complete pair coverage")
    need(max_orthogonal_common == 32, "orthogonal common-support maximum")
    need(len(MATCHING) == 55 and len({a for edge in MATCHING for a in edge}) == 110, "55 disjoint matching edges")
    witnesses = []
    for i,j in MATCHING:
        candidates = []
        for a,b in ((i,j),(j,i)):
            need((a,b) in exclusive, "matching edges are nonorthogonal")
            support = exclusive[a,b]
            if len(support) != 27:
                continue
            rank = g.mod_rank(lift(a,support),101)
            if rank != 27:
                continue
            projection_norm = Fraction(dot(R[b],R[b])) - Fraction(dot(R[a],R[b])**2,dot(R[a],R[a]))
            need(projection_norm == 3, "projected normal squared norm")
            need(all(dot(R[b],R[t])**2 == dot(R[t],R[t]) for t in support), "known irreducible quadratic vanishes")
            candidates.append({"oriented_pair":[a,b],"exclusive_support":support,
                               "exclusive_size":27,"quadratic_evaluation_rank":27,
                               "projected_normal_squared_norm":"3","quadratic_form_rank":7})
        need(candidates, "matching edge has irreducible exclusive endpoint")
        witnesses.append({"edge":[i,j],"witness":candidates[0]})
    # The strict boundary of the universal argument: two complementary
    # V-planes in dimension 2V need not have a nonzero intersection.
    for V in (1,2,5):
        first = [1 << i for i in range(V)]
        second = [1 << i for i in range(V,2*V)]
        need(len(g.basis(first+second)) == 2*V, "strict dimension boundary negative control")
    repeated = MATCHING + [MATCHING[0]]
    need(len({a for e in repeated for a in e}) != 2*len(repeated), "overlapping pseudo-matching rejected")
    need(len(exclusive[92,54]) < 27 and len(exclusive[54,92]) < 27, "not every nonorthogonal pair has full exclusive support")
    return {"status":"PASS_AUTHOR_UNIVERSAL_CANONICAL_PAIR_GATE",
            "source_path":g.NATIVE,"source_sha256":g.PIN,
            "credited_helper_sha256":HELPER_PIN,"coefficient_fields":"all characteristic-two fields",
            "block_width":"every positive integer V","quotient_hypothesis":"canonical enlargement dimension d < 2V",
            "canonical_dimension":9,"one_row_restriction_rank":8,
            "pair_restriction_rank_histogram":dict(restrictions),
            "canonical_foreign_quadratic_rank_histogram":dict(canonical_quadratic),
            "ordered_nonorthogonal_exclusive_real_rank_histogram":dict(real_ranks),
            "real_minor_prime":101,"orthogonal_pair_closed_intersection_max":max_orthogonal_common,
            "matching":MATCHING,"matching_size":55,"matching_witnesses":witnesses,
            "negative_controls":{"overlapping_pseudo_matching_rejected":True,
                "dimension_boundary_complementary_planes":[1,2,5],
                "pivot_pair_92_54_exclusive_sizes":[len(exclusive[92,54]),len(exclusive[54,92])]},
            "proved_total_saving_upper_bound":57,"proved_chi_lower_bound":165,
            "excluded_marked_route_chi_caps":[138,131],"new_complete_kappa":False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo",type=Path,required=True)
    parser.add_argument("--geometry-check",type=Path)
    parser.add_argument("--output",type=Path,required=True)
    args = parser.parse_args()
    helper_path = args.geometry_check
    if helper_path is None:
        helper_path = args.repo / "research/moonshot-005-program/results/bit-quadratic-exterior/author/check.py"
    result = run(args.repo,helper_path)
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("matching","matching_witnesses")}))


if __name__ == "__main__":
    main()
