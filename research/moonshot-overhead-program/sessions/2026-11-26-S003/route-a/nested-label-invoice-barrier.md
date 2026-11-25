# Asymmetric and deeper labels do not improve the cubic-logarithmic invoice

Status: **proved scoped invoice obstruction, pending independent review**.

This extends the S002 characteristic-two labels to arbitrary nesting depth
and different distance parameters at each level, then proves a lower bound
for their literal shared-pencil invoice. It uses the **actual scalar rank**,
not merely the previously used upper bound, and does not require the rank
occupancy term to be at most one. Thus sharper rank estimation, unequal
inner/outer distances, and additional nesting cannot by themselves improve
the existing `log m = O(J^3 log J)` scale within this invoice.

This is not a lower bound for all physical routing, all label geometries,
all predictor representations, or integer multiplication. The source's
invoice is an upper bound for a specified implementation; a different
implementation may charge fewer conversions. No new complete overhead
bound follows from this obstruction.

Sources: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, tape
`build/interchange.tex`, especially `lem:interchange-labels`,
`eq:interchange-gram` and `eq:interchange-stage-cost`; programme S002
`routes/B/characteristic-two-label-geometry.md` and
`routes/A/fixed-field-extraction-theorem.md`, read at programme
`0607d044d1d09489580da0e5828588820e1a6775`. Route C independently developed
the symmetric two-level rank/incidence obstruction during S003. This note
records the general-depth asymmetric extension and its separate proof.

All logarithms are binary.

## 1. The exact family and invoice

Fix an integer depth `ell >= 2`, powers of two `d_1,...,d_ell >= 2`, and
`q=2^t`, `t>=1`. Put `h_i=2d_i-1`, `V_0=[q]`, and

    V_i = V_(i-1)^(h_i),
    N_i = |V_i| = q^(h_1 ... h_i),
    P = d_1 ... d_ell.

Distinct elements of V_0 are called far. Recursively, two elements of V_i
are far if they differ in exactly d_i coordinates and the corresponding
elements of V_(i-1) are far in all those coordinates. Let A_i be the integer
adjacency matrix of this far relation and set P_i=I+A_i over F2. At level
zero set P_0=J_q, the all-ones matrix, so A_0=J_q-I.

At level one use the source first-differing-bit rectangle partition: choose
the d_1 differing positions, fix the two distinct letters at their first
position, and use a first-differing-bit rectangle on every remaining
position. At each higher level choose the d_i differing positions and take
the product of the preceding rectangles. All unchanged coordinates are
fixed. This is an exact disjoint directed partition. The incidence on
either side is exactly

    lambda_1 = binom(h_1,d_1) (q-1) t^(d_1-1),
    lambda_i = binom(h_i,d_i) lambda_(i-1)^(d_i).       (N1)

Every label has this same incidence: a prescribed q-letter belongs to
exactly t of the first-differing-bit rectangles on each side. At every
level a side contains no far pair. At the top level, if k(v,w) counts far
V_(ell-1) coordinate pairs, then k=0 within either rectangle side and
k=d_ell across the two sides. Therefore the same rational Gram/endpoints
construction applies:

    G_(v,w) = (1-k(v,w)/d_ell) I_2 + (k(v,w)/d_ell) S,
    S = [[0,1],[1,0]],
    D = rank_Q(G),
    a = rank_F2(P_ell)/N_ell.

For the arity m>1 define the literal normalized pencil invoice

    I(m) = D (1+lambda_ell) (1+m a).                  (N2)

The source supplies a fixed absolute multiple of this invoice as a call
upper bound. All other tape expenses remain separately charged. Our
question is whether (N2), even evaluated with the exact rank a, can be
bounded by `m^(1/J)` with a smaller arity scale.

## 2. Exact elementary-symmetric form

For a matrix M acting on one factor, write M[j] for its action on tensor
factor j with identities elsewhere. For every level,

    P_i = e_(d_i)(P_(i-1)[1],...,P_(i-1)[h_i]).        (N3)

To prove this, consider an entry whose two labels differ in k immediate
coordinates. It is zero unless all changed coordinate pairs are far and
k<=d_i. If they are, its coefficient on the right is
`binom(2d_i-1-k,d_i-k)` modulo two. For k=0 this binomial coefficient is
odd. For k=d_i it equals one. For 0<k<d_i put r=d_i-k. The coefficient is
`binom(d_i-1+r,r)`, which is even: adding the positive integer r<d_i to
the binary all-ones integer d_i-1 has a carry. Equivalently, the coefficient
of T^r in `(1+T)^(d_i-1+r)` is zero modulo two by the elementary binary
factorization of `(1+T)^n`. This proves exactly the diagonal-plus-far
support claimed in (N3).

Since q is even, P_0^2=0. The summands in (N3) commute. Squaring in
characteristic two therefore kills every summand, proving

    P_i^2=0,       0 < rank(P_i)/N_i <= 1/2.           (N4)

The positivity also follows from the following rank estimate.

## 3. A lower bound for the actual scalar rank

Let M be a nonzero square-zero matrix on an n-dimensional F2-vector space,
of rank r. Choose U complementary to ker M, so M maps U bijectively onto
im M. In `e_d(M[1],...,M[2d-1])`, restrict the first d factors to U and
the remaining d-1 factors to ker M. Exactly one summand survives. Its image
has dimension `r^d (n-r)^(d-1)`. Consequently

    rank e_d(M[1],...,M[2d-1]) >= r^d (n-r)^(d-1).    (N5)

For a_i=rank(P_i)/N_i, (N4)--(N5) imply

    a_i >= a_(i-1)^(d_i) (1-a_(i-1))^(d_i-1)
        >= a_(i-1)^(d_i) 2^(-(d_i-1)),
    a_0=1/q=2^(-t).

