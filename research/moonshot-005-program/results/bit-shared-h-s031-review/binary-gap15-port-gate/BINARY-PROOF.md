# A derivative collision excludes arbitrary binary-linear bank gauges

**Strengthening of the independently reviewed geometric/gap15 port gate.
No new complete kappa. Separate review is required before admission.**

The field-linear gate left arbitrary F2-linear source gauges open because its
chosen scalar ratios could not be commuted through an arbitrary binary map.
A different pair of actual native receivers removes that restriction. Their
second-donor derivatives are equal, so the relevant difference factors without
commuting anything.

## 1. Retained source and exact quantifiers

Retain the source, native identity target, separated original banks and tight
H263 interface of
[the geometric/gap15 theorem](../../bit-geometric-gauge-port-gate/author/PROOF.md).
Let F be any finite extension of GF64 and k any positive admissible quotient
width. Each donor has input F^(16k) and quotient

    Q_(j,a)=[1,a,...,a^15] tensor I_k
                 +(a^16+1)e_15^t tensor A_j,

where A_j is an arbitrary k-square matrix over F. Each donor may undergo its
own arbitrary invertible F2-linear whole-bank input transformation. H encoding,
quotient-output relabelings and downstream decoding may be nonlinear. There
is no additional informative path or changed proper target.

Write A for the additive F2-vector space underlying F^k. The already reviewed
all-width source theorem gives an injective additive map

    E_j:A^6 -> F^(16k)

such that the entire off-H inverse fibre for receiver i is

    E_j(v_(j,i) tensor A),

where v_(j,i) is a nonzero vector in F2^6. The literal parameters for the
three donors are related by invertible binary maps J_j. On the corresponding
fibre the central source quotient is

    Q_(j,49) E_j(v_(j,i) tensor x)=d_(j,i)x,
    d_(j,i)=v_(j,i)^8+49^4 v_(j,i)^4 in GF64^*.

The injectivity and readout identities hold for every A_j, not just a finite
matrix example. The current proof uses them as explicit predecessor lemmas.

## 2. Connected binary directions force one additive amplitude map

We state the needed extension of the earlier amplitude argument.

Let X be a set of nonzero binary vectors spanning F2^r, with connected graph
joining v,w whenever v+w is in X. Let E and E' be injective additive maps from
A^r into two ambient additive spaces. Let J be an invertible binary r-square
map. Suppose an additive bijection T between the ambient spaces carries

    E(v tensor A) onto E'(Jv tensor A) for each v in X.

Then a single additive automorphism M of A satisfies

    T E(v tensor x)=E'(Jv tensor Mx) for every v in X and x in A.       (1)

To prove this, each individual fibre defines an additive automorphism M_v.
For an edge v,w, compare the image of E((v+w) tensor x) with the sum of the
images at v and w. The subspaces E'(Jv tensor A) and E'(Jw tensor A) intersect
only at zero: distinct nonzero binary vectors v,w are independent over F2,
and E' is injective. Therefore M_v=M_w=M_(v+w). Connectedness proves(1).
No linearity over GF64 is used.

At H263 the actual33 parameter vectors span F2^6 and their additive graph has
276 edges and is connected. The two actual J_j are independently checked in
the predecessor review. Tightness of the additive target first forces equality
of the pulled-back whole inverse fibres, so the relative source gauges satisfy
the hypotheses of(1). All original amplitude coordinates, extension-field
coordinates and source blocks may mix; no block-diagonal assumption is made.

## 3. The exact native derivative collision

Let D(t) be multiplication by t in GF64 on A, viewed as a binary matrix. The
required receiver aggregate, after an invertible change of its output
coordinates, has binary row space

    W_i = row[ I, D(d_(0,i)) M_1 D(d_(61,i))^(-1),
                  D(d_(0,i)) M_2 D(d_(62,i))^(-1) ],                 (2)

where M_1,M_2 are fixed arbitrary invertible binary amplitude maps. Replacing
an amplitude by its inverse only changes this convention, not the allowed
class. Crucially, no D(t) is commuted through M_j.

The actual native D108 exit is visible to both receivers5 and76. Their exact
derivative triples, in donor order0,61,62, are

    receiver5:  (30,18,12),
    receiver76: (38,18,52).

The difference of the second blocks in(2) is therefore

    D(30) M_1 D(18)^(-1) + D(38) M_1 D(18)^(-1)
      =D(56) M_1 D(18)^(-1).                                       (3)

Since56 and18 are nonzero field elements and M_1 is invertible, this operator
is invertible at every amplitude dimension. Equation(3) uses distributivity
and the same right-hand factors; it holds even if M_1 fails to commute with
every nontrivial field scalar.

Any row common to W_5 and W_76 has the same first block u. Equality of the
second blocks gives u times(3)=0, hence u=0 and the entire row is zero. Thus

    W_5 intersection W_76 = {0}.

The third donor's amplitude map is unrestricted and cannot alter this
two-block contradiction.

## 4. The actual positive shared packet is impossible

For each receiver, fixing its off-H observations leaves the H input tuple
surjective onto the full product alphabet. Its target aggregate and visible
H transcript have equal cardinalities. Exact recovery makes the transcript
a bijective function of the target aggregate. Every visible port is therefore
a function of that aggregate and has its full positive alphabet.

The single D108 packet must be a function of both binary-linear aggregates
in(2). A common function of linear observations is invariant under the sum
of their kernels. Their zero row-space intersection makes this sum the
whole H input space. Hence the packet is constant, contradicting its positive
full alphabet. At bank3840 this is an actual16-field packet within a240-field
receiver cut, with genuine early owners.

This proves the obstruction for arbitrary binary-linear whole-bank gauges,
all admissible widths and finite coefficient extensions. Nonlinear H or
downstream processing does not change the argument. The prior field-linear
proof remains correct within its smaller scope; this is an additional theorem
with a different receiver pair.

## 5. Scope, verification and next step

The checker authenticates the predecessor source/readout proof and independent
review, reconstructs the native D108 audience and all six derivative values,
and tests the factorization with binary matrices that do not commute with
field multiplication. It uses several amplitude widths and cross-copy mixing
as controls; universality comes from(1) and(3), not those finite tests.

The result still concerns the fixed scalar/gap15 quotient information and
identity target on this tight native cut. Multiple-gap feedback, independently
changed quotients, extra informative channels and changed targets are outside
its scope. A separate proposed nonlinear-core theorem investigates arbitrary
bank bijections; no global additivity of such a bijection is assumed here.

No source rank gap is converted into a return tariff. The full supplier,
ownership, compiler, precision and recursive obligations are unchanged.
No complete multiplication exponent or foundational discharge is claimed.

Credit @CubeJerry and the retained geometric-node, polynomial-feedback,
tight-cut and native-atlas authors. Root supplied the earlier universal gap15
core/readout theorem. S031 Worker C found the derivative collision and the
arbitrary-binary amplitude extension with substantial OpenAI assistance.
Independent review is recorded separately.
