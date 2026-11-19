# Exact fully early H linearization and necessary source coupling

**Local interface theorem and scoped source obstruction, pending separate
review. No new kappa.**

At the actual fully early H263 chart, nonlinear processing cannot evade an
exact direct-sum information constraint. The current identically repeated
full64 source cannot complete this chart for the unchanged target blocks.
Different uncoupled matrix copies also fail. A continuation must change
source coupling, relevant target blocks, or a retained route/phase premise.

## 1. Exact abstract theorem

Let F be finite and z range over F^N. There are m outgoing packets with
alphabet F^ell, where N=m*ell. Their combined encoder Y=(Y_D)_D must
preserve z, hence is a bijection to the full product alphabet. Receiver i
sees packets A_i and requires a linear observation T_i z of rank
r_i=|A_i|*ell. Put W_i=row(T_i). For each port D put I_D={i:D in A_i}.
Assume every I_D is nonempty and

    intersection_(i in I_D) A_i = {D}.                 (1)

Define Q_D=intersection_(i in I_D) W_i.

**Theorem1.** An exact preserving code exists, allowing arbitrary
deterministic encoders and decoders, if and only if

    dim Q_D=ell for all D,   direct_sum_D Q_D=(F^N)*.  (2)

When(2) holds a linear code exists over the same F, with the same packets
and no additional information channel. For every nonempty receiver set J,

    dim intersection_(i in J) W_i
        = ell * |intersection_(i in J) A_i|.          (3)

### Necessity

Uniform z gives independent uniform packets, because their full encoder
is bijective. The visible tuple Y_(A_i) has exactly |F|^r_i values. Exact
recovery of a surjective rank-r_i target makes it a bijective function of
T_i z.

A common function of linear observations factors through the intersection
of their row spaces: invariance under each kernel gives invariance under
the sum of kernels. A common function of coordinate subtuples of a full
Cartesian product depends only on their intersection coordinates: changing
a coordinate outside the intersection keeps at least one subtuple fixed.
Both facts apply to arbitrary nonlinear functions.

Thus Y_D is a function of Q_D z. Conversely, Q_D z is a function of every
T_i z for i in I_D, hence of every Y_(A_i); by(1) it is a function of Y_D
alone. They are bijectively equivalent, so dim Q_D=ell. All packets are
independent, so the combined Q_D observations have rank N. Their dimensions
sum to N, proving the direct sum. Applying the same two common-function
facts to any J proves(3).

### Sufficiency

Choose a basis of each Q_D and transmit its ell linear coordinates. The
combined map is invertible by(2). For D in A_i, Q_D lies in W_i. Their
direct sum has dimension |A_i|ell=r_i, so equals W_i and supplies a linear
decoder. No field extension or generic selection is needed for this local
criterion.

## 2. The actual H263 owner cut

The authenticated H263={0,61,62}. At bank480 each donor sends30 genuine
early fields. Its45 D4 exits each carry2 early fields, with no late fields
or informative bypass. Preserving every original early X at Hub therefore
requires the H output to distinguish all90 inputs. Stationary H caches do
not cross this cut. These counts scale with the retained atlas.

At ordinary quotient width p, N=3p and ell=p/15. The33 joint-tight native
receivers each see15 ports. All99 relevant proper target blocks are I:
receiver80 and donor10, the only perturbed stars, are absent here.

Every port is isolated by a triple of joint-tight receivers. In particular,

    A_4 intersection A_5 intersection A_6 = {D2835}.  (4)

The checker emits such a triple for every port, proving(1) directly. It
reconstructs all528 receiver-pair and5456 triple intersections and the
actual owner counts. Pair intersections contain3 or6 ports; triple counts
are0,1,2 or6.

Once compatible source inverse fibres supply the graph targets W_i,
condition(2) is an exact nonlinear necessary and linear sufficient test:
the45 common port spaces must each have dimension p/15 and be independent.

## 3. Identical repetition requires quotient block width divisible by15

Suppose a source consists of r identical copies of base linear quotients
of width d, so p=dr. Every tight source view and its inverse repeat
identically. Identity target blocks at H263 then give local graph spaces

    W_i=V_i tensor F^r,      dim V_i=d.                (5)

The required common inverse-fibre alignment is a prior necessity; if it
fails, the source is already excluded. Arbitrary copy mixing after source
emission does not alter(5). Apply(3) to the isolating triple(4):

    r*dim(V_4 intersection V_5 intersection V_6)=dr/15.

Cancelling r shows that d/15 is an integer.

