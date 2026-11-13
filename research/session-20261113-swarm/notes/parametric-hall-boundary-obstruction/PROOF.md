# A two-step escape blocks the ball-core Hall extension

This is a negative structural lemma about the proposed parametric Hall
certificate. It proves no global outward lower bound1/2 and does not disprove
such a bound. The argument uses no period, conserved sum, or equivariance of
the hypothetical rounder. Prepared with substantial OpenAI Codex assistance,
Apache-2.0. No standalone PR is proposed without further review.

## Setup and precise conclusion

Let

H=((1,1,1,1),(1,-1,1,-1),(1,1,-1,-1),(1,-1,-1,1)), U=H/2.

For b>0 and T⊂Z^4, write N_b(T) for the complete integer-output neighborhood
defined by ||y-Ux||<=1 and ||y||-||x||<b for some x∈T. Let
B_R={v∈Z^4:||v||^2<=R}. For an integer a>=2 put

R0=4a^2+3, R1=4a^2+2a+1,
beta_a=sqrt(R1)-sqrt(R0), gamma_a=sqrt(R0+3)-sqrt(R0),
Z_a=O^+(a,a,a,a+1).

Here O^+ is the signed-permutation orbit with the given absolute coordinate
multiset and positive product of signs. It contains32 points.

**Lemma.** For every a>=2 and b>gamma_a there is no N⊂B_R0 satisfying

N_b(N∪Z_a)⊂N.

In particular this containment is impossible at b=beta_a for every integer
a>=3, regardless of which points or orbits are deleted from the ball.
The radius-five construction a=2 is not contradicted: gamma_2>beta_2.
Thus the attempted same-core, ball-contained Hall proof does not extend
along this parameter family. The lemma does not assert that every set
N∪Z_a fails Hall's inequality against its actual neighborhood or against a
different target set. That stronger assertion has not been established.

## Exact D4 geometry and candidate counts

Let D4={v∈Z^4:sum v_i is even}, and h=(1/2,1/2,1/2,1/2).
All coordinates of Hx have parity sum x_i. Also sum(Ux)=2x_1 and U^2=I.
It follows that U maps D4 bijectively to D4 and

U Z^4=D4∪(h+D4).

For an integer-image row Ux∈D4, the radius-one integer outputs are exactly
Ux and Ux±e_i: nine candidates. For a half-integer-image row, every output
coordinate must be one of its two nearest integers. All16 choices have
four squared errors1/4, hence exact total error1; any other choice has
squared error at least(3/2)^2+3(1/2)^2=3>1. These are complete neighborhoods,
not selected samples of nearest points.

The graph has a paired W(D4) action. A member of W(D4) permutes coordinates
and changes an even number of signs. U normalizes this group: it preserves
D4 and hence its norm-squared-two roots ±e_i±e_j. Conjugation by U therefore
permutes the root reflections, which generate W(D4). For A∈W(D4), put
B=UAU. Then B∈W(D4), BU=UA, and A→B is a bijection. Thus (x,y)→(Ax,By)
preserves error and both norms. This is a symmetry of the allowed graph;
the unknown rounding map itself is not required to respect it.

For a pattern with one distinct positive coordinate and three repeated
positive coordinates, its fixed-product orbit has4*2^3=32 points. A pattern
with multiplicities2,1,1 has12*2^3=96. With zeros, their signs absorb the
even-sign restriction. These elementary counts will suffice; no large
lattice-ball counting or finite flow computation is needed.

## The explicit escape and proof of the lemma

Consider three integer points

z=(a+1,a,a,a), x=(2a,1,1,1), y=(a+2,a,a-1,a-1).

They satisfy exact identities

Uz=(2a+1/2,1/2,1/2,1/2),
Ux=(a+3/2,a-1/2,a-1/2,a-1/2),
||z||^2=R1, ||x||^2=R0, ||y||^2=R0+3,
||x-Uz||^2=||y-Ux||^2=1.

