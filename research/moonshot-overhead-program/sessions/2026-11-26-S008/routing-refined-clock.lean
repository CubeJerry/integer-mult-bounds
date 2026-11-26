import S008.RefinedFrame
import S008.RecountRefined

namespace S008.Piecewise.Refined
open S008.NumericalCutoff S008.WholeProfile S008.Piecewise
open S008.Recount.Refined (Z)

noncomputable def paid (t : ℝ) : ℝ := 183+4*logTwo (t+2)+
  max (D+48*phi (t+2)) (3035148971130625/1024+(17/32768)*(t+2)+(33/4)*phi (t+2))

private theorem at_endpoint : paid (Z:ℝ) ≤ (Z:ℝ)/1000 := by
  have h := S008.Recount.Refined.current_above_history
    (v:=(Z:ℝ)+2) (by linarith) (le_refl _)
  have hp := S008.Recount.Refined.passing
  change D < 3035148971130625/1024+(17/32768)*((Z:ℝ)+2)-(159/4)*phi ((Z:ℝ)+2) at h
  unfold S008.Recount.Refined.movement S008.Recount.Refined.A
    S008.Recount.Refined.β S008.Recount.Refined.α at hp
  unfold paid
  rw [max_eq_right (by linarith only [h])]
  linarith only [hp]

