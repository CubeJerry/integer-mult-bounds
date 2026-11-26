import S008.WholeProfile

namespace S008.AllLengths
open S008.NumericalCutoff S008.WholeProfile

private theorem phipos {x : ℝ} (hx : 0 ≤ x) : 0 ≤ phi x := by
  unfold phi logTwo
  apply Real.rpow_nonneg
  exact mul_nonneg (sq_nonneg _) (div_nonneg (Real.log_nonneg (by linarith))
    (Real.log_nonneg (by norm_num)))

private theorem log_lower {x : ℝ} (j : ℕ) (hx : (2:ℝ)^j ≤ x+2) :
    (j:ℝ) ≤ logTwo (x+2) := by
  have h := logTwo_mono (pow_pos (show (0:ℝ)<2 by norm_num) j) hx
  have he := logTwo_two_rpow (j:ℝ)
  rw [Real.rpow_natCast] at he
  rwa [he] at h

private theorem bounded_below (x a m : ℝ) (j : ℕ) (hx : a ≤ x) (ha : 0 ≤ a)
    (hlog : (2:ℝ)^j ≤ x+2) (hnum : m^3 ≤ a^2 * j) : m ≤ phi x := by
  have hy : 0 ≤ x := le_trans ha hx
  have hl := log_lower j hlog
  have hs : a^2 ≤ x^2 := by
    nlinarith [mul_nonneg (sub_nonneg.mpr hx) (by linarith : 0 ≤ x+a)]
  have hj : (0:ℝ) ≤ (j:ℝ) := by positivity
  apply le_of_pow_le_pow_left₀ (by norm_num : (3:ℕ) ≠ 0) (phipos hy)
  rw [phi_cube hy]
  exact hnum.trans (mul_le_mul hs hl hj (sq_nonneg x))

theorem dyadic_middle {x : ℝ} (hx : 5 ≤ x) (hmax : x ≤ 4097) :
    170+5*x ≤ 71*phi x := by
  by_cases h8 : x ≤ 8
  · have h := bounded_below x 5 3 2 hx (by norm_num) (by linarith) (by norm_num)
    linarith
  by_cases h32 : x ≤ 32
  · have h := bounded_below x 8 5 3 (by linarith) (by norm_num) (by linarith) (by norm_num)
    linarith
  by_cases h64 : x ≤ 64
  · have h := bounded_below x 32 8 5 (by linarith) (by norm_num) (by linarith) (by norm_num)
    linarith
  have hden : x ≤ 512*logTwo (x+2) := by
    by_cases h2 : x ≤ 2048
    · have h := log_lower 6 (by norm_num; linarith : (2:ℝ)^6 ≤ x+2)
      norm_num at h
      linarith only [h,h2]
    · have h := log_lower 11 (by norm_num; linarith : (2:ℝ)^11 ≤ x+2)
      norm_num at h
      linarith only [h,hmax]
  have hs : x/8 ≤ phi x := by
    have hxx : 0 ≤ x := by linarith
    apply le_of_pow_le_pow_left₀ (by norm_num : (3:ℕ) ≠ 0) (phipos hxx)
    rw [phi_cube hxx]
    nlinarith only [mul_le_mul_of_nonneg_left hden (sq_nonneg x)]
  linarith


theorem small_excess {x : ℝ} (hx : 1 ≤ x) : (60:ℝ) ≤ 71*phi x := by
  have h := bounded_below x 1 1 1 hx (by norm_num) (by linarith) (by norm_num)
  linarith

theorem coprime_excess {x : ℝ} (hx : 4096 ≤ x) :
    182+4*logTwo (x+2)+70*phi (x+2)+1 ≤ 71*phi x := by
  have hp : 0 ≤ x := by linarith
  have hs := shifted_phi (show 2≤x by linarith)
  have hlarge := bounded_below x 4096 512 8 hx (by norm_num) (by linarith) (by norm_num)
  have hlog := log_lower 8 (by norm_num; linarith : (2:ℝ)^8 ≤ x+2)
  have hh : 64*logTwo (x+2) ≤ x :=
    log_control 64 4096 13 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
      (by norm_num) hx
  have hbound : 16*logTwo (x+2) ≤ phi x := by
    apply le_of_pow_le_pow_left₀ (by norm_num : (3:ℕ) ≠ 0) (phipos hp)
    rw [mul_pow, phi_cube hp]
    have hsquare : (64*logTwo (x+2))^2 ≤ x^2 := by
      nlinarith [mul_nonneg (sub_nonneg.mpr hh) (by linarith : 0 ≤ x+64*logTwo (x+2))]
    nlinarith only [mul_nonneg (sub_nonneg.mpr hsquare) (show 0≤logTwo (x+2) by linarith)]
  linarith

end S008.AllLengths
