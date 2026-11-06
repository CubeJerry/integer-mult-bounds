# Independent adversarial review of the chain-cover refinement

Reviewer: worker B (`recovery_lower`), for @CubeJerry with substantial
OpenAI Codex assistance. Canonical base:
`7c49fe32c55de02c2c873655c804b16e4c3fef0a`.

**PASS.** The refinement is compatible with the already reviewed deterministic
round-offset construction. Its scoped exact cover count and explicit improved
lower-order capacity bound are valid. No mathematical blocker was found.
This is a separately assigned AI review, not independent human or
proof-kernel acceptance. Existing completed contribution files were unchanged.

## Reviewed byte pins

| File in this package | SHA256 |
|---|---|
| `CHAIN_COVER.md` | `7036d64030e4aa4fe31250c4240c10e6c74d0c4bb213ee28101e2e2fc3f36159` |
| `chain_construct.py` | `7818f057b521d6b6bfebde7ca4bba768bb1faf7333320366d7504a375af2f1cd` |
| `verify_chains.py` | `f5ed289a93cd30321fedfc23fecc5dad9d4766aee5a710e26c88073cc0b71027` |
| `chain_bounds.py` | `1a88180362299d7d467becbb56029dee636750ea2cf027e680842deea2775fae` |
| `verify_chains_independent.py` | `89c7bc833be2dcd4141f78f995460715847ee47e404d8c6243874301a6b2771e` |
| `CHAIN-COVERS.json` | `ab545aae60e0b3326433f969b69c8b510ccd474adb9d3b77313dbee692b36bf9` |
| `CHAIN-FIXTURES.json` | `bedb6d3ae4d7c68f94277cf108477a2e14a03eb43fe31cfd0044a13c011f4ecf` |

The separate `verify_chains_independent.py` has its own review and evidence. It was
not authored here and is not represented as this reviewer's independent
implementation.

## Universal decomposition, coverage, and scoped minimality

The symmetric-chain recurrence partitions each old chain and its new-label
copy into exactly two chains, omitting the second when empty. The first
contains every old set and the new-label copy of the old top set; the second
contains precisely the remaining new-label copies. Endpoint ranks sum to
the new dimension, and every step adds one element. Induction from the
empty cube proves a saturated symmetric-chain decomposition for every
dimension, not just the finite checked dimensions.

Each resulting chain meets the middle rank exactly once, so there are
`W_b=binom(b,floor(b/2))` chains. Listing the smallest set's elements first,
then the chain increments, then all remaining elements produces a genuine
permutation whose cardinality-indexed prefixes include the entire original
chain. Thus every nonempty group subset occurs as a prefix in at least one
of the `W_b` assigned rounds.

For minimality the proof correctly uses rank `ceil(b/2)`, which is nonempty
even at `b=1`. A permutation has just one prefix at that rank. Across `D`
disjoint groups, the `D*W_b` such group subsets form an antichain; one global
permutation-prefix chain cannot contain two of them. The lower bound is
therefore exact under the explicit rule that every group subset must be
available as one literal productive prefix. It is not an unrestricted
connector lower bound. The addendum states this limitation clearly and does
not claim an optimal lower-order term for `N(c)`.

## Round reuse, dirty state, and the inherited model

Two different subsets in one group chain may now select the same source
round. This creates no conflict: any one target mask has only one part in
that group, and distinct target outputs may read the connector at different
boundaries in the same round. Output calls leave the connector unchanged.
Distinct groups receive disjoint round sets, although the algebra itself
requires only the actual prefix identity.

Every productive read still sees `r*1+1_S`. The one additional positive
read at round start `(-sum r) mod c` cancels only the common offset and leaves
the desired disjoint union of group parts. The correction may reuse an
active round or boundary, and may occur earlier or later; sorting is legal.
The assumptions `D*W_b<=c` and `D+1<=c` ensure both source-round capacity
and output-read padding. The second is genuinely needed for this proof:
at `b=1`, the first alone would allow `c=D`.

