# Root exact-Fraction review

`check_candidate.py` and `RESULT.json` are the unchanged root implementation
and receipt. The root arithmetic was inspected separately in
`ROOT-ARITHMETIC-AUDIT.md`. `../../verify.py` compiles this checker and the
frozen integer checker from source bytes and compares their maps, inverses,
and exact failure controls. Its `n=1` matrix control instantiates CubeJerry's
pinned #6778 universal row/column noncommutation theorem for this candidate.

The finite cube and large-number cases corroborate the candidate; they do
not prove the all-input theorem in `../../proof/PROOF.md`. This role shared
the root-supplied candidate formula, so it is not blind review. The map meets
#6778's hypotheses because it is globally unit-covariant and exact on all
integral images of `C_+`; the scope and transfer are derived in the audit.

The cross-check also records a wrong-phase control at
`u=(-2-2i), v=(-2-i)`, for which global `i` covariance fails, and the exact
`F^4` counterexample. These finite controls complement the proof; they do not
replace it.

This is a finite implementation cross-check of a shared candidate formula.
It is not a formal proof, blind review, or evidence of any selected caller or
physical implementation.
