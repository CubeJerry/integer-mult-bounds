import Std

/-!
# Mixed payload and descriptor potential

This is the arithmetic bridge for an adaptive physical supplier whose local
time may grow while its payload coefficient remains fixed. It does not
construct a tape machine or prove an actual program meets the contract.
The descriptor allowance is any monotone function, not only a logarithm.
-/

namespace MoonshotS005.ResourcePotential

def cap (C h V : Nat) (descriptor : Nat → Nat) : Nat :=
  3 * C * V + (h + 1) * descriptor V

theorem payload_le (C h V : Nat) (descriptor : Nat → Nat) :
    C * V ≤ cap C h V descriptor := by
  have hm : C * V ≤ 3 * C * V :=
    Nat.mul_le_mul_right V (by omega)
  exact Nat.le_trans hm (Nat.le_add_right ..)

theorem descriptor_le (C h V : Nat) (descriptor : Nat → Nat) :
    descriptor V ≤ cap C h V descriptor := by
  have hm : descriptor V ≤ (h + 1) * descriptor V := by
    simpa using Nat.mul_le_mul_right (descriptor V) (show 1 ≤ h + 1 by omega)
  exact Nat.le_trans hm (Nat.le_add_left ..)

/-- A contracted child may retain a whole parent payload. -/
theorem small_step (C h V h' V' : Nat) (descriptor : Nat → Nat)
    (order : h' < h) (shrink : 3 * V' ≤ 2 * V)
    (mono : descriptor V' ≤ descriptor V) :
    C * V + cap C h' V' descriptor ≤ cap C h V descriptor := by
  have hvol : 3 * C * V' ≤ 2 * C * V := by
    have z := Nat.mul_le_mul_left C shrink
    simpa [Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm] using z
  have hh : (h' + 1) * descriptor V' ≤ h * descriptor V :=
    Nat.mul_le_mul (by omega) mono
  simp only [cap]
  have hv : C * V + 2 * C * V = 3 * C * V := by
    simp [Nat.mul_assoc]
    omega
  have hd : h * descriptor V ≤ (h + 1) * descriptor V :=
    Nat.mul_le_mul_right _ (by omega)
  omega

/-- A full-volume descent retains only its descriptor, after ownership
of the parent's payload region has been transferred. -/
theorem full_step (C h V h' V' : Nat) (descriptor : Nat → Nat)
    (order : h' < h) (contract : V' ≤ V)
    (mono : descriptor V' ≤ descriptor V) :
    descriptor V + cap C h' V' descriptor ≤ cap C h V descriptor := by
  have hv : 3 * C * V' ≤ 3 * C * V := Nat.mul_le_mul_left _ contract
  have hh : (h' + 1) * descriptor V' ≤ h * descriptor V :=
    Nat.mul_le_mul (by omega) mono
  have hd : (h + 1) * descriptor V = h * descriptor V + descriptor V := by
    rw [Nat.add_mul, Nat.one_mul]
  simp only [cap]
  omega

/-- Distinct siblings and phases reuse the same marked intervals: the
maximum child demand, rather than their sum, is the required address cap. -/
theorem siblings_max (parent first second : Nat)
    (hfirst : first ≤ parent) (hsecond : second ≤ parent) :
    max first second ≤ parent := Nat.max_le.mpr ⟨hfirst, hsecond⟩

/-- The descriptor budget may be discharged separately, for example from
exponentially large complete arrays and a fixed polynomial in address bits. -/
theorem linear_cap (C D h V : Nat) (descriptor : Nat → Nat)
    (budget : (h + 1) * descriptor V ≤ D * V) :
    cap C h V descriptor ≤ (3 * C + D) * V := by
  calc
    cap C h V descriptor ≤ 3 * C * V + D * V := Nat.add_le_add_left budget _
    _ = (3 * C + D) * V := (Nat.add_mul _ _ _).symm

#print axioms payload_le
#print axioms descriptor_le
#print axioms small_step
#print axioms full_step
#print axioms siblings_max
#print axioms linear_cap

end MoonshotS005.ResourcePotential
