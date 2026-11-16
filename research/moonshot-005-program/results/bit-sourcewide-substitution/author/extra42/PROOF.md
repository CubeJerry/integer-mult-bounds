# One retained Extra6 direction, preserving 42 outputs

The predecessor cyclic cache/import word has SHA256
`47cb0991e41d06efae453f0e2890af6f619ccc44109b46329749bee658a18d15`.
This word has SHA256
`d5726e001270e007209507c8eb9f385167a7d304a9f09c194381296b569f293f`.
The native source is unchanged and pinned in both words.

## Actual construction

The proper-birth packet `P6` previously read actual raw `X20` from
`EXTRA_AFF` at `Extra6`, descended to `L19`, retained that raw row in
`HKEEP_L19`, reset by adding the retained row, and loaded actual raw `X19`
for its existing ground terminal. Its retained row served only `Y20`.

Capture `X20` at its native line into new owner `GROUND20` and move that owner
to ground. The old `Y20` decoder is replaced by an actual ground read of this
row followed by direct ascent to its native facet. This costs exactly one
owned rank-one movement, one INIT/CLEAR pair, and one capture ADD.

The now-unneeded original `X20` visit to `Extra6` and its capture into
`EXTRA_AFF` are replaced by the corresponding actual original `X37` visit and
capture. Both original routes split rank seven as rank five plus rank two, so
their movement difference is zero. `P6` now retains raw `X37` at `L19`; its
existing reset still leaves the previous ground `X19` terminal unchanged.
Since native roots 19 and 37 are orthogonal, `Y37` ascends through `L19`, reads
that actual retained row, and continues to `F37`.

The old `Y20` subdivision and new `Y37` subdivision have identical rank
profiles and cancel in the signed invoice. All three actual imports
`IMPORT_E8`, `IMPORT_E9`, `IMPORT_E36` remain at `M1` unchanged.

## Complete invoice and scope

The exact change from the cyclic-imports41 word is **`+[1]`**. The new counts
are 125 INIT, 830 ADD, 484 MOVE, and 125 dirty CLEAR; peak ownership is 125.
The movement moment is enclosed by

`[1618.11691190364089695624798936899288,`
` 1618.11691190364089695624798936899586]`,

with necessary limiting room at least
`3.633968307511458289998160997998015`.

Every one of the 222 independent initial columns is replayed. All original X
values are restored at Hub; the 42 listed original Y records have their exact
requested increments, and all other Y values remain unchanged. Eight omitted
source, movement, receiver, or retirement operations fail the replay. Literal
binary identities lift to every characteristic-two field and every positive
whole-record width. This does not supply the remaining 69 outputs, a complete
recursive invoice, a new exponent, or any omitted foundational assumption.

This is an explicit source and history change, not the frozen-history model
excluded by earlier capacity gates. It is not cheaper in movement than simply
adding one new native-to-ground raw output; its value is to expose an actual
programmable Extra6 retention for coupled codes.

## Reproduction and next question

From the shared workspace root:

```sh
python3 -B workers/coded/build_extra42.py \
  --repo programme --base workers/coded/cyclic-imports41/WORD.json \
  --engine workers/audit/leaf-capacity-gate/check.py \
  --price-engine workers/audit/review36/check.py \
  --out workers/coded/extra42
```

The next construction couples this real source with a second original whose
old capture itinerary is repaired explicitly, rather than assuming arbitrary
Extra6 source loads. The actual43 package supplies the `{19,37,50}` case.

Predecessor code, the source-recovery certificate, root's endpoint reduction,
and C's proper-birth construction retain their attribution. Substantial AI
assistance was used; finite replay is not a complete multiplication proof.
