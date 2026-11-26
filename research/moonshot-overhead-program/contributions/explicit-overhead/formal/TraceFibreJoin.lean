import GroupedComposition
import Mathlib.Algebra.CharP.Two
import Mathlib.Algebra.CharP.Frobenius
import Mathlib.Algebra.CharP.Reduced
import Mathlib.Dynamics.PeriodicPts.Lemmas
import Mathlib.RingTheory.Coprime.Basic

/-! Actual polynomial remainders when joining the two relative-trace fibres. -/
open Polynomial
open scoped Polynomial
namespace Moonshot.TraceFibreJoin

variable {F : Type*} [Field F] [CharP F 2]

/-- The parent reconstructed from the two actual child polynomial remainders. -/
noncomputable def join (P A B : F[X]) : F[X] := A + P * (A + B)

omit [CharP F 2] in
private theorem monic_add_one {P : F[X]} (hp : P.Monic) (hd : 0 < P.natDegree) :
    (P+1).Monic :=
  hp.add_of_left (degree_lt_degree (by simpa only [natDegree_one] using hd))

private theorem rhs_identity (P A B : F[X]) :
    B + (P+1)*(A+B) = join P A B := by
  unfold join
  calc
    _ = (B+B) + (A+P*(A+B)) := by ring
    _ = _ := by rw [CharTwo.add_self_eq_zero, zero_add]

/-- Monic division recovers both arbitrary child remainders and their common quotient. -/
theorem recover_children {P A B : F[X]} (hp : P.Monic)
    (hA : A.natDegree < P.natDegree) (hB : B.natDegree < P.natDegree) :
    (join P A B) %ₘ P = A ∧ (join P A B) %ₘ (P+1) = B ∧
      (join P A B) /ₘ P = A+B := by
  have hd : 0 < P.natDegree := Nat.zero_lt_of_lt hA
  have left := div_modByMonic_unique (A+B) A hp ⟨rfl, degree_lt_degree hA⟩
  have hB' : B.natDegree < (P+1).natDegree := by simpa only [natDegree_add_one] using hB
  have right := div_modByMonic_unique (A+B) B (monic_add_one hp hd)
    ⟨rhs_identity P A B, degree_lt_degree hB'⟩
  exact ⟨left.2, right.2, left.1⟩

omit [CharP F 2] in
private theorem join_degree {P A B : F[X]}
    (hA : A.natDegree < P.natDegree) (hB : B.natDegree < P.natDegree) :
    (join P A B).natDegree < P.natDegree + P.natDegree := by
  have hab := (natDegree_add_le A B).trans_lt (max_lt hA hB)
  have hbnd := natDegree_mul_le (p := P) (q := A+B)
  have hsum := natDegree_add_le A (P*(A+B))
  change (A + P*(A+B)).natDegree < _
  omega

/-- The join of the two individual remainders is the ordinary remainder
modulo their product, on an input of any degree. -/
theorem actual_pair_remainder (f P : F[X]) (hp : P.Monic) (hd : 0 < P.natDegree) :
    f %ₘ (P*(P+1)) = join P (f %ₘ P) (f %ₘ (P+1)) := by
  have hp1 := monic_add_one hp hd
  have hn1 : P ≠ 1 := by
    rintro rfl
    simp at hd
  have hn2 : P+1 ≠ 1 := by
    intro h
    have hzero := congrArg natDegree h
    simp only [natDegree_add_one, natDegree_one] at hzero
    omega
  have hA := natDegree_modByMonic_lt f hp hn1
  have hB : (f %ₘ (P+1)).natDegree < P.natDegree := by
    simpa only [natDegree_add_one] using natDegree_modByMonic_lt f hp1 hn2
  let R := join P (f %ₘ P) (f %ₘ (P+1))
  have ha := recover_children hp hA hB
  have hleft : P ∣ f-R := (modByMonic_eq_zero_iff_dvd hp).mp (by
    rw [sub_modByMonic, show R %ₘ P = _ from ha.1, sub_self])
  have hright : P+1 ∣ f-R := (modByMonic_eq_zero_iff_dvd hp1).mp (by
    rw [sub_modByMonic, show R %ₘ (P+1) = _ from ha.2.1, sub_self])
  have cop : IsCoprime P (P+1) := ⟨-1, 1, by ring⟩
  have same := modByMonic_eq_of_dvd_sub (hp.mul hp1) (cop.mul_dvd hleft hright)
  have small : R.natDegree < (P*(P+1)).natDegree := by
    rw [natDegree_mul hp.ne_zero hp1.ne_zero, natDegree_add_one]
    exact join_degree hA hB
  exact same.trans ((modByMonic_eq_self_iff (hp.mul hp1)).mpr (degree_lt_degree small))

