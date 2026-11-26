# Independent review of the row-space/Walsh rank gate

Decision: **accept RG as a scoped exact rank and operator-norm theorem**.
No blocking gap was found. This is an independent written review and
an independently implemented finite replay; it is not a Lean/kernel
verification, human referee report or tape-runtime lower bound.

Reviewed proof: `../lead/rowspace-walsh-rank-gate.md`, SHA-256
`0dbf77a282e0f7417169fb0153e8255aad5c4f149c7b6d528c2b74ca44ea5cda`.
The source numerical interface is the normalized one-slot Walsh transform
on complete independent records, as in pinned OpenAI tape `walsh.tex`.

## The invariant separator is valid for every orbit block

The predicate is invertibility of the first A columns of the address
matrix. Multiplication on the left by GL_A(F2) preserves its determinant,
because the only nonzero binary determinant is one. Row-space classes
are exactly these left-GL orbits, including rank-deficient matrices.
Therefore a processor preserving every row space commutes with the
separator even if it mixes all R independent copies inside the block.
In particular its compressed P_0 D P_1 block is zero. No assumption
that D is a product of group permutations is needed.

## Halfspace blocks and the binary radical

For fixed remaining rows B, full rank of its first A columns is exactly
the condition that the determinant, as a function of the varying first
row, is a nonzero linear functional c. A nonzero kernel vector of B_0
is unique over F2, agreeing with the cofactor vector. If B_0 is rank
deficient the separator-one side is empty.

On a full-rank fibre the relevant Walsh block has input c dot x=1 and
output c dot y=0. Translating the input halfspace gives a harmless
diagonal sign on output rows and the character matrix of U=c-perp.
The radical is U intersect span(c): dimension zero for odd-weight c,
dimension one for even-weight c. Thus its normalized nonzero singular
values are respectively 1/sqrt(2) and 1, with ranks 2^(f-1) and
2^(f-2). The possible isotropic case is included, not discarded.

The independent implementation verified this without numerical singular
values. It formed the literal integer halfspace matrix M, then checked
that G=M M^T satisfies G^2=(2^(f-1)t)G, t in {1,2}, and used its trace.
Positivity follows from G=M M^T; this polynomial identity fixes every
nonzero eigenvalue. Literal rational Gaussian ranks give a second
method at small f.

## Full-array multiplicity and rank fraction

The fraction of full-rank (A-1)-by-A binary matrices is
product_(j=2)^A(1-2^(-j)). Each hyperplane has the same number of ordered
bases, so the nonzero cofactor vector is uniformly distributed. There
are 2^(A-1) odd-weight and 2^(A-1)-1 nonzero even-weight vectors.
The other f-A columns are unconstrained and contribute exactly
2^((A-1)(f-A)) choices. Walsh leaves B unchanged, so these fibres
form an orthogonal direct sum, and the R copies multiply rank by R.

These counts reproduce beta_A exactly. In particular beta_2=5/16,
beta_3=33/128 and beta_4=483/2048. The elementary product bound gives
alpha_A>1/2; the remaining factor is >3/8. Therefore beta_A>3/16.
The formula R N beta_A is integral because it was obtained by counting
actual fibre ranks, not by rounding a limiting density.

## Low-rank approximation conclusion

The nonzero right-singular subspace of M=P_0 H P_1 has dimension rank M
and lies in the P_1 input space. If rank(P_0 E P_1)<rank M, this subspace
meets the kernel of P_0 E P_1 nontrivially. A unit vector in the
intersection retains norm at least 1/sqrt(2) under M. Projection cannot
increase the full error norm. This proves RG3 for arbitrary E, with no
conditioning or norm restriction on D or E. The exact conclusion follows.

## Actual replay

Command:

    python -I -B research/moonshot-overhead-program/sessions/2026-11-26-S005/route-b/review_rowspace_rank.py

It passed 120 exact character-Gram checks, 26 literal rational-rank
checks, 86,112 explicit GL separator checks, full cofactor distributions
for A=2,3,4, and fibre-count identities for f=A,A+1,A+2. The omitted-
radical control c=11 has rank one rather than two, as required. The
receipt and source hashes are `rowspace-rank-independent-verification.json`.

The result rejects an orbit-preserving processor plus a correction of
vanishing relative rank for this isolated child. A fully priced
cross-orbit transform, changes of representation, additional workspace,
or whole-pencil cancellation remain open. A rank fraction is not an
actual time invoice. The theorem does not change the programme's complete
unconditional multiplication envelope.

Prepared independently by S005 Route B for @CubeJerry, with substantial
ChatGPT assistance. The S005 lead owns RG; Route A owns the separate
positive row-space compiler. Prior source and programme credits remain.
