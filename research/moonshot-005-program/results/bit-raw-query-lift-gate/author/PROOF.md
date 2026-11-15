# A same-quotient obstruction for arbitrary Hub seed lifts

**Proved source-specific algebraic obstruction; independent review pending.
No new κ.** This strengthens the preliminary W-contained-seed screen:
arbitrary D offsets in the seven Hub seeds are explicitly allowed and
fully represented. The result does not exclude new partial-cache exports,
changed source acquisition, an additional independent seed direction,
or genuinely new feedback information.

## Source spaces and generous information grant

Fix the authenticated native111 geometry and the actual delayed h9 source.
Let D be the span of its80 actual colored-cache rows, and W the native h9
fitting row space. Exact ranks are

    dim D=40, dim W=15, dim(D+W)=47, dim(D∩W)=8.

Let N be the actual P0 terminal, k0 its actual A15 incoming mixed row, and
R_q the sum of all actual colored cache reads in query q, for q=0,...,7.
Give the decoder all these fields globally for free, together with the
full axis sum a=e0+...+e7. Write

    B=span(N,k0,a,R0,...,R7).

This is an intentionally stronger grant than two paid first-facet raw-suffix
exports. All these rows lie in D and dim B=11. No physical delivery is
asserted for the grant; impossibility under it implies impossibility for any
model whose globally normalized extra information is a subspace of B.

The seven free Hub seed rows need not lie in W. More generally, over any
characteristic-two field k and positive whole-record width V, let S be any
subspace of k^(111V) such that

    dim S≤7V,  W⊗k^V ⊂ (D⊗k^V)+S.

This is exactly the minimal seven-direction history-acquisition requirement.
It implies

    S⊂(D+W)⊗k^V,  S∩(D⊗k^V)=0,  dim S=7V.

Indeed projection modulo D must contain the entire7V-dimensional W quotient;
the domain has dimension at most7V. Hence it is an isomorphism onto that
quotient. Every allowed D-offset lift is included.

For receiver i, let L_i be the coordinate span of all e_j with r_j⊥r_i.
A complete fitting would require, for each u∈k^V,

    e_i⊗u ∈ S+(B⊗k^V)+(L_i⊗k^V).

Arbitrary local side information and arbitrary block linear coding are thus
allowed. This is a generous necessary algebraic interface, not a proposed
physical decoder.

## Same-quotient lemma

Put A=D+W. Suppose two receivers i,j satisfy

    A∩L_i⊂D,  A∩L_j⊂D,  W_i+W_j∈D,

and a binary functional z satisfies

    z|B=0, z|L_i=0, z|L_j=0, z(e_i+e_j)=1.

Then the above complete fitting is impossible for every allowed S, field k,
and whole-record width V.

To prove this, assume fitting vectors f_i=e_i⊗u+ell_i and
f_j=e_j⊗u+ell_j lie in S+B⊗k^V, for any nonzero u. Because W_i and W_j are
native fitting rows, f_i+W_i⊗u and f_j+W_j⊗u lie in A⊗k^V intersected with
the respective local coordinate spaces. The first two hypotheses put these
differences in D⊗k^V. The third hypothesis therefore gives equal quotient
images of f_i and f_j modulo D. Projection is injective on S, and B⊂D,
so their S components agree. Consequently f_i+f_j lies in B⊗k^V. Applying
z⊗identity gives0 on that space but u on the displayed fitting expressions,
a contradiction. No assumption that S⊂W was made.

All intersections and ranks of the fixed binary spaces commute with
extension to characteristic-two fields and tensoring with k^V. Thus the
lemma is an all-block statement, rather than an extrapolated scalar search.

## Two exact native witnesses

The source has the following independently checkable binary witnesses:

| Receivers | A/local intersection dimensions | Functional support |
|---|---:|---|
| 8,11 | 15,16 | {8,37,78} |
| 22,23 | 16,13 | {22,33,61} |

For each receiver in either pair, the listed A/local dimension equals its
D/local dimension. Exact elimination verifies W8+W11∈D and W22+W23∈D.
Each three-coordinate functional is zero on B and on both local spaces,
but its value on the difference of the two demands is1. Either pair alone
proves the claimed obstruction. The complete certificate contains source
pins, actual B rows, dual supports and all asserted ranks.

This excludes raw whole-query-sum exports as a complete repair of the
minimal seven-seed source, even when every raw query, the mixed k0 row and
the entire axis bank are granted globally without cost. It does not exclude
exporting a different, informative partial color sum. For example, the
actual mixed class-zero kernels k_j=e_j+R_j,class0 have nonzero pairing with
both displayed duals for j∈{2,3,6,7}; these are genuine ways to leave this
specific information class, subject to acquisition, storage, chronology,
remaining receivers and full cost accounting.

## Verification and controls

```sh
python3 -B check.py \
  --repo /absolute/path/to/integer-mult-bounds \
  --source /absolute/path/to/delayed-correction-source/output/WORD.json
```

Expected status: `PASS_ARBITRARY_LIFT_RAW_QUERY_GATE`. The checker authenticates
the exact native geometry and source word, replays all222 coefficients to
verify its recorded cache/terminal values, reconstructs W from native
orthogonality, and checks both exact rank/intersection/dual certificates.
Granting all15 W directions is a positive control and fits all111 receivers;
granting the demanded point e8 or e22 breaks its corresponding dual. These
show why the seed-dimension and information-space restrictions matter.

Credit @CubeJerry; the source, normalization and quotient-interface authors;
root for identifying and insisting on arbitrary seed-lift scope; Worker A
for the same-quotient reduction and exact witnesses. Substantial OpenAI
assistance. No supplier or foundational assumption is discharged.
