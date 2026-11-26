# Independent review of the full-rate paired Bell executor

Decision: **accept BE1–BE5 as exact algebra and a guarded local physical
compiler in the supplied orbit layout; accept BE0/BE6 as the stated
conditional endpoint invoices**. Neither invoice yields a new complete
multiplication bound. The half-width transforms and present converter
remain real costs.

Reviewed source: Route A, paired-column-bell-executor.md, SHA-256
840492fcefb4d7f7accf68e1591e81bdfe3070b6de26e9d38c468516858aa5d3.

This review independently derived the character identities, reread the
actual source masks, and implemented a separate exact checker without
importing the author's code. It includes rank-deficient and dependent
translation logic. It is not a Lean proof or a full tape-machine execution.

## 1. The basis change preserves all independent inputs

For a fixed pair of columns, distinct \(u\) give disjoint supports in
the computational basis. At fixed \(u\), characters indexed by \(v\)
are orthogonal. There are exactly \(2^{2A}\) such vectors, so \(E_A\)
is a square real orthogonal matrix. Tensoring over \(t\) pairs gives
the complete original \(2^{2At}\)-dimensional data space.

This is not an encoding onto equal copies of an input vector, a
symmetric subspace, or orbit averages. The two members of each pair
are address coordinates of the original complete array. Pairing them
does not reduce the number of independently supplied payload entries.

The physical realization of \(E\) is exactly one half-width Walsh plus
the stated invertible address permutation, and its inverse has the
reverse costs. Both half-width Walsh calls act on the full current
volume. Their cost cannot be divided by two merely because the number
of selected address bits is halved.

## 2. Generator phases and orientations

Changing the summation variable \(z\) to \(Mz\) gives the contragredient
label update

\[
 (u,v)\longmapsto(Mu,M^{-T}v).
\]

Using \(M\) in both label positions would be wrong for a general
nonorthogonal binary matrix. The independent checks include such matrices.

For paired coordinate Walsh, the literal character sum vanishes unless
the two output bits sum to \(v_i\). On that support its phase is
\((-1)^{u_i q_i}\), which equals the coefficient of the swapped Bell
state multiplied by \((-1)^{u_iv_i}\). Thus the claimed swap and sign
are correct. Across paired columns the phase is the sum of those
quadratic products.

A quadratic \(q\), including affine and constant terms, satisfies

\[
 q(z)+q(z+u)=q(u)+q(0)+z^TL_qu.
\]

Hence the shift is \(v\mapsto v+L_qu\), with phase
\(q(u)+q(0)\). The constant term must appear in this formula even
though it cancels in a pair of identical original masks.
The proof includes it. Composition with linear label maps preserves
quadratic degree, so the generator word remains a signed linear
permutation on the stacked \(2A\)-row label matrix.

## 3. Arbitrary rational tables and dependent translations

A nonlinear table \(F\) of the original full-column parity keys becomes
\(F\) of the paired generators. It is generally **not**
\(F\) on the first half tensored with \(F\) on the second half.
The proof uses the former, correct functional calculus.

At fixed \(U\), all generators translate \(V\) by matrices
\(\Delta_j=L_jU\). Select an independent basis of their span and write
\(\Delta_j=\sum_h\alpha_{jh}\Delta_{j_h}\).
The corresponding signed translation operators commute. After the
suborbit Walsh, their joint eigenkeys are exactly

\[
 k_j=\eta_j(U)+\alpha_j\cdot\lambda.
\]

If the shifts obey a relation but the associated signs do not multiply
to one, this affine key image is restricted accordingly. Nothing in the
algorithm requires all \(2^m\) keys to occur, an independent generator
for every key, or a table expansion over the Boolean cube.
The \(d=0\) case simply evaluates \(F\) at its constant attained key.

The independent checker uses a nonlinear rational function with unequal
denominators, repeated polar forms with different affine phases, and
zero polar forms. Its direct original-coordinate action agrees on
every tested Bell basis column with the subgroup-convolution formula.
This specifically tests the functional-calculus and dependency seams.

## 4. Full cosets remain inside every row-space stratum

The update \(V\mapsto V+L_jU\) is induced by the invertible block matrix

\[
 \begin{pmatrix}I&0\\L_j&I\end{pmatrix}
\]

on the stacked address. It preserves row space and rank without
requiring full row rank. Every linear combination of the shifts is
another such shear. Thus, once a single \(V\) belongs to a row-space
block, all \(2^d\) distinct members of \(V+D_U\) do too.

In canonical coordinates \([U;V]=[C_U;C_V]B_W\), multiplication by
\(B_W\) is injective on coefficient rows. The span of \(L_jC_U\)
therefore has exactly the same dimension as the span of \(L_jU\);
elimination cannot create or lose a translation relation. Each vector
has \(Ar\le2A^2\) bits. The dimension bound
\(d\le\min(m,A\operatorname{rank}U)\) follows because every row of
\(L_jU\) lies in the row space of \(U\).

