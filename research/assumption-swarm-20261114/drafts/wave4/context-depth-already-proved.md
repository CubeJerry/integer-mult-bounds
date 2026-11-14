# Selected unfinished-context bound: resolved prior work

Disposition: **already proved under the retained ideal semantic/scheduling
premises; no new theorem or publication proposed.** Canonical base:
`e54523517d0f03e58352e647c403a5af3e525a57`.

Merged [#6901](https://github.com/CrocSwap/integer-mult-bounds/pull/6901),
head `4c7a4f00f09665276e145ac2cc1d12f8b8f9a7ac`, canonical
`research/compiled-root-clifford-precision/PROOF.md` §§3–4, already derives
`K(n)<=v*A*(1+floor(log2 n))^2` from chronological product, same-owner
completion, disjoint splitting and integer lockstep source/complement/exit
scheduling. Its original numerical instance used ambient145^1024. The
canonical `research/odd-native-common-grid/PROOF.md` §4 already specializes
v1920 and ambient153^1920; selected #7000 substitutes the current H_C.

The selected retained ambient-transfer proof §6 explicitly uses cap
A=153^1920 instead of the largest productive target145^1920. It proves
source band `(n/A,n]`, valid demanded children and strictly smaller exits.
Pending #7424 independently handles that ambient version. Source complements
contract by `(A-1)/A`; exits satisfy
`e/n <= (r_max/A)*(r_max/k_min)^G <= (A-1)/A`.
After A descents ranks more than halve. Counting the root correctly gives
at most `A*(1+floor(log2 n))` compiler frames, each contributing at most
`v*(1+floor(log2 n))` raw contexts. This is the existing argument.

The quantity is source-dependence depth on **one contribution path**, not
simultaneously live banks, replication, total calls or physical storage.
The proof already treats correlated owned inputs, complete ancestor remainder
factors, distinct nested source owners, relative-to-entrance endpoint resets,
and uninterrupted swaps. Completion/splitting and restored whole-job adapters
add Clifford actions without persistent exterior scalar debt. Batch-clearing
fractions are accounting weights, not runtime scalar multiplications.

Exact current check: v1920, A153^1920,
`H_C=14174600000000000000`,
`K_star=1920*153^1920*(H_C+1)^2`.
`bit_length(K_star)=14073`; `bit_length(4096*K_star)=14085 < H_C`.
Thus `4096*K_star<2^H_C` without constructing that enormous power. For
`ell=floor(log_N D)` and `t=K_star*ell`, the standard `N*ell<=D` gives
`356*t<D` whenever ell>=1; ell0 has t0.

`SOURCE-PINS.json` authenticates six canonical proof exports in `inputs/`.
`check_threshold.py` executes the exact current arithmetic, source authentication,
34 strict-power endpoint controls and bounded contraction checks; result is
`CHECKS.json`. No large compiler or duplicate tiny-flow replay was run.

Live overlap pins/status are in `OVERLAP.json`: #7345 rank tables, #7346
Pascal owners, #7347 source-row addresses, #7423 recursive leaf ownership,
#7424 independent ambient tables, #7464 plateau width-divisor visits and
#7532 historical source-count floors. None supersedes or newly supplies this
already merged context proof. Their counts must not be conflated with K.

No mathematical defect was found in the actual claimed bound. The narrower
ideal context claim remains separate from physical all-column services,
actual caller owner/frame presentation, initialized/restored backing, full
stock, instruction emission and analytic recovery. All five foundational
assumptions and the selected conditional kappa remain unchanged.

Audit by OpenAI under @CubeJerry's direction; no novelty or independent human
acceptance claimed. Investigation stopped when prior proof was located.
