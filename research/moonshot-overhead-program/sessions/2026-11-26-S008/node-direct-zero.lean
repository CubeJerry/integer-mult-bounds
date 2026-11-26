import NodeTables
import Mathlib.Tactic.FinCases

/-! The actual exported 169-state native table returns the zero-width interchange
    in five physical steps on all incoming payloads and restores every tape. -/

namespace S008.NativeZero

open OAI.Computability.IntegerMultiplication OAI.Computability.NearSquareRoot
open S008.Recount (Letter)
open S008.NodeSource
open S008.NodeTables (direct)

abbrev Tape := TM.Tape Letter
abbrev Cfg := TM.Config Letter (Fin 170) (Fin 17)
abbrev Input := Fin 17 → Letter
abbrev Banks := Fin 17 → Tape

set_option maxRecDepth 20000
set_option maxHeartbeats 3000000

private theorem r168 (rd : Input) :
    rule direct 168 rd=some (167,fun i => (rd i,.left)) := by
  apply congrArg some
  apply Prod.ext
  · rfl
  · funext i
    fin_cases i <;> rfl

private theorem r167 (rd : Input) :
    rule direct 167 rd=some (166,fun _ => (.left,.right)) := by
  apply congrArg some
  apply Prod.ext
  · rfl
  · funext i
    fin_cases i <;> rfl

private theorem r166 (rd : Input) (h : rd 1=.bit false) :
    rule direct 166 rd=some (1,fun i => (rd i,.stay)) := by
  let row : Instruction 17 169 :=
      ⟨some 1,[(.bit false,⟨1,[],[]⟩),(.bit true,⟨149,[],[]⟩)],none⟩
  have hr : direct.rows[166]?=some row := rfl
  simp [rule,select,issue,hr,row,h]

private theorem r1 (rd : Input) :
    rule direct 1 rd=some (0,fun i => (rd i,.left)) := by
  apply congrArg some
  apply Prod.ext
  · rfl
  · funext i
    fin_cases i <;> rfl

private theorem r0 (rd : Input) :
    rule direct 0 rd=some (169,fun _ => (.blank,.right)) := by
  apply congrArg some
  apply Prod.ext
  · rfl
  · funext i
    fin_cases i <;> rfl

private theorem stop (t : Banks) :
    TM.advance (rule direct) (⟨169,t⟩ : Cfg)=none := by
  have hh : direct.rows[169]?=none := by
    simp [direct.width]
  simp [TM.advance,rule,hh]

private def leftView (t : Tape) : Tape := ⟨t.pos-1,fun i => t.view (i-1)⟩
private def homeMark (t : Tape) : Tape :=
  ⟨t.pos,fun i => if i=(-1 : ℤ) then .left else t.view i⟩

private theorem rewriteLeft (t : Tape) : t.apply (t.view 0,.left)=leftView t := by
  apply congrArg₂ TM.Tape.mk
  · rfl
  · funext i
    change (if i+(-1)=0 then t.view 0 else t.view (i+(-1)))=t.view (i-1)
    split <;> rename_i h
    · rw [show i-1=0 by omega]
    · rfl

private theorem keepHead (t : Tape) : t.apply (t.view 0,.stay)=t := by
  rcases t with ⟨p,f⟩
  apply congrArg₂ TM.Tape.mk
  · simp [TM.Move.shift]
  · funext i
    change (if i+0=0 then f 0 else f (i+0))=f i
    simp only [Int.add_zero]
    split <;> simp_all

private theorem installHome (t : Tape) : (leftView t).apply (.left,.right)=homeMark t := by
  apply congrArg₂ TM.Tape.mk
  · change t.pos-1+1=t.pos
    omega
  · funext i
    change (if i+1=0 then .left else t.view (i+1-1))=
          (if i=(-1 : ℤ) then .left else t.view i)
    simp only [Int.add_sub_cancel]
    by_cases h : i=(-1 : ℤ)
    · subst i
      rfl
    · simp [h,show i+1≠0 by omega]

private theorem removeHome (t : Tape) (h : t.view (-1)=.blank) :
    (leftView (homeMark t)).apply (.blank,.right)=t := by
  rcases t with ⟨p,f⟩
  apply congrArg₂ TM.Tape.mk
  · change p-1+1=p
    omega
  · funext i
    change (if i+1=0 then .blank else
      if i+1-1=(-1 : ℤ) then .left else f (i+1-1))=f i
    simp only [Int.add_sub_cancel]
    by_cases q : i=(-1 : ℤ)
    · subst i
      exact h.symm
    · simp [q,show i+1≠0 by omega]

/-- On arbitrary tapes, the zero-width interchange reads only the leading width
    digit and its one-cell left guards. Every incoming head and every absolute
    data cell are restored. The active and scratch heads jointly visit 34 cells. -/
