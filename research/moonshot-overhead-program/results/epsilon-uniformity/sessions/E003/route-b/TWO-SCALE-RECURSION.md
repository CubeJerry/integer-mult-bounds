# Different arity schedules for interchange and Walsh

Status: **proved analytic and conditional physical transfer; source executor
premises under independent audit**. This note does not, by itself, establish
an unconditional new multiplication bound. In particular, no parameter is
substituted into an unquantified fixed-parameter `O` constant.

The distinction is consequential. Interchange has a polynomial local toll,
whereas Walsh also pays for calls to interchange. Using the same power-size
arity in both recursions does not control that second toll. The construction
below uses power-size arity for interchange and a smaller arity for Walsh.
Their jointly charged envelopes then lie on the same scale.

All logarithms are binary. For `y>=1`, put

```
Phi(y) = y^(2/3) [log2(y+2)]^(1/3),
Psi(y) = sqrt(y log2(y+2)).                              (T1)
```

The target implication is

```
T(n) <= n sqrt(L(n)) 2^(O(Phi(x))),
L(n)=1+log2 n,  x=log2 L(n),
visited cells <= C n,                                   (T2)
```

for one fixed exact deterministic finite-alphabet multitape machine.
This is stronger than the stationary profile scale
`log H=O(x^(3/4)(log(x+2))^(1/4))`, provided the physical premises below
are supplied. The comparison is between explicit programme envelopes,
not a priority claim against the paper's unspecified `o(1)`.

## 1. Exact sources and what is imported

OpenAI pin: `3344da59991ed94f9ba711217b29c1d760badfa6`.

* Tape `interchange.tex`, `thm:interchange`: fixed-template recurrence,
  arbitrary spectator fields, occupied reserves, and depth-first storage.
* Tape `walsh.tex`, `lem:tape-walsh`: full-rate batches on even widths,
  fixed-precision numerical arrays, source coordinate changes and unitary
  completed children.
* Fourier `kernel.tex`, `eq:kernel-pencil-cost` and
  `eq:kernel-template-saving`: shared endpoint transforms and the distinct
  ordinary middle coordinate changes for every query.
* Tape `integers.tex`, `eq:integer-budget`, `lem:synchronized-short` and
  `thm:integer`: the `Nk=Theta(n)`, `k=Theta(log n)` short-axis reduction.

Programme predecessor `a2d9c4b00c02dadf7bdc970acf9190dfabf9ec32`:

* `routes/A/fixed-field-extraction-theorem.md`, Q2--Q5, and
  `routes/B/characteristic-two-label-geometry.md`, C2-10--C2-11;
* the rational Walsh construction and quantitative operation list in
  `routes/B/pairwise-newton-division.md` and
  `routes/B/polynomial-auxiliary-cost-audit.md`;
* E002 `route-c/polynomial-interchange-invoice.md`, I1--I5, and the
  height, succinct-row, spectral and radix suppliers it cites;
* E001 `route-c/NONSTATIONARY-RECURSION.md`, C1--C4. The new result is
  not the generic recurrence-unfolding identity already proved there.

The concurrent S003 supplier at
`c65aac1156a46d10c0ef2aa36fd846c7a93518e1`,
`sessions/2026-11-26-S003/route-b/explicit-dyadic-geometry.md`, B2,
is a simpler address realization: fixed radix three works for every
template. E003 Route A supplies the explicit constant-space pencil
schedule, guarded stream primitives, comparison labels and full-rate
binary field packing. Route B's separate supplier review records the
proofs actually read and its isolated exact geometry replay.
Route A's `ALL-ARITY-LABEL-PROFILE.md` supplies the integer parameter
rule and a sufficient guard for every large arity, independently of
the earlier fixed-inverse-exponent trial subsequence.

Source fixed-parameter correctness and the cited finite identities are
imports. The separate E003 physical audits must verify that their new
uniform interfaces retain every paid operation.

## 2. Source-local call profiles

### Interchange profile

Write `z=log m`. With a power-of-two distance `d`, the retained source
label bound is

```
log2[D_I(1+lambda_I)] <= 3z/d + 10d^2 log2(4z).
```

