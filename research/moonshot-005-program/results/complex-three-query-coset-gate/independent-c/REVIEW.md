# Independent review of the three-query coset obstruction

**Verdict: accept within the stated fixed algebra and two-role source model.**
No mathematical correction is required. The new proof closes the final
same-side three-rank-one-query inventory left by S014. Its all-inventory price
corollary applies to the fixed three-head, common-seven-body, one-native model;
it is not a general lower bound for multiplication or for every larger head
architecture. No new complete kappa or foundation discharge follows.

Reviewed author proof SHA256:

    fdb59e195d42be9c19fe326b999fdbab86bc9d9f50aea78ce32442615aabd44d

Reviewed dependency manifest SHA256:

    de0aded7e1c03a6d9492c1fe9d4fc107775769e92e38a24dec0a603414feb1ec

Worker C read the full written proof and relevant admitted source, placement,
rank-bimodule and marked-factor dependencies. Nine dependency byte strings
were freshly authenticated by both SHA256 and Git blob identity. This review
did not import or run Worker B's checker. Root's separate review is not claimed
as part of this report.

## 1. Forced intermediate and ordinary pivots

The last query can lower Gaussian rank by at most one. Removing it from an
invertible pure-rank-three endpoint forces the two-query intermediate W2 to
have no component below two. Forward degree bounds place it in F3; every
degree-three term uses the second query and therefore lies in its one affected
row. The other row R is pure E2. Since W2 is invertible as a physical 2d-by-2d
matrix, this block row has row rank d.

Let B be the E2 component. The unaffected row of the final query forces O3 B
into one output row, so rank(B)<=d. The full-rank row R gives equality. Writing
B=O3^-1 e_i U, one has R=bU with b ordinary. The ranks force b invertible.
The second row of B is then b' b^-1 R and can be removed by an ordinary row
operation. Inverse closure follows from Cayley-Hamilton in the finite unital
ordinary algebra. No assertion that this algebra is an integral domain is
used.

The same argument applies to R's ordinary coefficient of the first query's
affected row: all E2 terms after that first query occur there, and their
multiplier must have full physical rank. Thus R and the untouched first-query
row S form an ordinary invertible row basis. In that basis, the pre-second-query
ordinary matrix is block triangular. Its complementary coefficient mu is
invertible even when its other individual blocks are zero divisors.

Normalizing R by its invertible ordinary coefficient does not turn a query
unit into an arbitrary nonordinary sum. It leaves the homogeneous first-query
unit q unchanged. In the second-query forms it only right-multiplies the
ordinary coefficients lambda, nu and C. The formula with g nu explicitly
allows the retained ordinary rescaling in the shear source row.

## 2. The coset statement is stronger than rank filtration

For nonordinary projective units a and g, `gHa` is disjoint from both `gH`
and `Ha`: cancellation in either proposed intersection would put a or g in H.
Likewise H is disjoint from `Ha^-1H`, so gH is disjoint from `gHa^-1H`.
These facts hold for every group/subgroup pair. No independence of gH from
Ha is claimed; their overlap is explicitly allowed and is needed for the
first-shear normal form.

The physical inference requires faithful independence of the projective group
classes in each actual tensor-width phase sector. That is an explicit inherited
premise. Scalar cocycles change coefficients but not projective support.
Therefore a nonzero rank-one term on gH cannot be cancelled by a term supported
on the disjoint `gHa^-1H`, even if the latter also has some rank-one classes.
This is why the argument works with arbitrary ordinary zero divisors rather
than only scalar ordinary coefficients.

## 3. First-query normalization and both second-query types

For a normalized pure-E2 row `R=(q w+h)L`, expansion separates qHa support
from Ha in its first block, forcing h1=0. In the second block, qHa support is
disjoint from qH union Ha. The rank-one terms must therefore cancel as
`q w1=-h2 a`, and the exact row becomes `q w D`. This does not claim ordinary
independent-input factorization; the right factor D is nonordinary. It remains
compatible with the previously constructed nonordinary seed.

If the first query is in-place, the untouched row is `S=zL` and the ordinary
matrix O=(w;z) is invertible. Direct expansion gives the stated second block
after multiplication by D^-1 O^-1:

    B + B z1 a^-1 (O^-1)22.

