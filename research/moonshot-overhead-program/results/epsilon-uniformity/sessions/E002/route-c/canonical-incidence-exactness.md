# Exact regular incidence of the canonical rectangle partition

Status: **new exact combinatorial component; independent review requested**.
This concerns the specific retained partition. It is not a lower bound on
other partitions, address routing, space schedules or multiplication.

Source: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, tape
`interchange.tex`, directed rectangles in the label lemma. Its retained
characteristic-two version is programme predecessor
`0607d044d1d09489580da0e5828588820e1a6775`,
`routes/B/characteristic-two-label-geometry.md`, Section 3. That note
states exact t incidence for one first-differing-bit partition, but only
an upper bound for the resulting two-level incidence.

## 1. One coordinate

Let `q=2^t`, t>=1, with letters their t-bit strings. For bit position
j, prefix p of length j, and orientation epsilon in {0,1}, take

\[
L_{p,\epsilon}=\{p\epsilon z:z\in\{0,1\}^{t-j-1}\},\qquad
K_{p,\epsilon}=\{p(1-\epsilon)z:z\in\{0,1\}^{t-j-1}\}.
\]

Every ordered unequal pair lies in exactly one rectangle, specified by
its first differing position. All rectangles are nonempty. Their number
is `sum_(j=0)^(t-1)2^(j+1)=2(q-1)`. Every letter lies in **exactly t**
source sides and t destination sides, one at each j, despite the varying
side sizes.

## 2. Inner distance rectangles

Put `h=2d-1`, d>=2, and `U=[q]^h`. Choose a d-subset S of positions,
fix common letters outside S, fix the ordered distinct letters at the
first position of S, and choose one Section 1 rectangle at each other
position of S. The Cartesian product is the source canonical inner
rectangle. These nonempty rectangles partition the ordered pairs at
distance d. Two words on one side can differ in at most d-1 positions,
since the first position of S is fixed.

**Lemma CI1.** Each inner word belongs to exactly

\[
\alpha=\binom hd(q-1)t^{d-1}                         \tag{CI1}
\]

source sides, and to exactly alpha destination sides.

**Proof.** For a fixed word choose S in `binom(h,d)` ways. All
outside letters are forced. The first opposite letter has q-1 choices.
At every other selected coordinate there are exactly t containing
rectangles by Section 1. The choices are independent and nonempty.
Distinct choices give distinct rectangles because the construction is a
disjoint nonempty edge partition. Destination incidence is identical. ∎

The total number of inner rectangles is exactly

\[
R_{\rm in}=\binom hd q^{h-d}q(q-1)[2(q-1)]^{d-1}
          =\binom hd 2^{d-1}[q(q-1)]^d.              \tag{CI2}
\]

Thus the average source-side size, from total incidence `|U| alpha`,
is `[q t/(2(q-1))]^(d-1)`. It need not be an integer.

## 3. Outer distance rectangles

Let `V=U^h`. Its off-diagonal support has exactly d unequal outer
positions, each at inner distance d. Choose those outer positions, fix
all other inner words, and take one inner rectangle at each selected
position. These Cartesian-product rectangles partition the support.
Across each rectangle the number of far inner positions is d; within
either side it is zero.

**Theorem CI2.** Every outer label belongs to exactly

\[
\lambda_{\rm can}=\binom hd\alpha^d
 =\binom hd^{d+1}(q-1)^d t^{d(d-1)}                  \tag{CI3}
\]

source sides and exactly the same number of destination sides.

**Proof.** Choose the d varying outer positions in `binom(h,d)`
ways. All other inner words are forced. At each selected position CI1
gives exactly alpha choices containing its inner word. Nonemptiness and
uniqueness of the edge partition make their product an exact count. ∎

The exact total rectangle count is

\[
R_{\rm out}=\binom hd |U|^{h-d}R_{\rm in}^d.          \tag{CI4}
\]

The average source-side size is
`[q t/(2(q-1))]^(d(d-1))`. These counting statements hold for every
integer d>=2. The programme's power-of-two condition is needed for its
characteristic-two rank formula, not for this partition count.

## 4. Consequence and limitation

The expression called an incidence majorant in the retained profile is
the **exact regular incidence of this canonical partition**. A sharper
count of the same partition cannot remove its q or `t^(d(d-1))`
factors. Combined with the sufficient rank guard, the lead's elementary
minimization gives an actual `exp_2(Omega(Phi(log m)))` incidence
count for this partition.

This does not prove that each incidence must cause a distinct expensive
physical operation. Endpoint plans might be shared, copies serialized,
cancellations combined, the partition changed, or the rank guard sharpened.
The current source invoice deliberately charges incidences independently,
so its scoped certificate barrier remains the appropriate conclusion.
There is still no multiplication or general-routing lower bound.

The next target is therefore more precise: improve delivery/retention of
incidences or change the rectangle family. Replacing the current upper
count by its exact value does not improve the asymptotic profile. This
lemma asserts no new positive multiplication envelope.

Credits: @CubeJerry; the pinned directed-rectangle construction; the
characteristic-two adaptation and prior profile; the lead's scoped
barrier; substantial ChatGPT multi-agent assistance. This is a complete
written combinatorial proof, not formal verification or full tape execution.

## 5. Exact finite supporting checks

`verify_canonical_incidence.py` constructs the actual coordinate-product
rectangles and independently enumerates the far ordered pairs. Six inner
cases `(d,q)=(2,2),(2,4),(2,8),(3,2),(3,4),(4,2)` verified 93,624
rectangles, 358,296 partitioned edges and regular source/destination
incidence at all 1,768 words. The full outer `(d,q)=(2,2)` case verified
13,824 rectangles/edges and incidence exactly 27 at all 512 labels.

The 1,609 negative controls include a wrong `(t-1)` incidence factor,
omitting a nonempty rectangle, and witnesses showing that removing the
first pinned coordinate can violate the within-side distance condition.
The receipt is `canonical-incidence-verification.json`. These checks
support the finite partition implementation; CI1/CI2's written counting
proof, not those checks, establishes the full family.
