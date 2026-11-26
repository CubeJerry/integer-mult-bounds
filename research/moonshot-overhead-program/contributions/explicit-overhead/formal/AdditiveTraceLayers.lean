import Mathlib.Algebra.CharP.Two
import Mathlib.Algebra.Field.Basic

/-!
# Recursive additive evaluation in characteristic two

The cube index puts the highest coordinate first. Its false child precedes
its true child. Arrays are arbitrary functions on that cube, so no symmetry
condition or prearranged relation between the two halves is assumed.

The small law interface below is instantiated for every Mathlib field of
characteristic two. The results concern
source semantics. They include no representation or time assumptions.
-/

namespace Moonshot.AdditiveLayers

universe u

class BinaryField (K : Type u) where
  zero : K
  one : K
  add : K → K → K
  mul : K → K → K
  inv : K → K
  addAssoc : ∀ a b c, add (add a b) c = add a (add b c)
  addComm : ∀ a b, add a b = add b a
  addZero : ∀ a, add a zero = a
  addSelf : ∀ a, add a a = zero
  mulAssoc : ∀ a b c, mul (mul a b) c = mul a (mul b c)
  mulComm : ∀ a b, mul a b = mul b a
  mulAdd : ∀ a b c, mul a (add b c) = add (mul a b) (mul a c)
  addMul : ∀ a b c, mul (add a b) c = add (mul a c) (mul b c)
  mulZero : ∀ a, mul a zero = zero
  oneMul : ∀ a, mul one a = a
  invMul : ∀ a, a ≠ zero → mul (inv a) a = one

/-- Supply the operations from any Mathlib field of characteristic two. -/
instance (priority := low) mathlibBinaryField (K : Type u) [Field K] [CharP K 2] :
    BinaryField K where
  zero := 0
  one := 1
  add := (· + ·)
  mul := (· * ·)
  inv := Inv.inv
  addAssoc := add_assoc
  addComm := add_comm
  addZero := add_zero
  addSelf := CharTwo.add_self_eq_zero
  mulAssoc := mul_assoc
  mulComm := mul_comm
  mulAdd := mul_add
  addMul := add_mul
  mulZero := mul_zero
  oneMul := one_mul
  invMul := fun _ h => inv_mul_cancel₀ h

local infixl:65 " ⊞ " => BinaryField.add
local infixl:70 " ⊠ " => BinaryField.mul

variable {K : Type u} [BinaryField K]

private theorem zeroLeft (a : K) : BinaryField.zero ⊞ a = a := by
  rw [BinaryField.addComm, BinaryField.addZero]

private theorem cancelLeft (a b : K) : a ⊞ (a ⊞ b) = b := by
  rw [← BinaryField.addAssoc, BinaryField.addSelf, zeroLeft]

private theorem cancelRight (a b : K) : (a ⊞ b) ⊞ b = a := by
  rw [BinaryField.addAssoc, BinaryField.addSelf, BinaryField.addZero]

private theorem addFour (a b c d : K) :
    (a ⊞ b) ⊞ (c ⊞ d) = (a ⊞ c) ⊞ (b ⊞ d) := by
  calc
    (a ⊞ b) ⊞ (c ⊞ d) = a ⊞ ((b ⊞ c) ⊞ d) := by
      rw [BinaryField.addAssoc a b (c ⊞ d), BinaryField.addAssoc b c d]
    _ = a ⊞ ((c ⊞ b) ⊞ d) := by rw [BinaryField.addComm b c]
    _ = (a ⊞ c) ⊞ (b ⊞ d) := by
      rw [BinaryField.addAssoc c b d, BinaryField.addAssoc a c (b ⊞ d)]

private theorem mulSwap (a b c : K) : a ⊠ (b ⊠ c) = b ⊠ (a ⊠ c) := by
  rw [← BinaryField.mulAssoc, BinaryField.mulComm a b, BinaryField.mulAssoc]

