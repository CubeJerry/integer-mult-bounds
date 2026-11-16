# Two native calls cannot amplify total head rank in the fixed monomial tensor interface

**Proved structural extension of the retained two-native theorem to the nonlinear, infinite-projective-order source. Independent review pending. No new kappa.**

## 1. Precise scope and what is new

Fix a one-column address dimension d. Let H be the entire finite group of d-by-d monomial matrices with phases in {1,i,-1,-i}. It contains the fixed ordinary tables of the caller and their inverses. The source Gaussians use the retained dyadic Gaussian normalization and such monomial gauges; consequently every monomial unitary arising in the finite word catalogue again has phases in {1,i,-1,-i}. Enlarging a caller's proof algebra to H grants no additional physical operation. All source and endpoint tables are fixed before tensor width V grows. Let O_V be the complex span of h^tensor V for h in H. Its matrix algebra on R banks is the ordinary coefficient algebra. Actual callers must still compile their finite ordinary expressions and inverses; this proof grants no free growing linear-algebra operation.

Allow two native calls, each on two retained independent banks, with arbitrary invertible ordinary matrices before, between and after them. They have head forms, up to role exchanges and ordinary scalar signs,

    L(a)=[[a,I],[0,a]],    U_c(a)=[[a,c a²],[0,a]],  c nonzero.       (1)

Each a=A^tensor V is an actual rank-one Gaussian unit and a² has pure Gaussian rank two. The two calls may have different admitted one-column heads. The four nonlinear Boolean sign sources and their exact inverses satisfy this requirement. There are no extra nonordinary queries, discarded inputs, clean auxiliary banks, or changed body incidence.

Assume the complete head word, up to invertible ordinary outer matrices, equals R independent Gaussian jobs G_j of ranks r_j>=0. Every G_j is a fixed one-column Gaussian word tensor-lifted to V with its actual ordinary gauges and phases. The identity must hold for all sufficiently large permitted widths. Then

    sum_j r_j <=4.                                             (2)

The retained predecessor proved (2) inside a finite Clifford algebra and used a separate one-native/two-query gate in its last case. The present extension uses only finite word separation, monomial invariance of Gaussian type, elementary support bounds, and a new ordinary-coset argument for that last case. No finite group containing the nonordinary A is assumed; the generated unitary group may be infinite. The earlier counterexample to a common invariant lattice at2 is therefore compatible with this theorem.

## 2. Finite tensor-word separation and support filtration

All expressions in this proof contain finitely many one-column unitary words; H itself is finite, even if large. Adjoin the finite sets needed for the inverse ordinary matrices and for every product appearing below. Distinct projective unitary words have normalized Hilbert-Schmidt inner product of absolute value less than1. Their tensor Gram matrix tends to the identity. Therefore, for all sufficiently large V, their tensor lifts are linearly independent after projectively identical words are identified with their **actual** width-dependent phase. This is the retained tensor-separation argument applied to a finite catalogue, not to an infinite group at once.

A scalar phase collision is never erased: if W=z U then W^tensor V=z^V U^tensor V. It can be combined only with that coefficient. All arguments below hold in each permitted phase sector and with width-dependent complex ordinary coefficients.

Let E_r denote the span of the catalogue's ordinary-bimodule class of pure Gaussian rank-r words. Multiplying a Gaussian unit on either side by a unit-phase monomial preserves its Gaussian rank and support size. Hence the E_r are disjoint at faithful width, and their projections pi_r commute with ordinary left and right multiplication. Consequently an ordinary-equivalent independent Gaussian endpoint satisfies

    rank(pi_r(M))=n_r D,       n_r=#{j:r_j=r},                   (3)

where D=d^V. Its non-Gaussian word components vanish as well.

For the support argument let F_s be the span of unitary words whose one-column rows and columns have support at most2^s. Products obey F_s F_t subset F_(s+t), and ordinary multiplication preserves these spaces. A pure rank-r Gaussian word has exactly2^r nonzero entries per one-column row and column, so no Gaussian rank above s occurs in F_s. This filtration includes non-Gaussian words. It does not assert that every small-support unitary is Gaussian.

