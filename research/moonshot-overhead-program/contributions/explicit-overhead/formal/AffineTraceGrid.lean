import Mathlib.FieldTheory.Finite.Basic
import Mathlib.Algebra.MvPolynomial.CommRing
import Mathlib.Algebra.Polynomial.Div
import Mathlib.Algebra.Polynomial.Roots
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.LinearCombination
import Mathlib.Algebra.CharP.Two

/-!
# The relative-trace affine plane

The cubic relative-trace fibre is sampled in coordinates x=t+vy+wz for
y,z in the base field. The two Frobenius coordinates x,x^a form a nonsingular
affine change of variables over the large field. Polynomials and arbitrary
arrays of values at all base-field pairs are both handled.
-/
namespace Moonshot.AffineTraceGrid
open Polynomial
open scoped Polynomial BigOperators

variable {L K : Type*} [Field L] [Fintype L] [Field K] [Algebra L K]

/-- The elements of an extension fixed by base-cardinality Frobenius are
exactly the embedded base field. No closure assumption on the extension. -/
theorem fixed_iff (x : K) : x^(Fintype.card L)=x ↔ ∃r : L, algebraMap L K r=x := by
  classical
  let n := Fintype.card L
  let f := (X^n-X : K[X])
  have nn : 1<n := Fintype.one_lt_card
  have nz : f≠0 := FiniteField.X_pow_card_sub_X_ne_zero K nn
  have hd : f.natDegree=n := FiniteField.X_pow_card_sub_X_natDegree_eq K nn
  let S := Finset.univ.image (algebraMap L K)
  have contained : S ⊆ f.roots.toFinset := by
    intro t ht
    obtain ⟨r,_,rfl⟩ := Finset.mem_image.mp ht
    apply Multiset.mem_toFinset.mpr
    rw [mem_roots nz,IsRoot.def]
    simp [f,n,←map_pow,FiniteField.pow_card]
  have sz : S.card=n := Finset.card_image_of_injective _ (algebraMap L K).injective |>.trans (Finset.card_univ)
  have maxroots : f.roots.toFinset.card ≤ S.card := by
    rw [sz,←hd]
    exact (Multiset.toFinset_card_le _).trans f.card_roots'
  have eq := Finset.eq_of_subset_of_card_le contained maxroots
  constructor
  · intro hx
    have root : x∈f.roots.toFinset := by
      apply Multiset.mem_toFinset.mpr
      rw [mem_roots nz,IsRoot.def]
      simp [f,n,hx]
    rw [←eq] at root
    obtain ⟨u,_,hu⟩ := Finset.mem_image.mp root
    exact ⟨u,hu⟩
  · rintro ⟨r,rfl⟩
    simp [←map_pow,FiniteField.pow_card]

/-- Determinant of the two ordinary and Frobenius columns. -/
def det (a : ℕ) (v w : K) := v*w^a-w*v^a

/-- A coefficient form of independence of v,w over the base field. -/
def independent (L : Type*) [Field L] [Algebra L K] (v w : K) :=
  ∀ y z : L, v*(algebraMap L K y)+w*(algebraMap L K z)=0 → y=0 ∧ z=0

/-- The Moore determinant is nonzero for every independent pair. -/
theorem moore_ne_zero (v w : K) (lin : independent L v w) : det (Fintype.card L) v w ≠ 0 := by
  have wn : w≠0 := by
    intro hw
    exact one_ne_zero (lin 0 1 (by simp [hw])).2
  intro hz
  have cross : v*w^(Fintype.card L)=w*v^(Fintype.card L) := sub_eq_zero.mp hz
  have ratio : (v/w)^(Fintype.card L)=v/w := by
    rw [div_pow,div_eq_div_iff (pow_ne_zero _ wn) wn]
    linear_combination -cross
  obtain ⟨r,hr⟩ := (fixed_iff (L:=L) (v/w)).mp ratio
  have vr : algebraMap L K r*w=v := (eq_div_iff wn).mp hr
  exact one_ne_zero (lin 1 (-r) (by simp; linear_combination -vr)).1

/-- Base-cardinality Frobenius as an algebra homomorphism. -/
noncomputable abbrev phi (L K : Type*) [Field L] [Fintype L] [Field K] [Algebra L K] :=
  FiniteField.frobeniusAlgHom L K

def chart (t : L) (v w : K) (yz : L×L) : K :=
  algebraMap L K t + v*algebraMap L K yz.1 + w*algebraMap L K yz.2

private theorem power_chart (t : L) (v w : K) (yz : L×L) :
    (chart t v w yz)^(Fintype.card L)=algebraMap L K t +
      v^(Fintype.card L)*algebraMap L K yz.1 + w^(Fintype.card L)*algebraMap L K yz.2 := by
  change phi L K (chart t v w yz)=_
  simp only [chart, map_add,map_mul,AlgHom.commutes]
  rfl

private def coords {R : Type*} (x y : R) : Bool→R := fun b => if b then y else x

