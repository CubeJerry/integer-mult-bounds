# Equivariant plurality sectors and active inverse-query volume

Status: joint lead/C derivation; independent review and exact controls in
progress. A scoped algebraic network bound, not a physical runtime lower
bound. The full-alphabet error constant extends to active query volume
and noncommuting rational fractions, without a small final polynomial
representation. This note includes C's equivariant tie correction.

## 1. Model and theorem

Fix r>=2 and a field K containing all r-th roots, with char(K) not dividing
r. Put A=K[x_1,...,x_m]/(x_i^r-1), N=r^m, chi=product_i x_i, m>=1.
Use the reduced monomial basis. A finite linear network starts and ends
with W independent A-valued rows. Constant K-linear row maps, copies,
additions and width changes act identically on the A coordinate. No free
operation mixes that basis.

An active query on h rows is a square matrix G over A of support degree
at most one: constants plus sums of univariate functions of individual
x_i. Direct G and inverse G^-1 queries are permitted, with invertibility
over A required for an inverse. Inactive rows are unchanged. Let Q_d,Q_i
be the sums of active h over the two kinds. A port is an arbitrary linear
map of regular rank at most hN; let H be the sum of its h over actual
occurrences. Computed port values may be copied and reused by constant
maps. The model charges an actually repeated operation, not reuse alone.

For the resulting regular input-output map P, let
E=rank_K(chi I-P)/(NW). When P is A-linear this equals average normalized
spectral rank error. For more general K-linear ports it is regular rank
error only. For alpha in {0,...,r-1}^m write n_j for its symbol counts,

    B_d={alpha: largest count minus second-largest count <=2d},
    tau_d=|B_d|/N.

**Theorem PA.** Every such network satisfies

    E+H/W+tau_1(Q_d+2Q_i)/W >= 1-1/r.                     (PA1)

For fixed r, tau_d=O_r((d+1)/sqrt(m)), capped by one. Consequently

    Q_d+Q_i=o(W sqrt(m)) => E+H/W>=1-1/r-o(1).             (PA2)

With H=0 the limiting constant is sharp: P=lambda I, lambda in mu_r,
has E=1-1/r and no queries. Arbitrary intermediate widths and depth are
allowed, with their active-width sums charged.

## 2. Equivariant sectors, including ties

Let M(alpha) be the nonempty set of symbols attaining the largest count.
Define phi(alpha) to be the member j of M(alpha) minimizing the integer
residue (j-alpha_1) mod r in {0,...,r-1}. This unique rule satisfies

    phi(alpha+1)=phi(alpha)+1 mod r.                        (PA3)

Indeed both M and alpha_1 translate by one, leaving all compared residues
unchanged. It follows that the sectors V_j={alpha:phi(alpha)=j} partition
ALL N basis vectors, have equal size N/r, and are cyclically permuted
bijectively by multiplication by chi. No tie set is discarded.

Call a map sector-preserving if it maps each V_j to itself, with arbitrary
row mixing inside the sector. Every such square map D on W rows obeys

    rank(chi I-D)>=(1-1/r)NW.                              (PA4)

The kernel equation at sector j is chi v_(j-1)=D_j v_j. Invert chi and
successively determine every component backwards from one chosen one.
The kernel dimension is at most NW/r. D need not be invertible.
These enlarged comparison maps are used only in a rank proof.

## 3. Polynomial boundaries

Multiplication by a support-degree-d monomial changes at most d exponent
positions. Each symbol count changes by at most d, so a difference of
two counts changes by at most 2d. If alpha is outside B_d, the largest
count exceeds every other count by more than 2d. Its symbol remains uniquely
largest after any such change; phi is unchanged because that maximizer
is unique. A support-degree-d matrix G on h rows thus maps every column
outside h copies of B_d entirely into its original sector.

For its sector-diagonal part G_0,

    rank(G-G_0)<=hN tau_d.                                 (PA5)

This permits arbitrary noncommuting coefficient matrices, arbitrary powers
of each variable and arbitrary sums of eligible monomials. It uses support
degree rather than ordinary degree. It is a regular-rank bound.

## 4. Invertible block completion

Suppose G is invertible and e=rank(G-G_0). Rank subadditivity implies
nullity G_0<=e. In each square sector block, add a matrix of rank equal
to its nullity to make it invertible: use invertible row/column operations
to reach rank normal form, fill its zero diagonal block with an identity,
and transform back. This works over every field, without generic choices.
The combined correction produces invertible sector-preserving H_0 with

    rank(H_0-G_0)=nullity G_0<=e,
    rank(G-H_0)<=2e,
    rank(G^-1-H_0^-1)=rank(G-H_0)<=2hN tau_d.                (PA6)

