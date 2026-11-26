import NodeLinearTapes
import WidthDispatch

/-! An extra unit coordinate homogenizes the signed tag programs, which append
    constant data digits. Setting it to one realizes the original physical rule. -/

namespace S008.AffineTags

open OAI.Computability.IntegerMultiplication OAI.Computability.NearSquareRoot
open S008.Recount (Letter)
open S008.NodeSource
open S008.DataLayout
open S008.LinearTapes

def liftExpr {k : ℕ} (data : Fin k → Bool) (dst : Fin k) : Expr k → Expr (k+1)
  | .literal (.bit true) => if data dst then .copy 0 else .literal (.bit true)
  | .literal x => .literal x
  | .copy i => .copy i.succ
  | .bx i j => .bx i.succ j.succ

def liftAction {k s : ℕ} (data : Fin k → Bool) (a : Action k s) : Action (k+1) s :=
  ⟨a.target,a.writes.map (fun w => (w.1.succ,liftExpr data w.1 w.2)),
    a.moves.map (fun w => (w.1.succ,w.2))⟩

def liftRow {k s : ℕ} (data : Fin k → Bool) (r : Instruction k s) : Instruction (k+1) s :=
  ⟨r.probe.map Fin.succ,r.branches.map (fun t => (t.1,liftAction data t.2)),r.otherwise.map (liftAction data)⟩

def lifted {k s : ℕ} (p : Table k s) (data : Fin k → Bool) : Table (k+1) s :=
  ⟨p.rows.map (liftRow data),by simp [p.width]⟩

def liftRead {k : ℕ} (r : Fin k → Letter) : Fin (k+1) → Letter := Fin.cases (.bit true) r

def liftOps {k : ℕ} (r : Fin k → Letter × TM.Move) : Fin (k+1) → Letter × TM.Move :=
  Fin.cases (.bit true,.stay) r

private theorem lookup_succ {k : ℕ} {α β : Type} (f : Fin k → α → β)
    (l : List (Fin k × α)) (i : Fin k) :
    (l.map (fun w => (w.1.succ,f w.1 w.2))).lookup i.succ=(l.lookup i).map (f i) := by
  induction l with
  | nil => rfl
  | cons w l ih =>
    rcases w with ⟨j,a⟩
    by_cases h : i=j
    · subst j
      simp
    · have hij : (i==j)=false := by simpa only [beq_eq_false_iff_ne] using h
      have hsucc : (i.succ==j.succ)=false := beq_eq_false_iff_ne.mpr (fun eq => h (Fin.succ_inj.mp eq))
      simp [List.lookup_cons,hij,hsucc,ih]

private theorem lookup_zero {k : ℕ} {α β : Type} (f : Fin k → α → β)
    (l : List (Fin k × α)) :
    (l.map (fun w => (w.1.succ,f w.1 w.2))).lookup (0 : Fin (k+1))=none := by
  induction l with
  | nil => rfl
  | cons w l ih =>
    rcases w with ⟨j,a⟩
    have never : ((0 : Fin (k+1))==j.succ)=false := by simp only [beq_eq_false_iff_ne]; exact (Fin.succ_ne_zero j).symm
    simp [List.lookup_cons,never,ih]

private theorem lookup_map_values {key α β : Type} [BEq key] (f : α → β)
    (l : List (key × α)) (i : key) :
    (l.map (fun w => (w.1,f w.2))).lookup i=(l.lookup i).map f := by
  induction l with
  | nil => rfl
  | cons w l ih =>
    rcases w with ⟨j,a⟩
    cases h : i==j <;> simp [List.lookup_cons,h,ih]

theorem value_lift {k : ℕ} (data : Fin k → Bool) (r : Fin k → Letter) (i : Fin k) (e : Expr k) :
    value (liftRead r) (liftExpr data i e)=value r e := by
  cases e with
  | literal a =>
    cases a with
    | bit b => cases b <;> cases h : data i <;> simp [value,liftExpr,liftRead,h]
    | _ => rfl
  | copy j => rfl
  | bx j l => rfl

