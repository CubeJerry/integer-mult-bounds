# E003 scientific report: uniformity, endpoint sharing and exact boundaries

Scientific results are assembled below. Actual session completion and
publication status are recorded in `SESSION.json` and the final
append-only log entry.

User-directed interval: **2026-11-25 22:01:09 UTC to
2026-11-26 01:01:09 UTC**. Repository branch:
`research/moonshot-overhead-program`. Concurrent E002, S003 and S004 work
retains its own files and provenance.

## 1. Complete mathematical outcome

The complete written construction admitted in E003 has

\[
T(n)=O\!\left(n\sqrt L\,
2^{O(x^{2/3}(\log_2(x+2))^{1/3})}\right),
\qquad L=1+\log_2 n,\quad x=\log_2 L,
\]

on one fixed exact deterministic finite-alphabet multitape machine, with
one absolute **O(n) bound on all visited tape cells**. This admission is
a written research review, not a proof-assistant artifact. See
`lead/ADMISSION-TWO-SCALE.md`, its pinned component manifest, and
`route-c/REVIEW-LEAD-INTEGRATION.md`.

This is an independent same-scale composition. E002 had already admitted
the same envelope at `8af1911b`, and S003 independently did so at
`2fde2b0c`. E003 does **not** claim a new programme-best complete rate,
priority over those sessions, or the exact endpoint. The pure
`2^{O(x^{2/3})}` overhead, polynomial-x overhead, and O(1) overhead remain
open here. No Weak ETH premise is used for the upper construction.

The proof uses different recursive scales for interchange and Walsh,
and supplies their contracts and the outer caller separately. Fixed radix
three, full-rate packing and fixed-array execution control preparation and
visited space. A sequential rowwise chunk wrapper turns the first
`n poly(x)` space estimate into one absolute linear-space bound without
changing the displayed overhead. No uniform efficiency-family hypothesis
remains in the admission. Exact schoolbook fallback handles all small or
failed-guard cases. An eventual absolute cutoff exists in the proof but
has not been practically evaluated.

## 2. Strongest constructive follow-on: shared Fourier states

Write **ell** for the number of local label coordinates, distinct from
global L. Set

\[
q=2^t,\quad D=2+\ell(q-2),\quad
\lambda=\frac{(1+t)^\ell-(1-t)^\ell}{2}.
\]

The original canonical free routine has axis-call invoice `2D lambda`
per original label row. These are normalized child-transform calls, not
measured machine instructions. Charged rectangles, scalar operations,
metadata, actual tape movement and numerical precision remain charged.

### One destination gauge

A free rectangle with destination span rank r originally ends with
D-r transformed directions. A full auxiliary Fourier gauge can be
shared once at each destination, leaving a residual of only r-1
directions. The complement identity works for degenerate subspaces too;
the fixed auxiliary output phase must be included in the common gauge.

For proper product sides, `r=1+sum_i(s_i-1)`. The changed free invoice is

\[
2(D-1)+2\lambda+4(q-1-t)\lambda'(t).
\]

This saves Theta(t) in the free component for t>=2, using a fixed number
of arrays. Lead and B independently reviewed the identity, physical
schedule and arithmetic, and the lead replayed the complement checks.
See `route-a/ROUTING-DESTINATION-GAUGE-SHARING.md` and its reviews.

Concurrent S004 independently obtained the matching canonical
span-weighted invoice through source/output preconditioning, plus a
two-channel version for asymmetric rectangles. Its complete final note
was read after reconciliation. This overlap carries no priority claim.

### A Gray traversal of prepared bases

Each canonical state has one rectangle incidence per label on each side.
One source array and one destination accumulator can stay in partial
Fourier bases while the state changes. Moving from U to V costs

\[
\dim U+\dim V-2\dim(U\cap V)
\]

axis transforms per half in the specified factorization, plus paid
monomial maps. Common transformed directions and fixed auxiliary phases
cancel; query-dependent phases remain in the middle.

For each odd coordinate support, traverse its levels in reflected Gray
order and return along the reverse path. Contributions are added only
on first forward visits. No numerical snapshots are needed. If
B=2^(ell-1), the exact free invoice for t>=2 is

\[
F_{\rm Gray}=2D+4(B-1)+8(q-2)(\lambda-B)/(t-1).
\]

The lead supplied this order after reviewing A's lexicographic walk.
Uniformly for ell,t>=2,

