# Independent review of the literal complete row controller

**Decision: pass within the stated successful ABI and retained-provider
boundary. No substantive defect was found.** This is model-assisted review,
not human approval or formal-kernel acceptance. There is no new kappa,
full-source dispatcher, recursive allocator or unconditional multiplier claim.

Reviewed scientific bytes:

| File | SHA256 |
| --- | --- |
| controller.py | `efc3d8b0d089a56765f3eb6a2cc2a641a99f257a58f069a4d26fe5c912b1abd3` |
| hardware.py | `8870da2142377a891ff9730a7868616e3eb1cf2b20a39440cc540548feceb10e` |
| join.py | `95f4d2bd4f2ae2a761381eee0c36c9b8d2aa6140ba9cbb0830bca2794c88df9d` |
| PROOF.md | `33f4340322be07b7000ef3ac089e25c3a853a7a8ca2f9f2aecabe6e230856bba` |

The 10,123-location graph has digest
`f8f0bd615531c914efc110d8a9d5ce2fafa2b00c8a568bdbfb86bf24868a0ef7`.
The predecessor is [B5 at exact commit be17dd21](https://github.com/CubeJerry/integer-mult-bounds/tree/be17dd21af36a8b0546942299ebca7b1c83c4675/research/current-crt-direct-switch-consumer).
Canonical main remains `e54523517d0f03e58352e647c403a5af3e525a57`.

## Universal control and restoration argument

The construction is a constant-size finite graph. I checked every instruction
in all four 2,500-location predecessor copies: reads and jumps use the exact
injective PC translation, tape operands and symbols are unchanged, each
successful halt becomes its one designated continuation jump, and unsuccessful
halts retain their status. These copies occupy exactly locations 123 through
10,122. The remaining 123 locations introduce no dynamic arithmetic or call
stack, and no instruction writes borrowed input roles 14–16.

Put M=2h−2. Entry overwrites the entire inactive owned p-bit row, not a live
borrowed value. Inverse initialization performs two increments for each unary
mark after the first, producing M. Since p>=h+1, every construction and later
update fits the row frame. This uses the typed equality between the binary
height and unary width; the graph is not claimed to prove that equality from
arbitrary malformed descriptors.

Immediately before call r, the forward row is r and the inverse row is M−r.
The width cursor lies at `1+min(r,M-r)`, which is the appropriate target for
both orders. Each unchanged point call reads the actual current wire, consumes
its physical Boolean, and returns the cursor and all other heads to their
entry locations. The point proof therefore composes with one literal update
before each later query. The cursor visits `1,...,h,h-1,...,1` exactly once
per displayed position, giving 2h−1 queries. At h=1 the center transition
moves from R through the sole mark to L and finishes after one query.

The canonical layers are involutions, so reversing their row order gives the
inverse complete padded rotation. The terminal zero-row scan leaves all p row
bits zero and preserves both markers. All heads finish at their own origins;
the fourteen point windows are blank and reenterable. Opaque earlier backing
outside the granted windows is untouched. These arguments do not establish
rollback or complete head return after rejection, which the proof excludes.

## Independent complete invoice derivation

A full row-zero scan costs `Z=7p+7`: two initial instructions, four per bit,
one terminal read and a rewind costing `3(p+1)+1`. An increment with c
trailing ones, or decrement with c trailing zeros, costs `7c+8`. Across
the full sequence 0 to M, the propagated-digit total is
`sum_(k>=1) floor(M/2^k)=M-popcount(M)`; decrements have the same total.
Thus either complete counter sequence costs `15M−7 popcount(M)`.

Forward startup after zeroing costs four instructions. Cursor control costs
`4h+1`; each of M updates has one subsequent jump. With two zero scans and
the terminal halt, the sum is exactly

`2(7p+7)+4+(4h+1)+M+15M−7 popcount(M)+1`

`=14p+36h−12−7 popcount(M)`.

Inverse startup costs `6h+8` plus another complete increment sequence.
Replacing the forward startup therefore gives
`14p+72h−38−14 popcount(M)`. In particular h=1 gives `14p+24` and
`14p+34`, consistent with the literal center transition. A successful point
halt and its replacement jump each cost one, so no point work disappears.
The complete bill must retain all 2h−1 full point calls, as it does here.

The fixed private window lengths sum to
`(p+2)+4(h+3)+3+(bit_length(h)+3)+7(h+4)`
`=p+11h+bit_length(h)+48`. The controller stays inside the row and width
frames, and every call reuses these same per-role windows. Storage is the
union with each owner's entire earlier retained interval, not this sum
multiplied by the number of queries and not a charge reduced after erasure.
Owner acquisition and all other entry resources remain supplied obligations.

## Separate sparse execution and controls

The supplementary checker imports neither the author's hardware nor verifier.
Its own sparse PC/memory interpreter checks and issues every physical R/W/M
action, compares complete backing state with its sparse map, and observes the
row, cursor, copied query, current wire, Boolean, individual point return and
complete-route return. Its canonical network oracle uses parity union-find
constraints and was reused verbatim from the earlier independent B5 review,
with attribution and the original script hash in the checker. Expected output
helpers from the retained source are never called.

Fifty focused complete routes execute 366 point calls and 1,667,878 literal
instructions. Coverage includes h=1, unit modulus, a high modulus bit, several
carry boundaries through h=9, non-power moduli, padding, arbitrary dirty
inactive row bits, h=5/p=97, translated owner origins and opaque older private
histories. Every row/cursor/current-wire invariant, point cost, exact driver
count, final byte/head state and fixed historical union is checked. This
bounded evidence supplements the universal proof; it does not infer the
all-height count by fitting samples.

Four actual graph mutations all **return successfully with every head and
nonresult body restored**, but produce wrong endpoints for h=2, s=3, a=2:

| Mutation | Actual output from input 0 | Correct output |
| --- | --- | --- |
| Skip ascending row increments | 1 | 2 |
| Enter forward order from the inverse entry | 2 | 1 |
| Reverse the cursor prematurely | 0 | 2 |
| Copy a stale original wire for each query | 3 | 2 |

The stale-wire control alone uses one explicitly additional test-only owner;
the reviewed controller remains a 20-owner graph. The independent oracle
detects every corruption. A separate zero-modulus run returns inherited
REJECT with the width head at its first mark, confirming why no whole-route
failure-head restoration is asserted.

## Actual source join and source authenticity

An AST comparison verifies that `route_address` is the only caller function
changed. The replacement passes the same twenty owner objects and chooses one
fixed direction entry; numerical leases, all-wire traversal, source staging,
commit, payload access, key writing, radix and disposal remain retained code.

The separate engine executes one actual non-power-modulus source roundtrip
with moduli `(5,7,2,3)` and values `(3,2,1,1)`. The selected left modulus two
gives offset `1*2^-1 mod 3=2`, destinations `[2,0,1,3]`, and forward tags
`[730,905,293,3681]`. Each leg has four full wire routes and twelve point calls.
There are 21,938 point instructions per leg, plus 492 forward or 648 inverse
controller instructions, totaling 22,430 and 22,586. Full source/key/payload
bytes, heads and backing identities restore. All 200 acquired symbol owners
remain counted, totaling 2,126 retained cells across both legs.

`RESULT.json` keeps the complete mixed cost vector, including source actions,
payload actions, radix instructions and passes, bucket/register extents and
outer actions. Those providers were executed unchanged, not reimplemented as
literal bit control by this review. No ROM amortization or full-system speed
claim follows from lowering this per-wire loop.

All 38 retained source-file pins are checked by size, SHA256 and Git blob.
The exact published B5 `adapter.py` and `caller.py` were additionally retrieved
at commit be17dd21 and their full UTF-8 bytes matched against the retained
copies. `SOURCE-CHECK.json` records this boundary. Full-history ancestry or a
new independent proof of the retained source/radix providers is not claimed.

## Reproduction and credit

Both read-only commands pass and emit byte-identical JSON:

```sh
python3.12 -I -W error -B independent_check.py /path/to/direct-row-controller
python3.12 -I -W error -O -B independent_check.py /path/to/direct-row-controller
```

The path argument is optional if the checker is copied into the reviewed
package. `FREEZE.json` records final review-file hashes. Construction credit
stays with the B6 author, @CubeJerry, B5/B4, Nick Petalas's #7504 canonical
switch work and the retained CRT/radix source authors. Substantial OpenAI
assistance contributed to this review. It is supplementary independent
verification, not a separate research-paper contribution.
