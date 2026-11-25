# An explicit all-arity profile for the characteristic-two labels

Status: **proved quantitative parameter lemma; independent review pending**.
This makes the previously established all-arity asymptotic label profile
fully discrete, with an effective sufficient guard. It is an enabling
quantification of retained mathematics, not a new multiplier theorem.

Sources: S002 `routes/B/characteristic-two-label-geometry.md`, C2.5--C2.11,
OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`; S003 explicit
dyadic geometry at programme
`c65aac1156a46d10c0ef2aa36fd846c7a93518e1`. The latter uses the same
scalar label matrix and rectangles, with ambient dimension
`D=2(2+h q^h)` and fixed address radix3. These label parameters are
distinct from that address radix.

## 1. Integer-only choice for every sufficiently large m

For an integer m>=2 put

    x=ceil(log2 m),          v=ceil(log2(x+2)).

Choose d as the least power of two, at least2, satisfying

    d^3 v >= x.

Then set

    t=2+ceil(x/d^2),   q=2^t,   h=2d-1,
    N=q^(h^2),        D=2(2+h q^h),
    Lambda=binom(h,d)^(d+1) (q-1)^d t^(d(d-1)).        (A1)

All choices use integer bit lengths, powers and comparisons. No real
root/logarithm oracle or j-dependent finite search is required. Lambda
is the source incidence upper bound, not a claim that every label has
that exact incidence.

**Theorem A.** For every m with `x>=2^40`, the family satisfies

    m r*/N <= 1/4,                                    (A2)
    N <= m^5,                D <= sqrt(m),             (A3)
    log2[D(1+Lambda)] <= 64 x^(2/3) v^(1/3).           (A4)

Consequently a completed shared-pencil/repair implementation whose
additional expense is an absolute factor C_geom has

    normalized spatial-call coefficient
      <= C_geom sqrt(m) 2^[64 x^(2/3) v^(1/3)],         (A5)

including occupied reserves after increasing C_geom by an absolute
factor. It has arity `m+2(D-2)<=2m` on this guard. Actual nonrecursive
physical work, encoding and space still need their separate suppliers.

The cutoff is deliberately very conservative and not claimed practical.
The statement covers every large admissible m, not only a trial
subsequence selected for a fixed inverse exponent J.

## 2. Rank and dimensions

The retained rank theorem gives

    r*/N <= 2^(2d^2-2) q^(-d^2).

Since `t d^2>=2d^2+x` and `m<=2^x`, multiplying gives A2.
Put `y=(x/v)^(1/3)`. On the stated guard y>2 and minimality gives

    y<=d<2y,       t<=3+x/d^2.                         (A6)

Thus

    log2 N=h^2 t <=4d^2(3+x/d^2)=4x+12d^2
             <4x+48x^(2/3) v^(-2/3).                 (A7)

For x>=2^40 the last added term is at most x/2, and
`(9/2)x<=5(x-1)`. Since `log2 m>x-1`, A3's label-count bound follows.

Because h>=3 and t>=2, `D=4+2h2^(ht)<=4h2^(ht)`, whence

    log2 D <=2+log2 h+h t
             <=3+log2 d+6d+2x/d.                      (A8)

For x>=2^40, `v<=x^(1/4)`: if `k=floor(log2 x)>=40`, then
`v<=k+2<=2^(k/4)<=x^(1/4)`. The middle inequality holds at k=40 and
persists because its exponential multiplier exceeds the successive
linear ratio. Therefore d>=y>=x^(1/4), while d<2x^(1/3). Substitution
into A8 gives

    log2 D <=3+2x^(1/3)+12x^(1/3)+2x^(3/4)
             <=4x^(3/4) <=(x-1)/2.

The last two elementary inequalities hold throughout the stated guard.
This proves `D<=sqrt(m)` and hence `m+2(D-2)<=2m` for m>=4.

## 3. The incidence envelope with absolute constants

Use `binom(h,d)<=2^h`, `log2(q-1)<=t`, and
`log2 t<=log2(x+3)<=v+1`. Then

    log2 Lambda
      <=h(d+1)+dt+d(d-1)log2 t
      <=d^2(v+4)+3d+x/d.                              (A9)

Lambda>=1, so A8--A9 imply

    log2[D(1+Lambda)]
      <=4+log2 d+9d+3x/d+d^2(v+4).                   (A10)

Let Phi=x^(2/3)v^(1/3). Since v>=4 and A6 holds,

    d^2(v+4)<=8 Phi,   3x/d<=3 Phi,
    9d<=18 Phi,       4+log2 d<=6 Phi.

Thus A10 is at most35 Phi, and the stated64 Phi leaves ample slack.
All estimates use absolute constants, and every integer rounding has
already been charged. This proves A4.

For A5, the retained complete finite repair uses O(sqrt(m)) predictor
stages times the shared-pencil factor plus O(sqrt(m)) finite-leaf calls.
The PS schedule changes the endpoint constant only absolutely. Its
`m r*/N` factor is at most1/4 by A2. The occupied-reserve contribution
is O(D), which is at most the right side of A5 after one absolute
enlargement. Therefore the entire normalized spatial coefficient has
the asserted form. This conclusion still imports the finite algebraic
correctness and compact execution interfaces explicitly listed above.

## 4. How this lemma is used, and what it does not prove

A variable spatial arity may choose an odd m near e^beta and then use
A1 directly. All sufficiently large choices satisfy the same guards.
The logarithmic child-call loss is

    O((log m)^(2/3)(log log(m+2))^(1/3)),

with an effective discrete constructor. It is unnecessary to substitute a
growing j into an unquantified fixed-j statement. Fixed small m or active
widths may use the explicit direct branch.

The rule does not bound the physical per-volume coefficient by itself,
does not remove leading-batch width, and does not prove a common visited-
space cap. Those remain the actual compact-processor, packing and stack
obligations. It supplies neither a global lower bound nor an endpoint.

Open next question: insert A1 into the jointly charged nonstationary
interchange recurrence with its actual finite description and primitive
cost exponents. The binary Walsh branch has a different label profile
and should retain a different arity schedule.

Credits: @CubeJerry; the source/S002 characteristic-two labels; S003's
fixed-radix realization; substantial AI-assisted E003 discrete
quantification. The O(Phi) asymptotic scale is recovered predecessor
mathematics, with its constants, guards and all-arity application made
explicit here.
