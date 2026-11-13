# Independent review: eight-target BIT mode-exchange bus

**Literal partial word: pass.** I interpreted the frozen 274-operation word
with an independent GF(2) bit-vector engine and exact rational chart tests. I
did not import or call the retained replay. The word completes eight Y rows,
restores all 111 X rows, and leaves the other 103 Y rows unchanged.

## Source and value replay

The native input hash is
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`; the
compressed literal word hash is
`9caac6d9b939c60bbfe54937bd30f2b2f6b2037a99f6e3a35ec10ac2794341be`.
Every MOVE has distinct source and destination dimensions and exact rational
nesting. Every ADD and CLEAR occurs at the field's current chart, and the sole
owned field is initialized once and cleared once.

The seven feedback checkpoints independently satisfy, for served role `k`
and captured role `k-1`,

| Checkpoint quantity | Replayed row |
|---|---|
| Y output after packet read | `y_k + x_k` |
| Source X field after capture | `x_(k-1) + x_k` |
| Packet after handoff | `x_(k-1)` |
| Source X field after Hub restoration | `x_(k-1)` |

At the last exchange the packet carries `x_0`; it adds that value to `Y_0` at
zero and is cleared with nonzero value `x_0`. The final public row matrix has
rank222 over F2. This verifies all input directions, not only selected sample
assignments.

## Recomputed profile and controls

The independent interpreter obtains 274 operations: 242 MOVE, 30 ADD, one
INIT and one CLEAR. The MOVE profile is `{1:12, 2:4, 3:4, 4:4, 5:4, 6:4,
7:210}`; one owned lifetime is retired, peak ownership is one, and all 242
MOVE pairs are distinct and nested. All four submitted controls fail as
claimed:

| Control | Result |
|---|---|
| Omit first X restoration | Public rows 0–6 are wrong |
| Omit first packet handoff | Public rows 0–5 and 117 are wrong |
| Reverse the first feedback order | Public rows 0–6 and 117 are wrong |
| Form packet before source reaches Hub | Rejected: packet is inactive |

The limiting-price arithmetic for the uncoded orthogonal tiling profile
`{7:222, 8:14}` also replays with directed 160-bit roots and gives a deficit
greater than `28.0442595295`. That arithmetic is conditional on the separately
asserted minimum of 14 packets for the plain uncoded tiling. It does not
restrict coded cross-frame buses.

## Scope

This is an actual finite F2 feedback word using the pinned source geometry.
It completes only roles 0–7 and preserves roles 8–110. It does not supply a
complete 111-target word, a compiler or uniformity proof, or a new kappa. The
plain-tiling price check does not imply a lower bound for coded buses.

The independent interpreter and machine-readable receipt are
[`verify_exchange_bus_independent.py`](verify_exchange_bus_independent.py) and
[`RESULT.json`](RESULT.json). The exact word/result bytes reviewed are pinned
in [`MANIFEST.json`](MANIFEST.json).
