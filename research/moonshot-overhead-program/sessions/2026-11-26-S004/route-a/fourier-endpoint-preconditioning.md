# Preconditioning Fourier endpoints changes incidence to a span-weighted bill

Status: **proved local algebra/call-invoice component; independent review
requested**. This improves a literal local invoice and supplies another
geometry target. Its first-difference specialization saves one logarithmic
factor locally, but does not improve the complete asymptotic envelope.

Source: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, full Fourier
`build/kernel.tex`, the arbitrary-subspace endpoint factorization and the
shared-query argument. The tape compilation uses the admitted E002
polynomial coordinate-map and rational numerical suppliers. Characteristic
two below describes address-direction spaces; data are rational numerical
records, as in the binary Walsh branch.

## 1. A full transform can supply many partial transforms

Let A be a d-dimensional binary vector space. Fix one coordinate basis
and its dual. For any h-dimensional subspace H, choose a complement C
and coordinates A=H direct-sum C. A normalized Fourier transform in the
fixed full coordinates, followed by a dual linear reindexing and an
inverse Fourier transform on the d-h complementary frequency coordinates,
gives the partial normalized Fourier transform along H. The other
coordinates return as ordinary coset coordinates.

Indeed, in adapted coordinates the unnormalized identity is

    2^(-(d-h)) sum_(eta in C*) (-1)^(c dot eta)
      sum_(h',c') (-1)^(xi dot h'+eta dot c') x(h',c')
       = sum_(h') (-1)^(xi dot h') x(h',c).

Normalized versions have exactly the same identity, with unitary full and
partial maps. It holds for every subspace, regardless of whether the
restriction of any ambient pairing to H is degenerate. Address basis
changes and frequency dual changes are ordinary linear permutations.

Consequently a full d-axis transform can be prepared once and reused to
supply many requested H transforms, paying only d-h inverse axis calls
for each request, in addition to its charged coordinate maps and copies.

## 2. Apply this to a free rectangle

Let I x J be any free rectangle in the source label geometry. Write
D for the nondegenerate binary direction-space dimension and
r_I=dim span{d_v:v in I}. The cross pairing is zero. The source endpoint
proof works for any H satisfying

    span(J) subset H subset span(I)^perp,

not just its displayed choice H=span(J). Take

    H=span(I)^perp,   dim H=D-r_I.

At a source v, H lies in d_v^perp, whose dimension is D-1. The source
partial transform therefore follows from one full auxiliary transform
by inverse-transforming only r_I-1 auxiliary directions. At a destination
w, the final transform runs along H^perp=span(I), of dimension r_I,
and lies in d_w^perp.

Perform the source's auxiliary initial phase once, followed by the full
auxiliary Fourier transforms on both halves, at each input label. This
phase and these full transforms are independent of the query j and of the
rectangle. Keep the original input for the charged term. For each rectangle,
copy its preconditioned source arrays, use the preceding inverse partial
transforms and coordinate maps, then run the source's ordinary middle
maps and row mixing. Accumulate across all queries before the destination
partial transforms, exactly as in the original shared-query proof.

All diagonal phases depending on the distinguished query coordinates remain
in the original middle maps. The source auxiliary phase is independent of
j because distinguished and auxiliary directions are orthogonal in the
fixed label basis; changing the rectangle basis only reexpresses this same
operation. No spectral mask is moved across an unperformed converter.

For N labels, define the actual span-weighted incidence

    K(I,J list)=(1/N) sum_R [ (r_(I_R)-1)|I_R| + r_(I_R)|J_R| ].  (EP1)

**Lemma EP1.** The free-rectangle endpoint axis-call bill per row is at most

    2(D-1)+2K,                                             (EP2)

plus the same polynomially many ordinary coordinate/scalar operations.
The charged common-query term is unchanged. Thus a complete pencil has
sufficient call bill

    O(D+K+m D N_ch/N).                                    (EP3)

Weighted rectangle coefficients do not change the number of axis calls.
The usual rational-height and norm-gain costs still count their magnitudes.

This is a genuine change to the source execution, not a reinterpretation of
its old D times maximum-load bound. It can help rectangles whose source
span is much smaller than the ambient direction space.

## 3. Physical interface

Each preconditioned full array is a constant extra copy of the original
volume. Subsequent source and destination arrays remain one per incidence,
with the same source row roles and labels. Coordinates are computed by
binary elimination and listed finite maps, polynomial in the local arity.
The new full transforms and inverse partial transforms are normalized
children in the same f-bit slots; for the source numerical template f is
even. Their coefficients are rational and completed maps are unitary.

All per-rectangle transformations still use only auxiliary fields at an
endpoint, so they remain shareable over j. Shared row matrices commute with
the spatial transforms as before. No per-query repeated full auxiliary
transform has been introduced. Grouping these calls within a label retains
the original actual child-volume interface. The additional global full
transforms and constant copies fit the existing polynomial ordinary bill,
incidence storage, numerical event-count bound and precision proof.

This component does not by itself supply a global common visited-space
cap or a faster multiplying machine; it can be inserted in the already
charged template grammar with the changed call coefficient EP2.

## 4. Exact bill for literal first-difference rectangles

Take even L, q=2^t, and the source exact odd-distance product partition.
For each coordinate in an unequal set S, a fixed label sees one interval
side of size 2^s for each s=0,...,t-1. Equal coordinates are singletons.
For a product side A with coordinate sizes a_i, the Gram quotient has

    dim span{d_v:v in A}=1+sum_i(a_i-1).                    (EP4)

Here every a_i<q. To prove equality, the affine differences in each
coordinate have their one-hot support inside a proper alphabet subset.
The only radical relations in the full additive-coordinate realization
are coordinatewise constant vectors with zero total. Such a relation
supported in a proper subset is zero in each coordinate. The differences
are therefore independent. Their self-pairing is zero, whereas d_v has
self-pairing one, so the base vector is independent as well.

Let

    lambda(t)=sum_(k odd) binom(L,k)t^k.

Every first-difference rectangle has equally sized sides. For a fixed label
on either side, the sum of (a_i-1) over one coordinate's t choices is

    sum_(s=0)^(t-1)(2^s-1)=q-1-t.

Summing EP1 over all odd unequal sets and all first-difference choices gives
exactly

    K=lambda(t)+2(q-1-t)lambda'(t).                        (EP5)

Thus the new free endpoint bill is

    2(D-1)+2lambda(t)+4(q-1-t)lambda'(t),
    D=2+L(q-2).                                           (EP6)

For example, q=4,L=4 gives D=10, lambda=40, lambda'=52 and K=144.
The old source endpoint invoice is 2D lambda=800 axis calls per row;
EP6 gives 306. This is a finite invoice calculation, not a full tape
runtime benchmark. At q=2 the formula correctly has q-1-t=0.

For growing q and L with t much larger than L,
lambda is of order L t^(L-1), whereas lambda' is of order
L(L-1)t^(L-2). EP6 therefore saves a factor of order t in the literal
free term, while changing its logarithm by only O(log t).

## 5. Why this alone does not remove the asymptotic Fourier logarithm

Even give the charged matrix its optimal rational rank rho. Consider the
improved homogeneous positive invoice

    C_new=D+K+m D rho/N.                                  (EP7)

It still obeys

    log2 C_new=Omega(sqrt(x log2 x)),  x=log2 m,             (EP8)

uniformly over all even L and powers q. This again is an invoice theorem,
not an algorithmic lower bound.

Here is a direct check. Write L=2r and b=log2 C_new. We have
b>=2r-1 from K>=lambda and b>=t from D>=q. For t>=2,
q-1-t>=q/4 and the k=L-1 derivative term give

    b>=t-1+(2r-2)log2 t.

The exact charged-rank lower bound in HF5 gives

    b>=x-(r-1)t-r.

If r=1, the last bound is at least x-1. Otherwise, if b<x/4,
r< x/8+1/2 and (r-1)t>=x/2 for all large x. Setting r'=r-1,
the same three-range argument as HF9, using t>=x/(2r'),
proves b>=c sqrt(x log x). If b>=x/4 the claim is immediate.
For t=1, rho/N is at least binom(2r,r)/2^(2r)>=1/(2r+1).
Together with b>=2r-1, the charged term rules out b<x/4 at large x.
The known constructive choice supplies the matching upper order.

Accordingly this preconditioning is a real local improvement and a useful
source-interface observation, but no log-free global envelope is claimed.
Further progress needs better span-weighted rectangle geometry or reuse
between these already-preconditioned partial transforms.

## 6. Exact finite checks

`verify_fourier_preconditioning.py` checks 153,896 exact partial-transform
identity entries across 320 basis/subspace cases, including 73 cases with
degenerate restricted pairing. Omitting the dual coordinate change rejects
45,961 entries; omitting the inverse normalization rejects 25,834.
The checker also verifies EP4 and EP5 on 8,408 product-side spans in seven
families. Its JSON receipt gives the exact old and new axis invoices.
All calculations use integers or exact rational numbers.

At L=2 a separate allowed family consists of one singleton-source star
per label in the odd-distance graph. Then r_I=1 and K=2(q-1), giving
free bill 2(D-1)+4(q-1). At q=4 this is 22, below the preconditioned
product bill 26 and the old product bill 48. This illustrates the changed
geometry objective; at fixed L it provides no asymptotic multiplier saving.
The tests concern finite identities and call counts, not an executed
fixed-tape implementation or a complete multiplier.

Credits: the source endpoint factorization and shared-query argument;
S004's exact Fourier rank/weighted-rectangle calculations; E002 physical
and precision suppliers; @CubeJerry; substantial ChatGPT research assistance.
No priority, full-machine execution, formal proof or human certification is claimed.

## 7. Symmetric output preconditioning and two accumulation channels

The lead proposed the output-side analogue during review. It is valid,
provided the auxiliary phases are placed in the following fixed order.
This makes the per-rectangle orientation choice executable.

At label v let P_v be the initial auxiliary sign phase in its fixed physical
paired bases, and let F_v be the full normalized Fourier transform on both
auxiliary halves. Set A_v=F_v P_v. The source endpoint associated with a
subspace H has the form T_(v,H) P_v, with ordinary basis/coset maps retained
explicitly. Section 1 factors this as

    T_(v,H) P_v = S_(v,H) A_v,                            (EP9)

where S uses only the inverse complementary partial transform, of
D-1-dim H axes per half, plus ordinary reindexing. The corresponding
output endpoint is its adjoint with the complementary subspace K:

    (T_(w,K) P_w)^* = A_w^* S_(w,K)^*,
    A_w^*=P_w^* F_w^*.                                   (EP10)

For binary phases P_w^*=P_w. This order matters: the output auxiliary
phase is applied after the global inverse full transform. It is not
commuted through that transform.

The source factorization of initial and final phases justifies their
independence. In every fixed label basis, the paired form is
x_j y_j + dot(x_aux,y_aux). Its auxiliary term uses the same reserved
fields for every query j and every rectangle. The distinguished term is
constant on auxiliary cosets and remains in the query's middle monomial
map. The same holds at the destination after returning to its physical
paired bases. P_v and P_w are therefore fixed label operators, while all
query-dependent phases stay inside their individual routed terms.

For each rectangle I x J there are two valid choices:

* Source preconditioning: H=span(I)^perp, cost
  (r_I-1)|I|+r_I|J| per half before the global transforms.
* Output preconditioning: H=span(J), K=H^perp, source cost r_J per
  incidence and output complementary cost r_J-1. Its corresponding bill
  is r_J|I|+(r_J-1)|J| per half.

Prepare both the phase-modified ordinary input P_v x_v and its transformed
version F_v P_v x_v. Keep two destination channels: an ordinary auxiliary
channel Y0 and a full-auxiliary-frequency channel Y1. Each rectangle uses
the channel selected by its smaller displayed bill, with ordinary maps
returning contributions to that label's fixed ordinary or full-frequency
coordinates. After every rectangle and query has been accumulated, return

    P_w^* [Y0 + F_w^* Y1].                                (EP11)

Complete charged contributions and add them separately in ordinary physical
coordinates. EP11 is linearity applied to EP9--EP10. No coordinate-dependent
phase is moved through an invalid sum. In particular S_(w,K)^* is applied
before accumulation into Y1; the fixed A_w^* is applied once afterward.

Define

    K_sym=(1/N) sum_R min{(r_I-1)|I|+r_I|J|,
                         r_J|I|+(r_J-1)|J|}.              (EP12)

The free axis-call bill is at most

    4(D-1)+2K_sym.                                       (EP13)

An unused global transform is omitted if all rectangles select one channel.
A compiler may therefore take the minimum of EP13 and either one-channel
version. A constant number of additional input/output arrays suffice.
Ranks and channel choices are computed in finite preflight; temporary
metadata are removed before children. The normalized-child, polynomial-map
and precision interfaces remain the same.

Homogeneous first-difference rectangles have equal side cardinalities and
span ranks. For them EP12 equals EP1, with no improvement over Section 4.
The symmetric version targets asymmetric rectangles and does not alter
the asymptotic conclusion of Section 5. Credit for this explicit symmetric
output and two-channel proposal belongs to the S004 lead.

The extended exact checker also passes 4,368 full-phase/adjoint identity
entries and 84 two-channel aggregation entries. It rejects 2,142 entries
when the output phase is placed on the wrong side of the full Fourier
transform. These checks complement the arbitrary-subspace identity tests
in Section 6; the phase ordering in EP10 is essential.
