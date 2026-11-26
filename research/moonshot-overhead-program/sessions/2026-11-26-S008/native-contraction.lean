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



theorem shrunk_width {z y : ℝ} (hz : 0 ≤ z) (hy : 0 ≤ y)
    (hzy : z ≤ (957/961:ℝ)*y) : phi z ≤ (2875/2883:ℝ)*phi y := by
  have hle : z ≤ y := by linarith
  have hlog := logTwo_mono (show 0 < z+2 by linarith) (show z+2 ≤ y+2 by linarith)
  have hLy : 0 ≤ logTwo (y+2) := by
    unfold logTwo
    exact div_nonneg (Real.log_nonneg (by linarith)) (Real.log_nonneg (by norm_num))
  have hz2 : z^2 ≤ ((957/961:ℝ)*y)^2 := by
    nlinarith [mul_nonneg (sub_nonneg.mpr hzy) (by linarith : 0 ≤ (957/961:ℝ)*y+z)]
  have hcube : (phi z)^3 ≤ ((2875/2883:ℝ)*phi y)^3 := by
    rw [mul_pow, phi_cube hz, phi_cube hy]
    nlinarith [mul_nonneg (sub_nonneg.mpr hz2) hLy, mul_nonneg (sq_nonneg z) (sub_nonneg.mpr hlog),
      mul_nonneg (sq_nonneg y) hLy]
  exact le_of_pow_le_pow_left₀ (by norm_num : (3:ℕ) ≠ 0)
    (mul_nonneg (by norm_num) (phi_nonneg hy)) hcube


/-- The actual rounded arity yields at least two bits of surplus for children. -/
theorem native_quarter_log {y s z : ℝ} (hy : 240*(2^17+2) ≤ y)
    (hlo : y/240-1 ≤ s) (hhi : s ≤ y/240) (hz : 0 ≤ z) (hzy : z ≤ y-s) :
    (13/2:ℝ)*phi s + 61*phi z + 2 ≤ 61*phi y := by
  have A : (0:ℝ) ≤ y := by linarith
  have B : (0:ℝ) ≤ s := by linarith
  have Hs := smaller_charge B A hhi
  have Hz := shrunk_width hz A (by linarith : z ≤ (957/961:ℝ)*y)
  have hlog := logTwo_mono (show (0:ℝ)<2 by norm_num) (show 2 ≤ y+2 by linarith)
  have htwo : logTwo 2 = 1 := div_self (ne_of_gt (Real.log_pos (by norm_num)))
  rw [htwo] at hlog
  have hphi : (5000:ℝ) ≤ phi y := by
    apply le_of_pow_le_pow_left₀ (by norm_num : (3:ℕ) ≠ 0) (phi_nonneg A)
    rw [phi_cube A]
    nlinarith [mul_nonneg (sq_nonneg y) (sub_nonneg.mpr hlog),
      mul_nonneg (by linarith : 0 ≤ y-1000000) (by linarith : 0 ≤ y+1000000)]
  linarith



/-- The executed child volume times its common per-bit price is at most a quarter. -/
theorem native_weight_quarter (V U E F M y z s : ℝ) (hV : 0 ≤ V)
    (hM : 0 ≤ M) (hMF : M*F ≤ E)
    (hy : 240*(2^17+2) ≤ y) (hlo : y/240-1 ≤ s) (hhi : s ≤ y/240)
    (hz : 0 ≤ z) (hzy : z ≤ y-s)
    (hmass : U ≤ V * Real.sqrt M * (2:ℝ)^((13/2:ℝ)*phi s)) :
    U * Real.sqrt F * (2:ℝ)^(61*phi z) ≤
      V * Real.sqrt E * (2:ℝ)^(61*phi y) / 4 := by
  have he := native_quarter_log hy hlo hhi hz hzy
  have hp := Real.rpow_le_rpow_of_exponent_le (show (1:ℝ) ≤ 2 by norm_num) he
  rw [Real.rpow_add (by norm_num), Real.rpow_add (by norm_num)] at hp
  norm_num at hp
  have hs : Real.sqrt M * Real.sqrt F ≤ Real.sqrt E := by
    rw [← Real.sqrt_mul hM]
    exact Real.sqrt_le_sqrt hMF
  have hpos (a : ℝ) : 0 ≤ (2:ℝ)^a := Real.rpow_nonneg (by norm_num) _
  have ha := mul_le_mul_of_nonneg_right hmass
    (mul_nonneg (Real.sqrt_nonneg F) (hpos (61*phi z)))
  have hb := mul_le_mul_of_nonneg_left hp (mul_nonneg hV
    (mul_nonneg (Real.sqrt_nonneg M) (Real.sqrt_nonneg F)))
  have hc := mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_left hs hV) (hpos (61*phi y))
  calc
    U * Real.sqrt F * (2:ℝ)^(61*phi z) ≤
      (V*Real.sqrt M*(2:ℝ)^((13/2:ℝ)*phi s)) * (Real.sqrt F*(2:ℝ)^(61*phi z)) := by
        simpa only [mul_assoc] using ha
    _ ≤ V * Real.sqrt E * (2:ℝ)^(61*phi y) / 4 := by
      nlinarith only [hb,hc]

end S008.NativeQuantitative

