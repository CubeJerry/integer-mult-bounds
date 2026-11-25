# Independent Route B review of the space and fixed-radix suppliers

Reviewer: E003 Route B. Result: **pass for the component statements below**.
This is independent AI-assisted written review, not human refereeing,
kernel verification or a complete multiplier execution. The two-scale
global proof is this reviewer's own work and is not independently
certified by this note.

## Sources read

Read in full E003 Route A's:

* `GUARDED-CONSTANT-SPACE-STREAMS.md`;
* `FULL-RATE-BINARY-FIELD-PACKING.md`;
* `STREAMING-COMPARISON-LABELS.md`;
* `SHARED-PENCIL-CONSTANT-SPACE.md`.

Compared the layout/volume claims with actual OpenAI tape
`build/interchange.tex`, particularly the complete reserve preparation,
rectangle delivery, low-rank delivery and depth-first proof, at
`openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`.
Read the relevant E002 height-priced, succinct cyclic, numerical precision,
small-radix and polynomial-interchange suppliers at programme predecessor
`a2d9c4b00c02dadf7bdc970acf9190dfabf9ec32`.

Also read in full S003 B's `explicit-dyadic-geometry.md`, with S003 A's
`review-explicit-dyadic-geometry.md` and C's
`REVIEW-B-COMPACT-INTERCHANGE.md`, now present at
`c65aac1156a46d10c0ef2aa36fd846c7a93518e1`. This reviewer independently
checked the following algebra rather than relying only on those reviews.

## 1. Guarded keys and the scope of the space claim

The affine header is per monotone run, not per symbol. There are `Pa`
headers and each is at most h bits; `qB>=h` gives `Pah<=PaqB<=V`.
The old payload padding remains less than four. Reusing each radix-pass
region proves a visited-space bound; counting only live keys would not
have sufficed. The inverse reuses the same short-coefficient run
decomposition, so a large modular inverse never changes the header bound.

The general row sort likewise needs its complete spatial suffix: a row
payload of at least its key length pays all headers. Cyclic grade
rotations do not use these headers at all. Descriptor powers are genuine
setup and can be absorbed by their complete fields; the proof explicitly
does not permit arbitrary `poly(log V)` work on every datum.

The strengthened nonbase condition is polynomial in m. Choosing one fixed
power-arity exponent smaller than its reciprocal ensures it at every
sufficiently large active width, including the extra `m` factor between
parent and child fields. This is compatible with the nonstationary
interchange recurrence. Below the guard, direct radix-digit moves have
constant payload space and their full actual time remains charged.

## 2. Full-rate field packing

FP1 is an exact vector-space bijection, not a zero embedding. The
`dW` binary input rows become W independent E-valued rows for every
opaque payload-bit position. All input coordinates remain independent.
The completed target is a permutation with coefficients zero/one, so
unpacking recovers the same permutation on every original bit row.

For a child call the encoded numerator volume is `d b |Omega|` and the
parent denominator is `W d b |Omega|`; d cancels. The child's own field
can differ because its input is an arbitrary binary record and it
returns a permutation of those bits. No algebra embedding from the
parent's field into the child's field is required.

FP2's d passes keep a constant number of arrays whose total payload
sizes never exceed a constant times V. Both accumulation and inverse
extraction preserve grouping and spectator order. The d dependence is
paid in time. The leading independent-row requirement is explicitly
`W_bin=dW_E`, and the existing multidigit batching pays its less-than-two
padding. This is the correct place to account for d; charging d both
there and again as new symbol volume would double-count it.

## 3. Simultaneous spectral comparisons

For each `N_j`, its control `H_j` is earlier in the declared layout.
The three consecutive runs therefore give exactly the order-three
spectral flags. Nested counters keep prior flags valid when entering a
later field. A single current tuple is sufficient for the on-demand
coefficient routine. No claim is made that an arbitrary scattered
predicate has this streaming property.

The field-loop reset cost is charged to its complete `Q S_j` fiber,
not to a nonexistent free random-access counter. Since the small
coefficient selector is polynomial in m, reading all m current flags
per controlled tuple preserves the local polynomial time bill. Reusing
the flag/counter region avoids m full-volume tracks. This satisfies the
actual spectral-order interface of the E002 repair note.

## 4. The rank accumulator schedule and exact common addresses

The crucial storage quantity is `m r*/N<=1`. Retaining all U_j requires
at most V total encoded bits, even though each U_j may use a different
query-specific common layout. The proof never adds U_j and U_k without
a paid layout change.

For basis row i of the rank factorization, the source identity is

```
X_i(S_(i,j)^(-1) z) + sum_(rectangles with i in K) X_(L,j)(z).
```

The first rectangle pass builds exactly these sums while each transformed
source collection is present. It also delivers the direct rectangle
contribution. Central multiplication by the rank-label inverse commutes
with A_j because those maps act on distinct label and internal-row
indices. It does not commute any address-dependent mask through a
converter.

