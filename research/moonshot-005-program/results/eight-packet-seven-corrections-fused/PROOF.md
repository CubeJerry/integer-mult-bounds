# Seven joint corrections with observation-aware private-route fusion

## Actual finite construction

The frozen seven-correction E8 word has 76,060 instructions and implements the partial private operator stated in its proof, with all 1,480 common outputs restored. This package applies the root's independently reviewed monotone route-fusion rewrite to that exact word. The new literal word has **74,757 instructions and 407 private raw MOVEs**, preserving every actual arithmetic access, all seven corrected coefficients, every one of the other 4,985 residual coefficients, all common outputs, and all final charts.

The parent word has compressed SHA256 `ae7a86a02b853f3166c6727d66e0a2440b0e5e4e8e3a7d35e69dae029d66942d`. The frozen source has compressed SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.

The rewrite and directed exact moment-bracketing code are reused from `root-research/route_fusion/build.py`, SHA256 `f42e7a10b22d10467d1463e4753a6c7cf064ece4bd7bbc1a7fed1378daec1526`. The adaptations are the parent pin and schema, dictionary boundary marks, the parent/native/prefix provenance fields, and the eight rank9 paid packet calls. The common/native programme and all non-MOVE instructions are unchanged. Prepared with OpenAI assistance; credit the original native, H4 invoice, E8 prefix, budget worker's joint controllers, and root's reviewed route rewrite.

## Why the rewrite preserves the actual interfaces

For a private public carrier, collect a maximal chain of strictly upward MOVEs between consecutive non-MOVE instructions that touch it. Other fields' instructions may lie between its MOVEs. Replace the chain `U0 -> ... -> Um` by the direct `U0 -> Um` at the last old MOVE position. The carrier stays at `U0` until that final replacement. Every earlier intervening instruction is independent of it, and every later actual read or write sees the same value at the same chart.

The source uses the logical-coordinate chart-transport convention, so physical maps compose as `C_target C_source^(-1)`. The direct nested transport implements the same composition as the chain. Its rank is the sum of the old rank increments. This uses the retained native, complete-field transport, scalar, layout, and compiler foundations; it is not a claim about arbitrary communication networks.

The implementation checks every original chain's strict nesting and continuity and verifies that no intervening non-MOVE instruction touches its carrier. It preserves all ordinary instructions and all non-raw MOVEs exactly. At a boundary marker it records the number of surviving earlier parent instructions, so the all-input replay sees the same semantic checkpoints. The native event map is translated to the new physical positions.

The raw donor caches are acquired at their initial charts before the E8 donor hoists; none requires an intermediate donor stop. All first-receiver history reads remain at their actual source times and charts. The six selected receiver routes retain precisely their read charts and endpoints:

| Raw receiver | Retained route after fusion |
|---|---|
| 116 | 3 → 449 → 929 → 131 |
| 144 | 3 → 911 → 157 |
| 145 | 3 → 914 → 158 |
| 160 | 3 → 911 → 171 |
| 161 | 3 → 914 → 172 |
| 172 | 3 → 524 → 183 |

The other 394 raw carriers each use a single rank8 endpoint MOVE. These include all 104 first donors, the 98 other first receivers, and the 192 hosted second roles. The controller additions, stationary caches, common-history observations, all 1,014 hub repair ADDs, and all 400 recouplings are unchanged.

The old 2,362-operation prefix count is now **semantic parent provenance**, not a count of literal retained instructions. The fused word stores the exact parent event for every emitted instruction and the list of old parent/source raw MOVE events represented by every fused call. The removed intermediate stops are unavailable. Any later construction that needs one must restore and price that access, or provide a different physical route.

## Complete endpoint identity remains unchanged

Let `q_i=v_i-u_i`, let `T` be the complete common native operator, and let `G` be the source E8 Gram matrix. At the 104 first receivers the fused word still has

\[
(Tu)_{i+112}+c_iq_{i+112}+\frac{c_i}{8}\sum_jG_{ij}q_j+\sum_dK_{i+112,d}q_d,
\]

with the same correction matrix as its parent:

| Receiver | Nonzero correction |
|---|---|
| 116 | `+q110/2` |
| 144 and 160 | `-q111/2` |
| 145 and 161 | `-q36/2` |
| 172 | `-(q37+q47)/4` |

