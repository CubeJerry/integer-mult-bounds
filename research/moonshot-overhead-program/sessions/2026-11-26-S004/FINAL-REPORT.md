# S004 final research report

Session: **2026-11-26-S004**. Requested active research interval:
**2026-11-25 22:01:15 UTC to 2026-11-26 01:01:15 UTC** (three hours;
09:01:15 to 12:01:15 Melbourne on 26 November). Active research completed at **2026-11-26T01:01:30Z**, after **10815 seconds**, satisfying
the full three-hour request. See [SESSION.json](SESSION.json) for the complete
record. Final publication and remote verification follow this closing record.

## 1. Outcome and proof status

The session produced reviewed conditional theorems, exact local Fourier
compilers, residual-correction constructions, and restricted-model obstruction
results. **S004 does not claim a stronger unconditional complete multiplication
bound than the concurrently admitted project result.** It does not determine the
optimal overhead exponent or reach the polynomial-overhead target.

Write `L=1+log2(n)` and `s=log2(L)`, and normalize time by
`T(n)=O(n sqrt(L) H(n))`. Complete constructions use a fixed deterministic
finite-alphabet multitape machine, output the full integer product, and use one
`O(n)` bound on **all tape cells ever visited**. Address movement, numerical
precision, effective preflight and recursion interfaces are charged.

| Conclusion | Status and attribution |
|---|---|
| `H(n) <= 2^{O(s^(2/3)(log2(s+2))^(1/3))}` | Current complete **written unconditional** project construction, first admitted in concurrent E002; S003 and E003 supply same-scale work. This is not an S004 discovery. |
| `JR => H(n) <= 2^{O_c(s^(2/3))}` | S004's complete **conditional written** transfer. JR is an explicitly open combinatorial hypothesis and the sole additional mathematical hypothesis in this transfer. |
| `H(n) <= s^a`, including constant overhead | Not established. |
| General multiplication or physical-routing lower bound | Not established by the restricted-model results below. |

The unconditional reference is E002's
[variable-profile theorem](../../results/epsilon-uniformity/sessions/E002/lead/variable-profile-theorem.md)
and [admission](../../results/epsilon-uniformity/sessions/E002/lead/ADMISSION-V.md).
The S004 conditional result is
[the two-scale transfer, Section 9](route-a/joint-rectangle-two-scale-transfer.md),
its [independent review](route-c/REVIEW-JOINT-RECTANGLE-TWO-SCALE.md), and
[second-wave admission](lead/SECOND-WAVE-ADMISSION.md).

These are AI-assisted mathematical drafts with independent agent review and
finite exact checks. They are not formal proofs, human referee reports, a full
machine implementation, or a claim of literature priority. Constants and an
actual numerical crossover have not been evaluated.

## 2. Conditional transfer and remaining combinatorics

For `q=2^t`, JR asks for an exact disjoint rectangle partition of the graph on
`[q]^k x [q]^k` whose edges have unequal endpoints in every coordinate. It asks
for a fixed integer `c>=2` with maximum per-side vertex load at most
`c^k(t+1)^c`, for every `t,k>=1`. Rectangle sides may have arbitrary internal
correlation. The transfer includes effective exhaustive certificate search,
its workspace and preflight cost; it does not assume a free partition oracle.

The two-scale composition with the admitted variable-profile compiler removes
the extra logarithmic factor in the exponent **if JR holds**. An earlier `3/4`
exponent is historical and superseded. A weaker rationally weighted odd-Hamming
rectangle-decomposition interface, OWL, was also isolated, including coefficient-height and
local-load charges. Its associated global construction gate remains open.

Local-load restrictions and a globally optimal load-three partition of
`C(4,2)` were verified. Neither this finite case nor fixed-alphabet products
proves JR. Full matrix rank forces many rectangles but does not by itself force
large vertex loads. The partition problem remains the principal conditional gap.

## 3. Fourier compilation: concrete savings and a fresh limit

Endpoint preconditioning moves an endpoint-dependent auxiliary transform outside
repeated incidences, with an explicit rank-weighted charge. It preserves the
correct order of phase multiplication and Fourier inversion. A symmetric
two-channel destination formula is also proved.

