import «compiler-binary-access»
import OAI.Computability.NearSquareRoot.VisitedCells

/-! Original finite-set visited-space and controller resource bounds for an addressed word access. -/

namespace S008.Compiler.Binary

open OAI.Computability.IntegerMultiplication OAI.Computability.NearSquareRoot

/-- At each elapsed step a deterministic computation has at most one position on each tape. -/
theorem covers_by_elapsed {A Q I : Type} [Fintype I] (m : TM.Rule A Q I)
    (start : TM.Config A Q I) (steps : ℕ) :
    VisitsAtMost m start steps ((steps+1)*Fintype.card I) := by
  classical
  let endAt (j : Fin (steps+1)) : TM.Config A Q I :=
    if h : ∃ c, Trace (TM.advance m) start j.val c then h.choose else start
  let locate (p : Fin (steps+1) × I) : I × ℤ := (p.2,((endAt p.1).tape p.2).pos)
  let cover := Finset.univ.image locate
  refine ⟨cover,?_,?_⟩
  · simpa only [Fintype.card_prod,Fintype.card_fin,Finset.card_univ] using
      (Finset.card_image_le (s := (Finset.univ : Finset (Fin (steps+1) × I))) (f := locate))
  · intro u hu c trace i
    let j : Fin (steps+1) := ⟨u,by omega⟩
    have ex : ∃ q, Trace (TM.advance m) start j.val q := ⟨c,trace⟩
    have equal : endAt j = c := by
      unfold endAt
      rw [dite_eq_left ex]
      exact trace_endpoint_unique ex.choose_spec trace
    apply Finset.mem_image.mpr
    refine ⟨(j,i),Finset.mem_univ _,?_⟩
    simp [locate,equal]

def binary_time (b : ℕ) (xs : List Bool) : ℕ :=
  Unary.eval 0 xs*(2*b+15)+3*b+8*xs.length+19-5*Unary.ones xs

theorem port_count : Fintype.card Port = 5 := by decide

theorem access_visits (store : Bool) (a d z : ℤ → Letter) (p q : ℤ) (b : ℕ) (xs : List Bool) :
    VisitsAtMost (rule store) (command (.prepare .read) a d z p q) (binary_time b xs)
      ((binary_time b xs+1)*5) := by
  simpa only [port_count] using covers_by_elapsed (rule store) (command (.prepare .read) a d z p q)
    (binary_time b xs)

private theorem time_bound (b M : ℕ) (xs : List Bool) (hm : 0<M) (hi : Unary.eval 0 xs<M)
    (width : xs.length≤b) : binary_time b xs ≤ 40*M*(b+1) := by
  have fi : Unary.eval 0 xs * (2*b+15) ≤ M*(15*(b+1)) :=
    Nat.mul_le_mul (by omega) (by omega)
  have fw : 3*b+8*xs.length+19 ≤ M*(19*(b+1)) := by
    calc
      _ ≤ 19*(b+1) := by omega
      _ = 1*(19*(b+1)) := by omega
      _ ≤ _ := Nat.mul_le_mul_right _ (by omega)
  have a15 : M*(15*(b+1)) = 15*(M*(b+1)) := by
    rw [Nat.mul_left_comm]
  have a19 : M*(19*(b+1)) = 19*(M*(b+1)) := by
    rw [Nat.mul_left_comm]
  rw [a15] at fi
  rw [a19] at fw
  unfold binary_time
  rw [Nat.mul_assoc]
  omega

theorem linear_port (store : Bool) (a d z : ℤ → Letter) (p q : ℤ) (b M : ℕ) (xs : List Bool)
    (hm : 0<M) (hi : Unary.eval 0 xs<M) (width : xs.length≤b) :
    binary_time b xs ≤ 40*M*(b+1) ∧
    VisitsAtMost (rule store) (command (.prepare .read) a d z p q) (binary_time b xs)
      (205*M*(b+1)) := by
  have h := time_bound b M xs hm hi width
  refine ⟨h,?_⟩
  obtain ⟨s,hs,hu⟩ := access_visits store a d z p q b xs
  refine ⟨s,hs.trans ?_,hu⟩
  rw [Nat.mul_assoc] at h ⊢
  have one : 0<M*(b+1) := Nat.mul_pos hm (by omega)
  omega

/-- Literal port-level exponents used by the finite controller, with arbitrarily occupied
    input records. The external numerical assumptions are the short controller's stated guards. -/
theorem controller_port (store : Bool) (a d z : ℤ → Letter) (p q : ℤ) (m b : ℕ) (xs : List Bool)
    (domain : 4096≤m) (bits : b+1≤m) (address : Unary.eval 0 xs<m^32) (width : xs.length≤b) :
    binary_time b xs ≤ m^37 ∧
    VisitsAtMost (rule store) (command (.prepare .read) a d z p q) (binary_time b xs) (m^34) := by
  have mpos : 0<m := by omega
  have bound := linear_port store a d z p q b (m^32) xs (Nat.pow_pos mpos) address width
  have ext : (m^32)*(b+1) ≤ m^33 := Nat.mul_le_mul_left _ bits
  have s205 : 205*(m^32)*(b+1) ≤ m^34 := by
    rw [Nat.mul_assoc,Nat.pow_succ m 33,Nat.mul_comm (m^33) m]
    exact Nat.mul_le_mul (by omega) ext
  have short : 40*m^32*(b+1) ≤ 205*m^32*(b+1) := by
    rw [Nat.mul_assoc,Nat.mul_assoc]
    exact Nat.mul_le_mul_right _ (by omega)
  have power : m^34≤m^37 := Nat.pow_le_pow_right mpos (by omega)
  obtain ⟨s,hs,hu⟩ := bound.2
  exact ⟨bound.1.trans (short.trans (s205.trans power)),s,hs.trans s205,hu⟩

#print axioms controller_port

end S008.Compiler.Binary
