# Independent review of the arbitrary two-direction envelope reduction

**Accepted as a universal algebraic theorem under the stated rigidity and
quotient hypotheses. Its native BIT corollary retains the pinned scalar205
dependency. No physical decoder, supplier or new kappa.**

Reviewed author proof SHA256:
`346ed8024ce966b7962a00cf2cb8f43bb91b7fafc2d35837bd0873d83acda8fd`.

I read and checked the argument directly. The independent checker imports
no author code and does not treat repeated source-checker execution as
independent mathematical verification.

## Proof audit

The rigidity hypothesis says that the scalar code has exactly one local
direction at each allowed receiver support, with own coefficient one.
Consequently any quotient-kernel vector of a block row equals its
canonical local row with coefficient equal to the own output vector. A
single erased nonzero canonical contact kills that vector. Thus every
contact-deleting row injects its entire value width into the quotient.

If the global quotient contains a full scalar-line tensor, the stated
strict dimension inequality leaves fewer than V dimensions over its scalar
extension. Rowwise kernel scalarization then produces a support-contained
scalar fitting in that one-direction code. This uses the independently
reviewed subwidth argument and does not require a common kernel vector or
functional across receivers.

If there is no full scalar line, a deleting row must see both scalar
directions locally. The own-zero local representatives are unique because
the canonical local kernel is one-dimensional. Subtracting their operator
coefficients leaves exactly the canonical identity tensor row. If the two
coefficient matrices were scalar-linearly dependent, the equation at any
deleted contact would make both scalar multiples of identity and force a
full scalar tensor line. Hence the matrices are independent. Every deleted
contact must have exactly the same normalized pair of local scalar
evaluations.

The global choice h1+t h2 over k(t) avoids every nonzero row annihilator.
Its row-dependent normalization deletes every contact deleted by the block
row. Its local representatives have zero own coordinate and no support
outside the fitting set, so neither diagonal normalization nor support
containment hides an additional assumption. Unchanged rows can retain K_i.
The conclusion therefore controls the whole support pattern, not only the
coarse arrival charge.

The field extension is legitimate. Scalar support/rank facts from the
binary native source persist. Moreover, the set of scalar h whose whole
tensor line lies in E is the kernel of the linear map
h -> (h tensor e_s mod E)_s; its dimension is unchanged by extension.
This justifies the author's line-free extension statement without a
nonlinear descent claim. The generic direction need not exist over the
base finite field, and the proof correctly states its conclusion over k(t).

The strict d<2V assumption is essential. The native scalar two-patch
example with ell193 tensors to d=2V, and a smaller source-free diagonal
identity example also disproves support domination at equality. Neither
control supplies a physical chronology.

## Independent exact controls

The3-receiver binary matrix is reconstructed from its literal blocks. Its
ordinary rank and total code rank are both5; the canonical tensor has
dimension2, so the quotient has dimension3. No one of the three binary
scalar quotient lines has its entire width-two tensor in the code. The
zero locations are exactly(0,1),(1,2),(2,0).

Over F2 no scalar one-direction extension dominates this zero pattern.
Over F4, independently implemented as polynomials modulo x^2+x+1, both
nonbinary slopes work. This is a verified reason to retain the extension
field in the theorem, rather than an incidental choice of proof technique.

Each receiver has eight code rows with each prescribed own basis vector,
hence64 normalized block-row choices. All262144 complete fittings from
the fixed five-dimensional code were checked. Exactly128 lack an F2
one-direction domination; every one has an F4 domination. This verifies
only that finite code family. The universal theorem is supplied by the
proof audit above.

From the authenticated rational native roots, the checker independently
rebuilds the canonical rank9 code, all111 forbidden restriction ranks8,
the two17-beneficiary patch sets with overlap5, and the ell193 scalar
fitting. Its widths1,2,3,5 have actual canonical quotient2V. The diagonal
identity boundary example has quotient4=2V and fails one-direction scalar
domination even over F4, consistently with the elementary rank obstruction.

Normal and optimized Python executions have identical mathematical
receipts. Explicit checks use exceptions rather than assertions. Native
and proof byte pins are enforced. The scalar205 theorem itself remains an
identified prior dependency, not a claim established by this finite review.

## Reproduction

```bash
python3 -I -B check.py --native NATIVE.json.gz --proof ../author/PROOF.md --output RESULT.json
python3 -I -O -B check.py --native NATIVE.json.gz --proof ../author/PROOF.md --output optimized/RESULT.json
```

Expected status is
`PASS_INDEPENDENT_TWO_DIRECTION_ENVELOPE_CONTROLS`, with262144 fixed-code
fittings,128 F2 failures, zero F4 failures and native boundary ell193.

This is an independent AI-assisted mathematical review by Worker C for
@CubeJerry. Credit the author's generic-envelope argument and the earlier
scalarization, native code and scalar-savings results. No human reviewer or
formal proof kernel is represented.
