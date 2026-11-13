# Temporal two-cache zero-erasure bypass: corrected interface audit

**Correction status.** This version supersedes the earlier draft in this folder.
That draft used the older 18-call word, kept the MOVE, treated an earlier
restricted scalar list as a universal coefficient ban, and assigned a flat
physical cost to route records. This review instead uses the current #7481
native input (`acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9`),
removes the MOVE, and leaves physical record costs symbolic under the retained
fixed-rational service contract.

## Scope and chart-typed witnesses

Consider one owned MOVE from A to B. Let `x_A` be the exact row in the source
chart A. Let `x_B` be the exact target row that the unchanged MOVE would have
delivered in chart B, including its source-to-target frame action and phase.
The witnesses are chart typed: an earlier B-bank witness must synthesize
`x_B`, and a strictly later A-bank witness must synthesize `x_A`. If the
normalized scalar row is unchanged by this frame transition, both may be
written `x`.

The proof below is conditional on those exact arbitrary-input identities and
on the native clear/reinitialize interface. From the prior application review
it reuses only the generic per-service and per-record bounds; its old
18-call source census is not reused. It proves no source-specific
provider, compiler extension, complete admission, paid saving margin, or
kappa. New coefficients and actual providers still require a source-bound
catalogue entry, exact common-grid and precision replay, physical schedule,
caller replay, and a full recalculation of the outer budget.

## Schedule and arbitrary-input identity

At the strictly earlier B cut, write

\[
x_B=\sum_{i=1}^{r_B}\alpha_i b_i,
\]

where all `b_i` are live in B at that cut. Choose a positive common
denominator `D_B` and integers `m_i=D_B alpha_i`. Initialize a fresh owned
B cache `c_B=0`, use integer COPY/ADD operations to form

\[
c_B=\sum_i m_i b_i=D_B x_B,
\]

then apply the fixed rational scale `1/D_B` exactly. Hold `c_B=x_B` in B
until the old MOVE position.

Immediately before that position, initialize a distinct owned A cache
`c_A=0`. COPY `o` into `c_A`, then subtract `c_A` from `o`. Thus `c_A=x_A`
and `o=0`. CLEAR `o` at A. **Delete the original MOVE.** At its old position,
INIT the now-free owner slot `o` at B, then COPY `c_B` into it. This gives
the post-MOVE target row `o=x_B`. Subtract `o` from `c_B`, leaving the B
cache zero, then CLEAR `c_B`.

At the strictly later A cut, write

\[
x_A=\sum_{j=1}^{r_A}\gamma_j a_j,
\]

where the donors are native A-bank rows and exclude both caches. Set
`D_A>0` and `n_j=D_A gamma_j`. Scale `c_A` by `D_A`, subtract each
`n_j a_j`, then CLEAR the resulting zero cache.

| Time | Original owner `o` | B cache `c_B` | A cache `c_A` |
| --- | --- | --- | --- |
| Earlier B witness | Native state | Prepared as `x_B` and held | Not initialized |
| Just before old MOVE | `x_A`, then zeroed and cleared at A | `x_B` | Initialized and copied to `x_A` |
| Old MOVE position | Reinitialized at B, then restored to `x_B` | Zeroed and cleared | Holds `x_A` at A |
| Later A witness | Native state | Cleared | Subtracted to zero and cleared |

All equalities are rational row identities in their stated charts, so the
schedule preserves the map for every input assignment. The A cache retains
the exact source row while it is available at A; the B cache independently
holds the exact target row, including the original MOVE's target-chart
interpretation. After the old MOVE position, the original owner row and frame
match the unmodified program. Every subsequent native instruction therefore
sees its original operands. The extra caches end at zero. No equality is
approximate, and no cache supplies its own witness.

This relies on the native interface allowing CLEAR of a zero owned slot at A
and a new INIT of that freed slot at B. The pinned old syntax validator
accepts INIT at a declared frame after the ID is not live, but a #7481-specific
word and application admission must verify the owner lifecycle, zero-at-clear
condition, exact chart IDs, phases, and absence of an observable boundary
between the surgery and restored native state. No MOVE is performed on the
zero slot. Each CLEAR is after an exact arithmetic result of zero in that
field. The proof does not treat CLEAR as permission to discard arbitrary
stale backing: the concrete fixed-rational service must leave the owned value
at the contractually required stored zero and retire its own scratch before
CLEAR. If only a formal row is zero while hidden backing or entanglement
remains, the retained owned-clear contract has not been met.

## Cumulative chronological observations

The single-cut witnesses can be replaced by finite cumulative identities.
For B, suppose donors `b_i` are observed at strictly earlier cuts `t_i` in
one fixed B coframe and satisfy the exact identity
`x_B=Σ_i α_i b_i(t_i)`. Initialize `c_B=0` at the first needed observation.
Immediately after each donor is available, and before its next native
mutation, COPY the first nonzero integer term `m_i b_i(t_i)` into the cache
and ADD every later term, where `m_i=D_B α_i`. After the last donor
observation, at a cut still before the removed MOVE, divide once by `D_B`.
The donor is a source and is preserved by the accumulator operation. The
result is `c_B=x_B` at the seam.

