# Independent review of the radix wrapper

Status: **accepted after the explicit bit-order correction described below**.
Reviewer: Route C, S004, 2026-11-26 Melbourne.
Reviewed proof: Route A, `no-padding-radix-wrapper.md`.
Accepted source SHA256:
`66b3f1d1b36a2a753f4ae9a9d04963a685c7aa3342f4eef15e01227df9feb28a`.
Source checked: `openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`,
November tape manuscript `build/interchange.tex`, definition of the field
interchange operation, elementary scans, recursion and final radix-padding
paragraph. This review covers the wrapper implication, not the existence
of an oracle satisfying its parameter-uniform premises.

## 1. Physical scans and coordinate order

For one prescribed interval rectangle, input restriction and output
placement each preserve the lexicographic order of the remaining fields.
Extracting by a full input scan and merging by a full accumulator scan
therefore needs no per-symbol address tag. There is a fixed number of
range fields. Membership changes occur only at prescribed run boundaries;
flags can be retained rather than searching a long counter for every
symbol. Low-end ripple counters, returns and complete-range resets have
amortized constant work per symbol. A fixed number of run endpoints and
products are computed before their complete runs.

The same argument implements a move of a cardinality-R field in `O(RV)`
steps: for each value, its selected subsequence has the same remaining
field order at source and destination. One scratch stream and one output
accumulator suffice, and are reused for all R values. The algorithm does
not allocate R parallel tapes or streams.

For unequal dyadic widths with an arbitrary intervening gap G, exchanging
only fixed bit positions is insufficient: the number of bit slots before
the gap changes. The revised proof correctly uses individual cardinality-2
field moves around the gap. The exact orders are:

1. Move the Y bits in their original order immediately before the X block
   (or before G if X is empty).
2. Move the X bits in reverse order immediately after G.

For example `X0 X1 G Y0 Y1` becomes `Y0 Y1 X0 X1 G`, then
`Y0 Y1 G X0 X1`. Reversing those two move orders would reverse each
internal field. This was a real defect in the first explicit version;
it does not change the number of moves or the asymptotic bounds once
corrected. Splitting off the next bit leaves only a fixed number of
contiguous field blocks, so the tape/descriptor count remains uniform.

Local dyadic padding multiplies a rectangle's volume by less than four;
it never constructs a padded whole M-by-M square. Thus the arbitrary
rectangular fallback costs `O(u V_rect)` time and `O(V_rect)` space,
including the arbitrary gap and spectators.

## 2. Partition and total work

Retaining Q radix levels gives at most `(b-1)Q` actual intervals. If a
tail remains, its length satisfies `r/M < b^(1-Q) <= 1/(u+1)`.
The two residual rectangles `T x [M]` and `([M]\\T) x T` are disjoint,
cover every omitted pair, and occupy at most `2V/(u+1)`. Their generic
fallback therefore costs `O(V)` after summation. Their extraction and
merge add only a fixed number of full scans.

For a retained p-by-q pair, splitting the longer radix field into high
and low parts, one equal-width oracle call and one high-part field move
give the desired order. Both `p>=q` and `q>p` formulas in the proof are
correct, including exponents zero. The local invoice is

    V_pq F_b(min(p,q)) + O(b^abs(p-q) V_pq).

The weighted estimate is sound. For p>=q,

    a_p a_q b^(2p) = (a_p b^p)^2 * (a_q/a_p) < b M^2

whenever both digits are positive. It applies to all ordered level pairs,
with the symmetric argument when p<q. Their sum costs `O(b Q^2 V)`.
The more conservative `O(b^2 Q^2 V)` full-scan count dominates this term.
Oracle volumes sum to at most V, and monotonicity of F gives total oracle
work at most `V F_b(E)`.

All wrapper descriptor arithmetic has an absolute fixed polynomial degree
in the supplied bit lengths. When b<=M, these lengths are `O(log V)`;
the fixed-degree bound is at most `C V` with an absolute constant. Repeating
it per rectangle is covered by the already charged full-scan count.
For b>M, reading and preprocessing the potentially much longer radix is
retained separately, as in the theorem.

## 3. Visited space and oracle qualifications

Read-only input, output accumulator and a fixed number of local scratch
streams occupy `O(V)` cells. Only one oracle is active. Its actual input
volume is at most V, so its proportional term is at most `S_b V`, without
a wrapper factor b squared. Its additive bound must be maximized over
both actual exponents and actual volumes; the revised theorem does this.
An unjustified monotonicity substitution for D would be incorrect.

For each call, mark the visited interval boundaries on its fixed tapes,
clean that interval and restart from the same work origins. Boundary
maintenance costs a constant factor per actual transition. Cleaning and
head return cost at most the actual visited interval lengths, hence at
most a constant factor of the call's actual time plus its input length.
One need not scan a possibly very loose upper bound for D. Reusing these
marked regions bounds the union of visited cells, not just peak live data.

The premise requires one callable processor on a uniform fixed number of
tapes, with its own generation, retained setup and per-call costs charged
as stated. The wrapper does not prove a uniform processor from an abstract
family whose tape count or omitted setup depends on b. Similarly, the
conclusion preserves S_b; it does not establish an absolute proportional
space constant for an unproved local supplier.

## 4. Verification actually performed

The source checker was copied to an isolated replay directory and run:

```sh
python3 replay-no-padding/verify_no_padding_radix.py
python3 verify_rectangular_bit_moves.py
```

The first replay passed 65,008 parameter profiles, 47,463 nonempty-tail
cases, 230 unequal-field decompositions (504,006 symbols), and 1,790 full
wrapper permutations (8,705,970 symbols). Its 54 negative controls detect
omission of the unequal-field correction. It tests combinatorics with
explicit finite arrays, not the all-size tape-cost argument.

The independent named-bit checker verifies the actual sequence of elementary
moves for all widths 0 through 32: 1,089 layouts, including empty fields.
It rejects the earlier reversed-order prescription in 1,085 nontrivial
cases. This is needed because a final sort-based array test by itself
would not catch an incorrect prescribed elementary move order.

Both JSON outputs are preserved with checker hashes. No tape simulator,
full multiplier execution or Lean build was run.

## Decision

The corrected wrapper establishes the claimed reduction with

    V [F_b(floor(log_b M)) + O(b^2 Q^2)]

time and `O((1+S_b)V)` proportional visited space plus the explicit
additive maxima/setup. It removes the source's full-volume radix padding
from this particular conversion. The new ordinary-time expense and the
local processor's own space/precision obligations remain. It is an enabling
component, not a new complete overhead theorem.

Credits: Route A construction; source OpenAI tape framework; lead and
Route C independent gap/order/space checks; @CubeJerry; substantial
ChatGPT research assistance.
