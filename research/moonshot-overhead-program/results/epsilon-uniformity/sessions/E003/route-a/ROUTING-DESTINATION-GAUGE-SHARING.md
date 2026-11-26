# Sharing one destination transform across all free rectangles

Status: **proved source-compatible call-invoice refinement; independent
review pending**. This changes the literal free-rectangle invoice, while
retaining its optimized leading logarithmic loss. It does not improve the
complete multiplication bound.

Sources: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier
`build/kernel.tex` (complete endpoint subsection and binary labels) and
`build/binary.tex`; E003 `RATIONAL-WALSH-CONSTANT-SPACE.md` and the lead's
`../lead/binary-walsh-label-invoice-barrier.md`. These were read in full.
The new gauge factorization and rank-weighted count are derived here.

## 1. A full transform after a partial transform

Let K be a d-dimensional nondegenerate paired space over F_2, and V any
v-dimensional subspace, possibly with degenerate restricted pairing.
A partial-Fourier basis consists of characters on affine cosets of V.
Full normalized Fourier sends each such vector to a character supported
on an affine coset of V^perp. Indeed,

    sum_(z in V) (-1)^(xi(z)+<z,y>)

vanishes unless the restriction of y to V equals xi, and is |V| on
that coset. Its dimension is d-v. Consequently full Fourier composed
with an inverse partial Fourier along V is a partial Fourier of
dimension d-v, together with coordinate changes and signs. This is an
exact equality of normalized maps.

Binary elimination constructs the bases and complements. No orthogonal
direct-sum decomposition V plus V^perp is assumed; that would fail for
degenerate V. For the source's paired two-half kernel, the residual uses
2(d-v) one-axis calls.

## 2. One common destination transform

For a free rectangle I x J put H=span{d_w:w in J} and r=dim H. Its first
endpoint uses 2r calls because H is auxiliary at every source. Its last
endpoint runs along V=H^perp at destination w. This V lies in the
nondegenerate space K_w=d_w^perp, of dimension D-1, and has dimension
D-r. The original last endpoint costs 2(D-r) calls.

Choose a fixed full auxiliary endpoint E_w: normalized paired full
Fourier on K_w, followed by the auxiliary part of the source's final
quadratic phase. It acts on the D-1 original auxiliary axes and is
independent of j and of the rectangle.

The source puts the distinguished final phase into the middle, where it
is constant on the V-cosets. Changes of representatives are also middle
coordinate/sign maps. After separating those specified monomial maps,
the original last endpoint is inverse partial Fourier along V followed
by that same auxiliary final phase. In E_w^(-1) times this endpoint the
phases cancel. Section 1 leaves an exact residual R_(w,J) such that

    original last endpoint = E_w R_(w,J),             (D1)
    residual call count = 2[(D-1)-(D-r)] = 2(r-1).      (D2)

The complementary subspace inside K_w is H intersection d_w^perp; it
has dimension r-1 because H contains the norm-one vector d_w. It need
not be nondegenerate. The character/coset construction proves D1 in
that case as well; an orthogonal-basis argument would be insufficient.

Process each rectangle in the original query-sharing order, replacing
its last endpoint by R_(w,J). Accumulate all free contributions in one
destination collection in the common E_w^(-1) coordinates. After all
free rectangles, apply E_w once. Row matrices commute with these
transforms. Charged and ordinary pointwise contributions are accumulated
separately in ordinary coordinates and added after E_w. Thus no large
per-query or per-charged-rectangle transform is hidden in this change.

The executor uses only a constant number of extra arrays, with sequential
rectangle scratch and fixed marked regions as in RW. It preserves the
independent input-row count and every complete spectator range. Zeroed
accumulators are workspace, not additional independent inputs. Bases,
monomial changes and finite descriptions retain polynomial-m bounds;
completed calls remain unitary. The existing physical-time and precision
allowances still apply. No smaller middle-routing toll is asserted.

## 3. Exact ranks and incidence-weighted calls

Write q=2^t, t>=1, L>=2. The exact binary Gram dimension is
D=2+L(q-2). A canonical free rectangle has an odd set U of unequal
positions. At i in U both letter sets have size s_i=2^(t-b_i), with
b_i in {1,...,t}; other letters are fixed. Every letter set is proper,
and the two rectangle sides have equal cardinality.

**Lemma D3.** The destination span has dimension

    r = 1+sum_(i in U)(s_i-1).                         (D3)

Fix one w_0 in J. Coordinate-i differences give functions
`1_(v_i=a)+1_(v_i=(w_0)_i)` spanning dimension s_i-1. A sum of functions
on separate coordinates vanishes identically only if each is constant.
Proper letter sets force these constants to be zero, so the difference
spaces are independent. Every difference d_w+d_(w_0) has self-pairing
zero, whereas d_(w_0) has self-pairing one. Self-pairing is a linear
functional in characteristic two, so the base vector adds one dimension.

