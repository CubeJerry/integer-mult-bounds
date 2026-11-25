# Binary-length scheduling of the published attempts

Status: **proved source-specific scheduling transformation**, conditional only
on the correctness/finite-tape attempt construction in the cited manuscript.
This is not an explicit new asymptotic multiplication bound: the actual
candidate constants and applicability thresholds remain unquantified. The
coding principle is standard universal-search mathematics; the contribution
here is its charged fixed-tape, common-space specialization and the resulting
parameter ledger for this source family.

## Sources and model

Source pin: `openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`,
`preprints/The-logarithmic-exponent-of-integer-multiplication-on-tapes-November-24-2026/build/uniformity.tex`,
Section `sec:single-machine`, especially the subsections on a common number of
tapes and scheduling within linear space. The source attempt consists of the
entire generator, interpreter, shape/precision work, chunk products,
accumulation and output. It is not an arithmetic circuit gate count.

Let `Attempt(j,k)` denote exactly this attempt, with `j >= 1`, `k >= 0`,
`r = 2^k`, and the source's common marked work areas of `O(n)` cells. A count
`r > n` is ineligible. An attempt either returns the correct exact product,
reports ineligibility/space failure, or remains unfinished. A run returning
the product after `t` steps has `t` measured on the fixed physical interpreter,
including its generation and all preparation and recovery. All runs can be
interrupted, cleaned and restarted as in the source. Schoolbook multiplication
is a separate correct `O(n^2)`-time, `O(n)`-visited-space fallback.

Write `ell(z) = floor(log_2 z)+1` for positive integers. Parameters supplied to
an attempt are written in binary. The scheduler never writes `2^k` before
checking, inside the attempt's charged budget, whether `k <= floor(log_2 n)`.

## B1. A fixed common-space scheduler with polynomial parameter penalty

Fix a total computable map `f` from positive integers to positive integers.
The following machine schedules `Attempt(f(q),k)`, for `q >= 1`, `k >= 0`.
Evaluating `f(q)` is part of the attempt and is charged; no efficiency of `f`
is assumed. Let

```
a = ell(q),  b = ell(k+1),  lambda(q,k) = 2a+2b,
W(q,k) = 2^lambda(q,k).
```

There is one fixed deterministic multitape machine, with a fixed finite
alphabet and a uniform `O(n)` bound on all cells ever visited, whose time on
any length-`n` input satisfies

```
T(n) <= C n + C W(q,k)(t+1)
```

for every successful attempt at these parameters of duration `t`. The same
constant `C` works for all `n,q,k,t`. In particular,

```
W(q,k) <= 16 q^2 (k+1)^2.
```

### Proof

Do the initial input scan and fixed space marking once, in `O(n)` steps.
Round `s >= 1` first gives schoolbook multiplication `2^(s-1)` steps, and
then visits every pair with `lambda <= s`, each with budget `2^(s-lambda)`.
All candidate execution is sequential; all copies, decoding of the requested
candidate, and generation count against that budget. A timeout or space
failure triggers cleanup; a completed product terminates the machine.

For every positive binary length `a` there are `2^(a-1)` values of `q`.
Consequently

```
sum_(q>=1) 2^(-2ell(q)) = 1/2,
sum_(q>=1,k>=0) 2^(-lambda(q,k)) = 1/4.
```

Thus allotted simulation steps in round `s`, including schoolbook, sum to at
most `(3/4)2^s`. Let `m=floor(s/2)`. For `m >= 2` the number of parameter
pairs is exactly

```
N_s = sum_(h=2)^m (h-1)2^(h-2) = (m-2)2^(m-1)+1.
```

Enumerate binary lengths and then binary values with nested tape counters.
At most a fixed polynomial in `s` steps per pair suffice for control, copying
its binary labels and clock setup. The total is at most
`poly(s) 2^(s/2) = O(2^s)`, with a universal constant. There is no dependence on
the numerical value of `f(q)` here: its expansion belongs to the time-limited
attempt. The source's low-end binary clocks take `O(s+v+1)` physical steps
over an attempt of `v` ticks; frontier-mark cleanup takes the same order.
Hence every complete round costs `O(2^s)` in actual head movements.

Schoolbook succeeds by `s=O(1+log n)`. The pair labels, loop counters and clocks
therefore have `O(1+log n)` bits. A fixed number of candidate tapes each has a
marked interval of length `O(n)`; input, output, scratch and control use a
fixed number of other marked intervals. Cleanup reuses these intervals, so
the bound is on the union of all visited cells, not merely simultaneous
live storage. These facts establish one fixed tape count and alphabet and a
uniform visited-space constant.

The round `s=lambda+ceil(log_2(t+1))` grants the successful attempt enough
time. If schoolbook succeeds earlier that only helps. Geometrically summing
all round costs gives the claimed inequality. Finally,
`2^ell(z) <= 2z` gives `W <= 16q^2(k+1)^2`. This proves B1.

## B2. A sharper schedule with an explicit logarithmic control allowance

The same conclusion holds with

```
lambda(q,k) = a + 3ell(a) + b + 3ell(b),
W(q,k) = 2^lambda(q,k)
          <= 256 q(k+1) ell(q)^3 ell(k+1)^3.
```

The logarithmic factors pay for label handling on physical tapes. This
statement does not rely on free constant-time random access to integers of
unbounded length.

### Proof

For a positive integer parameter `z`, assign length
`c(z)=ell(z)+3ell(ell(z))`. Grouping first by `a=ell(z)` and then by
`ell(a)` gives

