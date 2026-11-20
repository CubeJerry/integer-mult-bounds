# Independent root review

The parent five-message linear operator theorem is accepted within its
stated frozen-word scope. The two-sided Woodbury identity is valid without
commutation among the five operators, because the exact scalar interaction
matrix is diagonal with entries 1,0,0,0,0. The five witnesses concern complete
physical bank blocks, not isolated coordinate zeros. Independent arbitrary
bank bijections preserve the corresponding functional independence.

`check.py` imports neither the author's checker nor the historical surgery
implementation. It reads the authenticated raw word, reconstructs the paid
surgery explicitly, checks every local operand and all 1289 output fields,
then computes sensitivities by backward expansion. The complete inverse is
obtained by sparse elimination rather than the author's 1x1/2x2 component
inversion. Both matrix products and all five whole-bank isolators are checked.

The accompanying `NONLINEAR-PROOF.md` strengthens the theorem to arbitrary
per-message functions: only translations survive, and zero-preserving maps
must be identities. This extension is new root mathematics and receives a
separate independent proof review before admission. Two full nonlinear
width-two literal executions, their exact inverse recoveries, five explicit
dependency controls, the singular deletion control and the translation
positive control exercise the derived formulas.

Reproduction from the repository root:

```sh
python -I -B research/moonshot-005-program/results/complex-survivor-boundary-rigidity/root-review/check.py --repo . --out /tmp/s031-complex-nonlinear-root-review
```

Expected marker:
`PASS_ROOT_NONLINEAR_FIVE_MESSAGE_BOUNDARY_REVIEW 1289 5`.

Coupled recoding, altered surrounding forms, new routes and altered boundary
bank partitions remain open. Neither this finite reconstruction nor either
theorem supplies a complete complex word or a new kappa.
