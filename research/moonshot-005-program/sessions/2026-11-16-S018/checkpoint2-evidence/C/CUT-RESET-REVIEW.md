# Independent review of the known-source cut reset

**Final theorem and both physical47-output controls: accepted.** This
review binds root's final qualified proof at SHA256
`ed754aec0a04d4e9d4bf44f80bb09145d365f8365649db5d2c975c9447505d28`.
The extension to arbitrary intermediate original-Y feedback is correct.
The earlier reviewed proof pin was
`42b82eed13017355e34d4797a1ae40d6480f9cd321607eb376c3adba44e9d0f1`;
its optional Hub-side-information aside was subsequently clarified as
requested below. That qualification is now explicitly present and accepted.

## Independent algebraic proof

Write the old cut state as

    X=x,  Y=y+B x_S,  Z=C x_S.

Only the original Y fields contain arbitrary y columns. Write the final
public blocks of the fixed continuation on independent boundary variables
as

    X_out=A X + P Y + Q Z,
    Y_out=L X + H Y + K Z.

The boundary variables Z need not in fact be independent; this notation
only describes the continuation's fixed linear map before substituting
the actual cut values. All intermediate Y-to-X, Y-to-owner and joint
operations are included in these blocks.

Correctness of the original word on every independent y forces P=0 and
H=I. This argument uses exactly the theorem's stated cut hypothesis: no
other cut field contains an initial y column. Zeroing B and C changes no
homogeneous y block. In the reset execution, X_out=A x and Y_out=Lx+y.
The old correct identity implies A-I and L-D are supported only on the
known S columns. Inserting the actual ground preload -(L-D)x therefore
changes final Y by precisely that amount and changes final X by zero.
An actual inverse of A at Hub then restores all originals, if A is
invertible.

This is the M=I homogeneous-Y specialization of C's separately written
`GROUND-OUTPUT-NORMALIZATION.md`. It needs no prohibition on intermediate
Y feedback. It also does not grant remote access to an initial y, a known
x_S coordinate, or a historical owner row.

The pure-original reversible-X grammar is a valid sufficient condition for
A=I: its original-X evolution depends only on the cut raw originals, so
changing owners and known output offsets cannot alter it. General
continuations need the stated matrix test. Direct original movements and
zero births at the old live charts preserve every future geometric
co-location. The formula for the initializer's movement and the binary
inverse bound are valid. Added ADDs, owner births/retirements and downstream
compiler expenses remain present.

## Actual source and continuation audit

`review_cut_reset.py` imports no A or root execution/checking code. It uses
C's separate rational-space native interpreter, authenticates the original
root source, reconstructs every native line/facet, and replays all222
columns of both physical words:

* Old control:
  `ffb84c8b14f460818b34dbcfec5e099a6d712ce5d46dd9218b9553bd2b9aad61`.
* Reset control:
  `7c70a61320a81bed31f70378be8be0668244024058bbbc418f3b575873ec6bcf`.

The pinned A source is
`c7cf9a565d5dd6613342274979a9aa5de1bbb209cc3704a2a19e60eecb034245`.
At its declared cut758 there are94 live owners, whose actual row span has
rank45 and whose exact combined source support, together with Y offsets,
is S=T46 union {61,67}, of size48. Every original X is raw:78 at native
lines and33 at Hub. Every original Y has its own independent y column.

The old control changes only the placement of Y13, keeping it at ground
until its new reader operations. The independent review checks that its
prefix is literally the source prefix with that one MOVE removed. It also
checks that the reset's continuation is literally identical to the old
continuation, followed by the declared two-ADD Hub inverse. All94 cut
owners are actually zero at the same charts in the reset, and all initial
ground-preload operands were physically captured and descended.

The useful nontrivial differences are reconstructed, not read from the
author's result. Before the new inverse, the actual X5 row is

    x5+x29+x42,

while every other X is raw and all111 are physically at Hub. This complete
original matrix has rank111 and zero arbitrary-y block. Actual X29 and
X42 therefore supply the two displayed restoring ADDs. Independently
removing the ground preloads shows that the additional Y13 discrepancy is
x7; its actual RESET_RAW7 read cancels it. Every other required preload
is also recovered from the difference of full endpoint rows.

The control itself has no Y-source operations. It tests actual source
resetting, known output offsets and a nonidentity original restoration
matrix. The wider Y-feedback conclusion rests on the block proof above,
not on claiming that this one word exercises every permitted operation.

