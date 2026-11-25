# Actual and hypothetical size profiles for the order-three construction

Status: **quantitative finite profile and conditional bridge**. The compact
predictor hypothesis below is not proved. The unconditional construction
retains the generic module; no new unconditional overhead rate follows
merely from working over four elements.

## 1. Actual generic module

In the integral order-three count predictor, each coordinate contributes
one affine expression in `1,C_j,C_j^2`. After collecting terms, a degree-D
predictor has at most

\[
 H_D\le\sum_{s=0}^{D}\binom ms2^s
       \le(D+1)(2em/D)^D\quad(1\le D\le m/2)
\]

monomials. Here `D=O(sqrt m)`. With `b` the next power of three and the
source matrix root, the row width before label batching can be taken as

\[
 R=32\,3^m b^{H_D},\qquad
 \log_2\log_2 R=O(\sqrt m\log(m+2)).                  \tag{P3-1}
\]

The three-power check-node extension has degree `O(R)` over `F4`.
All predictor and discrepancy scalars have coefficients in `F4`; node
inverse products and finite table entries can be represented explicitly
as polynomials in the root of degree `O(R)`. Exact construction, all
frequency tables, field-coordinate scalar maps, and the finite contraction
unrolling cost `R^C` for an absolute `C`, using ordinary polynomial and
integer algorithms. This does not enumerate all elements of the enormous
finite alphabet as a truth table.

The label count and rational-address elimination data have polynomial-m
dimensions and bit lengths under the optimized distance choice. Their
numeric magnitudes, compatible radix selection and padding costs are at
most `2^(m^C)` and are dominated by a common actual envelope

\[
 P_m\le 2^{\,2^{C\sqrt m\log(m+2)}}.                    \tag{P3-2}
\]

The additional batch factor is at most `16m`, and the final swap word has
three transforms. Neither changes (P3-2). The four-element discrepancy
identity improves five predictor evaluations to two; it changes the finite
call coefficient, not this tower height.

## 2. A small-field full-rate hypothesis

The following hypothesis is sufficient and asks only for a representation
in characteristic two. It is a different characteristic-specific premise
from a dyadic representation which specializes to every odd characteristic;
neither is asserted to imply the other.

**IP4.** There are absolute constants `C,c` and a deterministic constructor
which, for every sufficiently large `m`, supplies a finite commutative
characteristic-two algebra containing `F4` and a full-rate row program for
commuting order-three queries. At every tuple `k in {0,1,2}^m` its final
row multipliers `p_i(k)` lie in `F4` and disagree with
`z(k)=omega^(sum k_j)` on at most `R/32` of its `R` independent input rows.
The multipliers and a containing exceptional set are effectively known.
The total normalized row volume of its routed pencils is at most
`c sqrt m`: explicitly, the sum of active pencil row counts divided by the
number of independently transformed input rows is at most this bound.
All row widths, scalar-algebra coordinates, coefficient lists, ordinary
instructions, exception tables, generation time and generation workspace
are bounded by `2^(m^C)`.

The abstract evaluator is an explicit finite list of scalar row-linear
maps and affine pencils in the individual query powers. Ordinary row maps
act at the same address, with fixed coefficients independent of the query
eigenvalues. Copies and temporary rows are allowed, with their actual
widths and work charged. The physical address instructions are those
supplied by the shared-pencil compiler, with their complete endpoint lists
charged. An uncompiled permutation or spectral oracle is not an ordinary
instruction under IP4. The finite checks include actual
construction of every polynomial-value and exception table, all common
algebra arithmetic, and validation of the full row-program identity at all
`3^m` spectral tuples. With the displayed bounds, straightforward dense
arithmetic performs these checks in `2^(m^C')` time and space for a fixed C'.

For a total constructor at every m>=2, dovetail the proposed constructor
and these finite checks with the known generic constructor and its checks.
Return the first valid program meeting a fixed stage-volume bound
`c_* sqrt m`, where c_* dominates both absolute constants. The generic
branch guarantees termination for the finitely many initial m at which
IP4 makes no promise. For sufficiently large m the IP4 branch and all its
checks finish in `2^(m^C')` work. By that time the competing branch has
used no more than that order of charged work and visited space. If it
finished first, its emitted data also fit that same budget. Thus this
totality guard preserves the single-exponential asymptotic profile.

The canonical integral predictor would satisfy IP4 if it had such a compact
full-rate evaluator. A different predictor with the stated rowwise property
would suffice. Computing it in one designated output while treating most
coordinates as zero workspace does **not** satisfy the normalized-volume
condition. A large scalar field is not a free unit-cost alphabet: its full
coordinate representation and constructor are in the hypothesis.

