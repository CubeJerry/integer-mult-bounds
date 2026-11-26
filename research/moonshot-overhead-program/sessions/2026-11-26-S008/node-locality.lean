import NodeExactCells

/-! Install an audited finite-table trace in arbitrary occupied tape context. -/

namespace S008.Locality

open OAI.Computability.IntegerMultiplication OAI.Computability.NearSquareRoot
open S008.Recount (Letter)
open S008.NodeSource

variable {A Q I : Type}

/-- Replace every cell outside the indicated interval by ambient tape data. -/
def overlayTape (lo hi : ℤ) (outside : ℤ → A) (t : TM.Tape A) : TM.Tape A :=
  ⟨t.pos,fun u => if lo≤t.pos+u ∧ t.pos+u≤hi then t.view u else outside (t.pos+u)⟩

def install (lo hi : I → ℤ) (ctx : I → ℤ → A) (c : TM.Config A Q I) : TM.Config A Q I :=
  ⟨c.pc,fun i => overlayTape (lo i) (hi i) (ctx i) (c.tape i)⟩

theorem overlay_apply {lo hi : ℤ} (ext : ℤ → A) (t : TM.Tape A)
    (u : A × TM.Move) (h : lo≤t.pos ∧ t.pos≤hi) :
    (overlayTape lo hi ext t).apply u=overlayTape lo hi ext (t.apply u) := by
  rcases u with ⟨sym,m⟩
  apply congrArg₂ TM.Tape.mk
  · rfl
  · funext i
    change (if i+m.shift=0 then sym else
          if lo≤t.pos+(i+m.shift) ∧ t.pos+(i+m.shift)≤hi then t.view (i+m.shift)
          else ext (t.pos+(i+m.shift)))=
        (if lo≤t.pos+m.shift+i ∧ t.pos+m.shift+i≤hi then
          (if i+m.shift=0 then sym else t.view (i+m.shift)) else ext (t.pos+m.shift+i))
    rw [show t.pos+m.shift+i=t.pos+(i+m.shift) by omega]
    by_cases e : i+m.shift=0
    · simp [e,h]
    · simp [e]

theorem installed_advance (m : TM.Rule A Q I) (lo hi : I → ℤ) (ext : I → ℤ → A)
    (c : TM.Config A Q I) (head : ∀ i, lo i≤(c.tape i).pos ∧ (c.tape i).pos≤hi i) :
    TM.advance m (install lo hi ext c)=(TM.advance m c).map (install lo hi ext) := by
  have read : (fun i => ((install lo hi ext c).tape i).view 0)=(fun i => (c.tape i).view 0) := by
    funext i
    simp [install,overlayTape,head i]
  unfold TM.advance
  rw [read]
  change ((m c.pc _).map _) = _
  cases q : m c.pc (fun i => (c.tape i).view 0) with
  | none => rfl
  | some act =>
    rcases act with ⟨pc,u⟩
    apply congrArg some
    apply congrArg (TM.Config.mk pc)
    funext i
    exact overlay_apply _ _ _ (head i)

def within (m : TM.Rule A Q I) (c : TM.Config A Q I) (n : ℕ) (lo hi : I → ℤ) : Prop :=
  ∀ u≤n, ∀ w, Trace (TM.advance m) c u w → ∀ i, lo i≤(w.tape i).pos ∧ (w.tape i).pos≤hi i

theorem installed_trace (m : TM.Rule A Q I) (lo hi : I → ℤ) (ext : I → ℤ → A)
    {c d : TM.Config A Q I} {n : ℕ} (tr : Trace (TM.advance m) c n d)
    (bounds : within m c n lo hi) :
    Trace (TM.advance m) (install lo hi ext c) n (install lo hi ext d) := by
  induction tr with
  | nil c => exact .nil _
  | @cons x w z n h rest ih =>
    have first := installed_advance m lo hi ext x (bounds 0 (by omega) x (.nil _))
    rw [h] at first
    apply Trace.cons first
    apply ih
    intro u hu d hd i
    exact bounds (1+u) (by omega) d (.cons h hd) i

theorem prefix_exists {X : Type} {f : X → Option X} {c d : X} {n u : ℕ}
    (tr : Trace f c n d) (hu : u≤n) : ∃ w, Trace f c u w := by
  induction tr generalizing u with
  | nil c =>
    have eq : u=0 := by omega
    subst u
    exact ⟨c,.nil _⟩
  | @cons x w z k hx tail ih =>
    cases u with
    | zero => exact ⟨x,.nil _⟩
    | succ v =>
      obtain ⟨e,hv⟩ := ih (u:=v) (by omega)
      exact ⟨e,by simpa [Nat.add_comm] using Trace.cons hx hv⟩

