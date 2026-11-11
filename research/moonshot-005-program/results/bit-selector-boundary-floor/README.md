# Optimal endpoint repair in the selected BIT shared-core model

No new κ. The selected selector lift loses independent low-side source rank.
Any repair using same-chart scalar linear operations, zero/independent dirty
scratch and charged single-field nested MOVEs must pay at least **111(m−1)**
in recursive moment. The previous explicit rank-one repair attains this floor.
Thus no cheaper endpoint repair in this class can make that fixed source and
caller clear κ=.005. The statement is quantified over every m>=2 and every
finite correction word; it is proved in [PROOF.md](PROOF.md).

The q-core version needs at least 111(m−q) repair when its entry cut rank is
at most 111q. Its unchanged full caller has strictly negative target moment
for every even m>=2, 1<=q<=m. That rank premise is explicit and does not bind
every possible temporal shared-core construction.

The source chronology has a second precise property: every X main is always
in a strictly higher-dimensional frame than every Y main. This covers all
34,138 cuts by checking all 755 main-frame configurations. Direct X/Y cochart
correction ADDs therefore have no legal insertion point on this frozen path.

The programme's next construction must change causal delivery before the
cut rank is lost, or change the invoice/target/primitive interface. Core-mediated
temporal switches remain open. All five global assumptions remain.

## Reproduction

From repository root, with this directory substituted for PACKAGE:

```sh
python3 -I -B PACKAGE/verify.py \
  --word research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz \
  --caller research/paired-query-only-bit/data/query_only_6980.json \
  --expected PACKAGE/RESULT.json
```

Expected marker: `PASS_SELECTOR_BOUNDARY_REPAIR_FLOOR`. Add `-O` for the
second registered check. The check writes no files and requires only Python's
standard library. [VERIFY.json](VERIFY.json) supplies portable registered
commands; [SOURCES.json](SOURCES.json) pins canonical evidence and the selector
predecessor. Inputs live in canonical upstream and are not repackaged here.

The finite checks corroborate the written proof and bind its premise to the
actual source. They do not prove universal physical Gaussian, tape, ownership,
compiler or analytic contracts. See [VALIDATION.md](VALIDATION.md) for coverage.

Prepared for @CubeJerry with substantial OpenAI Codex assistance. Classical
linear-rank arguments and all source/predecessor credit are retained. No
independent human or formal-kernel acceptance is claimed.
