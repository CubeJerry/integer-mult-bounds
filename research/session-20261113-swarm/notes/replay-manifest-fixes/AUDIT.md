# Archive replay-manifest naming audit

## Finding

The generic research-package planner scans only immediate
`research/<slug>/VERIFY.json` paths. In
[`repo/scripts/research_package.py`](../../repo/scripts/research_package.py),
`planning_manifests()` filters tracked files by that exact suffix and scans
the same filename for immediate children of `research/` (lines 848–862).
The strict validator then requires all three of `TASK.json`, `SOURCES.json`,
and `VERIFY.json` (lines 390–399), followed by the registered schema fields
and command-object checks (lines 431–480).

The four source snapshots are currently under `publication/...`, outside the
parser's `repo/research/` root, so the generic planner does not select those
paths directly. A temporary Git fixture placed each unchanged archive
manifest at `research/<slug>/VERIFY.json`: the planner selected all four, and
`--check-only` rejected every one immediately because its archive layout has
no `TASK.json`. Their custom verification records also use a different schema
(for example `standalone_only` and command arrays), so adding the missing task
metadata would not make these archive records valid registered manifests.

## Isolated maintenance copies

The four full copies are in sibling directories:

- `literal-selected-move-join/`
- `literal-once-rounded-selected-move/`
- `affine-period-outward-slack/`
- `sharp-finite-gaussian-outward-slack/`

Each copy renames only its top-level `VERIFY.json` to `REPRODUCTION.json`;
the renamed file is byte-identical to its source. The README now calls out
standalone direct replay, read-only defaults, and the lack of generic hook
registration. Relevant README links, `FREEZE.json` or
`PUBLICATION-MANIFEST.json` paths, and top-level `CHECKSUMS.sha256` entries
were updated. Scientific source, proof, result, certificate, and verifier
files were not edited.

Exact paths relative to each archive directory:

| Copy | Deleted | Added, same bytes | Other changed paths | Other files preserved byte-for-byte |
| --- | --- | --- | --- | ---: |
| `literal-selected-move-join` | `VERIFY.json` | `REPRODUCTION.json` | `README.md`, `FREEZE.json` | 51 |
| `literal-once-rounded-selected-move` | `VERIFY.json` | `REPRODUCTION.json` | `README.md`, `FREEZE.json`, `PUBLICATION-MANIFEST.json`, `CHECKSUMS.sha256` | 52 |
| `affine-period-outward-slack` | `VERIFY.json` | `REPRODUCTION.json` | `README.md`, `PUBLICATION-MANIFEST.json`, `CHECKSUMS.sha256` | 17 |
| `sharp-finite-gaussian-outward-slack` | `VERIFY.json` | `REPRODUCTION.json` | `README.md`, `PUBLICATION-MANIFEST.json`, `CHECKSUMS.sha256` | 42 |

`INTEGRITY-REPORT.json` lists every file hash that remained byte-identical,
the exact metadata files whose bytes changed, and the rename receipt. It also
records successful validation of each applicable checksum, freeze, and
publication inventory. The four retained-manifest SHA256 values are:

| Archive | `REPRODUCTION.json` SHA-256 |
| --- | --- |
| `literal-selected-move-join` | `50c71e702b569a3fcc7953c0f07e3c5bae8d4b3e0b566bf0ca21145d725b37b5` |
| `literal-once-rounded-selected-move` | `095d154e05db1600fab6654e9f47acaa9cabeef722670a122811bee89f976ed1` |
| `affine-period-outward-slack` | `c392c163eb22f23dc7085b8bc1e81343031cafa1329b610a77133282a0fd97b7` |
| `sharp-finite-gaussian-outward-slack` | `f1ea9f91bf0f6517b30e278e2ae32bb8b23d4a451901eaae5a0ed652d1d5689c` |

## Planner checks

Using the exact parser source in a temporary Git repository:

1. The four original custom `VERIFY.json` files were discovered and selected
   as `research/<slug>` replay packages.
2. Strict metadata validation failed all four on the missing `TASK.json`.
3. Repeating planning with the renamed `REPRODUCTION.json` copies selected
   no packages.
4. All copied top-level checksum files passed `sha256sum -c`; every row in
   applicable `FREEZE.json` and `PUBLICATION-MANIFEST.json` inventories
   matched its current path, byte count and digest (and Git blob ID where
   present).

The scientific replay commands were not rerun: this is a filename and
documentation maintenance copy, and the executable source and recorded
receipts remain byte-identical. Direct standalone replay instructions remain
available in each `REPRODUCTION.json` and README.
