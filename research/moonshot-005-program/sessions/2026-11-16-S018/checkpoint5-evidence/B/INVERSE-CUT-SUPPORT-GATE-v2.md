# An inverse-support cut excludes rank4 from the isolated-rank1 reduction

**Universal fixed-template theorem, pending independent review.**
The nonclean idle wrapper is an exact positive ordinary identity, but its
remaining two-bank M42 equation cannot have an independent rank4 endpoint.
This is a support-filtration theorem, not a failed finite search.

## General cut lemma

Let F_s be the span of a fixed finite catalogue of unitary one-column words
whose rows and columns have at most2^s nonzero entries, tensor-lifted with all
actual phases. Ordinary multiplication preserves this support filtration.
Assume an invertible bank matrix factors M=P W, with every block of P^-1
in F_s and every block of W in F_t. The ordinary matrices appearing in their
finite expressions and inverses are fixed before width grows.

If M is ordinary-equivalent to independent Gaussian jobs, every job has
rank r<=s+t. This assertion uses finite tensor separation at a catalogue-
dependent threshold V0 and makes no isolated-small-width claim.

To prove it, suppose M=O diag(G_j) R with ordinary units O,R and one Gaussian
job G of rank r>s+t. Multiplying by P^-1 and selecting its input job column
(after R^-1) gives

    P^-1 O e_j G = W R^-1 e_j.                          (1)

The right side lies in F_t. Expand the left side into its finite unitary
word generators T H G, where H is ordinary monomial and T has rows/columns
of support at most2^s. The inverse of T H has column support at most2^s.
For every individual column v of G, which has support exactly2^r,

    |supp(v)| <= 2^s |supp(T H v)|.

Indeed v=(T H)^-1(T H v), and each nonzero coordinate on the right can
contribute to at most2^s output coordinates. Thus every column of T H G
has support at least2^(r-s)>2^t. No such one-column word is projectively
identical to a word in F_t. Faithful finite tensor separation, including
every actual projective phase, forces both sides of(1) to vanish. But
P^-1 O is a unit, and its j-th block column followed by the unit G is
injective. This contradiction proves the cut lemma.

This argument does not claim a support bound on an arbitrary numerical sum.
It separates the unitary word catalogues before invoking their faithful tensor
independence. No Clifford group, common 2-adic lattice, genericity assumption,
monomial pivot or division by a sector projector is used.

## Apply the cut to the actual remaining equation

The exact isolated-rank1 wrapper gives

    M42=D0(a) B U Q_A L,
    D0(a)=diag(a,I),
    L=[[a,0],[I,a]], U=[[a,-a²],[0,a]],                  (2)

where B,Q_A are arbitrary ordinary units. Neither their entries nor their
inverse recipes need commute. Split P=D0(a) B U and W=Q_A L. The literal
inverse is

    U^-1=[[a^-1,I],[0,a^-1]],
    P^-1=U^-1 B^-1 diag(a^-1,I).                       (3)

Each one-column word in(3) has at most two inverse rank1 source factors,
so both its rows and columns have support at most4: P^-1 lies in F2.
Every block of W lies in F1. The cut lemma gives r<=3 for every independent
Gaussian job in M42. In particular no ordinary equivalence to independent
(4,2) is possible, for ANY B,Q_A in the fixed ordinary interface.

The conclusion includes arbitrary b,u,f in the wrapper, beta outside the
square algebra, completely unrestricted Q_A, and arbitrary ordinary endpoint
encodings. It is much broader than the cyclic-clock or G512 searches. The
wrapper's exact middle rank1 isolation consumes the structural freedom needed
for a rank4 endpoint in this placement; changing the clock or finite Q basis
cannot repair it.

## Sharp control, scope and next equation

For the original three-native word, L U L=[[0,-a⁴],[a²,0]]. Its cut after
L U has inverse degree3 because L^-1 contains -a^-2. Together with the last
L in F1, the same lemma permits rank4, and the displayed exact identity
attains that upper rank bound. The query D0(a) in(2) has inverse degree1;
replacing it by L changes the decisive cut. No ordinary rank1 query is being
silently replaced by a two-bank native.

This theorem excludes the exactly isolated-rank1 family(2), not every
three-native three-bank421 architecture. A surviving construction must retain
coupling of the rank1 job through the remaining stages or otherwise change
the placement/interface so this F2/F1 cut is unavailable. All native-body,
ordinary/endpoint/compiler, source/owner, precision and recursion obligations
remain. No new kappa or saving is claimed. Credit @CubeJerry, retained tensor
separation and support-filtration arguments, root's wrapper verification,
and Worker B with substantial OpenAI help.

## Complete clean-first-two-entry exclusion (root extension)

The same cut closes the ENTIRE necessary normal form, without requiring the
rank1 job to be explicitly isolated by the wrapper. This extension was
identified by root from the above cut and independently reconstructed by B.
Assume only a C00 a^-1 and a C10 a^-1 ordinary. The previously reviewed
normal-form theorem gives

    C=[[s,b,0],[t,d,e],[u,f,0]],
    Q=[[q00,q01,0],[q10,q11,0],[q20,q21,q22]],           (4)

with s,e,q22,Q_A units, im(E1)=middle bank, and
im(E4)=im(V), V=(shat,that,0)^T, shat=a s a^-1 a unit.
The blocks u and every block of Q are otherwise unrestricted ordinary.

Let J project the three output banks onto top and bottom. Direct multiplication
of the actual normal form gives

    J E = [M,0],
    M=D0(a) B U_A Q_A L_A,
    B=[[s,b],[u,f]].                                   (5)

B is a unit: permuting C's output rows to(top,bottom,middle) gives the block
lower-triangular matrix [[B,0],[*,e]], and C,e are units. Thus the prefix
P=D0(a) B U_A is a unit and P^-1 lies in F2 exactly as above.

Write the asserted ordinary endpoint E=O diag(G4,G2,G1) R, and let
v=O e4 be its ordinary rank4 output column. Its image is im(V), so its
bottom block vanishes and its top block is a unit: top projection is an
isomorphism on the graph im(V). Consequently Jv is an injective, nonzero
ordinary two-bank column. Let z be the first two block rows of R^-1 e4;
z is ordinary. Selecting the rank4 endpoint column and applying J gives

    M z = (Jv) G4,
    P^-1 (Jv) G4 = Q_A L_A z.                          (6)

The right side is in F1. Every one-column word on the left has inverse
support degree at most2 before G4, hence every column has at least4 nonzero
entries. The same finite tensor-separation argument forces both sides of(6)
to vanish. Since P and G4 are units, this forces Jv=0, a contradiction.
No stable cancellation theorem or ordinary inverse of an individual unknown
block is needed beyond the already proved normal form.

**Final theorem.** For the literal three-native architecture L C U Q L,
no fixed finite ordinary template valid at all sufficiently large faithful
widths can provide independent421 if both a C00 a^-1 and a C10 a^-1 are
ordinary. This permits arbitrary genuine idle coupling C20, arbitrary
noncommuting and outside-square Q, and arbitrary ordinary endpoint encodings.
It contains every coherent R(D_b^tensor V)diag(I,h,I) first interface for
arbitrary ordinary h, and strengthens both the whole-square and all-clean
first-column gates. A surviving caller must make C00 or C10 nonclean, or
change the source/native/endpoint architecture. It does not claim that such
a changed first column is sufficient. All physical pricing obligations and
all five foundations remain.
