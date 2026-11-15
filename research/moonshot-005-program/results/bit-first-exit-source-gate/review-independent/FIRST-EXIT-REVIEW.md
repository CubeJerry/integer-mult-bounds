# Independent first-exit theorem and orientation review

**PASS for the specified original-only preprocessing model. No universal
singular-code or multiplication impossibility is claimed.**

Worker A identified the native singleton-source obstruction and all 64
complement choices. Worker C independently derived the first-exit invariant
and rebuilt the finite source test without importing A's code or certificate.

## 1. General theorem

Let original moving records X_j begin on distinct real lines L_j. They may
move only to containing charts. All auxiliary records are initialized with
zero dependence on the original X variables and remain stationary. Arbitrary
same-chart linear arithmetic, including arbitrary reversible recoding of all
original X values, is allowed. There are no additional moving copies,
descending records or moving original Y relays in this preprocessing stage.
Track physical record trajectories through any whole-role relabelings.

Fix an original index j and a finite set of required acquisition charts
`F_1,...,F_s`, s>=2. A specified value at each F_a must have a nonzero
coefficient on x_j. Let

`I = intersection_a F_a`.

Assume I is a strict subchart of every F_a, L_j is contained in I, and **no
other original starting line** is contained in I. The strict-subchart condition
holds for a family of distinct facets; it excludes a nested chain whose first
acquisition could already occur at I. Then the required values cannot all be
acquired in this model.
The claim holds over every field and at every positive block width, with
arbitrary block linear coefficients. It does not require the original records
to remain unchanged during preprocessing.

### Proof

Set every independent original input other than x_j to zero and follow
dependence on x_j. An ascending original whose starting line is not in I can
never enter a chart contained in I. Consequently, among moving records, only
the physical original X_j can ever visit such a chart. Stationary caches
created there can therefore transfer x_j dependence only to X_j itself.

Until X_j first moves to a chart C not contained in I, every x_j-dependent
record is either X_j or a stationary cache at a chart contained in I. No other
moving original has acquired that dependence. If X_j never exits I, no target
chart outside I acquires x_j, so completion fails.

At the first exit choose an a for which `C` is not contained in F_a. From then
on X_j cannot return to any chart contained in F_a: all its moves are upward.
Every later original or stationary cache that first acquires x_j dependence
from this external influence does so at a chart outside F_a. An ascending
original so influenced also cannot enter F_a's downset.

The earlier x_j-dependent stationary caches inside I are the only possible
exception, but they are inert with respect to other originals: no other
original can enter any of their charts, and X_j can no longer return. Thus
none can carry dependence to the target at F_a. Before the first exit the
target at F_a had no x_j dependence; afterward no active channel can supply it.
Its required nonzero coefficient is impossible. QED.

The proof does not identify support containment with physical access. A cache
at a smaller chart inside F_a is not a cache at F_a and cannot move there in
the stated model. This is exactly why previously deposited caches in I do not
repair the lost branch.

## 2. Exact application to the fixed seven acquisitions

The six native D8 normals are `(1,3,5,10,30,61)`. Each has its full-geometry
orthogonal partner with binary coordinate `r+s`, s=38. Replacing a normal by
its partner complements the half-spinor mode:

`hK_(r+s) = h + hK_r`.

There are 64 such orientation choices. The seventh acquisition is the fixed
proper mode K_b at the omitted normal

`b=(0,0,1,1,0,0,1,-1)`.

The independent checker reconstructs the full 120 roots from the pinned native
source, obtains partners from its independently recovered binary coordinates,
and calculates every support by exact real dot products. For every orientation
and native source j, it gathers the facets whose requested modes contain x_j
and checks all 111 original lines against their intersection. It records a
singleton witness exactly when the intersection contains only L_j.

For the unflipped six normals, x_6 is requested at all six facets and their
common chart contains only its source line. Of the 64 six-mode orientations,
59 have a singleton witness. The five exceptions are

`26,28,41,47,53`.

Thus a statement that all 64 *six*-mode orientations fail this test would be
false. The exception set is a useful negative control and does not certify a
source construction for those orientations.

Adding the seventh fixed K_b acquisition yields a singleton witness for
**every** orientation. The number of witnesses per orientation has histogram

| Witnesses | Orientations |
|---:|---:|
| 1 | 28 |
| 2 | 4 |
| 3 | 13 |
| 4 | 19 |

The checker also independently verifies that the same eight published seeds
plus each oriented seven-mode collection span the full rank-15 W code.
The obstruction therefore concerns actual acquisition, not a loss of the
desired algebraic basis under a complement change.

By the general theorem, this fixed seven-acquisition setup cannot be completed
entirely in the original-X-only monotone preprocessing stage, even with
arbitrary reversible recoding and arbitrarily many stationary caches.

## 3. Boundaries and constructive meaning

The theorem does not cover an interleaved source with descending packets,
additional moving copies, or moving original Y receivers. Such a record can
enter the common chart independently or carry an earlier saved value out of
it, breaking the singleton-original premise. The theorem also does not cover
a different set of proper W modes or different designated acquisition charts.
The code has 69 proper words, and the fixed seven forms are only one target
basis. A new basis must receive its own source and chart analysis.

The two-facet masked construction passes this first-exit screen because its
common chart contains two additional donor originals. Its successful replay
does not imply that six or seven such constructions can be freely combined.
The new theorem identifies the point where that proposed combination fails
and makes interleaving, alternative carriers or a different basis a concrete
next obligation.

This result is compatible with the earlier W-localization theorem and with
the terminal-history counterexample. It is about the propagation of an input
through original-only preprocessing, not about a packet's terminal rank.
All movement, ownership, precision, compiler, uniform supplier and complete
recursive obligations remain. No new kappa.

## Reproduction and evidence

```sh
python research/moonshot-005-program/work-in-progress/2026-11-15-S014/worker-c/review-a/first_exit_check.py \
  --source research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json \
  --output research/moonshot-005-program/work-in-progress/2026-11-15-S014/worker-c/review-a/FIRST-EXIT-RESULT.json
```

Expected status `PASS_INDEPENDENT_SINGLETON_FIRST_EXIT_GEOMETRY`. The certificate
lists every orientation, all actual normals, every singleton witness, all
source incidences and the full rank-15 target test. The source recovery hash is
independently pinned; no fresh original-gzip replay is asserted by this check.

Credit Worker A for the source-specific obstruction/application, Worker C for
the independent invariant and exact orientation review, the singular-pivot
authors, the source/history/cut predecessors, and @CubeJerry. Substantial
OpenAI assistance; no independent human or formal-kernel review is asserted.
