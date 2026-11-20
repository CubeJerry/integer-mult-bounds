# A shared-port obstruction after arbitrary field-linear donor gauges

**Exact source-specific theorem. No new complete kappa.**

This result excludes the shared-node geometric scalar source, and its entire
single-gap15 matrix-feedback family, at one actual native H cut. It permits
arbitrary independent invertible **GF64-linear** changes of the complete
donor banks, arbitrary finite coefficient extensions, and unrestricted
deterministic processing at and after H. Arbitrary binary-linear gauges that
do not preserve the GF64 scalar action are outside this theorem.

## 1. Precisely fixed interface

Use the S030 global 28-node assignment over F0=GF(64), with modulus
x^6+x+1. At H263 the donors are 0,61,62 and the node is c=49. The 33
native receivers seeing H have identity foreign blocks in the S028 target:
none is exceptional receiver80 and none of these donors is donor10.

For any finite extension F/F0 and positive k divisible by15, each donor
has input F^(16k), source quotient width k, and H has three such inputs.
Every one of its45 exits has k/15 symbols; each receiver sees15 exits.
The actual bank3840t instance is k=240t. The existing tight additive-cut
lemma applies: the fifteen other observed source quotients leave a
k-dimensional uncertainty fibre, and the H tuple has exactly that capacity.
Each individual visible exit must have its full alphabet and be a function
of the required H aggregate. Same-chart caches do not add a new outgoing
channel. This is the existing route contract, not an assumption of free
access to other donor data.

The scalar source at node a is [1,a,...,a^15] tensor I_k. More generally
allow at donor j an arbitrary matrix A_j in M_k(F), and use

    Q_(j,a) = [1,a,...,a^15] tensor I_k
               + (a^16+1) e_15^t tensor A_j.             (1)

This is the single-gap15 subfamily of the admitted polynomial-feedback
construction. Its source views are invertible for every A_j; zero A_j
gives the scalar source. An arbitrary whole-input field-linear bijection
may additionally be applied separately at every donor. Separate output
relabelings of each source quotient do not change its information.

## 2. The six-dimensional fibre diagram survives every A_j

Let U_c(v) be the 16-coefficient vector

    [L_v(z)+L_v(c)]/(z+c),

where L_v is the pinned binary-linear geometric polynomial. At a receiver
with parameter v this is v^2 times the monic fifteen-root polynomial of
the off-H source observations. It extends to an injective F-linear map
U_c:F^6 -> F^16 from the six binary coordinates of v.

Let J_z be multiplication by z modulo z^16+1, and N_c=J_z+cI. The inverse
formula for (1) gives the entire off-H fibre as the image of

    E_j(v) = U_c(v) tensor I_k + N_c U_c(v) tensor A_j.  (2)

The map E_j:F^(6k)->F^(16k) is injective for every A_j. Here is an
all-width argument. J_z has only eigenvalue1 over an algebraic closure,
because z^16+1=(z+1)^16. Thus I+tN_c is invertible except possibly at
t=(1+c)^(-1); c is never1. At that exceptional scalar the checked
16-by6 matrix (I+tN_c)U_c still has rank6. Consequently the pencil has
rank6 at every scalar in the algebraic closure, not merely at the64
base-field values. Triangularize A_j over that closure. The resulting
block triangular map has these injective pencils on its diagonal;
induction on the copy coordinate proves (2) injective. Rank cannot fall
on descent to F. The finite certificate checks the exceptional pencil at
all28 nodes; only c=49 is needed here.

The H quotient on this normalized fibre is unchanged by feedback:

    Q_(j,c) E_j(v) = d_c(v) I_k,
    d_c(v)=v^8+c^4 v^4.                                (3)

Indeed e_c U_c=d_c, e_c N_c U_c+(c^16+1)e_15 U_c=0,
and e_15 N_c U_c=0. The coefficients of A_j and A_j^2 vanish separately.
These are exact small matrix identities. Every actual receiver has
d_c(v) nonzero because its full sixteen-quotient view is invertible.

## 3. Any compatible field-linear gauges have one amplitude map

For donors0 and61, the actual receiver parameters obey w=Jv for an
invertible binary-linear J. The 33 allowed v span F^6. The graph joining
v,w whenever v+w is also allowed is connected. These properties are
reconstructed from the actual native receiver list.

