import NodeBridge

/-! Source-level finite-table certificate valid on every valuation of independent data bits. -/

namespace S008.Symbolic

open OAI.Computability.IntegerMultiplication OAI.Computability.NearSquareRoot
open S008.Recount (Letter Window)
open S008.NodeSource (Expr Action Instruction Table Runtime)

inductive Formula where
  | bit (b : Bool)
  | input (n : ℕ)
  | xor (a b : Formula)
  deriving DecidableEq, Repr

def Formula.eval (v : ℕ → Bool) : Formula → Bool
  | .bit b => b
  | .input n => v n
  | .xor a b => a.eval v != b.eval v

inductive Glyph where
  | fixed (a : Letter)
  | bits (f : Formula)
  deriving DecidableEq, Repr

def Glyph.eval (v : ℕ → Bool) : Glyph → Letter
  | .fixed a => a
  | .bits f => .bit (f.eval v)

def Glyph.asBit : Glyph → Option Formula
  | .fixed (.bit b) => some (.bit b)
  | .bits f => some f
  | _ => none

private def bitOf : Letter → Option Bool
  | .bit b => some b
  | _ => none

private theorem bit_eval (v : ℕ → Bool) (a : Glyph) :
    a.asBit.map (Formula.eval v) = bitOf (a.eval v) := by
  cases a with
  | fixed x => cases x <;> rfl
  | bits f => rfl

def value {k : ℕ} (r : Fin k → Glyph) : Expr k → Option Glyph
  | .literal c => some (.fixed c)
  | .copy i => some (r i)
  | .bx i j => do
    let a ← (r i).asBit
    let b ← (r j).asBit
    return .bits (.xor a b)

private theorem xor_eval (u w : Letter) :
    (do let a ← bitOf u
        let b ← bitOf w
        pure (Letter.bit (a != b))) =
       (match u,w with | .bit a,.bit b => some (.bit (a != b)) | _,_ => none) := by
  cases u <;> cases w <;> rfl

theorem value_eval {k : ℕ} (v : ℕ → Bool) (r : Fin k → Glyph) (e : Expr k) :
    (value r e).map (Glyph.eval v) = S008.NodeSource.value (fun i => (r i).eval v) e := by
  cases e with
  | literal a => rfl
  | copy i => rfl
  | bx i j =>
    simp only [value,S008.NodeSource.value]
    rw [← xor_eval ((r i).eval v) ((r j).eval v),← bit_eval,← bit_eval]
    cases (r i).asBit <;> cases (r j).asBit <;> rfl

/-- An unknown bit may control only a probe that gives both bits its default branch. -/
def pick {k s : ℕ} (row : Instruction k s) (r : Fin k → Glyph) : Option (Action k s) :=
  match row.probe with
  | none => row.otherwise
  | some i =>
    match r i with
    | .fixed a => (row.branches.lookup a).orElse (fun _ => row.otherwise)
    | .bits _ =>
      if (row.branches.lookup (.bit false)).isNone && (row.branches.lookup (.bit true)).isNone
      then row.otherwise else none

theorem pick_eval {k s : ℕ} (v : ℕ → Bool) (row : Instruction k s) (r : Fin k → Glyph)
    {a : Action k s} (h : pick row r=some a) :
    S008.NodeSource.select row (fun i => (r i).eval v)=some a := by
  unfold pick at h
  unfold S008.NodeSource.select
  cases q : row.probe with
  | none => simpa [q] using h
  | some i =>
    rw [q] at h
    cases x : r i with
    | fixed u => simpa [x,Glyph.eval] using h
    | bits f =>
      simp only [x] at h
      by_cases x0 : row.branches.lookup (.bit false)=none
      · by_cases x1 : row.branches.lookup (.bit true)=none
        · simp [x0,x1] at h
          cases b : f.eval v <;> simp [x,Glyph.eval,b,x0,x1,h]
        · simp [x0,x1] at h
      · simp [x0] at h

def issue {k s : ℕ} (a : Action k s) (r : Fin k → Glyph) :
    Option (Fin (s+1) × (Fin k → Glyph × TM.Move)) :=
  if !(a.writes.all (fun w => (value r w.2).isSome)) then none
  else some (a.target,fun i => (((a.writes.lookup i).bind (value r)).getD (r i),
                                (a.moves.lookup i).getD .stay))

theorem issue_eval {k s : ℕ} (v : ℕ → Bool) (a : Action k s) (r : Fin k → Glyph) :
    (issue a r).map (fun z => (z.1,fun i => ((z.2 i).1.eval v,(z.2 i).2))) =
    S008.NodeSource.issue a (fun i => (r i).eval v) := by
  have valid (e : Expr k) :
      (S008.NodeSource.value (fun i => (r i).eval v) e).isSome=(value r e).isSome := by
    rw [← value_eval]
    cases value r e <;> rfl
  unfold issue S008.NodeSource.issue
  simp_rw [valid]
  split
  · rfl
  · apply congrArg some
    apply Prod.ext
    · rfl
    · funext i
      apply Prod.ext
      · change (((a.writes.lookup i).bind (value r)).getD (r i)).eval v =
           ((a.writes.lookup i).bind (S008.NodeSource.value (fun i => (r i).eval v))).getD _
        cases h : a.writes.lookup i with
        | none => rfl
        | some e =>
          change ((value r e).getD (r i)).eval v=(S008.NodeSource.value (fun i => (r i).eval v) e).getD _
          rw [← value_eval]
          cases value r e <;> rfl
      · rfl

