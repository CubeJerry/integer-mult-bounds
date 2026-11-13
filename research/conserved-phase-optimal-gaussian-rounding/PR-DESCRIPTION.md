## Summary

This package proves an explicit bijection on Gaussian integer pairs relative
to Ali Romman's #6509 ideal operator
`C_+(u,v)=((s+i*d)/2,(s-i*d)/2)`. It preserves `s=u+v` exactly, commutes
with global multiplication by `i` and wire swap, has combined Euclidean
error at most one, and has an inverse related by complex conjugation. Its
bilateral pair-radial supremum is exactly `1/sqrt(2)`.

The upper bound is proved for the constructed map. A fixed-sum sequence proves
that every exact-sum integer-output map with error at most one has bilateral
radial supremum at least `1/sqrt(2)`, without requiring bijectivity. Thus the
constant is optimal under exact-sum conservation. Conjugation-as-inverse
pairs every radial jump with its negative, so the forward outward supremum
is also `1/sqrt(2)`, optimal among exact-sum error-one bijections satisfying
that inverse identity. The root audit proves this corollary; no forward-only
lower bound is claimed without the inverse identity.

## Construction and proof

For `s=u+v` and `d=u-v`, if the two real-coordinate parities of `s` agree,
the output difference is `Jd`. In the mixed-parity case, set
`p=Re(s) mod 2`, `t=(H/2)Jd`, and use the phase-swapped two-axis half-grid
involution `M_p`. The output difference is `H M_p(t)`, and the pair is
reconstructed as `((s+d')/2,(s-d')/2)`. The proof establishes integrality,
bijectivity fiberwise at each sum, the inverse, unit-phase covariance, and
error one. The score-pair argument gives strict radial movement below
`1/sqrt(2)` for each changed pair. The fixed-sum lower-bound family makes
the supremum sharp.

## Verification

The original integer checker, its finite receipt and source notice are copied
byte-for-byte under `proof/`. The root's separately written exact `Fraction`
checker and receipt are under `review/root/`. `verify.py` compiles the two
checker source files from their recorded bytes, cross-checks 6,561 integer
cube inputs, 60 deterministic large inputs and 20 large powers of two, and
checks exact phase-mutant and fourth-power counterexamples. Normal and
optimized commands are listed in `VERIFY.json`; every replay is read-only.

## Related work and credit

Credit Ali Romman for #6509's exact-sum Gaussian pair operator and rounding
lineage; credit Nick Petalas for #6619's outward-slack optimization question.
The [global-half construction](https://github.com/CubeJerry/integer-mult-bounds/commit/26226aa52337e6e94bc0cdf3cf6b89d16bb42f5f) is related work with a different
contract and `1/2` bilateral slack. Exact commit, path, Git blob and SHA-256
pins are recorded in `SOURCES.json` and `proof/SOURCES.json`.

CubeJerry's universal #6778 row/column obstruction also applies to this map: global
unit covariance follows from global `i` covariance, and the map is exact on
every integral image of the `n=1` ideal operator `C_+`. Thus this same
stateless map cannot commute across row and column applications. This does
not rule out an ordered caller, different maps, or an enlarged state or
representation. Its exact source pin and the `n=1` witness are recorded in
`SOURCES.json` and the root arithmetic audit.

The root supplied the candidate pairing formula and wrote the separate
`Fraction` checker. The proof/integer-check role formalized and tested the
same proposed map. This is not blind review, human review or formal
verification. See `ROLE-BOUNDARIES.md` for evidence roles.

## Limits

This is an unbounded-integer arithmetic result. No fixed-width or tape
implementation, selected caller admission, precision recurrence, physical
cost bound, or kappa change is claimed. Same-map row/column commutation is
excluded by #6778 under this map's hypotheses. The map also fails a
fourth-power identity and therefore cannot square to wire swap. All five selected framework
assumptions remain.

## Base and registered reproduction

Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`.

```sh
python3 -B scripts/research_package.py --package research/conserved-phase-optimal-gaussian-rounding --check-only
python3 -B scripts/research_package.py --package research/conserved-phase-optimal-gaussian-rounding
```

Expected markers include `PASS_CONSERVED_PHASE_COVARIANT_CROSS_IMPLEMENTATIONS` and `PASS_REGISTERED_RESEARCH_PACKAGE`. The package contains the complete proof, exact inverse, source pins, six bounded replay commands and original frozen evidence.

**No new kappa.** The selected `363005817/100000000000` remains unchanged. Prepared for **@CubeJerry** with substantial OpenAI ChatGPT/Codex assistance. Apache-2.0.
