# Active query volume with inverses and arbitrary spectral repairs

Status: **proved scoped linear-algebraic theorem; independent review
requested**. This is a second obstruction mechanism beyond the
polynomial-output rank theorem in Route B. It allows inverse affine gates,
nonuniform path depth, arbitrary workspace and row mixing. It charges the
sum of active row volumes. It does not lower-bound general tape time or
establish a new multiplication overhead envelope.

Let `r>=2`, `m>=1`, and let K contain all r-th roots of unity with
`char(K)` not dividing r. Put

    A=K[x_1,...,x_m]/(x_1^r-1,...,x_m^r-1),
    N=r^m,  chi=product_j x_j,  Omega=mu_r^m.

Monomials with coordinate exponents in `{0,...,r-1}` form a K-basis of A.
Support weight counts nonzero exponents. For an integer k, let `Pi_k`
be the K-linear projection retaining exactly the monomials of support
weight at most k. This projection is defined in the monomial basis; it
is not asserted to be a cheap physical operation.

Define

    n_j = binom(m,j) (r-1)^j  for 0<=j<=m, and 0 otherwise,
    B_k = n_k+n_(k+1),
    J_k = #{alpha: 1_[wt(alpha)<=k] !=
                       1_[wt(alpha+1 mod r)<=k]}.

The following statements hold over finite fields as well as characteristic
zero. All ranks are ordinary K-linear ranks after expanding in the monomial
basis, or equivalently summed spectral ranks when specified.

## 1. A boundary-rank lemma for affine queries and their inverses

A query gate on h rows is multiplication by an h-by-h matrix

    Q(x)=Q_0 + sum_(j=1)^m sum_(a=1)^(r-1) Q_(j,a) x_j^a,

where the coefficient matrices lie in K. No commutation among them is
required. It acts on `A^h`; other state rows, if any, are untouched.
Every monomial term changes support weight by at most one. Therefore

    rank(Pi_k Q-Q Pi_k) <= h B_k.                         (C1)

Indeed, a term can cross the cut only between support levels k and k+1.
The commutator has both its row support and its column support inside
the direct sum of these two homogeneous spaces, whose dimension is h B_k.
Diagonal and within-side blocks cancel. This argument does not diagonalize Q.

If Q is invertible at every spectral tuple, it is invertible on `A^h` by
the Chinese remainder decomposition, and

    [Pi_k,Q^-1] = -Q^-1 [Pi_k,Q] Q^-1.

Consequently

    rank[Pi_k,Q^-1] = rank[Pi_k,Q] <= h B_k.              (C2)

The entries of Q inverse may have very high polynomial degree. The equality
above is precisely why the argument still applies to such a rational gate.
The theorem does not assume an inexpensive physical algorithm for inversion;
it grants the inverse as an allowed gate and still proves the restriction.

## 2. Networks, changing row counts and spectral tables

Consider any finite linear straight-line network whose input and output
each have W arbitrary independent rows. Its state may have any finite
number of rows at intermediate steps. Permit these operations:

* Query-independent K-linear row maps, including copies, accumulation,
  zero initialization and deletion.
* Affine query gates as above on h_i active rows, or their everywhere
  defined inverse gates on the same rows.
* Arbitrary spectral-table gates with a query-independent reference gate.
  If `Delta_i(omega)` is the departure from that reference, set

      ell_i = N^-1 sum_omega rank Delta_i(omega).

  A table acting on at most ell channels has `ell_i<=ell`. The gate may
  be used repeatedly; each occurrence is charged separately.

All gates preserve the common spectral decomposition. Query-independent
row maps have the form `C tensor I_A`; an arbitrary permutation of physical
addresses need not have this form and is not automatically free.

Let T be the network's input-output map and put

    q = (sum_i h_i)/W,
    h = (sum_i ell_i)/W,
    e = (NW)^-1 sum_omega rank(T(omega)-chi(omega) I_W).

