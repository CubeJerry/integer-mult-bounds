# Independent review: four-edit protection is uniform and the count is sharp

**ACCEPT.** The theorem strengthens the prior two-edit propagation guarantee
to four arbitrary linear quotient edits, conditional on the stated complete
source cuts. The five-edit counterexample establishes sharpness for precisely
that source-cut theorem. It is not a compatible H word or physical invoice.

## 1. Universal proof audit

The normalized geometric fibre core has basis

    1, z+a, D_(3,a), D_(7,a), D_(13,a)+D_(4,a), D_(15,a).

Its six distinct leading degrees are 0,1,3,7,13,15. The admitted Moore-coordinate
identity identifies this basis with the span of all geometric inverse fibres
at node a. It remains a six-dimensional space over every coefficient extension.

The crucial new identity is exact:

    D_(15,a)+a²D_(13,a)=z^15+a z^14.

Multiplication by z+a reduces it to cancellation of the two a^16 terms.
After quotienting out the eight-dimensional space of polynomials of degree
below eight, each core contributes one D13 class plus the common two-space
spanned by z14 and z15. Thus r distinct cores span at most r+10 dimensions,
with the ambient cap sixteen. For one core use dimension six; for two use
the independently admitted intersection span(1,z), giving dimension ten.
The resulting bounds for one through five cores are 6,10,13,14,15.

For an actual receiver, use its old invertible geometric view as coordinates.
Every unchanged off-H observation vanishes on the new off-H fibre. Therefore
only the old H block and edited visible blocks can contribute. All such
inverse blocks lie in the one fixed envelope W formed by the cores at H and
the edited nodes. Taking a sum over any number of receivers keeps it in W.

Every considered receiver also sees R. Hence the propagated sum lies in
W intersect ker F'_R. The subtraction of one full quotient width is justified
in both cases:

* If R is unedited, constant polynomials lie in W and its evaluation is
  surjective on that copy of the amplitude space.
* If R is edited, a new inverse-R block from any one of the assumed invertible
  source views maps isomorphically to the R output. Its unchanged coordinates
  vanish, so it lies in the old edited-block envelope, and therefore in W.

An empty receiver family is trivial. Thus the R restriction has full rank k
whenever it is needed, and the propagated sum has dimension at most dim W-k.
With m edits other than H this gives 5k,9k,12k,13k,14k for m=0,1,2,3,4.
The proof covers arbitrary matrices mixing all k amplitude coordinates and
every actual receiver subfamily. No random-rank or genericity premise enters.

The statement about whole-bank coordinate changes was made explicitly linear
during review. Output bijections preserve the original information fibres;
arbitrary nonlinear input bijections do not automatically preserve linear
propagation ranks and are not admitted by this theorem.

## 2. Independent exact reconstruction

The checker imports only authenticated S030 independent field/root primitives,
reads raw native geometry, and treats the five-edit source rows as literal data.
It imports no author source constructor or S031 checker, and it does not use
the author's saved inverse fibres to compute ranks.

It separately verifies the 28 core identities, all 756 ordered two-core ranks,
and representative sharp core-envelope ranks 6,10,13,14,15,16. These finite
checks authenticate the geometric premises and examples. The uniform theorem
comes from the algebraic argument above, not extrapolation from those ranks.

The actual scalar source at donor 0 changes exactly nodes 0,3,5,7,8. Using
the global labels, these are planes 806,854,293,283,13. Every one of its 63
actual geometric source views has rank sixteen. At H17 (node 10) and R806
(node 0), the checker independently solves the fifteen off-H equations for
each of the fifteen native receiver indices

    1,7,10,11,12,48,55,56,73,81,90,95,96,97,102.

The resulting fifteen fibres are independent and are all annihilated by the
actual edited R row. They therefore span its complete fifteen-dimensional
kernel. Removing one receiver lowers this rank to fourteen. Restoring the
unedited geometric source on the same receiver set gives propagation rank
five, a control on both the native incidence and the changed information.

The witness uses scalar coefficients in GF64. Tensoring every source row
with I_k preserves all source cuts and raises the propagation rank to 15k.
Field extension also preserves these exact ranks. Hence a universal strict
five-edit guarantee under only the theorem's source-cut assumptions is false
at every positive width. This does not claim that every five-edit source
saturates, or that the counterexample has compatible H providers.

## 3. Constructive consequence and scope

The already admitted two-H component has at most two edits per donor. Its
uniform propagation guarantee improves from 42 to 36 at width three for
two-edit donors, and from 30 to 27 for one-edit donors. Up to four edits can
retain strict protection if source cuts remain full, creating room for coupled
anchor changes. The separate joint-translation obstruction must still be
checked: avoiding saturation does not ensure common source fibres or readouts.

The theorem concerns linear source edits and rank propagation. It introduces
no price per edit, free computation, global continuation, D/K/facet map,
return-excess bound, strict supplier or multiplication exponent.

Replay:

    python -I -B research/moonshot-005-program/results/bit-shared-h-s031-construction/four-edit-protection/root-review/check.py --repo . --out FRESH

Expected: PASS_ROOT_FOUR_EDIT_PROTECTION_AND_SHARPNESS_REVIEW 63 15 5.

Root, S031. Separate model-assisted proof review and native reconstruction;
not human peer review or formal-kernel acceptance.
