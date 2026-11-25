# The symmetric characteristic-two label invoice has the cubic-logarithmic scale

Status: **proved within the explicitly specified label and rectangle-invoice
model; awaiting independent review**. This is not a lower bound for general
interchange algorithms, compressed executors, or integer multiplication.

Session: S003, 26 November 2026 (Australia/Melbourne). Programme source:
`0607d044d1d09489580da0e5828588820e1a6775`. The construction audited here is
`routes/B/characteristic-two-label-geometry.md`, Sections 1--4, and the
completed invoice is `routes/A/fixed-field-extraction-theorem.md`, Q2--Q7.
The underlying directed-rectangle source is OpenAI
`math@3344da59991ed94f9ba711217b29c1d760badfa6`, November tape paper,
`build/interchange.tex`.

All logarithms are binary. Let `d>=2` be a power of two, `h=2d-1`,
`q=2^t` with integer `t>=1`, `U=[q]^h`, `n0=q^h`, and `V=U^h`,
`N=n0^h`. Let `B=P0` be the binary matrix on `U` marking inner Hamming
distance zero or `d`. Let `P*` mark equality or exactly `d` differing outer
coordinates, with inner distance `d` in each differing coordinate. These
are exactly the source-specific matrices; no alternate rank factorization
or rectangle cover is built into the statement.

The prescribed directed rectangles have one fixed ordered pair at the
first differing inner coordinate and the first-differing-bit partition at
the other `d-1` coordinates. Denote the number containing a fixed label on
one prescribed side by `lambda`. The source pencil upper invoice includes
`D_route(1+lambda)(1+m rank(P*)/N)`. We study its optimistic subinvoice
`sqrt(m) lambda`, under the source occupancy choice

    m rank_F2(P*) / N <= 1.                                  (L0)

The occurrence count is charged as separate endpoint work in this invoice.
A new executor which provably shares those occurrences can leave this
model; the theorem does not price such sharing.

## 1. A nilpotent tensor form of both selector matrices

Let `J` be the `q`-by-`q` all-ones matrix and `I` the identity. The inner
selector from the source is

    B = sum_{S subset [h], |S|<d}
          tensor_i ((I+J) if i in S else J)      over F2.    (L1)

For a fixed subset `T` of positions at which the expanded term uses `I`,
of size `a<d`, its coefficient is

    c_a = sum_{s=a}^{d-1} binom(h-a,s-a)
        = binom(h-a-1,d-a-1) mod 2.                        (L2)

The second equality follows by taking a coefficient in
`(1+z)^(h-a)/(1+z)` in `F2[[z]]`. Put `b=d-a-1`.
For `1<=b<d`,

    (1+z)^(d-1+b) = (1+z^d)(1+z)^(b-1),

because `d` is a power of two; its coefficient of `z^b` is zero.
For `b=0` that coefficient is one. Thus only `a=d-1` survives in (L1):

    B = sum_{|T|=d-1} I_T tensor J_[h]\T
      = e_d(J_1,...,J_h),                                  (L3)

where `J_i` acts by `J` on tensor coordinate `i` and by the identity on
the others. Since `q` is even, `J^2=0`. The tensor operators commute, so
each summand of (L3) squares to zero and characteristic two removes all
cross terms. Therefore

    B^2=0,             rank(B)<=n0/2.                       (L4)

The outer construction uses entrywise products `B` and `B+I`: the latter
is `B` restricted to distinct inner labels, because every diagonal entry
of `B` is one. Its identical expansion gives

    P* = sum_{|S|<d} tensor_i ((B+I) if i in S else B)
       = e_d(B_1,...,B_h).                                 (L5)

These are matrix identities, not merely ranks or identities on sampled
labels. The power-of-two hypothesis on `d` is essential.

## 2. A lower rank witness, without an exact rank formula

Restrict `B` to words whose last `d` inner coordinates have a prescribed
value. The other `d-1` coordinates vary arbitrarily. Two distinct such
words have distance between one and `d-1`; hence this principal submatrix
is the identity of order `q^(d-1)`. Consequently, writing `r=rank(B)`,

    r >= q^(d-1),             r/n0 >= q^(-d).              (L6)

Choose a complement `A` of `ker(B)` in the `n0`-dimensional vector space.
Then `dim(A)=r`, and `B|A` is an isomorphism onto `im(B)`. In the first
`d` outer tensor coordinates restrict inputs to `A`; in the remaining
`d-1` coordinates restrict inputs to `ker(B)`. In the sum (L5), every
term except the one applying `B` to exactly the first `d` coordinates
vanishes on this subspace. The surviving tensor map is injective. Thus

    rank(P*) >= r^d (n0-r)^(d-1).                          (L7)

Using (L4) and (L6) gives the useful uniform lower bound

    rank(P*)/N >= 2^(-(d-1)) q^(-d^2).                    (L8)

It follows from the actual occupancy requirement (L0), rather than merely
the source's sufficient rank upper bound, that

    x := log m <= d-1 + d^2 t.                            (L9)

The source upper bound has the same `q^(-d^2)` exponent. Improving only
its prefactor cannot remove the parameter constraint driving the result
below.

## 3. The source rectangle incidence is an exact count

