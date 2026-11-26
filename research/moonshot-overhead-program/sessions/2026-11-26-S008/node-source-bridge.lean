import RecountHandoff

/-! Executable finite node rule tables on the published multitape step and visit semantics. -/

namespace S008.NodeSource

open OAI.Computability.IntegerMultiplication
open OAI.Computability.NearSquareRoot
open S008.Recount (Letter Window)

inductive Expr (k : ℕ) where
  | literal (v : Letter)
  | copy (i : Fin k)
  | bx (i j : Fin k)

def value {k : ℕ} (read : Fin k → Letter) : Expr k → Option Letter
  | .literal a => some a
  | .copy i => some (read i)
  | .bx i j =>
    match read i, read j with
    | .bit a,.bit b => some (.bit (a != b))
    | _,_ => none

structure Action (k states : ℕ) where
  target : Fin (states+1)
  writes : List (Fin k × Expr k)
  moves : List (Fin k × TM.Move)

structure Instruction (k states : ℕ) where
  probe : Option (Fin k)
  branches : List (Letter × Action k states)
  otherwise : Option (Action k states)

structure Table (k states : ℕ) where
  rows : Array (Instruction k states)
  width : rows.size=states

def select {k states : ℕ} (row : Instruction k states) (read : Fin k → Letter) :
    Option (Action k states) :=
  match row.probe with
  | none => row.otherwise
  | some i => (row.branches.lookup (read i)).orElse (fun _ => row.otherwise)

def issue {k states : ℕ} (take : Action k states) (read : Fin k → Letter) :
    Option (Fin (states+1) × (Fin k → Letter × TM.Move)) :=
  if !(take.writes.all (fun w => (value read w.2).isSome)) then none
  else
    some (take.target,fun i =>
      (((take.writes.lookup i).bind (value read)).getD (read i),
       (take.moves.lookup i).getD .stay))

/-- The instruction table, including any copy/XOR of old scanned symbols, is fixed
    finite control. Its alphabet, program counter set, and tape index set are finite. -/
def rule {k states : ℕ} (p : Table k states) : TM.Rule Letter (Fin (states+1)) (Fin k) :=
  fun pc read => do
    let row ← p.rows[pc.val]?
    let take ← select row read
    issue take read

/-- A finite local view of all heads, including exact low/high materialized positions. -/
structure Runtime (k states : ℕ) where
  pc : Fin (states+1)
  windows : Vector Window k
  low : Vector ℤ k
  high : Vector ℤ k

def physical {k states : ℕ} (r : Runtime k states) :
    TM.Config Letter (Fin (states+1)) (Fin k) :=
  ⟨r.pc,fun i => r.windows[i].physical⟩

def initial {k states : ℕ} (entry : Fin (states+1)) (words : Array (List Letter)) :
    Runtime k states :=
  ⟨entry,Vector.ofFn (fun i => ⟨0,[],(words[i.val]?).getD []⟩), Vector.replicate k 0,
    Vector.replicate k 0⟩

def step {k states : ℕ} (p : Table k states) (r : Runtime k states) :
    Option (Runtime k states) := do
  let (q,op) ← rule p r.pc (fun i => r.windows[i].atHead)
  let w := Vector.ofFn (fun i : Fin k => r.windows[i].apply (op i).1 (op i).2)
  return ⟨q,w,Vector.ofFn (fun i => min r.low[i] w[i].pos),
    Vector.ofFn (fun i => max r.high[i] w[i].pos)⟩

theorem physical_step {k states : ℕ} (p : Table k states) (r : Runtime k states) :
    (step p r).map physical = TM.advance (rule p) (physical r) := by
  unfold TM.advance physical step
  simp only [S008.Recount.Window.read_physical]
  rcases hr : rule p r.pc (fun i => r.windows[i].atHead) with _ | qr
  · rfl
  rcases qr with ⟨q,op⟩
  simp [S008.Recount.Window.physical_apply]

def run {k states : ℕ} (p : Table k states) (r : Runtime k states) :
    ℕ → Option (Runtime k states)
  | 0 => some r
  | n+1 => (step p r).bind (fun r' => run p r' n)