private theorem squareSum (x y : K) :
    (x ⊞ y) ⊠ (x ⊞ y) = (x ⊠ x) ⊞ (y ⊠ y) := by
  rw [BinaryField.addMul, BinaryField.mulAdd x x y, BinaryField.mulAdd y x y,
    BinaryField.mulComm y x, BinaryField.addAssoc, cancelLeft]

private theorem axpySwap (a b c d s t : K) :
    (a ⊞ t ⊠ b) ⊞ s ⊠ (c ⊞ t ⊠ d) =
      (a ⊞ s ⊠ c) ⊞ t ⊠ (b ⊞ s ⊠ d) := by
  rw [BinaryField.mulAdd s c (t ⊠ d), BinaryField.mulAdd t b (s ⊠ d), mulSwap s t d]
  exact addFour _ _ _ _

private theorem invLeft {d : K} (hd : d ≠ BinaryField.zero) (x : K) :
    BinaryField.inv d ⊠ (d ⊠ x) = x := by
  rw [← BinaryField.mulAssoc, BinaryField.invMul d hd, BinaryField.oneMul]

private theorem invRight {d : K} (hd : d ≠ BinaryField.zero) (x : K) :
    d ⊠ (BinaryField.inv d ⊠ x) = x := by
  rw [mulSwap, invLeft hd]

/-- The recursive, monic subspace polynomial, evaluated at x. -/
def subspace (β : Nat → K) : Nat → K → K
  | 0, x => x
  | j+1, x =>
    let y := subspace β j x
    let d := subspace β j (β j)
    y ⊠ y ⊞ d ⊠ y

theorem subspace_add (β : Nat → K) (j : Nat) (x y : K) :
    subspace β j (x ⊞ y) = subspace β j x ⊞ subspace β j y := by
  induction j with
  | zero => rfl
  | succ j ih =>
    simp only [subspace]
    rw [ih, squareSum, BinaryField.mulAdd]
    exact addFour _ _ _ _

/-- Product of (x + sum bits_i β_i), by the two halves of the address cube. -/
def rootProduct (β : Nat → K) : Nat → K → K
  | 0, x => x
  | j+1, x => rootProduct β j x ⊠ rootProduct β j (x ⊞ β j)

theorem subspace_eq_rootProduct (β : Nat → K) (j : Nat) (x : K) :
    subspace β j x = rootProduct β j x := by
  induction j generalizing x with
  | zero => rfl
  | succ j ih =>
    simp only [rootProduct]
    rw [← ih x, ← ih (x ⊞ β j), subspace_add]
    simp only [subspace]
    rw [BinaryField.mulAdd, BinaryField.mulComm (subspace β j x) (subspace β j (β j))]

