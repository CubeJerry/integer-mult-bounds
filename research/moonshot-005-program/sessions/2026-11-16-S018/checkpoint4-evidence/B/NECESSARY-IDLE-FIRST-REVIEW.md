# Independent review: the first input must feed the idle bank

**Accepted within the stated universal fixed-template scope.** Reviewed root
proof SHA256 b3b6cc6abcdde814c093f1b300cd977634f30903a173e81be1d8b1d3f6c19a45.
The independent checker is review_necessary_idle_first_column.py, with exact
results in NECESSARY-IDLE-FIRST-REVIEW.json. It imports no root verifier.

The one-sided stripping lemma is valid. Projection selects a finite sum of
literal rank1 words A R A; multiplying by a^-1 turns each selected tensor
word into R^tensor V a, still pure rank1, while a h becomes ordinary h.
Finite faithful tensor separation then forces h=0. Retained projective scalar
phases travel with their terms, so exterior-i and i^V are not conflated.

The previous normal form makes the rank1 image the middle bank and the rank4
image a graph over the top bank with an invertible top block. Their direct
sum is exactly the top two banks. Hence the bottom projection on the rank2
image is injective. Under u=0, f is a unit, the exact bottom column0 gives
q11=0 by stripping, and the active corner unit gives q01,q10 units. Column1
has zero bottom, no rank4, and therefore no rank2; its top is also invisible
to rank1. The exact nonzero top block shat a²q01a is the contradiction.
This argument handles sector idempotents and singular individual Q blocks
without dividing by them. It does not elevate nonzero u to a unit.

The separate exact checker reconstructs A from the literal input phase abd,
verifies A S^-1 A=X_b S and that A² S^-1 A has support2 in every column,
and verifies S^-1 is outside the square monomial class. These are controls,
not a finite proof of the universal stripping or image argument.

The claim remains a sufficiently-large faithful-width gate for a fixed
finite catalogue. It neither excludes isolated width1 factorizations nor
provides a physical endpoint or saving. Actual ordinary lowering, body,
source/owner, precision and recursion obligations remain unchanged.

A complementary strengthening is already written independently in
ALL-CLEAN-FIRST-COLUMN-GATE-v1.md: if a u a^-1 is also ordinary, apply a to
the pure-rank2 bottom row. Its rank4 projection is -uhat X, where X is
surjective because the original rank4 top block is -shat X. Thus u=0,
contradicting this reviewed theorem. That stronger extension still awaits
root's independent review and is not silently folded into this acceptance.
