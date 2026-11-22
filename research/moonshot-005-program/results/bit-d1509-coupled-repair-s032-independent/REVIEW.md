# Independent review: a bounded D1509 repair and its remaining obstruction

Session: `2026-11-22-S032`. This review accepts the exact local statements below. It does not establish a common fifth whole fibre, a completed supplier, a global return word, or a new multiplication exponent.

## Reconstructed inputs and evidence

`check.py` reconstructs the eleven physical ingress maps
\(P_j:\mathbb F_{64}^{96}\to\mathbb F_{64}^{35}\)
from the literal paired source maps, local frame matrices, physical H phase matrices, and raw owner routes. Root orthogonality comes from the integer root coordinates. Selected D packets come from the canonical global allocation witness. The author ingress matrices agree entry by entry with this reconstruction.

No executable from the new author packages is imported. The checker reuses the earlier independent GF64 arithmetic and independent binary-lift compiler. Exact input bytes are bound in `SOURCE-PINS.json`. The independent output and reconstructed ingress are saved in `output/RESULT.json` and `output/RECONSTRUCTED-INGRESS.json.gz`.

The source bank has 480 field coordinates, of which the protected 96 coordinates support the present fibres. For each of the eleven donors and receivers in \(\{6,9,48,73,95\}\), the checker constructs the entire protected off-D proper restriction: an \(88\times96\) matrix of rank 88. The other 384 coordinates and the previous direct-sum preservation result remain unchanged. This is enough to check whole eight-dimensional isolated fibres rather than a selected vector alone.

## Positive statements that pass

The exact phase-legal space of D-matrix changes preserving the four retained oriented readouts on their actual ingress frames has dimension **360** over GF64. The contract is

\[
\Delta T[O_r]P_jL_r=0
\qquad(j\in J,\quad r\in\{6,9,48,73\}),
\]

with the first 19 output rows restricted to the first 19 input columns. Here \(O_r\) is the actual receiver output-owner set. The contract concerns outputs seen by each receiver; it does not freeze the entire 35-coordinate D packet.

Both saved candidate words pass the following checks:

- the 19/16 early/late phase split, zero early dependence on late inputs, and invertibility of both phase matrices;
- all 144 geometric eight-by-eight D sections, including the geometric donor omitted from the eleven native source family;
- all 44 retained whole inverse fibres and their identity readouts on the unchanged source/H word.

The first candidate is a rank-one change that cancels the forced vector's donor-0/donor-61 discrepancy. The second is the saved seed-1 rank-six change in `ALL-DONOR-VECTOR.json`. It makes that same literal source vector \(v\) have the common D95 readout

\[
(14,5,63,1,1,49,6,27)
\]

at all eleven native donors. The old readout difference between donors 0 and 61 was

\[
(0,28,45,17,0,62,23,17).
\]

The ten all-donor contrasts on this vector have rank 10 both on the first 19 coordinates and on all 35 coordinates. Thus the free target rows can be chosen from annihilators of dimensions 9 and 25 respectively. The exact saved matrices, rather than the bounded search's reported success, are the objects verified here.

## Why this is not a fifth whole-fibre repair

Changing D readouts leaves the source/H off-D proper restriction unchanged. The forced vector \(v\) is isolated at receiver 95 for donor 61, but has a nonzero off-D response for **every one of the other ten donors**. Its common D readout does not remove that leakage.

The independent checker also reconstructs and orients the entire new receiver-95 fibre for every donor. The donor-0 and donor-61 eight-dimensional fibres have join rank **14**, so they remain distinct. Neither a common whole fibre nor agreement on all eight source parameters follows from the successful one-vector repair.

The H phase maps and all source maps remain the previously reviewed ones. The new D word therefore preserves the literal retained H interfaces already established in the four-receiver package; its whole retained D fibres and readouts are separately checked here.

## A complete frozen-ingress obstruction on the forced four-space

Let \(K\) be the four-dimensional intersection of the donor-61 whole D95 fibre with the 32-dimensional span of the retained common receiver frames. The checker obtains \(K\) afresh from the actual off-D kernel and verifies agreement in column space with the author's saved basis.

