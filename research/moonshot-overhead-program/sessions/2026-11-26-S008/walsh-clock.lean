import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity

/-! A direct cubic proof of the adaptive binary Walsh potential decrement. -/
namespace Moonshot.AlignedWalsh.Clock

noncomputable def logTwo (x : ℝ) : ℝ := Real.log (x+2)/Real.log 2
noncomputable def phi (x : ℝ) : ℝ := (x^2*logTwo x)^(1/3:ℝ)
noncomputable def psi (y : ℝ) : ℝ := Real.sqrt (y*logTwo y)

private lemma logTwo_nonneg {x : ℝ} (hx : 0≤x) : 0≤logTwo x :=
  div_nonneg (Real.log_nonneg (by linarith)) (Real.log_pos (by norm_num)).le

private lemma logTwo_mono {x y : ℝ} (hx : 0≤x) (hxy : x≤y) : logTwo x ≤ logTwo y :=
  div_le_div_of_nonneg_right (Real.log_le_log (by linarith) (by linarith)) (Real.log_pos (by norm_num)).le

private lemma phi_nonneg {x : ℝ} (hx : 0≤x) : 0≤phi x :=
  Real.rpow_nonneg (mul_nonneg (sq_nonneg x) (logTwo_nonneg hx)) _

private lemma phi_cube {x : ℝ} (hx : 0≤x) : (phi x)^3 = x^2*logTwo x := by
  unfold phi
  have hn := mul_nonneg (sq_nonneg x) (logTwo_nonneg hx)
  rw [← Real.rpow_natCast, ← Real.rpow_mul hn]
  norm_num

/-- Rounded child widths decremented by y/2 lose at least one third of the local
square-root/log charge in the *actual* base-two cube-root potential. -/
theorem numerical_decrement {x xp y : ℝ} (hx : 0<x) (hxp : 0≤xp) (hy : 0≤y)
    (hyx : y≤x) (hstep : xp≤x-y/2) (harity : phi x≤y) :
    psi y/3 ≤ phi x-phi xp := by
  have hx0 := hx.le
  have hp := phi_nonneg hx0
  have hpp := phi_nonneg hxp
  have hL := logTwo_nonneg hx0
  have hs := Real.sqrt_nonneg (y*logTwo y)
  have hmid : 0 ≤ x-y/2 := by linarith
  have hsub : xp^2*logTwo xp ≤ (x-y/2)^2*logTwo x :=
    mul_le_mul (pow_le_pow_left₀ hxp hstep 2) (logTwo_mono hxp (by linarith))
      (logTwo_nonneg hxp) (sq_nonneg _)
  have hpoly : (3*x)^3*(x-y/2)^2 ≤ (3*x-y)^3*x^2 := by
    have hlast : 0≤9*x/4-y := by linarith
    have hprod := mul_nonneg (mul_nonneg (sq_nonneg x) (sq_nonneg y)) hlast
    nlinarith only [hprod]
  have hcube : (3*x*phi xp)^3 ≤ ((3*x-y)*phi x)^3 := calc
    _ = (3*x)^3*(xp^2*logTwo xp) := by rw [mul_pow,phi_cube hxp]
    _ ≤ (3*x)^3*((x-y/2)^2*logTwo x) := mul_le_mul_of_nonneg_left hsub (by positivity)
    _ = ((3*x)^3*(x-y/2)^2)*logTwo x := by ring
    _ ≤ ((3*x-y)^3*x^2)*logTwo x := mul_le_mul_of_nonneg_right hpoly hL
    _ = _ := by rw [mul_pow,phi_cube hx0]; ring
  have hcoeff : 0≤3*x-y := by linarith
  have hdec := (pow_le_pow_iff_left₀ (mul_nonneg (by positivity) hpp)
    (mul_nonneg hcoeff hp) (by decide : (3:ℕ)≠0)).mp hcube
  have hsqs : (x*psi y)^2 ≤ (y*phi x)^2 := calc
    _ = x^2*y*logTwo y := by
      rw [psi,mul_pow,Real.sq_sqrt (mul_nonneg hy (logTwo_nonneg hy))]
      ring
    _ ≤ x^2*y*logTwo x := mul_le_mul_of_nonneg_left (logTwo_mono hy hyx)
      (mul_nonneg (sq_nonneg _) hy)
    _ = y*(phi x)^3 := by rw [phi_cube hx0]; ring
    _ ≤ y*(y*(phi x)^2) := by
      apply mul_le_mul_of_nonneg_left _ hy
      rw [show (phi x)^3=phi x*(phi x)^2 by ring]
      exact mul_le_mul_of_nonneg_right harity (sq_nonneg _)
    _ = _ := by ring
  have hps := (pow_le_pow_iff_left₀ (mul_nonneg hx0 hs)
    (mul_nonneg hy hp) (by decide : (2:ℕ)≠0)).mp hsqs
  change x*psi y ≤ y*phi x at hps
  have hfinal : x*psi y ≤ x*(3*(phi x-phi xp)) := by nlinarith only [hdec,hps]
  have := le_of_mul_le_mul_left hfinal hx
  linarith

/-- Full multiplicity up to 2^(10ψ), including the normalized square-root volume,
spends at most one quarter of the parent's clock at coefficient 36. -/
theorem quarter_clock {x xp y B M : ℝ} (hx : 0<x) (hxp : 0≤xp) (hy : 0≤y)
    (hyx : y≤x) (hstep : xp≤x-y/2) (harity : phi x≤y) (hpsi : 1≤psi y)
    (hB : 36≤B) (hM : M≤(2:ℝ)^(10*psi y)) :
    M*(2:ℝ)^(B*phi xp) ≤ (1/4)*(2:ℝ)^(B*phi x) := by
  have hd := numerical_decrement hx hxp hy hyx hstep harity
  have hpos : 0≤phi x-phi xp := by linarith
  have hm := mul_le_mul_of_nonneg_right hB hpos
  calc
    _ ≤ (2:ℝ)^(10*psi y)*(2:ℝ)^(B*phi xp) :=
      mul_le_mul_of_nonneg_right hM (Real.rpow_nonneg (by norm_num) _)
    _ = (2:ℝ)^(10*psi y+B*phi xp) := (Real.rpow_add (by norm_num) _ _).symm
    _ ≤ (2:ℝ)^(B*phi x-2) := Real.rpow_le_rpow_of_exponent_le (by norm_num)
      (by nlinarith only [hd,hm,hpsi])
    _ = _ := by rw [Real.rpow_sub (by norm_num)]; norm_num; ring

end Moonshot.AlignedWalsh.Clock

#print axioms Moonshot.AlignedWalsh.Clock.numerical_decrement
#print axioms Moonshot.AlignedWalsh.Clock.quarter_clock