theorem subspace_vanishes (β : Nat → K) (j i : Nat) (hlt : i < j) :
    subspace β j (β i) = BinaryField.zero := by
  induction j with
  | zero => omega
  | succ j ih =>
    by_cases h : i = j
    · subst i
      exact BinaryField.addSelf _
    · have h' : i < j := by omega
      simp only [subspace, ih h', BinaryField.mulZero, BinaryField.addZero]

/-- Each new pair is (highest bit, remaining lower bits). -/
def Digits : Nat → Type
  | 0 => Unit
  | n+1 => Bool × Digits n

abbrev Row (K : Type u) (n : Nat) := Digits n → K

def lower {n : Nat} (p : Row K (n+1)) : Row K n := fun k => p (false, k)
def upper {n : Nat} (p : Row K (n+1)) : Row K n := fun k => p (true, k)
def join {n : Nat} (a b : Row K n) : Row K (n+1) :=
  fun k => if k.1 then b k.2 else a k.2

omit [BinaryField K] in
@[simp] theorem lower_join {n : Nat} (p q : Row K n) :
    lower (join p q) = p := rfl

omit [BinaryField K] in
@[simp] theorem upper_join {n : Nat} (p q : Row K n) :
    upper (join p q) = q := rfl

omit [BinaryField K] in
theorem join_parts {n : Nat} (p : Row K (n+1)) : join (lower p) (upper p) = p := by
  funext k
  rcases k with ⟨h, i⟩
  cases h <;> rfl


/-- The anchor plus the ordered sum of the selected directions. -/
def address (β : Nat → K) : (n : Nat) → K → Digits n → K
  | 0, a, _ => a
  | n+1, a, k =>
    if k.1 then address β n (a ⊞ β n) k.2 else address β n a k.2

theorem subspace_address (β : Nat → K) (m : Nat) :
    ∀ n, n ≤ m → ∀ (a : K) (k : Digits n),
      subspace β m (address β n a k) = subspace β m a := by
  intro n
  induction n with
  | zero => intro h a k; rfl
  | succ n ih =>
    intro h a k
    rcases k with ⟨bit, k⟩
    cases bit with
    | false => exact ih (by omega) a k
    | true =>
      change subspace β m (address β n (a ⊞ β n) k) = subspace β m a
      rw [ih (by omega) (a ⊞ β n) k, subspace_add,
        subspace_vanishes β m n (by omega), BinaryField.addZero]

def axpy {n : Nat} (p : Row K n) (t : K) (q : Row K n) : Row K n :=
  fun k => p k ⊞ t ⊠ q k

private theorem lower_axpy {n : Nat} (p q : Row K (n+1)) (t : K) :
    lower (axpy p t q) = axpy (lower p) t (lower q) := rfl

private theorem upper_axpy {n : Nat} (p q : Row K (n+1)) (t : K) :
    upper (axpy p t q) = axpy (upper p) t (upper q) := rfl

/-- The global polynomial in the ordered monic product basis, evaluated at x. -/
def polynomial (β : Nat → K) : (n : Nat) → Row K n → K → K
  | 0, p, _ => p ()
  | n+1, p, x =>
    polynomial β n (lower p) x ⊞ subspace β n x ⊠ polynomial β n (upper p) x

theorem polynomial_axpy (β : Nat → K) :
    ∀ n (p q : Row K n) (t x : K),
      polynomial β n (axpy p t q) x =
        polynomial β n p x ⊞ t ⊠ polynomial β n q x := by
  intro n
  induction n with
  | zero => intro p q t x; rfl
  | succ n ih =>
    intro p q t x
    simp only [polynomial, lower_axpy, upper_axpy, ih]
    exact axpySwap _ _ _ _ _ _

/-- Explicit basis weight at k, the product of the S_i whose bit is true. -/
def weight (β : Nat → K) (x : K) : (n : Nat) → Digits n → K
  | 0, _ => BinaryField.one
  | n+1, k =>
    if k.1 then subspace β n x ⊠ weight β x n k.2 else weight β x n k.2

def sumCube : (n : Nat) → Row K n → K
  | 0, f => f ()
  | n+1, f => sumCube n (lower f) ⊞ sumCube n (upper f)

private theorem sum_scale :
    ∀ n (t : K) (f : Row K n),
      sumCube n (fun k => t ⊠ f k) = t ⊠ sumCube n f := by
  intro n
  induction n with
  | zero => intro t f; rfl
  | succ n ih =>
    intro t f
    change sumCube n (fun k => t ⊠ lower f k) ⊞ sumCube n (fun k => t ⊠ upper f k) =
      t ⊠ (sumCube n (lower f) ⊞ sumCube n (upper f))
    rw [ih t (lower f), ih t (upper f), BinaryField.mulAdd]

theorem polynomial_eq_basisSum (β : Nat → K) :
    ∀ n (p : Row K n) (x : K), polynomial β n p x =
      sumCube n (fun k => weight β x n k ⊠ p k) := by
  intro n
  induction n with
  | zero =>
    intro p x
    exact (BinaryField.oneMul (p ())).symm
  | succ n ih =>
    intro p x
    change polynomial β n (lower p) x ⊞ subspace β n x ⊠ polynomial β n (upper p) x =
      sumCube n (fun k => weight β x n k ⊠ lower p k) ⊞
        sumCube n (fun k => (subspace β n x ⊠ weight β x n k) ⊠ upper p k)
    rw [ih (lower p) x, ih (upper p) x]
    simp only [BinaryField.mulAssoc]
    rw [sum_scale n (subspace β n x) (fun k => weight β x n k ⊠ upper p k)]

/-- Compute the two actual child coefficient arrays, then recurse. -/
def forward (β : Nat → K) : (n : Nat) → K → Row K n → Row K n
  | 0, _, p => p
  | n+1, a, p =>
    let t := subspace β n a
    let d := subspace β n (β n)
    let u := axpy (lower p) t (upper p)
    let v := axpy u d (upper p)
    join (forward β n a u) (forward β n (a ⊞ β n) v)

theorem forward_value (β : Nat → K) :
    ∀ n (a : K) (p : Row K n) (k : Digits n),
      forward β n a p k = polynomial β n p (address β n a k) := by
  intro n
  induction n with
  | zero =>
    intro a p k
    cases k
    rfl
  | succ n ih =>
    intro a p k
    rcases k with ⟨bit, k⟩
    cases bit with
    | false =>
      change forward β n a (axpy (lower p) (subspace β n a) (upper p)) k =
        polynomial β n (lower p) (address β n a k) ⊞
          subspace β n (address β n a k) ⊠ polynomial β n (upper p) (address β n a k)
      rw [ih, polynomial_axpy, subspace_address β n n (Nat.le_refl _) a k]
    | true =>
      let b := a ⊞ β n
      let t := subspace β n a
      let d := subspace β n (β n)
      change forward β n b (axpy (axpy (lower p) t (upper p)) d (upper p)) k =
        polynomial β n (lower p) (address β n b k) ⊞
          subspace β n (address β n b k) ⊠ polynomial β n (upper p) (address β n b k)
      rw [ih, polynomial_axpy, polynomial_axpy,
        subspace_address β n n (Nat.le_refl _) b k]
      change (_ ⊞ t ⊠ _) ⊞ d ⊠ _ = _ ⊞ subspace β n (a ⊞ β n) ⊠ _
      rw [subspace_add, BinaryField.addMul, BinaryField.addAssoc]

/-- Direct coefficient dot product with the product basis at the requested leaf. -/
theorem forward_is_evaluation (β : Nat → K) (n : Nat) (a : K)
    (p : Row K n) (k : Digits n) :
    forward β n a p k =
      sumCube n (fun h => weight β (address β n a k) n h ⊠ p h) := by
  rw [forward_value, polynomial_eq_basisSum]


/-- Recover the high coefficient half, using the actual nonzero gap at this stage. -/
def recoverHigh {n : Nat} (d : K) (u v : Row K n) : Row K n :=
  fun k => BinaryField.inv d ⊠ (u k ⊞ v k)

def recoverLow {n : Nat} (t d : K) (u v : Row K n) : Row K n :=
  axpy u t (recoverHigh d u v)

private theorem recover_forward_high {n : Nat} {d : K} (hd : d ≠ BinaryField.zero)
    (t : K) (p h : Row K n) :
    recoverHigh d (axpy p t h) (axpy (axpy p t h) d h) = h := by
  funext k
  change BinaryField.inv d ⊠ (axpy p t h k ⊞ (axpy p t h k ⊞ d ⊠ h k)) = h k
  rw [cancelLeft, invLeft hd]

private theorem recover_forward_low {n : Nat} {d : K} (hd : d ≠ BinaryField.zero)
    (t : K) (p h : Row K n) :
    recoverLow t d (axpy p t h) (axpy (axpy p t h) d h) = p := by
  unfold recoverLow
  rw [recover_forward_high hd t p h]
  funext k
  exact cancelRight _ _

private theorem recover_then_low {n : Nat} (t d : K) (u v : Row K n) :
    axpy (recoverLow t d u v) t (recoverHigh d u v) = u := by
  funext k
  exact cancelRight _ _

private theorem recover_then_high {n : Nat} {d : K} (hd : d ≠ BinaryField.zero)
    (u v : Row K n) : axpy u d (recoverHigh d u v) = v := by
  funext k
  change u k ⊞ d ⊠ (BinaryField.inv d ⊠ (u k ⊞ v k)) = v k
  rw [invRight hd, cancelLeft]

def inverse (β : Nat → K) : (n : Nat) → K → Row K n → Row K n
  | 0, _, y => y
  | n+1, a, y =>
    let t := subspace β n a
    let d := subspace β n (β n)
    let u := inverse β n a (lower y)
    let v := inverse β n (a ⊞ β n) (upper y)
    join (recoverLow t d u v) (recoverHigh d u v)

def NonzeroGaps (β : Nat → K) (n : Nat) : Prop :=
  ∀ j, j < n → subspace β j (β j) ≠ BinaryField.zero

private theorem gaps_prefix {β : Nat → K} {n : Nat} (h : NonzeroGaps β (n+1)) :
    NonzeroGaps β n := by
  intro j hj
  exact h j (by omega)

theorem inverse_forward (β : Nat → K) :
    ∀ n, NonzeroGaps β n → ∀ (a : K) (p : Row K n),
      inverse β n a (forward β n a p) = p := by
  intro n
  induction n with
  | zero => intro h a p; rfl
  | succ n ih =>
    intro h a p
    have hd := h n (Nat.lt_succ_self n)
    have hp := gaps_prefix h
    simp only [forward, inverse, lower_join, upper_join, ih hp,
      recover_forward_high hd, recover_forward_low hd, join_parts]

theorem forward_inverse (β : Nat → K) :
    ∀ n, NonzeroGaps β n → ∀ (a : K) (y : Row K n),
      forward β n a (inverse β n a y) = y := by
  intro n
  induction n with
  | zero => intro h a y; rfl
  | succ n ih =>
    intro h a y
    have hd := h n (Nat.lt_succ_self n)
    have hp := gaps_prefix h
    simp only [forward, inverse, lower_join, upper_join, recover_then_low,
      recover_then_high hd, ih hp, join_parts]

/- An actual four-element field and two independent directions. -/
namespace Example

inductive Four | zero | one | generator | generatorPlusOne deriving DecidableEq

private def plus : Four → Four → Four
  | .zero, y => y
  | x, .zero => x
  | .one, .one | .generator, .generator | .generatorPlusOne, .generatorPlusOne => .zero
  | .one, .generator | .generator, .one => .generatorPlusOne
  | .one, .generatorPlusOne | .generatorPlusOne, .one => .generator
  | .generator, .generatorPlusOne | .generatorPlusOne, .generator => .one

private def times : Four → Four → Four
  | .zero, _ | _, .zero => .zero
  | .one, y | y, .one => y
  | .generator, .generator => .generatorPlusOne
  | .generatorPlusOne, .generatorPlusOne => .generator
  | .generator, .generatorPlusOne | .generatorPlusOne, .generator => .one

private def reciprocal : Four → Four
  | .zero => .zero
  | .one => .one
  | .generator => .generatorPlusOne
  | .generatorPlusOne => .generator

instance : BinaryField Four where
  zero := .zero
  one := .one
  add := plus
  mul := times
  inv := reciprocal
  addAssoc := by intro a b c; cases a <;> cases b <;> cases c <;> rfl
  addComm := by intro a b; cases a <;> cases b <;> rfl
  addZero := by intro a; cases a <;> rfl
  addSelf := by intro a; cases a <;> rfl
  mulAssoc := by intro a b c; cases a <;> cases b <;> cases c <;> rfl
  mulComm := by intro a b; cases a <;> cases b <;> rfl
  mulAdd := by intro a b c; cases a <;> cases b <;> cases c <;> rfl
  addMul := by intro a b c; cases a <;> cases b <;> cases c <;> rfl
  mulZero := by intro a; cases a <;> rfl
  oneMul := by intro a; cases a <;> rfl
  invMul := by
    intro a h
    cases a <;> first | rfl | exact (h rfl).elim

def directions : Nat → Four
  | 0 => .one
  | 1 => .generator
  | _ => .zero

theorem directions_valid : NonzeroGaps directions 2 := by
  intro i hi
  have h : i = 0 ∨ i = 1 := by omega
  rcases h with rfl | rfl <;> decide

theorem field_four_roundtrip (a : Four) (p : Row Four 2) :
    inverse directions 2 a (forward directions 2 a p) = p :=
  inverse_forward directions 2 directions_valid a p

end Example

section MathlibField

variable {F : Type u} [Field F] [CharP F 2]

/-- The initial point translates the entire ordered binary address list. -/
theorem translate_address (β : ℕ → F) (n : ℕ) (x y : F) (k : Digits n) :
    address β n (x+y) k = x + address β n y k := by
  induction n generalizing x y with
  | zero => rfl
  | succ n ih =>
    rcases k with ⟨bit,k⟩
    cases bit with
    | false => exact ih x y k
    | true =>
      change address β n ((x+y)+β n) k = x + address β n (y+β n) k
      rw [add_assoc]
      exact ih x (y+β n) k

/-- In an actual characteristic-two field the roots are exactly the points
of the indicated binary span, including the depth-zero boundary. -/
theorem rootProduct_zero_iff_address (β : ℕ → F) (n : ℕ) (x : F) :
    rootProduct β n x = 0 ↔ ∃ k : Digits n, address β n x k = 0 := by
  induction n generalizing x with
  | zero =>
    constructor
    · exact fun h => ⟨(), h⟩
    · exact fun ⟨_,h⟩ => h
  | succ n ih =>
    change rootProduct β n x * rootProduct β n (x+β n) = 0 ↔ _
    rw [mul_eq_zero, ih, ih]
    constructor
    · rintro (⟨k,h⟩ | ⟨k,h⟩)
      · exact ⟨(false,k), h⟩
      · exact ⟨(true,k), h⟩
    · rintro ⟨⟨bit,k⟩,h⟩
      cases bit with
      | false => exact Or.inl ⟨k,h⟩
      | true => exact Or.inr ⟨k,h⟩

/-- No direction is a binary subset sum of the earlier directions. -/
def independentDirections (β : ℕ → F) (n : ℕ) :=
  ∀ j < n, ∀ k : Digits j, address β j (0 : F) k ≠ β j

theorem gaps_of_independent {β : ℕ → F} {n : ℕ}
    (h : independentDirections β n) : NonzeroGaps β n := by
  intro j hj bad
  rw [subspace_eq_rootProduct] at bad
  obtain ⟨k,hz⟩ := (rootProduct_zero_iff_address β j (β j)).mp bad
  apply h j hj k
  have trans : address β j (β j) k = β j + address β j 0 k := by
    simpa only [add_zero] using translate_address β j (β j) 0 k
  rw [trans] at hz
  have he := congrArg (fun t : F => β j + t) hz
  simpa only [← add_assoc, CharTwo.add_self_eq_zero, zero_add, add_zero] using he

/-- The actual recursive interpolation/evaluation maps are inverse for every
independent ordered binary prefix in any Mathlib field of characteristic two. -/
theorem independent_field_equivalence {β : ℕ → F} {n : ℕ}
    (h : independentDirections β n) (a : F) :
    Function.LeftInverse (inverse β n a) (forward β n a) ∧
    Function.RightInverse (inverse β n a) (forward β n a) :=
  ⟨inverse_forward β n (gaps_of_independent h) a,
   forward_inverse β n (gaps_of_independent h) a⟩

end MathlibField

#print axioms rootProduct_zero_iff_address
#print axioms gaps_of_independent
#print axioms independent_field_equivalence

#print axioms subspace_eq_rootProduct
#print axioms forward_is_evaluation
#print axioms inverse_forward
#print axioms forward_inverse
#print axioms Example.field_four_roundtrip

end Moonshot.AdditiveLayers