/-- The two additive fibres give exactly the translated quadratic modulus. -/
theorem translated_pair (T : F[X]) (a : F) :
    (T + C a) * (T + C a + 1) = T^2 + T + C (a^2 + a) := by
  calc
    _ = (T+C a)^2 + (T+C a) := by ring
    _ = _ := by rw [CharTwo.add_sq, map_add, map_pow]; ring

open Moonshot.GroupedComposition

/-- Each one-point lower caller gives the polynomial on its true trace fibre. -/
theorem fibre_from_coefficients (T : F[X]) (hT : T.Monic) (ht : 0 < T.natDegree)
    (a : F) (g : ℕ → F[X]) :
    grouped T g %ₘ (T+C a) = grouped T (fun k => C ((g k).eval a)) := by
  have h := (actual_grouped_division (X-C a) T (monic_X_sub_C a) hT
    (by simp) ht g).2
  simp only [sub_comp, X_comp, C_comp, modByMonic_X_sub_C_eq_C_eval] at h
  simpa only [CharTwo.sub_eq_add] using h

/-- Applied to the base-T digits, the two genuine fibre evaluations reconstruct
exactly the ordinary S006 parent remainder, including its nonzero translation. -/
theorem actual_trace_fibre_join (T : F[X]) (hT : T.Monic) (ht : 0 < T.natDegree)
    (a : F) (g : ℕ → F[X]) :
    grouped T g %ₘ (T^2 + T + C (a^2+a)) =
      join (T+C a) (grouped T (fun k => C ((g k).eval a)))
        (grouped T (fun k => C ((g k).eval (a+1)))) := by
  have hm : (T+C a).Monic := hT.add_of_left (degree_lt_degree (by simp [ht]))
  have hd : 0 < (T+C a).natDegree := by simpa only [natDegree_add_C] using ht
  rw [← translated_pair, actual_pair_remainder (grouped T g) (T+C a) hm hd,
    fibre_from_coefficients T hT ht a g]
  have hshift : T+C a+1 = T+C (a+1) := by rw [map_add, map_one, add_assoc]
  rw [hshift, fibre_from_coefficients T hT ht (a+1) g]


/-- On every parent below the actual product degree, joining its two
ordinary remainders reconstructs the input exactly. -/
theorem recover_parent (R P : F[X]) (hp : P.Monic) (hd : 0 < P.natDegree)
    (hr : R.natDegree < P.natDegree + P.natDegree) :
    join P (R %ₘ P) (R %ₘ (P+1)) = R := by
  rw [← actual_pair_remainder R P hp hd]
  apply (modByMonic_eq_self_iff (hp.mul (monic_add_one hp hd))).mpr
  apply degree_lt_degree
  simpa only [natDegree_mul hp.ne_zero (monic_add_one hp hd).ne_zero, natDegree_add_one] using hr

