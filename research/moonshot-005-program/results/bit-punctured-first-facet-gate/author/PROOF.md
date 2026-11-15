# A punctured rank-nine witness and the first-facet feedback limitation

**Proved within the explicit normalization model; independent review pending.
No new κ.** This package gives an exact rank9V witness after removing native
port0, then applies the programme's existing spatial normalization in two
different ways. It rules out completing the remaining110 receivers with
eight terminal fields and only a first-facet singular cell. It also rules
out moving that feedback deeper when its entire new kernel information,
modulo local data, is still only x0. A new mixed kernel or a changed physical
interface remains an open construction route.

## 1. The actual110-port puncture has minimum rank9V

Fix the authenticated111 real native roots r_i, and retain roles
`I={1,...,110}`. For a field k and V>=1, a fitting is an I-by-I block matrix
A with V-by-V diagonal blocks I_V and A_ij=0 at every nonorthogonal foreign
pair. Blocks may be nonsymmetric, singular and noncommuting.

**Proposition1.** Every such fitting has rank at least9V over every field.
In characteristic two the exact minimum is9V.

The actual point frame

    [1,8,9,30,37,46,73,77]

has eight pairwise real-nonorthogonal roots and avoids0. The certificate
lists27 actual edge roles, also avoiding0. Each is real-orthogonal to exactly
its two incident point roles. Their underlying graph is K8 minus the edge
between point indices0 and2; its degrees are

    6,7,6,7,7,7,7,7.

Every two edge roles whose edges meet at a point are real-nonorthogonal.
Thus all zeros needed by the star argument are actual fitting zeros on
these35 retained roles. No abstract graph is substituted for the native.

Here is the credited star rank argument, rederived to expose its hypotheses.
Factor the35-role principal fitting at its actual rank r=8V+j. The point
principal block is I_(8V), so j>=0 and a factor-basis change makes the eight
point factors coordinate projections/inclusions. An edge e={a,b} then has
factors only in point blocks a,b and a complementary j-dimensional space.
Write alpha_e(a),alpha_e(b) for its two point-block products and S_e for its
complement product. The diagonal identity is

    alpha_e(a)+alpha_e(b)+S_e=I_V.

Set gamma_e(a)=alpha_e(a)+S_e, g_e(a)=rank gamma_e(a), and
G_a=sum_(e incident a)g_e(a). At a fixed point a, restrict incident edge
factors to the V+j coordinates `a,last`. Their product is block diagonal,
because distinct incident edges are noncontacts; its diagonal blocks are
gamma_e(a). If ell,rho are the stacked row/column ranks and lambda_e,mu_e
their individual ranks, the kernel inclusions and Sylvester inequality give

    lambda_e-g_e(a) <= ell-G_a,
    mu_e-g_e(a) <= rho-G_a,
    ell+rho <= V+j+G_a.

Also alpha_e(a)=I-gamma_e(b), so lambda_e and mu_e are each at least
V-g_e(b). Combining yields the prior star inequality

    G_a+V <= j+2(g_e(a)+g_e(b)).

Sum over both ends of all edges. Then

    sum_a(degree(a)-4)G_a <= 2·27·(j-V).

The left side is nonnegative. Hence j>=V and r>=9V. The full110-role fitting
has at least the rank of this principal submatrix. This proof works over
every field with arbitrary block factors; no divisibility or commutativity
assumption is used. It is the rank-floor application of the star inequality
credited in the programme to DreamingOfClouds, CrocSwap/integer-mult-bounds
#7114, and the independently admitted saturated-star package.

For characteristic-two attainment, restrict the canonical native K9 fitting
to rows/columns I. Exact elimination gives rank9. Its binary identities and
nonzero minor persist over every characteristic-two extension, and tensoring
with I_V gives rank9V. This is stronger than a generic rank-lowering estimate
from deleting one port: the actual puncture still has the complete9V floor.

## 2. A sole singular terminal facet cannot supply the other110 receivers

Use the precise monotone source-packet model of the admitted
`bit-y-feedback-normalization`: original X records ascend from their native
lines, original Y records ascend from ground to their distinct native
facets, and q persistent width-V packets descend from Hub to ground. Local
linear blocks can be arbitrary and noncommuting. Stationary zero-born
helpers and properly acquired ascending helpers introduce no independent
input. No extra descending channel, packet restart, nonlocal birth or
nonnested movement is granted. Every physical expense remains owed.

