# A generic Stein-rank floor for every binary Gaussian vertex order

**Scoped universal theorem; no new kappa.** For a fixed positive integer d,
put N=2^d and H=⊗_i [[1,q_i],[q_i,1]]. Outside one proper real algebraic
exceptional set, every simultaneous row/column vertex ordering has ordinary
Stein rank at least

\[
2\left\lceil\frac{N+3}{5}\right\rceil.
\]

The same statement holds for every ordered exact inverse. Here the ordinary
Stein operator is E(A)=A−ZAZᵀ for the nilpotent one-step lower shift. The
exceptional set is uniform over all N! orders at the fixed dimension; its
complement is dense and has full measure in (0,1)^d. The theorem does not
claim full generic rank N or a pointwise statement for every distinct tuple.

The result closes the arbitrary-order loophole for a **generic linear-rank
floor** in this explicit binary family. Earlier lexicographic rank results
restrict the order, and symmetry-cycle results restrict the construction.
This proof permits every vertex order, including orders that follow no
single global symmetry. It is an enabling obstruction for one structural
decoder route, not a discharge of the full analytic-recovery assumption.

## Exact argument

Every nonzero XOR translation defines a perfect matching of the ordered
vertices. Superimposing that matching and its one-step truncated shift gives
one even open path and C_v alternating cycles. Its signed adjacency has rank
N−2C_v. Deleting two adjacent vertices from each cycle gives a principal minor
with determinant ±1; that value is a coefficient of the same Gaussian minor.
This supplies genuine polynomial noncancellation, including in characteristic
2, rather than inferring it from a nonzero matrix support pattern.

If m is the greatest multiplicity of a consecutive XOR direction, two
independent counts give ranks at least 2m and (N−m+3)/2. Their combination,
rounded upward to an even integer, gives the displayed bound. A two-way
Schur-complement rank identity transfers the all-order statement to inverses.
See [PROOF.md](PROOF.md) for the full argument and exact quantifiers.

For an exact expression A=Σ_j L(u_j)U(v_j), where L and U are ordinary
triangular Toeplitz factors, E(A)=Σ_j u_jv_jᵀ. Consequently at least the
stated number of terms is required generically, in every order. Separately
materializing both length-N vectors of each term takes Ω(N²) scalar slots.
This count is confined to that dense format; it does not exclude implicit,
shared, sparse, tensor or other displacement representations or algorithms.

## Reproduction and evidence

From the repository root, with Python 3.12 and its standard library:

```sh
python3 -I -W error -B research/arbitrary-order-binary-gaussian-rank/verify.py
python3 -I -O -W error -B research/arbitrary-order-binary-gaussian-rank/verify.py
python3 -B scripts/research_package.py --package research/arbitrary-order-binary-gaussian-rank
```

The direct commands print JSON with status
`PASS_ARBITRARY_ORDER_BINARY_GAUSSIAN_RANK`. They are read-only and require no
Git, network, nonstandard package or external runtime input. [RESULT.json](RESULT.json)
is the retained primary output. Normal and optimized execution must agree.
The registered commands have a 120-second limit each.

The primary checks include every translation-normalized order for d=1,2,3:
5,047 orders and 35,299 nonzero translation masks. Every retained unit minor
is computed by integer Bareiss elimination; separate characteristic-two row
elimination checks the predicted rank. Nineteen small minors are expanded
literally as multivariate polynomials. Four rational forward/inverse fixtures,
two exact kernel vectors, three lower/upper generator identities, explicit
d4/d5 failures of the stronger connected-graph test and eleven semantic or
domain controls are checked. Finite checks corroborate the universal proof.
Separate review implementations and proof assessments are recorded independently.
No independent human or formal proof-kernel acceptance is claimed.

Important controls retain the following distinctions:

- q=(1/2,1/3,1/5) has distinct positive entries but the specified exceptional
  order and the standard Gray order each have rank 6, not 8. Replacing 1/5
  by 1/7 yields rank 8 for both orders.
- In dimension 2, equal parameters q_1=q_2=1/2 admit a Gray-order rank of 2,
  below the generic lower bound 4. Homogeneity cannot be silently excluded.
