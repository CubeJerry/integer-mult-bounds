"""Independent checks for the S010 single-cut consumer-access control."""
import argparse
import gzip
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

PIN = "2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883"
B = [5, 56, 65, 69, 77, 96, 100, 103]
J_DISJOINT = [0, 7, 20, 27, 36, 46, 57, 111]


def need(ok, message):
    if not ok:
        raise AssertionError(message)


parser = argparse.ArgumentParser()
parser.add_argument("--repo", required=True, type=Path,
                    help="root of the pinned programme checkout")
args = parser.parse_args()
source = args.repo / "research/shared-wire-split-composition/data/final.json.gz"
raw = source.read_bytes()
need(hashlib.sha256(raw).hexdigest() == PIN, "pinned native source SHA-256")
s = json.loads(gzip.decompress(raw))


def root(role):
    bits = s["frames"][s["initial"][role]][0]
    support = [i for i in range(9) if (bits >> i) & 1]
    if len(support) == 3:
        if 8 in support:
            return [2 * int(i in support) for i in range(8)]
        return [1 if i in support else -1 for i in range(8)]
    if len(support) == 7:
        i, j = [k for k in range(9) if k not in support]
        if j == 8:
            return [1 if k == i else -1 for k in range(8)]
        return [2 * ((k == i) - (k == j)) for k in range(8)]
    raise ValueError((role, bits, support))


host = {
    s["live"][k]: (s["hosted"]["X2"][p], s["hosted"]["Y2"][p])
    for p, k in enumerate(s["hosted"]["Dports"])
}
H = sorted(host)
need(len(H) == 96 and set(B) <= set(H) and set(J_DISJOINT) <= set(H),
     "hosted frame coordinates")
roots = {i: root(i) for i in H}


def gram(i, j):
    return Fraction(sum(a * b for a, b in zip(roots[i], roots[j])), 8)


for clique in (B, J_DISJOINT):
    need(all(gram(i, j) == int(i == j) for i in clique for j in clique),
         "selected frame is exactly orthonormal")

# Negative arithmetic control: the source has a root pair with inner product
# +4. Floor division by 8 would incorrectly erase this nonorthogonality.
positive_four_pair = (0, 1)
inner = sum(a * b for a, b in zip(roots[positive_four_pair[0]],
                                  roots[positive_four_pair[1]]))
need(inner == 4, "positive-four inner-product control pair")
need(gram(*positive_four_pair) == Fraction(1, 2),
     "exact normalized nonorthogonal value is 1/2")
need(inner // 8 == 0, "legacy floor would falsely label control pair orthogonal")
need(set(B).isdisjoint(J_DISJOINT), "hosted frames are disjoint")

# Exact native chart evidence for the actual D endpoints and Hub consumer.
W = 127
need(len(s["frames"][W]) == 9, "Hub chart dimension")
native_pairs = Counter((e[2], e[3]) for e in s["program"] if e[0] == "MOVE")
endpoints = []
for i in B:
    b, d = host[i]
    F = s["final"][d]
    need(len(s["frames"][F]) == 8, f"D endpoint facet dimension for {i}")
    need(s["final"][b] == W, f"current target B row at Hub for {i}")
    # The exact chart pair occurs in the pinned source. A new owned use remains
    # a new invocation with its own rank-one charge.
    need(native_pairs[(F, W)] > 0, f"native facet-to-Hub chart pair for {i}")
    endpoints.append({"i": i, "b_field": b, "d_field": d, "F_chart": F,
                      "F_dim": 8, "W_chart": W, "W_dim": 9,
                      "native_pair_occurrences": native_pairs[(F, W)],
                      "new_owned_MOVE_rank": 1})


def binary_span(frame):
    span = {0}
    for vector in frame:
        span |= {x ^ vector for x in tuple(span)}
    return frozenset(span)


F_by_role = {i: binary_span(s["frames"][s["final"][host[i][1]]]) for i in H}
need(len(set(F_by_role.values())) == 96, "all hosted endpoint facets are distinct")
need(all(not F_by_role[i] <= F_by_role[j] for i in B for j in J_DISJOINT),
     "no B source facet lies in a selected J-principal downset")

print(json.dumps({
    "status": "PASS_SINGLE_CUT_CONSUMER_ACCESS_CONTROL",
    "source_gzip_sha256": PIN,
    "hosted_roles": len(H),
    "Hub": {"chart": W, "dimension": 9},
    "cut_frame_B": B,
    "disjoint_frame_negative_control": J_DISJOINT,
    "B_gram_identity": True,
    "disjoint_frame_gram_identity": True,
    "positive_four_gram_negative_control": {
        "roles": list(positive_four_pair), "inner_product": inner,
        "normalized_exact": str(gram(*positive_four_pair)),
        "legacy_floor_by_8": inner // 8
    },
    "B_and_negative_control_disjoint": True,
    "actual_D_endpoints_and_rank1_Hub_moves": endpoints,
    "single_cut_demand": 8,
    "single_cut_added_MOVE_price": 8,
    "all_positive_whole_field_volumes": "each capacity is multiplied by V; price is unchanged",
    "scope": "one hosted orthogonal-frame cut only; not a construction satisfying the complete family or all native duties"
}, indent=2))
