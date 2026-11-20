# Geometric core overlaps and a necessary condition for preserving a second centre

**Author theorem and exact native example. Independent admission is pending. No common global H word or new kappa.**

The previous geometric cycle glued independent cores and lost protection at alternate native triangles. This result studies the stricter constructive repair: keep each donor a geometric Reed–Solomon source except at at most two centre quotients, and keep the original inverse fibres at both centres. The existing two-edit theorem would then protect every propagation span. The missing compatibility is real: the quadratic-annihilator H mechanism cannot preserve the old fibres of a second centre when its own evaluation node is nonzero. This claim concerns that explicit mechanism and preserved fibres, not arbitrary changed sources or H words.

## 1. The shared two-dimensional core intersection

Let F contain GF(64), represented by x^6+x+1. Put q(v)=v^9+v^18+v^36, let Q={a:q(a)=0}, and write

    L_v(z)=v z^8+v^2 z^16+v^4(z^14+z^5)+v^8 z+v^16 z^2+v^32 z^4,
    U_a(v)=(L_v(z)+L_v(a))/(z+a).

For fixed a the scalar source core S_a is the F-span of U_a(v), v in GF(64). The six powers v,v^2,v^4,v^8,v^16,v^32 have invertible Moore coordinate matrix, so S_a is spanned by six coefficient polynomials of respective leading degrees 7,15,13,0,1,3. In particular 1 and z+a belong to S_a.

For any distinct a,b in Q,

    S_a intersection S_b = span_F{1,z}.                         (1)

Compare two expressions for a common polynomial, beginning at degree15. Their leading coefficients agree, while degree14 differs by (a+b) times that coefficient; hence it vanishes. The same comparison at degrees13/12, 7/6 and3/2 removes the other four high-degree coefficient pairs. The remaining polynomial has degree at most1. Conversely every such polynomial belongs to both cores. This proves (1) over every field extension.

Let P_(b,a) be the span of all old b-fibres at receivers seeing both b and a. Their normalized parameters span the binary hyperplane b_q(v,a+b)=0. The geometric field theorem gives dim P_(b,a)=5. Equivalently use the linear extension of U_b to that hyperplane. Every such polynomial vanishes at a. Hence (1) implies

    S_a intersection P_(b,a) = span_F{z+a}.                    (2)

For inclusion in the other direction, in Moore coordinates take the coefficient of v^16 to be1, that of v^8 to be a+b, and all others zero. U_b then equals z+a. The polar equation has value (a+b)^2+(a+b)^2=0. This proves (2) algebraically; the finite replay verifies all756 ordered node pairs and their actual20-parameter families.

At quotient width k these statements tensor with F^k. Therefore any replacement central quotient C_a that preserves every old b-fibre must satisfy

    C_a ((z+a) tensor I_k)=0.                                  (3)

Indeed, each old b-fibre seen with a is an off-b uncertainty space, so the replacement a-observation must annihilate it. This is a condition on actual unchanged uncertainty spaces, not dimension counting alone.

## 2. A nonvanishing theorem for the quadratic-annihilator pencil

Use the actual nine Desarguesian ports from the geometric H construction. Let E be their9-by3 linear evaluation matrix and E2 their9-by6 quadratic evaluation matrix. Let N be any3-by9 full left annihilator of E2. The exact port certificate gives

    rank E=3, rank E2=6,
    ker K=col E,
    K_((p,q),d)=N_(p,d) E_(d,q), rank K=6.                    (4)

These are elementary fixed-field identities; the checker rebuilds them on actual H263 ports. They hold after extending F and after invertible changes of the three linear coordinates.

Choose nonzero weights alpha,beta,alpha+beta at every port. Let W_gamma be any full3-row annihilator of diag(gamma)E2, and assume

    T=[W_(alpha+beta); W_beta; W_alpha]

is invertible. Define A_alpha(r)=diag(alpha)diag(E r)E and A_beta(r) similarly, and

    D0(r)=W_(alpha+beta) A_alpha(r),
    D1(r)=W_beta A_alpha(r),
    D2(r)=W_alpha A_beta(r).

