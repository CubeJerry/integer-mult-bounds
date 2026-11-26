# Independent review of Bell encoding at the integer-caller boundary

Decision: **accept BO1–BO8 as exact boundary identities and scoped
invoice calculations**. They preserve the positive BE local algebra
and do not lower-bound all encoded multiplication or convolution algorithms.

Reviewed Route B file: bell-outer-boundary.md, SHA-256
d9c5190ab0dcaf5b3418848f93bbeb7a3d6dd9378bb1f2ec9b27d1798cefa045.

The ordinary caller and its chirp/phase construction were independently
checked in OpenAI math 3344da59991ed94f9ba711217b29c1d760badfa6,
tape build/integers.tex. The identities below were independently derived
from the explicit Bell transform.

## 1. Product normalization and full input dimension

At fixed \(u\), the encoding is the normalized Walsh of
\(z\mapsto f(z,z+u)\). Inserting both inverse expansions, character
orthogonality contributes \(Q\) when the two frequency indices sum
to the output label. Three factors \(Q^{-1/2}\) therefore leave

\[
 Q^{-1/2}\sum_w\widehat f(u,w)\widehat g(u,v+w).
\]

The normalization is \(Q^{-1/2}\), not \(Q^{-1}\) or one.
There is no operand conjugation: the source uses an ordinary bilinear
pointwise product and the Walsh characters are real.

The \(Q\) complete fibres each have \(Q\) entries, retaining all \(Q^2\)
independent values. Transforming every fibre is a call on the full
corresponding volume, not a \(1/Q\)-volume child. The two one-entry
adverse inputs correctly reject encoded pointwise multiplication.
Unitarity and \(\|f\odot g\|_2\le\|f\|_2\|g\|_2\) give the stated
stability estimate. The missing ingredient is improved physical execution.

## 2. General diagonals and the third-root control

Two normalized transforms give the kernel

\[
 \kappa_u(t)=Q^{-1}\sum_z(-1)^{t\cdot z}d(z,z+u),
\]

hence the claimed convolution on \(v\). For the paired phase
\(\operatorname{diag}(1,\omega)^{\otimes2}\), the \(u=0\) diagonal is
\((1,\omega^2)\), so the Bell conjugate is

\[
 \frac{1+\omega^2}{2}I+\frac{1-\omega^2}{2}X.
\]

Both coefficients are nonzero. The zero Bell address therefore reaches
\(u=0,v=1\), outside the zero row-space block.
In \(\mathbb Q(\omega)\) the two coefficients are \(-\omega/2\) and
\(1+\omega/2\); their squared moduli sum to one and their cross inner
product is zero. The matrix is unitary. The failure is independent
of numerical error, conditioning or unequal paired masks.

This does not contradict BE, whose real quadratic-sign keys do not
include a primitive third-root phase.

## 3. The actual outer interfaces are not already covered

The source chirp has
\(\chi(j)=\exp(2\pi i(j^2+(\ell\bmod2)j)/(2\ell))\).
For odd \(\ell>2\), \(\chi(1)=\exp(2\pi i/\ell)\) is not a binary
sign. The source also prepares general unit-modulus phase ratios.
Thus its full phase interface cannot be inferred from BE's inner
quadratic-key repair interface.

BO4 is correctly described as a control against an unrestricted
extension, not as an entire large source layer. Actual phase tables,
borrowed coordinates, changing pairings and inverse layouts need
their own encoded execution theorem. A common Bell pairing is not
promised by the synchronized-short-transform lemma. The retained
rounding/carry routine also requires the ordinary ordered coefficients.

## 4. Shared boundaries and the six-call ledger

Interior \(E^TE\) pairs cancel when all stages share one encoding.
This already benefits BE's complete local algebra; the external
input and output transforms remain.

Even with all intervening linear stages supplied cheaply, the source
multiplication graph has two input encoders and one final decoder.
The standard encoded product adds three full-volume half-width
Walsh transforms, one for each operand and one for their output.
The total is six, matching separate wrapping of the two forward
transforms and the adjoint.

This is an accounting statement for that implementation. It does not
exclude a different bilinear executor, a proved structural cancellation,
or a changed caller exploiting actual digit padding.

## 5. Defined positive invoice and rounded shapes

For the explicitly defined positive bill
\(B(a)=2B(a/2)+P(a)\), expanding the recurrence gives at least
\(2^h\) positive base occurrences. Bounded \(P\), or
\(P=O(a^\eta)\) for \(\eta<1\), gives linear upper order as well.
A local \(O(a)\) converter gives an \(O(a\log a)\) upper bill.
An algorithmic upper recurrence alone would not lower-bound actual
execution time; the note correctly avoids that inference.

On exact shapes \(a=2Af\), the two endpoint expansions have total
child-volume ratio \(2b_A\) and child width \(a/(2A)\), giving
\(\sqrt2\,b_A/\sqrt A\). On rounded shapes the same expression is
an upper bound because the actual even child width is smaller.
The \(O(A)\) remainder and all internal endpoint/converter bills
remain charged.

A future bounded critical template could absorb the extra constant
in a polynomial-logarithmic potential. BO does not supply that
template or a fast converter.

## Independent exact replay

Command:

    python3 -I -B verify_bell_outer_independent.py

The checker uses integer Walsh numerators to test normalization
without floating-point square roots. It passed 16,383 product and
16,383 arbitrary-diagonal coordinates, a wrong-pointwise-product
control, exact cyclotomic unitarity/nonzero spill coefficients, and
11 defined endpoint-invoice cases.

The receipt is bell-outer-independent-verification.json.
The unbounded character proof carries the theorem. These checks
neither prove nor exclude an improved convolution executor.

Prepared independently by S005 Route C for @CubeJerry, with substantial
ChatGPT assistance. The Fourier product identities retain their standard
provenance; no new unconditional bound or priority claim is made.

