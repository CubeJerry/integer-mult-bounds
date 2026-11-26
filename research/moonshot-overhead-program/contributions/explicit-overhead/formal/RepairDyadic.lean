import OAI.Computability.NearSquareRoot.KernelPass
import Mathlib.Algebra.Ring.Subring.Basic
import Mathlib.Data.Rat.Lemmas
import Mathlib.Data.Nat.Choose.Sum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum

/-!
The published binary-plan syntax operates over Z[1/2]. The rational Newton
repair used by the adaptive Walsh construction has a one-seed active block
whose division by its true nonzero gap has 73 in its reduced denominator.
The file also checks the two-term Newton tail at arbitrary odd degree and
its consequence for a full active check matrix on independent coordinates.

Source pin: openai/math 3344da59991ed94f9ba711217b29c1d760badfa6.
-/

namespace Moonshot.WalshPlan

open OAI.Computability.NearSquareRoot.KernelPass
/-- OpenAI's ProtectedRationals module defines the same closure. The small
imports above avoid compiling its separate maximal-ideal theory. -/
def dyadicRationals : Subring ℚ := Subring.closure {(2 : ℚ)⁻¹}

/-- The one-denominator specialization of OpenAI's protectedRationals. -/
private def protectedDenominator (p : ℕ) : Subring ℚ where
  carrier := {q | p.Coprime q.den}
  zero_mem' := by change p.Coprime 1; simp
  one_mem' := by change p.Coprime 1; simp
  neg_mem' {a} ha := by
    change p.Coprime (-a).den
    simpa using ha
  add_mem' {a b} ha hb :=
    (ha.mul_right hb).coprime_dvd_right (Rat.add_den_dvd a b)
  mul_mem' {a b} ha hb :=
    (ha.mul_right hb).coprime_dvd_right (Rat.mul_den_dvd a b)

private theorem dyadic_protected {p : ℕ} (odd : Odd p) :
    dyadicRationals ≤ protectedDenominator p := by
  apply Subring.closure_le.mpr
  apply Set.singleton_subset_iff.mpr
  change p.Coprime (((2 : ℚ)⁻¹).den)
  rw [Rat.inv_ofNat_den]
  exact Nat.coprime_two_right.mpr odd

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
    dyadic_protected (p := 73) (by decide) h
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

/-- At count d+2 above the starting offset, exactly the last two binomial
terms are omitted by a degree-d Newton predictor. The seed sign can be
applied after this unsigned discrepancy. -/
def twoTermGap (d : ℕ) : ℚ :=
  (∑ h ∈ Finset.range (d+1), (-2 : ℚ)^h * ((d+2).choose h : ℚ)) - (-1 : ℚ)^(d+2)

theorem twoTermGap_eq (d : ℕ) :
    twoTermGap d = -((-2 : ℚ)^(d+1) * d) := by
  let term (h : ℕ) : ℚ := (-2 : ℚ)^h * ((d+2).choose h : ℚ)
  have total : (∑ h ∈ Finset.range ((d+2)+1), term h) = (-1 : ℚ)^(d+2) := by
    simpa only [term, one_pow, mul_one, show (-2 : ℚ)+1 = -1 by norm_num] using
      (add_pow (-2 : ℚ) 1 (d+2)).symm
  have expand : (∑ h ∈ Finset.range ((d+2)+1), term h) =
      (∑ h ∈ Finset.range (d+1), term h) + term (d+1) + term (d+2) :=
    (Finset.sum_range_succ term (d+2)).trans
      (congrArg (fun z => z + term (d+2)) (Finset.sum_range_succ term (d+1)))
  have penultimate : term (d+1) = (-2 : ℚ)^(d+1) * ((d : ℚ)+2) := by
    dsimp only [term]
    rw [show (d+2).choose (d+1) = d+2 from Nat.choose_succ_self_right (d+1)]
    push_cast
    ring
  have last : term (d+2) = (-2 : ℚ)^(d+1) * (-2) := by
    simpa only [term, Nat.choose_self, Nat.cast_one, mul_one] using
      (pow_succ (-2 : ℚ) (d+1))
  change (∑ h ∈ Finset.range (d+1), term h) - (-1 : ℚ)^(d+2) = _
  rw [← total, expand, penultimate, last]
  ring

private theorem oddInverse_not_mem (d : ℕ) (odd : Odd d) (large : 1 < d) :
    (d : ℚ)⁻¹ ∉ dyadicRationals := by
  intro h
  have self : d.Coprime (((d : ℚ)⁻¹).den) := dyadic_protected odd h
  rw [Rat.inv_natCast_den_of_pos (by omega : 0 < d)] at self
  have heq : d = 1 := by simpa [Nat.Coprime] using self
  omega