Every source still occurs exactly `c` times. Padding to exactly `c` output
reads cancels arbitrary initial connector dirt, and disjoint-source copies
concatenate with zero residual coefficients modulo `c`. No signed call,
free copy, clean row, extra connector, source mutation, map commutation,
prime characteristic, or additional restoration operation is assumed.

## Binomial estimates and the explicit global guarantee

The elementary estimate in section 4 was checked algebraically. For
`u_m=binom(2m,m)/4^m`, its recurrence is exact. The upper induction
`u_m<=1/sqrt(3m+1)` follows because

`(3m+1)(2m+2)^2-(3m+4)(2m+1)^2=m>=0`.

Its even and odd consequences give `W_b<=2^b/sqrt(b)` for every `b>=1`.
The stated lower induction and odd-case factor give
`W_b>=2^b/(4 sqrt(b))`. The consecutive-width ratio is at most two, so
maximal feasible `b` indeed satisfies
`b=log_2 x+(1/2)log_2 log_2 x+O(1)` for round allowance `x` tending to
infinity. This justifies the optional fixed-`D` second-order expansion.

The explicit all-characteristic bound requires only the upper estimate.
For `c>=16`, write `L=log_2 c`, `D=floor L`, and
`b=floor(L-(1/2)log_2 L-1)`. Then `D+1<=c`, `1<=b<=L`,
`b>=L-(1/2)log_2 L-2>=L/4`, and `2^b<=c/(2 sqrt(L))`.
The last lower bound on `b` holds at `L=4` and increases thereafter.
Consequently

`D*W_b <= L*2^b/sqrt(b) <= c`.

Applying the exact concatenation bound gives

`N(c)>=c*b-c*b/(D+1)-D*b
      >=c*L-(1/2)c*log_2 L-2c-c-L^2
      >=c*L-(1/2)c*log_2 L-4c`.

Here `b<=L<D+1`, `D<=L`, and `L^2<=2^L=c` for `L>=4` were checked.
This proves the claimed `-(1/2)c log_2 log_2 c-O(c)` lower term uniformly
for every integer `c>=16`. It strengthens the guarantee while leaving the
already established leading limit one unchanged.

## Code review and actually executed corroboration

The constructor implements precisely the reviewed recurrence. Its locator
records each symmetric-chain member's chain, and the emitted permutation
places that member at its cardinality prefix. Global round assignment,
modular correction, and time offsets for disjoint-source copies match the
proof. The executable's finite size restrictions are verification limits,
not restrictions on the mathematical induction.

An independent no-import check executed here inspected all 8,190 subset
memberships in the literal covers for `b=1..12`: exact partition, saturation,
symmetry, permutation validity, chain count, locator, and actual prefix
containment all passed. A separate exact-integer check passed
`W_b^2*(b+1)<=4^b` for every `b=1..2048`. This latter inequality is slightly
stronger than the bound used in the addendum, but its finite testing is only
corroboration, not a universal proof.

The final packaged primary checker was executed in both modes from the
repository root:

```sh
python3 -B research/connector-round-offset-capacity/verify_chains.py
python3 -O -B research/connector-round-offset-capacity/verify_chains.py
```

Both passed with identical receipts: 12 covers, five literal fixtures,
4,739 nonzero target masks, 30,180 complete calls, and 69 rejected controls,
plus the arithmetic checks below. Rerunning the author checker is
regression evidence; it is not described as independent mathematical
verification.

## Final exact-arithmetic delta

The added `chain_bounds.py` and its call from `verify_chains.py` were reviewed
separately. With `W_b=binom(b,floor(b/2))`, the recurrence is exact:

- For odd `b`, `W_(b+1)=2 W_b`.
- For even `b`, `W_(b+1)=W_b*(b+1)/(b/2+1)`; the integer division is exact.

Starting with `b=W_b=1` and increasing while `D*W_(b+1)<=c` therefore finds
the largest feasible width. `D=c.bit_length()-1` equals `floor(log_2 c)`
for every accepted integer `c>=2`; `D+1<=c` and the starting width is
feasible. The central widths strictly increase for `b>=1`, so the search
terminates. The former subset-per-round width expression
`(c//D+1).bit_length()-1` is exactly `floor(log_2(1+c/D))`, since taking a
positive number's integer floor does not change its binary-logarithm floor.

