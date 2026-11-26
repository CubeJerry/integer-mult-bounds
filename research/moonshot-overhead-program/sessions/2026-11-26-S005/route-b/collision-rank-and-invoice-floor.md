# Label collisions, charged rank, and the polynomial-overhead budget

Status: **proved scoped algebra and positive-invoice analysis; independent
review requested**. These statements do not lower-bound actual tape time.
They identify a condition that a bounded-mass template must escape, even
if its free rectangles improve on the retained Hamming family.

The exact identity-on-labels decomposition is from Fourier `kernel.tex`
at OpenAI math `3344da59991ed94f9ba711217b29c1d760badfa6`, particularly
`eq:kernel-routing-block` and the charged/free rectangle construction.
The source uses a finite field for geometry and a different ring for
scalar weights. No reduction of scalar weights to the geometry field
is assumed below.

## 1. A field-independent collision rank bound

Let E be a D-dimensional vector space over F_q, with any bilinear pairing.
For i=1,...,N choose destination and source directions u_i,v_i satisfying

    <u_i,v_i>=1.                                       (CR1)

Let K be **any** field, not necessarily F_q. Let P,F be matrices over K
such that

    I_N=P+F,
    F_ij=0 whenever <u_i,v_j> is nonzero in F_q.        (CR2)

P is the aggregate charged correction and F the aggregate free part.
Signed weights, overlapping rectangles and cancellation inside F are
allowed, provided CR2 is exact. An all-ones target instead of I_N is
outside the theorem.

Partition labels by projective source direction [v_i]. No v_i is zero.
If v_i=c_i v for one nonzero v, then for i,j in that class,

    <u_i,v_j>=c_j/c_i !=0.

Therefore F restricted to the class is zero and P restricted to it is
the **full identity matrix**. If s projective classes occur and
r=rank_K P, then

    r>=max_class |class|>=N/s,
    r/N>=(q-1)/(q^D-1).                               (CR3)

This uses an identity principal submatrix over K, not a rank inequality
across different fields. The identity target is essential.

For R independent scalar rows per label, assume instead I_(NR)=P+F
and that every forbidden label block of F is zero. The same principal
block is I_(R|class|), so

    rank_K(P)/(NR)>=1/s.                               (CR4)

General row mixers in P do not evade this conclusion. Changing the
overall target or permitting non-free support may leave the hypotheses.

## 2. Sharper symmetric binary count and the actual Fourier role

Suppose q=2, the pairing is symmetric, and u_i=v_i=d_i with
<d_i,d_i>=1. The function v-><v,v> is linear over F2: cross terms
cancel and v_j^2=v_j. Since value one occurs, its one-fibre has exactly
2^(D-1) vectors. Consequently

    r/N>=2^(1-D).                                      (CR5)

If P is a sum of N_ch scalar weighted rectangles, rank(P)<=N_ch, giving

    N_ch/N>=2^(1-D).                                   (CR6)

More generally, use total normalized rectangle rank for block-row
coefficients. In particular,

    m r/N<=C or m N_ch/N<=C
       implies D>=1+log2(m/C).                         (CR7)

The source binary Fourier directions have exactly this symmetric
unit-self-pairing property, and the free part vanishes on all pairs
with nonzero pairing. Thus CR7 applies to arbitrary replacements within
that identity-on-labels interface: no Hamming, Cartesian, positive-weight
or particular degree hypothesis is needed. The result is about the
charged scalar rank even though the geometry is binary.

For D=2 equality is attainable: take t copies of each e_1,e_2 and
P=J_2 tensor I_t in direction/copy order. Its within-direction blocks
are identities, its cross-direction blocks are free, and rank(P)=t
for N=2t. Thus r/N=1/2=2^(1-D). This finite equality does not supply
an unbounded efficient template family.

## 3. Consequence for a dimension-charging positive invoice

Suppose a declared positive cost certificate charges at least
c sqrt(m) D for a completed template, and child width f lies between
a/(c_s m) and a/m. Its normalized child coefficient is at least
c' D. Under CR7 this is at least c'' log m at large m.

Therefore improving incidences to a constant while retaining that
dimension price cannot meet bounded local mass CT3 in
`critical-template-transfer.md`. A route through CT must share the
dimension work, change the geometry/target, improve a different
normalization, or leave this invoice. This does not prove that D
physical calls are necessary for every executor. For a sufficiently
large fixed arity cutoff, c''y>=2sqrt(y), so the next model can use
p=1/2 and B=2 on those arities. If bounded smaller arities are also
allowed indefinitely, their positive normalized gap must be checked
separately; an unexamined small template is not ruled out.

The next theorem quantifies this issue for arbitrary adaptive arities
and an explicit ordinary-work price. It extends the earlier constant-loss
invoice calculation, rather than lower-bounding arbitrary algorithms.

## 4. An arbitrary-arity log-squared invoice floor