For A, suppose donors `a_j` are observed at strictly later cuts `s_j` in one
fixed A coframe and satisfy `x_A=Σ_j γ_j a_j(s_j)`. At the source seam,
copy `x_A` to `c_A`, zero and CLEAR `o` at A, then scale `c_A` by `D_A`.
Immediately after each later `a_j(s_j)` becomes available, and before its
next native mutation, subtract `n_j a_j(s_j)` from `c_A`, where
`n_j=D_A γ_j`. After the last term the exact row is zero, so CLEAR `c_A`.
A single-cut witness is the special case with all donors observed at one cut.
The same cache IDs suffice, but `c_B` starts at its first B observation and
`c_A` remains live through its last A observation. The longer occupied
intervals and every partial-sum mass must be included in storage, width and
service checks.

These conditions constructively implement a finite pooled-history identity
when coefficients are fixed rationals, all donors are observed in the same
coframe, the accumulator source is preserved, and each update has a legal
insertion point. A pooled-span membership result alone does not provide the
coframe, coefficients, insertion points, exact grid proof or physical
service. This cumulative statement identifies no actual #7481 provider.

## Information bound for a B-history cache

There is also a general necessity test for any deterministic cache whose
input-dependent information comes only from the native B history. Let `A` be
the exact rational matrix whose rows are every B-bank latent-row coefficient
available before the old MOVE, and let `c` be the target row `x_B`. If
`c` is outside `rowspan_Q(A)`, exact linear duality gives a rational vector
`t` with `A t=0` and `c t != 0`. Multiply `t` by a common denominator to
make it integral; the two equalities remain true.

For any allowed whole input array `z`, assign the independent native inputs
`X_h=t_h z`. Every native B-history observation is then exactly zero for
every such `z`. Compare `z=0` with a nonzero legal `z`, or use two distinct
legal `z` values if zero is outside the input domain. Since `c t != 0` and
the fixed native B-chart map is invertible, the required target values differ.
A deterministic algorithm whose only
input-dependent information is those histories, and which otherwise knows
only fixed program metadata, receives identical data in the two executions,
so it cannot return both targets. This argument applies to arbitrary
postprocessing of the history values, including nonlinear and
operator-valued cache state; it does not assume ADD/COPY arithmetic or
classical inspection of the arrays.

The exact-grid version requires that the input domain admit a nonzero legal
`z` for which both assignments and the target are represented, and that all
rows included in `A` really account for every input-dependent observation.
Clearing denominators in `t` makes the history cancellations exact integer
identities; no rounded zero is used. If the algorithm can read an A-bank
source, import another cache, inspect an omitted public field, access an
unrecorded input register coherently, depend on input-dependent phase/side
information, or use a changed native history, that information must be
included in the observation map or the argument does not apply. This is a
necessary obstruction for the stated history-only interface, not a universal
native/physical admission theorem.

## Exact-rational and fixed-grid contract

The retained application review's §4 implements a fixed reduced rational
`a/b` by exact finite carry/remainder procedures. A nonzero final remainder
is an error, not rounding. Therefore a denominator such as 7 is not excluded
by the older selected word's `{2,3,5}`-smooth coefficient check alone. The
older `independent.py` validator is pinned only as provenance for that earlier
word's grammar; it is not the coefficient admissibility theorem for this
general fixed-rational service. New fixed coefficients still need to be
entered into and checked by the current finite service catalogue.

For denominator clearing, exactness is especially direct: integer sums create
`D_B x_B`, so every integer component on the current representation grid is
divisible by `D_B`; division returns precisely `x_B`, which was already
representable on that grid. The A-side multiplication by `D_A` and integer
subtractions likewise preserve the source rows' grid. These facts are
sufficient for the scalar arithmetic portion, provided the fixed-rational
operations are entered in the finite service catalogue and exact division
returns the required grid row. They are not a necessary-and-sufficient
criterion for full physical admission. The actual #7481 grid, row-mass and
precision bounds must be obtained from its own validation. `D_B x_B`,
`D_A x_A`, and partial sums may increase coefficient width and component
volume; this review assigns no source-specific width or cost to them.

## Ownership and structural budget deltas

Per native invocation the surgery adds two owned cache IDs and three
lifetimes: one lifetime for each cache and one restarted lifetime for `o`.
The old MOVE lifetime of `o` ends at CLEAR(A); a new lifetime starts at
INIT(B), and the original later CLEAR closes that new lifetime. There are six
added INIT/CLEAR events: INIT/CLEAR for each cache, plus CLEAR(A)/INIT(B) for
`o`. Peak simultaneously live owned fields can rise by at most two. No cache
MOVE is added, and the original MOVE is removed.

For the current 17-call #7481 caller, assuming this same source MOVE is used
once in each call, the structural deltas are:

- `-17` paid MOVE positions, with the corresponding rank recorded in each
  invocation's source-bound invoice;
- `+34` separately tagged cache field allocations, `+51` lifetimes,
  `+102` INIT/CLEAR operations, and at most `+2` live owned fields per
  invocation;