theorem select_lift {k s : ℕ} (data : Fin k → Bool) (row : Instruction k s) (r : Fin k → Letter) :
    select (liftRow data row) (liftRead r)=(select row r).map (liftAction data) := by
  cases hp : row.probe with
  | none => simp [select,liftRow,hp]
  | some i =>
    simp only [select,liftRow,hp,Option.map_some,Fin.cases_succ,liftRead]
    rw [lookup_map_values]
    cases h : row.branches.lookup (r i) <;> rfl

theorem issue_lift {k s : ℕ} (data : Fin k → Bool) (a : Action k s) (r : Fin k → Letter) :
    issue (liftAction data a) (liftRead r)=(issue a r).map (fun z => (z.1,liftOps z.2)) := by
  have ok : (liftAction data a).writes.all (fun w => (value (liftRead r) w.2).isSome)=
         a.writes.all (fun w => (value r w.2).isSome) := by
    simp [liftAction,Function.comp_def,value_lift]
  unfold issue
  rw [ok]
  split
  · rfl
  · apply congrArg some
    apply Prod.ext
    · rfl
    · funext i
      refine Fin.cases ?_ (fun j => ?_) i
      · have movesZero := lookup_zero (fun (_ : Fin k) (m : TM.Move) => m) a.moves
        simp [liftAction,lookup_zero,liftOps,liftRead,movesZero]
      · simp only [liftAction,liftOps,Fin.cases_succ]
        have movesSucc : (a.moves.map (fun w => (w.1.succ,w.2))).lookup j.succ=a.moves.lookup j := by
          simpa using lookup_succ (fun (_ : Fin k) (m : TM.Move) => m) a.moves j
        rw [lookup_succ,movesSucc]
        cases h : a.writes.lookup j with
        | none => simp [liftRead]
        | some e => simp [value_lift,liftRead]

theorem rule_lift {k s : ℕ} (p : Table k s) (data : Fin k → Bool) (pc : Fin (s+1)) (r : Fin k → Letter) :
    rule (lifted p data) pc (liftRead r)=(rule p pc r).map (fun z => (z.1,liftOps z.2)) := by
  unfold rule
  simp only [lifted,Array.getElem?_map]
  cases h : p.rows[pc.val]? with
  | none => rfl
  | some row =>
    change (select (liftRow data row) (liftRead r)).bind _=((select row r).bind _).map _
    rw [select_lift]
    cases a : select row r with
    | none => rfl
    | some act => exact issue_lift data act r

def unitTape (b : Bool) : TM.Tape Letter := TM.Tape.loaded .blank [.bit b]
def extend {k s : ℕ} (b : Bool) (c : TM.Config Letter (Fin (s+1)) (Fin k)) :
    TM.Config Letter (Fin (s+1)) (Fin (k+1)) := ⟨c.pc,Fin.cases (unitTape b) c.tape⟩

theorem advance_unit {k s : ℕ} (p : Table k s) (data : Fin k → Bool)
    (c : TM.Config Letter (Fin (s+1)) (Fin k)) :
    TM.advance (rule (lifted p data)) (extend true c)=(TM.advance (rule p) c).map (extend true) := by
  have reads : (fun i => ((extend true c).tape i).view 0)=liftRead (fun i => (c.tape i).view 0) := by
    funext i
    exact Fin.cases rfl (fun _ => rfl) i
  unfold TM.advance
  rw [reads]
  change (rule (lifted p data) c.pc _).map _=_
  rw [rule_lift]
  cases h : rule p c.pc (fun i => (c.tape i).view 0) with
  | none => rfl
  | some z =>
    rcases z with ⟨q,f⟩
    apply congrArg some
    apply congrArg (TM.Config.mk q)
    funext i
    refine Fin.cases ?_ (fun _ => rfl) i
    exact S008.WidthDispatch.same_stay (unitTape true)

theorem trace_unit {k s : ℕ} (p : Table k s) (data : Fin k → Bool)
    {a z : TM.Config Letter (Fin (s+1)) (Fin k)} {n : ℕ} (tr : Trace (TM.advance (rule p)) a n z) :
    Trace (TM.advance (rule (lifted p data))) (extend true a) n (extend true z) := by
  induction tr with
  | nil a => exact .nil _
  | @cons x y z n hx _ ih =>
    have eq := advance_unit p data x
    rw [hx] at eq
    exact .cons eq ih