private theorem scalar_density {z t c a r : ℝ} (hz : 2 ≤ z) (ht : z ≤ t)
    (hc : 0 ≤ c) (hr : 0 ≤ r)
    (he : c+a*z+4*logTwo (z+2)+r*phi (z+2) ≤ z/1000) :
    c+a*t+4*logTwo (t+2)+r*phi (t+2) ≤ t/1000 := by
  have hlog := log_density hz ht
  have hphi := shifted_density hz ht (phi_nonneg (by linarith : 0≤z+2)) (le_refl (phi (z+2)))
  have hphi' := mul_le_mul_of_nonneg_left hphi hr
  have hc' := mul_nonneg (sub_nonneg.mpr ht) hc
  have he' := mul_le_mul_of_nonneg_left he (by linarith : 0≤t)
  by_contra! hn
  nlinarith only [hlog,hphi',hc',he',mul_pos (by linarith : 0<z) (sub_pos.mpr hn)]

/-- Every larger real input scale passes, including future dyadic degree changes. -/
theorem paid_all_later {t : ℝ} (ht : (Z:ℝ) ≤ t) : paid t ≤ t/1000 := by
  have hZ : (2:ℝ) ≤ (Z:ℝ) := by norm_num [Z]
  have he := at_endpoint
  unfold paid at he ⊢
  have h₁ := le_max_left (D+48*phi ((Z:ℝ)+2))
    (3035148971130625/1024+(17/32768)*((Z:ℝ)+2)+(33/4)*phi ((Z:ℝ)+2))
  have h₂ := le_max_right (D+48*phi ((Z:ℝ)+2))
    (3035148971130625/1024+(17/32768)*((Z:ℝ)+2)+(33/4)*phi ((Z:ℝ)+2))
  have b₁ := scalar_density (c:=183+D) (a:=0) (r:=48) hZ ht (by norm_num [D])
    (by norm_num) (by linarith only [he,h₁])
  have b₂ := scalar_density (c:=183+3035148971130625/1024+2*(17/32768)) (a:=17/32768) (r:=33/4)
    hZ ht (by norm_num) (by norm_num) (by linarith only [he,h₂])
  rcases le_total (D+48*phi (t+2))
    (3035148971130625/1024+(17/32768)*(t+2)+(33/4)*phi (t+2)) with h | h
  · rw [max_eq_right h]
    linarith only [b₂]
  · rw [max_eq_left h]
    linarith only [b₁]

private theorem ln_two_lower : (1/2:ℝ) ≤ Real.log 2 := by
  have h := Real.log_le_sub_one_of_pos (show (0:ℝ) < 1/2 by norm_num)
  rw [Real.log_div (by norm_num) (by norm_num), Real.log_one] at h
  linarith

/-- The actual rounded root invoice, with natural logarithms and unit time
    coefficient at the refined integer endpoint. -/
theorem natural_clock (H : ℝ → ℝ) (hS : supports H) (n cost : ℝ) (a : ℕ)
    (hn : (2:ℝ)^((2:ℝ)^(Z:ℝ)) ≤ n) (ha : (activeLog a:ℝ) ≤ logTwo (logTwo n)+2)
    (hcost : cost ≤ n*Real.sqrt (logTwo n)*(2:ℝ)^(182+4*logTwo (logTwo (logTwo n)+2)+
        envelope (fun j => H (j:ℝ)) (activeLog a))) : cost ≤ n*(Real.log n)^(501/1000:ℝ) := by
  have hnpos : 0<n := lt_of_lt_of_le (Real.rpow_pos_of_pos (by norm_num) _) hn
  have hlog := logTwo_mono (Real.rpow_pos_of_pos (show (0:ℝ)<2 by norm_num) _) hn
  rw [logTwo_two_rpow] at hlog
  have hL : 0 < logTwo n := lt_of_lt_of_le (Real.rpow_pos_of_pos (by norm_num) _) hlog
  have hl2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have hln : 0 ≤ Real.log n := by
    unfold logTwo at hL
    exact le_of_lt ((div_pos_iff_of_pos_right hl2).mp hL)
  have hg := rounded_frame H hS (activeLog a) _ ha
  have he := paid_all_later (length_gate n _ hn)
  unfold paid at he
  let exponent := 182+4*logTwo (logTwo (logTwo n)+2)+envelope (fun j => H (j:ℝ)) (activeLog a)
  have hx : exponent+1 ≤ logTwo (logTwo n)/1000 := by
    unfold exponent
    linarith only [he,hg]
  have hpow := Real.rpow_le_rpow_of_exponent_le (show (1:ℝ) ≤ 2 by norm_num) hx
  rw [Real.rpow_add (by norm_num),Real.rpow_one] at hpow
  have hid : (2:ℝ)^(logTwo (logTwo n)/1000) = (logTwo n)^(1/1000:ℝ) := by
    rw [div_eq_mul_one_div,Real.rpow_mul (by norm_num : (0:ℝ)≤2),two_log_cancel hL]
  rw [hid] at hpow
  change cost ≤ n*Real.sqrt (logTwo n)*(2:ℝ)^exponent at hcost
  have hb : 2*cost ≤ n*(logTwo n)^(501/1000:ℝ) := by
    calc
      2*cost ≤ n*Real.sqrt (logTwo n)*(logTwo n)^(1/1000:ℝ) := by
        nlinarith only [hcost,mul_le_mul_of_nonneg_left hpow
          (mul_nonneg hnpos.le (Real.sqrt_nonneg (logTwo n)))]
      _ = _ := by rw [Real.sqrt_eq_rpow,mul_assoc,← Real.rpow_add hL]; norm_num
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

/-- Concrete upper-shape specialization, with its supports already verified. -/
theorem explicit_natural_clock (n cost : ℝ) (a : ℕ)
    (hn : (2:ℝ)^((2:ℝ)^(8931714897907030:ℝ)) ≤ n) (ha : (activeLog a:ℝ) ≤ logTwo (logTwo n)+2)
    (hcost : cost ≤ n*Real.sqrt (logTwo n)*(2:ℝ)^(182+4*logTwo (logTwo (logTwo n)+2)+
        envelope (fun j => upper (j:ℝ)) (activeLog a))) : cost ≤ n*(Real.log n)^(501/1000:ℝ) := by
  apply natural_clock upper upper_supports n cost a _ ha hcost
  convert hn using 3; norm_num [Z]

end S008.Piecewise.Refined
