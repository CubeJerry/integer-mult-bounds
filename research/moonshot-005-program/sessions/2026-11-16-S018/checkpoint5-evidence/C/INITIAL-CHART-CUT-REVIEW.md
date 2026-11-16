# Independent review: initial-chart transcript and physical source repair

**Verdict: accept the universal fixed-cut theorem, all three acyclic witnesses,
both sharp all111 movement controls, and the changed native-cached57 source.**
The proof does not require initial chart-local payloads, and global nonlocal
rank does not invalidate it. It uses every live field's actual initial chart.
It permits arbitrary deterministic nonlinear cocharted arithmetic and arbitrary
intermediate original-Y feedback under a fixed schedule and fixed finite
whole-record alphabet.

## Pins, scope and independent machinery

The reviewed root proof is `R/initial-chart-cut/PROOF.md`, SHA256
`dbf00c71814d1c274cfd5bb474fb063e1b8c07e1a30c523437deaf8090cbc58c`.
C's verifier `review_initial_chart_cut.py` imports only C's exact Fraction
native interpreter and directed integer-root pricing. It imports no root or
A execution code. The receipt is `initial-chart-cut-review/RESULT.json`.
It checks every native line and facet against source SHA256
`8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`.

The three source pins are:

| Source | Word SHA256 | Cut |
|---|---|---:|
| A paid59 | dd60233b57be5fdef83b86a2d2b816e665e3d939850da94b680838d1d6d178ce | 1380 |
| A five-mode46 | 14503b00ad6f9d1e4d85ec09769a51c14eca36d61edabe19d9ae2907608c7501 | 1364 |
| C liberated55 | 4fe64237569a99a41578a378145a7df7ceac8394d33c82ca4f5e1be166b8859c | 350 |

The verifier replays all 222 arbitrary input columns of all three sources and
all three physical controls, recomputes the complete actual access graph from
every live original and owner, verifies each explicit sink-elimination order,
checks the suffix shape needed for the movement comparison, and prices the
complete words. No search outcome is promoted to a universal assertion.

## Universal proof audit

Write f_k for the symbolic value of a live record at the cut, and H_k for its
chart at that cut. Record in T the entire payload of every future strict
downward owned MOVE, in chronological order. A current record at chart H is a
function of T and the f_k with H_k contained in H.

The induction is valid for every allowed primitive. At the cut a record's
own f_k is in the allowed set. A zero birth adds no dependence. Cocharted
deterministic arithmetic composes functions with the same allowed argument
set. An upward MOVE enlarges that set. A downward MOVE appends precisely the
moving payload to T, so after arrival the record is a function of T alone,
regardless of its previous encoded or nonlinear contents. CLEAR conveys no
information. Giving the entire transcript, including later payloads, to every
receiver only relaxes the task. There is no reliance on chronological access
to this optimistic grant in a positive construction.

Fix all original Y inputs and all X inputs outside a proposed witness W.
At F_i, grant separately every x_j occurring in any initial cut field whose
initial chart is contained in F_i. For these binary-linear prefixes, union of
the exact nonzero X columns gives a valid coordinate superset of every such
field's dependencies. This grant may reveal more than the actual encoded row;
that makes the lower bound weaker, hence remains safe. It also ignores
incompatibility of visiting several available charts on one monotone route.

The final increment x_i is therefore a function of T and these granted
coordinates. If the induced graph on W is acyclic with no self loop, first
recover a sink x_i from T, then remove it and continue. Every required side
coordinate inside W has already been recovered at its turn. The entire
independent tuple x_W is thus a function of T. With a nontrivial finite
whole-record alphabet A, at most |A|^m possible transcripts cannot distinguish
|A|^|W| possible tuples unless m is at least |W|.

The conclusion does not use linearity of the continuation. It does require
the stated equal fixed record width and data-independent schedule. Wider
records, adaptive route information, uncocharted reads or fresh input-dependent
births are outside the theorem. Intermediate original mutation, mutual
original borrowing and nonlinear Y feedback do not escape the invariant.
Even granting upward owned motion leaves the induction intact.

The retained `results/endpoint-side-information/PROOF.md`, section 3, already
contains the acyclic reconstruction argument for common linear broadcasts.
The new contribution is the initial-chart transcript invariant, its finite
alphabet extension to arbitrary deterministic continuations, and these
authenticated actual-cut applications. This is not a new abstract minrank
claim or a bound on earlier replacement prefixes.

## Exact source graphs and floors

For paid59 the entire 52-role unfinished graph has exactly ten arcs:
{26, 61, 67, 72, 84} each points to {5, 15}; every other row is empty.
For five46 the entire 65-role graph has twenty arcs:
{18, 26, 61, 67, 68, 71, 72, 81, 84, 85} each points to {5, 15}; all other
rows are empty. Both whole graphs are acyclic. These calculations include
the five genuinely nonlocal fields of five46 at their actual holding charts.

For liberated55 the verified witness is

