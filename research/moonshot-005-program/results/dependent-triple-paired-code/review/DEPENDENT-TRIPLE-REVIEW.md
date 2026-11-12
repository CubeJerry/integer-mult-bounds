# Independent dependent-triple admission and the exact reverse-residual gate

**Status:** proved finite normalized source construction, subject to the
retained parent contracts; independently reviewed against all 1,880 input
coordinates. The actual hosted reverse residual has rank **95**, and one
nontrivial linear combination of reverse targets is correct. No individual
reverse pair is complete. **No new complete κ.**

This is a change in the assembled source map, not a rank prediction from a
candidate matrix. The reviewer independently emitted all instructions of the
75,081-operation forward intermediate and 76,039-operation final word, checked
the actual values at their physical source-read events, constructed the full
400-row private inverse, and recomputed the complete caller invoice.

## Pins and independent work

| Object | SHA256 |
| --- | --- |
| Native source compressed payload | `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883` |
| Admitted fused parent compressed word | `1536c714dd3500709c7717b8687b53f98d7a30f482aa5b09e5c25a4a23cf8153` |
| Fused parent decompressed payload | `05b503f0c2f219f328353b984ca821db9d6c3cc0225ff3380c551708d247e8d8` |
| Parent independent review | `a0ad37e09f691e57128d0eda773aaeb3bea62a757759c7cba0059686cae9ea6e` |
| New forward intermediate decompressed payload | `4be96b8164f389c69995fb202fc7194fae71d9989644ac89cd8d5622414ee3ad` |
| New paired final decompressed payload | `19a7a89b4623f7f095833a46369fad7bf6d63eabd6bf5a7929ed52a87b55b121` |
| New paired compressed word | `13d43635c2900a7220b5bd1da21e63807d728d4c67ccf2370178f171db62ef0c` |

The author is credited for choosing and constructing the dependent triple.
The independent reviewer derived its source Gram matrix, exact chart
intersections, complete operation sequence, live values, final map, and costs
without importing the author's generator or verifier. The review imports only
the reviewer's earlier exact geometry and word machinery. Source, dependency,
word, and review-code pins are recorded in `DEPENDENT-TRIPLE-REVIEW.json`.

## 1. Exact selected-column rank theorem

Let `H` index the 96 genuinely hosted first-X/X2 pairs, and let `S` be any
subset of `H`. Write `a_x,b_x,c_x,d_x` for the four independent raw difference
banks at a hosted index. Let `G` be the exact rational source root Gram matrix,
with `G_xx=8`. Define the selected correction rows

\[
A_{x,y}=\delta_{xy}-G_{xy}/8,
\qquad x\in S,\ y\in H.
\]

Suppose an actual source word supplies the whole transpose correction, so that

\[
b^{\rm out}=b-A^\mathsf{T}d_S=b+Rd,
\]

where `R` has zero columns outside `S`. Suppose further that the current
selected `d` values read by that word really are the original independent
`d` inputs. This is an interface premise that the actual word review below
checks; arbitrary matrices or abstract chart reachability do not supply it.

The desired hosted reverse output is `b-d`. Its residual coefficient matrix is

\[
B=I+R,
\qquad
B_{:,S}=G_{H,S}/8,\quad B_{:,H\setminus S}=I_{:,H\setminus S}.
\]

Order rows and columns as `S,C`, with `C=H\setminus S`. Then

\[
B=\begin{pmatrix}
G_{S,S}/8&0\\G_{C,S}/8&I_C
\end{pmatrix},
\qquad
\boxed{\operatorname{rank}B=96-|S|+\operatorname{rank}G_{S,S}}.
\]

**Proof.** For each selected column, subtract its lower entries using the
complementary identity columns. This invertible column operation leaves the
block diagonal matrix `diag(G_SS/8,I_C)`, proving the formula over any field
in which 8 is invertible. For the pinned rational root Gram matrix, the
kernel of `G_SS` is the kernel of the selected root matrix: this follows over
the reals from `G_SS=V_S^T V_S`, and the exact rational ranks and kernels then
extend to every characteristic-zero field. Thus each source root relation
supported on `S` supplies both a right null vector of `B` and a left null
vector supported on `S`. The latter gives an already correct linear
combination of hosted reverse targets. ∎

