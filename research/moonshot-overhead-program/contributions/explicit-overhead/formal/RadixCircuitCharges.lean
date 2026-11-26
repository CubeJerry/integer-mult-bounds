import TraceRadixMatrix

/-!
# Counting shared XOR gates across ordered coefficient cuts

A polynomial stores the original input coefficients in a signal. Its lowest
nonzero degree is the least participating input index. Each circuit names its
operand forms, together with proofs that each is an input or a previous sum.
Unbounded reuse of inputs and intermediate results is allowed.
-/
namespace Moonshot.RadixCircuitCharges
open Polynomial Matrix
open scoped Polynomial BigOperators

variable {F : Type*} [Field F]

/-- Topologically ordered additions with no auxiliary input linear forms. -/
structure Circuit (F : Type*) [Field F] (n g : ℕ) where
  left : Fin g → F[X]
  right : Fin g → F[X]
  left_source : ∀ j, (∃ t : Fin n, left j = X^t.val) ∨
    ∃ k : Fin g, k < j ∧ left j = left k + right k
  right_source : ∀ j, (∃ t : Fin n, right j = X^t.val) ∨
    ∃ k : Fin g, k < j ∧ right j = left k + right k

variable {n g : ℕ}

def Circuit.available (C : Circuit F n g) (x : F[X]) :=
  (∃ j : Fin n, x=X^j.val) ∨ ∃ k : Fin g, x=C.left k+C.right k

/-- Every output is an available signal with the prescribed coefficients. -/
def Circuit.realizes (C : Circuit F n g) (M : Matrix (Fin n) (Fin n) F) :=
  ∀ i, ∃ x, C.available x ∧ ∀ j, x.coeff j.val = M i j

/-- Counted minimum cancellations. Zero-form gates never provide an extra
projected vector. -/
def Circuit.jumps (C : Circuit F n g) (j : Fin g) :=
  C.left j ≠ 0 ∧ C.right j ≠ 0 ∧ C.left j + C.right j ≠ 0 ∧
    (C.left j).natTrailingDegree = (C.right j).natTrailingDegree ∧
    (C.left j).natTrailingDegree < (C.left j + C.right j).natTrailingDegree

private abbrev inside (s h t : ℕ) := s ≤ t ∧ t < s+h

private abbrev crosses (s h a b : ℕ) := inside s h a ∧ inside (s+h) h b

private abbrev ordinary (s h a b : ℕ) := crosses s h a b ∨ crosses s h b a

private def exceptional (C : Circuit F n g) (s h : ℕ) (j : Fin g) :=
  C.jumps j ∧ (C.left j).natTrailingDegree < s ∧
    inside s h (C.left j+C.right j).natTrailingDegree

private def charged (C : Circuit F n g) (s h : ℕ) (j : Fin g) :=
  ordinary s h (C.left j).natTrailingDegree (C.right j).natTrailingDegree ∨ exceptional C s h j

private noncomputable def source (C : Circuit F n g) (s h : ℕ) (j : Fin g) : F[X] := by
  classical
  exact if crosses s h (C.left j).natTrailingDegree (C.right j).natTrailingDegree then C.right j
    else if crosses s h (C.right j).natTrailingDegree (C.left j).natTrailingDegree then C.left j
    else C.left j+C.right j

private def view (s h : ℕ) (f : F[X]) : Fin h → F := fun j => f.coeff (s+h+j.val)

private theorem view_add (s h : ℕ) (x y : F[X]) : view s h (x+y) = view s h x + view s h y := by
  ext i; exact coeff_add ..

private theorem view_zero (s h : ℕ) : view s h (0 : F[X]) = 0 := by ext i; simp [view]

private theorem view_above {s h : ℕ} {f : F[X]} (far : s+2*h ≤ f.natTrailingDegree) :
    view s h f = 0 := by
  ext i
  apply coeff_eq_zero_of_lt_natTrailingDegree
  have := i.isLt
  omega

