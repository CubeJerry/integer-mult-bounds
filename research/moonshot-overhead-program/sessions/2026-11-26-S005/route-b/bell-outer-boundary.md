# Bell endpoint accounting through the actual integer caller

Status: **exact boundary identities and a scoped invoice stop gate**.
The positive BE local algebra is retained. Its present endpoint costs
do not imply an improved complete multiplication bound. This note
identifies the extra operators needed to carry its encoding through the
actual outer caller, and counts the two full-volume endpoints correctly.

Dependencies: `../route-a/paired-column-bell-executor.md` (BE), RO, and
OpenAI math `3344da59991ed94f9ba711217b29c1d760badfa6`, tape
`build/integers.tex` (synchronized short transforms, phase streaming and
exact recovery) and `build/walsh.tex`. The outer source formulas were
read directly. No runtime lower bound is asserted.

## 1. Full-rate convention

Let a=2s, Q=2^s. Flatten the A by t column-pair labels of BE to two
s-bit strings u,v. Its orthogonal encoding is

    E |u,v> = Q^(-1/2) sum_z (-1)^(v dot z) |z,z+u>.

For a physical data array f(x,y), write its encoded array as

    fhat(u,v)=(E^T f)(u,v)
      =Q^(-1/2) sum_z (-1)^(v dot z) f(z,z+u).        (BO1)

There are Q^2 independent data entries on both sides. Each u is a
complete Q-entry fibre. Further spectators and numerical work rows are
independent copies. No symmetry of f, zeroed half or initialized copy is
assumed. One E or E^T executes a normalized s-bit Walsh on every such
fibre and a separately charged linear index permutation.

## 2. Pointwise multiplication becomes full XOR convolution

For arbitrary independent arrays f,g,

    (E^T(f odot g))(u,v)
      =Q^(-1/2) sum_w fhat(u,w) ghat(u,v+w).          (BO2)

All additions in indices are binary. The scalar is Q^(-1/2), not 1/Q
and not 1. To prove the identity, insert the inverse normalized Walsh
expansions for f(z,z+u) and g(z,z+u), then sum the character at v over
z. The sum is Q when the two frequency indices add to v, and zero
otherwise. Three factors Q^(-1/2) and that factor Q give BO2.

Consequently retaining Bell encoding across the source's coordinatewise
product requires a full-rate s-bit XOR-convolution executor on every u
fibre. It is a genuine bilinear task, outside BE3--BE5's linear algebra.
The standard Fourier implementation uses three s-bit transforms on the
full corresponding array volumes: one for each operand and one for the
output, plus the pointwise products. These calls are not volume 1/Q
children of the original problem; their Q independent u-fibres together
contain all Q^2 entries. A better bilinear executor remains possible,
but must be constructed and priced rather than inferred from BE.

A small adverse control: at Q=2, let f be supported at physical (0,0)
and g at (1,1). Then f odot g=0. On the u=0 fibre, their encoded values
are respectively (1,1)/sqrt(2) and (1,-1)/sqrt(2); their coordinatewise
product is nonzero. Thus encoded pointwise multiplication is incorrect
even on two one-entry inputs.

BO2 preserves the source stability bound. E is unitary, so

    norm(E^T(f odot g))_2 <= norm(f)_2 norm(g)_2.

The missing conclusion is an improved physical execution time, not an
uncontrolled normalization or an inevitable numerical instability.

## 3. A general source phase becomes a convolution operator

For an arbitrary ordinary diagonal D=diag(d(x,y)), define

    kappa_u(t)=Q^(-1) sum_z (-1)^(t dot z) d(z,z+u).

Then its exact Bell conjugate is

    (E^T D E h)(u,v)=sum_t kappa_u(t) h(u,v+t).       (BO3)

This follows by the same character expansion, now with two normalized
Walsh factors. A general d gives dense kappa. BE's quadratic parity
tables are a special family with a much better shared executor; BO3
does not override that positive result. It shows why arbitrary outer
phase tables do not automatically inherit it.

For a precise control choose Q=2 and a primitive third root omega, and
let D=diag(1,omega) tensor diag(1,omega). On the u=0 fibre its Bell
conjugate is

    ((1+omega^2)/2) I + ((1-omega^2)/2) X,             (BO4)

where X swaps v=0,1. Both coefficients are nonzero. Thus the vector at
the zero Bell address reaches a nonzero address, leaving the zero RO
rowspace block. Even identical phase functions on the two members of
each pair need not give a signed permutation or an orbit-local map.
This example is unitary. It does not rely on a large coefficient or
an approximation error. It lies outside the real quadratic-sign scope
proved in BE, so there is no contradiction.

The actual tape caller uses arbitrary block phase tables prepared from
chirps, radix-two phases and the displayed L(z) decomposition. In
particular its chirp is

    chi(j)=exp(2 pi i (j^2+(ell mod 2)j)/(2 ell)),

