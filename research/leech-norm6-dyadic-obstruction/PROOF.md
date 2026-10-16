# A fixed Leech norm-six basis has no dyadic dual for the full cubic kernel

## 1. Statement and scope

Let `x` range over the 98,280 canonical Leech minimal lines in the integer
coordinates of DominikScholz's PR598: `x.x = 32`, with the physical coordinates
obtained by dividing by `sqrt(8)`. Let `a_0,...,a_2599` be the first 2,600
canonical norm-six directions from its `norm6_centers.py` generator (seed
6242600). Their exact source-pair records are bundled in `DIRECTIONS.json`.
Each `a.a = 48`.

Define

$$
 E_a(x)=\frac{(a\cdot x)^3-256(a\cdot x)}{3},\qquad
 K(x,y)=\frac{E_y(x)}{8192}.
$$

Thus `K(x,y) = (t^3-4t)/48`, where `t=x.y/8`, exactly the predecessor's
specified full cubic kernel. The norm-six encoders `E_a/8192` are also dyadic
on this shell. The factor 1/3 in the displayed polynomial is an integer-valued
coefficient convention, not an allowed run-time division by an odd integer.

**Theorem.** There are no dyadic coefficients `d_i` satisfying

$$
 E_y(x)=\sum_{i=0}^{2599}d_iE_{a_i}(x)
 \quad\text{for every minimal line }x,
 \qquad y=(4,4,0,\ldots,0).
$$

Consequently these fixed encoders have no dyadic decoder for the **full
specified kernel**. Gaussian-dyadic coefficients cannot help: taking real
parts of an exact representation would give a real-dyadic one.

**One-prime escape.** Replacing direction 2599 with direction 2600 makes the
2,600-by-2,600 coefficient matrix invertible over F5. This removes this exact
obstruction without adding an encoder. It proves neither a dyadic inverse nor
a paid supplier: other odd primes and higher arithmetic obligations remain.

This is not a lower bound for all norm-six choices, arbitrary masked fits,
other kernels, different coefficient domains, or a decoder allowed to read
additional source-dependent functions. It is not a new multiplication bound.

## 2. Integer-valued coordinates

Use the following 2,600 functions, in the order in `model.py`:

$$
 A_i(x)=\frac{x_i^3-31x_i}{3}\quad(24),\qquad
 A_{ij}(x)=x_ix_j^2\quad(i\ne j;\ 552),\qquad
 A_{ijk}(x)=x_ix_jx_k\quad(i<j<k;\ 2024).
$$

These are the predecessor's dyadic factorization coordinates. Every displayed
integer-coordinate numerator divided by 3 is divisible by 3, since
`n^3 = n (mod 3)`.

For `x.x=32`, we have

$$
 x_i=3A_i+\sum_{j\ne i}A_{ij},\qquad
 x_i^3=96A_i+31\sum_{j\ne i}A_{ij}.
$$

Expanding the dot-product cube therefore gives `E_a(x)=A(x).C(a)`, with

$$
\begin{aligned}
 C_i(a)&=32a_i^3-256a_i,\\
 C_{ij}(a)&=a_i a_j^2+\frac{31a_i^3-256a_i}{3},\\
 C_{ijk}(a)&=2a_i a_j a_k.
\end{aligned}
$$

All 2,600 coordinates of `C(a)` are integers. This formula is valid for every
integer `a`, not only the finite direction fixture. In particular `C(y)` is
also the target coefficient vector from the predecessor's full kernel.

The verifier independently expands the homogeneous numerator
`(a.x)^3-8(a.x)(x.x)` and compares all 2,600 coefficients for every one of the
2,601 bundled directions, with denominators cleared. It also checks 256 direct
polynomial evaluations. The algebra above, not sampling alone, proves the
identity on the whole norm-32 sphere.

## 3. Why equality on the finite shell forces coefficient equality

We give a direct injectivity argument instead of assuming that a polynomial
identity follows from a finite replay, or importing a spherical-design theorem.

On the norm-32 sphere,

$$
 A_i=\frac{x_i^3-31\sum_{j\ne i}x_ix_j^2}{96}.
$$

Consequently the `A` functions are an invertible rational change from all
homogeneous cubic monomials. It suffices to prove that a homogeneous cubic
vanishing on the canonical lines is zero. A cubic is odd, so vanishing on
canonical representatives also implies vanishing on their negatives.

Write such a cubic as

$$
 H(x)=\sum_i u_i x_i^3+\sum_{i\ne j}v_{ij}x_ix_j^2
        +\sum_{i<j<k}w_{ijk}x_ix_jx_k.
$$

The shell contains `4(e_i+e_j)` and `4(e_i-e_j)`, and their negatives.
Evaluating `H` at them implies

$$
 v_{ij}=-u_i\quad\text{for every }i\ne j.
$$

For every Golay octad `O`, the shell also contains the vectors `2s_O`, with
`s_i` in `{+1,-1}` and `product(s_i)=1`. On this sign group the characters
indexed by singletons and triples of `O` are all distinct: two characters
coincide only when their indexing subsets differ by the whole eight-set, but
the symmetric difference of two such sets has size at most six.

Orthogonality of these sign characters, over the rationals, gives

$$
 u_i+\sum_{j\in O\setminus\{i\}}v_{ij}=0,\qquad
 w_{ijk}=0\quad(\{i,j,k\}\subset O).
$$