private theorem pivot_lower {x y : F[X]} (hz : x+y≠0) :
    min x.natTrailingDegree y.natTrailingDegree ≤ (x+y).natTrailingDegree := by
  by_contra! hl
  rw [lt_min_iff] at hl
  have hnon := coeff_natTrailingDegree_ne_zero.mpr hz
  rw [coeff_add, coeff_eq_zero_of_lt_natTrailingDegree hl.1,
    coeff_eq_zero_of_lt_natTrailingDegree hl.2, zero_add] at hnon
  exact hnon rfl

private theorem pivot_add_left {x y : F[X]} (hx : x≠0) (hlt : x.natTrailingDegree < y.natTrailingDegree) :
    (x+y).natTrailingDegree = x.natTrailingDegree := by
  have nz : (x+y).coeff x.natTrailingDegree ≠ 0 := by
    rw [coeff_add, coeff_eq_zero_of_lt_natTrailingDegree hlt, add_zero]
    exact coeff_natTrailingDegree_ne_zero.mpr hx
  have hxy : x+y ≠ 0 := by intro e; simp [e] at nz
  exact le_antisymm (natTrailingDegree_le_of_ne_zero nz) ((min_eq_left hlt.le) ▸ pivot_lower hxy)

private theorem side_transfer (s h : ℕ) (W : Submodule F (Fin h → F)) (a b : F[X])
    (aIn : inside s h a.natTrailingDegree) (hab : a.natTrailingDegree<b.natTrailingDegree)
    (takeA : inside s h a.natTrailingDegree → view s h a ∈ W)
    (takeB : inside s h b.natTrailingDegree → view s h b ∈ W)
    (crossB : crosses s h a.natTrailingDegree b.natTrailingDegree → view s h b ∈ W) :
    view s h (a+b) ∈ W := by
  rw [view_add]
  apply W.add_mem (takeA aIn)
  by_cases lo : b.natTrailingDegree<s+h
  · exact takeB ⟨by have := aIn.1; omega,lo⟩
  by_cases hi : b.natTrailingDegree<s+h+h
  · exact crossB ⟨aIn,by omega,hi⟩
  rw [view_above (by omega : s+2*h≤b.natTrailingDegree)]
  exact W.zero_mem

private theorem input_span (s h : ℕ) (W : Submodule F (Fin h → F)) (t : ℕ)
    (hL : inside s h (X^t : F[X]).natTrailingDegree) : view s h (X^t : F[X]) ∈ W := by
  rw [natTrailingDegree_X_pow] at hL
  have z : view s h (X^t : F[X]) = 0 := by
    ext i
    change (X^t : F[X]).coeff (s+h+i.val) = 0
    rw [coeff_X_pow, ite_eq_right (by have := hL.2; omega)]
  rw [z]; exact W.zero_mem

