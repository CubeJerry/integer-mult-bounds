# A common isotropic preparation cannot merge all opposite anchors

Status: **proved scoped geometric counterexample; accepted by lead review** in `../lead/review-scoped-adaptive-obstructions.md`. This records a failed attempt to remove a large endpoint-incidence factor after the varying-arity construction. It is not a lower bound for other shared-address compilers, field interchange or integer multiplication.

Pins: OpenAI math `3344da59991ed94f9ba711217b29c1d760badfa6`; programme `0607d044d1d09489580da0e5828588820e1a6775`; S003 B `explicit-dyadic-geometry.md`, B2.3/B2.7. C/A's literal-invoice barriers already exclude improving that invoice merely by retuning symmetric or nested distances. Here the attempted escape is to share one physical reserve preparation across rectangles with the same source anchor and different opposite anchors.

## 1. Attempt and optimistic budget

The prescribed incidence contains (q-1)^d choices of opposite first letters. Many leave the source side unchanged. Sharing one preparation across them, followed only by lower triangular query maps, would remove d log q from the logarithmic endpoint bill, a consequential saving at the optimized scale.

The direct construction would enlarge the rectangle's totally isotropic late-reserve difference space to one common totally isotropic space containing every opposite-anchor difference. This would retain the source proof: endpoint differences use late reserves and other coordinates project into the early complement. The proposition shows that this specific mechanism fails for a complete (q-1)^d family in the existing labels. A compiler with other flags, nonisotropic forms, extra cross terms or different labels is outside the claim.

## 2. Explicit mutually incompatible anchors

Let d>=2 and q>=2 be powers of two; h=2d-1. For c in [q] define

    u(c)=(c repeated d times, then 0 repeated d-1 times).

Different u(c),u(c') have inner Hamming distance exactly d. The source l has u(0) in all h outer positions. For a=(a_1,...,a_d) in {1,...,q-1}^d, let k(a) have u(a_i) in its first d outer positions and u(0) elsewhere. Every (l,k(a)) is a supported off-diagonal label pair. The far inner-pair count between k(a),k(b) is exactly dist(a,b), their tuple Hamming distance.

In the rational form, z_v=z+sum_i f_(i,v_i) satisfies

    <z_v,z_w>=2-4 FarCount(v,w)/d.

The oriented opposite-anchor difference from B2.7 is

    g_a=-z_l-z_(k(a)).                                  (IP1)

Expanding the four bilinear terms gives

    <g_a,g_a>=0,
    <g_a,g_b>=-4 dist(a,b)/d.                            (IP2)

Indeed both cross terms with z_l equal -2, its norm is 2, and the remaining term is 2-4 dist(a,b)/d. Every distinct pair is nonorthogonal over Q.

**Proposition IP.** A totally isotropic rational subspace contains at most one g_a. At least (q-1)^d different totally isotropic difference spaces are therefore needed to cover this family. One common isotropic late-reserve extension cannot serve even two of these distinct anchors.

**Proof.** Pairings of any two vectors in a totally isotropic subspace vanish. Equation (IP2) excludes every distinct pair. QED.

The obstruction survives reduction of these dyadic vectors and forms modulo 3^f whenever 3^f>d: d is a unit, and 1<=dist(a,b)<=d<3^f. This is rational/radix-3 address geometry. Reducing pairings in the characteristic-two data field would change the model and incorrectly erase the obstruction.

## 3. The obstruction persists with the identical source side

Restrict each a_i to the high half {q/2,...,q-1}. In one inner rectangle choose the first d coordinates as differing; freeze its first source letter at 0 and first destination letter at a_i; use the first-bit split in every other differing coordinate. Its source side is

    L0={u: u_1=0; u_2,...,u_d<q/2; other letters 0},

independent of a_i. Its destination side is

    K0(a_i)={u: u_1=a_i; u_2,...,u_d>=q/2; other letters 0}.

These are actual members of the retained directed-rectangle construction. Take their product over the first d outer positions and fix the other outer positions at u(0). All resulting outer rectangles have the identical source side L0^d times the fixed positions. Their destination anchors u(a_i) are valid. The preceding proof therefore forces at least (q/2)^d common isotropic difference spaces even for an identical source endpoint set. Its logarithm is d log2(q)-d, so the opposite-letter dependence survives at its leading scale in this reuse model.

## 4. Consequence and limits

The failed construction replaces every opposite-anchor-specific isotropic preparation by one depending only on the source anchor or source set. Proposition IP gives an explicit obstruction. It does not prove that the required distinct spaces force distinct expensive calls on all data: prefix sharing, algebraic aggregation, nonisotropic layouts or another compiler may still help. It does not price the separate t^(d(d-1)) factor or assert any new general exponent-2/3 barrier.

A second generic attempt sums inputs in a source-only common layout, then changes each sum to a full rectangle layout separately for each query. Its cost is m times the number of rectangles divided by N. The inner rectangle count is

    R0=binom(h,d) 2^(d-1) q^d (q-1)^d.

The outer count divided by N is binom(h,d)(R0/q^h)^d, which is at least one: q-1>=q/2 gives R0/q^h>=binom(h,d)q/2>=1. Thus the generic per-query conversion already costs at least m normalized spatial calls and cannot meet a sqrt(m) subexponential invoice. A query-independent aggregate identity would be a different mechanism.

`verify_isotropic_preparation_obstruction.py` constructs sparse primal vectors and evaluates the Gram form directly, rather than merely substituting (IP2). It checks self-isotropy, distinct pairings, the identical-source-side subfamily, radix-3 reductions and wrong-vector controls. These finite checks supplement the exact argument. No tape-machine execution or new global multiplication result is claimed.

Prepared for Jerry Chen (@CubeJerry), with substantial OpenAI AI assistance.