Choose `d` within a factor two of
`(z/log2(z+2))^(1/3)`. This is an integer algorithm: take
`z_hat=ceil(log2 m)`, `v=ceil(log2(z_hat+2))`, the least power
of two at least two with `d^3 v>=z_hat`, and
`t=2+ceil(z_hat/d^2)`, `q=2^t`. Route A's all-arity lemma proves,
for every `z_hat>=2^40`, the exact guards `m r_*/N<=1/4`,
`N<=m^5`, `D_I<=sqrt(m)`, and
`log2[D_I(1+lambda_I)]<=64 z_hat^(2/3)v^(1/3)` for the new
dyadic dimension. Thus for all sufficiently large `m` it gives

```
D_I = m^o(1),  N<=m^5,
Lambda_I(m) <= sqrt(m) 2^(C_I Phi(log2 m)).              (I1)
```

The constant `C_I` includes E002's larger predictor window, the factor-two
batch padding, the reserve calls, E003 A's revised `2^19` schedule
allowance, and the additional absolute factor of S003's explicit dyadic
endpoint lists. The dyadic ambient dimension is twice the preceding
coarse dimension bound, which adds only an absolute constant to the
displayed logarithmic estimate. Exact old numerical admission constants
are not reused silently. Formula I1 is a
bound on the exact sum of child payload volumes divided by parent volume,
after the full finite repair is completed. It is not a circuit-only count.
This is the source's existing optimized local profile; no novelty is
claimed for its two-term balance.

### Walsh profile

For the rational binary construction, choosing its even label parameter
within a factor two of `sqrt(z/log2(z+2))` gives

```
2m <= A_m <=4m,  W_m<=m^C,
sigma_m/W_m <= sqrt(A_m) 2^(C_F Psi(log2 m)).            (W1)
```

Use the same integer square-root and even rounding as the predecessor's
polynomial operation audit. This follows from Q5's logarithmic excess
`2z/L+L log2(3z)+log2(3L)+O(1)`. The count includes finite repair leaves;
the completed rational batch width is polynomial in `m`.

Ordinary local operations still number at most `m^C` per original
volume, and each physical coordinate change can call interchange on
fields of width at most the current active width. This polynomial local
cost is retained. The free-rectangle proof shares Fourier endpoints;
it does not say that all middle coordinate changes are free on tapes.

## 3. Physical premises, stated separately from the conclusion

Choose one absolute integer `C` large enough to dominate the following
finite bounds. They concern a specified source template grammar, not an
oracle for a near-root multiplication algorithm.

**P-I: local interchange executor.** At active radix width `e` and arity
`m`, with complete positive spectator ranges, the finite identity is
correct, has child width

```
f = floor((e-ell_m)/(m+2a_m)),
a_m=D_I-2,  ell_m=ceil(log_b W_I,m),                    (P1)
```

Here `W_I,m=d_m W_E,m` is the completed **binary** row count of the
interchange template: `d_m` is its finite-field degree over F2 and
`W_E,m` its completed field-row count. Only
`log W_I,m<=m^C` is needed; it must not be confused with the
polynomial numerical Walsh batch width `W_m` in W1. Full-rate packing
has exactly `W_I,m` input bit rows and the same number of output bit
rows; the child's sum-of-volume ratio remains I1. Leading padding by
this binary count is already the factor at most two paid in I1.

At nonbase nodes satisfying
`e>=m^(C+2)`, all nonrecursive work costs at most

```
V m^C (1+log(u+2))^C + 2^(C m^C),                      (P2)
```

where `u` is the binary root width and `V` is the encoded payload volume.
The primary implementation uses S003's fixed radix `b=3` and E003 A's
full-rate binary packing with a local field of `O(log(m+2))` bits.
The following slightly looser statement also permits
`log b=O(log(u+2))` and a common root field of `O(log(u+2))` bits.
In either case, all interpretation, arithmetic, comparisons, masks, record/row
metadata, address changes, head returns and cleanup are included.

