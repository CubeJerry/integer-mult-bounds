# Independent review: point-retained handoff obstruction

**Accepted in the explicitly stated monotone, cocharted, point-only local
read interface. No complete source, tariff improvement, or new kappa.**

The exact reviewed proof hash is recorded in RESULT.json. During review the
author added an explicit clarification requested here: a stationary point
copy at `L_j` can be read only when the receiver itself is cocharted at
`L_j`, not merely at a containing chart. This is the physical premise used
by the one-point suffix argument. No further correction was required.

## Mathematical review

The decomposition into canonical-plus-supported contribution `A` and local
point contribution `B` is valid for arbitrary linear block operations. At
handoff, all public X rows belong to `W_T`, so `B` starts at zero. A read of
an actual `W_T`-valued nonreceiver contributes to `A`, while a stationary
source-line read contributes to `B`. Public interactions act on both parts
linearly. This remains valid if a nonreceiver previously read a receiver:
its actual X rows at the later read must still belong to `W_T`. Original
Y coefficients do not change this formal separation because the X and Y
inputs are independent. Arbitrary matrices, including singular and
noncommuting ones, preserve membership in the tensor code.

For `B`, a point source line remains contained in every later chart visited
by that contribution. Every transmission between public trajectories is
cocharted, and every trajectory is monotone upward. Therefore a final
receiver cannot have `B` contributions from its own source line or any
noncontact source line. At a good receiver outside `T`, the identity output
forces its canonical contribution to have identity own block and zero
noncontact blocks outside `T`. The diagonal-zero punctured-code distance
then makes that canonical contribution exactly `K_i tensor I`.

The all-field extension of this distance is correct. Expand the finitely
many value-field coefficients in an F2-independent basis. A zero coordinate
forces all binary constituents to vanish there, and their supports cannot
cancel across independent basis components. A nonzero internal coordinate
of an operator-valued row supplies the required scalar constituent. This
does not assume the matrix coefficients commute or are invertible.

The last incoming public interaction is the correct chronological cut.
Immediately before or during it, every point-local source contributing to
the chosen trajectory lies in that interaction chart. The chart lies in
the final facet of every participating physical trajectory, including a
different trajectory ending at `F_h`. All prior point contributions are
therefore supported on `S_h`. Later point reads lie on one upward nested
trajectory, which can coincide with at most one of the distinct source
lines. Hence at least `|S_i minus S_h|-1` contacts remain unavailable.
Self operations and outgoing reads do not import new `B` support; reads
whose actual X rows lie in `W_T` belong to `A` instead.

Whole chart/value relabellings do not defeat this argument: it follows the
physical trajectory ending at the chosen final facet. The one-point bound
would be false if a relabelling were interpreted as an uncharged geometric
jump or a remote point read. Neither is granted by the declared interface.
An arbitrary public downward turn is likewise outside scope.

Finally, twenty-four receivers have both `rho_i>=21` and `g_i>=21`. Every
set `T` with at most twenty indices omits one of them. At least twenty-one
canonical foreign contacts are then missing from `B`, and at most twenty
are supported by the exceptional component. One nonzero identity block
remains uncancelled, contradicting the required endpoint. This proves the
stated twenty-port exclusion and the necessity of at least twenty-one
supported innovations **within this interface**.

## Novelty and relation to the previous nineteen-port result

The canonical-distance, analytical separation, last-public-interaction, and
pigeonhole proof pattern already appears in `bit-code-decoder-robustness`.
The present theorem credits that dependency correctly. It should not be
described as a new proof of those underlying principles.

Its useful new scope is the actual retained-point handoff, whose stationary
local records sit at individual source lines. The last suffix can read
only one such record, giving new gaps twenty through twenty-five instead
of the older clean-cache-chain gaps. Combined with the same punctured
distances, these yield the twenty-port exclusion. It also states the
generalized actual-`W_T` read contract, so Y-bearing or receiver-dependent
records are covered when their actual X rows satisfy that contract. It
does not grant an unrestricted moving outside-code relay.

The new conclusion is useful even for a proposed fitting whose arrival
proxy passes: it excludes physical continuation from this particular
location/interface state. It neither prices additional records nor proves
that twenty-one ports suffice. The older nine-Hub tariff and its numerical
deficit are not transferred to the new handoff without another cost proof.

## Independent finite reconstruction and controls

`check.py` imports no author checker, row census, or WIP builder. It reads
the pinned rational native word, normalizes each source line to a primitive
integer vector, verifies all 111 lines are distinct and all 111 final
facets are the corresponding seven-dimensional perpendicular spaces, and
reconstructs the contact graph. A reversed canonical basis and Gray-code
traversal enumerate all 512 binary codewords independently.

The reproduced censuses are:

| Quantity | Exact histogram |
|---|---|
| Diagonal-zero noncontact distance | 18:7, 19:24, 20:52, 21:16, 22:11, 23:1 |
| Last-interaction gap after one point read | 20:4, 21:26, 22:47, 23:25, 24:8, 25:1 |

The checker reconstructs the exact twenty-four good receivers and all
threshold counts. Twenty is the largest excluded `|T|` certified by this
particular threshold-count argument; this is not an upper bound on the
true necessary support.

For every receiver it supplies a nonzero diagonal-zero canonical word
attaining `rho_i`. Deleting precisely that noncontact support permits a
different canonical contribution with the correct diagonal, demonstrating
why `rho_i>|T|` is strict. Canonical rows themselves demonstrate why the
zero-own-coordinate condition must be retained.

Two distinct contact source lines in one receiver facet give an explicit
rank-two mixed-bank geometry. One upward trajectory cannot directly visit
both lines. The geometric path `0,L_j,0,L_k` can visit both after a downward
turn and shows why public monotonicity is a real restriction. This is a
geometric scope control, not a claimed complete native source word.

The two candidate WIP bank supports are checked only as explicit sets:
their planes have rank three and are perpendicular, and their union with
`{0}` has thirteen ports. This makes the conditional seven-extra-coordinate
consequence correct. No uncommitted WIP source, its reported `ell=192`, or
its alleged decoder is admitted or reproduced by this review.

## Reproduction

```bash
python3 -I -B research/moonshot-005-program/results/bit-point-retained-handoff-gate/review-c/check.py \
  --native research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz \
  --author-proof research/moonshot-005-program/results/bit-point-retained-handoff-gate/author/PROOF.md \
  --programme research/moonshot-005-program \
  --output /tmp/point-retained-handoff-review
```

Expected status: `PASS_INDEPENDENT_POINT_RETAINED_HANDOFF_GATE`. Normal and
optimized Python runs produce identical JSON. The exact native and
predecessor proof hashes are in RESULT.json.

Both strict suppliers and all five foundations remain open. Actual mixed
banks outside `W_T`, richer histories, or paid public turns require new
source/endpoint/invoice arguments. Independent review by Worker C for
@CubeJerry with OpenAI assistance; predecessor credit retained. No human
or formal-kernel acceptance is claimed.
