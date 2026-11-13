# Complex-pair exact-sum phase-covariant map

This package records a bounded mathematical supplement to the #6509
conservative Gaussian-rounding branch. It uses the ideal
\(C_+(u,v)=((s+id)/2,(s-id)/2)\), preserves \(s=u+v\) exactly, commutes
with global multiplication by i and wire swap, and has inverse given in
PROOF.md.

The map has error at most one and bilateral pair-radial supremum exactly
\(1/\sqrt2\). The upper bound comes from the two-coordinate score pairing;
the lower bound holds for every exact-sum, error-one map by the fixed-sum
family in PROOF.md. This result is a candidate supplement to the existing
rounding branch, not a separate micro-PR. It makes no physical cost or
multiplication-bound claim.

The exact checker tests inverse, phase covariance, conjugation-as-inverse,
wire swap, and the failure of a fourth-power identity. In particular,
conjugation-as-inverse holds while naive forward conjugation equivariance
fails, and the exact F^4 counterexample is saved in RESULT.json.

~~~~sh
python3 -I -B check.py > /tmp/complex-map-result.json
cmp /tmp/complex-map-result.json RESULT.json
python3 -I -O -B check.py
~~~~

The exhaustive challenge covers 625 pairs with four real coordinates in
\([-2,2]\) and 20 large exact examples through scale \(2^{512}\). All
general claims are proved algebraically; these checks corroborate the
branch, inverse, symmetries, exact error/slack tests, and negative controls.
