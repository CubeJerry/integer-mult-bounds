import S008.Packing
import S008.AllLengths

namespace S008.InputClock
open S008.NumericalCutoff S008.Packing S008.AllLengths

set_option exponentiation.threshold 8192

private theorem log_two_nat_pow (k : ℕ) : logTwo ((2:ℝ)^k) = (k:ℝ) := by
  simpa only [Real.rpow_natCast] using logTwo_two_rpow (k:ℝ)

/-- Transfer the ceiling-division geometry to the real input-size branches. -/
theorem input_geometry {n : ℕ} (hn : 2^48<n) :
    (addressWidth n:ℝ) ≤ logTwo n ∧ logTwo n < 2*(addressWidth n:ℝ) ∧
    5 ≤ logTwo (logTwo n) ∧
    (addressWidth n < 2^4096 → logTwo (logTwo n) ≤ 4097) ∧
    (2^4096 ≤ addressWidth n → 4096 ≤ logTwo (logTwo n)) := by
  obtain ⟨h32,hb,hN,_⟩ := physical_sizes hn
  have hlNat : 2^(addressWidth n)<n := hN
  have hl : (2:ℝ)^(addressWidth n) ≤ (n:ℝ) := by exact_mod_cast hlNat.le
  have huNat := Nat.le_pow_clog (by decide : 1<2) n
  change n ≤ 2^digitWidth n at huNat
  have hu : (n:ℝ) ≤ (2:ℝ)^(digitWidth n) := by exact_mod_cast huNat
  have lp := logTwo_mono (pow_pos (by norm_num : (0:ℝ)<2) _) hl
  rw [log_two_nat_pow] at lp
  have np : (0:ℝ)<(n:ℝ) := by exact_mod_cast (show 0<n by omega)
  have up := logTwo_mono np hu
  rw [log_two_nat_pow] at up
  have hbr : (digitWidth n:ℝ)<2*(addressWidth n:ℝ) := by exact_mod_cast hb
  have hr := lt_of_le_of_lt up hbr
  have h32r : (2:ℝ)^5 ≤ (addressWidth n:ℝ) := by exact_mod_cast h32
  have hs := logTwo_mono (pow_pos (by norm_num : (0:ℝ)<2) 5) (h32r.trans lp)
  rw [log_two_nat_pow] at hs
  have hlog_pos : 0 < logTwo n := lt_of_lt_of_le (pow_pos (by norm_num : (0:ℝ)<2) 5) (h32r.trans lp)
  refine ⟨lp,hr,by exact_mod_cast hs,?_,?_⟩
  · intro hk
    have hkr : (addressWidth n:ℝ) < (2:ℝ)^4096 := by exact_mod_cast hk
    have hr' : logTwo n ≤ (2:ℝ)^4097 := by
      rw [pow_succ]
      linarith only [hr,hkr]
    have hf := logTwo_mono hlog_pos hr'
    rw [log_two_nat_pow] at hf
    exact_mod_cast hf
  · intro hk
    have hkr : (2:ℝ)^4096 ≤ (addressWidth n:ℝ) := by exact_mod_cast hk
    have hf := logTwo_mono (pow_pos (by norm_num : (0:ℝ)<2) 4096) (hkr.trans lp)
    rw [log_two_nat_pow] at hf
    exact_mod_cast hf

theorem phi_mono {x y : ℝ} (hx : 0 ≤ x) (hxy : x ≤ y) : phi x ≤ phi y := by
  have hl := logTwo_mono (show 0<x+2 by linarith) (show x+2≤y+2 by linarith)
  have h0 : 0≤logTwo (x+2) := by
    unfold logTwo
    exact div_nonneg (Real.log_nonneg (by linarith)) (Real.log_nonneg (by norm_num))
  have hs : x^2 ≤ y^2 := by nlinarith [mul_nonneg (sub_nonneg.mpr hxy) (by linarith : 0≤y+x)]
  have hh := mul_le_mul hs hl h0 (sq_nonneg y)
  unfold phi
  exact Real.rpow_le_rpow (mul_nonneg (sq_nonneg x) h0) hh (by norm_num)

