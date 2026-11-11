# Exact finite-depth BIT requirements for a κ=1/200 assembly

**No new κ.** This package proves the precise covered-BIT price needed to
reach a desired ordinary price through finitely many fully charged wrappers.
The construction of a stronger covered supplier remains open.

Under the source's three-term cost and completed-backend contracts, a stage
starting at ordinary b and covered C has strict supremum
`F_C(b)=C/(1+C-b)`. At h fixed stages,
`(C-F_C^h(b))/(1-F_C^h(b))=C^h(C-b)/(1-b)`. This gives an exact inverse
target/depth test, with equality rejected, and rules out exceeding a frozen
covered price by rearranging acyclic wrappers. These are scoped theorems
about the declared interface, not universal algorithmic lower bounds.

From the selected ordinary b=.00385248, one stage exceeds .005 only if
covered `C>3112961/621875000≈.00500576643216`. A hypothetical C=.0050001
requires two stages; exact witnesses reach ordinary .00500007 and join a
hypothetical uniform complex .00500006 through all current 54+4 outer rows.
No such new covered/native supplier is supplied here. The selected covered
C=.0038525298 and fixed atom rho=.004 each fail the target for distinct
reasons; they are frozen-certificate limits, not universal architecture caps.

[PROOF.md](PROOF.md) contains the full quantifiers, costs, strict supremum,
finite-depth construction, assumptions and open next questions.
[LIFT-GUARD.md](LIFT-GUARD.md) repairs the selected input-lift inequality
through k=.0051; the old sufficient Taylor guard fails there, while a direct
derivative bound proves the gain remains positive. This repairs an enabling
arithmetic check without changing the native word or its accounting.

Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`.
The selected frontier is .00363005817 (#7000/#7001); all five assumptions
remain unchanged. Sources are pinned in [SOURCES.json](SOURCES.json).
The generic outer-region theorem is credited prior work by Nick Petalas.
Finite ordinary replacement is credited to Rohan Arun's #185/#199/#204
lineage and the retained delayed-cover/compiler/native source authors.

## Reproduction

From a checkout containing the pinned canonical sources:

```sh
python3 -I -B research/bit-target-bootstrap/verify.py
python3 -I -O -B research/bit-target-bootstrap/verify.py
```

Expected status: `PASS_TARGET_BIT_BOOTSTRAP`. No scientific files are
written. `--write` regenerates RESULT.json for the author only.
`--source-root PATH` can be repeated for an authenticated sparse export.
The verifier uses Python standard library only and explicit checks under -O.
It authenticates nine source files, checks 1,520 recurrence identities,
18,810 rational atom comparisons, 570 constructed strict witnesses, the
literal current outer arithmetic, seven rejection controls, and a rational
all-interval derivative certificate. Finite grids corroborate the written
universal proof and are not used as evidence for untested native operators.

The finite-depth envelope method is prior work by Isaac Grannis (@BagMan9)
in #768, reused by `t37-bootstrap-depth-seed60`; the new optimized map here
decouples covered C from the atom exponent rho. See [OVERLAP.md](OVERLAP.md).

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
Independent mathematical review is a separate publication gate; this package
does not assert independent human or proof-kernel acceptance.
