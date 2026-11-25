# Cross-session review of E002 on-demand spectral repair

Reviewer: S003 Route C. Status: **accepted in the stated scalar-repair
interface**. This is an independent proof comparison, not a claim to
originate E002's work or a complete multiplier theorem.

Read in full after completing S003's independent derivation/checker:
`results/epsilon-uniformity/sessions/E002/lead/on-demand-spectral-repair.md`,
imported by the session lead from the concurrent remote checkpoint
`9d5abf18ff741ff6f8b9f82790e0475fc662b4fe`.
Also read the E002 Route A composition review. All use OpenAI math
`3344da59991ed94f9ba711217b29c1d760badfa6` and the common S002 predecessors.

## Comparison and critical checks

E002 SR1's closed predictor formula agrees exactly with S003 SR3. E002
proves it by truncating the formal series after writing the signed count
as qT+r; S003 independently used the factored low-bit Lucas expression.
Both accommodate negative offsets. The actual gap criterion
`floor((c-u)/T) mod3 !=0` is a useful E002 formulation; central-window
containment alone suffices for the repair.

E002 SR3 first recovers the supported error using inverse Vandermonde,
multiplies by squared F4 gaps, and then applies the **transpose inverse**
to obtain check-space coordinates. This is the correct small-phase lift.
It does not write a sparse error into all B spectral rows and silently
convert them back. Its lifted correction may be nonzero off the exception
set; that is harmless because the original multiplier discrepancy there
vanishes. Zero gaps inside the containing set are safe, because no gap
inverse is taken. General extension-field gaps would break the cube-one
step, but both p and z are explicitly in the embedded F4.

The physical argument matches the independent S003 procedure: generate
comparison trits by complete-fibre scans, attach O(m) control bits,
recompute polynomial-size coefficients per record, and apply only
polynomially many coarse-role scans. The independent module is a complete
unchanged spectator. Fixed tape count is preserved even when small
matrix accesses are implemented by full sequential scans.

The padded check count remains S=R/32. For explicit packed composition one
should retain w separately from v=32w: parent coarse roles have size32B,
the padded checks have B coarse roles (32 floor(B/32) real and the rest
zero), and two-family phases have2B coarse roles, each followed by w.
E002 A's composition review already states the corresponding copy16/half2
regrouping, and S003's proof now makes this split explicit as well. No
whole-v divisibility is required for the padding remainder.

## Evidence and scope

S003's independently implemented on-demand table was checked against six
whole physical-orbit repairs with both query signs and 6,912 scalar
outputs, including transpose/gap/converter/module-order negative controls.
It also checked containing sets with zero gaps. That corroborates the
common identity through a different checker; it is not an independent
execution of E002's complete physical machine.

This component is independently convergent across E002 and S003. Credit
and source pins must be retained together when composing it. Neither
review alone closes shared endpoint/rank maps, exponential-width batching,
numerical Walsh, or the uniform whole-input budget.
