# B review: the integer assembly part of A's physical ledger

Status: **bounded independent review completed; no missing asymptotic factor
found in the assigned integer-assembly interface**. This does not certify the
separate finite-template generator, affine-stream compiler, or whole overhead
theorem.

Reviewed file: `../A/physical-compiler-ledger.md`, SHA256
`4450f436175b5d0ab2334b9478809d59d39a27723135e664c21023a40c073a9d`.
Read against the November 24 tape source at
`3344da59991ed94f9ba711217b29c1d760badfa6`, principally `integers.tex`
(all 491 lines), `permutations.tex` (all 236 lines), and the work/space and
precision parts of `walsh.tex`. This is a mathematical audit, not a replay of
a physical Turing-machine implementation.

## 1. CRT preparation has a uniform polynomial degree

For `l=20 ceil(log2 k)`, an ordinary axis has at most `2^20 k^20`
positions. Trial division through all candidates and all possible divisors
therefore takes a fixed polynomial in `k`, with constants independent of the
selected Fourier/interchange template. The one possible short final axis is
smaller. The source tests the successful shape explicitly. Its fixed
prime-gap cutoff is independent of the exponent parameter.

For a prescribed left-control address, reconstruct the original digits
successively from the triangular CRT equations. Maintain
`B_i=sum_{j<i} P_j t_j`, which has at most `k+O(1)` bits, and compute
`t_i=y_i-mu_i B_i mod a_i`. Schoolbook arithmetic gives a fixed polynomial
bound for all `O(k)` axes. The right rotations use the reconstructed sum,
and each complete short-axis table has at most `2^20 k^20` entries. This
does not introduce an exponent depending on `P`.

At a fixed balanced-tree depth the left children contain at most half the
ordinary axes; the unequal final axis changes the bit count by only
`O(log k)`. Thus a fixed free fraction, for example `1/4`, is valid above
an absolute cutoff. Both directions require `O(log k)` depths.

## 2. Short transforms fit the claimed degree envelope

A block contains at most seven axes, hence at most `2^140 k^140`
coordinates. A direct explicit permutation table, quadratic cycle scans,
and the Beneš construction all have fixed polynomial degree. Even allowing
word arithmetic, allocation, every layer, and all `O(k)` blocks leaves the
proposed degree 1000 a very generous common envelope. There is no recursive
call to an unspecified template-dependent short-transform algorithm here.

The phases are sums of polynomially many roots of unity of polynomial-size
order, followed by a bounded number of arithmetic operations and square
roots. In the source, `1-|z|^2>=3/4`, and the pair-factorization divisors have
the positive lower bound `(sqrt(3)-1)/(2 sqrt(2))`. Thus `Ck+O(log k)`
fractional bits suffice uniformly. Schoolbook implementations of the table
preparation are polynomial in `k`; their slowness affects setup only.

For a complete diagonal, prefix extension produces fewer than `2N`
products, not `N` times the number of blocks. Its two alternating streams
have total volume `O(Nk)`. The record products must retain the fixed
`O(k log k)` short multiplier; using schoolbook multiplication for these
`Theta(N)` products would indeed lose the proposed time bound. A's ledger
explicitly retains the required multiplier.

## 3. The fourth logarithm is sufficient

The controlled-block lemma costs
`P^{O(1)} V k^rho (1+log k)^3` per layer, after the proposed guard adjustment.
Its three factors are the guard/position-permutation cost, the block batches,
and the Beneš stages. There are `O(log k)` CRT depths and `O(log k)` short
Fourier layers. Each is composed sequentially, so their cost is added; they
do not create a product of the two layer counts. Consequently

`P^{O(1)} Nk k^rho (1+log k)^4`

covers them all. Walsh layers cost only one such logarithm before the
outer layer count; phases and pointwise products cost `O(Nk log k)` per
layer. These fit inside the fourth-power envelope.

## 4. Precision and visited cells

Conditional on the stated finite-template bound, at most `P` scalar updates
with coefficient bit height at most `P` give a one-level log-norm bound
`O(P^2)`. A source recursion path has `O(log k)` levels, so an
input/error-to-intermediate gain is bounded by
`2^{O(P^2)}(1+k)^{O(P^2)}`. The setup/node envelope
`P^{O(1)}(1+k)^{1000+ceil(log2 P)}` and this gain are both below fixed
exponentials `2^{c k}` once `k>=P^C`, after enlarging a universal `C` and an
absolute cutoff. Thus a fixed absolute multiple of `k` bits per numerical
record is consistent with A's claimed large-input interface.

The source's boundary allowances leave substantial slack: input digit norm
at most `2^{4k}`, forward/inverse transform error below `2^{-40k}`, product
error below `2^{-30k}`, and final scale at most `2^{k/2}`. These suffice for
Euclidean error below `1/2` and exact coefficient recovery. Carry propagation
then uses `O(k)`-bit registers and `O(Nk)` scans.

The short multiplier may use more than `O(k)` scratch cells. This is not a
missing full-stream factor: the same word workspace is reused for every
record, and its polynomial size is absorbed by `Nk` at the stated cutoff.
The same observation applies to phase/permutation tables and descriptor
stacks. Only a fixed number of full streams is retained, and the source
depth-first child volumes form a geometric series. This supports candidate
space `P^{O(1)}n+d`, conditional on A's separate primitive compiler.

Minor presentation safeguard: a completely general template node-count
bound can include an additional factor `1+log k` for the base-arity pieces;
it is absorbed by the fixed-degree setup envelope and does not change any
conclusion. The literal source templates have ample branching for the
sharper displayed estimate.

## Scope of the finding

The integer conversion, short transforms, numerical precision, visible
logarithmic factors, and reuse of their workspaces do not reveal a new
unpaid factor. The difficult remaining dependencies are exactly the ones
outside this bounded review: the quantitatively valid finite template,
source affine operations on fixed tapes, and their common-cap compilation.
No complete new multiplication envelope is certified by this note alone.

Credits: source authors; Jerry Chen (@CubeJerry); AI-assisted independent
audit during the 2026-11-25 session.