theorem trace_extract {k s : ℕ} (p : Table k s) (data : Fin k → Bool)
    {a : TM.Config Letter (Fin (s+1)) (Fin k)} {z : TM.Config Letter (Fin (s+1)) (Fin (k+1))} {n : ℕ}
    (tr : Trace (TM.advance (rule (lifted p data))) (extend true a) n z) :
    ∃ w, Trace (TM.advance (rule p)) a n w ∧ z=extend true w := by
  generalize base : extend true a=x at tr
  induction tr generalizing a with
  | nil x =>
    subst x
    exact ⟨a,.nil _,rfl⟩
  | @cons x y z n hx rest ih =>
    subst x
    rw [advance_unit] at hx
    cases ha : TM.advance (rule p) a with
    | none => rw [ha] at hx; contradiction
    | some w =>
      rw [ha] at hx
      have same : extend true w=y := Option.some.inj hx
      obtain ⟨v,t,f⟩ := ih same
      exact ⟨v,.cons ha t,f⟩

def tagData : Fin 11 → Bool := fun i => Nat.ble i.val 1
def withUnit {k : ℕ} (data : Fin k → Bool) : Fin (k+1) → Bool := Fin.cases true data

theorem plus_tag_safe : safe (lifted S008.NodeTables.tagFwd tagData) (withUnit tagData)=true := by decide +kernel
theorem minus_tag_safe : safe (lifted S008.NodeTables.tagBack tagData) (withUnit tagData)=true := by decide +kernel

private theorem project_unit (b : Bool) : projectTape true (unitTape b)=unitTape false := by
  apply congrArg₂ TM.Tape.mk
  · rfl
  · funext i
    cases i with
    | ofNat n => cases n <;> rfl
    | negSucc n => rfl

theorem project_extend {k s : ℕ} (data : Fin k → Bool) (b : Bool)
    (c : TM.Config Letter (Fin (s+1)) (Fin k)) :
    project (withUnit data) (extend b c)=extend false (project data c) := by
  apply congrArg (TM.Config.mk c.pc)
  funext i
  exact Fin.cases (project_unit b) (fun _ => rfl) i

private theorem blend_unit (b c : Bool) :
    blendTape true (unitTape b) (unitTape c)=unitTape (b != c) := by
  apply congrArg₂ TM.Tape.mk
  · rfl
  · funext i
    cases i with
    | ofNat n => cases n <;> rfl
    | negSucc n => rfl

theorem combine_extend {k s : ℕ} (data : Fin k → Bool) (b c : Bool)
    (x y : TM.Config Letter (Fin (s+1)) (Fin k)) :
    combine (withUnit data) (extend b x) (extend c y)=extend (b != c) (combine data x y) := by
  apply congrArg (TM.Config.mk x.pc)
  funext i
  exact Fin.cases (blend_unit b c) (fun _ => rfl) i

theorem project_combine {k s : ℕ} (data : Fin k → Bool)
    (a b : TM.Config Letter (Fin (s+1)) (Fin k)) : project data (combine data a b)=project data a := by
  apply congrArg (TM.Config.mk a.pc)
  funext i
  apply congrArg₂ TM.Tape.mk
  · rfl
  · funext j
    change erase (data i) (blend (data i) ((a.tape i).view j) ((b.tape i).view j))=erase (data i) ((a.tape i).view j)
    generalize (a.tape i).view j=x
    generalize (b.tape i).view j=y
    cases data i <;> cases x <;> cases y <;> rfl

theorem extend_injective {k s : ℕ} (u : Bool) : Function.Injective (@extend k s u) := by
  intro a b h
  have trim := congrArg (fun (v : TM.Config Letter (Fin (s+1)) (Fin (k+1))) =>
        (⟨v.pc,fun i : Fin k => v.tape i.succ⟩ : TM.Config Letter (Fin (s+1)) (Fin k))) h
  exact trim

