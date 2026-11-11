# A causal information-arrival floor for a frozen-prefix shared core

Status: source-bound linear theorem, with independent review in `review/`.
No new kappa; no universal shared-core obstruction. All five selected foundational
assumptions remain. Source: `research/shared-wire-split-composition/data/final.json.gz`
at canonical `e54523517d0f03e58352e647c403a5af3e525a57`, SHA-256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.

## Model and proposition

Run two virtual copies of the pinned source with independent 400-field main
inputs x1,x2 and the same arbitrary 1080-field helper input h. Require both
physical main banks to equal their prescribed virtual prefix values at every
source event boundary, to follow the source main itineraries, and, crucially,
EVERY physical source-main MOVE to transport its literal virtual prefix row.
Temporary repurposing of these funded main MOVE payloads is excluded from this
fixed-route theorem; endpoint equality alone does not establish this premise. Local macros
may use any finite cochart linear operations and arbitrary extra fields; all
extra cross-chart information must arrive in real transported complete fields.
A normalized field is one scalar linear row on the entering complete arrays,
tensored with the identity on their arbitrary allowed complete-array dimension V.
A chart MOVE preserves its normalized row and costs a positive child rank r.
Free source rereads, uncharged cross-chart linear array services, and packing
several independent complete arrays into one field are outside this model.

Fix one source-independent scalar lambda. Suppose the single shared helper
bank uses a fixed-code MOVE payload: every source-helper MOVE transports
lambda times its current virtual copy-one row plus (1-lambda) times copy two.
In particular the shared helpers may not be temporarily repurposed as difference
carriers during those paid source MOVEs. Such repurposing is one of the explicit
escape mechanisms quantified below. Owned fields may be encoded arbitrarily; their source
MOVE routes are counted separately below. Let x_c=lambda*x1+(1-lambda)*x2 and
Delta=x1-x2. This change of entering variables is invertible for every lambda.
Grant the implementation all (x_c,h) information freely at every chart. After
quotienting by that granted common subspace, the coded helpers carry no Delta;
the physical main pair supplies precisely the one-source main rows obtained
by running the source on input Delta with all helper and owned inputs zero.
This grant only strengthens the implementation and is not a physical recipe.

The following optimistic relaxation has an exactly computable minimum number
D of fresh normalized-row arrivals. Every chart may retain unlimited immutable
copies of every row ever available there, at zero storage/scalar/erasure cost.
Give it every initial Delta-main row in its entry chart and every prescribed
Delta-main MOVE arrival for free. At a source ADD into a main field from an
auxiliary, require its current homogeneous auxiliary source row to be known in
that chart. A paid arrival may teleport ANY desired scalar row into ANY chart
for one unit, with no acquisition, route, timing, coefficient or rank restriction.

**Theorem 1 (causal arrival count).** For the pinned finite source, the minimum
number of arrivals in that relaxation is D=984 (equal-span chart IDs 1091 and 1092 are merged for free). Therefore any physical realization
within the stated fixed-prefix/common-helper contract needs at least D incoming
complete fields beyond its prescribed main arrivals. Granting all 47 original
owned MOVEs arbitrary useful Delta payloads still requires at least D-47 extra
arrivals. Every positive-rank extra MOVE has r^(199/200)>=1, so the same number
is a lower bound on its added paid moment. This remains true with arbitrarily
many stationary sidecars, arbitrary prefetching, coded deliveries, and unlimited
cochart scalar work.

## General proof of the causal-count lemma

At each chart maintain a greedy vector space B, initially spanned by its free
entry rows. Add every free prescribed main-arrival row to B. At each demand d,
add d to B; increment D only if this increases dimension. This gives an upper
bound in the teleport relaxation: import exactly d at each such increment.