Suppose arbitrary field-linear input gauges aligned the whole off-H
fibres required by the additive target. Their relative action on the two
injective six-dimensional diagrams must have, at each allowed v, an
invertible amplitude matrix M_v satisfying

    E_0(v) x -> E_61(Jv) M_v x.

For a graph edge v,w, the images of E_61(Jv) and E_61(Jw) are disjoint:
injectivity of E_61 reduces this to independence of two distinct binary
vectors over F. Additivity and E_j(v+w)=E_j(v)+E_j(w) then force
M_v=M_w=M_(v+w). Connectedness gives a single invertible M, independent
of the receiver. The same statement applies to donor62. This argument
allows unrestricted mixing of all k amplitude coordinates and all16
source blocks; it does not assume a block-diagonal bank gauge.

Choose donor0's fibre coordinates as the common target coordinates.
After a fixed invertible change on each H input, the required aggregate
row space for receiver i is therefore

    W_i = row[ d_0(i)^(-1) I_k,
               d_1(i)^(-1) M_1,
               d_2(i)^(-1) M_2 ],                     (4)

with fixed invertible M_1,M_2. The precise orientation of M_j depends
on the gauge convention and is immaterial. Scalars commute with every
M_j because the gauges are F-linear.

The same argument permits arbitrary GF64-linear gauges over a larger
coefficient field F. Restrict scalars along a GF64 basis of F: width k
becomes k[F:GF64], each A_j becomes a matrix over GF64, and all geometric
coefficients and derivative ratios still lie in GF64. The proof then
applies to all GF64-linear mixing of the extension coordinates. It still
does not cover gauges that are merely F2-linear.

If d_0(i)/d_1(i) differs from d_0(r)/d_1(r), then W_i intersect W_r=0.
To see this, equate the first two blocks of a common row. Eliminating
the first block leaves a nonzero field scalar times an invertible M_1;
the common row is zero. This implication holds for every k and every
choice of M_1,M_2.

## 4. One actual shared exit contradicts the tight cut

The actual native D108 exit is seen by receivers5 and7. In the specified
GF64 convention the exact ratios are

    d_0(5)/d_1(5)=26,       d_0(7)/d_1(7)=49.

Thus their required aggregate row spaces have zero intersection. The
exit is nevertheless required to have |F|^(k/15)>1 possible values and
to be a function of each aggregate. A function of two linear maps is
invariant under both kernels, hence under their sum. Zero intersection
of the row spaces makes that kernel sum the whole input space, so the
function is constant. This contradicts its full positive alphabet.

This last step permits nonlinear exit encoders, arbitrary quotient-output
relabelings, and nonlinear downstream computation. It uses a positive
paid exit and exact capacity, not a linearity assumption on the decoder.
Consequently no source in (1), after the allowed bank gauges, completes
this fixed H cut for the exact native identity/S028 demands.

## 5. Boundaries, controls and next questions

The theorem changes no supplier exponent and gives no general lower bound
on the return rank of different target fittings. It excludes neither
multiple-gap feedback, genuinely changed source quotients, independent
node relabelings, additional paid channels, nor arbitrary binary-linear
bank gauges. In particular, a binary-linear amplitude map need not commute
with multiplication by a GF64 scalar, so the last elimination in Section3
cannot silently be reused for that larger class.

The exact checker verifies geometry, actual capacities/owners, all33
parameters, the additive graph, the readout identities and every exceptional
pencil. Positive controls use the same receiver twice and a distinct pair
with equal ratios; both retain a nonzero two-donor common row space. A
non-diagonal matrix A tests the source/readout identities beyond scalar
feedback. Negative controls alter the shared-port claim, parameter map,
and source readout coefficient and are required to fail.

Open next questions are to construct a multiple-gap source with compatible
entire fibre diagrams, or exploit explicitly binary-linear amplitude maps
outside the field-linear gate. Either needs the common D/K/facet word,
an affordable actual return, source and owner invoices, both strict
suppliers, and all remaining foundational/outer contracts.

Credit @CubeJerry and the S030 geometric-node, global seven-form,
polynomial-feedback and tight-cut authors, with their pinned notices.
S031 root derived the port gate and universal single-gap pencil argument.
Substantial OpenAI assistance. Separate independent review is required
before programme admission.