The inverse identity gives the last equality. H_0 need not be A-linear
or physically efficient: it is a comparison map, not a new free operation.
If G is singular with regular nullity eta NW, the same construction gives
rank(G-H_0)<=eta NW+2e. This variant is used below.

## 5. Telescope the actual network

Replace direct queries by G_0, inverse queries by H_0^-1, and ports by
zero. The resulting P_0 preserves sectors. Change one gate at a time;
the change in the final map is the local difference sandwiched between
fixed prefix and suffix maps. Rank cannot increase under these maps,
even with rectangular widths, fan-out or reused values. Thus

    rank(P-P_0)<=N tau_1(Q_d+2Q_i)+NH.

Combine PA4 with rank(chi I-P)>=rank(chi I-P_0)-rank(P-P_0) to obtain PA1.
No final polynomial representation or separate-child converter invoice
is assumed. Shared port values are treated as part of the actual network.

## 6. Noncommuting rational fractions

Let A_0,B_0 now denote arbitrary W-by-W polynomial matrices of support
degrees a,b; this section's subscripts are names, not sector projections.
If B_0 is invertible, P=A_0 B_0^-1 or B_0^-1 A_0 satisfies

    E(P)>=1-1/r-tau_a-2tau_b.                              (PA7)

To prove this, project A_0 to sector blocks, losing rank at most NW tau_a.
Project and complete B_0 to an invertible sector map, losing rank at most
2NW tau_b. The product inverse identity and rank subadditivity bound the
difference between P and the corresponding sector-preserving fraction by
the sum of those two losses. No commutation between A_0 and B_0 is used.

More generally, if A_0=P B_0 or A_0=B_0 P and B_0 has normalized regular
nullity eta_B, then

    E(P)+eta_B>=1-1/r-tau_a-2tau_b.                        (PA8)

Use the singular completion bound in PA6. For A_0=P B_0, for example,
P minus the completed sector fraction is the sum of the numerator error
and P times the denominator-completion error, followed by the completed
inverse. The rank sum is at most NW(tau_a+2tau_b+eta_B). The other order
is identical with multiplication on the other side. In particular,
a+b=o(sqrt(m)) has the same sharp limiting constant for these fractions.
This is complementary to the binary rare-error tail, not a replacement
of it at every finite parameter.

## 7. Elementary atom bounds

For fixed a!=b, n_a-n_b is a sum of +1,-1,0 steps with probabilities
1/r,1/r,1-2/r. Conditional on J=n_a+n_b~Bin(m,2/r), every atom is at most
1/sqrt(J+1), by the central-binomial bound. On J>=m/r this is at most
sqrt(r/m), while Chebyshev gives Pr[J<m/r]<=2r/m. For m>=r, each
unconditional atom is at most 3sqrt(r/m); for m<r use one. This is the
same elementary estimate proved in C's survivor note. With
beta=min(1,3sqrt(r/m)), the boundary implies that some pair of counts
differs by at most 2d. A union bound therefore gives

    tau_d<=min(1,(4d+1) binom(r,2) beta).                  (PA9)

For d=0 the actual off-block error is zero, since constant matrices
preserve every sector; using tau_0 in PA7 is a valid weaker bound.
PA9 proves PA2 and the fraction limit. Constants are deliberately coarse,
not optimized physical thresholds. The sharp upper example follows from
uniformity of chi on mu_r.

## 8. Scope and credit

For the full order-three alphabet, sub-square-root active query volume
cannot reduce error plus port width below 2/3-o(1), even using inverses
and width changes. The result permits actual shared ports. Two-point
commutator bounds remain useful elsewhere. E003's order-five two-by-two
gate exposes {1,zeta,zeta^-1}, not all five roots; the r=5 statement cannot
be imported for it. Nonlinear/input-dependent suppliers and other repair
interfaces remain separate questions, without an efficiency assertion.

The uniform average here is an abstract spectral average. A physical
representation with unequal spectral multiplicities does not have that
normalized rank automatically. An exact common-spectrum physical
network still inherits the port-budget statement when its query and port
identities hold at every root tuple: each port has rank at most h there.
Any claim about a physical average error needs its own multiplicity ledger.

Lead and C independently identified the cyclic-sector method from C's
survivor analysis; C supplied the equivariant tie rule and fraction
extension, lead supplied the written active-network composition and
completion audit, and C supplies independent exact controls. Prior inputs:
B's rank telescoping, the inverse-query model, C's atom bound and the
pinned OpenAI full-spectrum interfaces. Credits: @CubeJerry, predecessor
sources and substantial ChatGPT research assistance. No novelty
certification, full tape execution, or formal-kernel proof is claimed.