Two further constructions share more work. The source graph adapts a basis to
nested prefix flags, makes actual copies at branches, and transforms only new
axes along each edge. The destination graph receives **independent** rectangle
arrays and accumulates them bottom-up. Its shear identity includes the required
controlled sign when a representative has selected internal components. The
proof retains one leaf-axis transform per incidence, ordinary maps, copying,
additions, precision guards and common visited-space obligations.

| Alphabet `q`, block length `L=4` | Original local calls | Endpoint preconditioning | Source sharing | Both sharing graphs |
|---|---:|---:|---:|---:|
| 4 | 800 | 306 | 230 | **154** |
| 8 | 6,240 | 2,082 | 1,342 | **630** |
| 16 | 31,552 | 9,282 | 5,502 | **1,906** |
| 256 | 4,234,880 | 768,930 | 404,510 | **53,650** |

These are exact **local call-list** counts, not measured total runtimes.
References: [endpoint preconditioning](route-a/fourier-endpoint-preconditioning.md),
[source sharing](route-a/nested-fourier-source-reuse.md),
[destination accumulation](route-a/shared-fourier-destination-accumulation.md), and
[independent destination review](route-c/REVIEW-SHARED-FOURIER-DESTINATION.md).

The cost analysis was rederived after changing the executor. For `x=log2(m)>=16`,
the retained positive invoice `J0=D+lambda+m D rho/N` obeys
`log2(J0)>=sqrt(x log2(x)/2)`, with matching constructive order in this family.
This is an invoice theorem for specific incidence and rank charges, **not** a
runtime lower bound against every possible executor. See the
[new invoice proof](route-a/shared-fourier-invoice-scale.md) and its
[review](route-c/REVIEW-SHARED-FOURIER-INVOICE-SCALE.md).
Concurrent E003 independently obtains overlapping state-sharing and invoice
conclusions; no exclusive S004 priority is claimed. The [canonical leaf classification](route-a/fourier-leaf-line-classification.md)
removes the selected-internal sign in one specially chosen basis. At `q>=4`,
distinct rectangle spans share no odd geometric line; this only excludes that
specific grouping mechanism. At `q=2`, all free calls really collapse to four,
but any compatible charged correction matrix has rank at least `N/2`, leaving
a charged coefficient at least `m`. The literal incidence invoice is therefore
not applied to this exceptional changed executor. The overlapping state and
binary-exception facts retain concurrent E003 attribution.

## 4. Exact correction and a complete, slower supplier

Several complementary residual interfaces now have explicit algorithms:

- A promised signed sparse residual is recovered deterministically by folded
  products and isolation, with height, arithmetic and workspace costs.
- A nonnegative residual admits a sound budgeted certificate using mass and
  first/second moments. False sparsity budgets do not produce false acceptances;
  the analogous unrestricted signed assertion is explicitly rejected.
- A dense residual satisfying a short forward recurrence can be recovered. The
  tall-Hankel variant specifies its exact prefix, tail and rank conditions.
- A dense bounded-amplitude residual is corrected by a classical triadic modular
  multiplication construction with an explicit fixed-tape stack schedule. Dispatch,
  cleanup, coefficient reduction and any scalar mass product are charged.
- Dense-small residuals with a sparse set of large outliers combine the amplitude
  and sparse routines. Signed and one-sided promises have different certification
  guarantees, stated separately.

A fast corrector alone does not provide a fast all-input supplier. The session
therefore constructed a complete supplier: a deterministic dyadic FFT, with
effective integer square roots, fixed precision and sequential twiddle streams,
emits `C` with `0 <= (AB)_i-C_i < M` on every input. The actual triadic engine
then computes the residues needed to recover the exact product.

**The clean composition uses least nonnegative residues modulo `M`.** A centered
amplitude interface instead needs its own modulus greater than twice its residual
bound; at most `2M` suffices here. Centered lifting modulo `M` would be wrong at
`M=2`, where the residual may equal one.

The supplier has one `O(h(b+log h))` visited-cell bound and charges roots, every
FFT stage, fixed-width arithmetic and stream movement. In the ordinary packed
regime, choosing the fixed budget `a=1` (`M=2`), its complete time is `O_alpha(n log n (log log n)^alpha)` for fixed
`alpha>1/2`. **This is slower than the current project bound.** It establishes
a fully paid supplier bridge and identifies why this full-word schedule misses
the target. Classical FFT and modular multiplication ingredients are attributed.

