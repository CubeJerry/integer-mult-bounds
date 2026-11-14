# Two scalar patch directions have indivisible whole-width saving thresholds

**Author source-specific theorem; independent review pending. No new physical
decoder, supplier, foundational discharge, or complete kappa.**

The proposed width-two, three-dimensional quotient escape fails for this
entire frozen two-patch family. The obstruction is uniform in field and
block width; the exact fifteen-hyperplane calculation is a separate check.
It does not exclude a different quotient geometry or a general irreducible
operator code.

## 1. Exact family and theorem

Use the actual 111-port BIT canonical binary fitting `K` and its scalar
nine-dimensional row code `C`. Work over any characteristic-two field `k`
and any positive integer width `V`. Set

    S1={2,9,12,30,38,42},
    S2={2,26,63,65,81,87},
    h1=1_S1, h2=1_S2,
    D=span_k(h1+C,h2+C) <= k^111/C.

The two quotient directions are independent. Write `C_V=C tensor k^V`
and identify `D_V=D tensor k^V` with the canonical quotient of
`(C+span(h1,h2)) tensor k^V`. Let `E` be ANY linear subspace of `D_V`,
not necessarily a tensor product or a commuting-operator space. A fitting
is permitted when its row space lies in the preimage of `E`, its diagonal
blocks are identity, and its prescribed noncontact blocks are zero.

Define the three whole-width scalar-line subspaces

    L1=span(h1+C) tensor k^V,
    L2=span(h2+C) tensor k^V,
    L3=span(h1+h2+C) tensor k^V.

Any two of them sum directly to `D_V`. Thus a proper `E<D_V` contains at
most one of these three subspaces.

**Theorem (exact permitted-space minimum).** The least possible value of
`sum_i ell_i(A)`, where

    ell_i(A)=1[foreign block support>36]+1[foreign block support>52],

is exactly:

| Whole-width subspaces contained in E | Minimum ell |
|---|---:|
| None of L1,L2,L3 | 222 |
| L1 only, or L2 only | 205 |
| L3 only | 216 |
| At least two, equivalently E=D_V | 192 |

“Only” refers to these three named subspaces, not to all possible scalar
lines over a larger field. Arbitrary extra entangled directions in `E`
do not change these minima. Attainment is over the permitted code space;
an attaining fitting need not use every available direction of `E`.

In particular, every fitting whose actual canonical quotient is a proper
subspace of `D_V` satisfies `ell>=205`. Any fitting in this family meeting
the retained all-route target cap `ell<=194` must use the full `2V`
canonical quotient. No fractional compression of these two fixed patches
can meet the target, even with noncommuting and singular matrix blocks.

## 2. Independently checkable native availability census

For receiver `i`, let `Z_i={j:K_ij=0}` and define its scalar available
quotient subspace

    P_i={a h1+b h2+C : (a h1+b h2)|Z_i belongs C|Z_i} <= D.

The own-coordinate condition does not affect quotient availability because
`K_i` is supported on the closed contact set and has own coordinate one.
The native single restriction has rank eight; its canonical kernel is
`span(K_i)`. Exact binary restriction ranks give the following census:

| P_i | Receiver count |
|---|---:|
| 0 | 77 |
| span(h1+C) | 14 |
| span(h2+C) | 14 |
| span(h1+h2+C) | 0 |
| D | 6 |

The six doubly available receivers are

    J={33,57,68,79,102,106}.

Let `U1` consist of the first-line and doubly available receivers, and
define `U2` similarly. Both have twenty members. The exact native check
also establishes:

1. `Ua` is precisely the receiver set real-orthogonal to every source in
   `Sa`. In particular every such receiver is outside `Sa`, and the pure
   representative `ha` itself has zero own and forbidden coefficients.
2. Of the fourteen receivers in `U1 minus J`, exactly twelve have canonical
   foreign degree at most 58. The same is true of `U2 minus J`.
3. The degrees of the six receivers in the displayed order of `J` are
   `60,58,58,58,58,58`.
4. `|S1 minus S2|=|S2 minus S1|=5` and `S1 intersect S2={2}`.
5. Every native canonical foreign degree is at least 55.

These are fixed finite source facts, checked directly from authenticated
rational root coordinates. The availability subspaces are kernels of
binary linear maps. Their ranks, basis directions, and all displayed
kernel/intersection identities persist over every characteristic-two
extension field. No coefficient-field search is extrapolated here.

## 3. Every saving row injects its full value width

For a fitting `A`, the map

    phi_i : u -> u A_i+C_V

has image in `E intersect (P_i tensor k^V)`. The tensor statement follows
entrywise from the defining binary forbidden restriction equations; it does
not require `E` itself to be a tensor product.

If `u` lies in the kernel, then `u A_i` is canonical and vanishes on `Z_i`.
The canonical restriction kernel gives `u A_ij=K_ij v`. The identity
diagonal forces `v=u`. If the row has any erased canonical contact block,
that block forces `u=0`. Thus every saving row has an injective map of its
whole `V`-dimensional value space into the canonical quotient.

Consequently a receiver with `P_i=0` cannot save. At a receiver with
one-dimensional `P_i=span(ha+C)`, any saving forces the image of `phi_i`
to be the ENTIRE `La`, and therefore `La<=E`. Because `ha` itself is local
and has zero own coordinate at such a receiver, its canonical part is
`K_i tensor I`. It can erase at most the six contacts in `Sa` and never
reach foreign support at most 36. It saves at most one, and can save only
when its canonical degree is at most 58. Hence the first-only and
second-only receiver groups contribute at most twelve savings each, and
only when their corresponding whole-width subspace is contained in `E`.

