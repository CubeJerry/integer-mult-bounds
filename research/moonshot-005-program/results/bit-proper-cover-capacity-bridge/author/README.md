# Operator consequences of the reviewed proper-cover capacity

This package transfers the scalar chi-saving cap16 to arbitrary operator
quotient images using one common generic value functional. It preserves
the distinction between cardinality ell, the linear/quadratic proxy gamma,
and exact capped proper-cover charge chi.

The resulting source-specific requirements are:

- canonical quotient d>=V+ceil(V/16) whenever chi saving exceeds16;
- weighted and finite-field incidence refinements;
- d>=sum(v_j+ceil(v_j/16)) for a common invariant filtration;
- V*S_chi<=16r under the inherited small decomposable or MDS hypotheses;
- MDS r>=ceil(7V/4) at target saving28, excluding the old V3/r5 point.

V4/r7 is only a remaining arithmetic possibility under cap16, not a
construction. The proof retains a generic capacity-L form for future
independently established scalar improvements. It does not assume L=14.

PROOF.md is the universal argument. SOURCES.json pins the scalar theorem
and review plus every inherited structural premise. check.py supplies
exact native and abstract controls, including a genuine native support
fitting at the strict2V boundary and an abstract sharp17/16 incidence family.
Neither is a physical source implementation. No new kappa.

```sh
python PACKAGE/author/check.py --native NATIVE --output /tmp/cover-bridge.json
python -O PACKAGE/author/check.py --native NATIVE --output /tmp/cover-bridge-O.json
```

Use the pinned BIT-NATIVE-WORD.json.gz for NATIVE. No third-party package is
required. Expected status is PASS_PROPER_COVER_CAPACITY_BRIDGE_CONTROLS;
the V3/r5 chi bound is196, and normal/-O JSON receipts agree.
