import Mathlib.Data.Nat.Log
import S008.WholeProfile

/-! A finite, nondecreasing surplus at the actual spatial child widths,
    and the two-branch numerical clock at the R=240 endpoint. -/
namespace S008.Piecewise

open S008.NumericalCutoff S008.WholeProfile
open scoped BigOperators

/-- The log address actually used by a spatial child of bit width f. -/
def activeLog (f : ℕ) : ℕ := Nat.clog 2 (f+2)

theorem activeLog_mono : Monotone activeLog := by
  intro f a h
  exact Nat.clog_mono_right 2 (Nat.add_le_add_right h 2)

/-- Prefix surplus, sampled at the integer arguments used by recursion. -/
noncomputable def history (H : ℕ → ℝ) : ℕ → ℝ
  | 0 => max 0 (H 0 - (159/4:ℝ)*phi 0)
  | n+1 => max (history H n) (H (n+1) - (159/4:ℝ)*phi ((n+1:ℕ):ℝ))

noncomputable def envelope (H : ℕ → ℝ) (n : ℕ) : ℝ :=
  48*phi (n:ℝ) + history H n

theorem history_mono (H : ℕ → ℝ) : Monotone (history H) :=
  monotone_nat_of_le_succ (fun _ => le_max_left _ _)

theorem history_nonneg (H : ℕ → ℝ) (n : ℕ) : 0 ≤ history H n :=
  (le_max_left _ _ : 0 ≤ history H 0).trans (history_mono H (Nat.zero_le n))

theorem history_current (H : ℕ → ℝ) (n : ℕ) :
    H n - (159/4:ℝ)*phi (n:ℝ) ≤ history H n := by
  cases n with
  | zero => simp [history]
  | succ n => exact le_max_right _ _

theorem history_upper (H : ℕ → ℝ) {n : ℕ} {D : ℝ} (hD : 0 ≤ D)
    (h : ∀ j ≤ n, H j - (159/4:ℝ)*phi (j:ℝ) ≤ D) : history H n ≤ D := by
  induction n with
  | zero => simpa [history] using (max_le hD (h 0 (le_refl _)))
  | succ n ih =>
    exact max_le (ih fun j hj => h j (Nat.le_succ_of_le hj)) (h (n+1) (le_refl _))

/-- The native bill at any rounded existential child left in the local data
    invoice fits the parent bound. H itself is only sampled, not required monotone. -/
theorem covers_earlier (H : ℕ → ℝ) {v x : ℕ} (hv : v ≤ x)
    (hphi : phi (v:ℝ) ≤ phi (x:ℝ)) :
    H v + (33/4:ℝ)*phi (x:ℝ) ≤ envelope H x := by
  have h := (history_current H v).trans (history_mono H hv)
  unfold envelope
  linarith

/-- An index represents a paid child invocation, including repeat uses. The factor
    w may contain the occupied child volume and its own square-root width. -/
theorem weighted_quarter {ι : Type*} (s : Finset ι) (f : ι → ℕ) (a : ℕ)
    (w : ι → ℝ) (parent : ℝ) (H : ℕ → ℝ)
    (hf : ∀ i ∈ s, f i ≤ a) (hw : ∀ i ∈ s, 0 ≤ w i)
    (hq : ∑ i ∈ s, w i*(2:ℝ)^(48*phi (activeLog (f i):ℝ)) ≤
      parent*(2:ℝ)^(48*phi (activeLog a:ℝ))/4) :
    ∑ i ∈ s, w i*(2:ℝ)^(envelope H (activeLog (f i))) ≤
      parent*(2:ℝ)^(envelope H (activeLog a))/4 := by
  have h2 : (0:ℝ) < 2 := by norm_num
  calc
    _ ≤ ∑ i ∈ s, (w i*(2:ℝ)^(48*phi (activeLog (f i):ℝ))) *
        (2:ℝ)^(history H (activeLog a)) := by
      apply Finset.sum_le_sum
      intro i hi
      rw [envelope, Real.rpow_add h2, ← mul_assoc]
      exact mul_le_mul_of_nonneg_left
        (Real.rpow_le_rpow_of_exponent_le (by norm_num) (history_mono H (activeLog_mono (hf i hi))))
        (mul_nonneg (hw i hi) (Real.rpow_nonneg h2.le _))
    _ = (∑ i ∈ s, w i*(2:ℝ)^(48*phi (activeLog (f i):ℝ))) *
        (2:ℝ)^(history H (activeLog a)) := by rw [Finset.sum_mul]
    _ ≤ (parent*(2:ℝ)^(48*phi (activeLog a:ℝ))/4) *
        (2:ℝ)^(history H (activeLog a)) :=
        mul_le_mul_of_nonneg_right hq (Real.rpow_nonneg h2.le _)
    _ = _ := by rw [envelope, Real.rpow_add h2]; ring