`{5,13,14,31,33,52,57,58,59,60,82,83,86,87,89,91,96,97,98,99,100,101,105,106,107,109}`.

Its first sink batch is {5, 89, 91, 98, 99, 106, 107}. The remaining 19
vertices are exactly the mask donors. Every witness arc goes from one of
those donors to the seven sinks. Thus 92 raw native originals do not by
themselves restore the missing side information of the 19 originals that
have already ascended to Hub.

The frozen tails consist of direct required original closures and CLEARs:
52 MOVEs / 185 CLEARs, 65 MOVEs / 132 CLEARs, and 148 MOVEs / 63 CLEARs,
respectively. Every unfinished Y begins at ground. In liberated55 the 148
closures additionally include 92 direct native-original X ascents.
For p=199/200, splitting a positive rank difference cannot reduce its total
p-moment. Each future strict owned descent costs at least one. Consequently
the complete closed partial price plus the required descent count is a valid
floor for every replacement suffix.

| Fixed source | Required future descents | Complete movement floor | Excess over necessary allowance |
|---|---:|---:|---:|
| paid59 | 52 | 1671.210689048551331... | 49.459808837398976... |
| five46 | 65 | 1677.137283799758513... | 55.386403588606158... |
| liberated55 | 26 | 1628.327705963120503... | 6.576825751968147... |

These are directed exact rational enclosures, not rounded comparisons. All
other future costs are optimistically omitted. The exclusion concerns the
three exact prefixes through their specified cuts.

## Sharp all111 physical controls

All X originals in the paid59 and five46 cuts are actually raw at Hub. Root's
two controls create one new zero owner per unfinished role there, copy its
raw X, descend one rank to its actual facet, move its Y directly to the same
facet, and ADD the new owner into Y. The owners are explicitly retired.
The frozen prefix is byte-for-byte unchanged. Both controls pass all 222
columns and every native movement/cochart condition in C's interpreter.

| Control | Word SHA256 | INIT / ADD / MOVE / CLEAR |
|---|---|---|
| paid59 all111 | ccc022135e052b37f3a770b262901473e45dee848875a4298600fb0e503920db | 240 / 771 / 626 / 240 |
| five46 all111 | d05ee9a36a551f3b159c224c4a09f0a1d79f809ffd152691bb5a94fa03c23383 | 197 / 942 / 550 / 197 |

Their complete movement profiles equal the original closed profiles plus
exactly 52 and 65 unit descents. Thus these two fixed-cut movement floors are
sharp, not just lower estimates. The words exceed the target movement budget;
they do not supply a target-compatible all111 construction.

## Native-cached57 changes the premise physically

The reviewed repaired source is
`R/initial-chart-cut/control/NATIVE-CACHED57-WORD.json`, SHA256
`7df1fc8f696545185c417c6df4161b324869bf084b503138506425510e841fa2`.
Its cut is 392.

Before the 19 mask donors leave their native lines, a 38-instruction prelude
creates and fills one stationary owned raw cache at each actual native line.
The complete original liberated55 prefix then executes literally. Every old
cut value and chart is unchanged except Y61 and Y67. Those two receive actual
ground raw61/raw67 from the already paid raw source and ascend to their
facets before the new cut. Their old suffix MOVEs are removed, so no MOVE is
added anywhere.

At the new cut there are 57 completed Y records at their facets, 54 raw
ground Y records, 92 raw native X originals, 19 other raw originals at Hub,
57 actual raw ground inputs, the same three proper masks and three common
mask copies, plus the 19 native raw donor caches. The whole invoice is
82 INIT, 155 ADD, 301 MOVE, 82 CLEAR, all 82 retirements dirty. The complete
profile remains

`57[1] + 22[2] + 19[5] + 203[7]`,

with moment `1602.327705963120502679476564437395707...`.

The old 26-role graph is now cyclic. An explicit two-cycle is 5 to 13 to 5:
X5 still supplies its raw coordinate at L5; the new actual raw13 cache supplies
the opposite incidence at L13. Both native lines lie in the opposite target
facet. Several other explicit two-cycles are recorded. The old acyclic
witness therefore no longer applies to this changed prefix.

A missing raw13 capture leaves every final endpoint of the partial word
correct, but changes its native snapshot to zero; the independent source
contract check rejects that mutation. This distinguishes real retained side
data from endpoint correctness. Omitting the actual ground61 ADD fails the
Y61 endpoint directly. All 19 caches are checked individually for a real raw
capture, their exact native chart, no MOVE and explicit final retirement.

The repaired source does not assert that a receiver can visit multiple
incomparable native caches on one monotone route. It removes a concrete
information-access obstruction while leaving the physical decoder obligation
open. The extra INIT/ADD/CLEAR operations are counted; unchanged movement
does not mean unchanged complete ordinary or ownership cost.

The global foundations native_all_columns, owned_erasure, compiler,
precision_tape and analytic_recovery remain open. Full 222-column identities
of these finite words are distinct from the global native_all_columns gate.
Both strict suppliers, complete recursion and a new kappa remain unproved.