Since a>=2, R1>R0. The first edge z→x is inward and belongs to every
strict graph with b>0. If N_b(N∪Z_a)⊂N, z∈Z_a forces x∈N. Therefore
x∈N∪Z_a, and when b>gamma_a its second edge forces y∈N. But y lies
outside B_R0. This contradicts N⊂B_R0 and proves the lemma.

At b=beta_a, the second edge is strict precisely when

R0+3<R1 ⇔ 4a^2+6<4a^2+2a+1 ⇔ 2a>5.

For integers a>=2, this means exactly a>=3. At a=2 its squared output norm
is22, exceeding R1=21, so the edge is excluded by the strict-beta_2 filter.
The successful a=2 certificate is therefore a genuine small-parameter
phenomenon that this proposed extension cannot inherit.

## Symbolic neighborhood and forced-orbit counts

The complete strict-beta_a neighborhood of Z_a can be described exactly.
At the representative z, all16 error-one corners choose large coordinate
2a or2a+1 and three coordinates0 or1. Every large-coordinate2a corner is
inward, because its squared norm is4a^2+k<=R0<R1,0<=k<=3.
No large-coordinate2a+1 corner is strict-beta_a. For the least such norm,
the required comparison follows from

[(2a+1)+sqrt(R0)]^2-4R1
 =2(2a+1)(sqrt(R0)-2a)>0.

Thus (2a+1)-sqrt(R1)>sqrt(R1)-sqrt(R0). Larger corners are excluded too.
There are exactly eight strict corners per Z_a input. By the paired action,
their union is the disjoint union of

O(0,0,0,2a), O(0,0,1,2a), O(0,1,1,2a), O^+(1,1,1,2a).

Its size is8+48+96+32=184. In particular it forces the complete32-point
orbit X_a=O^+(1,1,1,2a) into a proposed target core N.

For a>=3, each X_a input has exactly three error-one neighbors in
Y_a=O^+(a-1,a-1,a,a+2), all strict-beta_a and all outside B_R0. At the
representative x they select the large upper corner and exactly one of
the three small upper corners. The paired group action supplies every
Y_a point. Since |Y_a|=96 and32*3=96, each Y_a output has one such X_a
neighbor. Consequently the certificate forces at least96 output points
outside its permitted ball. Merely deleting more inside-ball orbits cannot
repair its neighborhood-containment claim. This escape count alone is not
a general Hall-cardinality impossibility argument.

## Limits and predecessor relation

The candidate thresholds are positive, strictly increasing for real a>1,
and tend to1/2: rationalization gives
beta_a=(2a-2)/(sqrt(R1)+sqrt(R0)), and differentiation has positive sign
because
(4a+1)^2*R0-(4a)^2*R1=36a^2+24a+3>0.
But gamma_a=3/(sqrt(R0+3)+sqrt(R0)) tends to zero. Hence existence of this
same-core containment would require b<=gamma_a, contradicting beta_a
already from a=3. A limit of candidate boundary increments is not a limit
of proved Hall lower bounds.

The frozen R5 compact proof uses a=2, with
N=B19\(O0033∪O0133), T=N∪O2223^+ and deficiency32. Its theorem remains
unchanged. This note did not read or use C's new bounded search constructor,
code, or proof. The independent affine-point and orbit calculations here
are not a shared search mechanism. The global infimum at error cap one
remains unresolved by this note; in particular,1/2 is neither established
nor excluded. A larger target core, several added input orbits, a non-ball
shape or a different Hall certificate needs a new analysis.

Ali Romman's #6509 supplies the global bijective error-one Gaussian map;
Nick Petalas's #6619 supplies the rational norm-rounding obstruction and
credits ywz65's #2589 finite-ball argument. The current CubeJerry workstream
and frozen R5/compact verification supply the beta_2 lower bound and the
H4/2-to-Gaussian-pair transfer. D4 geometry, orbit counting and Hall's theorem
are classical. Exact source pins are in SOURCES.json. No multiplication
constant or framework assumption changes.