theorem installed_visited (m : TM.Rule A Q I) (lo hi : I → ℤ) (ext : I → ℤ → A)
    {c d : TM.Config A Q I} {n : ℕ} (tr : Trace (TM.advance m) c n d)
    (bounds : within m c n lo hi) :
    visitedCells m (install lo hi ext c) n=visitedCells m c n := by
  ext ⟨i,z⟩
  constructor
  · rintro ⟨u,hu,e,he,atpos⟩
    obtain ⟨w,hw⟩ := prefix_exists tr hu
    have tight : within m c u lo hi := fun j hj => bounds j (le_trans hj hu)
    have eq := trace_endpoint_unique he (installed_trace m lo hi ext hw tight)
    subst e
    exact ⟨u,hu,w,hw,atpos⟩
  · rintro ⟨u,hu,e,he,atpos⟩
    have tight : within m c u lo hi := fun j hj => bounds j (le_trans hj hu)
    exact ⟨u,hu,install lo hi ext e,installed_trace m lo hi ext he tight,atpos⟩

/-- Shift a head and its entire local tape independently on each physical bank. -/
def rebase (offset : I → ℤ) (c : TM.Config A Q I) : TM.Config A Q I :=
  ⟨c.pc,fun i => ⟨(c.tape i).pos+offset i,(c.tape i).view⟩⟩

theorem rebase_advance (m : TM.Rule A Q I) (offset : I → ℤ) (c : TM.Config A Q I) :
    TM.advance m (rebase offset c)=(TM.advance m c).map (rebase offset) := by
  unfold TM.advance
  change (m c.pc (fun i => (c.tape i).view 0)).map _ = _
  cases h : m c.pc (fun i => (c.tape i).view 0) with
  | none => rfl
  | some act =>
    rcases act with ⟨q,f⟩
    apply congrArg some
    apply congrArg (TM.Config.mk q)
    funext i
    apply congrArg₂ TM.Tape.mk
    · change (c.tape i).pos+offset i+(f i).2.shift=(c.tape i).pos+(f i).2.shift+offset i
      omega
    · rfl

theorem rebase_trace (m : TM.Rule A Q I) (offset : I → ℤ) {c d : TM.Config A Q I} {n : ℕ}
    (tr : Trace (TM.advance m) c n d) :
    Trace (TM.advance m) (rebase offset c) n (rebase offset d) := by
  induction tr with
  | nil c => exact .nil _
  | @cons x y z k hx _ ih =>
    have e := rebase_advance m offset x
    rw [hx] at e
    exact .cons e ih

theorem rebase_visited (m : TM.Rule A Q I) (offset : I → ℤ)
    {c d : TM.Config A Q I} {n : ℕ} (tr : Trace (TM.advance m) c n d) (i : I) (z : ℤ) :
    (i,z+offset i)∈visitedCells m (rebase offset c) n ↔ (i,z)∈visitedCells m c n := by
  constructor
  · rintro ⟨u,hu,e,he,atpos⟩
    obtain ⟨w,hw⟩ := prefix_exists tr hu
    have eq := trace_endpoint_unique he (rebase_trace m offset hw)
    subst e
    refine ⟨u,hu,w,hw,?_⟩
    change (w.tape i).pos+offset i=z+offset i at atpos
    exact add_right_cancel atpos
  · rintro ⟨u,hu,e,he,atpos⟩
    refine ⟨u,hu,rebase offset e,rebase_trace m offset he,?_⟩
    change (e.tape i).pos=z at atpos
    change (e.tape i).pos+offset i=z+offset i
    rw [atpos]

/-- A checked raw bank run can be embedded at arbitrary physical offsets with all
    data beyond each exact visited interval supplied freely by its caller. -/
theorem install_checked {k s : ℕ} (p : Table k s) {r d : Runtime k s} {n : ℕ}
    (hr : S008.ExactCells.precise r) (h : run p r n=some d) (halt : d.pc.val=s)
    (ctx : Fin k → ℤ → Letter) (offset : Fin k → ℤ) :
    let placed := fun c => rebase offset (install (fun i => d.low[i]) (fun i => d.high[i]) ctx c)
    Trace (TM.advance (rule p)) (placed (physical r)) n (placed (physical d)) ∧
    TM.advance (rule p) (placed (physical d))=none ∧
    ∀ i z, (i,z+offset i)∈visitedCells (rule p) (placed (physical r)) n ↔
      d.low[i]≤z ∧ z≤d.high[i] := by
  let lo := fun i : Fin k => d.low[i]
  let hi := fun i : Fin k => d.high[i]
  have bnd : within (rule p) (physical r) n lo hi := by
    intro u hu w hw i
    exact (S008.ExactCells.visited_iff p h hr i _).mp ⟨u,hu,w,hw,rfl⟩
  have t := installed_trace (rule p) lo hi ctx (sound p h) bnd
  have e := installed_advance (rule p) lo hi ctx (physical d) (bnd n le_rfl _ (sound p h))
  rw [halt_sound p d halt] at e
  have stop := rebase_advance (rule p) offset (install lo hi ctx (physical d))
  rw [e] at stop
  refine ⟨rebase_trace (rule p) offset t,stop,?_⟩
  intro i z
  rw [rebase_visited (rule p) offset t,installed_visited (rule p) lo hi ctx (sound p h) bnd]
  exact S008.ExactCells.visited_iff p h hr i z

end S008.Locality
