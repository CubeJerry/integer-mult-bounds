# Exhaustive necessary screen for the two added endpoints

For the exact seven-deletion plan in the parent package, every successful .005
repair must use two grade-one messages between old physical banks. This exact
screen leaves **120 unordered endpoint pairs**. The list is in
`EXPECTED-SURVIVORS.json`; none is claimed to implement a repaired supplier.

The screen permits arbitrary surviving local linear recoding, histories, and
retiming. Its exclusions use only required source/target minors and the paid
communication graph. They do not freeze surviving message payloads.

## Exhaustion and rejection logic

The parent proof excludes new physical banks under this two-message budget.
The exact binary-span inventory then gives 4802 possible directed grade-one
routes between the 1102 old physical banks. Parallel additions are permitted.
Of these routes, 424 cross the new six-versus-four cut. Both new messages must
be among those 424. Requiring the other three verified initial minor cuts to
gain their missing capacity leaves 27002 unordered pairs, including possible
duplicate routes.

For each pair and each of the four exact predecessor minor certificates,
temporarily remove the certificate's boundary and the seven declared deletions.
Take the forward closure of its source charts after adding the proposed pair.
All selected input fields remain inside. The subset of the selected outputs
that remains outside has a nonzero diagonal minor of the corresponding size.
The checker compares that rank against the full surviving outgoing boundary.
All unblocked old edges are closed by construction, and the two new edges
are also closed. Formerly internal blocked edges are counted if they become
outgoing. These exact reclosure checks leave 180 pairs.

For those 180 pairs, a bounded integral flow calculation searches for more
separating cuts with the same source/target minors. A claimed rejection is
accepted only after a direct graph check establishes that every chosen source
chart is inside, every chosen terminal chart is outside, and the full old-plus-
new boundary has fewer messages than the exact minor rank. The flow solver's
optimality is not trusted. This supplies 60 more exact cut rejections, leaving
120 endpoint pairs.

| Stage | Count |
| --- | ---: |
| All directed grade-one old-bank routes | 4802 |
| Routes crossing the rank-six cut | 424 |
| Unordered pairs passing the four fixed cuts | 27002 |
| Pairs passing the exact reclosure cuts | 180 |
| Additional directly checked minor-cut exclusions | 60 |
| Remaining endpoint pairs | 120 |

Every rejected route pair has a whole-field rank obstruction: tensor its
nonzero diagonal minor with the identity on a field of width `V`, and compare
the required rank with the number of exported fields times `V`. Therefore
the exclusions apply at every positive finite width under the parent's scope.
The screen does not claim that these are all rank obstructions, nor that any
surviving pair has a causal implementation.

## Replay

```sh
python -I -B research/moonshot-005-program/results/complex-paid-export-s031-coupled-repair/endpoint-screen/check.py --repo . --out /tmp/s031-coupled-endpoint-screen
```

This reruns the parent source, cut, and price verifier, independently checks
the four source minors copied from the predecessor certificate, exhausts all
affordable old-bank endpoint pairs, and reconstructs all exclusions. It uses
only the Python standard library and exact integer/Boolean graph operations.
The 60 final cuts are retained as explicit chart sets and boundaries in
`output/CUT-REJECTIONS.json`. `output/RESULT.json` records the complete screen
and surviving list. Both are author evidence; independent admission is separate.

The cut data originates in `complex-paid-export-s031-repair`. Exploratory
mixed-integer and modular calculations are not used by this checker.

## Open next question

Supply a complete exact causal word for one surviving pair, or a further
obstruction valid under arbitrary internal linear recoding. A failed attempt
that keeps all surviving payloads fixed does not settle that obligation.