private theorem signals_span (C : Circuit F n g) (s h : ℕ) (W : Submodule F (Fin h → F))
    (receipt : ∀ j, charged C s h j → view s h (source C s h j) ∈ W) (x : F[X])
    (available : C.available x) (inL : inside s h x.natTrailingDegree) : view s h x ∈ W := by
  classical
  have all_gates (u : Fin g) : inside s h (C.left u + C.right u).natTrailingDegree →
      view s h (C.left u + C.right u) ∈ W := by
    induction u using Fin.strong_induction_on with
    | h j ih =>
      let a := C.left j
      let b := C.right j
      intro result
      change inside s h (a+b).natTrailingDegree at result
      change view s h (a+b) ∈ W
      have before (y : F[X]) (valid : (∃t:Fin n, y=X^t.val) ∨ ∃k:Fin g, k<j ∧ y=C.left k+C.right k)
          (hin : inside s h y.natTrailingDegree) : view s h y ∈ W := by
        rcases valid with ⟨t,rfl⟩ | ⟨k,hk,rfl⟩
        · exact input_span s h W _ hin
        · exact ih k hk hin
      have takeA := before a (C.left_source j)
      have takeB := before b (C.right_source j)
      by_cases az : a=0
      · simp [az] at result ⊢; exact takeB result
      by_cases bz : b=0
      · simp [bz] at result ⊢; exact takeA result
      by_cases sumZ : a+b=0
      · rw [sumZ, view_zero]; exact W.zero_mem
      rcases lt_trichotomy a.natTrailingDegree b.natTrailingDegree with lt | eq | gt
      · rw [pivot_add_left az lt] at result
        apply side_transfer s h W a b result lt takeA takeB
        intro cross
        have ticket := receipt j (Or.inl (Or.inl cross))
        change view s h (if crosses s h a.natTrailingDegree b.natTrailingDegree then b else _) ∈ W at ticket
        rw [ite_eq_left cross] at ticket
        exact ticket
      · have monotone : a.natTrailingDegree ≤ (a+b).natTrailingDegree := by simpa [eq] using pivot_lower sumZ
        by_cases below : a.natTrailingDegree < s
        · have moved : a.natTrailingDegree < (a+b).natTrailingDegree := below.trans_le result.1
          have jump : C.jumps j := ⟨az,bz,sumZ,eq,moved⟩
          have ticket := receipt j (Or.inr ⟨jump,below,result⟩)
          have noLeft : ¬crosses s h a.natTrailingDegree b.natTrailingDegree := by intro e; have := e.1.1; omega
          have noRight : ¬crosses s h b.natTrailingDegree a.natTrailingDegree := by intro e; have := e.1.1; omega
          change view s h (if crosses s h a.natTrailingDegree b.natTrailingDegree then b else
            if crosses s h b.natTrailingDegree a.natTrailingDegree then a else a+b) ∈ W at ticket
          simpa only [noLeft, noRight, ↓reduceIte] using ticket
        have aIn : inside s h a.natTrailingDegree := ⟨by omega, by have := result.2; omega⟩
        rw [view_add]; exact W.add_mem (takeA aIn) (takeB (eq ▸ aIn))
      · rw [add_comm] at result ⊢
        rw [pivot_add_left bz gt] at result
        apply side_transfer s h W b a result gt takeB takeA
        intro cross
        have ticket := receipt j (Or.inl (Or.inr cross))
        have noLeft : ¬crosses s h a.natTrailingDegree b.natTrailingDegree := by
          intro e; have := e.1.2; have := cross.2.1; omega
        change view s h (if crosses s h a.natTrailingDegree b.natTrailingDegree then b else
          if crosses s h b.natTrailingDegree a.natTrailingDegree then a else a+b) ∈ W at ticket
        rw [ite_eq_right noLeft, ite_eq_left cross] at ticket
        exact ticket
  rcases available with ⟨t,rfl⟩ | ⟨j,rfl⟩
  · exact input_span s h W _ inL
  · exact all_gates j inL


private theorem output_pivot (M : Matrix (Fin n) (Fin n) F) (htri : M.IsUpperTriangular)
    (hdiag : ∀i, M i i≠0) (i : Fin n) (x : F[X]) (hx : ∀j : Fin n, x.coeff j.val = M i j) :
    x.natTrailingDegree = i.val := by
  have n1 : x.coeff i.val ≠ 0 := (hx i) ▸ hdiag i
  have nz : x≠0 := by intro e; simp [e] at n1
  apply le_antisymm (natTrailingDegree_le_of_ne_zero n1)
  by_contra! lt
  let j : Fin n := ⟨x.natTrailingDegree, lt.trans i.isLt⟩
  have eq := (hx j).trans (htri (show j < i from lt))
  exact (coeff_natTrailingDegree_ne_zero.mpr nz) eq

/-- Count of scalar gates which can contribute an independent vector at a
particular cut, given the actual external input ordering. -/
noncomputable def chargesAt (C : Circuit F n g) (s h : ℕ) : Finset (Fin g) := by
  classical exact Finset.univ.filter (charged C s h)

