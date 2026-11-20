# Exact partial tap isolation, with residual failures retained

The checker implements a causal local patch after the seven D1 deletions. It removes eleven uses of retained export 48 and six other source-export coefficients of input 332. The exact complete target column of input 332 is restored; all other endpoint columns remain those of frozen D1.

All 272 source-only outside control memberships then pass, including the previously failing terminal 155100. The full source-control rank remains 909. However, 102 other pinned memberships still fail, their quotient rank remains five, and the total response rank remains 1288. No full repair, supplier or new kappa is claimed.

Run `python author/check.py`. The exact rational replay writes `author/output/PATCH.json` and `author/output/RESULT.json`. `PROOF.md` gives the control-space argument and explains why the successful partial condition does not remove the main obstruction. This package is separate from the frozen baseline gate certificates.
