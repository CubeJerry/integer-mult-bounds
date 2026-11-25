# Lead acceptance: full-rate formula construction and uniform envelope

Status: **accepted written theorem for the specified source implementation**.
Reviewed during S002, 2026-11-25 UTC. The finite-constructor gate is closed.
The accepted physical compiler and common-cap machine are reused through
stated interfaces, which the new representation satisfies. This is an
AI-assisted mathematical audit, not a formal kernel proof or full execution.

## Sources and new proofs actually read

The lead read complete B `formula-full-rate-linearization.md` (FL1--11,
including the retained scalar phase), C `FORMULA-CYCLOTOMIC-GENERATOR.md`,
and A `formula-extraction-theorem.md` (F1--13). The original physical
compiler ledger and full uniform assembly were reread, as were source
integral prediction/matrix-root, binary implementation, kernel and tape
Walsh padding interfaces. Earlier complete source reads retain their scope.

The tensor sum is established mathematics. The lead retrieved and read
Sheng--Tribone, *Tensor products of d-fold matrix factorizations*, DOI
[10.1017/nmj.2025.12](https://doi.org/10.1017/nmj.2025.12), Definition 3.1,
Proposition 3.2 and its ring hypothesis. Only a ring homomorphism from the
integral cyclotomic ring is required; specialized roots need not retain
primitive order. No priority claim for that tensor operation is made.

## Full-rate factorization and actual formula size

The invariant includes every cyclic rotation, not merely one ordered
product. Products concatenate factor lists on separate tensor coordinates.
Identity padding and scalar absorption handle unequal degrees and zero
constants. At a length-d sum, total-grade pieces have dimension d*r*s.
The integral Gaussian-binomial identity makes each d-stage product equal
to (f+g) times the whole identity. Every row accepts independent input.

The balanced count-coefficient formula copies subexpressions into a real
tree. Syntactic degree is bounded by the coefficient index; no high-degree
cancellation is used. Its explicit recurrence gives size
[8(D+1)]^(ceil(log2(m))+3)=2^{O((log m)^2)} for the original rare-tail
D=O(sqrt(m log m)). Width is at most D^S. Source shift phases are retained
as scalar factors. Fixed shape/degree budgets give equal widths for shifts.

## Specialization, coefficient heights and bounded generation

One common cyclotomic conductor, chosen from pre-descent width R, includes
all factor lengths and a power of two at least R. It is at most 2R^2
above an absolute cutoff, with a baseline for bounded initial cases.
The algebra is finite free over Z[1/2]. All odd-characteristic reductions,
including primes dividing the conductor, preserve the identities. Check
nodes belong to a power-two subgroup and have the explicit unit differences
required by Hermite repair. Basis expansion uses the existing block maps;
it does not require a circular second enlargement of the node set.

The proof supplies bounded loops for cyclotomic polynomials, formula
factors, all shifts/frequencies, Hermite maps and basis multiplication.
Assembly copies/twists affine coefficients; it does not repeatedly square
coefficient matrices. Unreduced logarithmic heights are polynomial in
formula size and original scalar heights. Root exponent reduction modulo
the conductor, then in its monic cyclotomic basis, adds at most quadratic
conductor bit height. Explicit difference inverses and Lagrange products
have polynomial height as well. Dense schoolbook construction therefore
has a fixed polynomial actual bill in the expanded bound. This conclusion
is not inferred merely from the final output size of an arbitrary machine.

Numeric rational-address magnitudes and the compatible radix still obey
2^{m^{O(1)}} bounds. Combining all data gives the absolute envelope

    P_m <= 2^{2^{C(log2(m+2))^2}},

including generation, workspace, scalar bit heights and numeric address
values. Finite algebras use basis coordinates, not tables of every element.

## Physical interfaces and complete profile

The source shared-pencil construction accepts arbitrary fixed matrices
at each stage. Replacing b repeated stages by D<=b possibly different
stages preserves every previous call bound. Labels, shifted defects,
Hermite repair, occupied reserves and recursive child volumes are unchanged.
Thus the strict tests and log2 m_j=O(J^3 log2 J) search remain valid.

The source allows arbitrary integer W: binary batches use ceil(2^s/W),
and tape Walsh pads the leading row range to a multiple of W^J. The
quarter pre-padding margin and existing cutoff pay this cost. An optional
direct-residual wrapper is unnecessary for this compiler.

The complete finite data fit the accepted polynomial-P physical ledger:
instruction access, scalar encoding, numerical norms/precision, short
multiplication, preparation, address changes, clocks, stack parking, CRT
and carries all remain charged. The threshold is max(U_abs,2^{P^K}), with
one absolute source cutoff. Common-cap chunking and the fixed schedule give

    log2 D_j, log2 L(N_j) <= 2^{C J^6(log2 J)^2}.

The lead independently checked F1--F13. For s=log2 L(n), z=log2 s, select
J as the largest dyadic number below [z/(2C(log2 z)^2)]^(1/6). The profile
is at most sqrt(s), proving eligibility and a negligible prefactor beside
s/J. One fixed exact deterministic finite-alphabet multitape machine has

    T(n)=O(n sqrt(L(n))
            2^{O(s(n)(log2 log2 s(n))^(1/3)/(log2 s(n))^(1/6))}),
    visited cells=O(n), L(n)=1+log2 n.

Generation stays inside timed attempts. Chunking includes all products,
movement and carries. The correct fallback supplies totality. No compact-IP
hypothesis is a premise of this unconditional written theorem.

## Exact finite evidence and limits

The unchanged B checker, copied into a fresh directory, passed 196 rotated
formal-polynomial matrix identities and 264 unfolded formula size/degree
checks, including zero children, unequal degrees and ramified reductions.
Wrong twists, wrong grades and a one-product-only invariant are rejected.
The independent C checker passed 120 cyclotomic height checks, 25 integer
and 75 odd-characteristic inverse identities, 522 Gaussian coefficients
(138 ramified), and 216 rotated products in 48 ramified examples. A nonzero
square-zero partial sum rules out a false unit-denominator shortcut; a
noncyclotomic root is rejected. Isolated records preserve script hashes.

Finite tests corroborate the algebra. The all-size constructor and rate
rest on the written proofs. No giant template, complete multiplier, formal
build, practical crossover or independent human refereeing is claimed.
Absolute constants remain unevaluated. The envelope improves the programme's
previous explicit bound, without a comparison against an unspecified
published o(1). It still does not reach 2^{O(s^beta)} for beta<1,
polynomial-s overhead, or the constant endpoint.

## Final independent synthesis gate

The lead read C's complete `REVIEW-A-FORMULA-EXTRACTION.md` and A's complete
`review-formula-linearization.md`; both pass. B's separate
`varying-pencil-source-interface-audit.md` also passes. The final theorem
is unconditional within the stated exact source implementation, with no
remaining compact-representation premise. C's wording refinement is
retained: comparisons with s^beta refer to the displayed upper-bound scale,
not a lower bound on the actual running time.
