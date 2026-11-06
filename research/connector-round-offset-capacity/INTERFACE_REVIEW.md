# Independent audit: deterministic round-offset capacity

Reviewer: worker B (`recovery_lower`), for @CubeJerry with substantial
OpenAI Codex assistance. No completed recovery-package files changed.

Reviewed `worker-e/research/connector-round-offset-capacity/PROOF.md`,
SHA256 `686788130046ab982d756cd916eced3982bb710b7fb116dd0d7725ceeb96db47`.
Canonical source base: `7c49fe32c55de02c2c873655c804b16e4c3fef0a`.

**PASS:** no blocking mathematical or model-compatibility issue found.
This is an independently assigned mathematical AI review, not a proof-kernel
or independent human acceptance. Worker C owns literal finite replay, and
the upper-bound reviewer separately checks the inherited counting argument.

## Literal correction and hidden restrictions

Every round contains each source exactly once. Thus its starting prefix is
exactly `r*1` over the integers, regardless of the permutation used inside
that round. After a designated subset `S` is called first, the actual prefix
is exactly `r*1+1_S`. The designated group subsets for a target mask are
disjoint and sum to that mask.

Selecting the ordinary positive read at round start
`r_0=(-sum r(S_i)) mod c` therefore cancels the scalar offset modulo `c`.
This read does not need an unused round. It can be earlier than the active
reads, later, in an active round, or even at the same source boundary as
another read. The inherited contract allows repeated boundaries, and calls
to an output preserve the connector, so chronological sorting is valid.
The negative sign is used only in computing a nonnegative boundary index;
no inverse data operation or negative map call appears.

The assumptions `D,b>=1`, `D(2^b-1)<=c`, and `D+1<=c` suffice. They ensure
that distinct assigned rounds exist and that the `t+1<=D+1` reads can be
padded to exactly `c`. An empty global block part uses no local reads.
All cases remain valid in composite characteristic. Arbitrary dirty input
and output values are retained as stated; the order `A_M B_j` never changes.

## Concatenation and uniform parameter choices

Completed blocks have prefix zero modulo `c` on their source coordinates.
Consequently later-block reads cannot introduce unwanted earlier-block
coefficients. At most `floor(c/(D+1))*(D+1)<=c` reads are selected for any
global mask; padding at global zero cancels the dirty connector coefficient.
Each source and output has exactly `c` complete calls. The lower bound
`N(c)>=D*b*floor(c/(D+1))` follows with no restriction to a subsequence of
integer characteristics.

For every fixed integer `d>=2`, setting `D=d-1` and
`b=floor(log_2(1+c/D))` is admissible for all `c>=d`. It gives
`k=(d-1)log_2(c)-O_d(1)`, matching the inherited fixed-depth leading upper
term. The construction need not beat the best known finite depth-two word;
the claim is the leading coefficient, not pointwise finite optimality.

The explicit varying-depth choice in section 2 was checked separately.
For `c>=16`, write `L=log_2 c`, `D=floor L`, and take the stated `b`.
Then `D+1<=c`, `b>=L-log_2 D-1`, `b<=L`, and `D<=L<D+1`. Expanding the
floor gives

`D*b*floor(c/(D+1)) >= c*b-c*b/(D+1)-D*b`.

The three terms are bounded below by
`c*L-c*log_2 L-c`, `-c`, and `-L^2`, respectively.
For `L>=4`, `2^L/L^2` is increasing, since its logarithmic derivative is
`ln 2-2/L>0`, and it equals one at `L=4`. Hence `L^2<=c`, proving exactly
the claimed explicit lower bound

`N(c)>=c log_2 c-c log_2(log_2 c)-3c`.

This is a uniform all-integer bound. Together with the inherited upper
estimate, it proves the limit one directly, without requiring an exchange
of two asymptotic limits.

## Upper-bound interpretation

There are `cn` indexed source boundaries after identifying the initial and
final boundaries. Prefix vectors may coincide; counting indexed multisets
still gives a valid upper bound. Each multiset determines at most one mask.
The argument therefore covers every exact-floor word, not only the proposed
construction. The substitution `x=(n+1)/c` in equation (4) is correct.
Using `log_2 x<=x/2` for `x>=4` yields `n=O(c log c)`; substitution back
then yields the stated upper leading coefficient one. The proof correctly
credits this inherited counting estimate.

## Complete costs and scope

The explicit schedule construction uses no additional data operation.
Its `O(ck)` source-label construction/storage accounting is an offline
combinatorial description; it does not price arbitrary maps or imply that
group extraction and modular arithmetic are physically free.

The exact map-call bill has `cn` source calls and `c(2^n-1)` output calls.
The full physical bill must retain input admission/layout, coefficient
preparation, complete source/coefficient access, target updates, scratch
restoration, head returns, instruction construction/storage/read/dispatch,
workspace, precision, routing, and outer costs. Section 4 explicitly retains
unknown physical costs and makes no favorable supplier or new-kappa claim.
For maximum clarity, the orchestrator was advised to name coefficient
preparation and instruction storage/dispatch explicitly, and reiterate the
inherited complete-call scratch/head contract. This is a prose clarification,
not a mathematical blocker.

The result changes no selected frontier, discharges none of its assumptions,
and supplies no physical consumer. Exact finite capacity and lower-order
asymptotics appropriately remain open.

## Provenance

The separate `OFFSET_OVERLAP_REVIEW.md` records the bounded canonical archive
and live all-state PR search. No matching result was located. Generic
partitions and palettes retain classical and repository predecessor credit,
especially CrocSwap/integer-mult-bounds#4256 and
CrocSwap/integer-mult-bounds#2208 in different demand/operation models.

This review is pinned to the proof bytes above. Material changes to the
theorem, parameters, or interface require another review. Final package
metadata and committed-byte checks remain integration obligations.
