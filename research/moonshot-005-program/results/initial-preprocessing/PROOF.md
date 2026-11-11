# Exact105-arrival minimum for initial-only acquisition of four full return rows

**Proved within the stated preprocessing grammar, with a sharp literal upper
witness. No new kappa.** This continues the existing paid weighted-preload
construction by testing whether its four remaining owned observations can all
be replaced by complete return rows computed before the source calendar starts.
They can, but the exact minimum number of new positive-rank arrivals is105,
which exceeds even the optimistic H4 allowance below98.399076951.

## 1. Source and quantifiers

The source is the71,261-event word at programme baseline
ce2846f5ac40be3392ece83b4f61ca0757af449f, compressed SHA256
2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883.
The four historical returns and their exact source versions are inherited from
historical-owned/WITNESSES.json, SHA256
d46db515a5fead49b752b8d798472c883aff7698d7e5e948f0d4e336ec99054b.

For every permitted complete-array dimension V and characteristic-zero scalar
field F, give the constructor400 independent raw main differences q_i in their
pinned initial charts. The entering helper differences are zero, because the
two virtual copies share arbitrary common/helper inputs. The raw q encoding
itself is a physical premise; forming it from actual x,y holders is not free.

The restricted task is to materialize the FOUR ENTIRE normalized returned rows
at their four destination charts BEFORE ANY ORIGINAL SOURCE INSTRUCTION.
The original source word is subsequently retained except for the four specified
return replacements and physical-owner renaming. All cross-chart messages in
the initial phase are new paid channels, not relabelled free original calls.
Allow arbitrary linear coding within all V coordinates, unlimited free local
memory/scalar work, shared aggregation, multicast, arbitrary timing within this
phase and arbitrary intermediate charts. Quotient aliases with the same binary
span into one chart. Every channel between distinct charts carries one complete
V-coordinate field and costs at least one positive-rank paid MOVE.

This theorem does not constrain dynamic aggregation using the existing funded
source routes, moved source instructions, changed input interfaces, or arbitrary
joint common/difference codes. It is not a universal four-return transport bound.

## 2. General outgoing chart-cut lemma

Let a linear target map send initially independent fields to designated output
charts. For an initial chart f, restrict all outputs located OUTSIDE f to the
input fields initially INSIDE f, and let its scalar coefficient matrix have
rank r_f. Then every linear message algorithm materializing those outputs needs
at least r_f outgoing complete fields from f. Consequently its total number of
cross-chart field messages is at least sum_f r_f.

Proof: fix every outside initial input to zero. Initially outside f contains no
information about its independent input block. An outgoing V-coordinate message
adds at most V dimensions of such information; incoming feedback cannot increase
outside information without a preceding outgoing message. The required outside
output restriction has rank r_f*V. Thus at least r_f outgoing messages are
necessary. Each message has exactly one source chart, so summing does not
multiply-charge any channel. This is a dimension argument for every V, not an
extrapolation from finite trials. Repeated messages and arbitrary local coding
are allowed. It also applies to an arbitrary supergraph of legal nested routes.

## 3. Exact source certificate

Fresh exact rational replay reconstructs the four source rows before their MOVEs.
Their400-input coefficient supports split as follows:

| Return event | Destination | Empty-chart3 coordinates | Other coordinates | Other initial charts |
|---:|---:|---:|---:|---:|
|28141|470|48|52|52|
|33554|431|45|52|52|
|34467|394|45|52|52|
|37597|520|54|52|52|

The union of nonempty-chart input coordinates contains101 inputs in101 distinct
initial binary spans. Each contributes rank1 to the four-output restriction;
none of the four output charts is an initial chart of these inputs. The empty
chart3 block has rank4. Therefore sum_f r_f=101+4=105.

Both the distributed and empty-chart components have rank4. Explicit nonzero
minors are available directly from the certificate. For distributed columns
(q4,q2,q1,q0), in the listed return order, the matrix is

