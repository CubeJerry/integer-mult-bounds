# Linear dependence on the space-normalizing chunk count

Status: **proved source-specific quantitative implementation lemma**. This
refines the `O_r(n)` accumulation/gathering term in the source; it does not
provide bounds on the source's unknown program-dependent constants.

**Overlap and attribution correction.** Concurrent programme session S002,
`routes/A/scheduler-and-chunking.md`, Propositions A3–A4, already proves an
`O(nr)` wrapper by diagonal accumulation with an amortized high carry and
gives a stronger space ledger separating proportional space `c_j u` from
additive description space `d_j`. This note independently obtains the same
linear dependence by rowwise single-digit carries. It is an alternative
proof, **not a new asymptotic improvement over S002**. The more informative
S002 `c_j u+d_j` ledger should be used when its separate constants are
available; the special case here intentionally follows the published
`c_j(u+1)` contract and can overcharge fixed description space.

Source: `openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`, tape paper,
`build/uniformity.tex`, subsection “Scheduling within linear space.” The
source forms `r^2` digit products and gives an unspecified `O_r(n)` cost for
gathering and accumulation. The construction below realizes that cost as
`O(r n)` with an absolute constant, on a fixed number of physical tapes.

## C1. Rowwise chunk multiplication

Let `1 <= r <= n`, let `u=ceil(n/r)`, and let `B=2^u`. Suppose one fixed
interpreter can correctly multiply two `u`-bit operands in `t(u)` actual
steps, using at most `s(u)` visited work cells, including any repeated setup,
cleanup and return to its documented input/output head positions. There is
a fixed-tape wrapper which multiplies two `n`-bit
operands in

```
r^2 t(u) + O(r n)
```

actual steps and visits at most `s(u)+O(n)` cells in fixed reusable work
regions. The implicit constants are independent of `n,r` and the candidate
program. Its candidate interpreter and any immutable description tape are
those included in `t,s`; no unit-cost universal interpretation is assumed.

### Construction and proof

Reverse the inputs into least-significant-digit-first order, pad to `r`
base-`B` digits, and initialize `2r` zero accumulator digits. These streams
have lengths `ru <= n+r <= 2n` and `2ru <= 4n`, and their initialization
costs `O(n)`.

For rows `i=0,...,r-1`, hold `a_i` in a `u`-bit buffer, reset a carry `c=0`,
and scan `b_0,...,b_(r-1)` sequentially. At column `j`, call the candidate
multiplier on `a_i,b_j`. With the accumulator head at digit `z_(i+j)`, form

```
t = a_i b_j + z_(i+j) + c,
z_(i+j) = t mod B,
c = floor(t/B).
```

If `0 <= a_i,b_j,z_(i+j),c <= B-1`, then `0 <= t <= B^2-1`; hence the
carry remains a single `u`-bit digit. Each local addition and split costs
`O(u)` physical steps with standard bitwise addition and low-end amortized
binary counters. There is no possibly long carry propagation across the
whole accumulated product.

At the end of row `i`, set `z_(i+r)=c`. This digit was zero: previous rows
have touched only digits through `i+r-1`. The usual positional expansion
of this row recurrence proves that the accumulator now contains
`sum_(h=0)^i a_h B^h * sum_j b_j B^j`. After the last row it is the exact
product. The invariant also proves that no update outside the two local
digits is being omitted.

During a row, both the `b` stream and the accumulator move sequentially
over `r` digits. Rewinding `b` and returning the accumulator to the next
row's starting digit each cost `O(ru)=O(n)` per row. The `a` input advances
by one digit per row. Preparing operand copies, clearing wrapper buffers,
accessing the held digit and maintaining the local carry cost `O(u)` per pair
in addition to the already charged `t(u)`. Candidate scratch cleanup and
candidate head returns are part of `t(u)`, not assumed to cost `O(u)`. The loop
counters can be advanced amortized in `O(1)` steps per increment, with their
initializations and returns included in the row scans. Thus all wrapper
work is `O(r^2 u + r n) = O(r n)`. Final trimming and reversal cost `O(n)`.

All streams and buffers live in fixed regions of total size `O(n)`.
Candidate calls reuse the same work region, so the claim counts the union
of visited cells. The number of extra tapes is absolute. This proves C1.

## C2. An explicit space-normalization transfer

For a candidate `j`, suppose the *complete interpreted* `u`-bit run has,
for all integers `u >= U_j`,

```
t_j(u) <= a_j u (1+log_2 u)^theta_j,  a_j >= 1, theta_j >= 0,
```

and at every length its physical workspace, including generation, is at
most `c_j(u+1)`, where `c_j >= 1` is an integer. Let `r_j` be the least
power of two strictly larger than `2c_j`. Then

```
2c_j < r_j <= 4c_j,
k_j=log_2 r_j <= 2+log_2 c_j,
N_j = max(4c_j, r_j U_j).
```

For every integer `n >= N_j`, C1 finishes correctly within a common marked
candidate-work interval of `n` cells per tape and has time

```
t_attempt,j(n) <= C a_j c_j n (1+log_2 n)^theta_j
```

for one absolute constant `C`. The remaining input, accumulator and
controller regions have fixed `O(n)` allowances.

Indeed `r_j <= n`, `u=ceil(n/r_j) >= U_j`, and

```
c_j(u+1) <= c_j(n/r_j+2) < n/2+2c_j <= n.
```

Also `r_j^2 u <= 2r_j n` and `u <= n`. Substituting into C1 and using
`a_j >= 1`, `theta_j >= 0`, `r_j <= 4c_j` proves the time bound. Small
lengths and other chunk counts retain the source's abort/fallback behavior.

### Consequence for the quantitative ledger

The source family can use sufficient constants of the form

```
A_j <= C a_j c_j,
b_j <= log_2(1+log_2(max(4c_j, 4c_j U_j))).
```

This statement is only as effective as the supplied `a_j,c_j,U_j`.
No bound on their growth in `j` has been proved here. Nevertheless it
isolates the exact normalization loss: a linear factor in the candidate's
space constant is sufficient; an arbitrary quadratic gathering invoice
is unnecessary.

Combined with B2 of `binary-length-schedule.md`, the multiplicative
certificate penalty for a selected candidate is bounded by an absolute
constant times

```
a_j c_j q (1+log_2 c_j) ell(q)^3
                 ell(ceil(2+log_2 c_j)+1)^3,
```

where `j=f(q)`. The separate feasibility threshold still contains `U_j`
and `c_j`; it must not be discarded when choosing `j=j(n)`.

## Limits and open next questions

This is ordinary exact digit multiplication with an efficient physical
layout, not a new multiplication exponent. The candidate can regenerate
its program on every digit call: that cost remains inside `t_j(u)`.
Retaining an immutable generated description may save additional setup,
but C1 does not assume or credit that saving.

The consequential next question is whether the source's live-stream and
descriptor recurrences yield a computable small `c_j` and whether an
efficient macro interpreter can remove generic full-transition-list scans
from `a_j`. Neither question is answered by the rowwise carry invariant.

Attribution: @CubeJerry; OpenAI's November 24, 2026 tape construction;
classical positional multiplication; concurrent S002 Propositions A3–A4
for the same linear chunking bound and the sharper separated-space ledger.
Prepared with ChatGPT multi-agent
assistance. Finite arithmetic checks are complementary to the proof, not
kernel verification or a measured tape implementation.
