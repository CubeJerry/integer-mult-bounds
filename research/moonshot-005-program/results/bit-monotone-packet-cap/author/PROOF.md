# At most ten monotone whole-record packets in the retained target envelope

**New scoped analytic theorem; independent review pending. No new kappa.**

## 1. Exact statement

Use the programme's actual111-root BIT interface and the retained paired
fixed-even-m caller. Every original X carrier ascends from its rank1 root
to rank8 Hub; every original Y ascends from0 to its rank7 terminal facet.
There are q whole-V packet lifetimes descending from Hub to0, counted by
physical carriers. All paths are monotone, but jumps of any positive rank
are permitted. Local mixing may be arbitrary; final carrier identities and
whole-record cost units are those of the admitted source contract. Additional
paid transfers only strengthen the lower bound.

For every fixed even integer m>=2 and every k in[1/200,1], q>=11 fails the
retained complete signed-moment test at t=1-k. Thus any source admitted by
that test in this route model has q<=10. Together with the existing physical
downset theorem q>=8, its possible packet counts are8,9,10.

This is not a lower bound on general multiplication algorithms. It does not
exclude a changed caller, altered carrier interface, fractional-volume cost
model or a source outside the stated monotone whole-record assumptions.
It does not assert that any of the three surviving counts is realizable.

## 2. Lower bound valid for arbitrary monotone jumps

For 0<t<=1, positive a,b obey (a+b)^t<=a^t+b^t. Applying this repeatedly to
the rank increments of an ascending original path gives cost>=7^t; each
descending packet has cost>=8^t. At t=0 every path has at least one positive
MOVE, so the same inequality holds with r^0=1. Therefore every actual profile
Q satisfies

    Q_t >= 222*7^t + q*8^t.                              (1)

Unit splitting is NOT assumed. The right side optimistically gives each
original and packet one full jump and ignores all other positive expenses.
It need not be a realizable interacting source.

## 3. Complete caller allowance and cancellation

The pinned prior source receipt is
`results/bit-eight-packet-target/author/RESULT.json`, SHA256
`f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2`.
It records the admitted native and exact paired profiles:

    N={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10},
    H={2:1,4:25,6:1,8:410},
    P2=36N+444[1]+444*sum(j=1..8)[7j],
    T2=36H+222[127]+444*sum(j=1..9)[1+7j].

For an actual replacement profile Q, retained complete accounting is

    P_m=(m/2)P2-18(m-1)N+18(m-1)Q,
    T_m=(m/2)T2-18(m-1)H.

Divide (T_m-P_m)_t by the positive18(m-1). Positivity requires Q_t<B_m(t),
where, writing S=(T2-P2)_t/36,

    B_m(t)=B_inf(t)+S(t)/(m-1),
    B_inf(t)=N_t-H_t+S(t).

Native terms cancel exactly from B_inf:

    B_inf(t)=(37/6)*127^t
             +(37/3)*(64^t-1
                 +sum(j=1..8)((7j+1)^t-(7j)^t)).          (2)

This formula uses the actual retained caller, not a local substitute invoice.

## 4. Monotonicity extends exact endpoint signs to the whole target range

Let Phi(t)=B_inf(t)/7^t. In (2), after dividing by7^t, the first term is
(37/6)(127/7)^t. The other terms are

    (37/3)*((64/7)^t-(1/7)^t
              +sum(j=1..8)((j+1/7)^t-j^t)).

Every displayed difference has positive derivative for t>=0: the first
has one base>1 and one<1; for j>=1, x^t log x is strictly increasing in
x>=1. Also127/7>16 and log2>1/2, so on0<=t<=1

    Phi'(t) > (37/6)*log(127/7) > 37/3.

Define R_11(t)=Phi(t)-222-11(8/7)^t. Using log(1+u)<u and t<=1,

    R_11'(t) > 37/3 - 11*(8/7)*(1/7)
              =37/3-88/49 >0.                            (3)

For the finite-m correction, the exact signed profile is

    H-N=-1386[1]-1252[2]-62[3]-22[4]-9[5]
        -103[6]-10[7]+410[8].

After division by7^t, every negative coefficient has base<=1 and hence
nonnegative derivative; the positive8/7 term has positive derivative.
Since S/7^t=Phi+(H-N)_t/7^t, it too is strictly increasing on[0,1].

At t*=199/200, the exact outward rational intervals in RESULT.json prove

    S(t*)=-12.335089345342768... <0,
    B_inf(t*)-222*7^t*-11*8^t*=-4.292499775590789... <0.

The decimal displays are not the certificate. Equation(3) and the preceding
monotonicity imply both strict negative signs throughout0<=t<=t*. Thus

    B_m(t)<B_inf(t)<222*7^t+11*8^t <= Q_t

for every m>1 and q>=11. This contradicts the retained positivity condition
and proves the theorem for all stated k,m. In particular, increasing a fixed
m cannot rescue q11, and using nonunit jumps cannot rescue it either.

## 5. Exact checks and negative controls

The accompanying arithmetic checker verifies both paired profile
identities, the native cancellation and every coefficient sign used above.
For each required integer r it brackets r^(199/200) by rational endpoints
on a1e-30 grid and verifies their200th powers using integers. Signed interval
arithmetic proves the strict endpoint signs. No floating decision is used.

At the target endpoint the optimistic limiting q10 margin is positive
3.624753475730866..., so this argument does not overclaim q<=9. At t=1,
the q11 limiting margin is positive; that control prevents extending the
target interval without the monotonicity endpoint premise. Extra whole
records, ordinary work, owned storage/erasure and compiler services have all
been granted zero cost here. Charging them cannot reverse this exclusion.

## 6. Composition with receiver-downset constraints

Subject to separate admission of the new receiver-downset theorem, a scalar
history W containing the class code U and contained in U+C, with h extra
canonical quotient dimensions, requires q>=16-2^h. The packet cap then
excludes h=0,1,2 (q>=15,14,12), even for arbitrary monotone jumps. Therefore
this scalar canonical-extension family needs h>=3, or dim W>=18, before
physical construction can be attempted. The same applies to a fixed scalar
code tensored across V; it is not an18V theorem for arbitrary non-tensor
operator-valued extensions. No such construction is supplied by this proof.

Credit @CubeJerry, retained paired/native authors and prior q8 budget and
physical-cut work. The new contribution is arbitrary-jump packet exclusion
over the entire target-exponent interval, with an elementary normalized
monotonicity proof. Prepared with substantial OpenAI assistance. Both strict
suppliers and all five foundational assumptions remain open.