\[\begin{pmatrix}
-3/4&0&0&0\\
0&-1/4&0&0\\
1/2&1/2&1/2&0\\
0&0&0&-8
\end{pmatrix}\]

with determinant-3/4. For empty-chart columns(q131,q129,q142,q150), it is

\[\begin{pmatrix}
3/8&0&-11/8&0\\
0&-9/8&-1/8&9/8\\
5/4&1&1&0\\
0&4&4&0
\end{pmatrix}\]

with determinant-495/64. Low global output rank4 therefore does not mean four
initially cochart input fields are available: the101 spatial cuts remain.

A literal raw-q carrier following only its own original main-role itinerary
visits none of its respective required destination charts before that return.
This separate finite source census does not rule out relays or changed payloads.
For example q4=1 and every other q=0 gives first return value-3/4, while any
chart3-only initial preload evaluates to zero. This is a concrete counterexample
to replacing the complete first return by its empty-chart input restriction.

## 4. Sharp upper construction and complete local bill

Create four owned accumulators in chart3 and add their empty-chart input terms:
192 ADDs total. For each of the101 other required q_i, INIT a reusable scratch
owner in q_i's initial one-dimensional chart, ADD q_i into it, and MOVE it down
to chart3 with rank1. Add its coefficients to the relevant accumulators, then
CLEAR the scratch owner. This takes101 input-copy ADDs and208 accumulator ADDs.
Finally MOVE the four accumulators from chart3 to470,431,394,520, with ranks
3,3,3,6. Thus exactly105 extra arrivals attain the lower bound.

At each original return, CLEAR its old owned field in its old source chart and
rebind its virtual role to the corresponding accumulator already at destination.
Rewrite all later operands and eventual CLEAR to this owner; a later INIT of a
reused logical label starts its ordinary new lifetime. Exact equality of the
old and new rows before each rebinding establishes continuation by induction.
No historical helper or later owned observation is read by this preprocessing.
The unchanged common rail remains separate and paid; dirty CLEAR retains the
owned-erasure assumption.

The actual72,073-instruction rewritten reference difference word checks all400
independent q directions and all1480 public endpoints, with final charts and
owned cleanup. Relative to the supplied source rail it adds501 ADDs,105 INITs,
105 CLEARs and105 paid MOVEs, while removing four MOVEs of ranks2,2,2,5. Its net
MOVE increase is101. Declared owned labels rise51 to56; lifetimes54 to159; peak
live fields43 to44. The temporary gathering owner is reused101 times. The
initial phase contains812 instructions. These counts exclude raw-q formation;
193 distinct q_i are used and each can be formed by one cochart subtraction
when the original paired holders are available. A full q bank, other helper
rail fields, output recoupling, source control and precision are not free.

At t=199/200 the added paid moment is

    101 + 3*3^t + 6^t.

The previous weighted-preload profile paid only the latter four terms. Keeping
all other provisional14-skip profile terms fixed, the new raw margin is reduced
by18*101=1818. It becomes strictly negative. This is a sharp ARRIVAL COUNT result,
not a claim that the displayed gathering tree minimizes the weighted rank price.

## 5. Verification and scope

source_partition.py independently derives target rows, chart cuts and raw-route
contacts from all71,261 source events using exact fractions and canonical span
sets. whole_preload.py emits and checks the literal word using the pinned
historical-accumulator typed interpreter. These author checks are not each
other's independent review. Separate review must authenticate both the lower
bound and whole-word equivalence. Normal/-O receipts are retained.

Mutations change a preload coefficient, falsely mark an owned gathering MOVE
public, and reference a retired owner after rebinding; all are rejected. Rank
controls include duplicate output rows and the zero map. The source and witness
files are authenticated before replay.

The useful next task is funded DYNAMIC aggregation of these distributed forms,
possibly jointly with the ten current-return identities. This packet closes
all nine historical observation premises only in an unaffordable initial phase;
it does not improve kappa or supply the complete shared native. All five global
foundational assumptions remain. Prepared for @CubeJerry with OpenAI assistance;
credit the source authors, S002 historical identities and typed preload work.
