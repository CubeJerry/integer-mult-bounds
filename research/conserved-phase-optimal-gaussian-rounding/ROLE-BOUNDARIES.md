# Root and proof/check role boundaries

## Shared mathematical proposal

The root supplied the phase-dependent two-axis pairing proposal. The proof
role wrote and checked the all-input parity, bijection, error, symmetry,
inverse and radial arguments recorded in `proof/PROOF.md`, alongside the
integer implementation in `proof/check.py`. Both implementations work from
the same proposed formula.

## Separate implementation check

The root wrote `review/root/check_candidate.py` using exact `Fraction`
coordinates and a separately expressed transform. The proof checker uses
doubled half-integer coordinates and integer arithmetic. The root checker
checks the global integer cube and deterministic large inputs; `verify.py`
cross-compares both forward and inverse outputs and pins their executed
source bytes in its receipt.

The root reviewed the written proof and independently checked the candidate
arithmetic. This is not a blind rediscovery, a human review, or a
proof-assistant proof. Both roles had the same proposal and the finite runs
do not establish the all-input theorem.

## Scope boundary

The proved contract is exact complex-sum preservation, global multiplication
by `i` covariance, wire-swap covariance, bijectivity, inverse-by-conjugation,
error at most one, and sharp bilateral pair-radial slack `1/sqrt(2)`.
The same-map row/column commutation identity is impossible under #6778's
global-unit covariance and integral-image exactness hypotheses; the exact
`n=1` witness is checked in `verify.py`. The package does not establish `F^4`,
square-to-swap, selected caller admission, a finite-width implementation, a
physical tariff, or any kappa change. The square-to-swap question remains
pending in a separate workstream.
