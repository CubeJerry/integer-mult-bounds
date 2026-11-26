# A minimum-spanning-tree schedule for shared Fourier states

Status: **proved exact finite-state scheduling refinement; independent
review pending**. The lead proposed the threshold-component mechanism;
routing A independently derived the components, exact tree weight,
factorial bound and executor below. This changes the free call invoice
beyond the support-Gray walk. Its optimized leading Psi scale remains.

Sources are the pinned OpenAI endpoints and canonical binary labels,
as mediated by the separately reviewed E003
`ROUTING-STATE-WALK-SHARING.md`. We retain that note's exact subspace
transition formula, source-compatible phases, fixed-array implementation,
and charged-rectangle routine. No universal tape lower bound is claimed.

## 1. The finite weighted state graph

Fix L>=2, t>=2, q=2^t, D=2+L(q-2). Vertices are the states
s in {0,...,t}^L with an odd number of nonzero coordinates. Their count is

    lambda=[(t+1)^L-(1-t)^L]/2.

Put a(0)=1 and a(b)=2^(t-b) for b>0. Distinct states have edge weight

    c(s,z)=1+sum_(i:s_i!=z_i)(max(a(s_i),a(z_i))-1).     (T1)

This is the exact combined source/destination transition invoice divided
by four, by W3--W5 of the state-walk note. It is a metric, but computing
a spanning tree does not require triangle inequality. All weights are
positive integers. The graph and its edge list are finite and effective.

## 2. Exact threshold components

At threshold w>=1 call a nonzero symbol high when a(b)>w. Let h be the
number of high symbols. Any changed high symbol would contribute at
least a(b)-1 to T1, and the additional one gives c>w. Hence every high
symbol and its coordinate are frozen within a threshold component.

Conversely fix such a frozen pattern. All other symbols are low. Reset
each nonzero low symbol to t; this changes one coordinate, preserves
the parity of the support, and costs at most w. The remaining zero/t
assignments with the required parity are connected by toggling pairs
of coordinates, each at cost one. This includes a single free coordinate,
where its parity fixes its value. Therefore a frozen pattern with at
least one free coordinate is precisely one nonempty connected component.

There are (h+1)^L patterns if each coordinate is high with h choices
or free. An all-high pattern has no free coordinate; it is an admitted
odd-support state exactly when L is odd. Thus the exact component count is

    C_L(h) = (h+1)^L                    if L is odd,
             (h+1)^L-h^L                if L is even.  (T2)

At w=1 there are t-1 high symbols. At w=2^k, 0<=k<=t-1, there are
t-1-k. No component merger occurs between these powers of two. The
initial graph with no edges has lambda components; the final graph has
C_L(0)=1. The parity qualification in T2 is essential.

## 3. Exact minimum spanning-tree weight

Kruskal's rule now gives the exact minimum weight

    M = lambda-C_L(t-1)
      +sum_(h=0)^(t-2) 2^(t-1-h)[C_L(h+1)-C_L(h)].     (T3)

At each threshold the component-count decrease is exactly the number
of new tree edges selected at that weight. Equivalently, every spanning
tree must connect the lower-threshold components, giving the same lower
bound by telescoping; the greedy construction attains it.

The complete graph may be generated and processed by exact integer
arithmetic. An alternative sparse graph uses active-low changes to t
and zero/t pair toggles. The component proof shows that it has the same
threshold connectivity and hence the same minimum tree weight. Either
construction is polynomial in the finite state count, L and t. Under
the retained parameter guard this remains polynomial in m, since
lambda<=q^L and the original label count is polynomial in m.

## 4. A closed tree traversal on fixed arrays

Choose as root a state with one active coordinate at level t. Its source
span has rank one. Traverse a minimum spanning tree depth first and
return to the root. Each edge is crossed twice. Add a state's rectangle
contributions only when it is first visited; return visits change bases
but add nothing. The tree's discrete visited flags and traversal stack
are finite control data. No numerical snapshot is stored at a tree node.

