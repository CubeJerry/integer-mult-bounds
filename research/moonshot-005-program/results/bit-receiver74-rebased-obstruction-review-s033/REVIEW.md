# Receiver74 obstruction with common invertible D readout rebasing

**Independent review: accepted.** Fixed H words, owners and literal native H
interface actions, together with the old receiver6 and receiver73 source fibre
spaces, exclude a common entire receiver74/D1509 fibre. The result permits
arbitrary separate linear full480-to-full30 source maps, arbitrary D
coefficients, and invertible D readouts Q6,Q73 common across donors. It needs
neither the old88-coefficient rectangle, the phase-zero pattern, nor the
833-parameter affine restriction. No new kappa or compiler claim.

## Exact finite evidence

The checker independently verifies a forced two-space K=L6 W6+L73 W73,
with both W blocks rank2. At all sixteen source0 quotients visible at74 it
reconstructs native H-only decompositions of K. Direct physical propagation
checks every actual off74 output vanishes and the D ingress has rank2.
Literal H observations therefore force K into source0's entire74 fibre, so a
common entire fibre must contain K at donor38.

The checker also rebuilds donor38's full112-row parent off74 matrix C=[C6,C73]
from actual physical H words and owners. Its rank is12 and both blocks have
rank6, so ker C=ker C6 direct-sum ker C73, with each block kernel dimension2.
The retained full30 H-section interpretation is inherited from the independently
verified alternative-receiver screen, whose output is pinned here.

This new check reconstructs all four source0 D parents: H71,H116,H263,H283.
For each r=6,73 put B_r=T_old[O_r,{4,5}] and X_r=L_r B_r. It independently
expresses X_r in native H observation generators at every parent, verifies
noncentral full30 values are zero, and reconstructs all eight source0 full30
retained H sections. The actual physical D ingress, stacked across **all four
parents**, is exactly the35-by2 insertion matrix E_{4,5}. Thus arbitrary source
changes preserving literal H actions satisfy

\[
 P'_0X_r=P_0X_r=E_{\{4,5\}}.                              \tag{1}
\]

This identity is checked directly from physical phase matrices and owners;
it is not assumed from the original fixed D rectangle or from one parent.

The coefficient and column witnesses are

\[
 W_6=9 B_6,\qquad W_{73}=15 B_{73},
\]

with nonzero GF(64) scalars. For U_r=ker C_r and old donor38 section S_38,r,
the old input-kernel space V_r=S_38,r^{-1} U_r contains the local coordinate
of global input flag19. Donor0's actual input set contains flags4,5,19.
All decompositions, tuple images, stacked ingress, block kernels, and flag19
coordinates are retained in `output/CERTIFICATE.json.gz`.

## Normalization and the singular-section proof

Let T' be an arbitrary proposed D word. Retaining im(Lr) with common invertible
readout Q_r gives T'[O_r,:] P'_0 L_r=Q_r. Multiply by B_r and use (1):

\[
 Q_r B_r=T'[O_r,\{4,5\}].
\]

Therefore the normalized row matrix A_r=Q_r^{-1}T'[O_r,:] satisfies

\[
 A_r[:,\{4,5\}]=B_r.                                    \tag{2}
\]

The new word T' need not retain those literal columns. Their **normalized**
values are forced by the retained H interface actions.

Invertible full30 H donor sections force the full source identity

\[
 F'_{jh}L_r=F_{jh}L_r S_{jr}(S'_{jr})^{-1}Q_r.
\]

Extra source rows or unprotected bank coordinates cannot alter its prescribed
values on Lr. Write A_jr=A_r[:,I_j]=Q_r^{-1}S'_jr. The direct-sum kernel at donor38
makes parent isolation on K equivalent to the two separate conditions

\[
 C_r S_{38,r} A_{38,r}^{-1}W_r=0.
\]

Because the indicated maps and W_r have rank2, this implies equality of the
two-dimensional spaces A_38,r im(V_r)=im(W_r). Equivalently,

\[
 \operatorname{Ann}(W_r) A_{38,r} V_r=0.                  \tag{3}
\]

For literal D readouts Q_r=I this is precisely construction's linearization
Ann(W_r) S'_38,r S_38,r^{-1}U_r=0. For arbitrary Q, one must use the normalized
matrix; applying the literal affine equations unchanged would be unjustified.

Since e19 lies in V_r, equation (3) places A_r[:,19] in im(W_r). Together with
(2) and im(W_r)=im(B_r), this gives

\[
 A_r[:,19]\in\operatorname{span}\{A_r[:,4],A_r[:,5]\}.
\]

Donor0's section contains all three distinct columns. They span at most two
dimensions, so rank(A_0r)<=7. Since S'_0r=Q_r A_0r, the required donor0 section
is singular: a contradiction. Either active receiver supplies this witness;
the joint6/73 isolation condition supplies the separate equations.

## Scope

Q_r is common across donors, so one normalized physical row matrix A_r applies
to donor38 and donor0. Unrelated donor-specific readouts would invalidate that
column transfer and are not the retained common interface contract.

The theorem keeps the old6/73 source fibre spaces, H words, routing, and
**literal physical H interface actions**. Preserving only H fibre spaces while
changing their physical readouts is outside the proof. Changed H processing,
changed retained D spaces, cross-donor coding, nonlinear maps, and other
receiver targets are also outside it. No such relaxation is asserted feasible.

All identities survive coefficient-field extension. Repeating by k makes the
three columns into three k-column blocks inside a2k-space, forcing section
rank at most7k even with linear mixing of copies under the same interfaces.

## Reproduction

```sh
python3 -B research/moonshot-005-program/results/bit-receiver74-rebased-obstruction-review-s033/check.py \
  --repo . --out /tmp/s033-rebased74-obstruction-review
```

Expected: `PASS_REBASED_RECEIVER74_COLUMN_OBSTRUCTION`. The checker uses the
separate physical-gate GF(64) arithmetic and imports no construction or
adversarial normalized-obstruction executable. The earlier admitted whole-H
observation lemma remains inherited evidence. This is independent agent
review, not proof-assistant or human certification.

## Open next questions

A receiver74 continuation must change an admitted surrounding interface.
Receiver87 and the other remaining targets need their own normalized analysis. Physical H readout
changes preserving H spaces require a new compatibility proof and fresh
source, isolation and cost accounting.

Credit @CubeJerry, S031/S032 H/source contributors, construction's receiver74 column witness, adversary's independent review, and the root's
normalization direction. Substantial OpenAI assistance. Apache-2.0.
