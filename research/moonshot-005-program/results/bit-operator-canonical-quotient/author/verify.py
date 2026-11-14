#!/usr/bin/env python3
"""Exact finite controls for the separately proved operator-quotient theorem.

This does not enumerate all fields or block widths. Source geometry is reused
from authenticated independent evidence, and its proof remains a dependency.
Prepared for @CubeJerry with OpenAI assistance; Apache-2.0.
"""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
from pathlib import Path

BASELINE = 'a22f6932c7a57328f92bcf7a6f373c1433ec52f8'
NATIVE = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
DEPS = {
    'results/bit-one-extra-coset/author/PROOF.md': 'a6b0a34517fd550c1565be4af47c975c464c5373bf52f0aea5a487a68fdc04fd',
    'results/bit-one-extra-coset/review/REVIEW.md': 'a45fe7e44bc383869f50293f83865345d43ae6e4697e4d83155f9f0a8f303e60',
    'results/bit-quotient-direction-savings/author/PROOF.md': '8e83d29e18e78e1b6f8e30a154b9cc84ad089c5283b2c04c807e048ffee5229b',
    'results/bit-quotient-direction-savings/review/REVIEW.md': '60cf45eceae4f3cd3dcd658e59fcbce7a3c626decc7eaefcf4e65ea42f980612',
    'results/bit-quotient-direction-savings/review/RESULT.json': '9ef3fb7f23605f8f7dd053dfb3a42b1ea1f71ab0f6945e365481262e72e771a8',
    'results/bit-all-route-rank-gap/ADMISSION.md': '871510f1d9eb76e66b4efe737274af719100e610c375343e78859ba08da062c7',
}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def rank(rows):
    basis = {}
    for x in rows:
        while x:
            b = x.bit_length() - 1
            if b in basis:
                x ^= basis[b]
            else:
                basis[b] = x
                break
    return len(basis)


def row_times(x, rows):
    y = 0
    while x:
        b = (x & -x).bit_length() - 1
        y ^= rows[b]
        x &= x - 1
    return y


def mm(a, b):
    return tuple(row_times(row, b) for row in a)


