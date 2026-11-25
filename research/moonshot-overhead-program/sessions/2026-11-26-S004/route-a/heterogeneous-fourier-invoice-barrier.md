# Heterogeneous alphabets do not remove the literal Fourier routing logarithm

Status: **proved scoped invoice theorem; independent review requested**.
This concerns a specified positive source invoice. It is not a lower bound
for Fourier transforms, the interchanger, integer multiplication, arbitrary
rectangle decompositions, or the square-root endpoint. It does not oppose
the conditional JR transfer, whose correlated rectangles change the very
incidence charge retained here.

The finite family is the actual binary Fourier label construction in
OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier
`build/kernel.tex`, allowing a different power-of-two alphabet in each
coordinate. The complete source file was read. The ordinary rank and
finite-rank calculations below are over Q and F2 respectively; they are
not interchanged.

## 1. The enlarged family and its exact quantities

Let L=2r>=2, q_i=2^(t_i), t_i>=1 integers, and

    V=product_(i=1)^L [q_i],     N=product_i q_i.

For labels v,w let Delta be their Hamming distance. Define

    Gamma(v,w)=1-Delta(v,w) in F2,
    P(v,w)=p(Delta(v,w)) in Q,
    p(k)=product_(h=1)^r (1-k/(2h)).                         (HF1)

Keep the source's literal first-difference product decomposition on the
odd-distance free support. A fixed label belongs to exactly t_i directed
first-difference rectangles on its specified side in coordinate i. Its
free incidence is therefore exactly

    lambda=sum_(S subset [L], |S| odd) product_(i in S) t_i
           =[product_i(1+t_i)-product_i(1-t_i)]/2.           (HF2)

Every odd-distance weight -p(k) is nonzero. No omitted zero-weight piece
reduces HF2. The same load holds on the other side.

Allow the charged matrix P even an optimal rational rank factorization,
better than the source's explicit cylinder rectangles. Write
rho=rank_Q P and D=rank_F2 Gamma. For m>=2 define the positive invoice

    C(m;t_1,...,t_L)=D [lambda + m rho/N].                   (HF3)

The theorem lower-bounds this specified expression. Source execution
provides sufficient dimension/incidence/charged-rank bounds; that fact
alone does not prove every actual implementation must spend HF3 time.
Endpoint optimization or cancellation can leave this theorem's scope.

There is no imposed hard guard m rho/N<=1. The result thus also tests
whether relaxing that usual sufficient guard could improve this same
literal invoice. Alphabet sizes are unrestricted and need not agree.

## 2. Exact binary Gram rank

**Lemma HF1.**

    D=2+sum_i(q_i-2).                                      (HF4)

In particular D>=max_i q_i.

Proof. For a function f on the full label product, let F=sum_v f(v), and
let g_i(a)=sum_(v:v_i=a) f(v) be its coordinate marginals, all over F2.
Every tuple of marginals with sum_a g_i(a)=F for each i is attainable.
Fix one reference label, place all nonreference marginal values on its
coordinate lines, and adjust the reference value to have total F. This
explicitly constructs the required function.

The space of attainable marginal tuples has dimension sum_i q_i-L+1.
The Gram action is

    (Gamma f)(w)=(1-L)F+sum_i g_i(w_i).

If this is zero for every w, varying one coordinate at a time forces
each g_i to be constant, say a_i. Since each q_i is even, its sum is
zero, hence F=0. The remaining condition is sum_i a_i=0, a kernel of
dimension L-1. Subtracting gives sum_i q_i-2L+2. This argument also
works for odd L, although only even L is used below. QED.

This exact formula explains why the coarse source dimension 1+sum_i q_i
cannot be made logarithmic in the largest alphabet by a better rank
factorization. For the all-binary family it correctly gives D=2.

## 3. An exact charged-rank lower bound

Expand the rational polynomial in the source binomial basis:

    p(k)=sum_(j=0)^r c_j binom(L-k,j).

The leading ordinary polynomial coefficients give c_r=2^(-r), hence
it is nonzero. Each binomial term is the sum over j-coordinate equality
cylinders. Decompose Q^[q_i] into the constant line and its zero-sum
subspace, of dimensions 1 and q_i-1. These are a direct sum over Q.

For a coordinate subset T of size exactly r, take the tensor product of
zero-sum subspaces in T and constant lines outside. In a cylinder term
indexed by S, an all-ones factor annihilates this space unless T subset S.
Since |S|<=r, only S=T survives. P acts on this whole subspace as the
nonzero scalar

    2^(-r) product_(i notin T) q_i.