abbrev Bi (K : Type*) [Field K] := MvPolynomial Bool K

private noncomputable def subst (c : Bool→Bi K) (p : Bi K) :=
  p.eval₂ MvPolynomial.C c

private noncomputable def forwardVars (a : ℕ) (t v w : K) : Bool→Bi K :=
  coords
    (MvPolynomial.C t + MvPolynomial.C v * MvPolynomial.X false + MvPolynomial.C w * MvPolynomial.X true)
    (MvPolynomial.C t + MvPolynomial.C (v^a) * MvPolynomial.X false + MvPolynomial.C (w^a) * MvPolynomial.X true)

private noncomputable def inverseVars (a : ℕ) (t v w : K) : Bool→Bi K :=
  let u := MvPolynomial.X false-MvPolynomial.C t
  let z := MvPolynomial.X true-MvPolynomial.C t
  let denom := MvPolynomial.C (det a v w)⁻¹
  coords (denom*(MvPolynomial.C (w^a)*u-MvPolynomial.C w*z))
         (denom*(MvPolynomial.C v*z-MvPolynomial.C (v^a)*u))

private theorem undo_on_grid (t : L) (v w : K)
    (hd : det (Fintype.card L) v w≠0) (yz : L×L) :
    let x := chart t v w yz
    MvPolynomial.eval (coords x (x^(Fintype.card L))) ∘
        inverseVars (Fintype.card L) (algebraMap L K t) v w =
      coords (algebraMap L K yz.1) (algebraMap L K yz.2) := by
  dsimp only
  rw [power_chart]
  funext b
  cases b <;> simp [Function.comp_apply,inverseVars,coords,chart] <;>
    field_simp [hd] <;> unfold det <;> ring

/-- Applying the two-variable polynomial coordinate change to any input
polynomial computes its value at (x,x^a) on every base-field pair. -/
theorem forward_evaluates (t : L) (v w : K) (P : Bi K) (yz : L×L) :
    let x := chart t v w yz
    MvPolynomial.eval (coords (algebraMap L K yz.1) (algebraMap L K yz.2))
        (subst (forwardVars (Fintype.card L) (algebraMap L K t) v w) P) =
      MvPolynomial.eval (coords x (x^(Fintype.card L))) P := by
  dsimp only
  unfold subst
  rw [←MvPolynomial.eval_assoc]
  rw [power_chart]
  apply congrArg (fun u => MvPolynomial.eval u P)
  funext b
  cases b <;> simp [Function.comp_apply,forwardVars,coords,chart]

/-- Interpolation on the embedded base-field grid has extension-field
coefficients and accepts any independent extension values. -/
private noncomputable def indicator (side : Bool) (r : L) : Bi K :=
  1-(MvPolynomial.X side-MvPolynomial.C (algebraMap L K r))^(Fintype.card L-1)

noncomputable def interp (values : L×L → K) : Bi K :=
  ∑ y : L, ∑ z : L, MvPolynomial.C (values (y,z)) * indicator false y * indicator true z

