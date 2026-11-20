# Five surviving complex messages cannot be repaired only at the boundary

This is a scoped negative result for the exact rational #7830 native word,
with the genuine paid fifth-channel #7833 compensation applied. It follows
the S031 saturated-cut package, which left five high-grade occurrences
unexcluded by its cut argument:

`86, 97232, 97241, 97323, 99064`.

**Result.** Freeze every other internal form and route. At each of these five
messages, apply any linear operator on the complete field carried by the
message. Allow arbitrary independent bijections, even nonlinear ones, within
every original physical input bank and every original physical output bank.
The original complete target can be recovered in this model **only when all
five message operators are the identity**. This holds at every positive
finite field width over any characteristic-zero field.

The calculation is exact rational algebra. The two essential identities are

\[
H=0,\qquad P E^{-1}B=\operatorname{diag}(1,0,0,0,0).
\]

Here `E` is the complete invertible 1289-field target, `P` contains the five
original message payloads, `B` propagates independent additive errors at those
messages to every target field, and `H` is their internal interaction matrix.
Five originally zero inverse-bank blocks isolate the five operator changes.
The proof makes no generic-position or numerical rank assumption.

| Changed message | Input axis / original chart | Terminal slot / original chart | Isolating coefficient |
| --- | --- | --- | --- |
| 86 | 17 / 16 | 154899 / 145 | −63/128 |
| 97232 | 17 / 16 | 154918 / 162 | 1/2 |
| 97241 | 19 / 18 | 154897 / 143 | −1/2 |
| 97323 | 17 / 16 | 155544 / 134 | 1 |
| 99064 | 19 / 18 | 154918 / 162 | 1/2 |

Deleting message 86 makes the endpoint noninjective. Deleting any nonempty
subset of the other four preserves global invertibility but creates an
inverse dependency between banks that the original target did not have.
Independent boundary-bank bijections preserve those dependency relations.

## Scope and its relevance

The theorem rules out deleting/rescaling these messages and then absorbing
the resulting target into separate source-bank and terminal-bank coordinate
changes. It permits arbitrary mixing among fields and coordinates *within*
each boundary bank. Equal-span chart aliases are merged before defining banks.

It does not allow changing the other internal forms, replacing a message by
an arbitrary new combination of several locally stored messages, adding
communication, merging distinct banks, or revising the caller's target roles.
In particular, it does not settle the promising paid grade-one 127→239 route
with coupled internal recoding; such a route needs its own graph analysis.
Nor does it strengthen the arbitrary-internal-
recoding cut theorem to a universal source rigidity result. No new κ is claimed.

## Replay

From the repository root:

```sh
python -I -B research/moonshot-005-program/results/complex-survivor-boundary-rigidity/author/check.py --repo . --out /tmp/s031-complex-boundary-rigidity
```

The standard-library checker authenticates the two frozen sources; replays
all 1289 target fields; reconstructs and multiplies the full exact inverse;
rebuilds the derivative matrices from the actual literal DAG; verifies all
five whole-bank-zero and isolation witnesses; and directly replays three
simultaneous scalar changes against the formula. Those controls include
the singular all-five deletion and two invertible changes whose complete
inverse formulas have exact zero left/right product residuals, evaluated
through the five-dimensional factorization. Two malformed certificates must
be rejected.

`author/output/RESULT.json` is the retained author receipt. The written
all-width proof is in `PROOF.md`. Author replay is distinct from independent
mathematical admission and from a formal proof-kernel check.

## Open next questions

The next construction obligation is a paid communication repair with changes
to old internal forms and complete target restoration. Crossing the four
previously known saturated cuts alone does not construct a supplier: the
cuts must also be reclosed after adding the proposed routes. Compute the
exact deletion defect and permit new payloads chosen jointly with surviving
local recodings; either give a complete causal word or identify a further
cut or rank obstruction.

A second question is whether a larger, explicitly charged change of boundary
interface can make a changed target useful to the complete caller. The present
theorem only handles independent bijections within the original boundary banks.