Thus q is total normalized active query-row volume, not maximum depth;
h is total normalized table rank width, not the number of distinct tables;
e is final average normalized rank defect.

**Theorem C.** Every such network satisfies

    (B_k/N) q + 2h + 2e >= J_k/N.                        (C3)

This holds for every k; the best cut may be chosen after the network.

### Proof

For a rectangular K-linear map G from one state to another, write its
commutator as `Pi_out G-G Pi_in`, using the projection for the relevant
number of rows. Constant row maps have zero commutator. For composable
maps, the identity

    [Pi,UV] = [Pi,U]V+U[Pi,V]

uses the appropriate intermediate projection and is valid with changing
dimensions. Rank subadditivity and (C1)--(C2) bound the contribution of
the query gates by `B_k sum h_i`.

For a table gate, subtract its constant reference, which commutes with
the projections. Its departure has global rank `N ell_i` under spectral
decomposition, so its commutator has rank at most `2N ell_i`. Telescoping
the entire network therefore gives

    rank[Pi_k,T] <= B_k sum h_i + 2N sum ell_i.           (C4)

Multiplication by chi permutes reduced monomials by adding one to every
exponent. Its commutator with Pi is a permutation matrix restricted to
the J_k basis monomials whose cut membership changes, with nonzero signs.
Its rank on W rows is exactly `W J_k`, also in characteristic two.

Let E=T-chi I. Its global rank is `NW e`, and its commutator has rank
at most `2NW e`. Applying the triangle inequality for rank to
`[Pi,chi I]=[Pi,T]-[Pi,E]` and using (C4) proves (C3). QED.

## 3. Exact binary and ternary cuts

For r=2 and odd m, choose `k=(m-1)/2`. Multiplication by chi complements
every exponent bit, so every monomial crosses the cut. Consequently

    J_k=2^m,   B_k=2 binom(m,(m-1)/2),

and (C3) becomes the exact inequality

    [2 binom(m,(m-1)/2)/2^m] q + 2h+2e >= 1.            (C5)

For even m, choose `k=m/2-1`. The central layer remains on the same side
under complementation, and all other monomials cross. Hence

    J_k=2^m-binom(m,m/2),
    B_k=binom(m,m/2-1)+binom(m,m/2).                     (C6)

Stirling's formula then gives, for any fixed `eta<1/2` and networks with
`h+e<=eta`,

    q >= [sqrt(pi/8)(1-2eta)-o(1)] sqrt(m).              (C7)

For r=3, choose `k=floor(2m/3)` and put `a=ceil(m/3)`.
A reduced monomial lies below the cut exactly when its count n_0 of zero
exponents is at least a. After multiplication by chi, the same condition
uses the count n_2. Thus J_k counts tuples for which those two threshold
indicators differ.

The three counts `(n_0,n_1,n_2)` are exchangeable and sum to m. Except
when all three equal m/3, exactly one or two of their threshold indicators
are one: all three cannot be below threshold, and all three cannot be
above threshold. Among the three unordered pairs, exactly two then differ.
By exchangeability, each pair differs with probability 2/3. Therefore

    J_k/3^m = 2/3                         if 3 does not divide m,
    J_k/3^m = (2/3) [1 - m!/((m/3)!^3 3^m)]  otherwise. (C8)

This is an exact finite count, not a normal approximation. The exceptional
balanced-count probability is O(1/m). The binomial layer estimate gives

    B_k/3^m = [3/sqrt(pi)+o(1)] / sqrt(m).

For any fixed `eta<1/3`, the ternary F4 source interface therefore obeys

    q >= [2sqrt(pi)/9 (1-3eta)-o(1)] sqrt(m)
                     whenever h+e<=eta.                 (C9)

No invalid binary character in characteristic two appears in this argument.
The three cube roots in F4 are distinct, and the support-weight boundary
counts each of q_j and q_j squared as one affine query term.

