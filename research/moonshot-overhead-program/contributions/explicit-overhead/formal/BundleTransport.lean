import AdditiveTraceLayers
import Mathlib.Algebra.Ring.Equiv
import Mathlib.Algebra.Group.Subgroup.Basic
import Mathlib.Algebra.CharP.Reduced
import Mathlib.Algebra.CharP.Frobenius
import Mathlib.Data.Fintype.Card

/-!
# Transport of complete additive records by a field automorphism

An ordered coset address is an actual element of a characteristic-two field.
On two conjugate supports an automorphism fixes the source-to-target address
permutation, including the translation of a chosen coset representative. The
map below evaluates a complete source record, transports point values and
interpolates in the target basis. Its point semantics, uniqueness and
two-sided invertibility cover arbitrary independent orderings. The construction
uses choice to identify addresses and does not assert a routing-time bound.
-/

namespace Moonshot.BundleTransport
open Moonshot.AdditiveLayers

universe u
variable {F : Type u} [Field F] [CharP F 2]

/-- Every independent ordered address labels a unique point. Surjectivity of
the forward evaluator on arbitrary tables separates any pair of addresses. -/
theorem address_injective {β : ℕ → F} {n : ℕ}
    (h : independentDirections β n) (a : F) :
    Function.Injective (address β n a) := by
  classical
  intro i j same
  by_contra different
  let y : Row F n := fun t => if t = i then 0 else 1
  let p := inverse β n a y
  have sep : forward β n a p i = forward β n a p j := by
    rw [forward_value, forward_value, same]
  have roundtrip : forward β n a p = y :=
    forward_inverse β n (gaps_of_independent h) a y
  rw [roundtrip] at sep
  simp [y, Ne.symm different] at sep

/-- Equality here concerns the entire conjugate point set in the two orders. -/
def SameSupport (σ : F ≃+* F) {n : ℕ} (β γ : ℕ → F) (a d : F) : Prop :=
  ∀ z, (∃ i : Digits n, σ (address β n a i) = z) ↔
    ∃ j : Digits n, address γ n d j = z

theorem unique_source_digit (σ : F ≃+* F) {β γ : ℕ → F} {n : ℕ} {a d : F}
    (hb : independentDirections β n) (hs : SameSupport (n := n) σ β γ a d)
    (j : Digits n) : ∃! i, σ (address β n a i) = address γ n d j := by
  obtain ⟨i,hi⟩ := (hs (address γ n d j)).mpr ⟨j,rfl⟩
  exact ⟨i,hi,fun k hk => address_injective hb a (σ.injective (hk.trans hi.symm))⟩

/-- The map is identified by actual field addresses. It includes every affine
offset of the chosen representative and permits different ordered bases. -/
noncomputable def sourceDigit (σ : F ≃+* F) {β γ : ℕ → F} {n : ℕ} {a d : F}
    (hb : independentDirections β n) (hs : SameSupport (n := n) σ β γ a d)
    (j : Digits n) : Digits n :=
  Classical.choose (unique_source_digit σ hb hs j).exists

theorem sourceDigit_spec (σ : F ≃+* F) {β γ : ℕ → F} {n : ℕ} {a d : F}
    (hb : independentDirections β n) (hs : SameSupport (n := n) σ β γ a d)
    (j : Digits n) :
    σ (address β n a (sourceDigit σ hb hs j)) = address γ n d j :=
  Classical.choose_spec (unique_source_digit σ hb hs j).exists

