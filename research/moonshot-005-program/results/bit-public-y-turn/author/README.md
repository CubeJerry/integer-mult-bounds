# A paid original-Y turn with gauge and canonical cores

Status: two actual nine-target partial words; no complete supplier and no new kappa. The canonical variant uses the separately reviewed canonical3+6 static interface. Both retain an exact six-future-channel cut after the two local cell packets retire.

```sh
python worker-a/public-turn-nine/build.py --native bit-native.json.gz --prefix-builder worker-a/half-class-point-prefix/build_point_prefix.py --output worker-a/public-turn-nine/reproduced-gauge
python worker-a/public-turn-nine/build.py --native bit-native.json.gz --prefix-builder worker-a/half-class-point-prefix/build_point_prefix.py --core-code worker-c/canonical-core-prefix/CODE.json --output worker-a/public-turn-nine/reproduced-canonical
```

Expected both: PASS_PUBLIC_Y_TURN_NINE_TARGET_RECODING,121 INIT,882 partial unitMOVEs,5 partial CLEARs, peak118,18 rejected semantic controls. Gauge has463 ADDs; canonical has514. Closing gives1596 unitMOVEs and121 CLEARs. Exactly one original-Y downward occurrence is admitted and charged; no owned upward move occurs.

Reproduce the actual coalesced movement profile with:

```sh
python worker-a/public-turn-nine/check_profiles.py --word worker-a/public-turn-nine/canonical/CLOSED-WORD.json.gz --moment-checker worker-a/half-class-point-prefix/check_budget.py --output worker-a/public-turn-nine/reproduced-budget.json
```

The complete proof and full invoices are in PROOF.md. Standalone words include actual frames and operations. Each variant's RESULT-OPTIMIZED.json matches RESULT.json byte-for-byte. BUDGET.json is only a partial-source moment screen. No later decoder may read an absent halfbank or treat a source-line cache as a free larger-chart input.

@CubeJerry and predecessor/Worker C/root credit in PROOF.md; OpenAI assistance.
