# One packet cannot restore the root-2 endpoint in this fixed interface

Prepared for @CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.
The source construction and open lead are DreamingOfClouds' PR6144, pinned at
`4f3b67e7c37ae270da9584033132866d0cf63e42`. This note concerns that exact word,
not the selected frontier or an unrestricted lower bound for P104 circuits.

## Frozen source and the question

All event numbers are zero-based indices in the pinned source program. A cut
`i` means the state immediately **before** source event `i`; after deleting an
event, its original index still identifies its cut. In the source, owned
register 772 contains a packet `v` after event 13483. It follows the path
`529 -> 520 -> 737 -> 595`. Register 451 reads register 228 at frame 737 and
then reads `-4` times register 772 there. The proposed direct path for 451 is
`3 -> 595 -> 738 -> 911 -> 127`.

Let `x` be register 228's value at cut 12918, and let `v` be register 772's
value just after event 13483. The question is whether one replacement packet,
combined with arbitrary free linear recoding at the proposed contacts, can
restore the **complete final endpoint**. Intermediate values are allowed to be
wrong and to propagate through the fixed outside program; there is no premise
that a recipient must be corrected before its next use.

Define the packet-free comparison program **B** by these exact edits:

1. Delete `COPY 772 <- 146` at event 13481, so 772 stays zero after its INIT.
2. Delete all nine ADDs whose source is 772, at events 13485, 13487, 13489,
   13490, 13614, 13615, 13616, 13617 and 13618.
3. Delete `451 += 228` at event 12918.
4. Change 451's MOVE at event 12913 from `3 -> 737` to `3 -> 595`, and its
   MOVE at event 14523 from `737 -> 738` to `595 -> 738`.

Every other opcode, scalar coefficient, source event order and frame path is
fixed. B is an information-flow comparison program, not a proposed supplier or
a successful endpoint construction. In particular, it deliberately deletes the
information whose replacement is being studied.

## A two-coordinate certificate

Restrict every formal input to zero except the independent initial values of
main input registers 0 and 8. Write a field's two coefficients as `(a,b)`, meaning
`a X_0 + b X_8` on this restricted input. Equivalently, give every other one of
the 797 other formal coordinates (768 public inputs and 29 owned slots) freely to the proposed replacement. This is a
relaxation: a construction correct for arbitrary inputs must also work on these
two input columns.

The exact replay certificate establishes:

- At every cut of the **entire** 22,818-event source timetable, including the
  initial and final cuts, every field of B at any of frames **3, 595 or 738**
  has projection `(0,0)`. This includes register 772. The primary enumerates
  7,283,846 field-at-cut observations; it does not inspect only packet-read
  events or selected snapshots.
- The original source has `v = (1/4,-1/4)` and `x = (1,0)` in this projection.
- The original source has the prescribed endpoint on both input columns.
  Let `D = prescribed endpoint - endpoint of B`. There are 79 nonzero rows of
  D. Its rows 112 and 144 form the exact minor

  `[[1/2,-1/2],[0,-1/2]]`, whose determinant is `-1/4`.

Thus D has rank two. These are exact rational coefficient identities, not
sampled numerical inputs. The simple functional `ell(a,b)=a+b` annihilates
`v` but takes value 1 on `x`, giving an intuitive distinction between the
information carried by the old packet and by the removed 228 read. The theorem
below uses the full final residual, not an obligation to preserve those
intermediate values.

## Allowed replacements and the rank-one obstruction

The following model deliberately allows more free recoding than the literal
edit would normally have:

- All original fields keep B's paths and outside-event timetable, including the
  declared changed path for 451.
- At every reference cut, arbitrary rational scalar linear recoding among fields
  at frames 3, 595 and 738 is allowed. All such fields, not only the originally
  changed recipients, may mix. Free copies, rescalings and auxiliary linear
  storage initially equal to zero are allowed, as are all the other 797 formal
  input coordinates for free. This does not add an independent read at another
  frame or change which reference fields are available at a contact.
- One **fixed** packet `q` may be chosen arbitrarily. To strengthen the
  relaxation further, arbitrary additive injections `field += a*q` are allowed
  into any field at any time, with arbitrary rational `a`. Its construction,
  delivery and repeated use are free in this information argument. The packet
  is not restricted to combinations of the six holders at frame 529.
- Apart from those recodings and additive injections, outside instructions are
  unchanged. Outside fields may carry and propagate the resulting deviations;
  they are not assumed to retain their old values. No changed outside
  coefficient, new independent source read, new frame contact or second
  independently chosen packet is supplied for free.
- Success means the prescribed complete final endpoint, on arbitrary inputs.
  No intermediate first-use or restoration deadline is imposed.

The reference path of the zero packet carrier 772 is only bookkeeping here:
global free injections already relax every cost and timing constraint on delivery
of its one fixed packet. The obstruction therefore does not follow from requiring
the real carrier to retain the stage one hopes to remove. The ordinary receiver
paths, however, remain those of B; in particular, 497's path has not been
recharted by this theorem.

The word **additive** in the packet-injection rule is essential. Overwriting an
outside field with nonzero reference projection by `q` would also subtract the
old field, thereby introducing another input direction. Such an overwrite is
not a free operation in this model. It is harmless at a reference-zero recoding
contact. The actual replacement of 772's deleted COPY is included: B's 772 is
zero when the replacement packet is loaded, so loading `q` there is additive.

**Claim.** No replacement in this model can restore the complete endpoint.