/-- An arbitrary topological scalar-sum circuit for an upper triangular
matrix must supply the entire right-input row rank at every adjacent cut. -/
theorem interval_rank_le (C : Circuit F n g) (M : Matrix (Fin n) (Fin n) F)
    (computes : C.realizes M) (htri : M.IsUpperTriangular) (hdiag : ∀i, M i i≠0)
    (s h : ℕ) (bound : s+2*h≤n) :
    let l := TraceRadixMatrix.atOffset (h:=h) s (n:=n) (by omega)
    let r := TraceRadixMatrix.atOffset (h:=h) (s+h) (n:=n) (by omega)
    (M.submatrix l r).rank ≤ (chargesAt C s h).card := by
  classical
  dsimp only
  let l := TraceRadixMatrix.atOffset (h:=h) s (n:=n) (by omega)
  let r := TraceRadixMatrix.atOffset (h:=h) (s+h) (n:=n) (by omega)
  let S := chargesAt C s h
  let receipt (j : S) := view s h (source C s h j.val)
  let W := Submodule.span F (Set.range receipt)
  have recorded (j : Fin g) (hc : charged C s h j) : view s h (source C s h j) ∈ W := by
    apply Submodule.subset_span
    exact ⟨⟨j,Finset.mem_filter.mpr ⟨Finset.mem_univ _,hc⟩⟩,rfl⟩
  have rows : Submodule.span F (Set.range (M.submatrix l r).row) ≤ W := by
    apply Submodule.span_le.mpr
    intro row hrow
    obtain ⟨i,rfl⟩ := hrow
    obtain ⟨x,hx,hcoef⟩ := computes (l i)
    have pi := output_pivot M htri hdiag (l i) x hcoef
    have pIn : inside s h x.natTrailingDegree := by
      rw [pi]; change s≤s+i.val ∧ s+i.val<s+h; have := i.isLt; omega
    have sub := signals_span C s h W recorded x hx pIn
    have eq : view s h x = (M.submatrix l r).row i := by ext j; exact hcoef (r j)
    exact eq ▸ sub
  rw [Matrix.rank_eq_finrank_span_row]
  exact (Submodule.finrank_mono rows).trans ((finrank_range_le_card receipt).trans_eq (Fintype.card_coe _))


private theorem index_unique {t p q x : ℕ} (pLo : t*p≤x) (pHi : x<t*(p+1))
    (qLo : t*q≤x) (qHi : x<t*(q+1)) : p=q := by
  apply le_antisymm
  · exact Nat.le_of_lt_succ (Nat.lt_of_mul_lt_mul_left (pLo.trans_lt qHi))
  · exact Nat.le_of_lt_succ (Nat.lt_of_mul_lt_mul_left (qLo.trans_lt pHi))

private theorem no_larger_cross {v i j p q x y : ℕ} (hij : i<j)
    (small : crosses (2*(v*2^i)*p) (v*2^i) x y)
    (large : crosses (2*(v*2^j)*q) (v*2^j) x y) : False := by
  obtain ⟨k,hk⟩ := Nat.exists_eq_add_of_le (Nat.succ_le_of_lt hij)
  have factor : v*2^j = 2*(v*2^i)*(2^k) := by rw [hk, pow_add, pow_succ]; ring
  let t := 2*(v*2^i)
  let b := 2^k*(2*q+1)
  have mid : 2*(v*2^j)*q + (v*2^j) = t*b := by rw [factor]; dsimp [t,b]; ring
  have low : t*p<t*b := by simpa only [mid] using small.1.1.trans_lt large.1.2
  have high : t*b<t*(p+1) := by
    rw [← mid]
    exact large.2.1.trans_lt (small.2.2.trans_eq (by dsimp [t]; ring))
  have := Nat.lt_of_mul_lt_mul_left low
  have := Nat.lt_of_mul_lt_mul_left high
  omega

private theorem cross_unique {v i j p q x y : ℕ}
    (a : crosses (2*(v*2^i)*p) (v*2^i) x y)
    (b : crosses (2*(v*2^j)*q) (v*2^j) x y) : i=j ∧ p=q := by
  rcases lt_trichotomy i j with lt | eq | gt
  · exact (no_larger_cross lt a b).elim
  · subst j
    refine ⟨rfl, index_unique a.1.1 ?_ b.1.1 ?_⟩
    · exact a.1.2.trans_le (by rw [Nat.mul_succ]; omega)
    · exact b.1.2.trans_le (by rw [Nat.mul_succ]; omega)
  · exact (no_larger_cross gt b a).elim

