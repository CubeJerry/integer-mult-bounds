# Independent Route B review: address scaling and F4 repair

Date: 2026-11-25 UTC, E002. This is a written independent-agent audit, not
human refereeing or proof-assistant certification. OpenAI math source pin:
`3344da59991ed94f9ba711217b29c1d760badfa6`.

## 1. Height-priced affine streams

Reviewed file: Route A `HEIGHT-PRICED-AFFINE-STREAMS.md`, SHA-256
`8c28e7886faf8ede9b6d54f4eec2fe9b260c73996ed8c6b1ccc0e8c052c9c8a3`.
I also read `verify_height_streams.py` and the November source elementary-
affine discussion in `interchange.tex`. Finite replay is recorded below.

**Verdict: accept Theorem HS and its lower-triangular corollary as written
components, with their stated scope.** They do not make general coordinate
permutations free and do not alter the shared recursive-call invoice.

With `Q=aq+s`, `y_r=ceil(rQ/a)` and `t_r=(-rQ) mod a`, a position
`y_r+k` maps to `ak+t_r`, and `ell_r=q+1` exactly for `t_r<s`.
Coprimality makes the run-key map bijective. Padding to q+1, sorting by
the small key, padding row count to a power of two and transposing gives
natural output order. Known dummy positions handle ragged boundaries.
The inverse uses an inverse modulo a, not a large coefficient modulo Q.
Negative coefficients use the explicit block reversal, preserving payload
order within each block.

The cost does not pay a times the whole array: all a runs move during the
same scans. Headers have at most h bits, `a<=Q`, and padded payload is
less than four times the original volume. One row-digit move across an
arbitrary `[q+1]` field is binary splitting/interleaving, not a recursive
near-root interchange. Repeating h scans costs polynomial h per volume.
Per-run long-counter calculations are paid by that run's complete `qB`
symbols. Unrelated prefix counters are not fully reread at each record.
Reused fixed regions bound visited cells.

The triangular reduction retains descending physical target order.
Off-diagonal offsets are computed once per complete target fibre, paying
for polynomial log-Q arithmetic. A general matrix retains its separately
charged field permutation.

## 2. On-demand F4 spectral repair

Reviewed file: lead `on-demand-spectral-repair.md`, SHA-256
`0bab33fbe84278385cf857c43acdb39d8cbce7dd1aa155b281c2c35de4433bc5`.
I read the predecessor power-two predictor, structured shift checks,
order-three closure, and source `subsec:swap-spectrum` comparison scan.

**Verdict: accept SR1--SR3 and the aligned-row implementation in SR4.
Bookkeeping clarification requested: choose v=32w and append zero check
rows as in the predecessor before asserting exact phase size R/16.**
The identities themselves hold for arbitrary module width v.

For signed a=qT+r and power-of-two T,
`(1+X)^a=(1+X^T)^q(1+X)^r` in formal power series. Its degree-<T
truncation is exactly `(1+X)^r`, including q<0. Evaluating that finite
polynomial at omega-1 proves SR1. The ratio formula follows because
`c_beta-sum beta-sum k` is divisible by three. Outside-window rows can
have zero gap; the squared-gap repair correctly avoids division by it.

The inverses have the right orientations: first recover
`e_J=(p-z)X_J` from the first ell check coordinates; then the transpose
inverse makes the lifted values `(p-z)^2 e_J`. A nonzero F4 gap has
cube one; a zero gap needs no correction. Every error therefore vanishes.
Tensoring with the module identity preserves all independent input rows.

The matrix dimension is O(m), independent of module width, and field
elements have O(log m) bits. Repeated full sequential scans of the small
matrix remain polynomial fixed-tape work. The comparison masks are paid
by complete later-field/suffix fibres as in the source. For aligned rows,
serial input-role/output-role scans accumulate the small maps in polynomial
work per volume. Recomputing the entire matrix per record remains a safe
polynomial overcount. Forward/inverse converter words remain paid.

This does not certify another layout, an uncharged diagonalizer, the
predictor executor, radix batching or a complete multiplier.

## 3. Isolated finite replays actually performed

Route B copied each checker to its own output directory before execution,
so no shared artifact was regenerated. Commands from this route directory:

```
python height-replay/verify_height_streams.py
python f4-replay/verify_spectral_repair.py
```

The height replay passed 8,562 forward, 8,562 inverse, 8,562 signed and
4,996 rational permutations; 312 transposes; 527,486 run identities;
7,989 wrong-sign controls and 8,177 ragged-padding controls. Its JSON is
`height-replay/height-streams-verification.json`.

The F4 replay passed 2,310 signed truncations, 6,930 phase cases and
23,664 full-basis repairs, including 1,020 containing sets with zero gaps.
It rejected 2,766 wrong-transpose, 2,328 wrong-gap and 96 outside-F4
controls. Its JSON is `f4-replay/spectral-repair-verification.json`.

These are separate executions of the authors' exact checkers. They are
not an independently implemented physical machine. The written mathematical
audit above supplies the separate proof review; finite tests do not prove
the asymptotic physical bills. No full multiplier or Lean build was run.

Credits: @CubeJerry; OpenAI sources and programme predecessors; Route A and
the lead's E002 constructions; independent Route B review with substantial
ChatGPT assistance.