The source array and destination accumulator change their prepared
bases along each edge using the state-walk executor. Reverse traversal
uses inverse transitions on the live arrays. The same fixed auxiliary
phases cancel. The initial source preparation uses two calls and the
final destination flush uses 2(D-1), restoring ordinary coordinates.
Charged/pointwise contributions remain in a separate ordinary accumulator.
The resulting exact free invoice per original label row is

    F_tree = 2D+8M.                                   (T4)

All labels follow the same state tree, and their transition ranks are
label-independent. Arbitrary independent rows, complete spectators and
normalized child volumes are preserved. A constant number of payload
collections suffices, with polynomial-m descriptors and reused marked
regions. All partial-basis transitions are unitary; the earlier finite
precision and polynomial physical-work allowances remain available.

For q=2 the state metric T1 is not the actual transition cost: all source
and destination subspaces are constant. Use the reviewed four-call free
schedule instead. The q=2 charged-rank obstruction is unchanged.

## 5. A factorial bound independent of t in the incidence exponent

The exact T3 implies

    M <= (q/2) sum_(h>=0) 2^(-h) C_L(h+1).             (T5)

To see this, bound each positive difference in T3 by C_L(h+1), and
bound its separate lambda term by C_L(t). For even L,
lambda=[C_L(t)+C_L(t-1)]/2<=C_L(t); for odd L it is also at most
C_L(t). The h=t-1 term of the extended sum has coefficient one, so it
pays that term. Dropping the negative initial term only enlarges the sum.

Since C_L(h+1)<=(h+2)^L,

    sum_(h>=0) 2^(-h) C_L(h+1)
      <=4 sum_(k>=1) k^L 2^(-k)
      <=4 · 2^L · L!.

For the last inequality use
`k^L<=L! binom(k+L-1,L)` and the elementary generating sum
`sum_(k>=1)binom(k+L-1,L)z^k=z/(1-z)^(L+1)` at z=1/2.
Consequently

    M<=2q · 2^L · L! <=2q(2L)^L,
    F_tree<=2D+16q(2L)^L.                             (T6)

This replaces the Gray schedule's incidence factor of order
lambda/t by a function of L alone in T6. When t/L grows, it can save
much more than a fixed polynomial factor: the previous powers of t are
replaced by factorial growth in L. Exact finite comparisons should use
T3, since T6 is a deliberately coarse universal estimate. The compiler
may choose the least of the separately proved old, destination-gauge,
lexicographic, support-Gray and tree invoices.

## 6. The changed invoice still has the same leading scale

There are lambda vertices and all edge weights are at least one, so
M>=lambda-1. Thus T4 retains both a D boundary charge and a lambda
transition charge. Adding the unchanged highest charged-rectangle term,
the full tree invoice dominates

    J_tree=D+lambda
       +mD binom(L,floor(L/2))q^(-ceil(L/2)).          (T7)

The independently reviewed W9--W11 proof applies to precisely these
positive terms: for m>=2^16 and q>=4,

    log2 J_tree >= (1/2)sqrt((log2 m) log2 log2 m).      (T8)

At q=2 the charged term alone is at least m. The retained optimized
labels still give the matching O(Psi(log m)) upper profile, either
by using T6 or by choosing the previously admitted schedule. The tree
therefore changes the literal invoice substantially without changing
its optimized leading asymptotic order. No actual-runtime lower bound
has been inferred.

## 7. Finite checks and next questions

`ROUTING-verify-state-tree.py` checks complete finite threshold graphs,
their frozen-pattern components, actual minimum spanning trees and
closed traversals against T2--T4, as well as integer bounds T6--T7.
Its receipt records case sizes. No full tape multiplier is executed.

Further progress would need to avoid visiting all distinct prepared
source subspaces, change the charged label term, or combine contributions
through a different operator representation. Finding a cheaper tree
inside this exact state metric is closed by T3. A smaller physical
middle-routing toll remains a separate open problem.

Credits: @CubeJerry; pinned OpenAI endpoint geometry; E003 lead's
threshold-component/MST proposal; E003 routing A's independent proof,
factorial estimate and executor; earlier E003 state-walk, gauge and
literal-invoice suppliers; substantial ChatGPT assistance. No new complete
H, general runtime lower bound, formal proof or human refereeing is claimed.
