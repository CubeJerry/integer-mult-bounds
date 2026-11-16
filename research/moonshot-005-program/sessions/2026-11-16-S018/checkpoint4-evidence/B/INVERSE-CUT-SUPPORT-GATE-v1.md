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
