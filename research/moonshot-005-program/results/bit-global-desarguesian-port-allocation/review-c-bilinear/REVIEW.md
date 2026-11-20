# Independent bilinear supplement: admitted finite geometry, no source word

This append-only supplement independently verifies the seven-form description, the common GF64 node assignment, every actual receiver view, the induced local field structures, and the algebraic claims in the final author prose. The frozen allocation review in `review-c/` remains unchanged. The independent checker imports no author or predecessor code; it uses the author tables only as witnesses whose contents it reconstructs and checks.

**Verdict:** `PASS_INDEPENDENT_GLOBAL_BILINEAR_MARKING_AND_SHARED_NODES`. This is a finite geometric and algebraic certificate. It certifies no common H word, no complete source word, and no new complete kappa.

## Reproduction and binding

From the repository root:

```sh
python -I -B research/moonshot-005-program/results/bit-global-desarguesian-port-allocation/review-c-bilinear/check.py --repo . --out FRESH
```

The output line is:

```text
PASS_INDEPENDENT_GLOBAL_BILINEAR_MARKING_AND_SHARED_NODES 315 28 7560 6470 40320
```

`SOURCE-PINS.json` binds the exact native layout, E8 lattice basis, allocation witness, global-node witness, author bilinear implementation, both final author prose files (`PROOF.md` and `BILINEAR-PROOF.md`), and the frozen allocation-review checker. `MANIFEST.json` binds this supplement and its independent outputs. The author implementation is hashed for provenance and is never imported or executed by the reviewer.

## Independent method

The reviewer represents each alternating form as a symmetric, zero-diagonal eight by eight binary matrix and evaluates it by ordinary parity operations. This differs from the author's wedge-mask implementation. It independently reconstructs binary quadratic values from the pinned E8 data, the anisotropic planes, the marked radical lines, all contraction maps, and the local field operators. Its GF64 arithmetic uses carryless polynomial convolution followed by polynomial reduction modulo X^6+X+1. Every field and node identity is checked with this implementation.

## Complete seven-form description

In wedge order 01,02,...,07,12,...,67, the seven masks are

```text
138420225, 16418, 16777284, 131088, 33587328, 135406080, 67637248.
```

They are independent. Their first coordinate agrees with the native polar form on all 65,536 ordered pairs. Their complete common-zero set among all two-dimensional binary subspaces has exactly 315 members; it equals the 315 distinct radicals of the 630 selected native D charts. This enumeration does not assume in advance that a common-zero plane is singular. The marked Pluecker vectors have rank 21 in the 28-dimensional exterior square, so the seven forms are the entire alternating annihilator of the selected radical lines.

For all 135 nonzero singular vectors x, the contraction C_x has rank four. Its 16-vector kernel is a totally singular four-space. These 135 kernels are distinct, and each contains exactly seven marked lines. For all 120 nonsingular x, the contraction has rank seven and kernel {0,x}. Among the 127 nonzero linear combinations of the seven forms, 63 have rank four and 64 have rank eight. These extra checks establish the complete finite contraction structure used by the source construction.

For q(x)=1 and b(x,y)=1, write C(x,y)=1+2u in six tail coordinates u0,...,u5. The reviewer derives the Boolean algebraic normal form by a Moebius transform and obtains

```text
q(y) = Q(u) = u1*u3 + u2*u4 + u0*u5.
```

The ANF masks are exactly 10, 20 and 33, without constant or linear terms. All 15,360 eligible ordered pairs satisfy this same function, and Q has 28 ones.

## Global labels and actual source views

For every H={a,b,a+b}, the value c_H=C(a,b) is independent of its chosen distinct pair. The 28 possible labels are exactly the odd seven-bit words whose tails satisfy Q=1. Each label occurs on 40 H planes. Every one of the 120 donor stars meets each label once; thus every label class partitions the 120 roots into 40 disjoint triples.

The pinned node witness takes c0=21 and identifies

```text
q0(t) = 1 + Q((c0 >> 1) + t)
```