theorem all_inputs (t : Banks) (width : (t 1).view 0=.bit false)
    (guards : ∀ i, (t i).view (-1)=.blank) :
    Trace (TM.advance (rule direct)) (⟨168,t⟩ : Cfg) 5 (⟨169,t⟩ : Cfg) ∧
    TM.advance (rule direct) (⟨169,t⟩ : Cfg)=none ∧
    VisitsAtMost (rule direct) (⟨168,t⟩ : Cfg) 5 34 := by
  let c0 : Cfg := ⟨168,t⟩
  let c1 : Cfg := ⟨167,fun i => leftView (t i)⟩
  let c2 : Cfg := ⟨166,fun i => homeMark (t i)⟩
  let c3 : Cfg := ⟨1,fun i => homeMark (t i)⟩
  let c4 : Cfg := ⟨0,fun i => leftView (homeMark (t i))⟩
  let c5 : Cfg := ⟨169,t⟩
  have s1 : TM.advance (rule direct) c0=some c1 := by
    simp [TM.advance,c0,c1,r168,rewriteLeft]
  have s2 : TM.advance (rule direct) c1=some c2 := by
    simp [TM.advance,c1,c2,r167,installHome]
  have key : (homeMark (t 1)).view 0=.bit false := by simpa [homeMark] using width
  have s3 : TM.advance (rule direct) c2=some c3 := by
    simp [TM.advance,c2,c3,r166 (fun i => (homeMark (t i)).view 0) key,keepHead]
  have s4 : TM.advance (rule direct) c3=some c4 := by
    simp [TM.advance,c3,c4,r1,rewriteLeft]
  have s5 : TM.advance (rule direct) c4=some c5 := by
    simp [TM.advance,c4,c5,r0,removeHome _ (guards _)]
  have h0 : Trace (TM.advance (rule direct)) c0 0 c0 := .nil _
  have h1 := Trace.single s1
  have h2 := h1.trans (Trace.single s2)
  have h3 := h2.trans (Trace.single s3)
  have h4 := h3.trans (Trace.single s4)
  have h5 := h4.trans (Trace.single s5)
  refine ⟨h5,stop t,?_⟩
  have cost : (∑ i : Fin 17, ((t i).pos+1-((t i).pos-1)).toNat)=34 := by simp
  rw [← cost]
  apply visitsAtMost_of_tape_fences (lo:=fun i => (t i).pos-1) (hi:=fun i => (t i).pos)
  intro u hu c hc i
  have cases := show u=0 ∨ u=1 ∨ u=2 ∨ u=3 ∨ u=4 ∨ u=5 by omega
  rcases cases with rfl|rfl|rfl|rfl|rfl|rfl
  · have e := trace_endpoint_unique hc h0
    subst c
    exact ⟨by change (t i).pos-1≤(t i).pos; omega,le_refl _⟩
  · have e := trace_endpoint_unique hc h1
    subst c
    exact ⟨le_refl _,by change (t i).pos-1≤(t i).pos; omega⟩
  · have e := trace_endpoint_unique hc h2
    subst c
    exact ⟨by change (t i).pos-1≤(t i).pos; omega,le_refl _⟩
  · have e := trace_endpoint_unique hc h3
    subst c
    exact ⟨by change (t i).pos-1≤(t i).pos; omega,le_refl _⟩
  · have e := trace_endpoint_unique hc h4
    subst c
    exact ⟨le_refl _,by change (t i).pos-1≤(t i).pos; omega⟩
  · have e := trace_endpoint_unique hc h5
    subst c
    exact ⟨by change (t i).pos-1≤(t i).pos; omega,le_refl _⟩

/-- Every one of the 34 addresses is attained, for all bank contents in the theorem. -/
theorem visited_exactly (t : Banks) (width : (t 1).view 0=.bit false)
    (guards : ∀ i, (t i).view (-1)=.blank) :
    (visitedCells (rule direct) (⟨168,t⟩ : Cfg) 5).ncard=34 := by
  apply le_antisymm ((visitsAtMost_iff_ncard _ _ _ _).mp (all_inputs t width guards).2.2)
  let point (x : Fin 17 × Bool) : Fin 17 × ℤ :=
    (x.1,if x.2 then (t x.1).pos-1 else (t x.1).pos)
  have inj : Function.Injective point := by
    rintro ⟨i,b⟩ ⟨j,c⟩ e
    have same : i=j := congrArg Prod.fst e
    subst j
    have sides := congrArg Prod.snd e
    cases b <;> cases c <;> simp [point] at sides ⊢
    all_goals omega
  have size : (Set.range point).ncard=34 := by
    rw [Set.ncard_range_of_injective inj]
    simp
  have step : TM.advance (rule direct) (⟨168,t⟩ : Cfg)=some (⟨167,fun i => leftView (t i)⟩ : Cfg) := by
    simp [TM.advance,r168,rewriteLeft]
  have inside : Set.range point ⊆ visitedCells (rule direct) (⟨168,t⟩ : Cfg) 5 := by
    rintro z ⟨⟨i,b⟩,rfl⟩
    cases b with
    | false => exact ⟨0,by decide,_,.nil _,rfl⟩
    | true => exact ⟨1,by decide,_,Trace.single step,rfl⟩
  rw [← size]
  exact Set.ncard_le_ncard inside (visitedCells_finite _ _ _)

end S008.NativeZero
