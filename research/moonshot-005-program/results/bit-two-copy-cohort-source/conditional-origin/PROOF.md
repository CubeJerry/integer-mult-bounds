# A concrete conditional two-lane source attaining W19 at width two

**Conditionally verified execution; retained compiler admission open.
No new κ.** This package makes the block-capacity construction concrete:
its actual80-dimensional cache-read space meets W30 in dimension19.
The conditional word is checked on all444 independent original columns,
restores all111 original X records, and completes both coordinates of Y0.
Every whole-record MOVE is unchanged. It explicitly uses778 invocations
of a new local selected-lane XOR service; none is declared free or silently
replaced by an admitted full-record ADD.

## 1. Exact new local service

For a positive integer s, each record has two consecutive banks of length s,
so its total width is V=2s. At one actual chart C define

    ADD_LANE(A,a,B,b): B_b <- B_b + A_a,

where a,b are0 or1. All other banks remain unchanged. Distinct banks of the
same record may be used; adding a bank to itself is forbidden. Inputs and
outputs are characteristic-two field vectors. The service must preserve
record ownership, chart locations and the source bank, and must expose any
extra temporary records, communication or address service it needs.

For the emitted V=2 circuit, each bank is one scalar coordinate. For V=2s,
tensor that same finite circuit with I_s. Its bit XOR work is linear in s,
but a uniform compatible implementation of selected-bank access and any
required control/spectator is a separate physical obligation. The required
interface is listed in the word itself, with
`retained_compiler_admitted=false`.

This service is genuinely additional to a grammar consisting only of
full-record scalar ADD/SCALE and coordinate permutations within a record.
If every input record is constant across its coordinates, those operations
and zero INIT preserve that property in every record. The present circuit
violates it: at actual operation309 at chart A15, the selected-lane update
`X58[1] -> X52[1]` makes the two banks of X52 different under repeated inputs.
The receipt gives their exact original-input coefficient rows. Consequently
that narrower grammar cannot implement the conditional circuit for all
inputs. The construction does not use lower-bound permission for arbitrary
blocks as an upper-bound compiler proof.

## 2. Cohort-local block forms and restoration

Use the same pinned22 source cohorts,40 runs,80 colored caches and h9 W code
as the scalar reprogramming package. For the class-zero code W0 of dimension7,
let H=span(24,32,64) in the pinned coefficient dual. On input bank0 take the
four-dimensional code H^perp; on input bank1 take all of W0. Their direct sum
has dimension11. In each two-run cohort its projection has dimension4,
exactly the capacity of two two-lane whole records. Other cohort capacities
are respected. Class-one carrier spans are the old spaces tensored with two
banks, contributing dimension8 of W1.

At a cohort S, choose2r_S independent forms spanning a space that contains
the required projection. Assign two output forms to each of the existing
r_S run-carrier records. Complete these forms to an invertible binary matrix
on all2|S| original coordinates, with |S|<=8. The generator supplies the
matrix and an explicit Gaussian-elimination CNOT list. A row swap is expanded
as three selected-lane XORs; no coordinate swap is free.

Apply the reverse elimination list at the cohort's common starting chart.
Send the same r_S physical original records along its existing upward runs
and the remaining originals directly to Hub. Once all originals of that
cohort are at Hub, apply the forward elimination list. It exactly restores
all original coordinates. The source transformation and restoration together
use570 ADD_LANE invocations. No extra moving record or stationary linear
record is assumed by the abstract service semantics.

This is genuine inter-coordinate packing. A constrained cohort needs one
independent projected form from bank0 and three from bank1, distributed over
two two-lane physical carriers. It is not two coordinatewise scalar sources
each using the original two carriers independently. The exact capacity theorem
in the scalar package proves that19 is optimal at V=2 within this fixed
cohort/run-capacity class.

Every actual source deposit is still a full-record ADD into a colored cache
at a chart visited by its carrier. The80-by40 binary read-incidence matrix
has rank40; after the two-bank lift it has rank80. The actual cache fields
therefore span the chosen80 independent run coordinates. Literal elimination
gives `dim D=80` and `dim(D intersection W30)=19`.

