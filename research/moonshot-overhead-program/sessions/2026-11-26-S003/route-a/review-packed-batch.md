# Independent Route A review of packed leading-digit batching

Result: **accepted as a conditional local component**, subject to explicit
setup absorption. Reviewed `../lead/packed-batch-with-small-radix.md`,
sections 1--5, against source `build/interchange.tex` at OpenAI
`3344da59991ed94f9ba711217b29c1d760badfa6`.

The leading ell radix-b digits enumerate B=b^ell values. Extending to
C=W ceil(B/W) and interpreting z=W batch+row retains the existing
lexicographic order; no transpose is hidden. Since B>=W, beta=C/B<2.
The completed whole-row map preserves the genuine range z<B, so removing
padding is correct even if intermediate predictors mix rows. The 2a
reserve calls and direct exchange of ell leading and fewer than K
remainder digits complete the full swap.

The grouped-call contract requires actual prefix/gap/suffix layouts,
unchanged normalized sum of child volumes, and each child volume at most
one quarter of the padded volume. Under that contract, beta*q+2a is the
correct recurrence coefficient, and main child volumes are strictly below
one half of the parent. The source parking proof applies. Arbitrary
succinct matrices are not assumed to satisfy this contract.

The descriptor/setup term g(log(V+2)) must be absorbed at a stated
threshold or with an explicit constant. A polynomial whose degree depends
on the template can have a non-polynomial absorption constant. The note
retains this term separately and leaves its uniform degree/coefficients
to the complete compiler; invoke its polynomial prefactor only after that
gate. With this qualification, the stated induction and eta dependence
are valid.

This removes the logical necessity of b>W. It supplies neither small
endpoint coefficients nor a complete multiplication envelope. This is an
independent mathematical review, not a formal proof or tape execution.
Credits: source recursion, lead S003 batching, Jerry Chen (@CubeJerry),
and AI-assisted review.