private theorem ordinary_unique {v i j p q x y : ℕ}
    (a : ordinary (2*(v*2^i)*p) (v*2^i) x y)
    (b : ordinary (2*(v*2^j)*q) (v*2^j) x y) : i=j ∧ p=q := by
  rcases a with a|a <;> rcases b with b|b
  · exact cross_unique a b
  · have := a.1.2.trans_le a.2.1
    have := b.1.2.trans_le b.2.1
    omega
  · have := a.1.2.trans_le a.2.1
    have := b.1.2.trans_le b.2.1
    omega
  · exact cross_unique a b

/-- The number of gates which cancel their least contributing input index. -/
noncomputable def jumpGates (C : Circuit F n g) : Finset (Fin g) := by
  classical exact Finset.univ.filter C.jumps

/-- Dyadic windows at the requested scales. The number of included full
parents may be chosen independently at each scale. -/
abbrev Cuts (d : ℕ) (parents : Fin d → ℕ) := (i : Fin d) × Fin (parents i)

private abbrev half (v : ℕ) {d : ℕ} {parents : Fin d → ℕ} (t : Cuts d parents) := v*2^t.1.val

private abbrev start (v : ℕ) {d : ℕ} {parents : Fin d → ℕ} (t : Cuts d parents) := 2*half v t*t.2.val

private theorem distinct_cut {d : ℕ} {parents : Fin d → ℕ} {a b : Cuts d parents}
    (iEq : a.1.val=b.1.val) (pEq : a.2.val=b.2.val) : a=b := by
  obtain ⟨i,p⟩ := a
  obtain ⟨j,q⟩ := b
  obtain rfl : i=j := Fin.ext iEq
  obtain rfl : p=q := Fin.ext pEq
  rfl

private theorem gate_total (C : Circuit F n g) (v d : ℕ) (parents : Fin d→ℕ) (j : Fin g) :
    let selected := Finset.univ.filter (fun t : Cuts d parents => j ∈ chargesAt C (start v t) (half v t))
    selected.card ≤ 1 + if j∈jumpGates C then d else 0 := by
  classical
  let S := Finset.univ.filter (fun t : Cuts d parents => j ∈ chargesAt C (start v t) (half v t))
  change S.card ≤ _
  have chargedAt {t : Cuts d parents} (ht : t∈S) : charged C (start v t) (half v t) j :=
    (Finset.mem_filter.mp (Finset.mem_filter.mp ht).2).2
  by_cases jump : C.jumps j
  · have exceptionalAt {t : Cuts d parents} (ht : t∈S) : exceptional C (start v t) (half v t) j := by
      rcases chargedAt ht with regular|ex
      · have eq := jump.2.2.2.1
        rcases regular with cross|cross
        all_goals have := cross.1.2; have := cross.2.1; omega
      · exact ex
    have inj : Set.InjOn (fun t : Cuts d parents => t.1) (S : Set (Cuts d parents)) := by
      intro a ha b hb same
      have ia := (exceptionalAt ha).2.2
      have ib := (exceptionalAt hb).2.2
      have sameH : half v a=half v b := by simp [half,same]
      have ip : a.2.val=b.2.val := by
        apply index_unique ia.1 ?_ (sameH ▸ ib.1) ?_
        · exact ia.2.trans_le (by dsimp [start]; rw [Nat.mul_succ]; omega)
        · have hb' := ib.2
          dsimp [start] at hb' ⊢
          rw [← sameH] at hb'
          exact hb'.trans_le (by rw [Nat.mul_succ]; omega)
      exact distinct_cut (congrArg Fin.val same) ip
    have bound : S.card≤d := by
      rw [← Finset.card_image_of_injOn inj]
      simpa using (S.image (fun t => t.1)).card_le_univ
    have jj : j∈jumpGates C := Finset.mem_filter.mpr ⟨Finset.mem_univ _,jump⟩
    rw [ite_eq_left jj]; omega
  · have regularAt {t : Cuts d parents} (ht : t∈S) :
        ordinary (start v t) (half v t) (C.left j).natTrailingDegree (C.right j).natTrailingDegree := by
      rcases chargedAt ht with reg|ex
      · exact reg
      · exact (jump ex.1).elim
    have bound : S.card≤1 := Finset.card_le_one.mpr (fun a ha b hb =>
      let eq := ordinary_unique (regularAt ha) (regularAt hb)
      distinct_cut eq.1 eq.2)
    have jj : j∉jumpGates C := by intro e; exact jump (Finset.mem_filter.mp e).2
    simpa only [ite_eq_right jj, Nat.add_zero] using bound

