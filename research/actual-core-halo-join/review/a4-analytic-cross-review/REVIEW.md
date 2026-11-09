# Independent review of the normalized Core/halo seam

Prepared for @CubeJerry with substantial OpenAI assistance. This is an
independent mathematical cross-review of C3, not a new research claim.
Worker A owns this analytic review; worker B owns signed-word and
original-matrix execution checks, and the root review owns materialization
and cost accounting.

**Disposition: conditional analytic PASS.** The stated domain implies all
three bounds in C3 `PROOF.md` Section 6. I found no missing dimension,
normalizer, complex-component, or tensor factor. The written derivation below
is universal on that domain. **This review does not accept a complete physical
execution:** that requires its separate completed receipt, cleanup checks and
the other reviews. No physical program was run for this review.

The reviewed package is `worker-c3/research/actual-core-halo-join` in the
shared workspace. `SOURCE-HASHES.json` gives complete SHA256, Git blob, byte
length and retained dependency origin for every inspected source. The four
primary hashes at the start of review were:

| File | SHA256 |
| --- | --- |
| PROOF.md | `1f7950bb5149beceb4647aa357d95b86da6fdbafb6bce6529cceb34c9d4ce2a9` |
| attachment.py | `8f040a3da9b1ed0f723231e11fe6ebb466f5a3560a2984bc55f23f0ef273d2cf` |
| format_bridge.py | `037dd2265e637f92c6f51320409fb348b148ce9a5e873a353aba053a5c94d1d3` |
| source_geometry.py | `bbee918cd3492ca016d3edc668e884af6e22784a521f1102acad28e3cd2bc622` |

The final hash guard detected a documentation revision during review. I read
the revised proof in full: it makes the field norm explicit and expands the
real-coefficient and intermediate-radius explanation. The reviewed final
PROOF.md SHA256 is
`37e7f9995725543917ec593184842c0453e6954d633af4e2573ad835a292b3ac`.
The other three primary files and all inspected retained sources were
unchanged. The manifest records the old and new proof hashes rather than
asserting false start/end identity.

## 1. Exact target and hypotheses

The original coordinate space has T records, including every coarse context
and spectator. Write

\[
 |z|_1=|\Re z|+|\Im z|,\qquad \|x\|_*=\max_r |x_r|_1.
\]

Each H_i=I-E_i is **real**, so absolute row sums bound this induced norm.
Retain one immutable reference per axis, with

\[
 \|E_i\|_\infty\le\rho_i=1-\delta_i<1,\quad 0<\delta_i\le1,
 \quad a_i=2^{u_i},\quad u_i\in\mathbb Z_{\ge0},\quad a_i\delta_i\ge1.
\]

Let S_i be the direct sum of H_i[C,C]^-1 over the ordinary complete cores C.
Including the identity on spectators, put

\[
 S=I_{\rm spec}\otimes\bigotimes_i S_i,\quad
 A=\prod_i a_i=2^U,\quad U=\sum_i u_i,\quad
 \overline S=S/A,\quad
 B=I_{\rm spec}\otimes\bigotimes_i(H_i^{-1}/a_i).
\]

The actual complete Core has the retained all-input guarantee
`||S_hat(x)-Sx||_2 <= epsilon` at the actual original-grid x, with all global
source, radius, precision, signed-width and current-state premises funded.
This is the whole-field guarantee from retained `core/NUMERICS.md` Sections
1--5, not a guarantee reset at each context. Its allocation actually gives
2^(-target)/2; C3's epsilon=2^(-target) is conservative.

The entry has grid 2^(-q) and norm at most R_in. All halo plans share q and
integer R_halo>=R_in. Valid original geometry, exact saved pre-mutation input,
same-reference sections/pages and unique return ownership are inherited
hypotheses. A claimed hash, width or radius declaration alone does not prove
these hypotheses.

## 2. Original layout and tensor compatibility

`layout_for` reverses the halo's most-significant-first active axis widths
into Layout's low-bit axis numbering and puts spectators above them. Its
selected local bits move by a complete bit permutation. `original_base(c)`
applies the inverse permutation to the packed coarse label; `core_starts(c)`
therefore gives actual original starts, without treating c as an unpermuted
Cartesian tuple.