The subspaces for different T are disjoint. Therefore

    rho >= sum_(|T|=r) product_(i in T)(q_i-1)
         = e_r(q_1-1,...,q_L-1).                            (HF5)

Relabel so t_1<=...<=t_L and put T0=sum_(i=1)^r t_i. The summand
on the r largest alphabets and q_i-1>=q_i/2 yield

    rho/N >= 2^(-T0-r).                                    (HF6)

For the literal cylinder count, the stronger lower bound
N_ch/N>=2^(-T0) follows immediately. HF6 permits arbitrary rank
compression of the charged matrix and is the bound used below.

## 4. Uniform barrier, without a charged-rank guard

**Theorem HF2.** There are absolute constants c>0 and x0 such that,
for every m with x=log2 m>=x0, every even L>=2, and every list of
integer t_i>=1,

    log2 C(m;t_1,...,t_L) >= c sqrt(x log2 x).              (HF7)

One may use c=1/8 and x0=256 in the elementary estimates below.

Proof. Put b=log2 C. Since all products in HF2 are at least one,

    log2 lambda >= L-1=2r-1.                               (HF8)

The odd subset [L] minus its smallest index contains the r largest t_i.
Every one of those is at least T0/r; other factors are at least one.
Together with HF4 and HF6 this gives

    b >= T0/r,
    b >= r log2(T0/r),
    b >= 2r-1,
    b >= x-T0-r.                                          (HF9)

If b>=x/4, HF7 holds for x>=256. Otherwise the third and fourth
inequalities imply

    r<(x/4+1)/2,       T0>=x-b-r>=x/2.

Write w=sqrt(x/log2 x), v=sqrt(x log2 x).
If r<=w, the first inequality of HF9 gives b>=v/2.
If r>=v/8, the third gives b>=v/4-1>=v/8.
In the remaining range w<r<v/8,

    log2(T0/r)>=log2(x/(2r))
               >2+(log2 x)/2-(log2 log2 x)/2
               >=(log2 x)/4.

The second inequality gives b>=v/4. Every case proves HF7. QED.

The homogeneous constructive choice in the predecessor attains
O(sqrt(x log(x+2))) for this logarithmic invoice. Consequently neither
heterogeneous alphabets, exact minimization of the Gram rank, arbitrary
rank compression of P, nor simply weakening the charged-rank guard can
remove the logarithm while the literal first-difference free incidence
HF2 is retained.

## 5. Exact finite checks

`verify_heterogeneous_fourier.py` imports the elementary exact helpers in
`verify_joint_rectangle_fourier.py`. Its receipt
`heterogeneous-fourier-verification.json` reports 13 heterogeneous matrix
families covering 101,200 entries. Binary elimination gives HF4 exactly;
modular elimination at an explicitly checked good odd prime agrees with
the rational eigenspace rank and verifies HF5. The bad-field control
uses q_1=q_2=4: the zero-one Gram matrix has binary rank six but rational
rank sixteen. The heterogeneous (2,4,8,8) control has a vanishing
lower-degree eigenvalue, while every top-degree eigenvalue remains nonzero.

The checker also verifies the exact first-difference incidences and passes
1,452 integer invoice-majorant profiles with up to 64 coordinate alphabets.
These finite checks do not prove the asymptotic theorem; that proof is the
uniform inequality argument above. No floating-point rank is used.

## 6. Consequence for the current research route

The conditional JR construction replaces HF2 by an exp(O(L)) poly(t)
bound with correlated sides. It changes a binding premise of HF2 and is
not contradicted by this theorem. A weaker parity-specific construction
could also escape: it would suffice to decompose the exact free matrix
I-P into weighted cross-orthogonal rectangles with substantially smaller
per-label incidence and polynomial coefficient heights and descriptions.
Such a family need not partition every all-coordinate-unequal graph, but
its exact weights and support must be proved.

Other possible escapes are a smaller endpoint execution bill, a different
charged predictor matrix, or a different Fourier architecture. The theorem
supplies a falsifiable gate for tempting parameter changes; it does not
claim those alternatives are impossible.

Credits: the pinned OpenAI Fourier label and endpoint construction;
S002's quantitative Fourier profile; E002's separate literal interchange
invoice barrier; S004's joint-rectangle transfer; @CubeJerry; substantial
ChatGPT research assistance. The heterogeneous exact-rank calculation and
relaxed-guard Fourier invoice argument are derived here. No priority,
full-machine execution, formal proof or human-referee certification is claimed.
