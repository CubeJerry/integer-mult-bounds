import S008.ProfileLimit

namespace S008.Effective53
open S008.NumericalCutoff S008.WholeProfile

/-- Ten contractions at the certified band allowances already put the height below 7.235. -/
theorem contraction_gate {b r u:ℝ} (hr:0≤r) (hmax:r≤1/4) (hu:u≤(167/500)*(21/10)) :
    6+r*(b-3+u) ≤ max 6 (36169/5000+(b-36169/5000)/4) := by
  by_cases h : 0≤b-3+u
  · refine le_trans ?_ (le_max_right _ _)
    have := mul_le_mul_of_nonneg_right hmax h
    linarith only [this,hu]
  · refine le_trans ?_ (le_max_left _ _)
    have := mul_nonpos_of_nonneg_of_nonpos hr (le_of_not_ge h)
    linarith only [this]

theorem numerical_gates :
  (36169/5000:ℚ) + 20/4^10 < 1447/200 ∧
  4*(1447/200:ℚ)-((1447/200)+3*(8001/1000-1)+(167/500)*(21/10))=3/5000 ∧
  (240:ℚ)*(1447/200)^3 < (4497/100)^3 ∧
  (4497/100:ℚ)+8*(1001/1000) = 26489/500 ∧
  960*(34548+2) < (2:ℕ)^25 := by norm_num

/-- The initial logarithmic majorant persists across every future degree band. -/
theorem label_density {j:ℝ} (hj:11500≤j) : 500*(logTwo (j+2)+9) ≤ j := by
  have den := log_density (by norm_num : (2:ℝ)≤11500) hj
  norm_num1 at den
  have high := logTwo_mono (show (0:ℝ)<11500+2 by norm_num)
    (show (11500:ℝ)+2≤(2:ℝ)^14 by norm_num)
  have hi := logTwo_two_rpow (14:ℝ)
  norm_num1 at hi
  norm_num1 at high
  rw [hi] at high
  have hh := mul_le_mul_of_nonneg_left high (show 0≤j by linarith)
  linarith only [hh,den,hj]

set_option exponentiation.threshold 70000 in
/-- The literal integer gate exceeds the whole prefix retained from earlier true-label widths. -/
theorem history_length_gate (Q:ℕ) (hq:Q=34548) :
    (4*(240*(Q*2^(3*11510)+2)))^2 < 2^69110 := by
  have hp : (0:ℕ) < 2^(3*11510) := by positivity
  have he : 4*(240*(Q*2^(3*11510)+2)) < 2^(3*11510+25) := by
    rw [pow_add]
    have hq2 : 960*(Q+2)<2^25 := by rw [hq]; decide
    have hl := Nat.mul_lt_mul_of_pos_left hq2 hp
    nlinarith only [hl,hp]
  have hs := Nat.pow_lt_pow_left he (by decide : (2:ℕ)≠0)
  rw [← pow_mul] at hs
  exact hs

/-- One binary step in the exponent pays for the conversion to natural logarithms. -/
theorem whole_clock {t:ℝ} (ht:(2:ℝ)^30≤t) :
    182+4*logTwo (t+2)+(26489/500)*phi (t+2)+1 ≤ 53*phi t := by
  have hp : 0≤t := by linarith only [ht]
  have hlog := logTwo_mono (show (0:ℝ)<2 by norm_num) (show 2≤t+2 by linarith only [ht])
  have hlog2 : logTwo 2=1 := div_self (ne_of_gt (Real.log_pos (by norm_num)))
  rw [hlog2] at hlog
  have hbound : 4096*logTwo (t+2) ≤ t :=
    log_control 4096 (2^30) 31 (by norm_num) (by norm_num) (by norm_num)
      (by norm_num) (by norm_num) ht
  have hr : 256*logTwo (t+2) ≤ phi t := by
    apply le_of_pow_le_pow_left₀ (by norm_num : (3:ℕ) ≠ 0) (S008.Piecewise.phi_nonneg hp)
    rw [mul_pow,phi_cube hp]
    have hs : (4096*logTwo (t+2))^2≤t^2 := by
      nlinarith only [mul_nonneg (sub_nonneg.mpr hbound) (show 0≤t+4096*logTwo (t+2) by linarith only [hp,hlog])]
    nlinarith only [mul_le_mul_of_nonneg_right hs (show 0≤logTwo (t+2) by linarith only [hlog])]
  have hsize : (2:ℝ)^20 ≤ phi t := by
    apply le_of_pow_le_pow_left₀ (by norm_num : (3:ℕ) ≠ 0) (S008.Piecewise.phi_nonneg hp)
    rw [phi_cube hp]
    nlinarith only [mul_nonneg (sub_nonneg.mpr ht) (show 0≤t+2^30 by linarith only [ht]),
      mul_nonneg (sq_nonneg t) (sub_nonneg.mpr hlog)]
  linarith only [hr,hsize,shifted_phi (show 2≤t by linarith only [ht])]

end S008.Effective53