theorem sound {k states : ℕ} (p : Table k states) {r d : Runtime k states} {n : ℕ}
    (h : run p r n = some d) :
    Trace (TM.advance (rule p)) (physical r) n (physical d) := by
  induction n generalizing r with
  | zero =>
    have e : r=d := Option.some.inj h
    subst d
    exact .nil _
  | succ j ih =>
    unfold run at h
    rcases hs : step p r with _ | v
    · rw [hs] at h
      contradiction
    rw [hs] at h
    have s := physical_step p r
    rw [hs] at s
    simpa [Nat.add_comm] using (Trace.cons s.symm (ih h))

theorem halt_sound {k states : ℕ} (p : Table k states) (r : Runtime k states)
    (h : r.pc.val=states) : TM.advance (rule p) (physical r) = none := by
  have missing : p.rows[r.pc.val]?=none := by simp [h,p.width]
  simp [TM.advance,rule,physical,missing]

theorem extrema_step {k states : ℕ} (p : Table k states) {r d : Runtime k states}
    (h : step p r=some d) (i : Fin k) :
    d.low[i]≤r.low[i] ∧ r.high[i]≤d.high[i] ∧
      d.low[i]≤d.windows[i].pos ∧ d.windows[i].pos≤d.high[i] := by
  unfold step at h
  rcases hr : rule p r.pc (fun j => r.windows[j].atHead) with _ | qr
  · rw [hr] at h
    contradiction
  rcases qr with ⟨q,op⟩
  rw [hr] at h
  cases h
  simp

theorem extrema_run {k states : ℕ} (p : Table k states) {r d : Runtime k states} {n : ℕ}
    (h : run p r n=some d) (i : Fin k) : d.low[i]≤r.low[i] ∧ r.high[i]≤d.high[i] := by
  induction n generalizing r with
  | zero =>
    have e : r=d := Option.some.inj h
    subst d
    exact ⟨le_refl _,le_refl _⟩
  | succ j ih =>
    unfold run at h
    rcases hs : step p r with _ | v
    · rw [hs] at h
      contradiction
    rw [hs] at h
    obtain ⟨l,g⟩ := ih h
    obtain ⟨l',g',_⟩ := extrema_step p hs i
    exact ⟨le_trans l l',le_trans g' g⟩

def fenced {k states : ℕ} (r : Runtime k states) : Prop :=
  ∀ i : Fin k, r.low[i] ≤ r.windows[i].pos ∧ r.windows[i].pos ≤ r.high[i]

theorem run_fenced {k states : ℕ} (p : Table k states) {r d : Runtime k states}
    {n : ℕ} (hr : fenced r) (h : run p r n=some d) : fenced d := by
  induction n generalizing r with
  | zero =>
    have e : r=d := Option.some.inj h
    exact e ▸ hr
  | succ j ih =>
    unfold run at h
    rcases hs : step p r with _ | v
    · rw [hs] at h
      contradiction
    rw [hs] at h
    exact ih (fun i => (extrema_step p hs i).2.2) h

theorem run_add {k states : ℕ} (p : Table k states) (r : Runtime k states) (u v : ℕ) :
    run p r (u+v) = (run p r u).bind (fun y => run p y v) := by
  induction u generalizing r with
  | zero => simp [run]
  | succ j ih =>
    rw [Nat.succ_add]
    simp only [run,Option.bind_assoc]
    apply congrArg (Option.bind (step p r))
    funext s
    exact ih s

theorem visits_sound {k states : ℕ} (p : Table k states) {r d : Runtime k states}
    {n : ℕ} (h : run p r n=some d) (hr : fenced r) :
    VisitsAtMost (rule p) (physical r) n
      (∑ i : Fin k, (d.high[i]+1-d.low[i]).toNat) := by
  apply visitsAtMost_of_tape_fences (lo:=fun i => d.low[i]) (hi:=fun i => d.high[i])
  intro u hu c hinput i
  have eq : u+(n-u)=n := by omega
  have both := run_add p r u (n-u)
  rw [eq,h] at both
  rcases e : run p r u with _ | v
  · rw [e] at both
    contradiction
  rw [e] at both
  have q := trace_endpoint_unique hinput (sound p e)
  subst c
  obtain ⟨hl,hh⟩ := (run_fenced p hr e) i
  obtain ⟨ll,gg⟩ := extrema_run p both.symm i
  exact ⟨le_trans ll hl, le_trans hh gg⟩

