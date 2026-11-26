import RootFactorDirectory
import Mathlib.FieldTheory.Finite.Extension
import Mathlib.FieldTheory.Finite.GaloisField

/-! The literal binary factor inventory and its product reconstruction. -/
namespace Moonshot.RootFactorDirectory
open Polynomial Function
open scoped Polynomial BigOperators

/-- The distinct actual FS1 factors of a binary vanishing polynomial. -/
noncomputable def binaryFactors (b : ℕ) : Finset (ZMod 2)[X] :=
  (UniqueFactorizationMonoid.normalizedFactors (X^(2^b)-X : (ZMod 2)[X])).toFinset

private theorem vanishing_ne {b : ℕ} (hb : 0<b) : (X^(2^b)-X : (ZMod 2)[X]) ≠ 0 :=
  FiniteField.X_pow_card_pow_sub_X_ne_zero (ZMod 2) hb.ne' (by decide : 1<2)

private theorem vanishing_monic {b : ℕ} (hb : 0<b) : (X^(2^b)-X : (ZMod 2)[X]).Monic := by
  apply (monic_X_pow (2^b)).sub_of_left
  rw [degree_X, degree_X_pow]
  exact_mod_cast Nat.one_lt_two_pow hb.ne'

theorem binary_factor_iff {b : ℕ} (hb : 0<b) (u : (ZMod 2)[X]) :
    u ∈ binaryFactors b ↔ Irreducible u ∧ u.Monic ∧ u.natDegree ∣ b := by
  classical
  simp only [binaryFactors, Multiset.mem_toFinset, Polynomial.mem_normalizedFactors_iff (vanishing_ne hb)]
  constructor
  · rintro ⟨hi,hm,hd⟩
    exact ⟨hi,hm,hi.natDegree_dvd_of_dvd_X_pow_card_pow_sub_X (by simpa only [Nat.card_zmod] using hd)⟩
  · rintro ⟨hi,hm,hd⟩
    exact ⟨hi,hm,by simpa only [Nat.card_zmod] using hi.natDegree_dvd_iff_dvd_X_pow_card_pow_sub_X.mp hd⟩

theorem binary_factor_product {b : ℕ} (hb : 0<b) :
    ∏ u : binaryFactors b, (u : (ZMod 2)[X]) = X^(2^b)-X := by
  classical
  let V := (X^(2^b)-X : (ZMod 2)[X])
  have nonzero : V ≠ 0 := vanishing_ne hb
  have divisor : 2 ∣ 2^b := dvd_pow_self 2 hb.ne'
  have simple : (UniqueFactorizationMonoid.normalizedFactors V).Nodup :=
    (UniqueFactorizationMonoid.squarefree_iff_nodup_normalizedFactors nonzero).mp
      (galois_poly_separable 2 (2^b) divisor).squarefree
  have hp := leadingCoeff_mul_prod_normalizedFactors V
  rw [show V.leadingCoeff=1 from vanishing_monic hb, C_1, one_mul] at hp
  change (∏ u : binaryFactors b, id (u : (ZMod 2)[X])) = V
  calc
    _ = (binaryFactors b).prod id := Finset.prod_coe_sort (binaryFactors b) id
    _ = (binaryFactors b).val.prod := (Finset.prod_val (binaryFactors b)).symm
    _ = (UniqueFactorizationMonoid.normalizedFactors V).prod := by
      exact congrArg Multiset.prod (Multiset.dedup_eq_self.mpr simple)
    _ = V := hp

