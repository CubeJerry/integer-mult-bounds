import S008.NumericalCutoff

/-! Real-variable endpoint control for the continuous true-label curve.
    Algebraic Jensen proof using only log(u) ≤ u−1, with no derivative oracle. -/
namespace S008.TrueLabel

noncomputable def cubicGap (h e m r : ℝ) := h+3*(r^3-1)+3*e*Real.log r-m*r^2

private theorem log_spread {p q a b r : ℝ} (hp : 0≤p) (hq : 0≤q) (hpq : p+q=1)
    (ha : 1≤a) (hb : 1≤b) (hr : r=p*a+q*b) :
    Real.log r-(p*Real.log a+q*Real.log b) ≤ p*q*(b-a)^2 := by
  have hpa : 0<a := by linarith
  have hpb : 0<b := by linarith
  have hr1 : 1≤r := by
    nlinarith only [hr,hpq,mul_nonneg hp (sub_nonneg.mpr ha),mul_nonneg hq (sub_nonneg.mpr hb)]
  have hpr : 0<r := by linarith
  have hx := Real.log_le_sub_one_of_pos (div_pos hpr hpa)
  have hy := Real.log_le_sub_one_of_pos (div_pos hpr hpb)
  rw [Real.log_div hpr.ne' hpa.ne'] at hx
  rw [Real.log_div hpr.ne' hpb.ne'] at hy
  have hprod := add_le_add (mul_le_mul_of_nonneg_left hx hp) (mul_le_mul_of_nonneg_left hy hq)
  have hratio : p*(r/a-1)+q*(r/b-1)=p*q*(b-a)^2/(a*b) := by
    rw [hr,show p=1-q by linarith]
    field_simp
    ring
  have hlin : p*(Real.log r-Real.log a)+q*(Real.log r-Real.log b)=
      Real.log r-(p*Real.log a+q*Real.log b) := by
    rw [show p=1-q by linarith]
    ring
  rw [hratio,hlin] at hprod
  exact hprod.trans (div_le_self (by positivity) (one_le_mul_of_one_le_of_one_le ha hb))

/-- Under the numerical guard that holds in both applications, the transformed
    signed residual is convex between any two cube-root endpoints at least one. -/
theorem cube_jensen {p q a b r h e m : ℝ} (hp : 0≤p) (hq : 0≤q) (hpq : p+q=1)
    (ha : 1≤a) (hb : 1≤b) (hr : r=p*a+q*b) (he : 0≤e) (hm : m+3*e≤9) :
    cubicGap h e m r ≤ p*cubicGap h e m a+q*cubicGap h e m b := by
  have hlog := log_spread hp hq hpq ha hb hr
  let v := p*q*(b-a)^2
  have hv : 0≤v := by dsimp [v]; positivity
  have hr1 : 1≤r := by
    nlinarith only [hr,hpq,mul_nonneg hp (sub_nonneg.mpr ha),mul_nonneg hq (sub_nonneg.mpr hb)]
  have hrem : 0≤v*(3*(a+b+r)-m-3*e) := mul_nonneg hv (by linarith)
  have heq : p*cubicGap h e m a+q*cubicGap h e m b-cubicGap h e m r =
      v*(3*(a+b+r)-m)-3*e*(Real.log r-(p*Real.log a+q*Real.log b)) := by
    unfold cubicGap
    dsimp [v]
    rw [hr,show p=1-q by linarith]
    ring
  have hcharge := mul_le_mul_of_nonneg_left hlog (show 0≤3*e by linarith)
  change 3*e*(Real.log r-(p*Real.log a+q*Real.log b)) ≤ 3*e*v at hcharge
  nlinarith only [heq,hrem,hcharge]

private theorem gap_root {t : ℝ} (h e m : ℝ) (ht : 0<t) :
    cubicGap h e m (t^(1/3:ℝ)) = h+3*(t-1)+e*Real.log t-m*t^(2/3:ℝ) := by
  have h3 : (t^(1/3:ℝ))^3=t := by
    rw [← Real.rpow_natCast,← Real.rpow_mul ht.le]
    norm_num
  have h2 : (t^(1/3:ℝ))^2=t^(2/3:ℝ) := by
    rw [← Real.rpow_natCast,← Real.rpow_mul ht.le]
    norm_num
  unfold cubicGap
  rw [h3,h2,Real.log_rpow ht]
  ring