theorem twoTermGap_inverse_not_dyadic (d : ℕ) (odd : Odd d) (large : 1 < d) :
    (twoTermGap d)⁻¹ ∉ dyadicRationals := by
  intro h
  have base : (-2 : ℚ) ∈ dyadicRationals :=
    dyadicRationals.neg_mem (natCast_mem dyadicRationals 2)
  have factor := dyadicRationals.neg_mem (dyadicRationals.pow_mem base (d+1))
  have scaled := dyadicRationals.mul_mem factor h
  have hd : (d : ℚ) ≠ 0 := by exact_mod_cast (by omega : d ≠ 0)
  have hp : (-2 : ℚ)^(d+1) ≠ 0 := pow_ne_zero _ (by norm_num)
  have cancel : -((-2 : ℚ)^(d+1)) * (-((-2 : ℚ)^(d+1)*(d:ℚ)))⁻¹ = (d:ℚ)⁻¹ := by
    field_simp [hd, hp]
  rw [twoTermGap_eq, cancel] at scaled
  exact oddInverse_not_mem d odd large scaled

/-- Powers of actual nodes i/2^r form the active Vandermonde check matrix. -/
def checkMatrix {n : ℕ} (width : ℕ) (label : Fin n → ℕ) : Matrix (Fin n) (Fin n) ℚ :=
  fun i j => ((label j : ℚ) / (2 : ℚ)^width)^i.val

private theorem checkMatrix_mem {n : ℕ} (width : ℕ) (label : Fin n → ℕ) (i j : Fin n) :
    checkMatrix width label i j ∈ dyadicRationals := by
  unfold checkMatrix
  apply dyadicRationals.pow_mem
  rw [div_eq_mul_inv, ← inv_pow]
  exact dyadicRationals.mul_mem (natCast_mem _ _) (dyadicRationals.pow_mem halfInverse_mem width)

private theorem matrixMul_mem {n : ℕ} {P Q : Matrix (Fin n) (Fin n) ℚ}
    (hp : ∀ i j, P i j ∈ dyadicRationals) (hq : ∀ i j, Q i j ∈ dyadicRationals) :
    ∀ i j, (P*Q) i j ∈ dyadicRationals := by
  intro i j
  rw [Matrix.mul_apply]
  exact dyadicRationals.sum_mem (fun a _ => dyadicRationals.mul_mem (hp i a) (hq a j))

/-- Multiplying both sides by the original dyadic check matrix exposes
the reciprocal of the true discrepancy. Other defective seeds cannot make
the entire isolated check-to-lift table dyadic by cancellation. The equality
hypothesis is precisely the selected diagonal entry of Vᵀ T V=diag(1/g).
The two alternatives retain the seed sign. -/
theorem checkBlock_has_nondyadic_entry {n : ℕ} (width d : ℕ) (label : Fin n → ℕ)
    (odd : Odd d) (large : 1 < d) (T : Matrix (Fin n) (Fin n) ℚ) (seed : Fin n)
    (hgap :
      let V := checkMatrix width label
      (V.transpose * T * V) seed seed = (twoTermGap d)⁻¹ ∨
        (V.transpose * T * V) seed seed = -((twoTermGap d)⁻¹)) :
    ∃ i j, T i j ∉ dyadicRationals := by
  classical
  by_contra! hT
  let V := checkMatrix width label
  have hv : ∀ i j, V i j ∈ dyadicRationals := checkMatrix_mem width label
  have hvt : ∀ i j, V.transpose i j ∈ dyadicRationals := fun i j => hv j i
  have hm : (V.transpose * T * V) seed seed ∈ dyadicRationals :=
    matrixMul_mem (matrixMul_mem hvt hT) hv seed seed
  have hn := twoTermGap_inverse_not_dyadic d odd large
  rcases hgap with he | he
  · exact hn (he ▸ hm)
  · have hneg := dyadicRationals.neg_mem (he ▸ hm)
    exact hn (by simpa only [neg_neg] using hneg)

#print axioms twoTermGap_eq
#print axioms checkBlock_has_nondyadic_entry
#print axioms plan_entries_dyadic
#print axioms actual_repair_gaps
#print axioms gap_has_factor_73
#print axioms native_plan_excludes_singleton_repair

end Moonshot.WalshPlan
