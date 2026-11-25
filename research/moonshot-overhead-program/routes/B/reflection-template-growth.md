# What survives after paying for the reflection template

Status: **proved finite-size comparison and parameter estimate; any final
overhead consequence remains conditional on the separately reviewed physical
compiler**. The reflection mechanism improves a physical main-call bill,
but its generic module is still large.

## 1. Retain the degree when counting monomials

The source integral binary predictor is multilinear in `m` individual query
variables, with degree at most `D`. After collecting terms it has at most

\[
 H_D=\sum_{r=0}^{D}\binom mr
 \le(D+1)(em/D)^D\qquad(1\le D\le m/2)                 \tag{TG1}
\]

monomials. Bound each binomial term by `(em/r)^r`, whose logarithm increases
for `r<=m`. Zero monomials may pad all shifted predictors to the same count.

With `b` the next power of two above `D`, the source matrix-root dimension
is `d0=b^(H_D)`. Its batch uses `R=2^m d0` rows. The constant-tail window
has `D=O(sqrt(m))`, giving

\[
 \log_2\log_2 R=O(\sqrt m\log(m+2)).                  \tag{TG2}
\]

The source rare-tail window has `D=O(sqrt(m log m))`; the same calculation
gives `log2 log2 R_rare=O(sqrt(m)(log(m+2))^(3/2))`. These are upper bounds
for the literal generic construction, not lower bounds for every
representation. A's simpler `H_D<=2^m` bound loses this comparison.

## 2. The changing targets do not add a new tower

For `h=ceil(log2(m)/4)`, the batch enlargement is at most `8m^(3/4)`.
All half-angle roots already lie in the source `R`-th-root extension for
large `m`. The finite unrolling has at most `2^(h+1)-1` nodes, polynomial
in `m`. There is no extension tower indexed by family depth.

The source cyclotomic degree is at most `R`; its explicit inverse
node-difference products, Lagrange inverses and Hermite tables have coefficient
bit lengths bounded by a fixed power of `R`, as independently detailed in
`../A/scalar-template-growth.md`. A half-angle coefficient adds only
boundedly many root monomials and powers of two. Listing all stages,
tables, families and unrolling therefore still takes `R^C` time, output
size and workspace for an absolute `C`, by exact schoolbook arithmetic.

Under the source optimized labels, their count is `m^(4+o(1))`. Rational
address elimination has polynomial-m dimensions and bit heights, so numeric
magnitudes are at most `2^(m^c)` for an absolute `c`. This is eventually
dominated by the enlarged common envelope

\[
 P_m=2^{\,2^{C\sqrt m\log(m+2)}}.                       \tag{TG3}
\]

Trial division for a compatible address prime above the expanded batch
width and every required nonzero numerator/denominator also fits a fixed
power of (TG3), by Bertrand's bound. Hence this envelope bounds the expanded
data, numeric scalings, scalar symbols and actual direct generator. It is
still double exponential in a positive power of `m`.

## 3. The source label loss determines the inverse-exponent scale

Let `J>=2` be inverse target slack: the desired local exponent is
`1/2+Theta(1/J)`. Use the uniform estimates in
`../A/interchange-label-growth.md`. Choose a prime `p` in `[KJ,2KJ]` for
a sufficiently large absolute `K`, and put `u=log2 m`. The rounded label
parameter and routing loss satisfy

\[
 t=\log_2q\le1+u/p^2+C\log(p+1),
\]
\[
 \log_2 R(m)\le(3p-1)t+p(p-1)\log_2\max(1,t)
                       +C(p^2+\log(p+1)).             \tag{TG4}
\]

Take `u=C0 J^3 log2(J+2)`. The first part of (TG4) is at most
`3u/p+O(p log p)`. Choose `K` so `3u/p` uses less than a quarter of the
target `u/J` slack. All remaining terms are `O_K(J^2 log(J+2))`.
A sufficiently large absolute `C0` pays for these and a fixed contraction
margin. A possible `log C0` in the fixed constant is dominated by `C0`.
The reserve dimension has logarithm `O(u/p+p log p)`, so its full-volume
bill is much smaller than `m^(1/2)` at these parameters.

For the Fourier geometry choose even `L=Theta(J)`. Its log routing loss
is `2u/L+O(L log(u+L))`, paid by the same scale. Choose an odd
`m=2^ceil(u)+1` to preserve the source binary parity condition. Thus exact
local call-margin tests can succeed at

\[
 m\le2^{O(J^3\log(J+2))}.                              \tag{TG5}
\]

The rare-tail factor adds only `O(log u)` to the call logarithm, also paid
at this scale. Therefore (TG5) is available **with or without** reflection.
Its improvement over a sixth-power coarse estimate comes from sharpening
the same source label accounting, not from a new label geometry.

## 4. Conditional whole-profile implication

Suppose the physical compiler independently supplies
`a_J,c_J,g_J,d_J<=P_m^C` and `U_J<=2^(P_m^C)`, with a common capped-machine
schedule as in A. Combining (TG3) and (TG5) then gives

\[
 \log_2(\text{candidate prefactor}_J),\quad
 \log_2 L(N_J)\le2^{\,2^{O(J^3\log(J+2))}}.             \tag{TG6}
\]

For `s=log2 L(n)` and `Y=log2 log2 s`, select an available dyadic inverse
slack `J` within a constant factor of `c(Y/log2(Y+2))^(1/3)`, with `c`
sufficiently small. The candidate overhead in (TG6) is then `s^o(1)`
inside `log2 H`, while exponent slack contributes `O(s/J)`. Under the
stated compiler premise this yields

\[
 H(n)\le2^{O\left(s\left({\log(Y+2)\over Y}\right)^{1/3}\right)}.
                                                               \tag{TG7}
\]

This is a conditional parameter sharpening, not a claim of an independently
completed tape compiler. Crucially, the same iterated-log scale follows
from the degree-sensitive rare-tail construction: its extra `sqrt(log m)`
changes lower-order profile terms. The new reflection mechanism alone does
not improve that coarse whole-overhead class. A much smaller full-rate
module, or better physical labels, is needed for a larger change.

Credits: source generic matrix-root representation and address geometry;
A's explicit uniform label/height bounds; the new B reflection family;
Jerry Chen (@CubeJerry); AI-assisted quantitative comparison.
