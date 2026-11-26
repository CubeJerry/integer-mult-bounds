# Full-rate Bell encoding and a shared quadratic-key executor

Status: **new constructive algebra and a local fixed-tape compiler;
independent review pending**. No improved multiplication envelope is
claimed. The numerical and layout entry/exit costs are displayed first
and remain binding. This representation preserves arbitrary independent
payloads; it does not compress them to orbit averages.

Pins: programme `62d9d8e917379cb2edc17c9761e12e2345bc01f4`; OpenAI math
`3344da59991ed94f9ba711217b29c1d760badfa6`. Dependencies: S005 RO1--RO3;
S003 `route-a/compact-rational-walsh.md` (CW), especially section 2;
actual Fourier `kernel.tex`, `binary.tex`, and `repair.tex` at that pin.

## 1. Optimistic complete budget and immediate unfavorable recurrence

Let f=2t, a=A f, and V be the encoded bit volume of arbitrary independent
payloads at all addresses in F2^(A by f). Pair the f columns. A full-rate
orthogonal Bell transform E changes their basis. In that basis, every
columnwise binary reindexing and every whole-row Walsh transform becomes
a signed linear permutation on 2A rows of t-bit slots. Quadratic-key
tables also admit the local executor proved below.

Let B_(2A,t) be the cost per bit of entering and leaving the RO layout
on these labels, and L(a) the actual field-XOR/reorder bill for Bell
encoding. A circuit with polynomially many admitted local stages has
the complete tentative invoice

    T_circuit(a) <= 2 T_Walsh(a/2)
                   + V B_(2A,t) + V L(a)
                   + V poly(A,m) scalar_cost(k).       (BE0)

Each half-width Walsh acts on the FULL incoming V, once at entry and
once at exit. If the entire transform is recursively computed this way,
even free layout/local work gives t(a)<=2t(a/2)+O(1), hence the resulting
upper bill is O(a), not O(sqrt(a)). At square-root normalization the
child mass is 2 sqrt(1/2)=sqrt(2). This is a limitation of this direct
recursion, not a complexity lower bound.

The present generic RO converter has B_(2A,t)=O(poly(A)+a). The claimed
benefit is the exact closure of a broader local algebra in one full-rate
representation, with a single shared entry/exit. A faster converter,
endpoint cancellation or another complete recurrence is still required.

## 2. The Bell change of basis

For u,v in F2^A define

    E_A |u,v> = 2^(-A/2) sum_z (-1)^(v dot z) |z,z+u>.  (BE1)

The states on the right are an orthonormal basis: unequal u have
disjoint supports, and for equal u character orthogonality distinguishes
v. Thus E_A is square and invertible. Put E=E_A^(tensor t), after the
specified column pairing. It has exactly 2^(Af) input and output
coordinates. No zero-initialized ancilla or discarded coordinate occurs.

Writing all first labels u as one s=A t-bit field and all v as another,
E is one normalized Walsh H_s on v followed by the linear permutation

    (u,z) -> (z,z+u).                                  (BE2)

Its inverse performs the inverse permutation then H_s. The permutation
and column-pair layout must be physically implemented; BE2 never makes
them free. In the source's even arity A, s is even and the normalization
is dyadic. Other parities can use Q(sqrt(2)) or an explicit one-bit
normalization, with its cost charged.

## 3. Exact monomialization of the generator family

**BE3.** Let G_M|x>=|Mx> for M in GL_A(F2), and let H_i be normalized
Hadamard on coordinate i. In Bell labels their paired actions are

    E_A^T (G_M tensor G_M) E_A |u,v>
        = |M u, M^(-T) v>,                            (BE3a)

    E_A^T (H_i tensor H_i) E_A |u,v>
        = (-1)^(u_i v_i) |swap_i(u,v)>.               (BE3b)

Here swap_i exchanges just u_i and v_i. Any product of these generators
and quadratic sign phases is therefore a signed linear permutation.
The action on all t paired columns applies that same binary matrix to
each column and multiplies a sign from a sum of quadratic column forms.

**Proof.** In BE3a change z to Mz in BE1. For BE3b, the one-bit
coefficient of |p,q> is

    2^(-3/2) sum_z (-1)^(v z + p z + q(z+u)),

which vanishes unless p+q=v and otherwise equals
2^(-1/2)(-1)^(q u). This is (-1)^(uv) E_1|v,u>.
Tensor with the other coordinates. The quadratic phase case is BE4
below. Products preserve the signed-permutation property. QED.

