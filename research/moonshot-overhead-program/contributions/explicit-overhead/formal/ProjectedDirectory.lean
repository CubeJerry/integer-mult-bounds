import Mathlib.FieldTheory.Finite.Basic
import Mathlib.FieldTheory.Minpoly.Field
import Mathlib.Algebra.Polynomial.AlgebraMap
import Mathlib.Algebra.Polynomial.Degree.Domain
import Mathlib.Algebra.Polynomial.Monic
import Mathlib.RingTheory.Coprime.Basic
import Mathlib.Tactic.Ring

/-! Two exact algebraic decisions in the finite-field point/directory adapter:
which projected recurrence detects a genuine annihilator, and which two
Euclidean cofactors give the reduced rational function at the first cutoff. -/

open Polynomial
open scoped Polynomial
namespace Moonshot.ProjectedDirectory

section Functional
variable {F K : Type*} [Field F] [Field K] [Algebra F K]

/-- Vanishing on the powers of `z` implies vanishing on any polynomial in `z`. -/
theorem annihilate_polynomial_combinations (L : K →ₗ[F] F) (z w : K)
    (h : ∀ n : ℕ, L (z ^ n * w) = 0) (q : F[X]) :
    L (aeval z q * w) = 0 := by
  refine q.induction_on' (fun p q hp hq => ?_) fun n a => ?_
  · rw [map_add, add_mul, map_add, hp, hq, add_zero]
  · rw [aeval_monomial, mul_assoc, ← Algebra.smul_def a (z ^ n * w), map_smul, h n, smul_zero]

/-- A single deterministic functional nonzero at one detects the true recurrence
on every generated subfield, regardless of the degree of `z`. -/
theorem projected_annihilator_iff [Fintype K] (L : K →ₗ[F] F) (z : K)
    (h1 : L 1 ≠ 0) (p : F[X]) :
    (∀ n : ℕ, L (z ^ n * aeval z p) = 0) ↔ aeval z p = 0 := by
  constructor
  · intro h
    by_contra hz
    have c : 1 < Fintype.card K := Fintype.one_lt_card
    have ex : Fintype.card K - 2 + 1 = Fintype.card K - 1 := by omega
    have hp := annihilate_polynomial_combinations L z (aeval z p) h (p ^ (Fintype.card K - 2))
    rw [map_pow, ← pow_succ, ex, FiniteField.pow_card_sub_one_eq_one _ hz] at hp
    exact h1 hp
  · intro h n
    simp [h]

