# A quantitative compiler for the source candidate family

Status: **proved enabling statements**, pending independent review of this
write-up. These refine the uniformization interface; they do not supply a new
explicit overhead envelope in the input length. The restart construction is a
specialization of weighted universal search, not a claim to invent it.

## Source and model

Source: `openai/math` commit
`3344da59991ed94f9ba711217b29c1d760badfa6`,
`preprints/The-logarithmic-exponent-of-integer-multiplication-on-tapes-November-24-2026/build/uniformity.tex`,
Section `sec:single-machine`. It generates correct candidates with
`theta_j = 1/2 + 1/(j+2)`, serializes them onto a common fixed number of tapes,
and caps every attempt within marked linear-size regions. Its schedule proves
`T(n) <= Cn + C' 2^i(t_i(n)+1)` for a successful attempt at index `i`.
Its chunk assembly has an unquantified `O_r(n)` cost for fixed `r`.

Below, the task remains exact full-product multiplication on fixed
finite-alphabet multitape machines, with head motion charged and one common
`O(n)` visited-cell cap. Only a completed correct attempt may return an answer.

## A1. A restart schedule with almost linear index overhead

For `i >= 1`, define

\[
b_i=\lfloor\log_2 i\rfloor,\qquad
\ell_i=b_i+2\lceil\log_2(b_i+1)\rceil+3.
\]

Reserve `i=1` for schoolbook multiplication. In round `s>=1`, restart every
index with `ell_i<=s`, in increasing order, giving it at most `2^(s-ell_i)`
simulated elementary steps. Its generator, scans of the input/length
descriptor, and output construction are included in its timed work. Abort on
timeout or crossing a space mark, clean its scratch, and stop on first output.

**Proposition A1.** If the index decoder takes `O((1+log i)^2)` steps and
`O(1+log i)` cells, and the source's capped attempts and schoolbook fallback
are available, one fixed machine satisfies, for every successful attempt `i`,

\[
T(n)\le C\,[n+i(1+\log_2 i)^2(t_i(n)+1)]. \tag{A1}
\]

The constant is independent of `n,i` and candidate-specific constants. The
machine visits `O(n)` cells uniformly.

**Proof.** A bucket `2^b<=i<2^(b+1)` has `2^b` indices and constant length.
Thus

\[
\sum_{i\ge1}2^{-\ell_i}
=\frac18\sum_{b\ge0}2^{-2\lceil\log_2(b+1)\rceil}
=\frac18\left(1+\sum_{a\ge1}2^{a-1}2^{-2a}\right)=\frac3{16}. \tag{A2}
\]

The sum of round budgets is at most `3*2^s/16`. A binary clock costs `O(s)`
to initialize and amortized constant time per decrement, including head
returns. As in the source, cleanup is proportional to executed work plus
clock/control setup. The decoder and binary counters cost `O((s+1)^2)` per
eligible index. Input scans are inside the attempt's clock, not this control
bound.

Let `B` be the largest eligible bucket. The number of eligible indices is
`N_s=2^(B+1)-1`. If `B>=s/2`, then

\[
N_s\le2^{B+1}\le\frac{2^{s-2}}{(B+1)^2}
\le\frac{2^s}{(s+2)^2}.
\]

If `B<s/2`, then `N_s<=2^(s/2+1)` and
`N_s(s+1)^2=O(2^s)`. All round control and clock setup therefore costs
`O(2^s)`, as does the round itself. Counter scans also compute the bucket
lengths within this allowance.

Attempt `i` can finish by round
`ell_i+ceil(log2(t_i(n)+1))`. Summing the geometric round costs and using
`2^ell_i <= 32*i*(1+log2 i)^2` proves (A1), after the initial `O(n)` scans.
Schoolbook succeeds in `O(n^2)` steps, so the actual final round is
`O(1+log n)`. All clock/index descriptors use `O(1+log n)` bits. Attempt and
generator work stays in the same marked linear regions; cleanup reuses them.
The original inputs, tentative output and controller have separate fixed
linear capacities. Their union has `O(n)` cells. ∎