This is the elementary Pauli-conjugation identity for a real Clifford
action, but BE1--BE3 give a direct proof and exact conventions. It is
not asserted for arbitrary orthogonal matrices or arbitrary phases.

**Corollary BE3L.** In the RO layout of the stacked label matrix
Z=[U;V] in F2^(2A by t), every such generator costs poly(A) V plus its
charged scalar arithmetic, with absolute O(V) visited cells. RO3 applies
to the 2A by 2A linear matrix. Its sign is evaluated from the reconstructed
address in poly(A) times record width. A polynomially long generator
word retains a polynomial-A local bill.

## 4. Arbitrary tables of quadratic parity keys remain local

Let q_j:F2^A->F2, 1<=j<=m, be explicit degree-at-most-two polynomials.
Write their polar forms as

    q_j(x+y)+q_j(x)+q_j(y)+q_j(0) = x^T L_j y,

where L_j is symmetric with zero diagonal. The table at an original
address X depends on the keys

    k_j(X)=sum_(c=1)^(2t) q_j(X_c) mod 2.             (BE4a)

It may apply an arbitrary specified matrix F(k_1,...,k_m) to the
independent row roles. No low degree or sparsity is required of F;
its actual coefficient-generation and arithmetic costs remain charged.

**BE4.** The Bell conjugate of D_j=diag((-1)^(k_j(X))) acts by

    |U,V> -> (-1)^(eta_j(U)) |U,V+L_j U>,             (BE4b)
    eta_j(U)=sum_(h=1)^t [q_j(U_h)+q_j(0)].

For fixed U let D_U be the span of the m matrices L_j U. Its dimension
d is at most min(m,A rank(U)), and every coset V+D_U stays in one
rowspace block of [U;V]. The entire table F is diagonalized by one
d-bit Walsh on each such coset, followed by the table on a computable
affine subspace of the m keys, followed by the inverse Walsh.

**Proof.** Multiply the coefficient of |z,z+u> in BE1 by
(-1)^(q_j(z)+q_j(z+u)). Its exponent is
q_j(u)+q_j(0)+z^T L_j u, giving BE4b. Tensor over pairs. Choose
independent generators Delta_(j_h)=L_(j_h) U, h=1,...,d, and express

    Delta_j=sum_h alpha_(j,h) Delta_(j_h).

In coordinates z in F2^d on a fixed coset, D_j is translation by
alpha_j with scalar sign (-1)^(eta_j). After Walsh its eigenkey is

    k_j=eta_j(U)+alpha_j dot lambda.                  (BE4c)

This explicitly handles dependent generators: a relation among the
translations can have a nonzero phase and need not give the identity.
All D_j commute. Joint spectral functional calculus, or expansion of
F on the Boolean cube, therefore gives the asserted table identity.
The argument retains every coordinate and does not require enumerating
the cube of 2^m possible keys. Finally V->V+L_j U is an invertible
row operation on [U;V], so a whole coset lies in its same RO block. QED.

## 5. Fixed-tape execution of BE4 in the supplied RO layout

Assume the same complete fibres, outer spectators, record widths and
absolute-volume conventions as RO3, with at most polynomially many row
roles. In a rowspace W of rank r, write

    [U;V]=[C_U;C_V] B_W.

The shear generators are represented by L_j C_U in F2^(A by r).
Thus all elimination, coset-representative and local-coordinate work
uses vectors of at most A r<=2A^2 bits, independent of t. Gaussian
elimination computes a canonical representative Cbar_V modulo their
span and the d-bit translation coordinate z. Sort within W by

    (C_U,Cbar_V,role,z).

The key has O(A^2+log roles) bits and also O(a+log roles) bits, so it
fits a constant number of numerical records. Every resulting suborbit
has exactly 2^d independent entries for each role, since all its shear
matrices are invertible on the stacked address. This completeness is
why the within-suborbit Walsh does not require padded missing entries.

Compute an unnormalized Walsh on z by d stages of actual streaming
butterflies. At a stage, sort by the partner bit and the remaining
O(A^2)-bit local key, then scan paired streams and form sums/differences.
Sort back or retain the explicit next-stage order. This costs a fixed
polynomial in A,m times V and uses a fixed number of full streams, with
the same intervals reused. Apply F on keys BE4c by serial row-role
scans, then perform the second unnormalized Walsh and scale by 2^(-d).
Finally sort by (role,C-rank) to restore the supplied RO layout.

