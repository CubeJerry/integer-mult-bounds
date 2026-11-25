# E001 research report: epsilon decay and uniformity

Session completed:2026-11-25 13:25:26 UTC to16:26:41 UTC,
10,875 actual seconds (at least the requested three hours). In Melbourne
this is26 November,00:25:26 to03:26:41.
The work is saved to the programme branch; no background research remains running.

## 1. Strongest complete envelope in the shared programme

Let
\[
L=1+\log_2 n,\qquad x=\log_2 L,\qquad z=\log_2(x+16).
\]
The strongest accepted written construction currently in the shared programme is
\[
T(n)=O\!\left(n\sqrt L\;
 2^{O\left(x(\log_2(z+2)/z)^{1/3}\right)}\right),
\qquad\text{visited cells}=O(n).
\]

This is S002's fixed-field theorem at
[848fbf1](https://github.com/CubeJerry/integer-mult-bounds/blob/848fbf1d7a5e192aa352d79b4d3e36fa06be21ee/research/moonshot-overhead-program/routes/A/fixed-field-extraction-theorem.md).
Its count construction, complete physical composition and eligible parameter
choice passed S002's separate B, C and lead reviews. E001 root read the new
finite construction, complete theorem, lead review and historical bridge.
E001 independently passed the [finite count audit](route-c/S002-COUNT-FORMULA-REVIEW.md)
and [physical composition audit](route-a/S002-FIXED-FIELD-REVIEW.md). Root
read both receipts in full. Their precise division of review scope is explicit.

The claim is one fixed exact deterministic finite-alphabet multitape machine,
contiguous binary inputs and full output, actual head movement and generation
charged, and a uniform bound on all cells ever visited. Correct fallback covers
every input length. No new representation hypothesis, Weak ETH premise or
old five-assumption interface is used in this upper bound.

The residual exponent is explicitly
\[
\delta(n)=O((\log_2(z+2)/z)^{1/3}).
\]
This result does not establish bounded overhead, polynomial overhead in x,
or a bound of the form \(2^{O(x^\beta)}\) for any fixed \(\beta<1\).
No kappa on the polynomial-in-x benchmark scale is assigned.
Constants and the eventual cutoff are not numerically evaluated.

The result is a mathematical algorithm/profile construction. It is not
a practical implementation, full astronomical-template execution, Lean
refinement, human referee report or literature-priority certification.
The comparison is among explicit upper envelopes in this programme,
not against the unknown actual residual term in the published theorem.

## 2. This focused session's independent complete construction

[THEOREM.md](THEOREM.md) proves the separate dyadic envelope
\[
T(n)=n\sqrt L\;
2^{O\left(x\left([\log_2(z+2)]^2/z\right)^{1/6}\right)}
\]
with the same exact model and common visited-space guarantees.
Routes A, B, C and root supplied separate written audits.

The new algebraic construction replaces the source's literal monomial tensor
representation. Balanced variable splitting yields an actual, fully unfolded
arithmetic formula of size \(2^{O(\log^2m)}\) and syntactic degree
\(D=O(\sqrt{m\log m})\). A cyclic factorization keeps every rotated product
equal to the computed scalar times the entire identity.

Products concatenate factors on separate tensor coordinates. Sums use the
known graded tensor construction; integral Gaussian-binomial cancellation
prevents division by odd integers. All internal root orders lie in one
explicitly generated cyclotomic ring. A final cyclic block and regular
representation give a dyadic affine pencil satisfying
\[
L_m(X)^b=P_m(X)I
\]
on every independent input coordinate. There is no free initialized
workspace or designated-output interpretation.

The matrix dimension, expanded coefficient output, actual generator time
and workspace are all bounded by
\[
Q_m\le 2^{\,2^{C(\log_2(m+2))^2}}.
\]
All shifts, repair tables, finite-field specialization and both the interchange
and numerical Fourier branches are charged. The refined rational-address
proof controls numeric values as well as bit lengths.

With \(Z_j=(j+2)^3\log_2(j+3)\), the full finite budget is
\(S_j\le E_2(CZ_j^2)\), where \(E_2(t)=2^{2^t}\).
The physical compiler, exact fallback, common-space chunking and actual
weighted schedule then give
\[
d_j,b_j\le 2^{CZ_j^2}.
\]
Choosing an eligible integer \(j\) proportional to
\((z/[\log_2(z+2)]^2)^{1/6}\) proves the displayed rate. The index is an
analysis witness for one fixed machine, not uncharged input-dependent advice.

S002 independently reached the same formula envelope at58c754b. Both
derivations are preserved with separate provenance. S002 then improved it
using characteristic-two carry formulas: their fully unfolded bit formula
size satisfies \(S_{r,k}\le8^r\binom{r+k}{k}\), while the degree budget is
\(2^k\). This produces the needed count coefficients with polynomial formula
size. The characteristic-two construction is not syntactically multilinear
as a formal polynomial and does not establish E001's different dyadic MR
hypothesis.

The earlier baseline theorem is preserved byte-for-byte in
[BASELINE-THEOREM.md](BASELINE-THEOREM.md), so its historical review hashes
remain meaningful.

## 3. Uniformization certificate: what was proved and what it means

[CERTIFICATE.md](CERTIFICATE.md) reconstructs the source actual-step guarantee,
including initialization, generation, clocking, aborted attempts, cleanup,
interpretation and output. For a complete admissible attempt define
\(D_j=2^{i_j}A_j\), \(d_j=\log_2D_j\), and
\(b_j=\log_2(1+\log_2N_j)\). Its sufficient envelope is controlled by
\[
F(x)=\inf_{j:b_j\le x}\left(d_j+\frac{x}{j+2}\right).
\]

The constant-overhead coverage criterion accounts for nonattained infima:
eventual boundedness requires coverage of attainable x by the intervals
\([b_j,(j+2)(K-d_j)]\), with a fixed enlargement or arbitrarily small slack.
An infinite subsequence of bounded constants alone does not control late
applicability thresholds.

If \(d_j\to\infty\), then \(F(x)\to\infty\). Under the explicitly specified
full sum-diagonal enumeration, the stronger restricted estimate
\(F(x)\ge c x^{2/3}\) is proved. These are lower bounds for that sufficient
certificate. They are not lower bounds on actual scheduler running time or
on integer multiplication. A tighter analysis or another mechanism can evade
them.

Exact integer and sparse parameter choices, joint threshold checks and
effective-but-arbitrarily-delayed family examples establish why fixed-epsilon
asymptotics alone do not supply a decay rate.

## 4. Concrete obstructions and directions that remain open

The [matching recipe theorem](route-c/FORMULA-RECIPE-LOWER-BOUND.md) reduces
the published Hrubes–Yehudayoff homogeneous multilinear formula lower bound
to the matrix rank actually charged by the unreduced cyclic recipe.
Only additions of degree at least two multiply the rank. Compressing the
other parts produces a formula of size \(O(mD(s+1))\), where s counts those
expensive additions. Hence the retained source window forces
\[
K\ge2^{\,2^{\Omega(\log^2m)}}.
\]
This matches the scale of the balanced construction within that exact class.
It leaves nonmultilinear cancellations, Boolean-quotient identities,
invariant summands, different composition rules and changed repair open.
S002's carry method illustrates why those restrictions matter.

Other reviewed results include:

- Gram rank and reserve constraints force opposite-parity count aliases
  modulo the source odd characteristic; count-only scalar reduction fails.
- The literal transfer modulo the square of that characteristic has a
  quantified large factor rank. This does not cover arbitrary corrected lifts.
- Exact Hamming-window parity has degree and affine-query depth at least
  the window width. The specified all-shift, window-marked full-conversion
  resource tradeoff is \(\Theta(\sqrt{m\log m})\), with its scope explicit.
- Input-dependent compatible radices repair a literal padding obstruction,
  including actual prime search and bounded or summably small volume loss.
  The complete varying-radix physical address compiler remains open.

[FORMULA-SIZE-TRANSFER.md](FORMULA-SIZE-TRANSFER.md) proves a general complete
conditional conversion from degree-preserving dyadic formula bounds to
overhead rates. The dyadic MR hypothesis would attain the same rate as
S002's current fixed-field construction, but remains a separate open
algebraic claim.

The [bounded-preflight theorem](route-b/preflight-selection.md) proves
\(H=O(x^a)\), including the endpoint at a=0, under explicit actual physical
family, generation and threshold hypotheses. Those stronger hypotheses are
not established. The variable-arity interchange implication is also complete
conditionally, but does not by itself give a complete multiplier.

## 5. Dominant remaining obligation

For the current strongest construction, the retained parameter and finite-data
profiles are
\[
\log m_J=O(J^3\log J),\qquad
P_m\le2^{m^C},\qquad
\log D_J,\ \log L(N_J)\le2^{O(J^3\log J)}.
\]
These joint prefactor and threshold costs determine the available rate.

A consequential next step is to improve the complete routing/representation
profile while preserving all input rows and actual tape access, or to
construct the precise stronger preflight family. A symbolic small matrix,
a circuit with shared internal values, or an uncosted algebra basis is
insufficient. The numerical Fourier branch, precision, repair, threshold
and common visited-space constraints must still compose.

## 6. Verification, source pins and publication

Root independently replayed the new formula checker in an isolated Python
process: 84 predictor cases,152 cyclic-product identities and72 complete
descended matrix-root checks, maximum dimension96. It includes wrong-phase,
unequal-padding, non-Boolean-shift and nonsemisimple characteristic-three
controls. Earlier separate checks cover repair, scalar units, window tails,
radix selection, p-adic factor ranks, scheduling, chunk products and carries.

The universal asymptotic statements rest on the written proofs, not on those
finite enumerations. [REVIEWS.md](REVIEWS.md) identifies actual readers,
snapshot hashes, reruns and limitations. S002's own exact replays are
credited separately and are not represented as E001 executions.

Source branch heads were rechecked unchanged at16:20:39 UTC; the two prompt
blobs were separately verified unchanged at16:15:45 UTC:

| Source | Revision |
|---|---|
| OpenAI math |3344da59991ed94f9ba711217b29c1d760badfa6 |
| CrocSwap canonical main |e54523517d0f03e58352e647c403a5af3e525a57 |
| Prompt repository |02d6478f212049f92a68f3d622604bf26bff9cee |
| Focused prompt blob |ce6fe4edbf039aa964a08aaec216a1cc60dbfe2a |
| Parent prompt blob |b5762a4dacb999703e83621301a455fbb12755f7 |

The sixth focused checkpoint is d1f3baccdcc547263c0c0cc7241aa0cb1ef12bee,
verified on research/moonshot-overhead-program. Concurrent S002 changes
were read and preserved. A transient lease-update error was resolved using
a freshly checked fast-forward-only update; no history was forced.
Concurrent closing commit28a7435337195b837f35dac12bedc31a0eea77ce was read
and preserved. Its optional prime-carry and structured-check refinements
are preserved without a fresh E001 proof audit or stronger global claim.
The final session completion and subsequent reconciliation are recorded
in SESSION.json and the append-only logs. No upstream PR was opened.

Credit: @CubeJerry, the OpenAI manuscripts and cited predecessors,
established matrix-factorization and arithmetic-formula results, the
concurrent S002 work, and substantial GPT-6 Astra Pro assistance from the
lead and three separate task agents.
