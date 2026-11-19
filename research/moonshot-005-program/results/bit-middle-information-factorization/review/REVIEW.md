# Independent review of the saturated middle information bridge

**Verdict: accept Theorems1 and2 in their stated local information model.**
They give exact necessary information tests and a simultaneous linear
assignment theorem. They do not certify a physical source, arbitrary
original-Y restoration, pure-wave invertibility or a complete supplier.

## Mathematical review

The saturated-message argument is valid. A receiver target has exactly
|F|^r values, and its r physical symbols have no larger alphabet. Correct
decoding forces the attained message tuples and target values into a
bijection. In particular every shared message is a function of each
receiver target that uses it. This is stronger than mere recoverability
and is where saturation is essential.

For linear observations, common deterministic functions factor through
the intersection of the observation row spaces. Translation invariance
under the kernel of each observation implies invariance under the sum of
those kernels; the annihilator is precisely the row-space intersection.
This proof covers nonlinear functions and finite fields of any characteristic.
Availability contributes another observation to the same intersection.

Every receiver subtuple is surjective onto its product alphabet. Its
cardinality therefore gives the stated sublist rank inequalities. Conversely,
independent representatives provide one successful assignment for each
receiver separately. The product of those determinant polynomials is
nonzero. Each coefficient variable belongs to one physical slot and appears
in at most that slot's audience size many determinants, once in each.
The individual-degree finite-grid bound therefore gives a simultaneous
assignment when |F| exceeds the maximum slot audience size. This bound
does not grow with the number of receivers or the number of stripe copies.

Equal-Q slots can be grouped without changing Hall tests provided the
group also has a common audience, or its capacity is indexed by receiver.
This refinement was sent to the author. The native `(K,phase)` grouping
has a common audience automatically. It is not valid to give a receiver
the full capacity of equal-Q slots it does not actually see.

For two-wave compression, fixing the early observation leaves
|F|^(r-dim(V intersect E)) possible target values. Late symbols must
distinguish them, proving the second inequality for arbitrary nonlinear
early and late codes. Total target cardinality proves the first inequality.
Choosing max(0,r-l) useful early rows from V intersect E and completing
them to a target basis proves linear sufficiency over the base field.
Unused abstract slots can carry constants only in the information model;
the author's original-owner restoration caveat is necessary.

The two-layer formulation correctly conditions the K test on one chosen
common D assignment. Per-D determinant feasibility alone does not control
the ranks of the resulting K demands or their early availability. Thus it
does not silently claim sufficiency of individual cuts for the full native
network. For fixed i, saturated D demand packets are jointly surjective,
and different D boundary groups are independent by premise; this justifies
the unique induced K contribution maps used by the compression criterion.

## Separate finite verification

The review checker imports no author implementation. It uses F3^2 for
the common-function and independent-representatives controls, rather than
repeating the author's F2^3 census. All six ternary subspaces produce18,432
Boolean common-function checks and36 independent-representatives instances.

A separate nonlinear causal search checks all225 target-space,
early-observation and zero/one/two-bit capacity combinations on F2^2.
It searches the full finite deterministic encoder domain until a witness
is found, or exhausts that domain for a negative case. It examines2,177
encoder pairs and finds171 feasible combinations, exactly matching the
written criterion. This test does not restrict encoders to linear maps.

A four-audience control has every individual representative condition
satisfied over F3, while all19,683 possible ternary shared functions fail
simultaneous decoding. Over GF9=F3[u]/(u^2+1), the shared function x+uy
works with each private observation x,y,x+y,x+2y. Each of the four tuple
ranges contains81 points. This is a different field/audience instance
from the author's three-audience F2/GF4 example.

Reproduction:

    python3 -B check.py --author AUTHOR_PACKAGE --out OUTPUT

Expected marker: `PASS_INDEPENDENT_MIDDLE_INFORMATION_REVIEW`. Reviewed
author hashes and exact results are in the output directory. The native
fanout-three claim also follows directly from the already independently
checked three-root A2 flags; no global source or physical capacity is added.

Reviewed by S027 Worker C with substantial OpenAI assistance. Credit
@CubeJerry, retained source and atlas authors, and Worker B. Classical
independent-representatives and finite-grid arguments are credited in the
author proof. No human or formal-kernel verification, new complete kappa,
or foundational discharge is claimed.
