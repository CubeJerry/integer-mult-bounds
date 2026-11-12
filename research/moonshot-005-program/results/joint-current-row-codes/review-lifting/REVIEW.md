# Independent review of shared invertible column realization

**Accepted as a linear-algebraic interface over every field. No new kappa.**
The lead read the full proof and independently checked its necessity,
constructive sufficiency, sharp zero-padding width, reciprocal maps and
stated physical bill. The actual one/two-departure source words have a
separate independent source review; this algebra does not grant their routes.

Let A:F^r->F^m and B:F^d->F^m. If the first d columns V of an invertible r-by-r
matrix realize AV=B, V is injective and embeds ker B into ker A. This proves
both image containment and nullity(B)<=nullity(A). Conversely choose a
section J of A on its image and an injection H from ker B to ker A. For a
projection P onto ker B, V=JB+HP satisfies AV=B; Vx=0 forces Bx=0 and then
Hx=0, hence x=0. Extending V to a full basis proves sufficiency. These are
finite-dimensional arguments valid for finite and infinite fields, including
the zero-dimensional cases.

For A_s=[A,0_s], image containment is unchanged and nullity grows by exactly
s. Therefore the stated maximum of zero and the nullity deficit is sharp
within this invertible-column interface. Equal quotient columns do not imply
equal record values, and initial zero padding still requires genuine extra
primal and dual fields. The source proof correctly charges both records,
their real routing and later inverse operations.

I found and requested correction of one wording issue before freezing the
review: for d>r the nullity inequality alone need not fail without image
containment. The accepted text now includes that premise. The independent
checker preserves the counterexample A=0 (width two), B=I_3: the nullity
inequality passes but image containment fails. No main theorem was changed.

For a'=Z^{-1}a and b'=Z^T b, the old quotient is (AZ)a', and the displayed
inverse maps recover both full independent banks. The generic four-map
snapshot implementation costs 4n INIT, 4n CLEAR and
8n+2 nnz(Z)+2 nnz(Z^{-1}) ADDs, besides the 2s persistent padding fields.
Each map uses n temporary snapshots sequentially, so additional peak at most
2s+n follows. Erasing snapshots retains the explicit owned-erasure premise;
this is not claimed as a free reversible bit operation. The scalar count
also does not replace a precision or uniformity analysis.

`check.py` imports no author code. It enumerates every A,B in independently
chosen small domains over F2 and F3 and compares the criterion with the
actual set of products AV for all injective lifts V. It checks 90,512 matrix
pairs, includes r=0 and over-width requests, and preserves image and repeated-
column negative controls. This finite corroboration is distinct from the
universal proof above. `output/RESULT.json` pins the corrected author proof.

The source plus/minus instance requires characteristic different from two.
The general theorem still holds in characteristic two and correctly rejects
that singular requested pair. No characteristic-two source implementation,
complete supplier, or foundational assumption is discharged by this result.