/-- Every legal assignment on the actual distinct binary irreducibles of
degrees dividing b has a unique contiguous polynomial below length 2^b. -/
theorem binary_directory_lift {b : ℕ} (hb : 0<b)
    (r : binaryFactors b → (ZMod 2)[X]) (hr : ∀ u, (r u).degree < u.val.degree) :
    ∃! f : (ZMod 2)[X], f.degree < ((2^b : ℕ) : WithBot ℕ) ∧
      ∀ u : binaryFactors b, f %ₘ u.val = r u := by
  have fact (u : binaryFactors b) := (binary_factor_iff hb u).mp u.property
  have cop : Pairwise fun u v : binaryFactors b => IsCoprime u.val v.val := by
    intro u v h
    rcases (fact u).1.isCoprime_or_dvd v.val with ok | bad
    · exact ok
    · exact False.elim (h (Subtype.ext (eq_of_monic_of_associated (fact u).2.1
        (fact v).2.1 ((fact u).1.associated_of_dvd (fact v).1 bad))))
  have ex := independent_directory (fun u : binaryFactors b => u.val) r
    (fun u => (fact u).2.1) cop hr
  rw [binary_factor_product hb, degree_eq_natDegree (vanishing_ne hb),
    FiniteField.X_pow_card_pow_sub_X_natDegree_eq (ZMod 2) hb.ne' (by decide : 1<2)] at ex
  exact ex

/-- Pointwise multiplication in the actual factor directory followed by its
canonical inverse returns the full ordinary binary polynomial product whenever it fits. -/
theorem binary_directory_product {b : ℕ} (hb : 0<b) (f g h : (ZMod 2)[X])
    (hfg : (f*g).degree < ((2^b : ℕ) : WithBot ℕ))
    (hh : h.degree < ((2^b : ℕ) : WithBot ℕ))
    (rows : ∀ u : binaryFactors b,
      h %ₘ u.val = ((f %ₘ u.val) * (g %ₘ u.val)) %ₘ u.val) : h = f*g := by
  let r := fun u : binaryFactors b => ((f %ₘ u.val)*(g %ₘ u.val)) %ₘ u.val
  have hr (u : binaryFactors b) : (r u).degree < u.val.degree :=
    degree_modByMonic_lt _ ((binary_factor_iff hb u).mp u.property).2.1
  have unique := binary_directory_lift hb r hr
  exact unique.unique ⟨hh, rows⟩ ⟨hfg, fun u => mul_modByMonic f g u.val⟩

/-- An orbit-covering choice of actual field points reaches exactly the irreducibles
of degrees dividing b, including the proper subfields. -/
theorem binary_factor_at_selected {K : Type*} [Field K] [Fintype K]
    [Algebra (ZMod 2) K] {b : ℕ} (hb : 0<b) (hc : Fintype.card K = 2^b)
    (sel : Set K) (cover : ∀ z : K, ∃ x ∈ sel, ∃ g : K ≃ₐ[ZMod 2] K, g x=z)
    (u : (ZMod 2)[X]) :
    u ∈ binaryFactors b ↔ ∃ x ∈ sel, minpoly (ZMod 2) x = u := by
  classical
  let V : (ZMod 2)[X] := X^(2^b)-X
  have mem : u ∈ binaryFactors b ↔ Irreducible u ∧ u.Monic ∧ u ∣ V := by
    simp only [binaryFactors, Multiset.mem_toFinset, Polynomial.mem_normalizedFactors_iff (vanishing_ne hb)]
    rfl
  constructor
  · intro hu
    obtain ⟨hi,hm,hd⟩ := mem.mp hu
    have splits : (V.map (algebraMap (ZMod 2) K)).Splits := by
      change ((X^(2^b)-X : (ZMod 2)[X]).map _).Splits
      rw [←hc]
      exact FiniteField.splits_X_pow_card_sub_X 2
    have hnz : V.map (algebraMap (ZMod 2) K) ≠ 0 :=
      (Polynomial.map_ne_zero_iff (algebraMap (ZMod 2) K).injective).mpr (vanishing_ne hb)
    have us := splits.of_dvd hnz (map_dvd (Polynomial.mapRingHom (algebraMap (ZMod 2) K)) hd)
    change (u.map (algebraMap (ZMod 2) K)).Splits at us
    obtain ⟨z,hz⟩ := us.exists_eval_eq_zero (by
      rw [degree_map_eq_of_injective (algebraMap (ZMod 2) K).injective]
      exact (degree_pos_of_irreducible hi).ne')
    obtain ⟨x,hx,g,rfl⟩ := cover z
    exact ⟨x,hx, (at_conjugate g x u).1.symm.trans
      (minpoly.eq_of_irreducible_of_monic hi (by simpa only [eval_map_algebraMap] using hz) hm).symm⟩
  · rintro ⟨x,_,rfl⟩
    have hx := Algebra.IsIntegral.isIntegral (R := ZMod 2) x
    refine mem.mpr ⟨minpoly.irreducible hx, minpoly.monic hx, minpoly.dvd_iff.mpr ?_⟩
    change aeval x (X^(2^b)-X : (ZMod 2)[X]) = 0
    simp only [map_sub, map_pow, aeval_X, ← hc, FiniteField.pow_card, sub_self]

#print axioms binary_factor_at_selected
#print axioms binary_directory_product
#print axioms binary_factor_iff
#print axioms binary_factor_product
#print axioms binary_directory_lift

end Moonshot.RootFactorDirectory