For halo axis i, `source_family` uses Reference_i at
`core_starts(c)[g-1-i]`. The retained dense preparer reverses each family row
once, and `PreparedRoutes` checks these starts, sizes and periods. The exact
endpoint on each context is the tensor of the corresponding ordinary Q
section inverses. A context-dependent interior decomposition does not change
that same-Reference Q endpoint. Record permutations preserve both norms here.

Every principal E section retains the same row bound. Its inverse norm is at
most 1/delta_i. Hence

\[
 \|S_i/a_i\|_\infty\le1,\quad
 \|H_i^{-1}/a_i\|_\infty\le1,\quad
 \|\overline S\|_{*\to *}\le1,\quad\|B\|_{*\to *}\le1.
\]

Only exact maps are asserted to be contractions. Direct sums and spectator
identity factors introduce no numerical factor. Physical route realization
and its full cost remain separate.

## 3. Lift, summed normalization, truncation and radius

Put h_q=2^(-q), distinct from the source word-width variable h. An input
component n/2^q is lifted to X=n*2^(P-q) at grid 2^(-P). P>=q makes this an
integer shift. The sufficient carrier condition w>=h+P-q, where
h=q+bit_length(R_halo)+1, supplies a genuine sign bit. The Core's separately
funded internal widths remain required.

After the complete Core, the return rule is

\[
 d=P+U-q,\qquad
 Y=\operatorname{sign}(X)\lfloor |X|/2^d\rfloor.
\]

At grid 2^(-q), this is componentwise truncation toward zero of the actual
Core return divided by A. The full product A is applied once. The halo's
per-axis divisions have the same product. It is unnecessary to require
q>=U; q>=u_i for every i is the separate halo recurrence condition.
P>=q and U>=0 imply d>=0. For d>=w, zero remains the correct truncation.

For every complex field v,

\[
 \|\operatorname{trunc}_q(v)-v\|_*\le2h_q,\qquad
 \|\operatorname{trunc}_q(v)\|_*\le\|v\|_*.
\]

For each coordinate r, |e_r|_1<=sqrt(2)|e_r|<=2||e||_2. Thus the actual
normalized, truncated Core return c obeys

\[
 \boxed{\|c-\overline Sx\|_*\le2\epsilon/A+2h_q=E_{\rm seam}.}
\]

No extra sqrt(T) is needed: epsilon already bounds the complete field's
Euclidean defect. Conversely the *input* Euclidean admission must use
R_0^2>=T R_in^2, since |x_r|<=|x_r|_1<=R_in. `admit_radii` uses 2^n records,
including every context and spectator.

Before truncation the actual output radius is at most R_in+2epsilon/A;
truncation cannot increase it. Therefore R_halo>=R_in+2epsilon/A is enough
for every output, including those later discarded. The displayed pair
R_halo>=2R_in and 2epsilon/A<=R_in implies this condition. The integer radius
and h above fit endpoint values strictly inside the sign-magnitude range.
The actual input radius is a valid-input premise; the bridge alone does not
establish R_in for arbitrary encoded input.

## 4. Kept-output inequality

Put tau_i=rho_i^(J_i)/delta_i. The inherited #6880 comparison gives

\[
 \|\operatorname{row}_r(S_i/a_i-H_i^{-1}/a_i)\|_1
 \le2\tau_i/a_i
\]

when the output is farther than (J_i-1)W_i from its core complement. C3
supplies this through (J_i-1)W_i<=b<B_face and a kept coordinate in
[B_face,L-B_face). Its sections are ordinary sections of the same original
reference. Period, bandwidth and outside-window hypotheses are retained.
This review consumes the cited locality/tail theorem.

Telescope a kept tensor row between its normalized section row factors and
global row factors. Every other factor has l1 norm at most one, and row
tensor-product norms multiply. The full row difference is consequently at
most 2 sum_i tau_i/a_i. Apply it to the same original x and add the actual
Core seam error:

\[
 \boxed{E_{\rm keep}\le2\epsilon/A+2h_q
                 +2R_{\rm in}\sum_i\tau_i/a_i.}
\]

This uses neither internal locality of the rounded Core nor zero error on
its discarded coordinates. All errors in actual dense and sparse stages
are already within the complete Core's epsilon contract.