**Corollary2.** Identically repeated base-width16 source quotients cannot
realize the H263 targets and preserve all early owners on these routes.
This includes the full64 covariant and general two-evaluation sources when
repeated as stated on independent End(S) copies. Their source-only theorem
remains valid; the obstruction concerns the missing shared H decoder.

A repeated block coupling k sixteen-spinor quotient copies requires
15|16k, equivalently15|k. Identical blocks must therefore couple at least
15 matrix copies. At the smallest compatible bank3840 that is the entire
source bank. This necessary dimension condition is not code existence.

## 4. Varying uncoupled copies fail too

Suppose a common H input-dual decomposition is direct_sum_s E_s and every
target splits as W_i=direct_sum_s V_(i,s), with V_(i,s)<=E_s and
dim V_(i,s)=d_s independent of i. Different linear maps in separate
original matrix copies have this property after their required identity
inverse fibres align. Donor-specific gauges that mix the original
components are outside this premise.

Intersections preserve the direct decomposition. Set

    Q_(D,s)=intersection_(i in I_D) V_(i,s),
    q_(D,s)=dim Q_(D,s), a nonnegative integer.

From Theorem1, W_i=direct_sum_(D in A_i) Q_D. Taking a component yields

    sum_(D in A_i) q_(D,s)=d_s for every i.             (6)

An explicit native mod3 dual is: weight2 on receivers4,5,6,7,53,55;
weight1 on receivers8,10,47,48; weight0 on the other23. The total weight is16.
At every actual port the sum of audience weights is3,6 or12, divisible
by3. Weighting(6) and summing therefore makes16d_s divisible by3. Thus

    3 divides every d_s.                              (7)

**Corollary3.** Independently varying uncoupled width16 source maps also
fail. Varying their coefficients is insufficient: each common source
component must couple at least3 sixteen-spinor copies, or an explicit
construction must remove the common-component premise. General coupled
arrays and altered source gauges are not excluded.

The two conditions have different scopes. Varying coupled blocks need
3-divisible quotient width; identical repetition requires15-divisible
width. Neither condition alone gives compatible source coefficients.

## 5. Positive controls and the paid sufficient compiler

The existing five actual nine-port classes show that3 is tight for this
local component-size test. In one class, give each donor3 scalar inputs
and apply a9-by9 Vandermonde matrix over GF32. Every receiver sees3 ports
and has an invertible3-by3 projection on each donor. This component has
d=3 and port dimensions1 on that class,0 elsewhere. Five classes give a
45-by45 invertible H word with d=15, satisfying the repetition divisor.
Tensoring with S=F^16 gives five varying coupled3-copy components of width48
and the full p240 H module. This is local capacity/word feasibility, not
source inverse-lift gluing; the fixed-class D obstruction remains relevant.

A negative control drops early preservation: encode only z0+z61+z62 using
a45-by15 Vandermonde matrix over GF64. Each receiver recovers its target
from15 ports, but the whole output rank is15 instead of45. The targets
need not then satisfy(3). This identifies the indispensable owner-
preservation premise and avoids a false impossibility claim for arbitrary
receiver decoding without early restoration.

If actual graph spaces satisfy(2), bases of Q_D form an invertible H
matrix. Over GF(2^e), expand to n=3pe binary whole-record coordinates.
In-place elimination gives at most2(n^2+3n) ADD for the map and its inverse,
with no new MOVE, INIT or dirty CLEAR for this pure-early local map. Every
holder is an actual co-located early owner; no Y owner visits H263. At
p240,e9, n6480 and this bound is84,019,680 ADD. All other source, middle,
global inverse, return, physical-compiler and complete-caller costs remain
separate. This is a local finite bound, not a complete supplier invoice.

## 6. Next construction and scope

Extend the full64 source to one genuinely coupled fifteen-copy block, or
to varying coupled blocks of3-divisible quotient width, and solve its
actual inverse-graph spaces jointly with(2). The same source must satisfy
all other native charts and avoid fixed-class middle obstructions.
Nonlinear H processing gives no extra existence benefit on this exact
fully early cut.

Changed local target blocks, informative bypasses, altered early chronology,
nonsaturated receivers, or different component premises need fresh proofs.
No MOVE lower-bound tariff, supplier, recurrence, new kappa or foundation
discharge follows. All five foundational assumptions remain.

Credit @CubeJerry; native asymmetric, common-function, repeated-field-two,
fully early H263, Clifford-source and nine-port authors. S028 Worker A
derived the common-coordinate linearization, divisor15 gate and explicit
mod3 component witness, with substantial OpenAI assistance. Independent
review is recorded separately.