private theorem eval_indicator [DecidableEq L] (point : Bool→L) (b : Bool) (r : L) :
    MvPolynomial.eval (algebraMap L K ∘ point) (indicator b r : Bi K) =
      if point b=r then 1 else 0 := by
  have pos : 0<Fintype.card L-1 := by have := Fintype.one_lt_card (α:=L); omega
  simp only [indicator,map_sub,map_one,map_pow,MvPolynomial.eval_X,MvPolynomial.eval_C,Function.comp_apply]
  by_cases eq : point b=r
  · simp [eq,zero_pow pos.ne']
  · have nz : point b - r ≠ 0 := sub_ne_zero.mpr eq
    rw [←map_sub,←map_pow,FiniteField.pow_card_sub_one_eq_one _ nz,map_one,sub_self,ite_eq_right eq]

theorem interp_at (values : L×L→K) (yz : L×L) :
    MvPolynomial.eval (coords (algebraMap L K yz.1) (algebraMap L K yz.2)) (interp values)=values yz := by
  classical
  have pt : coords (algebraMap L K yz.1) (algebraMap L K yz.2) =
      algebraMap L K ∘ coords yz.1 yz.2 := by funext b; cases b <;> rfl
  rw [pt]
  simp [interp,eval_indicator,coords,mul_ite]

/-- Substituting the Frobenius graph W=X^a into a bivariate polynomial. -/
noncomputable def collapse (a : ℕ) (P : Bi K) : K[X] :=
  P.eval₂ Polynomial.C (coords X (X^a))

theorem collapse_at (a : ℕ) (P : Bi K) (x : K) :
    (collapse a P).eval x = MvPolynomial.eval (coords x (x^a)) P := by
  change (Polynomial.evalRingHom x) (P.eval₂ Polynomial.C (coords X (X^a)))=_
  rw [MvPolynomial.hom_eval₂]
  have ce : (Polynomial.evalRingHom x).comp Polynomial.C = RingHom.id K := by ext z; simp
  rw [ce,MvPolynomial.eval₂_id]
  apply congrArg (fun c => MvPolynomial.eval c P)
  funext b
  cases b <;> simp [coords]

/-- Pack increasing monomial exponent k into the two base-a digits
(k % a,k / a), as in the physical input. -/
noncomputable def pack (a : ℕ) (P : K[X]) : Bi K :=
  ∑ k∈Finset.range (P.natDegree+1), MvPolynomial.C (P.coeff k) *
      MvPolynomial.X false^(k%a) * MvPolynomial.X true^(k/a)

theorem collapse_pack (a : ℕ) (P : K[X]) : collapse a (pack a P)=P := by
  change (MvPolynomial.eval₂Hom Polynomial.C (coords X (X^a))) (pack a P)=P
  unfold pack
  rw [map_sum]
  conv_rhs => rw [P.as_sum_range_C_mul_X_pow]
  apply Finset.sum_congr rfl
  intro k _
  simp only [map_mul,map_pow,MvPolynomial.eval₂Hom_C,MvPolynomial.eval₂Hom_X']
  change C _ * X^(k%a) * (X^a)^(k/a) = C _ * X^k
  rw [mul_assoc,←pow_mul,←pow_add,Nat.mod_add_div]

/-- The polynomial made by the forward affine change on ordinary inputs. -/
noncomputable def forward (t : L) (v w : K) (P : K[X]) :=
  subst (forwardVars (Fintype.card L) (algebraMap L K t) v w) (pack (Fintype.card L) P)

theorem forward_at (t : L) (v w : K) (P : K[X]) (yz : L×L) :
    MvPolynomial.eval (coords (algebraMap L K yz.1) (algebraMap L K yz.2)) (forward t v w P) =
      P.eval (chart t v w yz) := by
  rw [forward,forward_evaluates,←collapse_at,collapse_pack]

/-- Relative trace with three summands, matching the cubic fibre polynomial. -/
noncomputable def traceValue (L : Type*) [Field L] [Fintype L] [Algebra L K] (x : K) :=
  x + phi L K x + phi L K (phi L K x)

noncomputable def fibrePoly (t : L) : K[X] :=
  let a := Fintype.card L
  X^(a*a) + (X^a+X-C (algebraMap L K t))

private theorem fibre_monic (t : L) :
    (fibrePoly (K:=K) t).Monic ∧ (fibrePoly (K:=K) t).natDegree = Fintype.card L*Fintype.card L := by
  let a := Fintype.card L
  have ha : 1<a := Fintype.one_lt_card
  have h1 : (X : K[X]).degree < (X^a : K[X]).degree := by
    rw [degree_X,degree_X_pow]; exact_mod_cast ha
  have hc : (C (algebraMap L K t)).degree < (X^a+X : K[X]).degree := by
    rw [degree_add_eq_left_of_degree_lt h1,degree_X_pow]
    exact (degree_C_le).trans_lt (by exact_mod_cast (show 0<a by omega))
  have h2 : (X^a+X-C (algebraMap L K t) : K[X]).degree < (X^(a*a) : K[X]).degree := by
    rw [degree_sub_eq_left_of_degree_lt hc,degree_add_eq_left_of_degree_lt h1,degree_X_pow,degree_X_pow]
    exact_mod_cast (show a<a*a by nlinarith)
  exact ⟨(monic_X_pow _).add_of_left h2,
    by rw [fibrePoly,natDegree_add_eq_left_of_degree_lt h2,natDegree_X_pow]⟩

theorem fibre_eval (t : L) (x : K) : (fibrePoly t).eval x=traceValue L x-algebraMap L K t := by
  simp only [fibrePoly,eval_add,eval_sub,eval_pow,eval_X,eval_C,traceValue,FiniteField.frobeniusAlgHom_apply,phi,←pow_mul]
  ring

theorem trace_chart [CharP K 2] (t : L) (v w : K)
    (hv : traceValue L v=0) (hw : traceValue L w=0) (yz : L×L) :
    traceValue L (chart t v w yz)=algebraMap L K t := by
  unfold traceValue at hv hw ⊢
  simp only [chart,map_add,map_mul,AlgHom.commutes]
  linear_combination (algebraMap L K yz.1)*hv + (algebraMap L K yz.2)*hw +
    CharTwo.add_self_eq_zero (algebraMap L K t)

/-- The inverse interpolation, pullback along the inverse affine map, and
ordinary monic reduction to the relative-trace fibre. -/
noncomputable def recover (t : L) (v w : K) (values : L×L→K) : K[X] :=
  (collapse (Fintype.card L) (subst (inverseVars (Fintype.card L) (algebraMap L K t) v w)
      (interp values))) %ₘ fibrePoly t

theorem recover_at [CharP K 2] (t : L) (v w : K)
    (hv : traceValue L v=0) (hw : traceValue L w=0) (lin : independent L v w)
    (values : L×L→K) (yz : L×L) :
    (recover t v w values).eval (chart t v w yz)=values yz := by
  have root : (fibrePoly t).eval (chart t v w yz)=0 := by rw [fibre_eval,trace_chart t v w hv hw,sub_self]
  rw [recover,modByMonic_eq_sub_mul_div,eval_sub,eval_mul,root,zero_mul,sub_zero,collapse_at,
    subst,←MvPolynomial.eval_assoc,undo_on_grid t v w (moore_ne_zero v w lin),interp_at]

theorem recover_degree (t : L) (v w : K) (values : L×L→K) :
    (recover t v w values).natDegree < Fintype.card L*Fintype.card L := by
  have ht := fibre_monic (K:=K) t
  by_cases zz : recover t v w values=0
  · simp [zz,Fintype.card_pos]
  · rw [natDegree_lt_iff_degree_lt zz,←ht.2,←degree_eq_natDegree ht.1.ne_zero]
    exact degree_modByMonic_lt _ ht.1


/-- Different base-field coordinate pairs produce different fibre points. -/
theorem chart_injective (t : L) (v w : K) (lin : independent L v w) :
    Function.Injective (chart t v w) := by
  intro p r eq
  let get (x : K) := MvPolynomial.eval (coords x (x^(Fintype.card L))) ∘
    inverseVars (Fintype.card L) (algebraMap L K t) v w
  have undo (s : L×L) : get (chart t v w s) = coords (algebraMap L K s.1) (algebraMap L K s.2) :=
    undo_on_grid t v w (moore_ne_zero v w lin) s
  have both := (undo p).symm.trans ((congrArg get eq).trans (undo r))
  exact Prod.ext ((algebraMap L K).injective (congrFun both false))
    ((algebraMap L K).injective (congrFun both true))

/-- The grid exhausts the literal polynomial fibre: its cardinality already
attains the degree of the monic fibre polynomial. -/
theorem fibre_iff [CharP K 2] (t : L) (v w : K) (hv : traceValue L v=0)
    (hw : traceValue L w=0) (lin : independent L v w) (x : K) :
    traceValue L x=algebraMap L K t ↔ ∃ yz : L×L, chart t v w yz=x := by
  classical
  let f := fibrePoly (K:=K) t
  have hd := fibre_monic (K:=K) t
  let S := Finset.univ.image (chart t v w)
  have contained : S ⊆ f.roots.toFinset := by
    intro y hy
    obtain ⟨yz,_,rfl⟩ := Finset.mem_image.mp hy
    apply Multiset.mem_toFinset.mpr
    rw [mem_roots hd.1.ne_zero,IsRoot.def,fibre_eval,trace_chart t v w hv hw,sub_self]
  have sc : S.card=f.natDegree := by
    rw [Finset.card_image_of_injective _ (chart_injective t v w lin), Finset.card_univ, Fintype.card_prod,hd.2]
  have eq := Finset.eq_of_subset_of_card_le contained
    (by rw [sc]; exact (Multiset.toFinset_card_le _).trans f.card_roots')
  constructor
  · intro hx
    have root : x∈f.roots.toFinset := by
      rw [Multiset.mem_toFinset,mem_roots hd.1.ne_zero,IsRoot.def,fibre_eval,hx,sub_self]
    rw [←eq] at root
    obtain ⟨yz,_,ey⟩ := Finset.mem_image.mp root
    exact ⟨yz,ey⟩
  · rintro ⟨yz,rfl⟩
    exact trace_chart t v w hv hw yz

/-- Interpolating arbitrary values and evaluating gives back those values;
evaluating a degree-<a² polynomial and interpolating gives back the polynomial. -/
theorem round_trip [CharP K 2] (t : L) (v w : K)
    (hv : traceValue L v=0) (hw : traceValue L w=0) (lin : independent L v w) :
    (∀ values : L×L→K, ∀yz, (recover t v w values).eval (chart t v w yz)=values yz) ∧
    (∀ P : K[X], P.natDegree<Fintype.card L*Fintype.card L →
      recover t v w (fun yz => MvPolynomial.eval (coords (algebraMap L K yz.1) (algebraMap L K yz.2))
        (forward t v w P))=P) := by
  refine ⟨recover_at t v w hv hw lin,?_⟩
  intro P size
  apply Polynomial.eq_of_natDegree_lt_card_of_eval_eq _ _ (chart_injective t v w lin)
  · intro yz
    rw [recover_at t v w hv hw lin,forward_at]
  · rw [Fintype.card_prod]
    exact max_lt (recover_degree ..) size


private noncomputable def traceMap (L K : Type*) [Field L] [Fintype L] [Field K] [Algebra L K] :
    K →ₗ[L] K :=
  LinearMap.id + (phi L K).toLinearMap + ((phi L K).comp (phi L K)).toLinearMap

/-- A cubic binary extension supplies the required independent pair without
an extra hypothesis on the normal basis or the coordinates of the fibre. -/
theorem exists_cubic_chart [Fintype K] [FiniteDimensional L K] [CharP K 2]
    (dim : Module.finrank L K=3) :
    ∃ v w : K, traceValue L v=0 ∧ traceValue L w=0 ∧ independent L v w := by
  classical
  let n := Fintype.card L
  let f := traceMap L K
  let fr := phi L K
  have card : Fintype.card K=n^3 := by
    rw [Module.card_eq_pow_finrank (K:=L),dim]
  have third (x : K) : fr (fr (fr x))=x := by
    change ((x^n)^n)^n=x
    rw [←pow_mul,←pow_mul,show n*(n*n)=n^3 by ring,←card,FiniteField.pow_card]
  have fixed (x : K) : fr (f x)=f x := by
    change fr (x+fr x+fr (fr x))=x+fr x+fr (fr x)
    rw [map_add,map_add,third]
    abel
  have contained : f.range≤Submodule.span L {(1:K)} := by
    rintro _ ⟨x,rfl⟩
    obtain ⟨c,hc⟩ := (fixed_iff (L:=L) (f x)).mp (fixed x)
    exact Submodule.mem_span_singleton.mpr ⟨c, by simpa [Algebra.smul_def] using hc⟩
  have one : f 1=1 := by
    change 1+fr 1+fr (fr 1)=1
    simp [CharTwo.add_self_eq_zero]
  have onto : f.range=Submodule.span L {(1:K)} := by
    apply le_antisymm contained
    apply Submodule.span_le.mpr
    rintro x hx
    have eq : x=1 := by simpa using hx
    exact ⟨1, one.trans eq.symm⟩
  have ranks := f.finrank_range_add_finrank_ker
  rw [onto,finrank_span_singleton one_ne_zero,dim] at ranks
  have hk : Module.finrank L f.ker=2 := by omega
  let B := Module.finBasisOfFinrankEq L f.ker hk
  let v := (B 0 : K)
  let w := (B 1 : K)
  refine ⟨v,w,(B 0).property,(B 1).property,?_⟩
  intro y z zero
  have inside : y • B 0 + z • B 1 = (0 : f.ker) := by
    apply Subtype.ext
    simpa [v,w,Algebra.smul_def,mul_comm] using zero
  constructor
  · have eq := congrArg (fun x => B.repr x (0 : Fin 2)) inside
    simpa using eq
  · have eq := congrArg (fun x => B.repr x (1 : Fin 2)) inside
    simpa using eq


private noncomputable def pullHom (a : ℕ) (t v w : K) : Bi K →+* K[X] :=
  (MvPolynomial.eval₂Hom Polynomial.C (coords X (X^a))).comp
    (MvPolynomial.eval₂Hom MvPolynomial.C (inverseVars a t v w))

private theorem pull_C (a : ℕ) (t v w r : K) : pullHom a t v w (MvPolynomial.C r)=C r := by
  simp [pullHom]

private theorem pull_var_degree (a : ℕ) (ha : 1≤a) (t v w : K) (b : Bool) :
    (pullHom a t v w (MvPolynomial.X b)).natDegree≤a := by
  have ud : (X-C t : K[X]).natDegree≤a :=
    (natDegree_sub_le ..).trans (by simpa using ha)
  have zd : (X^a-C t : K[X]).natDegree≤a :=
    (natDegree_sub_le ..).trans (by simp)
  have two (u z : K[X]) (hu : u.natDegree≤a) (hz : z.natDegree≤a) (c p q : K) :
      (C c*(C p*u-C q*z)).natDegree≤a :=
    (natDegree_C_mul_le ..).trans ((natDegree_sub_le ..).trans
      (max_le ((natDegree_C_mul_le ..).trans hu) ((natDegree_C_mul_le ..).trans hz)))
  cases b
  · simpa [pullHom,inverseVars,coords,MvPolynomial.eval₂_sub] using
      two _ _ ud zd (det a v w)⁻¹ (w^a) w
  · simpa [pullHom,inverseVars,coords,MvPolynomial.eval₂_sub] using
      two _ _ zd ud (det a v w)⁻¹ v (v^a)

private theorem pull_indicator_degree (t v w : K) (b : Bool) (r : L) :
    let a := Fintype.card L
    (pullHom a t v w (indicator b r)).natDegree≤a*(a-1) := by
  let a := Fintype.card L
  let H := pullHom a t v w
  change (H (1-(MvPolynomial.X b-MvPolynomial.C (algebraMap L K r))^(a-1))).natDegree≤a*(a-1)
  have hc : H (MvPolynomial.C (algebraMap L K r))=C (algebraMap L K r) := pull_C ..
  rw [map_sub,map_one,map_pow,map_sub,hc]
  apply (natDegree_sub_le ..).trans
  apply max_le (by simp)
  have dx : (H (MvPolynomial.X b)-C (algebraMap L K r)).natDegree≤a :=
    (natDegree_sub_le ..).trans (max_le (pull_var_degree a (by dsimp [a]; exact Fintype.card_pos) t v w b) (by simp))
  exact natDegree_pow_le.trans
    ((Nat.mul_le_mul_left _ dx).trans_eq (Nat.mul_comm _ _))

/-- The literal polynomial before the one high fold. Its degree is at most
2a(a-1), even when all entries of the grid are independent. -/
noncomputable def inverseLift (t : L) (v w : K) (values : L×L→K) : K[X] :=
  collapse (Fintype.card L) (subst (inverseVars (Fintype.card L) (algebraMap L K t) v w) (interp values))

theorem inverseLift_degree (t : L) (v w : K) (values : L×L→K) :
    let a := Fintype.card L
    (inverseLift t v w values).natDegree ≤ 2*(a*(a-1)) := by
  let a := Fintype.card L
  let H := pullHom a (algebraMap L K t) v w
  change (H (interp values)).natDegree≤2*(a*(a-1))
  rw [interp,map_sum]
  apply natDegree_sum_le_of_forall_le
  intro y _
  rw [map_sum]
  apply natDegree_sum_le_of_forall_le
  intro z _
  rw [map_mul,map_mul,pull_C]
  have yl := pull_indicator_degree (algebraMap L K t) v w false y
  have zl := pull_indicator_degree (algebraMap L K t) v w true z
  apply natDegree_mul_le.trans
  calc
    _ ≤ a*(a-1)+a*(a-1) := Nat.add_le_add ((natDegree_C_mul_le ..).trans yl) zl
    _ = _ := by ring

/-- The general remainder used by recover is exactly the one-fold formula
which splits the collapsed polynomial once into low and high a²-bit powers. -/
theorem inverse_one_fold (t : L) (v w : K) (values : L×L→K) :
    let a := Fintype.card L
    let f := inverseLift t v w values
    let base : K[X] := X^(a*a)
    let e := X^a+X-C (algebraMap L K t)
    recover t v w values = f%ₘbase-e*(f/ₘbase) := by
  let a := Fintype.card L
  let N := a*a
  let f := inverseLift t v w values
  let base : K[X] := X^N
  let e : K[X] := X^a+X-C (algebraMap L K t)
  let B := f/ₘbase
  let A := f%ₘbase
  have h1 : 1<a := Fintype.one_lt_card
  have baseDeg : base.natDegree=N := natDegree_X_pow _
  have bounds := inverseLift_degree t v w values
  change f.natDegree≤2*(a*(a-1)) at bounds
  have exact_bound : 2*(a*(a-1))=2*N-2*a := by
    dsimp [N]
    rw [Nat.mul_sub, Nat.mul_one,Nat.mul_sub]
  have bdeg : B.natDegree ≤ N-2*a := by
    rw [show B.natDegree=f.natDegree-base.natDegree from natDegree_divByMonic f (monic_X_pow _),baseDeg]
    rw [exact_bound] at bounds
    omega
  have edeg : e.natDegree ≤ a := by
    apply (natDegree_sub_le ..).trans
    apply max_le _ (by simp)
    exact (natDegree_add_le ..).trans (by simp; omega)
  have esmall : a+(N-2*a)<N := by
    have two : 2*a≤N := by dsimp [N]; nlinarith
    omega
  have small : (e*B).degree < (N:WithBot ℕ) := by
    apply degree_le_natDegree.trans_lt
    exact_mod_cast natDegree_mul_le.trans_lt ((Nat.add_le_add edeg bdeg).trans_lt esmall)
  have adeg : A.degree < (N:WithBot ℕ) := by
    simpa [base] using f.degree_modByMonic_lt (monic_X_pow (R:=K) N)
  have ht := fibre_monic (K:=K) t
  have remDeg : (A-e*B).degree < (fibrePoly (K:=K) t).degree := by
    rw [degree_eq_natDegree ht.1.ne_zero,ht.2]
    exact (degree_sub_le ..).trans_lt (max_lt adeg small)
  change f %ₘ fibrePoly t=A-e*B
  apply (div_modByMonic_unique B _ ht.1 ⟨?_,remDeg⟩).2
  change A-e*B+(base+e)*B = f
  rw [show A-e*B+(base+e)*B=A+base*B by ring]
  exact modByMonic_add_div f base


/-- The physical two-axis polynomial rectangle, expressed directly on
ordinary occupied coefficient positions. -/
def rectangle (a : ℕ) (P : Bi K) :=
  ∀s∈P.support, s false<a ∧ s true<a

private noncomputable def geometricLift (t : L) (v w : K) (G : Bi K) :=
  collapse (Fintype.card L) (subst (inverseVars (Fintype.card L) (algebraMap L K t) v w) G)

/-- Reversing the affine polynomial substitution has the correct value
at every point, for any interpolating polynomial provided by either axis
algorithm. -/
theorem geometricLift_at (t : L) (v w : K) (lin : independent L v w)
    (G : Bi K) (yz : L×L) :
    (geometricLift t v w G).eval (chart t v w yz) =
      MvPolynomial.eval (coords (algebraMap L K yz.1) (algebraMap L K yz.2)) G := by
  rw [geometricLift,collapse_at,subst,←MvPolynomial.eval_assoc,undo_on_grid t v w (moore_ne_zero v w lin)]

/-- The same pre-fold degree bound holds for every supplied rectangle. -/
theorem rectangle_lift_degree (t : L) (v w : K) (G : Bi K) (rect : rectangle (Fintype.card L) G) :
    let a := Fintype.card L
    (geometricLift t v w G).natDegree≤2*(a*(a-1)) := by
  classical
  let a := Fintype.card L
  let H := pullHom a (algebraMap L K t) v w
  change (H G).natDegree≤2*(a*(a-1))
  have ce : H.comp MvPolynomial.C=Polynomial.C := RingHom.ext (fun x => pull_C a (algebraMap L K t) v w x)
  have expand : H G=G.eval₂ Polynomial.C (fun i => H (MvPolynomial.X i)) := calc
    _=H (G.eval₂ MvPolynomial.C MvPolynomial.X) := congrArg H (MvPolynomial.eval₂_eta G).symm
    _=_ := by rw [MvPolynomial.hom_eval₂,ce]
  rw [expand,MvPolynomial.eval₂_eq']
  apply natDegree_sum_le_of_forall_le
  intro d hd
  rw [Fintype.prod_bool]
  apply (natDegree_C_mul_le ..).trans
  apply natDegree_mul_le.trans
  rw [natDegree_pow,natDegree_pow]
  obtain ⟨df,dt⟩ := rect d hd
  change d false<a at df
  change d true<a at dt
  have bound (b : Bool) := pull_var_degree a (by dsimp [a]; exact Fintype.card_pos) (algebraMap L K t) v w b
  calc
    _ ≤ (a-1)*a+(a-1)*a := Nat.add_le_add (Nat.mul_le_mul (by omega) (bound true))
        (Nat.mul_le_mul (by omega) (bound false))
    _ = _ := by ring

/-- On a base-field coordinate the replacement n ↦ n-a+1 preserves the
monomial for every n≥a, including the zero point. -/
def foldExponent (a n : ℕ) := if n<a then n else n-a+1

private theorem fold_power (x : K) (a n : ℕ) (fixed : x^a=x) : x^(foldExponent a n)=x^n := by
  by_cases lt : n<a
  · simp [foldExponent,lt]
  · rw [foldExponent,ite_eq_right lt,pow_succ]
    calc
      _=x^(n-a)*x^a := by rw [fixed]
      _=x^n := by rw [←pow_add,show n-a+a=n by omega]

private theorem fold_below {a n : ℕ} (ha : 1<a) (hl : n≤2*(a-1)) :
    foldExponent a n<a := by unfold foldExponent; split <;> omega

/-- Reduce each axis once modulo X^a-X on the actual monomial supports. -/
noncomputable def foldAxes (a : ℕ) (P : Bi K) : Bi K :=
  ∑ d∈P.support, MvPolynomial.C (P.coeff d) *
      MvPolynomial.X false^(foldExponent a (d false)) *
      MvPolynomial.X true^(foldExponent a (d true))

theorem foldAxes_at (P : Bi K) (yz : L×L) :
    let u := coords (algebraMap L K yz.1) (algebraMap L K yz.2)
    MvPolynomial.eval u (foldAxes (Fintype.card L) P)=MvPolynomial.eval u P := by
  dsimp only
  let a:=Fintype.card L
  let x:=algebraMap L K yz.1
  let y:=algebraMap L K yz.2
  have fx : x^a=x := by simp [x,a,←map_pow,FiniteField.pow_card]
  have fy : y^a=y := by simp [y,a,←map_pow,FiniteField.pow_card]
  rw [foldAxes,map_sum,MvPolynomial.eval_eq' _ P]
  apply Finset.sum_congr rfl
  intro d _
  simp only [map_mul,map_pow,MvPolynomial.eval_C,MvPolynomial.eval_X,Fintype.prod_bool]
  change P.coeff d*x^(foldExponent a (d false))*y^(foldExponent a (d true))=
    P.coeff d*(y^(d true)*x^(d false))
  rw [fold_power x a _ fx,fold_power y a _ fy]
  ring

private theorem forward_var (a : ℕ) (t v w : K) (b : Bool) :
    (forwardVars a t v w b).totalDegree≤1 := by
  have affine (p q : K) : (MvPolynomial.C t+MvPolynomial.C p*(MvPolynomial.X false : Bi K)+
      MvPolynomial.C q*MvPolynomial.X true).totalDegree≤1 := by
    have scale (x : K) (j : Bool) : (MvPolynomial.C x*MvPolynomial.X j : Bi K).totalDegree≤1 :=
      (MvPolynomial.totalDegree_mul ..).trans (by simp)
    apply (MvPolynomial.totalDegree_add ..).trans
    exact max_le ((MvPolynomial.totalDegree_add ..).trans (max_le (by simp) (scale ..))) (scale ..)
  cases b <;> apply affine

/-- The literal external packing and affine change produce no coordinate
larger than 2a-2 throughout their terminal polynomial. -/
theorem forward_degree (t : L) (v w : K) (P : K[X])
    (bound : P.natDegree<Fintype.card L*Fintype.card L) :
    (forward t v w P).totalDegree≤2*(Fintype.card L-1) := by
  let a:=Fintype.card L
  let H := MvPolynomial.eval₂Hom MvPolynomial.C (forwardVars a (algebraMap L K t) v w)
  have pos : 0<a := Fintype.card_pos
  change (H (pack a P)).totalDegree≤2*(a-1)
  rw [pack,map_sum]
  apply MvPolynomial.totalDegree_finsetSum_le
  intro k hk
  have kn : k<a*a := by have := Finset.mem_range.mp hk; change P.natDegree<a*a at bound; omega
  have md := Nat.mod_lt k pos
  have qd := (Nat.div_lt_iff_lt_mul pos).mpr kn
  rw [map_mul,map_mul,map_pow,map_pow]
  have hc : (H (MvPolynomial.C (P.coeff k))).totalDegree=0 := by simp [H]
  have dx (b : Bool) (r : ℕ) : ((H (MvPolynomial.X b))^r).totalDegree≤r := by
    rw [show H (MvPolynomial.X b)=forwardVars a (algebraMap L K t) v w b from MvPolynomial.eval₂Hom_X' ..]
    exact (MvPolynomial.totalDegree_pow ..).trans ((Nat.mul_le_mul_left r (forward_var a (algebraMap L K t) v w b)).trans_eq (Nat.mul_one _))
  apply (MvPolynomial.totalDegree_mul ..).trans
  have low := MvPolynomial.totalDegree_mul (H (MvPolynomial.C (P.coeff k))) ((H (MvPolynomial.X false))^(k%a))
  rw [hc,zero_add] at low
  have u := low.trans (dx false (k%a))
  have e := dx true (k/a)
  omega

theorem foldAxes_rectangle (a : ℕ) (ha : 1<a) (P : Bi K) (hp : P.totalDegree≤2*(a-1)) :
    rectangle a (foldAxes a P) := by
  classical
  have exp (b : Bool) (d : Bool→₀ℕ) (hd : d∈P.support) : foldExponent a (d b)≤a-1 := by
    have h := (MvPolynomial.degreeOf_le_iff.mp (MvPolynomial.degreeOf_le_totalDegree P b)) d hd
    have h' := fold_below ha (h.trans hp)
    omega
  have lim (b : Bool) : (foldAxes a P).degreeOf b≤a-1 := by
    apply (MvPolynomial.degreeOf_sum_le ..).trans
    apply Finset.sup_le
    intro d hd
    apply (MvPolynomial.degreeOf_mul_le ..).trans
    have hleft := MvPolynomial.degreeOf_mul_le b (MvPolynomial.C (P.coeff d)) (MvPolynomial.X false ^ foldExponent a (d false))
    rw [MvPolynomial.degreeOf_C,zero_add] at hleft
    cases b
    · simpa [MvPolynomial.degreeOf_X_pow_of_ne] using hleft.trans (by simpa using exp false d hd)
    · have hz : (MvPolynomial.C (P.coeff d)*MvPolynomial.X false ^ foldExponent a (d false)).degreeOf true=0 :=
        Nat.eq_zero_of_le_zero (by simpa [MvPolynomial.degreeOf_X_pow_of_ne] using hleft)
      simpa [hz] using exp true d hd
  intro d hd
  have l := MvPolynomial.degreeOf_le_iff.mp (lim false) d hd
  have r := MvPolynomial.degreeOf_le_iff.mp (lim true) d hd
  omega

/-- Both the actual two-axis bounded rectangle and its values are certified. -/
theorem forward_rectangle (t : L) (v w : K) (P : K[X])
    (bound : P.natDegree<Fintype.card L*Fintype.card L) :
    let G := foldAxes (Fintype.card L) (forward t v w P)
    rectangle (Fintype.card L) G ∧ ∀ yz : L×L,
      MvPolynomial.eval (coords (algebraMap L K yz.1) (algebraMap L K yz.2)) G=P.eval (chart t v w yz) := by
  exact ⟨foldAxes_rectangle _ Fintype.one_lt_card _ (forward_degree t v w P bound),
    fun yz => (foldAxes_at _ yz).trans (forward_at t v w P yz)⟩


#print axioms forward_rectangle
#print axioms rectangle_lift_degree
#print axioms inverse_one_fold
#print axioms inverseLift_degree
#print axioms exists_cubic_chart
#print axioms round_trip
#print axioms fibre_iff
#print axioms recover_at
#print axioms recover_degree
#print axioms forward_at
#print axioms moore_ne_zero
#print axioms forward_evaluates

end Moonshot.AffineTraceGrid
