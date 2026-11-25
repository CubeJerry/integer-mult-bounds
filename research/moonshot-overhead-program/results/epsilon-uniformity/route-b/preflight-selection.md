# Linear-budget preflight: move search loss into applicability

Status: **proved conditional fixed-tape selection theorem and complete
conditional rate transfer**. A source-wide sound time/space billing compiler
has not been constructed. The hypotheses of the endpoint corollary have not
been proved for the published multiplier, and several are deliberately
stronger than its fixed-parameter assertions.

The idea of searching for quickly evaluated time bounds before committing
most work to a program is established prior art. Hutter's Theorem 1 (2002)
has a program-independent multiplicative factor on a proved time bound,
plus program-dependent additive terms for finding/evaluating that bound.
The result here is a smaller, family-specific construction with an explicit
linear preprocessing budget, a fixed physical executor, fixed tape count,
and a uniform bound on **all cells ever visited**. It is not a claim to
invent that general search principle.

Primary reference: Marcus Hutter, *The Fastest and Shortest Algorithm for All
Well-Defined Problems*, IJFCS 13(3), 431–443 (2002), Theorem 1 and Sections
2, 4–6; [author's manuscript](https://www.hutter1.net/ai/pfastprg.pdf),
[arXiv:cs/0206022v1](https://arxiv.org/abs/cs/0206022v1).

## 1. An explicit, falsifiable plan interface

Fix two deterministic finite-alphabet multitape machines, a **preflight**
`P` and an **executor** `E`. Their programs, tape counts and alphabets are
fixed once, independent of `j,n`. The input to `P` is the binary pair `(j,n)`.
It uses no bits of the numerical operands. It may reject, remain unfinished,
or output a finite plan `D`, an integer time bill `U`, and a finite resource
derivation which a fixed checker accepts.

The required soundness contract is:

> Every accepted plan for length `n` makes the **actual fixed executor `E`**
> compute the full exact product for every two `n`-bit inputs in at most `U`
> physical steps, including operand loading, template/table access,
> interpreter dispatch, rounding, carries, head movements and output. All
> visited cells lie in a fixed number of regions of at most `C_* n` cells,
> for one constant `C_*` independent of the plan. Its description and every
> retained table are included in this spatial contract.

This is a sound-family interface, not an oracle for arbitrary program
termination. A concrete implementation must specify its legal plan grammar
and prove the checker sound. For example, a legal derivation may combine
proved bills for streaming primitives by sequential addition, bounded
iteration, and well-founded recursive calls, with explicit region reuse and
parked-frame bounds. A purported certificate consisting only of the sentence
“this program runs fast” does not meet the interface.

Preflight cost `g_j(n)` includes generating the template, determining and
checking the data shape, computing enough numerical precision, writing the
description and derivation, checking it, and returning heads to the declared
positions. Treat a nonreturning/rejected preflight as `g_j(n)=infinity` for
the corresponding plan. No useful upper bound is assumed at this stage.
Executing the accepted plan is a separate operation; work not actually done
by `P` must be included in `U`.

The executor itself may interpret descriptions. Its physical interpretation
cost is then part of `U`. The theorem never multiplies an abstract candidate
step count by a silently program-independent simulation constant.

## 2. The selection theorem

Let `ell(z)=floor(log_2 z)+1` and define

```
c(j) = ell(j)+3ell(ell(j)),
w_j = 2^c(j) <= 16 j ell(j)^3,
e_j(n) = g_j(n)+ceil(log_2(n+2))+1.
```

The `log n` term pays for comparing an offered integer bill against the
current best bill. The machine starts with a fixed correct schoolbook plan
whose bill `U_sb(n)=C_sb(n+1)^2` is computed with elementary binary arithmetic.
Offers with a larger bill are ignored. Thus a retained bill always has
`O(log(n+2))` bits.

**Theorem P1.** There are absolute constants `C_0,C_1`, and one fixed
deterministic multitape machine `M`, such that `M` always computes the exact
full product and visits `O(n)` cells. For every input length `n`,

```
T_M(n) <= C_1 n + C_1 min(U_sb(n),
       inf { U_j(n) : C_0 w_j(e_j(n)+1) <= n }),                 (P1)
```

where the infimum ranges only over accepted preflights and is `infinity`
when empty. `C_0,C_1` depend on the fixed machines and plan interface, never
on `j,n` or the accepted plan. The time spent generating, comparing,
installing and discarding plans is fully included.

### Proof: an actual preprocessing algorithm

Read and preserve the inputs, compute their length in `O(n)` steps, and
prepare a constant number of marked work regions, each of length `O(n)`.
Initialize the best plan to schoolbook. Run bounded rounds of *preflight
search only*. In round `s`, for each `j` with `c(j)<=s`, run `P(j,n)` from
the beginning for at most `2^(s-c(j))` steps. All finite construction and
checking is interrupted on timeout or a region crossing. An accepted offer
is considered only after its entire output and checker run are complete.
Copying the binary length `n` to an attempt, or reading it from a preserved
length tape and returning that head, belongs to this same budget. An attempt
with too few steps to initialize its input simply times out. Only the first
scan of the two numerical inputs is performed outside the preflight budget.

As in B2 of `binary-length-schedule.md`,

```
sum_j 2^(-c(j)) = 1/12,
sum_j ell(j)2^(-c(j)) <= 1/4.
```

Binary-length enumeration and low-end clocks therefore take `O(2^s)` actual
steps per round. In this preflight variant the final bill comparison costs
`O(log(n+2))`; charge it to a completed preflight by requiring that its
allocated budget also cover this operation. Formally enlarge `P` into a
fixed offer routine that reserves these comparison steps and keeps no offer
unless they finish. A successful offer routine has time `O(e_j(n))`.

An accepted replacement is copied into a second best-plan region before a
flag swaps which region is authoritative. A timeout during copying leaves
the previous best intact. The copy costs at most a constant times the
preflight output length, hence at most a constant times its successful
runtime. Erasing a superseded plan is charged amortized to the earlier copy
which created that plan; each copied bit is erased at most once. Finite
metadata and bill comparisons are included in the offer routine. The two
best-plan regions, current preflight regions and original inputs use a
constant number of tape intervals. There is never an array of all completed
plans.

It follows that there is an explicit implementation constant `C_R` for
which every prefix through round `s` costs at most `C_R 2^(s+1)`, including
all pending cleanup. Complete only those rounds whose bound is at most a
fixed fraction of `n`. If no positive round fits, use the initial plan.
One can alternatively stop a global amortized binary clock and finish
bounded cleanup; either convention costs `O(n)` and preserves a complete
best plan.

A spare best-plan region is cleared before it is reused; after a replacement,
its old contents are erased as the amortized cleanup just charged to their
earlier installation. The authoritative copy remains intact throughout.
A successful offer of cost `O(e_j(n))` appears by round
`c(j)+ceil(log_2(C(e_j(n)+1)))`. For a sufficiently large absolute `C_0`,
the condition in (P1) puts this round inside the allowed preprocessing
prefix. The final best bill is no larger than every such `U_j(n)`.
Install that one plan for `E`, if its input interface needs a copy, and
return its exact output. Installation costs `O(|D|)<=O(n)` and is included
in the initial/additive allowance, or in the plan's stronger bill if already
specified there. Soundness gives
both its time bill and its uniform region bound. The preprocessing visited
at most a fixed number of `O(n)` regions and the execution does likewise;
the union is still `O(n)`. Adding the initial and preprocessing cost proves
(P1), including every input length by the schoolbook default. ∎

**Why this is not a free selector.** The eligibility condition retains the
actual preflight cost and its search weight. A slow generator simply will
not supply a candidate at that length. There is no assumption that the
machine knows `g_j`, a threshold, or the minimizing index in advance. It
runs the stated bounded computations and compares the integer bills they
actually finish.

## 3. A complete conditional transfer on the polylog-log scale

Here `L(n)=1+log_2 n` and `x=log_2 L(n)`. The following hypotheses all refer
to the same fixed `P,E`, the same description encoding, the same checker,
and its actual physical tape model.

For every integer `j>=1`, assume an accepted plan exists at all `n>=N_j`.
Assume constants `a>=0` and positive `C_A,C_N,C_G,C_V` exist, independent
of `j,n`, and numbers `G_j,v_j>=1`, such that:

1. **Complete plan bill:**
   `U_j(n) <= C_A j^a n L(n)^(1/2+1/(j+2))` for every `n>=N_j`.
2. **All-length shape threshold:**
   `log_2(1+log_2 N_j) <= C_N j`.
3. **Constructive preflight cost:**
   `g_j(n) <= G_j L(n)^v_j`,
   `log_2 G_j <= 2^(C_G j)`, and `v_j <= 2^(C_V j)`.
4. **Sound physical resource interface:** the plan contract in Section 1,
   including one common `O(n)` visited-space constant and exact outputs,
   holds. In particular, the bills are bounds for `E`, not for a stronger
   random-access, free-parallel or unbounded-alphabet model.

**Theorem P2.** Under these hypotheses one fixed deterministic multitape
machine computes exact multiplication in

```
T(n) = O(n sqrt(L(n)) x^a),     visited cells = O(n).             (P2)
```

For `a=0`, this is the exact square-root logarithmic endpoint. For `a>0`,
it is a complete conditional overhead bound with `H(n)=O(x^a)`. No claim
is made that these hypotheses hold for the manuscript's literal family.

### Proof with parameter and threshold details

Take a fixed positive `c` so small that
`c C_N,c C_G,c C_V <= 1/4`. For all sufficiently large `x`, let
`j=floor(cx)`. Then `j>=cx/2>=1`. The applicability condition follows from
`log_2(1+log_2 N_j)<=C_N j<=x/4<=x`, hence `n>=N_j`.

Since `G_j,v_j>=1`, the added bill-comparison term satisfies
`e_j(n)+1 <= C G_j L(n)^v_j`. Consequently

```
log_2[C_0 w_j(e_j(n)+1)]
 <= O(log(j+2)) + log_2 G_j + v_j x
 <= O(log(x+2)) + (1+x)2^(x/4)
 = o(2^x).
```

But `log_2 n = 2^x-1`. Thus this chosen preflight satisfies the precise
eligibility condition in P1 for every sufficiently large attainable `x`.
Finally

```
j^a <= (cx)^a,
2^(x/(j+2)) <= 2^(2/c).
```

Substitution into P1 yields (P2). All exceptional initial lengths are
covered by schoolbook and absorbed in the fixed big-O constant. The proof
uses only attainable `x=log_2(1+log_2 n)`; no interpolation of an algorithm
to real-valued input lengths is involved. ∎

The theorem tolerates doubly exponential *constant setup time* in `j` and
an exponentially growing polylogarithmic degree. That does not make such
setup free. It is paid by the explicit linear preprocessing window, whose
eligibility condition is proved above when `j` is a sufficiently small
constant multiple of `x`.

### Equivalent source-level hypotheses instead of an unexplained bill

One way to establish premise 1 is to certify for the source's complete
interpreted digit programs constants `a_j,c_j,U_j^core` as in C2 of
`linear-chunk-overhead.md`, prove `a_j c_j <= C j^a`, and use its explicit
rowwise chunk wrapper. The resulting threshold is
`max(4c_j,r_j U_j^core)`, with `2c_j<r_j<=4c_j`. The new obligations are
therefore separately testable properties of actual instruction time,
physical live storage, core thresholds and the compiler, rather than an
assumption that a uniform endpoint multiplier already exists.

The original paper proves fixed-`j` bounds only. Bounded `a_j c_j` is a
strong additional hypothesis and is incompatible with some literal
growing-template layouts, as the separate padding obstructions explain.
For an endpoint application one would need a different representation or a
uniformly efficient replacement for those layouts. A program-size factor
from scanning a full generated transition list cannot be removed from
`a_j` merely because the *selection* now costs `O(n)`.

## 4. A source-motivated route to an honest bill compiler

### Constant normalization has a threshold price

For the selector, unbounded fixed-candidate coefficients are not by
themselves an invariant obstruction. There is a precise tradeoff.

**Lemma P3.** Suppose sound, explicitly computable plans have bills

```
V_j(n) <= B_j n L^(1/2+1/(2(j+2)))      (n >= M_j),  B_j >= 1.
```

Then those same plans have the uniform-coefficient bill
`V_j(n) <= n L^(1/2+1/(j+2))` whenever

```
x >= max(log_2(1+log_2 M_j), 2(j+2)log_2 B_j).                 (P3)
```

This is the identity `B_j <= 2^(x/(2(j+2)))` substituted into the first
bill. A preflight can test an integer upward-rounded version of the bill
inequality and reject plans until it holds; it need not know an asymptotic
cutoff in advance. The finite comparison and its rational-power arithmetic
are charged to `g_j(n)`. Using `Lhat` as below changes only an absolute
coefficient. In the original exponent family the inner candidate can be
indexed by `2j+2`, since `1/((2j+2)+2)=1/(2(j+2))`.

Consequently, the force of P2 lies in the **joint** control of the bill,
threshold and preflight cost. A bounded coefficient alone is inexpensive to
manufacture from a fixed-epsilon family by delaying applicability. It does
not give an endpoint unless the resulting thresholds remain small enough.
P3 is a sufficient accounting trade, not a necessary lower bound on the
threshold of every alternative analysis or implementation.

At `openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`:

- `uniformity.tex`, “Certifying enough precision,” gives an effective
  enumeration of `poly_j(1+k)` array instructions and explicit norm/error
  majorants, with `k=Theta(log n)` for the multiplication shape.
- `integers.tex`, `eq:integer-box` and `lem:synchronized-short`, make the
  shape, coprimality, local-table and precision preparation input-length
  dependent but independent of operand values; it is polynomial in `k`
  for each fixed template.
- `walsh.tex`, `lem:tape-walsh`, has a fixed-branching macro recursion of
  logarithmic depth and explicit piece/padding rules.
- `interchange.tex`, the proof of `thm:interchange`, provides shrinking
  main streams, full-volume descriptor-only reserve descents and a
  depth-first parking rule. These are the ingredients of a computable
  visited-region bill, but its full compiler has not been implemented.

The difficult work is not evaluating `n L^theta` once given a constant. It
is proving a uniform finite vocabulary of physical operations and deriving
sound time/space bills from their actual implemented contracts, including
data-dependent control-table routines and every transition-list access.
The `poly_j(log n)` sentence about numerical preparation alone does not
prove that such bills can be produced with the costs in P2.

Integer bills can avoid numerical logarithm/root oracles: use
`Lhat=1+ceil(log_2 n)`, determine rational powers by integer comparisons,
and round upward. For `j>=1`, `theta_j=(j+4)/(2j+4)<=1`; replacing `L`
by `Lhat<=2L` and rounding the positive power changes its bill by at most
an absolute factor. All integer arithmetic used to produce that bill
belongs to `g_j(n)`.

## 5. What was proved and what remains open

P1 proves a common-space selector with a concrete physical implementation
and an exact coverage condition. P2 proves the entire endpoint/poly-`x`
implication from explicit quantitative family and compiler properties.
Neither theorem verifies those properties for the published construction.
These selector theorems alone therefore leave its unconditional
`n L^(1/2+o(1))` statement unchanged. Consult the parent programme state for
any separately audited explicit extraction from Route A; it is not supplied
by this conditional selector.

The main open question is **a sound, efficient bill compiler for one
specific scalable family with controlled time and space coefficients**.
It must expose costs that binary reweighting alone leaves inside `A_j`.
Useful next steps are to construct the finite macro vocabulary, prove its
primitive physical bills, and compute the complete recurrence/region
derivation for a nontrivial source template. A claimed endpoint still also
needs premise 1 with `a=0`; solving only the compiler does not supply it.

Attribution: @CubeJerry; OpenAI's November 24, 2026 tape and Fourier papers;
Levin and Hutter for universal-search and time-bound-search principles;
the predecessor programme's source/space accounting. Prepared with
substantial OpenAI ChatGPT multi-agent assistance. No human refereeing,
Lean kernel check or fully implemented multiplier is claimed.