noncomputable def raw (x : ℝ) : ℝ :=
  2^25+4*logTwo (x+2) + max (2220000000000+48*phi (x+2))
    (4112174977105665/1024+(17/32768)*(x+2)+(33/4)*phi (x+2))

/-- Shifting the argument by two preserves the density comparison in the
    direction needed by the physical rounded log width. -/
theorem shifted_density {z t P : ℝ} (hz : 2 ≤ z) (ht : z ≤ t)
    (hp : 0 ≤ P) (hP : phi (z+2) ≤ P) : z*phi (t+2) ≤ t*P := by
  have h := phi_density (by linarith : 2 ≤ z+2) (by linarith : z+2 ≤ t+2)
  have h₁ := h.trans (mul_le_mul_of_nonneg_left hP (by linarith : 0 ≤ t+2))
  have h₂ := mul_le_mul_of_nonneg_left h₁ (by linarith : 0 ≤ z)
  have h₃ := mul_le_mul_of_nonneg_right
    (show z*(t+2) ≤ t*(z+2) by nlinarith only [ht]) hp
  by_contra! hn
  nlinarith only [h₂, h₃, mul_pos (by linarith : 0 < z+2) (sub_pos.mpr hn)]

/-- Two scalar tests at any left endpoint imply the complete raw exponent
    inequality for every later real scale, with one conversion bit in reserve. -/