**Proof.** Let `q_bar` be the projection of the fixed packet on `(X_0,X_8)`.
Compare the replacement's state with B. Initially their difference is zero.
Every fixed outside instruction is linear, so it maps deviations in
`span(q_bar)` to deviations in the same space. This includes the retained
COPY, INIT and CLEAR semantics. An additive injection of any multiple of the
one fixed packet also preserves the statement.

At an allowed recoding contact, B's projected fields are all zero by the
certificate. Hence every currently available projected field of the replacement
lies in `span(q_bar)`. Any rational linear mixing, copying, rescaling or storing
of those fields remains in that span. The 797 freely supplied other coordinates
have zero projection and cannot enlarge it. This proves the invariant by
induction over the complete finite outside timetable and any finite number of
interleaved allowed recodings. In particular, changes can propagate through
outside fields and later return: the fixed outside instructions preserve their
one-dimensional deviation space.

Consequently the correction matrix at the final endpoint has all its rows in
`span(q_bar)` and has rank at most one, including when `q_bar=0`. Restoring the
prescribed endpoint would require this correction matrix to equal D, whose
explicit minor has determinant `-1/4`. That is impossible. **End of proof.**

This rules out arbitrary packet coefficients, arbitrary coupled recoding in the
entire three-frame region, and later compensation through the unchanged outside
program. It is not merely failure to solve for one packet such as `v-x/4`, does
not retain the old receiver coefficients, and does not require restoration
before an intermediate read. It remains a fixed-path, scalar-linear interface
result, not a lower bound for arbitrary native circuits or arbitrary changed
outside programs. In particular, q is one uniform scalar-linear coefficient
row, not an arbitrary coordinate-dependent native encoder. A new such encoder
or decoder would change the model and must be priced and checked separately.

## Complete local cost screen for an extra paid repair

The original path-rank lists relevant to dropping both staging points are

- 772: `[1,2,3]`;
- 497: `[3,3,1,2]`;
- 451: `[4,2,1,2]`.

The optimistic direct paths would replace their combined list by
`[6,1,6,2,1,5,1,2]`. Both lists have total rank 24. Writing `H_r=r^(1-C)`,
the corresponding **new minus old** paid profile is

`-2 H_2 - 3 H_3 - H_4 + H_5 + 2 H_6`.

This is only an optimistic invoice: it does not provide the missing information
flow. The paired direct-path invoice also changes 497's path; it is a separate
cost screen, not an assertion that this larger change falls inside the fixed-path
model of the rank theorem above. Its integer concave-order gain hinges at ranks 1 through 6 are
`[3,6,7,5,2,0]`, so the declared raw invoice is favorable for every `0<C<1`.
The unchanged complete caller repeats a local invoice 18 times; at unchanged
productive targets the optimistic paid count would be 66,708 rather than
PR6144's 66,762. This count is not a feasible construction claim.

There is nevertheless a useful uniform bound on what this local invoice can
pay for. For integer `r>=1` and `0<=C<=1`, concavity in `r` gives

`r^C <= 1+C(r-1)`.

Therefore

`r^(1-C) >= r/(1+C(r-1)) >= r-C r(r-1)`.

Each old paid term is at most its rank. Since old and optimistic new rank masses
agree, their saving is at most

`C * sum_new r(r-1) = 84 C`.

Over the currently admitted BIT range `0<=C<=17/5000`, this is at most
`357/1250 = 0.2856`. For dropping only frame 737 and using 451's direct path,
the new rank list is `[1,5,1,5,1,2]`, the equal old/new rank mass is 15, and
`sum_new r(r-1)=42`. Its saving is at most `357/2500 = 0.1428`.

An additional **uncredited positive-rank call per local replacement** costs at
least 1 throughout this range. Consequently it exceeds either entire optimistic
local saving. Repeating that local repair in all 18 caller invocations multiplies
both sides of the losing comparison by 18. Productive targets, helper credits,
caller query/idle charges and the remaining local profile are held fixed in
this comparison.

The information obstruction does **not** prove that a second information channel
requires a new paid call. Existing paid work might carry it after a different
rerouting, or a new construction might change productive credits or other costs.
A shared global repair across invocations, changed outside paths, and a different
consumer boundary also lie outside this local cost screen. No such expense is
silently treated as zero, and no universal cost barrier is claimed.

## Scope, evidence and remaining questions

The finite replay establishes the source-bound two-coordinate invariant. The
written linear-induction argument extends it to all finite rational recodings
in the declared model. Neither is a proof-assistant verification of the complete
integer-multiplication theorem. The five inherited framework assumptions remain;
there is no new native supplier, materialized uniform word or rounded multiplier.
**No new kappa.**

The fixed paths and the region where arbitrary recoding is allowed are material
restrictions. A different construction could change outside instructions, visit
another frame that supplies an independent direction, or carry another packet
using a changed existing route. Those possibilities are not excluded here. The
practical handoff is to name and price that new contact or outside-program
change before repeating a one-packet resynthesis in the same three-frame
interface. Merely allowing the intermediate values to be wrong and propagating
those errors through the unchanged outside program does not evade this result.

Credit DreamingOfClouds for PR6144 and its root-2 lead, PR6143 and the selected
PR6030/PR5907 lineage; Ali Romman for PR5827 and the retained local/native/caller
contracts; @CubeJerry's PR6145 for the independent integer-dyadic replay used
during exploration; Matarener and Clear1nsight for independent replay/native
precedents; and the repository's retained contributors. The classical rank-one
information argument and concave tariff inequalities are not claimed as new
mathematical methods. The contribution is their exact application to this frozen
open contact-removal question, with explicit witnesses and limitations.
