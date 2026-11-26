import TraceCoefficientPrefix
import Mathlib.RingTheory.Polynomial.DegreeLT
import Mathlib.Algebra.Polynomial.RingDivision
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas

/-!
# Coefficient-band rank for powers of the trace radix

`bandMap` reads the actual consecutive ordinary coefficients of a polynomial
product. The top two blocks of a product evolve linearly under the next
multiplication. This gives the upper-right block rank without constructing
a Toeplitz matrix or enumerating a field.
-/

namespace Moonshot.TraceRadixRank
open Polynomial
open scoped Polynomial

variable {F : Type*} [Field F]

private noncomputable abbrev Word (F : Type*) [Field F] (h : ℕ) := Polynomial.degreeLT F h

private theorem word_natDegree {h : ℕ} (hh : 0 < h) (x : Word F h) :
    (x : F[X]).natDegree < h := by
  by_cases hz : (x : F[X]) = 0
  · simpa only [hz, natDegree_zero] using hh
  · exact (natDegree_lt_iff_degree_lt hz).mpr (mem_degreeLT.mp x.property)

/-- A literal output band in increasing ordinary coefficient order. -/
noncomputable def bandMap (h start : ℕ) (g : F[X]) :
    Polynomial.degreeLT F h →ₗ[F] (Fin h → F) where
  toFun x i := (g * (x : F[X])).coeff (start + i.val)
  map_add' x y := by ext i; simp [mul_add]
  map_smul' c x := by ext i; simp

private noncomputable def low (h : ℕ) (e : F[X]) : Word F h →ₗ[F] Word F h where
  toFun x := ⟨(e * (x : F[X])) %ₘ X^h, mem_degreeLT.mpr (by
    simpa only [degree_X_pow] using degree_modByMonic_lt (e * (x : F[X])) (monic_X_pow (R := F) h))⟩
  map_add' x y := by ext1; simp [mul_add, add_modByMonic]
  map_smul' c x := by ext1; simp [smul_modByMonic]

private noncomputable def feedbackMap (h : ℕ) (hh : 2 ≤ h) (e : F[X])
    (he : e.natDegree ≤ h/2) : Word F h →ₗ[F] Word F h where
  toFun x := ⟨(e * (x : F[X])) /ₘ X^h, mem_degreeLT.mpr (by
    rw [← degree_X_pow (R := F) h]
    apply degree_lt_degree
    rw [natDegree_divByMonic _ (monic_X_pow h), natDegree_X_pow]
    have := natDegree_mul_le (p := e) (q := (x : F[X]))
    have := word_natDegree (by omega) x
    omega)⟩
  map_add' x y := by ext1; simp [mul_add, add_divByMonic]
  map_smul' c x := by ext1; simp [smul_divByMonic]

private noncomputable def upper (h : ℕ) (hh : 2 ≤ h) (e : F[X]) (he : e.natDegree ≤ h/2) :=
  LinearMap.id (R := F) (M := Word F h) + feedbackMap h hh e he

private theorem upper_coe {h : ℕ} (hh : 2 ≤ h) (e : F[X]) (he : e.natDegree ≤ h/2)
    (x : Word F h) : (upper h hh e he x : F[X]) = (x : F[X]) + (e*(x : F[X])) /ₘ X^h := rfl

private theorem low_coe (h : ℕ) (e : F[X]) (x : Word F h) :
    (low h e x : F[X]) = (e*(x : F[X])) %ₘ X^h := rfl

private theorem word_split {h : ℕ} (hh : 2 ≤ h) (e : F[X]) (he : e.natDegree ≤ h/2)
    (x : Word F h) : (X^h+e)*(x : F[X]) =
      X^h*(upper h hh e he x : F[X]) + (low h e x : F[X]) := by
  rw [upper_coe, low_coe]
  linear_combination -(modByMonic_add_div (e * (x : F[X])) (X^h))

variable [CharP F 2]

private theorem upper_involution {h : ℕ} (hh : 2 ≤ h) (e : F[X]) (he : e.natDegree ≤ h / 2) :
    Function.Involutive (upper h hh e he) := by
  intro x
  apply Subtype.ext
  rw [upper_coe, upper_coe, mul_add, add_divByMonic]
  have hn := CoefficientPrefix.feedback_square_zero hh he (word_natDegree (by omega) x)
  change (e*(e*(x : F[X]) /ₘ X^h)) /ₘ X^h = 0 at hn
  rw [hn, add_zero, add_assoc, CharTwo.add_self_eq_zero, add_zero]

