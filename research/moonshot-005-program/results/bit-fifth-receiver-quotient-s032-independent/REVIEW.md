# Independent review of the literal source-quotient obstruction

**Accepted under the frozen-interface contract below. No new kappa or
complete supplier is established.**

## Scope and necessary local observations

Start from S032's four-receiver source/H/D word. Allow independent arbitrary
linear changes to every full paired source quotient, including mixing all480
source coordinates. Keep actual owner routing, source phase interfaces,
and physical H/D maps fixed. Preserve the literal values on all retained
native H263/H642 whole-fibre interfaces and on D1509 whole fibres for
receivers6,9,48,73.

Common rebasing of retained interfaces, changed H/D maps, extra information,
altered routing, joint coding across source banks and nonlinear quotient
maps are outside this gate. It does not rule out every source redesign.

For a retained H whole fibre, the frozen complete donor/H section is invertible.
Keeping proper output values fixes the source quotient's value on that fibre.
For a retained D fibre, all other proper D packets vanish and the D readout
is fixed. Its invertible eight-by-eight section fixes the eight D input
values; the other proper packets are zero. Invertibility of the H section
then fixes each complete visible source quotient.

Thus every permitted linear quotient change annihilates the span of retained
whole H fibres visible at that quotient and retained D fibres visible there.
The independent checker derives these spans from its own H-fibre matrices and
the verified common four-frame, rather than importing the author's edit solver.
Other source banks cannot cancel one donor's independent input columns.

## Forced collision and conflicting actual readouts

The intersection of source61's receiver95 isolated fibre and the retained
32-dimensional four-frame span has dimension4. Every one of its sixteen
source quotients visible at receiver95 has a local necessary-observation
span containing that entire four-space.

Only native H receivers below111 are used. Removing all geometric-only
receivers leaves the local ranks unchanged:

| H | Local span dimension |
| ---: | ---: |
|263|76|
|269|58|
|284|66|
|333|54|
|343|62|
|375|58|
|384|66|
|394|62|
|468|58|
|481|70|
|642|76|
|660|66|
|783|66|
|808|58|
|906|54|
|947|70|

The independent checker supplies its own explicit decomposition of the witness
v at every quotient. Consequently every permitted edit leaves the complete
receiver95 proper restriction unchanged on v at source61. Its off-D packets
stay zero and its actual D95 readout remains

    [14,8,50,38,1,0,0,0].

At source0 every D1509 parent quotient, H71,H116,H263,H283, is visible to all
four retained receivers. Since v belongs to their common32-space, these D
ingress values are also fixed. Its actual readout remains

    [14,20,31,55,1,62,23,17].

Both outputs were freshly reconstructed through actual source phase frames,
early/late H blocks and cross blocks, named D owners and outgoing K flags.
Their difference is

    [0,28,45,17,0,62,23,17].

On the whole forced four-space the readout discrepancy has rank2.

If source0 still has an off-D observation of v, its isolated fibre cannot equal
source61's. If edited source0 quotients remove those observations, the two
D readouts on the same isolated vector v still disagree. Either outcome
precludes a common exact receiver95 whole fibre and readout.

This excludes receiver95 under the precise retained-interface contract.
It does not exclude every other fifth receiver through this particular
witness.

## Verification and controls

The checker imports no constructor executable. Generic finite-field arithmetic
comes from the prior independent review. Exact source hashes, actual routes,
independent H fibres and the frozen four-receiver source payloads are bound
in SOURCE-PINS.json. The checker regenerates local decomposition certificates.

A control at H333 changes one input coefficient so that the quotient value
on v changes by1. H333 is invisible to all four retained D receivers, but
the edit necessarily changes a native retained H observation. The checker
identifies the precise generator and nonzero change. This explains why
omitting H preservation would invalidate the argument; it does not claim
that this altered source is a complete valid construction.

Run from repository root with Python3 and NumPy:

```sh
python3 -B research/moonshot-005-program/results/bit-fifth-receiver-quotient-s032-independent/check.py
```

Expected status: PASS_INDEPENDENT_RECEIVER95_QUOTIENT_OBSTRUCTION.

The [result](output/RESULT.json) and [native-only decompositions](output/LOCAL-DECOMPOSITIONS.json.gz)
record the exact evidence. Field-extension and repeated-lane versions follow
from the same linear identities and nonzero output difference, under the
corresponding literal-interface contract on those extended banks.

Prepared for @CubeJerry by S032 worker C with substantial OpenAI assistance.
Worker A found the source-quotient witness and gate. This review independently
reconstructs its necessary local observations and physical contradiction.
No independent human review or formal-kernel certification is claimed.


