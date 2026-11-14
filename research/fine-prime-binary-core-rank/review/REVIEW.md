# Independent review of the exact fine-prime specialization

**Outcome: PASS for the stated exact unshifted binary core. No new kappa.**
This is a separate OpenAI-assisted mathematical/code review, not a human
review, proof-assistant certification, or numerical verification of a
transcendence theorem. The author implementation is neither imported nor
used as an oracle by `independent_check.py`.

Reviewed proof SHA256:
`d9b2029c6e65e715563be10ae4cf41e12491281bb44e0cfdf7167a3b6dff3b45`.
Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`.
The all-order combinatorial predecessor is
[085b30f8e036f69421d5953d0993ac4974ec3f24](https://github.com/CubeJerry/integer-mult-bounds/commit/085b30f8e036f69421d5953d0993ac4974ec3f24).
The retained A9 proof has SHA256
`3e87c32b9cb3695dc42c2ef10da9c05e74d1742a37e49ce0fe5890ea093463dc`.
That predecessor's universal matching/counting theorem is an inherited
lemma, previously independently reviewed; the present bounded replay does
not re-prove it by enumerating examples.

## Claim checked

For `g>=1`, `N=2^g`, distinct odd primes `s_i`, positive integer powers of
two `t_i`, and a common positive integer `alpha`, put

    q_i = exp(-pi alpha^2 t_i/s_i),
    H = tensor_i [[1,q_i],[q_i,1]],
    R_N = 2 ceil((N+3)/5),
    r = min(R_N, min_i(s_i)-1).

For every simultaneous row/column ordering, the ordinary nilpotent Stein
displacement of H and its exact inverse has rank at least r. The claim is
pointwise at every declared parameter tuple, not merely generic. It gives
no rank or rounding tolerance for a shifted, chirped, physical, periodic,
larger, or stored finite-precision source matrix.

## Independent mathematical checks

### 1. Trimming and a nonzero coefficient

The inherited A9 certificate is a principal signed-matching minor whose
induced graph is a disjoint union of even paths. An even path on `2a`
vertices has a unique perfect matching. For any even requested size k no
larger than the sum of the path sizes, distribute `k/2` units among their
capacities a and keep the corresponding even prefixes. The induced
components remain even paths, so the determinant is a product of unit
signed determinants. Empty components contribute one. This proves all
smaller even sizes, rather than relying on an arbitrary vertex deletion.

Every entry of the full binary Gaussian Stein matrix is a difference of
squarefree monomials. A size-k determinant therefore has individual degree
at most k. To contribute exponent k on each bit selected by a nonzero XOR
mask v and exponent zero on every other bit, all k selected monomials must
equal `Q^v`. Its coefficient is exactly the retained signed-matching minor,
which is +1 or -1. Thus the determinant polynomial is nonzero over the
integers, including after coefficient reduction modulo two.

These are principal minors of **E(H)** with the original predecessor
indices. Forming E after compressing H is a different operation. The
independent checker uses the original positions `i-1,j-1` explicitly.

Both `R_N` and `s_min-1` are even, and `r>=2`. Hence trimming to r is
admissible and gives every individual degree strictly below every s_i.
The proof correctly applies this construction separately for each order;
there is no specialization of the high-degree product over all orders.

### 2. CRT injectivity and the classical input

Let pairwise coprime moduli `m_i>=2` and numerators `u_i` coprime to their
own moduli be given. For `M=product m_i`, the integer weights
`e_i=u_i M/m_i` distinguish every exponent vector in the box
`0<=a_i<m_i`: reduction of a purported collision modulo m_k leaves only
the k-th term, whose multiplier is a unit. Its difference is both zero
modulo m_k and strictly smaller than m_k, so it is zero. Primality is
sufficient for the source tuple, but pairwise coprimality and unit
numerators are the exact hypotheses of this algebraic lemma.

With `S=product s_i`, put `z=exp(-pi alpha^2/S)` and
`e_i=t_i S/s_i`. The odd-prime/power-of-two hypotheses give the needed
units and make every exponent an integer. The common alpha belongs in z,
so divisibility of alpha by any or all of the source primes is harmless.

I independently opened the original primary source: A. Gelfond,
*Sur le septieme probleme de Hilbert*, Bulletin de l'Academie des Sciences
de l'URSS, no. 4 (1934), pp. 623-634, specifically the logarithm-ratio
theorem on p. 628. The [official record](https://www.mathnet.ru/eng/im4924)
links the [original text](https://www.mathnet.ru/links/c0cf84a10d83188958c7ee31f49617b3/im4924.pdf).
For nonzero algebraic numbers different from one, the theorem excludes an
algebraic irrational ratio of their complex logarithms. If z were
algebraic, the selected values `log z=-pi alpha^2/S` and `log(-1)=i*pi`
would have ratio `i alpha^2/S`, algebraic and nonrational, a contradiction.
This verifies the use of Gelfond-Schneider, with Schneider's independent
historical credit retained. `SOURCE-REVIEW.json` records the citation.

Consequently each chosen minor maps to a nonzero univariate integer
polynomial in a transcendental z. It is nonzero at that exact z. Applying
the argument independently to each order proves the simultaneous
pointwise conclusion without enlarging the degree of a polynomial.
No finite enumeration or floating exponential certifies this classical
transcendence premise.

### 3. Inverse transfer and source scale

Each factor is positive definite because `0<q_i<1`. The two Schur
complements of `[[A,Z],[Z^T,A^-1]]` give

    rank E(A) = rank(A^-1 - Z^T A^-1 Z).

Applying this to A inverse and conjugating by the reversal permutation J
gives `rank E(A^-1)=rank E(JAJ)`. Reversal is another allowed vertex
ordering, so the inverse lower bound follows without persymmetry.

The retained source uses a common integer alpha, distinct original odd
primes, and target sides in `{r_source,r_source/2}`. Its exact narrow
identity has `gamma_i=pi alpha^2 t_i/s_i`. For `h=j-i`, its linear factor
is an actual diagonal similarity with diagonal
`exp(-2 gamma_i shift_i x)`, and the separate centered quadratic factor
is a second chirp similarity. Removing **both** identifies the unshifted
two-point core. A coordinate translation does not change its differences.
The proof correctly assigns no ordinary Stein-rank invariance to either
similarity and claims no free execution of those changes of coordinates.

The source relation `log s_min=Theta(p^(1-epsilon))` gives the full linear
floor when `R_(2^g)<s_min`. In particular `g=o(p^(1-epsilon))` suffices
eventually. When `g=Theta(p^beta)` with `beta>1-epsilon`, the degree cap
is active and only `s_min-1=exp(Theta(p^(1-epsilon)))` is supplied. This
is superpolynomial in p but not linear in `2^g`; the equality case needs
its constants. These asymptotic statements are consistent with the exact
minimum in the theorem.

## Independent executable evidence

The checker constructs signed matching matrices directly from XOR labels,
extracts paths from the resulting matrix entries after cancellation, and
checks their minors by separate exact Fraction elimination. It expands
Gaussian determinants with a subset dynamic program over polynomial
dictionaries. It compares (a) the complete multivariate determinant followed
by substitution and (b) substitution in the original matrix entries
followed by a univariate determinant. The latter two routes share the
independent determinant engine; they are not claimed to be two separate
software implementations. The unit coefficient is additionally checked
against the Fraction determinant of the signed matrix.

Normal and optimized Python runs produced identical deterministic receipts:

| Check | Completed coverage |
| --- | --- |
| Full expanded symbolic minor comparisons | 53, containing 1,409 nonzero terms |
| Resulting rank floors | 17 of size 2; 16 of size 4; 20 of size 6 |
| Bounded even-prefix minor checks | 119, including empty and size-eight cases |
| Exhaustive finite exponent-box vectors | 730 across four boxes |
| Bounded source interval witness | primes 971, 977, 487; targets 1024, 1024, 512 at p=3 |
| Distinct controls | 11 |

Order coverage consists of the one-axis order, all six first-vertex-zero
two-axis orders, and ten three-axis orders (two declared and eight seeded
at 10703). The trim checks additionally include a declared sixteen-vertex
order. The p=3 fixture verifies primality and the exact fine-prime interval
inequalities; it does not instantiate the whole eventual source schedule.
The checker reauthenticates the three retained input files by their exact
SHA256 hashes before any algebra.

The controls demonstrate the actual failures excluded by the proof:

- At the degree threshold, `Q_1^3-Q_2^5` collapses for `(s,t)=((3,5),(8,8))`.
- Distinct odd but noncoprime denominators 9 and 27 collide already in
  `Q_1-Q_2^3`, below both individual thresholds. Repeated primes and
  nonunit numerators are separately rejected.
- Odd-size trimming is rejected. Common alpha=105, despite sharing all
  primes 3,5,7, preserves the complete 105-element exponent box.
- The actual four-point homogeneous Gaussian similarity control has
  Stein rank 2 before, rank 4 after `diag(1,2,3,4)`, and exact displaced
  determinant `-3/512`. A second, symbolically expanded three-point
  Gaussian similarity has determinant `q^2(1-q^4)/12`.
- A five-point Gaussian Toeplitz matrix has Stein rank 2, while its
  irregular section on indices 0,1,3,4 has Stein rank 4. Thus section
  lifting cannot be assumed. Exact rational source exponents separately
  detect omission of the shift and omission of the chirp.
- In the theorem's abstract parameter family, alpha=10, primes 5,7
  and targets 8,8 make every off-diagonal entry less than `2^-16`, using
  only `pi>3` and `e>2`. Downward sixteen-bit rounding then gives the
  identity, whose Stein rank is one. This illustrates the missing
  quantitative margin; it is **not** a counterexample at the retained
  source's legal alpha(p), Cp, and full production parameters.

## Reproduction and limits

When the review script is installed beside the package's `inputs/`:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
```

