import Std

/-!
# Copied carry formulas: truth, syntactic degree, size and polynomial budget

The syntax is a tree, so repeated inputs are really copied. The previous
carry occurs once in xy + (x+y)c. This file proves that fact quantitatively,
then proves the 2^(4r+k) bound for the exact repeated-prefix size majorant.
It does not formalize the cyclic factorization or a tape implementation.
-/

namespace MoonshotS005

inductive BitFormula
  | constant (b : Bool)
  | variable (index : Nat)
  | add (left right : BitFormula)
  | mul (left right : BitFormula)

namespace BitFormula

def size : BitFormula → Nat
  | .constant _ => 1
  | .variable _ => 1
  | .add x y => 1 + x.size + y.size
  | .mul x y => 1 + x.size + y.size

def degree : BitFormula → Nat
  | .constant _ => 0
  | .variable _ => 1
  | .add x y => max x.degree y.degree
  | .mul x y => x.degree + y.degree

def eval (env : Nat → Bool) : BitFormula → Bool
  | .constant b => b
  | .variable i => env i
  | .add x y => Bool.xor (x.eval env) (y.eval env)
  | .mul x y => (x.eval env) && (y.eval env)

def carry (x y c : BitFormula) : BitFormula :=
  .add (.mul x y) (.mul (.add x y) c)

def sumBit (x y c : BitFormula) : BitFormula :=
  .add (.add x y) c

theorem carry_size (x y c : BitFormula) :
    (carry x y c).size = 2 * x.size + 2 * y.size + c.size + 4 := by
  simp only [carry, size]
  omega

theorem sumBit_size (x y c : BitFormula) :
    (sumBit x y c).size = x.size + y.size + c.size + 2 := by
  simp only [sumBit, size]
  omega

/-- Exactly the ordinary sum bit and carry at Boolean valuations. -/
theorem adder_truth (env : Nat → Bool) (x y c : BitFormula) :
    2 * ((carry x y c).eval env).toNat +
      ((sumBit x y c).eval env).toNat =
    (x.eval env).toNat + (y.eval env).toNat + (c.eval env).toNat := by
  cases hx : x.eval env <;> cases hy : y.eval env <;> cases hc : c.eval env <;>
    simp [carry, sumBit, eval, hx, hy, hc]

theorem carry_degree {x y c : BitFormula} {B : Nat}
    (hx : x.degree ≤ B) (hy : y.degree ≤ B) (hc : c.degree ≤ B) :
    (carry x y c).degree ≤ 2 * B := by
  have hxy : max x.degree y.degree ≤ B := Nat.max_le.mpr ⟨hx, hy⟩
  simp only [carry, degree]
  omega

theorem sumBit_degree {x y c : BitFormula} {B : Nat}
    (hx : x.degree ≤ B) (hy : y.degree ≤ B) (hc : c.degree ≤ B) :
    (sumBit x y c).degree ≤ B := by
  simp only [sumBit, degree]
  exact Nat.max_le.mpr ⟨Nat.max_le.mpr ⟨hx, hy⟩, hc⟩

def carryChain (x y : Nat → BitFormula) : Nat → BitFormula
  | 0 => .constant false
  | i + 1 => carry (x i) (y i) (carryChain x y i)

theorem carryChain_degree (x y : Nat → BitFormula)
    (hx : ∀ i, (x i).degree ≤ 2 ^ i)
    (hy : ∀ i, (y i).degree ≤ 2 ^ i) (i : Nat) :
    (carryChain x y i).degree ≤ 2 ^ i := by
  induction i with
  | zero => simp [carryChain, degree]
  | succ i ih =>
      have h := carry_degree (hx i) (hy i) ih
      simpa [carryChain, Nat.pow_succ, Nat.mul_comm] using h

def prefixLess (f : Nat → Nat) : Nat → Nat
  | 0 => 0
  | k + 1 => prefixLess f k + f k

