# At most two quotient edits preserve nonsaturation

**Author note by Worker B; separate review pending. No common-H construction
or physical price is asserted.**

Fix one ordinary donor's geometric RS tuple over a field extension K of
GF64, with bank V=K^(16t), t>=1, and maps
`F_Q=(1,a_Q,...,a_Q^15) tensor I_t` at its 28 geometrically labelled planes.
Every relevant native view contains sixteen distinct planes. Replace
F_Q arbitrarily by a linear t-by-16t matrix at a set S of at most two
planes; leave every other quotient information space unchanged. Require
the new sixteen-plane source views used below to be invertible.

Let H and R be distinct source planes. Consider any finite receiver family
T, each receiver seeing both H and R. Let L'_r be the new off-H kernel at
receiver r. Then

    dim sum_(r in T) L'_r <= (5 + 4m + epsilon)t <= 14t,

where m=|S minus {H}| and epsilon is one if R belongs to S minus {H},
and zero otherwise. In particular this family cannot saturate a
15t-dimensional quotient kernel. One edited plane gives the stronger
upper bound10t; zero edits gives5t. If H itself is edited, its matrix is
not among the off-H observations, so it is correctly omitted from m.

## Proof

For receiver r, use its *old* invertible sixteen-plane evaluation map
as coordinates on V. Let L_(Q,r) be the old inverse space of the Q block.
The unchanged off-H observations force all old coordinates outside

    {H} union (S intersect visible(r))

to vanish on L'_r. Hence

    L'_r subset L_(H,r) + sum_(s in S, s!=H, s visible at r) L_(s,r).

Taking the sum over receivers preserves this containment. The old H
contribution sees both H and R and has rank at most5t by the geometric
two-node formula. If an edited s equals R, its old inverse spaces also
see two distinct nodes and contribute at most5t.

For every other edited s, the contributing receivers see the three
distinct nodes H,R,s. In the field coordinates appropriate to centre s,
their parameters satisfy

    b(v,a_H+a_s)=0,   b(v,a_R+a_s)=0.

The two nonzero normal vectors are distinct, hence binary independent.
Nondegeneracy of b makes their common kernel four-dimensional over F2.
The proved Moore-rank formula bounds the old s contribution by4t.
Dimension subadditivity now gives the stated bound. No independence
between contributions is assumed. The replacement coefficients are
otherwise unrestricted and may mix every coordinate of this tensor bank.

## Quantifiers and useful direct-sum form

The assertion concerns a single ordinary source and arbitrary finite
families of its actual receivers. It allows arbitrary choices of the
one or two edited planes. Additional leaf-plane visibility restrictions
only shrink the receiver family, so the bound applies to every triangle
propagation of the earlier array-anchor criterion.

It does not prove full source rank after an edit, compatible H readouts,
simultaneous alignment at two centres, or an actual early/late source
word. Those remain separate requirements. With three edits the displayed
dimension estimate can reach or exceed15t; no protection for three edits
is claimed. This is a linear-array lemma; no unrestricted nonlinear-edit
extension is asserted here.

If a larger source is a direct sum of components and one component
satisfies this strict nonsaturation bound, then its whole propagation
cannot saturate either, provided the other components retain full source
cuts. Every other component's span lies in its transported quotient
kernel and has rank at most its own15t-component bound. One strict
component therefore leaves a strict deficit in the sum. This observation
also survives output-basis changes and a common invertible bank-coordinate
change, since they preserve the relevant kernels and ranks.

For example, at the established sixteen-copy k=3 plus k=12 bank,
protection of the marked k=3 component after two edits gives at most
`16*(42+180)=3552`, strictly below the saturation target3600. One edit
gives at most`16*(30+180)=3360`. These are information ranks, not operation
prices or new return-rank lower bounds.

Credit the root's geometric-node construction and field identity and the
independent Moore-rank proof in the parent review. OpenAI-assisted author
note, session S030.
