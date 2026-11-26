import Mathlib.Algebra.Polynomial.Taylor
import Mathlib.Algebra.Polynomial.Div
import Mathlib.Algebra.CharP.Two
import Mathlib.Tactic.Ring

/-!
# Relative-trace shears and the one-row carry

The inner polynomial variable is the ordinary coefficient index. The outer
variable is the row index. Actual low and high rows come from monic division
of each inner coefficient by the fixed power of the inner variable.
-/
namespace Moonshot.TraceShearRadix
open Polynomial
open scoped Polynomial

variable {F : Type*} [Field F]

/-- Combine the two strip shears in the actual degree-a relative trace. -/
theorem two_shifts (a : ℕ) (p : (F[X])[X]) :
    taylor (X^a : F[X]) (taylor X p) = taylor (X^a + X) p :=
  taylor_taylor p _ _

/-- Extract every actual low half. -/
noncomputable def lowRows (h : ℕ) (s : (F[X])[X]) : (F[X])[X] :=
  s.sum fun j p => monomial j (p %ₘ X^h)

/-- Extract every actual high half. -/
noncomputable def highRows (h : ℕ) (s : (F[X])[X]) : (F[X])[X] :=
  s.sum fun j p => monomial j (p /ₘ X^h)

theorem row_split (h : ℕ) (s : (F[X])[X]) :
    lowRows h s + C (X^h : F[X])*highRows h s = s := by
  classical
  unfold lowRows highRows Polynomial.sum
  rw [Finset.mul_sum, ← Finset.sum_add_distrib]
  conv_rhs => rw [← sum_monomial_eq s]
  apply Finset.sum_congr rfl
  intro j _
  change (monomial j) (s.coeff j %ₘ X ^ h) + C (X^h) * monomial j (s.coeff j /ₘ X^h) = monomial j (s.coeff j)
  rw [C_mul_monomial, ← map_add]
  exact congrArg (monomial j) (modByMonic_add_div _ _)

variable [CharP F 2]

/-- The forward normalizer returns exactly the original polynomial when
evaluated in its trace radix. The high row is used at its own index and as
the carry to the next index. -/
theorem forward_trace (h a : ℕ) (p : (F[X])[X]) :
    let u := (X^a + X : F[X])
    let t := (X^h : F[X]) + u
    let s := taylor u p
    (lowRows h s + C u * highRows h s + X * highRows h s).eval t =
      p.eval (X^h) := by
  dsimp only
  let u := (X^a + X : F[X])
  let v := (X^h : F[X])
  let s := taylor u p
  change (lowRows h s + C u * highRows h s + X * highRows h s).eval (v+u) = p.eval v
  have cancel : v+u+u = v := by rw [add_assoc, CharTwo.add_self_eq_zero, add_zero]
  calc
    _ = (lowRows h s + C v * highRows h s).eval (v+u) := by
      simp only [eval_add, eval_mul, eval_C, eval_X, add_mul]
      have hc (x y z : F[X]) : x + y + (z + y) = x + z := calc
        _ = (x+z)+(y+y) := by ac_rfl
        _ = _ := by rw [CharTwo.add_self_eq_zero, add_zero]
      exact hc _ _ _
    _ = s.eval (v+u) := by rw [show lowRows h s + C v * highRows h s = s from row_split h s]
    _ = _ := by simp only [s, taylor_eval, cancel]

omit [CharP F 2] in
/-- On arbitrary incoming trace digits, synthesis in ordinary coefficient
blocks requires only the carry from the previous high half. -/
theorem reverse_trace (h a : ℕ) (p : (F[X])[X]) :
    let u := (X^a + X : F[X])
    let s := taylor u p
    (lowRows h s + X * highRows h s).eval (X^h : F[X]) =
      p.eval ((X^h : F[X])+u) := by
  dsimp only
  let v := (X^h : F[X])
  let s := taylor (X^a + X : F[X]) p
  change (lowRows h s + X * highRows h s).eval v = _
  calc
    _ = (lowRows h s + C v * highRows h s).eval v := by simp only [eval_add, eval_mul, eval_X, eval_C]
    _ = s.eval v := by rw [show lowRows h s + C v * highRows h s = s from row_split h s]
    _ = _ := taylor_eval _ _ _

#print axioms two_shifts
#print axioms row_split
#print axioms forward_trace
#print axioms reverse_trace
end Moonshot.TraceShearRadix