theorem all_later {z t L P : ℝ} (hz : 2 ≤ z) (ht : z ≤ t)
    (hL : logTwo (z+2) ≤ L) (hp : 0 ≤ P) (hP : phi (z+2) ≤ P)
    (hD : 2^25+4*L+2220000000000+48*P+1 ≤ z/1000)
    (hM : 2^25+4*L+4112174977105665/1024+(17/32768)*(z+2)+(33/4)*P+1 ≤ z/1000) :
    raw t+1 ≤ t/1000 := by
  have hlog := (log_density hz ht).trans
    (mul_le_mul_of_nonneg_left hL (by linarith : 0 ≤ t))
  have hphi := shifted_density hz ht hp hP
  have hzpos : 0 < z := by linarith
  have ht0 : 0 ≤ t := by linarith
  have h₁ := mul_le_mul_of_nonneg_left hD ht0
  have h₂ := mul_le_mul_of_nonneg_left hM ht0
  have hD' : 2^25+4*logTwo (t+2)+2220000000000+48*phi (t+2)+1 ≤ t/1000 := by
    by_contra! hn
    nlinarith only [h₁,ht,hlog,hphi,mul_pos hzpos (sub_pos.mpr hn)]
  have hM' : 2^25+4*logTwo (t+2)+4112174977105665/1024+
      (17/32768)*(t+2)+(33/4)*phi (t+2)+1 ≤ t/1000 := by
    by_contra! hn
    nlinarith only [h₂,ht,hlog,hphi,mul_pos hzpos (sub_pos.mpr hn)]
  unfold raw
  rcases le_total (2220000000000+48*phi (t+2))
    (4112174977105665/1024+(17/32768)*(t+2)+(33/4)*phi (t+2)) with h | h
  · rw [max_eq_right h]
    linarith only [hM']
  · rw [max_eq_left h]
    linarith only [hD']

private theorem log_at_cutoff :
    logTwo ((11700000000000000:ℝ)+4) ≤ 54 := by
  have h : (11700000000000000:ℝ)+4 ≤ (2:ℝ)^(54:ℕ) := by norm_num
  have hm := logTwo_mono (by norm_num : (0:ℝ) < 11700000000000000+4) h
  rw [← Real.rpow_natCast, logTwo_two_rpow] at hm
  exact hm

theorem simple_raw {t : ℝ} (ht : (11700000000000000:ℝ) ≤ t) :
    raw t+1 ≤ t/1000 := by
  have hL : logTwo ((11700000000000000:ℝ)+2) ≤ 54 :=
    (logTwo_mono (by norm_num) (show (11700000000000000:ℝ)+2 ≤ 11700000000000000+4 by
        norm_num)).trans log_at_cutoff
  have hP : phi ((11700000000000000:ℝ)+2) ≤ 194800000000 := by
    apply le_of_pow_le_pow_left₀ (by norm_num : (3:ℕ) ≠ 0) (by norm_num)
    rw [phi_cube (by norm_num)]
    have hlog := log_at_cutoff
    norm_num at hlog ⊢
    linarith only [hlog]
  exact all_later (by norm_num) ht hL (by norm_num) hP (by norm_num) (by norm_num)

private theorem ln_two_lower : (1/2:ℝ) ≤ Real.log 2 := by
  have h := Real.log_le_sub_one_of_pos (show (0:ℝ) < 1/2 by norm_num)
  rw [Real.log_div (by norm_num) (by norm_num), Real.log_one] at h
  linarith

/-- For the natural-logarithm source convention the prefactor remains one. -/
theorem natlog_at_simple (n cost : ℝ)
    (hn : (2:ℝ)^((2:ℝ)^(11700000000000000:ℝ)) ≤ n)
    (hcost : cost ≤ n*Real.sqrt (logTwo n)*(2:ℝ)^(raw (logTwo (logTwo n)))) :
    cost ≤ n*(Real.log n)^(501/1000:ℝ) := by
  have hnpos : 0<n := lt_of_lt_of_le (Real.rpow_pos_of_pos (by norm_num) _) hn
  have hlog := logTwo_mono (Real.rpow_pos_of_pos (show (0:ℝ)<2 by norm_num) _) hn
  rw [logTwo_two_rpow] at hlog
  have hL : 0 < logTwo n := lt_of_lt_of_le (Real.rpow_pos_of_pos (by norm_num) _) hlog
  have hl2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have hln : 0 ≤ Real.log n := by
    unfold logTwo at hL
    exact le_of_lt ((div_pos_iff_of_pos_right hl2).mp hL)
  have hex := simple_raw (length_gate n _ hn)
  have hpow := Real.rpow_le_rpow_of_exponent_le (show (1:ℝ) ≤ 2 by norm_num) hex
  rw [Real.rpow_add (by norm_num), Real.rpow_one] at hpow
  have hid : (2:ℝ)^(logTwo (logTwo n)/1000) = (logTwo n)^(1/1000:ℝ) := by
    rw [div_eq_mul_one_div, Real.rpow_mul (by norm_num : (0:ℝ) ≤ 2), two_log_cancel hL]
  rw [hid] at hpow
  have hb : 2*cost ≤ n*(logTwo n)^(501/1000:ℝ) := by
    calc
      2*cost ≤ n*Real.sqrt (logTwo n)*(logTwo n)^(1/1000:ℝ) := by
        nlinarith only [hcost, mul_le_mul_of_nonneg_left hpow
          (mul_nonneg hnpos.le (Real.sqrt_nonneg (logTwo n)))]
      _ = _ := by rw [Real.sqrt_eq_rpow, mul_assoc, ← Real.rpow_add hL]; norm_num
  have hupper : logTwo n ≤ 2*Real.log n := by
    unfold logTwo
    rw [div_le_iff₀ hl2]
    nlinarith only [mul_nonneg hln (sub_nonneg.mpr ln_two_lower)]
  have hmono := Real.rpow_le_rpow hL.le hupper (by norm_num : (0:ℝ) ≤ 501/1000)
  rw [Real.mul_rpow (by norm_num) hln] at hmono
  have hfactor := Real.rpow_le_rpow_of_exponent_le (show (1:ℝ) ≤ 2 by norm_num)
    (show (501/1000:ℝ) ≤ 1 by norm_num)
  rw [Real.rpow_one] at hfactor
  have hh := mul_le_mul_of_nonneg_right hfactor (Real.rpow_nonneg hln (501/1000:ℝ))
  nlinarith only [hb,mul_le_mul_of_nonneg_left (hmono.trans hh) hnpos.le]

end S008.Piecewise