## 5. Producer precision and actual halo radius

The coefficient constant was checked against executed producer expressions,
not only inherited from its proof. In retained `shrinking-reference-halo`:

- `source.py:source_entry` returns the real rational
  `I-Reference.entry('narrow',row,column).value`.
- `engine.py:prepare_table` converts that value to `Fraction`, then calls
  `inward(value, plan.bits)`, producing **one** integer C at scale 2^q.
- It checks both |C/2^q-E_rc|<2^(-q) and |C/2^q|<=|E_rc|, and checks each
  exact stored row mass against 1-delta_i. The off-band zero hypothesis is
  supplied separately by the Reference support theorem or complete support
  admission; row checks alone do not prove it.
- `coefficient_width=q+2` is a signed carrier width, not q+1 fractional
  precision. There is no hidden extra fractional bit in this argument.

Consequently the real coefficient error multiplies a complex z with norm
|delta C|(|Re z|+|Im z|). It costs h_q times the declared component-l1 radius,
not 2h_q times that radius. A source with independently rounded complex
coefficients would need a different coefficient bound; that source is outside
the stated real-Reference domain. With s_i=2W_i+1,

\[
 \|\widehat E_i-E_i\|_\infty<s_i h_q,\qquad
 \|\widehat E_i\|_\infty\le\rho_i.
\]

For the actual incoming line v at radius at most R_halo, the retained engine
implements

\[
 z_0=0,\qquad
 z_{k+1}=\operatorname{trunc}_q(v/a_i+\widehat E_i z_k).
\]

In integer arithmetic it first forms
`V*2^(q-u_i)+sum C*Z` on the 2q product grid. The Plan constructor enforces
q>=u_i>=0. Thus the source summand is exact on that grid and there is **one**
final truncation for each real/imaginary completed sum, not a separate rounded
source term followed by another rounding. Their combined defect is <=2h_q.

If ||z_k||_*<=R_halo, then the unrounded next state has norm at most

\[
 R_{\rm halo}/a_i+\rho_i R_{\rm halo}
 \le\delta_i R_{\rm halo}+(1-\delta_i)R_{\rm halo}
 =R_{\rm halo}.
\]

Toward-zero truncation preserves this bound. The initial state is zero, so
every *computed* iterate and every actual later-axis input has this radius.
The same absolute-mass estimate bounds partial accumulators, though their
physical signed-width admission is part of the retained engine contract.

## 6. Halo error and tensor composition

For the same actual v, set
`y_k=(1/a_i) sum_(j=0)^(k-1) E_i^j v`. Comparing its recurrence with the
computed one at the actual z_k gives

\[
 e_{k+1}\le\rho_i e_k+(s_i R_{\rm halo}+2)h_q,\qquad e_0=0.
\]

Summing the finite geometric series and relaxing it by 1/delta_i proves

\[
 \|z_{J_i}-(P_i/a_i)v\|_*\le
 \eta_i:=\frac{(s_iR_{\rm halo}+2)h_q}{\delta_i},\qquad
 P_i=\sum_{j=0}^{J_i-1}E_i^j.
\]

This verifies the questioned coefficient and two-component constants.
The inherited shrinking-domain theorem identifies each returned local
rectangle with the corresponding restriction of this complete-period rounded
recurrence. Saved lengths are nonaliasing: L+2b<2L<=N_i. Shrinking earlier
axes to their targets retains all later-axis dependency coordinates, as that
theorem requires. No independently translated Reference is introduced.

For the exact normalized polynomial maps F_i=P_i/a_i, ||F_i||<=1. Write the
residual of each computed axis at its **actual** input as
`r_i=vhat_i-F_i(vhat_(i-1))`. The preceding bound gives ||r_i||_*<=eta_i,
because the actual radius induction has already been proved. Expanding

\[
 \widehat v_g-F_g\cdots F_1x
 =\sum_i F_g\cdots F_{i+1}r_i
\]

therefore costs at most sum_i eta_i. This exact-suffix expansion does not
assume additivity or nonexpansiveness of any rounded routine.

The inherited tail bound is ||F_i-H_i^-1/a_i||<=tau_i/a_i. Telescoping its
tensor product against normalized inverse contractions costs at most
R_halo sum_i tau_i/a_i. (R_in would also bound the original x, but the
advertised R_halo is conservative.) Thus

