# Exact multi-source cuts for the paid complex observer repair

**No new κ.** Four exact cuts make six of the eleven remaining high-grade
cycle occurrences mandatory. Combined with S030's circulation theorem,
1,071 of 1,076 high-grade occurrences are forced in the retained route
contract. The best remaining high-grade-only deletion budget misses the
κ = 0.005 caller by more than 6.807280786880 units per native use.

- [Proof and precise scope](PROOF.md)
- [Four small cut/minor certificates](CUTS.json)
- [Exact verifier](author/check.py)
- [Replayed result](author/output/RESULT.json)
- [Source pins](SOURCE-PINS.json)
- [Provenance and limits](PROVENANCE.md)

Low-grade deletions and other changed routes remain open. The κ = 0.0043
optimistic screen retains about 8.013 units but supplies no physical repair.

```sh
python -I -B research/moonshot-005-program/results/complex-paid-export-s031-repair/author/check.py --repo . --out /tmp/s031-complex-rank-cuts
```

Expected final marker before the two price rows:

```text
PASS_S031_SATURATED_COMPLEX_CUTS_AND_HIGH_GRADE_SCREEN 4 6 5
```

Author verification passed. Independent programme admission is pending.
