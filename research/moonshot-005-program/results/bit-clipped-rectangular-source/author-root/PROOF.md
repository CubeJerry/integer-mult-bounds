# Clipped cohort filtration with extra physical source channels

**Proved universal linear-algebra theorem and scoped source consequence;
independent review requested. No new κ.** The previous rectangular filtration
can become vacuous when there are twice as many acquisition channels as target
coordinates. Keeping each cohort's nonnegative rank contribution gives a
positive all-field bound. It excludes a concrete repair of the one-hop MDS
source even if every original Y is first used as an additional source courier.

## 1. General rectangular theorem

Fix a field k, width V>=1, and nonempty target cohorts of sizes n_i, with
n=sum n_i independent width-V target blocks. Cohort i has m_i acquisition
row blocks, m=sum m_i. Let U be cohort block diagonal, with block dimensions
n_i V by m_i V, and P be an mV by nV matrix. Every acquisition row assigned
to cohort i has zero support on that same target cohort and reads at most d
OTHER target cohorts, for a fixed integer d>=1. Internal V-by-V coefficients
are arbitrary and need not commute. Let A=I-UP.

For any linear order π of cohorts, let g_i(π) count acquisition rows in i
whose cohort precedes every cohort in their support. Then

    rank A >= V max_π Σ_i max(0,n_i-m_i+g_i(π)).          (1)

Proof. Filter ker A by vectors supported on cohort prefixes, as in the
admitted cohort-acquisition theorem. At cohort i every good acquisition row
vanishes on that prefix. The new kernel increment has dimension at most
(m_i-g_i)V, but also at most n_i V. Summing these minimum bounds and subtracting
from nV gives (1). No inverse of U, commutative coefficient or generic-rank
assumption is used. The nonnegative clipping is kept BEFORE the cohort sum.

If m<=λn, λ>=0, then (1) implies

    rank A >= V ceil(n I_d(λ)),
    I_d(λ)=integral_0^1 max(0,1-λ+λu^d) du.              (2)

Proof. Give cohorts independent continuous priorities. Conditional on the
priority of cohort i leaving proportion u of priorities later, a row with s
other source cohorts is good with probability u^s>=u^d. By convexity of the
positive part,

    E[max(0,n_i-m_i+g_i) | u]
      >= max(0,n_i-m_i+m_i u^d).

Integrate and sum. The sum of positive parts is at least the positive part
of the sum, giving integral max(0,n-m+m u^d). For m<=λn this is at least
n I_d(λ), since u^d<=1. The maximum of the integer-valued cohort sum in (1)
is at least the ceiling of its expectation. This proves (2).

For0<=λ<=1, I_d(λ)=1-λ+λ/(d+1). Forλ>1, set
α=(1-1/λ)^(1/d). Direct integration gives

    I_d(λ)=1-dλ/(d+1)+d(λ-1)α/(d+1).                   (3)

At λ1 this recovers the admitted n/(d+1) bound. At λ2,d3 it gives
I_3(2)=(3/4)2^(-1/3)-1/2 >119/1250. The last entirely rational bound follows
by integrating 2u³-1 only over[4/5,1]; the omitted positive interval is nonempty.
Thus for m<=2n and d<=3,

    rank A >= V ceil(119 n/1250).                       (4)

Neither (2) nor (4) is claimed sharp. The older un-clipped rectangular bound
n-m+ceil(m/4) is negative at m=2n; dropping the cohort-wise clipping would
lose this conclusion.

## 2. Actual one-root source channels at one E6 stage

Retain the111 native source-root/facet pairs and b separately paid copies,
so n=111b. An actual source-local acquisition interface may form arbitrary
linear maps from the b original X banks at each L_j into m_j width-V channels.
These channels may include the original X banks and original Y banks that
first visit L_j and copy a source form. All copied and original Y values remain
independent; we consider the X coefficient equation only, a favorable relaxation.
Channels assigned to j contain no X source information from another root.

Each channel next ascends to ONE E6 chart containing L_j, then only containing
final facets and Hub. Arbitrary mixing at that E6 chart and its final facets
is allowed. The authenticated geometry puts that E6 chart in at most three
native facets, none equal F_j. Earlier cross-root preprocessing, another lower
chart, fresh descending source histories or a later enlarged global space are
outside this source interface and must be explicitly charged if introduced.

Write E=diag(E_j), where E_j has m_j V rows and bV columns. Let D map physical
channels to output coordinates through the allowed continuation. Each D
column block affects at most three OTHER receiver cohorts. With actual global
X information G, complete delivery implies

    I=G+D E,       G^T=I-E^T D^T.                       (5)

Apply (4) with cohort-local U=E^T and acquisition P=D^T. If at most all111b
original X and111b original Y records serve as these channels, m<=222b=2n.
Consequently

    rank G >= V ceil(13209 b/1250) >9bV.                (6)

This excludes canonical9bV global supply even after granting EVERY original Y
as a second source-channel resource, arbitrary uneven allocation among roots,
all within-root recoding and all block coefficient mixing. It does not assume
that two encodings of a source are scalar multiples, and does not import an
uncharged independent duplicate as a new input.

The simpler root-only source had m=n and needed ceil(111b/4)V. The expanded
source can lower that obstruction, but cannot reach9bV with the existing2n
public records. Equation(2) quantitatively screens further channel additions.
Any extra physical width, repeated effective observations or changing packet
history needs actual source access and cost. The theorem does not exclude a
source with genuine overlapping cross-root acquisition before the E6 stage.

## 3. Verification, relation to earlier results and limits

The companion checker tests rectangular cohort matrices, unequal channel
allocations, arbitrary width-one/two internal blocks and singular encoders over
F2 andF3. It enumerates every cohort order in its small domains and compares
actual rank with (1) and (4). It also checks exact rational integration.
Scope controls remove own-cohort exclusion, permit cross-cohort preencoding,
or add enough physical channels/receiver support to violate the stated bound.
These controls supplement the universal proof, rather than extrapolating it.

The geometry and zero-own-cohort premise are independently admitted in
results/bit-shared-facet-one-hop-gate/. The earlier kernel filtration is in
results/cohort-acquisition-rank/author/PROOF.md. This package contributes the
cohort-wise clipping, conditional-priority integral and expanded physical
channel application. The theorem is unrelated to a finite κ optimization.

All retained memory, physical source formation, ownership, ordinary/compiler,
precision, recursive and five-foundation requirements persist. No globally
working MDS decoder or profitable supplier is claimed. Credit @CubeJerry,
root's clipping/integral theorem, the admitted cohort-filtration/index-coding
predecessors and native chart geometry; OpenAI assistance.
