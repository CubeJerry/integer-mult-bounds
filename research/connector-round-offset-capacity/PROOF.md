# Sharp connector capacity by cancelling round offsets

In the unsigned, immutable-source, one-dirty-connector interface of
CrocSwap/integer-mult-bounds#4231/#4248, let N(c) be the maximum source
capacity in integer characteristic c>=2. We prove

    N(c) = (1+o(1)) c log_2 c.

This matches the known counting upper coefficient one. For every fixed
d>=2 we also construct depth-d blocks on (d-1)log_2 c-O_d(1) sources,
matching the leading term of #6107's fixed-depth upper bound. The earlier
general lower coefficient from #6071 was one half. **No new κ:** this is
an abstract connector theorem, not a physical supplier or complete
multiplication recurrence.

## 1. Literal interface and deterministic block

The only calls are B_j: z+=B_j x_j and A_M: y_M+=A_M z, for immutable
sources x_j, arbitrary dirty z, and one output per nonempty source subset M.
Maps are arbitrary compatible linear maps over any nonzero unital ring of
characteristic c. Each source and each output must occur exactly c times.
The desired output increment is sum_(j in M) A_M B_j x_j; z must be
restored and initial output contents otherwise retained.

A source word with each label occurring c times has prefix count vectors
q_t. A depth-d block represents every nonzero binary mask modulo c by a
sum of at most d prefixes. Repeated boundaries are permitted. Output reads
do not change z, so their requested boundaries can be sorted chronologically.
Padding an output to c reads at boundary zero cancels its dirty coefficient.
This is the inherited prefix criterion, restated to fix the exact model.

Choose D,b>=1 and c>=D+1 with D(2^b-1)<=c. Partition k=Db labels into D
groups of size b. Assign a distinct round r(S) in {0,...,c-1} to each
nonempty subset S of each group. There are exactly D(2^b-1) assignments.
Round r(S) calls every source once, with S first, then its complement.
Unused rounds may use any permutation. Concatenate all c rounds. Every
source is called exactly c times. At the start of round r, q_(rk)=r*1;
immediately after its first |S| calls,

    q_(rk+|S|) = r*1+1_S.                               (1)

For a nonempty mask M let S_1,...,S_t be its nonempty group parts, t<=D.
Read their prefixes (1). Their sum is (sum_i r(S_i))*1+1_M. Put

    r_0=(-sum_i r(S_i)) mod c,    0<=r_0<c.

One additional positive read at boundary r_0*k has count r_0*1 and
cancels the common offset modulo c. Thus t+1<=D+1 prefixes represent M.
This is a depth-(D+1) block.

The correction may occur before, after, or in the same round as a productive
read. It need not use an unassigned round: a round's starting count is
independent of its permutation. Repeated boundaries are legal. No negative
call is introduced; the negative residue selects an ordinary positive read.
A correction at r_0=0 is a legitimate zero-prefix read.

Pad each output to exactly c reads at zero. Its c copies of initial z cancel,
its source coefficient is 1_M, and all initial output contents are preserved
apart from the desired increment. The source word adds c copies of each
source to z and restores it. Sources never change. The order A_M B_j is
never exchanged, so no commutativity or primality assumption is used.

## 2. Concatenation and explicit capacity

Concatenate B=floor(c/(D+1)) blocks on disjoint sources. Each ends at
zero modulo c. For a global mask, represent each nonempty block part in
its own block, use no reads for empty parts, and pad the total to c at the
global zero boundary. There are at most B(D+1)<=c nonpadding reads.
Earlier blocks contribute multiples of c at later reads. Hence

    N(c) >= Db floor(c/(D+1)).                           (2)

For fixed d=D+1 take b=floor(log_2(1+c/D)). Then D(2^b-1)<=c and
k=(d-1)log_2 c-O_d(1). The upper bound of #6107 is
k<=(d-1)log_2 c+O_d(log log c), so the leading term is sharp.

For an explicit choice for every c>=16 put L=log_2 c, D=floor L,
b=floor(log_2(1+c/D)). We have D+1<=c, b>=L-log_2 D-1, b<=L,
and D<=L<D+1. Therefore (2) yields

    N(c) >= cb-cb/(D+1)-Db
         >= cL-c log_2 L-2c-L^2
         >= c log_2 c-c log_2(log_2 c)-3c,               (3)

using L^2<=c for c>=16. This applies to all sufficiently large integer
characteristics, not just a subsequence.

## 3. Matching inherited upper bound

For n sources there are cn distinct source-call boundaries after identifying
q_(cn) with q_0 modulo c. An output's c reads form a multiset of boundaries;
its sum can represent at most one binary mask. Thus, as in #4248/#6107,

    2^n-1 <= binom(cn+c-1,c) <= (e(n+1))^c,
    n <= 1+c log_2(e(n+1)).                             (4)

This necessary condition holds for all schedules in the exact interface,
not merely block schedules. Set x=(n+1)/c. Equation (4) implies
x<=log_2 c+log_2 x+log_2 e+2/c. For x>=4 use log_2 x<=x/2; for x<4
there is already a constant bound. Thus n=O(c log c). Substituting back
into (4) gives n<=c log_2 c+O(c log log c). Together with (3), this proves
N(c)/(c log_2 c)->1. The upper bound is credited, not claimed as new.

## 4. Construction cost and scope

The subset-to-round map is explicit: enumerate groups, then their nonempty
binary subsets. Building one local source word uses O(ck) label operations
and stores ck labels. Decoding a local mask takes D group extractions and
one modular sum. These describe schedule construction, not the physical
costs of arbitrary maps. No probabilistic existence theorem or search is
needed.

For n total sources the complete word has cn source calls and c(2^n-1)
output calls. It has exponentially many outputs. A physical caller must
still pay input access I, helper/frame work sum P_F, decoder D_W,
c sum_j cost(B_j), c sum_M cost(A_M), and applicable address, workspace,
layout, routing, precision, restoration and outer costs. Dirty cancellation
and connector restoration are proved; unknown physical costs are not zero.
No selected-frontier assumption is discharged. The selected κ remains
0.003125804.

The bounded expansion decision is to finish this structural theorem and
independent exact controls, then stop. It answers whether one half is a
barrier beyond depth two and determines the unrestricted leading constant.
A physical implementation campaign requires a named consumer and favorable
complete invoice; neither is supplied here.

## 5. Provenance and remaining questions

Base 7c49fe32c55de02c2c873655c804b16e4c3fef0a. SOURCES.json pins the
merged interface, Gray-growth and bounded-depth-cap READMEs. #6107 Open
Questions 1--2 ask for sharp higher-depth blocks and the unrestricted
constant; both leading-constant questions are addressed. #6071 supplies
the earlier one-half lower bound and general-constant question. #4231/#4248
supply the interface, concatenation and counting bound. No unmerged code
is a dependency.

Subset enumeration and modular arithmetic are classical. The contribution
is the round-boundary offset correction and its complete use in this
floor-word model. Open: lower-order asymptotics, exact finite capacities,
better finite blocks, and a fully paid physical consumer. Finite tests
support the written proof; they do not establish its universal quantifiers.

Prepared for @CubeJerry with substantial OpenAI Codex assistance in the
construction, proof, implementation and separately assigned AI reviews.
Credit Nick Petalas (#4231/#4248), apoursh/Armin Pourshafeie (#6071),
JosieElliston (#6107), and the retained Ross Richardson/Riquelme Soares
connector lineage. Apache-2.0. No human or proof-kernel acceptance is claimed.
