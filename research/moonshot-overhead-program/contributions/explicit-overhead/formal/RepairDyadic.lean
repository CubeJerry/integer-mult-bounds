import OAI.Computability.NearSquareRoot.KernelPass
import Mathlib.Algebra.Ring.Subring.Basic
import Mathlib.Data.Rat.Lemmas

/-!
The published binary-plan syntax operates over Z[1/2]. The rational Newton
repair used by the adaptive Walsh construction has a one-seed active block
whose division by its true nonzero gap has 73 in its reduced denominator.
Both the plan invariant and the actual six-bit singleton are checked here.

Source pin: openai/math 3344da59991ed94f9ba711217b29c1d760badfa6.
-/

namespace Moonshot.WalshPlan

open OAI.Computability.NearSquareRoot.KernelPass
/-- OpenAI's ProtectedRationals module defines the same closure. The small
imports above avoid compiling its separate maximal-ideal theory. -/
def dyadicRationals : Subring ℚ := Subring.closure {(2 : ℚ)⁻¹}

/-- The singleton-73 specialization of OpenAI's protectedRationals carrier
and closure proof (same source pin as KernelPass). -/
private def prime73Ring : Subring ℚ where
  carrier := {q | Nat.Coprime 73 q.den}
  zero_mem' := by decide
  one_mem' := by decide
  neg_mem' {a} ha := by
    change Nat.Coprime 73 (-a).den
    simpa using ha
  add_mem' {a b} ha hb :=
    (ha.mul_right hb).coprime_dvd_right (Rat.add_den_dvd a b)
  mul_mem' {a b} ha hb :=
    (ha.mul_right hb).coprime_dvd_right (Rat.mul_den_dvd a b)

private theorem dyadicRationals_le_prime73Ring : dyadicRationals ≤ prime73Ring := by
  apply Subring.closure_le.mpr
  apply Set.singleton_subset_iff.mpr
  change Nat.Coprime 73 (((2 : ℚ)⁻¹).den)
  rw [Rat.inv_ofNat_den]
  decide

private theorem halfInverse_mem : (2 : ℚ)⁻¹ ∈ dyadicRationals := by
  apply Subring.subset_closure
  simp

private theorem coefficient_mem (c : Coefficient) : value c ∈ dyadicRationals := by
  change (c.1 : ℚ) / (2 : ℚ) ^ c.2 ∈ dyadicRationals
  rw [div_eq_mul_inv, ← inv_pow]
  exact dyadicRationals.mul_mem (intCast_mem _ _) (dyadicRationals.pow_mem halfInverse_mem _)

private theorem pairEntry_mem (x y : Fin 2 → ZMod 2) :
    pairEntry x y ∈ dyadicRationals := by
  have hh : (1 / 2 : ℚ) ∈ dyadicRationals := by simpa only [one_div] using halfInverse_mem
  unfold pairEntry
  split
  · exact hh
  · exact dyadicRationals.neg_mem hh

private theorem childEntry_mem {A : ℕ} (axis : Fin A) (y x : Column A) :
    childEntry axis y x ∈ dyadicRationals := by
  unfold childEntry
  split
  · exact pairEntry_mem _ _
  · exact dyadicRationals.zero_mem

