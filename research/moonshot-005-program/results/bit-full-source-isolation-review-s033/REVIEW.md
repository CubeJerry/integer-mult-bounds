# Independent review: full-source receiver-95 isolation obstruction

**Accepted with literal H interface actions as an explicit premise.** The
receiver-95 obstruction survives arbitrary separate linear source recoding of
all 480 coordinates, arbitrary compatible changed D words, and invertible
rebasing of the retained D readouts. It does not currently cover changing the
physical H readout actions while retaining only their fibre spaces. This is a
scoped linear-algebra theorem with exact finite GF(64) certificates, not a
complete multiplication theorem or a new kappa.

## Precise admitted theorem

Keep the physical H words, owner routing, and literal native whole H263/H642
interface actions. Retain the source subspaces represented by the four common
D1509 frames at receivers 6, 9, 48 and 73. Their common readout matrices may be
replaced by arbitrary invertible matrices Q_r, independently at each receiver.
Allow an arbitrary new D word with invertible relevant donor sections that
satisfies these retained whole-fibre interfaces. Allow each source quotient
map to be an arbitrary separate linear map from its donor's entire
480-coordinate bank to all 30 quotient coordinates, including mixing the
protected 96 coordinates with the remaining 384.

Then the common **entire** receiver-95/D1509 inverse-fibre condition cannot
hold. Donor 32 necessarily has off-D1509 response of rank at least two on a
four-space K that the retained literal H interfaces force into donor 61's
entire receiver-95 inverse fibre. Only the retained receiver-48 and receiver-73
spaces are needed for the donor-32 bound. No fixed affine rectangle in D,
fixed source coefficients, or common source input gauge is assumed. Other
source validity conditions may be granted without removing the obstruction.

## The source-61 anchor is independent of D

The forced frame satisfies

\[
K=L_{48}W_{48}+L_{73}W_{73},\qquad
\operatorname{rank}W_{48}=\operatorname{rank}W_{73}=4.
\]

The reviewer independently reconstructs the native H generators and checks
all sixteen source-61 decompositions supplied by the adversarial certificate.
Every decomposition uses **H observations alone**. The generator span has rank
60 at H263 and H642, and rank 54 at each other visible quotient. Noncentral
H observations have zero entire 30-entry source tuples; central observations
have prescribed literal values under the whole-H interface contract. The
admitted full H donor-section observation lemma therefore fixes every
replacement source tuple on K.

With H words and owners fixed, source-61 proper outputs on K remain old. The
independent replay checks all 88 marked off-D outputs vanish and the eight
D ingress outputs have rank four; its whole-interface interpretation uses the
admitted S032 H/source interface. Thus K remains in source 61's entire
receiver-95 fibre regardless of D changes. A common entire fibre would have
to contain K at donor 32 as well.

This strengthens the evidence in construction's `FORCED-K.md`: zero-valued
retained D observations used in its nonparent argument are unnecessary for
this particular K. The H-only decompositions also make D readout rebasing
harmless to the anchor argument.

## Full 30-input sections force the retained-frame values

Donor 32's four D1509 parents are H71, H481, H646 and H940. The reviewer
reconstructs the full physical donor sections B(h,r) for r=48,73 from the H
early/late/cross matrices, owners and source phase frames. All eight are
30 by 30 and invertible. Output membership is derived directly from root-table
inner products and D-chart incidences.

Let F_h be the old normalized full 30-row source map, S_r the old donor-32
D section, and E(h,r) the literal insertion of its two D1509 input flags among
the thirty outputs. The checker verifies on every row and column

\[
 B(h,r)F_hL_rS_r=E(h,r).
\]

A replacement retaining the whole fibre space and readout Q_r must satisfy

\[
 B(h,r)F'_hL_r=E(h,r)(S'_r)^{-1}Q_r.
\]

Invertibility of B(h,r) therefore forces

\[
 F'_hL_r=F_hL_rS_r(S'_r)^{-1}Q_r.                 \tag{1}
\]

This identity controls all 30 source coordinates. Extra quotient rows,
arbitrary extensions outside the protected bank, and a different invertible
source phase normalization provide no independent freedom on L_r.

## Full-parent off-D certificate and rank-two leakage

Independently of the adversary's sixteen marked rows, this review takes
**all 112** actual receiver-95 H output rows outside D1509 from the four
parents: 28 per parent. Let C be their old response on [L48,L73]. Exact
arithmetic gives

\[
 C\in\mathbb F_{64}^{112\times16},\quad
 \operatorname{rank}C=12,\quad \dim\ker C=4,\quad
 \dim\pi_{48}(\ker C)=\dim\pi_{73}(\ker C)=2.
\]

The full matrix and kernel basis are saved in `output/CERTIFICATE.json.gz`.
The marked-row obstruction thus agrees with the complete parent outputs.
By (1), the new off-D response on K is C V, where

\[
 V=\begin{bmatrix}V_{48}\\V_{73}\end{bmatrix},\qquad
 V_r=S_r(S'_r)^{-1}Q_rW_r.
\]

Each V_r has rank four. If u belongs to ker(CV), then V48 u belongs to the
rank-two space pi48(ker C). Since V48 is injective, dim ker(CV) is at most two,
so rank(CV) is at least two. K cannot belong to donor 32's entire fibre,
contradicting the source-61 anchor.

These fixed identities and ranks survive field extension. For k repeated
copies the projection rank is 2k and the block rank 4k, giving leakage rank
at least 2k, even with arbitrary linear mixing of copies under the same
interfaces. The maps are linear over the stated coefficient field; no
nonlinear-source claim is made.

## Literal actions versus preservation of H spaces

| Proposed freedom | Status of this proof |
|---|---|
| Arbitrary invertible common D readout rebasing Q48,Q73 | Admitted. Even donor-specific invertible choices do not remove the local donor-32 bound. |
| Coordinate changes describing the same physical H interface map | Admitted: prescribed source observations remain unchanged. |
| Preserve H fibre spaces but physically change their nonzero common readout actions | Not established: the source-61 anchor uses nonzero central H observations. |
| Change H words, owners, or retained L48/L73 spaces | Outside the theorem. |
| Cross-donor source coding or a different isolation contract | Outside the theorem. |

“Same H spaces” must not silently replace “same literal H interface actions.”
The missing proof for physical H readout gauges is not evidence that such
gauges give a completion. Consistency among the retained H interfaces may
impose additional constraints; that requires a fresh argument.

## Reproduction and provenance

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-full-source-isolation-review-s033/check.py \
  --repo . --out /tmp/s033-independent-full-source-isolation
```

Expected status: `PASS_INDEPENDENT_FULL_SOURCE_FIXED_H_ISOLATION_REVIEW`.
The checker imports the separately implemented GF(64) arithmetic from the
physical three-receiver gate review. It imports neither `isolation_gate.py`
nor `forced_K.py`. Supplied H-only decomposition coefficients are checked
against independently rebuilt native generators. Source pins identify every
physical input, reviewed statement and arithmetic module. Owner data and the
admitted whole-H interface lemma remain inherited source evidence. This is
independent agent review, not proof-assistant or human certification.

## Open next questions

A receiver-95 continuation must change at least one admitted premise. For
physical H readout changes preserving spaces, first characterize compatible
central H tuple actions, then test whether K remains forced. Changed retained
D spaces or H processing need fresh source, isolation and cost arguments.
Other fifth receivers are outside this obstruction. No selected frontier or
foundational assumption is changed.

Credit @CubeJerry, S031/S032 source/H contributors, S033 construction and
adversarial workers, and the root's kernel-projection argument.
Substantial OpenAI assistance. Apache-2.0.