- Coordinate-mask graphs miss 672 of the 5,040 normalized dimension-3
  orders. Allowing all masks covers that finite domain, but explicit
  dimension-4 and dimension-5 orders have no connected mask graph.
- Endpoint q=0/1, uncancelled parallel edges, a cyclic replacement shift,
  deleting only one cycle vertex and a dropped minor entry expose incorrect
  extensions or certificate implementations.

## Source pins, predecessor credit and scope

Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`; priority revision 8.
[SOURCES.json](SOURCES.json) pins the selected certificate, framework audit,
task catalogue and accepted #7000 review as provenance. The mathematical
proof is self-contained and imports no predecessor scientific program or data.

Credit the following published research packages and their preserved lineage:

- [Lexicographic tensor rank](https://github.com/CubeJerry/integer-mult-bounds/commit/326844a3e0c570fdafa4f3737095cd37154743a6),
  whose restriction to lexicographic orders motivates this question.
- [Orbit-order construction](https://github.com/CubeJerry/integer-mult-bounds/commit/8f1a09fb4f696bd5f20e1953210936308571416e),
  which proves that homogeneous coordinate reordering can help.
- [Optimal symmetry-cycle scale](https://github.com/CubeJerry/integer-mult-bounds/commit/2ae2fa14eeefe301652f62313b137a97036ab13d)
  and [heterogeneous Gaussian symmetries](https://github.com/CubeJerry/integer-mult-bounds/commit/be76d6ae53fc887f977a04ceaa6ef56bb9e98fb7),
  which concern one global-symmetry successor class.

Classical matching components, displacement generators, Schur complements
and polynomial zero-set facts retain their credit. Olshevsky, Oseledets and
Tyrtyshnikov's [tensor/displacement paper](https://doi.org/10.1016/j.laa.2005.03.040)
is relevant background, not a source for the present all-order conclusion.
The bounded overlap check in [OVERLAP.md](OVERLAP.md) distinguishes
[#1754](https://github.com/CrocSwap/integer-mult-bounds/pull/1754),
[#4198](https://github.com/CrocSwap/integer-mult-bounds/pull/4198),
[#6228](https://github.com/CrocSwap/integer-mult-bounds/pull/6228),
[#6239](https://github.com/CrocSwap/integer-mult-bounds/pull/6239) and
[#7263](https://github.com/CrocSwap/integer-mult-bounds/pull/7263).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance.
The lead proposed the arbitrary-order question and complementary matching,
support and inverse observations; the worker derived the unit-minor and
combined-count proof and wrote the primary checks. The lead and another
agent independently checked critical obligations. This is separate AI review,
not independent human or formal-kernel certification. Apache-2.0.

All five foundational assumptions remain. The selected accepted complete
conditional bound is unchanged. A generic theorem does not identify actual
fine-prime parameters: a discrete source family may lie entirely inside an
exceptional algebraic set. Rounding, conditioning, gauges, actual source
acquisition, periodic/rectangular interfaces, full caller costs and complete
multiplication recurrence remain outside this package. No selected cold
replay, predecessor scientific suites, Lean, Docker or hosted CI is claimed.

## Open next questions

1. Is the Stein determinant a nonzero polynomial for every order in every
   dimension? The connected-translation certificate fails in dimensions 4
   and 5; a new noncancellation argument or a generic counterexample is needed.
2. Does a pinned actual source family avoid a certified minor's zero set
   with enough margin for its rounding budget? Exact source parameters and
   a quantitative norm/determinant bound are both missing here.
3. Can an implicit or alternative-format application improve a complete
   source caller after setup, access, precision, transport and restoration
   are charged? The dense-generator slot count alone gives no runtime answer.

## Executed independent review

`review/REVIEW.md` records a separate proof derivation and standalone symbolic/rational checker. Normal and optimized runs agree. Coverage includes 22 fully expanded small minors, 35,299 exhaustive translation graphs, 872 larger sampled graphs, 33 exact rational rank/minor checks, the full exceptional determinant identity and seven failure controls. This evidence corroborates the written all-d proof; it does not establish source-specific nonvanishing or a rounding margin.

```sh
python3.12 -I -W error -B research/arbitrary-order-binary-gaussian-rank/review/independent_check.py
python3.12 -I -O -W error -B research/arbitrary-order-binary-gaussian-rank/review/independent_check.py
```
