# Exact access gate for the frozen full-W source

**Proved application of existing normalization, with new exact source
certificates. No new general scattering theorem, supplier or kappa.**

The source audited in `FULL-HISTORY-REVIEW.md` has terminal packet code T of
rank eight and full chronological history G of rank 29 containing W15.
The current word delivers no Y outputs.

## The existing normalization applies

The admitted `results/bit-source-packet-scattering/author/PROOF.md`, Theorem 1,
already normalizes invertible-through cells to terminal modes plus local
original inputs. Here every proper through-block is I: packets only add
stationary pure-X cache values supported inside their current chart.

If a packet is observed at C contained in receiver facet F_i, every later
chart is contained in C and every later increment is F_i-local. The observed
value therefore differs from its terminal value only by local data. This
telescoping calculation is a special case of the cited prior theorem, not a
new general result. Arbitrary new nonlocal Y feedback would change its scope.

Grant every receiver all actual packet observations at every chart in its
downset, ignoring chronology, and all original inputs local to F_i, ignoring
acquisition costs. The checker verifies, for each of all 111 receivers,
equality of the full projected observation space and the projected T space.
Exactly receivers 17 and 59 fit; 109 fail. Every failure has an exact binary
dual input supported outside F_i, annihilating all accessible observations
and having own coordinate one. Multiplying that counterinput by any nonzero
v in K^V proves failure over every characteristic-two field and positive
width. Noncommuting decoder blocks and nonlinear processing cannot recover
a value that differs on two inputs with identical observations.

The two feasible fitting equations do not complete two outputs: the frozen
word still delivers zero. The admitted all-width minrank9V theorem likewise
precludes completing eight packets merely by changing seeds or stops while
remaining in this terminal-normalization class. Singular through-cells,
Y-coupled nonlocal histories or paid extra moving records are possible exits.

## At most three frozen cache rows cannot repair it

There are 27 nonpoint caches, of which 22 have nonzero values. Grant any
selected subset globally to every receiver, along with T and all local
original inputs. Exact exhaustive binary linear algebra gives:

| Selected rows | Subsets checked | Maximum fitted receivers |
|---|---:|---:|
| 1 | 22 | 5 |
| 2 | 231 | 9 |
| 3 | 1540 | 12 |

Every tested subset has a checked dual counterinput for at least one failed
receiver. A best pair is {DC2_3,DC3_2}; best triples are
{DC2_2,DC2_3,DC3_2} and {DC2_3,DC3_2,DC3_3}. Exact maxima and receiver sets are
stored in `FULL-ACCESS-RESULT.json`. The finite exhaustive result scalar
extends to all K,V through the same dual witnesses. It is not an asymptotic
inference from a failed heuristic search.

The scope permits arbitrary recombination of the selected rows. It does not
exclude new linear combinations formed from more cache rows, source changes,
new meetings or packet/Y exchanges. In particular, this is not a bound on
three arbitrary vectors chosen from the full cache span.

As a positive control, all 22 values plus T have rank 29 and fit every
receiver. The source has sufficient algebraic information; its availability
in receiver downsets is the obstruction. Any actual descent of selected
fixed values is weaker than the global availability granted by this test.

## Reproduction and next obligation

The independent checker replays the actual word, proves locality of every
stationary cache at its chart, checks all packet-history congruences and
constructs receiver/subset dual witnesses. It imports only Worker C's own
utilities. The manifest pins the old scattering proof and admission as
dependencies and preserves their authors' credit.

```sh
python research/moonshot-005-program/work-in-progress/2026-11-15-S014/worker-c/review-a/full_access_check.py --source research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json --word research/moonshot-005-program/work-in-progress/2026-11-15-S014/worker-a/full-history-output/WORD.json --output /tmp/full-access-independent.json
```

Expected status: `PASS_EXACT_FULL_HISTORY_ACCESS_GATE`.
The next construction must materialize a singular-through or Y-coupled
continuation, preserve arbitrary Y columns and the needed source information,
restore originals, deliver actual outputs and pay every new cost. Such a
continuation is outside this negative result. **No new kappa.**
