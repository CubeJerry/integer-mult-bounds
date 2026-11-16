# A paid native-port repair preserving all34 endpoints and every terminal value

**Status:** proved literal placement repair. All34 endpoints and every seed-cut value remain unchanged. One actual rank4 owned helper move relocates the P3 line cell from L0 to L29. This changes the information-coverage obstruction, but does not complete111 receivers or establish a new kappa.

## Pins and actual move

Base34 word: `46e299557269f8f78aedd9e049a2db020b22e64c6e7df59101a8c61cca05224e`. Repaired word: `8580350db073049f01268989d6acdb4bf770699a079760163a394d2867323c36`. Native source SHA256: `8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`, at `research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json`.

The predecessor P3 carries h2=X0+X2+X28+X29 from M1 to L0, retains h2 in ZKEEP2 there, resets, then reads a stationary raw X0 helper ZRAW0. Its terminal value is X0+E6. Receiver2 preloads X0+X28 at ground, reads h2 at L0, then reads raw X29 from ZCORR2 at Jnew2=span(L0,L29), and reaches F2.

The repaired source places ZKEEP2 at L29. Its helper ZRAW0 is now initialized at M1. Original X0 already follows L0 to C2=M1 to Hub and is still raw on its first C2 arrival. Immediately after that actual arrival, copy X0 into ZRAW0 and execute an **owned MOVE from M1, dimension5, to L29, dimension1**. This rank4 movement is explicit in the word and full invoice. The earlier native-line capture is removed; it is not counted twice or reused after relocation.

P3 follows M1 to L29 to ground, using the unchanged retain/reset/query sequence. It therefore has exactly the same h2 retention value and terminal X0+E6 value as before. Only their physical line location changes. Receiver2 follows ground to L29 to Jnew2 to F2. Exact native geometry gives L29 subset M1 and L29 subset Jnew2 subset F2, so every read and move is legal. The same algebra yields Y2+X2. Every other receiver reads unchanged values at unchanged locations, so all34 endpoints remain correct for arbitrary original X and Y records.

All original X routes, all reversible source recoding/restoration and all owner retirements remain unchanged. The only seed-cut location changes are ZRAW0 and ZKEEP2, both now at L29. **Every seed-cut value remains identical.** The original `d=0` metadata still denotes the raw terminal point source; new explicit `retention_port=29` distinguishes it from the placement. No new raw point is claimed at ground.

The construction is an identity of binary whole-record operations and holds for every positive record width over every characteristic-two field.

## Full invoice

INIT, ADD and dirty CLEAR counts remain114,902,114. There is one additional MOVE, for a total436. The P3 path distances remain4 then1; the Y2 path distances remain1,1,5. The new helper move is the only movement change. Consequently the profile is `{1:110,2:65,3:56,4:14,5:73,6:24,7:94}` and the exact increment at t=199/200 is4^t.

All source preparation is included: ZRAW0 has a genuine birth at M1, an actual raw original read there, a fully paid descent and dirty retirement. The repair does not treat an original point as freely available at a different line. Directed exact movement price and remaining room are recorded in `output/PRICE.json`; all nonmovement and complete-supplier obligations remain separate.

The resulting movement lower endpoint is1618.662365963086010513454934598012745919218787459217, leaving approximately3.08851424806634 of the limiting movement allowance. This is a substantial paid change despite the unchanged endpoint count. It should be retained as an exact placement-repair option, not silently replace the cheaper34 source as the programme's preferred cost baseline.

## What the repair removes, and the new binding constraint

The predecessor separated-bank envelope at ports(0,28,44) for h1 failed receivers24,42,69. The repaired h1 ports are(29,28,44). In the same generous envelope—all h0 raw52, non-Extra h1 raw53, the two fixed higher preload classes, all completed34 points globally, all proper raw locals and free point feedback—the closure is now110. It includes all three old failures but excludes receiver46.

The new exact dual is e46. The checker verifies that it annihilates every allowed receiver46 row and all110 granted points while pairing to1 with X46. Thus the repair does not solve the full coded-load problem; it moves the binding access constraint. This is why matching only the old three receivers is insufficient. The separate complete51-case port screen identifies other single-line changes with111 optimistic coverage, but their source custody and decoder repairs remain to be assembled.

For the actual repaired word the full frozen live/history/raw-local envelope still closes at34. The additional helper is nonlocal at L29, but its raw X0 value was already globally available, so it adds no independent normalized information. There are23 proper nonlocal fields, normalized rank36, and the same147 rank after111 Y nuisance columns are adjoined. The package records actual histories and77 outsider dual witnesses for the frozen34 closure. None of these statements grants the historical rows as free global fields.

## Verification and reproducibility

```bash
python build.py --base /path/to/higher-source-thirtyfour/output/WORD.json --out /tmp/port29
python check.py --repo /path/to/programme --base /path/to/higher-source-thirtyfour/output/WORD.json --out /tmp/port29
```

All222 columns, native rational chart directions, raw X0 capture at the actual first M1 arrival, the paid helper MOVE, every original restoration, all34 endpoints, all seed values and every owner retirement are checked. Nine semantic controls remove the actual raw capture, helper movement/query, a retention/delivery/correction or retirement, or restore an incorrect old native birth. They fail with invoice, source-cut metadata and milestone assertions disabled. This directly rejects the tempting late-born/free-helper substitution.

The word and verification receipts are pinned by `MANIFEST.json`. Proposed by the root and implemented by `/root/bit_construction`, with independent `/root/bit_bridge` review, in the @CubeJerry programme with AI assistance. The exact cheaper predecessor and its proof remain unchanged. The next complete construction must choose source mixing, port placement and decoder rows together, respecting every resulting helper expense.
