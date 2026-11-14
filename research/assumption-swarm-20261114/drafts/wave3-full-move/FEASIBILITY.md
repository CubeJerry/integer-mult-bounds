# Proposed next scope: old-coded complete selected MOVE

Status: feasibility only; implementation not started. Parent scope approval
is required before allocating this new package. Wave1 and wave2 are frozen.

## Exact predecessor and live overlap pins

On 2026-11-14, PR #7563 is open at CubeJerry head
`5dd80e8ab9c989336b5e448e14147c2ba29da89b`, canonical base
`e54523517d0f03e58352e647c403a5af3e525a57`. Its
`research/literal-selected-move-join/move.py` is already a complete
same-width, same-grid 31-tape selected MOVE24472. It has 82,813 locations,
SHA256 `42e4293ab59ffa1c99e0dbbd5fded0833a5d726e1e794f0f263ae9a4686587a5`,
and graph hash (predecessor repr convention)
`14f38b15157a9c9cd2828861f6904701a29b1e27507a7e43d60030e1ae4d9238`.
Its frozen core was originally commit
`3a27ab1d302d13b1ce52411f8a174e7a32baab77`.

The same PR additionally contains a 52-tape sharp endpoint scale/width
wrapper, which is a different domain extension. PR #7568 is open at
`6c68c9d55b518c997fe5f53d127810e4009e9903`; it gives a 54-tape arbitrary-input
once-rounded wrapper. Their live metadata has no comments and unchanged
canonical base. Neither packed full MOVE is new work. PR #7566 already
joins a full packed MOVE to HOME. The prospective new seam is strictly
OLD23/three-bit-coded entry -> existing complete MOVE -> OLD23 return.

The frozen bridge is CubeJerry
`30497f40d89f2a137a4bc31a4fee1229b9af1440`,
`research/selected-move-packed-codec/machine.py`, 6,003 locations, 43 tapes,
SHA256 `119b69594a2a33550eec9b6e083db8f496c3fb3d9c1214b6703d687a0a662eba`.
The common-root numerical premise remains #7578 at
`e9b6d75397e3553af77bab81d5816e4b8708a501`.

## Proposed exact claim and physical seam

Join the unchanged 31-tape unscaled core by fixed relocation only. Its
HEADER0 maps to bridge GAMMA3, DATA1 to PACK2, and its private2..30 to
new43..71. Thus the full program has 72 tapes and 88,816 locations. The
alphabet map and two unit-cost continuations are the wave2 pattern.
The 29 extra owners begin blank through origin-1; the core installs and
retires its own wrapper and module guards. All bridge metadata remains
live but disjoint through the complete MOVE.

The existing full core already orders right phase, right linear map,
right translation, positive C on every column, left phase and left linear
map, including the actual i^f constant. It already has a full private
transaction and original-packed-owner return. No monomial implementation,
packed MOVE theorem, native factorization or source identity is rebuilt.

The old gather reverses the column labels uniformly in all nine slots.
A product of identical nine-bit source operators over all f columns
commutes with this common column permutation. Therefore the same inverse
address/codec continuation returns the complete selected MOVE in old
coordinates, with absolute phase and every spectator preserved.

## Numerical domain and grid issue

The chosen unscaled core needs all phase rotations/negations to fit and
every C-axis output to be integral and fit the fixed width. Under the
complete-root selected invariant, any right/left monomial prefix and any
completed C subset is again a Gaussian-dyadic Clifford on the same n-bit
root, with the same exterior coefficient budgets. The #7578 row/grid bound
therefore extends over every factor prefix. At common quantum
`Delta=2^-(p+n)` and width `w=p+h+2n+3`, all stored prefix components are
integral and have strict magnitude `<2^(w-1)`. This also excludes the
most-negative signed value, so every required phase negation fits.

Gamma6 has no explicit Delta field. That is not a blocker for this one-field
same-grid exact service: its integer-word action is homogeneous, and all
copies, permutations, Gaussian-unit phases and exact halves retain an
arbitrary fixed semantic Delta. No format conversion changes that Delta.
OLD23's ignored metadata cannot certify the common-root provenance, and
neither can Gamma6; that producer/source condition remains an explicit
caller premise. No quantum equality is inferred from merely matching
header shapes or widths across unrelated owners.

The #7563 endpoint wrapper could alternatively be used with its paid
scale, wider volume and exact unscale. The #7568 wrapper adds rounding and
an error/caller obligation outside the selected exact route unless one
proves rounding is identity on its actual domain. Neither extra wrapper
is needed when the above common-root all-prefix premise already holds.

## Optimistic complete bill

Let V_o be old physical bits, V_p packed bits and E the old header length.
The proved bridge gives `V_p<V_o/3`, `E_g<=V_p+E`,
`T_bridge<=2^20((9f+1)V_o+E+1)` and history64(V_o+E+1).
The exact unscaled core gives `T_core<=2^24(fV_p+E_g+1)` and
history1024(V_p+E_g+1). The two continuation replacements keep unit cost.
Thus the complete prospective bounds can conservatively be

```
T <= 2^25 (f V_o + E + 1)
K_after <= K_entry + 2048 (V_o + E + 1).
```

Indeed the fV_o coefficient in units2^20 is `10+32/3<32`, and the
E+1 coefficient is17<32. The history sum is at most
`(64+2048/3)V_o+1088(E+1)`, below the displayed bound. This accounts for
both old codecs, all routing passes, the complete core's six factors,
both levels of staging, all guards, original-owner commits and returns.
No width conversion is present in this chosen same-width core; none is
assigned a zero fee. Original caller acquisition/transport remains a
supplied entry obligation. Cost remains Theta(fV_o+E), not a faster nonleaf
service or a new kappa.

## Verification and stop rule if approved

Authenticate the exact 16-file small core closure and source witness,
retaining all notices and the pinned bridge. Use a fresh absent import
cache prefix or exact-byte loaders so pinned .py bytes cannot be bypassed
by stale bytecode. Compare all 82,813 embedded instructions with an
independent port/symbol/PC translation.

Run one uninterrupted actual full f=1 old-coded packet with nonzero complex
values, and one common-root-width model. Use an old-address oracle built
from the exact source kernel/frame witness, independent of CNOT words,
phase counters, packed-index routines and tape arithmetic. Negative
controls must detect wrong absolute phase, omitted translation, wrong
port/cardinality, aliasing and precommit numerical rejection. Check all
72 heads, original43 guards, added29 blank guards, private histories and
original-owner return. No full f=2 replay is planned.

Stop after this exact boundary theorem. Do not claim an emitted full-word
dispatcher, HOME/root reservation admission, global owned reset, complete
recursive invoice, failure-time cleanup, fast nonleaf rate, assumption
discharge or unconditional multiplication.