The local workspace uses at most an absolute number of payload copies
plus `2^(C m^C)+poly(log V,log u)` extra cells. It does not use
`m^C V` visited cells. Main-child grouped payloads shrink by a fixed
factor at most `2/3`; before a full-volume reserve child, merge and
clear all parent payloads and template workspace, retaining descriptors
only. Child templates are regenerated with their own local bill; a giant
root description is not rescanned per datum.

For the primary implementation, dyadic coordinate lists make all
templates compatible with radix three; no prime-menu premise is needed.
The more general alternative uses Theorem R of `COMMON-RADIX-MENU.md`.
Direct radix-digit swaps use its elementary Lemma D (constant cost when
`b=3`). The whole construction acts on one fixed binary alphabet.
E003 A's full-rate packing treats a parent's record as arbitrary binary
payload, so a child's chosen field causes no multiplicative bit-volume
expansion. Alternatively `COMMON-CHECK-FIELD.md` supplies one field for
the whole menu with an explicitly charged initial encoding factor.
The changes of `m` and of the check field occur only when a completed
spatial-permutation call descends to its smaller spatial width. The
local predictor's internal `F`/`F^-1` repair descendants retain that
node's `m`, field, row coordinates and exact algebra throughout their
finite unrolling. A fresh template is never substituted for one of
those internal algebraic maps.

**P-W: local numerical executor.** The rational batch in W1 accepts
arbitrary independent numerical rows with complete spectators. Its
whole nonrecursive bill at active width `a` and outer record parameter
`k` is at most

```
V m^C (1+log(k+2))^C [1+I(a,k)]
  + 2^(C m^C) (1+k)^(m^C),                             (P3)
```

where `I(a,k)` is the proved bit-volume cost of interchanging fields of
at most `a` bits. The factor `m^C` includes all middle-query coordinate
maps, packed-XOR/controlled maps, row preparation and repeated scans.
No child Walsh volume is inflated by its temporary keys or tags.

The number of actual children/ordinary array operations per local node,
including finite repair unrolling, is at most `m^C`. A compact local
description has size at most `m^C`; coefficient height is at most `m^C`.
The logarithmic gain bound `m^C` applies to every input-to-intermediate
map and to propagation of an additive error from any intermediate array
to every later local array or output, with completed children counted
as unitary operations. It is not merely a bound on the completed target.
The polynomial operation count times the polynomial coefficient/dimension
height proves this after increasing C. Exact numerical
preparation, including per-key coefficient generation, has the explicit
additive profile in P3 with one fixed absolute `C`; its degree in `k`
is allowed to grow as `m^C`. Completed numerical children and
the target are normalized unitaries.

For all sufficiently large `k`, temporary metadata fits the `Theta(k)`
numerical record width; a fixed number of payload arrays and marked
reusable regions gives `V(1+log(k+2))^C` visited space plus the additive
setup workspace. Descents park geometrically shrinking payloads, and
siblings reuse regions. These are bounds on all visited cells.

**P-O: outer source reduction.** The exact short-axis/CRT/carry reduction
retains its original shape and numerical correctness with absolute
`Theta(k)` record widths once the proved interpolation/rounding budget
below is supplied. Its number of record-permutation/Walsh layers and
other logarithmic factors is `(1+log k)^C`; its additional preparation
is `poly(k)` with an absolute degree. These are the unchanged operations
of the source integer proof, not a new near-root arithmetic premise.
`OUTER-REDUCTION-TRANSFER.md` checks this premise directly against the
full pinned permutation, Walsh and integer source files: packed XOR,
bit-position moves and controlled small-block permutations use the
interchange envelope linearly, while outer setup and precision constants
are absolute. The remaining physical admission gates are P-I and P-W.

P-I's guarded payload storage and P-W's exact physical composition are
the current admission gates. Their polynomial generation alone would
not supply them.

## 4. Power arity for interchange

Take a fixed integer `r>8(C+2)` and `beta=1/r`. At integer width `e`
choose the largest odd integer

```
m(e) <= floor(e^(1/r)).                                (I2)
```

For sufficiently large `e`, `e^beta/3<=m(e)<=e^beta`.
Small widths use the direct digit routine. The primary dyadic realization
uses the same radix three at every node. In the general alternative,
the binary root's menu contains all odd parameters through
`floor(u^(1/r))`.