## Additional actual Y-feedback variant

Root subsequently supplied a separate positive feedback variant. This is
also independently accepted using the same C interpreter with no root
execution code. Its old and reset word pins are, respectively,

    4baab219091309a0191cb351ba091b5f32f6912b408be78e0d01b4ab887dc396
    1f0bd254b3e9316f02b31701f593ed361bae99eadc8b02283666d79e22bc7ab8

The same source support, literal continuation identity, actual ground
preloads, rank111 original matrix and two-ADD Hub inverse all pass. At F13
the real original X0 swaps with Y13, so X0 actually contains y13+x7.
The new descending packet is added to this mixed X0, and the second real
swap restores X0=x0 and leaves Y13=y13+x13. The independent trace checks
both mixed and restored rows, and every operand is actually at F13.
Omitting a Y13-to-X0 swap ADD is independently rejected.

This variant has143 INIT,110 ADD,273 MOVE,143 CLEAR,49 dirty clears and
peak95 owners. Its profile is50[1]+[3]+[4]+[6]+220[7], with independently
enclosed movement1587.9915706813019147724859155024257... and necessary
limiting room33.7593095298504404737602348645693.... The extra split is the
actual native-to-F13-to-Hub route of X0. Seven rejection controls, including
the separately reconstructed singular fixture, pass. Results are in
`cut-reset-feedback-review/RESULT.json`; use `--feedback` with the review
script to reproduce this second replay. The generalized feedback theorem
therefore has a positive physical control as well as the block proof.

## Complete independently recomputed ledger

Both physical words complete exactly47 targets, including13, and preserve
all other arbitrary original inputs. The reset counts are143 INIT,104 ADD,
272 MOVE and143 CLEAR, with49 dirty clears and peak95 owners. The movement
profile is

    49[1]+[3]+[4]+221[7].

Independent exact integer200th-root bounds give

    Q=1587.9773068000523925593453697576131...,
    necessary limiting room=33.7735734110999626869007806093819... .

The direct48 reference is independently recomputed as

    48[1]+222[7],
    Q=1586.9535942222049378881997678350504...,
    necessary limiting room=34.7972859889474173580463825319446... .

These prices are complete finite partial-word movement ledgers. They are
not all111 supplier prices, finite-multiplicity completion margins or a
new exponent. The exact rational enclosures are in
`cut-reset-review/RESULT.json`.

Five independent omission controls reject missing Y13 preload, missing
native capture, missing physical ground arrival, missing owner retirement
and missing final Hub inverse. A separately reconstructed native singular
fixture first verifies the old correct endpoint, then zeros the old
restoration owner. Its reset original map is diag(0,1,...,1), rank110,
with kernel e0. The native endpoint interpreter rejects the forced reset.
This demonstrates the necessity of the restoration condition and does not
exclude an additional actual paid source of the missing direction.

## Confirmed qualification for the optional side-information aside

The final proof's sentence citing `rank[M;C_Hub]=n` for additional actual
Hub side records now explicitly requires pure-X sides. For sides with
arbitrary-y nuisance it instead invokes the full-column observation
criterion and includes the x+y counterexample. This resolves the review
qualification. The main theorem retires all owners and uses invertible M,
so its main conclusion and controls were unaffected throughout.

With arbitrary intermediate Y feedback, an optional retained Hub side row
can contain unknown y. Its X projection alone is not a usable raw side
row. For example, an original z=0 and a side field s=x+y have stacked
X-projection rank1, yet the input pairs (x,y)=(0,0) and (1,1) are
indistinguishable and require different x outputs. In that general case
use the full-column observation condition: the desired pure-X rows must
belong to the actual Hub observation row span on all independent x/y
columns. For y-free sides this reduces to the stated stacked-rank test.

## Scope

The reset is a substantive reduction of a known-source prefix, conditional
on a real legal continuation and its restoration matrix. It does not build
the remaining64 increments or remove any future source acquisition,
decoding, movement or ordinary cost. Both strict suppliers, full recursion
and all five foundations remain open: native_all_columns, owned_erasure,
compiler, precision_tape and analytic_recovery. Credit @CubeJerry, root's
reset proof, A's pruning, C's projection/conduit and their predecessors.
Review performed with substantial OpenAI assistance.
