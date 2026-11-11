# Stable histories exclude the first recoverable encoder

The universal PROOF.md gives the stable-history quotient gate. If zero-baseline
history relations annihilate neutral controls, encoder response descends to G
on D=row(E) intersect row(W_T) intersect row(F0), and
rank(G)<=dim(D)-dim(D intersect S) for certified stable history rows S.
A positive quotient is necessary, not sufficient, for a unit channel.

Two independent source implementations establish at chart71/pre29098:
E has roles287/847/1050 and rank3; D=span(u77), and
u77=final common189-initial common189. The published220-chart history theorem
and literal local history lift make this mode stable for all neutral controls.
Thus no generalized single encoder in this fixed interface has unit gain.
The restriction includes all220 admitted stations and all receiver histories,
but no external correlated side channel or changed native processing.
Other cuts, modes, access and coupled encoders remain open. No new kappa.

The source author uses stacked quotient residuals and explicit representations;
the reviewer uses separately written max-pivot intersections and a literal
receiver-chart history lift. They import no routines from one another. The
root read both proofs and the independent algorithm, checked the composition
with the nine-relation theorem, and retained each normal/optimized receipt.
The general gate has the separate review/STABLE-GATE-REVIEW.md. This is
model-assisted verification, not human or formal-kernel certification.

From repository root:

```sh
python3 -B research/moonshot-005-program/results/stable-history-encoder/source/derive.py --repository . --output /tmp/stable-source.json
python3 -B research/moonshot-005-program/results/stable-history-encoder/review/verify.py --source research/shared-wire-split-composition/data/final.json.gz --output /tmp/stable-review.json
```

Repeat with -O and compare each result to its own frozen receipt; the two
independent receipt formats differ. Source proofs/data and exact pins are in
source/ and review/. Raw-source fees and all multiplication assumptions remain.
Credit @CubeJerry, native authors, S004 orchestrator and both workers; OpenAI
assistance disclosed.
