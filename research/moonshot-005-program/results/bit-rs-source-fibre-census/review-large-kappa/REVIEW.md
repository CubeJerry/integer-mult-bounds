# Independent review: ordinary RS source fibre census

**Accepted within the stated source and route contract. No new complete κ.**

The 2,281 certified obstructions cover every nonorthogonal pair among the
99 nonsingleton native donors other than donor 10. All use the actual source
nodes 1 through 28, omit receiver 80, and have polynomial span ranks 15 and
16. The conclusion survives arbitrary separate bijections of the complete
original donor banks, arbitrary invertible quotient labels, and arbitrary
deterministic downstream processing on the specified routes. The retained
donors must therefore be pairwise orthogonal real roots, so at most eight
of these 99 ordinary source information systems can survive unchanged.

The 31-centre packing counts in the author proof are correct: 78 special
donors include eight singleton donors and 70 members of this 99-donor set;
29 ordinary systems remain. The global bound requires at least 21 further
changes. An additional exact search on those **actual remaining 29 donors**
strengthens this to **at least 22 further changes**, because their largest
pairwise orthogonal subset has size seven. This is a source information
obligation, not an additional MOVE lower bound.

## What was checked independently

`check.py` imports no author or predecessor Python and uses only the standard
library. It authenticates the decompressed geometry, 106,560 actual route
records, plane phases, original paid RS source and receipt, S028 target
assignment, compact witness table, and all four packed-source parameter
and cost tables. Its finite-field multiplication uses ordinary binary
polynomial convolution followed by long division modulo `0b1000011`.
It finds multiplicative inverses for all 63 nonzero elements.

The checker reconstructs all real orthogonality relations from the 120
eight-dimensional root tuples. Every native donor has 28 actual source
planes. Every one of the 6,470 proper donor/receiver pairs sees exactly
16 of those planes. The eleven singleton donors are

    8, 31, 49, 53, 58, 77, 82, 93, 97, 105, 106.

The remaining 100 include donor 10. Removing that exceptional target
column leaves the claimed set J of 99 donors. Each of its nonorthogonal
pairs lies in exactly one actual A2 plane. There are precisely 2,281 such
pairs, and the compact certificate has exactly one record for each.

For every recorded donor and receiver, the checker forms the degree-16
annihilator of all sixteen visible nodes and obtains the inverse fibre by
synthetic division by the shared plane's linear factor. It checks the
result is monic of degree 15, vanishes at the other fifteen nodes, and is
nonzero at the shared node. This differs from the author's direct
fifteen-factor construction. A separate descending-pivot row-space
elimination gives the following exact census:

| Ordered rank pair in the recorded donor order | Witnesses |
| --- | ---: |
| (15, 16) | 1,134 |
| (16, 15) | 1,147 |
| Total | 2,281 |

The checker verifies the receiver labels against the real geometry,
requires sixteen distinct labels, and excludes receiver 80. A concrete
negative control replaces one receiver of a rank-16 witness by a duplicate;
the rank falls to 15. No random search, floating arithmetic, interval sign,
or imported author eliminator is used in this review.

## The mixed-phase cut is genuinely tight

The source and capacity statements must be considered together. At each
nonsingleton donor, four planes receive the complete ordinary quotient
early and 24 planes receive complementary early and late halves. The
ordinary quotient in every case is the same set of 240 scalar evaluations
of 240 independent degree-below-16 polynomials. Its two temporal pieces do
not give two independent 240-symbol observations. The eleven singleton
sources have genuine extra derivative information and are correctly
excluded from this theorem.

The checker reads all actual bank-480 routes and verifies that every
H-to-D port has exactly two original field owners across its chronological
phases: two early, one early and one late, or two late as prescribed. Each
H has 45 such ports. For every native receiver perpendicular to H, exactly
15 of those ports lead to D charts perpendicular to that receiver. There
are 37,296 checked native receiver/H incidences. After the actual eightfold
repetition, the cut capacity at each incidence is therefore

    15 ports × 2 genuine owners × 8 copies = 240 field symbols.

The D duality is also reconstructed from real root dot products. Every
actual H/D incidence is containment; every D/K incidence is containment in
the exact perpendicular D. An input from an H not perpendicular to the
receiver cannot reach its facet through a monotone H/D/K route. At a fixed
donor the only potentially informative source planes for that receiver
are consequently its sixteen visible planes.

Fix all fifteen visible source quotients other than the shared H. These
fix both temporal pieces and every stationary copy derived from those
quotients. Other source inputs and all original Y baselines can be held
fixed as well. Variations in the two selected donors can then reach the
receiver only through the 240-symbol shared-H cut. Allowing arbitrary
deterministic processing at D, K or the facet cannot increase the number
of distinguishable cut transcripts. A stationary H cache supplies no new
path across the cut; a D cache can retain an earlier value but cannot
increase the alphabet of the actual incoming early and late transcript.

This argument would fail if a cache had another permitted outgoing
information path, an informative return/preload entered the proper
computation, or a changed source sent an extra observation. These are
explicitly outside the reviewed theorem. It is important to retain those
scope conditions when quoting the result. The theorem does not prohibit
such changes; it says the present ordinary source partitions cannot be
repaired solely by changing downstream maps on the fixed routes.

## The nonlinear extension is valid

Let F be a finite extension of GF(64), let s be the number of polynomial
channels, and let q = |F|^s. The original additive bank is F^(16s). For
one receiver and one shared H, fixing the other fifteen quotients at a
donor gives an affine fibre of cardinality q. Pulling it back by an
arbitrary bijection of the donor's complete original bank still gives a
q-element set. Source coordinate linearity is not assumed.

