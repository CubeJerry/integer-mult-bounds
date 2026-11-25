# Independent review of full-rate field packing

Status: **accepted in the stated interface**. A read B's complete
`route-b/full-rate-field-packing.md` and its checker, checked the physical
digit order and the completed-map algebra, and replayed an isolated copy.
This is an AI-assisted independent component review, not a full multiplier
or formal-kernel verification.

## Scope checked

The power-of-two choice of the F4 extension degree gives a binary coordinate
dimension h=2e that is a power of two. Field construction remains polynomial
in the arity: e<2 ceil(log_4 B) permits a coarse B^O(1) enumeration bound.
The stronger earlier bound 4^e<4B is unnecessary here and is not used.

The packing is bijective on all hW binary rows. It does not embed a single
bit in a mostly zero field symbol. The completed K program has coefficient
matrix I_W tensor Q, so every independent binary coordinate receives Q.
Intermediate coordinate mixing is harmless only because this is the whole
completed identity; extracting one component or one invariant subspace
would not suffice.

The physical order is correct. Exposing the final h factor of the leading
row index gives `(coarse,module,coordinate,physical)`. Moving the coordinate
digits from last to first places them after the physical range while
preserving their original significance. Each elementary move is a two-row
split/interleave over complete ranges and uses O(V) scans with a fixed
number of alternating regions. It does not enumerate or transpose the
exponentially long module address. Reverse moves unpack exactly.

For a recursive spatial call, the parent's field-component bits are an
ordinary suffix spectator of the binary input. A new child's field basis
can mix its own full independent leading rows, and its completed exact
permutation returns those bits unchanged except for the requested physical
field swap. This validates changing fields between spatial levels. It
does not change the field inside one finite scalar-repair program.

The new batch hW changes log W only by O(log log m). Its leading padding
must still be paid at every recursive node, exactly as B's separate packed
recurrence does. Packing adds no multiplicative h payload factor.

## Replay

From the programme root:

    python3 -B research/moonshot-overhead-program/sessions/2026-11-26-S003/route-a/verify_independent_field_packing.py

The isolated copy checks four shapes, 2,898 distinct moved positions, 66
independent binary input arrays, exact inverse packing and a completed
spatial swap. Wrong component order is rejected. The recorded output is
`field-packing-verification.json` in this directory. The checker does not
execute the full scalar template; its role is the physical packing order
and independent-component conjugation.

No remaining objection was found in this local interface. Uniform scalar
repair, shared-pencil memory, varying-arity recursion and numerical
precision remain separately reviewed obligations.
