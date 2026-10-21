# The right-vector cost gap lifts to F2[S3]

**Scoped proof and explicit bit circuit. No new κ.** An invertible,
non-diagonal two-register target over `F2[S3]` needs exactly **three** paid
right-vector factors, although the free-basis column lower bound is **two**.
This resolves open question 2 of Nick Petalas's [PR4265](https://github.com/CrocSwap/integer-mult-bounds/pull/4265).
The selected multiplication result and its bit supplier are unchanged.

The predecessor established the gap over `M2(F2)` by enumeration. This
package gives an explicit lift that preserves the other component of the
group algebra, a short geometric proof excluding every two-factor word,
and a faithful 72-XOR realization on two arbitrary six-bit banks. It does
not repeat the predecessor's eleven-domain census or assert a better
multiplication exponent.

## Exact result

The paid alphabet is `I + u y^T`, with `u in F2[S3]^2`, `y in F2^2`, and
free `GL2(F2)` maps anywhere. No extra register is permitted. The full
model, algebra isomorphism and proof are in [PROOF.md](PROOF.md).

In the group basis `(012,021,102,120,201,210)`, a six-bit mask records a
formal sum of permutations. With `α=60` and `β=30`, the three chronological
updates are

```text
x <- x + α y
y <- y + β x
x <- x + α y
```

The resulting matrix has row-major masks `(42,60,30,50)` and squares to
the identity. Both registers are active outputs with arbitrary entering
values. The full group-algebra identity holds on every module over this
algebra; the finite regular-action check does not instantiate a uniform
native supplier or the full multiplication algorithm.

The new lower-bound argument projects to a four-dimensional binary space.
Every paid factor fixes one of three planes. Any two-factor invertible
word forces an intersection dimension of zero or two; the target forces
dimension one for every pair of those planes, including after a free
basis change. This is a written proof. The finite census is corroboration.

## Reproduce

From the repository root, with CPython 3.12 and its standard library:

```sh
python3.12 -B scripts/research_package.py --package research/s3-right-vector-lift
```

Expected: ordinary and optimized runs both print
`PASS_S3_RIGHT_VECTOR_LIFT cost=3 column_bound=2`, then
`PASS_S3_RIGHT_VECTOR_INDEPENDENT factors=766 pairs=586756 target_hits=0 dirty_inputs=4096 scalar_xors=72`,
and the runner ends with
`PASS_REGISTERED_RESEARCH_PACKAGE research/s3-right-vector-lift outcome=completed`.
The full registered replay is normally a few seconds. It writes no package
or source files. The scripts can also run directly with `-I -O -B`.

[CERTIFICATE.json](CERTIFICATE.json) is regenerated only by the explicit
`python3.12 -B research/s3-right-vector-lift/verify.py --write-certificate`
command. Default replay recomputes and compares its complete parsed contents.

## Evidence and controls

| Check | Completed coverage |
|---|---:|
| Explicit `F2[S3] -> F2[C2] × M2(F2)` map | 64 elements, all 4,096 multiplication pairs |
| Lifted matrix units | all 16 products |
| Column bound with free basis | all six `GL2(F2)` maps, dimension two each |
| Geometric obstruction table | all nine plane intersections, dimension one each |
| Separate binary-matrix census | all 766 factors, all 586,756 ordered pairs; 64,852 distinct products; zero hits on six free-normalized targets |
| In-place 72-XOR circuit | all 4,096 arbitrary two-bank inputs, all 12 basis columns, and all 4,096 inverse returns |

The two implementations share neither algebra routines nor predecessor
code. They have the same AI-assisted authorship and are not independent
human reviews. The census includes singular factors and identity factors;
there is no invertibility pruning, randomized sampling or search timeout.

Meaningful controls reject each omitted factor (3,072 bad inputs each),
wrong chronology, one coefficient mutation, and replacing left action by
right action (3,840 bad inputs each). Omitting the hidden central component
still passes the matrix quotient but has full regular rank eight instead
of twelve. A free register swap calibrates the minimization over free maps:
its raw column rank is one while its minimized bound and paid cost are zero.
Retained predecessor files are checked against both original Git-blob and
SHA256 identities. Checks remain enabled under `-O`.