**Pencil nonvanishing.** For every nonzero r in F^3, none of D0(r),D1(r),D2(r) is the zero matrix. This does not assert their determinants are nonzero at arbitrary extension-field parameters.

It is enough to prove the D1 case. Put s=E r. If D1(r)=0, the three columns diag(alpha/beta)diag(s)E belong to col E2. By (4), t=diag(alpha/beta)s lies in col E; write t=E u. Define the nine-vector

    y=diag(beta) [t * (s+t)],

where * denotes coordinatewise multiplication. Since s,t,s+t are evaluations of linear forms, their pairwise products belong to col E2. The identity alpha*s=beta*t gives

    y/beta=t*(s+t),
    y/alpha=s*(s+t),
    y/(alpha+beta)=s*t.

All divisions use the nonzero declared weights. Thus y belongs to each of the three weighted quadratic column spaces and Ty=0. Because r is nonzero and E has rank3, some s_d is nonzero. At such a coordinate, the nonzero alpha,beta,alpha+beta force t_d and s_d+t_d to be nonzero; therefore y_d is nonzero. This contradicts invertibility of T. Relabeling the three weights proves the other two cases.

The proof is uniform over every extension field. Its only finite premise is (4), authenticated by the exact9-port certificate. Proportional alpha and beta provide a negative control: T is singular and the pencils may vanish identically, so invertibility is essential.

## 3. Why nonzero centre nodes prevent this preservation mechanism

In a literal geometric source chart, receiver parameters at centre a satisfy q(v)+b_q(v,a)=1. The Hermitian coordinates used by the local quadratic construction form a binary-linear bijection

    R:GF(64) -> GF(4)^3,
    sum_l R_l(v)^3=q(v)+b_q(v,a).                             (5)

Write its unique linearized polynomial representation

    R(v)=sum_(s=0)^5 r_s v^(2^s),  r_s in GF(64)^3.

The central control of the quadratic mechanism is fixed on the entire geometric core by

    C_a [U_a(v) tensor I_3]=D_j(R(v)).                         (6)

The geometric norm-one parameters span the six-dimensional binary space, so the equality extends to the full scalar coefficient core. In U_a(v), the coefficient of v^16 is exactly z+a. Therefore

    C_a [(z+a) tensor I_3]=D_j(r_4).                           (7)

If (3) holds, the pencil nonvanishing theorem forces r_4=0. Since R takes values in GF(4)^3, R(v)^4=R(v), so the even coefficients r_0,r_2,r_4 vanish together. Consequently R is GF(4)-antilinear:

    R(omega v)=omega^2 R(v), omega^2+omega+1=0.

The right side of (5) must then be unchanged by v->omega v. q already has this invariance, and hence b_q((omega+1)v,a)=0 for every v. Nondegeneracy of the polar form and omega+1 nonzero force **a=0**.

Thus any quadratic-annihilator central control at a nonzero node a cannot preserve all old inverse fibres of even one other centre b. Changing port weights, output frames, or the free tail of the central control cannot remove this obstruction. A donor has only one node0, so this particular way of gluing two quadratic centres while preserving their original geometric fibres cannot succeed.

This conclusion assumes the same geometric source tuple and the stated quadratic-annihilator realization on its original core. It does not exclude a two-edit source whose inverse fibres move, different coupled H providers, additional source maps, or general whole-bank mixing. Nor does it prove a return-rank lower bound.

## 4. Constructive meaning and next questions

The obstruction identifies the exact equation that a successor must change: at least one centre must use moving inverse fibres or a different central-readout mechanism. The positive algebraic extension at node0 remains available when R is GF(4)-antilinear: its forced common line is killed, and a central control prescribed on S_0 extends to annihilate P_(b,0), since their intersection is exactly that line. All other free-tail choices, native early bases and simultaneous second-centre H words still require construction and validation.

Next test the all-width polynomial feedback family with correlated parameters, or allow the second quotient edit to move the first centre's fibres and solve both H graph systems jointly. Reusing independent cores or generic free tails would discard the very global nonsaturation property this investigation was meant to preserve.

Credit @CubeJerry and the S030 geometric-source, two-edit, Desarguesian-port and quadratic-annihilator packages. Substantial OpenAI assistance in S031. Separate independent verification is required before admission. No new complete kappa.