/-- Total available rank budget on all selected scales, allowing every
possible cancellation and arbitrary sharing of previous signals. -/
theorem sum_charges_le (C : Circuit F n g) (v d : ℕ) (parents : Fin d → ℕ) :
    (∑ t : Cuts d parents, (chargesAt C (start v t) (half v t)).card) ≤
      g+d*(jumpGates C).card := by
  classical
  let test (t : Cuts d parents) (j : Fin g) := j∈chargesAt C (start v t) (half v t)
  have count (t : Cuts d parents) : (chargesAt C (start v t) (half v t)).card =
        ∑ j : Fin g, if test t j then 1 else 0 := by simp [test]
  rw [Finset.sum_congr rfl (fun t _ => count t), Finset.sum_comm]
  calc
    _ ≤ ∑ j : Fin g, (1 + if j∈jumpGates C then d else 0) := by
      apply Finset.sum_le_sum
      intro j _
      rw [Finset.sum_boole]
      exact gate_total C v d parents j
    _ = _ := by simp [Finset.sum_add_distrib, Nat.mul_comm]


/-- The concatenation of independent ordered coefficient records. `width` is
positive. The matrix includes interactions across all prefixes as zeros. -/
noncomputable def repeated (width records : ℕ) (pos : 0<width)
    (M : Matrix (Fin width) (Fin width) F) : Matrix (Fin (records*width)) (Fin (records*width)) F :=
  fun i j => if i.val/width = j.val/width then
      M ⟨i.val%width,Nat.mod_lt _ pos⟩ ⟨j.val%width,Nat.mod_lt _ pos⟩ else 0

private theorem repeated_order {width records : ℕ} {pos : 0<width}
    (M : Matrix (Fin width) (Fin width) F) (htri : M.IsUpperTriangular) (hdiag : ∀i, M i i≠0) :
    (repeated width records pos M).IsUpperTriangular ∧ ∀i, repeated width records pos M i i ≠ 0 := by
  constructor
  · intro i j hij
    dsimp only [repeated]
    split
    next eq =>
      apply htri
      change j.val%width < i.val%width
      have hI := Nat.mod_add_div i.val width
      have hJ := Nat.mod_add_div j.val width
      rw [eq] at hI
      change j.val < i.val at hij
      omega
    next => rfl
  · intro i; simpa only [repeated, ↓reduceIte] using hdiag ⟨i.val%width,Nat.mod_lt _ pos⟩

private theorem local_offsets {width h parents : ℕ} (pos : 0<width) (hP : 0<parents)
    (tiles : (2*h)*parents=width) (p t : ℕ) (ht : t<2*h) :
    (2*h*p+t)/width=p/parents ∧ (2*h*p+t)%width=2*h*(p%parents)+t := by
  have inside : 2*h*(p%parents)+t < width := calc
    _ < 2*h*(p%parents+1) := by rw [Nat.mul_succ]; omega
    _ ≤ 2*h*parents := Nat.mul_le_mul_left _ (Nat.mod_lt p hP)
    _ = width := tiles
  have loc : 2*h*p+t = (2*h*(p%parents)+t)+width*(p/parents) := calc
    _ = 2*h*(p%parents + parents*(p/parents))+t := by rw [Nat.mod_add_div]
    _ = _ := by rw [←tiles]; ring
  rw [loc, Nat.add_mul_div_left _ _ pos, Nat.div_eq_of_lt inside, Nat.zero_add,
    Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt inside]
  exact ⟨rfl,rfl⟩