Ordinary inverses remain in the finite-dimensional ordinary matrix algebra whenever they exist at the chosen width: apply the characteristic polynomial to an invertible element. This algebraic closure does not replace the caller's actual physical inverse recipe or price.

## 3. Two-call degree and the necessity of a rank-two job

If both calls have square crosses U, invert the entire asserted identity algebraically. The inverse of U has an ordinary cross and head a^-1; endpoint Gaussian ranks and ordinary invertibility are preserved. This normalization does not supply a free physical inverse operation. Otherwise leave the identity unchanged. At most one U remains.

Two L calls lie in F_2. A mixed L/U pair lies in F_3, and its rank-three component can appear only in the one output block row affected by U's square cross if U is last, or the corresponding one input block column if U is first. Thus

    r_j<=3,       n_3<=1.                                      (4)

For an independent Gaussian endpoint in this mixed case,

    n_3>0 implies n_2>0.                                       (5)

To prove this put U last and write W=C L, so W lies in F_1. On its two active output rows,

    M_1=a W_1+c a² W_2=a W_1+c a M_2,
    M_2=a W_2.

If n_2=0, the endpoint contains only Gaussian ranks0,1,3, by(4), and has no non-Gaussian component. The row M_2 is in F_2 and hence has no rank3 component, so M_2 lies in E_0+E_1, which is a subspace of F_1. It follows that M_1 lies in F_2 as well. Idle rows already lie in F_1. There is no rank3 component. Transpose the complete identity to handle U first. This explicitly uses endpoint purity; it does not equate F_2 with E_0+E_1+E_2 for arbitrary words.

## 4. Idle-bank rank accounting, with ordinary endpoints retained

This is the retained two-half block argument, now using the projections from Section2. Independently relabel each call's active pair as the first two banks, absorbing these relabelings into the middle ordinary matrix C. Let p=R-2 and block C into active/idle parts C_aa,C_ai,C_ia,C_ii.

The idle-idle block of M is C_ii, which is ordinary. The active-idle and idle-active blocks of pi_1(M) are exactly

    X=diag(a_2,a_2) C_ai,     Y=C_ia diag(a_1,a_1).              (6)

The native cross has pure rank0 or2, and therefore does not contribute to these rank1 blocks. The idle-idle block of pi_1(M) is zero. Its image contains the upper-block image of X, while its projection to idle outputs is the image of Y; hence

    rank(pi_1(M))>=rank(C_ai)+rank(C_ia).

Invertibility of C gives each of the latter ranks at least pD-rank(C_ii). Also rank(C_ii)<=rank(pi_0(M))=n_0 D. Consequently

    n_1>=2p-2n_0,
    n_1+2n_2+2n_3<=4.                                        (7)

Using(4), total head rank is at most5. If it is5, (5) and(7) force exactly

    n_3=1, n_2=1, n_1=0, n_0=p.                              (8)

## 5. Exact ordinary stable cancellation in the remaining case

Under(8), pi_1(M)=0. Equations(6) force C_ai=C_ia=0. Both C_aa and C_ii are invertible, and the word splits into an invertible two-bank head B and the ordinary idle block C_ii. Since rank(pi_0(M))=pD, the active block has pi_0(B)=0.

Write M=U diag(G_3,G_2,G_0) V with invertible ordinary U,V and with G_0 the p ordinary jobs. Its ordinary component is diag(0,C_ii). Its kernel is exactly the active input space and its image is exactly the idle output space. It follows that the high endpoint input rows of V restrict to an ordinary isomorphism on the active inputs, and the high endpoint output columns of U project to an ordinary isomorphism on active outputs. Taking the active-active block gives an ordinary two-bank equivalence

    B=U_high diag(G_3,G_2) V_high,                             (9)