### Stronger cut from concurrent E003: arbitrary nonzero local spectra

**Provenance.** The concurrent E003 note
`results/epsilon-uniformity/sessions/E003/route-c/MATRIX-PREDICTION-RANK-BARRIER.md`
supplies a weighted two-point basis which improves the ternary bound above.
It was read at programme commit
`df91e4c8e31b1020e05056db5b0eb16169ef3421`, file SHA256
`370e578d0add67196e62960bed110da9384f39c4497506b423c1e0541fe86778`.
The following transfer uses that basis with the independently developed
commutator argument. It is credited as a cross-session combination, not
an independent discovery of E003's polynomial-rank theorem.

Choose two distinct nonzero local eigenvalues a_i,b_i in K. On their
Boolean coordinate x_i put

    f_i=a_i+(b_i-a_i)x_i,
    z_i=x_i-b_i/(b_i-a_i),
    c_i=b_i-a_i,   d_i=-a_i b_i/(b_i-a_i).

Both c_i and d_i are nonzero, and in the two-point function algebra

    f_i*1=(a_i+b_i)*1+c_i z_i,     f_i*z_i=d_i,
    f_i^-1*1=d_i^-1 z_i.                                  (C9a)

Use the product basis `phi_S=product_(i in S) z_i`, and let Pi retain
degree at most `k=floor((m-1)/2)`. Multiplication by any function of one
local eigenvalue still changes this degree by at most one, since the
local function algebra has basis `(1,z_i)` and a quadratic reduction.
Thus the query boundary rank is the binary quantity

    B=binom(m,k)+binom(m,k+1).

Write L for degree at most k and H for degree at least m-k. They have
equal dimension `l=sum_(j<=k) binom(m,j)` and are disjoint. By (C9a),
the target `f=product_i f_i` sends H into L; invertibility and equal
dimensions imply `fH=L`. Its inverse sends L into H, also directly from
(C9a). Hence the off-diagonal block `Pi f(I-Pi)` has rank l. The block
`(I-Pi)f Pi` is injective on L: if v lies in L and fv lies in L, then
v lies in `f^-1 L=H`, forcing v=0. It also has rank l. Therefore

    rank[Pi,f]=2l
      = 2^m                          for odd m,
      = 2^m-binom(m,m/2)             for even m.             (C9b)

The complete network proof now gives exactly (C5)--(C7) on every two-point
product, in **every characteristic** permitting those two nonzero values.
No positivity of E003's algebraic weights is needed.

For larger finite local spectra S_i, choose a uniformly random unordered
pair in each S_i, then a uniformly random endpoint. The resulting point
is uniform on the full product. Active query volume q is unchanged by
restriction; table and final-error ranks average to their full-product
values. Averaging the two-point inequality proves the following stronger
form of the active-volume result:

**Corollary C-universal.** For arbitrary finite local sets of at least two
distinct nonzero field elements, target `product_i q_i`, and affine gates
whose entries are sums of arbitrary one-coordinate functions, the exact
binary inequalities (C5)--(C6) and asymptotic bound (C7) hold.

This includes the full ternary F4 spectrum and strengthens (C9). The exact
standard-basis ternary count (C8) remains valid and useful as a separate
finite check; it is no longer the best constant supplied by this method.
If a local target value is zero, this stronger argument does not apply.

## 4. A related rare-error theorem for one rational matrix fraction

The commutator result is robust under many inverses but gives a square-root
scale. A stronger rare-error tail survives for one general rational matrix
fraction on the binary spectrum.

Let `r=2`, `char(K)!=2`, and let A and B be W-by-W matrix polynomials on
the sign cube, of degrees at most a and b. Suppose B is pointwise invertible.
For either `P=A B^-1` or `P=B^-1 A`,

    average rank(chi I-P)/W
       >= Pr[Bin(m,1/2)>floor((m+a+b)/2)].               (C10)