def rule {k s : ℕ} (p : Table k s) (pc : Fin (s+1)) (r : Fin k → Glyph) :
    Option (Fin (s+1) × (Fin k → Glyph × TM.Move)) := do
  let row ← p.rows[pc.val]?
  let a ← pick row r
  issue a r

theorem rule_eval {k s : ℕ} (v : ℕ → Bool) (p : Table k s) (pc : Fin (s+1))
    (r : Fin k → Glyph) {q : Fin (s+1)} {ops : Fin k → Glyph × TM.Move}
    (h : rule p pc r=some (q,ops)) :
    S008.NodeSource.rule p pc (fun i => (r i).eval v)=
      some (q,fun i => ((ops i).1.eval v,(ops i).2)) := by
  unfold rule at h
  unfold S008.NodeSource.rule
  cases hr : p.rows[pc.val]? with
  | none => rw [hr] at h; contradiction
  | some row =>
    rw [hr] at h
    cases ha : pick row r with
    | none => simp [ha] at h
    | some a =>
      simp [ha] at h
      change ((S008.NodeSource.select row (fun i => (r i).eval v)).bind (fun a => S008.NodeSource.issue a (fun i => (r i).eval v)))=_
      rw [pick_eval v row r ha]
      have e := issue_eval v a r
      rw [h] at e
      exact e.symm

structure WindowS where
  pos : ℤ
  pre : List Glyph
  post : List Glyph
  deriving Repr

def WindowS.eval (v : ℕ → Bool) (w : WindowS) : Window :=
  ⟨w.pos,w.pre.map (Glyph.eval v),w.post.map (Glyph.eval v)⟩

@[simp] theorem pos_eval (v : ℕ → Bool) (w : WindowS) : (w.eval v).pos=w.pos := rfl

def WindowS.head (w : WindowS) : Glyph := w.post.headD (.fixed .blank)

def WindowS.apply (w : WindowS) (a : Glyph) (m : TM.Move) : WindowS :=
  match m with
  | .stay => ⟨w.pos,w.pre,a::w.post.tail⟩
  | .right => ⟨w.pos+1,a::w.pre,w.post.tail⟩
  | .left => ⟨w.pos-1,w.pre.tail,w.pre.headD (.fixed .blank)::a::w.post.tail⟩

theorem head_eval (v : ℕ → Bool) (w : WindowS) : (w.head).eval v=(w.eval v).atHead := by
  rcases w with ⟨p,b,d⟩
  cases d <;> rfl

theorem apply_eval (v : ℕ → Bool) (w : WindowS) (a : Glyph) (m : TM.Move) :
    (w.apply a m).eval v=(w.eval v).apply (a.eval v) m := by
  rcases w with ⟨p,b,d⟩
  cases b <;> cases d <;> cases m <;> rfl

structure State (k s : ℕ) where
  pc : Fin (s+1)
  windows : Vector WindowS k
  low : Vector ℤ k
  high : Vector ℤ k

def State.eval {k s : ℕ} (v : ℕ → Bool) (r : State k s) : Runtime k s :=
  ⟨r.pc,Vector.ofFn (fun i => r.windows[i].eval v),r.low,r.high⟩

def initial {k s : ℕ} (pc : Fin (s+1)) (words : Array (List Glyph)) : State k s :=
  ⟨pc,Vector.ofFn (fun i => ⟨0,[],(words[i.val]?).getD []⟩),
    Vector.replicate k 0,Vector.replicate k 0⟩

def step {k s : ℕ} (p : Table k s) (r : State k s) : Option (State k s) := do
  let (q,op) ← rule p r.pc (fun i => r.windows[i].head)
  let w := Vector.ofFn (fun i : Fin k => r.windows[i].apply (op i).1 (op i).2)
  return ⟨q,w,Vector.ofFn (fun i => min r.low[i] w[i].pos),Vector.ofFn (fun i => max r.high[i] w[i].pos)⟩

