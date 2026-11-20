# Independent review: geometric and gap15 sources fail the shared native port

**Accepted within the stated field-linear source-gauge scope.** The shared-node
geometric tensor source and every single-gap15 matrix-feedback source fail the
exact H263 identity-target cut after arbitrary separate GF64-linear whole-bank
gauges. The result holds at every positive admissible width and over all finite
coefficient extensions. H processing, quotient-output relabelings and downstream
decoders may be nonlinear. Arbitrary merely binary-linear input gauges remain
outside the theorem.

This review separately reconstructs the finite geometric facts and checks the
all-width proof. It does not infer a theorem from testing a few matrix sizes.
No new complete kappa or return-excess lower bound follows.

## Independent reconstruction

Reproduce from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 python -I -B research/moonshot-005-program/results/bit-geometric-gauge-port-gate/review-c/check.py --repo . --out FRESH
```

Expected output:

```text
PASS_INDEPENDENT_GEOMETRIC_GAP15_PORT_GATE 99 28 33 108 26 49
```

The checker imports no author or predecessor executable code. Its arithmetic
and exact lattice-coordinate methods are copied from this worker's separate
S031 feedback-partition checker, which credits the earlier independent Hermite
review. It constructs the polynomial

    L_v(z)=v z^8+v^2 z^16+v^4(z^14+z^5)+v^8 z+v^16 z^2+v^32 z^4

directly, divides L_v(z)+L_v(c) by z+c, and checks the remainder is zero. For
all99 actual donor/receiver incidences it compares this result to v^2 times
the independently multiplied fifteen-root annihilator. Thus the geometric
formula is tied to the literal source quotient information, rather than
accepted merely because an abstract parameter table has the right size.

The literal root table and lattice basis reconstruct the120 nonsingular root
labels and all perpendicular relations. H263 is exactly {0,61,62}, has node49,
and has33 native receivers, excluding80. The original-owner route stream gives
30 early slots per donor,720 fields at bank3840,45 exits of16 fields each and
240 fields visible to each relevant receiver. D108 is an actual exit seen by
both5 and7.

The parameter maps from donor0 to61 and62 are recovered using binary basis
extension, without the author's field-linear solve. Both are invertible on
all64 binary vectors. Their33 native parameter pairs agree, and the additive
graph has33 vertices and276 edges and is connected. The six-dimensional
polynomial core is independently checked to be injective and binary-linear.

For every one of the28 allowed nodes, the checker finds and records a nonzero
six-square minor at the unique potentially singular scalar pencil. It also
checks all three readout identities: the constant derivative term, cancellation
of the linear feedback term, and cancellation of the quadratic feedback term.
The proof only needs node49; checking the other27 nodes authenticates the
stated broader finite fact.

An additional control uses a3 by3 Jordan matrix whose diagonal is exactly the
exceptional scalar (1+49)^(-1), with nonzero superdiagonal entries. This forces
both the exceptional eigenvalue and nonsemisimple coupling. The resulting
48 by18 core still has rank18, and all33 derivative readouts agree. Kronecker
products involving this nonbinary matrix use actual GF64 multiplication.

Finally the independent derivative ratios at receivers5 and7 are26 and49.
Using a separate invertible triangular amplitude matrix, their two-donor row
spaces have union rank6 and hence zero intersection. The equal-ratio pair4,7
has union rank3, giving a positive control. A duplicated pencil column lowers
its certified rank from6 to5, and an incorrect receiver fails the D108
containment test.

## Why the all-width pencil argument is sufficient

For gap15, the monic off-H polynomial has top coefficient1. Its feedback
correction is therefore c_v tensor A, where c_v=(z+c)g_v modulo z^16+1.
Multiplying by v^2 yields precisely

    E=(U_c tensor I_k)+(N_c U_c tensor A),
    N_c=J_z+cI.

There is no unaccounted noncommuting product here: only one arbitrary matrix
A acts on the amplitude coordinates, and all polynomial coefficients are
field scalars. Since J_z has only eigenvalue1, I+tN_c is invertible except
possibly at t=(1+c)^(-1). The exact exceptional minor proves the restricted
16 by6 pencil remains injective there. It is therefore injective for every
scalar over the algebraic closure. Triangularizing A and using the injective
diagonal blocks proves the rectangular tensor pencil injective at every k,
including nondiagonalizable A. Descent preserves this rank statement.

The central quotient calculation includes terms in I,A,A^2. The two independent
zero coefficient identities remove A and A^2, leaving the stated derivative
scalar times I. Thus the amplitude readout is genuinely unchanged by every
allowed gap15 feedback matrix, rather than observed unchanged only for the
tested matrix.

## Relative gauges and the shared-port contradiction

An exact identity target with a tight additive cut first forces the donor
inverse-fibre spaces to coincide in original-input coordinates. Applying two
independent field-linear bank gauges therefore induces a linear isomorphism
between the two six-dimensional tensor diagrams. It may mix every source block
and every amplitude coordinate; the argument does not assume block-diagonal
gauges.

On a binary parameter triple v,w,v+w, the two distinct parameter lines are
independent over the coefficient field. Injectivity of E then forces the three
amplitude matrices to agree. Connectedness of the actual native parameter
graph propagates that agreement to all33 receivers. This proves the single
receiver-independent invertible amplitude map used in the author proof.

The output aggregate for a receiver is determined by the same H input tuple
after a fixed invertible change of each donor's amplitude coordinates. For
receivers5 and7, the differing scalar ratios already force zero intersection
using just donors0 and61. The third donor cannot restore a nonzero common row,
because any common three-block row would restrict to a common two-block row.

For each receiver, fixing the other source observations still lets the H
input tuple range over its full product alphabet: the complete16-quotient
source views are invertible. Its required aggregate has exactly the cardinality
of its visible H transcript. Exact recovery therefore makes that transcript a
bijection of the aggregate, so each visible exit is a function of the aggregate
and has its full positive alphabet. These conclusions hold on the same entire
H-input domain for both receivers, even though their fixed external
observations differ. A function of both linear aggregates is invariant under
the sum of their kernels. The zero row-space intersection makes this sum the
whole domain, so the common D108 exit must be constant. Its positive full
alphabet contradicts that conclusion. Nonlinear H encoding cannot repair it.

## Extension scope and explicit limits

The final author proof includes the requested restriction-of-scalars
clarification. A finite extension F/GF64 of degree m replaces an arbitrary
A in M_k(F) by a km-square GF64 matrix. All nodes and derivative ratios remain
in GF64. The argument therefore permits arbitrary GF64-linear mixing of the
extension coordinates, not merely F-linear gauges. Merely F2-linear gauges
need not commute with those scalar ratios and are correctly left open.

The theorem excludes the entire stated gap15 family, not just its example
matrix. It does not exclude multiple-gap feedback, altered node information,
different source preprocessing, paid additional channels, changed targets or
the still-open binary-linear-gauge route. No foundational assumption is
discharged. The full supplier and recursive accounting remain separate.

Credit @CubeJerry and the source authors retained by the author package. S031
Worker C independently checked this result with substantial OpenAI assistance;
this is independent agent review, not human or formal-kernel verification.
