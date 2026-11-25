# Independent review: the variable invoice and exact canonical incidence

Reviewer: E002 Route A. Status: **PASS, within the explicitly stated
certificate and canonical-partition scopes**. Neither note proves a
multiplication, routing, storage or general endpoint lower bound.

Reviewed snapshots:

- Lead `variable-invoice-barrier.md`, SHA256
  `2e73cb27ac99e114fcc61c959754945a3d102389b51741efa94c6a1d2cbbe7cb`.
- Route C `canonical-incidence-exactness.md`, SHA256
  `7bd3afe3eb57b283ae9af1e3dd045c212bdaa9b168ae71e0a25be16b6930d132`.
- C checker `verify_canonical_incidence.py`, SHA256
  `2ca147f8186074c7957eb0ca6926e856d425639afc39d6db96002e50dce93fa3`.

## 1. Lead's local minimization

Write z=log2 m and retain the displayed sufficient rank guard. Its
consequence `t>=z/d^2+2-2/d^2` is correct. The elementary binomial and
alphabet bounds give

    log2 lambda >= d^2-1+d(t-1)+d(d-1)log2 t
                >= (3/4)d^2+z/d+(d^2/2)log2 t.

The last inequality is valid for every d>=2: `d^2-1>=3d^2/4`,
`d(t-1)>=z/d+d-2/d>=z/d`, and `d(d-1)>=d^2/2`.
No power-of-two assumption on d was used.

For `a=(z/log2 z)^(1/3)` and `b=z^(1/3)(log2 z)^(1/6)`, the three
ranges d<=a, d>=b, and a<d<b exhaust all choices. In the middle range,
t>=z/d^2>=z^(1/3)/(log2 z)^(1/3), hence log2 t>=log2 z/6 for large z.
The resulting last term is at least `a^2 log2 z/12`. Each range therefore
gives a fixed positive multiple of `z^(2/3)(log2 z)^(1/3)`. Small z can be
absorbed into the stated threshold. VB1 is proved by this calculation.

## 2. Accumulation over a changing arity chain

The ratio comparison in VB5 is valid. Away from a fixed bounded interval,
Phi(z)/z is comparable, with absolute factors, to `(log2 z/z)^(1/3)`.
That comparison is decreasing for sufficiently large z. It follows
uniformly for `1<=z<=C1 Y` that

    Phi(z)/z >= c Phi(Y)/Y,

where c can depend on C1 but not Y or z. The bounded initial interval has
a positive minimum ratio and cannot violate the inequality for large Y.
Summing after multiplication by z_i proves the stated claim.

The warning about width contraction is necessary and correct. An upper
bound on child width alone does not force the sum of logarithmic arities
to be large. The admitted composite-radix chain has the checked two-sided
relation `u/(4m)<=v<=u/m+2`; above its guards this implies
`log2 u-log2 v=log2 m+O(1)`. Summation over O(log log U) levels, down to
a bounded or polylogarithmic terminal width, supplies the stated
Theta(log U) total. This is an application of the actual width chain,
not a consequence of an arbitrary recursion upper bound.

Finally an upper bound on a physical algorithm's cost cannot become a
lower bound by naming it a certificate. The lead explicitly assumes a
nonnegative *assigned* logarithmic charge at least c0 Phi(log2 m_i).
Under that premise the barrier applies to the specified product of
literal charges. The lead's limitation paragraphs correctly preserve
this distinction. No mathematical correction is required.

## 3. C's exact canonical partition

For one q=2^t letter coordinate, the first-differing-bit rectangles
are nonempty, pairwise disjoint on ordered unequal pairs, and exhaustive.
At each of the t bit positions a fixed letter occupies exactly one
source side and one destination side. The count 2(q-1) and exact t
incidences therefore hold without an averaging argument.

For an inner word in h=2d-1 coordinates, choose its d changed coordinates,
then the opposite letter in the first changed coordinate, and one of the
t containing rectangles at each of the other d-1 coordinates. All outside
coordinates are forced. This gives exactly

    alpha=binom(h,d)(q-1)t^(d-1).

Different choices cannot describe the same nonempty rectangle, since
the construction partitions nonempty ordered-pair sets. The direct
rectangle count is

    binom(h,d) q^(h-d) q(q-1) [2(q-1)]^(d-1)
      =binom(h,d)2^(d-1)[q(q-1)]^d.

Dividing |U| alpha by this expression gives exactly the claimed average
side size `[q t/(2(q-1))]^(d-1)`; the q and 2 exponents agree.

The outer count repeats this independent choice at each of d selected
outer coordinates. Each fixed outer label consequently has exactly
`binom(h,d) alpha^d` source incidences and exactly that many destination
incidences. Outside words are forced, so no additional q factor enters.
The total rectangle formula CI4 and average-size exponent d(d-1) follow.
These counting arguments do not require power-of-two d. CI1 and CI2 pass.

## 4. What the two notes establish together

The literal expression lambda is the exact regular incidence of this
particular retained canonical partition. Combining C's theorem with
VB1 strengthens the interpretation: within the sufficient rank guard,
that partition really has the stated large incidence count at every
label. Merely sharpening a counting estimate for the same partition
cannot remove that factor.

It remains possible for physical processing to share work between
incidences, consume them without simultaneous retention, or avoid a
separate expensive operation per incidence. Neither exact counting nor
the certificate theorem supplies a per-incidence time lower bound.
Other partitions or rank constructions are also outside the conclusion.
This is the decisive scope restriction in accepting both documents.

## 5. Independent finite replay

I inspected the checker, copied it unchanged to
`replay-canonical-incidence/`, and ran it independently. It reconstructs
all rectangle sides and compares the ordered edge set with a separate
Hamming-distance enumeration. All six inner instances passed: 93,624
rectangles, 358,296 edges, 1,768 words. The full d=2,q=2 outer instance
passed with 13,824 rectangles/edges and incidence 27 at all 512 labels.
All 1,609 stated negative controls passed. The copied receipt is retained.

The independent counting arguments above establish the full family;
these finite checks only corroborate the concrete implementation.
No tape execution or asymptotic complexity experiment is being claimed.

Credits: the E002 lead and Route C for the reviewed results; the pinned
OpenAI source and retained characteristic-two adaptation; @CubeJerry
and substantial ChatGPT multi-agent assistance.
