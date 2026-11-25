# Independent review of characteristic-two rank truncation

Reviewer: Route C, 2026-11-25. Status: **mathematical claims pass; one wording
correction identified**. Reviewed root proof SHA-256
`b59f5b7dcaecb59d2fddb97d24e148936894d0553d6d4b3c7714f4e642613cac`.

## Direct degree-cut bound

For t=floor((m-d)/2), input degrees <=t contribute rank at most
A=sum_(k<=t)binom(m,k). All higher inputs land in degrees >=t+d+1.
The latter output dimension equals the binomial sum through
`m-t-d-1`, which is t-1 when m-d is even and t when it is odd.
Thus it is at most A. This verifies the parity-sensitive cut, and the
proof applies to every multiplier with minimum degree d. In fact this
degree-cut statement is valid over every field; characteristic two is
needed for its group-algebra and subsequent automorphism applications.

The Chernoff calculation has the correct constant. For displacement d/2,
the exponential parameter -2d/m gives exponent -d^2/(2m). Hence the
normalized bound is `2 exp(-d^2/(2m))`, and the claimed constant-error
degree `sqrt(2m ln(2/delta))` follows.

## Exact binary-degree conjugacy

I independently derived the coefficient of a fixed h-element set in
e_(2a)(y). Reading the set from largest index downwards, unselected
indices can occur only between the first and second selected index,
then between the third and fourth, and so on. Distributing h-2a
unselected indices among a gaps gives `binom(h-a-1,a-1)`.
For a a power of two this is odd precisely when a divides h, by its
lowest binary digits. This proves the stated automorphism coefficient.

The change `y_i=x_i prod_(j<i)(1+x_j)` has the stated recursive inverse
and triangular monomial matrix with diagonal one. Therefore it is an
algebra automorphism. The unit identities

    E_d=P_(d-1) V_d,
    phi(e_d)=(1+e_(d/2)) V_d

hold for binary d>=2; d=1 follows by telescoping. Algebra automorphism
conjugacy and invertible unit multiplication preserve operator rank.
No assumption about full rank of homogeneous inclusion matrices enters.

One sentence should read **every element with zero constant term has
square zero**, rather than "every nonconstant w has square zero".
For example `(1+x_1)^2=1`. All elements to which the argument actually
applies have zero constant term, so this is a wording correction and
does not affect the proof.

## Address orbit and correction scope

The extension to arbitrary disjoint physical swaps is correct. Each orbit
is a regular algebra on its a nontrivial swaps, with all other x_i zero.
For a<d the error vanishes. Otherwise its relative rank is bounded by
`2 exp(-d^2/(2a))`, at most the m-based bound. A direct sum of these
orbit maps preserves the common relative bound, including all fixed
address pairs.

The displayed two-term projection identity gives an explicit algebraic
factorization through low-degree inputs and high-degree outputs. Its
factors still require the multiplication maps and basis conversions.
It does not establish their physical cost. The warning that address-space
rank differs from exceptional batch rows is essential and correct.

## Independent finite replay

The original verifier was replayed with its output directory redirected
under `routes/C/char2-review-replay/`. The final report is retained there.
The checker tests exact field algebra and rank, not a tape implementation.
Replay passed: 284 elementary products, 510 triangular basis images,
21 automorphism identities, 21 unit identities, 37 exact rank equalities,
175 general degree-cut cases, and both negative-control families (16
omitted-prefix failures and 31 predictor-rank failures).

With the stated wording correction, the component proof is approved.
No inference to the original odd-characteristic routing, cheap correction,
or a new complete overhead bound is made by this review.
