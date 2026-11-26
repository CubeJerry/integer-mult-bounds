import Mathlib.Algebra.Group.AddChar
import Mathlib.Algebra.Ring.Action.Group
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.CharP.Two
import Mathlib.Algebra.CharP.Reduced
import Mathlib.Algebra.GroupWithZero.Units.Fintype

/-! Inversion of a trace-projected multiplicative Fourier matrix over a finite field. -/
namespace Moonshot.ProjectedTraceCRT

open scoped BigOperators

variable {R F G : Type*} [CommRing R] [Fintype R] [DecidableEq R]
  [Field F] [Group G] [Fintype G]

/-- Sum of the field automorphisms. For the Galois group of a finite-field extension this
is the image of its field trace. -/
noncomputable def orbitTrace (act : G →* (F ≃+* F)) (x : F) : F := ∑ r, act r x

/-- Both trace-projected Fourier matrices, with the same frequency and sample indexing. -/
noncomputable def projected (act : G →* (F ≃+* F)) (ψ : AddChar R F) (γ : F) : Matrix R R F :=
  fun a i => orbitTrace act (γ * ψ (a*i))

noncomputable def reciprocal (act : G →* (F ≃+* F)) (ψ : AddChar R F) (δ : F) : Matrix R R F :=
  fun i a => orbitTrace act (δ * ψ (-(a*i)))

omit [DecidableEq R] in
private theorem character_sum_zero {χ : AddChar R F} (hχ : χ ≠ 1) : ∑ a, χ a = 0 := by
  obtain ⟨b,hb⟩ := AddChar.ne_one_iff.mp hχ
  have h : ∑ a, χ (b+a) = ∑ a, χ a := (AddGroup.addLeft_bijective b).sum_comp χ
  simp_rw [AddChar.map_add_eq_mul] at h
  rw [← Finset.mul_sum] at h
  exact eq_zero_of_mul_eq_self_left hb h

private def pairChar (act : G →* (F ≃+* F)) (ψ : AddChar R F) (t : G) (i j : R) : AddChar R F where
  toFun a := ψ (-(a*i)) * act t (ψ (a*j))
  map_zero_eq_one' := by simp
  map_add_eq_mul' a b := by
    simp only [add_mul, neg_add_rev, AddChar.map_add_eq_mul, map_mul]
    ring

private noncomputable def pairSum (act : G →* (F ≃+* F)) (ψ : AddChar R F) (t : G) (i j : R) : F :=
  ∑ a, pairChar act ψ t i j a

omit [DecidableEq R] [Fintype G] in
private theorem pair_fixed (act : G →* (F ≃+* F)) (ψ : AddChar R F) (hcard : (Fintype.card R : F) = 1)
    (r t : G) (i j : R) : act r (pairSum act ψ t i j) = pairSum act ψ t i j := by
  classical
  by_cases h : pairChar act ψ t i j = 1
  · simp [pairSum, h, hcard]
  · simp [pairSum, character_sum_zero h]

omit [Fintype G] in
private theorem at_identity (act : G →* (F ≃+* F)) (ψ : AddChar R F)
    (hψ : ∀ a, ψ a = 1 → a = 0) (hcard : (Fintype.card R : F) = 1) (i j : R) :
    pairSum act ψ 1 i j = if i=j then 1 else 0 := by
  classical
  by_cases h : i=j
  · subst j
    have hchar : pairChar act ψ 1 i i = 1 := by
      ext a
      change ψ (-(a*i)) * act 1 (ψ (a*i)) = 1
      rw [map_one, RingAut.one_apply, ← AddChar.map_add_eq_mul, neg_add_cancel, AddChar.map_zero_eq_one]
    simp [pairSum, hchar, hcard]
  · have hchar : pairChar act ψ 1 i j ≠ 1 := by
      intro ht
      have hv := DFunLike.congr_fun ht (1:R)
      change ψ (-(1*i)) * act 1 (ψ (1*j)) = 1 at hv
      rw [one_mul, one_mul, map_one, RingAut.one_apply, ← AddChar.map_add_eq_mul] at hv
      apply h
      have := hψ _ hv
      exact neg_add_eq_zero.mp this
    simp [pairSum, h, character_sum_zero hchar]

