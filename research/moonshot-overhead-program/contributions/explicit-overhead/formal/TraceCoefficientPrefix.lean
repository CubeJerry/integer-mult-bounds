import Mathlib.Algebra.CharP.Two
import Mathlib.Algebra.CharP.Lemmas
import Mathlib.Algebra.Polynomial.Div
import Mathlib.Algebra.Polynomial.AlgebraMap
import Mathlib.Tactic.LinearCombination

/-!
# One-correction division on the binary coefficient stream

If a monic divisor has its next term at degree at most half its leading
degree, division of a two-word input needs only one high-half correction.
The result below identifies both output words with Mathlib's ordinary
polynomial quotient and remainder. The proof uses polynomial degree only.
-/
namespace Moonshot.CoefficientPrefix
open Polynomial
open scoped Polynomial

universe u
variable {F : Type u} [Field F]

/-- High-half projection. For the sparse trace divisor, this is at most five
shifted scans of the source word. -/
noncomputable def feedback (h : ℕ) (e b : F[X]) := (e*b) /ₘ X^h

private theorem feedback_degree {h : ℕ} (hh : 2 ≤ h) {e b : F[X]}
    (he : e.natDegree ≤ h / 2) (hb : b.natDegree < h) :
    (feedback h e b).natDegree < h / 2 := by
  have product_bound := natDegree_mul_le (p := e) (q := b)
  rw [feedback, natDegree_divByMonic _ (monic_X_pow h), natDegree_X_pow]
  omega

/-- The high-half correction squares to zero on every word below the cut. -/
theorem feedback_square_zero {h : ℕ} (hh : 2 ≤ h) {e b : F[X]}
    (he : e.natDegree ≤ h / 2) (hb : b.natDegree < h) :
    feedback h e (feedback h e b) = 0 := by
  apply (divByMonic_eq_zero_iff (monic_X_pow h)).mpr
  apply degree_lt_degree
  rw [natDegree_X_pow]
  have hc := feedback_degree hh he hb
  have hp := natDegree_mul_le (p := e) (q := feedback h e b)
  omega

/-- A remainder below degree h and the quotient are obtained using the high
part of e*b and a second low product. This version holds in all fields. -/
theorem truncated_quotient_remainder {h : ℕ} (hh : 2 ≤ h) (a b e : F[X])
    (ha : a.natDegree < h) (hb : b.natDegree < h) (he : e.natDegree ≤ h / 2) :
    let c := feedback h e b
    let q := b - c
    let r := a - ((e*b) %ₘ X^h) + e*c
    (a + X^h*b) /ₘ (X^h+e) = q ∧ (a + X^h*b) %ₘ (X^h+e) = r := by
  dsimp only
  have heh : e.degree < (X^h : F[X]).degree := by
    apply degree_lt_degree
    rw [natDegree_X_pow]
    omega
  have mon := (monic_X_pow (R := F) h).add_of_left heh
  have hC := feedback_degree hh he hb
  have ecN := natDegree_mul_le (p := e) (q := feedback h e b)
  have ecD : (e * feedback h e b).degree < (X^h : F[X]).degree := by
    apply degree_lt_degree
    rw [natDegree_X_pow]
    omega
  have aD : a.degree < (X^h : F[X]).degree := by
    apply degree_lt_degree
    simpa only [natDegree_X_pow] using ha
  have remD := degree_modByMonic_lt (e*b) (monic_X_pow (R := F) h)
  apply div_modByMonic_unique _ _ mon
  constructor
  · unfold feedback
    linear_combination -(modByMonic_add_div (e*b) (X^h))
  · rw [degree_add_eq_left_of_degree_lt heh]
    exact lt_of_le_of_lt (degree_add_le _ _) (max_lt
      (lt_of_le_of_lt (degree_sub_le _ _) (max_lt aD remD)) ecD)

variable [CharP F 2]

/-- On binary coefficients subtraction is XOR. These outputs are the literal
monic quotient and remainder used by a recursive radix split. -/
theorem binary_quotient_remainder {h : ℕ} (hh : 2 ≤ h) (a b e : F[X])
    (ha : a.natDegree < h) (hb : b.natDegree < h) (he : e.natDegree ≤ h / 2) :
    let c := feedback h e b
    (a + X^h*b) /ₘ (X^h+e) = b+c ∧
      (a + X^h*b) %ₘ (X^h+e) = a + ((e*b) %ₘ X^h) + e*c := by
  simpa only [CharTwo.sub_eq_add] using truncated_quotient_remainder hh a b e ha hb he

