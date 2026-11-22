# A universal isolation obstruction with fixed H processing

**Independently verified scoped obstruction.** This closes the proposed
receiver-95 continuation while the specified H words and existing receiver-48
and receiver-73 fibre subspaces remain fixed. It permits arbitrary linear
changes to the full source tuples, arbitrary compatible D coefficients, and
invertible rebasing of the retained D readouts. It does not exclude changed
H processing or changed retained fibre subspaces.

## 1. The forced four-space and the source-61 anchor

Let L48 and L73 be the existing common eight-dimensional source frames. The
S032 forced frame K has the exact decomposition

    K = L48 W48 + L73 W73,

where both eight-by-four matrices W48 and W73 have rank four. Its coefficients
at the other retained receivers vanish.

For every one of source 61's sixteen quotients visible at receiver 95, the
independent certificate expresses all four columns of K using retained native
H263/H642 fibre columns only. Those H-observation spans have dimension 60 at
the two centres and 54 at the other fourteen quotients. No D-fibre generator
is needed for these decompositions.

By the retained whole-H interface contract, an arbitrary linear replacement
source tuple must preserve its values on each such H observation. It therefore
preserves its values on K. This uses the actual whole-H source observation
lemma established in the S032 source-edit obstruction, rather than assuming
that source coefficients are globally frozen. The old physical source-61
proper restriction has all 88 off-D rows zero on K; this identity is rechecked.
Thus K is still forced into source 61's whole receiver-95 inverse fibre.
Any common entire fibre must contain K at the other donors as well.

The physical H words and owner routes and the literal actions of the retained
H interfaces are fixed premises. Invertible readout rebasing below applies
to the D interfaces; arbitrary rebasing of the H anchor actions is not covered.

## 2. The exact donor-32 matrix

At donor 32, take the proper receiver-95 output rows belonging to its four
D1509 parents, remove the eight actual D1509 ingress rows, and retain the
remaining sixteen rows. Let Aoff be their original map on the protected
source coordinates and put

    M = Aoff [L48,L73].

This is a literal sixteen-by-sixteen matrix reconstructed from the actual
source gauge, labelled proper rows and H owner records. The independent
checker finds

    rank M = 12,
    dim ker M = 4,
    rank pi48(ker M) = rank pi73(ker M) = 2,

where pi48 and pi73 project onto the first and last eight coordinates.
It saves M, a full kernel basis, the actual sixteen row labels and both
rank-four coefficient blocks. The same projection profile is found at seven
other donors, but the donor-32 certificate alone proves the obstruction.

## 3. Arbitrary full source records

The argument does not assume that a replacement source uses only the old
six protected record rows. Two separately checked formulations establish this.

First, for each of donor 32's four D parents and each receiver 48 or 73,
the checker reconstructs the entire thirty-by-thirty physical H donor section.
All eight sections are invertible. Output membership is reconstructed directly
from the pinned root-table inner products and D-chart incidences. Each section
B(h,r), the original full source tuple F(h), and the old D section Sr satisfy

    B(h,r) F(h) Lr Sr = E(h,r),

where E inserts the two actual D1509 inputs belonging to that H parent into
the full thirty output rows, and every other output is zero. This identity
is checked on all thirty rows and eight frame columns. Any changed full source
tuple F'(h) retaining whole isolation with a new section S'r and invertible
common readout Qr must satisfy

    B(h,r) F'(h) Lr = E(h,r) (S'r)^(-1) Qr.

Invertibility of B(h,r) therefore forces

    F'(h) Lr = F(h) Lr Sr (S'r)^(-1) Qr.

Second, the reviewer independently
reconstructs the full physical H maps from all 30 normalized source input
records to the selected proper outputs at receivers 6,9,48,73 and 95.
Each is a six-by-thirty matrix of rank six.

These five maps factor through one common rank-six projection Vh:

    B(h,r) = C(h,r) Vh,