The registered primary checks use exact integer arithmetic for both squared
binomial estimates at `b=1..2048`, all 16,383 integer characteristics
`c=2..16384`, and eight additional power-of-two characteristics with exponents
`4,8,16,32,64,128,1024,4096`. They verify round feasibility, maximality,
concatenation, and no loss against the old subset-per-round guarantee.
The printed ratios are downward-rounded parts per million, not floating
point approximations used as proof premises. These finite arithmetic tables
corroborate the written all-parameter proof; they do not replace it.

An independent oracle was executed for all 16,391 entries in those two
domains (including their repeated endpoints). It located the maximal width
by binary search using direct `math.comb` evaluations of `D*W_b<=c`, rather
than using the incremental central-binomial recurrence. Its width, actual
central coefficient, and copy count agreed with every `capacity(c)` result,
including the `2^4096` endpoint. Seven invalid characteristic inputs
`True`, `False`, `-1`, `0`, `1`, `2.0`, and `"2"` were rejected.
This checks the new numerical mechanism by a distinct algorithm. The
symbolic recurrence derivation above, not the finite sample, supplies its
universal justification.

## Bounded overlap and classical credit

Live all-state GitHub searches used `repo:CrocSwap/integer-mult-bounds
is:pr`, with up to 100 returned results and no result-count truncation:

| Additional terms | Returned / total |
|---|---:|
| `"symmetric chain"` | 0 / 0 |
| `"chain cover" "connector"` | 3 / 3 |
| `"Sperner"` | 0 / 0 |
| `"binomial" "connector"` | 10 / 10 |
| `"maximal chain"` | 1 / 1 |
| `"middle layer" "connector"` | 0 / 0 |
| `"Boolean lattice"` | 7 / 7 |

Relevant titles and body passages were inspected. The chain-cover connector
hits concern sequential nilpotent/chain-map schedules
(CrocSwap/integer-mult-bounds#6560,
CrocSwap/integer-mult-bounds#4343,
CrocSwap/integer-mult-bounds#4748), not Boolean subset-prefix covers.
Boolean-lattice hits such as CrocSwap/integer-mult-bounds#172 and
CrocSwap/integer-mult-bounds#6393 concern zeta networks or multilinear
dirty-input evaluation. The previously reviewed partition construction in
CrocSwap/integer-mult-bounds#4256 remains conceptual context with a different
output demand and source-call budget. No matching connector chain-cover
refinement was located. The retained full path metadata also showed no
package explicitly named for this symmetric-chain/Sperner cover mechanism.
This is a bounded search, not an exhaustive novelty certificate; discussion
comments, arbitrary historical diffs, most archive bodies, and unpublished
work remain unchecked.

Symmetric-chain decomposition and middle-layer minimality are classical.
The 1951 de Bruijn, van Ebbenhorst Tengbergen, and Kruyswijk publication
details were independently confirmed from the authors' institutional record:
https://research.tue.nl/en/publications/on-the-set-of-divisors-of-a-number/ .
The scan fetch was unavailable, so this review relies on the self-contained
induction rather than claiming to have audited the original article text.
The addendum appropriately credits the classical construction and limits its
new claim to this connector realization and its capacity consequence.

## Integration limits

Physical coefficient access/preparation, schedule construction and storage,
dispatch, scratch/head restoration, routing, precision, and outer bills stay
payable. No physical consumer or new multiplication exponent is supplied.
Only the scoped cover representation has an exact minimum proved here.

The integrated `verify_chains_independent.py` was compared with its reviewed
scratch predecessor. Its only changes are the attribution/shebang header
and explicit fixture references to `CHAIN-COVERS.json` and
`CHAIN-FIXTURES.json`. Its packaged normal-mode replay also passed, including
89 rejected controls. No unresolved fixture-name integration issue remains.
Final metadata, executable registrations, committed bytes, export checks,
and remote-tree checks belong to integration.
