# Independent review of delayed class correction at A15

**PASS within the stated partial-construction scope. No new κ.**
Reviewed author proof `worker-a/delayed-correction-source/PROOF.md`, SHA256
`d89bd2bdc51a1004dd9fe2b5dfdfaed118ba14ebfb5d769a7a0ef722097abc8b`.
The independent checker imports no author code. It reconstructs the native
geometry with rational row spaces, replays every operation on all222 original
X/Y columns, checks every chronological co-location and monotone MOVE, and
reconstructs the h9 W rows from the pinned roots.

## Independently established facts

The actual P0 whole-cell boundary arrival at A15 equals `k0=e0+R0`, where
R0 is the total class-zero raw-cache sum. The first exchange immediately
follows that arrival, so there is no unnoticed interior/local translation.
Y0 arrives with `y0+R0_suffix`, reads P0 and feeds back; its later genuine
class-zero prefix reads complete `y0+x0` at F0. P0's unchanged suffix reads
and actual captured y0 cancellation give terminal `R1_suffix`. All original
X restore at Hub; no other Y receives an unintended update.

The kernel is genuinely mixed modulo its own chart-local inputs and x0:
adding k0 increases `span(e0, Local(A15))` from dimension12 to13. Its binary
coefficient identity gives the same strict independence over every
characteristic-two extension and at every positive block width V. This is
an enabling kernel construction, not a supplier.

The literal packet-history span has rank48, y-projection rank1, pure-X
dimension47, and contains all111 W fitting rows (dimension15). The80 actual
colored cache increments have span40 and W intersection8. The terminal
space has rank8 and W intersection7. Adjoining k0 increases terminal rank
to9; the resulting normalized space has W intersection7 and canonical C
intersection0. After deleting input0, the terminal and normalized ranks are
still8 and9 respectively, so the new kernel escapes the earlier pure-point
puncture test. It does not escape the admitted complete target rank floor
`9V+ceil(V/3)`: only one width-V kernel is present.

The closed word has200 zero-born owners,943 ADDs,495 MOVEs and200 dirty
retirements. Its movement profile is
`183[1]+12[2]+119[3]+71[4]+110[7]` at exponent199/200. Independent exact
integer-root interval arithmetic gives movement1606.54416195179121546...
and retained-caller limiting room15.20671825936113978.... The complete
finite-even-m movement formula is positive already at m=2 and has positive
slope. This is a movement-only comparison; all remaining supplier,
ordinary-operation, ownership and recursive costs remain owed.

The live word is checked separately, with all live owner handoff rows and
charts verified. Its partial movement is not reported as a complete invoice.
The closed receipt includes all110 unfinished receiver ascents and every
owner retirement. Six independently implemented semantic mutants all reject:
omitted feedback, suffix read, later correction, preload, y0 capture and y0
unmask. These tests accompany, rather than replace, the symbolic proof.

## Reproduction and retained scope

```sh
python3 -B check.py --repo /path/to/programme \
  --word /path/to/delayed-correction-source/output/CLOSED-WORD.json \
  --out /path/to/review-delayed/closed-output
python3 -B check.py --repo /path/to/programme \
  --word /path/to/delayed-correction-source/output/WORD.json \
  --out /path/to/review-delayed/live-output
```

Expected status: `PASS_INDEPENDENT_DELAYED_CORRECTION_SOURCE` in both cases.
`MANIFEST.json` pins the reviewed proof, generator, both words, independent
checker and receipts. The author prototype receipt in `output/` is preserved
only as an earlier review checkpoint; the clean portable live/closed receipts
are authoritative for this review. No complete decoder, new κ, or discharge
of a foundational assumption is claimed.

This is independent mathematical and implementation review by Worker C,
not a rerun of the author's verifier. Construction and schedule credit
remain with @CubeJerry, the programme's colored-source and stationary-history
predecessors, and the root/Worker A delayed-correction proposal; AI assistance
is disclosed in the cumulative programme record.