References: [amplitude correction](route-b/bounded-amplitude-residual-repair.md),
[hybrid correction](route-b/dense-small-sparse-outlier-repair.md),
[FFT supplier](route-b/certified-fft-lower-candidate.md),
[A review](route-a/review-certified-fft-supplier.md), and
[C review](route-c/REVIEW-CERTIFIED-FFT-LOWER-CANDIDATE.md).

## 5. Obstruction results and their boundaries

The linear-query route includes direct queries, inverse queries, changing row
widths, noncommuting numerator/denominator matrices, singular-denominator nullity,
and rank-limited ports. Proofs retain actual occurrences and active-row costs.
Subset spectra are treated through actual multiplicities and ratio subgroups;
unsupported full-root assumptions are not imposed on smaller alphabets.

The final bridge works directly with **actual swap orbits**, including
characteristic two. It uses permutation orbits rather than diagonalization.
For `m` field pairs with sizes `q_j`, put `pi0=product(1/q_j)`. The inequality is

`E + H/W + eta1 (Qd+2Qi)/W >= (1-pi0)/2`,

with `eta_d=O((d+1)/sqrt(m))` for fixed support degree. Here `E` is normalized
actual rank error, `H` total port rank in payload units, `W` payload rows, and
`Qd,Qi` active direct/inverse query volumes. The identity predictor attains the
baseline exactly. Arbitrary address masks, comparisons, payload permutations,
nonlinear suppliers and efficient physical inversion remain outside this model.
See [actual swaps](route-c/nonsemisimple-physical-swap-corollary.md) and its
[independent review](route-b/review-nonsemisimple-physical-swaps.md).

Other gates are similarly scoped. The fixed nonnegative bilinear model has the
sharp product count `h^2-S h+floor(S^2/4)=floor((2h-S)^2/4)` under its one-sided
mixed-error promise with `0<M<=U^2` and `0<=S<=2h-1`, where `U` is
the input amplitude. This is not a general bit-operation bound; the classical
zero-error `h^2` result is attributed. Missing-input and bilinear-energy gates
allow adaptive outlier positions while retaining their information or algebraic
restrictions. Finite two-converter repair-tree floors do not exclude every
architecture or an unproved one-converter construction.

## 6. Verification actually performed

Admitted components have written proof reviews, exact checkers and source-scope
records. Examples from the final waves are:

| Verification | Exact finite coverage |
|---|---|
| Destination shears and accumulation | 164,932 shear entries; 9,250 independent-input output entries; 52,304 adverse entries with the required sign omitted |
| Certified FFT supplier | 217 complete cases; 2,542 residual coefficients; 37,148 rounding controls; 2,229 fixed-precision stages |
| Actual FFT plus triadic correction | 34 complete cases; 568 corrected coefficients; 16 maximum-digit controls; mass and integer carry identities |
| Actual swaps | 1,461 boundary-column checks; 14 exact baselines; characteristic-two inverse and mixed-stratum controls |

The lead independently replayed these final checkers in isolated directories.
Finite calculations do not execute the abstract fixed-tape algorithm or prove
asymptotic statements by themselves. Physical time and all-visited space are
supported by written constructions. Hash manifests describe the commits
containing them; later revisions may intentionally have different bytes.

## 7. Publication and remaining questions

Work is integrated into the requested fork on
`research/moonshot-overhead-program`. Concurrent S003, E002 and E003 work is
preserved without force-pushing. No upstream pull request was opened.

| Saved checkpoint | Commit |
|---|---|
| Setup | `842f879d3adf45b86d38cf3ff52dbead638cfe74` |
| First wave | `04c1cb0da225d990d65aef86006cadbd929e0e31` |
| Second wave | `af5d7983fce7c50a8df5fe13428e587e96543727` |
| Third wave | `39b90725c48b732307be587b8cb53e1b2d0e3fc0` |
| Fourth wave | `e2f2eac3743b6f0e807ec460369fd5ec6931b46c` |
| Fifth wave | `62d9d8e917379cb2edc17c9761e12e2345bc01f4` |
| Final report and closure | Commit containing this report and finalized SESSION.json |

The concrete unresolved tasks are to prove or refute JR at growing alphabet
and dimension; share remaining leaf transforms with a full physical invoice;
supply the correction routines at competitive time; or develop an invariant
covering physical addressing beyond the current query algebra. These are open
steps, distinct from the constructions and finite checks completed here.

Prepared for @CubeJerry with substantial ChatGPT assistance.
