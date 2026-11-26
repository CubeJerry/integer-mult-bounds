import Mathlib.Algebra.Group.Equiv.Basic
import Mathlib.SetTheory.Cardinal.Finite
import Mathlib.Data.Fintype.BigOperators

/-!
# Binary trace decomposition for the representative layout

In a field of degree 3c, take S to be the c-th Frobenius power. The
fixed field and the kernel of the relative trace split the additive
group, including when c is even. The two-mark lemma checks the full-degree
direction in coordinates of a normal basis for all positive c.
-/
namespace Moonshot.TraceBundles
variable {G : Type*} [AddCommGroup G]

def tr (S : G ≃+ G) (x : G) := x + S x + S (S x)

theorem tr_add (S : G ≃+ G) (x y : G) : tr S (x + y) = tr S x + tr S y := by
  simp only [tr, map_add]
  ac_rfl

theorem tr_fixed (S : G ≃+ G) (cycle : ∀ x, S (S (S x)) = x) (x : G) :
    S (tr S x) = tr S x := by
  simp only [tr, map_add, cycle]
  ac_rfl

theorem tr_of_fixed (S : G ≃+ G) (charTwo : ∀ x : G, x + x = 0)
    {x : G} (fixed : S x = x) : tr S x = x := by
  simp [tr, fixed, charTwo]

/-- On a cyclic extension of relative degree three, every trace-zero vector
is a sum of a vector and its conjugate, with the explicit witness S x. -/
theorem kernel_iff_pair_image (S : G ≃+ G) (charTwo : ∀ x : G, x + x = 0)
    (cycle : ∀ x, S (S (S x)) = x) (x : G) :
    tr S x = 0 ↔ ∃ y, x = y + S y := by
  constructor
  · intro h
    refine ⟨S x, ?_⟩
    calc
      x = x + tr S x := by rw [h, add_zero]
      _ = (x + x) + (S x + S (S x)) := by simp only [tr, add_assoc]
      _ = _ := by rw [charTwo, zero_add]
  · rintro ⟨y, rfl⟩
    simp only [tr, map_add, cycle]
    calc
      _ = (y + y) + (S y + S y) + (S (S y) + S (S y)) := by ac_rfl
      _ = _ := by simp only [charTwo]