/-- Multiplying a point value by a polynomial realizes the corresponding
linear combination of future scalar moments. -/
theorem moment_shift_formula (L : K →ₗ[F] F) (z : K) (p : F[X]) (n : ℕ) :
    L (z ^ n * aeval z p) =
      ∑ i ∈ Finset.range (p.natDegree + 1), p.coeff i * L (z ^ (n+i)) := by
  rw [aeval_eq_sum_range, Finset.mul_sum, map_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [mul_smul_comm, map_smul, smul_eq_mul, ← pow_add]

/-- The explicitly shifted scalar sequence has exactly the multiples of the
intrinsic minimal polynomial as its recurrence polynomials. -/
theorem moment_recurrence_iff_minpoly_dvd [Fintype K] (L : K →ₗ[F] F) (z : K)
    (h1 : L 1 ≠ 0) (p : F[X]) :
    (∀ n : ℕ, ∑ i ∈ Finset.range (p.natDegree + 1), p.coeff i * L (z ^ (n+i)) = 0) ↔
      minpoly F z ∣ p := by
  simp_rw [← moment_shift_formula L z p]
  exact (projected_annihilator_iff L z h1 p).trans minpoly.dvd_iff.symm

/-- A window as long as a monic modulus distinguishes all legal subfield
values. Only the first `M.natDegree` moment equations are assumed. -/
theorem finite_projected_window [Fintype K] (L : K →ₗ[F] F) (z : K) (M p : F[X])
    (h1 : L 1 ≠ 0) (hM : M.Monic) (rootM : aeval z M = 0)
    (h : ∀ n : ℕ, n < M.natDegree → L (z ^ n * aeval z p) = 0) : aeval z p = 0 := by
  by_contra hp
  have Mne : M ≠ 1 := by
    intro heq
    rw [heq, map_one] at rootM
    exact one_ne_zero rootM
  have c : 1 < Fintype.card K := Fintype.one_lt_card
  have ex : Fintype.card K - 2 + 1 = Fintype.card K - 1 := by omega
  let q : F[X] := p ^ (Fintype.card K - 2)
  have cutoff := natDegree_modByMonic_lt q hM Mne
  have hpair : L (aeval z (q %ₘ M) * aeval z p) = 0 := by
    rw [aeval_eq_sum_range' cutoff, Finset.sum_mul, map_sum]
    apply Finset.sum_eq_zero
    intro i hi
    rw [smul_mul_assoc, map_smul, h i (Finset.mem_range.mp hi), smul_zero]
  rw [aeval_modByMonic_eq_self_of_root rootM] at hpair
  dsimp [q] at hpair
  rw [map_pow, ← pow_succ, ex, FiniteField.pow_card_sub_one_eq_one _ hp] at hpair
  exact h1 hpair
end Functional

section Pade
variable {F : Type*} [Field F]

/-- The small-remainder row of the Euclidean algorithm on a descending
moment encoding returns the denominator and numerator in its two *cofactors*.
The statement includes a zero `R`; the polynomial bounds hold at a strict
midpoint cutoff and `M,V` have their standard monic normalization. -/
theorem descending_cutoff_cofactors (b : ℕ) (G A M U V R E : F[X])
    (hR : R = V * G - U * X ^ (2*b)) (hE : E = M * G - A * X ^ (2*b))
    (hA : IsCoprime A M) (hU : IsCoprime U V) (hM : M.Monic) (hV : V.Monic)
    (degreeM : M.natDegree ≤ b) (degreeV : V.natDegree ≤ b)
    (smallR : R.natDegree < b) (smallE : E.natDegree < b) : V = M ∧ U = A := by
  have hcross : M * R - V * E = X ^ (2*b) * (V*A-M*U) := by rw [hR,hE]; ring
  have hdiv : (X : F[X]) ^ (2*b) ∣ M * R - V * E := ⟨_, hcross⟩
  have hsmall : (M * R - V * E).natDegree < 2*b := by
    refine lt_of_le_of_lt (natDegree_sub_le _ _) (max_lt ?_ ?_)
    · exact lt_of_le_of_lt (natDegree_mul_le) (by omega)
    · exact lt_of_le_of_lt (natDegree_mul_le) (by omega)
  have hzero : M * R - V * E = 0 := eq_zero_of_dvd_of_natDegree_lt hdiv (by simpa using hsmall)
  rw [hcross, mul_eq_zero] at hzero
  have hx : ((X : F[X]) ^ (2*b)) ≠ 0 := pow_ne_zero _ X_ne_zero
  have hm : V * A = M * U := sub_eq_zero.mp (hzero.resolve_left hx)
  have hmV : M ∣ V := hA.symm.dvd_of_dvd_mul_right ⟨U, hm⟩
  have hvM : V ∣ M := hU.symm.dvd_of_dvd_mul_right ⟨A, hm.symm⟩
  have eqV : V = M := eq_of_monic_of_associated hV hM (associated_of_dvd_dvd hvM hmV)
  refine ⟨eqV, ?_⟩
  rw [eqV] at hm
  exact (mul_left_cancel₀ hM.ne_zero hm).symm
end Pade

end Moonshot.ProjectedDirectory
#print axioms Moonshot.ProjectedDirectory.annihilate_polynomial_combinations
#print axioms Moonshot.ProjectedDirectory.projected_annihilator_iff
#print axioms Moonshot.ProjectedDirectory.moment_shift_formula
#print axioms Moonshot.ProjectedDirectory.moment_recurrence_iff_minpoly_dvd
#print axioms Moonshot.ProjectedDirectory.finite_projected_window
#print axioms Moonshot.ProjectedDirectory.descending_cutoff_cofactors