\[
4q\lambda/t\le F_{\rm Gray}\le19q\lambda/t.
\]

The free component therefore improves by Theta(ell t) against the
original endpoints and Theta(ell) against destination-only sharing.
Lead and B independently accepted the source-compatible fixed-array
schedule and fresh invoice analysis. See
`route-a/ROUTING-STATE-WALK-SHARING.md` and `lead/review-state-walk.md`.

### An exact minimum spanning tree

The lead then proposed a stronger state order. Put a(0)=1 and
a(b)=2^(t-b). The exact transition bill divided by four is

\[
c(s,z)=1+\sum_{i:s_i\ne z_i}(\max\{a(s_i),a(z_i)\}-1).
\]

At an edge-weight threshold, high symbols cannot change. Low symbols
reset to the last level, then parity-compatible zero/last-level patterns
connect by pair toggles. With h high symbols, the exact component count is

\[
C_\ell(h)=
\begin{cases}
(h+1)^\ell,&\ell\text{ odd},\\
(h+1)^\ell-h^\ell,&\ell\text{ even}.
\end{cases}
\]

Kruskal's component-count formula gives the exact minimum tree weight

\[
M=\lambda-C_\ell(t-1)+
\sum_{h=0}^{t-2}2^{t-1-h}[C_\ell(h+1)-C_\ell(h)].
\]

A closed depth-first traversal, adding each state's contribution once,
has free invoice

\[
F_{\rm tree}=2D+8M,\qquad
M\le2q\,2^\ell\ell!\le2q(2\ell)^\ell.
\]

This replaces the Gray estimate's growing power of t with factorial
growth in ell. Its state controls remain within the retained polynomial-m
allowance, and the live numerical arrays are reused. A independently
derived the component formula, bound and executor; B independently
reviewed them. See `route-a/ROUTING-STATE-TREE-SHARING.md`. Optimality
concerns the stated metric's spanning tree, not arbitrary Fourier
algorithms or the shortest open visiting walk.

At ell=4,t=8 the exact free invoices are:

| Schedule | Axis calls per original label row |
|---|---:|
| Original endpoints | 4,234,880 |
| Shared destination | 768,930 |
| Support Gray walk | 603,536 |
| Closed state tree | 140,700 |

These formula evaluations are in `lead/local-invoice-comparison.json`.
They are not runtime benchmarks; independent label volume and the
remaining operations must still be paid.

### Why the complete exponent is unchanged

For q>=4 every tree visits lambda distinct source subspaces, retaining
at least lambda-1 positive transitions and a D boundary charge. The
highest charged Newton coefficient is also unchanged and nonzero.
The resulting subinvoice is

\[
D+\lambda+mD\binom{\ell}{\lfloor\ell/2\rfloor}
q^{-\lceil\ell/2\rceil}.
\]

Its logarithm is at least half of
`sqrt(log2(m) log2(log2(m)))` for m>=2^16. This is a fresh proof for
the changed schedule; the original D-lambda lower argument is not reused
after its mechanism was replaced. At q=2 the free work really collapses
to four calls, while the retained charged term is at least m. The
optimized local leading loss remains on the Psi scale. Applying the
coupled global invoice theorem still requires its **separate positive
normalized routing toll**. These are not universal machine-time bounds.

## 3. Other reviewed contributions

| Result | What it establishes | Scope |
|---|---|---|
| Header-free rational scaling | Height-priced exact scalar processing with an absolute payload-space constant | Polynomial control and rational-height time remain charged |
| Full-rate changing-field packing | Fields can change between completed spatial permutations without inflating original independent volume | No arbitrary change inside masked or numerical intermediates |
| Rational Walsh fixed-array executor | Shared pencils, row mixing, comparison flags and children reuse fixed numerical collections | Written source-compatible schedule, not a full executed multiplier |
| Order-five gate and classification | Short converter/swap words, including a nonsymmetric classification | The specified word pair; other words and larger gates remain open |
| Matrix prediction and port floors | Rank/degree and parity-sensitive restrictions survive the declared row mixing | Representation and positive-invoice results |
| Laminar and maximal rectangles | Exact ordering/hierarchy obstruction; sharp maximal-side load product; rank-essential thinning | General nonlaminar, nonmaximal JR remains open |

The exact free middle kernel exposes a weighted sum of hub transpositions.
A monomial representation needs m terms; a separate support-monotone
circuit theorem restricts shared scalar additions on an injective sector.
Neither establishes m physical interchanges as necessary.

