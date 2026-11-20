# Full45 two-H shared-source pair

Frozen author witness for simultaneous H263/H642 at five complete donors.
Read PROOF.md for the exact theorem and limits. No full global return or new kappa.

The standalone check reads coefficient literals and raw atlas/owner data; it
imports no construction executable. Run from the repository root:

    OPENBLAS_NUM_THREADS=1 python -I -B research/moonshot-005-program/results/bit-shared-h-s031-review/full45-two-h-pair/author/check.py --repo . --out FRESH

Expected: PASS_FULL45_TWO_H_SHARED_SOURCE_PAIR 315 291 72 67 45 44 216 16.

PAIR-TWELVE.json.gz is the newly regenerated complementary source on the current
marked-port allocation. The retained predecessor uses a different allocation;
its original literals must not be substituted. build_pair_literal.py documents
how the new seed0 witness was materialized, with credited retained code.

output/COEFFICIENTS.json.gz contains every full source map and both logical and
owner-bound H words. FIBRES, EARLY and COMPILER contain full readout, basis and
binary-word literals. SOURCE-CUT-DETERMINANTS records exact nonzero determinants.
SOURCE-PINS authenticates inputs. MANIFEST pins this frozen author package.

Status: exact author checks pass; independent reviews are required for admission.
