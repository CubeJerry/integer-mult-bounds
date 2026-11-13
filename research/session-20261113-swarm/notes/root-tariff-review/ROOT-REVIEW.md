# Independent literal adapter cost review

Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`.
The reviewed #7430 source is commit
`39b40c465f7636a4bb6d70af28595fe8f70f4f3f`, file
`research/literal-selected-linear-maps/linear.py`, SHA256
`d56704082b82e37d4a360b8aad7e0af63499f4160c6bbcfd338804453c46fa33`.
This is a scoped implementation audit, not a general permutation or
multiplication lower bound. The positive C child is absent from this count.

## Universal count

For fixed coordinates `0 <= high < low <= 8` and column `0 <= j < f`,
the physical unary guides have lengths

```
A_j = P * 2^((high+1)f - 1 - j),
M   = 2^((low-high)f - 1),
B_j = 2 r S w * 2^((8-low)f + j).
```

These are positive integers. Initial geometry builds j=0; each nonfinal
column halves A and doubles B. Their product is
`4 A_j M B_j = 2 P S r w 2^(9f) = V`.
The PREFIX loop visits A_j marks. Each prefix loads two halves of length
`2 M B_j`, and its two final emit_stream calls write both complete halves
into the destination bank. Both data symbols have explicit branches; zero
does not terminate a stream. Thus each column writes V nonblank payload bits.
F advances only at column_done and has f marks, proving fV actual merge
writes. The unchanged right/left words have19/27 CNOTs and at least19fV/27fV
such writes. Geometry, reads, copies, erasures, returns and C work are extra.

## Independent execution

`check_cnot_writes.py` compiles the pinned single-CNOT unit graph and executes
a separate byte-tape CPU. It never executes the author Machine. Two f=1
calls exercise both physical directions and nontrivial r/P/S. A complete
f=2,w=2 zero field has V=1,048,576 bits; its133,596,442 transitions include
exactly2,097,152 merge writes, with consecutive totals V and2V. All unit-call
heads return and the old source bank retires.

A mutant sends the nonfinal F continuation directly to completion. It still
returns zero data but writes only V bits. The expected two-column count
detects the fault, showing why zero-output agreement alone is insufficient.
The supplied unit boundary includes physical unary guides and complete fields;
it is not an entry producer or a full selected caller. The74,880 finite
geometry specializations check consistency; the displayed identity and loop
invariants give the universal proof.

Reproduce from the session root:

```sh
python3 -I -W error -B root-work/tariff-review/check_cnot_writes.py
```

Expected marker: `PASS_INDEPENDENT_CNOT_WRITE_COUNT`. Exact counts are in
`RESULT.json`. This is a recovery-review artifact, not a separate PR.

## Rate and scope

For fixed0<tau<1, the fV term fits `O(V((f log p)^tau+1))` on a joint
family exactly when `f=O((log p)^(tau/(1-tau)))`. Selected metadata is
separately dominated by the complete record fibre. A polynomial lower bound
on f violates this condition even with a tiny positive exponent.
The separate compiler_routing review approves the actual polynomial group
family, with explicit qualifications. Capacity for h=d does not establish
a scheduled h=d call. The stronger whole-layer conclusion additionally
requires unchanged occurrence expansion and a nontrivial root adapter on a
fixed positive fraction of full call volume. Without that premise retain
only the per-record obstruction. Direct leaves and faster compact-control
schedules remain open. All five global assumptions and kappa are unchanged.
