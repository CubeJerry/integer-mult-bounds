# The literal (3,2,2) target has no two-interstage ordinary realization

**Status: proved in the stated faithful group-span model; independent review
pending. No new κ.** This is a full ordinary-span obstruction for one fixed
source word and fixed literal endpoint gauge. It does not exclude arbitrary
ordinary encodings before and after the word.

## 1. Exact problem and model

Let `O` be the ordinary computational-monomial group span in the faithful
phase-aware Clifford representation used by the programme. Let `a` be the
actual three-head source of `SOURCE-222-BASE.md`, at an admissible tensor width.
The source is invertible, lies in the rank-one Gaussian component, and its
square lies in the rank-two component. In particular, the right cosets
`H`, `aH`, and `a⁻¹H` of the ordinary subgroup are distinct. Thus their spans
satisfy the direct sum assertion

\[
\mathcal O\oplus a\mathcal O\oplus a^{-1}\mathcal O.       \tag{1}
\]

This is a group-coset assertion in the faithful group algebra, with physical
central phases retained. It is not an assertion about arbitrary matrices in
the small-width representation: at a small width the ordinary span may have
additional representation-theoretic linear dependencies. The obstruction
holds at every width at which the programme's actual phase representation is
faithful, and therefore excludes a proposed all-width caller in this model.

Set

\[
K=\begin{pmatrix}I&0&a-I\\a&0&-a\\I&I&-I\end{pmatrix},
\qquad D=\operatorname{diag}(a^3,a^2,a^2).
\]

The source word `K=LT` uses one native and the explicit ordinary three-bank
matrix from `SOURCE-222-BASE.md`; `K³=diag(a²,a²,a²)` is already proved.
The proposed improvement inserts two arbitrary invertible ordinary stages
`P,Q ∈ GL₃(O)` and asks for

\[
KPKQK=D.                                                  \tag{2}
\]

No Gaussian rank-one query is added. Its optimistic complete Gaussian price
would be `3[1]+6[7]+3[8]`, against `[24]+2[23]`. The exact target invoice is
favorable at κ=1/200, as recorded in `BUDGET-RESULT.json`; equation (2) is the
missing construction, not a consequence of that arithmetic.

## 2. The exact linear-intersection reduction

Put `R=Q⁻¹`. Equation (2) is equivalent to

\[
P=BRK^{-1},\qquad B=K^{-1}DK^{-1}.                         \tag{3}
\]

Therefore it is equivalent to an invertible `R ∈ Mat₃(O)` in the linear
subspace defined by `BRK⁻¹ ∈ Mat₃(O)`. If such an R existed, P would be
invertible because B, R, and K are invertible. In a finite-dimensional unital
ordinary algebra, an ordinary matrix which is invertible in the represented
matrix algebra has ordinary inverse, by its characteristic polynomial.
That observation is only an existence statement: physical construction of
`Q=R⁻¹` would still require an explicit ordinary circuit, cost, and precision
analysis. No free physical inverse is asserted.

The Laurent identities, valid for every invertible element a of an
associative unital algebra, are

\[
K^{-1}=\begin{pmatrix}
a^{-1}&a^{-1}-a^{-2}&0\\
0&-a^{-1}&I\\
a^{-1}&-a^{-2}&0
\end{pmatrix},
\quad
B=\begin{pmatrix}
a&a-2I+a^{-1}&a-I\\
a&0&-a\\
a&a-I+a^{-1}&-I
\end{pmatrix}.                                            \tag{4}
\]

## 3. A zero ordinary-preimage lemma

**Lemma.** If `(r₁,r₂,r₃)ᵀ ∈ O³` and `B(r₁,r₂,r₃)ᵀ ∈ O³`, then
`r₁=r₂=r₃=0`.

**Proof.** The second row of the product is `a(r₁-r₃)`. By (1), an element
of `aO` which is ordinary is zero. Invertibility of a gives `r₁=r₃`.
The third row is

\[
a(r_1+r_2)+a^{-1}r_2-r_2-r_3.
\]

Its first two displayed summands belong to the distinct coset spans `aO`
and `a⁻¹O`. Since the entire row is ordinary, (1) gives `r₂=0` and then
`r₁=0`. Hence `r₃=0`. This uses no invertibility of any individual ordinary
coefficient and remains valid when O has zero divisors. ∎

## 4. The obstruction

**Theorem.** Equation (2) has no solution `P,Q ∈ GL₃(O)`.

**Proof.** Equation (3) implies `BR=PK`. The second column of K is
`(0,0,I)ᵀ`. Thus the second column of `PK` is the third column of P and is
ordinary. The lemma applied to the second column of R forces that column
to be zero. An invertible matrix cannot have a zero column. ∎

The theorem allows arbitrary, noncommuting, singular entries in the two
ordinary interstages and arbitrarily large finite ordinary support. The
finite catalogues in `linear_interstage.py` were a discovery tool only. The
written coset argument supplies the universal conclusion within this exact
literal-gauge scope.

## 5. Scope and next escape

The theorem does not establish that three native calls and three retained
roles can never produce independent Gaussian heads (3,2,2). A general caller
may include nontrivial ordinary endpoint encodings, different authenticated
native orientations, or different source head gauges. Those modifications
replace B in (3); the zero-preimage lemma need not persist.

The established base (2,2,2), the one-interstage obstruction, and this two-
interstage literal-gauge obstruction point to one specific next obligation:
find an authenticated change of boundary or source representation which
admits a full ordinary frame through the corresponding B, without paying
the additional rank-one query. Simply enlarging the ordinary catalogue in
equation (2) cannot work.

## 6. Exact diagnostics and negative controls

`check_linear_gate.py` independently expands the Laurent identities, checks
them on all columns at physical widths 1 and 2, and verifies the original
(2,2,2) base as a positive control. It also checks a nonordinary source with
ordinary square `a²=-I`: then `a⁻¹=-a`, the two coset spans in (1) coincide,
and `B(0,I,0)ᵀ=(-2I,0,-I)ᵀ` is a nonzero ordinary preimage. This demonstrates
why the actual source-square hypothesis belongs in the proof.

These finite checks validate identities and controls, not the large-width
faithfulness theorem or the complete multiplication assumptions.

**Credit.** @CubeJerry's persistent programme; GPT-6 Astra Pro assistance.
The linear-intersection reduction was independently proposed by the lead
orchestrator and Worker B in this session. Source provenance and all retained
foundational assumptions remain as in `DEPENDENCIES.json` and the programme.
