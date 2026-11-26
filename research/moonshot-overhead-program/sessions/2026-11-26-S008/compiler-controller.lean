import OAI.Computability.IntegerMultiplication.TMModel

/-! Original tape-model traces for advancing an indexed-memory cursor through occupied records. -/

namespace S008.Compiler

open OAI.Computability.IntegerMultiplication

inductive Letter where
  | blank | home | bit (b : Bool) | delimiter | count
  deriving DecidableEq, Repr, Inhabited

instance : Fintype Letter := Fintype.ofList [.blank,.home,.bit false,.bit true,.delimiter,.count] (by
  intro x
  cases x with
  | bit b => cases b <;> decide
  | _ => decide)

inductive Phase where
  | check | scan | done
  deriving DecidableEq, Repr, Inhabited

instance : Fintype Phase := Fintype.ofList [.check,.scan,.done] (by intro x; cases x <;> decide)

/-- False is the original occupied bank, true is an already enumerated index. -/
def rule : TM.Rule Letter Phase Bool := fun q s =>
  match q with
  | .done => none
  | .check => match s true with
    | .count => some (.scan,fun i => (s i,.stay))
    | .delimiter => some (.done,fun i => (s i,.stay))
    | _ => none
  | .scan => match s false with
    | .bit _ => some (.scan,fun i => (s i,if i then .stay else .right))
    | .delimiter => some (.check,fun i => (s i,.right))
    | _ => none

/-- Absolute tape contents A with the head at p. Arbitrary exterior cells are retained. -/
def atPos (A : ℤ → Letter) (p : ℤ) : TM.Tape Letter := ⟨p, fun k => A (p+k)⟩

private theorem read_at (A : ℤ → Letter) (p : ℤ) : (atPos A p).view 0 = A p := by simp [atPos]

private theorem move_at (A : ℤ → Letter) (p : ℤ) (v : TM.Move) :
    (atPos A p).apply (A p,v) = atPos A (p+v.shift) := by
  unfold atPos TM.Tape.apply
  congr 1
  funext i
  by_cases h : i + v.shift = 0
  · simp only [h, ite_true]
    congr 1
    omega
  · simp only [h, ite_false]
    congr 1
    omega

/-- One W-bit array tape and a unary index tape obtained from the finite compiler. -/
def config (q : Phase) (A B : ℤ → Letter) (p c : ℤ) : TM.Config Letter Phase Bool :=
  ⟨q, fun i => if i then atPos B c else atPos A p⟩

private theorem ext_config {q : Phase} {f g : Bool → TM.Tape Letter} (h : ∀ i, f i = g i) :
    (TM.Config.mk q f) = (TM.Config.mk q g) := congrArg (TM.Config.mk q) (funext h)

private theorem open_record (A B : ℤ → Letter) (p c : ℤ) (h : B c = .count) :
    TM.advance rule (config .check A B p c) = some (config .scan A B p c) := by
  unfold TM.advance config rule
  simp only [ite_true, read_at, h, Option.map_some]
  congr 1
  apply ext_config
  intro i
  cases i <;> simp [read_at,move_at,TM.Move.shift]

private theorem end_index (A B : ℤ → Letter) (p c : ℤ) (h : B c = .delimiter) :
    TM.advance rule (config .check A B p c) = some (config .done A B p c) := by
  unfold TM.advance config rule
  simp only [ite_true, read_at, h, Option.map_some]
  congr 1
  apply ext_config
  intro i
  cases i <;> simp [read_at,move_at,TM.Move.shift]

private theorem next_bit (A B : ℤ → Letter) (p c : ℤ) (b : Bool) (h : A p = .bit b) :
    TM.advance rule (config .scan A B p c) = some (config .scan A B (p+1) c) := by
  unfold TM.advance config rule
  simp only [Bool.false_eq_true, ite_false, read_at, h, Option.map_some]
  congr 1
  apply ext_config
  intro i
  cases i <;> simp [read_at,move_at,TM.Move.shift]

private theorem end_record (A B : ℤ → Letter) (p c : ℤ) (h : A p = .delimiter) :
    TM.advance rule (config .scan A B p c) = some (config .check A B (p+1) (c+1)) := by
  unfold TM.advance config rule
  simp only [Bool.false_eq_true, ite_false, read_at, h, Option.map_some]
  congr 1
  apply ext_config
  intro i
  cases i <;> simp [read_at,move_at,TM.Move.shift]


