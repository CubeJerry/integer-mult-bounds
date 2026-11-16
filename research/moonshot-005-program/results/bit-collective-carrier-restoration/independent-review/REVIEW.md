# Independent review: simultaneous physical restoration

Reviewed source: `work-S018/R/RESTORATION-LEMMA.md`.
Reviewer: Worker C. No author verification code was imported.

## Verdict

The proposition is correct with its stated current co-location, independent
input and paid-operation premises. The construction produces an invertible
update on the original carrier records while keeping every raw and retained
side record unchanged. No correction to the mathematical statement is needed.

## Universal proof review

Writing the observations as z=Ax+Br, s=Cx+Dr and rawr, a simultaneous kernel
vector of A and C makes two distinct x inputs observationally identical for
the same r. Every deterministic subsequent algorithm restricted to those
observations therefore gives identical results on those two inputs and cannot
restore x correctly. This is a genuine nonlinear impossibility within the
specified information interface; it is not a claim about new source access.

For sufficiency, let K=kerC. The stacked-rank hypothesis makes A|K injective.
Choose a basis k1,...,kd of K. The lists Ak1,...,Akd and k1,...,kd are both
linearly independent and can be extended separately to bases of k^h. The map
between those extended bases is an invertible U with UAkj=kj. Consequently
I−UA vanishes on K. The annihilator of kerC is exactly rowC over any field,
so there is a matrix V with VC=I−UA. With W=−UB−VD, direct substitution gives

    U(Ax+Br)+V(Cx+Dr)+Wr=x.

The ambient update matrix on(z,s,r) is block triangular with diagonal blocks
U,I,I and is therefore invertible, even when those current observations are
linearly dependent as functions of the original inputs. Thus the proposed
restoration does not rely on unpriced discarding of side information.

This basis-extension argument handles A singular and C rank deficient as well
as the two extreme cases C=0 and A=0. No assumption of a particular field
cardinality, algebraic closure or positive characteristic is needed.

The exact linear side deficit is nullityA: the restriction C|kerA must be
injective, so q≥dimkerA; a linear extension of a dual basis of kerA attains
equality abstractly. For finite fields, every fiber of A at fixedr has
|k|^nullityA members, giving the same necessary fixed-length side-alphabet
bound for arbitrary deterministic nonlinear side information. Physical source
acquisition and delivery of that side information are explicitly separate.

## Physical and width scope

The statement assumes that z, s and rawr are **simultaneously** at the actual
restoration chart. A raw x0 value at ground does not satisfy this premise for
a Hub restoration. Its existence elsewhere cannot be used in the formula.

For fixed binary matrices tensored with I_V, all algebra can be selected over
F2 and lowered to a fixed finite ADD word, with every swap implemented by
three ADDs. The conservative h(h−1)+3h bound follows by eliminating at most
h−1 off-diagonal entries per pivot and at mosth row swaps. Side/raw additions
cost at mosth(q+m) further ADDs. Nonbinary elementary scalings require their
own scalar implementation and price, as the source says. ArbitraryV-dependent
block matrices alone would not imply a uniform bounded instruction template.

The two identical mixed carriers control is valid: with z0=z1=x0+x1 and
s=x0 at the same chart, the three stated ADDs give z0=x0 andz1=x1 while
s is unchanged. Omitting s gives the collision vector(1,1), and no subsequent
deterministic observation-only map can repair both inputs.

## Independent finite controls

`review_restoration.py` exhausts every binaryh×h matrix A and every binary
side row subspace for h=1,2,3. It independently searches all invertible U
for I−UA in rowC, checks that existence agrees with full stacked rank, derives
V, and directly replays all carrier and two nuisance coefficient columns on
every positive instance. Every negative case has an explicit nonzero vector
annihilated by A and C. Both essential two-carrier examples are included.

The resulting census is in RESTORATION-RESULT.json. These are finite controls
of the matrix interface; the universal proof above establishes the all-field
claim. No new supplier, exponent, erasure service or compiler implementation
is inferred.

Credit @CubeJerry and the root author's precise physical restoration interface;
this linear-algebra argument is elementary and is not claimed as a novel
matrix-inversion theorem. Substantial OpenAI assistance.
