# The missing cyclic ordinary conjugacy reduces to one rank-one scalar matrix

**Proved exact construction criterion in the declared cyclic interface.**
This solves the ordinary-Q conjugacy portion of the middle-native test for a
specific implementable family. It does not assert a `(4,2,1)` endpoint or
ordinary membership of the remaining first interstage C.

## 1. Exact source channel, including every phase block

Keep the literal four-bit source `A=C_b D_acd P`, `a=A^(tensor V)`, and let h
be one of the following actual diagonal quarter-phase monomials:

    D_b, D_c, L4 D_b L4, R4 D_c R4.

Their one-column phase exponents, valued in {0,1}, are respectively

    b, c, b xor cd, c xor ab.                           (1)

Write `h_V=h^(tensor V)` and
`Pi_s=(1/4)sum_(j=0)^3 i^(-sj) h_V^j`.
For every V>=3 and all s,t in {0,1,2,3},

    Pi_s a Pi_t !=0.                                    (2)

Here is a direct proof, not a large-width approximation. The nonzero
one-column source entries have input `(a,b,c,d)` and output
`(b,c xor epsilon,d,a)`, epsilon in {0,1}. For each function in (1), the pair
of output/input phase bits takes all four values in `{0,1}^2` on this
support. For b and c this is immediate from the two independent input bits
and epsilon. For `b xor cd`, epsilon freely changes the output bit. For
`c xor ab`, take input b=0, leaving input phase c and output phase d
independent. Choose V supported column pairs with output/input bit counts
congruent to s/t. Once V>=3, counts0,1,2,3 can all be chosen independently.
The corresponding tensor entry of (2) is a product of nonzero source entries,
so it is nonzero. Spectral blocks with different ordered(s,t) have disjoint
input/output supports, making their scalar coefficients independently
identifiable.

## 2. The declared inverse/conjugacy problem

Suppose the middle-native calculation supplies operators of the form

    P = sum_s P_s tensor Pi_s,
    T = sum_(s,t) M_st tensor (Pi_s a Pi_t),              (3)

where the sixteen three-by-three Gaussian-rational matrices `M_st` and four
matrices `P_s` are fixed before V varies. This is an explicit interface
restriction: arbitrary full ordinary P or arbitrary rank-one-Gaussian
components T need not have the form (3).

We seek one cyclic ordinary unit

    Q(h_V)=sum_s q_s tensor Pi_s,

with its explicit inverse, satisfying

    P=Q^-1 E_22 Q,
    T=Q^-1 (-a E_01) Q                                 (4)

at every positive V. The preceding quarter-phase unit theorem reduces its
unit condition to `q_s in GL_3(Q(i))` for all four s.

Form the twelve-by-twelve scalar block matrix

    M = (M_st)_(s,t=0)^3.                               (5)

**Theorem.** A cyclic ordinary unit satisfying (4) exists if and only if all
the following finite exact conditions hold:

1. Every `P_s` is a rank-one idempotent.
2. `rank M=1`, and every three-by-three block `M_st` is nonzero.
3. Factor `M=-u v`, where u is a twelve-entry column and v a twelve-entry
   row. Partition them into three-entry columns `u_s` and rows `v_s`.
   For every s,

       P_s u_s=0,       v_s P_s=0,       v_s u_s=0.      (6)

Conditions (6) do not depend on the nonzero global scalar ambiguity in the
factorization. The nonzero-block condition ensures every u_s and v_s is
nonzero.

This criterion checks coherence between different phase blocks. Sixteen
unrelated rank-one block factorizations are not enough.

## 3. Necessity and an explicit construction

If (4) holds, set

    u_s=q_s^-1 e_0,       v_s=e_1^T q_s.

By (2), comparing spectral blocks in (4) gives

    P_s=q_s^-1 E_22 q_s,
    M_st=-u_s v_t.

This proves every stated necessary condition, including rank one of the
entire matrix M, rather than just its individual blocks.

Conversely, factor M as in the theorem. For each s choose any nonzero column
`w_s` of `P_s`. Choose a standard coordinate vector e_j with `v_s e_j !=0`
and put

    z_s=(I-P_s)e_j/(v_s e_j),
    R_s=[u_s, z_s, w_s],       q_s=R_s^-1.              (7)