For one label on either side, let lambda count its free incidences and
mu sum their ranks r. The exact first-difference partition gives

    lambda(t) = sum_(j odd) binom(L,j)t^j
              = [(1+t)^L-(1-t)^L]/2,
    mu(t) = lambda(t)+(q-1-t) lambda'(t).              (D4)

Here `sum_(b=1)^t(2^(t-b)-1)=q-1-t`; summing one size term from D3
over all incidences gives the derivative. All odd-distance weights are
nonzero over the characteristic-zero numerical field.

The old free call count was 2D lambda per label row, since equal side
sizes cancel the endpoint ranks r and D-r. The new count is exactly

    F_new = 2mu+2(mu-lambda)+2(D-1)
          = 4mu-2lambda+2(D-1).                      (D5)

For t>=2L, D5 is Theta(D lambda/t) with absolute constants. The highest
odd term of lambda has degree h in {L-1,L}, and consecutive lower terms
have ratio at most L^2/t^2<=1/4. Thus lambda'/lambda=Theta(L/t).
Also q-1-t=Theta(q), D=Theta(Lq), and lambda>=Lt absorbs the common D
term. This saves a factor Theta(t) in that regime, which includes the
eventual optimized labels. The polynomial-arity physical toll remains.

## 4. A fresh lower bound for the changed positive invoice

Put x=log2 m and s=floor(L/2). The charged label polynomial has nonzero
highest Newton coefficient 2^(-s), so its binom(L,s) q^s rectangles are
present. Define a positive subinvoice

    J_new = D+mu+m D binom(L,s) q^(-ceil(L/2)).         (D6)

The full call invoice dominates this up to an absolute constant; indeed
D5>=D+2mu for D>=2, and the retained charged term is present. This is
a statement about a specified positive cost certificate, not runtime.

**Theorem D4.** Uniformly for L>=2, t>=1 and m>=2^16,

    log2 J_new >= (1/4)sqrt(x log2 x)-2.               (D7)

If t=1, choosing one element from each of s disjoint pairs proves
`binom(L,s)>=2^s`. Since D=2, the charged term is at least m. If L=2,
it is `(4-4/q)m>=2m`. Both cases satisfy D7.

Otherwise t>=2 and L>=3. Put u=L-2 and b=log2 J_new. We have
`q-1-t>=q/4` and `lambda'(t)>=L(1+t)^(L-2)`. For odd L the latter
follows from the sum in the derivative; for even L use
`(1+t)^(L-1)-(t-1)^(L-1)>=2(1+t)^(L-2)`. Thus

    b+2 >= t+u log2(t+1).                              (D8)

Since D>=q and `ceil(L/2)-1<=u`, the charged term also gives

    b >= x-u t.                                       (D9)

Set B=b+2. If B>=x/2, D7 follows for x>=16. Otherwise ut>x/2, and
`B>=t+[x/(2t)]log2(t+1)`. If t<=sqrt(x), decreasing
`log2(t+1)/t` gives `B>=(sqrt(x)/4)log2 x`, which suffices. If
t>=sqrt(x), AM--GM gives `B>=t+x log2 x/(4t)>=sqrt(x log2 x)`.
This proves D7 without reversing an upper bound.

For the upper comparison, every incidence has r<=D, so mu<=D lambda.
The new complete invoice is at most an absolute multiple of the old
one, with the same charged part. The previous optimized labels still
give `log(invoice)=O(sqrt(x log(x+2)))`. Hence the optimized leading
scale is unchanged. The old literal-invoice lower bound was not assumed
to apply automatically after the schedule changed.

## 5. Evidence, limits and next questions

The verifier `ROUTING-verify-destination-gauge.py` checks the normalized
partial/full complement identity including degenerate subspaces,
canonical ranks, weighted incidences, endpoint counts and integer
inequalities used above. Its receipt states finite scope. No physical
tape timing or complete multiplier is executed.

This schedule shares one endpoint across all free rectangles and leaves
smaller residual transforms on each. Further progress could share those
residual transforms or coordinate changes, or change the labels. A
one-gauge scheme eliminating every residual transform is a stronger
claim, addressed separately by the triangle obstruction. The positive
polynomial-arity routing toll also remains unresolved.

Credits: @CubeJerry; pinned OpenAI endpoint factorization and normalized
binary construction; E003 RW, lead exact Gram/invoice and two-scale work;
substantial ChatGPT assistance. No new programme best, runtime lower
bound, formal verification, human refereeing or exhaustive novelty result
is claimed.
