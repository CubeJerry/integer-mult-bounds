# Worker C independent review of compiler lifecycle lowering

Reviewed 2026-11-09. **Scoped pass; no blocking chronology defect found** in the
reviewed source. Native numerical, geometry and ordinary-row service bodies
remain the explicit premises in A's relative theorem. This review does not
claim to implement them or discharge an entire selected assumption.

## Exact reviewed bytes

- `worker-a/research/compiled-owned-bank-lifecycle/source_ir.py` SHA256:
  `54dd93bc50bd10e974c70794df1c13da27f0e3d8cdb6cfe6791a63280096f1b1`.
- `worker-a/research/compiled-owned-bank-lifecycle/PROOF.md` SHA256:
  `8e7473a63d47a6fc912dede57614e53adeb8485994c2192620ff6b2c4025eb1a`.
- Authenticated unchanged source executor SHA256:
  `0bda14a3e5f4da348cd5c89ebe29d717e7a5406ec31b164d5b9e1d25f7f38e0e`;
  canonical Git blob `9469443a3d7cc6310a7369daf77c7756d5bd3f38` at base
  `7c49fe32c55de02c2c873655c804b16e4c3fef0a`.
- Independent checker `review/c_lifecycle_source_trace.py` SHA256:
  `6215e980fe34a3ec8009ef4208a894d33d521a258287c3f7401c505db5872d1a`.

The source author and reviewer are separate OpenAI agents. This is independent
AI checking, not human or proof-assistant acceptance. A's files were not edited.

## Independent source-trace experiment

The checker does not import A's flat ownership checker or its expected-value
oracles. It starts with the authenticated executor itself and inserts exactly
two observational callbacks in its AST: one at the top of the literal
`for j, ((r,owner),kind)` round loop, and one immediately after that loop.
Those callbacks emit the original unit's j-th nonpaid fragment using the source
executor's actual `fmap` and `omap`. Source class matching, source order,
replication, call order and source permission operations remain unchanged.

A separate subclass removes the predecessor's optional budget fallback, expands
every complete non-base smaller program, and records its actual field list and
complement rank/offset. At elementary rank it records each rank-one axis leaf.
It does not use A's adaptive `begin_round`, `pending` or fragment-detection
logic. The expected trace is therefore tied directly to the source loop which
the proposed annotation claims to refine.

The test unit has two differently ranked productive fields and two private
names; one private name has two disjoint lifetimes. There are explicit scalar
services both before and after paid work, COPYs, private and public paid owners,
and final cleanup. Six compiler ranks are compared event-for-event, including
source fragment operands/tokens, whole-subprogram entry/return field order,
source-complement rank/offset, deepest-exit request identities and elementary
PAID axis/owner.

| Rank | Productive width | Replication | PAID leaves | Borrowed private entries | Source trace events | Maximum exit batches in one round |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 1 | 1 | 2 | 0 | 2 | 0 |
| 3 | 2 | 1 | 5 | 0 | 28 | 1 |
| 4 | 2 | 1 | 7 | 0 | 32 | 1 |
| 6 | 6 | 1 | 28 | 3 | 181 | 1 |
| 9 | 16 | 4 | 101 | 24 | 730 | 4 |
| 12 | 84 | 6 | 689 | 204 | 5,138 | 6 |

Normal and optimized Python both pass, with identical complete traces and
receipts. Commands:

```sh
python3 -B review/c_lifecycle_source_trace.py
python3 -O -B review/c_lifecycle_source_trace.py
```

Logs are `review/c_lifecycle_source_trace.log` and
`review/c_lifecycle_source_trace-optimized.log`.

Two semantic adverse controls are included. Altering every paired
source-complement offset by one is rejected against the direct source trace,
even though the entry and inverse-return tokens still match one another.
Dropping one original nonpaid scalar service is also rejected. These test
source chronology/geometry information, beyond simple balanced ownership.

## All-size source inspection

The finite result supports, but does not replace, the following inspection of
the relative proof.

1. The metadata enumeration in `Lowerer.run_class` has exactly the source
   executor's copy/Pascal-point/multiplicity nesting. Each source guid is globally
   fresh. Thus the stored field map and column belong to that exact occurrence,
   including a productive child role backed by a live parent-private field.
2. For a nondeepest round, the source calls the next class only after forming
   all issuers. `begin_round(parent)` emits the entire preceding fragment before
   any child matching/entry service. No field operation occurs between the
   source issuer checks and this callback, so the slight location difference
   from the direct loop annotation changes no operand value. The call must
   return before the source advances its round.
3. At a deepest round, the pending set groups exactly the current class's
   guids, and the source divides the ordered requests into complete integral
   batches. Every batch's exact owner/name/rank is checked. The final fragment
   is emitted only from the source's final class-release hook, after every
   synchronous batch call has returned. Source and private-bank stack returns
   then follow the original order.
4. Complement metadata carries the current containing program rank and
   complement rank; the claimed offset is their difference. Hence the interval
   is the original `[source_rank, containing_rank)`. The complete ordered field
   list is retained, and the inverse program services occur after the full
   smaller program. There is no additional runtime row split at this boundary.
5. Private banks are keyed by source guid and private name. The parent INIT
   appears in its preceding fragment before a private paid owner can be lent.
   A child sees that field as productive and has disjoint own-private names.
   It cannot emit CLEAR of the borrowed productive field. Actual owner cleanup
   follows all returns; no depth-only allocation is used.
6. The only remaining PAID instructions are explicit rank-one leaves at the
   elementary base. Their owner is the actual handed field and their axis/base
   rank remain in the token. Non-base `sub` always expands the exact compiled
   width. The PAID count is checked against the source compile count; the
   independent trace additionally checks placement/order, which a count alone
   would not establish.

These facts support the stated structural induction on strict smaller program
ranks and chronological class rounds, conditional on the imported compiler
matching/termination theorem and the declared service endpoints. The product
and completion/splitting code preserves explicit before/after services and
occurrence-qualified private names. I found no mismatch with the claimed
source chronology in those constructions.

## Small wording clarification

The `pending` set removes the final batch's guids **before** entering that last
synchronous smaller program. Accordingly, `pending is None` by itself means
all batches have been issued, not that the last one has already returned.
The implementation is correct because the ordinary Python construction call
stack cannot resume the parent or reach its final cleanup until that call and
its inverse services return. The proof's sentence attributing the entire
no-resumption guarantee to the pending set can be made more precise by naming
both the set and synchronous call order. This is not a blocker and requires no
algorithm change.

## Remaining limits

This review checks source annotation and explicit context/lifetime information.
It does not check native table numerical correctness or tariffs, the actual
selected astronomical template's materialization, the ordinary stopping/row
supplier, or analytic recovery. A final publication should bind this review to
unchanged source bytes, or rerun the small source-trace experiment after a
relevant change.

## Portable package adaptation

The independently authored checker is included as `independent_source_trace.py`.
Its only code change is replacing the workspace-specific ROOT with
`Path(__file__).resolve().parents[2]`; the expected trace and adverse controls
are unchanged. The report above retains the original review snapshot hashes.
The package proof now explicitly names synchronous call order alongside the
pending set; machine.py and source_ir.py are unchanged.

Portable commands:

```sh
python -B research/compiled-owned-bank-lifecycle/independent_source_trace.py
python -O -B research/compiled-owned-bank-lifecycle/independent_source_trace.py
```

Prepared for @CubeJerry with substantial OpenAI assistance; separate reviewer
and author methods, without human or proof-kernel acceptance.
