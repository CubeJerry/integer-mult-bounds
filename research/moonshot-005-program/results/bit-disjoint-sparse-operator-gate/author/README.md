# Native minimum distance excludes sparse disjoint operator components

The source's forbidden canonical restriction codes have minimum distance
at least18. This gives an all-field obstruction for operator quotients
with at most V+1 generators and pairwise disjoint scalar component supports,
each of size at most8. At width V>=3 every canonical block remains present.
At width2, only receivers in the selected supports can save, each by at most
one unit. Six supports of size at most4 therefore have ell>=198, excluding
the target194. The native halfclass pairing is one application.

PROOF.md contains the universal argument. check.py reconstructs the source,
enumerates all111 fixed restriction codes, and tests exact matrix and native
controls. It uses only Python's standard library. SOURCES.json pins inherited
dependencies; RESULT.json is finite evidence rather than the universal proof.

```sh
python PACKAGE/author/check.py --native NATIVE --output /tmp/disjoint-gate.json
python -O PACKAGE/author/check.py --native NATIVE --output /tmp/disjoint-gate-O.json
```

Replace PACKAGE by this package directory and NATIVE by the pinned native
BIT-NATIVE-WORD.json.gz. Expected status is PASS_DISJOINT_SPARSE_OPERATOR_GATE,
distance census18:7,19:24,20:52,21:16,22:11,23:1, and9216 exact GF4 matrix
controls. The two receipts must agree. The check also includes two disjoint
nine-point supports with the same nonzero residual, a width-two native
one-saving fitting, and a width-three overlapping-support counterexample.

Overlapping or densely mixed scalar directions remain open. No physical
history, complete supplier or new kappa is established. Prepared for
@CubeJerry with OpenAI assistance and predecessor credit in the proof.