@[simp] theorem fenced_initial {k states : ℕ} (entry : Fin (states+1))
    (words : Array (List Letter)) : fenced (initial (k:=k) entry words) := by
  intro i
  simp [initial]

/-- Canonical finite presentation of a half tape, with all trailing blanks removed. -/
def trim : List Letter → List Letter
  | [] => []
  | a :: xs =>
    match trim xs with
    | [] => if a=.blank then [] else [a]
    | b::ys => a::b::ys

theorem get_trim (xs : List Letter) (n : ℕ) :
    (trim xs)[n]?.getD .blank = xs[n]?.getD .blank := by
  induction xs generalizing n with
  | nil => rfl
  | cons a xs ih =>
    cases h : trim xs with
    | nil =>
      by_cases e : a=.blank
      · subst a
        cases n with
        | zero => simp [trim,h]
        | succ n => simpa [trim,h] using ih n
      · cases n with
        | zero => simp [trim,h,e]
        | succ n => simpa [trim,h,e] using ih n
    | cons b ys =>
      cases n with
      | zero => simp [trim,h]
      | succ n => simpa [trim,h] using ih n

def windowMatches (a b : Window) : Prop :=
  a.pos=b.pos ∧ trim a.pre=trim b.pre ∧ trim a.post=trim b.post

instance (a b : Window) : Decidable (windowMatches a b) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _))

theorem physical_eq_of_matches {a b : Window} (h : windowMatches a b) :
    a.physical=b.physical := by
  apply congrArg₂ TM.Tape.mk h.1
  funext i
  cases i with
  | ofNat n =>
    change a.post[n]?.getD .blank=b.post[n]?.getD .blank
    rw [← get_trim a.post n, ← get_trim b.post n, h.2.2]
  | negSucc n =>
    change a.pre[n]?.getD .blank=b.pre[n]?.getD .blank
    rw [← get_trim a.pre n, ← get_trim b.pre n, h.2.1]

def caseWords {k : ℕ} (ws : Array (List Letter)) : Vector Window k :=
  Vector.ofFn (fun i => ⟨0,[],(ws[i.val]?).getD []⟩)

/-- Full expected windows check both the resulting tape function and the head.
    The declared fare includes every cell traversed, including erased work. -/
def check {k states : ℕ} (p : Table k states) (entry : Fin (states+1))
    (start : Array (List Letter)) (clock fare : ℕ) (expected : Vector Window k) : Bool :=
  match run p (initial entry start) clock with
  | none => false
  | some d => decide (d.pc.val=states ∧
        (∑ i : Fin k, (d.high[i]+1-d.low[i]).toNat)=fare ∧
        ∀ i : Fin k, windowMatches d.windows[i] expected[i])

/-- A successful executable certificate implies the released exact-time physical trace,
    halting, visited-set upper bound, and equality of every full countable output tape. -/
theorem check_sound {k states : ℕ} (p : Table k states) (entry : Fin (states+1))
    (start : Array (List Letter)) (clock fare : ℕ) (expected : Vector Window k)
    (h : check p entry start clock fare expected=true) :
    ∃ c : TM.Config Letter (Fin (states+1)) (Fin k),
      Trace (TM.advance (rule p)) (physical (initial entry start)) clock c ∧
      TM.advance (rule p) c=none ∧
      VisitsAtMost (rule p) (physical (initial entry start)) clock fare ∧
      ∀ i : Fin k, c.tape i=expected[i].physical := by
  cases hr : run p (initial entry start) clock with
  | none => simp [check,hr] at h
  | some d =>
    simp only [check,hr,decide_eq_true_eq] at h
    refine ⟨physical d,sound p hr,halt_sound p d h.1,?_,?_⟩
    · rw [← h.2.1]
      exact visits_sound p hr (fenced_initial entry start)
    · intro i
      exact physical_eq_of_matches (h.2.2 i)

end S008.NodeSource
