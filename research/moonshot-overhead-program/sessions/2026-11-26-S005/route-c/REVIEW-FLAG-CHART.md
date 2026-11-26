# Brief independent review of the flag-chart identities and invoice

Decision: **accept FC1–FC4 and the corrected charged upper invoice**.
This review is limited to the coordinate and physical-accounting part
of the note. It does not independently verify the external paper,
its implementation timings or its formalization scope.

Reviewed Route A file: flag-converter-invoice-and-pivot.md, SHA-256
29bb1c05d2e7211a6d88da5f1267a0444d9582cd60c5fb3d322d82932a0aa852.

## Constant-density chart

When the first \(A\) columns form an invertible matrix \(C\), there is
a unique \(Z=C^{-1}X_{\rm tail}\), giving \(X=[C\mid CZ]\).
Left multiplication by \(C^{-1}\) produces the actual canonical
row-reduced basis \([I\mid Z]\). Thus the chart identity is exact.

The density is \(|GL_A(\mathbb F_2)|/2^{A^2}
=\prod_{j=1}^A(1-2^{-j})\). For \(A\ge2\), the first two factors
are \(3/8\), while the remaining finite product is at least
\(1-\sum_{j=3}^{\infty}2^{-j}=3/4\), giving \(9/32\).
For \(A=1\), density \(1/2\) satisfies the same bound directly.
Padding only the \(C\)-field therefore has an absolute volume factor
on this chart. It does not cover other ranks or pivot charts.

Moving its \(A^2\) control bits to the required field positions can be
paid by \(O(A^2)\) elementary address-bit moves. This is polynomial
local work independent of the long tail width. It does not implement
the controlled tail map \((C,Z)\mapsto(C,CZ)\): computing its destination
key is a separate task from moving the independent payloads there.

## Corrected long-width bill

Gaussian elimination gives polynomially many controlled row additions
and exchanges on the tail slots. The original draft omitted the
retained packed-XOR compiler's common root logarithm and its setup.
After this independent review the invoice was corrected to

\[
 V\,\operatorname{poly}(A)(1+I(f-A))(1+\log(k+2))
   +\operatorname{poly}(A,k).
\]

This matches the source distinction between an exact interchange
and an implemented binary slot addition. The guard/control degree is
fixed, and \(k\) is the unchanged numerical address/record parameter.
For a narrow exceptional tail, direct elementary bit operations fit
the displayed bound; for \(f=A\) the operation is the identity.

If fewer than three long slots are available, the packed-XOR
auxiliary slot can be taken from unused halves of the source/target
slots, with the residual bit handled directly. This uses a constant
number of smaller-slot calls, restored after use; a monotone
interchange envelope bounds them by the displayed width. For
\(A\ge3\), a separate complete tail slot is available.

The correction strengthens the unfavorable upper invoice. Neither
it nor generic radix sorting is a lower bound against all converters.
The full chart-to-all-input assembly remains open, as the note states.

## Dual coordinates

For an invertible full basis matrix \(M_B\), primal coordinates use
\(x=M_B(\alpha,\beta)\), while the Fourier dual uses
\(y=M_B^{-T}(\gamma,\delta)\). Converting the output back to primal
coordinates gives

\[
 M_B^{-1}M_B^{-T}(\gamma,\delta)
   =(M_B^TM_B)^{-1}(\gamma,\delta).
\]

The full matrix \(M_B^TM_B\) is invertible even if the restricted form
on the spectator span is degenerate. Its determinant is
\((\det M_B)^2\ne0\). Hence FC4 is valid, and determining output
orbit labels from \(\delta\) alone would need an additional special
basis or orthogonality hypothesis.

The brief review finds no remaining mathematical issue in FC1–FC4.
No all-input supplier, global overhead improvement, external literature
endorsement or universal converter lower bound follows.

Prepared independently by S005 Route C for @CubeJerry, with substantial
ChatGPT assistance.