The first equation is `-6u_i=0`. Every coordinate belongs to an octad, so all
`u_i`, then all `v_ij`, vanish. Every coordinate triple belongs to an octad, so
all `w_ijk` vanish. The checker reconstructs all 759 octads from the exact
Golay generator and checks coverage of all 2,024 triples; it does not assume
this incidence property from a catalogue.

Thus the 2,600 functions `A` are linearly independent on the actual finite
shell over Q (and hence over its extensions). An exact decoder for every `x`
therefore necessarily gives the **integer-coordinate equation**

$$
 C(y)=\sum_i d_i C(a_i).
$$

No assertion about independence after reduction modulo five is needed here.
This distinction matters: coefficient reduction is applied only after exact
characteristic-zero equality has been established.

## 4. The separating certificate

Let `z` be the 2,600-entry F5 vector in `CERTIFICATE.json`. The verifier checks
with ordinary integer dot products that

$$
 C(a_i)\cdot z=0\pmod5\quad(0\le i<2600),\qquad
 C(y)\cdot z=3\pmod5.
$$

There is a ring homomorphism `Z[1/2] -> F5`, because 2 is invertible modulo 5.
Reducing a putative dyadic coefficient equation and pairing with `z` would
therefore give `3=0` in F5, a contradiction. This proves the theorem.

This is a constructive obstruction, not a failed search, and it does not
misidentify rational nonsingularity as dyadic admissibility. For example, the
one-dimensional equation `5d=1` has a rational solution but no dyadic solution.

Multiplying any encoder by an invertible dyadic scalar does not change the
obstruction. Repeated use of the same prepared encoders and further dyadic
linear combinations cannot leave their dyadic span. Changing the prepared
source functions, admitting odd denominators, or relaxing the specified kernel
is a different problem.

## 5. Exact rank and the single-row escape

The additional direction is

```
(1,-1,1,1,1,1,1,-1,-3,1,1,1,-3,-1,1,-3,-1,-1,-1,1,-1,1,-1,1).
```

It is generator index 2600, with a bundled decomposition into two authentic
minimal lines. Its residue is `C(a_2600).z = 1 (mod 5)`.

The exact F5 checker verifies that rows `0,...,2598,2600` have rank 2600.
Their first 2599 rows are independent. The original rows have a nonzero right
annihilator, so their rank is at most 2599; the shared independent rows give
the reverse inequality. Hence the original rank is **exactly 2599**.

The experiment changes one row and keeps 2,600 encoders. Two explicit 24-row
support minors in `CERTIFICATE.json` independently check rank at least 24 for
the removed and replacement encoder, using the predecessor's binary pairing
`1+(x.y/8) mod 2`. Together with PR598's norm-six support upper bound, their
support ranks are 24. The old claimed copying allowance `2600*24=62400` is
therefore unchanged by this swap. This is a support-rank statement, **not** a
new frame schedule or a physical invoice.

Invertibility modulo five implies rational invertibility for the exchanged
matrix, but not invertibility over `Z[1/2]`. A different odd prime can still
divide its index. No dyadic decoder for the exchanged basis is supplied here.

### Why the bit-plane rank checker is exact

Each column is represented by three bits encoding its residue 0 through 4.
The Boolean full-adder equations in `rank5.plus` form the four-bit sum 0
through 8. The mask `s3 | (s2 & (s1 | s0))` is true exactly for sums at least
five; the output bits subtract five at precisely those columns. Negation
implements `0,1,2,3,4 -> 0,4,3,2,1`.

Bit operations on Python integers act independently at every column; there is
no packed-integer addition with cross-column carries. Pivot normalization uses
only nonzero F5 scalars, and elimination removes an existing leading column.
The usual row-span invariant proves the rank result. Scalar truth tables,
4,097 mixed columns, all 625 two-by-two matrices and 200 seeded rectangular
matrices are also checked against a separate entrywise modular implementation.
These implementation checks are not a proof-assistant formalization.

## 6. Bounded optimistic budget and stopping decision

We retain, rather than improve or re-certify, the explicitly optimistic model
in PR598 `COSTS.txt`. For `K=1,...,50`, let

$$
 L=2K+1,\quad m=24L+1,\quad W=2K\cdot98280,\quad
 D=2K\cdot98280-L\cdot62400.
$$

Its mandatory local data mass is `A=2*98280*L*24`; the remaining paid mass is
`B=mW-D-A`. Coalesce each mandatory path to rank 24 and place all other mass
at the two-level cap `c=floor(m/sqrt(2))`. This deliberately favorable moment is

$$
 F(a)=\frac{A(m/24)^a+B(m/c)^a}{mW}.
$$

It retains the stated source/target path, copying, restoration and recursive
mass obligations in aggregate, but grants the cheapest placement of remaining
mass and no additional banks. It is not an executable schedule. Extra banks
add a positive excess relative to the acceptance threshold; no physical
helper budget has been established.

`budget.py` verifies `F(a)>1` for the nominal target 1.05 times the pinned
selected kappa, at all 50 stage counts, conditional on this fixed model.
It uses only rational lower bounds: range reduction and 24 positive terms of
`log(q)=2*sum z^(2j+1)/(2j+1)`, followed by four nonconstant positive terms of
the exponential series. Thus a positive computed excess is a rigorous
rejection, not a floating root estimate. This fails the catalogue's 5% large-
expansion gate even before the missing physical construction costs are paid.

Different controllers, copied ranks, path requirements, or stage counts
outside the stated range are not excluded. The screen neither establishes
that the exchanged basis is usable nor bounds every Leech construction.
No selected certificate is changed. **No new kappa.**
