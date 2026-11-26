import Mathlib.RingTheory.AdjoinRoot
import Mathlib.Tactic.Ring
import Mathlib.Tactic.LinearCombination

/-! Mixed-radix Fourier entries and the exact cyclotomic tower over a commutative ring. -/
open Polynomial
open scoped Polynomial BigOperators
namespace Moonshot.MacroTriadic

variable {R : Type*} [CommRing R]

/-- For `m = 3t` a positive power of three this is the defining polynomial of `S_m`. -/
noncomputable def tri (R : Type*) [CommRing R] (t : ℕ) : R[X] := X ^ (2*t) + X^t + 1

theorem tri_comp (t h : ℕ) :
    (tri R t).comp (X^h) = tri R (h*t) := by
  simp [tri, ← pow_mul, Nat.mul_left_comm, Nat.mul_comm, Nat.mul_assoc]

/-- The large cyclotomic algebra is the actual iterated quotient, at every coefficient precision. -/
noncomputable def restrictionEquiv (t h : ℕ) :
    AdjoinRoot (tri R (h*t)) ≃ₐ[R]
      AdjoinRoot ((X : (AdjoinRoot (tri R t))[X])^h - C (AdjoinRoot.root (tri R t))) := by
  let e := (AdjoinRoot.algEquivOfEq R _ _ (tri_comp (R := R) t h).symm).trans
    (AdjoinRoot.compAlgEquiv (tri R t) (X^h))
  exact e.trans (AdjoinRoot.algEquivOfEq R _ _ (by rw [Polynomial.map_pow, Polynomial.map_X]))

/-- Canonical coordinates in the tower comprise h arbitrary small-ring coefficients. -/
noncomputable def laneBasis (S : Type*) [CommRing S] [Nontrivial S] (w : S) (h : ℕ) (hh : 0 < h) :
    Module.Basis (Fin h) S (AdjoinRoot ((X : S[X])^h-C w)) :=
  (AdjoinRoot.powerBasisAux' (Polynomial.monic_X_pow_sub_C w hh.ne')).reindex
    (finCongr Polynomial.natDegree_X_pow_sub_C)

/-- A length-AB cyclic transform has two child Fourier kernels and its actual middle twiddle. -/
theorem cooley_tukey_entry (ρ : R) (A B j₀ j₁ k₀ k₁ : ℕ) (period : ρ^(A*B) = 1) :
    ρ^((j₀+A*j₁)*(k₁+B*k₀)) =
      (ρ^A)^(j₁*k₁) * ρ^(j₀*k₁) * (ρ^B)^(j₀*k₀) := by
  have e : (j₀+A*j₁)*(k₁+B*k₀) = A*(j₁*k₁)+j₀*k₁+B*(j₀*k₀)+(A*B)*(j₁*k₀) := by ring
  rw [e, pow_add, pow_add, pow_add, pow_mul ρ A (j₁*k₁), pow_mul ρ B (j₀*k₀), pow_mul ρ (A*B) (j₁*k₀), period, one_pow, mul_one]

/-- Every child Fourier coefficient is the sum of separately transformed scalar-module lanes. -/
theorem separated_lanes {L h : ℕ} (Y : R) (weight : Fin L → R) (a : Fin L → Fin h → R) :
    (∑ j, weight j * (∑ u : Fin h, Y^(u : ℕ) * a j u)) =
      ∑ u : Fin h, Y^(u : ℕ) * (∑ j, weight j * a j u) := by
  simp_rw [Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro u _
  apply Finset.sum_congr rfl
  intro j _
  ring

/-- The odd cyclic chirp identity holds for either sign and any group unit, including over Z/2^H. -/
theorem odd_chirp {G : Type*} [CommGroup G] (w : G) (i j s L z ε : ℤ)
    (hs : 2*s = 1+L*z) (period : w^L = 1) :
    w^(ε*s*i^2) * w^(ε*s*j^2) * w^(-ε*s*(i-j)^2) = w^(ε*i*j) := by
  rw [← zpow_add, ← zpow_add]
  have ex : ε*s*i^2 + ε*s*j^2 + -ε*s*(i-j)^2 = ε*i*j + L*(z*ε*i*j) := by
    linear_combination (ε*i*j) * hs
  rw [ex, zpow_add, zpow_mul w L (z*ε*i*j), period, one_zpow, mul_one]

/-- The second (twisted) cyclic product recovers the true high outer coefficient. -/
theorem twisted_high (w inv3 low high : R) (hw : w^2 + w + 1 = 0) (h3 : 3*inv3 = 1) :
    ((low+w*high)-(low+high))*(w^2-1)*inv3 = high := by
  have factor : (w-1)*(w^2-1) = 3 := by linear_combination (w-2)*hw
  calc
    _ = high*((w-1)*(w^2-1))*inv3 := by ring
    _ = high := by rw [factor, mul_assoc, h3, mul_one]

end Moonshot.MacroTriadic

#print axioms Moonshot.MacroTriadic.tri_comp
#print axioms Moonshot.MacroTriadic.restrictionEquiv
#print axioms Moonshot.MacroTriadic.laneBasis
#print axioms Moonshot.MacroTriadic.cooley_tukey_entry
#print axioms Moonshot.MacroTriadic.separated_lanes
#print axioms Moonshot.MacroTriadic.odd_chirp
#print axioms Moonshot.MacroTriadic.twisted_high
