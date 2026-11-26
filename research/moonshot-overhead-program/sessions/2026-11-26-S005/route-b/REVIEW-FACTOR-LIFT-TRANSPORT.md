# Independent review: factor-lift carry transport

Decision: **accept FL1--FL8 and the stated first-layer conditional cost
transfer**. No fast CRT, fast carry supplier, or unconditional rate
improvement is obtained.

Reviewed source: `../route-a/factor-lift-carry-transport.md`, SHA-256:

    65a69a9a2ed9879ea980bb80cf4d1b796dd855c6b54f9d7f821d90cda295c893

## Independently checked algebra

For Q=2^t, squarefree binary reduction makes g_dot invertible modulo
(Q,g). With delta=-h/g_dot, beta=alpha+Qdelta is a root of g+Qh modulo
Q^2. The new-to-old coefficient matrix is I+QB, inverted by I-QB.
This acts on every coefficient word of the entire rank-d module.

Taylor expansion of F(beta)=r_new(beta) gives

    r_new=r_old+Qdelta(E_t(F_dot)-r_dot) mod Q^2,

where r is the canonical degree-below-d low remainder. Its derivative
is a polynomial representative derivative, not an abstract quotient
derivation. Reducing the correction modulo (Q,g) and using the common
low digits proves FL3 with the stated sign, for all inputs. Rearrangement
transports either carry map into the other.

For d dividing b, alpha^q-alpha has even canonical coefficients modulo
four. The derivative of X^q-X is -1 modulo two, so beta=alpha+2s is a
root. With h=s g_dot, beta also satisfies g+2h. The quotient isomorphism
therefore proves divisibility by the new factor. Comaximality and total
degree q prove the complete product equals X^q-X modulo four.

At b=2, X+1 becomes X+3 modulo four while X and X^2+X+1 remain unchanged.
For F=X in the linear factor, carry one becomes zero. For F=X^2 in
the unchanged quadratic factor, remainder -X-1 still has high digits
(1,1). The Hensel factor format does not erase carry.

## Costs and recurrence scope

The invoice is consistent with UC's reviewed small-polynomial arithmetic.
With r supplied, only one extra low CRT computes E_t(F_dot); both UC5
callers have r. A standalone high-digits-only oracle additionally needs
the CRT producing r unless its interface supplies it. Input derivative
indices can be reduced modulo 2^t during a scan. Local products and
reduction retain their stated arithmetic and reused-scratch charges.

FL5 charges unit inversion and lifting; it does not generate h. The
modulo-four construction directly supplies delta. Its b squarings per
factor total q b polylog(b) time, with O(q) directory bits and reused
polynomial scratch. At H=Theta(b), this one-time root setup is
n polylog(b), eventually below n sqrt(b). It is shared across leaves.

The H/2 bottom carry nodes add O(qH(B(b)+polylog(b))), including FL4's
local arithmetic. Thus D(b,1)=O(B(b)+polylog(b)); the stricter pointwise
D(b,1)=O(1) need not survive. Both terms are at most O(qH sqrt(b))
when B(b)=O(sqrt(b)), so the summed endpoint implication survives.
Using the extra CRT at every
precision changes two recursive children to three, with normalized
child volume 3/2. No all-precision consequence is admitted.

The final coherence paragraph correctly permits replacing the bottom
K_1 of UC's fixed-family recurrence while leaving its higher K_t gates
open. Changing an entire factor family would require coherent higher
lifts and their separately supplied carry procedures.

## Independent finite controls

`verify_factor_lift_independent.py` uses literal integer polynomial
division, with modular reduction afterward, without importing the
proposed transport routine. Its receipt records:

- 6,272 general transport inputs at t=1,2;
- nine individual modulo-four root factors for b=1,2,3;
- three complete factor products;
- 2,816 failures for the wrong correction sign;
- 2,712 failures when the representative derivative is omitted.

See `factor-lift-independent-verification.json`. These finite checks
support the algebra, not a fast CRT or all-precision setup supplier.

Route B agent review, with substantial ChatGPT assistance. No claim
of mathematical priority, kernel verification, or human review.
