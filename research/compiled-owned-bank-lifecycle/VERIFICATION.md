# Executed verification

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
Executed on 2026-11-09 with Python3.12.14, standard library only.

The following read-only commands completed successfully against the same
scientific receipt:

```sh
python -B research/compiled-owned-bank-lifecycle/verify.py
python -O -B research/compiled-owned-bank-lifecycle/verify.py
GIT_NO_LAZY_FETCH=1 python -B scripts/research_package.py --package research/compiled-owned-bank-lifecycle --check-only
```

Both scientific runs printed
`PASS_SOURCE_BOUND_PHYSICAL_LIFECYCLE`, with 642,410 source events, 2,118
current private lifetimes, 5 physical fixtures and 16 adverse controls. Their
canonical scientific-result SHA256 was
`1d16e1c0704785a2f6d6b40a3134163021345ebcc9cc56eb8747e1a8c08eea55`.
The package hook printed `PASS_PACKAGE_METADATA_AND_PINS`; that is a metadata
and source-integrity check, not mathematical acceptance. Initially missing
canonical Git blobs were inserted centrally only after tree-ID, SHA256 and
Git-blob verification; no source file changed to make the hook pass.

## Source-complete compiler fixtures

| Rank | Productive width | Private names | Emitted events | Private-field borrow occurrences | Maximum nested scope depth |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 2 | 1 | 37 | 0 | 3 |
| 15 | 10 | 14 | 472 | 4 | 5 |
| 20 | 200 | 377 | 12,571 | 112 | 6 |
| 25, product/completion/splitting | 4 | 5 | 271 | 0 | 3 |

The 4 and 112 private borrow occurrences use 2 and 56 distinct actual private
fields. Each instance includes source complements and deepest exits; every
elementary axis has an explicit entry and inverse return. The product fixture
actually completes a small target and splits a paid job into nonleading pieces.

## Literal physical fixtures

Every case runs twice on the same fixed physical tapes. Written backing and
visited backing include retained history; the verifier predicts every tape's
capacity before execution and checks reuse and protected prefixes afterward.

| Program | Ordinary fixture depth | Physical actions, both runs | Dirty CLEARs | Fixed tapes | Final backing including visited cells |
| --- | ---: | ---: | ---: | ---: | ---: |
| Rank5 | 2 | 902,107 | 172 | 8 | 1,412 |
| Rank15 | 1 | 13,029,266 | 3,976 | 29 | 20,780 |
| Rank20 | 0 | 2,120,982 | 1,508 | 582 | 180,484 |
| Rank25 product/pass | 1 | 3,195,497 | 1,060 | 14 | 2,681 |
| Entire current raw caller | 0 | 22,625,896 | 4,236 | 14,075 | 703,510 |

The row-depth predicate and distinguishing native bit writes are structural
fixtures, not the selected numerical rank cutoff or Gaussian maps. A separate
value-level oracle predicts all productive outputs. These checks establish
specific execution evidence for the written universal refinement proof.

Nine complete call-boundary tests recover the exact action formula at ancestor
prefix lengths 0,17,257. Seventy legal signed additions, twelve dirty INIT
formats and two overflow cases exercise the literal arithmetic routines.
Six complete controller runs branch on a runtime raw binary descriptor, preserve
its bytes/head and retire dirty native scratch. The raw context separately
rejects writing, origin crossing and frontier crossing.

The 16 primary adverse controls cover current source misuse, static borrowing,
physical output loss, residual-dropping COPY, numerical-zero versus physical
erasure, logical-blank truncation and source-byte drift. Their exact diagnostics
are in RESULT.json. Normal and optimized execution share those checks.

## Portable independent checks

The following four additional registered commands were actually executed and
passed after portability adaptation, with unchanged machine.py and source_ir.py:

```sh
python -B research/compiled-owned-bank-lifecycle/independent_source_trace.py
python -O -B research/compiled-owned-bank-lifecycle/independent_source_trace.py
python -B research/compiled-owned-bank-lifecycle/independent_primitives.py
python -O -B research/compiled-owned-bank-lifecycle/independent_primitives.py
```

The source reviewer independently annotates the authenticated source round loop,
then compares exact fragments, operands, whole-program entries/returns and
elementary leaves at ranks2,3,4,6,9,12. Both modes print
`PASS_INDEPENDENT_LITERAL_SOURCE_CHRONOLOGY`, including rank12's 5,138 trace
events, 204 private borrow occurrences and up to six deepest batches per round.
Paired wrong-complement offsets and an omitted scalar service are rejected.
Only the checker's repository ROOT expression changed for portability.

The root reviewer's separate sparse hardware and signed-word oracle checks
4,095 legal pairs and 1,365 overflows, twelve canonical zero/retirement formats,
seven scan bills, and coded-blank/origin behavior. Both modes print
`PASS_ROOT_LIFECYCLE_PRIMITIVE_REVIEW`. Its portable adaptation changes only
the source path and loading of captured bytes. Neither reviewer imports this
package's hardware, fixture encoder or expected-value functions.

The reviewer methods and original snapshot hashes are retained in the two
INDEPENDENT review reports. The one proof clarification concerns the pending
set and synchronous final-batch return; it changes no machine or source-lowering
code. The original full fixture receipt remains valid and unchanged. A final
metadata/pins check covers the extended six-command manifest with total declared
timeout1040 seconds. These are scoped independent AI checks, not human or formal
theorem approval.