Receiver172 obtains one aggregate, not two independent observations. All other private main roles still have `(Tu)_r+q_r`, and every common field equals `Tu`. All public outputs retain their prescribed final charts. The seven selected E8 residuals vanish; all other 4,985 coefficients are unchanged. No first receiver is complete, and the private hosted/coupled reverse duties remain open. The full 400-row private difference inverse still holds.

## Exact emitted operation bill

| Quantity | Seven-correction parent | Fused word |
|---|---:|---:|
| Instructions | 76,060 | 74,757 |
| Common MOVEs | 6,310 | 6,310 |
| Raw MOVEs | 1,710 | 407 |
| Paid E8 rank9 MOVEs | 8 | 8 |
| Total MOVEs | 8,028 | 6,725 |
| ADD | 64,227 | 64,227 |
| SCALE | 3,670 | 3,670 |
| COPY | 1 | 1 |
| INIT / CLEAR | 67 / 67 | 67 / 67 |
| Peak owned fields | 43 | 43 |
| Final owned fields | 0 | 0 |

The raw rank sum remains exactly 3,200. The source and new raw histograms are

\[
R_{\rm source}=\{1:990,2:360,3:105,4:112,5:133,6:8,7:2\},
\]

\[
R_{\rm new}=\{1:5,2:2,5:1,6:1,7:4,8:394\}.
\]

The complete word's MOVE histogram, including unchanged common and packet transport, is `{1:4080,2:830,3:811,4:241,5:321,6:18,7:16,8:400,9:8}`. Exactly 1,303 old raw calls are absent.

## Conditional complete caller invoice

The authentic H4 invoice is included as `INPUT-INVOICE.json`, SHA256 `b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248`. With its target `T4` unchanged, the new paid histogram is exactly

\[
P=P_4+18(R_{\rm new}-R_{\rm source})+18\cdot8\,\{\text{rank }9\}.
\]

No erased route is retained as a paid call or as free side information. The eight E8 packets are charged explicitly. The resulting histogram has 27,344 target positions, 129,114 paid positions, and rank surplus 3,760. The full histogram is recorded in `RESULT.json`.

At `t=199/200`, the per-native moment saving from the actual route deletion is

\[
\Delta=\sum_r(R_{\rm source}[r]-R_{\rm new}[r])r^t
       =19.77604617001255\ldots.
\]

The remaining provisional moment per native is

\[
H=H_4+\Delta-8\,9^t=46.96179481981380\ldots.
\]

Both quantities are certified by rational lower and upper bounds computed with integer 200th-root brackets; the decimals are explanatory. The lower bound for `H` is

\[
\frac{211328076689162089111673074982281}{4500000000000000000000000000000},
\]

and the upper bound has the same denominator and numerator `211328076689162089111673074998683`. This is a provisional budget for the actual partial word. It does not pay for the remaining 4,985 residual terms, private reverse duties, or missing supplier and compiler obligations. Positive margin alone is not a complete algorithm or a new kappa.

## Exact typed and chart-map verification

`replay.py` explicitly reuses the pinned seven-correction exact rational interpreter, SHA256 `0367ae2b674de218acaad4528a5efb1ff488b136f5a2cec867829ff1ea4adfaa`. On the actual fused word it checks all 1,880 independent input columns, every typed arithmetic/transport access, the COPY guard, actual cache values, timed receiver gains, all pre-repair and repaired common rows, all 400 private endpoints and charts, ownership counts, and the private difference inverse. This is an integration replay using the existing interpreter, not a new independent engine.

The root's `check_chart_maps.py` is copied unchanged and run with assertions enabled. It compiles every one of the 209 introduced source/target chart pairs using the retained exact Clifford engine, and checks each resulting recipe against the separately implemented signed-Pauli/global-phase engine. Every new map has the correct complete recursive rank. A deliberately incorrect global phase is rejected. `CHART-MAPS.json` records every recipe and the actual frozen engine hashes.

These finite map checks authenticate the newly emitted transports under the retained chart conventions. They do not replace the uniform all-field supplier, compiler, precision, layout, or compatible BIT/complex foundations. Non-MOVE rational scalar services are inherited unchanged from the parent and remain real obligations.

Normal and optimized builder runs produce identical compressed word and invoice bytes. Normal and optimized full-input integration replays produce identical receipt bytes. The exact chart compiler was run only with assertions enabled, and both engine hashes agree with the root chart-map receipt.
