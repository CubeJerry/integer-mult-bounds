# A two-input obstruction to a one-packet root-2 shortcut

**No new κ.** This package answers a restricted version of the open root-2
staging lead in [PR6144](https://github.com/CrocSwap/integer-mult-bounds/pull/6144).
Repacking one carried value and freely rewriting linear operations at the
specified frame-3/595/738 contacts cannot repair the proposed shortcut. The
obstruction survives arbitrary coupled recoding and propagation through the
entire remaining fixed program; it does not require intermediate readers to
return correctly at their old deadlines.

The exact certificate uses just original input coordinates **0 and 8**. In the
zero-packet reference, every field at every permitted contact has zero
projection on these two inputs. The required final correction has rank **2**:
its rows 112 and 144 are

| Final row | Input 0 | Input 8 |
| --- | ---: | ---: |
| 112 | 1/2 | −1/2 |
| 144 | 0 | −1/2 |

The determinant is **−1/4**. One arbitrary linear packet supplies at most one
row-space direction, even if copies of it are injected freely anywhere. This
is an exact finite certificate plus a written argument for all rational linear
recodings in the declared model, not a failed finite search or a universal
lower bound for P104.

## Exact model and relevance

The input is DreamingOfClouds' PR6144 word at
`4f3b67e7c37ae270da9584033132866d0cf63e42`, retained byte for byte in
`inputs/pr6144-WORD.json.gz`. Its published lead proposes removing owned
register 772's stages 520 and 737 by changing the readers. This package first
examines reader 451 moving from `3→737→738` to `3→595→738`.

The reference deletes the one COPY into 772, its nine outgoing ADDs, and
451's read of 228 at frame 737. It changes the two indicated MOVE endpoints.
It is an instrumented **zero-packet reference**, not a legal claimed supplier.
Every other opcode and its order remain fixed. The model then grants:

- all 797 other formal coordinates freely (768 public inputs and 29 owned slots);
- one fixed packet with any rational linear dependence on the inputs, with
  arbitrarily many free additive injections into any field;
- arbitrary rational linear recoding of the fields whose **reference** chart
  is 3, 595 or 738 at each cut, even allowing free mixing across these charts.

The allowance includes changed packet coefficients, extra scalar operations,
self-rescaling, coupled readers and propagated intermediate errors. It does
not give another independently encoded packet, a new contact outside that
reference envelope, changed outside opcodes, or data-dependent/nonlinear
coefficients. A new coordinate-dependent native encoding is also outside the
scalar-row model; one physical register with arbitrary new operators is not
proved insufficient. New trajectories and additional productive targets require a
new analysis. Read [PROOF.md](PROOF.md) for the precise induction and scope.
There is no claim of a bug in PR6144 or its existing construction.

The optimistic complete local rank changes are priced separately. For
`0 ≤ C ≤ 17/5000`, their gain is at most **357/2500** for skipping 737 with the
direct 451 route, or **357/1250** for both stages with the ideal direct routes.
One extra uncredited positive-rank call **per local invocation** costs at least
1, so either repair loses even before other costs. The physical caller uses
18 local invocations. This does not prove that a second information channel
must require a new call: reuse of existing work, another contact or a changed
contract remains open. The proposed direct 497 route is only an optimistic
budget, not a constructed circuit.

## Reproduce

Python 3.12, standard library only:

```sh
python3.12 -B scripts/research_package.py --package research/p104-root2-packet-cut
```

Expected: `PASS_ROOT2_PACKET_CUT`,
`PASS_ROOT2_PACKET_CUT_INDEPENDENT`, `PASS_ROOT2_PACKET_CUT_ARTIFACT_CONTROLS`, and
`PASS_REGISTERED_RESEARCH_PACKAGE`. The scientific scripts also run directly,
without Git or network, from a clean exported package.

The primary uses normalized integer dyadic pairs and enumerates every cut and
every field. It checks **7,283,846** eligible observations across all 22,818
source events, including initial/final states and owned field 772. A separate
Fraction-based interpreter independently reconstructs the reference, checks
the endpoint columns, source observations and rank witness. All **79** nonzero
final residual rows are retained in [CERTIFICATE.json](CERTIFICATE.json).
[VALIDATION.md](VALIDATION.md) records only checks actually completed.

## Novelty, sources and limits

PR6144 supplies the exact word and the open staging lead. PR6136's five-class
chart-only search concerns PR6030 and does not cover arbitrary scalar
recoding on this changed word. This result adds an explicit information-rank
obstruction for the declared one-packet/contact model. It is not another
chart-only census, a claim that every root-2 redesign fails, or a new κ claim.

Base: `721c03822c421b7f7fcbb2598993b947c4d88419`; priority revision 8; OS seed
**23**, complex-supplier track. [TASK.json](TASK.json) records selection,
overlap limitations, the local claim, checkpoints and stopping rule.
[SOURCES.json](SOURCES.json) records exact source pins. The pending PR6144
inputs are vendored; no unmerged Git commit is needed for offline replay.
The selected κ remains **0.003125804**. All five framework assumptions remain.
No supplier admission, new native map, compiler/outer cold replay, hosted CI,
proof-kernel verification or independent human acceptance is claimed.

## Open next questions

1. Can a pre-existing paid route deliver a second independent correction
   direction without increasing the complete bill? Start with the two-column
   residual and identify a concrete source/contact outside the certified
   envelope. A rank argument alone does not provide that route.
2. Can a different reader trajectory avoid the obstruction? Start by finding
   the first new contact whose reference row has a nonzero 0/8 projection;
   then emit the complete word, preserve arbitrary inputs, and price every
   native operation, target, owned lifetime and caller charge.

These are model changes, not requests to rerun the same closed linear search.

## Attribution

Prepared for **@CubeJerry** with substantial **OpenAI Codex assistance**,
including separate construction, mathematical review and independent-checking
agents. Apache-2.0. Credit **DreamingOfClouds** for PR6144/6143/6030/5907 and the
explicit open lead; **Ali Romman** for the P104 source and verifier lineage,
**Matarener**, **Josie Elliston** (PR6136), **Clear1nsight**, **Mason Hale**,
**Pierre-Loic Doulcet**, **Douglas Colkitt**, and the retained native/controller/
compiler/BIT/analytic predecessors. PR6145 (@CubeJerry) independently developed
the 772 relay descent; it is credited context, not a dependency of this proof.
The retained PR6144 README preserves its source-specific credits. No claim is
made to invent the general linear information-rank argument.
