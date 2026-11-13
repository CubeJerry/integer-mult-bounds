# Original-coordinate helper restrictions: author funding certificate

**Author candidate result, pending independent source and proof review.**
On the exact #7481 source, helper restrictions that leave any original
coordinate subset I jointly arbitrary cannot improve the power
target-minus-paid moment for 0<=kappa<=1/4 by removing only identically zero
MOVEs while retaining all other native operations, charts and chronology. This candidate bound
grants all preparation/frame/owned-lifetime/cleanup costs free. No changed
supplier, physical admission or new kappa is claimed. All five inherited
assumptions remain.

The universal nine-min-tariff certificate does fail: the 347-row component
has rank 342 and gain +5 at `min(r,1)`. The useful power interval is instead
covered by support domination and four small row-matroid components. The
computational claims and proposed Laplace composition proof below are
author evidence, not independent acceptance.

The literal source is exact #7481 WORD SHA256
`acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9`,
76,475 instructions. A fresh exact-Q interpreter extracts the full scalar
rows of every main-free MOVE in the original helper coordinates. It checks
cocharted scalar operands, owned INIT/CLEAR, fresh-zero COPY, final charts,
every helper's exact unit-row endpoint, and main independence of helper
inputs. There are 468 nonzero main-free MOVE rows in 806 used helper
columns. Each of the other 5,811 rows has a nonzero main coefficient. No
empty-support original MOVE is silently omitted. ROWS.json SHA256 is
`15de6d0e53a846efdd5d3f9b34beb8d57fc51534967cc464b12c305ed2cf1834`.

## Precise graph restriction and rank criterion

Retain a subset I of the original helper coordinates as independently
arbitrary productive inputs, with their original target ranks. Demote its
complement H and impose `x_H=B*x_I`, for a fixed scalar matrix B. All main
inputs remain independent and arbitrary. Grant all input copies, frame
conversions, owned lifetimes, zero reframes and output cleanup free for this
optimistic funding test. Keep the source scalar contacts, and remove only
MOVEs whose rows become identically zero.
Every other native operation, chart and chronological contact is fixed.

Preserving the **original retained coordinates** is essential. Old target
prices are not assigned to newly rotated productive directions. Graph
dependence on main inputs, changed scalar contacts, new productive credit
for correlated copies and additional paid replacements are excluded.

For a MOVE set S let M_S be its full rational coefficient matrix. All rows
vanish under the graph for arbitrary x_I iff

\[
 M_{S,H}B+M_{S,I}=0.
\]

Thus H must preserve rank: `rank_Q(M_S[:,H])=rank_Q(M_S)`. This does not
assert independence of the listed MOVE occurrences. Conversely rank
preservation permits a rational B by solving the equation column by column
in this optimistic model. The condition remains the same over complex
scalars because the matrix is rational. Dependent rows retain their
separate paid charges.

The rank-preserving condition is necessary more broadly than linear graphs.
Allow any relation on helper inputs whose projection onto the retained
original coordinates I is surjective onto all jointly arbitrary I, with
no dependence on the independent mains. If a rowspace vector v of M_S has
v_H=0, identically zero source rows imply `v_I X_I=0` for every retained
input tuple, and therefore v_I=0. Projection of the rowspace to H is
injective, proving the same rank equality. Nonlinear, operator-valued and
even multivalued helper preparations obey this necessary condition when
that surjectivity holds. Linear-graph sufficiency above is not asserted
for these broader preparations. The deleted MOVE set consists of fixed
source occurrences vanishing for every admissible input, not branch-wise
sets obtained by restricting the retained inputs.

For nonnegative prices, H contains a column basis J of M_S, so lost targets
cost at least

\[
 B_f(S)=\min_{J\text{ a column basis of }M_S}\sum_{h\in J}f(R_h),
\]

where R_h is the original helper target rank. Therefore
`B_f(S)>=sum(e in S) f(r_e)` is sufficient to fund the zero MOVEs. A failure
only refutes this optimistic inequality; it need not survive the actual
input/frame/cleanup/ordinary invoice.

## Support components and bounded subset checks

The exact helper-support graph has 94 components: 86 with one row, four
with two rows, and one each with 3, 5, 19 and 347 rows. Component 0 is
347 by 669 helper columns; component 51 is 19 by 20. Exhaustive enumeration
of their `2^347-1` and 524,287 nonempty row subsets was not launched.

All 136 nonempty subsets in the 92 components of at most five rows were
checked exactly, covering 102 MOVE rows and 117 helper columns. All 1,224
integer inequalities for the nine `min(r,k)` tariffs pass. Each small
component's full row matrix has full row rank. The subset tables and
explicit omissions are in SMALL-RESULT.json.

