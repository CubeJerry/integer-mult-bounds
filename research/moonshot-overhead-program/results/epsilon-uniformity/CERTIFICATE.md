# Quantitative uniformity: scope of the published certificate

Status: **proved analytic consequences of a stated successful-attempt contract**.
The diagonal result is a **scoped negative result for one certificate**. None
lower-bounds the actual machine or integer multiplication. These diagnostics
are preparatory, not a new multiplication theorem.

Source: OpenAI `math` at `3344da59991ed94f9ba711217b29c1d760badfa6`, tape
`build/uniformity.tex`, Section `sec:single-machine`; baseline in
`build/intro.tex`, Theorem `thm:uniform-main`.

## 1. Complete attempts and the global bound

Let n>=2, L=1+log2(n), x=log2(L), j>=1. A complete attempt includes decoding
its program/chunk pair, generation, interpretation, copying/gathering inputs,
all chunk products, erasure, shifted accumulation and final output. Tape
fences apply during generation. For each j, suppose a specified pair has
index i_j and constants A_j>=1, integer N_j>=2 such that for every n>=N_j,
on every input, it succeeds within the fences in at most

    A_j n L^(1/2+1/(j+2))

actual interpreted steps. N_j includes availability of its chunk count.
The manuscript gives fixed-j existence, not a quantitative growth law in j.

Round s grants attempt i at most 2^(s-i) steps. Amortized clocks, abort
cleanup and control give O(2^s) total round cost: the allowances sum to less
than 2^s and polynomial control in s is O(2^s). An attempt requiring t steps
finishes by round i+ceil(log2(t+1)). The geometric sum of rounds is
O(2^i(t+1)), with a constant independent of i and t, plus O(n) initial marking.
The schoolbook attempt bounds the last round by O(log(n+1)), keeping clocks
and control in O(n) cells. Every completed attempt gives the exact product.

Put D_j=2^i_j A_j, d_j=log2(D_j), b_j=log2(1+log2(N_j)). With inf(empty)=infinity,
an all-length sufficient envelope is

    H_all(n)=1+min(n/sqrt(L), inf_{b_j<=x} D_j*2^(x/(j+2))).       (1)

There is one constant C0 with T(n)<=C0*n*sqrt(L)*H_all(n). The schoolbook
constant is absorbed into C0, as is the additive one in t+1. Each candidate
inequality uses the same scheduler constant, so taking the infimum is valid
without assuming attainment. For n=1 use a fixed direct computation.
For sufficiently large n the feasible set is nonempty, and the focused
certificate is

    H_cert(n)=1+2^F(x),
    F(x)=inf_{b_j<=x}(d_j+x/(j+2)).                             (2)

(1) can be smaller than (2). Neither is an equality for actual runtime.

## 2. Elementary envelope/exponent equivalence

For H>=1 and x>0 set delta_H=log2(H)/x. Then L^delta_H=H exactly. Thus
H=O(1) iff delta_H=O(1/x); H=O(x^a) iff
delta_H<=(a log2(x)+O(1))/x; and H<=2^{O(x^beta)} iff
delta_H=O(x^(beta-1)), for a>=0 and 0<beta<1. The polynomial statement is
an eventual upper inequality, not an asymptotic equality. Bounded H need
not converge to 1. These conversions contain no new algorithmic result.

## 3. Exact coverage and the bounded-constant trap

A candidate term in (2) is at most K exactly on the interval

    I_j(K)=[b_j,(j+2)(K-d_j)],                                (3)

empty when its right endpoint is below b_j. Eventual coverage of
X={log2(1+log2(n)): integer n>=2} by union_j I_j(K) implies F<=K.
Conversely F<=K implies coverage by union_j I_j(K+eta) for every eta>0.
Consequently F=O(1) is equivalent to eventual coverage for some fixed K.
Slack is necessary at a prescribed level: with b_j=1,d_j=K, F(x)=K for x>=1,
although every contributing term is strictly greater than K.

Bounded constants along an infinite subsequence are insufficient. Set d_j=0,
b_j=(j+2)^2. For x>=9, F(x)=x/floor(sqrt(x))>=sqrt(x). Integer thresholds
can realize these b_j exactly: N=2^(2^B-1) gives log2(1+log2(N))=B for
every integer B>=1. This example is abstract, not the source candidate family.

The real-x extension preserves eventual boundedness. Between consecutive
attainable x_n,x_(n+1), there is no new b_j since N_j is an integer. Active
lines have slopes at most 1/3, so F(x)<=F(x_n)+(x-x_n)/3 on that half-open
interval. Since x_(n+1)-x_n tends to zero, eventual boundedness on X is
equivalent to boundedness on the real half-line with harmless fixed slack.
Regular slowly varying rates transfer similarly; an arbitrary discontinuous
target should instead be stated directly on X.

## 4. Growing constants forbid a bounded certificate

