# Append-only terminal gate for the finite-m private rails

## Statement

At the actual endpoint of the standalone private rail `Q`, keep all previous
operations fixed and allow an arbitrary later field-linear suffix on its 400
private fields and zero-owned records. Assume the suffix must complete all 96
hosted reverse targets at Hub 127, retain all original hosted `D` values at
their prescribed facets, and may charge every new MOVE normally. Then at least
96 new field-MOVEs are required. If the already-composed 31-column consumer is
part of Q, its 31 rank-one returns have already been paid and its actual
remaining matrix has 65 nonzero columns; any such suffix still needs at least
65 new field-MOVEs. Thus either form needs at least 96 rank-one-equivalent MOVE
price per private rail in total.

More generally, after `m-1` independent Q rails have run and the single shared
native word has completed, an arbitrary joint field-linear suffix across all
private banks needs at least `96(m-1)` new field-MOVEs from the base-Q state,
or `65(m-1)` after the 31-return rail. The 31 earlier returns in each rail
bring the latter total back to `96(m-1)`. Cross-bank coding does not reduce
this bound.

This is a terminal append-only result. It does not apply to a redesign of Q
before this interface, to a changed earlier shared/native itinerary, or to a
later funded common schedule that has not yet been run and can carry these
variations. Such a schedule must expose its actual rows, calls, and invoice.

## Exact current-row premises checked

Independent replay of the pinned 4,779-operation Q gives, for the 96 hosted
ports, `B_i` at Hub with an identity block on the independent hosted `b`
coordinates and `D_i=d_i` at 96 distinct proper facets `F_i`. Write the
current Hub rows as

\[
  z_i=b_i+\sum_j R_{ij}d_j,
  \qquad M=I+R.
\]

The exact 96-by-96 matrix M has rank 82, unit diagonal, and no zero columns.
Every other one of Q's 400 live endpoint fields has zero coefficient on every
hosted `b_j` and `d_j` input. This last property is checked directly from the
full 400-coordinate row matrix; it is not inferred from the intended endpoint
map.

The appended B7+24 word copies each selected original `d_j` from its restored
facet, charges one rank-one MOVE to Hub, and subtracts the full actual column
`M[:,j]` from all affected B rows. Its residual is M with those 31 columns
zeroed: rank 58, 24 complete hosted outputs, and 65 nonzero columns. Every
other endpoint field remains independent of hosted `b,d`; all96 D rows remain
restored. Each of the31 charged chart pairs is present in the pinned cyclic
source. The 31 return costs are already part of Q's current invoice.

The fixed-m word has literal form: form `v_j-u_main`, run Q on each private
bank in sequence, run the shared native word once, then recouple each common
main output into its private output. Its exact full-input rows are

\[
  W(u)\quad\text{and}\quad E u_{main}+L(v_j-u_{main}),
  \qquad j=1,\ldots,m-1.
\]

Thus the common output is fixed when only private hosted `b,d` inputs vary.
The bank's B rows have the same actual residual M (or its 31-column-zeroed
version), its D rows retain the independent source variation at their facets
plus a fixed common term, and every other private field is unchanged under the
same variation. The exact m=3 checker verifies the literal word and all 2,280
independent input coordinates.

## First-departure proof at original chart nodes

This uses the separated-source terminal lemma already recorded in
`results/dependent-triple-paired-code/review/DEPENDENT-TRIPLE-REVIEW.md`.
Apply it to the actual Q rows above. For each nonzero residual column i,
perturb the hosted `d_i` coordinate by an arbitrary whole-field vector δ and
perturb the hosted `b` inputs by `-R[:,i]δ`. Every Hub row z is then fixed,
while the required target `b-d` changes by `-M[:,i]δ`. All other current
fields are fixed by the checked row-support condition; only the original D_i
field at F_i carries δ.

The first conveyance of any part of this variation out of F_i must be a MOVE
whose source **chart node is F_i**. Local INIT, CLEAR, SCALE, and cochart
ADD/COPY cannot put a δ-dependent field at another chart. This is a node-source
argument, not a claim that distinct downset exits must be different. Two D
values may descend separately into a common intersection and later share one
outbound MOVE from that intersection; that still requires two earlier MOVE
events sourced at the two distinct original facets.

At fixed m, the m−1 private banks supply m−1 independent δ_{j,i} variations
at the same original node F_i. The required outside joint B target has rank
`(m−1)V` on these variations for every nonzero M column. One field-MOVE carries
at most V independent scalar coordinates, regardless of its chart-rank tariff;
therefore at least m−1 distinct MOVE events must depart node F_i. A MOVE has
one source chart, so departure-event classes for distinct F_i are disjoint.
Summing over 96 nodes gives 96(m−1) events when all columns are nonzero. After
the 31 earlier returns, only the 65 unreturned columns require new events,
giving 65(m−1). This argument permits arbitrary joint suffix recoding and
feedback among the private banks.

Each new event is a positive integer-rank MOVE and costs `r^(199/200)≥1`.
The corresponding lower bound on additional movement moment is therefore the
same count. This is valid for every positive whole-field volume V: the
independent variation rank and every field-MOVE capacity scale by V, while the
normalized number of events does not.

## Full finite-m allowance comparison

Recomputing the pinned complete caller formula gives the total Q moment room

\[
 A_m=A_\infty-\frac d{m-1},\qquad
 A_\infty=129.9388553172829\ldots,\quad d=31.5397783670854\ldots.
\]

For the 4,779-operation base Q, its actual current movement profile has cost
`c_0=72.8425150488410...` beyond the fixed old raw profile. Its maximum
remaining room is therefore
`A_∞-c_0=57.0963402684419...`, below the required 96. For m=3 the room is
41.3264510848992..., also below 96.

The B7+24 consumer adds exactly 31 rank-one calls, so `c_1=c_0+31`. Its
remaining room is 26.0963402684419... even as m tends to infinity, below the
65 remaining columns; at m=3 the room is 10.3264510848992..., also below 65.
The gap is the same in either comparison: 38.9036597315580... at the limiting
ceiling and 54.6735489151007... at m=3. Since A_m is strictly below A_∞ for
every finite m, no fixed finite m can append this private-only completion to
the current Q within the remaining moment allowance.

The independent receipt
`check_mcopy_consumer.json` contains exact rational interval brackets for the
Q profiles, full m=3 target/paid profiles, moment, rank surplus and both
remaining-room comparisons. It confirms 83,345 instructions, 7,990 MOVE
events, 858 retired lifetimes, peak 43, 31,296 target positions, 155,916 paid
positions, rank surplus 4,380, and per-rail remaining m=3 moment
10.326451084899253... after the B7+24 consumer.

## Scope

The result rules out completing this exact terminal Q by appending a private
field-linear suffix under the declared normalized MOVE grammar, even when a
fixed number of copies share one already-spent native word. It does not rule
out changing Q before D and B reach this separated terminal interface, jointly
designing an earlier common/native consumer, using additional funded source
events before that cut, or replacing the old movement schedule. It is not a
complete supplier, a proof of the global programme impossible, or a new κ.
All five foundational assumptions remain.
