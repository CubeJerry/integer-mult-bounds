# Fixed-tape execution of succinct row permutations

Status: proved component; independent review pending. This supports a
structured finite-template executor. It does not itself establish that all
matrices in the multiplication construction meet the stated interface.

Source: the elementary fixed-tape scans in OpenAI `math` at
`3344da59991ed94f9ba711217b29c1d760badfa6`, September tape
`build/sections/02-streams.tex`, and November tape `build/uniformity.tex`.
This note makes the dependence on a growing number of independent rows
explicit instead of representing each row by a separate machine tape.

## 1. Uniform row-permutation lemma

**Lemma SR1.** Let an array be in lexicographic order on
`[P] x [R] x [B]`, with volume V=PRB and positive integer ranges. Put
`h=ceil(log2(2R))`. Suppose a fixed deterministic algorithm, given a
parameter description of at most K bits and r in [R], computes a
permutation pi(r) of [R] in at most poly(K+h) actual steps and space, with
an absolute polynomial. Then one fixed finite-alphabet multitape machine
moves every whole B-symbol row from r to pi(r) in

    V*poly(K+h) actual steps and cells ever visited.       (SR1)

The constants do not depend on P,R,B. The description is not rescanned
through an unrelated exponentially large finite artifact.

Proof: scan each prefix fiber and attach the h-bit destination pi(r) to
its row. The r counter has O(h) bits and each map calculation is charged
once per complete row; because B>=1, PR*poly(K+h)<=V*poly(K+h).
Compute pi from the bounded parameter description and row counter, without
reading the long prefix or suffix indices. Stable-sort the whole tagged
rows by destination with h binary LSD passes, using two output tapes per
pass and per-prefix boundary counts. Every pass moves at most
O(V+PR*h) cells. Reading a key bit by scanning its complete h-bit header
is allowed, so all h passes cost O(V*h+PR*h^2). Remove the keys. Bijectivity
ensures exactly one incoming row at every required destination.

A row's internal order is never changed. Counter reset for its B symbols
costs O(log(2B))<=O(B); increments are amortized by the source ripple
argument. A fixed number of canonical descriptors is prepared once at
fixed polynomial cost in log(2V)+K, which fits V*poly(K+h). Unrelated long
prefix counters are only advanced and tested. Tags occupy PR*h<=V*h cells;
the sort uses a fixed number of full-volume tapes and reuses them. This
bounds visited cells as well as live data. QED.

The method is a sequential tape algorithm. It does not postulate random
access, constant-cost variable-width comparison, or R physical tapes.
No near-root interchanger is invoked, so there is no recursive circularity.
A positive integer R need not be a power of two.

## 2. Diagonal weights and a sum of monomial maps

Symbols may instead be fixed-length coordinate blocks representing a
finite field or finite commutative algebra. Let each block contain d bits,
with d<=poly(m), and suppose exact addition/multiplication of two such
blocks and generation of the row weight mu(r) cost poly(m+h) actual bit
steps, uniformly. The payload length B is then a multiple of d.

**Lemma SR2.** A map on the R independent rows of the form

    A=sum_(s=1)^S Diag(mu_s) P_(pi_s)                  (SR2)

has a fixed-tape implementation in

    V*S*poly(m+h) steps and V*poly(m+h) visited cells,

provided S<=poly(m), the common parameter data is polynomial in m, and
pi_s and mu_s satisfy the stated uniform algorithms. Zero weights permit
masks. Every input row is arbitrary and independent; no row is assumed to
be initialized to zero or set aside as an output register.

For each s, copy the original input into one reusable work region. Apply
SR1 to pi_s; multiply every symbol in the destination row by mu_s of that
destination, computed once for that row. Accumulate into one ordered
output array using exact aligned scans. Erase/reuse the work region for
the next term. Initial zeroing of the output is internal paid workspace,
not an additional independent parent input. There are only a fixed number
of live payload arrays. This proves the statement. Per-record scalar
arithmetic is paid explicitly; no expanded algebra truth table is assumed.

The same conclusion applies if weights are specified at source rows:
compute them before permuting instead. No inverse of pi_s is required.

## 3. Tensor spectators and small dense factors

For a factor acting on one or several tensor coordinates, flatten the
complete module index to r. A succinct arithmetic rule for changing those
coordinates is an eligible pi_s when its bit complexity is polynomial
in m+log R. All unused tensor coordinates remain occupied and independent.
SR1 permutes their records as spectators and preserves them exactly.
It is not necessary to expand the R-by-R permutation matrix.

If a map has the form H0 tensor I_w with a p-by-q matrix H0, p,q<=poly(m),
and scalar entry arithmetic is polynomial in m, its full application can
be implemented by at most p*q serial copies, small-coordinate reindexings,
weights and aligned additions. Each copied w-row block retains all its
independent data. The work/space is polynomial in m times the input-plus-
output volume. A rectangular check map is charged at its actual output
volume; this observation does not turn extra zero rows into independent
parent inputs.

## 4. Interface to the source pencils

For an affine pencil A0+sum_j Aj Qj, the Qj act on the per-row address
fields and the Aj act on the row index. SR2 implements the Aj operations
at whichever common physical layout the source shared-swap proof uses.
It does not change the source's recursive Qj invoice. The source's label
mixing and endpoint coordinate changes require their own bounds; here
only their finite row maps are given a compact executor.

To use SR2 for the characteristic-two cyclic formula construction one
must prove, separately, that every actual factor has polynomially many
masked monomial terms, coefficient field degree polynomial in m, and
index/weight algorithms with polynomial description and execution cost.
A matrix being sparse as a mathematical object is insufficient without
those uniform procedures. C's E002 structural decomposition is the
proposed supplier for this interface, subject to independent review.

## 5. Open next questions and credit

The remaining bridge is exact application to every predictor, query,
check/inverse-check and repair operation, including coefficient selection
from the spectral pattern. An exponentially large table may remain an
additive construction artifact only if this executor never scans it per
row or symbol. A fixed structured interpreter must dispatch the compact
operations directly.

Credit: Jerry Chen (@CubeJerry), source elementary tape scans and uniform
serialization, established stable radix sorting, the session lead's
whole-row sorting observation, and substantial AI-assisted E002 work.
The contribution is the explicit fixed-tape cost/space interface for a
growing, exponentially numerous collection of independent rows.
