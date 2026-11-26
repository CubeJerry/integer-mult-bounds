import CopiedCountFormula

/-!
# Whole-word semantics for the copied balanced count formula

This file imports the unchanged first-wave syntax/size/degree proof.
All values below are ordinary natural-number binary words, rather than
characteristic-two sums. Leaves contain a single Boolean at bit zero,
and false in every higher position.
-/

namespace MoonshotS005.BitFormula

def wordValue (env : Nat → Bool) (bits : Nat → BitFormula) : Nat → Nat
  | 0 => 0
  | n + 1 => wordValue env bits n + 2 ^ n * ((bits n).eval env).toNat

theorem wordValue_lt (env : Nat → Bool) (bits : Nat → BitFormula) (n : Nat) :
    wordValue env bits n < 2 ^ n := by
  induction n with
  | zero => simp [wordValue]
  | succ n ih =>
      have hb : ((bits n).eval env).toNat ≤ 1 := by
        cases (bits n).eval env <;> decide
      have hm := Nat.mul_le_mul_left (2 ^ n) hb
      simp only [wordValue, Nat.pow_succ, Nat.mul_one] at *
      omega

def rippleOutput (x y : Nat → BitFormula) (i : Nat) : BitFormula :=
  sumBit (x i) (y i) (carryChain x y i)

/-- Exact natural-number addition with the final outgoing carry retained. -/
theorem ripple_value (env : Nat → Bool) (x y : Nat → BitFormula) (n : Nat) :
    wordValue env (rippleOutput x y) n +
      2 ^ n * ((carryChain x y n).eval env).toNat =
    wordValue env x n + wordValue env y n := by
  induction n with
  | zero => simp [wordValue, carryChain, eval]
  | succ n ih =>
      have hlocal := adder_truth env (x n) (y n) (carryChain x y n)
      have hweighted := congrArg (fun z : Nat => 2 ^ n * z) hlocal
      simp only [Nat.mul_add] at hweighted
      simp only [wordValue, rippleOutput, carryChain, Nat.pow_succ, Nat.mul_assoc]
      omega

/-- Discarding the outgoing carry gives precisely addition modulo 2^n. -/
theorem ripple_value_mod (env : Nat → Bool) (x y : Nat → BitFormula) (n : Nat) :
    wordValue env (rippleOutput x y) n =
      (wordValue env x n + wordValue env y n) % (2 ^ n) := by
  have h := congrArg (fun z : Nat => z % (2 ^ n)) (ripple_value env x y n)
  simpa only [Nat.add_mul_mod_self_left,
    Nat.mod_eq_of_lt (wordValue_lt env (rippleOutput x y) n)] using h

/-- Actual count leaves: one independent Boolean variable and no higher bits. -/
def booleanLeaves : Nat → Nat → BitFormula
  | block, 0 => .variable block
  | _, _ + 1 => .constant false

theorem booleanLeaves_value (env : Nat → Bool) (block n : Nat) :
    wordValue env (booleanLeaves block) (n + 1) = (env block).toNat := by
  induction n with
  | zero => simp [wordValue, booleanLeaves, eval]
  | succ n ih =>
      simpa only [wordValue, booleanLeaves, eval, Bool.toNat_false,
        Nat.mul_zero, Nat.add_zero] using ih

def leafTotal (env : Nat → Bool) : Nat → Nat → Nat
  | 0, block => (env block).toNat
  | r + 1, block => leafTotal env r (2 * block) + leafTotal env r (2 * block + 1)

theorem leafTotal_le (env : Nat → Bool) (r block : Nat) :
    leafTotal env r block ≤ 2 ^ r := by
  induction r generalizing block with
  | zero =>
      simp only [leafTotal, Nat.pow_zero]
      cases env block <;> decide
  | succ r ih =>
      have hl := ih (2 * block)
      have hr := ih (2 * block + 1)
      simp only [leafTotal, Nat.pow_succ]
      omega

