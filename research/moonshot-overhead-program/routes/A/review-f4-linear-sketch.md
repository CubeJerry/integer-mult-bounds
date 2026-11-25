# Independent review of the F4 additive-sketch obstruction

Reviewer: Route A. Date: 2026-11-25, S002.

**Verdict: PASS for F4-1 through F4-5 and the stated full-rate affine-pencil
consequence.** This is a scoped mathematical obstruction, not a lower bound
for arbitrary representations or integer multiplication.

I independently read `../../results/f4-linear-sketch/PROOF.md` and its exact
checker, checked the constants and additive-character normalization, and
replayed an isolated copy in `f4-sketch-review-replay/`. The proof snapshot
had SHA-256

    bfe88c150af8263a3281d1af023c75ad4a91db76fec249cf705ba3eacbe84e68

and the replayed checker had SHA-256

    26071571e9f26059975c175b066ebc0241c849a1606840c0ed2b0b99160d19b3

## Character energy and agreement

For X uniform on F4*, the nontrivial multiplicative character has mean
zero. The trace character has value +1 at 1 and -1 at omega and omega^2.
Thus its nonzero-frequency Gauss sum is exactly 2/3 in absolute value.
A nonzero coefficient changes only its multiplicative-character phase.

An arbitrary F2-linear sketch A has image size 2^k. Characters of that image
pull back injectively to additive characters of F4^m; nondegeneracy of the
trace pairing expresses each as a coordinate product with coefficients
c_j in F4. A zero coefficient kills the signed Fourier coefficient, while
an all-nonzero tuple has squared magnitude (4/9)^m. Parseval on the image
and Cauchy--Schwarz therefore give the exact energy and stated bound

    Delta^2 <= N(A)(4/9)^m <= (2^k-1)(4/9)^m.

The factor 2^k is needed; the trivial character contributes zero. The
three-root equality indicator gives success at most 1/3+(2/3)Delta.
Combining the inequalities with error delta<2/3 gives precisely
k ln 2>=2m ln(3/2)+2 ln(1-3delta/2). The constant is correct.

Allowing every F2-linear sketch is essential here: entries involving both
X_j and X_j^2 are additive but need not be F4-linear. The proof covers
these maps, including Frobenius. Merely proving an F4-linear version would
not justify the stated pencil consequence.

## Exact recovery and matrix entries

Every nonzero additive-kernel vector v yields two nonzero-coordinate inputs
u,u+v in the same fiber with different coordinate products. On a nonzero
coordinate of v, the ratio (u_i+v_i)/u_i can be either omega or omega^2.
Those choices are independent over coordinates; changing one changes the
product ratio, so not all choices can have ratio one. This proves exact
recovery requires kernel zero, hence k=2m; injectivity is sufficient.

Expanding e-dimensional F4-algebra coefficients in a fixed basis gives at
most e D R^2 F4-valued additive summaries for D square R-row pencils.
Constants and fixed row maps do not add variable summaries. Any output
entry is a function of that sketch. Full-rate correctness of a row for
arbitrary independent inputs requires its diagonal coefficient to equal
the target, with off-diagonal constraints only strengthening that demand.
This proves F4-5 and the consequence R=Omega(m^(1/4)/sqrt(e)) when
D=O(sqrt(m)). It permits polynomial width and does not refute the compact
predictor hypotheses or the new large formula factorization.

Coordinate multiplication, coordinate inversion and target phases preserve
the uniform product distribution and character estimate. Inversion on
F4* is squaring and extends to an additive map on F4. Taking a fixed
nonnegative average of individually bounded row-success probabilities
requires no independence between their error sets.

## Exact replay

The isolated checker passed 5,238 exact Parseval/success cases, including
5,127 explicit kernel collisions and 111 injective sketches. It checked
all four one-coordinate additive characters, 16 Frobenius-additivity
controls and the two stated negative controls. The largest domain has
3^6 inputs. All calculations use integers and exact arithmetic in the
third-root relation; no floating-point comparison is used.

The checker tests general binary row maps and accounts for multiplicity
when characters of a redundant codomain restrict to the same image
character. Thus it tests the rank-sensitive normalization in the proof,
not only full-rank codomains. It also verifies that a single additive bit
does not recover one F4 coordinate exactly.

Finite enumeration supports these identities and catches normalization
errors; the all-size result follows from the character and kernel proofs.
No exhaustive priority search, proof-assistant certificate or complete
multiplier execution is claimed.
