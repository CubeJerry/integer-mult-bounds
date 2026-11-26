import NodeTables

/-! A check on each fixed instruction proves the same trace geometry for every
    binary filling of any occupied data/metadata layout, at arbitrary widths. -/

namespace S008.DataLayout

open OAI.Computability.IntegerMultiplication OAI.Computability.NearSquareRoot
open S008.Recount (Letter)
open S008.NodeSource

def erase (data : Bool) (a : Letter) : Letter :=
  match data,a with | true,.bit _ => .bit false | _,a => a

def exprOK {k : ℕ} (data : Fin k → Bool) (i : Fin k) : Expr k → Bool
  | .literal a => erase (data i) a == a
  | .copy j => data i==data j
  | .bx j l => data i==data j && data i==data l

def actionOK {k s : ℕ} (data : Fin k → Bool) (a : Action k s) : Bool :=
  a.writes.all (fun w => exprOK data w.1 w.2)

def probeOK {k s : ℕ} (data : Fin k → Bool) (row : Instruction k s) : Bool :=
  match row.probe with
  | none => true
  | some i => !data i || ((row.branches.lookup (.bit false)).isNone && (row.branches.lookup (.bit true)).isNone)

def rowOK {k s : ℕ} (data : Fin k → Bool) (row : Instruction k s) : Bool :=
  probeOK data row && (row.branches.all (fun b => actionOK data b.2) &&
                       row.otherwise.toList.all (actionOK data))

def safe {k s : ℕ} (p : Table k s) (data : Fin k → Bool) : Bool :=
  p.rows.toList.all (rowOK data)

theorem lookup_mem {α β : Type} [BEq α] [LawfulBEq α] {l : List (α × β)}
    {a : α} {b : β} (h : l.lookup a=some b) : (a,b)∈l := by
  obtain ⟨x,y,e,_⟩ := List.lookup_eq_some_iff.mp h
  simp [e]

theorem expr_projection {k : ℕ} (data : Fin k → Bool) (read : Fin k → Letter)
    (i : Fin k) (e : Expr k) (h : exprOK data i e=true) :
    (value read e).map (erase (data i))=value (fun j => erase (data j) (read j)) e := by
  cases e with
  | literal a =>
    have eq : erase (data i) a=a := by simpa [exprOK] using h
    simp [value,eq]
  | copy j =>
    have eq : data i=data j := by simpa [exprOK] using h
    simp [value,eq]
  | bx j l =>
    obtain ⟨hj,hl⟩ : data i=data j ∧ data i=data l := by simpa [exprOK] using h
    simp only [value,← hj,← hl]
    generalize read j=x
    generalize read l=y
    cases data i <;> cases x <;> cases y <;> rfl

theorem selected_projection {k s : ℕ} (data : Fin k → Bool) (row : Instruction k s)
    (r : Fin k → Letter) (h : probeOK data row=true) :
    select row (fun i => erase (data i) (r i))=select row r := by
  unfold select
  cases p : row.probe with
  | none => rfl
  | some i =>
    cases td : data i with
    | false => simp [erase,td]
    | true =>
      obtain ⟨a,b⟩ : row.branches.lookup (.bit false)=none ∧ row.branches.lookup (.bit true)=none := by
        simpa [probeOK,p,td] using h
      change (row.branches.lookup (erase (data i) (r i))).orElse (fun _ => row.otherwise)=
        (row.branches.lookup (r i)).orElse (fun _ => row.otherwise)
      rw [td]
      cases u : r i with
      | bit c => cases c <;> simp [erase,a,b]
      | _ => rfl

theorem selected_safe {k s : ℕ} (data : Fin k → Bool) (row : Instruction k s)
    (r : Fin k → Letter) {a : Action k s} (h : rowOK data row=true)
    (chosen : select row r=some a) : actionOK data a=true := by
  obtain ⟨_,hs,hd⟩ := (show probeOK data row=true ∧
    (∀ x ∈ row.branches, actionOK data x.2=true) ∧
    ∀ y ∈ row.otherwise.toList, actionOK data y=true by simpa [rowOK] using h)
  have fallback (q : row.otherwise=some a) : actionOK data a=true := hd a (by simp [q])
  cases hp : row.probe with
  | none => exact fallback (by simpa [select,hp] using chosen)
  | some i =>
    cases hr : row.branches.lookup (r i) with
    | none => exact fallback (by simpa [select,hp,hr] using chosen)
    | some v =>
      have q : v=a := by simpa [select,hp,hr] using chosen
      subst a
      exact hs _ (lookup_mem hr)