omit [DecidableEq R] [Fintype G] in
private theorem fiber_sum (act : G →* (F ≃+* F)) (ψ : AddChar R F) (hcard : (Fintype.card R : F) = 1)
    (δ γ : F) (r t : G) (i j : R) :
    (∑ a, act r (δ * ψ (-(a*i))) * act (r*t) (γ * ψ (a*j))) =
      act r (δ * act t γ) * pairSum act ψ t i j := by
  rw [← pair_fixed act ψ hcard r t i j, ← map_mul]
  simp only [pairSum, Finset.mul_sum, map_sum, map_mul, RingAut.mul_apply]
  apply Finset.sum_congr rfl
  intro a _
  change _ = act r δ * act r (act t γ) * act r (ψ (-(a*i)) * act t (ψ (a*j)))
  rw [(act r).map_mul (ψ (-(a*i))) (act t (ψ (a*j)))]
  ring

/-- Orthogonality of an arbitrary primitive Fourier character after two dual trace projections.
Short Frobenius orbits and repeated index congruences need no separate hypothesis. -/
theorem matrix_inverse [DecidableEq G] (act : G →* (F ≃+* F)) (ψ : AddChar R F)
    (hψ : ∀ a, ψ a = 1 → a = 0) (hcard : (Fintype.card R : F) = 1) (δ γ : F)
    (hdual : ∀ t, orbitTrace act (δ * act t γ) = if t=1 then 1 else 0) :
    reciprocal act ψ δ * projected act ψ γ = 1 := by
  classical
  ext i j
  rw [Matrix.mul_apply, Matrix.one_apply]
  unfold reciprocal projected
  simp only [orbitTrace, Finset.sum_mul, Finset.mul_sum]
  have swap (f : R → G → G → F) : (∑ a, ∑ r, ∑ s, f a r s) = ∑ r, ∑ s, ∑ a, f a r s := by
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro r _
    rw [Finset.sum_comm]
  rw [swap, Finset.sum_comm]
  calc
    _ = ∑ r:G, ∑ t:G, ∑ a:R, act r (δ * ψ (-(a*i))) * act (r*t) (γ * ψ (a*j)) := by
      apply Finset.sum_congr rfl
      intro r _
      exact ((Group.mulLeft_bijective r).sum_comp (fun s:G => ∑ a:R, act r (δ * ψ (-(a*i))) * act s (γ * ψ (a*j)))).symm
    _ = ∑ t:G, orbitTrace act (δ * act t γ) * pairSum act ψ t i j := by
      simp only [fiber_sum act ψ hcard]
      rw [Finset.sum_comm]
      simp [orbitTrace, Finset.sum_mul]
    _ = pairSum act ψ 1 i j := by simp [hdual, ite_mul]
    _ = _ := at_identity act ψ hψ hcard i j

/-- The actual primitive Fourier character used by the physical trace transform. -/
def rootCharacter {m : ℕ} [NeZero m] (ζ : F) (hζ : orderOf ζ = m) : AddChar (ZMod m) F where
  toFun a := ζ^a.val
  map_zero_eq_one' := by simp
  map_add_eq_mul' a b := by
    have hpow : ζ^m=1 := hζ ▸ pow_orderOf_eq_one ζ
    simp only [ZMod.val_add, ← pow_eq_pow_mod _ hpow, pow_add]

private theorem root_primitive {m : ℕ} [NeZero m] (ζ : F) (hζ : orderOf ζ = m)
    (a : ZMod m) (h : rootCharacter ζ hζ a = 1) : a=0 := by
  change ζ^a.val=1 at h
  obtain hd := orderOf_dvd_of_pow_eq_one h
  rw [hζ] at hd
  exact (ZMod.val_eq_zero a).mp (Nat.eq_zero_of_dvd_of_lt hd (ZMod.val_lt a))

