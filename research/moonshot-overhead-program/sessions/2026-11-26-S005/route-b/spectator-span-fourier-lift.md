# A full-rate spectator-span Fourier lift and its priced boundary

Status: **exact algebra proved; physical boundary supplier open**.
The factorization includes every spectator rank, every Fourier frequency
and the dual-to-primal output correction. It is not an improved Walsh
algorithm by itself. Section 6 gives a source-specific conditional
physical transfer, rather than assuming a completed transform bound.

Pins: OpenAI math `3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier
`build/kernel.tex` and `binary.tex`, tape `build/walsh.tex`; programme
`62d9d8e917379cb2edc17c9761e12e2345bc01f4`. The relevant positive local
compiler is `../route-a/rowspace-orbit-compiler.md` (RO). The complete
integer transfer and established numerical invoices are CT in this
directory and E002 NI / S003 NT, explicitly cited below.

## 1. Preserve the actual frames and all input entries

Let E=F2^f with its ordinary nondegenerate dot product. An address is

    X=(x; B),   x in E,   B in F2^((A-1) by f).

The ordered spectator tuple B is fixed by the selected-row Walsh call.
Its span U has rank r, where 0<=r<=min(A-1,f). B is not replaced by U:
all ordered tuples spanning U carry independent data and remain distinct
fibres. Extra complete spectator indices and numerical work-row roles
are also retained, with no invariance assumption on their data.

Choose the unique nonzero-row RREF basis u_1,...,u_r of U, with pivots
p_1,...,p_r, and complement C consisting of the standard vectors e_j at
nonpivot positions. Put s=f-r and M_B=[u_1 ... u_r e_j ...], with these
vectors as columns. Then M_B is invertible and

    x=M_B(alpha,beta),  alpha in F2^r, beta in F2^s.       (SF1)

For beta=0 the full address rowspace is U. For beta!=0 it is
U+<C beta>. Over F2 distinct nonzero beta give distinct such rowspaces.
For this fixed B, each beta group contains exactly 2^r independent
entries. The grouping is a bijection, not an averaging projection.

The number of ordered B of rank r is

    [f choose r]_2 h(A-1,r),
    h(t,r)=product_(j=0)^(r-1)(2^t-2^j), h(t,0)=1.        (SF2)

Therefore all rank strata together contain

    sum_r [f choose r]_2 h(A-1,r) 2^f = 2^(A f)           (SF3)

entries. The Gaussian coefficient counts U; h counts its ordered,
possibly redundant, spanning spectator tuples. No frame multiplicity
may be dropped when comparing with a scalar table on subspaces.

## 2. Exact normalized quotient factorization

Write F_B(alpha,beta)=F(M_B(alpha,beta),B). First take

    G_B(gamma,beta)
      =2^(-r/2) sum_alpha (-1)^(alpha dot gamma)
                                      F_B(alpha,beta),   (SF4)

then, for EVERY gamma in F2^r, take

    Z_B(gamma,delta)
      =2^(-s/2) sum_beta (-1)^(beta dot delta)
                                      G_B(gamma,beta).   (SF5)

Since x dot y=(alpha,beta) dot (M_B^T y), the answer is exactly

    (H_f F)(y,B)=Z_B(M_B^T y),
    y=M_B^(-T)(gamma,delta).                            (SF6)

Thus the first stage is H_r inside each rowspace coset; the second is
H_(f-r) on the quotient coordinates in each of 2^r frequency channels.
Both stages together are unitary, including r=0 or s=0, where H_0=1.
The factors 2^(-r/2) and 2^(-s/2) multiply to the required 2^(-f/2).
For odd intermediate widths these identities are over R (or Q(sqrt2));
the pinned binary source explicitly supplies the Q(sqrt2) normalization
and its dyadic approximation. No unsupported exact dyadic claim is made.

The output coordinates in SF6 are DUAL coordinates. To return to the
primal coset convention in SF1 one must apply

    (alpha',beta')=(M_B^T M_B)^(-1)(gamma,delta).          (SF7)

This generally mixes gamma and delta. It is not correct to label the
output rowspace using delta alone. The restriction of the dot product
to U may be degenerate even though the full form on E is nondegenerate.

There is no need to construct a dense f by f matrix. In pivot/nonpivot
order write the RREF basis as [I_r R], where R is r by s. Then

    input:  x_p=alpha,  x_nonpivot=R^T alpha+beta;
    output: y_p=gamma+R delta, y_nonpivot=delta;
    primal output:
      alpha'=gamma+R delta,
      beta'=delta+R^T(gamma+R delta).                    (SF8)

The basis and all coordinate arithmetic need O(poly(A) f) bits of
work per record and O(A f) basis storage. In the numerical application
the record width is Theta(k) with A f<=k, so this metadata arithmetic
fits a polynomial-A times volume bill. Rearranging the payload records
according to those keys is a separate physical operation.

For example, f=2 and U=<11> has pivot 1 and R=[1]. Then

    (gamma,delta)=(1,0) -> y=10 -> beta'=1.

Reading delta=0 as the output coset U would give the wrong answer.
This isotropic example is retained in the finite checks.

## 3. Exact strength of every coset-to-coset block

Fix B and two cosets x_0+U, y_0+U. The normalized block of H_f has
entries

    2^(-f/2)(-1)^((x_0+u) dot (y_0+v)),  u,v in U.      (SF9)

Let d=dim(U intersection U^perp). Removing row and column signs leaves
the character matrix of the restricted bilinear form on U. A change
of its row and column bases gives

    D_2^(tensor (r-d)) tensor J_(2^d),

where J is all ones. Consequently EVERY block SF9 has

    real/complex rank = 2^(r-d),
    every nonzero singular value = 2^((r+d-f)/2).        (SF10)

This is a numerical-field rank, not rank modulo two. In particular the
r=0 fibres contain a full ordinary f-bit Walsh transform across 2^f
singleton cosets. For nondegenerate U, d=0; for isotropic U the rank
can drop, while the surviving singular values increase accordingly.

Proof of the singular-value formula: the nonzero singular values of
the unnormalized Walsh factor are 2^((r-d)/2), and the unique nonzero
singular value of J_(2^d) is 2^d. Multiply them and then multiply by
2^(-f/2). Translations only apply diagonal signs. QED.

These block ranks cannot be added as separately charged running time.
The complete transform on one B-fibre has rank 2^f; its blocks share
one global linear operation. SF10 specifies the information that a
collective physical executor must carry, not a universal time bound.

## 4. The missing regrouping, and the subspace-transform comparison

The orbit layout is grouped by W=rowspace(X), with a full-rank
coefficient frame C_X inside W. The factorization uses a different
order: B, beta, alpha, followed by B, gamma, delta. Entry must regroup
all flags U<=W together with their ordered B frames; exit must implement
SF7 and regroup by the resulting W. These are bijections of exactly
the entries in SF3. An efficient rank/unrank formula does not pay for
these payload movements on finitely many tapes.

The hyperplane-cut Fourier mechanism in Perles--Weinstein,
*Subspace convolution*, arXiv:2611.13134 (primary author manuscript,
section 1.2.1, equations (3)--(4)), similarly Fourier transforms a
coset table and regroups (B,lambda) as (lambda,B), with B<=ker lambda.
Its scalar subspace table is not the present full-rate framed table.
Here gamma=0 is the U-invariant channel; all gamma!=0 channels retain
the nonconstant values on each U-coset. There are h(A-1,r) independent
B frames per U, and SF7 remains necessary. Reusing the published
arithmetic regrouping requires an explicit lift with these channels,
counts, representation sizes and tape movements. The local equations
above make that additional interface precise; they do not assert that
the published subspace transform supplies it.

At the source shapes f>=m^(K+1), A=Theta(m), one has r<=A-1=o(f).
Therefore the quotient call has width f-r=(1-o(1))f. Merely replacing
H_f by SF4--SF5 does not obtain a useful arity shrink. It also executes
two transformations on the same full fibre volume, not on disjoint
fractions of that volume. A claimed recurrence must count that volume.

## 5. A concrete physical permutation supplier

The following open supplier, FC, concerns only representation changes;
it does not assume the running time of H_f or of multiplication.

For the actual source A_m=Theta(m), even f, root k>=A_m f and complete
spectators, FC converts ordinary selected-slot order to the RO orbit
layout and back. It is an exact bijection on arbitrary independent
Theta(k)-bit records, including every rank in SF2. Write J(f) for the
per-volume upper envelope of a separately completed exact interchanger.
Require

    time <= C V [m^K + D_m(1+J(f))](1+log(k+2))^b,
    D_m <= 2^[C sqrt(log(m+2) loglog(m+4))].            (FC)

All spectator extraction, frame/control construction, coordinate maps,
radix passes, head returns, input/output and erasure are included. The
coefficient of J(f) is subpower in m; a polynomial-m coefficient there
does not satisfy FC. The polynomial m^K ordinary term is allowed.
There is an absolute C V visited-cell bound, with an absolute number
of payload copies, polynomial(m,k) descriptors, reusable marked regions
and an effective finite guard on all actual selected shapes. Compact
preparation and its time are charged under the same source contracts.

SF4--SF8 identify one possible framed route to FC, but do not prove it.
The current direct sort has O(V A_m f) time and does not meet FC.
Charging J(A_m f) at every child boundary also does not imply FC: it
introduces another factor of order sqrt(m) in the separated invoice.
At fixed A=2, the FC contract permits charging the available J(f)
upper envelope; it does not silently assume a linear-time interchanger.

## 6. FC changes the actual numerical invoice

Retain the proved rational source template with

    A_m=Theta(m), W_m a power of two,
    sigma_m/W_m <= C sqrt(m) R_m,
    log R_m=O(sqrt(log(m+2) loglog(m+4))).              (SF11)

Use RO for every nonrecursive columnwise GL map and every pointwise
mask in a single orbit layout. Constant row mixers operate on the same
addresses and retain that layout. Their actual polynomial-m arithmetic,
coefficient preparation, norm and height bounds are unchanged. Enter
orbit order once per local template. At each Fourier child, convert its
whole work row to ordinary order, execute the actual f-bit child on
complete spectator fibres, then convert back. Exit once at the end.

The total volume of conversions divided by the original V is at most

    2 + 2 sigma_m/W_m <= C sqrt(m) R_m.                (SF12)

This charges conversions around EVERY child; it does not treat the
Fourier child as orbit-local. Each such converter has source axis width
f and parent axis count A_m. Polynomial-m ordinary work accumulated in
SF12 is absorbed by increasing its fixed degree K. FC's difficult work
therefore has local bill

    C V sqrt(m) R_m D_m J(f) polylog(k).               (SF13)

If J(u)<=C sqrt(u+1) E_I(u) with E_I monotone, f<=a/A_m gives

    local bill <= C V [m^K + sqrt(a+1) R_m D_m E_I(a)]
                  polylog(k),                       (SF14)

with a harmless whole-width boundary term if the source caller needs
one. Thus FC + RO proves the separated physical gate SN of S003 NT,
and the sharpened NI5-type volume threshold, up to the already retained
subpower factor. This is a mechanism-specific implication: an orbit
converter would remove the repeated query-map m factor from NI4.

For completeness, take m=Theta(a^delta) on the actual minus-one arity
sequence, with fixed small rational delta and every shape guard met.
Normalize numerical time by V sqrt(a), put x=log2(a+2), and let
psi(x)=sqrt(x log2(x+2)). The child logarithmic width is at most rho x
for fixed rho<1; SF11--SF14 give

    U_k(a) <= C a^(delta K-1/2)
                +2^[O(psi(x))] E_I(a)
                +2^[O(psi(x))] U_k(f),              (SF15)

apart from a fixed root-log factor. If E_I(a)<=2^[C chi(log2(a+2))],
monotonicity bounds every local E_I(a_i) by E_I(a_root). Pull that
single common factor out of the expanded recurrence. Only the recursive
psi losses must be summed; sum_j psi(rho^j x)=O(psi(x)). The number of
levels contributes at most O(log log(x+2)) to the exponent. Thus no
geometric summability premise on chi is needed, and iteration gives

    T_W(a,V)<=V sqrt(a+1)
       2^[O(chi(log2(a+2))+psi(log2(a+2)))] polylog(k).
                                                        (SF16)

This is the existing NI6 numerical transfer, now supplied conditionally
by the explicit representation-change mechanism FC. It is credited to
NI rather than presented as a new recurrence theorem. With the current
chi(x)=(x^2 log(x+2))^(1/3), the complete frontier is unchanged. If a
future exact supplier has chi=O(psi), FC preserves the square-root-log
scale through the numerical layer. If chi=O(log x), the retained
Fourier mass still leaves psi; FC alone does not give polynomial-x.

Batching, setup, precision and visited space follow with the actual
counts, not from algebra alone: product W_m along a path is polynomial
in root active width and divides the source's complete spectator range;
polynomial-m node counts and sufficiently small delta put preparation
below the numerical volume; FC's exact permutations have norm one and
introduce no numerical error; RO's scalar operations retain the existing
polynomial-m height/gain bounds. The source common-ancestor estimate
then permits p=C0 k, with its computed guard and fallback. FC's absolute
regions, serial RO work and shrinking numerical children give one O(Nk)
bound on all visited cells. Applying the pinned outer caller adds only
fixed logarithmic factors, hence the complete CONDITIONAL bound is

    T(n)<=C n sqrt(L)
          2^[O(chi(x)+psi(x)+log(x+2))],
    L=1+log2 n, x=log2 L, visited cells O(n).          (SF17)

FC is unproved. SF17 therefore does not change the unconditional
frontier, and it is not a constant-overhead or polynomial-x theorem.

## 7. Verification and status

`verify_spectator_span_lift.py` checks exact bit-coordinate identities,
all-rank fibre counts, the literal signed Fourier factorization on every
small B, and exact Gram identities for SF10. It includes rank zero,
rank-deficient B, nondegenerate U and isotropic U. Normalizations are
tracked as powers of two; no floating spectrum is used. The receipt is
`spectator-span-verification.json`. Finite checks do not establish FC,
the unbounded physical algorithm or a formal theorem.

Credits: Jerry Chen (@CubeJerry); the pinned source's primal/dual free
rectangle factorization; standard finite-field Fourier coordinates;
the independently developed RO layout and E002 NI/S003 NT invoice;
Perles--Weinstein's primary coset-Fourier comparison; substantial
ChatGPT assistance. No priority claim is made for elementary Fourier
factorization or character-matrix rank.
