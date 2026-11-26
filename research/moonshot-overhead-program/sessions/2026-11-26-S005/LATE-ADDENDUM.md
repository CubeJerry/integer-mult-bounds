# S005 late result: factor-lift carry transport

This supplements the frozen, independently reviewed [main report](FINAL-REPORT.md).
**No new unconditional multiplication bound is obtained.** The result is an
exact interface identity and an affordable construction at precision four.

## Accepted result FL

Let Q=2^t and let g be monic with squarefree reduction modulo two.
For g_new=g+Qh, choose delta=-h/g' in (Z/Q)[X]/g. The change
X -> X+Qdelta is a full-module isomorphism between the two quotients
modulo Q^2. If E_t is their common low-precision remainder map and
r is its canonical degree-below-deg(g) polynomial representative, then

    K_new(F)=K_old(F)+delta[E_t(F')-r'] mod Q.

Here K denotes the new high t remainder bits. The derivative r' is
the derivative of the specified polynomial, not a quotient-ring derivation.
The correction requires one extra low-precision CRT when r is already
available, as in both UC precision-lifting callers; otherwise it requires
another call to obtain r. Unit inversion, delta preparation and local
arithmetic are explicitly charged.

For q=2^b and the literal irreducible factors g_i of the binary
X^q-X, set alpha_i=X mod g_i and

    s_i=(alpha_i^q-alpha_i)/2 mod 2,
    h_i=s_i g_i' mod (2,g_i),
    g_i^H=g_i+2h_i mod 4.

The product of these monic lifts is exactly X^q-X modulo four. Their
construction uses b local squarings per factor and costs
q b polylog(b)+poly(b) time with an O(q)-bit directory and reused
local scratch. It does not construct the degree-q product polynomial.
At the integer caller, qH=Theta(n) and H=Theta(b), so this one-time
setup fits below the prospective n sqrt(b) budget after a fixed cutoff.

## What this changes, and what remains open

The first carry gate can now be studied in either the literal-factor
format or the exact modulo-four Hensel-factor format. Transport at that
bottom layer adds O(qH[B(b)+polylog(b)]) across the complete precision
tree, including the local arithmetic. The binary-call portion is absorbed
into the existing binary-CRT term. The stricter pointwise D(b,1)=O(1)
contract need not survive: D(b,1)=O(B(b)+polylog(b)) is sufficient for
the summed endpoint implication when B(b)=O(sqrt(b)).

This does not erase carry or construct a fast supplier. It does not
select a coherent factor family at every precision, and the higher
K_t for UC's fixed literal factors remain open. Applying the extra CRT
at every precision changes two recursive calls to three, with normalized
child volume 3/2. That recurrence is outside UC's accepted bound.

The next discriminating task is a binary CRT or first-carry procedure
whose actual tape invoice improves in the Hensel-factor format. A
successful procedure can then be transported using this explicit cost.
Higher-precision suppliers and the common absolute space cap must still
be supplied before any complete complexity improvement is claimed.

## Evidence and provenance

- [Complete FL proof](route-a/factor-lift-carry-transport.md), SHA-256
  `65a69a9a2ed9879ea980bb80cf4d1b796dd855c6b54f9d7f821d90cda295c893`.
- [Independent written review](route-b/REVIEW-FACTOR-LIFT-TRANSPORT.md), SHA-256
  `877e929c3191f8e0fec96b1154679c36d0652a071e191fb42f7757245b2ee9d6`.
- [Independent exact receipt](route-b/factor-lift-independent-verification.json):
  6,272 general transport inputs, nine small factor checks and three
  complete modulo-four products; adverse controls detect the wrong sign
  and omission of the representative derivative.

The lead derived the initial perturbation and modulo-four construction;
Route A independently checked and wrote the proof and tape invoices;
Route B derived the identity independently and supplied the review and
finite controls. The lead read both complete documents before admission.
These are written arguments and small exact checks, not kernel or human
verification. Standard Hensel lifting and the existing UC/FS arithmetic
retain their provenance. Substantial ChatGPT assistance; no priority claim.