/-- In a twisted quotient orbit a parent is fixed exactly when coefficient
conjugation exchanges the two unrestricted polynomial child remainders. -/
theorem twisted_iff (φ : F →+* F) {P A B : F[X]} (hp : P.Monic)
    (hA : A.natDegree < P.natDegree) (hB : B.natDegree < P.natDegree)
    (hs : P.map φ = P+1) : (join P A B).map φ = join P A B ↔
      A.map φ = B ∧ B.map φ = A := by
  have children := recover_children hp hA hB
  have hs' : (P+1).map φ = P := by
    rw [Polynomial.map_add, Polynomial.map_one, hs, add_assoc, CharTwo.add_self_eq_zero, add_zero]
  constructor
  · intro fixed
    constructor
    · calc
        _ = ((join P A B) %ₘ P).map φ := congrArg (Polynomial.map φ) children.1.symm
        _ = B := by rw [map_modByMonic φ hp, fixed, hs, children.2.1]
    · calc
        _ = ((join P A B) %ₘ (P+1)).map φ := congrArg (Polynomial.map φ) children.2.1.symm
        _ = A := by rw [map_modByMonic φ (monic_add_one hp (Nat.zero_lt_of_lt hA)),
          fixed, hs', children.1]
  · rintro ⟨h1,h2⟩
    simpa only [join, Polynomial.map_add, Polynomial.map_mul, h1, h2, hs,
      add_comm B A] using (rhs_identity P A B)

/-- When conjugation fixes the two fibres separately their two child
polynomials are independently fixed. -/
theorem untwisted_iff (φ : F →+* F) {P A B : F[X]} (hp : P.Monic)
    (hA : A.natDegree < P.natDegree) (hB : B.natDegree < P.natDegree)
    (hs : P.map φ = P) : (join P A B).map φ = join P A B ↔
      A.map φ = A ∧ B.map φ = B := by
  have children := recover_children hp hA hB
  have hs' : (P+1).map φ = P+1 := by rw [Polynomial.map_add, Polynomial.map_one, hs]
  constructor
  · intro fixed
    constructor
    · calc
        _ = ((join P A B) %ₘ P).map φ := congrArg (Polynomial.map φ) children.1.symm
        _ = A := by rw [map_modByMonic φ hp, fixed, hs, children.1]
    · calc
        _ = ((join P A B) %ₘ (P+1)).map φ := congrArg (Polynomial.map φ) children.2.1.symm
        _ = B := by rw [map_modByMonic φ (monic_add_one hp (Nat.zero_lt_of_lt hA)),
          fixed, hs', children.2.1]
  · rintro ⟨h1,h2⟩
    simp only [join, Polynomial.map_add, Polynomial.map_mul, h1, h2, hs]

/-- At the actual d-fold Frobenius power, a translated trace fibre with
an exchanged anchor has exactly the twisted compatibility condition. -/
theorem frobenius_twisted (T A B : F[X]) (a : F) (d : ℕ) (hT : T.Monic)
    (hA : A.natDegree < T.natDegree) (hB : B.natDegree < T.natDegree)
    (hfixed : T.map (iterateFrobenius F 2 d) = T) (ha : a^(2^d) = a+1) :
    (join (T+C a) A B).map (iterateFrobenius F 2 d) = join (T+C a) A B ↔
      A.map (iterateFrobenius F 2 d) = B ∧ B.map (iterateFrobenius F 2 d) = A := by
  have ht := Nat.zero_lt_of_lt hA
  apply twisted_iff
  · exact hT.add_of_left (degree_lt_degree (by simp [ht]))
  · simpa using hA
  · simpa using hB
  · rw [Polynomial.map_add, hfixed, map_C, iterateFrobenius_def, ha, map_add, map_one, add_assoc]


/-- The orbit length in the actual binary Frobenius action. -/
noncomputable def orbitPeriod (t : F) : ℕ := Function.minimalPeriod (frobenius F 2) t

private theorem fixed_iff_period_dvd (t : F) (n : ℕ) :
    iterateFrobenius F 2 n t = t ↔ orbitPeriod t ∣ n := by
  change _ ↔ Function.minimalPeriod _ _ ∣ n
  rw [← Function.isPeriodicPt_iff_minimalPeriod_dvd]
  change iterateFrobenius F 2 n t = t ↔ (⇑(frobenius F 2))^[n] t = t
  rw [← coe_iterateFrobenius F 2 n]

private theorem same_pair {x t : F} (h : x^2+x = t^2+t) : x = t ∨ x = t+1 := by
  have z : (x+t)*(x+t+1) = 0 := by
    calc
      _ = (x+t)^2 + (x+t) := by ring
      _ = (x^2+x) + (t^2+t) := by rw [CharTwo.add_sq]; ring
      _ = 0 := by rw [h, CharTwo.add_self_eq_zero]
  rcases mul_eq_zero.mp z with h0|h1
  · exact Or.inl (sub_eq_zero.mp (by simpa only [CharTwo.sub_eq_add] using h0))
  · exact Or.inr (sub_eq_zero.mp (by simpa only [CharTwo.sub_eq_add,add_assoc] using h1))

/-- On every finite characteristic-two field, the two fibres either belong
to distinct length-d orbits or are interchanged at d in one length-2d orbit. -/
theorem actual_orbit_period [Finite F] (t : F) :
    let d := orbitPeriod (t^2+t)
    (orbitPeriod t = d ∧ t^(2^d) = t) ∨
      (orbitPeriod t = 2*d ∧ t^(2^d) = t+1) := by
  let s := t^2+t
  let d := orbitPeriod s
  let D := orbitPeriod t
  have hd : 0 < d := Function.minimalPeriod_pos_of_mem_periodicPts
    ((frobenius_inj F 2).mem_periodicPts s)
  have ts : iterateFrobenius F 2 D t = t := (fixed_iff_period_dvd t D).2 dvd_rfl
  have sd : iterateFrobenius F 2 d s = s := (fixed_iff_period_dvd s d).2 dvd_rfl
  have dD : d ∣ D := (fixed_iff_period_dvd s D).1 (by
    change iterateFrobenius F 2 D (t^2+t) = t^2+t
    rw [map_add, map_pow, ts])
  have pair : (iterateFrobenius F 2 d t)^2 + iterateFrobenius F 2 d t = t^2+t := by
    simpa only [s,map_add,map_pow] using sd
  change (D = d ∧ iterateFrobenius F 2 d t = t) ∨
    (D = 2*d ∧ iterateFrobenius F 2 d t = t+1)
  rcases same_pair pair with h0|h1
  · exact Or.inl ⟨Nat.dvd_antisymm ((fixed_iff_period_dvd t d).1 h0) dD,h0⟩
  · have dd : D ∣ d*2 := (fixed_iff_period_dvd t (d*2)).1 (by
      rw [Nat.mul_two, iterateFrobenius_add_apply, h1, map_add, map_one, h1,
        add_assoc, CharTwo.add_self_eq_zero, add_zero])
    obtain ⟨e, he⟩ := dD
    have he2 : e ∣ 2 := Nat.dvd_of_mul_dvd_mul_left hd (he ▸ dd)
    rcases (Nat.dvd_prime Nat.prime_two).1 he2 with he1|he1
    · have eq : D = d := by simpa only [he1,Nat.mul_one] using he
      rw [eq,h1] at ts
      exact (add_ne_left.mpr one_ne_zero ts).elim
    · exact Or.inr ⟨by rw [he,he1,Nat.mul_comm],h1⟩


/-- Translation by one preserves the actual Frobenius period. -/
theorem translated_period (t : F) : orbitPeriod (t+1) = orbitPeriod t := by
  apply Nat.dvd_antisymm
  · apply (fixed_iff_period_dvd _ _).1
    rw [map_add,map_one, (fixed_iff_period_dvd t _).2 dvd_rfl]
  · apply (fixed_iff_period_dvd _ _).1
    have h := (fixed_iff_period_dvd (t+1) _).2 dvd_rfl
    rw [map_add, map_one, add_left_inj] at h
    exact h

/-- The two anchors lie on the same orbit exactly in the twisted case.
This certifies when the lower caller supplies one factor rather than two. -/
theorem same_orbit_iff_twisted [Finite F] (t : F) :
    (∃ n : ℕ, t^(2^n) = t+1) ↔ t^(2^(orbitPeriod (t^2+t))) = t+1 := by
  constructor
  · rintro ⟨n,hn⟩
    rcases actual_orbit_period t with ⟨hperiod,_⟩|⟨_,ht⟩
    · have hs : iterateFrobenius F 2 n (t^2+t) = t^2+t := by
        rw [map_add,map_pow,show iterateFrobenius F 2 n t = t+1 from hn, CharTwo.add_sq]
        simp only [one_pow]; calc
          t^2+1+(t+1) = t^2+t+(1+1) := by ring
          _ = _ := by rw [CharTwo.add_self_eq_zero, add_zero]
      have hdiv := (fixed_iff_period_dvd _ _).1 hs
      rw [← hperiod] at hdiv
      have ht := (fixed_iff_period_dvd t n).2 hdiv
      rw [iterateFrobenius_def,hn] at ht
      exact (add_ne_left.mpr one_ne_zero ht).elim
    · exact ht
  · exact fun h => ⟨_,h⟩

#print axioms translated_period
#print axioms same_orbit_iff_twisted
#print axioms actual_orbit_period
#print axioms recover_parent
#print axioms twisted_iff
#print axioms untwisted_iff
#print axioms frobenius_twisted

#print axioms recover_children
#print axioms actual_pair_remainder
#print axioms translated_pair
#print axioms fibre_from_coefficients
#print axioms actual_trace_fibre_join
end Moonshot.TraceFibreJoin