/-- Powers of one field automorphism whose `c`th power is the identity. -/
noncomputable def cyclicAction {c : ℕ} [NeZero c] (σ : F ≃+* F) (hσ : σ^c=1) :
    Multiplicative (ZMod c) →* (F ≃+* F) where
  toFun r := σ ^ (Multiplicative.toAdd r).val
  map_one' := by change σ ^ (0 : ZMod c).val = 1; simp
  map_mul' r s := by
    change σ^((Multiplicative.toAdd r)+(Multiplicative.toAdd s)).val = _
    rw [ZMod.val_add, ← pow_eq_pow_mod _ hσ, pow_add]

private theorem cyclicAction_nat {c : ℕ} [NeZero c] (σ : F ≃+* F) (hσ : σ^c=1) (n : ℕ) :
    cyclicAction σ hσ (Multiplicative.ofAdd (n : ZMod c)) = σ^n := by
  change σ ^ (n : ZMod c).val = _
  rw [ZMod.val_natCast, ← pow_eq_pow_mod _ hσ]

/-- Orbit traces are fixed under every automorphism in the group. -/
theorem trace_fixed (act : G →* (F ≃+* F)) (r:G) (x:F) : act r (orbitTrace act x) = orbitTrace act x := by
  unfold orbitTrace
  rw [map_sum]
  simpa only [map_mul, RingAut.mul_apply] using (Group.mulLeft_bijective r).sum_comp (fun s:G => act s x)

section BinaryField
variable [Fintype F] [CharP F 2]

private noncomputable def binaryFrob (F : Type*) [Field F] [Fintype F] [CharP F 2] : F ≃+* F :=
  RingEquiv.ofBijective (frobenius F 2) ⟨frobenius_inj F 2, Finite.surjective_of_injective (frobenius_inj F 2)⟩

private theorem binaryFrob_pow (n : ℕ) (x : F) : (binaryFrob F ^ n) x = x ^ (2^n) := by
  induction n generalizing x with
  | zero => simp [RingAut.one_apply]
  | succ n ih =>
    rw [pow_succ, RingAut.mul_apply, ih]
    change (x^2)^(2^n) = _
    rw [← pow_mul, pow_succ, Nat.mul_comm 2 (2^n)]

omit [CharP F 2] in
private theorem field_power [DecidableEq F] (x : F) : x ^ Fintype.card F = x := by
  by_cases h : x=0
  · subst x; exact zero_pow Fintype.card_ne_zero
  · have hu : (Units.mk0 x h) ^ Fintype.card Fˣ = 1 := pow_card_eq_one
    have hv := congrArg (fun z:Fˣ => (z:F)) hu
    simp only [Units.val_pow_eq_pow_val, Units.val_mk0, Units.val_one, Fintype.card_units] at hv
    calc
      _ = x^((Fintype.card F-1)+1) := by rw [Nat.sub_one_add_one_eq_of_pos Fintype.card_pos]
      _ = _ := by rw [pow_succ, hv, one_mul]

private theorem period {c : ℕ} (hf : Fintype.card F = 2^c) : binaryFrob F ^ c = 1 := by
  classical
  ext x
  rw [binaryFrob_pow, ← hf, field_power, RingAut.one_apply]

/-- The literal `c`-term sum of Frobenius conjugates. -/
noncomputable def binaryTrace (c : ℕ) [NeZero c] (x : F) : F := ∑ r : ZMod c, x^(2^r.val)

private theorem binary_orbit_trace {c : ℕ} [NeZero c] (hf : Fintype.card F = 2^c) (x:F) :
    orbitTrace (cyclicAction (binaryFrob F) (period hf)) x = binaryTrace c x := by
  unfold orbitTrace binaryTrace
  exact Fintype.sum_equiv Multiplicative.toAdd _ _ (fun r => binaryFrob_pow _ x)