theorem issue_projection {k s : ℕ} (data : Fin k → Bool) (a : Action k s) (r : Fin k → Letter)
    (h : actionOK data a=true) :
    (issue a r).map (fun z => (z.1,fun i => (erase (data i) (z.2 i).1,(z.2 i).2)))=
    issue a (fun i => erase (data i) (r i)) := by
  have ok : ∀ w ∈ a.writes, exprOK data w.1 w.2=true := by simpa [actionOK] using h
  have eq (w : Fin k × Expr k) (hw : w∈a.writes) :
      (value (fun i => erase (data i) (r i)) w.2).isSome=(value r w.2).isSome := by
    rw [← expr_projection data r _ _ (ok w hw)]
    cases value r w.2 <;> rfl
  have valid : a.writes.all (fun w => (value (fun i => erase (data i) (r i)) w.2).isSome)=
      a.writes.all (fun w => (value r w.2).isSome) := by
    apply Bool.eq_iff_iff.mpr
    simp only [List.all_eq_true]
    constructor
    · intro hp w hw
      rw [← eq w hw]
      exact hp w hw
    · intro hp w hw
      rw [eq w hw]
      exact hp w hw
  unfold issue
  rw [valid]
  split
  · rfl
  · apply congrArg some
    apply Prod.ext
    · rfl
    · funext i
      apply Prod.ext
      · change erase (data i) (((a.writes.lookup i).bind (value r)).getD (r i))=
          ((a.writes.lookup i).bind (value (fun i => erase (data i) (r i)))).getD _
        cases q : a.writes.lookup i with
        | none => rfl
        | some e =>
          change erase (data i) ((value r e).getD (r i))=
            (value (fun i => erase (data i) (r i)) e).getD _
          rw [← expr_projection data r i e (ok (i,e) (lookup_mem q))]
          cases value r e <;> rfl
      · rfl

theorem rule_projection {k s : ℕ} (p : Table k s) (data : Fin k → Bool)
    (hp : safe p data=true) (q : Fin (s+1)) (r : Fin k → Letter) :
    (rule p q r).map (fun z => (z.1,fun i => (erase (data i) (z.2 i).1,(z.2 i).2)))=
    rule p q (fun i => erase (data i) (r i)) := by
  unfold rule
  cases t : p.rows[q.val]? with
  | none => rfl
  | some row =>
    have allsafe : ∀ x∈p.rows.toList, rowOK data x=true := by simpa only [safe,List.all_eq_true] using hp
    have good := allsafe row (Array.mem_toList_iff.mpr (Array.mem_of_getElem? t))
    have probe : probeOK data row=true := (Bool.and_eq_true_iff.mp good).1
    change ((select row r).bind (fun a => issue a r)).map _ =
      (select row (fun i => erase (data i) (r i))).bind _
    rw [selected_projection data row r probe]
    cases c : select row r with
    | none => rfl
    | some a => exact issue_projection data a r (selected_safe data row r good c)

def projectTape (d : Bool) (t : TM.Tape Letter) : TM.Tape Letter :=
  ⟨t.pos,fun i => erase d (t.view i)⟩

def project {k s : ℕ} (data : Fin k → Bool)
    (c : TM.Config Letter (Fin (s+1)) (Fin k)) : TM.Config Letter (Fin (s+1)) (Fin k) :=
  ⟨c.pc,fun i => projectTape (data i) (c.tape i)⟩

private theorem project_apply (d : Bool) (t : TM.Tape Letter) (a : Letter × TM.Move) :
    projectTape d (t.apply a)=(projectTape d t).apply (erase d a.1,a.2) := by
  apply congrArg₂ TM.Tape.mk
  · rfl
  · funext i
    change erase d (if i+a.2.shift=0 then a.1 else t.view (i+a.2.shift))=
      if i+a.2.shift=0 then erase d a.1 else erase d (t.view (i+a.2.shift))
    split <;> rfl