No commutation between A and B is assumed.

To prove it, put `v=floor((m-a-b-1)/2)` and restrict `D=chi B-A` to
polynomial vectors of degree at most v. The output `Bz` has degree at
most v+b; its chi multiple has degree at least `m-v-b`. The vector Az
has degree at most v+a, strictly smaller. They cannot cancel. If Dz=0,
both are zero; invertibility of B forces z=0. Thus D is injective on a
space of dimension `W sum_(j<=v) binom(m,j)`. Multiplication by B on the
appropriate side preserves the rank of the error. Binomial symmetry gives
(C10). For v<0 the zero lower bound is understood.

If B is allowed singularities, put

    eta_B = (NW)^-1 sum_omega nullity B(omega).

Whenever P is defined and satisfies `A=P B` or `A=B P`, the same argument
loses at most the global kernel dimension of B, and gives

    average rank(chi I-P)/W + eta_B
       >= Pr[Bin(m,1/2)>floor((m+a+b)/2)].               (C11)

Indeed, the kernel of D on the low-degree subspace is contained in the
kernel of B. This exposes singular denominators as a charged defect rather
than treating them as a free escape.

Consequently a one-fraction model with rank error plus denominator defect
at most `m^-c` requires

    a+b >= (1-o(1)) sqrt(2c m ln m).

The numerator and denominator must both be charged. A small selected entry
of a much larger inverse matrix is a different interface: its unused rows
cannot be counted as independently transformed data. The active-volume
network theorem above is designed to retain that expense.

The same E003 basis also extends (C10)--(C11) to arbitrary nonzero local
spectra. On a two-point product, degree is measured in the phi basis,
equivalently ordinary Boolean degree. For a low-degree vector z, Bz has
degree at most v+b, whereas `f^-1 A z` has degree at least `m-v-a` by
(C9a). Those degree ranges are disjoint when `2v+a+b<m`. Thus
`B-f^-1 A` has the same injection modulo the kernel of B as in the binary
proof. Multiplying by the nonzero f and the appropriate B preserves or
bounds ranks exactly as before. Averaging two-point restrictions gives
the same binomial tail for the full local spectrum. This extends the
rare-error numerator-plus-denominator restriction to the characteristic-two
order-three setting with the binary leading constant, with explicit E003
provenance.

For larger local alphabets, a and b in this extension bound the Boolean
degrees of A and B on every product of two-point restrictions. A support
degree bound or a charged affine-query construction gives this premise.
An uncharged arbitrary spectral table does not supply such a degree bound.

## 5. Scope, relation to the programme and next questions

Route B's polynomial theorem is sharper for a fixed polynomial output
depth, especially when rank repair is polynomially rare. The present
commutator theorem covers inverse-affine gates and charges every active
row occurrence even with nonuniform depths and initialized workspace.
It shows that adding a cheaply declared inverse to the same spectral
model does not make the square-root local query expense disappear.

Neither result proves a general time lower bound. An actual physical
coordinate transformation may mix spectral tuples and need not commute
with the cut projection. Nonlinear operations are also outside the model.
To use either theorem in an end-to-end invoice, prove that the supplier's
charged gates meet the stated interfaces; do not equate algebraic width
with head movement, precision or visited cells.

The exact field cuts and constants are potentially useful for deciding
whether a proposed inverse-based or highly unbalanced predictor merely
transfers its cost. They do not rule out the exact square-root endpoint.
The remaining constructive question is whether the necessary square-root
query volume can be reached with efficient routing, constant-fraction
repair and a uniform physical caller.

Credits: classical rank-commutator and degree-filtration methods; Route B's
spectral rank model and rank-repair formulation; the pinned OpenAI source
query interfaces; @CubeJerry; substantial ChatGPT mathematical assistance.
No literature-priority claim is made. Independent review and finite exact
checks are recorded separately; no formal kernel build or tape execution
is implied by this draft.
