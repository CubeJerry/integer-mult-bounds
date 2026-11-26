# A shared destination accumulation graph for first-difference rectangles

Status: **new local execution draft; independent review requested**.
This supplies a destination counterpart to `nested-fourier-source-reuse.md`.
It retains one auxiliary-axis transform per rectangle and shares the other
destination transforms by linear accumulation. The lead and Route C
independently suggested the same line/shear factorization during review;
this note records their contribution as well as the author's derivation.
No new complete asymptotic multiplication envelope is claimed.

Notation: q=2^t, even L>=2, N=q^L, D=2+L(q-2), and
lambda=sum_(k odd) binom(L,k)t^k. Keep H=span(I)^perp, so the destination
transform is along K=span(I). Fourier children below are normalized.
Characteristic-two geometry concerns addresses; data arithmetic remains
the rational numerical branch.

## 1. Independent internal spaces of sibling blocks

Fix a destination w. For each coordinate i and a!=w_i, put
z_i(a)=d_(w with coordinate i changed to a). These belong to A_w=d_w^perp,
and their pairings are

    <z_i(a),z_i(b)>=1_(a=b),
    <z_i(a),z_j(b)>=1 for i!=j.                           (DA1)

At first-difference level s, let C_i(s) be the sibling binary prefix
block of size 2^s opposite w_i. The t blocks partition the alphabet except
w_i. Choose a base letter a_i(s) in each, and let

    U_i(s)=span{z_i(a)+z_i(a_i(s)):
                       a in C_i(s), a!=a_i(s)}.          (DA2)

All these spaces, over every i,s, are independent, and dim U_i(s)=2^s-1.
A relation has coefficients c_i(a) with even sum in every sibling block,
hence even sum for each coordinate i. Pairing it with z_i(b) gives c_i(b)
by DA1: every other coordinate has even coefficient sum. Thus every
coefficient vanishes. The spaces lie in the norm-zero hyperplane of A_w.

The map nu(x)=<x,x> is linear in characteristic two. A_w is nondegenerate
and contains odd-norm vectors z_i(a). Choose one such vector e. Extend
the independent bases of all U_i(s) to a basis of ker(nu|A_w), and adjoin
e. This gives one fixed destination basis B_w, independent of rectangle
and query. The internal blocks occupy disjoint fixed coordinate slots;
e occupies one further fixed auxiliary slot.

For a canonical rectangle incident to w, let S be its odd set of unequal
coordinates and s_i their levels. Then

    K=span(I)=U_R direct-sum <v_R>,
    U_R=direct-sum_(i in S) U_i(s_i),
    v_R=sum_(i in S) z_i(a_i(s_i)).                       (DA3)

The last identity with the base label follows by pairing with every d_u:
the sum has the same Gamma row as that label when |S| is odd. Variations
inside I give exactly U_R. Since nu(v_R)=1, its fixed coordinates have
the form v_R=e+alpha_R, with zero e coordinate in alpha_R. The vector
alpha_R can have components in the selected U_R; no common complement
is assumed to contain all rectangle representatives.

## 2. Factor the large partial transform outside one leaf routine

Work in B_w coordinates. Let W be the coordinate set spanning U_R, and
let M send e to e+alpha_R while fixing every other basis vector. Write
P_M for its pushforward permutation of complete address arrays. Using
the adapted basis W,v_R and the remaining fixed vectors, the output
endpoint, up to original ordinary input-coordinate maps, is

    P_M F_W F_e.                                         (DA4)

Split alpha_R into alpha_W and alpha_out, and M into the two commuting
shears M_W and M_out. The exact controlled-shift identity gives

    P_(M_W) F_W=F_W D_(alpha_W),
    P_M F_W F_e=F_W D_(alpha_W) P_(M_out) F_e.             (DA5)

Here D is the sign whose exponent is the sum, over W slots and f bit
columns, of alpha_i times the e bit times the W bit. M_out changes only
slots outside W, controlled by e, so commutes with F_W. These are explicitly
generated ordinary binary coordinate and scalar maps. DA5 accounts for
the phase caused by moving the shear; it is not a free commutation.

Each rectangle therefore performs one e-axis transform followed by the
ordinary maps P_(M_out) and D. Its remaining expensive output operator is
F_W in fixed slots. B_w need not be orthonormal: its paired dual is used
in the intermediate frequency coordinates. Changes from the common
rectangle representative to these coordinates are the ordinary coset and
frequency maps permitted by the source kernel proof.

Apply this argument independently to both output halves. Returning from
B_w to the label's physical bases is one fixed coordinate permutation per
half. The original final auxiliary phase P_w^* stays after that return
and after the entire accumulated output. Distinguished phases remain in
their individual middle maps. Since e is auxiliary and fixed at w, its
transform is still taken after the sum over queries and row mixing, once
per rectangle incidence.

## 3. Bottom-up accumulation of independent contributions