Changing every query to its inverse supplies the negative target with the
same bound. Duplicate the row program by a fixed factor if needed to make
`32|R`. Adjoining common three-power check nodes of order `O(R)` multiplies
the algebra dimension by only `O(R)` and keeps the entire data within
`2^(m^C')`. The known exceptional sets permit the explicit source check
tables. Since nonzero discrepancies lie in `F4`, the two-predictor repair
and the finite group-word closure apply without any gap inversion problem.

Even the weaker version allowing arbitrary known predictor values in a
finite common algebra can use the original five-application Hermite repair;
the same asymptotic bridge then holds. Requiring `F4` values makes the
cleaner two-application version available.

## 3. From IP4 to one fewer exponential in the finite profile

Under IP4, the completed main swap program and its source address geometry
have a common expanded-data envelope

\[
 P_m\le2^{m^{C_1}}.                                    \tag{P3-3}
\]

The rational Walsh template of `pairwise-newton-division.md` and
`polynomial-auxiliary-cost-audit.md` also has data bounded by a single
exponential in `m`: its row widths and rational coefficient bit heights
are polynomial, its frequency/column tables are `2^O(m)poly(m)`, and its
column maps are binary. Its ordinary arithmetic circuit bound alone does
not supply tape time; the source's physical column movements use the
completed interchange caller and are charged accordingly.

A rational fixed row coefficient introduces no additional tower in the
numerical compiler. For a coefficient `a/b` of bounded bit height, compute
its dyadic approximation at the chosen `O(k)` precision by ordinary integer
division once as coefficient setup. Schoolbook division costs a fixed
polynomial in its stored height and `k`, absorbed by the source setup
threshold. Every record multiplication still uses the fixed short
`O(k log k)` multiplier. The operator perturbation is bounded by the
coefficient error times the finite row/array norm, already part of the
quantitative precision ledger. This is the physical preparation needed
before using the exact rational circuit as a numerical Walsh template.

Let `J` be inverse exponent slack. For the new geometry choose a power of
two distance `d` in `[KJ,2KJ]` and

\[
 \log_2m=C_2J^3\log_2(J+2).
\]

The explicit label inequalities pay the routing loss and a strict spatial
margin, as in `reflection-template-growth.md`; no growing-prime `O_p`
constant is involved. The Fourier local margin needs at most this scale.
Thus, under the independently reviewed bounded-template physical compiler,

\[
 a_J,c_J,g_J,d_J\le P_{m_J}^{C_3},\qquad
 U_J\le\max\{U_{\rm abs},2^{P_{m_J}^{C_3}}\},\qquad
 m_J\le2^{O(J^3\log(J+2))}.                            \tag{P3-4}
\]

The common-cap chunking and schedule therefore have

\[
 \log_2(\text{candidate prefactor}_J),\quad
 \log_2 L(N_J)\le2^{O(J^3\log(J+2))}.                  \tag{P3-5}
\]

This is one exponential below the actual generic-module profile. Writing
`s=log2 L(n)` and taking an available dyadic `J` within a fixed factor of
`c(log s/log log(s+2))^(1/3)`, with small enough `c`, makes the candidate
log-prefactor `s^a` for a fixed `a<1`. The exponent slack contributes
`O(s/J)` and dominates it. Consequently IP4 plus that physical compiler
would yield

\[
 H(n)\le
 2^{O\left(s\left({\log\log(s+2)\over\log(s+2)}\right)^{1/3}\right)}
 \qquad\text{for sufficiently large }n.                \tag{P3-6}
\]

This is a complete **conditional** target with an explicit missing
mathematical representation premise. IP4 is not inferred from a polynomial
arithmetic circuit, a single-output branching program, matrix rank alone,
or a finite but unbounded construction. The actual generic evaluator only
supplies (P3-2), and hence retains the extra iterated logarithm in the
available coarse unconditional extraction.

The constant `U_abs` is the source's one fixed absolute prime-shape cutoff.
Actual shape tests and the correct fallback keep the machine total without
knowing a numerical value for it. This note's generic comparison remains
a record of that route: the separately proved formula construction in
`formula-full-rate-linearization.md` improves the unconditional finite
profile but still does not meet IP4's `2^(m^C)` promise.

Credits: source physical compiler interfaces and finite ring repair;
A's quantified common-cap schedule and explicit label accounting;
B's rational Walsh template and characteristic-two order-three closure;
Jerry Chen (@CubeJerry); AI-assisted conditional profile analysis.