Write U and V for any such fibres at the two donors. For receiver i ≠ 80
and either donor j ≠ 10, the prescribed foreign target block is the
identity. This is checked against all 123 modified S028 block locations:
every modification lies in row 80 or column 10. After fixing the other
original inputs, the demanded output ranges over a translate of U+V.
The tight shared-H cut has at most q possible transcripts, so

    |U| = |V| = q,   |U+V| ≤ q.

Here U+V uses the original additive coordinates. Arbitrary later decoders
do not weaken the cardinality bound, since the exact required output must
still distinguish distinct sums.

For completeness, the elementary equality lemma can be proved without
assuming U or V is a subspace. Choose v0 in V. Since U+v0 already has q
elements, U+V = U+v0. Thus each v-v0 stabilizes U. The translation stabilizer
L of U contains V-v0 and has at least q elements. For any u0 in U, the
coset u0+L lies in U, giving |L| ≤ q. Consequently |L| = q, and both U and
V are cosets of L. This is a statement about finite abelian groups; L
need not initially be an F-linear subspace.

Every pair of fibres is available because the original donor banks are
independent. Holding a fixed fibre U0 while varying V forces every V to
have stabilizer L = Stab(U0). Holding one of these V while varying U gives
the same conclusion for every U. Hence the entire two fibre partitions
coincide as unlabelled partitions of the original additive bank. This
consistency step is needed; showing only that selected individual fibres
have equal cardinality would not suffice.

Apply this to each indexed receiver. The composition of the two source
bijections carries the coset partition of W_j,i to that of W_k,i
simultaneously for all i. Any bijection preserves the equivalence relation
generated by a family of partitions and the cardinalities of its classes.
For linear coset partitions, the generated relation has the cosets of
the sum of their direction spaces as its classes: a chain of partition
steps adds vectors from those spaces, and every such sum gives a chain.
The class sizes are therefore |F|^(s r_j) and |F|^(s r_k), where r is the
rank of the corresponding degree-15 scalar polynomials. The 15-versus-16
certificate is incompatible with such a bijection for every positive s.

This proof permits a source bijection to mix all 240 polynomial channels,
sectors and copies. It does not reduce the permitted changes to separate
scalar gauges. Bijective labels applied to an individual quotient leave
its partition unchanged and are harmless. Extension of the finite field
preserves the certified ranks. Positive body repetition multiplies both
exponents, including arbitrary binary invertible changes of all replicated
source coordinates. An infinite-field cardinality argument is not being
asserted. Changes that couple originally independent source banks are
also outside this theorem.

The checker corroborates the equality lemma on all 4,900 ordered pairs of
four-element subsets of F2^3: all 28 pairs with a four-element sumset are
cosets of the same four-element subgroup. This is a failure-mode control;
the preceding group argument proves the general statement.

## Complete counts for recorded packings

The following counts are reconstructed by taking the union of the actual
native roots in the chosen central H charts and comparing that set with
every key of the corresponding `special_donor_costs` table. Thus they are
not inferred just from a headline chart count. Donor 10 belongs to none
of these special sets.

| Central charts | Special donors | Special singletons | Special donors in J | Retained in J | Further changes from ≤8 | Exact largest orthogonal retained set | Further changes from actual retained set |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 23 | 68 | 0 | 68 | 31 | 23 | 7 | 24 |
| 24 | 71 | 4 | 67 | 32 | 24 | 8 | 24 |
| 30 | 75 | 0 | 75 | 24 | 16 | 6 | 18 |
| 31 | 78 | 8 | 70 | 29 | 21 | 7 | 22 |

The exact maxima in the last two columns are a reviewer addition. The
checker exhaustively branches on including or excluding a native root;
the include branch restricts candidates to its real perpendicular roots.
It prunes only when the selected and remaining vertices together cannot
beat the current witness. At most 259 recursive calls are needed in these
four cases. A maximum orthogonal subset for the 31-centre residual is

    {30, 41, 50, 57, 65, 80, 84}.

These seven roots are explicitly checked as pairwise orthogonal. The
exhaustive search excludes an eighth among the same residual 29 roots.
No construction is supplied that makes even those seven source systems
compatible with the whole physical circuit. The geometric upper bound
is a necessary condition only.

## Reproduction, scope and remaining work

From the repository root:

    python -I -B research/moonshot-005-program/results/bit-rs-source-fibre-census/review-large-kappa/check.py --repo . --out FRESH

Expected status: `PASS_INDEPENDENT_RS_SOURCE_FIBRE_CENSUS`. The output
`RESULT.json` records all source hashes, rank counts, physical capacity
checks, exact packing counts and controls. Normal and Python-optimized
runs use explicit exceptions rather than removable assertions.

The reviewed result is a source-only obstruction for the exact original
S028 target and declared geometry. It allows free downstream retuning,
but does not assert an impossibility for every low-return target, for a
different source, for coupled sources, or for more informative routes.
It provides no quantitative MOVE charge for replacing a source quotient,
no lower bound above 34,688 for arbitrary fittings, no strict supplier,
and no discharge of any foundational assumption.

The next constructive question is to replace source information on enough
actual donors and then realize a shared H/D/K transport using that same
source. The exact residual counts show why simply adding a small number
of isolated central repairs to the recorded packings is insufficient.

Independent review by S030 Worker B for @CubeJerry, with substantial
OpenAI assistance. Credit the original native geometry and route authors,
the S028 two-sided target, S029 paid RS source and packing authors, and
the S030 census author. This is mathematical and executable review, not
formal-kernel or independent human verification.