private theorem repeated_cut {width records h parents : ℕ} (pos : 0<width) (hP : 0<parents)
    (tiles : (2*h)*parents=width) (p : Fin (records*parents)) (M : Matrix (Fin width) (Fin width) F) :
    let s := 2*h*p.val
    let t := 2*h*(p.val%parents)
    ∀ (bound : s+2*h ≤ records*width) (localBound : t+2*h ≤ width),
    (repeated width records pos M).submatrix (TraceRadixMatrix.atOffset (h:=h) s (by omega))
        (TraceRadixMatrix.atOffset (h:=h) (s+h) (by omega)) =
      M.submatrix (TraceRadixMatrix.atOffset (h:=h) t (by omega))
        (TraceRadixMatrix.atOffset (h:=h) (t+h) (by omega)) := by
  dsimp only
  intro bound localBound
  ext i j
  have hi := local_offsets pos hP tiles p.val i.val (by have := i.isLt; omega)
  have hj := local_offsets pos hP tiles p.val (h+j.val) (by have := j.isLt; omega)
  change (if (2*h*p.val+i.val)/width = (2*h*p.val+h+j.val)/width then
      M ⟨(2*h*p.val+i.val)%width,_⟩ ⟨(2*h*p.val+h+j.val)%width,_⟩ else 0) =
      M ⟨2*h*(p.val%parents)+i.val,_⟩ ⟨2*h*(p.val%parents)+h+j.val,_⟩
  have eq : (2*h*p.val+i.val)/width = (2*h*p.val+h+j.val)/width := by
    rw [hi.1, Nat.add_assoc, hj.1]
  rw [ite_eq_left eq]
  congr 1
  · exact Fin.ext hi.2
  · apply Fin.ext; simpa [Nat.add_assoc] using hj.2

private theorem change_start {n h s u : ℕ} (M : Matrix (Fin n) (Fin n) F) (eq : s=u)
    (bs : s+2*h≤n) (bu : u+2*h≤n) :
    (M.submatrix (TraceRadixMatrix.atOffset (h:=h) s (by omega)) (TraceRadixMatrix.atOffset (h:=h) (s+h) (by omega))).rank =
    (M.submatrix (TraceRadixMatrix.atOffset (h:=h) u (by omega)) (TraceRadixMatrix.atOffset (h:=h) (u+h) (by omega))).rank := by
  subst u; rfl