By I1, `a_m=o(m)`; by the menu bound, `ell_m<=1+C m^C=o(e)`.
Enlarge a fixed base threshold `E` so that, for all `e>E`, P1 obeys

```
e/(8m) <= f <= e/m,     2<=f<e.                        (I3)
```

The same choice makes `e>=m^(C+2)`. Since `beta C<1`, the additive
constructor cost is at most `2^(e/2)` for large `e`, and is absorbed
by local payload `V>=b^(2e)>=2^(2e)`. For bounded `e`, direct swaps
cost `poly(log u) V` with an absolute number of payload copies.

Let `y_i=log2 e_i` along any recursive width chain. From I2--I3, after
enlarging `E`, there are fixed `0<q_-<q_+<1` such that

```
q_- y_i <= y_(i+1) <= q_+ y_i.                         (I4)
```

Normalize time per volume by `sqrt(e)`. The normalized child coefficient
is at most `2^(C_I Phi(log m))`, because `f<=e/m`. The accumulated
logarithmic multiplier is bounded by

```
C_I sum_i Phi(log m_i)
 <= C' sum_i Phi(y_i)
 <= C' Phi(y_0) sum_i q_+^(2i/3)
 = O(Phi(y_0)).                                        (I5)
```

The second inequality uses monotonicity; the third follows since the
logarithmic factor decreases with `y_i`. The normalized local toll is
at most `poly(log u) e_i^(-eta)` for a fixed
`eta=1/2-beta C>0`. Successive `y_i` have a fixed positive separation
above `log E`, so the sum of `2^(-eta y_i)` is bounded by an absolute
geometric series, independent of the root. The normalized terminal
cost is `poly(log u)`. Exact recurrence unfolding therefore proves

```
I(u) <= sqrt(u) 2^(O(Phi(log2(u+2)))),                  (I6)
```

after absorbing polynomial logarithmic factors into the displayed
exponential. Initial bounded binary padding, field packing and output
unpacking are included by P-I. The fixed-three realization has padding
factor below nine, with no radix search. The general alternative charges
Theorem R's selector too. The result has at most a
`V poly(log(u+2))` visited-space coefficient; primary full-rate packing
avoids even the root field encoding multiplier. The looser bound is
retained until the final chunk wrapper and is not called constant.

## 5. Smaller arity for Walsh

Set `y=ceil(log2(a+2))`, `v=ceil(log2(y+2))`, and choose

```
z = ceil(cuberoot(y^2 v)),   m = 2^z+1.                 (W2)
```

These are integer algorithms. `z=Theta(Phi(log2(a+2)))=o(log a)`.
For a sufficiently large fixed base threshold, W1 gives `A<=4m<=a/4`.
Use even child width

```
f = 2 floor(a/(2A)).                                   (W3)
```

The remaining fewer than `2A` bits are transformed directly. Their
cost belongs to P3's polynomial-`m` local term. For nonbase `a`,

```
a/(2A) <= f <= a/A,       a^(1/2) <= f < a,
log2 a-log2 f = z+O(1).                                (W4)
```

Thus active logarithmic width decreases by `Theta(Phi(y))`, rather than
a fixed fraction of `y`. The outer record width `k` remains fixed.

### Leading-row padding at all variable scales

The width chain W3 and its templates depend only on the root selected
width. Precompute that finite chain. If its batch widths are
`W_0,...,W_(D-1)`, pad the root leading spectator count to a multiple of
`B=product_i W_i`. At level `i` the leading count is divisible by
`product_(j>=i) W_j`; split it by `W_i`, exactly as in the source.

Since `W_i<=m_i^C` and `f_i<=a_i/A_i` with `A_i>=m_i`,

```
sum_i log m_i <= log a_0,     log B <= C log a_0.        (W5)
```

Hence `B<=a_0^C<=k^C`. Source selected widths satisfy
`a_0<=c k/log(2+k)`, so root spectators number at least `2^(k/2)`
for all sufficiently large `k`. Initial padding is at most two and
all deeper splits are exact. No accumulated padding factor or free
input rows have been omitted. The added spectator rows are arbitrary
padding and are removed after the completed transform.

