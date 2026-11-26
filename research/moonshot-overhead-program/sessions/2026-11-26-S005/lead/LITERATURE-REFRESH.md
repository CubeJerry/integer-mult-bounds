# Scoped fresh literature and source refresh

No exhaustive priority search or general novelty claim is made. These
leads bear directly on the layout questions; their stated algorithms
are not imported as unaudited physical primitives.

## Stable tape sorting, revision of 25 November 2026

Yann Tal, *Sorting in o(N log N) Time on a Multitape Turing Machine*,
ECCC TR26-331, revision 1:
<https://eccc.weizmann.ac.il/report/2026/331/revision/1/download/>.
The report page dates this revision to 25 November 2026; it supersedes
the original 22 November bound for this comparison.

The lead read the introduction/results, tape model and interchange
interface, and Appendix A's wide-string construction through its
recurrence setup. The paper states stable sorting of n records of total
bit volume N, including payloads, in
N log(n)/(log log log(n))^(1/2-o(1)) time and O(N) space. Its wide-string
theorem reaches QB(log Q)^(1/2+o(1)) for Q destination-labelled strings
of width B>=2^(Q^alpha), fixed alpha>0, using the current interchange
result. The complete sorting proof and two-tape appendix were not audited.

**Programme inference.** For 2^a records of width k polynomial in a,
the stated general expression is Va/(log log a)^(1/2-o(1)), still
larger than V sqrt(a) times any fixed power of log a. The wide-string
condition needs k>=2^(2^(alpha a)), absent at the main caller. Relative
record widths can increase deep in recursion, but earlier levels and
uniform constants would still need payment. This comparison is not a
lower bound on a structured converter.

## Subspace convolution and formal scope

Shlomo A. Perles and Omri Weinstein, *A Fast Algorithm for Subspace
Convolution*, 2026. Primary repository:
<https://github.com/shlomi-perles/subspace-convolution/tree/f9b0a122432aa18f3ce292fc798437c1b5bc2692>.
Route A's relevant paper-section reads are recorded in its flag-converter
note. The lead independently read the repository overview and operation
model portion of `lean/README.md`. The documented formal costs are
nonuniform straight-line-program gates; index construction with its
ambient-dimension polynomial factor is outside that formal model.
No local Lean build or independent complete paper reading is claimed.

**Programme inference.** Scalar subspace-indexed inputs do not retain
all independent ordered-frame payloads in RO. Frame changes and physical
index costs must be proved before importing an arithmetic estimate.
SF independently supplies the all-frame Fourier identity and keeps its
physical converter open. The new polynomial-CRT caller is a distinct
proposal; neither literature item solves its transform gate.

Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance.
