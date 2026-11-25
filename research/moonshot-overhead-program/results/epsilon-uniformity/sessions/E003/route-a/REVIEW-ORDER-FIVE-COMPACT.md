# Independent review of the compact order-five substitution

Reviewer: E003 Route A. Result: **pass for the stated finite construction
and component transfer**. This is independent AI-assisted written review
and an isolated finite replay. It is not a full fixed-tape execution,
formal proof, human refereeing, or a stronger multiplication envelope.

## Exact objects and scope

Read in full Route C's:

* `ORDER-FIVE-COMPACT-SUBSTITUTION.md`, SHA-256
  `ac252bac2ac832c70cf1d9a6fb21913ad817c365bd161c57645978929d59442c`;
* `ORDER-FIVE-ONE-TRANSFORM-CONVERTER.md`, SHA-256
  `87715da425476902ca099f434d2122c813150f6832ba9d35f21045616ad70d0e`.

Also read root's `order-five-word-classification.md` and compared the
substitution with the actual E002 cyclic, small-check and spectral
processors and E003 A's guarded/constant-array, comparison and full-rate
packing statements. The primary source interfaces are the paid shared
pencil and spectral converters of OpenAI tape `interchange.tex` at
`math@3344da59991ed94f9ba711217b29c1d760badfa6`. Those source portions
were read directly in this session.

The previous copied count-formula/factorization theorem is an identified
import. This review checks that the different digit alphabet and constant
field satisfy its explicit input and degree-budget interface; it does
not claim a new independent proof of that entire predecessor theorem.

## 1. Field, spectrum and converter words

The polynomial `X^4+X+1` has no binary root and is not divisible by the
only irreducible binary quadratic, so the specified quotient is F16.
The displayed C has distinct reciprocal eigenvalues zeta,zeta^-1 of
order five. Direct field multiplication gives the diagonal-equivalent
eigenbasis and the two-power swap word. Root's cross-ratio classification
also reproduces this gate inside its precisely restricted symmetric
two-by-two word model.

All local operators are defined as the identity on equal-field fixed
points. This is necessary and is included: an arbitrary pair diagonal
on such a point would otherwise alter the target. On nontrivial
smaller/larger orbits the spectral labels are 1 and 4; fixed points
have label zero. For F_r those exponents are multiplied by r. The same
eigenbasis diagonalizes every C^r, so converter children F4/F1 are
correct even when the parent's target is F2.

The forward spectral converter is `Delta_B^-1 F4 Delta_A^-1`, and
the inverse is `Delta_A F1 Delta_B`. Each contains one complete target
transform. The final ordinary swap product uses F1 and F2 successively.
The closed target family `{F1,F2,F4}` is therefore sufficient. There is
no same-size recursive cycle: finite-repair height decreases at every
such converter call, and depth-zero leaves use direct ordinary swaps.

For every nonzero power r, the two off-diagonal entries of C^r coincide.
Thus the four power terms can be collected into one shared Q_j pencil
per original query index j. The remaining diagonal masks are applied in
ordinary physical order. Their number is a fixed factor four, not a
new factor multiplying the recursive shared-pencil invoice or its
rank guard. Pointwise row matrices commute with these address masks
because they act on a different coordinate; no spectral mask is moved
through an unperformed converter.

## 2. Predictor values and the small check map

For any integer a, including negative a, reduction modulo X^T gives
`(1+X)^a=(1+X)^(a mod T)` when T is a power of two in characteristic
two. The right-hand side has degree less than T. Consequently the
finite predictor polynomial has the claimed value

```
p_beta=zeta^(u-sum beta+((c_beta-u) mod T)).
```

No infinite series is evaluated at a field element. Division of
`c_beta-u` by T yields the stated ratio to the target z, so predictor
values and every actual gap lie in F16 even when check nodes lie in
the larger field E.

The correction exponent 14 is valid for exactly this reason. For a
nonzero gap g in F16, `g^15=1` and `g^14 g=1`. For a zero gap the
error is already zero and the formula uses no inverse. The containing
outside-window set may therefore include accidental zero-gap rows.
The two successive Vandermonde solves have the required inverse and
transpose-inverse order. After lifting, the output error is
`(p_beta-z)(Xhat_beta-Zhat_beta)` and vanishes on every row.

There are O(m) shift seeds. Their projective normals are nonproportional,
so every two forms are jointly uniform over F5; translation by an
arbitrary spectral tuple preserves that fact. The mean and variance
are 2m and 2m. With the chosen window the exceptional fraction is at
most 1/18, hence its integer size is at most `floor(B0/16)`. This
holds without an additional large-B0 rounding assumption.