At a proper nonzero chart C aggregate the actual chronological operations
using formal boundary-arrival variables. Its entire packet-through matrix
D_C is square. This is the full joint matrix, not one selected diagonal.
Let Z_p be each actual packet's first-ground-arrival value, before arbitrary
later ground mixing. Each Z_p has width V and can contain arbitrary y.

**Proposition2.** Suppose D_C is invertible at every proper nonzero chart
except possibly F0. If all receivers in I are completed, then q>=9.

For every proper chart C other than F0, the existing spatial induction
gives

    H_C = Lambda_C Z + E_C y + B_C x,

where B_C has original-X support only on lines contained in C. Indeed its
proper predecessors and packet successors have smaller dimension and thus
are not F0. Ground histories are generated by Z and arbitrary original y.
Invert D_C to reconstruct packet arrivals from departures and ascending
inputs, then substitute the lower-chart identities. Local X supports remain
inside C. F0 itself is excluded from this induction; nothing is asserted
about the missing kernel information there. This is a restriction of the
credited spatial proof, not a new claim that chronology can be rearranged.

For i in I, F_i differs from F0 and is a proper chart. Taking the X part of
the completed output identity gives

    e_i tensor I_V = Lambda_i Z_x + B_i.

The row A_i=Lambda_i Z_x has own block I_V and zeros at every forbidden
foreign contact. Restricting its input columns to I gives a fitting on the
110-role puncture, of rank at most qV. Proposition1 forces qV>=9V.
Independent y symbols affect additional endpoint equations; they add no
X-information rank and have not been assumed zero in the execution.

This statement permits arbitrary seeds, ordering, invertible intermediate
mixing and original-Y feedback within the stated cell condition. It does
not exclude a new singular cell below a facet, a new paid channel, or a
legitimate change of model. Merely improving seeds of an eight-packet word
with its sole singularity at F0 cannot complete the other110 outputs.

## 3. Point-kernel information at arbitrary depth is still insufficient

The deeper version needs a distinct hypothesis. At each singular chart C,
let T_C be its actual kernel coordinate in the admitted inverse-cell identity

    P_in = R_C(P_out-N_C U_in)+J_C T_C.

Suppose its actual X/Y coefficient decomposition has the form

    T_C = M_C x0 + L_C x + E_C y,

where every nonzero input column of L_C has source line contained in C.
There is no restriction on M_C, E_C, kernel dimension or block commutation.
The charts need not be facets. The hypothesis concerns actual historical
coordinates, including local translations, not a guessed scalar nullity.

**Proposition3.** In this model, completing all receivers in I again requires
q>=9. In particular q8 cannot be completed using only such kernels.

In the spatial induction substitute the displayed form of T_C into the
inverse-cell identity. Include the single raw input x0, of width V, in the
global algebraic information tuple along with all Z_p. Absorb J_C L_C x
into the chart-local remainder and J_C E_C y into the nuisance y term.
Both operations preserve support inside C. The same induction therefore
normalizes every proper-chart history using `(Z,x0)`, arbitrary y and local
X. This is a lower-bound relaxation; x0 is not a free physical read.

At the outputs the resulting fitting factors through `(Z_x,e0 tensor I_V)`.
After deleting input column0, the e0 term vanishes. Restricting to receiver
rows I yields a110-port fitting of rank at most qV, contradicting
Proposition1 for q<=8. The proof is uniform in all positive widths and does
not replace noncommuting block products by scalar coefficients.

This local-translate formulation is essential. The value immediately before
an interior feedback operation may be x0 even though the full chart's
incoming packet is x0 plus a cache read later inside that chart. The latter
is the formal boundary coordinate. It can be replaced by x0 in normalization
only after proving the difference chart-local; this package checks that
condition on the recorded deeper probe. Merely observing an interior x0
without this compatibility check would not justify the corollary.

The same proof holds for a specified input set E if all kernel coordinates
are E-supported modulo their respective local data, and the E-punctured
native has fitting floor greater than qV. Only E={0} is certified here.
No claim about the minimum size of such an E or a universal source obstruction
is made.

## 4. Exact frozen-word access certificate

