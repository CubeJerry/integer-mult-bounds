import Mathlib.Algebra.Polynomial.Div
import Mathlib.Algebra.Polynomial.Degree.Lemmas

/-! Ordinary quotient and remainder on products of the trace-bundle factors. -/
open Polynomial
open scoped Polynomial BigOperators
namespace Moonshot.GroupedComposition
variable {K : Type*} [Field K]

noncomputable def grouped (S : K[X]) (g : ℕ → K[X]) : K[X] :=
  ∑ k ∈ Finset.range S.natDegree, X ^ k * (g k).comp S

theorem actual_grouped_division (m S : K[X]) (hm : m.Monic) (hS : S.Monic)
    (hmpos : 0 < m.natDegree) (hv : 0 < S.natDegree) (g : ℕ → K[X]) :
    grouped S g /ₘ (m.comp S) = grouped S (fun k => g k /ₘ m) ∧
    grouped S g %ₘ (m.comp S) = grouped S (fun k => g k %ₘ m) := by
  classical
  have hmon := hm.comp hS (Nat.ne_of_gt hv)
  have hm1 : m ≠ 1 := by
    rintro rfl
    simp at hmpos
  apply div_modByMonic_unique _ _ hmon
  constructor
  · unfold grouped
    rw [Finset.mul_sum, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro k _
    have he := congrArg (fun p : K[X] => p.comp S) (modByMonic_add_div (g k) m)
    simp only [add_comp, mul_comp] at he
    calc
      _ = X ^ k * (((g k %ₘ m).comp S) + (m.comp S) * ((g k /ₘ m).comp S)) := by ring
      _ = _ := by rw [he]
  · have hbot : ⊥ < (m.comp S).degree := by
      rw [degree_eq_natDegree hmon.ne_zero]
      exact WithBot.bot_lt_coe _
    unfold grouped
    refine (degree_sum_le _ _).trans_lt ((Finset.sup_lt_iff hbot).2 ?_)
    intro k hk
    apply degree_lt_degree
    have hc := natDegree_modByMonic_lt (g k) hm hm1
    have hki := Finset.mem_range.mp hk
    calc
      _ ≤ (X ^ k : K[X]).natDegree + ((g k %ₘ m).comp S).natDegree := natDegree_mul_le
      _ = k + (g k %ₘ m).natDegree * S.natDegree := by rw [natDegree_X_pow, natDegree_comp]
      _ < S.natDegree + (g k %ₘ m).natDegree * S.natDegree := Nat.add_lt_add_right hki _
      _ = ((g k %ₘ m).natDegree + 1) * S.natDegree := by
        rw [Nat.add_mul, Nat.one_mul, Nat.add_comm S.natDegree]
      _ ≤ m.natDegree * S.natDegree := Nat.mul_le_mul_right _ (Nat.succ_le_of_lt hc)
      _ = _ := natDegree_comp.symm

#print axioms Moonshot.GroupedComposition.actual_grouped_division
end Moonshot.GroupedComposition
