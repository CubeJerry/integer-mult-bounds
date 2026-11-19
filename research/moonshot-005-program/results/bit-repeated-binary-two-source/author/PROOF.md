# Repeating a binary two-dimensional quotient cannot complete the native source

## Statement

Retain the balanced native source, its ordinary quotient capacities, the
fixed canonical row code, all paid proper routes, and the exact native
target. Suppose every original source bank has one common decomposition

`G=(F_2^32)^r`,

and, after bijective quotient relabellings, every ordinary source quotient
is `A_(j,H) tensor I_r`, for an arbitrary binary rank-two matrix
`A_(j,H):F_2^32 -> F_2^2`. The matrices may vary with donor and plane. They
need not have commuting coefficient blocks, a common kernel, or a common
donor basis. The r copies of a particular base quotient are identical.
The eleven larger singleton source maps are unrestricted within capacity.

**Theorem.** No complete deterministic native code in this interface exists,
even with nonlinear downstream maps and arbitrary mixing of copies after
source emission. Actual balanced replication requires `r=180s` for some
positive integer s, so ordinary quotient width is `2r=360s`; the proof
applies to every such s.

The complete plane boundary would carry at most

`(40747/15)r = 2716.4666...r`

binary information dimensions, while the canonical-zero native input has
dimension `3264r`. At the base balanced normalization r=180 these numbers
are **488,964** and **587,520**, a deficit of **98,556**.

This excludes an arbitrary noncommuting binary32-coordinate base source
followed by identical repetition. It does not exclude larger base blocks,
independently varying binary32-coordinate blocks, arbitrary donor gauges
mixing the copies, F4-linear two-dimensional quotients, an added information
channel, or a changed canonical bank. No new supplier or kappa is claimed.

## 1. Local targets inherit the repeated two-dimensional form

Use the admitted quotient/saturated-plane argument. For an ordinary H,
let J_H be its m native donors, m=2 or3, and let I_H be the receivers for
which every donor in J_H has a tight source cut. At such a receiver each
donor's sixteen visible quotient matrices stack to an invertible binary
32-by32 matrix. Its inverse is repeated across the same r copies.
The common inverse-coordinate fibre for H therefore also repeats.

Consequently the required H-target row space, in the m independent quotient
inputs, is

`W_(i,H) tensor F_2^r`,

where W_(i,H) is two-dimensional in `(F_2^2)^m` and projects invertibly onto
each donor's F_2^2 coordinate. This is a **graph subspace**. This conclusion
does not choose a physical receiver-specific source map: it follows from
the same fixed A_(j,H) and the native sum contract. Quotient relabellings
do not change the information spaces.

Each of i's fifteen H-to-D ports has `2r/15` bits and their combined
capacity is exactly the target's `2r` bits. Recovery makes the full tuple
a bijective relabelling of the target. Thus every port factors through
that target. A port shared by several tight receivers factors through the
intersection of their target row spaces, even if its actual function is
nonlinear: it is invariant under every target kernel and hence their sum.
This is precisely the admitted common-function lemma.

## 2. Physical shared ports force pairwise intersection at base width

The exact native geometry has45 D4 exits at every ordinary H. Every visible
receiver sees15 of them. Any two distinct receivers in I_H share either3
or6 exits. The new finite check reconstructs this for every ordinary H.

The shared-port tuple has its full product range: it is a coordinate
subtuple of a bijection from the 2r-bit target to fifteen full-capacity
port alphabets. If q>=3 ports are shared, that tuple has `2qr/15` bits.
It factors through

`(W_(i,H) intersect W_(k,H)) tensor F_2^r`.

Hence `r*dim(W_i intersect W_k)>=2qr/15>0`. The base intersection
dimension is an integer, so every pair of these two-dimensional graph
spaces intersects nontrivially. Identical repetition is essential here.
With independently changing base blocks the total intersection could be
distributed among different copies, and this inference would fail.

## 3. Binary graph planes with pairwise intersections share a line

**Lemma.** Let W_a be two-dimensional subspaces of `(F_2^2)^m`, each
projecting isomorphically onto every coordinate F_2^2. If every pair
intersects nontrivially, all W_a contain one common line L.