def mx(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def identity(v):
    return tuple(1 << i for i in range(v))


def zero(v):
    return (0,) * v


def tensor_row(word, channel, v):
    return sum(1 << (j*v+channel) for j in range(111) if word >> j & 1)


def tensor_basis(words, v):
    return [tensor_row(word, a, v) for word in words for a in range(v)]


def flatten(blocks, v):
    return [sum(blocks[j][a] << (j*v) for j in range(111)) for a in range(v)]


def scalar_tensor(K, v):
    I, Z = identity(v), zero(v)
    return [[I if word >> j & 1 else Z for j in range(111)] for word in K]


def inspect_fitting(A, K, basis, v):
    I, Z = identity(v), zero(v)
    need(len(A) == 111 and all(len(row) == 111 for row in A), '111 block rows/columns')
    full_rows = []
    row_quotients = []
    canonical = tensor_basis(basis, v)
    base_rank = rank(canonical)
    foreign = []
    deletion_rows = []
    for i, blocks in enumerate(A):
        need(blocks[i] == I, 'identity diagonal')
        need(all(blocks[j] == Z for j in range(111) if not K[i] >> j & 1), 'prescribed zeros')
        rows = flatten(blocks, v)
        full_rows.extend(rows)
        q = rank(canonical + rows) - base_rank
        row_quotients.append(q)
        count = sum(blocks[j] != Z for j in range(111) if j != i)
        foreign.append(count)
        if count < K[i].bit_count() - 1:
            deletion_rows.append(i)
            need(q == v, 'deleted block forces full V-dimensional quotient image')
    quotient = rank(canonical + full_rows) - base_rank
    ell = sum((n > 36) + (n > 52) for n in foreign)
    if quotient < v:
        need(ell == 222 and not deletion_rows, 'strictly subwidth quotient retains every contact')
    if quotient <= v:
        need(ell >= 205, 'one-width quotient gate')
    return dict(V=v, canonical_dimension=base_rank, fitting_rank=rank(full_rows),
                canonical_quotient_dimension=quotient, ell=ell,
                deletion_rows=deletion_rows, row_quotient_dimensions=row_quotients,
                foreign_support_histogram=dict(sorted(Counter(foreign).items())))


def make_supported_operator_fitting(K, v, G, maps):
    A = scalar_tensor(K, v)
    I = identity(v)
    for i, M in maps.items():
        base = mx(I, mm(M, G[i]))
        for j in range(111):
            A[i][j] = mx(base if K[i] >> j & 1 else zero(v), mm(M, G[j]))
    return A


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--programme', type=Path, required=True)
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    for name, digest in DEPS.items():
        need(hashlib.sha256((args.programme/name).read_bytes()).hexdigest() == digest, 'dependency pin: '+name)
    raw = args.native.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == NATIVE, 'native pin')
    native = json.loads(gzip.decompress(raw))
    roots = [tuple(map(Fraction, native['frames'][str(native['start'][i])]['B'][0])) for i in range(111)]
    orthogonal = [[sum(x*y for x, y in zip(a,b)) == 0 for b in roots] for a in roots]
    K = [sum(int(i == j or orthogonal[i][j]) << j for j in range(111)) for i in range(111)]
    basis = []
    indices = []
    for i, word in enumerate(K):
        if rank(basis+[word]) > len(basis):
            basis.append(word)
            indices.append(i)
    need(indices == [0,1,2,4,8,9,14,30,59], 'canonical binary basis')
    mask = (1 << 111) - 1
    zeros = [mask ^ row for row in K]
    for i in range(111):
        need(rank([w & zeros[i] for w in basis]) == 8, 'single forbidden restriction')
        for j in range(i):
            need(rank([w & zeros[i] & zeros[j] for w in basis]) == 7, 'pair forbidden restriction')
    degree = [word.bit_count()-1 for word in K]
    need(dict(Counter(degree)) == {55:1,56:11,57:16,58:36,59:28,60:13,61:5,62:1}, 'degree census')

    geometry = json.loads((args.programme/'results/bit-quotient-direction-savings/review/RESULT.json').read_text())
    need(geometry['status'] == 'PASS_INDEPENDENT_17_SAVINGS_PROOF_SOURCE_PREMISES', 'reviewed geometric premises')
    need(geometry['max_rank3_eligible'] == 17 and geometry['max_orthogonal4_eligible'] == 7, 'exceptional geometry')
    N = [0,1,3,6,12,20,36,111,111]
    envelope = []
    for r in range(1,9):
        for s in range(r,N[r]+1):
            for j in range(min(r,s)+1):
                if s > j+N[r-j]:
                    continue
                b = min(N[8-r],sum(d <= 52+s for d in degree))+min(N[8-r],sum(d <= 36+s for d in degree))+2*j
                envelope.append([r,s,j,b])
    need(len(envelope) == 569, 'parameter envelope')
    critical = [e for e in envelope if e[3] >= 17]
    need(critical == [[3,5,0,20],[3,6,0,20],[4,4,3,18],[4,4,4,20]], 'only inherited exceptional cases')

    S = [0,2,38,41,42,45]
    U = [i for i in range(111) if all(orthogonal[i][j] for j in S)]
    need(len(U) == 20 and not set(S)&set(U), 'sharp support geometry')
    h = sum(1 << j for j in S)
    sharp_scalar = [row ^ h if i in U else row for i,row in enumerate(K)]
    sharp = []
    for v in [1,2,3,5]:
        out = inspect_fitting(scalar_tensor(sharp_scalar,v),K,basis,v)
        need(out['canonical_quotient_dimension'] == v and out['fitting_rank'] == 10*v and out['ell'] == 205, 'all tested sharp lifts')
        sharp.append(out)

    # A genuinely non-tensor quotient with noncommuting G blocks and maps.
    v = 2
    I, P, Q = (1,2), (3,2), (1,3)
    need(mm(P,Q) != mm(Q,P), 'noncommuting controls')
    matrices = list(itertools.product(range(4),repeat=2))
    G = [zero(v) for _ in range(111)]
    for j, block in zip(S,[I,P,Q,mm(P,Q),I,P]):
        G[j] = block
    maps = {i: matrices[t % len(matrices)] for t,i in enumerate(U)}
    operators = make_supported_operator_fitting(K,v,G,maps)
    operator_check = inspect_fitting(operators,K,basis,v)
    need(operator_check['canonical_quotient_dimension'] == v, 'full operator quotient width')
    # Uniform right channel maps preserve scalar-tensor quotient lines.
    # Exhibiting failure of closure proves this quotient is not such a line.
    cbase = tensor_basis(basis,v)
    grows = []
    for E in [(1,0),(2,0),(0,1),(0,2)]:
        transformed = [mm(block,E) for block in G]
        if rank(cbase+flatten(G,v)+flatten(transformed,v)) > 9*v+v:
            grows.append(list(E))
    need(grows, 'genuinely entangled quotient, not a scalar coset tensor k^V')
    singular = [i for i,M in maps.items() if rank(M) < v]
    need(all(i not in operator_check['deletion_rows'] for i in singular), 'singular maps cannot erase an entire block')

    # One-dimensional quotient at V=2 changes blocks but erases no block.
    Gsmall = [zero(2) for _ in range(111)]
    Gsmall[0] = (1,0)
    smallmaps = {i:I for i in range(111) if orthogonal[i][0]}
    small = inspect_fitting(make_supported_operator_fitting(K,2,Gsmall,smallmaps),K,basis,2)
    need(small['canonical_quotient_dimension'] == 1 and small['ell'] == 222, 'strictly subwidth control')

    # At d=V+1 deletion-row quotient images can differ: common-image gluing
    # is no longer justified. Both rows erase column 0 in full width two.
    larger = scalar_tensor(K,2)
    i,l = U[:2]
    hs = [1<<0,(1<<0)|(1<<2),(1<<0)|(1<<38)]
    for receiver,hsecond in [(i,hs[1]),(l,hs[2])]:
        for j in range(111):
            correction = ((hs[0]>>j&1), (hsecond>>j&1)<<1)
            larger[receiver][j] = mx(larger[receiver][j],correction)
    beyond = inspect_fitting(larger,K,basis,2)
    need(beyond['canonical_quotient_dimension'] == 3 and larger[i][0] == (0,0) and larger[l][0] == (0,0), 'd=V+1 distinct-image control')
    local_rows = [flatten(larger[t],2) for t in (i,l)]
    local_dims = [rank(cbase+r)-18 for r in local_rows]
    joint_dim = rank(cbase+local_rows[0]+local_rows[1])-18
    need(local_dims == [2,2] and joint_dim == 3, 'two injective quotient images differ')

    # The conclusion is not an impossibility for unrestricted extensions.
    largeS = [0,1,2,3,4,9,30,8]
    sm = sum(1 << j for j in largeS)
    scalar_large = [(1<<i) if i in largeS else word & ~sm for i,word in enumerate(K)]
    outside = inspect_fitting(scalar_tensor(scalar_large,1),K,basis,1)
    need(outside['ell'] == 183 and outside['canonical_quotient_dimension'] > 1, 'scope counterexample')

    # The identity diagonal hypothesis is indispensable to the injection step.
    bad = scalar_tensor(K,2)
    bad[0][0] = (0,0)
    rejected = False
    try:
        inspect_fitting(bad,K,basis,2)
    except ValueError as e:
        rejected = str(e) == 'identity diagonal'
    need(rejected, 'reject missing diagonal premise')

    result = dict(status='PASS_OPERATOR_CANONICAL_QUOTIENT_CONTROLS', baseline_sha=BASELINE,
                  native_sha256=NATIVE, source_restrictions=dict(single=111,pair=6105),
                  parameter_cases=len(envelope), exceptional_geometry_reused_not_rerun=True,
                  dependency_sha256=DEPS, sharp_tensor_controls=sharp,
                  noncommuting_entangled_control=operator_check,
                  tensor_line_invariance_failures=grows, singular_map_receivers=singular,
                  strict_subwidth_control=small, dimension_V_plus_one_control=beyond,
                  distinct_image_dimensions=local_dims, distinct_image_join_dimension=joint_dim,
                  unrestricted_extension_counterexample=outside,
                  negative_controls=dict(bound206_rejected_by_sharp205=True,
                                         common_image_extension_beyond_V_rejected=True,
                                         missing_identity_diagonal_rejected=rejected),
                  proof_scope='All characteristic-two fields and widths proved separately. Finite controls are not an exhaustive operator theorem.',
                  classification='New author proof pending independent review; no supplier or new kappa.')
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status=result['status'],sharp_ell=[x['ell'] for x in sharp],
                         entangled_quotient_dimension=operator_check['canonical_quotient_dimension'],
                         strict_subwidth_ell=small['ell'],
                         larger_image_dimensions=local_dims+[joint_dim],
                         unrestricted_control_ell=outside['ell'])))


if __name__ == '__main__':
    main()