/-- The actual scanning formula uses the low part of e times the recovered
quotient itself. High and low here are ordinary division by X^h. -/
theorem streamed_binary_split {h : ℕ} (hh : 2 ≤ h) (a b e : F[X])
    (ha : a.natDegree < h) (hb : b.natDegree < h) (he : e.natDegree ≤ h / 2) :
    let q := b + feedback h e b
    (a + X^h*b) /ₘ (X^h+e) = q ∧
      (a + X^h*b) %ₘ (X^h+e) = a + ((e*q) %ₘ X^h) := by
  dsimp only
  obtain ⟨qu, re⟩ := binary_quotient_remainder hh a b e ha hb he
  have ecD : (e * feedback h e b).degree < (X^h : F[X]).degree := by
    apply degree_lt_degree
    rw [natDegree_X_pow]
    have := feedback_degree hh he hb
    have := natDegree_mul_le (p := e) (q := feedback h e b)
    omega
  refine ⟨qu, ?_⟩
  conv_rhs => rw [mul_add, add_modByMonic, (modByMonic_eq_self_iff (monic_X_pow h)).mpr ecD, ← add_assoc]
  exact re

/-- Taking p=2^c gives the relative trace of the cubic finite-field extension. -/
noncomputable def traceBase (p : ℕ) : F[X] :=
  let t := X + X^p + X^(p*p)
  t^2+t

noncomputable def traceLow (p t : ℕ) : F[X] :=
  X^(p*p*t) + X^(p*2*t) + X^(p*t) + X^(2*t) + X^t

theorem trace_power_form (p i : ℕ) :
    (traceBase (F := F) p)^(2^i) =
      X^(p*p*2*(2^i)) + traceLow p (2^i) := by
  simp only [traceBase, traceLow, CharTwo.add_sq, add_pow_expChar_pow, ← pow_mul]
  simp only [Nat.mul_assoc, add_comm, add_left_comm, add_assoc]

omit [CharP F 2] in
private theorem traceLow_degree (p t : ℕ) (hp : 2 ≤ p) :
    (traceLow (F := F) p t).natDegree ≤ p*p*t := by
  have hw : p*2 ≤ p*p := Nat.mul_le_mul_left p hp
  have h1 : p*t ≤ p*p*t := Nat.mul_le_mul_right t (by omega)
  have h2 : (p*2)*t ≤ p*p*t := Nat.mul_le_mul_right t hw
  have h3 : 2*t ≤ p*p*t := Nat.mul_le_mul_right t (by omega)
  have h4 : t ≤ p*p*t := by
    simpa only [one_mul] using Nat.mul_le_mul_right t (show 1 ≤ p*p by omega)
  have join {u w : F[X]} (hu : u.natDegree ≤ p*p*t) (hw' : w.natDegree ≤ p*p*t) :
      (u+w).natDegree ≤ p*p*t := (natDegree_add_le _ _).trans (max_le hu hw')
  unfold traceLow
  apply join (join (join (join ?_ ?_) ?_) ?_) ?_
  all_goals rw [natDegree_X_pow]
  all_goals omega

/-- The one-correction split works for each actual Frobenius power of the
trace-bundle polynomial and for all two-word inputs, not just sampled fields. -/
theorem trace_power_exact (p i : ℕ) (hp : 2 ≤ p) (a b : F[X])
    (ha : a.natDegree < p*p*2*(2^i)) (hb : b.natDegree < p*p*2*(2^i)) :
    let h := p*p*2*(2^i)
    let e := traceLow (F := F) p (2^i)
    let q := b + feedback h e b
    (a + X^h*b) /ₘ ((traceBase p)^(2^i)) = q ∧
      (a + X^h*b) %ₘ ((traceBase p)^(2^i)) = a + ((e*q) %ₘ X^h) := by
  dsimp only
  rw [trace_power_form]
  have hw : p*p*2*(2^i) = 2*(p*p*(2^i)) := by ring
  have hpos : 0 < p*p*(2^i) := by positivity
  have hlow := traceLow_degree (F := F) p (2^i) hp
  apply streamed_binary_split _ a b _ ha hb
  · omega
  · omega

#print axioms feedback_square_zero
#print axioms streamed_binary_split
#print axioms trace_power_form
#print axioms trace_power_exact
#print axioms truncated_quotient_remainder
#print axioms binary_quotient_remainder
end Moonshot.CoefficientPrefix