The values eta_j are computed from U=C_U B_W in poly(A,m) t bit work,
which is poly(A,m) times the record width w>=a. They can be retained
for each fixed U subrun or recomputed; neither option needs a 2^m table.
If the supplied F evaluator costs P(A,m,k) bit steps per coefficient,
its full polynomial-role volume is added explicitly. Under the CW
coefficient bounds, impose a fixed numerical guard
k>=C(A+m)^c, with absolute effective C,c large enough to dominate all
coefficient heights and polynomial control parameters. Assume a<=k,
and use the resulting fixed O(k)-bit format throughout, including
the extra O(d) integer/fractional margin of the local transforms.
With k-bit numerical records the bill is then

    time <= V poly(A,m) (1+log(k+2))
            + polynomial(A,m,k) setup,                (BE5)
    visited cells <= C V + polynomial(A,m,k),

with C absolute. Setup is not assumed absorbed except where a complete
numerical application proves that its exponential fibre volume pays it.
This is a physical local compiler in a supplied layout, not a complete
uniform global Walsh theorem.

Each unnormalized local transform has operator norm 2^(d/2). Before
the final 2^(-d) scaling, the combined excursion can be
2^d ||F||, where d<=a/2<=k/2. This requires O(d) additional bits plus
the guarded coefficient-height margin, still within a fixed O(k)-bit
format. A normalized version avoids that growth but may introduce
sqrt(2). Either implementation has a transparent local
precision invoice. A global numerical proof must include rounding at
these extra gates and coefficient preparation; BE5 alone does not
assert the final NW error bound.

## 6. Check against the actual source masks and repair

At the pinned Fourier source `kernel.tex`, the j-th binary query key is

    sum_c [X_(c,j) Z_(c,j)+sum_aux X_(c,i) Z_(c,i)] mod 2.

It is exactly BE4a. Initial/final kernel signs and representative
changes are bilinear forms in a column, and source/destination changes
apply the same binary matrix separately to every column. Substituting
a linear map into a quadratic polynomial preserves degree at most two.
`binary.tex` implements the selected row Walsh on every f-bit axis.
These concrete gates lie in BE3--BE4; the generic phrase "fixed column
functions" would not by itself establish the required quadratic scope.

The scalar repair table in `repair.tex` is a matrix function of the
query keys. S003 CW section 2 gives the actual polynomial evaluator:
enumerate O(m) seeds, compute shifted counts and Newton values, find
the nonzero-gap defect set, and compute its Vandermonde inverse and
division coefficients. The map can be dense as a Boolean function.
BE4 invokes its evaluator on each attained affine key BE4c, without
expanding 2^m terms. It conjugates F of the paired generators; it does
not incorrectly replace this by the tensor square of F. Copies, scalar
row maps, zero rows and restrictions commute with the common
address-basis change and retain the source's constant-array schedule.

This covers the stated source local algebra, including full-rate repair,
for common even slot width and common pairing. It does not cover
arbitrary address masks: degree-three column forms can leave quadratic
dependence on the Bell summation variable and fail BE4b. Different forms
on the two members of a pair are not automatically covered. Spectators
must be outer fibres; arbitrary active/spectator coupling is not asserted.

## 7. What the representation achieves, and what remains

The ordinary rowspace layout was not closed under a full Walsh child.
Bell encoding moves to a different invariant decomposition. Both the
child Walsh and the source repair algebra remain within its 2A-row
orbit blocks, with full independent input dimension. The earlier RG
rank gate concerns the ordinary rowspace partition and is not violated.

This closes an algebraic and local-delivery gate, not the numerical
recurrence. Even a single full Walsh becomes a signed permutation;
that observation is no cheaper than the two real half-width Walsh
calls preparing and removing E. A source template with child volume
factor b_A, expanded once inside each encoder, would yield

    t(a) <= 2 b_A t(a/(2A)) + endpoint/local bills.     (BE6)

Its normalized child mass is sqrt(2) b_A/sqrt(A), counting both
encoder expansions and their local costs. Substitution alone does not
erase costs inside those encoders. The current orbit converter still
contributes V a at the parent, dominating the desired square-root scale.

The positive object is a full-rate common-layout executor for the
larger algebra with an exact endpoint invoice. Further work must
improve or amortize an actual Bell/orbit converter, or prove endpoint
cancellation in the complete application with arbitrary inputs,
precision and absolute O(V) visited cells intact. Counting Clifford
generators or omitting the exit transform does not discharge that gate.