`E=F_(16^e)`, `e=ceil(log_16 B0)`, supplies B0 distinct nodes.
Enumerating its monic degree-e polynomials and possible factors is
polynomial in B0, because `16^e<=16 B0`; exact field arithmetic and
sequential Gaussian elimination remain polynomial in m. There is no
5^m lookup in the compact runtime.

## 3. Formula and module applicability

Each of the three Boolean input bits for a digit in `{0,...,4}` is an
affine combination of its five spectral indicators, hence of the four
nonconstant query powers and the constant. The assigned degree budgets
1,2,4 dominate these affine degrees. The predecessor's weighted carry
induction therefore applies with a constant number of input bits per
digit. It supplies the same polynomial copied-formula size and the
required count-bit degree budgets.

For `D=T-1`, the product of the t factors
`1+(zeta-1)^(2^i) B_i` evaluates the truncated predictor. Its total
factor length is `sum_(i<t) 2^i=T-1`; no top-level sum of non-power-of-two
budget is introduced. Every cyclic sum still has a power-of-two length,
so its characteristic-two twist is one. The full module dimension may
be exponential, but its logarithm and the copied formula are polynomial
in m.

Keeping the same syntax, budgets, zero leaves and module coordinates
for every shift and target power is explicitly required. Otherwise
target-dependent pruning could invalidate canonical finite-child
regrouping. The note preserves this condition.

E002 C3--C5 apply over any fixed characteristic-two base field. Replacing
F4 by F16 changes only a constant-sized scalar table and the fixed
number of affine leaf terms. The masked translations, input-grade
guards, row layout, one-term scratch and accumulator are unchanged.
Multiplication by a base F16 coefficient is coordinatewise in E;
general E operations remain separately charged in the check map.

## 4. Occupied rows, fields and physical storage

The genuine checks occupy `16 floor(B0/16) w` rows. Padding them to
`s=B0 w` is paid internal workspace, so the two-check phase has exactly
`2s=R/8` rows. The unused check coordinates return zero. The finite child
algorithm remains correct for arbitrary input rows, even when a particular
call happens to contain these known internal zeros; no volume is removed
because a value is zero.

Eight parent copies times two check halves form the 16 duplicate roles
of one canonical child batch. The bijection preserves the label and
the entire module coordinate. It neither drops independent coordinates
nor embeds them with an unpaid coefficient-degree multiplier.

There are two sequential children of fraction 1/8, so the total finite
child mass is 1/4. This yields O5-11, and the two final target words
give O5-12. The old leading padding, spatial reserves and source label
factor still have to be paid, as the note says. The shorter converter
does not remove that label overhead.

All compact operations fall within the specified absolute-array
suppliers. Comparison labels use one current tuple, the shared pencil
uses its rank-volume budget, and role/check operations are serialized.
The complete spatial suffix pays any permitted row headers. Finite
children contract and reserve children clear parent payload before
descent. Parameters and fields change only for **completed spatial
permutations**; each F_r finite-repair word keeps its local E and
template. Full-rate binary descent is valid only after the final Q
word has become the ordinary permutation with F2 coefficients.

This establishes the compact component statement under exactly its
named predecessor contracts. It does not authorize replacing the
numerical rational Walsh branch by F16 arithmetic.

## 5. Independent finite replay and conclusion

Copied the exact Route C checker into `order-five-review-replay/` and ran

```
python3 -B research/moonshot-overhead-program/results/epsilon-uniformity/sessions/E003/route-a/order-five-review-replay/verify_order_five_converter.py
```

The copied script hash is
`bdaafe102358aca9f921a4a3455835c50c4ae527f069094b8726975acc16853d`;
the independently generated receipt hash is
`3f7e6cfc4fe1e11b96b96e2651cfb73c6c26db939fa71ed31b8789b813912cbd`.
It passed the four shared-swap decompositions, tensor words through
three physical pairs, 653 pairwise-shift pairs, 18 exact moment cases,
46,875 spectral values, 375 invertible minors, 750 complete discrepancy
repairs and 12 occupied regroupings. It rejected 162 old-order-three
one-gate candidates and 417 omitted-lift controls.

The toy repair has marked fraction 14/125 and child mass 56/125. It
does not numerically certify the asymptotic 1/16 choice; that choice
is established by the separate variance/window proof above. Neither
the checker nor this review is a full physical machine execution.

No blocking defect was found. The compact substitution passes as a
bounded useful new local mechanism with exactly the scope claimed.
Its current profile consequence is an improved finite word and batch
overhead, with the same asymptotic label loss. A stronger whole-input
claim needs a separate new argument.

Credits: @CubeJerry; Route C's order-five construction; root's independent
word classification; the OpenAI source and predecessor characteristic-two
formulas/executors; substantial AI-assisted review.
