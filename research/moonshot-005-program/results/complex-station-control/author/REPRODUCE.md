# Reproduction

Use Python3 standard library only. The checker does not import a producer
engine or use numerical rank tolerances. `check_influence.py` independently
replays all400 input directions, checks legal source operations, constructs
the formal200-arrival Hub circuit, and propagates exact adjoints.

Set NATIVE to the pinned `research/shared-wire-split-composition/data/final.json.gz`,
PARENT to the pinned `complex-compensated-ferries/general/author/source-evidence/rail-consumer.json.gz`,
FOUR to the pinned `complex-compensated-ferries/four/author/output/rail-cross-four.json.gz`,
and FULL to pinned `research/shared-wire-split-composition/FULL-RESULT.json`.

```sh
python3 -I -B check_influence.py --native NATIVE --parent PARENT --output OUT/parent
python3 -I -B check_influence.py --native NATIVE --parent PARENT --four FOUR --output OUT/four
python3 -I -B price.py --full FULL --parent OUT/parent/RESULT.json --four OUT/four/RESULT.json --output OUT/PRICE.json
```

Expected checker status is `PASS_EXACT_ALL_TIME_D_STATION_B_INFLUENCE` with
protected counts74 and66, influence-chart counts131 and139, and field-state
checks4360 and4904. The price status is
`PASS_BOTH_ALL_FIXED_M_WHOLE_FIELD_RETURN_EXCLUSIONS`.

The source and price checks use explicit exceptions, so Python -O does not
remove their gates. Repeated execution by the author is not independent
mathematical verification. Root review remains pending.
