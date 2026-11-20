# Frozen source gates and a five-form recoding lower bound

This package reconstructs two exact rational obstructions for the frozen D1 deletion while keeping the 909 existing chart-3 exports free. Neither proposed second new route is installed in the baseline.

| Test | Exact result |
|---|---:|
| Full source-control rank | 909 |
| Outside external defect rank | 2 |
| Affected external input columns | 73 |
| Affected columns outside chart 27 | 72 |
| Affected outside terminal rows | 75 |
| Pinned quotient defect rank | 5 |
| Individually failed pinned memberships | 103 of 376 |
| Source-only outside coordinates | 272 |
| Source-only quotient defect rank | 1 |
| Sole failed source-only coordinate | terminal 155100 |

The outside defect is supplied as two basis columns and exact rational coefficients for all 73 columns. The pinned gate reduces to an eight-variable system; explicit kernels, small nonzero rational minors and isolating witnesses are retained. The proof also shows that at least five surrounding scalar forms must change in any successful repair on a common fixed acyclic supergraph. This counts local form edits, not paid routes.

Read `PROOF.md` for the scope and exact algebra. Run `python author/check.py`; it uses the retained authenticated source and SymPy for small exact matrices, and writes `author/output/RESULT.json`. No numerical fit, modular rank inference, endpoint-pair exclusion, positive supplier or new kappa is claimed.
