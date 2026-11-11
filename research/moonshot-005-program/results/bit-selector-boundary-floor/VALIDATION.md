# Verification record

- Normal and optimized Python executions pass and produce byte-identical
  generated receipts in RESULT.json and RESULT-OPTIMIZED.json.
- Both input files are checked by SHA256 and Git blob identity before use.
- All 659² source public scalar coefficients, main-only identity, absence
  of main/core SWAPs and main resets, final charts and owned retirement are
  checked directly. This implementation imports no predecessor scientific code.
- Boundary basis/annihilator ranks and orthogonality are checked over the
  rationals; the full dimension-8 chart is checked literally. This is not
  an independent audit of all original nested MOVE geometries.
- Finite m=2,4,6 selector lifts attain entry/exit cut ranks (111,222),
  (111,444), (111,666). All 111,333,555 repair crossings raise rank exactly
  one; retirement preserves it. The universal theorem is the written proof.
- All 755 main-frame configurations cover every one of 34,138 source cuts.
  Minimum X dimension minus maximum Y dimension is at least one; all 628
  original main-only ADDs are X-to-X.
- All 4,096 three-row/three-source/binary-cut states receive 65,536 exact
  local transition checks. Controls exhibit a free cross-chart ADD, a
  value-only unequal-chart SWAP, and a preloaded X-dependent low-side helper.
  These demonstrate why those operations/premises must be excluded or charged.
- Literal caller J, QUERY, IDLE_ONE and target masks reproduce all root terms.
  Exact adjacent integer 200th-root enclosures with denominator 10^30 give
  M2<-444 and D<88. Omitting repair gives a positive m=2 false-positive
  moment; charging the rank floor reverses the sign.
- A first receipt comparison failed because Python integer histogram keys
  deserialize from JSON as strings. Comparison now canonicalizes through
  JSON; both scientific runs had identical values. Corrected normal/-O
  replay passed. No mathematical result changed.

Lead review found the rank-cut argument sound within the stated normalized
scope. This is same-team model-assisted review, not human or kernel acceptance.
Any additional independent artifact is separate.

Bootstrap predecessor reproduction also passed with unchanged source pins:
BOOTSTRAP-AUTHOR-REPLAY.json is PASS_TARGET_BIT_BOOTSTRAP;
BOOTSTRAP-REPLAY.json is PASS_INDEPENDENT_BOOTSTRAP_REVIEW. These replay
existing checks, not newly independent verification of that theorem.