theorem advance_projection {k s : ℕ} (p : Table k s) (data : Fin k → Bool)
    (hp : safe p data=true) (c : TM.Config Letter (Fin (s+1)) (Fin k)) :
    (TM.advance (rule p) c).map (project data)=TM.advance (rule p) (project data c) := by
  unfold TM.advance
  change ((rule p c.pc (fun i => (c.tape i).view 0)).map _).map _ =
    (rule p c.pc (fun i => erase (data i) ((c.tape i).view 0))).map _
  rw [← rule_projection p data hp]
  cases h : rule p c.pc (fun i => (c.tape i).view 0) with
  | none => rfl
  | some step =>
    rcases step with ⟨q,ops⟩
    apply congrArg some
    apply congrArg (TM.Config.mk q)
    funext i
    exact project_apply _ _ _

/-- Equal occupied layouts and metadata imply an exact lockstep run, including the
    terminal program counter and the absolute position of every individual head. -/
theorem matched {k s : ℕ} (p : Table k s) (data : Fin k → Bool) (hp : safe p data=true)
    {a b z : TM.Config Letter (Fin (s+1)) (Fin k)} {n : ℕ}
    (heq : project data a=project data b) (tr : Trace (TM.advance (rule p)) a n z) :
    ∃ w, Trace (TM.advance (rule p)) b n w ∧ project data z=project data w := by
  induction tr generalizing b with
  | nil a => exact ⟨b,.nil _,heq⟩
  | @cons x y z j hx rest ih =>
    have next := advance_projection p data hp x
    rw [hx,heq,← advance_projection p data hp b] at next
    cases hb : TM.advance (rule p) b with
    | none => rw [hb] at next; contradiction
    | some w =>
      rw [hb] at next
      obtain ⟨endw,remaining,equal⟩ := ih (Option.some.inj next)
      exact ⟨endw,.cons hb remaining,equal⟩

theorem halt_iff {k s : ℕ} (p : Table k s) (data : Fin k → Bool) (hp : safe p data=true)
    {a b : TM.Config Letter (Fin (s+1)) (Fin k)} (heq : project data a=project data b) :
    TM.advance (rule p) a=none ↔ TM.advance (rule p) b=none := by
  have eq := advance_projection p data hp a
  rw [heq,← advance_projection p data hp b] at eq
  cases ha : TM.advance (rule p) a <;> cases hb : TM.advance (rule p) b <;> simp_all

theorem visited_equal {k s : ℕ} (p : Table k s) (data : Fin k → Bool) (hp : safe p data=true)
    {a b : TM.Config Letter (Fin (s+1)) (Fin k)} (heq : project data a=project data b) (n : ℕ) :
    visitedCells (rule p) a n=visitedCells (rule p) b n := by
  have one {x y : TM.Config Letter (Fin (s+1)) (Fin k)} (eq : project data x=project data y) :
      visitedCells (rule p) x n ⊆ visitedCells (rule p) y n := by
    rintro ⟨i,h⟩ ⟨u,hu,z,hz,head⟩
    obtain ⟨w,hw,same⟩ := matched p data hp eq hz
    refine ⟨u,hu,w,hw,?_⟩
    change (z.tape i).pos=h at head
    have eread := congrArg (fun c => (c.tape i).pos) same
    exact eread.symm.trans head
  exact Set.Subset.antisymm (one heq) (one heq.symm)

def directData (i : Fin 17) : Bool := (Nat.beq i.val 0) || !(Nat.ble i.val 7)
def roleData (i : Fin 15) : Bool := decide (i.val≤1)

/-- Actual 169-state direct transpose and both actual 138-state packed role tables. -/
theorem direct_safe : safe S008.NodeTables.direct directData=true := by decide +kernel
theorem copy_safe : safe S008.NodeTables.copyRole roleData=true := by decide +kernel
theorem xor_safe : safe S008.NodeTables.xorRole roleData=true := by decide +kernel

def packData (i : Fin 9) : Bool := (Nat.beq i.val 0) || !(Nat.ble i.val 6)
def padData (i : Fin 9) : Bool := Nat.ble i.val 1

theorem pack_safe : safe S008.NodeTables.packFwd packData=true := by decide +kernel
theorem unpack_safe : safe S008.NodeTables.packBack packData=true := by decide +kernel
theorem pad_safe : safe S008.NodeTables.padFwd padData=true := by decide +kernel
theorem unpad_safe : safe S008.NodeTables.padBack padData=true := by decide +kernel
theorem range_safe : safe S008.NodeTables.rangeFwd roleData=true := by decide +kernel
theorem unrange_safe : safe S008.NodeTables.rangeBack roleData=true := by decide +kernel

end S008.DataLayout