For the lower bound, let K be the span of every row an arbitrary successful
implementation has ever had in the chart, granting permanent local retention.
After every demand, B is a subspace of K. Track e=dim(K)-dim(B)>=0 separately
at every chart. Initially e=0. Any extra delivery can increase e by at most one.
A free arrival is added to both spaces; its dimension increase in K is no larger
than in B because B is a subspace of K, so it cannot increase e. Local scalar
operations create no new row outside K. At a demand, K must contain d, so every
greedy increment decreases e by one. Thus each demand increment consumes one
unit of excess dimension previously supplied by a delivery. Summing over time
and charts gives D<=the number of deliveries. Arbitrary anticipatory linear
combinations and proactive deliveries are covered by this potential argument.

A demand need not be explicitly materialized by a proposed macro. If a source
ADD has nonzero coefficient c and changes prescribed main row a to a+c*d,
then the granted permanent local memory retains both rows. Their difference
divided by c yields d in K. Thus any correct cochart macro satisfying the frozen
main prefix induces the demand. Temporary in-place encodings do not evade it.

A MOVE of one complete field contributes at most one row at its destination;
the memory grant lets its source keep a copy. Equal-span charts can be merged
for free, giving a strictly more permissive relaxation if basis changes were
otherwise charged. Zero initialization conveys no input information. Erasure
cannot increase knowledge. The argument tensors with I_V and is therefore a
universal statement in V under the specified scalar-normalized grammar; its
source count is a finite exact rational certificate.

## Budget and structural implication

The existing H4 target profile allows added paid moment strictly below
1771183385103604616 / 18000000000000000 per native, which is less than
98.399076951 and, decisively, less than 99, when every other target/caller term
is unchanged. This exact upper endpoint is inherited from the independently
checked `research/shared-core-target-obligations/INVOICE-RESULT.json`, pinned in
SOURCES.json; it is not a newly recomputed supplier price. Therefore
at most 98 added positive-rank MOVE arrivals fit even before ordinary costs.
Granting all 47 original owned routes as useful information channels cannot
meet the constant-helper-code lower bound (984-47=937 before any rank>1 fee).

More generally, allow the source helper routes to carry difference information
by varying the shared coding weights or temporarily repurposing their physical MOVE payloads.
Each such helper arrival can contribute at most one row to K. With the same
frozen main prefixes, the relaxed necessary condition becomes

    useful helper arrivals + useful owned arrivals + extra arrivals >= D.

This formula still assumes literal main MOVE payloads. If those main routes are
also repurposed, add `useful nonliteral main arrivals` to the left. The relaxation
may grant the prescribed main rows anyway and count each actual nonliteral
arrival once; the same excess-rank argument remains a necessary inequality.
The resulting extra freedom can evade the 839-helper floor and is not excluded.

Consequently at least 984-47-98=839 source helper arrivals must contribute
usable difference information if that unchanged H4 budget and literal-main MOVE contract are to hold, even
after the most favorable 47-owned/98-extra grants. This is a necessary innovation
count, not a construction, and it does not say that every credited arrival can
actually be funded or made causally useful. Changed main-prefix information or
main itineraries escape the free-input list and require a new source analysis.

## What this adds and what remains open

The earlier endpoint floor only priced a final correction, and the fixed/switch
results excluded selected particular lifts. Here correction may occur anywhere,
stationary memory is unlimited, and ordinary scalar work is free; an exact
causal information count still excludes fixed common helper MOVE payloads with the prescribed
main prefixes. Role-dependent helper coding, changed main prefixes, changed
contact geometry, and a changed full invoice remain open. The theorem does not
exclude the programme's current changed-main-state direction.

Open next question: construct a changed-main-state schedule that lowers this
arrival obligation while realizing the same endpoint, or exhibit a causal
variable-helper code with the hundreds of required useful source arrivals,
explicit common-information preservation, and the full storage/transport invoice.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit the retained
selected native and #7000 authors and the programme's S001 capacity/coded-lift
packages. The potential argument is elementary linear algebra; the new result is
its exact source-bound causal delivery floor and fully delimited budget bridge.