on an ell-coordinate occupied axis, extended by identity on borrowed
coordinates. For odd ell>2, chi(1)=exp(2 pi i/ell) is not a binary sign.
The source also explicitly prepares phase ratios from complex z and
positive square roots. Therefore one cannot invoke BE's quadratic
binary-parity theorem for the complete outer phase interface. A new
encoded-phase executor must cover these actual tables, their different
block schedules, occupied spectators and borrowed-coordinate restoration.
BO4 is a discriminating counterexample to the unrestricted extension;
it is not asserted to be an entire large source phase layer by itself.

There is a further pairing issue. The source changes which selected bit
is transformed in each participating block, separated by arbitrary
within-block permutations. BE's monomial formula pairs TWO copies of
the same one-column action. A fixed global pairing must be shown to
respect each such layer, or its changing pairing must be implemented
and charged. The synchronized-short-transform lemma supplies no such
Bell-pair invariance.

## 4. What cancellation actually saves

If all linear stages L_1,...,L_j share one admissible encoding E, then

    L_j ... L_1
      =E (E^T L_j E) ... (E^T L_1 E) E^T.

The intermediate E^T E pairs cancel exactly. BE already receives this
benefit by encoding once around its entire local source algebra,
including rational repair tables. The input E^T and output E remain.
Deleting either boundary changes the output contract for arbitrary
independent input data.

The pinned multiplication caller is

    A*B = sqrt(S) U^*((U A) odot (U B)),              (BO5)

followed by inverse CRT and exact rounding/carries. Its forward and
adjoint U each contain O(log k) phase, permutation and selected-Walsh
layers. To carry E from the two forward transforms through the product
and into the adjoint, one must implement BO2, BO3 and every changed
pairing/layout in the same common format. BE alone supplies none of
these extra interfaces. Inverse CRT and the final ordered coefficient
stream also require the ordinary output format before rounding/carries.

Even under the optimistic assumption that all intervening LINEAR
stages are already cheap in Bell coordinates, carrying the encoding
through BO5 leaves two input encoders and one final decoder. The
standard implementation of the encoded product BO2 adds the three
full-volume half-width transforms just described. These are the same
six endpoint transforms as wrapping the three linear transforms
separately. This is an accounting observation about that implementation,
not a lower bound on all possible encoded multiplication algorithms.

The actual input digit arrays have structural padding. This note does
not rule out exploiting it in a changed outer algorithm. The retained
Walsh component, its recursive rows and its borrowed coordinates have
an arbitrary-input contract; that contract cannot be weakened silently
to justify deleting endpoints.

## 5. The direct recursive endpoint bill returns linear active width

For dyadic a above a fixed positive base a_0, consider the explicitly
evaluated positive Bell bill

    B(a)=2 B(a/2)+P(a),   B(a_0)>0, P(a)>=0.          (BO6)

The two children each transform half as many address bits on the FULL
incoming encoded volume. Iterating gives

    B(2^h a_0) >= 2^h B(a_0).                        (BO7)

With bounded local work, the evaluated bill is Theta(a); with
P(a)=O(a^eta), eta<1, it remains O(a). A full V a converter at every
node instead gives an O(a log a) upper bill. At square-root
normalization each level has child mass sqrt(2), not 1 and not
1/sqrt(2). BO7 is a lower bound on this DEFINED positive invoice;
an upper inequality t(a)<=2t(a/2)+P(a) does not lower-bound actual time.

If an ordinary source template with actual child-volume ratio b_A is
expanded once inside each encoder, then on clean admissible widths
a=2Af with even f the new actual ratio is 2 b_A and child width
a/(2A). Its normalized ratio is

    (2 b_A) sqrt(1/(2A)) = sqrt(2) b_A/sqrt(A).        (BO8)

For rounded source widths choose the largest permitted even
f<=a/(2A). The same expression upper-bounds the normalized child
mass, and the O(A) leftover bits stay in the paid local remainder.

The endpoint template's nonrecursive address work and its own layout
conversions must also be paid. BE's existing local closure does not
erase them. With the retained subpower binary mass, BO8 keeps that
mass and an additional constant; with a future bounded critical mass,
the extra constant could fit a polynomial-logarithmic potential. No
part of BO8 supplies the missing critical template or fast converter.

## 6. Decision and verification

Retain BE as a positive common-representation executor for the actual
finite Walsh/repair algebra. Do not claim that it closes the complete
Walsh recurrence or the outer integer caller. A useful next proof
must do at least one concrete job: reduce a paid endpoint/conversion
invoice; construct the encoded phase and bilinear product interfaces;
or supply an outer format in which fewer expensive boundaries are
actually required. Direct endpoint recursion with the current converter
does not meet the target.

`verify_bell_outer_boundary.py` checks BO2 and BO3 using exact integer
Walsh numerators, the normalization factors, the third-root adverse
control in Q(omega), and the exact endpoint-volume arithmetic. Its
receipt is `bell-outer-boundary-verification.json`. The tests neither
prove a faster encoded convolution nor exclude one.

Credits: Jerry Chen (@CubeJerry); BE's explicit full-rate conventions;
the pinned outer Fourier/convolution caller; elementary finite-group
Fourier product identities; substantial ChatGPT assistance. No priority
claim is made for the convolution theorem or Bell coordinates.