/-- Unconditional lockstep on the original k physical tapes of an affine program. -/
theorem matched_original {k s : ℕ} (p : Table k s) (data : Fin k → Bool)
    (ok : safe (lifted p data) (withUnit data)=true)
    {a b z : TM.Config Letter (Fin (s+1)) (Fin k)} {n : ℕ}
    (eq : project data a=project data b) (tr : Trace (TM.advance (rule p)) a n z) :
    ∃ w, Trace (TM.advance (rule p)) b n w ∧ project data z=project data w := by
  have eq' : project (withUnit data) (extend true a)=project (withUnit data) (extend true b) := by
    rw [project_extend,project_extend,eq]
  obtain ⟨w,tw,endEq⟩ := matched _ _ ok eq' (trace_unit p data tr)
  obtain ⟨y,ty,h⟩ := trace_extract p data tw
  subst w
  rw [project_extend,project_extend] at endEq
  exact ⟨y,ty,extend_injective false endEq⟩

/-- Three-way XOR preserves both zero and one constants. Specializing to an all-zero
    third payload gives the ordinary XOR of two results plus the fixed affine bias. -/
theorem affine_three {k s : ℕ} (p : Table k s) (data : Fin k → Bool)
    (ok : safe (lifted p data) (withUnit data)=true)
    {a b c x y z : TM.Config Letter (Fin (s+1)) (Fin k)} {n : ℕ}
    (ab : project data a=project data b) (ac : project data a=project data c)
    (ta : Trace (TM.advance (rule p)) a n x) (tb : Trace (TM.advance (rule p)) b n y)
    (tc : Trace (TM.advance (rule p)) c n z) :
    Trace (TM.advance (rule p)) (combine data (combine data a b) c) n (combine data (combine data x y) z) := by
  have eab : project (withUnit data) (extend true a)=project (withUnit data) (extend true b) := by
    rw [project_extend,project_extend,ab]
  have t0 := combine_traces _ _ ok eab (trace_unit p data ta) (trace_unit p data tb)
  simp only [combine_extend] at t0
  have eac : project (withUnit data) (extend false (combine data a b))=
        project (withUnit data) (extend true c) := by
    rw [project_extend,project_extend,project_combine,ac]
  have t1 := combine_traces _ _ ok eac t0 (trace_unit p data tc)
  simp only [combine_extend] at t1
  obtain ⟨w,tw,h⟩ := trace_extract p data t1
  have final := extend_injective true h
  exact final ▸ tw

theorem affine_halt {k s : ℕ} (p : Table k s) (data : Fin k → Bool)
    (ok : safe (lifted p data) (withUnit data)=true)
    {a b : TM.Config Letter (Fin (s+1)) (Fin k)} (eq : project data a=project data b) :
    TM.advance (rule p) a=none ↔ TM.advance (rule p) b=none := by
  have eq' : project (withUnit data) (extend true a)=project (withUnit data) (extend true b) := by
    rw [project_extend,project_extend,eq]
  have h := halt_iff (lifted p data) (withUnit data) ok eq'
  simpa [advance_unit] using h

theorem affine_visited {k s : ℕ} (p : Table k s) (data : Fin k → Bool)
    (ok : safe (lifted p data) (withUnit data)=true)
    {a b : TM.Config Letter (Fin (s+1)) (Fin k)} (eq : project data a=project data b) (n : ℕ) :
    visitedCells (rule p) a n=visitedCells (rule p) b n := by
  have one {x y : TM.Config Letter (Fin (s+1)) (Fin k)} (hxy : project data x=project data y) :
      visitedCells (rule p) x n ⊆ visitedCells (rule p) y n := by
    rintro ⟨i,u⟩ ⟨j,hj,z,hz,hp⟩
    obtain ⟨w,hw,same⟩ := matched_original p data ok hxy hz
    refine ⟨j,hj,w,hw,?_⟩
    change (z.tape i).pos=u at hp
    have e := congrArg (fun c => (c.tape i).pos) same
    exact e.symm.trans hp
  exact Set.Subset.antisymm (one eq) (one eq.symm)

end S008.AffineTags
