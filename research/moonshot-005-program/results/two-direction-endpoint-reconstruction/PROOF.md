# Reconstruction and full-source audit of the two-direction endpoint code

## Status and provenance

This is a finite exact partial construction, reconstructed independently in S008 from the published S007 ROOT-ENDPOINT-CANDIDATE.md recipe. The old builder and generated archive were unavailable after interruption. The new word is a new serialization and is not claimed byte-identical to that unavailable artifact. It reproduces its mathematical map, operation counts, residual counts, inverse determinant and numerical invoice.

The scientific input is research/shared-wire-split-composition/data/final.json.gz, SHA256 2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883. The source has 1,480 public fields and 71,261 events. Its 400 main fields comprise 104 first X/Y pairs and 96 hosted X2/Y2 pairs; the other 1,080 public fields are arbitrary independent helpers. The H4 invoice is results/eight-packet-budget-and-reverse/INVOICE-SOURCE.json, SHA256 b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248.

The E8 integer coordinates and their tight-frame identity are predecessor results, credited to results/eight-packet-prefix/ and its independent review-algebra package. This package contributes reconstruction, complete source comparison, an explicit actual word and corrected whole-word accounting, not a new E8 representation.

## Exact source targets

Let X_i, Y_i be the 104 first pair roles. Let U be the eight coupled indices, and H its 96-index complement. On hosted indices define reverse roles R_i=X2_i and S_i=Y2_i; on coupled indices define R_i=X_i and S_i=Y_i.

The source targets, in normalized coordinates, are:

    hosted first: X_i -> X_i, Y_i -> Y_i+X_i;
    hosted second: R_i -> R_i-S_i, S_i -> S_i;
    coupled: X_i -> X_i-Y_i, Y_i -> (X_i+Y_i)/2;
    every helper -> itself.

The separate audit_source.py starts all 1,480 final output covectors and propagates them backward through every actual source event. It checks the complete resulting input matrix against these targets, including every helper. It separately pulls the actual COPY destination at event 31,737 backward through its exact prefix and obtains the zero row on every public input. The resulting SOURCE-AUDIT.json and SOURCE-ENDPOINTS.json.gz record this finite source audit. No previous 400-output-only receipt substitutes for it.

## Candidate map and literal schedule

Use two independent main banks u and v and one common helper bank. Form the 400 physical differences q=v-u at each actual initial cochart. Let A be the 104-by-8 integer root matrix, and P=A A^T/8. Its diagonal is one. Let c_i=1 on H and c_i=1/2 on U.

For one main bank the desired approximate transformation is

    Y_i' = c_i*(Y_i + sum_j P_ij X_j),
    R_i' = R_i - sum_j P_ij S_j.

Hosted X and hosted S remain unchanged. On coupled coordinates both formulas use original values.

The word first transports all 1,080 helpers directly from their initial to final charts. Every direct helper pair is a proper nested inclusion. It then performs the following block separately on u and q.

1. At the actual empty chart 3, form and retain eight reverse records sum_j A_jk S_j from original S values.
2. Move all 200 X-like public fields to hub 127. Normalize the eight coupled Y values by one-half at chart 3.
3. For each of eight forward records, form sum_j A_jk X_j at the hub, pay one owned rank-nine descent to chart 3, add c_i*A_ik/8 times the record to each applicable Y_i, and retire the record.
4. Pay each retained reverse record's rank-nine ascent to the hub, add -A_ik/8 times it to each R_i, and retire it.
5. Move all 200 Y-like public fields from chart 3 to their actual final facets.

The reverse records were formed before any coupled Y update; the forward records are formed before any reverse X update. Consequently the two displayed formulas use original values exactly. Every scalar access is checked against current charts. The largest live owned set consists of eight retained reverse records and one forward record.

Finally recouple all 400 q outputs with the corresponding u outputs. Since the same linear map B was executed in both passes, the second bank contains B(v-u)+Bu=Bv, with no remaining u contamination. The two copies are independent at the boundary.

## Input preservation

The hosted untouched X and S rows recover the corresponding opposite shear once the coupled originals are recovered. Write P0=P_UU and, using current outputs,

    a = X_U' + P_UH S_H,
    b = 2Y_U' - P_UH X_H.

Then a=x_U-P0*y_U and b=y_U+P0*x_U. Hence

    y_U = (I+P0^2)^(-1)*(b-P0*a),
    x_U = a+P0*y_U.

P0 is rational and symmetric. Over the characteristic-zero coefficient field, I+P0^2 is nonsingular; its actual exact determinant is 1384497/4096. The checker reconstructs all 400 inverse rows and composes them with the candidate map. Thus all 1,880 original directions survive. This is an information statement, not a free physical inverse operation.

The construction and inverse do not imply correctness against the source. Its exact discrepancies are

    c_i*(P-I)_i X       at first Y_i,
    -(P-I)_i S          at reverse R_i.

There are 208 nonzero residual rows and 9,984 nonzero coefficients per independent copy: 416 rows and 19,968 coefficients in total. These are actual unpaid target duties.

## Literal and complete conditional accounting

The word has 6,952 events: 4,960 ADD, 16 SCALE, 1,912 MOVE, 32 INIT and 32 CLEAR. There are 32 owned lifetimes, peak nine, and no owned field survives the boundary. The MOVE histogram is

    {1:13, 2:18, 3:44, 4:215, 5:68, 6:42, 7:18, 8:867, 9:627}.

All 1,880 public fields move exactly once; 32 owned rank-nine packets are additional.

Use the corrected whole-word difference in ERRATUM.md. The complete provisional H4 profile has 42,480 paid positions, 27,344 productive positions and rank surplus 1,888. Directed integer 200th-power bounds enclose the remaining paid moment/native at t=199/200 around 14.812385620139944, so at most 14 additional positive-rank full-field MOVEs can fit with everything else fixed. The packet fees are already included.

Every ordinary operation, storage lifetime, coefficient service and erasure is explicit in the finite word. Their eventual uniform physical realization, common grid, precision, fixed-tape service and complete compiler tariff are still separate obligations. The raw count is not a literal tape-step cap.

## Verification and limitations

The independent reconstruction interpreter checks all 1,880 input columns, all current and final charts, typed ownership, public ascent, every ordinary scalar, the inverse and the complete invoice. Seven actual word mutations fail: wrong reverse sign, missing reverse MOVE, public descent, omitted coupled normalization, missing helper route, missing input difference and missing recoupling.

All 292 chart pairs introduced relative to the pinned source are checked with the retained exact Clifford compiler and its separate signed-Pauli/global-phase interpreter. This explicitly credited engine reuse is not a new independent implementation and does not prove every unbounded-column foundational contract.

The five foundations remain native_all_columns, owned_erasure, compiler, precision_tape and analytic_recovery. Both uniform complex and completed ordinary BIT suppliers strictly above .005 remain open. No new kappa.

## Open next question

The separate terminal-completion package closes inexpensive repair appended to this boundary. A useful successor must change the earlier encoding or route schedule, carry informative side records before the source directions become separated, or alter the native/caller interface with a complete new invoice. Repeating the same terminal repair with a new encoding basis cannot evade its destination information deficits.

Prepared for @CubeJerry with substantial OpenAI assistance. The S007 recipe, E8 representation, native geometry, caller, compiler and source contributors retain credit; Apache-2.0.

