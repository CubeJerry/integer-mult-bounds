# Exact free-rectangle counts in the binary Fourier geometry

Status: **proved combinatorial counts and a conditional routing target**.
This does not supply an improved Fourier kernel or tape algorithm.

Source pin: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`,
Fourier `kernel.tex`, label decomposition and endpoint transforms. The
numerical family uses ell=2, even L>=2, q=2^s, and labels `[q]^L`.
Use s for letter bit length, distinct from the source polynomial degree.

## 1. Nonzero free support

The source polynomial is

\[
p(k)=\prod_{r=1}^{L/2}(1-k/(2r)).
\]

On k in {0,...,L}, `I-p(Delta)` vanishes at distance zero and all
positive even distances. At every odd distance p(k) is nonzero, because
an odd k cannot equal 2r. Thus the free support is exactly odd Hamming
distance. The binary Gram value `1-Delta mod 2` vanishes on this support.

At an equal coordinate the canonical rectangle fixes one common letter.
At an unequal coordinate the first-differing-bit partition has exactly
`2(q-1)` nonempty directed rectangles and exactly s incidences at every
letter on either side. Their products over an odd unequal set partition
the corresponding support uniquely.

## 2. Exact regular incidence and output count

**Theorem FR.** Every label has exactly

\[
\lambda_{\rm free}
=\sum_{j\text{ odd}}\binom Lj s^j
=\frac{(1+s)^L-(1-s)^L}{2}                           \tag{FR1}
\]

free incidences on each side. The number of free rectangles is exactly

\[
R_{\rm free}
=\sum_{j\text{ odd}}\binom Lj q^{L-j}[2(q-1)]^j
=\frac{(3q-2)^L-(2-q)^L}{2}.                        \tag{FR2}
\]

**Proof.** For a fixed label choose its odd unequal set. Equal letters
are forced and every unequal coordinate has s containing rectangles.
For the total count, every equal coordinate has q common-letter choices
and every unequal coordinate has `2(q-1)` rectangle choices. All choices
are independent and nonempty. The odd-binomial identities give the closed
forms. ∎

Writing N=q^L gives

\[
R_{\rm free}/N
=\frac{(3-2/q)^L-(2/q-1)^L}{2}\le3^L/2.             \tag{FR3}
\]

The average source-side size is exactly `N lambda_free/R_free`.
Thus endpoint incidence and rectangle output volume differ structurally.
The odd-distance restriction alone does not remove the incidence loss:
for even L, the j=L-1 term gives `lambda_free>=L s^(L-1)`.

## 3. The paired hypothetical improvement

Choose integer `s>=2+2log_2(m)/L`, so q is a power of two with
`q>=4m^(2/L)`. The retained binary direction space has `D<=1+Lq`.
The charged rectangle count obeys
`R_charged<=2^L q^(L/2)`; hence `mR_charged/N<=1`.

The current complete pencil invoice charges endpoint incidences, of scale
`D(1+s)^L`, giving logarithmic excess
`O(sqrt(log m log log m))`. If a new complete endpoint mechanism proved

\[
R_m\le C D(1+R_{\rm free}/N+mR_{\rm charged}/N),      \tag{FR4}
\]

with source/query sharing, occupied auxiliary axes, full normalization
and a charged ordinary local bill, FR3 would instead give
`log R_m=O(log m/L+L+log L)`. Taking even
`L=Theta(sqrt(log m))` gives `O(sqrt(log m))`.
This is a conditional consequence of FR4, not an established compiler.

Together with RV4 in `rectangle-volume-invoice-target.md`, such a pair
of full delivery improvements would match the log-free 2/3 scale.
Interchange would have logarithmic excess `O(y^(2/3))`. A numerical
schedule `log m=Theta(y^(2/3))` would have a local logarithmic bill
O(y^(2/3)) and recursive loss O(y^(1/3)). The difference of
`y^(2/3)` over a step Theta(y^(2/3)) is Theta(y^(1/3)), so the
same strict-majorant proof could close, provided space and preparation
are also paid. Improving only one present logarithmic loss need not
improve the complete envelope.

## 4. The missing physical operation

The source first partial transform is shared across queries after
preparing each incident source's own auxiliary basis. Its later change
to the rectangle's common coset representative depends on the source
and current distinguished query coordinate. Summing input rows before
these changes generally loses the label information needed later.
Applying the whole common kernel separately per query can instead
reintroduce an m factor and destroy the saving.

FR4 therefore requires an actual shared gather/endpoint process. Counting
outputs does not align their inputs, commute label-dependent maps or pay
their partial Fourier transforms. Charged rectangles, free endpoints,
mixing, inverse delivery and tape movement all require a complete bill.
Exact regular incidence rules out improving the same partition merely by
counting it more accurately, but does not exclude another physical
organization or another partition.

Credits: @CubeJerry; the pinned binary Fourier rectangle mechanism;
the prior rational audit; E002 exact-count/frontier work; substantial
ChatGPT multi-agent assistance. No new unconditional multiplication
envelope or runtime lower bound is claimed.