In the second pass, each destination rectangle receives the low-rank
contribution in its prepared endpoint coordinates, then returns to
ordinary coordinates before adding to the global accumulator. Direct
and low-rank terms therefore cancel at the same logical address.
Endpoint preparation/return is repeated only an absolute number of
times, not once per query. The conservative factor four is valid for
the stated source bill; its use changes `2^17` to `2^19` before any
separate dyadic-geometry allowance.

The named arrays fit a fixed number of V-sized regions, and every
non-full-volume spatial child stays within one label. With the existing
padding its fraction is at most `2/N<=2/3`. Finite repair children keep
their `1/16` ratio. Parent arrays are cleared before full-volume reserve
calls. These are actual uniform contraction/clearing conditions, not
merely a count of simultaneously active recursive calls.

## 5. Explicit dyadic geometry and radix three

The block form `[[B,I],[I,0]]` has inverse `[[0,I],[I,-B]]` even when
B is singular. The primal pair `(e+z_v)/2,(e-z_v)/2` has unit self-Gram
and the required cross-Gram blocks. Projecting the coordinate complement
away from `span(e,z_v)` is injective, because their two primal pivots
are excluded from the complement.

For a rectangle, source and destination star pivots are disjoint. The
cross vector g has primal z coefficient -2 and hence is independent
of all stars. Pairwise Far values give `g^2=8-8=0`; all star/cross
pairings vanish, and each difference is orthogonal to every oriented
endpoint pair. This recovers the source isotropic difference space.

The reserve-only coordinates of g are

```
2 a_v - sum_a(f_(a,l_a)+f_(a,k_a)).
```

They equal `a+2 sum s` at a source and `-a+2 sum t` at a destination.
The distinguished anchor of a has coefficient one; all stars have
independent unit pivots. Thus the reserve basis and its transition are
explicitly unimodular, using only dyadic elementary operations.
The sign difference at destinations is necessary.

After moving the difference coordinates late, the early complement
changes by main-pair/later differences and the main pair changes by
late differences. This is precisely the source lower-triangular order.
Upper-target operations in complete endpoint lists pay two explicit
interchanges; the reserve-only lists are shared across queries.

All required diagonal units are powers of two. Consequently radix three
works for every template, and the initial binary-to-ternary full-grid
padding has factor less than nine. The ambient dimension is doubled
relative to the old coarse bound. The exact endpoint constants must
also increase: the source-specific `2^19` allowance alone is not the
whole new geometric invoice. The combined absolute constant has no
effect on the `Phi(log m)` scale, but is explicitly retained in the
global note's `C_I`.

## 6. All-arity label profile

Independently read E003 A's `ALL-ARITY-LABEL-PROFILE.md` and rederived
its inequalities A2--A10. With `x=ceil(log2 m)`,
`v=ceil(log2(x+2))`, `d` the least power of two satisfying
`d^3 v>=x`, and `t=2+ceil(x/d^2)`, the exact rank exponent gives
`m r_*/N<=1/4`. Minimality gives
`(x/v)^(1/3)<=d<2(x/v)^(1/3)` on the stated guard. The resulting
`4x+12d^2` label-count exponent is below `5 log2 m` for
`x>=2^40`; the displayed address-dimension estimate is below
`(log2 m)/2`. The incidence expansion yields at most
`35 x^(2/3)v^(1/3)`, so the stated factor 64 is conservative.

The completed E002 power-of-two-window predictor really has at most
`24 sqrt(m)` stages, as checked directly in its polynomial interchange
invoice I1; no suppressed `sqrt(log m)` factor is needed here.
The all-arity conclusion keeps a fresh absolute geometric factor.
It therefore applies to every sufficiently large odd arity selected
by the variable-width scheduler, rather than only a fixed-J subsequence.
This component review passes. No new numerical checker was needed to
resolve a remaining issue in these elementary inequalities; the author's
exact receipt remains separately attributed.

## 7. Replays and admission limits

Copied the original S003 exact checker into this route's isolated
`dyadic-review-replay/` and ran it there. It passed 64 Gram blocks,
200 isotropic pairs, 3,104 individual basis-vector inverse cases,
3,088 reserve-only inverse cases, 40 reserve columns and 30 fixed-radix
scalings. Wrong cross-vector and endpoint-reserve signs were rejected.
The retained receipt is in that directory; original evidence was not
regenerated or modified.

These facts close the listed local suppliers, subject to their stated
guarded layouts. They do not independently prove the source's entire
finite algebra or the two-scale global recurrence. The latter still
requires an independent review of constructor/node accounting, all
numerical Walsh operations, the common precision argument and final
all-length multiplication assembly.

Credits: @CubeJerry; pinned OpenAI source identities; S002/E002 component
authors; S003 B's explicit geometry and its A/C reviews; E003 A's new
storage schedules; substantial ChatGPT multi-agent assistance.
