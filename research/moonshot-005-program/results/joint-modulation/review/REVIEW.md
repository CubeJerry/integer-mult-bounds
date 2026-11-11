# Independent review of joint neutral modulation

**Verdict: ACCEPT the universal matrix criterion, conditional physical lowering,
and explicit illustrative typed construction. No source-native positive channel
or new κ is established.**

Reviewed proof SHA256:
`a40537ea4e64dc1a998085fe0a89f2428a6b26cd651fe8631a3695e9f50e81ae`.
Reviewed certificate SHA256:
`2235ef3ac3322be0d9031f3df1ad37c4cad8416bcdfcaf4a0241a7f3b4003d64`.
The independent review code imports no author verifier.

## Mathematical criterion

For the fixed control and observation interface, A includes all off-terminal
endpoint and guard responses, B the observation responses, and F₀ the
observations on all arbitrary common inputs. If K spans ker A and Z spans
the left nullspace of F₀, the criterion ZBK≠0 is correct: every neutral
control is Kx and every noise-canceling observation is tZ. Their signal is
exactly tZBKx. A nonzero entry supplies a control and decoder after the
explicit scalar normalization. That normalization remains a coefficient
admission obligation.

The block-rank identity is correct in all finite dimensions. Quotient the
lower output space by im F₀, accounting for rank F₀. Project the remaining
map onto its A component, accounting for rank A. The residual image is
πB(ker A). Since ker Z=im F₀, its rank equals rank ZBK. This proves the
formula, including zero-dimensional kernels or observation spaces. The
finite illustrative checks are not substituted for this argument.

When the excess is zero, every neutral Bc lies in im F₀, and can be absorbed
into a displacement of arbitrary common inputs. The indistinguishability
conclusion is valid for that fixed observation/access interface. Additional
data access, altered processing, common-input-dependent replacement
encodings or new transport require a new calculation.

## Physical scope and incremental tariff

The author clarified two points requested in this review: raw donor and
receiver carriers are distinct, and the incremental tariff starts with
formed raw differences. This matches the actual S004 roles and the toy.
Input conversions and final recoupling are charged separately when not
already in the caller's baseline.

The donor and receiver reservations are initially unused. Hoisting the
donor once and leaving stationary q records supplies every later control
at its actual chart; later receiver traversal collects actual observation
accumulators. There is no historical source reread and no reuse of a
carrier already moved to its terminal chart. The original common word
keeps its order. Live targets, chart matching, guards and coefficient
admission remain explicit requirements.

The displayed tariff is correct: r+d+s+L+t ADDs, s+L INITs and s+L CLEARs,
where s counts donor records, L receiver-chart accumulators, r controls,
d observation terms and t terminal corrections. Record creation costs
s ADDs and receiver collection L ADDs. The label/lifetime bound s+L and
peak bound native_peak+s+L are conservative. No MOVE is hidden in the
stationary records. Ordinary work, precision, storage and erasure are
retained rather than converted into free operations.

## Independent reconstruction of the typed example

The review uses explicit nested binary chart spaces, dense rational
vectors in all five independent inputs, and a fresh interpreter. The
18-instruction word yields common H=h,Y=y,X=x in the required charts,
unchanged raw Q=q, raw R=r+q, and no remaining owned field.

The original11-instruction native occurs as an ordered subsequence.
The two raw MOVEs have exactly the X and Y source route lineages.
The difference is five ADDs, with no new route or owned lifetime.
The complete word has eight ADDs, eight MOVEs, one INIT and one CLEAR.

The review independently toggles the literal two pulse instructions,
reconstructing A=(1,−1) and the displayed B. Independent column-span
reduction gives block rank3, rank A=1 and rank F₀=1. Either single-pulse
restriction has excess0; their joint restriction has excess1. Thus the
toy correctly separates individual neutrality from joint neutrality.

Removing the second pulse leaves a common Y error q; removing the early
noise observation leaves receiver error h; removing terminal restoration
leaves common H error q. Removing the funded raw donor MOVE causes a
cochart failure at the second pulse, checking actual source access.

## Reproduction and limits

From the integrated repository root, adjusting the review script path if
placed in a review subdirectory:

```sh
python research/moonshot-005-program/results/joint-modulation/review/review.py \
  --packet research/moonshot-005-program/results/joint-modulation \
  --output /tmp/joint-modulation-independent.json
```

Normal and optimized review executions agree and print
`PASS_INDEPENDENT_JOINT_MODULATION_REVIEW`. This is an independent agent
and implementation review, not human peer review or formal-kernel
verification. The toy is not the pinned programme native. Source-specific
positive matrices, the literal word, complete costs, uniformity and all
remaining global dependencies remain to be established.
