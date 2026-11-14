# Scalar equality14 package

PROOF.md proves an all-field source-specific equality classification:
a one-direction scalar fitting attaining proper-cover saving14 has
exactly seven double-saving rows on one orthogonal seven-root support.
This strengthens the independently reviewed sharp14 theorem structurally,
without changing its numerical bound or claiming a new kappa.

The checker requires Python3 standard library only. From the repository
root after integration, pass the package's actual location as PACKAGE:

```sh
python "$PACKAGE/check.py" \
  --native research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz \
  --sharp14-cases research/moonshot-005-program/results/bit-scalar-proper-cover-fourteen/author/output/CASES.json.gz \
  --output "$PACKAGE/reproduced"
python -O "$PACKAGE/check.py" \
  --native research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz \
  --sharp14-cases research/moonshot-005-program/results/bit-scalar-proper-cover-fourteen/author/output/CASES.json.gz \
  --output "$PACKAGE/reproduced-optimized"
```

Expected status: PASS_SCALAR_EQUALITY14_SOURCE_PREMISES, with94 rank3
equality cases, nine orthogonal4 equality cases,103 new quadratic minors,
1121 full native D4 complements,30632 six-cliques with two mutually
orthogonal outside roots, and31472 links to inherited seven-root minors.
Normal and optimized RESULT.json and EVIDENCE.json.gz are byte-identical.

EVIDENCE.json.gz contains all new cases, selected exact minors and the
complete six-to-seven links. Nonzero modular determinants are exact
integer nonvanishing certificates, not numerical rank estimates.
The all-field theorem follows from the written proof and its named
inherited premises; finite source checks alone are not that theorem.

During author development, the initial boundary-control code incorrectly
assumed the selected sharp seven-set had a native eighth orthogonal root.
It does not. The control now independently uses the eight coordinate
roots. This affected only the control choice; the classification proof
and new finite source premises were unchanged. No failed run is labeled
a completed verification.

Independent mathematical review is separate. No physical history,
supplier, complete multiplication bound or foundational assumption is
claimed. Prepared for @CubeJerry with OpenAI assistance and predecessor
credit retained in PROOF.md and SOURCES.json.