The frozen h9 colored source has eight terminal rows and its only actual
singular cell at F0. An independent literal replay records every nonhub
packet observation, including all222 original input columns. For each i!=0
and every packet observation P_q(t) at a chart contained in F_i, the checker
verifies the exact congruence

    (P_q(t)-T_q)_X is supported inside F_i.

There are2814 checked receiver/observation congruences. P0's sole exceptional
cell precedes every chart it can visit inside another receiver's facet.
After that cell its observations differ from its terminal by later local
cache increments and a nuisance y0 term. Other packets are additive throughout.
All actual raw and point cache values are local to their source charts.

Granting all terminal values, all compatible historical observations,
every original X input local to F_i, and every original y symbol still
allows only the following11 of the other110 receiver fittings:

    8,14,19,22,30,35,38,59,66,69,110.

Each of the99 remaining roles has an explicit binary dual input d with
support outside F_i, own coordinate one, and zero pairing with every granted
X-dependent observation. For arbitrary characteristic-two k and width V,
multiply d by any nonzero vector in k^V. It gives two inputs with identical
granted observations but different requested x_i. Thus even nonlinear
postprocessing of this enlarged frozen observation set cannot recover that
receiver. This finite, exact dual certificate is distinct from the universal
block-rank proof for changed seeds.

Receiver0 is an essential positive control: its full accessible history fits
while its terminal space does not. Its actual completion was independently
verified in the source review. Applying the terminal congruence to F0 itself
would be false. The deeper probe is a second scope control: depth changes
geometric access, but its independently checked kernel entry differs from
x0 only by a local form, so Proposition3 still applies.

The frozen observation exclusion permits free read-only taps and arbitrary
monotone ascending decoder processing. It does not permit changing packet
or source-cache histories, adding new packet/Y feedback, or introducing a
new descending export. Such changes must be recomputed against the actual
joint through matrices and kernel representatives.

## 5. Verification, dependencies and consequence for the programme

```sh
python3 -B check.py --repo /absolute/path/to/integer-mult-bounds \
  --word /absolute/path/to/colored-eight-source/output/COUPLED-WORD.json \
  --deep-word /absolute/path/to/deep-feedback-source/WORD.json \
  --out /absolute/path/to/first-facet-output
```

Expected status: `PASS_PUNCTURED_NINE_AND_FIRST_FACET_LOCALITY`.
The optional deeper word is checked only for its exact kernel entry/interior
and chart-local difference; it is not admitted as a complete source by this
checker. The fully audited colored source remains a valid partial result.

`output/RESULT.json` contains the actual27-edge star, all incidence checks,
all110 projected spaces,99 all-field dual inputs, the exceptional-facet
positive control and the deeper local-translate check. Source and theorem
pins appear in `DEPENDENCIES.json`. The checker imports no author code.
Its rejecting controls invalidate a star with a deleted point, a false
terminal value and the extension of normalization to the exceptional facet.

The nearest constructive requirement is therefore precise: an eight-packet
completion must create a physically acquired nonterminal kernel whose
normalized X part cannot all be absorbed into x0 and its own chart-local
inputs, or legitimately alter another premise. Moving a pure-point feedback
cell deeper does not meet that requirement. A mixed kernel must still meet
the actual proper-cover and complete movement/ordinary/ownership invoice;
passing this necessary gate would not establish a supplier.

The stronger existing target-wide rank gap remains in force. The admitted
`bit-uniform-rank-gap` theorem gives rank at least
`9V+ceil(V/3)` when the actual fitting has ell-charge at most196. Therefore
the retained target-arrival model with q8 requires total kernel dimension
at least `V+ceil(V/3)` even for genuinely mixed kernels. A single width-V
kernel cannot complete the target invoice. This package does not replace
that theorem or claim that one mixed cell would suffice. Its added content
is the exact110-port puncture, the first-facet locality restriction and the
point-kernel exclusion independent of that target charge bound.

Credit @CubeJerry; DreamingOfClouds's #7114 star inequality; the programme's
native rank-nine, saturated-star, source-scattering and Y-feedback-normalization
authors and reviewers; Worker A's colored source and deeper feedback probe;
Worker C's exact punctured star, restricted normalization, local-translate
corollary and independent controls. Substantial OpenAI assistance. All five
foundations remain; no new conditional or unconditional κ is established.