Support components are legitimate even when B mixes independent coordinates
across them. The matrix is block diagonal after a row/column permutation;
zero columns outside a component cannot span its rows. Rank-preserving H
must span each component separately. Minimum column-basis and row prices
add across these components. These initial checks alone do not settle
dependent subsets of the giant; the row decomposition below supplies the
remaining author certificate.

For any selected subset, exact-Q elimination greedily appends rank-increasing
columns in increasing order of `(R_h,helper ID)`. The linear-matroid exchange
argument gives a minimum column basis. This same order is nondecreasing for
every nondecreasing price f(R_h), including all nine min tariffs. All basis
ranks are rational and all min-tariff margins are integers. The min tariffs
generate the nonnegative nondecreasing concave cone with f(0)=0, so nine
successful signs suffice for that cone, including `r^(1-kappa)` for
0<=kappa<1. No floating sign decision is used.

## Full ranks and pointwise support domination

The full-set stage completed both large components within its 60-second
cap, without enumerating their large subsets. Component 51 is 19 rows by
20 columns with rank 19. Component 0 is 347 by 669 with rank 342. Its
full-set nine gain vector is
`[5,-289,-582,-891,-1085,-1279,-1449,-1618,-1779]`, refuting the broader
all-concave-tariff certificate. Its minimum basis has 342 columns, so the
first gain is 347 minus 342. FULL-RESULT.json retains actual basis columns,
events and rational directed .0038/.004 prices; these useful-power full-set
gains have negative upper bounds, approximately -1763.19742804840236 and
-1762.36913031777108 per native call. They do not settle proper subsets.

Every coefficient in all 468 main-free rows passes the stronger test
`r_e<=R_h whenever M[e,h]!=0`. For any independent row subset S and any
column basis J of its matrix, the square minor M[S,J] has nonzero
determinant. Some determinant term is nonzero, giving a bijection between
the rows and columns along nonzero entries. Pointwise domination gives
`sum_S f(r_e)<=sum_J f(R_h)` for every nondecreasing f. Taking the minimum
over bases funds every independent row subset, without concavity or an
interval restriction. Dependent occurrences retain their separate charges.

## Exact row-space decomposition

Fresh elimination chooses 342 original giant rows as an independent basis.
Each of the five remaining rows has its unique rational expansion in that
basis. All five relations are rechecked by summing the actual full source
rows. Joining rows in each fundamental relation leaves 321 singleton
coloops and four nonsingleton components:

| Component | Rows | Rank | Nonempty subsets | Dependent subsets |
|---:|---:|---:|---:|---:|
| 169 | 11 | 9 | 2047 | 28 |
| 227 | 5 | 4 | 31 | 1 |
| 228 | 5 | 4 | 31 | 1 |
| 233 | 5 | 4 | 31 | 1 |

MATROID-COMPONENTS.json records all original basis events and relations.
The power checker independently checks that the 342 original rows are
independent; all expansions are exact and use only original basis rows;
each expansion stays inside its declared component; and component basis
subsets partition the independent basis. It verifies all support-component
coverage/disjointness and independence of the other 121 source rows.
The full 468 rows therefore decompose into 442 singleton row spaces and
these four dependent blocks, with global rank 463. Their row spans form
a direct sum even when helper-column supports overlap.

All 2140 nonempty subsets in the four blocks are ranked over Q using their
certified original-row coordinates. Of these, 2109 are independent and
funded by the determinant argument. For each remaining subset the checker
uses full helper columns to compute a minimum-linear-weight column basis,
and verifies agreement with its row-coordinate rank. There are exactly
31 such dependent subsets. No 347-row exponential search is used.

## Exact power envelopes

The initial [0,.01] author check used `9*1000^100<1023^100` and verified
`1000*L(S)>=1023*sum_S r_e` for all 31 dependent subsets. Its receipt is
retained as POWER-RESULT-001.json. The three five-row circuits have paid
sum 9 and minimum basis sum 21, with integer margin 11793. The 11-row
block's minimum margin under that historical rule is 15563.

The stronger proposed interval uses only

\[
 9\cdot6^4=11664<14641=11^4.
\]

Thus `9^(1/4)<11/6`. For 0<=kappa<=1/4 and ranks 1<=r,R<=9,

\[
 r^{1-\kappa}\le r,\qquad R^{1-\kappa}\ge(6/11)R.
\]

Let L(S) be the minimum sum of original target ranks over column bases of
M_S. Every basis J has `sum_J R_h>=L(S)`. Consequently the integer test
`6*L(S)>=11*sum_S r_e` funds all powers in the proposed interval for every
column basis and hence its minimum power price. All 31 subsets pass this
stronger test. Exact rational powers or floating signs are unnecessary.