/-- Every matrix entry of every literal published plan at every column width. -/
theorem plan_entries_dyadic {A i o : ℕ} (p : Plan A i o) (h : ℕ) :
    ∀ (u : Fin o × Addr A h) (v : Fin i × Addr A h), p.eval h u v ∈ dyadicRationals := by
  classical
  induction p with
  | mix coeff =>
      rintro ⟨b,y⟩ ⟨a,x⟩
      simp only [Plan.eval]
      split
      · exact coefficient_mem _
      · exact dyadicRationals.zero_mem
  | xor g =>
      rintro ⟨b,y⟩ ⟨a,x⟩
      simp only [Plan.eval]
      split
      · exact dyadicRationals.one_mem
      · exact dyadicRationals.zero_mem
  | scale q test table =>
      rintro ⟨b,y⟩ ⟨a,x⟩
      simp only [Plan.eval]
      split
      · exact coefficient_mem _
      · exact dyadicRationals.zero_mem
  | child axis =>
      rintro ⟨b,y⟩ ⟨a,x⟩
      exact dyadicRationals.prod_mem (fun j _ => childEntry_mem axis (y j) (x j))
  | seq p q hp hq =>
      intro u v
      simp only [Plan.eval, Matrix.mul_apply]
      exact dyadicRationals.sum_mem (fun j _ => dyadicRationals.mul_mem (hp u j) (hq j v))
  | parallel p q hp hq =>
      rintro ⟨b,y⟩ ⟨a,x⟩
      refine Fin.addCases (fun l => ?_) (fun r => ?_) b <;>
        refine Fin.addCases (fun l' => ?_) (fun r' => ?_) a <;>
        simp only [Plan.eval, directSum, Fin.addCases_left, Fin.addCases_right]
      · exact hp (l,y) (l',x)
      · exact dyadicRationals.zero_mem
      · exact dyadicRationals.zero_mem
      · exact hq (r,y) (r',x)

/-- Parity of a six-bit address. -/
private def parity6 (n : ℕ) : Bool :=
  ((List.range 6).filter (fun b => n.testBit b)).length % 2 == 1

/-- Hamming weight of the shifted zero key. The 63 labels are all nonzero
six-bit words, numbered from one. -/
private def shiftedWeight (seed : ℕ) : ℕ :=
  ((List.range 63).filter (fun j => parity6 (seed &&& (j+1)))).length

/-- Term and partial sum of the actual Newton predictor. At h+1 the new
term is (-2) times (count-15-h)/(h+1) times the previous term. This is
(-2)^(h+1) times the generalized binomial at count-15. -/
private def newton (count : ℕ) : ℕ → ℤ × ℤ
  | 0 => (1,1)
  | h+1 =>
      let previous := newton count h
      let term := previous.1 * (-2) * ((count : ℤ) - 15 - h) / ((h : ℤ) + 1)
      (term, previous.2 + term)

/-- The zero frequency has target +1 and its seed sign is (-1)^(15-count). -/
private def gapAtCount (count : ℕ) : ℤ :=
  (if count % 2 = 0 then -1 else 1) * (newton count 33).2 - 1

def singletonGap : ℤ := -4510048854467219030016

theorem gap_at_zero : gapAtCount 0 = singletonGap := by decide
theorem gap_at_regular_seed : gapAtCount 32 = 0 := by decide

set_option maxRecDepth 4096 in
set_option maxHeartbeats 4000000 in
theorem actual_shift_weights :
    (List.range 64).map shiftedWeight = 0 :: List.replicate 63 32 := by decide

/-- In seed order exactly the first gap is nonzero. The one-by-one
Vandermonde check is [1], so the repair on independent check coordinates
uses the inverse of singletonGap. -/
theorem actual_repair_gaps :
    ((List.range 64).map shiftedWeight).map gapAtCount =
      singletonGap :: List.replicate 63 0 := by
  rw [actual_shift_weights]
  simp [gap_at_zero, gap_at_regular_seed]

theorem gap_has_factor_73 : (73 : ℤ) ∣ singletonGap :=
  ⟨-61781491157085192192, by decide⟩

theorem singleton_inverse_not_dyadic : ((singletonGap : ℚ)⁻¹) ∉ dyadicRationals := by
  intro h
  have allowed : Nat.Coprime 73 (((singletonGap : ℚ)⁻¹).den) :=
    dyadicRationals_le_prime73Ring h
  have denied : ¬ Nat.Coprime 73 (((singletonGap : ℚ)⁻¹).den) := by
    rw [Rat.den_inv, Rat.num_intCast]
    decide
  exact denied allowed

/-- Neither signed coefficient of the isolated singleton repair can occur
as an entry of a native plan acting on arbitrary independent check rows. -/
theorem native_plan_excludes_singleton_repair {A i o : ℕ} (p : Plan A i o) (h : ℕ)
    (u : Fin o × Addr A h) (v : Fin i × Addr A h) :
    p.eval h u v ≠ (singletonGap : ℚ)⁻¹ ∧
      p.eval h u v ≠ -((singletonGap : ℚ)⁻¹) := by
  have entry := plan_entries_dyadic p h u v
  constructor
  · intro he
    exact singleton_inverse_not_dyadic (he ▸ entry)
  · intro he
    apply singleton_inverse_not_dyadic
    simpa only [he, neg_neg] using dyadicRationals.neg_mem entry

#print axioms plan_entries_dyadic
#print axioms actual_repair_gaps
#print axioms gap_has_factor_73
#print axioms native_plan_excludes_singleton_repair

end Moonshot.WalshPlan