Use x=log2(active width), y=log2(arity), with fixed terminal cutoff X.
Consider a finite decreasing chain x_0,...,x_t, with x_i>X for i<t
and x_t<=X. At level i choose y_i>=1 and require

    0<x_i-x_(i+1)<=y_i+c_0,                            (CR8)

for fixed c_0>=0. Take X>=2 and x_t>=0. Let positive bills satisfy

    R_t>=1,
    R_i>=2^(K y_i-x_i/2)+B max(1,y_i^p) R_(i+1),      (CR9)

where K>1/2, p>0 and B>1 are fixed. This bills polynomial-arity
ordinary work and a logarithmically growing normalized child factor.
CR9 is not asserted for actual runtimes merely bounded above by it.

**Theorem CR-I.** For some c>0 depending only on the fixed parameters,
every such invoice satisfies, at all sufficiently large x_0,

    log2 R_0>=c (log2(x_0+2))^2.                       (CR10)

Arity choices may vary arbitrarily. This order is attained by the
specified model on exact power-of-two width shapes.

### Lower bound

Write H=log2 R_0. Every recursive factor exceeds one, so all local
tolls and the product of all factors are bounded by R_0. Therefore

    y_i<=(x_i/2+H)/K,
    H>=sum_i [log2 B+p log2 y_i].                     (CR11)

Choose beta in (1/(2K),1) and set r=1-beta>0. For sufficiently large
fixed A (depending on K,beta,c_0), x_i>=A(H+1) implies

    x_i-x_(i+1)<=beta x_i,
    x_(i+1)>=r x_i,       y_i<=x_i.                   (CR12)

For sufficiently large x and 1<=y<=x there is a fixed c_1>0 with

    log2 B+p log2 y>=c_1 y log2(x)/x.                 (CR13)

If y>=sqrt(x), use p log2 y>=(p/2)log2 x; if y<sqrt(x), the right
side is at most c_1 log2(x)/sqrt(x), eventually less than log2 B.
By CR8, y_i>=(x_i-x_(i+1))/(1+c_0). Thus the i-th logarithmic
multiplier is at least

    c_2 (x_i-x_(i+1)) log2(x_i)/x_i.

For large x_i and CR12, g(z)=log2(z)/z is decreasing and

    integral_[x_(i+1),x_i] g(z) dz
       <=(x_i-x_(i+1)) g(x_i)/r.                     (CR14)

Sum through the first step reaching x_j<A(H+1), or until the terminal
cutoff if reached first. If x_0>=A(H+1), all preceding steps satisfy
CR12-CR14. The integrals telescope, giving

    H>=c_3[(log2 x_0)^2
                  -(log2(max(X,A(H+1))))^2].         (CR15)

The constant ln(2)/2 is absorbed in c_3. If H>=(log2 x_0)^2 already,
the claim holds. Otherwise the subtracted logarithm is O(loglog x_0)
and x_0>=A(H+1) eventually. For sufficiently large x_0 the bracket
is at least half (log2 x_0)^2, proving CR10 uniformly over all chains.

### Matching order and failed-premise controls

For even integer x_i choose even y_i within fixed factors of delta x_i,
where 0<delta<1/(2K), and take x_(i+1)=x_i-y_i. Stop at a sufficiently
large fixed even X. These are exact widths 2^(x_i) and arities 2^(y_i)
without divisibility rounding. The depth is O(log x_0), the sum of
log(y_i) is O((log x_0)^2), and the normalized tolls have bounded sum
by the strict subcritical margin. Unfolding the equality recurrence gives

    log2 R_0=O((log2(x_0+2))^2).                       (CR16)

The assumptions matter. For K<1/2 one almost-full descent has bounded
toll and only polynomial-x child loss. If factors may equal one, bounded
arity and geometric toll summation can give bounded overhead. Without
the local toll, one large descent costs only polynomial x. Without CR8,
a fixed small arity can jump directly to the base. Exact finite controls
are supplied separately; they do not establish the asymptotic theorem.

## 5. Interpretation and open next questions

At the integer scale x=log2 L, CR10 means a certificate overhead
2^Omega((log x)^2), exceeding every fixed polynomial in x. It is still
far smaller than the current stretched-exponential certificate. A real
family attaining that changed scale could be useful intermediate progress;
neither its existence nor a new multiplier is proved here.

CR3-CR7 are unconditional finite algebra. Their cost consequence retains
the positive dimension price, ordinary-work bill and regular split.
Arbitrary joint delivery, nonmonomial changes, altered targets with paid
recovery and cancellation-aware global schedules remain outside scope.

Open next questions: can a full-rate executor remove the dimension
multiplier rather than just improve incidence? Can a changed scalar
target be restored cheaply enough to avoid CR2? Can one finite family
meet CT2 and CT3 simultaneously with actual delivery CT4?

Credits: the OpenAI identity-on-labels charged/free construction;
programme critical-mass and positive-invoice analyses; @CubeJerry;
substantial ChatGPT research assistance. No full machine, Lean proof,
human refereeing, universal lower bound or priority claim is made.