/-- Compose the three physical supplier inequalities at the actual input length. -/
theorem all_input_clock {n : ℕ} (hn : 2≤n) (cost : ℝ)
    (raw : n≤2^48 → cost ≤ (n:ℝ)*(2:ℝ)^60)
    (dyadic : 2^48<n → addressWidth n<2^4096 →
      cost ≤ (n:ℝ)*(2:ℝ)^(170+5*logTwo (logTwo n)))
    (coprime : 2^48<n → 2^4096≤addressWidth n →
      cost ≤ (n:ℝ)*Real.sqrt (logTwo n)*
        (2:ℝ)^(182+4*logTwo (logTwo (logTwo n)+2)+70*phi (logTwo (logTwo n)+2))) :
    cost ≤ (n:ℝ)*Real.sqrt (1+logTwo n)*(2:ℝ)^(71*phi (logTwo (1+logTwo n))) := by
  let ell := logTwo (n:ℝ)
  let x := logTwo (1+ell)
  let z := logTwo ell
  have hn0 : (0:ℝ)≤n := Nat.cast_nonneg n
  have nn : (2:ℝ) ≤ n := by exact_mod_cast hn
  have hlog2 : logTwo 2 = 1 := div_self (ne_of_gt (Real.log_pos (by norm_num)))
  have ell1 : 1 ≤ ell := by simpa only [hlog2] using logTwo_mono (by norm_num : (0:ℝ)<2) nn
  have x1 : 1 ≤ x := by
    have := logTwo_mono (by norm_num : (0:ℝ)<2) (show 2≤1+ell by linarith)
    simpa only [hlog2] using this
  have hz : z ≤ x := logTwo_mono (by linarith : 0<ell) (by linarith : ell≤1+ell)
  have hz0 : 0≤z := by
    unfold z logTwo
    exact div_nonneg (Real.log_nonneg ell1) (Real.log_nonneg (by norm_num))
  have hphi := phi_mono hz0 hz
  have hroot : 1 ≤ Real.sqrt (1+ell) := by
    calc
      (1:ℝ) = Real.sqrt 1 := by simp
      _ ≤ Real.sqrt (1+ell) := Real.sqrt_le_sqrt (by linarith)
  have hscale : (n:ℝ) ≤ (n:ℝ)*Real.sqrt (1+ell) := by
    simpa only [mul_one] using mul_le_mul_of_nonneg_left hroot hn0
  have hrule (e:ℝ) (hc : e≤71*phi x) : (n:ℝ)*(2:ℝ)^e ≤
      (n:ℝ)*Real.sqrt (1+ell)*(2:ℝ)^(71*phi x) :=
    mul_le_mul hscale (Real.rpow_le_rpow_of_exponent_le (by norm_num) hc)
      (Real.rpow_nonneg (by norm_num) _) (mul_nonneg hn0 (Real.sqrt_nonneg _))
  by_cases hsmall : n≤2^48
  · have he := hrule 60 (small_excess x1)
    have h60 : (2:ℝ)^(60:ℝ)=(2:ℝ)^(60:ℕ) := by norm_num
    rw [h60] at he
    exact (raw hsmall).trans he
  have hlarge := Nat.lt_of_not_ge hsmall
  obtain ⟨_,_,z5,zmid,zbig⟩ := input_geometry hlarge
  by_cases hm : addressWidth n<2^4096
  · have he := dyadic_middle z5 (zmid hm)
    exact (dyadic hlarge hm).trans (hrule _ (by linarith only [hphi,he]))
  · have hh := Nat.le_of_not_gt hm
    have he := coprime_excess (zbig hh)
    have hp := Real.rpow_le_rpow_of_exponent_le (by norm_num : (1:ℝ)≤2)
      (show 182+4*logTwo (z+2)+70*phi (z+2) ≤ 71*phi x by linarith only [he,hphi])
    have hsc := mul_le_mul_of_nonneg_left (Real.sqrt_le_sqrt (show ell≤1+ell by linarith)) hn0
    exact (coprime hlarge hh).trans (mul_le_mul hsc hp (Real.rpow_nonneg (by norm_num) _)
      (mul_nonneg hn0 (Real.sqrt_nonneg _)))

end S008.InputClock
