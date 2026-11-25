# Independent review of the asymmetric nested-label invoice obstruction

Reviewer: S003 Route C. Status: **accepted within the stated exact-family,
literal-invoice scope**. No lower bound on general physical routing or
integer multiplication is asserted.

Reviewed in full: `../route-a/nested-label-invoice-barrier.md`, Theorem N
and N1--N10, against the preceding characteristic-two construction in
`routes/B/characteristic-two-label-geometry.md`. Programme baseline:
`0607d044d1d09489580da0e5828588820e1a6775`; source OpenAI math:
`3344da59991ed94f9ba711217b29c1d760badfa6`.

Route C independently derived the symmetric two-level case and the
restricted tensor-domain rank witness before reading A's general theorem.
The narrower proof is retained as `SYMMETRIC-LABEL-INVOICE-LOWER-BOUND.md`.
A's theorem adds arbitrary nesting, asymmetric power-of-two distances,
exact rational Gram dimension, and the unrestricted actual rank term.
These are a related extension and independent corroboration, not two
unrelated discoveries.

## Identities and actual rank

For each pair of labels differing in `k` immediate coordinates, every
surviving term of `e_d(P_prev[1],...,P_prev[2d-1])` must select all changed
coordinates. If a changed pair is not far, its entry vanishes. Otherwise
the remaining choices give `binom(2d-1-k,d-k)`: this is one modulo two
exactly for `k=0,d`, and zero for `0<k<d`. This verifies the recursive
diagonal-plus-far support. The endpoint `k=0` uses that `2d-1` has all
low binary digits one; the other vanishing coefficients follow directly
from Frobenius and do not require division.

The square-zero induction starts from the even-order all-ones matrix.
Commuting tensor summands square separately in characteristic two.
Restriction to a complement of the kernel in `d` coordinates and to the
kernel in `d-1` coordinates leaves exactly one injective summand. This
proves N5 for arbitrary nonzero square-zero maps, not merely generic maps
or tested selectors. The exponent `P(t+1)-1` in N6 follows from the exact
telescoping sum and is uniform in the nesting depth.

## Literal rectangle and rational Gram bills

The prescribed-side incidence count is an equality for the retained
first-differing-bit product construction. Every word has exactly one
containing rectangle for each possible first differing bit, at each
unfixed differing coordinate. Higher-level products preserve equal
incidence and the absence of far pairs inside a side. This does not prove
that the cover is optimal over all possible covers.

The far adjacency has odd degree and is invertible modulo two because its
sum with the identity is square zero. Its rational restriction to the
sum-zero subspace is therefore invertible. The Gram matrix's plus block
has rank one; its minus block has one full nonconstant-coordinate
subspace for each top-level coordinate, and vanishes on tensors with two
or more such coordinates. Its constant mode cannot vanish:
`n*d=2*h*delta` would equate a power of two with 2-adic valuation at least
two to a number with valuation exactly one. Thus
`D=2+h*(n-1)` is exact. The proof keeps rational address rank separate
from binary scalar rank.

## Quantitative implication checked

Write `x=log2 m`, `P=product d_i`. From the actual rank factor, without
any occupancy cap,

    x/J >= x-P(t+1)+1,       hence x<2P(t+1)<=4Pt.

Keeping only the first-level incidence already gives

    x >= (JP/2)(1+log2 t).

For every real `J>=64`, these imply `t>=J/8>=8`, hence
`log2 t>=log2 J/2`. The Gram factor then forces `d_ell>J/4`; the
`(q-1)^(P/d_1)` incidence factor forces `d_1>J/8`. As every intermediate
distance is at least two,

    P>=2^(ell-2) J^2/32,
    x>=2^(ell-2) J^3 log2 J/128.

All inequalities have the indicated directions, and no bound hides a
constant depending on depth. The hypothesis `m>1` is sufficient: feasibility
of the stated invoice already forces large `m`; the proof does not need a
separate unmentioned cutoff. Powers of two are required for the selector
identity and are explicitly part of the theorem.

## Scope and publication judgment

The result genuinely closes the proposed strategy of improving the arity
scale merely by optimizing distances, adding these same label levels, or
using exact rank in the same billed construction. It does not lower-bound
actual execution time from an upper-bound invoice. A better executor at
the same arity, another rectangle partition, another endpoint representation,
or a different recurrence is outside the statement. A smaller true finite
template profile could still improve the global overhead at unchanged
arity. These limits are correctly stated in A's note.

Finite checks of the symmetric construction have been run separately by C
and are recorded beside its narrower theorem. C also replayed A's unmodified
`verify_nested_label_barrier.py` in an isolated temporary directory: four
actual matrix cases, nine arbitrary square-zero tensor cases, three Gram
rank cases, 1,089 depth/asymmetry cases and nine sufficient-invoice cases
passed. `independent-a-nested-replay.json` records the exact source SHA-256.
The unbounded theorem
rests on the algebraic and quantitative proof above. No Lean build, human
review, full multiplier execution, or endpoint theorem is claimed.
