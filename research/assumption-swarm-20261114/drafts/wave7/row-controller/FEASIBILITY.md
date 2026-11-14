# Literal complete per-wire CRT row controller: feasibility

Canonical main: `e54523517d0f03e58352e647c403a5af3e525a57`.
Exact B5 predecessor: CubeJerry `be17dd21af36a8b0546942299ebca7b1c83c4675`,
`research/current-crt-direct-switch-consumer`. Its point graph has 2,500
instructions on 20 tapes, digest
`2257055b689e0f88dca29532548639323dc3fa27a6e5150ea6652ed5636e07a2`.
This document proposes a construction; it is not a verification receipt.

## Precise implication and bounded overlap

B5's literal adapter reads encoded h,s,a,j,current x, computes the canonical
switch, consumes its Boolean on the actual target, and restores its private
bank. Its `caller.py:route_address` still uses an outer symbol-action loop
and finite Python flags to initialize/update j, follow the target cursor,
choose each call and terminate. The proposed theorem replaces that complete
per-wire controller by one fixed literal graph with forward/inverse entry
ports. No host loop, decoded h/current row, or runtime callback chooses a query.

Read canonical proofs/READMEs for `crt-current-row-query`,
`crt-uniform-rom-query`, `crt-stable-row-workspace`, `crt-paid-row-reentry`,
`crt-encoded-benes-rom-producer`, `crt-complete-binary-refinement`, and
`crt-mixed-width-caller`. They establish a source-to-one-row join, one ROM
query, stable backing across symbol-controlled calls, source reentry, literal
ROM production, a fixed supplied-ROM repair program's binary refinement,
and the logical mixed-width caller, respectively. None lowers this B5
direct-consumer row loop. Live bounded PR searches for current-row, row
controller, layer scan, Beneš titles and CRT-layer titles found #7504,
#5496, #5092, #4192, #7152 and #5538 as adjacent work. #7152 composes
numerical/ROM state across tree commands, not the direct-predicate loop.
Coverage excludes arbitrary historical diffs and unpublished work.

## ABI and fixed control construction

Retain the same 20 owners: 0..13 retired point-service bank; 14..16 borrowed
padded h,s,a headers; 17 a separate inactive owned p-bit row frame; 18 mutable
current h-bit wire; 19 borrowed unary width. All enter at L. The row body may
contain arbitrary bits with no live semantic obligation; overwrite all with
zero and leave zero. Distinct owners, supplied blank private windows, prior
history, opaque exteriors and header equality remain explicit B5 premises.
In particular binary h equals the number of width marks and p>=h+1.

Embed four statically renamed copies of the unchanged B5 graph for the four
finite control modes forward/ascending, forward/descending, inverse/ascending,
inverse/descending. All use the same owners; only fixed PC addresses and halt
continuations change. A constant four-copy product needs no unbounded return
stack or new tape. Constructor loops are over four fixed modes, never h.

Forward entry zeroes the row and selects the first unary width mark. Inverse
entry additionally scans all marks after the first, incrementing the row
twice per mark to construct 2h-2. The target cursor traverses all marks right,
then returns left. At R it moves left twice and changes finite mode; at L it
terminates. Between queries the row increments forward or decrements inverse
using literal carry/borrow and head return. Retirement zeroes the row frame.

After r queries the next forward row is r, the inverse row is 2h-2-r, and
the target is 1+min(r,2h-2-r). Hence exactly 2h-1 correctly bound calls run,
including h=1. Involutory canonical layers prove reverse order is the inverse.
Source/header production, all-wire enumeration, payload scans and radix stay
external; no complete CRT, assumption discharge, or new kappa is claimed.

## Optimistic complete bill before implementation

Put Q=2h-1 and retain B5's
`T_point <= 1024(h+3)^2 + 128(p+h+3)`.
Two full row scans cost O(p). Inverse initialization makes 2(h-1)
increments; routing makes 2h-2 row updates. Each update and return costs
O(p); the target cursor has O(h) moves. A provisional controller envelope is
`256(h+1)(p+1)`, to be justified or revised by counting emitted paths. The
complete proposed per-wire bill is Q*T_point plus that controller envelope,
including every call/return, carry, head return and erase.

The new driver touches only existing row/width frames. Point scratch has
fixed per-role windows at fixed h,p; the repeated historical union is O(p+h)
independent of Q. No sum-of-maxima is replaced by maximum aggregate stock,
no history is refunded, and no owner is reacquired per query. Four copies
increase fixed control size only. For N wires the caller pays N complete
drivers plus actual source/headers, indexing, keys, payload and radix work.
ROM build/query/disposal must be compared on that same complete workload;
there is no speedup claim from eliminating the ROM alone. The retained
numerical controller's symbol tariff remains distinct from literal costs.

## Verification and stopping rule

Compare every instruction in four point copies with exact PC/halt relocation.
Start one literal execution at a chosen entry, with no runtime callback.
Compare full routes/inverses with the original canonical Beneš compiler on
exhaustive small domains and h=5,s=17; include h=1, a=0, full/padded modulus,
carry boundaries, long p, origins, whole borrowed contents and all private
history/heads. Use returning stale-wire, wrong inverse-order, target-turnaround
and skipped-counter mutants; watchdog rejection is distinguished from a
returning semantic failure.

Substitute only `route_address` in B5's exact caller, retaining all other code,
and run the actual four-tag modulus-2 and modulus-3/left-2 fixtures with the
same payload mover and full inverse. This is a bounded actual source join.
Stop if the exact interface was already proved, a numeric decode or growing
dispatcher is required, or restoration/resource accounting fails. Credit
Nick Petalas #7504, B4/B5, #7388/#7352 and canonical CRT/row/radix predecessors;
retain Apache notices and exact pins in any verified package.
