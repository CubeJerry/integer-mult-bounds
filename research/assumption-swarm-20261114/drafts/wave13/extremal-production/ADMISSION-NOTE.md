# Bounded independent admission findings for A13

Status: positive source-admission finding; implementation/interface review
awaits the author's frozen adapter. This is not a publication verdict.
Base: `e54523517d0f03e58352e647c403a5af3e525a57`.

## Exact inherited scalar contract

The canonical #6085 proof, blob
`fd7f576039c8867053042d6f616441b41a4a103d`, quantifies isolated
`Exponentials.grid_interval` and `coefficient` calls for every represented
P,F>=1, rational 0<=f<=F, Boolean growth and sigma>=0. The downward
coefficient error is strictly below `2*2^-P`; exact-floor equality is not
claimed. The source retains the encoded Count/Rational operations and
their ownership semantics. The code does not require constructing Axis or
passing ProductionPlan. Its import-time authentication guard must still be
bound to the exact retained runtime in the actual adapter.

The unchanged `gaussian_exponentials.py` invokes the lower-bound checks,
Machin setup, directed Taylor/squaring, reciprocal and final shift itself.
No oracle value should be supplied as implementation input. `sigma=None`
is the literal zero-shift interface. `positive_exponent=False` selects decay.

## Four extremal arguments

Let u=alpha^2 and delta=t-s. A12's legal selected phase has
`beta_i=-(s-1)/(2s)` and `beta_(i+1)=beta_i+delta/s`. Direct source geometry
gives

`(rho+beta_i)^2-beta_(i+1)^2=(2delta+1)/s`,

`(beta_i-1)^2-beta_i^2=(2s-1)/s`.

Thus the required arguments are exactly
`f_plus=u(2delta+1)/s` and `f_minus=u(2s-1)/s`, one pair per axis.
For integer 1<s<t<2s and u>0, both lie strictly between zero and F=2u.
This domain admission is stronger than the fine-prime specialization and
does not depend on the incompatible #6099 guards.

With P=p+8 the coefficient error is `<2^(-p-7)`. At p>=4096 the A12 bound
`w^2>=(16p)^-36` gives
`2^(-p-7)<=2^-37*w^2`: at the cutoff, p+7=4103 exceeds
`37+36 log2(16p)=613`, and the difference increases thereafter. This is
more than enough for the alias-deleted factor error premise.

For an approximation to the actual matched periodic section, aliases must
be added. The existing A12 proof gives
`tail<=4 exp(-a t^2/8)` with t>=32,a>=1. Its same calculation sharpens to
`tail<=2^-37*w^2`, because `a(t^2/8-4)>=124>39 ln2`.
Consequently the emitted scalar approximation can have error below
`2^-36*w^2` relative to the periodic coefficient, with exact diagonal one
having only its own alias error. If the author instead keeps only the
displayed A12 alias cap `2^-36*w^2`, the resulting total should be stated as
`2^-35*w^2`, not silently called `2^-36*w^2`.

## Cost and encoding conditions that survive

The actual setup formulas have X=4F, and
`R=P+4X+4k+2ceil(log2(P+X+k+16))+64`. With F=2alpha^2 and the A12 alpha
choice, R=Theta(p). The inherited scalar tariff is
`O(R^3+(R+B_f)^2)`, where B_f includes the numerator and denominator lengths.
There are four calls and one reusable setup, each explicitly paid.

A12 only imposes a lower bound on s; arbitrarily long source primes are
still admitted. Therefore retain B, the encoded input bit-length scale,
in the joined cost. An `O(p^3)` specialization requires an additional
`B=O(p)` interface, such as the full retained fine-source side-length law.
It does not follow merely from s>=p^4.

Argument construction must use the actual Count arithmetic on copied
borrowed inputs, not host integer or Fraction values injected into protected
execution. Default Rational construction performs a gcd and exact division,
so their bit work must be charged. Explicit `reduce=False` is an existing
exact-rational ABI used elsewhere by the source; if adopted, its positivity
and fraction-value preconditions should be stated rather than pretending
that reduction happened for free.

Exponentials retains references to its P/F inputs and owns its fields.
Those borrowed parameters must outlive all four calls. Rational owns its
numerator and denominator; closing it must not erase the original source
parameter tapes. Returned coefficient Counts remain live until serialized
or explicitly transferred/retired. A scratch pool cannot be asserted empty
while those returned leases remain live. Output grid P and association of
the four fixed-order coefficients with the two selected axes must be explicit.

The pending review will check actual constructor/session binding, scratch
capabilities, input/head preservation, output transport, close paths and
the complete cost. Whole Gaussian production, arbitrary source sections,
inverse computation, full fixed-tape lowering and multiplication remain
outside this local four-coefficient admission result.