/-- The exact global gate budget on every linear record length appearing in
the trace construction. The direction chooses the true matrix inverse, and
all independent prefixes are presented to the same unrestricted XOR circuit. -/
theorem trace_circuit_budget [CharP F 2] (a d records g : ℕ) (ha : 2 ≤ a) (inverse : Bool) :
    let v := a*a*2
    let width := v*2^d
    let M := TraceRadixMatrix.digitBlock (CoefficientPrefix.traceBase (F:=F) a) v width 0 0
    let A := if inverse then M⁻¹ else M
    ∀ C : Circuit F (records*width) g,
      C.realizes (repeated width records (by dsimp [width,v]; positivity) A) →
      d*(records*(v-1)*2^(d-1)) ≤ g+d*(jumpGates C).card := by
  let v := a*a*2
  let width := v*2^d
  let M := TraceRadixMatrix.digitBlock (CoefficientPrefix.traceBase (F:=F) a) v width 0 0
  let A := if inverse then M⁻¹ else M
  have hv : 0<v := by dsimp [v]; positivity
  have hw : 0<width := by dsimp [width]; positivity
  let W := repeated width records hw A
  change ∀ C : Circuit F (records*width) g, C.realizes W → d*(records*(v-1)*2^(d-1)) ≤ g+d*(jumpGates C).card
  intro C computes
  have order := TraceRadixMatrix.trace_order (F:=F) a width ha inverse
  have wOrder : W.IsUpperTriangular ∧ ∀i, W i i≠0 := repeated_order A order.1 order.2
  let tileCount (i : Fin d) := 2^(d-1-i.val)
  let parents (i : Fin d) := records*tileCount i
  have tilePos (i : Fin d) : 0<tileCount i := by dsimp [tileCount]; positivity
  have tiles (i : Fin d) : (2*(v*2^i.val))*tileCount i=width := by
    dsimp [tileCount,width]
    calc
      _ = v*2^(i.val+1+(d-1-i.val)) := by rw [pow_add,pow_succ]; ring
      _ = _ := by congr 2; have := i.isLt; omega
  have node (t : Cuts d parents) : (v-1)*2^t.1.val ≤ (chargesAt C (start v t) (half v t)).card := by
    let h := half v t
    let u := t.2.val%tileCount t.1
    have cutfit : 2*h*t.2.val+2*h ≤ records*width := calc
      _ = 2*h*(t.2.val+1) := (Nat.mul_succ ..).symm
      _ ≤ 2*h*(records*tileCount t.1) := Nat.mul_le_mul_left _ t.2.isLt
      _ = records*width := by rw [←tiles t.1]; ring
    have localfit : 2*h*u+2*h ≤ width := calc
      _ = 2*h*(u+1) := (Nat.mul_succ ..).symm
      _ ≤ 2*h*(tileCount t.1) := Nat.mul_le_mul_left _ (Nat.mod_lt _ (tilePos t.1))
      _ = _ := tiles t.1
    have identical := repeated_cut hw (tilePos t.1) (tiles t.1) t.2 A cutfit localfit
    have positions : h*(2*u)=2*h*u := by ring
    have exactRanks := TraceRadixMatrix.trace_both_directions (F:=F) a t.1.val u width ha
      (by rw [show a*a*2*2^t.1.val = h from rfl, positions]; exact localfit)
    have localrank : (A.submatrix (TraceRadixMatrix.atOffset (h:=h) (2*h*u) (by omega))
        (TraceRadixMatrix.atOffset (h:=h) (2*h*u+h) (by omega))).rank = h-2^t.1.val := by
      have base : (A.submatrix (TraceRadixMatrix.atOffset (h:=h) (h*(2*u)) (by omega))
          (TraceRadixMatrix.atOffset (h:=h) (h*(2*u)+h) (by omega))).rank = h-2^t.1.val := by
        cases inverse <;> first | exact exactRanks.1 | exact exactRanks.2
      exact (change_start A positions (by omega) localfit).symm.trans base
    have full := interval_rank_le C W computes wOrder.1 wOrder.2 (start v t) (half v t) cutfit
    calc
      (v-1)*2^t.1.val = h-2^t.1.val := by rw [Nat.sub_mul,one_mul]
      _ = _ := localrank.symm
      _ = _ := (congrArg Matrix.rank identical).symm
      _ ≤ _ := full
  calc
    d*(records*(v-1)*2^(d-1)) = ∑ t : Cuts d parents, (v-1)*2^t.1.val := by
      rw [Fintype.sum_sigma]
      have level (i : Fin d) : (∑ _ : Fin (parents i), (v-1)*2^i.val) = records*(v-1)*2^(d-1) := by
        simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, Nat.nsmul_eq_mul]
        dsimp [parents,tileCount]
        calc
          _ = records*(v-1)*2^((d-1-i.val)+i.val) := by rw [pow_add]; ring
          _ = _ := by congr 2; have := i.isLt; omega
      simp only [level, Finset.sum_const, Finset.card_univ, Fintype.card_fin, Nat.nsmul_eq_mul]
    _ ≤ ∑ t : Cuts d parents, (chargesAt C (start v t) (half v t)).card := Finset.sum_le_sum (fun t _ => node t)
    _ ≤ g+d*(jumpGates C).card := sum_charges_le C v d parents

#print axioms trace_circuit_budget

#print axioms sum_charges_le

#print axioms interval_rank_le

end Moonshot.RadixCircuitCharges
