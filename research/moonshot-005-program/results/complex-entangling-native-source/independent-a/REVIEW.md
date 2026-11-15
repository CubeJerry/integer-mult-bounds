# Independent review of the order-nine source, local conservation and entangling order-fifteen source

**PASS for both exact source/interface constructions and the scoped
conservation and nonextension theorems, with the author's positive-native
pricing scope correction. No profitable caller, supplier or new κ follows.**

Worker A reviewed the frozen Worker B package
`worker-b/complex-order-nine-source/`. Exact reviewed hashes are recorded
in MANIFEST.json. The principal proof pins are:

- order-nine source: `44bb8a9d23bff2e521dd84533a43e067c7f1959866bfd6685ca75a071d6ca170`;
- local-wreath theorem: `178a1ded27a316770bfb289e19b262628cf9cebf0dba068ff208107c3460250d`;
- pricing correction: `7502af0fe2f15d4cf4529265d1bd8a6aa66f0b5518fc630afe9268d69e87048e`;
- entangling order-fifteen source: `ffa89a5d54178633b703668161acec34e72b5a9b8f8f56c2325250c15388d355`.

## 1. Separate exact source verification

The reviewer wrote a new sparse matrix implementation over pairs of rational
numbers. It imports no author matrix or verifier code. It reconstructs the
actual computational-basis cycle, quarter phases, Gaussian heads and CZ/CNOT
monomials, verifies all pinned predecessor bytes, and checks the six nonzero
coefficient blocks for all four independent source roles at widths1 and2.
The body F acts on disjoint fresh coordinates, so the displayed head
coefficient identities tensor with its unchanged action on every body input.
No original role is specialized, identified or erased.

For the order-nine source, the reviewer verified the actual local cubic L,
B=i C_b D_b P, all three physical boundary gauges, unitarity, exact order9,
all power traces, and the literal ordinary identity

    B^-4 D_b B^3 = -i (D_b P)^-1.

Power ranks were checked twice: by exact computational support and by a
new direct conjugation calculation of the Clifford mixing block on actual
Pauli matrices. The latter gives the exact binary ranks, rather than merely
assuming that a row-support count is a Gaussian-rank certificate. The
pattern is `(0,1,2,3,3,3,3,2,1)`.

For the entangling source, the reviewer independently verified

    S=D_b CZ_ac P,
    S X_b S^-1 = X_a Z_c,
    R=C_a^-1 S C_b S = J S^2,

with the explicit ordinary controlled map
`J|a,b,c> = i^c |a+c,b,c>`. Every entry of the S,R,S^-1 permutation/phase
tables agrees with the frozen proof. The native identities use R as that
actual ordinary monomial; no Gaussian inverse service is introduced.
The common A=C_bS has exact unitary order15 and the claimed power ranks
`(0,1,2,3,3,2,3,3,3,3,2,3,3,2,1)`. Independent Pauli conjugation also gives
symplectic order15. Thus the source cannot lie in a Clifford conjugate of
the order1296 three-head local symplectic wreath group.

Six semantic controls reject dropping the order-nine scalar i, imposing a
width-independent G2 minus, moving the field-level upper-cross minus inside
the tensor, reversing D in the stated ordinary bridge, omitting the
order-fifteen controlled gauge, and treating the width-one cyclotomic
relation as a width-two identity.

The physical phase qualification is essential: one-column i,-1,-i lift
to i^V,(-1)^V,(-i)^V, while the upper source's field-level minus remains
outside the tensor. The independent width-two coefficient checks explicitly
exercise this distinction.

## 2. Universal source and cyclic claims

The order-nine trace proof is valid: the nonidentity powers have trace-1,
and the cyclic character multiplicities are positive for every V>=2.
Consequently the nine powers are independent at every such width, including
against width-dependent scalar coefficients. The width-one cyclic sum
vanishes, whereas at width two it is nine times a rank-eight projector.
The reviewer verified the projector identity and trace exactly.

For order15, the character is the product of the nontrivial-character
representations of C3 and C5. Its tensor multiplicity formula gives every
cyclic character positive multiplicity for V>=2. At width1 only primitive
fifteenth roots occur. At width2 the full cyclic sum is15 times a rank-eight
projector; the width-one cyclotomic polynomial no longer vanishes. These
character arguments establish the stated all-width facts and do not create
any free physical Fourier service.

The order-nine nonextension is correctly limited to the preceding dihedral
bimodule shadow with cyclic covariance and the designated ordinary span.
The relation transporting powers3 and4 contradicts that specific interface.
It does not prohibit another agreeing representation; the new local-wreath
proof in fact supplies one.

The order-fifteen regular-cut obstruction is also valid. Difference rank2
for shift1 forces two circular sign boundaries, hence one interval. The
rank values at shifts3 and4 force its smaller length to be3, but shift5
would then have difference rank6 rather than the actual4. This excludes
only that diagonal regular-cycle sign construction.

