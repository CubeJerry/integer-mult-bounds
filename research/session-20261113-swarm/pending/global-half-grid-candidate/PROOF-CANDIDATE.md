# Candidate global error-one bijection with sharp bilateral radial slack1/2

Status at2026-11-13 12:00 UTC: root derivation and exact finite corroboration;
independent B proof and C implementation challenge still pending. Do not
publish this checkpoint as a verified contribution. Canonical basee54523517d0f03e58352e647c403a5af3e525a57.

Let U=H4/2, J=diag(1,1,1,-1), E=JU and R=UJU. With
s=(1,-1,-1,1), R=I-ss^T/2. Both E and R are orthogonal. U^2=R^2=I.

For even-total-parity integer x, Ux is integer with even total parity.
For odd integer x, t=Rx has four half-integer coordinates and odd coordinate
sum. R is a bijection from odd Z4 to A={t in(Z+1/2)^4:sum t odd}.
E maps B={t in(Z+1/2)^4:sum t even} bijectively to odd Z4.
Indeed sum Rx=sum x because sum s=0, and R sends A back to odd integers;
E^T y=UJ y is half-integral with sum2y1 even for odd integer y.

On every half-integer coordinate use one of two perfect pairings of the
line. Type0 pairs positive magnitudes(.5,1.5),(2.5,3.5),... and their
signed negative counterparts. Type1 has the central pair(-.5,.5), then
positive magnitudes(1.5,2.5),(3.5,4.5),... and signed negatives. Give every
coordinate the score equal to the smaller absolute magnitude of its pair,
except score0 for the central pair. Axes0,1 have type0; axes2,3 type1.

Choose the coordinate minimizing(score,index) and toggle its pair. Call
this M. Every coordinate's score remains unchanged when its pair is
toggled, including the central sign flip. Thus the selected coordinate is
the same on the return, and M^2=I. Exactly one coordinate changes by1,
so M swaps A and B and has displacement norm1.

If a central pair is selected, both endpoint norms are equal. Otherwise
write a for the lower magnitude in the selected pair. The other coordinate
of the same type has magnitude>=a. Both coordinates of the opposite type
have score and magnitude>=a+1: there is no central score0, the selected
score is minimal, and the two noncentral score progressions alternate in
steps1. Hence the smaller endpoint radius r satisfies

r^2 >= a^2+a^2+2(a+1)^2 =4a^2+4a+2.

The larger squared radius is r^2+2a+1. Since
4a^2+4a+2-(2a+3/4)^2=a+23/16>0,
r>2a+3/4 and therefore
sqrt(r^2+2a+1)-r<1/2.

Define F(x)=Ux on the even integer sublattice, and F(x)=E M(Rx) on the
odd coset. These are bijections of the even and odd cosets respectively;
for odd y the inverse is R M(E^T y). Since ER=U, the approximation error
on odd inputs is exactly1, and it is0 on even inputs. Orthogonality gives
bilateral radial distortion<1/2 at each finite input and supremum<=1/2.

The lower bound requires no bijection, parity or period premise. At
z_a=(a+1,a,a,a), a>=2, Uz_a=(2a+.5,.5,.5,.5). All error-one integer
outputs are its16 nearest corners. Among lower-first-coordinate corners,
the largest norm is sqrt(4a^2+3); among upper corners the smallest is2a+1.
The minimum absolute radial change is therefore
beta_a=sqrt(4a^2+2a+1)-sqrt(4a^2+3), provided the second gap is larger.
The latter inequality follows from
[(2a+1)+sqrt(4a^2+3)]^2-4(4a^2+2a+1)
=2(2a+1)(sqrt(4a^2+3)-2a)>0.
Rationalization gives beta_a=(2a-2)/(sqrt(4a^2+2a+1)+sqrt(4a^2+3)) ->1/2.
Every total error-one integer map has bilateral radial supremum>=1/2.
Thus the proposed bijection attains the optimal bilateral value.

For this construction, both directional outward suprema are also1/2.
For integer k>=0, direct formulas are
F(0,0,4k+2,1)=(2k+2,2k+1,-2k-1,-2k-1),
F(2k+1,2k+1,2k+2,2k+1)=(4k+2,0,-1,0).
The smaller/larger squared norms are16k^2+16k+5 and16k^2+20k+7.
Their square-root difference tends to1/2, in the two directions.
This is not a universal forward-only lower bound1/2.

The exact signed-permutation transfer H4=L(2C+)R_signed gives a global
bijection for the ideal #6509 Gaussian pair, with the same error and radial
bounds; define the negative provider by the actual inverse. It does not
inherit complex-sum preservation, phase covariance, fourth-power identity,
axis/tensor commutation, caller grids, fixed-word closure or physical tariff.
For example the transferred map sends(0,0,2,1) to(2,-1,1,1), changing the
complex sum. All five selected multiplication assumptions and kappa remain.

Root exact checks use only doubled integer coordinates, the explicit inverse,
integer radial inequalities and symbolic sequence polynomials. They cover
38416 half-grid-box cases,28561 full integer-cube cases,120 pseudorandom
signed inputs up to400 decimal digits, and8 huge directional sequences.
Three controls reject one-phase matching, an unbalanced1+3 phase split, and
selection by current magnitude instead of pair-invariant score. The universal
argument is the written pairing/coset/norm proof, not these finite checks.

The earlier R5/R9 finite package gives necessary forward lower
sqrt(78)-sqrt(73). If this candidate survives review, the global forward
interval becomes[sqrt(78)-sqrt(73),1/2]. Sharp bilateral optimality is a
different, stronger-direction contract. The original #6619 open question
asks the one-sided infimum, which would still not be completely solved.

Credit #6619 Nick Petalas, #2589 ywz65, #6509 Ali Romman and the current
@CubeJerry workstream. Lattice cosets, orthogonality and matching facts are
classical. Prepared with substantial OpenAI assistance; no human or formal
kernel acceptance. Do not publish before independent review and source gates.