/-- Every vector has a unique decomposition into its trace-zero and fixed parts. -/
theorem unique_trace_split (S : G ≃+ G) (charTwo : ∀ x : G, x + x = 0)
    (cycle : ∀ x, S (S (S x)) = x) (x : G) :
    ∃! p : G × G, tr S p.1 = 0 ∧ S p.2 = p.2 ∧ p.1 + p.2 = x := by
  let t := tr S x
  have ht : S t = t := tr_fixed S cycle x
  have htt : tr S t = t := tr_of_fixed S charTwo ht
  refine ⟨(x + t, t), ⟨?_, ht, ?_⟩, ?_⟩
  · change tr S (x + t) = 0
    rw [tr_add, htt]
    exact charTwo t
  · change (x + t) + t = x
    rw [add_assoc, charTwo, add_zero]
  · rintro ⟨u,v⟩ ⟨hu,hv,hx⟩
    change tr S u = 0 at hu
    change S v = v at hv
    change u + v = x at hx
    have ht' : t = v := by
      change tr S x = v
      rw [← hx, tr_add, hu, tr_of_fixed S charTwo hv, zero_add]
    apply Prod.ext
    · change u = x + t
      rw [← hx, ht', add_assoc, charTwo, add_zero]
    · exact ht'.symm

/-- The nonzero normal-coordinate positions of α + F^c α. -/
def twoMarks (c k : ℕ) : Prop := k = 0 ∨ k = c

/-- A rotation preserving this support in 3c cyclic positions is the identity. -/
theorem full_period_direction {c i : ℕ} (hc : 0 < c) (hi : i < 3*c)
    (stable : ∀ k < 3*c, twoMarks c k → twoMarks c ((k+i) % (3*c))) : i = 0 := by
  have atZero := stable 0 (by omega) (Or.inl rfl)
  simp only [Nat.zero_add, Nat.mod_eq_of_lt hi, twoMarks] at atZero
  rcases atZero with hz | he
  · exact hz
  · subst i
    have atC := stable c (by omega) (Or.inr rfl)
    rw [Nat.mod_eq_of_lt (by omega : c+c < 3*c)] at atC
    unfold twoMarks at atC
    omega

/-- Bits on g+1 cycles of a common length, canonical modulo a single
global complement. The origin of cycle zero is fixed to false. -/
def cyclicFlip (s x : Bool) : Bool := if s then !x else x

def walk (s x : Bool) : ℕ → Bool
  | 0 => x
  | n+1 => cyclicFlip s (walk s x n)

def CanonicalCycles (g length : ℕ) (s : Bool) :=
  {f : Fin (g+1) → ℕ → Bool //
    (∀ j n, f j (n+1) = cyclicFlip s (f j n)) ∧
    (∀ j, f j length = f j 0) ∧ f 0 0 = false}

private theorem recover_cycle {g l : ℕ} {s : Bool} (p : CanonicalCycles g l s)
    (j : Fin (g+1)) (n : ℕ) :
    p.val j n = walk s (p.val j 0) n := by
  induction n with
  | zero => rfl
  | succ n ih => rw [p.property.1, ih]; rfl

private theorem walk_no_flip (x : Bool) (n : ℕ) : walk false x n = x := by
  induction n with
  | zero => rfl
  | succ n ih => simpa only [walk, cyclicFlip, Bool.false_eq_true, ite_false] using ih

private theorem walk_even (x : Bool) (n : ℕ) : walk true x (2*n) = x := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [Nat.mul_succ, walk, cyclicFlip] using ih

private theorem walk_odd (x : Bool) (n : ℕ) : walk true x (2*n+1) = !x := by
  simp [walk, cyclicFlip, walk_even]

/-- For a consistent sign, choose one unrestricted bit on each cycle except
the anchored cycle. This equivalence counts the fixed quotient classes. -/
def initialized_cycles (g l : ℕ) (s : Bool) (close : ∀ x, walk s x l = x) :
    CanonicalCycles g l s ≃ (Fin g → Bool) where
  toFun p j := p.val j.succ 0
  invFun a := ⟨fun j n => walk s (Fin.cases false a j) n,
    fun _ _ => rfl, fun _ => close _, rfl⟩
  left_inv p := by
    apply Subtype.ext
    funext j n
    change walk s (Fin.cases false (fun k => p.val k.succ 0) j) n = p.val j n
    have seed : Fin.cases false (fun k => p.val k.succ 0) j = p.val j 0 := by
      refine Fin.cases ?_ (fun k => ?_) j
      · exact p.property.2.2.symm
      · rfl
    rw [seed, recover_cycle p j n]
  right_inv _ := rfl

theorem no_flip_count (g l : ℕ) : Nat.card (CanonicalCycles g l false) = 2^g := by
  rw [Nat.card_congr (initialized_cycles g l false (fun x => walk_no_flip x l))]
  simp

theorem even_flip_count (g k : ℕ) : Nat.card (CanonicalCycles g (2*k) true) = 2^g := by
  rw [Nat.card_congr (initialized_cycles g (2*k) true (fun x => walk_even x k))]
  simp

theorem empty_odd_flip (g k : ℕ) : IsEmpty (CanonicalCycles g (2*k+1) true) := by
  constructor
  intro p
  have h := p.property.2.1 0
  rw [recover_cycle p 0 (2*k+1), walk_odd, p.property.2.2] at h
  contradiction

/-- The two sign classes cannot describe the same cyclic word. -/
theorem disjoint_signs (g l : ℕ) (p : CanonicalCycles g l false)
    (q : CanonicalCycles g l true) : p.val ≠ q.val := by
  intro e
  have hp := p.property.1 0 0
  have hq := q.property.1 0 0
  rw [e] at hp
  rw [q.property.2.2] at hp hq
  simp [cyclicFlip] at hp hq
  exact Bool.false_ne_true (hp.symm.trans hq)

#print axioms no_flip_count
#print axioms even_flip_count
#print axioms empty_odd_flip
#print axioms disjoint_signs

#print axioms kernel_iff_pair_image
#print axioms unique_trace_split
#print axioms full_period_direction
end Moonshot.TraceBundles
