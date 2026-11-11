# Finite selector-family appendix

**No new κ.** All 19,600 explicitly named time-varying load/read schemes in
[PROOF.md](PROOF.md) have exact modular counterexamples to their required
rational endpoints. A separate agent independently replayed the entire
domain, including dirty helper inputs and all eight coupled ports. This is
not a universal shared-core or K4 impossibility theorem. Optimistic tariff
claims are deliberately outside this appendix.

From the repository root, with Python3.11+ and a C++17 `g++` compiler:

```sh
python3 -I -B research/shared-core-target-obligations/variable-selectors/verify.py
```

An explicit source path is supported:

```sh
python3 -I -B research/shared-core-target-obligations/variable-selectors/verify.py --source /path/to/final.json.gz
```

Expected marker: `PASS_INDEPENDENT_FINITE_SELECTOR_FAMILY`. The exact
[RESULT.json](RESULT.json) is compared read-only. `--write` explicitly
regenerates that compact receipt. The pinned native is a live canonical
repository input; a sparse checkout must include it. The replay authenticates
the source, compiles both interpreters with `g++ -O3 -std=c++17 -Wall -Wextra`,
generates every witness, independently checks all witnesses and complete
mismatch counts, and requires an altered-witness negative control to fail.

Large input tables, witness tables and executable binaries live only in a
temporary directory and are removed when replay exits. No network access,
hidden cache, external numerical package or previously generated table is
required. This full workflow was actually completed after portable integration.

`source_prepare.py` and `source_screen.cpp` are the original agent's finite
screen, with only path handling adapted. `independent_prepare.py` and
`independent_verify.cpp` were separately written by the reviewing agent and
use different register layouts/instruction preparation. Source/receipt hashes,
prime/denominator checks and compiler inputs are recorded in the proof and
receipt. All five foundational assumptions remain unchanged. Prepared for
@CubeJerry with substantial OpenAI Codex assistance; predecessor credit and
limitations appear in the proof. Apache-2.0.