E002's commuting Weyl-family executor remains a positive sharing example.
The star family does not admit its simultaneous diagonalization. For one
signed star sum, an invariant one-exceptional-letter sector supplies an
explicit quadratic spectral factor. The full nonzero binary shift family
has real irrational eigenvalues, already `(-1 +/- sqrt(17))/2` at m=3,
preventing scalar diagonalization over Q(i). Rational blocks or a newly
priced larger field remain possible. E002's later SWAP/Weyl contraction
gate was also read: occupied parameter fields carry independent data and
cannot be silently used as repeated broadcast copies.

The endpoint-gauge obstruction now has an exact directed-graph criterion.
In the graph of separate input/output copies, every component's input
directions must be orthogonal to every output direction in that component.
This parametrizes all allowed gauge subspaces. For a fully retained
orthogonality graph, feasible nontrivial components are complete bipartite.
A norm-one four-vertex path gives a triangle-free obstruction. The model
requires each cross-kernel route to be individually monomial; multiple
gauges and multi-path synthesis remain outside it.

## 4. Finite search outcome

For C(4,3), whole simultaneous translation orbits of product rectangles
have exact minimum common load six, including all nonmaximal product
sides. A difference-cube reduction gives a complete volume proof, and a
96-rectangle witness covers all 1,728 edges at load six on each side.
The lead independently read and replayed this result.

A load-five product partition, if it exists, contains one of three
high-efficiency shapes up to automorphism. The 125,000-candidate search
and three fixed-shape variants timed out without witnesses or
infeasibility certificates. A further restricted warm-start search
retained a verified load-six incumbent and did not settle load five.
These are **inconclusive searches**, not impossibility proofs.
Asymmetric product partitions and correlated sides remain open. The
standalone certificate checker and experiment ledger preserve that
distinction, including the separate C(8,2) load-nine positive control.

## 5. Verification, sources and publication

Verification combines original-source reading, independent AI-assisted
mathematical reviews, exact finite checkers, hash-pinned admissions and
fresh-fetch repository tree comparisons. The final manifest distinguishes
these levels of evidence. Representative exact checks include 4,280
ordered split gates with 144,744 diagonal-word trials; 1,165,984
partial-basis entries; and 15 complete state graphs with 368,280 edges.
The complete composition has its own fifteen-component hash manifest.

The lead read complete primary November tape interchange, permutations,
Walsh, integer and uniformity files; Fourier kernel, binary and repair
files; and September elementary streams. The OpenAI source pin is
`3344da59991ed94f9ba711217b29c1d760badfa6`. The wider archive and
literature/priority audit remain partial. `lead/EXTERNAL-LEADS.md`
records the actual external reading scope.

No full multiplier was executed, no formal refinement was built, and no
human refereeing is claimed. The practical eventual cutoff was not
evaluated. A formula, finite replay, reviewed construction and measured
machine runtime are different kinds of evidence here.

Progress was regularly committed and published with expected-head checks,
concurrent reconciliation and fresh-fetch tree verification. Verified
pre-close checkpoints include `efd0c7be`, `df91e4c8`, `3b220847`,
`d88a36ee`, `8fbe12b3` and `baeb200f`; close checkpoints are recorded in
`SESSION.json` and the final log. E003 created no upstream PR.

## 6. Precise handoff

The canonical state metric now has an exact minimum spanning tree, and
the retained charged term still fixes its leading invoice scale. Further
progress requires a changed mechanism:

1. Combine contributions without separately visiting every prepared source
   state, or share actual middle routing with a smaller fully priced toll.
2. Construct noncanonical rectangle geometry with small spans and low joint
   loads. The proved hierarchy, maximality and translation-orbit restrictions
   leave unrestricted JR open.
3. Supply a compact rational block form or priced algebraic basis for the
   balanced signed-star operator, preserving arbitrary occupied rows and
   composing across the complete predictor, including mixed rectangle terms.
4. Strengthen independent or formal review of the full numerical and
   fixed-machine composition, including its absolute visited-cell cap.

Credits: research directed by @CubeJerry; pinned OpenAI source manuscripts;
the community predecessor lineage; concurrent E002/S003/S004 contributions;
and substantial ChatGPT multi-agent assistance. No literature priority or
independently measured performance claim is made.
