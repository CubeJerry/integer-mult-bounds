# A Petersen obstruction forces nine nonlinear descent records

## Result and quantifiers

Fix the literal early-local canonical9 source word
`3643c6db33ce5ed1ea61724b126a8a3cad28be0c728376193b1f11fbf0457565`
and its cut immediately before operation783. For every finite alphabet A with
|A|>1, every fixed, data-independent, zero-error deterministic continuation
that completes the111 prescribed BIT receivers using the retained whole-record
chart rules must make **at least nine further strict owned downward transfers**.
Each transferred record has alphabet A; no wider payload, cross-chart read,
uncharged schedule information or input-dependent branch signal is supplied.
Cocharted arithmetic may be arbitrary and nonlinear. Original Y feedback is
allowed. This is a fixed-source theorem, not a universal movement bound for
changed earlier sources or an impossibility of the target multiplication bound.

Its full movement floor at t=199/200 is

    1613.257383014568907004412225980590... + 9
      = 1622.257383014568907004412225980590...,

which exceeds the necessary limiting allowance
1621.750880211152355246246150366995... by
**0.506502803416551758166075613595...**. Finite caller multiplicity and other
required costs cannot repair a failure of this necessary limiting comparison.
The earlier claim that this prefix escapes the *eight*-descent gate remains
correct; the present result supplies the missing stronger obstruction.

A second consequence is exact **nonlinear nine-symbol optimality in the
static native side-information relaxation** over every finite characteristic-two
field, with arbitrary positive whole-record width. This relaxation grants the
raw real-orthogonal neighbors to each receiver and one public transcript. It
does not implement physical co-location or a nine-MOVE complete native word.

## 1. The source gives a particular side-information graph

Let r_i be the actual rational native root and F_i its real orthogonal facet.
At the cut the unfinished roles are U63. Every one has an actual raw native
cache at its own line; its original X is already raw at Hub. The nine canonical
owners are at M1. No unfinished target facet contains M1. The48 ground source
coordinates and completed outputs belong to the complement of U63.

Fix every initial Y and every X outside the following14 roles:

    J = {5,35,90,93,96,97,109,110};
    E = {31,32,55,56,57,58}.

The source-bound checker examines the complete222-column value and actual chart
of **every** live cut field. For each selected receiver i, the union of its
initially upward-accessible X coordinates is precisely

    {j in J union E : r_i dot r_j = 0}.

Thus no hidden initial common field, native copy, completed output or arbitrary
Y column supplies a missing selected coordinate. This is verified from actual
cut values, not inferred from the labels of the owners.

The four roles {5,35,90,93} have no neighbors in this induced graph. On the
other ten roles, put a=96,b=97,c=109,d=110. The six added roles have neighbors
among {a,b,c,d} as follows:

| Role | Two base neighbors | Pair label for Petersen KG(5,2) |
|---|---|---|
| a=96 | — | {4,0} |
| b=97 | — | {4,1} |
| c=109 | — | {4,2} |
| d=110 | — | {4,3} |
|31|a,b|{2,3}|
|32|c,d|{0,1}|
|55|a,d|{1,2}|
|56|b,d|{0,2}|
|57|a,c|{1,3}|
|58|b,c|{0,3}|

Two ten-role vertices are adjacent exactly when their pair labels are disjoint.
The exact graph is therefore the Petersen graph together with four isolated
vertices. Every pair and every accessible cut support is checked by the
standalone source verifier. No approximate geometry is involved.

## 2. All future downward payloads form an optimistic public transcript

Let T be the sequence of all future owned strict downward payloads, granted to
every receiver for free. The initial-chart invariant from the admitted
BIT-INITIAL-CHART-TRANSCRIPT result says that any field at chart H is a function
of T and of initial cut values whose initial charts lie below H. This follows
by induction: same-chart operations and zero births preserve it; upward moves
increase available initial charts; a downward payload enters T; erasure adds no
information. Granting complete raw coordinates in every accessible initial
support can only help the receiver.

Consequently a physical continuation yields a zero-error index code on the
induced14-role graph. This reduction permits feedback and arbitrary nonlinear
operations. Fixed chronology and the finite whole-record alphabet are essential:
an adaptive schedule would have to be included and charged as information.

## 3. Exact entropy certificate for Petersen

The general Petersen index-coding rate5 is an existing result of Anna Blasiak,
Robert Kleinberg and Eyal Lubetzky, *Index coding via linear programming*,
arXiv:1004.1379v2, Fact5.6 (2011). The present package independently reconstructs
a short rational certificate rather than treating a numerical LP optimum as a
proof. The novelty here is its source-bound physical application and the
resulting precise cost gate, not the Petersen rate itself.