/-- Every finite output prefix is the exact count modulo its binary word size. -/
theorem balancedCount_value_mod (env : Nat → Bool) (r block n : Nat) (hn : 0 < n) :
    wordValue env (balancedCount booleanLeaves r block) n =
      leafTotal env r block % (2 ^ n) := by
  induction r generalizing block with
  | zero =>
      cases n with
      | zero => omega
      | succ n =>
          change wordValue env (booleanLeaves block) (n + 1) =
            (env block).toNat % (2 ^ (n + 1))
          have hlt := wordValue_lt env (booleanLeaves block) (n + 1)
          rw [booleanLeaves_value] at hlt
          rw [booleanLeaves_value, Nat.mod_eq_of_lt hlt]
  | succ r ih =>
      change wordValue env
        (rippleOutput (balancedCount booleanLeaves r (2 * block))
          (balancedCount booleanLeaves r (2 * block + 1))) n =
        (leafTotal env r (2 * block) + leafTotal env r (2 * block + 1)) % (2 ^ n)
      rw [ripple_value_mod, ih (2 * block), ih (2 * block + 1)]
      exact (Nat.add_mod _ _ _).symm

/-- r+1 output bits suffice for the exact total of 2^r Boolean leaves. -/
theorem balancedCount_value (env : Nat → Bool) (r block : Nat) :
    wordValue env (balancedCount booleanLeaves r block) (r + 1) =
      leafTotal env r block := by
  rw [balancedCount_value_mod env r block (r + 1) (by omega)]
  apply Nat.mod_eq_of_lt
  have hb := leafTotal_le env r block
  have hp : 0 < 2 ^ r := Nat.two_pow_pos r
  simp only [Nat.pow_succ]
  omega