theorem sourceDigit_bijective (σ : F ≃+* F) {β γ : ℕ → F} {n : ℕ} {a d : F}
    (hb : independentDirections β n) (hg : independentDirections γ n)
    (hs : SameSupport (n := n) σ β γ a d) :
    Function.Bijective (sourceDigit σ hb hs) := by
  constructor
  · intro j j' e
    apply address_injective hg d
    rw [← sourceDigit_spec σ hb hs j, ← sourceDigit_spec σ hb hs j', e]
  · intro i
    obtain ⟨j,hj⟩ := (hs (σ (address β n a i))).mp ⟨i,rfl⟩
    refine ⟨j,address_injective hb a (σ.injective ?_)⟩
    exact (sourceDigit_spec σ hb hs j).trans hj

/-- Evaluation and interpolation between one record and the ordered point table. -/
def evaluationEquiv {β : ℕ → F} {n : ℕ}
    (hb : independentDirections β n) (a : F) : Row F n ≃ Row F n where
  toFun := forward β n a
  invFun := inverse β n a
  left_inv := inverse_forward β n (gaps_of_independent hb) a
  right_inv := forward_inverse β n (gaps_of_independent hb) a

/-- The target rows are conjugated pointwise, permuted to their true addresses,
and restored to the target polynomial basis. -/
noncomputable def transport (σ : F ≃+* F) {β γ : ℕ → F} {n : ℕ} {a d : F}
    (hb : independentDirections β n) (hg : independentDirections γ n)
    (hs : SameSupport (n := n) σ β γ a d) : Row F n ≃ Row F n :=
  let idx := Equiv.ofBijective (sourceDigit σ hb hs) (sourceDigit_bijective σ hb hg hs)
  (evaluationEquiv hb a).trans
    ((Equiv.arrowCongr idx.symm σ.toEquiv).trans (evaluationEquiv hg d).symm)

theorem transport_at_point (σ : F ≃+* F) {β γ : ℕ → F} {n : ℕ} {a d : F}
    (hb : independentDirections β n) (hg : independentDirections γ n)
    (hs : SameSupport (n := n) σ β γ a d) (p : Row F n) (j : Digits n) :
    forward γ n d (transport σ hb hg hs p) j =
      σ (forward β n a p (sourceDigit σ hb hs j)) := by
  change forward γ n d (inverse γ n d _) j = _
  rw [forward_inverse γ n (gaps_of_independent hg)]
  rfl

def binaryHorner : List Bool → F → F
  | [], _ => 0
  | bit :: rest, z => (if bit then 1 else 0) + z * binaryHorner rest z

omit [CharP F 2] in
theorem binaryHorner_conjugate (σ : F ≃+* F) (bits : List Bool) (z : F) :
    σ (binaryHorner bits z) = binaryHorner bits (σ z) := by
  induction bits with
  | nil => exact map_zero σ
  | cons bit rest ih =>
    cases bit <;> simp [binaryHorner, ih]

/-- For every binary coefficient list, transporting its source remainder yields
the unique target remainder on the actual conjugate points. -/
theorem binary_remainder_transport (σ : F ≃+* F) {β γ : ℕ → F} {n : ℕ} {a d : F}
    (hb : independentDirections β n) (hg : independentDirections γ n)
    (hs : SameSupport (n := n) σ β γ a d) (bits : List Bool) (p : Row F n)
    (hp : ∀ i, forward β n a p i = binaryHorner bits (address β n a i)) :
    ∃! t : Row F n, ∀ j, forward γ n d t j = binaryHorner bits (address γ n d j) := by
  refine ⟨transport σ hb hg hs p, ?_, ?_⟩
  · intro j
    rw [transport_at_point, hp, binaryHorner_conjugate, sourceDigit_spec]
  · intro t ht
    apply (evaluationEquiv hg d).injective
    funext j
    change forward γ n d t j = forward γ n d (transport σ hb hg hs p) j
    rw [transport_at_point, hp, binaryHorner_conjugate, sourceDigit_spec, ht]

/-- The integer coefficient list denotes the same binary polynomial in both fields. -/
theorem transported_binary_at_point (σ : F ≃+* F) {β γ : ℕ → F} {n : ℕ} {a d : F}
    (hb : independentDirections β n) (hg : independentDirections γ n)
    (hs : SameSupport (n := n) σ β γ a d) (bits : List Bool) (p : Row F n)
    (hp : ∀ i, forward β n a p i = binaryHorner bits (address β n a i)) (j : Digits n) :
    forward γ n d (transport σ hb hg hs p) j = binaryHorner bits (address γ n d j) := by
  rw [transport_at_point, hp, binaryHorner_conjugate, sourceDigit_spec]

/-- Every Frobenius power is a genuine field automorphism of a finite field. -/
noncomputable def frobeniusPower [Finite F] (m : ℕ) : F ≃+* F :=
  RingEquiv.ofBijective (iterateFrobenius F 2 m) (by
    have hinj := iterateFrobenius_inj F 2 m
    exact ⟨hinj, Finite.surjective_of_injective hinj⟩)

@[simp] theorem frobeniusPower_apply [Finite F] (m : ℕ) (z : F) :
    frobeniusPower m z = z ^ ((2 : ℕ) ^ m) := by
  unfold frobeniusPower
  exact (RingEquiv.ofBijective_apply (iterateFrobenius F 2 m) _ z).trans
    (iterateFrobenius_def 2 m z)

theorem supportFromPowers [Finite F] (m : ℕ) {β γ : ℕ → F} {a d : F} {n : ℕ}
    (hs : ∀ z, (∃ i : Digits n, (address β n a i) ^ ((2 : ℕ) ^ m) = z) ↔
      ∃ j : Digits n, address γ n d j = z) : SameSupport (n := n) (frobeniusPower m) β γ a d := by
  simpa only [SameSupport, frobeniusPower_apply] using hs

/-- The stored representative gives each omitted binary remainder uniquely for
the actual map z ↦ z^(2^m), with arbitrary translations and ordered bases. -/
theorem finite_frobenius_remainder [Finite F] (m : ℕ)
    {β γ : ℕ → F} {n : ℕ} {a d : F}
    (hb : independentDirections β n) (hg : independentDirections γ n)
    (hs : ∀ z, (∃ i : Digits n, (address β n a i) ^ ((2 : ℕ) ^ m) = z) ↔
      ∃ j : Digits n, address γ n d j = z)
    (bits : List Bool) (p : Row F n)
    (hp : ∀ i, forward β n a p i = binaryHorner bits (address β n a i)) (t : Row F n) :
    (∀ j, forward γ n d t j = binaryHorner bits (address γ n d j)) ↔
      t = transport (frobeniusPower m) hb hg (supportFromPowers (β := β) (γ := γ) (a := a) (d := d) m hs) p := by
  constructor
  · intro ht
    apply (evaluationEquiv hg d).injective
    funext j
    exact (ht j).trans ((transported_binary_at_point (frobeniusPower m) hb hg _ bits p hp j).symm)
  · rintro rfl
    exact transported_binary_at_point (frobeniusPower m) hb hg _ bits p hp

/-- An address in an affine coset is its anchor plus a binary subset sum. -/
theorem enumerates_coset {β : ℕ → F} {n : ℕ} {V : AddSubgroup F}
    (enumerates : ∀ z, (∃ i : Digits n, address β n 0 i = z) ↔ z ∈ V) (a z : F) :
    (∃ i : Digits n, address β n a i = z) ↔ z - a ∈ V := by
  have shift (i : Digits n) : address β n a i = a + address β n 0 i := by
    simpa only [add_zero] using translate_address β n a 0 i
  constructor
  · rintro ⟨i,rfl⟩
    rw [shift, add_sub_cancel_left]
    exact (enumerates _).mp ⟨i,rfl⟩
  · intro h
    obtain ⟨i,hi⟩ := (enumerates (z-a)).mpr h
    exact ⟨i, by rw [shift, hi, add_sub_cancel]⟩

/-- Frobenius stability of the direction space and membership of the actual
anchor offset suffice for complete conjugate support, in arbitrary bases. -/
theorem stable_coset_support (σ : F ≃+* F) {β γ : ℕ → F} {n : ℕ}
    {a d : F} {V : AddSubgroup F}
    (hβ : ∀ z, (∃ i : Digits n, address β n 0 i = z) ↔ z ∈ V)
    (hγ : ∀ z, (∃ i : Digits n, address γ n 0 i = z) ↔ z ∈ V)
    (stable : ∀ z, z ∈ V ↔ σ z ∈ V) (offset : σ a - d ∈ V) :
    SameSupport (n := n) σ β γ a d := by
  intro z
  rw [enumerates_coset hγ d z]
  constructor
  · rintro ⟨i,rfl⟩
    have hx := (enumerates_coset hβ a (address β n a i)).mp ⟨i,rfl⟩
    have hσ := (stable _).mp hx
    rw [map_sub] at hσ
    simpa only [sub_add_sub_cancel] using V.add_mem hσ offset
  · intro hz
    have hd := V.sub_mem hz offset
    have hd' : z - σ a ∈ V := by
      simpa only [sub_sub_sub_cancel_right] using hd
    have pre : σ.symm z - a ∈ V := (stable _).mpr (by
      rwa [map_sub, RingEquiv.apply_symm_apply])
    obtain ⟨i,hi⟩ := (enumerates_coset hβ a (σ.symm z)).mpr pre
    exact ⟨i,by rw [hi, RingEquiv.apply_symm_apply]⟩

theorem reverse_support (σ : F ≃+* F) {β γ : ℕ → F} {n : ℕ} {a d : F}
    (hs : SameSupport (n := n) σ β γ a d) : SameSupport (n := n) σ.symm γ β d a := by
  intro z
  constructor
  · rintro ⟨j,hj⟩
    have hpoint : address γ n d j = σ z := (σ.symm_apply_eq.mp hj)
    obtain ⟨i,hi⟩ := (hs (σ z)).mpr ⟨j,hpoint⟩
    exact ⟨i,σ.injective hi⟩
  · rintro ⟨i,rfl⟩
    obtain ⟨j,hj⟩ := (hs _).mp ⟨i,rfl⟩
    exact ⟨j,σ.symm_apply_eq.mpr hj⟩

/-- Re-evaluating in the target basis and transporting back with the inverse
automorphism exactly restores an arbitrary source row, including its order. -/
theorem reverse_transport (σ : F ≃+* F) {β γ : ℕ → F} {n : ℕ} {a d : F}
    (hb : independentDirections β n) (hg : independentDirections γ n)
    (hs : SameSupport (n := n) σ β γ a d) (p : Row F n) :
    transport σ.symm hg hb (reverse_support σ hs) (transport σ hb hg hs p) = p := by
  apply (evaluationEquiv hb a).injective
  funext i
  change forward β n a _ i = forward β n a p i
  rw [transport_at_point, transport_at_point, RingEquiv.symm_apply_apply]
  congr 1
  apply address_injective hb a
  apply σ.injective
  rw [sourceDigit_spec]
  exact σ.symm_apply_eq.mp (sourceDigit_spec σ.symm hg (reverse_support σ hs) i)

/-- In a Frobenius-stable additive subspace, the source remainder and the
actual offset of the target anchor determine every conjugate binary remainder. -/
theorem finite_stable_coset_remainder [Finite F] (m : ℕ) {n : ℕ}
    {β γ : ℕ → F} {V : AddSubgroup F} {a d : F}
    (hb : independentDirections β n) (hg : independentDirections γ n)
    (hβ : ∀ z, (∃ i : Digits n, address β n 0 i = z) ↔ z ∈ V)
    (hγ : ∀ z, (∃ i : Digits n, address γ n 0 i = z) ↔ z ∈ V)
    (stable : ∀ z, z ∈ V ↔ z ^ ((2 : ℕ) ^ m) ∈ V)
    (offset : a ^ ((2 : ℕ) ^ m) - d ∈ V)
    (bits : List Bool) (p : Row F n)
    (hp : ∀ i, forward β n a p i = binaryHorner bits (address β n a i)) :
    ∃! t : Row F n, ∀ j, forward γ n d t j = binaryHorner bits (address γ n d j) := by
  have hs := stable_coset_support (frobeniusPower m) hβ hγ
    (by simpa only [frobeniusPower_apply] using stable)
    (a := a) (d := d) (by simpa only [frobeniusPower_apply] using offset)
  exact binary_remainder_transport (frobeniusPower m) hb hg hs bits p hp

#print axioms stable_coset_support
#print axioms reverse_transport
#print axioms finite_stable_coset_remainder
#print axioms address_injective
#print axioms transported_binary_at_point
#print axioms finite_frobenius_remainder
#print axioms unique_source_digit
#print axioms sourceDigit_bijective
#print axioms transport_at_point
#print axioms binaryHorner_conjugate
#print axioms binary_remainder_transport
end Moonshot.BundleTransport
