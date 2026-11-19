# Independent review of the fixed-transfer source-mask bridge

Root accepts the universal linear algebra statements in the pinned author
proof. This review was written after reading the proof and uses a separate
ternary enumerator; it does not import or rerun the author's binary checker.

The exact criterion is an equality of column images modulo the actual late
transfer, together with m<=b. Full row rank of the early source matrix is
surjectivity onto its m owner values, which establishes necessity. For
sufficiency, the author's decomposition into a section of the quotient
transfer and its kernel gives a square invertible coordinate change; extending
the independent quotient rows inside the b real source coordinates is valid
over the original field. The lift through the actual late transfer exists
column by column. No extra source fields are created.

The common output lift is correctly fixed before applying donor-wise criteria.
Allowing a different lift for each equation would discard the intended full
output geometry. The leakage identity follows because a surjective source map
sends the selected-output kernel onto the selected transfer's kernel. It
therefore measures actual information outside a selected projection. It does
not measure rank(I+B).

The minimum-rank proof also holds over small finite fields. The common
complement construction pairs basis vectors of two kernels after separating
their intersection. It uses no generic-field argument. The constructed image
S has dimension max(rank B,rank[C D]-rank D), at most b, so a surjective
source-domain map lifting the selected B exists. Applying the first theorem
then realizes that map with all m independent early values.

Independent finite verification over F3 exhausts 73,710 full-source target
criteria in output dimension two with b=2, m=0,1,2 and zero or one late
visit. It checks 80,966 attainable selected-target minimum ranks, 19,805
actual kernel-image leakage cases, and 3,888 injective-late rank controls.
A stored counterexample rejects the weaker equality-of-ranks condition when
the column spaces differ. Zero-source, zero-late and full-source cases are
included. These are finite controls supporting the all-dimension proof.

The physical bill is the inherited source compiler bill under its stated
actual-owner and inverse-placement premises. This review does not supply a
new coefficient-selection algorithm or review the author's separate native
literal-word checks. The latter remain distinct evidence with their own
word pins and reviewer scope. A complete receiver map, cheap return, strict
suppliers and the five foundations remain open. No new kappa.

Reproduce with `python check.py --author AUTHOR_DIRECTORY --out FRESH_DIRECTORY`.
The result pins the reviewed proof. Credit @CubeJerry, Worker B's theorem,
Worker A's native motivating example, and retained source-compiler authors.
Root performed this independent mathematical and computational review with
substantial OpenAI assistance.
