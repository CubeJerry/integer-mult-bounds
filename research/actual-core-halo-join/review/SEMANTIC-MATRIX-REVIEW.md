# Independent original-matrix review of the J2 observation

Prepared for @CubeJerry by seed78 with substantial OpenAI assistance.
**PASS in normal and optimized Python, with identical observer receipts.**
This checks exported semantic Core values followed by the literal bridge and
actual halo. It does not replay or certify a physical Core execution.

## Exact evidence and reproduction

The observed source is Reference(31,1,4,1,3,192), with period 32, two local
side 16 windows, q=56, Core P=356/w=381, R_in=1, whole-field R0=8, halo carrier 2,
normalizer 2, W=2, J=2, boundary 3 and saved halo 2. The producer explicitly records
physical_core_executed=false. Its immutable observed JSON has SHA256
`4e4a7c9f78eab6c757fe37f583a1a0deb2bb74c4dace520491bbf6352d0660a0`.

The reviewer periodic_review.py has SHA256
`326913215d59e9507f0bab3fc826f98225204ca6c980cfcf3a84c01cecf67d3c`.
Adjacent signed_oracle.py has SHA256
`46ceaa9e0f4f35e1a0748c70c8c63e084a8ea4350bebc81a810b8227beb342f7`.
Both semantic-periodic receipts have SHA256
`d8c42b5c0e667feb113774093ff5c752e1da7f5bcdabc3ca66d525a3e8c11692`.

```sh
python -I -B periodic_review.py --package /path/to/actual-core-halo-join --observed observations/semantic-q56.json --output normal.json
python -I -B -O periodic_review.py --package /path/to/actual-core-halo-join --observed observations/semantic-q56.json --output optimized.json
```

Expected status: INDEPENDENT_ORIGINAL_CORE_HALO_OBSERVER_PASS. Fresh producer
timing fields change the input provenance hash, so reruns must preserve their
own input hash; it is not a numerical equality field.

## Independent expected values

The observer authenticates the original Reference, exact arithmetic, Gaussian
helper and interval source hashes. It reads all original matrix entries and
computes the full periodic inverse and the two ordinary principal-window
inverses by separately written rational Gaussian elimination. Every inverse
has an exact residual check. No supplier Schur factor or staged oracle defines
these expected outputs.

A separate full-period recurrence computes the expected halo numerator at
each original coordinate, with independently coded inward coefficient rounding
and toward-zero arithmetic. The literal normalized source is decoded by the
separate sign-magnitude observer and compared exactly to the actual native
return divided by 2^(P+U-q). All 32 original addresses, 20 kept and 12 returned,
match the required exact grid words. The checked whole-field radius includes
all 32 records, and the output carrier is funded separately.

The exact squared Euclidean Core residual is approximately 2.6867664e-35,
well within the retained 1/32 error allowance. The exact rational number is
stored in the receipt. The maximum normalized periodic output error is
approximately 4.5412515e-8, including the J2 truncation tail. The independently
computed kept operator tail is approximately 6.7486099e-80. These are finite
fixture observations, not new uniform error or rate theorems.

The observer separately checks the normalized Core allowance
2*epsilon/A+2*2^-q, the complete halo numerical/tail allowance, and both original
output sets. A stronger fixture check distinguishes the unnormalized Core
from an identity passthrough; this prevents the loose admitted epsilon alone
from making a trivial output look persuasive.

## Active adverse controls and prior witness limit

Eight corrupted exported observations are rejected: an insufficient source
band, per-coordinate radius in place of whole-field radius, omitted input
grid lift, a one-unit Core corruption, floor in place of negative toward-zero
rounding, halo reuse of mutated Core input, replacement of kept Core by the
halo recurrence, and a one-grid-unit kept-output corruption. These test the
observer predicates; they are not eight mutated physical Core executions.

An earlier q28 semantic observation, SHA256
`98b34b038f87ed861f6e5286b6cc0743cd1c6a8786f36315c9d5a8a7d6dc1469`, passed the
original-matrix/rounding/merge checks up to a stronger witness gate: at that
grid all kept Core words equalled the independent J2 halo words. Replacing
one by the other was therefore not a distinguishable corruption. That was
an inapplicable witness-strength condition, not a correctness failure.
The q56 successor distinguishes them and passes the active substitution
control. The earlier observation was not relabelled as this successor.

The separate bridge review executes physical bit conversions on independent
sparse hardware; the separate asymmetric review executes metadata producers
and routes. Neither turns this semantic Core observation into a physical
Core run. The long complete physical transaction requires its own observed
receipt. Existing #6880/#6904 tail, recurrence and splice results are inherited;
the contemporaneous source-bridge work is credited in the author's NOTICE.
No five-assumption discharge, new kappa, human acceptance or proof-kernel
verification follows from this review.

## Publication-gate EOF cleanup

The reviewer was refreshed only to remove one terminal newline byte. Its
normal and optimized compiled-code bytes, and its parsed AST, are identical
to the prior frozen script. Exact old files are preserved under
provenance/periodic-before-eof-cleanup; PERIODIC-EOF-EQUIVALENCE.json records
the transfer. Both complete semantic observer commands were executed again
on the same input. Their scientific results are unchanged; only the script
provenance hash differs. No physical Core was replayed for this cleanup.