/-- The ordinary number of true variables in a contiguous finite input range. -/
def countRange (env : Nat → Bool) (start : Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => countRange env start n + (env (start + n)).toNat

theorem countRange_add (env : Nat → Bool) (start u v : Nat) :
    countRange env start (u + v) =
      countRange env start u + countRange env (start + u) v := by
  induction v with
  | zero => simp [countRange]
  | succ v ih => simp [countRange, ih, Nat.add_assoc]

theorem leafTotal_eq_countRange (env : Nat → Bool) (r block : Nat) :
    leafTotal env r block = countRange env (2 ^ r * block) (2 ^ r) := by
  induction r generalizing block with
  | zero => simp [leafTotal, countRange]
  | succ r ih =>
      have hs : 2 ^ r * (2 * block) = 2 ^ (r + 1) * block := by
        simp [Nat.pow_succ, Nat.mul_assoc]
      have ht : 2 ^ r * (2 * block + 1) = 2 ^ (r + 1) * block + 2 ^ r := by
        rw [Nat.mul_add, hs, Nat.mul_one]
      calc
        leafTotal env (r + 1) block =
            countRange env (2 ^ (r + 1) * block) (2 ^ r) +
              countRange env (2 ^ (r + 1) * block + 2 ^ r) (2 ^ r) := by
          rw [leafTotal, ih, ih, hs, ht]
        _ = countRange env (2 ^ (r + 1) * block) (2 ^ r + 2 ^ r) :=
          (countRange_add env _ _ _).symm
        _ = countRange env (2 ^ (r + 1) * block) (2 ^ (r + 1)) := by
          rw [Nat.pow_succ, Nat.mul_two]

/-- Exact whole-word semantics with the literal contiguous Boolean inputs. -/
theorem balancedCount_exact_count (env : Nat → Bool) (r block : Nat) :
    wordValue env (balancedCount booleanLeaves r block) (r + 1) =
      countRange env (2 ^ r * block) (2 ^ r) := by
  rw [balancedCount_value, leafTotal_eq_countRange]

theorem booleanLeaves_size (block k : Nat) : (booleanLeaves block k).size ≤ 1 := by
  cases k <;> simp [booleanLeaves, size]

theorem booleanLeaves_degree (block k : Nat) :
    (booleanLeaves block k).degree ≤ 2 ^ k := by
  cases k <;> simp [booleanLeaves, degree]

/-- The same actual formula has exact count semantics and the inherited
polynomial copied-tree size and per-bit syntactic degree bounds. -/
theorem balancedCount_complete_spec (env : Nat → Bool) (r block : Nat) :
    wordValue env (balancedCount booleanLeaves r block) (r + 1) =
        countRange env (2 ^ r * block) (2 ^ r) ∧
      ∀ k, k ≤ r →
        (balancedCount booleanLeaves r block k).size ≤ (2 ^ r) ^ 5 ∧
        (balancedCount booleanLeaves r block k).degree ≤ 2 ^ k := by
  constructor
  · exact balancedCount_exact_count env r block
  · intro k hk
    exact ⟨balancedCount_polynomial_size booleanLeaves booleanLeaves_size r block k hk,
      balancedCount_degree booleanLeaves booleanLeaves_degree r block k⟩

/-- Zero padding changes the environment only beyond the actual leaf count. -/
def paddedEnv (env : Nat → Bool) (m i : Nat) : Bool :=
  if i < m then env i else false

theorem countRange_padded_prefix (env : Nat → Bool) (m n : Nat) (hn : n ≤ m) :
    countRange (paddedEnv env m) 0 n = countRange env 0 n := by
  induction n generalizing m with
  | zero => simp [countRange]
  | succ n ih =>
      have hlt : n < m := by omega
      simp only [countRange, Nat.zero_add]
      rw [ih m (by omega)]
      simp [paddedEnv, hlt]

theorem countRange_padded_tail (env : Nat → Bool) (m d : Nat) :
    countRange (paddedEnv env m) m d = 0 := by
  induction d with
  | zero => simp [countRange]
  | succ d ih =>
      have hnot : ¬m + d < m := by omega
      simp [countRange, paddedEnv, hnot, ih]

theorem countRange_padded (env : Nat → Bool) (m n : Nat) (hm : m ≤ n) :
    countRange (paddedEnv env m) 0 n = countRange env 0 m := by
  have hn : n = m + (n - m) := by omega
  rw [hn, countRange_add, countRange_padded_prefix env m m (by omega),
    Nat.zero_add, countRange_padded_tail, Nat.add_zero]

theorem carryChain_eval_eq (env₁ env₂ : Nat → Bool)
    (x₁ y₁ x₂ y₂ : Nat → BitFormula)
    (hx : ∀ i, (x₁ i).eval env₁ = (x₂ i).eval env₂)
    (hy : ∀ i, (y₁ i).eval env₁ = (y₂ i).eval env₂) (n : Nat) :
    (carryChain x₁ y₁ n).eval env₁ = (carryChain x₂ y₂ n).eval env₂ := by
  induction n with
  | zero => rfl
  | succ n ih =>
      simp only [carryChain, carry, eval]
      rw [hx n, hy n, ih]

theorem balancedCount_eval_eq (env₁ env₂ : Nat → Bool)
    (input₁ input₂ : Nat → Nat → BitFormula)
    (hinput : ∀ block k, (input₁ block k).eval env₁ = (input₂ block k).eval env₂)
    (r block k : Nat) :
    (balancedCount input₁ r block k).eval env₁ =
      (balancedCount input₂ r block k).eval env₂ := by
  induction r generalizing block k with
  | zero => exact hinput block k
  | succ r ih =>
      have hc := carryChain_eval_eq env₁ env₂
        (balancedCount input₁ r (2 * block))
        (balancedCount input₁ r (2 * block + 1))
        (balancedCount input₂ r (2 * block))
        (balancedCount input₂ r (2 * block + 1))
        (ih (2 * block)) (ih (2 * block + 1)) k
      simp only [balancedCount, sumBit, eval]
      rw [ih (2 * block) k, ih (2 * block + 1) k, hc]

theorem wordValue_eval_eq (env₁ env₂ : Nat → Bool) (bits₁ bits₂ : Nat → BitFormula)
    (hbits : ∀ k, (bits₁ k).eval env₁ = (bits₂ k).eval env₂) (n : Nat) :
    wordValue env₁ bits₁ n = wordValue env₂ bits₂ n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [wordValue, hbits n, ih]

/-- The actual non-power-of-two input convention uses literal false leaves
above m, not extra independent variables. -/
def paddedLeaves (m : Nat) : Nat → Nat → BitFormula
  | block, 0 => if block < m then .variable block else .constant false
  | _, _ + 1 => .constant false

theorem paddedLeaves_eval (env : Nat → Bool) (m block k : Nat) :
    (paddedLeaves m block k).eval env =
      (booleanLeaves block k).eval (paddedEnv env m) := by
  cases k with
  | zero =>
      by_cases h : block < m <;> simp [paddedLeaves, booleanLeaves, eval, paddedEnv, h]
  | succ k => rfl

theorem paddedLeaves_size (m block k : Nat) : (paddedLeaves m block k).size ≤ 1 := by
  cases k with
  | zero =>
      by_cases h : block < m <;> simp [paddedLeaves, size, h]
  | succ k => simp [paddedLeaves, size]

theorem paddedLeaves_degree (m block k : Nat) :
    (paddedLeaves m block k).degree ≤ 2 ^ k := by
  cases k with
  | zero =>
      by_cases h : block < m <;> simp [paddedLeaves, degree, h]
  | succ k => simp [paddedLeaves, degree]

/-- Exact ordinary count of m independent input Booleans, with literal zero
padding to 2^r leaves and enough output bits to retain the total. -/
theorem paddedBalancedCount_exact_count (env : Nat → Bool) (m r : Nat) (hm : m ≤ 2 ^ r) :
    wordValue env (balancedCount (paddedLeaves m) r 0) (r + 1) =
      countRange env 0 m := by
  calc
    wordValue env (balancedCount (paddedLeaves m) r 0) (r + 1) =
        wordValue (paddedEnv env m) (balancedCount booleanLeaves r 0) (r + 1) :=
      wordValue_eval_eq env (paddedEnv env m) _ _
        (balancedCount_eval_eq env (paddedEnv env m) (paddedLeaves m) booleanLeaves
          (paddedLeaves_eval env m) r 0) (r + 1)
    _ = countRange (paddedEnv env m) 0 (2 ^ r) := by
      rw [balancedCount_exact_count, Nat.mul_zero]
    _ = countRange env 0 m := countRange_padded env m (2 ^ r) hm

/-- A single concrete copied formula meets all three source count obligations:
exact semantics, polynomial size in m, and the bit-specific degree bound. -/
theorem paddedBalancedCount_complete_spec (env : Nat → Bool) (m r : Nat)
    (hm : m ≤ 2 ^ r) (hpad : 2 ^ r ≤ 2 * m) :
    wordValue env (balancedCount (paddedLeaves m) r 0) (r + 1) =
        countRange env 0 m ∧
      ∀ k, k ≤ r →
        (balancedCount (paddedLeaves m) r 0 k).size ≤ 32 * m ^ 5 ∧
        (balancedCount (paddedLeaves m) r 0 k).degree ≤ 2 ^ k := by
  constructor
  · exact paddedBalancedCount_exact_count env m r hm
  · intro k hk
    constructor
    · calc
        (balancedCount (paddedLeaves m) r 0 k).size ≤ (2 ^ r) ^ 5 :=
          balancedCount_polynomial_size (paddedLeaves m) (paddedLeaves_size m) r 0 k hk
        _ ≤ (2 * m) ^ 5 := Nat.pow_le_pow_left hpad 5
        _ = 32 * m ^ 5 := by simp [Nat.mul_pow]
    · exact balancedCount_degree (paddedLeaves m) (paddedLeaves_degree m) r 0 k

#print axioms paddedBalancedCount_exact_count
#print axioms paddedBalancedCount_complete_spec


#print axioms ripple_value
#print axioms ripple_value_mod
#print axioms balancedCount_value_mod
#print axioms balancedCount_exact_count
#print axioms balancedCount_complete_spec


end MoonshotS005.BitFormula