For a prescribed inner word on a prescribed side, choose the `d`
differing coordinates in `binom(h,d)` ways. At the first one, the word's
letter is fixed and its opposite-side letter has `q-1` choices. At each
of the other `d-1` differing coordinates, the first-differing-bit partition
has exactly one rectangle containing the word for each of the `t` possible
first differing bit positions. Coordinates outside the differing set are
forced. Hence the inner prescribed-side incidence is exactly

    lambda0 = binom(h,d) (q-1) t^(d-1).

The outer construction chooses `d` varying outer positions, fixes every
other inner word, and chooses one of those inner directed rectangles at
each varying position. All these choices label actual directed rectangles
of the retained source construction. Therefore the occurrence count is
exactly

    lambda = binom(h,d) lambda0^d
           = binom(h,d)^(d+1) (q-1)^d t^(d(d-1)).        (L10)

Counting both prescribed sides would change this by a fixed factor. It is
the construction's incidence, not a claimed optimum over all rectangle
covers. Distinct source rectangles sharing one endpoint set still count
separately in this literal invoice.

Choosing one item from each of `d-1` pairs, together with one additional
item, proves `binom(2d-1,d)>=2^(d-1)`. Also `2^t-1>=2^(t-1)`. Thus

    log lambda >= d^2-1+d(t-1)+d(d-1) log t
               >= (dt+d^2 log(t+1))/2.                    (L11)

For the last inequality use `log(t+1)<=1+log t`. The remaining constant
part is at least `(d-2)(d+1)/2>=0`, and the coefficient of `log t` is
`d(d-2)/2>=0`. This includes `d=2,t=1`.

## 4. An explicit lower bound for the optimized invoice

**Theorem L.** For every real `m>=4`, every power of two `d>=2`, and every
integer `t>=1` satisfying the exact occupied-label condition (L0),

    log lambda >= (1/12) x^(2/3) (log x)^(1/3),
    x=log m.                                               (L12)

**Proof.** If `d>x/2`, (L11) gives `log lambda>=d^2/2>x^2/8`, which is
at least the right side of (L12) for `x>=2`.

Otherwise (L9) gives `d^2 t>=x/2`. Put

    T = x^(1/3) (log x)^(2/3).

If `t>=T`, then

    dt >= sqrt(xt/2) >= 2^(-1/2) x^(2/3)(log x)^(1/3),

and (L11) is stronger than (L12). If `t<=T`, the function
`log(1+t)/t` is decreasing on positive reals. Therefore

    d^2 log(t+1)
       >= (x/2) log(t+1)/t
       >= (x/2) log(T+1)/T
       >= (x/6) log(x)/T
        = (1/6) x^(2/3)(log x)^(1/3).

Here `log(T+1)>=log(x)/3` because `x>=2`. Apply (L11). QED.

The known source upper construction chooses a power-of-two distance within
a constant factor of `(x/log x)^(1/3)` and obtains the matching upper scale
`log lambda=O(x^(2/3)(log x)^(1/3))`. Thus this scale is sharp for the
specified symmetric label/rectangle invoice and occupancy regime.

## 5. Consequence for the cubic-logarithmic parameter search

Suppose even the optimistic retained invoice, omitting the positive
`D_route` and all other costs, were to satisfy

    sqrt(m) lambda <= m^(1/2+1/J).                        (L13)

Combining (L12) with (L13) gives

    x >= (J^3/1728) log x.                               (L14)

In particular `x=Omega(J^3 log J)` as `J` grows. Fixed multiplicative
constants in (L13) do not change this asymptotic conclusion. The current
accepted sufficient parameter choice `log m=O(J^3 log J)` is therefore
optimal in order within this specified invoice. This is a new limitation
of a retained method, not an additional hypothesis for its upper theorem.

The statement does **not** infer that an actual implementation must spend
`lambda` steps per datum. The lower bound is on the explicit charged
incidence formula: a proof exploiting a different cover, shared endpoint
execution, a different number of label levels, asymmetric parameters,
another occupancy regime, or a different recurrence must be assessed on
its own complete cost model. Nor does (L14) lower-bound candidate generation,
the true residual overhead `H(n)`, or general integer multiplication.

## 6. Audit implications and open next questions

1. Sharper rank estimates or smaller absolute constants alone do not
   improve the cubic-logarithmic parameter scale of the symmetric family.
2. The protected compact-executor route remains viable because it asks
   whether the literal endpoint incidence can be shared physically; this
   theorem does not charge that hypothetical executor.
3. Asymmetric or deeper label constructions can change (L9)--(L10). The
   first discriminating test is to derive their **actual** rank lower
   witness and exact per-label occurrence count, then optimize the joint
   invoice before constructing a large finite template.
4. Exact ranks of the nilpotent selector matrices may sharpen constants.
   They cannot improve the exponent of `q` used here without invalidating
   the proved tensor restriction (L7).

Verification is provided by `verify_symmetric_label_obstruction.py` and its
saved JSON output. The tests exercise exact binary matrix identities,
principal rank witnesses, outer selectors and rectangle incidence, with
negative controls. The unbounded theorem is the argument above; finite
tests do not replace it. No Lean build, complete multiplier execution, or
human refereeing is claimed.

Credits: the OpenAI source rectangle geometry and preceding S002
characteristic-two construction; Jerry Chen (@CubeJerry); AI-assisted
adversarial derivation in S003. The nilpotent tensor expansion, lower-rank
witness and optimized invoice obstruction are the additions of this note.