The first two columns of R_s are in the two-dimensional kernel of P_s.
They are independent because v_s kills u_s and takes value1 on z_s.
The third column spans the image of P_s, so R_s is invertible. Moreover

    P_s R_s=R_s E_22,
    v_s R_s=(0,1,0),
    R_s e_0=u_s.

These identities give `P_s=q_s^-1 E_22 q_s` and
`M_st=-q_s^-1 E_01 q_t`, proving (4). Fourier interpolation of q_s and R_s
provides the literal polynomial coefficients of Q and Q^-1. All formulas
are fixed finite exact arithmetic over Q(i), and the previous explicit
cocharted scalar schedules implement both operators with their nonzero
ordinary costs and width-independent amplification bounds. Root's direct
phase-table implementation eliminates the six optional conjugating adapters;
every actual clock wrapper remains separately paid.

The identities are spectral identities at every V, including smaller widths
where some sectors vanish. The all-sector comparison at V>=3 establishes
necessity; it does not exclude the small widths from the constructed source.

## 4. How to obtain the scalar matrices from actual words

If P and T are given by finite cyclic expansions

    P=sum_j P[j] tensor h_V^j,
    T=sum_(j,k) N[j,k] tensor (h_V^j a h_V^k),

then their data in (3) are the exact finite Fourier sums

    P_s=sum_j i^(sj) P[j],
    M_st=sum_(j,k) i^(sj+tk) N[j,k].                   (8)

Equation (2) makes this second coefficient representation faithful for the
declared sixteen channels at every V>=3. No full-monomial-group enumeration
or large unproved ordinary inverse is required for this part of the problem.

For a desired endpoint E, the complete remaining test is:

* form `B=L^-1 E L^-1` and its actual Gaussian components;
* require invertible `F=B_0+B_1` and determine whether
  `P=F^-1B_0,T=F^-1B_2` lie in the explicit class (3);
* apply the finite criterion and construct Q from (7);
* check `C=F Q^-1 diag(a^-1,a^-1,I)` is ordinary and provide its actual
  finite source/inverse recipe and full charge.

The last line remains a genuine obligation. Neither scalar rank conditions
nor the new Q construction silently grant an arbitrary ordinary C service.

## 5. A coherent-block negative control

Take every `P_s=E_22` and let

    M_st=-c_st E_01,
    c_st=1 except c_33=3/2.                            (9)

Every individual block is nonzero rank one, and all local kernel/image
conditions suggested by E_22 and E_01 hold. Yet the coefficient matrix c
has rank two, so M has rank two. The theorem rejects a cyclic Q.

This failure is not just caused by a singular underlying operator. The
associated operator is

    T=-E_01 tensor (a+(1/2)Pi_3 a Pi_3).

Its nonzero block is invertible: factor out a, and the remaining perturbation
of the identity has norm at most1/2. Consequently T has rank D, is square
zero, and obeys `PT=TP=0` at every V. Thus all these operator-level conditions
can hold while the required simultaneous cyclic conjugacy still fails.
The example excludes only a cyclic Q; it is not asserted to exclude an
arbitrary Q from the full ordinary algebra.

There is a separate reason to require each scalar projector P_s to have
rank one. Its physical rank alone is weaker, even at every positive width.
For the present Boolean half/half controls, the total dimensions of the
even and odd quarter sectors are equal: `trace(h_V^2)=0`. Choosing sector
projector ranks `(2,0,2,0)` therefore gives physical rank D for every V>0,
but it cannot be cyclically conjugate to E_22, whose rank is one on every
sector. The checker retains this all-width rank-census false positive.

## 6. Status, validation and complete cost boundary

The checker starts from four explicit different sector units, derives their
P_s and M_st, recovers sector units using (7) without importing the original
units as a solution, verifies all16 conjugacy equations, and Fourier-checks
the resulting inverse. It verifies the sixteen source channel blocks through
actual one-column support witnesses and tensor construction. It rejects the
incoherent-block example, a broken local flag, and a singular sector.

This is a completed algebraic and ordinary-implementation bridge for the
declared cyclic interface. Constructing an actual `(4,2,1)` E with the required
middle form and ordinary C remains open. All native/body/ordinary costs,
precision, source access, owned erasure, compiler and recursive contracts
remain. All five global foundations remain. **No new complete kappa.**

Credit @CubeJerry, the four-bit source, finite tensor separation, ordinary
compiler and native-interface predecessors; Worker B with substantial OpenAI
assistance. Independent review is separate from the author checker.