/-- The loop traversing b occupied bits. Neither tape is written, and the data
    may differ at every position. -/
private theorem scan_bits (A B : ℤ → Letter) (c : ℤ) (n : ℕ) (p : ℤ)
    (bits : ∀ j : ℕ, j < n → ∃ x : Bool, A (p+j) = .bit x) :
    Trace (TM.advance rule) (config .scan A B p c) n (config .scan A B (p+n) c) := by
  induction n generalizing p with
  | zero => simpa using (Trace.nil (step := TM.advance rule) (config .scan A B p c))
  | succ n ih =>
    obtain ⟨x,h⟩ := bits 0 (Nat.zero_lt_succ _)
    have start := next_bit A B p c x (by simpa using h)
    have rest : ∀ j : ℕ, j < n → ∃ x : Bool, A ((p+1)+j) = .bit x := by
      intro j hj
      simpa [Int.natCast_succ,add_assoc,add_comm,add_left_comm] using bits (j+1) (by omega)
    simpa [Int.natCast_succ,add_comm,add_left_comm,add_assoc,Nat.add_comm]
      using Trace.cons start (ih (p+1) rest)

/-- A whole record in an absolute bank, ignoring the rest of its tape. -/
def recordAt (A : ℤ → Letter) (p : ℤ) (b : ℕ) : Prop :=
  (∀ j : ℕ, j < b → ∃ x : Bool, A (p+j) = .bit x) ∧ A (p+b) = .delimiter

private theorem one_record (A B : ℤ → Letter) (p c : ℤ) (b : ℕ)
    (h : recordAt A p b) (h' : B c = .count) :
    Trace (TM.advance rule) (config .check A B p c) (b+2) (config .check A B (p+(b+1)) (c+1)) := by
  have t := (Trace.cons (open_record A B p c h') (scan_bits A B c b p h.1)).trans
    (Trace.single (end_record A B (p+b) c h.2))
  simpa [add_assoc,Nat.add_assoc,Nat.add_comm,Nat.add_left_comm] using t

/-- A complete indexed seek on the exact deterministic multitape machine. The
    independent bits in every original slot and all absolute exterior contents
    are preserved. The selected word may be followed by arbitrary occupied data. -/
theorem indexed_seek (A B : ℤ → Letter) (p c : ℤ) (b i : ℕ)
    (records : ∀ j : ℕ, j < i → recordAt A (p+(j*(b+1) : ℕ)) b)
    (marks : ∀ j : ℕ, j < i → B (c+j) = .count)
    (stop : B (c+i) = .delimiter) :
    Trace (TM.advance rule) (config .check A B p c) (i*(b+2)+1)
      (config .done A B (p+(i*(b+1) : ℕ)) (c+i)) := by
  induction i generalizing p c with
  | zero =>
    simpa using Trace.single (end_index A B p c (by simpa using stop))
  | succ i ih =>
    have head := one_record A B p c b (by simpa using records 0 (Nat.zero_lt_succ _))
      (by simpa using marks 0 (Nat.zero_lt_succ _))
    have pos (j : ℕ) : p + (↑b + 1) + ↑(j * (b+1)) = p + ↑((j+1)*(b+1)) := by
      simp [Nat.add_mul,Int.natCast_add,Int.natCast_mul,add_assoc,add_comm]
    have rr : ∀ j : ℕ, j < i → recordAt A (p+(↑b+1)+(j*(b+1) : ℕ)) b := by
      intro j hj
      rw [pos]
      exact records (j+1) (by omega)
    have rm : ∀ j : ℕ, j < i → B ((c+1)+j) = .count := by
      intro j hj
      simpa [add_assoc,add_left_comm,add_comm] using marks (j+1) (by omega)
    have rs : B (c+1+i) = .delimiter := by
      simpa [Int.natCast_succ,add_assoc,add_left_comm,add_comm] using stop
    have tail := ih (p+(↑b+1)) (c+1) rr rm rs
    have t := head.trans tail
    rw [pos] at t
    simpa [Nat.succ_mul,Int.natCast_succ,add_assoc,add_left_comm,add_comm] using t

/-- The seek stops at the new head positions without reading unrelated data. -/
theorem indexed_seek_halts (A B : ℤ → Letter) (p c : ℤ) :
    TM.advance rule (config .done A B p c) = none := rfl

#print axioms indexed_seek
#print axioms indexed_seek_halts

end S008.Compiler
