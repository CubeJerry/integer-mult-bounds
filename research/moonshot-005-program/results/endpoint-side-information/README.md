# Endpoint side-information routing certificate

This source-bound package proves a **54-field broadcast lower bound** for the declared timed neutral-helper routing graph, and a **43-field bound** even after freely retiming clean-owned moves and reusing every original raw-main move. It also gives explicit failure witnesses for all 104 first-endpoint receivers of the eight-root-packet code in the timed graph. In the largest graph five demands are directly delivered; the other 99 still fail that code.

These are pure-payload routing bounds. They do not cover arbitrary common-dependent controllers, dirty-history decoding, or every native architecture. Common restoration and original reservation duties are granted rather than constructed. **No new kappa.** Read `PROOF.md` for the exact interface and invoice implication.

## Reproduce

Python3.10 or later and its standard library suffice. From this directory:

```bash
python reproduce.py --source /absolute/path/to/final.json.gz --output VERIFICATION.json
```

The wrapper checks the native SHA256, runs both verifiers normally and with `-O`, and compares decompressed output bytes to the frozen payload hashes. Each subprocess has a 60-second timeout. Direct commands are:

```bash
python verify.py --source /absolute/path/to/final.json.gz --output reproduced-base.json.gz
python expanded_graph.py --source /absolute/path/to/final.json.gz --base RESULT.json.gz --output reproduced-expanded.json.gz
```

JSON input/output is gzip-compressed when its path ends in `.gz`. Expected summaries are673 entries/54 acyclic vertices for both timed variants;745/54 with free-owned retiming; and1746/43 after main-route reuse. Every source path, adjoint rejection witness, null vector and topological certificate is included in the compressed JSON payloads.

## Files and provenance

- `verify.py`: exact rational suffix classification, timed graph, root-code checks and acyclic witnesses.
- `expanded_graph.py`: stronger retiming/reuse overgrants, with revalidation of the entire base edge/graph certificate.
- `RESULT.json.gz`, `EXPANDED.json.gz`: frozen detailed certificates; their decompressed payload hashes appear in `SOURCES.json`.
- `reproduce.py`, `VERIFICATION.json`: bounded normal/optimized reproduction.
- `PROOF.md`: universal linear argument, source implications, limitations and credit.

Pinned native source: canonical `e54523517d0f03e58352e647c403a5af3e525a57`, `research/shared-wire-split-composition/data/final.json.gz`. Programme baseline: `be00a963d4a8c96681a9f6df691a694f1b4fc853`. See `SOURCES.json` for immutable identities. Independent review belongs beside this package when integrated; rerunning the author's checker is not independent verification.

Prepared for @CubeJerry with OpenAI assistance, preserving the selected source's authors and the permanent programme's predecessor credit. The E8 root-code mechanism and acyclic broadcast lemma are background; the contribution here is their exact source-specific routing and budget analysis.

The expanded screen diagnostic `known_odd_pairs` lists only receivers without direct own-demand delivery; the complete graph matrix is authoritative for all pairs.
