# Two-helper correlation: exact complete moment gate on #7481

There is no positive moment gain in this scope. The exact exhaustive census
has 21 eligible correlation families and both orientations, giving 42
candidates. Every family removes exactly one original MOVE. Its rank is no
larger than either orientation's lost helper target rank. Thus even granting
all ordinary initialization, zero-reframe, layout and final scalar/CLEAR work
free cannot produce a gain. No changed word or new supplier was emitted.
All five framework assumptions remain unchanged.

The word has 76,475 events and 6,279 MOVEs, SHA256
`acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9`.
The actual signed #7113 caller has 17 joint calls and SHA256
`255d89f38cd45e38e5770f559bc43dc217e989032359768cdc7e8cdfd64b47bc`.
These are the exact 117,156 Git bytes, blob
`9451ceaf6e8e037894680b549f3ef41c21b260d7`, bundled as
`reference/pr7481/CALLER-EXACT.json`. The earlier acquired copy has one extra
trailing LF and remains untouched; its old byte pin is not used here.
`scan.py` authenticates both files. All event indices are zero based.

## Mechanism and exact budget

Choose distinct helpers h,g with the same entrance chart and comparable
final GF(2) subspaces. Keep g as an arbitrary independent productive input.
Remove h's public input/target, initialize its newly owned field to zero at
the shared entrance, and COPY `h=q*g`, for nonzero fixed q. Run the same
native scalar operations and the same nonzero MOVEs. Any MOVE that becomes
identically whole-field zero is granted the local exact-zero implementation
interface, with its ordinary work retained. Reclassifying h's original
ascending MOVEs as owned is ownership bookkeeping, not an extra target.

At the source endpoint every helper has its own exact latent unit row; every
main endpoint has zero coefficients on all helper inputs. This is checked
by the fresh full rational replay, starting with all 1,501 inputs independent.
After the restriction, g and all other retained helpers therefore have the
same original outputs, and all mains are unchanged. The owned h ends as its
original final chart applied to `q*x_g`. MOVE it to g's final chart, subtract
`q*g`, and CLEAR the resulting exact zero. The owned MOVE can ascend or
descend because the two final subspaces are nested. The original h allocation
is not counted as an additional productive cache.

Write `f(0)=0`, R_h for h's original target rank, and d for the final chart
rank gap. If P_r MOVEs of rank r become zero, the complete native moment gain
relative to the original source is

\[
 G_f(h\leftarrow qg)=\sum_r P_r f(r)-f(R_h)-f(d).
\]

The actual caller multiplies this by 17. Both h-to-g and g-to-h orientations
are separately priced. The COPY, added owned lifetime, precision bounds,
layout/head returns, all scalar cleanup and zero-reframe ordinary work must
be charged in an emitted supplier. This gate optimistically grants them
free; losing under that grant suffices to stop the construction. It does not
claim free actual initialization, disposal or owned storage.

## Exhaustive candidate coverage

Every MOVE is replayed as an exact sparse rational row in the independent
initial inputs. The replay checks cocharted scalar operands, native MOVE
nesting and ownership, fresh-zero COPY, owned lifetimes and final charts.
There are no unconditional zero MOVE rows. Of the 6,279 rows, 468 contain no
main coefficient. Exactly 23 of these have support on two helpers.

For a row `a*x_h+b*x_g` with both coefficients nonzero, substitution
`x_h=q*x_g` can kill it only at `q=-b/a`. Every other original input remains
arbitrary. Therefore a row with a nonzero main coefficient, with three or
more helper coordinates, or with a single helper coordinate cannot vanish
under a nonzero two-helper correlation. A q not forced by one of the 23
two-coordinate rows removes no MOVE and has a negative target/cleanup bill.
The q=0 coordinate-zeroing mechanism is separate prior work.

Rows with the same unordered helper pair and forced q are grouped before
pricing, so every removed MOVE is counted once and all proportional rows
would be included. Reversal uses 1/q. The actual source gives one MOVE per
eligible family. Two rows fail the entrance condition: event 48162 uses
helpers 1199/1351 at entrance IDs 3/516; event 56959 uses 705/1253 at IDs
105/3. Neither pair even has equal entrance subspaces. There are no
equal-space/different-ID aliases requiring an extra chart-normalization
case. No remaining two-coordinate row fails final comparability.

