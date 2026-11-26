import Std

/-!
# Whole-path spectator divisibility for changing power-of-two batches

This proves the discrete budget used in NW10--NW11 without logarithms or
rounding. It is an abstract path theorem, not a numerical Walsh implementation.
All batches are powers of two; their whole product, rather than each batch
in isolation, must fit the root spectator range.
-/

namespace MoonshotS005

/-- Each changing-arity step consumes a power-of-two batch. Its size is bounded
by the Kth power of the actual active-width contraction factor A. -/
inductive BatchPath (K : Nat) : Nat → Type
  | stop {a : Nat} (positive : 1 ≤ a) : BatchPath K a
  | step {a f A w : Nat} (contraction : A * f ≤ a)
      (localBatch : 2 ^ w ≤ A ^ K) (child : BatchPath K f) :
      BatchPath K a

def BatchPath.exponent {K a : Nat} : BatchPath K a → Nat
  | .stop _ => 0
  | .step (w := w) _ _ child => w + child.exponent

/-- The complete batch product along an arbitrary finite path is at most a^K.
The exponent K is one fixed absolute number throughout the path. -/
theorem BatchPath.product_le {K a : Nat} (p : BatchPath K a) :
    2 ^ p.exponent ≤ a ^ K := by
  induction p with
  | @stop a positive =>
      simpa [exponent] using Nat.pow_le_pow_left positive K
  | @step a f A w contraction localBatch child ih =>
      calc
        2 ^ (w + child.exponent) = 2 ^ w * 2 ^ child.exponent :=
          Nat.pow_add _ _ _
        _ ≤ A ^ K * f ^ K := Nat.mul_le_mul localBatch ih
        _ = (A * f) ^ K := (Nat.mul_pow _ _ _).symm
        _ ≤ a ^ K := Nat.pow_le_pow_left contraction K

/-- A root spectator range at least a^K is divisible by the entire batch
product. Thus no per-level spectator padding is needed under these premises. -/
theorem BatchPath.product_dvd_spectators {K a S : Nat}
    (p : BatchPath K a) (rootBudget : a ^ K ≤ 2 ^ S) :
    2 ^ p.exponent ∣ 2 ^ S := by
  have h : 2 ^ p.exponent ≤ 2 ^ S :=
    Nat.le_trans p.product_le rootBudget
  exact Nat.pow_dvd_pow 2 ((Nat.pow_le_pow_iff_right (by decide : 1 < 2)).mp h)

/-- Every executed prefix of the same power-of-two path also divides the
root spectator range; the contract is stable under any early base stop. -/
theorem BatchPath.prefix_dvd_spectators {K a S t : Nat}
    (p : BatchPath K a) (rootBudget : a ^ K ≤ 2 ^ S)
    (prefixBound : t ≤ p.exponent) : 2 ^ t ∣ 2 ^ S := by
  have h : 2 ^ p.exponent ≤ 2 ^ S :=
    Nat.le_trans p.product_le rootBudget
  have htotal := (Nat.pow_le_pow_iff_right (by decide : 1 < 2)).mp h
  exact Nat.pow_dvd_pow 2 (Nat.le_trans prefixBound htotal)

#print axioms BatchPath.product_le
#print axioms BatchPath.product_dvd_spectators
#print axioms BatchPath.prefix_dvd_spectators

end MoonshotS005