## 3. Actual packet source and endpoint identities

Only11 additional W-coordinate directions are required modulo D. The
constructor greedily selects11 genuine W rows and places them in the first11
coordinate slots of P1,...,P6. The remaining bank of P6 and both banks of P7
are explicitly zero at handoff. No missing coordinate is counted as a free
information field. Actual Hub seeds subtract each packet's raw query sum.

The P0 delayed feedback is the two-bank form of the previously proved vector
identity. Its seed is the actual e0 vector plus the class-zero raw query and
all earlier raw reads. At A15 it has e0 plus the class-zero query. Y0 preloads
its genuine class-zero suffix, exchanges with P0, then acquires its actual
remaining class-zero prefix during ascent. Both unknown original y0 banks
are kept throughout. Y0 finishes as y0+x0, and the actual ground y0-mask
cancellation gives P0's class-one suffix.

Every raw cache coordinate is a difference of consecutive actual packet
histories. All11 W complement coordinates are actual terminal values.
The checker provides witnesses for all222 displayed W rows, whose span has
dimension30. Literal history has rank93, y-projection rank2 and pure-X
history dimension91. Terminal rank is13 and its W intersection is11. These
are source/history facts, not a complete decoder: only Y0 is delivered.
All other Y values remain unchanged, and every original X restores at Hub.

The V=2 proof consists of exact binary identities on444 independent original
columns. Tensoring with I_s proves the same conditional execution for every
even width V=2s over any characteristic-two field. The abstract capacity
theorem covers odd widths separately; this package does not silently assert
an odd-width physical compiler.

## 4. Full conditional operation invoice

The closed word has200 zero-born owners,674 full-record ADDs,778 ADD_LANEs,
495 whole-record MOVEs and200 explicit CLEARs. Of those retirements199 are
dirty; P7 is actually zero. The new lane calls comprise570 source-transform
calls and208 Hub-seed calls. All source formation, source restoration and
seed selection are charged.

At V=2s the exact value-XOR count is

    674(2s)+778s = 2126s = 1063V.

This counts value XORs only. The new selected-bank control/access service
must add its own proved ordinary time, temporary ownership and any movement.
Equivalently the local invoice retains

    674 C_ADD(2s) + 778 C_LANE(s),

with C_LANE an explicit unproved service price, rather than assigning it
zero or absorbing it into an existing scalar operation without a bridge.

The actual whole-record movement profile is

    183[1]+12[2]+119[3]+71[4]+110[7],

with rank-length1618, identical to the reviewed delayed source at the same
record width. Its previously established movement-only comparison remains
available. That equality does not price the new local service, establish
all ordinary/ownership/recursive costs, or supply the other110 receivers.
All five foundational assumptions and the separate complex-supplier
requirement remain. Neither a complete conditional nor unconditional κ
improves.

## 5. Reproduction and verification classification

```sh
python3 -B build.py --repo /path/to/programme \
  --base /path/to/delayed-correction-source/output/WORD.json \
  --out /path/to/conditional-packed/output
python3 -B check.py --repo /path/to/programme \
  --word /path/to/conditional-packed/output/CLOSED-WORD.json \
  --out /path/to/conditional-packed/verification
```

Expected status: `PASS_CONDITIONAL_LANE_SEMANTICS_ONLY`.
The author verifier checks every actual rational chart, co-location,
whole-record direction, all444 original columns, original restoration,
owned handoff, W witnesses, cache differences and retirement. Mutants omitting
lane formation, lane restoration or feedback reject. A separate admission
control rejects claiming the word belongs to the retained scalar grammar;
its constant-record counterexample is explicit. These are author checks,
with independent review pending.

The live word is an exact prefix of the closed word. MANIFEST.json pins all
source/proof/generator/checker/word/evidence files. The standalone exact
capacity theorem and the fully admitted-grammar scalar805-ADD source remain
separate contributions. Credit @CubeJerry and source predecessors, with
OpenAI assistance. This conditional package makes the next compiler service
concrete and reviewable; it does not claim the service has been established.