## 4. Doubly available rows force one of three full scalar lines

For `i in J`, both pure patch representatives are local and have own
coefficient zero. The canonical restriction and diagonal therefore force
the exact operator formula

    A_ij = K_ij I + (h1)_j M1 + (h2)_j M2,

with arbitrary `V` by `V` matrices `M1,M2`, in the stated order. Outside
`S1 union S2` all canonical blocks survive. At most eleven contacts can
disappear, so the foreign support is at least `55-11=44`. Thus each such
row can save at most one.

The blocks at the three disjoint patch regions vanish precisely as follows:

| Region | Number of contacts | Zero-block condition |
|---|---:|---|
| S1 minus S2 | 5 | M1=I |
| S2 minus S1 | 5 | M2=I |
| S1 intersect S2 | 1 | M1+M2=I |

All six receivers have degree at least 58, so a saving requires at least
six whole blocks to disappear. One region has at most five contacts; at
least two of the three zero conditions must hold. The possibilities are:

- `M1=I,M2=0`: the quotient-row image is exactly `L1`, and six contacts
  disappear. Only the five degree-58 receivers in `J` save.
- `M1=0,M2=I`: the image is exactly `L2`, with the same five savings.
- `M1=I,M2=I`: the image is exactly `L3`, and ten contacts disappear.
  All six receivers save.

The three conditions cannot hold simultaneously. No commutation or matrix
inverse has been used. In particular a rank-deficient or entangled partial
combination of the two scalar modes cannot create a different saving case.
Every actual saving again forces a complete named width-`V` subspace into E.

## 5. Exact totals and sharpness

If `E` contains no named full line, no receiver saves and `ell=222`.
If proper `E` contains `L1`, it contains neither `L2` nor `L3`; the total
savings are at most twelve first-only plus five doubly available, namely
seventeen. The standard first patch attains all seventeen. The second-patch
case is identical. If proper `E` contains only `L3`, exactly the six doubly
available receivers can save; using `h1+h2` there attains all six.

If `E=D_V`, at most twelve first-only, twelve second-only, and six doubly
available receivers save: thirty in total. The following binary scalar
fitting attains all thirty:

    K_i+h1       on eligible U1 minus J;
    K_i+h2       on eligible U2 minus J;
    K_i+h1+h2    on J;
    K_i          elsewhere.

It has `ell=192`, rank eleven, and canonical quotient dimension two. Those
binary rank identities are exactly checked and persist after scalar
extension. Its identity tensor lift attains the stated minimum at every
width, with quotient dimension `2V`. These algebraic attainments establish
the exact table, not any physical route or decoder.

The union support has eleven ports, twelve if the retained pivot coordinate
is added. The separately proved point-retained handoff gate still excludes
static monotone point-only continuation in that supported space. The
full-width algebraic code is therefore a boundary control, not a completed
target construction.

## 6. Exhaustive binary width-two check and its scope

For `V=2`, `D_V` has dimension four over F2 and has exactly fifteen
hyperplanes. The checker enumerates their nonzero defining normals, builds
each three-row quotient basis, and adds the eighteen canonical tensor rows.
At each receiver it computes the exact code kernel on the forbidden blocks,
then all affine rows with each required identity-diagonal value. It enumerates
every pair of these two normalized output rows and minimizes foreign whole-
block support. Different receiver rows have no further algebraic coupling
constraint in a fixed code space, so the sum of row minima is the exact
minimum `ell` in that code space.

The exact optimum census is:

| Hyperplane type | Number | Minimum ell |
|---|---:|---:|
| Contains L1 or L2 | 6 | 205 |
| Contains L3 only | 3 | 216 |
| Contains none | 6 | 222 |

The unrestricted four-dimensional quotient attains 192, and the two-
dimensional first-line quotient attains 205. These are meaningful controls
against broadening the proper-subspace obstruction to all of `D_V` or
raising its universal 205 threshold. The saved row witnesses and every
per-receiver affine enumeration size make the finite calculation auditable.

The all-field/all-width proof is Sections 2–5. The fifteen-case computation
alone would not justify those quantifiers, and no such extrapolation is made.

## 7. Consequence and next question

This retires compression of these two fixed scalar patches as a candidate
for a sub-double-width canonical quotient. A next operator construction
needs a different availability arrangement: more genuinely multidimensional
receiver availability, patch-region sizes that permit partial operator
coupling to delete enough whole blocks, or a new quotient geometry beyond
this fixed tensor span. Adding notation or searching more matrix coefficients
inside the excluded family cannot help.

No complete native chronology, public/owned route invoice, cover/compiler,
ordinary supplier, compatible complex supplier, precision/erasure service,
or foundational assumption is established. No new kappa.

Prepared for @CubeJerry with OpenAI assistance. Credit the canonical/native
source, the scalar seventeen-savings patches, the companion quotient-
injection work, the invariant-filtration construction/control, and the
point-retained handoff theorem. This contribution is the exact native
availability classification, full-width saving threshold, and independently
reviewable finite hyperplane census. No human or formal-kernel acceptance
is represented.