Induction, using the telescoping sum

    sum_(i=1)^ell (d_i-1) product_(k=i+1)^ell d_k = P-1,

gives the uniform actual-rank lower bound

    a >= 2^(-Pt-(P-1)) = 2^(1-P(t+1)).                (N6)

No presumed low-rank certificate, generic matrix rank, or unproved
concentration estimate is used here. This lower bound is deliberately
coarse; Route C's symmetric calculation can be sharper without changing
the implication below.

## 4. Exact rational address dimension

The far graph at every level is regular of odd degree. At level zero its
degree is q-1; at the next level it is
`binom(2d_i-1,d_i) delta_(i-1)^(d_i)`, also odd. Moreover
`A_i=P_i-I` is invertible modulo two by (N4), since `(P_i-I)^2=I`.
Thus its integer determinant is odd and A_i is invertible over Q.

Put n=N_(ell-1), h=h_ell, d=d_ell, A=A_(ell-1), and let delta be A's
odd valency. In the rational decomposition `Q^n = <1> direct_sum 1^perp`,
A has eigenvalue delta on <1> and an invertible restriction to 1^perp.
The matrix K of k(v,w) is the sum of h tensors with A in one factor and
J_n elsewhere. It has the following invariant summands:

* the constant tensor, with eigenvalue `h delta n^(h-1)`;
* tensors with exactly one factor in `1^perp`, on which its restriction is
  `n^(h-1) A|_(1^perp)` and is invertible;
* tensors with at least two such factors, on which K vanishes.

The sum/difference change on the final two coordinates decomposes G into
`J_(n^h)` and `J_(n^h)-(2/d)K`. The latter's constant eigenvalue is nonzero:
`nd != 2h delta`, because the right side has 2-adic valuation one while
n and d are both powers of two at least two. Hence

    D = 2+h_ell (N_(ell-1)-1) >= N_(ell-1),
    log2 D >= (h_1 ... h_(ell-1)) t >= (P/d_ell)t.    (N7)

This is an exact rank calculation for the rational Gram construction;
it does not identify that rank with its rank in the data field.

## 5. The cubic-logarithmic necessary scale

**Theorem N.** For the family (N1)--(N2), let m>1 and real J>=64. If

    I(m) <= m^(1/J),

then

    log2 m >= 2^(ell-2) J^3 log2 J / 128.             (N8)

**Proof.** Put x=log2 m. Each factor in (N2) is at least one. By (N6),

    x/J >= log2(1+m a) >= x-P(t+1)+1,
    x < 2P(t+1) <= 4Pt.                              (N9)

The first inequality remains true when m a>1; we have not imposed an
occupancy cap. The exact incidence (N1), together with
`binom(2d_1-1,d_1) >= 2^(d_1-1)`, gives

    log2 lambda_ell >= ((d_1-1)P/d_1)(1+log2 t)
                       >= (P/2)(1+log2 t).

Therefore

    x >= (JP/2)(1+log2 t).                           (N10)

Combining (N9)--(N10) yields `t+1 >= J/4`, so `t>=J/8>=8`.
In particular `log2 t >= log2 J-3 >= (log2 J)/2`.

Equations (N7) and (N9) imply

    (P/d_ell)t <= x/J < 4Pt/J,  hence d_ell > J/4.

The factor `(q-1)^(P/d_1)` in lambda_ell gives, since t>=2,

    log2 lambda_ell >= (P/d_1)log2(2^t-1)
                       >= (P/(2d_1))t.

Using (N9) again gives `d_1>J/8`. All intervening d_i are at least two,
so

    P >= 2^(ell-2) J^2/32.

Substitution into (N10), followed by `log2 t >= (log2 J)/2`, proves
(N8). QED.

The matching order `log2 m=O(J^3 log J)` for ell=2 is supplied by the
existing balanced choice in S002, with its separate complete invoice and
physical-cost proof. Thus the cubic-logarithmic arity scale is tight for
this literal family and invoice up to absolute constants. Additional
levels carry at least the factor shown in (N8). We do not assert that
this lower bound is sharp as a function of every individual d_i or ell.

## 6. Global consequence and the next useful question

With the current expanded finite-data bound `P_m<=2^(m^C)`, the complete
profile still has `log2 D_J, log2 L(N_J)<=2^(O(J^3 log J))`, giving the
previously accepted envelope

    H(n)<=2^(O(s (log2 log2 s/log2 s)^(1/3))),
    s=log2(1+log2 n).

Theorem N does **not** lower-bound the true finite-data costs or H(n).
It says that improving that envelope through a smaller arity while keeping
this exact normalized pencil invoice cannot be achieved by exact-rank
recalculation, asymmetric distance choices, or deeper copies of the same
label mechanism. A structured executor could improve finite-data costs at
the same arity and is outside this obstruction. A new rectangle mechanism,
new Gram representation, or a proof charging fewer endpoint conversions is
also outside its scope.

### Open next questions

1. Can one execute structured predictor and repair tensors while charging
   polynomial-in-m work per physical volume and preserving the full-rate
   row interface? Route B is pursuing this separate mechanism.
2. Can the literal endpoint-conversion charge D(1+lambda) be reduced by
   sharing successive endpoint changes, without moving the cost to scalar
   scans or introducing extra recursive calls?
3. Can a different rectangle partition preserve the same k=0/d endpoint
   geometry while reducing the exact incidence in (N1)? Theorem N assumes
   this specific first-differing-bit product partition.

Credits: the OpenAI tape and Fourier constructions and their cited
intersection/rectangle predecessors; S002 characteristic-two label
construction; independently convergent S003 Route C rank work;
Jerry Chen (@CubeJerry); AI-assisted proof and quantitative extension.