omit [CharP F 2] in
private theorem word_finrank (h : ℕ) : Module.finrank F (Word F h) = h := by
  simpa [Module.finrank_pi] using (degreeLTEquiv F h).finrank_eq


private noncomputable def shiftWord {z h : ℕ} (hz : z ≤ h) : Word F z →ₗ[F] Word F h where
  toFun x := ⟨X^(h-z)*(x : F[X]), mem_degreeLT.mpr (by
    rw [degree_mul, degree_X_pow]
    calc
      _ < (↑(h-z) : WithBot ℕ) + ↑z := WithBot.add_lt_add_left (by simp) (mem_degreeLT.mp x.property)
      _ = h := by rw [← Nat.cast_add, Nat.sub_add_cancel hz])⟩
  map_add' x y := by ext1; simp [mul_add]
  map_smul' c x := by ext1; simp

omit [CharP F 2] in
private theorem shiftWord_injective {z h : ℕ} (hz : z ≤ h) :
    Function.Injective (shiftWord (F := F) hz) := by
  intro x y heq
  have heq' := congrArg Subtype.val heq
  change X^(h-z)*(x : F[X]) = X^(h-z)*(y : F[X]) at heq'
  exact Subtype.ext (mul_left_cancel₀ (pow_ne_zero _ X_ne_zero) heq')

omit [CharP F 2] in
private theorem mem_shift_range {z h : ℕ} (hz : z ≤ h) (x : Word F h) :
    x ∈ LinearMap.range (shiftWord (F := F) hz) ↔ X^(h-z) ∣ (x : F[X]) := by
  constructor
  · rintro ⟨y,rfl⟩
    exact ⟨(y : F[X]),rfl⟩
  · rintro ⟨u,hu⟩
    have hu' : u.degree < (z : WithBot ℕ) := by
      have hd := mem_degreeLT.mp x.property
      rw [hu, degree_mul, degree_X_pow] at hd
      by_contra! hn
      have hle : (↑(h-z) : WithBot ℕ) + ↑z ≤ ↑(h-z) + u.degree := by gcongr
      rw [← Nat.cast_add, Nat.sub_add_cancel hz] at hle
      exact (not_le_of_gt hd) hle
    exact ⟨⟨u,mem_degreeLT.mpr hu'⟩, Subtype.ext hu.symm⟩

omit [CharP F 2] in
private theorem Xpow_dvd_of_trailing {n : ℕ} {g : F[X]} (hg : g ≠ 0) :
    X^n ∣ g ↔ n ≤ g.natTrailingDegree := by
  simpa [rootMultiplicity_eq_natTrailingDegree] using
    (le_rootMultiplicity_iff (a := (0:F)) (n := n) hg).symm

omit [CharP F 2] in
private theorem low_rank {z h : ℕ} (hz : z ≤ h) (e : F[X])
    (hne : e ≠ 0) (htr : e.natTrailingDegree = z) :
    Module.finrank F (LinearMap.range (low h e)) = h-z := by
  have hker : (low h e).ker = (shiftWord (F := F) hz).range := by
    ext x
    rw [mem_shift_range, LinearMap.mem_ker]
    constructor
    · intro hx
      by_cases h0 : (x : F[X]) = 0
      · simp [h0]
      have hh := congrArg Subtype.val hx
      change (e*(x : F[X])) %ₘ X^h = 0 at hh
      rw [modByMonic_eq_zero_iff_dvd (monic_X_pow h), Xpow_dvd_of_trailing (mul_ne_zero hne h0),
        natTrailingDegree_mul hne h0, htr] at hh
      apply (Xpow_dvd_of_trailing h0).2
      omega
    · intro hx
      apply Subtype.ext
      change (e*(x : F[X])) %ₘ X^h = 0
      rw [modByMonic_eq_zero_iff_dvd (monic_X_pow h)]
      by_cases h0 : (x : F[X]) = 0
      · simp [h0]
      rw [Xpow_dvd_of_trailing h0] at hx
      rw [Xpow_dvd_of_trailing (mul_ne_zero hne h0), natTrailingDegree_mul hne h0, htr]
      omega
  have dim := (low h e).finrank_range_add_finrank_ker
  rw [hker, LinearMap.finrank_range_of_inj (shiftWord_injective hz), word_finrank, word_finrank] at dim
  omega


/-- Highest and next-highest length-h blocks. The leading column comes first
in this proof state; `bandMap` always uses the original increasing order. -/
private def step {V : Type*} [AddCommMonoid V] [Module F V]
    (a f : V →ₗ[F] V) (state : V × V) : V × V :=
  (a state.1, f state.1 + a state.2)

private def stage {V : Type*} [AddCommMonoid V] [Module F V]
    (a f : V →ₗ[F] V) (x : V) : ℕ → V × V
  | 0 => (a x, f x)
  | n+1 => step a f (stage a f x n)

private theorem word_add_self {h : ℕ} (x : Word F h) : x + x = 0 := by
  apply Subtype.ext
  exact CharTwo.add_self_eq_zero (x : F[X])

omit [CharP F 2] in
private theorem two_steps {h : ℕ} (a f : Word F h →ₗ[F] Word F h)
    (ha : Function.Involutive a) (t l : Word F h) :
    step a f (step a f (t,l)) = (t, (f (a t)+a (f t)) + l) := by
  simp [step, map_add, ha t, ha l, add_assoc]

private theorem stage_density {h : ℕ} (a f : Word F h →ₗ[F] Word F h)
    (ha : Function.Involutive a) (x : Word F h) (p : ℕ) :
    (stage a f x (2*p)).2 = if p%2=0 then f x else a (f (a x)) := by
  have periodic (n : ℕ) : stage a f x (n+4) = stage a f x n := by
    change step a f (step a f (step a f (step a f (stage a f x n)))) = _
    obtain ⟨t,l⟩ := stage a f x n
    rw [two_steps a f ha, two_steps a f ha, ← add_assoc, word_add_self, zero_add]
  induction p using Nat.twoStepInduction with
  | zero => simp [stage]
  | one =>
    change (step a f (step a f (a x, f x))).2 = _
    rw [two_steps a f ha, ha x]
    simp only [Nat.reduceMod, one_ne_zero, ↓reduceIte]
    rw [add_comm (f x), add_assoc, word_add_self, add_zero]
  | more p hp _ =>
    rw [show 2*(p+2) = 2*p+4 by omega, periodic, hp]
    simp

omit [CharP F 2] in
private theorem degree_upper {h : ℕ} (e : F[X]) (he : e.natDegree ≤ h/2) :
    (X^h+e).degree ≤ (h : WithBot ℕ) := by
  apply (degree_add_le ..).trans
  rw [degree_X_pow]
  exact max_le le_rfl (degree_le_natDegree.trans (by exact_mod_cast (show e.natDegree ≤ h by omega)))

omit [CharP F 2] in
private theorem shifted_lt {u w : ℕ} {P : F[X]} (hd : P.degree < (w : WithBot ℕ)) :
    (X^u*P).degree < ↑(u+w) := by
  rw [degree_mul, degree_X_pow, Nat.cast_add]
  exact WithBot.add_lt_add_left (by simp) hd

omit [CharP F 2] in
private theorem stage_decomposition {h : ℕ} (hh : 2 ≤ h) (e : F[X]) (he : e.natDegree ≤ h/2)
    (x : Word F h) (n : ℕ) :
    let st := stage (upper h hh e he) (low h e) x n
    ∃ t : F[X], (X^h+e)^(n+1) * (x : F[X]) =
      X^(h*(n+1))*(st.1 : F[X]) + X^(h*n)*(st.2 : F[X]) + t ∧ t.degree < ↑(h*n) := by
  dsimp only
  induction n with
  | zero =>
    refine ⟨0, ?_, by simp⟩
    simpa [stage] using word_split hh e he x
  | succ n ih =>
    let st := stage (upper h hh e he) (low h e) x n
    obtain ⟨t,eq,ht⟩ := ih
    let tail := X^(h*n)*(low h e st.2 : F[X]) + (X^h+e)*t
    refine ⟨tail, ?_, ?_⟩
    · rw [pow_succ' (X^h+e) (n+1), mul_assoc, eq]
      change (X^h+e)*(X^(h*(n+1))*(st.1 : F[X]) + X^(h*n)*(st.2 : F[X]) + t) =
        X^(h*(n+1+1))*(upper h hh e he st.1 : F[X]) +
        X^(h*(n+1))*((low h e st.1 : F[X]) + (upper h hh e he st.2 : F[X])) + tail
      have high := word_split hh e he st.1
      have lower := word_split hh e he st.2
      simp only [Nat.mul_add, Nat.mul_one, pow_add, tail] at *
      linear_combination X^(h*n)*X^h*high + X^(h*n)*lower
    · apply (degree_add_le ..).trans_lt (max_lt ?_ ?_)
      · rw [Nat.mul_succ]
        exact shifted_lt (mem_degreeLT.mp (low h e st.2).property)
      · rw [degree_mul, Nat.mul_succ, add_comm (h*n) h, Nat.cast_add]
        calc
          _ ≤ (h : WithBot ℕ) + t.degree := by gcongr; exact degree_upper e he
          _ < _ := WithBot.add_lt_add_left (by simp) ht


omit [CharP F 2] in
private theorem band_state {h : ℕ} (hh : 2 ≤ h) (e : F[X]) (he : e.natDegree ≤ h/2)
    (x : Word F h) (n : ℕ) : bandMap h (h*n) ((X^h+e)^(n+1)) x =
    (degreeLTEquiv F h) (stage (upper h hh e he) (low h e) x n).2 := by
  obtain ⟨t,eq,ht⟩ := stage_decomposition hh e he x n
  ext i
  change (((X^h+e)^(n+1))*(x : F[X])).coeff (h*n+i.val) = _
  rw [eq, coeff_add, coeff_add]
  have hcut : ¬h*(n+1) ≤ h*n+i.val := by rw [Nat.mul_succ]; have := i.isLt; omega
  have htail : t.coeff (h*n+i.val) = 0 := by
    apply coeff_eq_zero_of_degree_lt (ht.trans_le ?_)
    exact_mod_cast Nat.le_add_right (h*n) i.val
  rw [htail, add_zero, coeff_X_pow_mul', ite_eq_right hcut, zero_add,
    Nat.add_comm (h*n) i.val, coeff_X_pow_mul]
  rfl

omit [CharP F 2] in
private theorem rank_conjugate {h : ℕ} (a f : Word F h →ₗ[F] Word F h)
    (ha : Function.Involutive a) :
    Module.finrank F (a.comp (f.comp a)).range = Module.finrank F f.range := by
  rw [LinearMap.range_comp, LinearMap.range_comp_of_range_eq_top f (LinearMap.range_eq_top.mpr ha.surjective)]
  exact (LinearEquiv.ofInvolutive a ha).finrank_map_eq f.range

/-- For any divisor with a half-degree gap and residual valuation z, the
actual middle band of every odd power has rank h−z, over any binary field.
The input covers all ordinary polynomials of length h, with no promise on
its coefficients. -/
theorem odd_power_band_rank {h z : ℕ} (hh : 2 ≤ h) (hz : z ≤ h)
    (e : F[X]) (he : e.natDegree ≤ h/2) (hne : e ≠ 0) (htr : e.natTrailingDegree=z) (p : ℕ) :
    Module.finrank F (bandMap h (h*(2*p)) ((X^h+e)^(2*p+1))).range = h-z := by
  let a := upper h hh e he
  let f := low h e
  let coord := degreeLTEquiv F h
  have ha : Function.Involutive a := upper_involution hh e he
  have hmap : bandMap h (h*(2*p)) ((X^h+e)^(2*p+1)) =
      coord.toLinearMap.comp (if p%2=0 then f else a.comp (f.comp a)) := by
    apply LinearMap.ext
    intro x
    rw [band_state hh e he, stage_density a f ha]
    split <;> rfl
  by_cases hp : p%2=0
  · rw [ite_eq_left hp] at hmap
    rw [hmap, LinearMap.range_comp, coord.finrank_map_eq]
    exact low_rank hz e hne htr
  · rw [ite_eq_right hp] at hmap
    rw [hmap, LinearMap.range_comp, coord.finrank_map_eq]
    exact (rank_conjugate a f ha).trans (low_rank hz e hne htr)

omit [CharP F 2] in
private theorem trace_low_parameters (a z : ℕ) (ha : 2 ≤ a) (hz : 0 < z) :
    let e := CoefficientPrefix.traceLow (F:=F) a z
    e.natDegree ≤ a*a*z ∧ e ≠ 0 ∧ e.natTrailingDegree = z := by
  dsimp only
  have haz : z < a*z := by simpa using Nat.mul_lt_mul_of_pos_right (show 1<a by omega) hz
  have h2z : z < 2*z := by omega
  have hasq : a ≤ a*a := by nlinarith
  have hasq2 : a*2 ≤ a*a := by nlinarith
  have h1 : a*z ≤ a*a*z := Nat.mul_le_mul_right z hasq
  have h2 : a*2*z ≤ a*a*z := Nat.mul_le_mul_right z hasq2
  have h3 : 2*z ≤ a*z := Nat.mul_le_mul_right z ha
  have h4 : a*z ≤ a*2*z := by nlinarith
  have hlarge : ∀ n, n ≤ z → n ≠ a*a*z ∧ n ≠ a*2*z ∧ n ≠ a*z ∧ n ≠ 2*z := by
    intro n hn; omega
  have c (n : ℕ) (hn : n ≤ z) : (CoefficientPrefix.traceLow (F:=F) a z).coeff n =
      if n=z then 1 else 0 := by
    obtain ⟨hA,hB,hC,hD⟩ := hlarge n hn
    simp [CoefficientPrefix.traceLow, coeff_X_pow, hA, hB, hC, hD]
  have cn : (CoefficientPrefix.traceLow (F:=F) a z).coeff z ≠ 0 := by simp [c z le_rfl]
  have en : CoefficientPrefix.traceLow (F:=F) a z ≠ 0 := by intro eq; simp [eq] at cn
  refine ⟨?_, en, le_antisymm (natTrailingDegree_le_of_ne_zero cn) ((Xpow_dvd_of_trailing en).mp ?_)⟩
  · have join {u w : F[X]} (hu : u.natDegree ≤ a*a*z) (hw : w.natDegree ≤ a*a*z) :
        (u+w).natDegree ≤ a*a*z := (natDegree_add_le ..).trans (max_le hu hw)
    unfold CoefficientPrefix.traceLow
    apply join (join (join (join ?_ ?_) ?_) ?_) ?_
    all_goals rw [natDegree_X_pow]
    all_goals omega
  · apply X_pow_dvd_iff.mpr
    intro n hn
    simp [c n hn.le, ne_of_lt hn]

/-- The literal printed trace polynomial, at all Frobenius levels and all
prefix positions. With a=2^c, h=2a²2^i and start=2ph, this is the actual
upper-half to lower-half radix-synthesis submatrix in ordinary B coordinates. -/
theorem trace_power_band_rank (a i p : ℕ) (ha : 2 ≤ a) :
    let z := 2^i
    let h := a*a*2*z
    Module.finrank F (bandMap h (h*(2*p))
       ((CoefficientPrefix.traceBase (F:=F) a)^((2*p+1)*z))).range = h-z := by
  dsimp only
  obtain ⟨he,hen,het⟩ := trace_low_parameters (F:=F) a (2^i) ha (by positivity)
  rw [Nat.mul_comm (2*p+1) (2^i), pow_mul, CoefficientPrefix.trace_power_form]
  have hpos : 0<2^i := by positivity
  have hbase : 2 ≤ a*a := by nlinarith
  have hh : 2 ≤ a*a*2*(2^i) := by nlinarith
  have hz : 2^i ≤ a*a*2*(2^i) := by nlinarith
  apply odd_power_band_rank hh hz _ _ hen het
  rwa [show a*a*2*(2^i) = 2*(a*a*(2^i)) by ring, Nat.mul_div_cancel_left _ (by decide : 0 < 2)]

/-- The same trace radix is monic of the caller's specified leaf width. -/
theorem trace_monic_degree (a : ℕ) (ha : 2 ≤ a) :
    (CoefficientPrefix.traceBase (F:=F) a).Monic ∧
    (CoefficientPrefix.traceBase (F:=F) a).natDegree = a*a*2 := by
  have decomp := CoefficientPrefix.trace_power_form (F:=F) a 0
  simp only [pow_zero, pow_one, Nat.mul_one] at decomp
  have he := (trace_low_parameters (F:=F) a 1 ha (by decide)).1
  simp only [Nat.mul_one] at he
  have hx : (CoefficientPrefix.traceLow (F:=F) a 1).degree < (X^(a*a*2) : F[X]).degree := by
    apply degree_lt_degree
    rw [natDegree_X_pow]
    nlinarith
  rw [decomp]
  exact ⟨(monic_X_pow _).add_of_left hx, by rw [natDegree_add_eq_left_of_degree_lt hx, natDegree_X_pow]⟩

#print axioms trace_monic_degree
#print axioms odd_power_band_rank
#print axioms trace_power_band_rank

end Moonshot.TraceRadixRank