\[
 \boxed{E_{\rm halo}\le\sum_i\eta_i
                    +R_{\rm halo}\sum_i\tau_i/a_i.}
\]

Here the retained halo proof uses its symbol tau_i for the *normalized*
quantity rho_i^(J_i)/(a_i delta_i); C3 defines an unnormalized tau_i and
divides by a_i explicitly. These conventions agree exactly.

## 7. Disjoint return and essential compatibility conditions

`AttachedCore.run` gathers and sorts the original halo values before any Core
mutation. The complete Core and normalized return then overwrite the current
dense field. The unchanged halo codec consumes saved original values. The
unchanged merge preserves current Core outputs exactly at kept coordinates
and replaces every other coordinate exactly once. Consuming those inherited
chronology/ownership guarantees, the returned field y obeys

\[
 \boxed{\|y-Bx\|_*\le\max(E_{\rm keep},E_{\rm halo}).}
\]

The maximum is legitimate because the output sets are disjoint. Sparse input
copies may overlap; that affects storage, not this numerical inequality. There
is no extra number-of-faces, number-of-contexts or dimension factor.

The precise compatibility gates used above are already stated in C3 or its
retained Plan/provider contracts:

| Gate | Reason and observed source boundary |
| --- | --- |
| One real immutable Reference per original axis | `source_family` checks IDs, period, gap and conservative physical support; original Q and halo E use its actual entries. Smaller bands require complete independent admission. |
| All actual axes and spectators | Layout/route family dimensions cover K contexts; global radius uses T; every sum and U uses the actual group. |
| Ordinary sections and kept margin | N_i-L>=W_i and (J_i-1)W_i<=b<B_face; inherited locality/tail statement applies to these sections. |
| One common halo grid/radius | Plan enforces q>=u_i and funded normalization; `bridge_values` checks common q/width; `admit_radii` checks every plan radius. These are combined contracts, not interchangeable checks. |
| Correct Core admissions at P,w | P>=q, full incoming radius and all original provider accuracy/range seals remain required after preparing the shared carrier. |
| Full product normalizer | `bridge_values` uses sum of every plan shift, and return drops P+U-q bits. No per-axis normalizer is silently omitted. |
| Actual normalized output fits | R_halo>=R_in+2epsilon/A suffices before truncation; truncation is toward zero. |
| Same original saved input | Gather precedes Core; halo never reads the mutated Core field. |

Several tempting weaker contracts would fail. Replacing U by max_i u_i
changes the exact target scale whenever several shifts are positive. Requiring
q>=U is unnecessary: for example q=3, u_1=u_2=2, P=5 gives legal source shifts
q-u_i=1 and final drop d=6. Replacing the two-component truncation term by h_q
fails for v=(h_q-t)+i(h_q-t), 0<t<h_q/2. Dropping T from the input Euclidean
radius fails on a constant real field of value R_in. C3 makes none of those
substitutions.

## 8. Review boundary and reproducibility

This review consumes #6880's exact kept-row comparison, the shrinking halo's
locality and source support statements, and the complete Core's numerical
contract. It does not reprove them or promote finite evidence into their
universal acceptance. It checks their explicit compatibility at this seam.
The real-coefficient producer and recurrence constants were inspected
directly. The earlier complete Core numerical review is reused transparently;
the present attachment derivation is separate from its author implementation.

No missing analytic hypothesis was found within the stated valid domain.
Actual-source precision, original-layout delivery, encoded control integrity,
signed execution, resource accounting, cleanup, and the five selected
framework assumptions remain the explicit contracts identified in C3. Incoming
error and undoing normalizers belong to the outer error ledger; multiplying
by A can multiply an error by A. No complete Gaussian/FFT/CRT or integer
recovery conclusion follows from this review.

The accompanying hash-only verifier imports no C3 module and executes no
physical or numerical payload. Run it against the reviewed directory with
`python verify_hashes.py --package /absolute/path/to/actual-core-halo-join`
and the same command under `python -O`. Its paired receipts establish source
identity for this review, not physical execution. A completed physical receipt
is still required before any complete-transaction acceptance.