Associate state zero to an equal coordinate or unequal level zero, and
positive state s_i to the chosen sibling block U_i(s_i). The distinct
states are Q={0,...,t-1}^L with at least one zero, of cardinality
Qsize=t^L-(t-1)^L. Rectangles with the same state share W, although their
post-DA5 leaf vectors differ. Add those leaf vectors into z_s.

For each nonzero state, set a smallest positive coordinate to zero and
take that state as its parent. This removes the entire corresponding
internal block, and gives a rooted tree on Q. The edge from p to s costs

    dim U_i(s_i)=2^s_i-1.                                (DA6)

Process from leaves to root, retaining the node's own input and adding
the transformed accumulators of its children:

    y_s=z_s+sum_(children c) F_(W(c)\W(s)) y_c.            (DA7)

Fixed disjoint slots imply F_(W(c))=F_(W(s))F_(W(c)\W(s)). Induction
therefore proves that the root equals sum_s F_(W(s)) z_s. This works for
unrelated incoming rectangle data; it does not assume a common source
array at the destination. Copies in a forward graph become additions in
this accumulation graph.

With S(L,t) the source-tree sum NR6, the destination edge bill is

    T(L,t)=sum_(ell=1)^(t-1)(2^ell-1)
       [(t-ell+1)^L-2(t-ell)^L+(t-ell-1)^L]
          =2S(L,t)-(Qsize-1).                            (DA8)

The one e-axis call per original incidence remains. Thus the destination
cost per half is lambda+T, replacing lambda+A where A=(q-1-t)lambda'.
The sum over queries is still taken before each leaf endpoint and does
not multiply this bill by m.

## 4. Combined call invoice and scope

Together with the source copying graph the free endpoint bill becomes

    F_shared=2(D-1)+2lambda+2S+2T
            =2(D-1)+2lambda+6S-2(Qsize-1).               (DA9)

For q=4,L=4, S=T=14 and Qsize=15, giving 154 calls, versus 230 with
source reuse alone, 306 with independent preconditioning, and 800 in the
original literal count. For q=8,L=4, S=78,T=92,Qsize=65, giving 630,
versus 1,342, 2,082 and 6,240. These are exact sufficient axis counts,
not measured full-machine runtimes.

The charged term is unchanged. The new free bill is at most
O(D+lambda+2^t(C L)^L). This changes the local invoice. Optimizing or
lower-bounding that new invoice is a separate calculation; an old
unshared-invoice barrier is not automatically reused. This note claims
no improved complete H(n), no actual-time lower bound, and no removal of
the open joint-rectangle hypothesis.

## 5. Physical and precision charges

Generate B_w, its dual, alpha_R, the tree and leaf maps by binary
elimination in polynomial local-arity preflight work. Newly introduced
coefficients are signs; normalized children retain the compiler's even-f
rational normalization. The one output direction and all internal block
directions occupy complete f-bit auxiliary fields throughout.

Store at most Qsize<=lambda destination accumulators, alongside the already
charged incidence arrays. Consume child accumulators after transforming
and adding them. The combined source/destination graphs fit an absolute
enlargement of the admitted O((1+lambda)V) local row storage. Every copy,
addition, row movement and return is charged to polynomial ordinary
routing work; none uses free random access. No tape is allocated per node.

The expensive axis counts are exactly those displayed. Ordinary maps act
within the same active fields and have compact finite descriptions. The
common root field and outer all-visited cap remain inherited interfaces
of the admitted compiler, rather than new results of this note.

Normalized transforms and permutations are unitary. Finite duplication
and addition maps have norm bounded by the square root of their fanout
or fanin, giving logarithmic growth O(log lambda). The compiler's path
and event-count guard charges the polynomial number of these events.
The final auxiliary phase stays in its original order, after the fixed
return to physical coordinates, and is not commuted through graph edges.

## 6. Exact finite checks

`verify_shared_fourier_destination.py` passes 164,932 exact shear identity
entries in 3,730 cases. The omitted-conjugation-phase control rejects
52,304 entries. Actual Gram quotient calculations verify 98 complete
rectangle spans and 9,250 entries of destination accumulation from
independent random integer leaf arrays. The latter includes an auxiliary
dimension-13 example at every output position. Twenty-five tested
representatives have nonzero components in selected internal spaces,
so the phase case cannot be removed by a claimed common complement.

Another 300 exact integer profiles verify DA8 and the combined invoice.
The self-contained JSON receipt is `shared-fourier-destination-verification.json`.
The checker imports basic exact helpers from
`verify_nested_fourier_source_reuse.py`. It tests both complete small
matrices and larger deterministic integer arrays, using unnormalized
Hadamard matrices on both sides of equal identities; normalization factors
match by dimension. No fixed-tape execution or formal proof is claimed.

Credits: the pinned arbitrary-subspace endpoint proof; S004 source reuse;
independent lead and Route C line/shear factorization observations;
concurrent E003's earlier rank-weighted invoice; E002 physical suppliers;
@CubeJerry; substantial ChatGPT assistance.
