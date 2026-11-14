# Independent review of the common-preload staircase rank theorem

**Accepted for the exact stated interface. No new kappa.**

The root reviewer checked the universal argument rather than inferring it
from the pentagon enumeration. Restricting to selected X coefficients is
valid even with arbitrary original-Y precoding or independent extra inputs.
The two-gate interaction leaves the packet equal to the old receiver, so
correctness forces A_i=H+J_1+...+J_i. The last local source space is zero
because each selected nonzero real vector fails its own perpendicular
constraint. Subtracting the last equation gives the required tail forms
modulo the common preload code.

For each bad position j, the rows for tail j-1 and columns for input j
have identity diagonal: j is not local by definition. Every block below
that diagonal is zero, since an earlier source fails its own perpendicular
constraint and has already left the later tail. The resulting block
upper-triangular minor has determinant one for arbitrary block size and
field. This proves bV without scalar, commuting or genericity assumptions.

Sharpness is exact in the relaxed interface: put all bad coordinate blocks
in the common code. Future good coordinates are local at every earlier
stage. Taking H as the sum of all selected X inputs and the specified
prefix-Y precoding realizes the feedback identities. This does not grant
a physical acquisition schedule. Good positions form an orthogonal set;
putting a maximum such set first proves the optimized value(s-omega)V.

The root's separate native checker reconstructs the exact source and
confirms its eight coordinate axes, hence omega=8 by the ambient real
dimension. It independently verifies the specified pentagon is a5-cycle
and has no triangle. Across its120 orders,80 have three bad positions and
40 have four. Therefore the native111 example requires103 common widths
and the pentagon requires three, within this interface. These statements
are not general packet-count lower bounds for interleaved histories.

The author has separate finite local-completion and illegal-locality
controls. Those checks support the concrete examples; the universal proof
is the block minor and explicit sharpness construction. No physical source,
supplier, recursive composition or foundational discharge is claimed.

Reviewed for @CubeJerry with OpenAI assistance, independently of the author
worker's verification implementation. Source premises are reconstructed in
the companion `bit-kronecker-quotient-gate/review-root/check_native.py`.