with every six-by-six C(h,r) invertible. The certificate verifies this matrix
identity on all 30 input columns, using the actual source phase frame and
the H early, late and cross matrices. It also checks that the full-input map
reproduces the original proper matrix used to form M.

Consequently an arbitrary new 30-row linear source tuple Fh has the effective
tuple Vh Fh for all these observations. Additional record coordinates cannot
change the receiver-95 off-D responses independently of the retained views.
This supplies the full-record justification for using M in a theorem about
arbitrary linear source maps, even when they mix all 480 source coordinates.

Let Sr be the old donor-32 D section and S'r any new invertible section. Let
Qr be any invertible common readout chosen on the unchanged retained fibre
space im(Lr); identity readouts are the special case Qr=I. Retaining whole
isolation and those readouts forces the effective source tuple on Lr to be
the old tuple composed with Sr (S'r)^(-1) Qr. Therefore the new sixteen-row
off-D response on K is exactly

    M X, where
    X = [ S48 (S'48)^(-1) Q48 W48 ;
          S73 (S'73)^(-1) Q73 W73 ].

Each eight-by-four block of X has rank four, whatever the new source extension
or compatible D word. No fixed 88-coefficient rectangle is required here.
The common readouts Q48 and Q73 may be chosen independently; the proof needs
only that they are invertible and common to the donors at their receiver.

## 4. A uniform rank-two leakage lower bound

If MX vanished, every column of X would lie in ker M. Its first block would
then have rank at most the projection rank two, contradicting its rank four.
More quantitatively, if u lies in ker(MX), then the first block X48 u belongs
to pi48(ker M). Since X48 is injective on its four-dimensional parameter
space, dim ker(MX)<=2. Hence

    rank(MX) >= 2.

Thus donor 32 necessarily has nonzero proper off-D response on K. K cannot
belong to its whole receiver-95 inverse fibre, whereas the preserved H
observations force it into source 61's. A common entire receiver-95 fibre is
impossible under the stated contract.

All fixed coefficient identities and rank statements persist under field
extensions. Tensor repetition by a positive integer k gives projection rank
2k and full block rank 4k, yielding leakage rank at least 2k, including
arbitrary linear source and D maps mixing copies under the same interfaces.
No nonlinear-source claim is made.

## 5. Relationship to the successful diagonal readout

The diagonal-code candidate supplies a common injective actual D readout on
K. This theorem shows why that success cannot be completed by further D
retuning or source coefficient changes under the same surrounding interfaces:
at least one other proper D record must still carry information about K.
The theorem excludes the entire 833-dimensional affine family, and indeed
a larger class of changed D words, rather than only that displayed candidate.

The construction programme must now change at least one stated premise:
H processing/ownership, the retained H anchor interfaces, or the receiver-48
and receiver-73 fibre subspaces. Another fifth receiver is outside this
receiver-95 theorem. Costs, native multiplicity, all five foundational
assumptions and the full multiplier remain separate obligations. No new kappa.

## Verification

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-coupled-fifth-review-s033/wave3/isolation_gate.py \
  --repo . --out /tmp/s033-universal-isolation-review
```

Expected status: `PASS_UNIVERSAL_FIXED_H_RECEIVER95_ISOLATION_GATE`.
The saved certificate includes the full-30-input factorizations, the sixteen
H-only anchor decompositions and the minimal donor-32 matrix. Controls include
the actual source-61 isolated four-space, a rank-two projected kernel and a
corrupted matrix rejected by the kernel identity. Native generator visibility
and full H output membership are independently reconstructed from the pinned
root-table inner products and A2/D4 incidence lists. The physical owner labels
themselves remain inherited source data; arithmetic and all new matrix
identities are independently reconstructed here.

Credit the root's kernel-projection observation, @CubeJerry, S031/S032 sources,
the S033 construction worker and retained geometry/compiler contributors.
Substantial OpenAI assistance. Independent agent review, not human/kernel
certification. Apache-2.0.
