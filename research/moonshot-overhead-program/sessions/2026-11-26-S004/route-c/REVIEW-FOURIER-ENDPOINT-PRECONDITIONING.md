# Independent audit of Fourier endpoint preconditioning

**Verdict: pass for EP1–EP13 as a local source-compatible call-invoice
component, including the symmetric two-channel extension.** Reviewed
the frozen A draft with SHA256
`912524ffb4d5236fbba0abb404a474574f5bc15dfad21c0c9c00c457f2eec1b4`.
The result changes a finite local executor. It does not improve the
complete asymptotic multiplication envelope by itself.

## Endpoint and phase interface

I reread the pinned Fourier `build/kernel.tex` sections defining the
product queries, sharing a pencil, and the full arbitrary-subspace
endpoint factorization. In particular, the paired auxiliary bases at
each label are fixed independently of the query j. The initial phase
factors as the auxiliary phase times the distinguished phase; the latter
is constant on auxiliary cosets and remains in the middle maps. These
are explicit source properties, rather than assumptions inferred from
an unweighted rectangle identity.

A full normalized Fourier transform followed by the inverse transform
on the complementary frequency coordinates gives the desired partial
transform. The dual coordinate change is necessary. Choosing a basis
and its full dual makes this valid even when the restricted pairing on
H is degenerate. Each half may have a different coordinate matrix in
the paired physical bases, but both are included ordinary permutations.

The source proof only needs span(J) subset H subset span(I)^perp. With
H=span(I)^perp, the source inverse complement has dimension r_I-1
inside its D-1 auxiliary coordinates; the destination partial transform
has dimension r_I. Nonempty free sides imply 1<=r_I<=D-1. The full
source auxiliary transform, after its auxiliary phase, can therefore be
prepared once per label and reused over both rectangles and queries.
Query-dependent coset phases and distinguished-coordinate operations
remain in the middle. Their row mixing commutes with the final spatial
endpoint, so the existing sum-over-j sharing survives.

Counting two halves gives exactly the sufficient free bill
2(D-1)+2K. The extra arrays are a constant number of full copies plus
the existing per-incidence storage. All additional coordinate maps,
copies and scalar signs are polynomially described ordinary work. Full
and inverse partial transforms use the existing normalized child slots;
the even f convention makes their numerical normalizations rational.
Their unitary maps and polynomial event count fit the admitted numerical
supplier after retaining the charged norm/precision bounds. No new
free address mask or uncharged child-volume reduction is needed.

## Symmetric output and accumulation order

Section 7 uses A_v=F_v P_v and its actual adjoint
A_v^*=P_v^* F_v^*. The output phase therefore follows the global inverse
full transform. The factorization T_(v,H)P_v=S_(v,H)A_v and its adjoint
give the two legal per-rectangle options. The output-side choice has
source dimension r_J and complementary output dimension r_J-1.

Two destination channels are sufficient: one in fixed ordinary auxiliary
coordinates, one in fixed full-frequency coordinates. Apply each
rectangle's residual endpoint map before accumulating into its selected
channel, and perform the fixed output map only after the accumulation.
The final expression P_w^*[Y0+F_w^*Y1] is exact by linearity. In
particular, P_w is not commuted through F_w. The compiler may use the
smaller orientation separately for each rectangle, paying both global
preconditioners when both are used; EP13 correctly charges 4(D-1).
Dropping an unused global transform gives the stated one-channel bound.

## Literal invoice and remaining barrier

For a product side with all alphabet subsets proper, the only radical
relations of the additive-coordinate realization are coordinatewise
constant vectors. A relation supported in those proper subsets is zero.
Thus its affine differences have dimension sum(a_i-1). Their self-pairing
is zero, while the base label vector has self-pairing one, proving EP4.

Literal first-difference rectangles have equal source/destination sizes
and ranks. Counting a fixed vertex's bit-split choices gives
K=lambda+2(q-1-t)lambda'. The q=4,L=4 calculation is consequently
K=144 and a new 306-call invoice, compared with the exact balanced-side
old invoice 2D lambda=800. This is a finite call comparison, not a tape
runtime measurement. The symmetric option does not improve these
balanced rectangles.

The asymptotic invoice proof retains its charged-rank term. With L=2r,
b>=t, b>=2r-1, b>=t-1+(2r-2)log t for t>=2, and
b>=x-(r-1)t-r. These inequalities force the stated square-root-logarithmic
lower order by the same elementary three-range split as the preceding
heterogeneous proof. The t=1 case follows from the central binomial rank
and the exponential incidence count. Thus the saved local logarithmic
factor does not establish a better complete envelope.

## Isolated exact replay

Copied the frozen checker and its helpers into
`replay-fourier-preconditioning/` and reran it independently. It passed
153,896 partial-transform entries across 320 cases, including 73
degenerate restricted subspaces, and 8,408 side-rank checks. The added
Section 7 tests passed 4,368 phase/adjoint entries and 84 two-channel
aggregation entries. Adverse controls reject 45,961 omitted-dual-change
entries, 25,834 omitted-normalization entries, and 2,142 wrong-output-phase
orders. The saved receipt is exact rational arithmetic and source call
accounting, not a complete fixed-tape execution.