A pure-E3 T can only produce ranks at least two under this right multiplication.
For an in-place second query, the first summand is invertible on gH and the
second is supported on the disjoint `gHa^-1H`. For a shear second query, the
corresponding support sets are H and `Ha^-1H`. Thus all four source/query cases
with first in-place are covered without dividing by z1 or `(O^-1)22`.

If the first query is a shear, the ordinary basis `(h;w)` is invertible and
h1=0, so h2 and w1 are invertible. After ordinary rescaling the exact rows are

    R=(a^2,a p a),  S=(a,I+p a),

with p possibly singular and noncommuting. For `T=A R+B S` and Y=T1,

    T2=Y a^-1 p a+B,
    T2 a^-1=Y a^-1 p+B a^-1.

The order of every factor is correct. Rank support forces B a^-1 into ranks
at least two. This directly contradicts a shear complement B=mu. For an
in-place complement B=g mu, expansion of Y a^-1 separates gHa from the two
rank-one supports Ha and gH, forcing `g mu=Ca`; then `B a^-1=C` is ordinary
as well as rank-at-least-two, hence zero, contradicting invertibility. The
proof does not invert p or assume that a and p commute.

## 4. Source orientations, marked factors and invoice

The exact quadratic-cross source has an F1 inverse; the ordinary-cross source
already has F1 form. Inverting an asserted caller and, when necessary,
transposing its algebra/placement are valid contradiction arguments. They
preserve query and Gaussian endpoint ranks. They do not assert that an inverse
native is a free physical operation. The previously admitted mixed-placement
gate handles the one-before/two-after and reversed cases.

The fixed marked-column extension is legitimate with matrix coefficients on
each projective bulk class. Expanding in matrix units preserves direct support
decompositions; all pivot arguments use total physical block dimension.
The source and queries must remain homogeneous nonordinary bulk units with
invertible finite-factor coefficients, exactly as stated. A width-growing
exceptional set or an arbitrary per-column ordinary algebra is outside this
reviewed theorem.

For the final three-query inventory, failure of independent (3,3) endpoints
gives total head rank at most five in the three-head model. With
`a0=8^t-7^t`, strict concavity gives 0<a0<1 and

    P=4+2*7^t+a0,
    T<=2*7^t+5*a0,
    P-T>=4*(1-a0)>0.

This is strict throughout 0<t<1. The earlier pinned inventory exhaustion covers
the remaining query counts/ranks, so the complete optimistic movement invoice
fails for every inventory in that fixed model. Added ordinary, compiler,
ownership, tape, precision and recursive services cannot improve this bound.
The algebraic theorem permits any fixed head count but only the claimed
pure-E3 endpoint; it does not by itself close a new four-head endpoint design.

## 5. Independent controls actually executed

`check_independent.py` is a separate implementation using Python and SymPy
1.14.0. It authenticates the nine dependency files and checks:

- all 82 nonordinary (a,g) cases across the six subgroups of S3 for the general
  coset-disjointness identities, while retaining 62 allowed gH/Ha overlaps;
- exact noncommutative row identities with an invertible rational a and a
  singular p that does not commute with it;
- an invertible ordinary 2-by-2 block boundary whose four individual blocks
  are all singular, verifying the common-right-factor identities without
  accidental block divisions;
- the full-rank pivot and component-separation identity.

The S3 checks illustrate group-support facts; S3 is not substituted for the
actual Clifford source. The rational 2-by-2 controls check identities and
zero-divisor hazards; no Gaussian grading is inferred from them. Mutating the
noncommutative factor order, correction order, full-rank pivot, or the
nonordinary-unit premise is detected. These finite checks supplement the
written universal proof and are not an exhaustive circuit search.

Reproduce:

```sh
python3 -B check_independent.py --repo /absolute/path/to/integer-mult-bounds --package /absolute/path/to/complex-three-query-coset-gate
```

Expected status: `PASS_INDEPENDENT_THREE_QUERY_COSET_CONTROLS`.
This is independent Worker C mathematical review and independent code, not
repeat execution of the author's verifier. @CubeJerry and all predecessor
authors retain credit; substantial OpenAI assistance. No new kappa.