/-- The projected transform stores actual binary values in the ambient field. -/
theorem binary_trace_bit {c : ℕ} [NeZero c] (hf : Fintype.card F = 2^c) (x:F) :
    binaryTrace c x=0 ∨ binaryTrace c x=1 := by
  let σ := binaryFrob F
  have h := trace_fixed (cyclicAction σ (period hf)) (Multiplicative.ofAdd ((1:ℕ) : ZMod c)) x
  rw [cyclicAction_nat, pow_one] at h
  change binaryFrob F _ = _ at h
  rw [binary_orbit_trace hf] at h
  change (binaryTrace c x)^2=binaryTrace c x at h
  have hprod : binaryTrace c x * (binaryTrace c x-1)=0 := by rw [mul_sub, mul_one, ← pow_two, h, sub_self]
  exact (mul_eq_zero.mp hprod).imp id sub_eq_zero.mp

/-- Physical forward coefficients as binary traces of powers of a primitive generator. -/
noncomputable def forward {m : ℕ} [NeZero m] (c : ℕ) [NeZero c] (ζ γ:F) : Matrix (ZMod m) (ZMod m) F :=
  fun a i => binaryTrace c (γ * ζ^(a*i).val)

/-- Physical reciprocal coefficients with the negative exponent. -/
noncomputable def backward {m : ℕ} [NeZero m] (c : ℕ) [NeZero c] (ζ δ:F) : Matrix (ZMod m) (ZMod m) F :=
  fun i a => binaryTrace c (δ * ζ^(-(a*i)).val)

/-- The two full-length matrices on the actual binary field. The setup supplies a
primitive generator and exactly the trace-dual coordinate identities. -/
theorem binary_matrices {c m : ℕ} [NeZero c] [NeZero m] (hf : Fintype.card F=2^c)
    (hm : m+1=2^c) (ζ δ γ : F) (hζ : orderOf ζ=m)
    (hdual : ∀ t : ZMod c, binaryTrace c (δ * γ^(2^t.val)) = if t=0 then 1 else 0) :
    backward (m:=m) c ζ δ * forward c ζ γ=1 ∧ forward (m:=m) c ζ γ * backward c ζ δ=1 := by
  classical
  let act := cyclicAction (binaryFrob F) (period hf)
  let ψ := rootCharacter ζ hζ
  have card : (Fintype.card (ZMod m):F)=1 := by
    rw [ZMod.card]
    apply add_right_cancel (b:=(1:F))
    calc
      (m:F)+1 = (2:F)^c := by
        simpa only [Nat.cast_add, Nat.cast_one, Nat.cast_pow, Nat.cast_ofNat] using congrArg (fun n:ℕ => (n:F)) hm
      _ = 0 := by rw [CharTwo.two_eq_zero, zero_pow (NeZero.ne c)]
      _ = 1+1 := (CharTwo.add_self_eq_zero (1:F)).symm
  have hd : ∀ t:Multiplicative (ZMod c), orbitTrace act (δ * act t γ) = if t=1 then 1 else 0 := by
    intro t
    change orbitTrace (cyclicAction (binaryFrob F) _) (δ * (binaryFrob F^(Multiplicative.toAdd t).val) γ) = _
    rw [binary_orbit_trace hf, binaryFrob_pow]
    exact hdual (Multiplicative.toAdd t)
  have h := matrix_inverse act ψ (root_primitive ζ hζ) card δ γ hd
  have hp : projected act ψ γ = forward (m:=m) c ζ γ := by
    ext a i
    exact binary_orbit_trace hf _
  have hq : reciprocal act ψ δ = backward (m:=m) c ζ δ := by
    ext i a
    exact binary_orbit_trace hf _
  rw [hp,hq] at h
  exact ⟨h, mul_eq_one_comm.mp h⟩

end BinaryField
end Moonshot.ProjectedTraceCRT
#print axioms Moonshot.ProjectedTraceCRT.matrix_inverse
#print axioms Moonshot.ProjectedTraceCRT.trace_fixed
#print axioms Moonshot.ProjectedTraceCRT.binary_trace_bit
#print axioms Moonshot.ProjectedTraceCRT.binary_matrices
