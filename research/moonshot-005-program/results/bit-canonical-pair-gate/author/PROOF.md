# A universal canonical pair gate below two block widths

Status: **proved for the pinned native 111-port BIT instance**, subject only to
the explicitly reproduced finite geometric premises below. This is a scoped
source obstruction, not a new integer multiplication bound. **No new κ.**

## 1. Statement and precise scope

Let `k` be any field of characteristic two and let `V >= 1`. Normalize the 111
native real root lines to vectors `r_i` of squared length four. Put

\[
 K_{ii}=1,\qquad K_{ij}=\mathbf1_{r_i\perp r_j}\quad(i\ne j),
 \qquad C=\operatorname{row}_k K\subseteq k^{111}.
\]

Write `J_i = supp K_i`, `Z_i = {0,...,110} \ J_i`, and `F_i = r_i^perp`.
A block fitting is a matrix `A=(A_ij)` with `V` by `V` blocks satisfying
`A_ii=I_V` and `A_ij=0` whenever `K_ij=0`. Its foreign support at row `i` is
the set of real source lines `r_j`, `j != i`, for which `A_ij != 0`.
Give this support charge zero when it fits in one proper linear subspace of
`F_i` (including the empty support); charge one when two proper subspaces
suffice but one does not; and charge two otherwise. Denote these charges
by `chi_i` and their sum by `chi(A)`.

Define the **canonical enlargement quotient**

\[
 E=\frac{\operatorname{row}_k A+(C\otimes k^V)}{C\otimes k^V},
 \qquad d=\dim_k E.
\]

**Theorem.** If `d < 2V`, then

\[
 \boxed{\chi(A)\ge165.}
\]

There is no restriction on the coefficient field beyond characteristic two,
on `V`, on the scalar reservoir, on commutativity of block coefficients, or
on the existence of pure tensors. In particular this theorem is not confined
to the quadratic or cubic Schur powers of the canonical code.

The statement concerns a fitting and its explicit canonical enlargement. It
does not identify `d` with `rank(A)-9V` when the row space of `A` does not
contain `C tensor k^V`. It also does not claim that every chronological
source has such a low-dimensional enlargement.

## 2. Exact native geometric premises

The source is
`research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz`,
SHA256
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
The author checker reconstructs all roots and all incidences from this file.
Its checks are finite exact premises for the universal argument, rather than
an experimental extrapolation.

1. `dim C = 9`; for every `i`, restriction `C -> k^{Z_i}` has rank eight.
   Thus `C cap k^{J_i} = k K_i`.
2. For every pair of distinct indices `i,j`, restriction
   `C -> k^{Z_i cap Z_j}` has rank seven. Its two-dimensional kernel is
   exactly `span(K_i,K_j)`, since these two independent rows belong to it.
3. Every canonical foreign support has quadratic evaluation rank 28 in the
   28-dimensional space of real quadratic forms on `F_i`. In particular it
   cannot be covered by two proper real subspaces, and has charge two.
4. For every ordered nonorthogonal pair `i,j`, the exclusive support
   `X_ij = {l != i : K_il=1, K_jl=0}` spans all of `F_i` over the reals.
   This is checked for all 5,740 ordered pairs.
5. There are 55 vertex-disjoint nonorthogonal pairs. On at least one end of
   every pair, `X_ij` has 27 points and its quadratic evaluation rank is 27.
   The 55 pairs and a certified orientation are recorded in `RESULT.json`.
6. If `r_i` and `r_j` are orthogonal, there are at most 30 other native roots
   orthogonal to both. Equivalently, `|J_i cap J_j| <= 32`.

Binary ranks in items 1 and 2 persist under every characteristic-two field
extension. The real ranks in items 3--5 are certified from nonzero minors
modulo the prime 101, together with their geometric upper bounds. Their
interpretation does not depend on the coefficient field of the fitting.

For clarity, item 5 implies that the indicated exclusive support cannot be
covered by two proper subspaces. Put `p=r_i`, `q=r_j`; then
`||p||^2=||q||^2=4` and `p.q=+/-2`. On the exclusive roots `v in F_i`,

\[
 Q(v)=\|v\|^2-(q\cdot v)^2=0.
\]

The projection `a` of `q` onto `F_i` has squared length
`4-(p.q)^2/4=3`. Therefore `Q` on `F_i` has symmetric matrix
`I-aa^T`, of rank seven: its eigenvalues are six copies of 1 and one copy
of -2. The evaluation rank 27 makes its kernel exactly the line generated
by this quadratic form. If two proper subspaces covered the 27 roots,
enlarging each to a hyperplane would give a nonzero product of two linear
forms vanishing on the support. Such a product has matrix rank at most two,
and cannot be a multiple of `Q`. This is a contradiction.

Not every nonorthogonal pair satisfies item 5. For example the punctured
exclusive sets for the actual pivot pair 92,54 are smaller. The proof uses
the certified matching, not an untrue assertion about all pairs.

## 3. Each positive-saving row supplies a V-plane in E

Let `P={i : chi_i<2}`, and for each `i` let `E_i` be the image in `E` of
the block row space of `A_i`. Every `i in P` deletes at least one canonical
foreign contact: otherwise its foreign support contains the whole canonical
support and, by item 3 and monotonicity of covering, would have charge two.

For a row coefficient `a in k^{1 by V}`, suppose `[a A_i]=0` in `E`.
Then `a A_i` is canonical and supported in `J_i`. Applying item 1 separately
to each of its `V` coefficient columns yields

\[
 aA_i=K_i\otimes a.
\]