with the GF64 quadratic form qF(z)=z^9+z^18+z^36 through a linear map theta. The source Witt basis is [1,32,4,16,2,8], and its field images are [3,5,13,18,1,58]. The reviewer checks all 64 quadratic values and all 4,096 linearity pairs. The 28 nodes a_H=theta((c_H+c0)>>1) are exactly the 28 zeroes of qF, and the assignment is genuinely shared across all H charts.

For distinct perpendicular roots j,i, the parameter v_ji=theta(C(j,i)>>1) is nonzero. Each donor's 63 perpendicular receivers bijects onto all 63 nonzero GF64 elements. For every actual receiver view, its sixteen H nodes are exactly

```text
bF(v_ji,a_H) = 1 + qF(v_ji).
```

The reviewer verifies all 7,560 geometric views and all 6,470 proper native views, including the literal native H labels. Each view has 16 distinct nodes, so its ordinary scalar Vandermonde matrix is invertible over GF64 by the determinant product. For every H and each of its 36 perpendicular receivers, the three parameters are nonzero and pairwise distinct and sum to zero: all 40,320 triples pass.

The author's argument using a base plane <j,u>, the restriction of C_j to its perpendicular six-space, and the identity q0(C_j(w)>>1)=q(w) is valid. The finite checker separately authenticates its conclusion for every native chart.

## Local F4 and unitary structures

For every H=<a,b>, both C_a and C_b restrict to bijections from H-perpendicular onto the six-dimensional first-coordinate-zero output hyperplane. The physical operator

```text
(C_a restricted to H-perpendicular)^(-1) composed with C_b
```

equals one of the two supplied operators J or J^2 at every one of the 1,120 H centres. The reviewer checks the identity on all vectors. It also verifies b(x,Jx)=q(x) on all 64 vectors of each local space.

The Hermitian formula in the author prose,

```text
h(x,y) = b(x,Jy) + omega*b(x,y),
```

has the stated first-variable linearity, second-variable conjugate linearity, Hermitian symmetry and diagonal q(x), with multiplication by omega represented by J. These identities follow from J^2+J+I=0, q-invariance, and the polar identities, all already checked. As an explicit additional test, the reviewer constructs three mutually Hermitian-orthogonal vectors of norm one at every H. Their successive orthogonal complements have 16, four and one vectors, the six binary vectors e,Je,f,Jf,g,Jg span the whole local space, and all 64 coefficients have standard norm r1^3+r2^3+r3^3. Hence all 1,120 local Hermitian identifications in the final author prose are constructively verified.

In the common target coordinates, let T_H=C_b C_a^(-1). For the 40 H having any fixed global label, the unordered operator pairs {T_H,T_H^2} are all distinct. The histogram is {40:28}. Checking all six ordered bases of all H gives 6,720 basis checks and confirms that this unordered pair is basis-independent.

Here the author's phrase "up to conjugacy" must be read narrowly as interchange of the two Frobenius generators T and T^2 in the fixed common output coordinates. It does not mean arbitrary GL6 conjugacy: abstract three-dimensional F4 vector spaces are isomorphic. The verified obstruction is that a global H label alone does not select one common coordinate operator. It is not an assertion of 40 abstract field-structure isomorphism classes.

## Adversarial checks and scope

The checker explicitly rejects a wrong polar-coordinate extraction, a one-entry theta-table mutation and a one-coefficient alternating-form mutation. The base allocation review separately supplied marking mutations, complete local endomorphism-algebra checks and the no-orthogonal-spread obstruction.

Both final author prose files are bound by hash and have been reviewed for the claims above. The node assignment and the triple relation do not prove equality of the three complete inverse source fibres at a receiver. Local Desarguesian spreads, even globally marked ones, do not by themselves give compatible common H/D/K/facet maps, early owners, a complete return, or a recursive caller. The scalar-repetition obstruction is not invalidated. This review therefore admits the finite geometric identities and the displayed elementary algebraic consequences, while preserving the explicit limits recorded by the author and all five foundational obligations.
