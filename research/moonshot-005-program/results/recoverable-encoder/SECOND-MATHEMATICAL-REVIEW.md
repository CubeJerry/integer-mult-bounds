# Independent mathematical review of the generalized recoverable encoder

**Accept the stated matrix criterion as a sufficient and necessary condition
within its explicitly supplied linear control/observation interface. No
source feasibility is established by this note.** Prepared by the S004
adversarial worker for the orchestrator's proposed extension.

Let u be the arbitrary common input, q an independent donor field, and F the
matrix of the receiver's chosen original native historical observations. At
a fixed encoder cut τ, E contains the actual common rows physically cochart
with the donor. Let W_T contain the reference public endpoint rows physically
at the donor's terminal chart T. Define the recoverable row space

\[
R=\operatorname{row}(E)\cap\operatorname{row}(W_T).
\]

The fixed control set consists of actual scalar injections of one retained
signal δ into common fields at specified cuts and charts. Its response
matrices are A for all off-terminal endpoint and COPY constraints, and B
for the listed receiver histories. These matrices must represent physically
admitted control events after the encoder, not a geometry or timing oracle.

Choose r∈R and physically encode δ=q−ru by adding an E-expansion of −r into
the donor. For a control coefficient vector c the actual history is

\[
Fu+Bc(q-ru).
\]

For a decoder row d to recover q for every u,q, coefficient comparison is
exactly

\[
Ac=0,\qquad dBc=1,\qquad dF=r\in R.
\]

Let K have columns spanning ker A. Let L have columns spanning the right
annihilator of R. Then `dF∈R` is equivalent to `dFL=0`. If Z has rows
spanning the left nullspace of FL, every admissible decoder is a row
combination of Z. Therefore a feasible encoder/control/decoder exists if
and only if

\[
ZBK\ne0.
\]

If an entry `Z_i B K_j=g` is nonzero, take d=Z_i, c=K_j/g and r=dF.
Conversely every feasible pair gives a nonzero product through those bases.
Thus this is a finite linear rank test, not a bilinear search heuristic.
Equivalent exact rank excess is

\[
\operatorname{rank}\begin{pmatrix}A&0\\ B&FL\end{pmatrix}
-\operatorname{rank}(A)-\operatorname{rank}(FL)
=\operatorname{rank}(ZBK).
\]

To see the identity, first eliminate the independent A columns, leaving BK
modulo the FL column space in the lower block. The quotient dimension is
`rank([FL,BK])−rank(FL)`. Multiplication by Z identifies that quotient and
has kernel exactly `col(FL)`, yielding the stated expression.

For a positive certificate, obtain r=eE=λW_T by exact row-space decoding.
The physical steps are Q−=eE, the certified injections cδ, and the genuine
history decoder d. Since Ac=0, all public perturbations end at T. While Q
still equals δ, subtract the full terminal perturbation from the common
outputs. They then equal Wu. Finally add λ times those restored terminal
outputs to Q; this returns Q to q. The receiver's cached decoded sum is q.
No γ inversion beyond the explicit nonzero normalization g is required, and
no helper has to equal q immediately after a particular source MOVE.

## Physical scope that must accompany the matrix test

1. E is evaluated at the actual encoder cut, before the common interventions
   represented by B. For a single module this is the original native row
   space at that cut. Earlier channels would require their real causal
   perturbation terms and a separate composition proof.
2. After encoding at chart A, δ can be left in stationary owned snapshots
   along the donor's **remaining** unused route from A to T. Earlier donor
   charts cannot receive δ for free. This restriction is stricter than the
   additive-q setup, where q snapshots may be seeded along the whole route
   before the native begins. Columns of A and B must be restricted
   accordingly unless another physical transport is explicitly provided.
3. Controls cannot precede the encoder. Source instruction order, live field
   charts, ownership and COPY zero guards must be retained. Histories before
   the encoder may be used only through actual retained observations.
4. The receiver decoder must be lowered to direct chronological reads or
   real stationary chart accumulators. Its source values cannot be reread
   after disappearance. Collecting accumulators after the common source
   finishes permits the receiver to follow its own funded route once.
5. Scalar coefficients e,c,d,λ, the division by g, precision, initialization,
   all scalar work, storage, erasure and retirement remain charged under the
   existing model. The matrix test alone is not a target-price certificate.
6. The donor is restored using the corrected common endpoints. Reading λ
   from the perturbed endpoints would introduce another response term.

The encoder may be any recoverable cochart linear form, which is broader
than using the value of one preselected helper. With R={0} the criterion
reduces to purely additive modulation and the native zero-common-history
relations. The nonzero-R cases are not ruled out by a failed R={0} test.
Likewise a failed fixed-helper test excludes only that chosen r, not the full
recoverable space R.

All arguments are exact over the declared characteristic-zero coefficient
field and extend coordinatewise to every admitted complete-field volume.
The criterion does not establish a positive certificate in the frozen
native, a compatible collection of channels, a complete second-native map,
or any new κ. The single most relevant next computation is a source-bound
test with correctly restricted post-encoder control columns and explicit
E/W_T/F source rows.

Credit: S004 orchestrator for the generalized encoder criterion and shared
research direction; adversarial worker for this independent derivation and
the remaining-route scope check. OpenAI assistance disclosed.
