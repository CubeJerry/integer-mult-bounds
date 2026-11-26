# Independent review of the row-space orbit compiler

Decision: **accept RO1–RO5 in their stated complete-fibre, wide-record
model**. The local compiler is a positive tape implementation result
once its orbit layout is supplied. The entry/exit converter is explicitly
paid and remains too expensive for a new multiplication envelope.
The child block formulas are exact algebra, not physical time lower bounds.

Reviewed Route A file: rowspace-orbit-compiler.md, SHA-256
b8c07d0cfc933636f4182555d5a41578167ebb58959be119bd5eaa5562117c40.

The relevant primary-source interface was reread in OpenAI math
3344da59991ed94f9ba711217b29c1d760badfa6, Fourier build/kernel.tex and
binary.tex and tape build/walsh.tex. Its address changes apply one
invertible binary matrix to every column; its numerical child is a
one-slot Walsh transform on independent complete records. The review
does not assume that the original source already supplies orbit order.

## 1. Orbit coordinates and compact ranking

An \(A\times f\) matrix defines a surjective map onto its row space.
Two such matrices with the same image differ by an invertible change
on the \(A\)-dimensional domain: choose compatible preimages of a basis
and then bases of the kernels. Thus row space is exactly the orbit
invariant, including deficient rank and the zero matrix.

For the canonical \(r\times f\) RREF basis \(B_W\), uniqueness in
\(X=CB_W\) follows from row independence. The columns of \(C\) form an
independent ordered \(r\)-tuple in \(\mathbb F_2^A\), giving the stated
product \(h(A,r)\). In particular its binary rank requires at most
\(Ar\le Af\) bits, even when \(f\) is arbitrarily large.

For the next column after \(j\) independent columns, the prefix
projection from their span has kernel dimension \(j-\rho\). A prefix
in its image has exactly \(2^{j-\rho}\) forbidden extensions; a prefix
outside its image has none. Subtracting these from \(2^{A-t}\) and
multiplying the number of choices for later independent columns gives
RO2. At most \(A^2\) decisions use polynomial-size binary integers and
Gaussian elimination arrays. No group table or enumeration over all
\(2^A\) possible vectors is required by the algorithm. A conservative
fixed polynomial bound, comfortably below the declared power 12,
covers the simple schoolbook implementations.

## 2. Why the tape and metadata bounds are valid

The complete-fibre and width conventions are essential, and have been
made explicit during review:

- Every fibre contains all \(2^{Af}\) addresses once, with arbitrary
  independent payload.
- The encoded record width is at least \(Af\) plus its row-address width.
  One-bit payloads acquire this metadata cost rather than receiving it free.
- Each orbit block is ordered first by role, then by local \(C\)-rank.
  Each role subblock can be sorted independently.
- Spectators are already outer indices of contiguous complete fibres.
  Converting strided source spectators into this form is separately paid.

Headers are \(O(Af)\) bits per nonempty orbit. Each header can therefore
be charged to at least one record of width at least \(Af\), giving an
absolute volume factor, not a factor equal to the number of orbits.
The reusable \(O(A^2)\)-bit control workspace fits the complete-array
volume \(V\ge2^{Af}Af\), uniformly even when \(f<A\).

Within a role subblock, \(C\mapsto MC\) permutes the full-rank coefficient
matrices. Its destination ranks are exactly the integers from zero to
\(h(A,r)-1\), once each. A stable binary radix pass uses a fixed pair of
scratch streams and scans, rewinds and concatenates the whole subblock.
At most \(Ar\le A^2\) passes are required. Appended destination keys have
at most \(Af\le w\) bits, so they enlarge encoded records by an absolute
factor. Rank calculation costs polynomial \(A\) per record and scanning
costs its full width; both are covered by \(O((A+1)^{12}V)\).

Repeated passes, roles and orbit blocks reuse the same scratch intervals.
Input and final output occupy a fixed number of global intervals, while
temporary streams need at most the largest block's size. Thus the union
of all visited cells is \(O(V)\), rather than merely \(O(V)\) live cells.
The argument requires these fixed marked intervals and rewind discipline;
retaining one scratch area per orbit would not prove the claim.

