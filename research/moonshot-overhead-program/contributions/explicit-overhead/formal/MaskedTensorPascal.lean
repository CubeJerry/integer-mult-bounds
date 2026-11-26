import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.CharP.Two
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Ring

/-! Exact five-letter realization of an arbitrary mask of binary shear gates.
The tensor row and column indices are actual bit strings. -/
namespace Moonshot.MaskedTensorPascal
open Matrix
open scoped BigOperators

variable {K : Type*} [Field K]
abbrev Two (K : Type*) := Matrix (Fin 2) (Fin 2) K
abbrev Bits (g : ℕ) := Fin g → Fin 2

def shear (z : K) : Two K := !![1,z; 0,1]
def phase (s : K) : Two K := !![s,0; 0,1]

theorem pair_phase (s t : K) (hs : s ≠ 0) (ht : t ≠ 0) :
    phase s * shear 1 * phase (s⁻¹*t) * shear 1 * phase t⁻¹ = shear (s+t) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [phase, shear, Matrix.mul_apply, Fin.sum_univ_two, hs, ht]
  ring

/-- Coordinate definition of a Kronecker product on indexed bit strings. -/
noncomputable def tensor {g : ℕ} (f : Fin g → Two K) : Matrix (Bits g) (Bits g) K :=
  Matrix.of fun r c => ∏ i, f i (r i) (c i)

theorem tensor_mul {g : ℕ} (f k : Fin g → Two K) :
    tensor f * tensor k = tensor (fun i => f i * k i) := by
  classical
  ext r c
  simp only [tensor, Matrix.mul_apply, Matrix.of_apply]
  rw [Fintype.prod_sum]
  apply Finset.sum_congr rfl
  intro u _
  rw [Finset.prod_mul_distrib]

noncomputable def first (w z : K) : K := by classical exact if z=0 then 1 else w*z
noncomputable def second (w z : K) : K := by classical exact if z=0 then 1 else w^2*z

variable [CharP K 2]

theorem choose_phases (w : K) (hw : w ^ 2 + w = 1) (z : K) :
    first w z ≠ 0 ∧ second w z ≠ 0 ∧ first w z + second w z = z := by
  have hn : w ≠ 0 := by
    rintro rfl
    simp at hw
  by_cases hz : z = 0
  · simp [hz, first, second, CharTwo.add_self_eq_zero]
  · have he : w + w^2 = 1 := by simpa [add_comm] using hw
    simp [first, second, hz, hn, ← add_mul, he]

/-- Every spectator sector, arbitrary rank and arbitrary local coefficients.
The middle and outer diagonal letters are explicit functions of these coefficients. -/
theorem masked_tensor {g : ℕ} (w : K) (hw : w^2+w=1) (z : Fin g → K) :
    tensor (fun i => phase (first w (z i))) * tensor (fun _ : Fin g => shear 1) *
    tensor (fun i => phase ((first w (z i))⁻¹ * second w (z i))) *
    tensor (fun _ : Fin g => shear 1) * tensor (fun i => phase (second w (z i))⁻¹) =
    tensor (fun i => shear (z i)) := by
  simp only [tensor_mul]
  apply congrArg tensor
  funext i
  obtain ⟨hs, ht, he⟩ := choose_phases w hw (z i)
  exact (pair_phase _ _ hs ht).trans (congrArg shear he)

#print axioms pair_phase
#print axioms tensor_mul
#print axioms choose_phases
#print axioms masked_tensor
end Moonshot.MaskedTensorPascal
