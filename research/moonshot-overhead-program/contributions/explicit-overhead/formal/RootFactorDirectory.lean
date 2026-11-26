import Mathlib.FieldTheory.Finite.Basic
import Mathlib.FieldTheory.Minpoly.Field
import Mathlib.RingTheory.Ideal.Quotient.Operations
import Mathlib.RingTheory.Coprime.Lemmas
import Mathlib.Algebra.Polynomial.RingDivision

/-! # Matching point values to polynomial remainders in the binary directory -/
namespace Moonshot.RootFactorDirectory
open Polynomial Function
open scoped Polynomial BigOperators

variable {k K : Type*} [Field k] [Field K] [Algebra k K]

theorem recover_literal_remainder {x : K} (hx : IsIntegral k x)
    (f r : k[X]) (hr : r.degree < (minpoly k x).degree) :
    r.aeval x = f.aeval x ↔ r = f %ₘ minpoly k x := by
  constructor
  · intro h
    have div : minpoly k x ∣ r - f := minpoly.dvd_iff.mpr (by rw [map_sub,h,sub_self])
    have eq := modByMonic_eq_of_dvd_sub (minpoly.monic hx) div
    rwa [(modByMonic_eq_self_iff (minpoly.monic hx)).2 hr] at eq
  · rintro rfl
    exact minpoly.aeval_modByMonic_minpoly f x

theorem at_conjugate (g : K ≃ₐ[k] K) (x : K) (f : k[X]) :
    minpoly k (g x) = minpoly k x ∧ f.aeval (g x) = g (f.aeval x) :=
  ⟨minpoly.algEquiv_eq g x, aeval_algHom_apply g.toAlgHom x f⟩

/-- Agreement at an orbit-covering set forces equality of low-degree inputs. -/
theorem selected_points_injective [Fintype K] (sel : Set K)
    (cover : ∀ z : K, ∃ x ∈ sel, ∃ g : K ≃ₐ[k] K, g x = z)
    (f h : k[X]) (hf : f.natDegree < Fintype.card K) (hh : h.natDegree < Fintype.card K)
    (he : ∀ x ∈ sel, f.aeval x = h.aeval x) : f = h := by
  have allpts (z : K) : f.aeval z = h.aeval z := by
    obtain ⟨x, hx, g, rfl⟩ := cover z
    rw [(at_conjugate g x f).2, (at_conjugate g x h).2, he x hx]
  have small : (f-h).natDegree < Fintype.card K :=
    lt_of_le_of_lt (natDegree_sub_le ..) (max_lt hf hh)
  have zero : ((f-h).map (algebraMap k K)) = 0 := by
    apply eq_zero_of_natDegree_lt_card_of_eval_eq_zero _ Function.injective_id
    · intro x
      change ((f-h).map (algebraMap k K)).eval x=0
      rw [eval_map_algebraMap, map_sub, allpts x, sub_self]
    · exact lt_of_le_of_lt (natDegree_map_le ..) small
  exact sub_eq_zero.mp ((Polynomial.map_eq_zero_iff (algebraMap k K).injective).mp zero)

variable {ι : Type*} [Fintype ι]

/-- All independently chosen reduced records have a unique canonical lift. -/
theorem independent_directory (m r : ι → k[X]) (hm : ∀ i, (m i).Monic)
    (hc : Pairwise fun i j => IsCoprime (m i) (m j))
    (hr : ∀ i, (r i).degree < (m i).degree) :
    ∃! f : k[X], f.degree < (∏ i, m i).degree ∧ ∀ i, f %ₘ m i = r i := by
  classical
  let M := ∏ i, m i
  have hM : M.Monic := monic_prod_of_monic _ _ (fun i _ => hm i)
  have hdvd (i : ι) : m i ∣ M := Finset.dvd_prod_of_mem _ (Finset.mem_univ i)
  let I (i : ι) : Ideal k[X] := Ideal.span {m i}
  have hI : Pairwise fun i j => IsCoprime (I i) (I j) :=
    fun i j hij => (Ideal.isCoprime_span_singleton_iff _ _).mpr (hc hij)
  obtain ⟨u, hu⟩ := Ideal.exists_forall_sub_mem_ideal hI r
  have du (i : ι) : m i ∣ u-r i := Ideal.mem_span_singleton.mp (hu i)
  have normalized (i : ι) : (u %ₘ M) %ₘ m i = r i := by
    calc
      _ = u %ₘ m i := modByMonic_eq_of_dvd_sub (hm i) ((hdvd i).trans (dvd_modByMonic_sub u M))
      _ = r i %ₘ m i := modByMonic_eq_of_dvd_sub (hm i) (du i)
      _ = _ := (modByMonic_eq_self_iff (hm i)).2 (hr i)
  refine ⟨u %ₘ M, ⟨degree_modByMonic_lt u hM,normalized⟩, ?_⟩
  rintro v ⟨hv, hres⟩
  have all (i : ι) : m i ∣ v-u := by
    have h1 := dvd_modByMonic_sub v (m i)
    rw [hres i] at h1
    have eq : v-u = -((r i)-v) - (u-r i) := by abel
    rw [eq]
    exact dvd_sub (dvd_neg.mpr h1) (du i)
  have bulk : M ∣ v-u := Fintype.prod_dvd_of_coprime hc all
  have eq := modByMonic_eq_of_dvd_sub hM bulk
  rwa [(modByMonic_eq_self_iff hM).2 hv] at eq

#print axioms recover_literal_remainder
#print axioms at_conjugate
#print axioms selected_points_injective
#print axioms independent_directory
end Moonshot.RootFactorDirectory
