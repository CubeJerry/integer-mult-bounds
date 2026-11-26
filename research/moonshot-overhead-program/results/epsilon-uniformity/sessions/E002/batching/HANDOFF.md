# Protected batching route handoff

This route produced one constructive local executor and two precise source
bridge tests. It does not change admitted E002 Theorem V, NI5, RV-I or RV-W.
All three notes request independent review; the parent controls admission.

`WEYL-STAR-BATCHING.md` (SHA256
8472657f7ac8307c1fa99908918a45ba3901048cd31f3a757111ea0c01a4bb02)
executes a weighted sum of Weyl translations/modulations on m independent
query fields by one common coset layout, m one-bit transforms and pointwise
row mixing. Its costly address factor is governed by the whole active width
a, not m separate f-field calls. Existing controlled-small-block tape
processors implement the simultaneous outer-product shear because the
unchanged controls occupy at most half the active address. Its cost is
V[m^K+sqrt(a)E_I(a)polylog(k)] plus separately charged preparation. The
common basis can be reused through stages with exactly the same family.
Rebuilding it through sqrt(m) stages still leaves a sqrt(m) coefficient;
no complete-source reuse is claimed.

`STAR-SWAP-FALSIFIER.md` (SHA256
5db06e11c67fba3e0ed5db2a060bf3616a40f42c5d2281853f58f50f50fd3ceb)
gives an actual q=4,L=2 canonical source rectangle in the rank-six Gram
quotient. Its exact middle map cross-swaps X_j with Z_b and Z_j with X_b.
Using complete composite registers x_j=(X_j,Z_j), z=(Z_b,X_b), these are
star swaps, after only a fixed exchange of other auxiliary slots. The
relative swaps do not commute, precluding common scalar diagonalization
of each term. No spectator query half exchange is assumed. This does not
rule out diagonalizing one fixed weighted sum, block methods, or the
complete original queries after label cancellation.

`SWAP-WEYL-CONTRACTION-GATE.md` (SHA256
5be659cade5396420a38ab06dbb852a59a56a3aa00858308f0be4f277033012b)
checks the lead's SWAP-to-Weyl bridge. The expansion has Q^2 parameters for
one Q-dimensional register. Reusing occupied parameter rows via a Walsh
conjugation gives an explicit nonzero signed-permutation block at every
row difference; it does not apply SWAP independently to the old rows.
Literal expansion costs Q^2 terms/volume, and diagonal-phase pinching has
a rank-Q^2 barrier within that mechanism. The equal-weight m=3 lift is
invertible while the target star-swap sum has an explicit kernel. Its
off-diagonal defect is full rank for one swap, and for odd m when Q>m.
These falsify specified contraction/repair shortcuts, not faster physical
implementations. For the source two-half composite, the register width is
twice the original axis width.

Exact finite checks passed, with no floating point:

- `verify_weyl_star_batching.py`, SHA256
  4f1b22db3b25ec520fd6e527d1e3eec5c1d6daea7b38a2eb2de4cc81e49c4905:
  30 one-word bijections, 5,036 layout positions, 4,340 local conjugacies,
  252 weighted pencils/38,776 entries, 252 genuine one-basis two-stage
  executions, 105 wrong-phase and 168 omitted-layout negative controls.
- `verify_swap_weyl_bridge.py`, SHA256
  d6c90c3dd4d1439d7ba1e805dba665dbb4fa5aba3ed583bb9e413f6e3626c75e:
  84 exact SWAP columns, 4,368 conjugated block columns including 4,284
  nonzero cross-row columns, 84 wrong-inverse-phase controls, 4,368
  character orthogonality entries, 36 actual Gram pairings and 16 span
  rows, 384 lifted involution/commutator checks, three kernel witnesses,
  and 768 complete two-half/composite swap identities.

Receipts are the two JSON files; captured runs are `execution.log` and
`bridge-execution.log`. These check finite exact algebra and layout,
not an asymptotic tape execution or a formal theorem. No main repository
files were edited by this route. The parent may copy selected frozen
artifacts and bind its independent review before admission.
