# Leech norm-six decoder: a mod-five obstruction and one-row escape

**No new kappa.** This is a completed, scoped algebraic result in the complex-
supplier track, seed **31**. It changes no selected supplier or predecessor file.

## Result

DominikScholz's [PR598](https://github.com/CrocSwap/integer-mult-bounds/pull/598)
supplies norm-six directional encoders with cheaper support rank, while
explicitly leaving their dyadic decoder unbuilt. For the **first 2,600
directions of that published generator**, this package proves that there is
**no dyadic linear decoder for its full specified cubic kernel**. A concrete vector
annihilates every source coefficient row modulo five but evaluates to three
on the required target column `y=(4,4,0,...,0)`.

The coefficient matrix has F5 rank **2599**. Swapping generator direction
**2599 for 2600** makes the rank **2600**, with the same number of encoders.
Exact support minors show that the removed and added encoders both have rank
24 under the inherited support upper bound. Thus this one-prime repair adds
no copying allowance. It **does not** establish a dyadic inverse: other odd
primes remain an unresolved issue.

This is not a contradiction of PR598, which did not claim a dyadic decoder.
It replaces one open arithmetic obligation by a precise obstruction for the
frozen prefix and a concrete next candidate. It does not exclude other norm-
six bases, other kernels or masked-only decoding.

## Reproduce

From the repository root, using Python **3.10+**, standard library only:

```sh
python3 -I -O -B research/leech-norm6-dyadic-obstruction/verify.py
```

Expected:

```text
PASS_LEECH_NORM6_DYADIC encoders=2600 prime=5 target_residue=3 ranks=2599->2600 controls=9 no_new_kappa
```

Verification is read-only and also works with this directory alone, without
Git, NumPy, network access or source archives. `--json` prints the complete
machine-readable result. The source-pair fixture is compressed data, not
executable code; its uncompressed payload and regenerated coordinates are
checked. Its bytes reconstruct the exact directions, not a random resample.

Additional checks:

```sh
python3 -I -O -B research/leech-norm6-dyadic-obstruction/test_verify.py
# Optional provenance replay only; NumPy 2.3.5 was used for this check:
python3 -I -B research/leech-norm6-dyadic-obstruction/reproduce_directions.py
```

The optional command independently reruns the predecessor's generator recipe
and requires equality of all **2,601** bundled source-pair records. NumPy is
not used by the mathematical verifier or its tests.

## Evidence and what was actually checked

`PROOF.md` gives the characteristic-zero polynomial-injectivity argument,
the dyadic-to-F5 reduction, the rank argument and the exact Boolean arithmetic
used by the rank checker. The finite premises are checked in ordinary integer
arithmetic, with no floating-point rank or tolerance in the shipped verifier.

The main replay checks all 2,600 annihilation equations, the separating target,
all **6,762,600** homogeneous coefficient identities for the 2,601 directions,
256 direct polynomial evaluations, full rank after the exchange, two rank-24
support minors, all 759 Golay octads and all 2,024 triple-cover premises. Its
random-access geometry reproduces the predecessor's SHA256 for the complete
98,280-line ordering. This is not an all-pairs lattice audit.

The nine in-replay controls distinguish a changed/zero annihilator, changed
coefficient, wrong target residue, wrong source sign, invalid/Boolean indices,
the larger coefficient field, and the false extension to all norm-six
encoders. Eight test groups add exact scalar truth tables, 4,097 mixed columns,
625 exhaustive two-by-two and 200 seeded rectangular rank comparisons,
malformed-input rejection, and a relocated Git-free read-only optimized run.
Missing and malformed on-disk inputs must produce failure.

An auxiliary **conditional** budget check reuses PR598's optimistic fixed
controller with copying mass 62,400, and rigorously rejects a 5% improvement
over the pinned selected result for its 50 stage counts. This is why the
experiment did not expand into a large, unpriced physical-circuit search.
It is not a newly constructed supplier or a universal lattice ceiling.

Local execution details and exact source pins are recorded in `TASK.json`
and `SOURCES.json`. Repository-wide `make verify`, selected cold
replay, hosted CI, Lean and independent human review are **not claimed**.
The optional generic research-package format was not used: this standalone
package has no runtime dependency on changing task catalogues or Git history.

## Pins, novelty and limits

Research base: `afc158a25ef3e0bd80de81d1eb5339f0dace118e`.
Predecessor PR598 head: `615ca6f06fdea0c50dbef733370c47349e25c555`.
Exact source-file Git blob IDs, the final publication base and the source
line-order digest are in `SOURCES.json`. Historical references are not imported
or silently treated as runtime dependencies.

The source generator uses seed **6242600**, not the task-assignment seed 31.
The latter diversifies prime-test order and independent controls. Discovery
checked the fixed 2,600-row matrix at primes 13, 7, 17, 31, 29, 11, 19 and 5,
stopping after a separating F5 witness. It then tested a single exchange.
No exhaustive search for a dyadic basis or decoder was performed.

PR2222 concerns a different, 48-dimensional norm-six lattice and is credited
as adjacent work, not reused as a proof dependency. PR1320, PR2338, PR2724 and
PR2784 concern different E8 masked-decoder restrictions. Targeted live PR
searches found no matching Leech arithmetic-obstruction package in their
coverage. Discussion access was unavailable; the local scope claim and that
coverage limitation are retained in `TASK.json`, not represented as a complete
novelty search.

The impossibility theorem fixes the full cubic kernel and prepared source
functions. Allowing different entries on unconstrained pairs, changing the
encoders, adding original-source access, or admitting odd-denominator
coefficients can escape it. The one-row exchange passes **one prime only**.
A paid side program, complete recursive profile, frame and helper schedule,
hosting, precision/tape and outer assembly are not supplied. No full integer-
multiplication theorem is verified and the selected kappa is unchanged.

## Open next questions

**Can the exchanged basis, or a small redundant extension, be decoded over
`Z[1/2]`?** This would turn the one-prime escape into an admissible algebraic
component. First compute an exact saturated row-module/index certificate, or
construct an explicit dyadic dual; checking more primes alone is not enough.
The blocker is odd-prime index information, not rational nonsingularity.

**Can a changed physical interface beat the fixed controller's budget?** The
present 50-stage-count screen fails the 5% expansion gate even optimistically.
A useful first step is a fully charged alternative path/copy profile before
building a large schedule. The missing decoder, helper preparation, dirty
restoration and complete native/outer obligations remain blockers.

## Credit

Prepared for **@CubeJerry** with substantial **OpenAI ChatGPT (GPT-6 Astra Pro)
assistance** in derivation, implementation, execution, self-review and writing.
The arithmetic implementations are separate methods within this same
AI-assisted contribution, not independent human reviews.

Credit **DominikScholz / PR598** for the norm-six direction recipe, the cheap
support question, Leech geometry, integer-valued factorization and optimistic
cost model. Preserve its Bannai--Sloane, Golay/SageMath and lattice-source
attribution; see `NOTICE.md`. Credit Cinna Davis / PR2222 for the distinct
48-dimensional direction that was inspected for overlap. Apache-2.0.