/-- One actual band is bounded everywhere by its two endpoint comparisons. -/
theorem whole_band {h e m u t : ℝ} (he : 0≤e) (hm : m+3*e≤9) (ht : 1≤t) (htu : t≤u)
    (h1 : h≤m) (hu : h+3*(u-1)+e*Real.log u ≤ m*u^(2/3:ℝ)) :
    h+3*(t-1)+e*Real.log t ≤ m*t^(2/3:ℝ) := by
  by_cases hu1 : u=1
  · have hte : t=1 := by linarith
    simpa [hte] using h1
  have hup : 1<u := lt_of_le_of_ne (ht.trans htu) (Ne.symm hu1)
  have htp : 0<t := by linarith
  let r := t^(1/3:ℝ)
  let b := u^(1/3:ℝ)
  have hr : 1≤r := Real.one_le_rpow ht (by norm_num)
  have hb : 1<b := Real.one_lt_rpow hup (by norm_num)
  have hrb : r≤b := Real.rpow_le_rpow htp.le htu (by norm_num)
  let p := (b-r)/(b-1)
  let q := (r-1)/(b-1)
  have hden : 0<b-1 := by linarith
  have hp : 0≤p := div_nonneg (sub_nonneg.mpr hrb) hden.le
  have hq : 0≤q := div_nonneg (sub_nonneg.mpr hr) hden.le
  have hpq : p+q=1 := by dsimp [p,q]; field_simp; ring
  have hblend : r=p*1+q*b := by dsimp [p,q]; field_simp; ring
  have hj := cube_jensen (h:=h) hp hq hpq (by norm_num : (1:ℝ)≤1) hb.le hblend he hm
  have hg1 : cubicGap h e m 1≤0 := by simpa [cubicGap,sub_nonpos] using h1
  have hgu : cubicGap h e m b≤0 := by
    rw [show b=u^(1/3:ℝ) by rfl,gap_root h e m (by linarith)]
    linarith only [hu]
  have hsum := add_nonpos (mul_nonpos_of_nonneg_of_nonpos hp hg1)
    (mul_nonpos_of_nonneg_of_nonpos hq hgu)
  have hgr := hj.trans hsum
  rw [show r=t^(1/3:ℝ) by rfl,gap_root h e m htp] at hgr
  exact sub_nonpos.mp hgr

private theorem root_eight : (8:ℝ)^(2/3:ℝ)=4 := by
  rw [show (8:ℝ)=(2:ℝ)^3 by norm_num,← Real.rpow_natCast,← Real.rpow_mul (by norm_num : (0:ℝ)≤2)]
  norm_num

theorem effective_band {u t : ℝ} (htu : t≤u) (ht : 1≤t) (hu : 8≤u)
    (hcap : u ≤ 8001/1000) (hlog : Real.log u ≤ 21/10) :
    (1447/200:ℝ)+3*(t-1)+(167/500)*Real.log t ≤ (1447/200:ℝ)*t^(2/3:ℝ) := by
  have hroot := Real.rpow_le_rpow (show (0:ℝ)≤8 by norm_num) hu (by norm_num : (0:ℝ)≤2/3)
  rw [root_eight] at hroot
  apply whole_band (by norm_num) (by norm_num) ht htu (by norm_num)
  linarith only [hcap,hlog,hroot]

theorem limiting_band {t : ℝ} (ht : 1≤t) (h8 : t≤8) :
    (7+Real.log 2/3)+3*(t-1)+(1/3)*Real.log t ≤ (7+Real.log 2/3)*t^(2/3:ℝ) := by
  have hl := Real.log_le_sub_one_of_pos (show (0:ℝ)<2 by norm_num)
  norm_num at hl
  have h8l : Real.log (8:ℝ)=3*Real.log 2 := by rw [show (8:ℝ)=(2:ℝ)^3 by norm_num,Real.log_pow]; norm_num
  apply whole_band (by norm_num) (by linarith) ht h8 (by rfl)
  rw [root_eight,h8l]
  linarith

/-- The expanded actual alphabet/cardinality invoice retains log(t) at every degree. -/
theorem true_letter_invoice {d s t σ : ℝ} (hd : 16≤d) (ht : 1≤t)
    (hwidth : t≤s/d^2+3) (hh : S008.NumericalCutoff.logTwo (2*d-1)≤d)
    (hin : σ+2 ≤ 39+S008.NumericalCutoff.logTwo (2*d-1)+(d+1)*(2*d-1)+
      (2*d-1+d)*t+d*(d-1)*S008.NumericalCutoff.logTwo t) :
    σ+2 ≤ 3*s/d+d^2*(S008.NumericalCutoff.logTwo t+3) := by
  have hg : 0≤S008.NumericalCutoff.logTwo t := by
    unfold S008.NumericalCutoff.logTwo
    exact div_nonneg (Real.log_nonneg ht) (Real.log_nonneg (by norm_num))
  have hp : 0<d := by linarith
  have hwidth' : 3*d*t≤3*s/d+9*d := by
    have h := mul_le_mul_of_nonneg_left hwidth (by linarith : 0≤3*d)
    have he : 3*d*(s/d^2+3)=3*s/d+9*d := by field_simp; ring
    rwa [he] at h
  have hquad : 39+12*d≤d^2 := by
    nlinarith only [mul_nonneg (sub_nonneg.mpr hd) (show 0≤d+4 by linarith)]
  have hsum : 0 ≤ (d-S008.NumericalCutoff.logTwo (2*d-1))+
      (3*s/d+9*d-3*d*t)+(d^2-(39+12*d))+t+
      d*S008.NumericalCutoff.logTwo t+(d+1) := by
    exact add_nonneg (add_nonneg (add_nonneg (add_nonneg (add_nonneg
      (sub_nonneg.mpr hh) (sub_nonneg.mpr hwidth')) (sub_nonneg.mpr hquad))
      (show 0≤t by linarith)) (mul_nonneg hp.le hg)) (by linarith)
  apply hin.trans
  apply sub_nonneg.mp
  convert hsum using 1
  ring

end S008.TrueLabel
