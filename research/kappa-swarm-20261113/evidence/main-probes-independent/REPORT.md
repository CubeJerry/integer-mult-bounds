# Independent main-only destination-history review

## Result

All 33 candidate cuts named by A as earlier-B misses independently fail the 400-main projection test. For each candidate event, this package contains an explicit integer input direction `t` supported only on the source-defined 400 main coordinates. Exact full-input row replay followed by projection gives zero dot product against every strictly earlier destination-history seed row and a nonzero dot product against the candidate target row. A separate direct scalar replay of the pinned word checks the zero/nonzero statements and coframed intermediate bank values without Gaussian elimination.

This is a scoped information obstruction for those 33 cuts. It does not evaluate the 14 cuts that pass A’s main projection, does not make a statement about all 1,501 columns, and does not establish an all-column source or supplier admission.

## Independent construction

- Pinned native word: SHA-256 `acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9` (`worker-a/inputs/pr7481-WORD.json.gz`).
- A was consulted only to select the 33 missed candidate event IDs; its row bases, targets, and the 14 passing cuts were not used.
- Reconstructed the main set from the pinned word as `live ∪ (live + 112) ∪ hosted.X2 ∪ hosted.Y2`: 400 coordinates. The sorted coordinate-set SHA-256 is `52270be5ea0af1c794b4c79db188eb0fbd0b921ae51298b7aa41b50ebd99e6aa`.
- Replayed every program row over all 1,501 original public input columns with exact `Fraction` arithmetic, through all 76,475 events; then projected each initial/arrival row to the 400 mains. The final chart/lifetime endpoint check passed.
- Canonicalized each frame independently with GF(2) row reduction. Maintained a dense exact-rational forward basis for earlier destination observations and solved the null equations by back-substitution. Each rational null vector was denominator-cleared and gcd-normalized to an integer vector.
- The earlier-history generators are initial public rows in the destination frame plus every strictly earlier MOVE arrival into that frame. INIT contributes zero; within-frame SCALE, ADD, and COPY produce linear combinations of these generators. Thus annihilating these seed rows annihilates every earlier scalar bank value obtainable from them.

## Explicit integer separators

Each `t` entry is `original-main-input-index:integer coefficient`; omitted coordinates have coefficient zero. The `target dot` is the exact rational value for the candidate target row. `past checks` counts initial-frame and earlier MOVE-arrival observations directly checked for that probe in the second replay.

| Candidate MOVE event | Earlier-history rank | Past checks | Integer `t` (index:coefficient) | Target dot |
|---:|---:|---:|---|---:|
| 30529 | 8 | 25 | `4:1` | `-1` |
| 30537 | 4 | 4 | `4:1` | `-1` |
| 30551 | 2 | 2 | `4:1` | `1/4` |
| 32939 | 7 | 11 | `2:1` | `1` |
| 33125 | 5 | 7 | `2:1` | `-1/2` |
| 33133 | 5 | 8 | `2:1` | `1` |
| 33140 | 3 | 3 | `2:1` | `-1/4` |
| 33142 | 1 | 17 | `2:1` | `-1/4` |
| 33149 | 3 | 4 | `2:1` | `-1/4` |
| 34524 | 7 | 12 | `2:1` | `1` |
| 34528 | 4 | 4 | `2:1` | `1` |
| 35443 | 3 | 3 | `2:1` | `1/4` |
| 36324 | 8 | 18 | `2:1` | `-1` |
| 36328 | 4 | 4 | `1:1` | `-1` |
| 36336 | 1 | 2 | `1:1` | `-1/4` |
| 39553 | 8 | 13 | `8:1` | `-1/16` |
| 39581 | 8 | 12 | `1:1` | `-1/8` |
| 39727 | 2 | 6 | `5:1` | `-1/2` |
| 39785 | 4 | 4 | `5:5, 8:-4, 9:-4, 10:-4, 164:2` | `-1` |
| 39814 | 2 | 2 | `5:1` | `1/4` |
| 39820 | 9 | 15 | `0:1` | `1/4` |
| 39853 | 4 | 5 | `0:1` | `1/4` |
| 40538 | 1 | 1 | `1:1, 142:1` | `1/2` |
| 40556 | 8 | 9 | `1:1` | `1/2` |
| 40563 | 4 | 18 | `1:1` | `1/4` |
| 40567 | 9 | 12 | `1:1` | `1/4` |
| 41491 | 7 | 13 | `15:1` | `5/16` |
| 42005 | 5 | 22 | `129:1, 131:-1` | `-1` |
| 42477 | 4 | 21 | `2:1` | `1/4` |
| 42482 | 6 | 6 | `2:1` | `1/4` |
| 44244 | 3 | 3 | `4:7, 129:-2` | `1` |
| 44251 | 4 | 4 | `899:1` | `2` |
| 45638 | 7 | 7 | `0:1` | `-1/4` |

All listed input indices are members of the independently reconstructed 400-main set. The target dots are nonzero. For every preceding destination seed observation, the direct replay reports exact zero under the corresponding `t` assignment. The replay also made 2,604 exact checks of values participating in coframed operations in relevant destination banks, confirming that intermediate ADD/COPY/SCALE/CLEAR states remain zero.

## Helper-only restrictions and cache consequence

Let `c` be the candidate target row over the 400 mains and let the rows of `H` be all strict-earlier destination-history generators after main projection. The certificate gives `H t = 0` and `c t ≠ 0`. Assign every helper input zero and every main input `X_j = t_j z`. Any homogeneous rule that constrains helper inputs alone and is independent of the mains accepts the helper assignment zero. Under the stated input-domain qualification, all earlier B observations are zero for every `z`, while the target is `(c t) z` and varies with `z`. Therefore no deterministic cache whose only input-dependent information is those prior B observations can recover the target for these 33 cuts; nonlinear post-processing cannot distinguish two `z` values from identical zero histories.

Qualification: this is an exact-rational latent-row argument. The permitted input domain must contain the zero assignment and the integer-multiple direction `X_j=t_j z` for a distinguishing legal `z`; the integer coefficients preserve any additive input lattice that admits those values. The result does not cover restrictions coupling main variables, domains excluding the separating direction, cross-chart reads/imports, extra side information, changed histories, or altered source semantics. It is not a full physical implementation or full-source admission result.

## Replay and controls

- `derive.py` independently generated the 33 vectors from the exact word. Normal run and `python -O` run generated byte-identical `PROBES.json` (SHA-256 is pinned in `SOURCES.json`).
- `verify_probes.py` assigned all 33 directions simultaneously as 33 exact scalar probes, executed all native instructions, and checked each strict-earlier observation, each participating value at coframed bank operations, and each target directly. It performed no Gaussian elimination.
- Normal and optimized direct-replay runs passed with identical `VALIDATION.json` bytes. The executed zero-vector mutant failed the required nonzero-target check for all 33 probes; the off-by-one mutant that treats the candidate’s own arrival as historical failed the required zero-history check for all 33.
- Counts: 61 initial rows checked in relevant destination frames, 2,604 direct coframed bank-value checks, 76,475 program events replayed, and 33 nonzero targets checked. Per-probe observation counts are listed above.

## Artifacts

- `derive.py`: full native row replay, 400-main projection, exact basis/backsolve, integer certificate generation.
- `PROBES.json`: explicit separator vectors and per-cut exact ranks/dots.
- `verify_probes.py`: direct scalar replay and executed negative controls.
- `VALIDATION.json`: replay receipt.
- `SOURCES.json`: source and artifact byte pins.
