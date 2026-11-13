# Parity-only bilateral Gaussian radial bound

Every total F:Z^4→Z^4 with error at most1 from H4/2 and preserving total
coordinate parity has supremum absolute radial change at least1/2.
Injectivity, periodicity, exact sums and equivariance are not needed.
For a bijection the conclusion is

max(forward outward slack,inverse outward slack)>=1/2.

This is bilateral. No forward-only lower bound1/2 is claimed.

At x=(2a,1,1,1), a>=2, the complete parity-preserving neighborhood has
eight candidates. Their squared norms are n-2a,n-2a+4,n+2a-2,n+2a+2,
with multiplicities3,1,1,3 and n=4a^2+3. The exact least absolute radial
gap is sqrt(n)-sqrt(n-2a+4), uniquely attained by the inward corner
(a+2,a-1,a-1,a-1). Its value increases from0 to1/2. PROOF.md establishes
every comparison and the limit for all a; finite tests are corroboration.

```sh
python3 -I -W error -B verify.py
python3 -I -O -W error -B verify.py
```

Expected marker: PASS_PARITY_BILATERAL_GAUSSIAN_RADIUS. `--write`
regenerates RESULT.json. Standard library only; no predecessor/search
code imported. Checks include132 family members, a=2..128 and values
through10^100, all16 corners and the eight parity-preserving choices,
integer radical intervals, two polynomial identities, the Gaussian
signed-permutation transfer and six premise/direction controls.

The parity-flipping corners with squared norms n-1 and n+3 have radial
gaps tending to zero. These defeat this local witness without parity;
they are not global counterexamples to an unrestricted radial theorem.
The unrestricted R5 Hall lower bound remains unchanged.

Ali Romman's #6509 supplies a nonempty exact-sum bijective subclass and
error-one upper bound; reverse triangle inequality gives absolute radial
slack at most1 for that inherited construction. The parity-bijective
infimum is therefore bounded by[1/2,1] here, with no attaining claim at1/2.
Nick Petalas's #6619 and the frozen R5/compact proof retain their separate
norm-contraction and finite-Hall credit. Exact pins and bounded novelty
metadata are in SOURCES.json and OVERLAP.json.

Open next questions are sharp global attainment in the parity-bijective
class, and the relation between its two outward directions. Neither is
settled by the pointwise family. No selected caller, physical tariff,
framework-assumption discharge or kappa change is made. No standalone PR
is proposed before review. Substantial OpenAI Codex assistance.