If d_j tends to infinity, then F(x) tends to infinity (empty feasible sets
have value infinity). Fix K, choose J with d_j>K+1 for j>=J, then take x
larger than all (j+2)(K+1-d_j) for j<J. Every term is greater than K+1;
the infimum is at least K+1>K. Threshold restrictions only raise it.

Distinct positive integer indices i_j necessarily tend to infinity, because
only finitely many can lie below any fixed bound. Since A_j>=1 gives d_j>=i_j,
the displayed source certificate for distinct labelled attempts cannot give
H_cert=O(1). This does not prove that the actual machine has unbounded overhead:
an upper estimate is not a lower bound on what it estimates.

## 5. Ordinary full diagonal enumeration

The source says computable diagonal order without a pairing formula. Adopt
explicitly the additional convention that all pairs (j,k), j>=1,k>=0, are
ordered by nondecreasing j+k, with index 1 reserved for schoolbook. There
are q(q-1)/2 pairs with j+k<q. Any pair with first coordinate j therefore
has index at least 2+j(j-1)/2, regardless of ties or its chunk count.
This is at least (j+2)^2/9: multiplying their difference by 18 gives
7j^2-17j+28>0. With y=j+2 and A_j>=1,

    d_j+x/(j+2)>=y^2/9+x/y>=(3/2)*(2/9)^(1/3)*x^(2/3).         (4)

The last expression is the minimum over real y>0, at y^3=9x/2. Thus
F(x)=Omega(x^(2/3)) and H_cert>=2^{Omega(x^(2/3))}, irrespective of thresholds
or better candidate constants. Every poly(x) certificate is excluded under
this convention. This does not exclude a sharper analysis of the machine,
different enumeration/weights, sparse subsequences or other multipliers.
The exact pairing in the separate Lean development is not identified here.
No rate in (4) is attributed to an arbitrary interpretation of diagonal order.

This motivates Route B's scheduling replacement before seeking a poly(x)
certificate. It is a source-specific diagnostic, not a global lower bound.

## 6. Rate extraction with integer choices

Write y=j+2>=3; assume the following bounds uniformly for all sufficiently
large j, with constants independent of j.

If d_j<=a log2(y)+c and b_j<=B*y, for a>=0,B>0, choose
y=floor(x/(2 max(B,1))), j=y-2. For large x, y>=3 and
y>=x/(4 max(B,1)). Then b_j<=x/2 and x/y<=4 max(B,1), giving
F(x)<=a log2(x)+O(1) and H_cert=O(x^a). When a=0 this is bounded.
These hypotheses cannot hold for the original diagonal certificate in Section 5.

If d_j<=A*y^p+C and b_j<=B*y^(p+1), p>0, take
y=floor(c*x^(1/(p+1))) for fixed
0<c<=min(1,(2 max(B,1))^(-1/(p+1))). Eventually y>=c*x^(1/(p+1))/2>=3.
Feasibility follows from B*c^(p+1)<=1/2; both d_j and x/y are
O(x^(p/(p+1))). Therefore H_cert<=2^{O(x^(p/(p+1)))}.

For any specified feasible integer choice j(x), the universal transfer is
F(x)<=d_{j(x)}+x/(j(x)+2). A proof of the growth laws and feasibility, rather
than a formal unconstrained optimization, is the indispensable algorithmic step.

## 7. Effective families still need quantitative moduli

Let R be a computable nonnegative rational-valued function on positive integers
with R(m)/m->0. There is a computable increasing sequence of finite integer
thresholds b_j, with d_j=0, for which F(x)/x->0 but
F(X_q)-R(X_q)->infinity along a computable sequence of integer X_q.

Set b_1=1. Given b_q and the preceding X, search integers
X_q>=max(b_q,X_(q-1)+1) until

    X_q/(q+2)>=2q,       R(X_q)<=X_q/(2(q+2)).

For q=1 omit the preceding-X condition. The limit assumption guarantees
termination. Set b_(q+1)=X_q+1. At x=X_q only j<=q are feasible, so
F(X_q)>=X_q/(q+2) and F(X_q)-R(X_q)>=q. For each fixed j, however,
F(x)/x<=1/(j+2) once x>=b_j. Letting j grow proves F(x)/x->0.
Each b_j is realized exactly by N_j=2^(2^b_j-1), so the witness points X_q
are also attainable from integer bit lengths.

Thus fixed-epsilon guarantees, even with a total effective threshold generator,
do not force a prescribed subpower envelope. This is an abstract inference
limitation, not a complexity lower bound. Effectiveness asserts termination;
it gives no polynomial, elementary or useful bound on generation time.

## Credits and open questions

OpenAI November 24 manuscripts and cited predecessors; @CubeJerry's programme;
analysis and drafting with OpenAI GPT-6 Astra Pro assistance. No authorship of
the source multiplication theorem is claimed. Next: obtain actual A_j,N_j
growth bounds, audit the alternative schedule, and control recursive routing
tolls. No complete new overhead bound follows from this document alone.