Let ten messages be independent uniform A-valued variables and P a valid
zero-error transcript. Normalize entropy by h=log|A|. For every subset S define

    X(S)=H(P,X_S)/h.

Then X(full)>=10; adding one message raises X by between0 and1; X is
submodular; and X(S union {i})=X(S) whenever S contains every neighbor of i.
These are ordinary entropy inequalities and the stated decoding property.

Average X over all120 permutations of the five symbols labeling KG(5,2).
The average Xbar retains every inequality and Xbar(empty)=X(empty). The
1024 subsets have34 orbits. A bitmask uses lexicographic pair order
(01,02,03,04,12,13,14,23,24,34); its orbit representative is the smallest
mask under these120 permutations.

`PETERSEN-SHORT-DUAL.json` contains21 inequalities with positive rational
multipliers. Each entry identifies an elementary inequality by its actual
subset and added vertex/vertices, not merely a claimed row of a numerical
matrix. `check_petersen_gate.py` rebuilds the120 actions, verifies all34
orbits, checks every decoding-neighborhood premise, reconstructs each exact
row, and adds the rows with Fraction arithmetic. The coefficient sum is
**exactly -Xbar(empty)** and the right-hand-side sum is **exactly -5**.
Thus H(P)>=5h for every such finite alphabet and code. No asymptotic limit,
linearity assumption or field-specific entropy identity is used.

The solver scripts are discovery tools only. Reproduction of the proof requires
Python's standard library and the committed21-term certificate, not SciPy or a
floating-point solver. Altered signs, an invalid decoding set, changed orbit
coefficients and an altered numerical bound are rejected negative controls.

## 4. Four isolates add four independent units

Write Z for the four isolated messages and X for the ten Petersen messages.
The isolated receivers have no side information in the induced graph, so Z is
a deterministic function of T. Hence

    H(T)=H(Z)+H(T|Z)=4h+H(T|Z).

For each fixed value z, X remains independent uniform, and the transcript with
Z=z is a valid Petersen index code. The exact certificate gives
H(T|Z=z)>=5h, so H(T)>=9h. If m records descend, their combined alphabet has
size at most |A|^m and H(T)<=mh. Therefore **m>=9**.

Private randomness does not improve a fixed-length zero-error code in the
usual sure-correct finite-domain model: fix any common seed for which every
input is decoded correctly. Randomized error or variable charged transcript
length is not claimed in this theorem. The result as stated is deterministic.

## 5. Cost consequence and static optimality

The authenticated suffix has only one direct remaining closure for each
unfinished original and the declared owner CLEARs. Any replacement monotone
original route has summed rank increments equal to the same total increment;
for0<t<=1 its power-sum cost is at least the single direct cost. Every new
strict downward MOVE has positive integral rank and therefore costs at least1.
Thus the original closed partial moment plus9 lower-bounds the movement of any
valid replacement suffix. Additional sources cannot be introduced for free.

For the static all111 contact graph, fixing all other variables leaves the same
Petersen-plus-four-isolates instance. Nine public symbols are therefore necessary
even for nonlinear coding. The existing canonical binary fitting K has diagonal1,
foreign support only on actual real-orthogonal contacts, and rank9. Broadcasting
a basis of its row space lets receiver i compute K_i x and subtract its known
foreign neighbors, recovering x_i. Tensoring this fixed binary identity with
I_V gives a nine-record upper bound over every finite characteristic-two field
and every positive width V. Therefore the static nonlinear optimum is exactly9.
This counts information, not physical acquisition, delivery or restoration cost.

## Open next questions

A profitable construction must change this earlier prefix enough to fund at
least nine descents and every other required operation, or change the actual
initial side-information/cut interface. A second local acquisition saving is
useful only if the donor routes, receiver access and complete source contract
compose. Existing canonical algebra gives no free receiver-chain implementation.
Both strict suppliers, full recursive accounting and all five foundations remain
open. No new complete kappa is claimed.

Credit: @CubeJerry; retained native, canonical fitting and transcript authors;
Worker A's new14-role block-star witness, Worker C's independent source audit;
Blasiak, Kleinberg and Lubetzky for the Petersen entropy theorem; root's exact
rational certificate, nonlinear physical reduction and static consequence.
Substantial OpenAI assistance. Agent reviews are not human or proof-kernel
acceptance.
