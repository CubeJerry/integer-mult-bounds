import GroupedComposition

/-! The fixed ambient monomial word for a grouped residue is a coefficient
of the ordinary remainder on the selected fibre, after scalar extension. -/
open Polynomial
open scoped Polynomial BigOperators

namespace Moonshot.GroupedAmbientWords
open Moonshot.GroupedComposition

variable {F K : Type*} [Field F] [Field K]

private theorem mapped_grouped (ι : F →+* K) (S : F[X]) (hS : S.Monic) (g : ℕ → F[X]) :
    (grouped S g).map ι = grouped (S.map ι) (fun k => (g k).map ι) := by
  classical
  unfold grouped
  simp only [Polynomial.map_sum, Polynomial.map_mul, Polynomial.map_pow, map_X, map_comp,
    hS.natDegree_map ι]

/-- Reduction by the actual fibre polynomial produces ambient monomial coordinates. -/
theorem fibre_remainder (S : K[X]) (hS : S.Monic) (hv : 0 < S.natDegree)
    (s : K) (g : ℕ → K[X]) :
    grouped S g %ₘ (S - C s) =
      ∑ k ∈ Finset.range S.natDegree, X ^ k * C ((g k).eval s) := by
  have h := (actual_grouped_division (X - C s) S (monic_X_sub_C s) hS
    (by simp) hv g).2
  simpa [grouped, sub_comp, modByMonic_X_sub_C_eq_C_eval] using h

/-- The grouped binary remainder obtained by the original division theorem
has, on scalar extension and ordinary fibre division, exactly the
monomial coefficients emitted using the prescribed root. -/
theorem grouped_then_fibre (ι : F →+* K) (m S : F[X]) (hm : m.Monic) (hS : S.Monic)
    (hmpos : 0 < m.natDegree) (hv : 0 < S.natDegree) (s : K) (g : ℕ → F[X]) :
    ((grouped S g %ₘ (m.comp S)).map ι) %ₘ (S.map ι - C s) =
      ∑ k ∈ Finset.range S.natDegree, X ^ k * C ((g k %ₘ m).eval₂ ι s) := by
  rw [(actual_grouped_division m S hm hS hmpos hv g).2, mapped_grouped ι S hS]
  rw [fibre_remainder _ (hS.map ι) (by simpa [hS.natDegree_map ι] using hv)]
  simp only [hS.natDegree_map ι, eval_map]

/-- The word at index k in the ordered stream equals the actual kth monomial coefficient. -/
theorem grouped_fibre_coefficient (ι : F →+* K) (m S : F[X]) (hm : m.Monic) (hS : S.Monic)
    (hmpos : 0 < m.natDegree) (hv : 0 < S.natDegree) (s : K) (g : ℕ → F[X])
    (k : ℕ) (hk : k < S.natDegree) :
    (((grouped S g %ₘ (m.comp S)).map ι) %ₘ (S.map ι - C s)).coeff k =
      (g k %ₘ m).eval₂ ι s := by
  classical
  rw [grouped_then_fibre ι m S hm hS hmpos hv s g]
  simp [coeff_X_pow, hk]

/-- At a root of the group minimal polynomial every orbit residue yields the
same ambient word as the original coefficient polynomial. No rank or basis
assumption is needed for this literal division identity. -/
theorem grouped_and_full_same_fibre (ι : F →+* K) (m S : F[X]) (hm : m.Monic)
    (hS : S.Monic) (hmpos : 0 < m.natDegree) (hv : 0 < S.natDegree)
    (s : K) (hs : m.eval₂ ι s = 0) (g : ℕ → F[X]) :
    ((grouped S g %ₘ (m.comp S)).map ι) %ₘ (S.map ι - C s) =
      (grouped S g).map ι %ₘ (S.map ι - C s) := by
  rw [grouped_then_fibre ι m S hm hS hmpos hv s g, mapped_grouped ι S hS]
  rw [fibre_remainder _ (hS.map ι) (by simpa [hS.natDegree_map ι] using hv)]
  simp only [hS.natDegree_map ι, eval_map,
    eval₂_modByMonic_eq_self_of_root hs]

#print axioms Moonshot.GroupedAmbientWords.fibre_remainder
#print axioms Moonshot.GroupedAmbientWords.grouped_then_fibre
#print axioms Moonshot.GroupedAmbientWords.grouped_fibre_coefficient
#print axioms Moonshot.GroupedAmbientWords.grouped_and_full_same_fibre

end Moonshot.GroupedAmbientWords
