# Independent signed-format bridge review

**Disposition: no blocker in the frozen bridge's declared valid domain.**
Normal and optimized Python produce identical receipts. The complete matrix
observation is separate; this report is not another physical Core replay.

Prepared for @CubeJerry by seed78 with substantial OpenAI assistance. This is
executable and mathematical review evidence, not independent human or formal
kernel acceptance. No new kappa or selected-assumption discharge.

## Frozen SHA256 pins

- format_bridge.py: `037dd2265e637f92c6f51320409fb348b148ce9a5e873a353aba053a5c94d1d3`
- Retained transport: `80b246fafae0adf53af7561e1be59f4374e6294d66bb7a12ef9524b9ef4f2a78`
- bridge_review.py: `9d84eb0f7b7b5e2ead0e9ceeffb70f91770af17b1b0c5c252ad1bacbcdcc0e69`
- signed_oracle.py: `46ceaa9e0f4f35e1a0748c70c8c63e084a8ea4350bebc81a810b8227beb342f7`
- Both bridge receipts: `c8264d883d7f9dcf02a803d82c6f8ddd0aa805e5839ecbc3f83acf9843b1fac4`

The transport predecessor is commit
`630c9c2a5d6373ca103c55108bb606b4868bc6fd`. The Core closure authenticates its
own Git/SHA256 dependencies before loading retained physical Count arithmetic.

Keep the two reviewer scripts adjacent and run:

```sh
python -I -B bridge_review.py --package /path/to/actual-core-halo-join --output normal.json
python -I -B -O bridge_review.py --package /path/to/actual-core-halo-join --output optimized.json
```

Expected status: `INDEPENDENT_CORE_HALO_BRIDGE_PASS`, with 19 success cases
and 9 rejection controls. Checks survive optimized Python. Source bytes are
checked before/after execution; review loaders bypass stale bytecode.

## Independent method

All transport/native payload ports and the one-word scratch role use separate
sparse hardware. Operations access the current cell and move one cell.
Translated origins have local ownership guards and prefix sentinels. Immutable
inputs reject writes. Original physical Count/pool operations remain active;
no encoded counter is replaced by a host integer. The production bridge runs
under the retained no_decode guard. Independent sign-magnitude/two's-word
encoders give expected bits; no author's fixture or expected-output routine
is imported. Host numeric operations occur only in fixture/observation code.

## Executed endpoints

Successes cover seven sign-magnitude widths, both signs, zero, coincident and
different grids, both complex components and production dimensions
`h31/w270/q28/P246`. Returns cover the minimum 9-bit signed value, negative
odds, and drop counts 0,1,2,8,9,10,19. Checks require exact complete records,
canonical zero, unchanged borrowed cells/Count ports, restored origins,
erased private roles and no online payload-role allocation.

Actual rejection controls cover a late negative zero, late malformed digit,
missing record delimiter, missing end marker, inadequate lifted carrier,
coarser proposed Core grid, and positive/negative/minimum-word output overflow.
Rejection restores the borrowed source and clears private work. Failed return
clears its target; it does not recover the old target contents. This is cleanup
rather than rollback.

A 150-bit call followed by a 4-bit call retains 151 scratch cells. The shorter
call uses 347 payload operations, matching a fresh shorter call with five
retained cells. Thus current clearing time is independent of old blank backing,
while historical space remains charged. Those 347 actions exclude Count work
and the Core; actual retained counter operations execute in the reviewer but
are not included in this payload-only number.

## Cost check

Let `ell=ceil(log2(2+h+w+P+q+drop))`. Every component loop is bounded by a
word width or a shift clamped to that width, using O(ell)-bit Counts. Whole
fields use end markers, avoiding a record-count decrement for every bit.
Lift scans magnitude forward/backward, restores position, writes explicit low
zeros and emits sign/extension bits. Its domain `h+P-q<=w` gives O(h+w)
payload work. Return scans to the sign and back, converts to unsigned magnitude
with finite carry, discards low bits, checks overflow, pads a word and reads it
backwards: again O(h+w). Even for drop>w only w data bits are read; the drop's
encoded length remains in ell.

A fixed number of short Count arithmetic calls per component, and encoded
counter work per iteration, give `O(T*(h+w)*poly(ell))`, including rewinds,
current target/input clearing and complete return scans. Under the declared
precision/normalizer bounds, h=O(w) and ell=O(log w), giving the required
`O(T*w*polylog w)` overhead. The sparse halo's quadratic scalar tariff is
not substituted for this dense conversion.

Extra roles are the fixed 64-role pool, one complete lifted input and one word
buffer. All old maximum extents stay charged. Core output/work/controls,
transport input/saved/return roles, archives and consumer roles retain their
complete separate bills.

## Limits

Same reference, compatible layout/controls, exact full-field extent and the
admitted Core supplier remain premises. This review does not establish native
multiplier/Hadamard rates. General axis reversal needs separate evidence.
The frozen AttachedCore enters input cleanup only after core.run returns;
if that supplier raises first, the lifted input remains for caller cleanup.
The author explicitly retains this composite error-path limit with no automatic
retry/rollback claim. The complete valid success domain is the theorem scope.
The #6904 consumer and #6880 disjoint numerical splice are predecessors.
