# Independent review of the full formula extraction

Reviewer: Route C, S002, 2026-11-25. Reviewed the complete current
`../A/formula-extraction-theorem.md` (F1--F13), B's integral construction
and generator sections FL6--FL11, and the already accepted source-parameter,
physical-compiler and common-cap contracts. The independent algebra and
generator review is `FORMULA-CYCLOTOMIC-GENERATOR.md`.

**Gate: PASS for the stated asymptotic upper envelope**, with exactly the
source and compiler hypotheses already recorded in the programme. This
is a composition proof and quantitative finite-constructor audit. It is
not a completed tape-machine implementation, a formal proof, an endpoint
result or a claim that the tensor operation is new.

## Finite constructor and padding

The balanced coefficient formula has syntactic degree at most the original
binary predictor degree D and copied-tree size
`[8(D+1)]^(ceil(log2 m)+3)`. The all-rotation matrix-factorization invariant
is sufficient for both concatenated products and graded sums. The result
is a product of D affine pencils on arbitrary occupied rows, including
the zero and constant branches, rather than a distinguished input/output
subblock requiring unused workspace. The architecture is independent of
the shift, so the direct sum of all `2^m` shifts is legitimate.

The common conductor in A's note differs harmlessly from Route C's smaller
lcm choice. With `M0=lcm(1,...,D)` and `tau=2^a>=R` least possible, the
conductor `M=M0*tau` is divisible by every sum length and supplies the
tau-th roots for the R check nodes. The latter are chosen before scalar
basis expansion. Their differences have explicit inverses with powers of
two as denominators. No primitive-root or separability assumption is made
after reduction at an odd prime dividing M0. Since
`log2 M0 <= D log2(D+1)=o(m)` and `R>=2^m`, eventually `M<=2R^2`.

The explicit cyclotomic construction, coefficient reductions, node
inverses and completed Hermite matrices have polynomial-in-R time,
workspace and bit height. In particular the factor induction performs
copies, identity tensors and root twists; it does not repeatedly square
coefficient polynomials. The independent ramified-ring verifier checks
the specialization at d=3 and d=6 over `F3[epsilon]/(epsilon^2)`, including
nonunit partial root sums. It does not rely on division by the factor
length.

Basis expansion multiplies occupied independent width and pencil calls
by the same algebra rank. An arbitrary resulting width W is permitted by
the source binary and tape-Walsh callers. Their leading padding is paid
once at the relevant invocation, and the accepted pre-padding test
`sigma/W <= A^rho/4` retains a factor-two margin. No impossible replication
to an exactly dyadic width is used. The optional fast-block/direct-remainder
wrapper in B is therefore unnecessary for this composition.

Keeping the source degree D no greater than its old padded stage count b
preserves the complete previously accepted call invoices, including all
predictor applications, checks, conversions, reserve occupancy and child
volumes. Consequently the accepted bound
`log2 m_j = O(J^3 log2 J)` remains applicable.

## Profile and actual eligibility

The combined finite envelope satisfies

    P_m <= 2^(2^(C (log2(m+2))^2)).

The rational address magnitudes `2^(m^c)` fit after increasing the fixed C;
so do the explicit generator, scalar matrices, retained tables and all
finite verification loops. With the already accepted physical contract
`a,c,d,g <= P^K` and `U<=max(U_abs,2^(P^K))`, substitution of the parameter
bound gives

    log2 P_j, log2(a_j+c_j+d_j+g_j+2), log2 L(U_j)
       <= E_J := 2^(C J^6 (log2 J)^2).

The threshold has the correct number of logarithms: from `U<=2^(P^K)` one
gets `log2 L(U)=O(1+log2 P)`, not `P^K`. The fixed absolute prime-shape
cutoff is retained and absorbed only as a constant; no numerical value is
assumed known to the machine.

For the common cap, `r_j>=4c_j` and `n>=4(c_j+d_j)` give directly

    c_j ceil(n/r_j)+d_j <= n/4+c_j+d_j <= n/2.

The additional condition `n>=r_j U_j` makes the chunk size eligible. The
`r_j^2` chunk products and physical assembly are paid by the stated
`O((a_j+1)c_j n L(n)^theta_j)` invoice. Generation occurs inside the timed
attempt, and the fixed restart factor is polynomial in `log P_j` and the
sparse index. Thus the prefactor D_j and threshold N_j obey

    log2 D_j, log2 L(N_j) <= E_J.

Now write `s=log2 L(n)` and `z=log2 s`, choose

    Y=(z/(2C(log2 z)^2))^(1/6),
    J=2^floor(log2 Y).

For sufficiently large s, `Y/2<J<=Y`, `log2 J<=log2 z`, and hence
`C J^6(log2 J)^2<=z/2`. Therefore `E_J<=sqrt(s)<s`, proving the actual
eligibility `n>=N_j`. The same candidate satisfies

    log2 H(n) <= O(1)+sqrt(s)+2s/Y
       = O(s (log2 log2 s)^(1/3)/(log2 s)^(1/6)).

The selection is solely an existence choice in the analysis. The fixed
machine retains the existing total schedule and correct fallback; it need
not know the absolute constants or compute Y. All finite small ranges are
covered by the existing fixed fallback.

## Scope and wording

The proof improves the programme's previous explicit upper envelope. It
does not compare numerically with an unspecified published o(1), prove
that actual running time is bounded below by this envelope, or reach
`log H=O(s^beta)` for a fixed beta<1. When describing the last separation,
the precise wording is that **the displayed upper-bound scale** grows
faster than every `s^beta`, rather than that the actual log H must do so.
This is a wording refinement, not a defect in F1--F13.

The d-fold graded tensor operation is attributed to the established
matrix-factorization literature in B. The application to the integral
predictor, the common algebra and its charged construction, and the
quantitative compiler/schedule composition are the scope assessed here.

No further test is needed for this algebraic composition gate: the
independent C ramified-ring and coefficient checks, B's formal polynomial
checks, and the earlier source-parameter/common-cap replays already
address the concrete finite risks. The asymptotic inversion above was
checked directly rather than inferred from numerical samples.