Across all 31, the exact minimum ratio `L(S)/sum_S r_e` is 11/6. One witness
is events `[32944,32945,32947,32951,33081,33089,33091,33100]`: paid
profile `{1:4,5:4}` has sum 24 and minimum-basis target profile
`{4:3,5:1,9:3}` has sum 44. Its quarter-rule integer margin is zero;
the strict integer power envelope still gives the required nonnegative
funding inequality. POWER-RESULT.json stores every rank table, basis,
price profile and both historical/current integer margins. This stronger
interval remains a proposal pending independent review.

## Laplace composition with overlapping column supports

For any selected row set S, partition it among the row-space components.
Choose an independent row basis B_i of each selected block S_i. Their union
is independent because the component spans form a direct sum. For every
global column basis J, the square matrix with these basis rows and columns
J has nonzero determinant.

Its block Laplace expansion sums over partitions of J into disjoint column
sets J_i of sizes |B_i|. Some term is nonzero, so every block minor
M[B_i,J_i] in that term is nonsingular. Each J_i is a column basis of the
full selected block S_i. With the same original helper price on each
column,

\[
 \sum_{h\in J}f(R_h)
 =\sum_i\sum_{h\in J_i}f(R_h)
 \ge\sum_i B_f(S_i).
\]

Taking the global minimum gives `B_f(S)>=sum_i B_f(S_i)`. The helper-column
supports need not be disjoint: the nonzero Laplace term supplies a disjoint
partition for each actual global basis. The independent-block determinant
bound and all 31 dependent-subset envelopes therefore give the candidate
global funding inequality throughout [0,1/4]. This is the composition step
requiring independent mathematical review.

Together with rank-preserving necessity, this candidate inequality says
saved paid prices cannot exceed lost original-coordinate helper targets,
even for preparations across different boundary groups and with free
setup/frame/owned-lifetime/cleanup. It excludes new decoded productive
types, changed retained target coordinates/frames, changed native
operations and deletion without an identically zero whole-array premise.

## Domain, costs and validation limits

Each variable denotes the complete native field array, including its full
root factor, external rows and spectators, in the normalized source chart.
Retained input arbitrariness concerns these whole arrays. It is not
arbitrariness of selected coordinates, sampled columns, a restricted family
of examples or approximate numerical values. A nonzero retained scalar
form is detected by choosing one retained array nonzero and the others
zero. Identically zero source rows must vanish for every admissible jointly
arbitrary retained tuple. A rounded residual is not an exact zero.

This is a source-specific necessary moment bound under an optimistic cost
grant, not a new zero-field implementation permission. The separate public
zero-reframe audit requires exact digital whole-array zero and keeps field
shapes/backing. Actual preparations, scalar services, frame conversions,
owned capacity/lifetimes, final cleanup, physical native admission, common
precision, compiler constants, restored input-dependent stock and the outer
invoice remain obligations of any changed supplier. No new productive
credit is given to correlated copies. All five foundational assumptions
remain unchanged.

The source inventory rejects empty support, nonzero-main rows and missing
helper target weights. Synthetic controls reject a false row direct sum
and an overpriced dependent pair, and compare greedy minimum bases with
brute column-basis enumeration. Exact graph rank necessity, row direct
sums and the block-Laplace inequality are independently reviewable proof
steps; the code's author status is explicitly pending that review.

The exact Git-byte caller is reference/pr7481/CALLER-EXACT.json, 117156
bytes, SHA256
`255d89f38cd45e38e5770f559bc43dc217e989032359768cdc7e8cdfd64b47bc`,
blob `9451ceaf6e8e037894680b549f3ef41c21b260d7`. Its 17 native calls are
checked by full_components.py. The directed root price engine is pinned
by SHA256 `527d1cb2756ac6c61bd0b08488441105b8902a20e953dce149127bebc74d32bb`.
Its directed intervals are supporting full-set diagnostics, not the
integer quarter-power certificate.

The source inventory is a fresh normal exact-Q replay. Normal and optimized
small/full/power checks agree after their elapsed times are removed. Replay:

```sh
python3 -B worker-b/helper-graph/inventory.py
python3 -B worker-b/helper-graph/small_subsets.py
python3 -B worker-b/helper-graph/full_components.py
python3 -B worker-b/helper-graph/matroid_components.py
python3 -B worker-b/helper-graph/power_funding.py
```

Source hashes, precise domains, complete subset/basis receipts and current
file hashes are recorded in SOURCES.json and VALIDATION.json. The preserved
initial .01 receipt is historical; [0,1/4] is the stronger proposal awaiting
independent review. No acceptance or publication is performed here.