This theorem is explicitly **96-dimensional**. The eight coupled source
coordinates have no independent X2 bank, and their target map is different.
Treating them as extra independent primal/dual coordinates would violate the
previously proved coupled-register gate. They are not added to `H` here.
Their first-X values are used by the forward construction, while their
coupled reverse obligations remain open.

The earlier orthogonal eight-frame has `rank(G_SS)=8`, so its rank remains
96. Its transpose addition is nilpotent across complementary support blocks.
A dependent selected set introduces mutual selected donor/receiver terms;
those terms are essential to the new nontrivial kernel.

## 2. The exact dependent triple and its physical schedule

For first-X roles `S={0,1,98}`, the independently reconstructed source roots are

\[
v_0=(1,1,-1,1,-1,-1,-1,-1),\quad
v_1=(1,1,-1,-1,1,-1,-1,-1),\quad
v_{98}=(0,0,0,2,-2,0,0,0).
\]

They obey `v_0-v_1-v_98=0`, and

\[
G_{S,S}=\begin{pmatrix}8&4&4\\4&8&-4\\4&-4&8\end{pmatrix},
\qquad \operatorname{rank}G_{S,S}=2.
\]

All selected roles are genuinely hosted. The full forward correction support
splits into exactly three 24-donor pair cohorts. Their hosted restrictions
retain full row rank two:

| First-Y recipients | Full donors | Hosted donors | Coupled donors omitted from dual | Acquisition chart |
| --- | ---: | ---: | --- | ---: |
| Y112, Y113 | 24 | 23 | X52 | 1095 |
| Y112, Y210 | 24 | 24 | none | 1096 |
| Y113, Y210 | 24 | 21 | X17, X19, X47 | 1097 |

Each new chart has dimension seven and is exactly the intersection of its
two source final facets. Every donor starts on a line contained in the
required intersection. Original source chart declarations are unchanged.

### Forward phase

The forward intermediate uses three stationary facet collectors and six pair
collectors. Nonpivot donors visit their pair acquisition chart, add their
source Gram coefficients to its two collectors, and continue to the hub.
The first-X pivots are logical role 2 for pair `(Y112,Y113)`, role 1 for
`(Y112,Y210)`, and role 0 for `(Y113,Y210)`.

Each pivot carries one pair aggregate through one recipient facet, contributes
to its stationary collector, and is reconstructed from its original peers at
the hub. The other receiver visits that pair chart. The three receivers then
read their facet collectors. No receiver is assumed to visit two incomparable
pair intersections. The reviewer checks both the actual encoded pivot values
and the actual restored originals. All 104 first-X differences are original
at forward boundary 823.

### Dual phase and composition

The final word first moves the three selected original Y2 values to their
actual final facets. For each hosted cohort it constructs an invertible
matrix `M` whose two chosen rows are its source correction matrix `A`,
encodes the actual hosted X2 values as `M^{-T}b` at the acquisition chart,
and sends the two selected carriers through the two recipient facets. Each
carrier subtracts the original corresponding Y2 value there, then reaches
the hub. Applying `M^T` to the actual hub values yields `b-A^T d`.

The reviewer chooses the pivot columns independently from the source rows,
inverts `M` exactly, reconstructs all encoder and decoder instructions, and
checks every matrix and snapshot marker. The three cohorts involve disjoint
hosted donor sets, so their original b inputs are available when each encoder
runs. The selected Y2 values remain original throughout all six actual reads.
The four coupled donors listed above appear only in the forward bank; no
nonexistent independent dual records are supplied for them.

