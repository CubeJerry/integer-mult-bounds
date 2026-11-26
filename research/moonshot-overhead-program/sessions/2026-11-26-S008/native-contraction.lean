import S008.NumericalCutoff

namespace S008.NativeQuantitative

open S008.NumericalCutoff

private theorem phi_nonneg {x : ℝ} (hx : 0 ≤ x) : 0 ≤ phi x := by
  unfold phi logTwo
  apply Real.rpow_nonneg
  exact mul_nonneg (sq_nonneg _) (div_nonneg (Real.log_nonneg (by linarith))
    (Real.log_nonneg (by norm_num)))

/-- Common rounding parameter for both geometry charges. -/
theorem shared_rounding {ξ l Q : ℝ} (hlo : 31/64 ≤ ξ) (hhi : ξ ≤ 33/32)
    (hl : 17 ≤ l) (hQ : 4096 ≤ Q) :
    33/Q + 3/ξ + (1+3/l)*ξ^2 ≤ 13/2 := by
  have hp : 0 < ξ := by linarith
  have ha : 33/Q ≤ (33/4096:ℝ) :=
    div_le_div_of_nonneg_left (by norm_num) (by norm_num) hQ
  have hb : 3/l ≤ (3/17:ℝ) :=
    div_le_div_of_nonneg_left (by norm_num) (by norm_num) hl
  have hsq : ξ^2 ≤ (33/32:ℝ)^2 := by
    nlinarith [mul_nonneg (sub_nonneg.mpr hhi) (by linarith : 0 ≤ 33/32+ξ)]
  have hfactor : 0 ≤ 3-(20/17:ℝ)*(31/64)*ξ*(31/64+ξ) := by nlinarith
  have hprod := mul_nonneg (sub_nonneg.mpr hlo) hfactor
  have hdec : 3/ξ + (20/17:ℝ)*ξ^2 ≤ 3/(31/64:ℝ)+(20/17:ℝ)*(31/64)^2 := by
    apply (le_of_sub_nonneg ?_)
    apply (nonneg_of_mul_nonneg_left ?_ hp)
    field_simp
    nlinarith
  have hco := mul_nonneg (sub_nonneg.mpr hb) (sq_nonneg ξ)
  nlinarith


/-- The true arity only needs its one-sided upper relation for this bound. -/
theorem smaller_charge {s y : ℝ} (hs : 0 ≤ s) (hy : 0 ≤ y) (hsy : s ≤ y/240) :
    phi s ≤ (2/77:ℝ) * phi y := by
  have hle : s ≤ y := by linarith
  have hlog := logTwo_mono (show 0 < s+2 by linarith) (show s+2 ≤ y+2 by linarith)
  have hLy : 0 ≤ logTwo (y+2) := by
    unfold logTwo
    exact div_nonneg (Real.log_nonneg (by linarith)) (Real.log_nonneg (by norm_num))
  have hs2 : s^2 ≤ (y/240)^2 := by
    nlinarith [mul_nonneg (sub_nonneg.mpr hsy) (by linarith : 0 ≤ y/240+s)]
  have hcube : (phi s)^3 ≤ ((2/77:ℝ) * phi y)^3 := by
    rw [mul_pow, phi_cube hs, phi_cube hy]
    nlinarith [mul_nonneg (sub_nonneg.mpr hs2) hLy, mul_nonneg (sq_nonneg s) (sub_nonneg.mpr hlog),
      mul_nonneg (sq_nonneg y) hLy]
  exact le_of_pow_le_pow_left₀ (by norm_num : (3:ℕ) ≠ 0)
    (mul_nonneg (by norm_num) (phi_nonneg hy)) hcube

end S008.NativeQuantitative

