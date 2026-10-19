# Local verification record

Executed 2026-10-19 on Linux with CPython 3.12.14, standard library only.
Research base: bb4bccbf42844d2801487450727c2f63e10d1d0f.
The exact PR4015 and PR4043 heads were rechecked unchanged before publication.
The current selected certificate was followed to its source construction and
review; `scripts/research_baseline.py` passed its bindings-only orientation
check. The selected result was not changed or independently reverified.

The completed registered command was:

```
python3.12 -B scripts/research_package.py --package research/qq16-streamed-exact-format
```

It passed all four registered commands, ending in
`PASS_REGISTERED_RESEARCH_PACKAGE research/qq16-streamed-exact-format outcome=completed`.

| Check | Actual result |
|---|---|
| Primary | Complete typed RESULT/TRACE equality; 3813 streamed events; grid `[9,3]` and width above P `[28,6]` in t=ceil(lambda/2)-1; 224 native calls |
| Separate coefficient/recurrence implementation | 65472 cut comparisons, depths 1,2,3,4,7,8,15,16; both signed kernels and all final fields |
| Bounded integer execution | 6 whole-word fixtures; 22848 completed cuts; 102144 pair calls; 1250 exhaustive pair cases; 13122 exhaustive quad cases; 12 arithmetic/ownership/support/cleanup controls |
| Same-input direct-lowering counts | Paired and sequential results agree at depths 1,2,3,4,7,8; every primitive counter matches LOWERING.json, including 9 versus 5 scalar cleanup writes |
| Export/failure controls | Git-free, permission-read-only export; primary/independent/numerical checks under normal and `-O` Python; unchanged file bytes; 13 corruption cases rejected in both modes; overwrite refused |
| Metadata/source binding | `--check-only` passed all declared canonical source and provenance pins |

The 13 export corruption cases cover retained word/proof, canonical word,
both manifests, Boolean/integer substitution, unexpected receipt fields,
an output polynomial, a cut grid, a truncated cut trace, the independent
checker's source binding, and an undercharged scalar-cleanup receipt.
The overwrite test is additional. The scalar controls include a numerator
overflow whose final values would fit, insufficient half/quarter grids,
missing dirty initialization/return, borrowed writes and overlapping axes.

One test-control mistake during development rewrote a grid to its existing
value, so it correctly failed to demonstrate rejection. It was corrected to
change the grid; the final registered suite above passed. An initially too-small
native-interior grid in the derivation was corrected after the separate
coefficient analysis exposed the even-depth prefix case. The released argument
retains that case explicitly. No failed scientific candidate is reported as an
impossibility theorem.

Finite source geometry and native inverse semantics remain inherited from the
pinned sources. The complete synthetic fixtures do not execute the real
73-axis cover. No Lean/proof-kernel check, actual tape implementation, full
selected-frontier cold replay, hosted CI, or independent human review is claimed.
Transport/tree checks and the published commit are recorded in the PR handoff;
they are separate from this scientific verification record. No new κ.
