# Independent review of the square-encoder support budget

Decision: **accept SU1–SU4 and the finite positive-invoice tree
consequence in the stated full-volume encoder class**.
This is an elementary support argument and an invoice restriction.
It does not lower-bound unrestricted Walsh or multiplication algorithms.

Reviewed Route A file: square-encoder-support-budget.md, SHA-256
09d7fc8bd28b7309a8798732e4325b0f8c31bfaeac10bf9a9f18f6318b9da3fe.

## Support and cycles

The normalized Walsh entries all have modulus \(N^{-1/2}\).
For a nonzero real or complex vector \(v\), the infinity-norm bound
and Cauchy–Schwarz give
\(\|Hv\|_\infty^2\le s(v)\|v\|_2^2/N\).
Multiplying by the output support and using unitarity gives
\(s(v)s(Hv)\ge N\), with no positivity assumption on \(v\).

If \(HE=EM\) and \(M\) is invertible monomial, \(H\) maps each
nonzero column of the invertible \(E\) to a nonzero scalar multiple
of the column selected by \(M\). Multiplication of the uncertainty
inequality around a permutation cycle counts every support twice.
Taking logarithms yields the claimed cycle average at least \(a/2\).
No orthogonality or conditioning assumption on \(E\) is used.

Indeed \(H^2=I\) also forces \(M^2=I\), so only cycles of length
one or two can actually occur here. The more general cycle proof
remains valid and does not rely on this extra restriction.

## Encoder word and normalization

A full-array partial Walsh on \(s_i\) address bits can spread one
supported input coordinate to at most \(2^{s_i}\) output coordinates.
A monomial map preserves support cardinality. Applied to every
standard basis vector, the complete word therefore has uniform
column support at most \(2^{\sum_i s_i}\), regardless of cancellations.
SU2 forces \(\sum_i s_i\ge a/2\).

When entry and exit execute the stated word and its reverse, each
occurrence has the full parent volume. Thus the normalized recursive
mass is genuinely

\[
 2\sum_i\sqrt{s_i/a}
 \ \ge\ 2\sqrt{\sum_i s_i/a}
 \ \ge\ \sqrt2.
\]

The first inequality follows by squaring the nonnegative sum. Zero-width
identity calls do not affect it. If every \(s_i\le a/A\), then
\(\sqrt{s_i}\ge s_i/\sqrt{a/A}\), yielding the stated lower mass
\(\sqrt A\). Its failure of a uniform bounded-mass criterion concerns
an unbounded arity parameter \(A\); for a fixed \(A\) it is simply the
displayed constant obstruction.

Bell's one \(a/2\)-width call saturates the support and square-root
inequalities. The argument therefore rejects replacing it by a
quarter-width square encoder made from the same full-volume word class.

## Recursive consequence and exact scope

For a finite recursive tree in this class, the sum of child widths at
each internal node is \(2\sum_i s_i\ge a_{\rm node}\).
Induction gives total leaf width at least the root width. If all
terminal widths lie in the fixed positive range \([1,b]\), at least
\(a/b\) full-volume base occurrences are billed. Under the declared
positive base-call invoice this is a linear-in-width invoice.

This conclusion uses separately billed occurrences, the same full
parent volume at every descent, and no cancellation of endpoints
between adjacent computations. It does not apply automatically to
variable-volume check rows, rectangular encoders, additional independent
row sectors, discarded initialized coordinates, shared physical work,
or a new encoder operation. It also does not turn an upper runtime
recurrence into a lower bound for all implementations.

No finite numerical experiment is needed for these inequalities.
This independent review accepts the written proof as a scoped stop
rule for optimizing the Bell pairing constant, while leaving the
common-layout algebra and other endpoint mechanisms open.

Prepared independently by S005 Route C for @CubeJerry, with substantial
ChatGPT assistance. Support uncertainty and the elementary norm/count
inequalities carry their standard provenance; no priority claim is made.

