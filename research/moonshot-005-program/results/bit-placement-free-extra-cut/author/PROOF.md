# Relocating leaf ports cannot repair the single Extra6 source channel

**Status: proved source-dimension obstruction in the fixed information interface.**

The preceding thirteen-capacity theorem used current leaf placement. This result shows that its Extra6 bottleneck is more fundamental: no reassignment of the eight leaf ports can compress the current Extra6 source information into one whole record while completing all111 demands, if the higher/common histories and source-bank assignments stay fixed.

The argument is a universal source cut, not a failed finite search. In particular it excludes every one-, two-, or three-port reassignment in the declared source charts. It does not exclude new source coupling or a changed common code.

## Source and interface

Use the reviewed36 word SHA256 `af51d0d7c872dbf3fa3744b582769d4c7763e0747e57c74005d091d19b7da474`, native root source SHA256 `8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`, and the exact source-bank definitions of the leaf-capacity theorem. In packet order P0,…,P7 these are

    H0+span(g1), H0, H0, H1, H1, H1, E+span(g0), H0+span(g1).

Each packet source may encode arbitrary fixed-length data from its entire specified bank. Existing fixed historical observations and geometric raw locals remain available at their actual receiver facets. Completed raw points and newly decoded raw points may be announced globally for free. New coded common data, changed higher measurements, or new source directions are not included.

Unlike the earlier placement-specific theorem, grant **all seven non-P6 source banks globally**. Also grant the P6 transcript globally. These generous grants remove every leaf-visibility and source-chart placement restriction. A lower bound in this larger information model applies to every legal placement in the original one.

## Exact four-coordinate cut

Take

    J = {8,9,36,37}.

None is among the36 completed points. Every pair of these native roots has nonzero real dot product. Their Gram matrix is

    [[ 4, 2,-2,-2],
     [ 2, 4,-2,-2],
     [-2,-2, 4, 2],
     [-2,-2, 2, 4]].

Therefore no J coordinate is geometrically local to a receiver in J. Direct replay of all1,692 historical states of every record shows that every fixed historical observation at any of these four receivers has zero projection to J. This includes original-Y X-parts, so arbitrary-Y nuisance has been generously removed.

Restrict inputs to J and fix all other X inputs and every original Y to zero. All seven non-P6 source banks together then have exactly one independent measurement:

    s = X8 + X9 + X37.

The reason is structural. H0 and H1 contain no coordinates of J. The only admitted cross-bank donor is the fixed g1, whose restriction is e8+e9+e37. Copies of that donor into P0 and P7 do not create a second direction. P6's Extra6 source itself has all four independent J coordinates.

If Z6 is the entire P6 transcript, every receiver's observation is now a function of (s,Z6). Every announced coordinate outside J is zero; every decoded-and-announced coordinate inside J is already a function of (s,Z6). Induction over arbitrary raw-point feedback shows that completing all four demands makes their entire independent input a function of (s,Z6).

Consequently

    dim(Z6) >= 3V.

For linear messages over every characteristic-two field, arbitrary V×V blocks included, this follows from rank: a map of rank at most V+dim(Z6) must recover a4V-dimensional input. For arbitrary exact deterministic fixed-length messages over finite characteristic-two fields, count inputs, or restrict to s=0. That kernel contains |F|^(3V) assignments and has the explicit independent directions

    e8+e37, e9+e37, e36.

Thus the entire P6 transcript requires at least3V field symbols. A single whole record has onlyV symbols and fails. Unlimited computation, free raw-point feedback, moving any of the ports, and even globally exposing every other bank cannot change this source-dimension deficit.

This is not a nonlinear theorem for unrestricted infinite alphabets or variable-length encodings without a worst-case symbol bound.

## Exact placement coverage

The actual immediately preceding source charts have these native leaf domains:

| Packet | Preceding chart | Chart rank | Number of native candidate leaves |
| --- | --- | ---: | ---: |
|P0|J16|4|7|
|P1|J23|4|7|
|P2|J22|4|7|
|P3|M1|5|20|
|P4|M1|5|20|
|P5|M1|5|20|
|P6|Extra6|6|36|
|P7|D3_21|6|28|

The checker computes every inclusion from exact rational charts. Allowing arbitrary choices in those domains gives137 configurations changing exactly one port,7,812 changing exactly two, and241,054 changing exactly three, plus the unchanged configuration. The universal argument covers all249,004 configurations at once. The counts are bookkeeping, not evidence for an asymptotic impossibility theorem. Port choices outside these domains are also excluded by the same information cut unless they change the source/history interface.

No old-decoder protection or movement costs are suppressed into a positive construction: none of these assignments yields a one-record source in the relaxed model, so there is no candidate physical invoice to admit. If source/history premises change, every raw terminal, old reader, helper, movement, restoration and retirement must be revisited.

## Precise necessary escape and a source-span repair

If P6 is to remain one whole record, other information available to this four-demand cut must contribute rank at least3V. The current other-bank contribution has rankV. Therefore at least2V additional independent J-information is needed outside that one P6 record, unless the receiver-side or output interface changes.

This requirement is tight as a *global source-span statement*. For example, supply new outside measurements X8 and X36, retain the existing s, and choose the one P6 message X9. Then all four J coordinates are recovered, with

    X37 = s + X8 + X9.

Removing either new outside direction restores a rank deficit. This four-equation repair is not a physical all111 decoder and does not assert that the needed values are placed at the receivers.

A relevant actual geometric opportunity survives: Extra6 has rank6 and contains M1 of rank5. Hence an owned whole-record transfer from Extra6 to M1 is a single rank-one downward MOVE. The four originals X8,X9,X36,X37 all pass Extra6 as still-raw records before the M1 principals arrive. Two properly captured independent E directions can therefore be investigated as real cross-bank imports. Their source custody, timing, readers, preservation of old decoders, complete costs and eventual endpoint use must be proved; none follows merely from the rank calculation.

## Reproduction and next construction

```bash
python check.py --repo /path/to/programme \
  --word /path/to/reprogram36/WORD.json \
  --engine /path/to/leaf-capacity-gate/check.py \
  --out /tmp/placement-independent-extra-cut.json
```

Next: build source-valid Extra6-to-M1 transfers or another mechanism supplying two independent E directions outside P6, then solve simultaneous source/receiver fitting with actual chronological delivery. A new common code involving those quotient directions can also escape. Further blind relocation of1–3 leaf ports under unchanged banks cannot remove this bottleneck.

Developed by `/root/delivery_audit` for @CubeJerry's persistent programme with substantial OpenAI assistance. Native geometry, source histories, prior bank definitions and the actual36 construction retain predecessor attribution. All full supplier, recursive and foundational obligations remain; no new κ is claimed.
