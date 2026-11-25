# Independent review of deterministic sparse residual recovery

Reviewer: Route C, S004. Status: **R1 passes the algebraic and physical
component audit**, subject to the stated sparse-residual promise. This
does not supply the missing fast candidate or a new multiplication bound.
The reviewed source is Route B's `deterministic-sparse-residual-repair.md`,
read in full; its reference checker was replayed in an isolated directory.

## 1. Collision-free lengths and signed packed coefficients

The all-moduli family is valid without primality. If a length ell creates
a collision, it divides one support difference and therefore the product
of all differences. If every ell up to K creates a collision, their least
common multiple divides that product. The lcm lower bound exceeds its
known size, giving a contradiction. The implication used is
`ell does not divide Delta => ell divides no individual difference`,
which is valid even for composite ell; coprimality is not assumed.

Each `binom(K-1,j)` divides `lcm(1,...,K)` by the factorial valuation
formula: every prime-power term contributes zero or one, and there are
at most `floor(log_p K)` nonzero terms. The maximum binomial coefficient
is at least the row average. This proves the stated lcm estimate and the
explicit K cutoff, including small values.

The bound `R>8D(s+1)(Emax+1)` pays for coefficient collisions, signs and
Euler weights. Value folds have coefficients bounded by `s Emax`, and
derivative folds by `D s Emax`, both strictly within the balanced-radix
margin. Their evaluations lie in the centered interval modulo `R^ell-1`.
Balanced digit extraction is therefore injective and recovers the true
signed fold, including ell=1 and cancellations in a bucket. A carry cannot
masquerade as a coefficient.

The product modulus may have common factors among its components. Only
divisibility by every component is used, so no CRT uniqueness assumption
is hidden in the proof.

## 2. Unknown support and acceptance soundness

At a collision-free length, each nonzero bucket contains one coefficient c
and its weighted value e*c, so the ratio yields the integer exponent e.
Every generated candidate is checked for exponent range, residue class,
coefficient height and at most s terms. Distinct buckets cannot yield the
same exponent because their required residue classes differ.

Passing the product-modulus check is sound under the promise: the difference
between truth and candidate has at most 2s terms and height at most 2Emax.
A collision-free length for that difference must reveal a nonzero fold.
The centered-radix bounds prevent its nonzero evaluation from being a
multiple of the corresponding modulus. Thus a false accepted candidate
is impossible under the promise, including accidentally integral ratios
or zero coefficient sums at other lengths.

The squared product polynomial used as a negative control is essential.
It and its Euler derivative vanish at every proposed fold while the
polynomial is nonzero. Its degree and height bounds are correctly stated.
The algorithm consequently remains a promised sparse corrector, not a
general exact product certificate or a Las Vegas verifier.

## 3. Short arithmetic and long tape scans

The chosen k bounds the bit length of the product modulus. For
`mu=floor(2^(2k)/M)` and `u<M*2^k`, the downward reciprocal error is less
than one in the quotient. The proposed quotient differs from the true
floor quotient by at most one, so one correction subtraction suffices.
The products have at most a fixed multiple of k bits, even when the
reciprocal itself uses up to 2k bits. The same fixed short multiplier
therefore gives the claimed time on each stream block.

Forming the derivative records is explicitly charged. Each index times
coefficient multiplication has O(beta)-bit operands and costs
`O_alpha(beta(1+log(beta+1))^alpha)`. There are O(D) records, and their
index updates, rewinds and copies fit the O(V) scan term. Splitting signed
records into positive and negative streams adds only a constant number
of scans and reused streams. Fixed-width records may be written in
increasing coefficient order, then read backwards with the corresponding
bit order to obtain a most-significant-first packed integer; this costs
O(V), not a separate array-sort expense.

All candidate decoding, exact ratio divisions, repeated squaring, short
modulus construction and support sorting have a fixed polynomial bound
in k. The displayed k^6 estimate is deliberately loose but sufficient:
`K,s,log D=O(k)`, and grade-school modular arithmetic uses O(k^2) steps.
One candidate, one fold pair and a constant number of O(k)-bit accumulators
are enough. The procedure does not retain K copies of the input.

## 4. Uniform visited space and fallback

When k<=V, all persistent streams and short-data work fit O(V). There is
a fixed number of tapes. Their work intervals are marked, cleared and
reused at the same origins, so this bounds the union of visited cells.
The fixed short multiplier has its own O(k) visited-space guarantee;
its constants are allowed to depend on the one fixed alpha.

When k>V, direct multiplication in the large radix R is correct because
all true ordinary convolution coefficients are below R. Schoolbook work
uses O(V^2) time and O(V) visited cells, and V^2<k^6. Recovering the residual
and carrying the corrected coefficients into the original radix add O(V).
This fallback is necessary: a bare claim of O(k) scratch would otherwise
violate the desired common O(V) cap for large supplied s.

## 5. Multiplication-scale interpretation and remaining bridge

With b of order log n, h of order n/log n and candidate coefficient height
O(log n), beta is of order log n, hence V is of order n. For every fixed
polylogarithmic sparsity exponent, k is a fixed power of log n; the k^6
term is lower order and the stated `n(log log n)^(3/4)` repair bound follows.
For fixed `0<tau<1`, the wider `s<=2^((log n)^tau)` regime and choice
`alpha=(1+tau)/(4tau)>1/2` also give the stated sub-root repair expense.
The proof does not substitute a growing parameter into an alpha-dependent
constant.

The missing theorem is a candidate constructor with a proved ordinary
residual sparsity bound at a useful total cost. The transform-level dense
error obstruction in the companion note is compatible with R1, but it
must remain in its stated independent-input transform plus coordinatewise
decoder model. It is not, by itself, a proof that every possible later
composition has a dense integer-product residual.

No Weak ETH assumption enters this upper-bound component. The derivative
ratio and modular interpolation viewpoint are credited to existing sparse
interpolation work; this review does not claim an exhaustive literature
novelty check or that those external papers were fully reconstructed here.

## 6. Actual independent replay

```sh
python3 replay-sparse-residual/verify_sparse_residual.py
```

Passed: 4,950 binomial/lcm divisibilities; 1,090 collision-family supports;
3,618 signed value/derivative folds; 465 long modular reductions comprising
2,811 reciprocal blocks; and 33 full sparse-recovery cases, seven requiring
a nontrivial fold. The zero-sum collision and wrong-reciprocal controls were
rejected. The dense false certificate passed all 28 fold probes as intended,
demonstrating the necessity of the sparsity promise. The checker also ran
12,480 ordinary rounding output checks for the companion dense-error claim.

The replay uses exact reference integers and explicit small arrays. It is
not a fixed-tape execution, a proof by finite enumeration, a formal build,
or human refereeing. Both the source checker and JSON output are retained.

Credits: Route B's construction and proof; source OpenAI short multiplication
theorem; established sparse interpolation and modular arithmetic methods;
lead and Route C independent reviews; @CubeJerry; substantial ChatGPT
assistance.
