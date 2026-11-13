# R5 Hall orbit preflight

This is a bounded follow-up to the frozen
`sharp-finite-gaussian-outward-slack` package. It checks whether that exact
1,692-input Hall witness can be compressed by signed-permutation symmetry,
squared-norm classes, or coordinate-parity classes. It does not modify or
replace the frozen finite R5 result.

Run with Python 3.10+ and the standard library:

```sh
python3 -B check.py
python3 -O -B check.py
```

The script authenticates and reads the certificate and verifier from the
sibling `sharp-finite-gaussian-outward-slack` directory. It writes no files
unless output is explicitly redirected. `RESULT.json` is the saved exact
receipt; `SOURCES.json` records hashes and predecessor credit.

The result is negative for the tested reduction: the Hall witness has
trivial stabilizer in the full signed-permutation graph automorphism group,
and none of the tested norm or parity templates gives a positive Hall
deficiency. No analytic membership rule for the witness was found.