The deterministic independent result digest is
`450a2c2ab2527c498ca09e3ad2f6e4c2236d9b1b6a4406fd2fa586b7bc35c1ee`.
The algebra certificate SHA256 is
`5059ae9edca1847a1298ad20e0eeb46f5b0171e0605d25492b6dde6cb7719f13`.
These identify result data, not a proof-kernel validation.

## Complete local bill and expansion decision

| Obligation | Status and cost |
|---|---|
| Completed two-register formal target | Proved minimum: three paid factors, zero free maps in the attaining word |
| Source access in the faithful six-address circuit | Constructive: twelve translated-bank XORs, 72 scalar XORs, 72 source reads + 72 destination reads + 72 writes |
| Helpers, copies, frame changes, scratch return | Zero in the specified finite in-place circuit; both banks are active outputs, no helper bank exists |
| Returning the two active outputs to their original values, if separately requested | Another three factors / 72 XORs; not included for free |
| Native supplier conversion, fixed-tape routing, physical hosting, precision and recursive moment | Uninstantiated; not assigned zero cost |

The optimistic hypothesis was that the column bound two was attainable.
The geometric obstruction rules this out even in the favorable full
right-vector alphabet. The 72-XOR expansion is a complete finite circuit
upper bound, not an optimal XOR count or a native paid-profile claim.
**Stop at this resolved handoff**: do not expand to a supplier search or
claim a κ gain without a named consumer and a complete native bill.

This does not contradict #4243's diagonal theorem: this target is
non-diagonal. It does not reopen the closed GL3 coordinate-CNOT or
torsion-free three-register searches. It does not cover added spectator
registers, ring-valued free maps, or ring-valued right vectors.

## Pins, selection and verification scope

Exact canonical-main base:
`12fa8c5c844be21bfefb38a19503fbd867a11244` (priority revision 7).
The accepted assembly remains complex-bound at
`κ = 836330098538459/500000000000000000`, with the #589 bit supplier.
The selected certificate, actual assembly and maintainer review were read;
the selected cold replay was not rerun for this isolated local result.

- PR4265: `665bfe79d726a0cb3494326d2f63ae81d313302f`.
- PR4243: `f0cde9eef1808d5b540d2aaa2cc3adddb1bf7197`.
- PR4099's model is pinned at the canonical base above.

[SOURCES.json](SOURCES.json) pins exact original blobs and hashes. The two
pending-PR texts are retained byte-for-byte in `references/`; they are
provenance, not imported executable dependencies or claims of ancestry.
All scientific calculations are self-contained. [TASK.json](TASK.json)
records seed **01** drawn from OS randomness, the three candidate tasks,
the explicit handoff override, overlap limitations and local claim.
There was no pinned sprint issue; the connector has no Discussion write
operation, so the claim and result are recorded locally.

Registered ordinary/optimized scientific replays, committed-byte/source-history
checks, and the Git-free committed export replay are required publication
gates for this package. Their executed results and publication tree binding
are reported in the PR handoff. No upstream CI or independent human review
is claimed merely from local execution.

## Open next questions

1. Does the cost remain three with one extra arbitrary dirty register that
   must be returned? This matters because auxiliary storage changes circuit
   feasibility. Start by applying the plane-intersection argument to the
   six-dimensional quotient and the target `diag(P,I2)`; the larger free
   `GL3(F2)` action is the blocker. No new census is requested by this result.
2. Can a concrete supplier boundary use this non-diagonal formal target,
   and what is its actual native bill? First specify one producer and
   consumer with legal address actions and price the twelve translated-bank
   XORs, including routing and eventual return. No such caller is supplied
   here, so the result gives no multiplication improvement.

## Attribution and license

Prepared for **@CubeJerry** with substantial **OpenAI Codex assistance**.
Credit **Nick Petalas** for #4265's original matrix target and lift question,
and #4243's normalization and free-basis model; **Wentao Li** for #4099's
right-vector column bound and alphabet; and the credited #2513 cyclic-root
lineage. The seed-selected task catalogue and selected construction retain
their original contributor credits. New code and text are Apache-2.0.
The retained source texts keep their original attribution; see [NOTICE.md](NOTICE.md).
