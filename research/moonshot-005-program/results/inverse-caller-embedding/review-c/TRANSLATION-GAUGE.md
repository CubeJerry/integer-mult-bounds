# An ordinary translation gauge makes each hybrid's two shear coefficients equal

**Additional source-bound lemma derived during independent review.** This is positive interface progress, not an independent review of this new lemma itself and not a complete caller. The frozen Worker B proof is unchanged. Root's independent review is requested before admission.

Use the actual M_s=X_tau P_s and O_s=X_sigma P_s, where P_s²=I on each port. Define a new symbol L_s=O_sM_s, distinct from the sign map J in the author proof. Then

\[
L_{s,h}=X_{\sigma_{s,h}+P_{s,h}\tau_{s,h}}.
\]

It is exactly a coordinate translation, including its actual displacement. It commutes with Q, D_s and every other coordinate translation or diagonal Fourier Gaussian on the same field. Port matrices need not commute with L_s.

The author interfaces are

\[
A_s^+=M_s^{-1}QR M_s,
\qquad A_s^-=O_sRQO_s^{-1}.
\]

Since Q commutes with M_s and O_s and Q⁴=I,

\[
\boxed{A_s^-=L_s(A_s^+)^{-1}Q^2L_s^{-1}.} \tag{1}
\]

Indeed the right side reduces to O_s R Q^-1 M_s Q²M_s^-1O_s^-1=O_s RQ O_s^-1. This proof does not commute Q through R.

## Preferred hybrid

The preferred actual hybrid has cross coefficients Y+=(A_s^-)^-1X and U−=A_s^+V, with the common D_s outside all roles. On its X/Y plane choose output gauges

\[
H_X=L_s^{-1},\qquad H_Y=Q^2L_s^{-1}.
\]

Preapply H_X^-1,H_Y^-1 to the corresponding entering roles, and postapply H_X,H_Y. Both gauges are translations and commute with D_s, so every arbitrary baseline and its body passage are restored. Its new forward coefficient is

\[
H_Y(A_s^-)^{-1}H_X^{-1}
=Q^2L_s^{-1}(A_s^-)^{-1}L_s=A_s^+.
\]

The U/V plane is unchanged. Thus the complete adjusted source is

\[
(X,Y,U,V)\longmapsto
D_s\bigl(X,\ Y+A_s^+X,\ U-A_s^+V,\ V\bigr). \tag{2}
\]

Both shear coefficients are the same A_s^+. This does not say A_s^+ is an involution, commutes with its own D_s, or equals the coefficient at another stage.

## Complementary hybrid

For the complementary source choose X/Y output gauges H_X=L_sQ² and H_Y=L_s, again with their inverses on input. Its original forward coefficient(A_s^+)^-1 becomes

\[
H_Y(A_s^+)^{-1}H_X^{-1}
=L_s(A_s^+)^{-1}Q^2L_s^{-1}=A_s^-.
\]

The reverse coefficient is already A_s^-. It therefore yields the analogue of(2) with A_s^- in both places.

Each version adds four ordinary monomial applications per port,448 over112 ports: pre/post on two banks. Q² and L_s can be composed into one literal translation per occurrence. There are no additional Gaussian calls, queries, fields, erasures or productive credits. Ordinary tape and precision work remains charged.

The independent checker verifies the exact translation character of L_s for all224 port-stage records, commutation with D_s, equation(1) and the preferred gauge for all896 nonzero source blocks. The complementary gauge is equation(1) itself. These are canonical degree-two Z4 polynomial comparisons including the actual route translations, with the scalar port coefficient retained once. The algebraic proof gives the all-stage/all-width conclusion.

Worker C derived the L_s relation while reviewing the inverse placement; Worker B identified the useful equal-coefficient hybrid gauges and communicated them to Worker A. This note records both contributions under @CubeJerry's programme, with OpenAI assistance. **No new κ.**
