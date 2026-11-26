import Mathlib.Algebra.CharP.Two
import Mathlib.Algebra.Polynomial.Expand
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.NormNum

/-! The same-precision ordinary polynomial product carry from three divided squares. -/
namespace Moonshot.DividedSquareProduct

/-- In the intended polynomial ring, φ is the endomorphism replacing the variable by
its square. The three divided squares in these premises have integer coefficients. -/
theorem exact_expansion {R : Type*} [CommRing R] [IsDomain R] [CharZero R]
    (φ : R →+* R) (f g h k qf qg qh : R)
    (hf : f^2 = φ f + 2*qf) (hg : g^2 = φ g + 2*qg)
    (hh : h^2 = φ h + 2*qh) (hk : f*g = h+2*k) :
    φ k + φ f * qg + φ g * qf + 2*qf*qg = qh + 2*h*k + 2*k^2 := by
  apply mul_left_cancel₀ (show (2 : R) ≠ 0 by norm_num)
  have hφ := congrArg φ hk
  simp only [map_mul, map_add, map_ofNat] at hφ
  calc
    2 * (φ k + φ f * qg + φ g * qf + 2*qf*qg)
      = (φ f+2*qf)*(φ g+2*qg)-φ h := by linear_combination -hφ
    _ = (f*g)^2-φ h := by rw [← hf, ← hg]; ring
    _ = (h+2*k)^2-φ h := by rw [hk]
    _ = 2*(qh+2*h*k+2*k^2) := by linear_combination hh

/-- The binary reduction computes the second digit of each product coefficient. -/
theorem binary_carry {R S : Type*} [CommRing R] [IsDomain R] [CharZero R]
    [CommRing S] [CharP S 2] (φ : R →+* R) (red : R →+* S)
    (f g h k qf qg qh : R)
    (hf : f^2 = φ f + 2*qf) (hg : g^2 = φ g + 2*qg)
    (hh : h^2 = φ h + 2*qh) (hk : f*g = h+2*k) :
    red (φ k) = red qh + red (φ f) * red qg + red (φ g) * red qf := by
  have h := congrArg red (exact_expansion φ f g h k qf qg qh hf hg hh hk)
  simp only [map_add, map_mul, map_pow, map_ofNat, CharTwo.two_eq_zero,
    zero_mul, add_zero] at h
  calc
    red (φ k) = red (φ k) + (red (φ f)*red qg + red (φ g)*red qf +
        (red (φ f)*red qg + red (φ g)*red qf)) := by rw [CharTwo.add_self_eq_zero, add_zero]
    _ = red qh + red (φ f) * red qg + red (φ g) * red qf := by rw [← h]; ring

open Polynomial

noncomputable def parity : ℤ[X] →+* (ZMod 2)[X] :=
  Polynomial.mapRingHom (Int.castRingHom (ZMod 2))

/-- Every integral polynomial has an integral divided square relative to X ↦ X². -/
theorem exists_divided_square (f : ℤ[X]) :
    ∃ q : ℤ[X], f^2 = Polynomial.expand ℤ 2 f + 2*q := by
  have hfrob : frobenius (ZMod 2) 2 = RingHom.id (ZMod 2) := by
    ext x
    fin_cases x <;> decide
  have hzero : parity (f^2 - Polynomial.expand ℤ 2 f) = 0 := by
    rw [map_sub, map_pow, sub_eq_zero]
    change (Polynomial.map (Int.castRingHom (ZMod 2)) f)^2 = _
    rw [← Polynomial.map_frobenius_expand, hfrob, Polynomial.map_id]
    exact Polynomial.map_expand.symm
  have dvd : Polynomial.C (2:ℤ) ∣ f^2 - Polynomial.expand ℤ 2 f := by
    apply (Polynomial.C_dvd_iff_dvd_coeff _ _).mpr
    intro i
    apply (ZMod.intCast_zmod_eq_zero_iff_dvd _ 2).mp
    have v := congrArg (fun p:(ZMod 2)[X] => p.coeff i) hzero
    change (Polynomial.map (Int.castRingHom (ZMod 2)) (f^2 - Polynomial.expand ℤ 2 f)).coeff i = (0:(ZMod 2)[X]).coeff i at v
    rw [Polynomial.coeff_map, Polynomial.coeff_zero] at v
    exact v
  obtain ⟨q,hq⟩ := dvd
  refine ⟨q,?_⟩
  have hq' : f^2 - Polynomial.expand ℤ 2 f = 2*q := by simpa using hq
  linear_combination hq'

/-- Even entries of the three-square formula return the high product digit; all odd
entries vanish. The premises encode the ordinary integer polynomial lifts. -/
theorem coefficient_recovery (f g h k qf qg qh : ℤ[X])
    (hf : f^2 = Polynomial.expand ℤ 2 f + 2*qf)
    (hg : g^2 = Polynomial.expand ℤ 2 g + 2*qg)
    (hh : h^2 = Polynomial.expand ℤ 2 h + 2*qh)
    (hk : f*g=h+2*k) (i : ℕ) :
    let out := parity qh + parity (Polynomial.expand ℤ 2 f)*parity qg +
      parity (Polynomial.expand ℤ 2 g)*parity qf
    out.coeff (2*i) = (k.coeff i : ZMod 2) ∧ out.coeff (2*i+1)=0 := by
  dsimp only
  have he := binary_carry (Polynomial.expand ℤ 2).toRingHom parity f g h k qf qg qh hf hg hh hk
  change parity (Polynomial.expand ℤ 2 k) = parity qh + parity (Polynomial.expand ℤ 2 f)*parity qg + parity (Polynomial.expand ℤ 2 g)*parity qf at he
  rw [← he]
  have hodd : ¬2 ∣ 2*i+1 := by omega
  simp [parity, Polynomial.coeff_map, Polynomial.coeff_expand (by decide : 0<2), hodd]

theorem coefficient_half (u r k : ℤ[X]) (hk : u = r+2*k) (i : ℕ)
    (hl : 0 ≤ r.coeff i) (hu : r.coeff i < 2) :
    k.coeff i = u.coeff i / 2 := by
  have h := congrArg (fun p : ℤ[X] => p.coeff i) hk
  change u.coeff i = (r+2*k).coeff i at h
  have two : (2 : ℤ[X]) = C (2:ℤ) := by norm_num
  rw [two, coeff_add, coeff_C_mul] at h
  omega

theorem binary_input_square_high (f q : ℤ[X])
    (hf : f^2 = Polynomial.expand ℤ 2 f + 2*q)
    (bits : ∀ j, 0 ≤ f.coeff j ∧ f.coeff j < 2) (i : ℕ) :
    q.coeff i = (f^2).coeff i / 2 := by
  apply coefficient_half (f^2) (Polynomial.expand ℤ 2 f) q hf
  · rw [Polynomial.coeff_expand (by decide : 0 < 2)]
    split
    · exact (bits _).1
    · rfl
  · rw [Polynomial.coeff_expand (by decide : 0 < 2)]
    split
    · exact (bits _).2
    · decide

end Moonshot.DividedSquareProduct

#print axioms Moonshot.DividedSquareProduct.exact_expansion
#print axioms Moonshot.DividedSquareProduct.binary_carry
#print axioms Moonshot.DividedSquareProduct.exists_divided_square
#print axioms Moonshot.DividedSquareProduct.coefficient_recovery
#print axioms Moonshot.DividedSquareProduct.coefficient_half
#print axioms Moonshot.DividedSquareProduct.binary_input_square_high
