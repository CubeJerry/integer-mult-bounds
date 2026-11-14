# Arbitrary one-width canonical quotient gate

The proposed theorem closes the previously explicit scalar/operator gap in
the one-extra-direction obstruction. It concerns the canonical quotient of
the full fitting/history, not packet count or arbitrary fitting rank.

For every characteristic-two field and every block width `V`, if
`dim((row(A)+C tensor k^V)/(C tensor k^V)) <= V`, then `sum ell_i(A) >= 205`.
The retained complete all-route target cap is 194. If the quotient dimension
is strictly below `V`, no canonical contact block can vanish and `ell=222`.

The proof's new argument is basis-free: an erased contact block makes the
row's quotient map injective. At quotient dimension `V`, all deletion rows
map onto the same quotient, so the existing gluing lemma extends entrywise
to unrestricted matrix coefficients. The existing root-support envelope
then still permits at most seventeen savings. The proof does not assume
that the extra quotient is a scalar tensor line, or that blocks commute.

`PROOF.md` states the universal argument. `SOURCES.json` pins the inherited
finite source geometry and physical target-cap dependency. `verify.py`
rebuilds all 111 single and 6,105 pair restriction ranks, reproduces the
569-case support envelope, and checks sharp lifts plus genuinely entangled,
noncommuting and singular operator examples. It reuses authenticated
independent exceptional-geometry evidence; it does not claim a fresh full
geometry replay or universal proof from finite tests.

```bash
python3 -I -B research/moonshot-005-program/results/bit-operator-canonical-quotient/author/verify.py \
  --programme research/moonshot-005-program \
  --native research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz \
  --output /tmp/operator-canonical-quotient
```

Expected status: `PASS_OPERATOR_CANONICAL_QUOTIENT_CONTROLS`. The same run
under `python3 -I -B -O` gives identical JSON. Independent proof review is
pending. No source, strict supplier, foundational discharge or complete
kappa is established. The primary next question is a useful physical
history whose canonical quotient exceeds one whole width, with every
acquisition and route paid.

Credit @CubeJerry, the pinned gluing/geometric/all-route predecessors and
native source contributors; substantial OpenAI assistance. Apache-2.0.
