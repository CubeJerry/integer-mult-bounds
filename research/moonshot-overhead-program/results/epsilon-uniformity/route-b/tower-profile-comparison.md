# Does preflight improve the literal tower extraction?

Status: **proved conditional comparison of explicit quantitative profiles**.
This comparison takes Route A's finite-template/compiler profiles as input;
it does not independently establish their full source compiler. It also does
not claim that the actual selected plans have the worst-case upper profiles.

## 1. The current profile

Route A's `elementary-tower-extraction.md` uses a quantity

```
S_j <= E_3(C (j+2)^3 log_2(j+3)),
E_1(z)=2^z, E_2(z)=2^(2^z), E_3(z)=2^(2^(2^z)),
```

which covers finite scalar rows/tables, radix size, generation cost,
coefficient heights, serialized scan counts, code and potential live roles.
Its physical candidate constants and proportional space coefficient are
bounded by fixed powers of `S_j`, with a valid-input condition
`log_2 n >= S_j^c` after enlarging an absolute constant `c`.

Put `Q_j=log_2 S_j`. Up to absolute fixed powers, the current coarse ledger
therefore has

```
log_2 A_j = O(Q_j),
b_j = O(Q_j),
chunk exponent k_j = O(Q_j).
```

For full sum-diagonal enumeration, `i_j=O((j+k_j)^2)`, so the *sufficient*
old logarithmic certificate constant is `O((j+Q_j)^2)`. Binary parameter
scheduling reduces its selection contribution to
`O(log(j+2)+log(Q_j+2))`; the actual `O(Q_j)` logarithm of `A_j` remains.
This is a real improvement in the parameter ledger. It does not change the
elementary tower height, because `Q_j=E_2(O(j^3 log j))` and any fixed power
of this upper bound is absorbed by enlarging its absolute constant.

## 2. Eligibility for a preflight of the same coarse height

Suppose an actual sound bill compiler for these candidates has cost

```
g_j(n) <= S_j^g L(n)^(S_j^v),       g,v > 0 fixed,
```

and emits a complete plan with the preceding actual-step/space bills.
This is a conditional compiler-cost premise, motivated by the source's
fixed-branching instruction enumeration. It must be established for the
chosen concrete compiler, not inferred merely from the existence of a
finite template.

**Lemma T1.** There is a constant `C` such that

```
x >= C(Q_j + log_2(j+2) + 1)
```

is sufficient for the preflight eligibility condition in P1 of
`preflight-selection.md`, uniformly for all `j` and all sufficiently large
`x`. The finitely many remaining small `x` can be included by enlarging `C`.

**Proof.** The logarithm of the complete discovery cost is at most

```
O(log(j+2)) + g Q_j + x 2^(v Q_j).
```

Choose `C` so that `v Q_j <= x/2`, the first two terms are `O(x)`, and
`x` exceeds a fixed absolute cutoff. Then
`O(x)+x 2^(x/2) < 2^x-1 = log_2 n` for every sufficiently large `x`.
Exponentiating proves the exact eligibility inequality, including its fixed
discovery constant. If `j` is small and `Q_j>=1`, increasing `C` covers the
remaining finite cutoff. ∎

Thus preflight does not eliminate the current `b_j=O(Q_j)` restriction.
It moves all search loss into another threshold of the **same coarse
height**, while leaving the logarithm of the actual execution bill at
`O(Q_j)`.

One can also spend exponent slack to move the latter coefficient into the
threshold. Lemma P3 of the preflight note, applied to a candidate with half
the requested residual exponent, gives a uniform coefficient at the cost
of an additional condition `x >= O((j+2)Q_j)`. This still has the same
coarse elementary height. It reinforces that the binding information is
the joint cost/threshold profile: the execution coefficient need not remain
in the displayed certificate if one honestly delays its valid range.

## 3. Consequence for the advertised explicit envelope

Write `y=log_2 log_2(x+16)`. The coarse profile admits a sufficiently small
integer choice

```
j = floor(c (y/log_2(y+2))^(1/3)),
```

for which `Q_j <= sqrt(x)` after enlarging fixed constants and taking `x`
large. Both the candidate threshold and the preflight threshold then hold.
The resulting preflight certificate obeys

```
log_2 H(n) = O(x (log_2(y+2)/y)^(1/3)).
```

This is the same advertised envelope scale as the coarse Route A extraction.
It is not a proof that the actual two algorithms have the same runtime, nor
that finer parameter bounds cannot yield a different rate. The old quadratic
search invoice and the new linear `Q_j` invoice can give different
pointwise guarantees. The conclusion is only that reweighting or preflight
alone does not yield a stronger asymptotic envelope from these coarse
tower-height estimates.

## 4. The next decisive expense

The current `S_j` includes genuine per-volume work: dense scalar transfers,
serialized rows, physical address/radix conversions, and numerical widths.
Generating tables earlier does not remove those operations from execution.
A transition-list scan at every raw interpreted step is also an execution
cost unless an alternative finite executor is proved.

An endpoint or poly-`x` application of P2 therefore needs a substantially
different execution/space profile and/or much earlier applicability, not
merely a better search weight. The most consequential selector follow-up is
to construct a sound **macro executor and bill compiler** which makes
description traversal additive in the number of macro calls while keeping
the physical table, arithmetic and routing operations fully charged. Even
that must be combined with a better core invoice; the existence of a quick
bill compiler by itself is not a new multiplication bound.

Credits: Route A's explicit source-profile extraction; concurrent S002's
separation of additive setup from proportional execution/storage;
@CubeJerry; the OpenAI source manuscripts and Hutter's time-bound search.
Developed with ChatGPT multi-agent assistance.
