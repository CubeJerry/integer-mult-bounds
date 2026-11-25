# Independent review of compact spectral repair

Result: **PASS for the stated scalar/scan interface**, with the clarifications
below. Read `../route-c/COMPACT-SPECTRAL-REPAIR-EXECUTOR.md` in full and its
checker, and replayed the checker in this route's directory. The review
does not assume a full compact shared pencil or complete multiplier.

## Correct table and scope of the lift

For j=|J|, the first j check entries of the discrepancy equal V_J e_J.
Equation SR4 followed by transpose lift therefore gives exactly

    Z_J=V_J^T V_J^(-T) diag(g_J^2) V_J^(-1)V_J e_J
       =diag(g_J^2)e_J.

There is no claim that the lifted Z is supported on J. It can be nonzero
outside J; correctness uses g=0 there. On J, g^3=1 when g is nonzero,
and a zero gap already makes the original error vanish. Thus the formula
also handles a containing exceptional set with accidentally correct rows,
without dividing by gaps. Only nonzero Vandermonde pivots are inverted.
The wording about vanishing outside J should refer to the original error,
not the lifted array.

## Field construction and actual control work

With e=ceil(log_4 B), one has 4^e<4B. Enumerating degree-e monic candidates
and their possible proper factors costs at most O(B^(3/2) poly(log B))
by the predecessor's bounded construction. Field-coordinate arithmetic,
inversion and all O(B)-dimension table computations are polynomial in m.
There is no field alphabet truth table or all-frequency table of hidden
exponential size.

The exact interchange records have only 2e scalar bits, so reading an
f-digit address at every record would be invalid. The note instead uses
the source three-run comparison scan: H_j is read once per complete N_j
fibre, and the complete target/suffix range pays for boundary computation.
Amortized counters handle arbitrary preceding and spectator ranges. Tags
are then zipped by scans. This keeps O(m^2) ordinary volume overhead and
does not introduce an f factor per record. Keys are used only between
completed converter words, in the correct original physical order.

## Packed widths and child volumes

The decomposition v=32w is essential. Nonpadding checks have 32s0 coarse
roles, while S=Bw has B roles; the remaining B-32s0 roles are zero. Thus
padding need not be a multiple of v, and every role retains the same whole
w-module. Sixteen two-family parent blocks contain exactly 32B coarse
roles, which can be reinterpreted as a complete child batch without a
transpose inside the w-module. The completed child acts identically and
independently on every row, so that reinterpretation has an exact return.

The R/16 ratio is a ratio of **raw scalar** volumes with 2e-bit records.
Temporary spectral keys are ordinary work and parked storage. They must
be removed before a recursive converter call; the table's final untagging
scan supplies this at its output, and its input keys are formed only after
the forward converter completes. The same requirement applies to any
separately implemented intermediate diagonal. With that convention the
four child phases retain total mass 1/4. The scalar coefficient polynomial
therefore sums geometrically through finite repair.

Shift/check maps loop over polynomially many coarse roles and scan a whole
(module,Omega) block at a time. Their pass count does not loop over w.
Recomputing a polynomial-size matrix per tagged record is a lawful, charged
polynomial-m operation. A fixed number of alternate work regions covers
copying, accumulation, removal, erasure and head returns, so visited cells
have the stated polynomial coefficient plus explicit descriptor term.

## Actual replay

The copied checker is `verify_independent_spectral_repair.py`; it preserves
the original checker bytes and accesses the same pinned predecessor orbit
routines. Running it passed six physical-orbit repair cases with 6,912
independently populated outputs, 250 generalized-binomial comparisons,
117 pairwise moment cases, three containing sets with zero gaps, 28 exact
padding/phase ledgers and nine negative controls. Results are recorded in
`compact-spectral-repair-verification.json`. The toy's larger check ratio
and the separate asymptotic 1/16 ledger are distinguished.

This is an independent mathematical interface review and exact finite
replay, not a full tape execution, proof-assistant result or human referee
certification. Credits: source ordered scans and converters, predecessor
structured shifts/checks, Route C's S003 executor, Jerry Chen (@CubeJerry),
and AI-assisted independent review.
