# Independent review: historical normalization with Y feedback

## Verdict

The proposed normalization and its physical arrival implication are sound under the explicit route and cache assumptions in the frozen proof. Allowing arbitrary cocharted Y feedback, arbitrary singular aggregate packet-through cells, and extra ascending zero-born records does not bypass the fitting/arrival constraint. No complete source or new kappa follows.

I focused on the ground boundary, kernel/image bookkeeping, local x support, and the additional-copy accounting. I did not repeat the E7, binary quotient, or price catalogues. The finite checker ran successfully, but its 2-by-2 F2 cases are controls; the universal result rests on the cell-complement algebra and chart-poset induction.

## Ground boundary and singular cells

For each descending packet, `Z_p` must be its value on first arrival at chart 0, before any ground ADD, swap, cancellation, or CLEAR. This handles packets that arrive at different times and any stationary ground history. Every ground history is then a linear function of the actual `Z_p` values and original `y` inputs; it has no additional local x source because original X inputs start on nonzero root lines. The first-ground control in the checker demonstrates why a value captured only after ground mixing could lose x information.

At a proper nonzero chart, the aggregate cell identity `P_out=C U_in+D P_in` remains valid with chronological Y/X/packet feedback because the independent boundary variables are substituted only after aggregating the actual local program. For arbitrary singular `D`, choose a kernel complement, a generalized inverse `R`, an embedding `J`, and coordinate map `h` with `RD=I-Jh`, `DJ=0`, `hJ=I`, and `hR=0`. Then for the actual history coordinate `T=hP_in`,

`P_in = R(P_out-CU_in) + JT`,

and the compatibility condition `(I-DR)(P_out-CU_in)=0` must still hold. This is algebraic normalization of the actual history, not a new freely available read. Every internal cache/history is a linear expression in the boundary values and `P_in`, so substituting this identity isolates all kernel information in `T` and does not lose histories annihilated by `D`.

With `G=(Z_p,T_C)`, there are at most `qV+Σ_C ν_C` x-information dimensions. Each packet visits at most one chart at each of the seven proper nonzero dimensions, so `Σ_C ν_C≤7qV` and `rank(G_x)≤8qV`. Singular feedback cells are covered; image compatibility is not discarded.

## Symbolic Y nuisance and locality

Treating original `y` as a symbolic nuisance is safe because its coefficient has zero x projection. A Y record can acquire x through feedback, but the acquired x part is separately normalized into global history `G` or a local remainder; it is never called pure y. At chart 0 all x arrives through first-ground packet values. At a higher chart, every ascending X/Y/additional-record boundary value has a normalized predecessor remainder supported inside its predecessor chart; original X born at the chart is local there; a descending packet's outgoing value is the incoming value at its next lower chart, already normalized in the low-to-high induction. The generalized-inverse identity adds only `T_C` to the global part. Left multiplication by arbitrary, possibly noncommuting block maps preserves the set of x columns, so every local remainder at C is supported on original X lines contained in C.

This induction is consistent with interleaving: it is a statement about the linear identities of the full finite cell, not a claim that formal boundary variables were simultaneously available. Physical chronology still must be checked separately for any construction.

## Terminal facet arrivals and extra copies

At final facet `F_i`, the local x support is covered by at most `1+r_i+a_i+s_i` proper subspaces: the last proper predecessor of its own Y path; one predecessor for each original X path arriving at `F_i`; one for each separately paid extra ascending record; and the first proper lower successor for each descending packet visiting `F_i`. Other original Y paths cannot visit `F_i`, since distinct same-dimension terminal facets are incomparable. A zero-born stationary cache at `F_i` adds no source subspace; any nonzero content came from one of the counted arrivals or from `G`.

The E7 bounds then imply `ell_i(A)≤r_i+a_i+s_i`: if the foreign fitting support exceeds 36 it needs at least two subspaces; if it exceeds 52 it needs at least three. The base Y predecessor is the first subspace, so the two thresholds require respectively at least one or two further arrivals. Summing gives `Σell_i≤111+q+Σa_i`, because each monotone original X or packet path can visit at most one distinct rank-seven facet. Each additional record arriving at a facet must have been born below it and physically MOVE there; copies born at the facet are zero and do not add x support. A copied Y value or a stationary cache is not free arrival credit.

For the q8 target, the stated movement-only invoice permits at most three additional unit-rank facet arrivals at any finite admissible even multiplicity, and only one at m=6. Thus its generous all-finite allowance is `111+8+3=122`. The scalar-F2 fitting theorem says a fitting with quotient dimension at most three needs at least 123 arrivals. This algebraic implication applies to the newly derived Y-feedback arrival bound; it does not claim the old no-Y-feedback source theorem itself covered Y feedback.

## Scope and interpretation

The quotient conclusion is precisely `dim_F2((row(A)+C)/C)≥4`. Since `row(A)⊆row(G_x)`, it also implies `dim((row(G_x)+C)/C)≥4`. It does not prove `C⊆row(G_x)` or `rank(A)≥13`; a code that actually contains C and the fitting rows has dimension at least13.

The physical proof assumes monotone original carriers, q counted persistent descending packet paths with no restarts or uncounted descending copies, zero-born caches/extra records, fixed whole-record accounting, and no nonlocal preloaded value. Every extra ascending record is counted at each facet arrival and each MOVE remains charged. Nonmonotone paths, uncounted down copies, nonlocal births, or fractional-volume pricing need a new argument. The quotient corollary is only scalar F2; the all-field/block result here is the normalization and rank bound, not a binary quotient claim for general fields or blocks.

## Frozen inputs and finite controls

Author proof package: `root-work/y-feedback-normalization/`, manifest SHA256 `d427cabd4770bdd787f8bf85e77640a16a0848264a6d9b74d4881f28e2a3cd56`; proof SHA256 `e10044c415cc48ccc2ee9676f9947c9ad7ea24af09b1499ca2d25b73e3f74135`; checker SHA256 `47e9dba1b8ac8ec0871ddaa4317d52370f37c2c7e9c27d379305084138493c8c`; result SHA256 `e1e503c8f866f304ed8e1c50072a52ef00a2f5b0cb8d377dcbbb207a4eeede01`.

The checker completed 65,536 small GF(2) cell cases, 1,048,576 input reconstructions, and 65,536 symbolic mixed-X/Y locality cases. Its Y-swap and first-ground controls fail the expected terminal-only substitutions. These controls support, but do not replace, the all-field generalized-inverse identity and universal induction.