This theorem concerns *actual interpreted completion cost*. It does not turn
an effective but slow generator into a fast generator or replace an `O_j`
estimate by a uniform estimate.

## A2. A sparse exponent sequence

Enumerating every integer `j` is unnecessary. For `h>=2`, generate

\[
j(h)=2^h-2,\qquad \theta_{j(h)}=1/2+2^{-h}. \tag{A3}
\]

This still approaches `1/2`. Producing the binary parameter `j(h)` takes
`O(h)` steps inside the attempt and its space cap. Enumerate `(h,k)`, `h>=2`,
`k>=0`, by `d=(h-1)+k` and then increasing `k`. With schoolbook at index 1,

\[
i(h,k)=2+d(d-1)/2+k\le(d+1)^2. \tag{A4}
\]

Maintain diagonal counters, or decode using binary integer square-root and
subtraction in quadratic bit time. Compute `r=2^k` and test `r<=n` only inside
the timed attempt; an enormous inadmissible `r` is never constructed outside
the clock or marks. The search penalty is consequently

\[
O((h+k+1)^2[1+\log_2(h+k+1)]^2). \tag{A5}
\]

This improves the explicit *search guarantee*, not a lower bound on the
source machine's actual runtime, and not yet its asymptotic exponent.

## A3. Physical diagonal assembly with linear chunk dependence

Let `1<=r<=n`, `u=ceil(n/r)`, `B=2^u`, and pad the inputs to `ru` bits:
`x=sum_a x_a B^a`, `y=sum_b y_b B^b`. A correct candidate supplies every
`2u`-bit digit product.

**Proposition A3.** After one retained candidate-program generation, a fixed
tape wrapper gathers, accumulates and returns the exact `2n`-bit product in

\[
O(nr)+\sum_{a,b}\tau_j(u;x_a,y_b) \tag{A6}
\]

steps. Here `tau_j` includes the interpreted digit call, its local input
copies, return and cleanup. The wrapper's constant is independent of
`j,n,r`; it uses `O(n)` cells besides the marked candidate regions.

**Proof.** Prepare the first operand in low-to-high chunk order, and the
second in high-to-low chunk order, retaining the candidate's bit order inside
each chunk. A constant number of scans and reversals does this in `O(n)`.
For diagonal `ell=0,...,2r-2`, the pairs `a+b=ell` traverse one contiguous
interval of the first chunks forward and of the second logical chunks
backward. In the prepared copies both physical cursors advance. Positioning,
reading and returning them costs `O(ru)=O(n)` per diagonal, hence `O(nr)`
overall. The candidate runs on separate local copies and never moves these
operand cursors.

Set `D_ell=sum_(a+b=ell) x_a y_b` and start carry `c_0=0`. Emit

\[
z_\ell=(c_\ell+D_\ell)\bmod B,\qquad
c_{\ell+1}=\lfloor(c_\ell+D_\ell)/B\rfloor. \tag{A7}
\]

Since `D_ell<=r(B-1)^2`, induction gives `c_ell<=r(B-1)` and a running
accumulator needs only `2u+ceil(log2(r+1))+O(1)` bits. Charge each product
addition to its low `2u` bits and high binary counter separately. Low work
costs `O(u)`; the high part increments by at most one. Over `q` additions,
high-counter ripples and returns cost `O(q+log(r+1))`, by amortized binary
counting. Its possibly nonzero initial carry contributes only the initial
`O(log(r+1))` potential once per diagonal. Shifting the accumulator and
emitting a digit costs `O(u+log(r+1))` per diagonal. Total work is

\[
O(r^2u+r\log(r+1))=O(nr),
\]

using `r^2u<=r(n+r)<=2nr` and `log2(r+1)<=2r`. Continue with zero coefficients
to emit `2r` digits; the product is below `B^(2r)`, so no carry remains.
Reverse the output digit stream, remove leading padding, and write exactly
`2n` bits in `O(n)` time.

