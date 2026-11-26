import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Data.Nat.Choose.Sum
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp

namespace S008.AxisSieve

/-- At depth j, the sum of the retained band weights scaled by 2^j. -/
def degreeNumer : ℕ → ℕ
  | 0 => 0
  | j+1 => 2 * degreeNumer j + 2*(4+2*j)

theorem degree_tail (j : ℕ) :
    degreeNumer j + (12+4*j) = 12 * 2^j := by
  induction j with
  | zero => decide
  | succ j ih =>
    simp only [degreeNumer, pow_succ]
    omega

/-- Evaluate the even Bonferroni truncation when exactly n distinct primes divide an integer. -/
def truncated (n d : ℕ) : ℤ :=
  ∑ i ∈ Finset.range (2*d+1), (-1:ℤ)^i * (n.choose i : ℤ)

theorem bonferroni_indicator (n d : ℕ) :
    (if n = 0 then (1:ℤ) else 0) ≤ truncated n d ∧
    truncated n d - (if n = 0 then (1:ℤ) else 0) ≤ (n.choose (2*d+1) : ℤ) := by
  cases n with
  | zero =>
    simp [truncated, Finset.sum_range_succ']
  | succ n =>
    have hx : truncated (n+1) d = (n.choose (2*d) : ℤ) := by
      unfold truncated
      rw [Int.alternating_sum_range_choose_eq_choose]
      simp [pow_mul]
    rw [hx]
    simp only [Nat.succ_ne_zero, ↓reduceIte, sub_zero, Nat.choose_succ_succ',
      Nat.cast_add]
    omega

/-- Exact deviation of the interval's count of multiples, including a negative left endpoint. -/
theorem interval_divisor_discrepancy (a y d : ℤ) (hd : 0 < d) :
    |d*(((a+y)/d)-(a/d))-y| < d := by
  have hx := Int.emod_add_mul_ediv a d
  have hxy := Int.emod_add_mul_ediv (a+y) d
  have he : d*(((a+y)/d)-(a/d))-y = a%d-(a+y)%d := by nlinarith
  rw [he, abs_lt]
  have h1 := Int.emod_nonneg a hd.ne'
  have h2 := Int.emod_nonneg (a+y) hd.ne'
  have h3 := Int.emod_lt_of_pos a hd
  have h4 := Int.emod_lt_of_pos (a+y) hd
  omega

/-- A positive band indicator, its even truncation and the next symmetric term. -/
structure Band where
  h : ℝ
  upper : ℝ
  err : ℝ
  hnonneg : 0 ≤ h
  hle : h ≤ upper
  hgap : upper - h ≤ err

def actual : List Band → ℝ
  | [] => 1
  | r :: rest => r.h * actual rest

def upper : List Band → ℝ
  | [] => 1
  | r :: rest => r.upper * upper rest

/-- Every product summand involves just one selected error factor. -/
def oneError : List Band → ℝ
  | [] => 0
  | r :: rs => r.err * upper rs + r.upper * oneError rs

theorem product_bounds (rs : List Band) : 0 ≤ actual rs ∧ actual rs ≤ upper rs := by
  induction rs with
  | nil => simp [actual, upper]
  | cons r rest ih =>
    exact ⟨mul_nonneg r.hnonneg ih.1,
      mul_le_mul r.hle ih.2 ih.1 (le_trans r.hnonneg r.hle)⟩

theorem single_omission (rs : List Band) : upper rs - oneError rs ≤ actual rs := by
  induction rs with
  | nil => simp [upper, actual, oneError]
  | cons r rest ih =>
    obtain ⟨hn, hu⟩ := product_bounds rest
    have he : 0 ≤ r.err := le_trans (sub_nonneg.mpr r.hle) r.hgap
    have h1 := mul_le_mul_of_nonneg_right r.hgap hn
    have h2 := mul_le_mul_of_nonneg_left hu he
    have h3 := mul_le_mul_of_nonneg_left ih (le_trans r.hnonneg r.hle)
    simp only [upper, oneError, actual]
    nlinarith

private def smallPrimes := (List.range 257).filter (fun p => decide (Nat.Prime p))

set_option maxRecDepth 100000 in
set_option maxHeartbeats 1600000 in
theorem exact_small_prime_product :
    smallPrimes.length = 54 ∧
    smallPrimes.prod < 10 * (smallPrimes.map (fun p => p-1)).prod := by
  decide +kernel

theorem bonferroni_relative :
    5*(8/5:ℚ)^5/120 + 7*(9/5:ℚ)^7/5040 + 12*(11/5:ℚ)^9/362880
      + 64*(3:ℚ)^11/39916800 + 64*(3:ℚ)^13/(6227020800*(1-9/(14*15:ℚ))) < 7/8 := by
  norm_num

private theorem log_two_lower : (1/2 : ℝ) ≤ Real.log 2 := by
  have h := Real.log_le_sub_one_of_pos (show (0 : ℝ) < 1 / 2 by norm_num)
  rw [Real.log_div (by norm_num) (by norm_num), Real.log_one] at h
  linarith

/-- Squared real scales times the exponential loss decrease from the initial threshold. -/
theorem decreasing_squared {t c : ℝ} (ht : 32 ≤ t) (hc : 1/8 ≤ c) :
    t^2 * (2 : ℝ)^(-c*t) ≤ 32^2 * (2 : ℝ)^(-c*32) := by
  have htpos : 0 < t := by linarith
  have hscale := Real.log_le_sub_one_of_pos (show (0:ℝ) < t/32 by positivity)
  rw [Real.log_div htpos.ne' (by norm_num)] at hscale
  have hcpos : 0 ≤ c := by linarith
  have hcl : (1/16:ℝ) ≤ c * Real.log 2 := by
    have h := mul_le_mul hc log_two_lower (by norm_num) hcpos
    linarith
  have hratio : 2*(Real.log t - Real.log 32) ≤ (t-32)*c*Real.log 2 := by
    nlinarith [mul_nonneg (sub_nonneg.mpr ht) (sub_nonneg.mpr hcl)]
  have hin := Real.exp_le_exp.mpr (show
      2*Real.log t + Real.log 2*(-c*t)
      ≤ 2*Real.log 32 + Real.log 2*(-c*32) by linarith)
  have ht2 : Real.exp (2*Real.log t) = t^2 := by
    rw [two_mul, Real.exp_add, Real.exp_log htpos, pow_two]
  have hb2 : Real.exp (2*Real.log (32:ℝ)) = 32^2 := by
    rw [two_mul, Real.exp_add, Real.exp_log (by norm_num), pow_two]
  rwa [Real.exp_add, Real.exp_add, ht2, hb2,
    ← Real.rpow_def_of_pos (by norm_num : (0:ℝ)<2),
    ← Real.rpow_def_of_pos (by norm_num : (0:ℝ)<2)] at hin


theorem leading_ratio {t : ℝ} (ht : 32 ≤ t) :
    (3/2) * (11*t/8)^2 * (2:ℝ)^(-(3/8:ℝ)*t) ≤ 363/512 := by
  have h := decreasing_squared (c:=3/8) ht (by norm_num)
  norm_num at h
  rw [neg_mul]
  nlinarith

theorem terminal_ratio {t : ℝ} (ht : 32 ≤ t) :
    3 * (11*t/8)^2 * (2:ℝ)^(-(17:ℝ)*t) < 1/1024 := by
  have h := decreasing_squared (c:=1) ht (by norm_num)
  norm_num at h
  have hex : (2:ℝ)^(-(17:ℝ)*t) ≤ 2^(-t) :=
    Real.rpow_le_rpow_of_exponent_le (by norm_num) (by linarith)
  nlinarith [mul_le_mul_of_nonneg_left hex (sq_nonneg t)]

theorem quartic_loss {t : ℝ} (ht : 0 ≤ t) :
    t^4 * (2:ℝ)^(-t/8) ≤ 64^4 := by
  have flex : t ≤ 64*(2:ℝ)^(t/32) := by
    have h := Real.add_one_le_exp (Real.log 2 * (t/32))
    rw [← Real.rpow_def_of_pos (by norm_num : (0:ℝ)<2)] at h
    nlinarith [mul_nonneg ht (sub_nonneg.mpr log_two_lower)]
  have h4 := pow_le_pow_left₀ ht flex 4
  have hcancel : ((2:ℝ)^(t/32))^4 * 2^(-t/8) = 1 := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul (by norm_num : (0:ℝ)≤2),
      ← Real.rpow_add (by norm_num : (0:ℝ)<2)]
    convert Real.rpow_zero 2 using 2
    norm_num
    ring
  have h := mul_le_mul_of_nonneg_right h4
    (Real.rpow_nonneg (by norm_num : (0:ℝ)≤2) (-t/8))
  simpa [mul_pow, mul_assoc, hcancel] using h

theorem discrepancy_ratio {t : ℝ} (ht : 32 ≤ t) :
    3*t*(11*t/8)^3 * (2:ℝ)^(-(44:ℝ)-t/8) < 1/1024 := by
  have h := quartic_loss (show 0 ≤ t by linarith)
  have hr : (2:ℝ)^(-(44:ℝ)-t/8) = (1/(2^44):ℝ) * 2^(-t/8) := by
    rw [show (-(44:ℝ)-t/8) = -44 + -t/8 by ring, Real.rpow_add (by norm_num : (0:ℝ)<2)]
    norm_num
  rw [hr]
  nlinarith

/-- The interval survives whenever the combinatorial sieve supplies the three proved losses. -/
theorem positive_survivor {t expected relativeObserved : ℝ} (ht : 32 ≤ t)
    (hmain : 1 ≤ expected)
    (hlower : expected
      - (3*t*(11*t/8)^3*(2:ℝ)^(-(44:ℝ)-t/8))
      - ((3/2)*(11*t/8)^2*(2:ℝ)^(-(3/8:ℝ)*t))
      - (3*(11*t/8)^2*(2:ℝ)^(-(17:ℝ)*t)) ≤ relativeObserved) :
    0 < relativeObserved := by
  linarith [leading_ratio ht, terminal_ratio ht, discrepancy_ratio ht]

end S008.AxisSieve