The 1,029 new dual instructions replace exactly 71 old direct raw MOVEs.
Chronological boundary transport, rather than a lookup of a retimed MOVE,
places the complete first-X restoration at 1,852 and common start at 3,328.
All 520 later E8 reads see the original first-X inputs.

## 3. What the assembled word proves

The exact 1,880-column pre-common state differs from the admitted parent only
in three first-Y rows and 68 hosted X2 rows. The latter contain exactly the
136 source transpose coefficients. All 252 explicit live row checks pass.
The remaining 72,711 instructions are literally the parent's common and
final suffix. Each changed private field is untouched there until its own
final common recoupling, so every common output and every other private row
is preserved.

An explicit triangular left inverse of all 400 terminal private rows proves
that the reverse residual kernel is **not loss of an input direction**.
The complete private transformation remains injective; the kernel concerns
only the still-missing target correction as a function of the Y2 inputs.

The actual residual has rank 95 and one-dimensional kernel generated, in the
Y2 input coordinate space, by

\[
e_{882}-e_{883}-e_{974}.
\]

There is also the exact already correct target relation

\[
b^{\rm out}_{772}-b^{\rm out}_{773}-b^{\rm out}_{868}
=(b_{772}-d_{882})-(b_{773}-d_{883})-(b_{868}-d_{974}).
\]

All three displayed b outputs are at the hub. This statement identifies a
linear combination of their current values; it does not claim that a new
physical output record was created at no arithmetic cost. Every individual
reverse residual retains its own coefficient 1, so **zero individual hosted
reverse pairs are complete**. The forward pairs X0/Y112, X1/Y113, X98/Y210
are complete. There remain 4,841 forward off-diagonal coefficient duties and
the separate coupled reverse obligations.

## 4. Rank reduction and the terminal spatial limitation

Rank 95 implies a lower bound of 95 additional scalar observations at a
fixed terminal hub. It does not by itself construct a 95-call repair. The
actual source endpoint geometry gives the following stronger statement.

**Separated-source terminal lemma.** Suppose a fixed normalized word has
finished with all common outputs restored, no owned records alive, hosted
values `b+Rd` at the hub, and the original independent `d_i` at 96 distinct
proper facets. Suppose every column of `B=I+R` is nonzero and every other
terminal field is independent of b and d. In the normalized cochart/MOVE
grammar, any appended finite field-linear word producing `b-d` at the hub
must contain at least **96 new paid MOVEs**, even if it performs arbitrary
subsequent linear coding or owned descents.

**Proof.** Parameterize inputs by an arbitrary vector `δ`: vary `d` by `δ`
and vary the independent hosted b inputs by `-Rδ`. The entire current hub
state remains fixed. Common and other private values also remain fixed;
only the local d field at facet i varies with `δ_i`. The desired hub output
changes by `-Bδ`. Since column i is nonzero, a correct suffix must convey
some dependence on `δ_i` outside its originating facet. Before the first
such conveyance, every field outside that facet has zero coefficient of
`δ_i`. INIT, CLEAR, SCALE and cochart arithmetic cannot create one there;
the first conveyance must therefore be a MOVE leaving that facet. These
first departures for different original facets are distinct events. There
are 96 facets, proving the count. Every proper MOVE has positive integer
rank and moment price at least one. ∎

This argument assumes the normalized word's actual local information
semantics. It grants no free input-dependent global communication through a
controller. Earlier code changes, additional current shared records, changed
common information, and later funded source calls are outside its scope.

For the actual triple word, every residual diagonal equals 1, so the lemma
applies. It also applies to **any selected-column Gram completion with the
same terminal interface**, because `G_ii/8=1` keeps every residual column
nonzero. Selecting more dependent roots alone will therefore not make an
appended repair affordable. The programme needs to supply the missing shared
information before this terminal interface, or change that interface with
all costs and restoration proved.