def prefixSum (f : Nat → Nat) (k : Nat) : Nat :=
  prefixLess f k + f k

/-- The carry tree has one copy of its previous carry, rather than a duplicated
expansion; all occurrences of the input formulas are counted. -/
theorem carryChain_size (x y : Nat → BitFormula) (S : Nat → Nat)
    (hx : ∀ i, (x i).size ≤ S i)
    (hy : ∀ i, (y i).size ≤ S i)
    (hpos : ∀ i, 1 ≤ S i) (i : Nat) :
    (carryChain x y i).size ≤ 1 + 8 * prefixLess S i := by
  induction i with
  | zero => simp [carryChain, size, prefixLess]
  | succ i ih =>
      simp only [carryChain, carry_size, prefixLess]
      have hxi := hx i
      have hyi := hy i
      have hpi := hpos i
      omega

/-- One balanced-adder output bit has the precise prefix-size bound used by
the characteristic-two count-formula construction. -/
theorem output_size (x y : Nat → BitFormula) (S : Nat → Nat)
    (hx : ∀ i, (x i).size ≤ S i)
    (hy : ∀ i, (y i).size ≤ S i)
    (hpos : ∀ i, 1 ≤ S i) (k : Nat) :
    (sumBit (x k) (y k) (carryChain x y k)).size ≤
      8 * prefixSum S k := by
  have hc := carryChain_size x y S hx hy hpos k
  have hxi := hx k
  have hyi := hy k
  have hpi := hpos k
  simp only [sumBit_size, prefixSum]
  omega

theorem output_degree (x y : Nat → BitFormula)
    (hx : ∀ i, (x i).degree ≤ 2 ^ i)
    (hy : ∀ i, (y i).degree ≤ 2 ^ i) (k : Nat) :
    (sumBit (x k) (y k) (carryChain x y k)).degree ≤ 2 ^ k :=
  sumBit_degree (hx k) (hy k) (carryChain_degree x y hx hy k)

/-- A direct geometric prefix estimate; no coarse maximum over bit positions. -/
theorem prefixSum_pow_bound (f : Nat → Nat) (B : Nat)
    (hf : ∀ i, f i ≤ 2 ^ (B + i)) (k : Nat) :
    prefixSum f k ≤ 2 ^ (B + k + 1) := by
  induction k with
  | zero =>
      simp only [prefixSum, prefixLess, Nat.zero_add, Nat.add_zero]
      exact Nat.le_trans (by simpa using hf 0)
        (Nat.pow_le_pow_right (by decide : 0 < 2) (by omega))
  | succ k ih =>
      change prefixSum f k + f (k + 1) ≤ 2 ^ (B + (k + 1) + 1)
      have ht : f (k + 1) ≤ 2 ^ (B + k + 1) := by
        simpa [Nat.add_assoc] using hf (k + 1)
      calc
        prefixSum f k + f (k + 1) ≤
            2 ^ (B + k + 1) + 2 ^ (B + k + 1) := Nat.add_le_add ih ht
        _ = 2 ^ (B + (k + 1) + 1) := by
          rw [show B + (k + 1) + 1 = (B + k + 1) + 1 by omega]
          simp [Nat.pow_succ, Nat.mul_two]

def copiedSizeProfile : Nat → Nat → Nat
  | 0, _ => 1
  | r + 1, k => 8 * prefixSum (copiedSizeProfile r) k