The coefficient is `a` because the own block of `A_i` is the identity.
At a deleted canonical foreign contact, the left side is zero and the right
side is `a`, so `a=0`. Thus the map `a -> [a A_i]` is injective and

\[
 \dim E_i=V\quad(i\in P).
\]

Consequently `d<2V` forces `E_i cap E_j != {0}` for every distinct pair of
positive-saving rows. This is the only dimensional forcing step.

## 4. Canonical pair gluing forces exclusive contacts

Take nonorthogonal `i,j in P` and a nonzero common quotient vector. There
are nonzero row coefficients `a,b` such that `[a A_i]=[b A_j]`. Since the
field has characteristic two,

\[
 a A_i+b A_j\in C\otimes k^V.
\]

The vector is supported in `J_i union J_j`. Item 2 gives unique vectors
`u,v in k^{1 by V}` with

\[
 a A_i+b A_j=K_i\otimes u+K_j\otimes v.
\]

Nonorthogonality means `K_ij=K_ji=0` and the fitting cross blocks vanish.
The own positions `i` and `j` therefore force `u=a` and `v=b`. Hence

\[
 a(A_i-K_iI_V)=b(A_j-K_jI_V).
\]

This common literal representative is supported in `J_i cap J_j`.
At every `l in X_ij`, it follows that `a A_il=a`, which is nonzero.
Thus `A_il` itself is nonzero. In particular the entire exclusive support
`X_ij` is contained in row `i`'s foreign support. This inference uses
neither a scalar factorization of `A_il` nor invertibility of that block.

Two consequences follow.

* On every certified matching edge, its two ends cannot both belong to `P`:
  the end with the irreducible 27-point exclusive support would then have
  charge two. Thus `p=|P| <= 111-55=56`.
* If `chi_i=0`, every other positive-saving root `r_j` is orthogonal to
  `r_i`. Otherwise item 4 forces a full-dimensional exclusive support into
  a single proper subspace of `F_i`.

## 5. Total saving is at most 57

Let `z=|{i:chi_i=0}|` and let `S=222-chi(A)` be the saving from the
canonical charge. Since each positive row saves one, and each zero-charge
row saves one additional unit,

\[
 S=p+z.
\]

If `z=0`, then `S<=56`; if `z=1`, then `S<=57`. If `z>=2`, choose two
zero-charge roots. They are mutually orthogonal, and every other positive
root is orthogonal to both. Item 6 implies `p<=32`. The zero-charge roots
are mutually orthogonal nonzero vectors in `R^8`, so `z<=8`. Hence this
case has `S<=40`. In every case `S<=57`, proving `chi(A)>=165`.

The inequality is deliberately not asserted to be sharp. No fitting
attaining 165 is supplied.

## 6. Consequences for the marked route and exact limitations

The programme's current completed marked-route arithmetic requires
`chi<=138` for eight full Hub-to-ground portions, and `chi<=131` for nine.
Both lie below 165. Thus under that route/accounting interface any candidate
whose canonical enlargement has `d<2V` is excluded, regardless of field,
block width, or polynomial degree of its scalar modes.

In particular a width-two three-dimensional quotient cannot meet either
marked cap, including the previously first-unexcluded pure four-direction
chain over F16. This strengthens the older coarse `chi<=194` classification
in the target-relevant direction. It does not contradict that classification:
165 alone does not exclude the coarse cap 194.

The first dimensional boundary left open is `d>=2V`. Already in dimension
`2V`, two `V`-planes can be disjoint, so the forcing in section 3 fails.
This is a boundary of the proof, not an existence theorem for native codes.
The current scalar point-punctured pivot fitting has raw rank 17 but
canonical enlargement rank 18; its enlargement quotient is nine, so it
lies outside the hypothesis even at scalar width. No obstruction to its
actual recorded chronological prefix is claimed here.

There are no physical operations, decoder, precision guarantees, ownership
implementation, recursive compiler, or supplier in this result. It changes
the admissible research search space. It does not establish a multiplication
algorithm or remove the programme's foundational assumptions.

## 7. Verification and provenance

The native source, the definition of the canonical enlargement, and the
proper-cover accounting are inherited from the persistent programme. The
coefficient-wise canonical support argument extends the local rigidity
used in `results/bit-operator-canonical-quotient/author/PROOF.md`. The
quadratic rank-seven exclusive-support argument is the same real geometric
mechanism established for the eight difficult rows in
`results/bit-pivot-filter-geometry/author/PROOF.md`, now applied to a
55-edge matching. The new result is the unrestricted pair-gluing theorem
and its all-width, all-characteristic-two-field saving bound.

`check.py` credits and imports only the root normalization and elementary
exact algebra helpers from the author checker for the quadratic/exterior
package. It does not import the independent root review. The independent
review reconstructs the source separately and uses prime 103 rather than
101. The author and independent checks are distinct finite verifications;
the all-width argument is sections 3--5, not a finite replay.

Reproduce from this directory, replacing the repository path as needed:

```sh
python check.py --repo /path/to/integer-mult-bounds --geometry-check /path/to/bit-quadratic-exterior/author/check.py --output RESULT.json
python -O check.py --repo /path/to/integer-mult-bounds --geometry-check /path/to/bit-quadratic-exterior/author/check.py --output RESULT.optimized.json
```

Expected status: `PASS_AUTHOR_UNIVERSAL_CANONICAL_PAIR_GATE`. All checks use
explicit exceptions, not removable Python assertions. Negative controls
include an overlapping-edge pseudo-matching and the strict `d=2V`
linear-algebra boundary. All source-specific contributions are part of the
shared @CubeJerry persistent programme, with AI assistance; prior credited
packages retain their attribution.
