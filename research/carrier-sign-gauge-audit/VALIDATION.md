# Validation record

Host: Linux x86-64, CPython 3.12.14, standard library only. Scientific base:
`3f0152a32eeebac0df11946dbd50cabe5a7f7839`. Subject PR6166:
`f7d6431080b375914216d76a8a6426f50c524471`. Exact input/source pins are in
SOURCES.json and UPSTREAM.json. The deterministic evidence is RESULT.json.

## Executed checks

- `python3.12 -I -B research/carrier-sign-gauge-audit/verify.py --write-result`
  completed the full domain and generated the receipt. A complete-domain run
  took 47.251 seconds before the final input-geometry guard and ordinal-label
  clarification. This is not a speedup claim.
- `python3.12 -u -B scripts/research_package.py --package research/carrier-sign-gauge-audit`
  passed the final source in both warning-strict normal and optimized Python,
  with `PASS_REGISTERED_RESEARCH_PACKAGE` and two identical
  `PASS_CARRIER_SIGN_GAUGE_AUDIT` outputs. Both runs checked the complete receipt
  and all five semantic controls, rather than regenerating an expected answer.
- The registered metadata/source-pin check passed separately.
- `python3.12 -B scripts/check_research_commit.py --package research/carrier-sign-gauge-audit --check-source-history --check-modes`
  passed for all 13 package/input files, with the base commit available in
  publication ancestry. The pending PR's source is retained locally, not a
  hidden Git-history dependency.
- The official `export_research_package.py export` and `check` commands passed.
  The extracted export was run in normal and optimized Python with Git absent
  from PATH and files/directories given read-only permissions. Both passed in
  46.079 / 46.019 seconds. All 14 exported files, including the export receipt,
  retained their hashes and the inventory had no extra files. Subsequent
  changes only recorded validation/freshness and removed a trailing blank line
  in README; the scientific source, source inputs and result receipt were fixed.
- Two extra temporary-copy integrity controls rejected a changed retained
  `inputs/code8.py` (`upstream SHA256`) and a flipped byte in the compressed
  selected word (`word SHA256`, under `-O`). Each exited 1 before scientific
  work. The actual frozen inputs were never modified.
- `python3 -B scripts/research_selected_baseline.py` passed with
  `PASS_RESEARCH_BASELINE_BINDINGS_ONLY` after materializing its declared
  sparse inputs. This is source-binding orientation, not the selected cold
  scientific replay.

The first redirected registered-run log was empty, so it is not used as
evidence. The registered run was repeated with directly captured terminal
output; only that visible successful run is claimed above.

## Scope

This audit checks sign orbits, merging, the stated stabilizer and equation
covariance. It does not execute PR6166's elimination or certificate replay,
nor certify its complete uniqueness theorem, support weights or descent bound.
It is not a formal proof-kernel verification. Full selected cold replay,
native/caller/compiler/outer checks, hosted CI and independent human review
were not run. No supplier, selected record or kappa changes.

## Freshness and coordination

Canonical main was fetched at startup and again at
`2026-10-29T03:56:00.428237+00:00`: the base, priority revision 8, selected
record and relevant guidance/ledger were unchanged. The frozen PR6166 head was
also unchanged. The updated PR6168 head is a separate projector investigation,
not a dependency of this audit. The latest visible handoff on Discussion 1166
was PR6167's cache-chronology request; it does not overlap this sign-pruning
obligation. Details and coverage limits are in CLAIM.md and TASK.json.

The final publication preflight and full-tree remote comparison are separate
from mathematical acceptance. The pull-request handoff records the published
commit and its tested tree identity; no upstream PR is submitted by this session.