Write \(B_j=P_jK\), with a common literal parameterization of \(K\), and form

\[
Z=[B_j-B_{61}]_{j\ne61}\in\mathbb F_{64}^{35\times40}.
\]

The exact ranks are

\[
\operatorname{rank}Z=30,\qquad
\dim\ker Z^T=5,\qquad
\operatorname{rank}(NB_{61})=2,
\]

where the five rows of \(N\) are a basis of \(\ker Z^T\). Meanwhile \(\operatorname{rank}B_{61}=4\). The checker emits a separate basis, contrast matrix, annihilator and response in `output/FULL-COLLISION-CERTIFICATE.json.gz`.

For any row \(t\) of any linear common D readout, equality \(tB_j=tB_{61}\) for every donor is equivalent to \(tZ=0\). Consequently every such row belongs to the row space of \(N\). Every linear common readout on the whole forced space therefore factors through \(NB_{61}\), and has rank at most 2. It cannot be injective on the four-dimensional parameter space. This conclusion allows arbitrary linear output rows and relaxes all phase restrictions, invertibility requirements and retained-receiver constraints. Adding these restrictions cannot overcome the rank loss.

The premise fixes the actual ingress maps and the same literal forced four-space. It does not exclude a source/H redesign that changes those maps or changes which vectors must lie in a common fifth fibre. It also does not concern nonlinear D transformations or independently chosen donor-specific postdecodings.

The rank identities persist under scalar extension. On \(k\) independent copies the corresponding ranks become \(30k\), \(5k\) and \(2k\), while the desired injective parameter space has dimension \(4k\). Arbitrary linear mixing of copy coordinates in the common readout still factors through the common-response space.

### Necessary support of an ingress change

With the same fixed coordinate labels and forced space, put

\[
q=\operatorname{rank}[Z\ B_{61}]-\operatorname{rank}Z=32-30=2.
\]

Deleting one coordinate row reduces \(q\) by either zero or one: if the rank of \(Z\) drops, the rank of the augmented matrix must also drop. Restoring one row can increase \(q\) by at most one. Thus replacing \(k\) distinct ingress coordinate positions across the donor family can increase \(q\) by at most \(k\). A common injective readout on this same four-space requires at least **two distinct changed ingress coordinate positions**. This is a support bound on changed functions; it is not a bound on paid MOVEs, new fields, helper exports, or total compiler cost.

## Exact changed-D compiler invoice

The checker independently lifts GF64 coefficients in the polynomial basis for \(x^6+x+1\), replays the actual chronological word on all 210 original binary input columns, and replays each pure phase inverse. It also recounts every cross ADD from the original early cache. The source/H invoice is inherited from the pinned prior independent receipt because those maps and allocations are unchanged.

| Component | ADD count |
|---|---:|
| Early phase, each direction | 6,672 |
| Late phase, each direction | 4,732 |
| Original early cache copy | 114 |
| Late cross contribution | 4,337 |
| D1509 local total, including pure phase inverses | 27,259 |
| Previous D1509 local total | 26,996 |
| Eight-lane increment | 2,104 |
| Updated local source/H/D eight-lane total | **453,939,712** |

The inherited allocation is **279,648 INIT and dirty CLEAR each**, with **16 gap-six field exports**. No new MOVE is needed by this changed D word. This invoice covers the local source/H/D construction; the global supplier and return invoice remains open.

## Controls and reproduction

The unchanged old D word fails the new all-donor vector equality despite retaining valid geometric sections. A coefficient mutation on an actually retained output row fails the corresponding oriented readout. These controls distinguish the claimed interface from bare D invertibility or an unobserved output change.

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-d1509-coupled-repair-s032-independent/check.py --out /tmp/s032-coupled-independent
```

Expected status: `PASS_INDEPENDENT_BOUNDED_COUPLED_D_REPAIR`. The checked result is a constructive one-vector D repair together with a complete linear frozen-ingress obstruction on the larger forced four-space.