/-- Fully copied balanced-addition formula sizes admit a polynomial envelope:
for k≤r this is at most 2^(5r), a fifth power of the padded leaf count. -/
theorem copiedSizeProfile_bound (r k : Nat) :
    copiedSizeProfile r k ≤ 2 ^ (4 * r + k) := by
  induction r generalizing k with
  | zero =>
      simp only [copiedSizeProfile, Nat.mul_zero, Nat.zero_add]
      simpa using Nat.pow_le_pow_left (by decide : 1 ≤ 2) k
  | succ r ih =>
      have hp := prefixSum_pow_bound (copiedSizeProfile r) (4 * r) ih k
      calc
        copiedSizeProfile (r + 1) k =
            8 * prefixSum (copiedSizeProfile r) k := rfl
        _ ≤ 8 * 2 ^ (4 * r + k + 1) := Nat.mul_le_mul_left 8 hp
        _ = 2 ^ (4 * (r + 1) + k) := by
          rw [show 4 * (r + 1) + k = 3 + (4 * r + k + 1) by omega]
          simp [Nat.pow_add, Nat.mul_assoc]

theorem copiedSizeProfile_fifth_power (r k : Nat) (hk : k ≤ r) :
    copiedSizeProfile r k ≤ (2 ^ r) ^ 5 := by
  have hle : 4 * r + k ≤ r * 5 := by omega
  calc
    copiedSizeProfile r k ≤ 2 ^ (4 * r + k) := copiedSizeProfile_bound r k
    _ ≤ 2 ^ (r * 5) := Nat.pow_le_pow_right (by decide : 0 < 2) hle
    _ = (2 ^ r) ^ 5 := Nat.pow_mul 2 r 5

theorem copiedSizeProfile_positive (r k : Nat) :
    1 ≤ copiedSizeProfile r k := by
  induction r generalizing k with
  | zero => simp [copiedSizeProfile]
  | succ r ih =>
      have hp := ih k
      simp only [copiedSizeProfile, prefixSum]
      omega

/-- A literal balanced tree of ripple-carry formulas, indexed by its block
number. Recursive children are copied into each syntactic occurrence. -/
def balancedCount (input : Nat → Nat → BitFormula) : Nat → Nat → Nat → BitFormula
  | 0, block, k => input block k
  | r + 1, block, k =>
      let left := balancedCount input r (2 * block)
      let right := balancedCount input r (2 * block + 1)
      sumBit (left k) (right k) (carryChain left right k)

theorem balancedCount_size (input : Nat → Nat → BitFormula)
    (leafSize : ∀ block k, (input block k).size ≤ 1)
    (r block k : Nat) :
    (balancedCount input r block k).size ≤ copiedSizeProfile r k := by
  induction r generalizing block k with
  | zero => exact leafSize block k
  | succ r ih =>
      exact output_size
        (balancedCount input r (2 * block))
        (balancedCount input r (2 * block + 1))
        (copiedSizeProfile r)
        (ih (2 * block)) (ih (2 * block + 1))
        (copiedSizeProfile_positive r) k

theorem balancedCount_degree (input : Nat → Nat → BitFormula)
    (leafDegree : ∀ block k, (input block k).degree ≤ 2 ^ k)
    (r block k : Nat) :
    (balancedCount input r block k).degree ≤ 2 ^ k := by
  induction r generalizing block k with
  | zero => exact leafDegree block k
  | succ r ih =>
      exact output_degree
        (balancedCount input r (2 * block))
        (balancedCount input r (2 * block + 1))
        (ih (2 * block)) (ih (2 * block + 1)) k

theorem balancedCount_polynomial_size (input : Nat → Nat → BitFormula)
    (leafSize : ∀ block k, (input block k).size ≤ 1)
    (r block k : Nat) (hk : k ≤ r) :
    (balancedCount input r block k).size ≤ (2 ^ r) ^ 5 :=
  Nat.le_trans (balancedCount_size input leafSize r block k)
    (copiedSizeProfile_fifth_power r k hk)

#print axioms adder_truth
#print axioms carry_size
#print axioms carryChain_degree
#print axioms output_size
#print axioms output_degree
#print axioms copiedSizeProfile_bound
#print axioms copiedSizeProfile_fifth_power
#print axioms balancedCount_size
#print axioms balancedCount_degree
#print axioms balancedCount_polynomial_size

end BitFormula
end MoonshotS005