## 3. Independent review of local-wreath conservation

The phase-exact algebra reduction is sound under its fixed finite uniform
tensor-group hypothesis. Choose arbitrarily large tensor widths divisible
by the finite central phase order. The retained tensor-Gram theorem then
makes distinct projective group elements linearly independent. At these
widths the projective multiplication cocycle is trivial, so the actual
all-width identity transfers to the projective group algebra before the
Pauli normal subgroup is quotiented.

A physically invertible ordinary role matrix has its inverse in the same
finite ordinary algebra by Cayley-Hamilton; faithfulness transfers that
inverse identity before quotienting. Hence the two sign representations
preserve invertibility of the ordinary outside encoders. This justifies
using rank invariance under those encoders. It does not supply a free
physical inverse implementation.

On the3d local Pauli axes, the sign involution distinguishes all Z axes
from X and Y axes. Ordinary local monomials and coordinate permutations
preserve this set. A nonmonomial one-coordinate Clifford moves Z and
contributes exactly two sign crossings. Thus the two representations agree
on the whole ordinary algebra and have difference rank2r(g) for every
wreath element g.

The native square-cross calculation is valid without assuming the two
representation images commute: X²-Y²=XE+EY for E=X-Y. Explicit invertible
block row and column operations remove this upper-right block, leaving
diag(E,E), of rank4 for a rank-one native. The inverse identity preserves
that difference rank. Telescoping over an arbitrary inventory then proves

    sum(endpoint head ranks) <= 2m + sum(query ranks).

The reviewer independently enumerated all1296 three-head quotient elements,
checked the signed-axis rank formula, all48 ordinary elements, and native
oriented/inverse difference ranks for all288 rank-one elements. These are
controls on the representation, not the universal proof itself.

### Correction identified and resolved during review

The original Section4 omitted an explicit positive-native qualification.
Its strict price bounds use7m>=7 and therefore require **m>=1**. The reviewer
supplied the exact m=0 counterexample: one rank-one Gaussian query has
price=target=1, so a strict positive gap would be false there. Worker B
preserved the original proof and added the pinned `LOCAL-WREATH-SCOPE.md`.
With that supplement the strict pricing statements are correct. The
conservation inequality itself remains valid for m=0.

For m>=1, concavity gives the claimed gap because
`delta=8^t-7^t` is strictly between0 and1. For the three-head paid-query
corollary, every nonzero query rank is at most3 and
`delta < t 7^(t-1) < r^(t-1)`, making every extra query term positive.
No all-d paid-query pricing conclusion is claimed for unbounded query ranks.

The group is fixed at the one-column level. Arbitrary column-specific
operators or growing tensor families are not covered. In particular the
actual CNOT and CZ monomials send a local Pauli to a product on two axes,
so this representation does not cover them. The independent checker
verifies those literal counterexamples. The order-fifteen source is
therefore a genuine change outside the proved local-wreath obstruction.

## 4. Complete cost boundaries

Each actual forward half keeps the original Gaussian MOVE ranks1,7,8 and
one field ADD. It adds three ordinary monomial services, each implemented
by a fixed coordinate permutation and a fixed unit-phase pass. The
permutation/layout/tape costs remain explicit. Unit phases are norm-one
sign changes and real/imaginary swaps. The finite-table odometer supplies
a uniform linear combinatorial phase generator, with O(V) control storage;
it is not a proof of the retained compiler or precision foundations.

The spectator's2^V volume multiplier is retained on every source and target
array. Inverse natives retain their genuine reversed-body F^-1; converting
to a common positive F requires the previously charged ordinary translations.
No source identity supplies a Gaussian power query for free.

A separate decimal-denominator integer-root calculation confirms the full
optimistic Gaussian invoices. Three natives on three retained roles with
heads(3,2,2) have target-minus-price about0.5610073396008915; four natives
with heads(3,3,3) have positive margin about0.29002615. Every rank-seven idle
is included. The repeated cubic controls with all head ranks2 have negative
margins. Positive movement arithmetic does not construct either desired
caller and does not pay the still-open ordinary, compiler, precision,
recursive, supplier or outer BIT interfaces.

## 5. Reproduction and status

```sh
python check_source.py --repo REPO --source AUTHOR_PACKAGE
python check_wreath.py --source AUTHOR_PACKAGE
python check_budget.py
```

The reviewed results are exact source/interface constructions, universal
scoped conservation, and exact nonextension statements. The necessary next
step is an actual profitable mixed-native/interstage word for the entangling
source, followed by the complete retained admission chain. All five
foundational assumptions remain explicit. No complete conditional target
bound, unconditional multiplication theorem or new κ is claimed.

Attribution remains @CubeJerry and all credited native/source/compiler,
tensor-Gram, pentagonal and cyclic predecessors. Worker B's author credit
and AI-assistance disclosure are preserved. This review is separate
mathematical analysis with new exact implementations, not a rerun of the
author's verifier.
