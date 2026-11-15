# Independent review: clipped rectangular filtration and chart sources

**Accepted within its explicit source-factorization scope. Proved universal
linear-algebra theorem; no new κ or complete supplier.** Reviewer: Worker A,
working independently of root's proof/checker implementation, for @CubeJerry
with OpenAI assistance, 2026-11-15.

Reviewed sources are root's `rectangular-chart-source-gate/PROOF.md` and the
separate `DISJOINT-COHORTS.md`; exact SHA256 pins appear in `RESULT.json`.
The general result improves the previous un-clipped rectangular filtration
by retaining each cohort's nonnegative contribution. The physical consequence
depends on the actual one-E6-stage source interface, not on dimension counting
alone.

## 1. Universal argument checked independently

Let K=ker(I-UP). For a fixed order, let K_i consist of kernel vectors supported
on the first i target cohorts. The coordinate-i map on K_i has kernel K_(i-1),
so it injects K_i/K_(i-1) into a space of dimension n_i V. For v in K_i the
equation at cohort i is v_i=U_i P_i v. Every acquisition row that reads only
strictly later cohorts vanishes on v, including the vacuously good zero rows.
The image therefore also has dimension at most (m_i-g_i)V. Consequently

    dim K_i/K_(i-1) <= V min(n_i,m_i-g_i).

Summing and subtracting from nV proves the stated clipped sum for every order,
hence its maximum. This reasoning permits m_i=0, arbitrary unequal n_i,m_i,
singular U_i, arbitrary block width, every field, and noncommuting internal
matrix coefficients. No rank-divisibility assumption is used.

For independent continuous priorities, condition on a cohort having fraction
u of priorities later than itself. An acquisition row supported on s<=d other
cohorts is good with probability u^s>=u^d. Dependence between different rows
does not matter: linearity gives E[g_i|u]>=m_i u^d. Jensen's inequality for the
positive part gives the claimed lower integral. Summing positive parts before
relaxing to the positive part of the sum is valid. Since u^d-1<=0, replacing
m/n by its upper bound λ can only decrease that integrand. Finally the
maximized cohort sum is an integer, giving the ceiling *before* multiplication
by V. This validates the statement even when the actual matrix rank is not a
multiple of V.

I independently integrated the positive part. For λ>1 its zero is
α=(1-1/λ)^(1/d), and integration over [α,1] gives
1-dλ/(d+1)+d(λ-1)α/(d+1). At λ=2,d=3, restricting to [4/5,1] gives exactly
119/1250, while (4/5)^3>1/2 ensures a nonempty omitted positive interval.
Thus the rational consequence and all numerical substitutions are sound.

## 2. Physical factorization and fixed disjoint cohorts

For the source-local interface, E maps each root cohort's independent X banks
to its actual outgoing source-channel X coefficients. Original Y couriers may
carry independent Y terms; discarding those terms is a favorable relaxation
and does not supply extra independent X inputs. The total number of distinct
source channels remains at most the two original record families, m<=2n.

After a channel reaches its single E6 chart, every permitted later chart is a
superchart. Mixing, duplication and Y anchors at that E6 chart can change the
linear coefficients but cannot move that channel's X contribution to a native
facet that does not contain the E6 chart. The admitted native geometry bounds
those facets by three. The channel's own root facet is absent because its
source line is contained in the E6 chart and is not contained in its own facet.
Thus the columns of D have at most three foreign-cohort supports and no own
support. Completion implies I=G+DE, with rank(G) bounded by the dimension of
the *actual global X-information space*. Transposing puts this equation in
the proved rectangular form. Globally supplied information must not be
identified merely with a count of terminal fields if additional retained
nonterminal histories remain accessible.

The disjoint-cohort corollary is valid. If all roots in a fixed cohort have
been jointly recoded at one common chart before any of its outgoing channels
branches, every later E6 destination contains all of those source lines.
It can therefore reach none of that cohort's own native facets. Grouping the
target coordinates by these larger cohorts preserves block diagonality and
the zero-own-cohort property; each E6 chart still reaches at most three *other*
larger cohorts. Unequal cohort sizes were already covered by the proof.
Counting support as three times the cohort size gives a weaker estimate and
does not show an escape from this stronger grouping argument.

The timing condition is substantive: an earlier channel may leave before a
later source joins an overlapping cohort. Such a schedule need not admit the
fixed common-chart factorization. A separate actual control in
`worker-a/overlapping-cohort-precursor/` demonstrates that physical possibility,
without claiming any useful global rank saving. Newly descended nonlocal
histories, successive interactions, additional paid channels, or a larger
global code likewise require a new factorization and cost analysis.

## 3. Independent computational controls

Run `python worker-a/review-rectangular-filtration/check.py` from the session
scratch root. The checker imports no author code. It constructs 128 seeded
rectangular examples over F2 and F3, widths one and two, two through five
cohorts, unequal positive target sizes, and zero through four acquisition
rows per cohort with total at most 2n. The block encoder and acquisition
matrices are built independently; actual row-block supports are recomputed
after zero entries. Every cohort order is enumerated. Direct Gaussian rank
is compared with the clipped maximum and the rational integral consequence.

Four explicit controls show why assumptions cannot simply be dropped:
own-cohort copying; a cross-cohort inverse encoder; 4n channels each reading
at most three foreign cohorts; and one channel reading eleven foreign cohorts.
The last two yield a rank-one all-ones residual on twelve target coordinates,
below the incorrectly retained two-channel/degree-three bound of two. The
first two produce a zero residual. These are scope controls, not counterexamples
to the actual theorem.

The native consequences are independently recalculated: b=1,2,4,16,80 require
at least 11,22,43,170,846 global width-V modes respectively, exceeding 9b.
The general proof supplies the all-field/all-width result; these finite checks
provide implementation and arithmetic controls only.

## 4. Admission and limits

Accept the theorem, its 2n-source one-E6 application, and the fixed-disjoint
common-chart corollary. No correction requested. Do not infer a lower bound
for all monotone algorithms, all cross-root recoding, or every stored history.
The source locality, one-E6 continuation, field/block linearity, actual global
information dimension, and total physical source-channel cap are all retained.
All five foundational assumptions and complete multiplication accounting remain
open or inherited exactly as before. This is a useful scoped obstruction to
an otherwise tempting source repair, not a new complete κ.