The 21 eligible families give 42 orientations. Forty have identical final
chart IDs and form the matching-boundary negative check against the prior
groupwise annihilator theorem. Twelve of those orientations are exactly
neutral at the complete native moment; 28 are dominated by a strictly larger
lost rank. No extra productive target is credited for the copy.

## The only unequal-boundary pair

Event 32402 moves public owner 336 and has exact row
`(1/2)*x_337-x_339`, of paid rank 1. Both helpers enter at chart 3. Their
final charts 240/241 are nested, with target ranks 4 and 5 and gap 1.

| Demoted h | Kept g | q | Removed paid | Lost target | Cleanup | Exact gain |
|---:|---:|---:|---:|---:|---:|---|
| 337 | 339 | 2 | f(1) | f(4) | f(1) | -f(4) |
| 339 | 337 | 1/2 | f(1) | f(5) | f(1) | -f(5) |

Their integer gains at `f_k(r)=min(r,k)`, for k=1,...,9, are respectively
`[-1,-2,-3,-4,-4,-4,-4,-4,-4]` and
`[-1,-2,-3,-4,-5,-5,-5,-5,-5]`. Multiplying by 17 preserves the sign.
They lose throughout the target kappa range, including .0038 and .004.

## Exact tariff proof and validation

All 42 nine-generator vectors are nonpositive integers. A nonnegative
nondecreasing concave tariff on ranks 0,...,9 with f(0)=0 is a nonnegative
linear combination of these nine min tariffs, so their signs certify the
whole concave class. More strongly, the actual source has one removed MOVE
of rank r<=R_h in each candidate. For every nonnegative nondecreasing tariff,
`G_f=f(r)-f(R_h)-f(d)<=-f(d)<=0`. This directly includes
`r^(1-kappa)` for 0<=kappa<1. No floating log, power estimate or directed
transcendental pricing is needed for the result.

Controls reject omitting the lost target, omitting the final cleanup debit,
using the wrong q, and counting a pair with a nonzero main coefficient.
They also check that proportional row coefficients give the same family q.
All helper endpoint unit rows and main independence are checked from the
actual complete source. Normal and optimized runs agree after elapsed time
is removed. `RESULT.json` contains all 42 oriented candidates, row
coefficients, event/owner/rank evidence and native/signed-17 tariff vectors.
`CANDIDATES.tsv` is a compact view of the same complete list.

## Related scope

The existing matching-entrance-and-exit group theorem already handles the
40 baseline candidates at its published kappa interval. Only the two
unequal-final orientations extend that boundary scope here.

PR #6170's toolkit contains `alias_core.py` P14 ALIAS: it redirects dirty
reads of a victim helper to an equal-content keeper, deletes victim contacts,
performs dead-code elimination, resolves frames/start loads and reprices.
That is related helper-aliasing work; its changed-contact mechanism is
broader and different from retaining all source scalar contacts under the
single input restriction tested here. This census does not claim a new
general correlation principle or exclude that toolkit's rewrites.

PR #6349's native input lifting uses an invertible helper input basis B,
delayed deliveries and a final B inverse, preserving every independent helper
input. Its proof explicitly says no helper is set to zero or replaced by a
copy. The present test deliberately demotes one original helper, debits its
target, and grants only a copy of another retained independent helper.
The reviewed canonical files and hashes are recorded in `SOURCES.json`.

Replay with Python 3.12 or newer:

```sh
python3 -B worker-b/pair-correlation/scan.py
python3 -O -B worker-b/pair-correlation/scan.py --output worker-b/pair-correlation/RESULT-O.json
```

This excludes only one nonzero two-helper correlation with unchanged native
scalar contacts and the stated cleanup. Multiple simultaneous correlations,
changed contacts, changed frames, lifetime retiming, cache imports and other
input-boundary changes are outside this census. No source word was emitted.