Operand copies and output occupy `O(ru)=O(n)` cells. Product buffer,
accumulator and counters occupy `O(u+log(r+1)+log n)=O(n)` cells and are
reused. The finite program remains on its candidate tape between calls. ∎

The amortized high-counter treatment is necessary: separately charging
`O(u+log r)` for all `r^2` additions would introduce an avoidable
`O(r^2 log r)` term.

## A4. Quantified consequence of a common cap

For a concrete candidate after source serialization and fixed interpretation,
let `g_j` bound program-generation time. For `u>=U_j`, bound all visited
candidate cells by `c_j u+d_j`, with `c_j,d_j>=1`, including generation,
retained program, one digit call, local copies and cleanup. The fixed
description/generator space belongs in `d_j`, separately from the
proportional live-stream coefficient `c_j`. Suppose also

\[
\tau_j(u)\le a_j u L(u)^{\theta_j}\quad(u\ge U_j),
\qquad a_j,U_j\ge1.
\]

These quantities exist for each fixed source candidate. Their useful uniform
growth bounds are *not* established by that existence statement. Put

\[
r_j=2^{\lceil\log_2(4c_j)\rceil},\quad k_j=\log_2 r_j,
\quad N_j=\max\{\lceil8c_j\rceil,\lceil4(c_j+d_j)\rceil,
\lceil r_jU_j\rceil\}. \tag{A8}
\]

For `n>=N_j`, one has `4c_j<=r_j<8c_j`, `r_j<=n`, `u>=U_j`, and
`c_j u+d_j<=c_j(n/r_j+1)+d_j<=n/4+c_j+d_j<=n/2`. Thus it fits the common marks, and
(A6) gives

\[
t_{j,k_j}(n)\le g_j+C(a_j+1)c_j nL(n)^{\theta_j}. \tag{A9}
\]

The universal machine never needs these unknown constants: trying all `k`
includes this one. For the dyadic candidates, write

\[
W_h=(h+k_{j(h)}+1)^2[1+\log_2(h+k_{j(h)}+1)]^2.
\]

Whenever the eligible set is nonempty, the complete candidate-relative bound is

\[
T(n)\le Cn+C\inf_{h:\ n\ge N_{j(h)}}W_h
\left[g_{j(h)}+1+(a_{j(h)}+1)c_{j(h)}nL(n)^{1/2+2^{-h}}\right]. \tag{A10}
\]

All displayed outer constants are universal after choosing the controller.
The empty range uses schoolbook. This includes generation, movement, cleanup
and uniform physical space. A complete explicit overhead theorem still needs
uniform bounds on `a_j,c_j,d_j,g_j,U_j` from valid constructions. The source's
undifferentiated bound `c_j(u+1)` is recovered by putting `d_j=c_j`. Separating
fixed and proportional space prevents a large program description from
automatically multiplying the chunk count by its own size.

## Verification, limitations and next questions

`verify_scheduler_chunking.py` checks exact schedule budgets and control-count
inequalities, the diagonal pairing, and exact carry identities exhaustively
on short inputs and deterministically on larger ones. It is arithmetic
verification, not a Turing-machine implementation or Lean proof.

The avoidable `2^i` search tax and an unspecified `O_r(n)` term are replaced by
quantified bounds. No template-generation, coefficient-height, interpreter,
physical-space or shape-threshold expense disappears. No new complete
overhead bound or `kappa_ov` is claimed.

Open next questions:

1. Bound `a_j,c_j,d_j,g_j,U_j` uniformly; their dominant growth determines the
   envelope, not the search improvement alone.
2. With such bounds, can a directly computed candidate replace the search,
   while charging selection and generation?
3. Independently audit the physical diagonal layout, accumulator amortization
   and retained-program storage.

Credits: Jerry Chen (@CubeJerry), the November 24 OpenAI tape manuscript and
its predecessors, and Leonid Levin's universal-search method. Developed with
AI assistance during the 2026-11-26 programme session; no authorship of the
source multiplication theorem is claimed.