The bound is sharp for the triple's normalized MOVE price. The reviewer
constructs a literal 616-instruction suffix: for each facet, initialize one
owned record, copy its original d value, make one rank-one move to the hub,
subtract the associated column of `B`, and clear the record. All 96 reverse
shears are then correct. The suffix uses only already authenticated source
chart-map pairs. It has 96 rank-one MOVEs, 96 INITs, 96 CLEARs, 96 acquisition
ADDs, and 232 decoder ADDs. This suffix does not complete the remaining
forward or coupled obligations.

## 5. Complete costs and target status

| Item | Actual dependent triple |
| --- | ---: |
| Instructions | 76,039 |
| ADD / SCALE / MOVE / COPY | 65,061 / 3,676 / 6,877 / 1 |
| INIT = CLEAR | 212 |
| Peak owned records | 43 |
| Raw MOVE calls / rank mass | 559 / 3,200 |
| Complete paid positions | 131,850 |
| Target positions | 27,344 |
| Complete rank surplus | 3,760 |
| Remaining native moment at κ=1/200 | 43.730571695159306... |
| Hosted reverse residual rank / nullity | 95 / 1 |
| New chart-map pairs | 84 |

The full paid profile is independently recomposed as

\[
P=P_4+18(R_{\rm new}-R_{\rm old})+18\cdot8\{9\}.
\]

All paid entries are nonnegative. Directed rational brackets for every
`r^(199/200)` give the exact interval in the receipt. The sharp terminal
repair has additional native price 96, so the remaining moment becomes
`43.730571695159306... - 96 < 0`. It cannot certify κ=1/200 at this fixed
invoice. The positive partial allowance is not a complete multiplication
theorem or supplier admission.

For the weaker information-rank gate alone, the admitted parent's remaining
moment is strictly between 46 and 47. If all new routes only subdivide its
direct raw routes and common/packet costs are fixed, a terminal observation
budget would require `96-|S|+rank(G_SS) ≤ 46`, equivalently
`|S|-rank(G_SS) ≥ 50`. This is necessary only. The separated-source lemma
explains why it is far from sufficient under the retained endpoint layout.

## Verification, controls, and reproduction

The review rejects wrong primal and dual coefficients, wrong inverse
coefficients, a stale partially transformed donor substituted for an
original snapshot, a missing actual Y2 arrival, a missing dual facet leg,
and a stale restoration marker. The independent matrix check also rejects
the wrong root-relation sign and shows that deleting the mutual selected
terms destroys the rank drop. The orthogonal frame is a rank-96 control.

All 84 introduced chart maps have independently checked coverage, geometry,
ranks, and word/source pins. The retained exact Clifford and signed-Pauli
global-phase engines and their negative phase control are credited to the
author's pinned run. This is not a newly implemented physical compiler or a
new independent implementation of those engines.

```bash
python -B check_dependent_triple.py --repo /path/to/programme-checkout --package /path/to/dependent-triple/output --output DEPENDENT-TRIPLE-REVIEW.json
python -O -B check_dependent_triple.py --repo /path/to/programme-checkout --package /path/to/dependent-triple/output --output DEPENDENT-TRIPLE-REVIEW-OPTIMIZED.json
cmp DEPENDENT-TRIPLE-REVIEW.json DEPENDENT-TRIPLE-REVIEW-OPTIMIZED.json
python -B selected_reverse_rank.py --source /path/to/programme-checkout/research/shared-wire-split-composition/data/final.json.gz --output SELECTED-REVERSE-RANK.json
```

Both word-review runs must pass and produce identical receipts. Required
neighbouring reviewer modules are `cohort_geometry.py`, `check_cohort_word.py`,
and `selected_reverse_rank.py`. The literal terminal suffix is retained in
`DEPENDENT-TRIPLE-TERMINAL-SUFFIX.json`.

The advancing mechanism is a source-realized dependent-root reverse relation
with full input retention. The next relevant construction must transport or
retain useful reverse information preterminally, alongside a compatible
larger forward code. Repeating the triple with reset raw carriers, or treating
its rank-95 matrix as a free terminal encoder, would not satisfy that task.