A fixed polynomial number of role maps or row-mixing scans can increase
the polynomial degree in \(A\), but not the number of retained full payload
arrays. This is why the extension is a fixed polynomial bound, not a
claim that the particular exponent 12 survives an arbitrary polynomial
number of successive operations. Numerical arithmetic and precision
remain separately priced as the statement requires.

## 3. The converter is genuinely paid in both directions

The corrected forward key is \((W,\mathrm{role},C\text{-rank})\);
the inverse key is \((\mathrm{role},X)\). Both sorts act within each
already-outer spectator fibre. Including the role is needed: sorting
only by \(X\), for example, would produce address-major rather than
the specified role-major order when several roles are present.

For a fixed polynomial role bound, the role tag has \(O(\log(A+1))\)
bits. A canonical RREF key, its rank field and the \(C\)-rank together
have \(O(Af)\) bits. Elimination and reconstruction cost polynomial
\(A\) times \(f\) per record, and \(w\ge Af\) pays that work. The
\(O(Af)\) radix passes therefore establish the displayed

\[
 O\!\left(V[(A+1)^{12}+Af]\right)
\]

time with an absolute visited-space coefficient in each direction.
No fast global sort is assumed. If source spectator fields are
strided, their rearrangement is an additional bill and may be larger;
RO3 does not erase it.

At \(A=2\), applying the row-exchange matrix in orbit layout and
converting back is interchange of two complete \(f\)-bit fields.
Thus a linear-time converter in this same encoded model would imply
a linear-time interchanger. This is a valid conditional implication,
not a proof that such a converter is impossible.

## 4. Fourier support and full-rank blocks

RO4 follows from the literal first-row Walsh transform of the zero
address. Every \(y\in\mathbb F_2^f\) occurs with nonzero amplitude.
The resulting row spaces are zero and the distinct nonzero binary
lines, giving exactly \(2^f\) blocks. Consequently a processor that
preserves every orbit block cannot implement this child. Support
count alone does not say how much a collective processor must cost.

For RO5, a nonzero Walsh matrix entry requires the ordered spectator
rows to coincide. Full rank forces them to be \(A-1\) independent
vectors in \(W\cap W'\). This proves the zero case and, when the
intersection has dimension \(A-1\), indexes the direct summands by
ordered bases of that intersection.

Within one summand the first rows are the two affine cosets
\(x_0+U\), \(y_0+U\). The fixed offsets produce invertible sign
diagonals, leaving the character matrix
\((-1)^{u\cdot v}\) on \(U\). If the restricted bilinear form has rank
\(t\), independent row and column basis changes put it into a rank-\(t\)
diagonal form. Over the numerical scalar field \(\mathbb R\) or
\(\mathbb C\), its character matrix is a \(t\)-bit Walsh matrix tensored
with an all-ones matrix. Its rank is exactly \(2^t\), including
degenerate and isotropic cases.

Distinct spectator tuples have disjoint supports, so summand ranks add.
When the form is nondegenerate this gives
\(2^{A-1}|\mathrm{GL}_{A-1}(\mathbb F_2)|\), equal to
\(h(A,A)/(2^A-1)\) by the ordered-basis count. The binary address rank
and the real/complex numerical matrix rank must not be conflated.

## 5. Scope and next gate

The result improves the local representation of columnwise address maps:
their destination keys depend on \(A\), not the long slot width \(f\).
It does not supply cheap entry/exit, a child algorithm in the same layout,
bounded normalized recursive mass, or a complete numerical precision
theorem. In particular a support count or a sum of matrix-block ranks
cannot be used as a tape-time invoice without an additional executor
restriction.

This written independent review found no remaining blocking gap after
the fibre, role-order, spectator and scalar-field clarifications.
It is not a full tape execution, a Lean proof of RO, human refereeing
or a new unconditional multiplication bound.

Prepared independently by S005 Route C for @CubeJerry, with substantial
ChatGPT assistance. The elementary orbit and character identities retain
their standard mathematical provenance; no priority claim is made.