First recall the elementary star-or-top argument for two-dimensional
subspaces. Choose distinct W_1,W_2 with intersection L. If a third W_3
does not contain L, its intersections with W_1 and W_2 are distinct lines,
so W_3 lies in the three-dimensional space T=W_1+W_2. Any other W not in T
would meet W_1 and W_2 in the same line L; its intersection with W_3 would
then force L into W_3, a contradiction. Therefore either all W contain L,
or all lie in one three-dimensional T.

In the latter case each coordinate projection T->F_2^2 is surjective and
has a one-dimensional kernel K_j. Their intersection is zero because T
embeds in the direct sum. At least two kernels are distinct. A graph
plane W in T must avoid both. Over F_2 there are exactly two hyperplanes
avoiding two distinct lines: their defining linear functionals take value1
on both nonzero generators, leaving one binary degree of freedom.
Thus there are at most two distinct W, which already share a line. A
family with no common line would require at least three. This proves
the lemma.

This use of F_2 is real. The verifier supplies three F4 graph planes that
pairwise meet in a line and have zero common intersection.

## 4. A common binary line bounds the whole plane alphabet

Fix H and its common line L=<l>. Each donor projection l_j is nonzero.
Choose a nonzero functional phi_j on F_2^2 with kernel <l_j>. For any
graph plane W containing L, any v in W outside L satisfies

`phi_j(proj_j v)=1` for every j.

The solution set to these m independent affine equations has dimension m.
Its linear span has dimension m+1, contains L, and contains every W.
Thus the union of all target row spaces has dimension at most m+1.

Color receiver i by its actual base target plane W_i. Distinct colors
intersect exactly in L. If no port neighborhood containing i were
monochromatic, every port visible to i would factor only through
`L tensor F_2^r`; it could not recover the 2r-bit target. Therefore this
coloring satisfies the same finite self-cover condition as in the admitted
varying-stripe package.

Let alpha_H be that package's color cap, capped at m. If alpha_H<m, the
number of distinct planes is at most alpha_H, so their span has dimension
at most 1+alpha_H. If alpha_H=m, the binary graph-plane span bound m+1
gives the same result. All covered H-port outputs therefore factor through
at most `(alpha_H+1)r` binary dimensions, regardless of subsequent mixing.

The independently admitted native caps are:

| Native donors m | alpha_H | Planes | New covered capacity per plane/r |
| ---: | ---: | ---: | ---: |
| 2 | 1 | 204 | 2 |
| 2 | 2 | 23 | 3 |
| 3 | 1 | 630 | 2 |
| 3 | 2 | 249 | 3 |
| 3 | 3 | 2 | 4 |

Their sum is2492r. Grant all1436 uncovered ports their full `2r/15` bits,
and all11 singleton planes their full3r source bits. The complete boundary
alphabet is at most `2^[(2492+2872/15+33)r]=2^[(40747/15)r]`.

The native canonical matrix K=I+O has rank9. On its kernel, of dimension
`(111-9)*32r=3264r`, the target determines every original source. Every
noncanonical varying route crosses the counted plane boundary, while the
canonical packets vanish. The smaller alphabet cannot injectively encode
this input space. This contradiction proves the theorem.

## Reproduction and proof boundaries

Run `python3 -B author/check.py --repo REPOSITORY --out OUTPUT`. The new check
authenticates native geometry and the admitted independent color-cap
certificate, reconstructs every joint-tight receiver set, every shared-port
intersection, all uncovered ports, and the exact global inequality. It
does not reclassify the old color search as a new independent verification.

It exhaustively enumerates all binary graph planes for m=2,3, their maximal
pairwise-intersecting families, their common lines, and the m+1 span bound.
It also checks a noncommuting GL2 pair and the F4 counterexample. These finite
controls complement the written all-replication proof.

The promised source maps are arbitrary A_(j,H), not merely diagonal or
semisimple2-by2 coefficient choices. However copying the same base is a
strict premise. Arbitrary cross-copy mixing at the source, varying modules,
larger coupled blocks, changed capacities, changed canonical messages and
additional paid syndrome channels remain separate live directions. The
information deficit is not a MOVE tariff. The complete source, suppliers,
caller and all foundational assumptions remain open.

Credit @CubeJerry, retained native/balanced source authors, and the admitted
quotient and varying-stripe port-cut proofs. This binary graph-plane extension
was developed with substantial OpenAI assistance from programme baseline
d8544284cbd0527cd03a0aad576a2d2c6eddcc0e. Independent review is recorded separately.