### Summing the normalized Walsh loss

Let `Y_i=log2 a_i`. W1 and W4 bound the normalized child coefficient by
`2^(C_F Psi(z_i+O(1)))`. For large `Y`, its successor satisfies
`Y/2<=Y'<Y`, and the explicit derivative of Phi gives

```
Phi(Y)-Phi(Y')
 >= c (Y-Y') Y^(-1/3) [log2(Y+2)]^(1/3)
 >= c' Y^(1/3) [log2(Y+2)]^(2/3)
 >= c'' Psi(z+O(1)).                                  (W6)
```

To justify the first inequality, on `[Y/2,Y]` the derivative of Phi
is at least a positive absolute multiple of
`Y^(-1/3)[log2(Y+2)]^(1/3)`. For the second use
`Y-Y'=Theta(z)` and `z=Theta(Phi(Y))`. For the third,
`log(z+2)=Theta(log(Y+2))`. Each constant is fixed; the bounded
initial range is absorbed into the base. Summing W6 telescopes:

```
sum_i Psi(z_i+O(1)) = O(Phi(Y_0)).                     (W7)
```

By I6 and P3, the normalized local toll at width `a_i` is at most

```
poly(log k) 2^(C' Phi(Y_i)).                           (W8)
```

The polynomial `m_i^C` is essential here: `log m_i=Theta(Phi(Y_i))`,
so it fits W8. In contrast, choosing `m_i=a_i^beta` would put a term
`Theta(Y_i)` in that exponent and would not prove this bound.

The depth is at most `O(log a_0)`, because each decrease in W4 is at
least one. Unfold the nonnegative recurrence. Every toll is multiplied
by a prefix of the products bounded in W7, and `Phi(Y_i)<=Phi(Y_0)`.
The depth and `poly(log k)` factors are absorbed into
`poly(log k)2^(O(Phi(Y_0)))`. Therefore

```
W(a_0,k) <= poly(log k) sqrt(a_0)
             2^(O(Phi(log2(a_0+2))))                  (W9)
```

per numerical bit volume, apart from the additive setup charged next.
The source's initial/final bit-position permutations obey the same
bound with `a_0` replaced by `k`, using I6.

## 6. Generation, nodes, precision and visited space

Along any Walsh path, W5 gives `sum log m_i<=log a_0`. Since each local
node has at most `m_i^C` actual children and operations, the whole tree
has at most `k^C'` nodes and array operations after increasing a fixed
exponent. This remains true with the finite repair descendants counted
inside their local program. It is not an assertion of constant work
per node.

The largest `m` is `2^(O(Phi(log k)))=k^o(1)`. Hence all additive setup
and finite-data generation, even if repeated at every node, cost at most

```
k^C' 2^(C m_max^C) (1+k)^(m_max^C)
       = 2^(k^o(1)) = o(2^k).                         (G1)
```

The same bound pays their visited storage. It is permissible to prepare
data before processing payloads, provided the executor accesses only
its compact local instructions during streaming. A whole `2^(m^C)`
table scan per record would violate P-W and is not covered by G1.

Before choosing the fixed format, explicitly test
`k>=m_max^K_2` for a sufficiently large absolute integer `K_2`.
This is E002's numerical guard, enlarged to dominate the local gain
and event exponents in P-W. In particular
`C m_max^K log2(k+2)<=k` follows from this guard after enlarging
`K_2`, using `log2(k+2)<=3sqrt(k)`. A failed guard selects the
exact schoolbook fallback. Since `m_max=k^o(1)`, it succeeds at
every sufficiently large outer width. Time/space caps alone would
not detect numerical inaccuracy and are not substituted for this test.

Local logarithmic numerical gain is at most `m_i^C`. Summing these
along the two ancestor paths through which an error can propagate gives
at most `k^o(1)`, since path depth is `O(log k)`. Completed children are
unitary; gain is not multiplied through every completed branch. There
are polynomially many array operations, each rounding error is at most
`poly(k) sqrt(N) 2^(-p)` plus its coefficient-rounding term, and the
input norm is `2^(O(k))`. Taking `p=C_0 k` with one fixed absolute
constant therefore controls every intermediate/output error by
`2^(-Dk)` for any fixed required `D`. Integer parts also use `O(k)`
bits, because ideal intermediate norms have logarithm `O(k)+k^o(1)`.
All bounded initial values are handled by the fixed fallback. Exact
short products and coefficient preparation are the charged operations
in P3; no unbounded-precision unit-cost arithmetic is used.

