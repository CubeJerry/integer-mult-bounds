# Decoder calendar capacity

No new kappa. The independent input, fixed-calendar, arbitrary linear-code
theorem is in PROOF.md; weaker difference-demand interfaces and their exact
scope are in WEAKER-INTERFACES.md. These restrict intermediate representations,
not the H4 endpoint in general.

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/decoder-calendar-capacity/scan.py
python3 -O -B research/moonshot-005-program/results/decoder-calendar-capacity/scan.py
python3 -B research/moonshot-005-program/results/decoder-calendar-capacity/weaker_demands.py
python3 -O -B research/moonshot-005-program/results/decoder-calendar-capacity/weaker_demands.py
```

Both commands are read-only unless --output is supplied. They authenticate the
native bytes and print summaries. RESULT.json records all 6310 MOVE innovations
and chart witnesses; WEAKER-RESULT.json records the 22098 weaker demands. The
optimized receipts are byte-identical to normal receipts. JSON is compactly
serialized to avoid duplicating formatting overhead.

The independent modular checker and conceptual review in review/ do not import
the author's rank implementation. They certify lower bounds over Q by nonzero
minors modulo a checked prime and compare records and chart maxima.

Source drift, bad ownership, invalid scalar/lifecycle contracts and inconsistent
counts reject. Controls preserve prefetch credits, refuse late payment of
earlier deficits and give zero when all moves carry two fields or only one copy
is requested. Endpoint-only zero is expressly not feasibility.

The continuation is a source/read-deadline code that may defer both main and
unused common-helper states, with full endpoint restoration and actual
transport, memory, scalar, precision and compiler costs.

All five foundational assumptions remain. Prepared for @CubeJerry with
substantial OpenAI assistance and selected source/programme authors' credit.