theorem step_eval {k s : ℕ} (v : ℕ → Bool) (p : Table k s) {r d : State k s}
    (h : step p r=some d) :
    S008.NodeSource.step p (r.eval v)=some (d.eval v) := by
  unfold step at h
  cases hr : rule p r.pc (fun i => r.windows[i].head) with
  | none => rw [hr] at h; contradiction
  | some item =>
    rcases item with ⟨q,op⟩
    rw [hr] at h
    cases h
    have correct := rule_eval v p r.pc (fun i => r.windows[i].head) hr
    simp_rw [head_eval] at correct
    have correct' : (S008.NodeSource.rule p (r.eval v).pc (fun i => (r.eval v).windows[i].atHead)) =
        some (q,fun i => ((op i).1.eval v,(op i).2)) := by simpa [State.eval] using correct
    unfold S008.NodeSource.step
    rw [correct']
    simp [State.eval,← apply_eval]

def run {k s : ℕ} (p : Table k s) (r : State k s) : ℕ → Option (State k s)
  | 0 => some r
  | n+1 => (step p r).bind (fun w => run p w n)

theorem run_eval {k s : ℕ} (v : ℕ → Bool) (p : Table k s) {r d : State k s}
    {n : ℕ} (h : run p r n=some d) :
    S008.NodeSource.run p (r.eval v) n=some (d.eval v) := by
  induction n generalizing r with
  | zero =>
    have e : r=d := Option.some.inj h
    subst d
    rfl
  | succ n ih =>
    unfold run at h
    cases hstep : step p r with
    | none => rw [hstep] at h; contradiction
    | some w =>
      rw [hstep] at h
      unfold S008.NodeSource.run
      rw [step_eval v p hstep]
      exact ih h

def trim : List Glyph → List Glyph
  | [] => []
  | a :: xs =>
    match trim xs with
    | [] => if a=.fixed .blank then [] else [a]
    | b::ys => a::b::ys

@[simp] theorem eval_blank (a : Glyph) (v : ℕ → Bool) :
    a.eval v=.blank ↔ a=.fixed .blank := by
  cases a with
  | fixed u => cases u <;> simp [Glyph.eval]
  | bits f => simp [Glyph.eval]

theorem trim_eval (v : ℕ → Bool) (xs : List Glyph) :
    S008.NodeSource.trim (xs.map (Glyph.eval v))=(trim xs).map (Glyph.eval v) := by
  induction xs with
  | nil => rfl
  | cons a xs ih =>
    cases h : trim xs with
    | nil =>
      by_cases ha : a=.fixed .blank
      · subst a
        simp [trim,S008.NodeSource.trim,ih,h,Glyph.eval]
      · simp [trim,S008.NodeSource.trim,ih,h,ha]
    | cons b ys => simp [trim,S008.NodeSource.trim,ih,h]

def same (w u : WindowS) : Prop :=
  w.pos=u.pos ∧ trim w.pre=trim u.pre ∧ trim w.post=trim u.post

instance (w u : WindowS) : Decidable (same w u) := inferInstanceAs (Decidable (_ ∧ _ ∧ _))

theorem same_eval (v : ℕ → Bool) {w u : WindowS} (h : same w u) :
    S008.NodeSource.windowMatches (w.eval v) (u.eval v) := by
  rcases h with ⟨q,l,r⟩
  simp [S008.NodeSource.windowMatches,WindowS.eval,q,trim_eval,l,r]

/-- All banks start with head zero; the list begins under the head and the wings are blank. -/
def home {k : ℕ} (words : Array (List Glyph)) : Vector WindowS k :=
  Vector.ofFn (fun i => ⟨0,[],(words[i.val]?).getD []⟩)

def check {k s : ℕ} (p : Table k s) (entry : Fin (s+1)) (start : Array (List Glyph))
    (clock cells : ℕ) (expected : Vector WindowS k) : Bool :=
  match run p (initial entry start) clock with
  | none => false
  | some d => decide (d.pc.val=s ∧ (∑ i : Fin k, (d.high[i]+1-d.low[i]).toNat)=cells ∧
                ∀ i : Fin k, same d.windows[i] expected[i])

/-- Once a shape's symbolic trace is checked, vary every source bit simultaneously.
    This proves the original physical rule's full output and visited bound. -/
theorem check_sound {k s : ℕ} (p : Table k s) (entry : Fin (s+1))
    (start : Array (List Glyph)) (clock cells : ℕ) (expected : Vector WindowS k)
    (h : check p entry start clock cells expected=true) (v : ℕ → Bool) :
    ∃ c : TM.Config Letter (Fin (s+1)) (Fin k),
      Trace (TM.advance (S008.NodeSource.rule p)) (S008.NodeSource.physical ((initial entry start).eval v)) clock c ∧
      TM.advance (S008.NodeSource.rule p) c=none ∧
      VisitsAtMost (S008.NodeSource.rule p) (S008.NodeSource.physical ((initial entry start).eval v)) clock cells ∧
      ∀ i : Fin k, c.tape i=(expected[i].eval v).physical := by
  cases hr : run p (initial entry start) clock with
  | none => simp [check,hr] at h
  | some d =>
    simp only [check,hr,decide_eq_true_eq] at h
    have real := run_eval v p hr
    refine ⟨S008.NodeSource.physical (d.eval v),S008.NodeSource.sound p real,
      S008.NodeSource.halt_sound p _ h.1,?_,?_⟩
    · rw [← h.2.1]
      apply S008.NodeSource.visits_sound p real
      intro i
      simp [initial,State.eval,WindowS.eval]
    · intro i
      exact S008.NodeSource.physical_eq_of_matches (by simpa [State.eval] using same_eval v (h.2.2 i))

end S008.Symbolic
