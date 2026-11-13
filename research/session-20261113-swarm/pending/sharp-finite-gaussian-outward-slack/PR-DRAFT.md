# Draft PR title

Prove the sharp finite R5 Gaussian outward-slack threshold

## Draft description

This package establishes the exact finite optimum
\(\sqrt{21}-\sqrt{19}\) for injective integer-output maps on the complete
radius-five ball \(S_5\), with Euclidean error at most one for the Sylvester
Hadamard transform \(H_4/2\). The compact certificate contains a full
3,121-input injection and a 1,692-input set whose complete strict-threshold
neighborhood has only 1,691 outputs. The independent standard-library checker
recomputes both sides of the optimum using exact integer and radical
comparisons.

The identity \(H_4=L(2C_+)R\), where \(L\) and \(R\) are signed
permutations, transfers the result to the actual #6509 ideal Gaussian pair.
This gives a necessary global lower bound at error cap one. #6509's inherited
global construction and the triangle inequality provide an upper bound of
one, so the unrestricted global infimum is currently only bracketed by
\([\sqrt{21}-\sqrt{19},1]\). No global construction at the lower endpoint is
claimed.

Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`. Exact hashes for
the candidate input and predecessor proofs are in `SOURCES.json`. Reproduce
with `python3 -B verify.py`; the same checker passes with `python3 -O -B
verify.py`. The default replay is read-only.

Credit @CubeJerry for the candidate workstream input; this package and the
candidate work were prepared with substantial OpenAI assistance. Credit Nick
Petalas (#6619, including its cited #2589 finite-sphere predecessor) and Ali
Romman (#6509) for the predecessor results. No new `kappa`, selected-frontier
change, or global sufficiency theorem is asserted.