```
S = sum_z 2^(-c(z)) = (1/2) sum_(a>=1) 2^(-3ell(a)) = 1/12,
M = sum_z ell(z) 2^(-c(z))
  = (1/2) sum_(a>=1) a 2^(-3ell(a)) <= 1/4.
```

For pairs, `sum 2^(-lambda)=S^2` and
`sum (a+b)2^(-lambda)=2MS` are finite absolute constants.
Enumerate `a,b <= s` and then all pairs having these lengths and
`lambda <= s`. A fixed-tape implementation spends `O(a+b+1)` steps per
pair for labels and loop management, plus `poly(s)` steps on length loops.
The resulting label cost is at most

```
C 2^s sum_(q,k) (a+b+1)2^(-lambda(q,k)) = O(2^s).
```

A clock for budget `2^(s-lambda)` costs `O(s-lambda+v+1)` rather than
`O(s)` at every tick. Since `u+1 <= 2^u` for integers `u >= 0`, summing clock
setup and cleanup costs contributes at most another constant times `2^s`.
Schoolbook still has its separate half-round budget. The space and
successful-round argument from B1 applies unchanged. The displayed bound
on `W` follows from `2^ell(z) <= 2z`, used also with `z=a,b`.

## B3. Exponentially spaced exponent indices

Take `f(q)=2^(q-1)`. This keeps exponents for `j=1,2,4,8,...`, which still
converge to `1/2`. Expanding `f(q)` needs `q` binary symbols and is charged
inside the attempt. For each `m >= 0`, suppose a particular chunk index
`k_m` is successful for all `n >= N_m`, with complete physical duration

```
t_m(n) <= A_m n L(n)^(1/2+1/(2^m+2)),  A_m >= 1.
```

B1 gives the sufficient envelope

```
H(n) <= C[1 + inf_(m:n>=N_m)
              (m+1)^2(k_m+1)^2 A_m 2^(x/(2^m+2))].
```

B2 replaces the polynomial prefactor by

```
(m+1)(k_m+1) ell(m+1)^3 ell(k_m+1)^3.
```

Empty feasible sets use schoolbook. These are upper-bound certificates,
not equalities or algorithmic lower bounds. The unknown `A_m` includes the
generator, finite alphabet/transition description, interpreted scans,
precision, the source's `r^2` chunk multiplications and accumulation.

### A precise conditional rate, with integer and threshold choices

Suppose constants `a >= 0`, `C_A,C_N >= 1`, and integer `K >= 0` satisfy,
for all `m >= m_0`,

```
A_m <= C_A (2^m)^a,
k_m <= K,
log_2(1+log_2 N_m) <= C_N 2^m.
```

Then the B2 machine has

```
T(n) = O(n sqrt(L) x^a (1+log_2 x)(1+log_2 log_2(x+2))^3).
```

For large `x`, put `m=floor(log_2(x/(2C_N)))`. Then
`x/(4C_N) < 2^m <= x/(2C_N)`, so the chosen candidate is applicable and
`x/(2^m+2) < 4C_N`. The claimed rate follows immediately. All initial
lengths are absorbed by the fixed fallback. The constants in the three
premises have not been established for the manuscript family.

## What this changes, and what it does not

The manuscript's *specific* one-based diagonal enumeration and weight `2^-i`
is quantitatively expensive as its labels grow. Binary-length scheduling,
and especially sparse exponent indexing, avoids that particular cost. It
does not remove growing actual interpreter/algorithm constants or late shape
thresholds. A conclusion about the old certificate is not a lower bound on
this replacement or on the old machine's true runtime.

The method is a specialization of Levin-style program-length scheduling,
not a claim to invent universal search. Hutter's 2002 paper, Section 2,
explicitly contrasts unary enumeration with program-length weights; see
`https://www.hutter1.net/ai/pfastprg.pdf` and `arXiv:cs/0206022v1`.
The present restricted family does not enumerate all programs, so one cannot
assume that it automatically contains a simulator of every improved search.

Concurrent S002, `routes/A/scheduler-and-chunking.md`, A1–A2, independently
provides a near-linear penalty in the diagonal *pair index* and uses a sparse
exponent sequence. That already removes the unary-index exponential. B2
here directly weights the two binary parameters and is a complementary
certificate, not a uniform improvement over S002: it can be smaller when
the parameters are very unequal, while S002 can have smaller logarithmic
factors when they are comparable. Sparse indexing and removal of the unary
tax are therefore shared/overlapping enabling results; the distinct main
Route B development is the preflight selector.

## Open next questions

1. Bound the source's **actual** `A_m,k_m,N_m` after sparse indexing. Removing
   enumeration alone cannot make these uniform.
2. Can a fixed-width looped implementation avoid a transition-list scan
   proportional to the entire generated candidate description at every step?
3. Can certified preflight move parameter-search cost into an applicability
   condition and permit one selected plan to run without multiplicative
   scheduling loss? See the separate preflight theorem.

Attribution: @CubeJerry; the OpenAI November 24, 2026 tape/Fourier manuscripts;
Levin's universal-search construction; Hutter's explicit coding discussion.
Credit also to concurrent S002 A1–A2 for the overlapping sparse/weighted
search result and A3–A4 for quantified chunk accounting.
Prepared with OpenAI ChatGPT multi-agent assistance. No Lean build or physical
Turing-machine implementation is claimed by this document.