Canonical reduction of \(C_V\) modulo this span, with its retained
coordinates, is a bijection. Consequently the sorting key
\((C_U,\overline C_V,\mathrm{role},z)\) preserves every input payload
and produces complete binary suborbits, including deficient-rank
and zero-shift cases. No inaccessible or initialized-only coordinates
are inserted.

## 5. Physical local execution and its precision guard

The compiler inherits RO's complete fibres, already-outer spectators,
wide encoded records, polynomial role count and common marked regions.
The coefficient keys have \(O(A^2+\log R)\) bits and also \(O(a+\log R)\)
bits, so metadata stays within an absolute volume factor under the
declared record-width convention.

Within each fixed suborbit, \(d\) is constant. Binary radix passes
align butterfly partners, two streams supply their operands, and
subsequent stages reuse the same intervals. Variable \(d\) across
different suborbits does not require a common padded length: the
dispatcher can process them successively. Serial role scans implement
a dense matrix \(F\), and sorting by role and full coefficient rank
returns the supplied orbit order. These operations have a fixed
polynomial-\(A,m\) scan bound and a fixed number of full arrays.

Reconstructing \(U=C_UB_W\) for the phases costs polynomial \(A,m\)
times \(t\), paid by record width at least \(a=2At\). Actual coefficient
evaluation is charged per attained key; its cost is not replaced by
unit-cost lookup or by a table of \(2^m\) entries.

Two numerical qualifications were added during this independent review:

1. BE5 now explicitly requires the CW-type guard
   \(k\ge C(A+m)^c\), \(a\le k\), and a fixed \(O(k)\)-bit working format.
   A bare polynomial coefficient-height bound would not guarantee
   an absolute encoded-volume factor for every \(k\).
2. Each unnormalized local Walsh has norm \(2^{d/2}\). The combined
   excursion before final scaling can be \(2^d\|F\|\), rather than
   merely \(2^{d/2}\|F\|\). The revised text gives this correct bound.
   Since \(d\le a/2\le k/2\), the extra margin is \(O(k)\) bits under
   the guarded coefficient heights.

This is a local finite-precision schedule with its costs exposed.
It does not by itself prove the complete NW error theorem; all new
rounding sites and their propagation must be included in any global
application. The normalized version can avoid the unnormalized growth
at the cost of the explicitly acknowledged square-root coefficient.

## 6. Applicability to the actual retained source

The source check was independent of the generic description of
binary.tex. The actual kernel/CW key is

\[
 k_j=\sum_{\text{columns}}
 \left(X_jZ_j+\sum_{\text{auxiliary }i}X_iZ_i\right)\pmod2.
\]

Initial/final phases and representative changes are bilinear column
forms; the coordinate changes are linear within each column. These
specific gates remain quadratic under substitution and satisfy BE4.
The phrase “fixed column functions” alone would permit higher-degree
masks and would not establish the result.

CW's Newton, defect-set, Vandermonde and division code computes the
actual rational table entry from the parity key in polynomial \(m\)
bit work and height. The Bell executor calls that evaluator on the
attained affine keys. It does not change the rational scalar field
to the binary address field.

Common pairing and the same form on both members of a pair are
essential. A degree-three mask or unequal paired forms can retain a
quadratic dependence on the Bell summation variable and spread over
several Bell states. The independent negative controls demonstrate
both failures. Arbitrary active/spectator coupling is also outside
the stated scope.

## 7. Endpoint invoice and decision

With the stated entry and exit, even an otherwise free local algorithm
has normalized child mass \(2\sqrt{1/2}=\sqrt2\). The simple recurring
upper bill is linear in active width. Replacing each endpoint by one
source-template expansion gives the displayed factor
\(\sqrt2\,b_A/\sqrt A\), counting both endpoints. Their internal bills
remain present.

The current orbit converter additionally costs \(Va\). These facts
prevent the local closure theorem from being a new complete
square-root multiplication bound. Conversely they are invoices of
the specified implementations, not lower bounds against all possible
converters or schedules. Any endpoint cancellation must be shown for
the complete application, with arbitrary independent inputs and its
numerical/space contract intact.

The positive result is precise: a single full-rate Bell/orbit
representation closes the retained paired linear, row-Walsh and
quadratic-key repair algebra with polynomial local physical work.
It changes the representation and thus does not contradict the earlier
ordinary-rowspace rank obstruction.

## Independent replay

Command:

    python3 -I -B verify_bell_independent.py --proof ../route-a/paired-column-bell-executor.md

The fresh checker passed 12,560 quadratic-mask basis columns,
12,388 paired-GL columns, 740 paired-Walsh columns and 592 nonlinear
rational-table columns. It includes 44 dependent-translation fibres,
five zero-translation fibres, and cubic/unequal-pair rejection controls.
All computations are exact integers or rational fractions.
The receipt is bell-independent-verification.json.

The finite replay supports the explicitly written unbounded proof; it
does not establish the physical time theorem by measurement. No
kernel verification, human refereeing or priority claim is made.

Prepared independently by S005 Route C for @CubeJerry, with substantial
ChatGPT assistance; the elementary Bell/Clifford identities retain their
standard provenance.

