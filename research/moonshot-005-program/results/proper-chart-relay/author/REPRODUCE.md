# Reproduction of the dyadic proper-chart relay

Python3, fractions and NumPy are required. The exact finite phase checker
uses the two pinned phase engines bundled under dependencies. Source files
remain external and SHA256-pinned; use the corresponding programme source
pins if their checkout location changes.

From this package directory, set task-specific paths:

```bash
relay_native=/path/to/shared-wire-split-composition/data/final.json.gz
relay_parent=/path/to/complex-compensated-ferries/general/author/source-evidence/rail-consumer.json.gz
relay_full=/path/to/shared-wire-split-composition/FULL-RESULT.json
```

For each size20 or44, run (replace44 with20 for the second word):

```bash
python3 build.py --native "$relay_native" --parent "$relay_parent" --engine dependencies/replay.py --size 44 --output /tmp/relay44-reproduced
python3 price.py --engine dependencies/interval.py --full "$relay_full" --receipt /tmp/relay44-reproduced/RESULT.json --output /tmp/relay44-reproduced/PRICE.json
python3 dependencies/check_phases.py --engines dependencies --word /tmp/relay44-reproduced/WORD.json.gz --parent "$relay_parent" --output /tmp/relay44-reproduced/PHASES.json
```

Expected source word SHA256s:

- 20: `0edf81ca8f6a7e60e5a01d4acdcaefdb74882180b8d12c408513bc91cd625b1c`.
- 44: `f3bd538e056c501c156bd06669656e7f7c2b46fe66d02f481c340dc78e170892`.

Both exact replay statuses are PASS_LITERAL_PROPER_CHART_DIRTY_RELAY. Both
retain all400 input directions and all400 native final chart identifiers,
restore exactly their named number of original D fields, use only dyadic
scalars, and never visit a hosted final facet with an owner. Five semantic
mutants must be rejected. All24 owned retirements are actually dirty.

Phase outputs contain358 introduced maps for20 and430 for44; the wrong phase
mutant must be rejected. The current reusable phase script has the historical
status name PASS_ALL_TRANSIENT_CODEC_INTRODUCED_CHART_MAPS; its input hash,
recipes and output paths bind it to the present relay word.

The complete movement caller limiting room must be46.50801152301453... for20
and -9.584891544029109... for44. The latter word is too expensive even before
its missing D/forward work. The former is only an incomplete partial source
with available movement allowance; it is not a completed conditional bound.