From its present separate review directory, supply `--package` with the
package path. The default prints a receipt and does not write files;
`--write PATH` explicitly saves one. Assertions are not used as validation
gates, so optimization leaves all checks active.

For a representation as an exact sum of lower/upper triangular Toeplitz
products with separately stored full generator vectors, rank at least r
forces at least r terms and at least `2Nr` scalar slots. This is a lower
bound for that stated format, not equality for the actual optimum and not
a machine-time, arbitrary-storage, or multiplication lower bound. Exact
transcendental scalars are not a finite-bit implementation. Source access,
setup, gauge application, transport, restoration, recursive children,
coefficient production and finite-precision errors remain separate costs.

No minor magnitude, condition number, singular-value gap, Cp tolerance,
periodic/rectangular/mixed source result, or larger-block rank transfer is
proved here. The theorem materializes neither a source page nor a caller.
All five selected assumptions and the accepted multiplication frontier
remain unchanged. No substantive defect was found in the frozen scoped
proof; the exact specialization is a useful reduction of a previous
generic exception, with the source boundary and quantitative obligations
still explicit.

Prepared for Jerry Chen / @CubeJerry by an independently executing OpenAI
review agent. The author and lead supplied the proposed claim and source
pins; the reviewer independently derived the algebraic steps, read the
primary transcendence source, and wrote the separate checker and controls.