with square invertible ordinary factors. This is the retained stable-cancellation argument. It concerns an asserted all-input identity and does not erase physical owners or supply free projections.

## 6. New non-Clifford ordinary-coset obstruction

In fact no mixed pair on two banks can have an independent Gaussian endpoint with both ranks at least2. Put the ordinary-cross native in lower form and the square-cross native in upper form, absorbing role exchanges into ordinary matrices. For arbitrary rank-one nonmonomial Gaussian heads a,b and an ordinary middle matrix

    N0(a)=[[a,0],[I,a]],     N2(b)=[[b,-b²],[0,b]],
    P=[[u,v],[w,z]],

the two lower entries of M=N0(a) P N2(b) are

    M_21=u b+a w b,
    M_22=-u b²-a w b²+v b+a z b.                              (10)

Let O b denote the ordinary right coset span. Its unitary generators have pure Gaussian rank1. The word sets a H b and H b are projectively disjoint: an equality a h b=phase*k b would make a=phase*k h^-1 monomial, contradicting its rank1 support. Thus projection onto O b annihilates every a w b and a z b with w,z ordinary.

If the endpoint in(10) is ordinary-equivalent to independent ranks at least2, every entry of M has zero ordinary component and zero O b component. Projecting M_21 onto O b forces u b=0, hence u=0. The ordinary projection of that same entry then gives

    pi_O(a w b)=0.                                           (11)

Right multiplication by b bijects projective word classes and maps O onto O b. Therefore, coefficientwise with every phase retained,

    pi_(O b)(a w b²)=pi_O(a w b) b=0.                         (12)

Projecting M_22 onto O b now forces v b=0, hence v=0. The first block row of P vanishes, contradicting its invertibility.

Transposition and simultaneous bank-role reversal reduce N2(a) P N0(b) to the same case. Nonzero scalar cross signs only multiply u,v by units and do not change the proof. The heads may differ, including forward/inverse or differently normalized nonlinear sources. No assumption on a finite group generated by a,b is used.

Equations(9)--(12) rule out the only total-rank5 case. This proves(2).

## 7. Exact whole-body cost consequence

If each native introduces a fresh rank-seven body and every retained bank receives both bodies, all2(R-2) inactive rank-seven services are paid. For [x]=x^t with0<t<1 and delta=[8]-[7],

    Price=2[1]+(2R-2)[7]+2[8]=2R[7]+2(1+delta),
    Target=sum_j[14+r_j] <=2R[7]+delta sum_j r_j.

The last inequality is concavity, with [14]<=2[7] and each subsequent integer increment bounded by delta. By(2),

    Price-Target>=2(1-delta)>0.                               (13)

Every ordinary wrapper, body translation, precision, layout, ownership, or recursive expense only enlarges this deficit. In particular the tempting two-role(3,2) Gaussian margin at t=199/200 is positive arithmetically but has no exact caller in this interface.

## 8. Verification, limitations, and next construction

The finite checker verifies the exact mixed-orientation block expansion, actual ordinary coset disjointness and transport, both native signs, all four nonlinear heads including distinct-head pairings, and sharp independent(2,2) controls. It includes an ordinary endpoint counterexample when the endpoint rank hypothesis is relaxed, and a singular middle control when invertibility is dropped. These finite controls supplement Sections2--6; they do not establish universal tensor separation by enumeration.

The theorem does not cover extra nonordinary queries, width-growing ordinary catalogues, approximate or singular endpoint limits, non-tensor spatial encodings outside O_V, changed body incidence, clean/discarded inputs, or three or more native calls. It does not rule out the three-call(3,2,2) target. The clock identity and actual inverse-native closure remain admissible mechanisms for that next count.

Credit @CubeJerry; the retained two-half component and two-native total-head proofs, including their idle-bank rank and stable-cancellation arguments; the retained tensor-separation and native-source contributors; Worker B with substantial OpenAI assistance. All five global foundations remain. No complete new supplier or kappa is claimed.