- zero productive-field or target credit for the private caches.

Let `u_B` and `u_A` be the counts of nonzero integer coefficients among the
`m_i` and `n_j`. With one fixed-rational scalar instruction per donor term,
the new scalar instruction count per native word is

\[
N_s=u_B+u_A+4+[D_B\ne1]+[D_A\ne1].
\]

The four seam operations are COPY to `c_A`, subtract from `o`, COPY from
`c_B`, and subtract from `c_B`. The B sum uses COPY on its first nonzero term
and ADD for the remaining terms. The A cleanup uses one ADD per nonzero
`n_j`. If a coefficient is zero its operation is omitted; if `D_B=1` or
`D_A=1` its identity scale is omitted. There is no 65,534 chunk limit in the
general exact-rational service. The exact coefficient catalogue must contain
each integer and rational used by the schedule.

The application review allows at most 32 scalar services per source scalar,
admin, or caller macro. If all added scalar and INIT/CLEAR operations use
that service class, a conservative incremental scalar-service count is

\[
\Delta S\le17\cdot32\cdot(N_s+6).
\]

With the review's `2^20` step reserve per padded component bit, this gives a
symbolic scalar term

\[
C_{scalar}\,2^{20}\,\Delta S\,V_{new},
\]

where `V_new` is the recomputed component volume after the new coefficients
and rows. If any new operation falls outside the 32-service macro, its own
compiler/service term must be added. New coefficient bit lengths, component
padding, and scalar-catalogue setup belong in the corresponding fixed
`C_scalar` and `G_add` terms. For the synthetic positive control below
(`u_B=u_A=2`, `D_B=D_A=7`), this generic envelope is at most 8,704 scalar
services across 17 calls, or coefficient 9,126,805,504 multiplied by
`C_scalar V_new`. This is a bound on the control schedule only, not a
#7481 source invoice.

The application review counts two complete monomial adapter maps per native
paid MOVE. Thus the deletion removes 34 such maps across 17 calls. Let
`R_del` be their actual compiled elementary-record count. The generic per-map
bound at ambient dimension `n` is `4(n+1)^2`, so the two deleted adapters
contribute at most `34\cdot4(n+1)^2` elementary records. Separately, the
removed rank-`r` child decreases the rank-one paid count by `17r`. A
route/phase record is charged using the retained generic primitive

\[
C_{move}V_{new}((f\log p)^\tau+1),
\]

with compiler descriptor work charged separately as a polynomial in address
length per record. Any newly required service, map, setup or workspace
increases `G`, `R` or `O_aux`. There is no flat 1,000-step charge per route
record.

Let the current #7481 binder supply its own values
`(W_current,O_current,P_current,R_current,G_current,V_current)` and its own
derived stock/cost formulas. Keep productive width free of cache credit;
recompute the actual width and component volume after adding the coefficient
and row growth. The structural updates are `P_new=P_current-17r` for the
rank-one paid count, `O_new=O_current+34+O_aux,new`,
`R_new=R_current-R_del+R_add`, and `G_new=G_current+G_add`. Recalculate every
downstream quantity using the #7481 binder. `G_add` must include the added
scalar and admin services, coefficient catalogue work, exact-grid/precision
replay, and any implementation workspace. `O_aux,new` reserves scratch and
field workspace; the longer cumulative-cache live intervals must also fit
its lifetime model. No source-dependent storage formula, common-grid scale,
or height from the older 18-call word is imported. These symbolic changes do
not establish that the full cost gate still passes.

## Controls and limits

`controls.py` uses two independent arbitrary input amplitudes in a complete
two-component vector. Its A-to-B chart map is the exact Gaussian-rational
`C_v=(1+i)I/2+(1-i)X/2` from the pinned Clifford convention, so
`x_B=C_v x_A` differs from the source-chart bytes. The control checks
`C_v^\dagger C_v=I` exactly and confirms its imaginary entries survive. Two
earlier B observations
`b_1=2x_B`, `b_2=3x_B` with coefficients `2/7` and `1/7` synthesize the exact
target; two later A observations with the same scale factors erase the A
cache. It performs the updates chronologically, clears at A, initializes at
B with **no MOVE**, restores the phase-sensitive target and erases the A
cache after its last donor. It checks a synthetic Gaussian integer grid with
scale 2 only; this is not a claim about #7481's actual grid. The exact `1/7`
divide passes because the B accumulator is `7x_B`; the control does not apply
the older smooth-coefficient validator. It counts ten scalar operations, six
INIT/CLEAR operations, two cache IDs, three added lifetimes, and one deleted
MOVE per native word. One negative uses `(1/3)(6x_B)=2x_B`; the other tries
to copy source-chart `x_A` as the B target. Both fail exact target equality.
The clear guard also rejects a nonzero stored formal row. Physical backing
and service scratch still require the owned-clear implementation contract.

Normal and optimized control runs must agree; see `VALIDATION.json`. The
current provider search and complete #7481 admission remain separate. This
artifact is an interface proof and budget template only; it makes no
source-specific improvement or kappa claim.
