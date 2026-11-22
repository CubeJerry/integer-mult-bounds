# Actual receiver95 readout, physical compilation, and the remaining isolation gate

**Accepted local source/D realization and actual forced-four-space readout.
The fifth whole receiver remains unbuilt.** No new complete κ or foundational
discharge follows.

## Independently checked actual readout

The checker reads the source-pinned S032 actual ingress matrices P_j, the new
full source gauges G_j, the fixed forced four-frame K and actual D owner rows.
It computes B_j=P_j G_j K directly. It does not import the pencil constructor
or use its section-inverse formula as the physical readout calculation.

For the eleven native donors, the literal new T satisfies

    T[O95] B_j = R,       rank R=4,
    rank Z=24,           rank[Z B_61]=28,
    rank T[O95,V]=8,      T[O95] Z=0.

Thus all eight actual receiver95 rows, not merely an abstract four-row decoder,
give the same injective readout on K. The overlap dimension of the retained48
and73 row spaces is2. The sharper three-receiver gate therefore permits rank24;
this candidate attains that necessary gate exactly. Since the contrast
annihilator has dimension8, its row space is precisely the actual95 native
row space.

The separate full-gauge composition review checks all308 literal source
quotients against F_old G_j, actual early-owner preparation, all whole paired
H fibres and all44 retained D frame identities. Every144 geometric D section
and both19/16 phase ranks are separately verified. Those checks pass using
arithmetic separate from the root gauge constructor.

## Exact physical bill

All11 changed source phases were compiled and symbolically replayed on their
31680 original binary columns. The changed D word was replayed on all210
columns, with arbitrary late baselines, and all pure phase inverses passed.
The280 unchanged H receipts are reused explicitly. The D per-base counts are
6436 early ADDs per direction,4608 late ADDs per direction,114 original-early
cache copies and5237 cross ADDs:27439 ADDs including pure inverses.

The gross eight-lane source/H/D bill is **454477664 ADDs**,540056 above the
S032 four-receiver physical baseline. INIT and dirty CLEAR remain279648 each;
the16 gap6 field exports and their96 binary MOVE records remain. No MOVE is
added. This is62568 ADDs below the three-overlap realization, while closing
its missing actual-row readout condition. It remains a local replacement bill;
global inverse placement, canonical return and the complete supplier invoice
are not supplied.

## Off-D isolation is still absent at ten donors

Equality of actual D outputs on K does not make K a common isolated source
space. To check this directly, the reviewer reconstructs each current source's
proper96-by96 receiver95 matrix from the pinned earlier proper matrix and its
S032 source gauge. It binds the eight D ingress rows to the actual owner labels
and independently checks equality with P_j. The other88 rows are the selected marked off-D observations in this protected
proper restriction. Nonzero response on these rows already proves leakage;
adding any omitted observations cannot remove it. Their restrictions after
the new gauge have ranks:

| Donors | Selected marked off-D response rank on K |
| --- | ---: |
| 61 | 0 |
| 0,45,62,100 | 2 |
| 32,35,38,68,69,90 | 4 |

The candidate therefore retains the genuine isolated four-space at donor61,
but that same four-space still leaks to other D packets at every other donor.
No claim of a fifth common whole eight-dimensional fibre is justified.

## A sharper source-isolation obstruction for the gauge family

Let L denote the32-dimensional sum of the four retained source frames, and
let C_j be the88-row selected marked off-D proper observation map at receiver95 in the
current S032 source system. Exact reconstruction gives

    dim(ker C_j intersect L) = 4  at j=61,
    dim(ker C_j intersect L) = 2  at each of the other ten donors.

The checker evaluates C_j L directly: the respective ranks are28 and30.
These numbers are intrinsic to the frozen proper-source diagram.

For any invertible source gauge G_j preserving L setwise, and any
four-dimensional space K0 contained in L,

    rank(C_j G_j restricted to K0)
      = 4 - dim(G_j K0 intersect ker C_j)
      >= 4 - dim(L intersect ker C_j).

Consequently the leakage rank is at least2 at every donor other than61.
The full source-gauge theorem fixes each retained-frame span, hence preserves
their sum L. It lies inside this obstruction's scope. No retuning of that
gauge lift or of invertible D sections can isolate the forced four-space
at all eleven donors while the underlying proper-source diagram and L remain
fixed. This is a quantified dimension obstruction, not a finite search failure.

This sharpens the next obligation: actual receiver95 readout equality has
been achieved, while its common isolation requires a changed source/H
information diagram (or a contract change that leaves this fixed-L gauge
scope). The result neither excludes such a redesign nor supplies one.

## Reproduction

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-coupled-source-validity-s033/global-gauge-pencil/review_actual.py --repo . --gauges research/moonshot-005-program/results/bit-coupled-source-validity-s033/global-gauge-pencil/GAUGES.json.gz --out /tmp/s033-pencil-actual-review
python3 -B research/moonshot-005-program/results/bit-coupled-source-validity-s033/compile.py --repo . --candidate research/moonshot-005-program/results/bit-coupled-source-validity-s033/global-gauge-pencil/CANDIDATE.json.gz --out /tmp/s033-pencil-compile
python3 -B research/moonshot-005-program/results/bit-coupled-source-validity-s033/review_global_gauge.py --repo . --gauges research/moonshot-005-program/results/bit-coupled-source-validity-s033/global-gauge-pencil/GAUGES.json.gz --candidate research/moonshot-005-program/results/bit-coupled-source-validity-s033/global-gauge-pencil/CANDIDATE.json.gz --out /tmp/s033-pencil-source-review
```

Expected first status: `PASS_INDEPENDENT_ACTUAL95_PENCIL_FORCED_K_READOUT`.
The coefficient identities and ranks persist under coefficient extensions;
direct-sum repetition scales the isolation bound. All five foundational
assumptions and all unbuilt whole interfaces, return and caller remain explicit.

Credit @CubeJerry, S033 pencil construction/root gauge theorem/adversarial
review, S031/S032 source/H/D interfaces and atlas/compiler predecessors.
Substantial OpenAI assistance. Independent agent review, not a human or
formal-kernel proof. Apache-2.0.
