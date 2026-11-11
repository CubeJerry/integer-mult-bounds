# Separate review implementation

REVIEW.md contains the independently derived fixed-channel, one-switch and
two-switch proofs. REVIEWED-FILES.json pins the exact authored proof and
scientific files examined. No author scientific module is imported.

From repository root, replacing REVIEW with this directory:

```sh
python3 -I -B REVIEW/independent.py \
  --source research/shared-wire-split-composition/data/final.json.gz
python3 -I -B REVIEW/two_switch.py \
  --source research/shared-wire-split-composition/data/final.json.gz \
  --certificate REVIEW/REVIEWED-287-SAMPLES.json
```

The first command uses the standard library and was run normally and with
-O, producing identical RESULT receipts. It checks the source by reverse
adjoints and frame row reduction, 2,304 rational cohort-factor pairs and
110,808 finite-field matrix triples. The latter matrices corroborate the
noncommuting one-switch equations; they are not a physical F2 half-broadcast.

The second command uses NumPy (version in REVIEWED-FILES.json) for an
independent transposed state replay and reverse-pivot modular elimination.
All 287 sampled prefix/suffix ranks were recomputed; 302/303 are rigorous
whole-cut lower bounds via separately counted rank-one updates. The source
has 71,262 cuts and residual rational rank at least 275, while maximum
prefix/suffix nullity sum is 195. No loop over all cut pairs is required.
The 287 expected sample map is the exact union of the author's original and
refinement rank receipts, retained after its portable packet was reduced.

The portable author's 52 samples are an exact subset of these recomputed
ranks. Independent interval recount gives the weaker but sufficient bounds
270/270 and nullity sum260<275 (PORTABLE-CERTIFICATE-CHECK.json). A fresh
execution of its standard-library verifier exactly matches its final receipt
(PORTABLE-AUTHOR-REPLAY.json); that repetition is not called independent
verification. The separate full modular implementation and written proof
review supply the independent evidence.

All conclusions retain the normalized source model and the exact global
exchange class. Extra wrappers, role-local codes and changed trajectories
are not excluded. This is model-assisted independent work within the same
research team, not human or formal proof-kernel acceptance.

ADDITIONAL-REVIEW.md extends the review to the fixed-input paid endpoint
repair floor and the conditional causal coded-storage interface. The new
independent source check is standard-library only:

```sh
python3 -I -B REVIEW/endpoint_independent.py \
  --source research/shared-wire-split-composition/data/final.json.gz
```

It gives the exact rational deficit208 across105 final frame cohorts; normal
and optimized executions agree. Desired E is reconstructed from the pinned
endpoint parameters, with source binding inherited from the retained native
and the earlier modular review. This is not a new400-column rational replay
of the complete native. The coded-storage review is algebraic and conditional;
no causal all-events witness, full invoice or new supplier is claimed.