For space, P-I gives geometrically parked main payloads, descriptor-only
full-volume reserves, and local setup absorbed into current volume.
The common radix is not changed inside that recursion. P-W gives
geometrically parked batch/finite-repair payloads and fixed marked
regions, plus G1 setup. Sequential siblings reuse the same intervals.
The complete digit routine consequently visits at most

```
C n (1+log2 L(n))^C                                    (G2)
```

cells. This is still an input-dependent coefficient and must be reduced
by the next step; G2 alone is not the requested uniform `O(n)` bound.

## 7. One common-space exact multiplier

Apply P-O to W9/I6/G1. Since `Nk=Theta(n)`, `k=Theta(log n)`, and
only polynomial-logarithmic extra layers occur, the resulting fixed
digit routine has time

```
n sqrt(L(n)) (1+x)^C 2^(C Phi(x)),                    (M1)
```

and space G2. All parameters come from integer width calculations,
finite constructors and guarded searches. Shape failures use the exact
fallback; the source prime theorem guarantees eventual successful shape.

To obtain one absolute visited-space cap, let `r_n` be the least power
of two at least `8C(1+ceil(log2 Lhat(n)))^C`, where
`Lhat(n)=1+ceil(log2 n)`. Split each operand into `r_n` chunks of
length `u_n=ceil(n/r_n)`, and run the same digit routine sequentially on
all chunk pairs. If `r_n>n`, use schoolbook multiplication directly;
this is an explicit branch and applies only to a bounded initial range.
Choose the fixed wrapper constant large enough to pay
its input/output, carry and marked-region overhead. Since
`x(u_n)<=x(n)+O(1)`, each core space bill is at most its allocated
constant fraction of `n`, for sufficiently large `n`; bounded lengths
use schoolbook. Additive retained setup is already charged in G2.

The rowwise positional assembly has exact time `O(n r_n)` and the
`r_n^2` products cost at most `O(r_n n)` times the per-bit bound at
`u_n`. Thus the wrapper multiplies M1 by only a polynomial in `1+x`.
Since `log(1+x)=o(Phi(x))`, this proves T2. A global marked-region
and execution cap with exact fallback handles every input length
without knowing any unstated asymptotic cutoff; eventual inequalities
prove that those guards no longer fail.

This establishes the **complete conditional implication** P-I/P-W/P-O
to T2, including generation, physical movement, precision, full output,
fallback and a uniform bound on all visited cells. It is not an
unconditional admission of the remaining executor premises.

## 8. What the mechanism changes

The stationary E002 balance pays `log m=O(J^3 log J)` once as a
proportional prefactor and `x/J` throughout the input. Its optimized
scale is `x^(3/4)(log x)^(1/4)`. Interchange instead uses fresh local
parameters whose logarithmic call losses form a geometric sum. Walsh
uses its independently better square-root local-loss profile to choose
a smaller arity, large enough to limit accumulated recursive losses
but small enough to pay its genuine polynomial routing toll. No toll
is erased and no `O_m` coefficient is declared uniform.

Open next questions are sharply located: close P-I's guarded constant
payload-space compiler and P-W's physical operator/precision composition;
independently review the leading-row product and the recorded outer
source substitutions. The optional common-radix menu is unnecessary
for the primary fixed-three construction. Improving this recursion toward polynomial
`x` or constant overhead would require better local call loss or a new
handling of Walsh's middle-query routing, not merely a larger fixed J.

Credits: @CubeJerry; the OpenAI manuscripts and cited predecessors;
E001 nonstationary calculus/prime selector; E002 compact execution and
separated preparation; substantial ChatGPT multi-agent assistance.
No formal-kernel proof, full multiplier execution or human refereeing
is claimed.
