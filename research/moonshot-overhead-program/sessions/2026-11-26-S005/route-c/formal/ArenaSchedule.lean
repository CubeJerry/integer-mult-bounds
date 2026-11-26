import Std

/-!
# Reused-arena schedules with shrinking children and released reserve descents

This is a self-contained abstract allocation lemma. It does not instantiate a
Turing machine, the AQ geometry, or the source's integer-multiplication theorem.
A schedule lives in one fixed arena whose left endpoint does not move between
sequential or reserve calls. Its span bounds every cell that it ever visits.
The input to a child is measured in the same raw-bit units as its parent.
-/

namespace MoonshotS005

/-- A finite execution tree with explicit release/reuse conventions.

`leaf` uses a local frame of size at most `C * V`.
`shrink` parks one such frame before a child of at most half the volume.
`reserve` releases all local payload before a child, reusing the same arena.
`sequence` reuses the same arena for both completed executions.
-/
inductive ArenaSchedule (C : Nat) : Nat → Type
  | leaf (V : Nat) : ArenaSchedule C V
  | shrink {V W : Nat} (half : 2 * W ≤ V)
      (child : ArenaSchedule C W) : ArenaSchedule C V
  | reserve {V W : Nat} (noGrowth : W ≤ V)
      (child : ArenaSchedule C W) : ArenaSchedule C V
  | sequence {V : Nat} (first second : ArenaSchedule C V) :
      ArenaSchedule C V

/-- The arena prefix covering every visited cell, not a peak-live-cell count. -/
def ArenaSchedule.span {C V : Nat} : ArenaSchedule C V → Nat
  | .leaf V => C * V
  | .shrink _ child => C * V + child.span
  | .reserve _ child => child.span
  | .sequence first second => max first.span second.span

theorem ArenaSchedule.span_le {C V : Nat} (s : ArenaSchedule C V) :
    s.span ≤ 2 * C * V := by
  induction s with
  | leaf V =>
      simp only [span]
      have heq : 2 * C * V = C * V + C * V := by
        simp [Nat.two_mul, Nat.add_mul]
      rw [heq]
      omega
  | @shrink V W half child ih =>
      simp only [span]
      have hm : C * (2 * W) ≤ C * V := Nat.mul_le_mul_left C half
      have heq : C * (2 * W) = 2 * C * W := by
        simp [Nat.mul_comm, Nat.mul_left_comm]
      rw [heq] at hm
      have hs : C * V + child.span ≤ C * V + C * V :=
        Nat.add_le_add_left (Nat.le_trans ih hm) _
      have hdouble : C * V + C * V = 2 * C * V := by
        simp [Nat.two_mul, Nat.add_mul]
      exact hdouble ▸ hs
  | @reserve V W noGrowth child ih =>
      simp only [span]
      exact Nat.le_trans ih (Nat.mul_le_mul_left (2 * C) noGrowth)
  | sequence first second ihFirst ihSecond =>
      simp only [span]
      exact Nat.max_le.mpr ⟨ihFirst, ihSecond⟩

/-- Every address allowed by the schedule's marked arena is inside one absolute
`2*C*V` interval. Sequential calls and released full-volume reserve chains do
not allocate new intervals. -/
theorem ArenaSchedule.visited_address_lt {C V : Nat}
    (s : ArenaSchedule C V) {address : Nat} (visited : address < s.span) :
    address < 2 * C * V :=
  Nat.lt_of_lt_of_le visited s.span_le

/-- Arbitrarily many completed reserve calls preserve exactly the same span. -/
def repeatedReserve {C V : Nat} (n : Nat) (s : ArenaSchedule C V) :
    ArenaSchedule C V :=
  match n with
  | 0 => s
  | n + 1 => .reserve (Nat.le_refl V) (repeatedReserve n s)

theorem repeatedReserve_span {C V : Nat} (n : Nat) (s : ArenaSchedule C V) :
    (repeatedReserve n s).span = s.span := by
  induction n with
  | zero => rfl
  | succ n ih => exact ih

/-- Failure control: parking a full-volume frame at every reserve descent
has linear dependence on the number of descents and violates any uniform
`2*C*V` cap after three nonzero frames. -/
theorem three_parked_full_frames_exceed {C V : Nat}
    (h : 0 < C * V) : 2 * C * V < 3 * (C * V) := by
  have heq : 2 * C * V = 2 * (C * V) := Nat.mul_assoc 2 C V
  rw [heq]
  omega

#print axioms ArenaSchedule.span_le
#print axioms ArenaSchedule.visited_address_lt
#print axioms repeatedReserve_span
#print axioms three_parked_full_frames_exceed

end MoonshotS005

