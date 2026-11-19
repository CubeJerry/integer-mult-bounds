# Separate review of fully early H263 linearization

**Accepted within the stated finite-field, preservation, route and common-component premises. No new complete kappa.**

Reviewer: S028 Worker C, separately from the author. This review combines a
written mathematical audit with an independently written reconstruction of
the native owner and incidence data. The reviewer did not import or execute
the author's checker to obtain the verification result.

## Mathematical audit

Let the input be uniform on a finite vector space of dimension N=m ell.
An exact preserving map into m packets of ell field symbols is a bijection
onto the full Cartesian packet alphabet. A receiver whose linear target has
rank exactly its visible capacity has two observations with equal finite
cardinality. Exact target recovery therefore makes its visible packet tuple
and its target mutually determining, even if the encoder and decoder are
nonlinear. No assertion that a nonlinear encoder is literally linear is
needed.

For linear observations with row spaces W_i, a common function is constant
on each kernel and hence on their sum. It therefore factors through the
intersection of W_i. For coordinate observations of a full Cartesian
alphabet, a common function depends only on the common coordinates: every
coordinate outside the intersection can be changed while leaving one of
the observations fixed. These statements concern arbitrary functions, not
only linear ones.

For an isolated port D, apply the two facts in both directions. Its packet
and the observation with row space Q_D=intersection over its audience of
W_i are mutually determining. Hence dim Q_D=ell. The packet tuple is fully
independent, so the combined Q_D observation has rank N. Their dimensions
sum to N and they form a direct sum. Conversely, transmitting bases of
these spaces supplies an invertible linear encoder and recovers every
target by dimension equality. Thus the author proves an exact existence
criterion, including nonlinear encoders, under the stated premises.

The same argument for any receiver subset gives the exact intersection
dimension. Applying the actual one-port triple to identical repeated
width-d observations gives r times an integer equal to dr/15. Cancelling
r proves 15 divides d. Postprocessing or copy mixing after the source has
already emitted these observations cannot alter this input information
invariant.

For a common direct-sum decomposition of the targets into equal-width
components, intersections and the resulting Q_D spaces split componentwise.
The incidence equations A q=d_s 1 follow, with integer dimensions q. The
explicit mod-3 row weights annihilate every incidence column while their
sum is 16. Therefore 3 divides each d_s. This conclusion covers varying
uncoupled width-16 components; it does not cover arbitrary coupled sources
or gauges that remove the common decomposition.

## Native premise audit

The checker reconstructs the actual H263 donors 0,61,62; its 45 outgoing
D charts; all 90 genuine early fields; the absence of late fields; and the
two fields on each exit. It reconstructs the 33 joint-tight receivers, all
99 ordinary source views and their 16 relevant source planes. Every port
has a triple isolator. The explicit receiver triple 4,5,6 isolates D2835.

There are two distinct conditioning arguments in the physical application.
To require full H preservation, fix all other early inputs and use the
retained restoration of the original early X owners at Hub, with no
informative bypass. To require each receiver's local graph target, use its
tight invertible 16-quotient source view and fix the other visible
quotients; proper nested routing prevents invisible source quotients from
supplying another route to that receiver. These are compatible arguments,
but neither should be silently replaced by a claim that the original X
coordinates remain independently variable after arbitrary source maps.
The existing source-invertibility and inverse-fibre alignment prerequisites
remain explicit.

The only altered endpoint stars in the present target are receiver80 and
donor10. Neither occurs in these 99 blocks, so the identity-block premise
is retained by the new two-sided target repair.

## Independent computation and controls

The checker reads pinned layout and routes, not author-produced incidence
tables. It reconstructs all 5,456 receiver triples. Their intersection-size
histogram is 0:1648, 1:411, 2:3305, 6:92. The modular audience-weight sums
are 3 on 16 ports, 6 on 26 ports, and 12 on 3 ports, with total receiver
weight 16.

It independently checks the five nine-port classes as nonnegative integer
profiles of component width3, making the divisibility obstruction sharp
for this local integer feasibility question. This is not a proof of global
source realizability. A separate GF4 Frobenius relabelling checks all64
states: a nonlinear packet labelling can serve saturated linear targets
while retaining the theorem's linear-information structure. Thus the
argument correctly allows nonlinear encoders rather than inadvertently
assuming them linear.

Run:

```sh
python -B check.py --repo PATH_TO_PROGRAMME --author PATH_TO_AUTHOR --out NEW_DIR
```

Expected marker: `PASS_SEPARATE_FULLY_EARLY_LINEARIZATION_REVIEW`.

## Result and limits

The repeated width16 full64 source is excluded from this unchanged fully
early H263 continuation. Independently varying uncoupled width16 sources
are excluded too. The source-only covariant information-sufficiency theorem
is unaffected. A genuinely coupled quotient block of width240, or varying
blocks of width48 with a compatible common structure, passes only the
stated divisibility gates; actual inverse-fibre gluing is still open.

Changes to targets, informative bypasses, phase chronology, saturation or
source-component premises require another analysis. This review establishes
no global impossibility, supplier admission, physical cost improvement,
recursive theorem, new kappa, or discharge of foundational assumptions.

Credit: @CubeJerry and the cited native geometry, source, early-owner and
nine-port predecessors; Worker A for the theorem and explicit modular dual.
Worker C performed the separate review with substantial OpenAI assistance.
