# Independent review of the causal full-plane F64 array interface

## Decision

Accept the explicit local theorem for all 881 A2 planes with three real
native donors. The V45 construction preserves all 1080 plane input field
dimensions, gives every visible receiver a 360-dimensional target whose
projection onto each donor quotient is invertible, and realizes the
required shared-port intersections. It uses genuine early and late
holders in separate phases and needs no extra MOVE, INIT or CLEAR at H.

This is a local quotient/port interface. It does not construct the source
quotients consistently at all planes, the subsequent D-to-K-to-F maps,
the global X inverse, the ground Y preload gauge, or a complete supplier.
Those limits in the author proof are necessary and correctly stated.

## Geometry and algebra

The independent checker reads the authenticated root layout and factor.
It recomputes all 45 actual D4 exits at each of the 881 planes and all
29,354 full-plane/native-receiver incidences. Every actual receiver sees
exactly fifteen exits. The factor cases are 709 planes with x=4, 84 with
x=5 and 88 with x=6. The early and late capacities are exactly those of
the physical balanced flags.

F64 arithmetic is independently implemented by carryless polynomial
multiplication followed by long reduction modulo z^6+z+1. No author
field or matrix routine is imported. All nonzero field elements have an
inverse. The coefficient file is compared with a separately constructed
Vandermonde matrix on the 45 distinct nonzero elements 1,...,45.

The full V45 determinant is checked by Gaussian elimination. For every
actual fifteen-port set, a separate Gaussian determinant calculation
checks its first fifteen columns. The other two donor blocks are their
nonzero diagonal scalings by alpha^15 and alpha^30. All 88,062 published
donor-projection determinant values agree, not merely their nonvanishing.
Since the 45 rows of V form a basis, any port set is a direct sum of its
row spaces and intersections are exactly the common rows. This proves
all simultaneous shared-port rank conditions for this local interface.

The exact receiver-pair census is 203,842 pairs sharing three ports and
271,177 pairs sharing six ports. With 24 field symbols per port, the
corresponding target intersections have dimensions 72 and 144. This is
the asserted intermediate intersection behavior; no global source
coordinate compatibility is inferred from it.

## Physical holder assignment and time order

The port index in the stripe formula must be its **local ordinal p from
0 to 44**, in the sorted list of actual D4 exits. The author clarified
this in the final proof. It cannot be the global D4 label modulo three.

For either phase let a be the number of holders from each donor on one
H-D flag: a=x early and a=8−x late. Assign the real holder with donor j,
local exit ordinal p and within-flag index s to

    stripe = s + a*((j+p) mod 3).

The checker explicitly partitions every actual holder in all three x
cases. Every stripe has one existing holder at every D4 exit and exactly
fifteen holders from each donor. Every early or late holder occurs once,
and no holder changes phase. There are 3x early stripes and 3(8−x) late
stripes, totaling 24. The early transform therefore reads only early
X holders; the late transform reads only late Y holders after their
physical source visits. No hidden cross-phase cache or source value is
needed by this full-plane construction.

The physical output holder indexed by p still travels to its original
D4 exit after the local map. Input donor grouping is achieved by actual
ADD swaps of contents at H, not by renaming a record's route or moving
it between charts. All holders in one phase are co-located at H while
this transform is applied. Their eventual destinations and ownership
identities remain attached to the original physical records.

## Literal permutations and ordinary cost

The 31,355-ADD binary word is replayed on all 270 original binary columns
against the independently expanded field matrix. Each operation has
distinct valid operands. Removing one ADD changes the result. Reversing
the ADD word inverts the local map.

In addition, the review materializes the three physical input
permutations, one for each value of floor(stripe/a). Their field-swap
counts are 42, 42 and 40. Each field swap is exactly three ADDs on each
of six binary lanes. The checker replays these literal prefix operations
followed by the author word and verifies the complete expected map from
the actual physical input-holder order to the fixed output-holder order.
It also verifies the full reversed operation sequence.

Across the early and late phases, each of the three permutation types
occurs exactly eight times. Thus the materialized permutations cost

    8*(42+42+40)*3*6 = 17,856 ADD per plane.

The resulting exact local implementation uses

    24*31,355 + 17,856 = 770,376 ADD per full plane,
    678,701,256 ADD for all 881 full planes.

This validates and slightly sharpens the author's conservative bound of
771,528 ADD per plane. Neither count includes source preparation, later
chart operations, whole-program inverses, canonical packets, body work
or recursive accounting. They remain additional obligations. The
six-copy binary realization of each F64 symbol is also explicitly paid.

## Artifacts and accepted boundary

The independent check.py imports no author code. RESULT.json records the
exact proof, author result, coefficient file, ADD word, layout and factor
hashes, the complete verification counts, and the exact ordinary cost.
HOLDER-PERMUTATIONS.json contains the three concrete physical input
orders and every binary ADD in their permutation prefixes.

The accepted positive statement is a causal, information-preserving
array interface on the actual full-plane holders with fully specified
finite coefficients. Its source inputs are independently supplied local
quotient coordinates. Extending those coordinates across all planes at
one donor is a separate system of compatibility equations. Invertibility
of this local map does not assert individual original-label restoration,
and the proof correctly reserves actual Hub and ground inverse work for
the eventual global construction. No new complete kappa is admitted.
