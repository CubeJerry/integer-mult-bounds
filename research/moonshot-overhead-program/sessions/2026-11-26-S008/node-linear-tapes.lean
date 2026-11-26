import NodeDataLayout

/-! All-width superposition for the actual native direct/copy/XOR tables. -/

namespace S008.LinearTapes

open OAI.Computability.IntegerMultiplication OAI.Computability.NearSquareRoot
open S008.Recount (Letter)
open S008.NodeSource
open S008.DataLayout

def blend (data : Bool) (a b : Letter) : Letter :=
  match data,a,b with
  | true,.bit x,.bit y => .bit (x != y)
  | _,a,_ => a

private def bitVal : Letter → Option Bool
  | .bit x => some x
  | _ => none

private def xorOp (a b : Letter) : Option Letter :=
  match a,b with | .bit x,.bit y => some (.bit (x != y)) | _,_ => none

private def blendOpt (data : Bool) (a b : Option Letter) : Option Letter := do
  let x ← a
  let y ← b
  return blend data x y

private theorem compatible_cases {a b : Letter} (h : erase true a=erase true b) :
    (∃ x y, a=.bit x ∧ b=.bit y) ∨ (a=b ∧ bitVal a=none) := by
  cases a <;> cases b <;> simp_all [erase,bitVal]

private theorem blend_fixed {a : Letter} (b : Letter) (h : bitVal a=none) :
    blend true a b=a := by cases a <;> simp_all [bitVal,blend]

private theorem missing_left {a : Letter} (b : Letter) (h : bitVal a=none) :
    xorOp a b=none := by cases a <;> simp_all [bitVal,xorOp]

private theorem missing_right (a : Letter) {b : Letter} (h : bitVal b=none) :
    xorOp a b=none := by cases a <;> cases b <;> simp_all [bitVal,xorOp]

private theorem xor_pair (d : Bool) (a a' b b' : Letter)
    (ha : erase d a=erase d a') (hb : erase d b=erase d b') :
    blendOpt d (xorOp a b) (xorOp a' b')=xorOp (blend d a a') (blend d b b') := by
  cases d with
  | false =>
    have h1 : a=a' := by simpa [erase] using ha
    have h2 : b=b' := by simpa [erase] using hb
    subst a'; subst b'
    cases a <;> cases b <;> rfl
  | true =>
    rcases compatible_cases ha with ⟨x,x',rfl,rfl⟩ | ⟨rfl,na⟩
    · rcases compatible_cases hb with ⟨y,y',rfl,rfl⟩ | ⟨rfl,nb⟩
      · cases x <;> cases x' <;> cases y <;> cases y' <;> rfl
      · simp [blend_fixed _ nb,missing_right _ nb,blendOpt]
    · simp [blend_fixed _ na,missing_left _ na,blendOpt]

private theorem literal_pair (d : Bool) (a : Letter) (h : erase d a=a) :
    blend d a a=a := by
  cases d <;> cases a <;> simp_all [erase,blend]

private theorem value_x {k : ℕ} (r : Fin k → Letter) (i j : Fin k) :
    value r (.bx i j)=xorOp (r i) (r j) := by
  cases x : r i <;> cases y : r j <;> simp [value,xorOp,x,y]

theorem expr_pair {k : ℕ} (data : Fin k → Bool) (a b : Fin k → Letter)
    (hread : ∀ j, erase (data j) (a j)=erase (data j) (b j))
    (i : Fin k) (e : Expr k) (ok : exprOK data i e=true) :
    blendOpt (data i) (value a e) (value b e)=
      value (fun j => blend (data j) (a j) (b j)) e := by
  cases e with
  | literal c =>
    have h : erase (data i) c=c := by simpa [exprOK] using ok
    simp [value,blendOpt,literal_pair _ _ h]
  | copy j =>
    have h : data i=data j := by simpa [exprOK] using ok
    simp [value,blendOpt,h]
  | bx j l =>
    obtain ⟨hj,hl⟩ : data i=data j ∧ data i=data l := by simpa [exprOK] using ok
    simp only [value_x]
    rw [← hj,← hl]
    exact xor_pair _ _ _ _ _ (hj.symm ▸ hread j) (hl.symm ▸ hread l)

private theorem blank_projection (d : Bool) (a b : Letter) :
    erase d (blend d a b)=erase d a := by
  cases d <;> cases a <;> cases b <;> rfl

private theorem choice_eq {k s : ℕ} (data : Fin k → Bool) (row : Instruction k s)
    (a b : Fin k → Letter) (good : probeOK data row=true)
    (h : ∀ i, erase (data i) (a i)=erase (data i) (b i)) :
    select row a=select row b ∧ select row (fun i => blend (data i) (a i) (b i))=select row a := by
  have h0 : (fun i => erase (data i) (a i))=(fun i => erase (data i) (b i)) := funext h
  have h1 : (fun i => erase (data i) (blend (data i) (a i) (b i)))=(fun i => erase (data i) (a i)) :=
    funext (fun _ => blank_projection _ _ _)
  exact ⟨(selected_projection data row a good).symm.trans ((congrArg (select row) h0).trans
             (selected_projection data row b good)),
         (selected_projection data row _ good).symm.trans ((congrArg (select row) h1).trans
             (selected_projection data row a good))⟩

private theorem issue_parts {k s : ℕ} (act : Action k s) (a : Fin k → Letter)
    {q : Fin (s+1)} {ops : Fin k → Letter × TM.Move} (h : issue act a=some (q,ops)) :
    (∀ w∈act.writes, (value a w.2).isSome=true) ∧
    q=act.target ∧ ops=(fun i => (((act.writes.lookup i).bind (value a)).getD (a i),
                                    (act.moves.lookup i).getD .stay)) := by
  unfold issue at h
  split at h
  · contradiction
  · rename_i ok
    cases h
    have yes : act.writes.all (fun w => (value a w.2).isSome)=true := by
      cases hv : act.writes.all (fun w => (value a w.2).isSome) <;> simp_all
    exact ⟨List.all_eq_true.mp yes,rfl,rfl⟩

theorem issue_pair {k s : ℕ} (data : Fin k → Bool) (act : Action k s) (ok : actionOK data act=true)
    (a b : Fin k → Letter) (h : ∀ i, erase (data i) (a i)=erase (data i) (b i))
    {q t : Fin (s+1)} {oa ob : Fin k → Letter × TM.Move}
    (ha : issue act a=some (q,oa)) (hb : issue act b=some (t,ob)) :
    q=t ∧ (∀ i, (oa i).2=(ob i).2) ∧ issue act (fun i => blend (data i) (a i) (b i)) =
      some (q,fun i => (blend (data i) (oa i).1 (ob i).1,(oa i).2)) := by
  obtain ⟨va,rfl,rfl⟩ := issue_parts act a ha
  obtain ⟨vb,rfl,rfl⟩ := issue_parts act b hb
  have shape : ∀ w ∈ act.writes, exprOK data w.1 w.2=true := by simpa [actionOK] using ok
  have valid : act.writes.all (fun w => (value (fun i => blend (data i) (a i) (b i)) w.2).isSome)=true := by
    apply List.all_eq_true.mpr
    intro w hw
    rw [← expr_pair data a b h _ _ (shape w hw)]
    cases x : value a w.2 with
    | none => have v := va w hw; simp [x] at v
    | some u =>
      cases y : value b w.2 with
      | none => have v := vb w hw; simp [y] at v
      | some v => rfl
  refine ⟨rfl,fun _ => rfl,?_⟩
  unfold issue
  rw [valid]
  apply congrArg some
  apply Prod.ext
  · rfl
  · funext i
    apply Prod.ext
    · change ((act.writes.lookup i).bind (value (fun i => blend (data i) (a i) (b i)))).getD _=
        blend (data i) (((act.writes.lookup i).bind (value a)).getD _) (((act.writes.lookup i).bind (value b)).getD _)
      cases key : act.writes.lookup i with
      | none => rfl
      | some e =>
        change (value (fun i => blend (data i) (a i) (b i)) e).getD _=
          blend (data i) ((value a e).getD _) ((value b e).getD _)
        have item := S008.DataLayout.lookup_mem key
        rw [← expr_pair data a b h i e (shape _ item)]
        cases ax : value a e with
        | none => have v := va _ item; simp [ax] at v
        | some u =>
          cases bx : value b e with
          | none => have v := vb _ item; simp [bx] at v
          | some v => rfl
    · rfl

theorem rule_pair {k s : ℕ} (p : Table k s) (data : Fin k → Bool) (safeP : safe p data=true)
    (state : Fin (s+1)) (a b : Fin k → Letter)
    (same : ∀ i, erase (data i) (a i)=erase (data i) (b i))
    {q t : Fin (s+1)} {oa ob : Fin k → Letter × TM.Move}
    (ha : rule p state a=some (q,oa)) (hb : rule p state b=some (t,ob)) :
    q=t ∧ (∀ i, (oa i).2=(ob i).2) ∧ rule p state (fun i => blend (data i) (a i) (b i)) =
      some (q,fun i => (blend (data i) (oa i).1 (ob i).1,(oa i).2)) := by
  unfold rule at ha hb ⊢
  cases hr : p.rows[state.val]? with
  | none => rw [hr] at ha; contradiction
  | some row =>
    rw [hr] at ha hb
    have valid : ∀ x∈p.rows.toList, rowOK data x=true := by simpa only [safe,List.all_eq_true] using safeP
    have ok := valid row (Array.mem_toList_iff.mpr (Array.mem_of_getElem? hr))
    obtain ⟨ab,ma⟩ := choice_eq data row a b (Bool.and_eq_true_iff.mp ok).1 same
    cases key : select row a with
    | none =>
      simp [key] at ha
    | some act =>
      have bk : select row b=some act := ab.symm.trans key
      have mk : select row (fun i => blend (data i) (a i) (b i))=some act := ma.trans key
      simp [key] at ha
      simp [bk] at hb
      simpa [mk] using issue_pair data act (selected_safe data row a ok key) a b same ha hb

def blendTape (d : Bool) (a b : TM.Tape Letter) : TM.Tape Letter :=
  ⟨a.pos,fun i => blend d (a.view i) (b.view i)⟩

def combine {k s : ℕ} (data : Fin k → Bool) (a b : TM.Config Letter (Fin (s+1)) (Fin k)) :
    TM.Config Letter (Fin (s+1)) (Fin k) := ⟨a.pc,fun i => blendTape (data i) (a.tape i) (b.tape i)⟩

private theorem blend_apply (d : Bool) (a b : TM.Tape Letter) (x y : Letter) (m : TM.Move) :
    (blendTape d a b).apply (blend d x y,m)=blendTape d (a.apply (x,m)) (b.apply (y,m)) := by
  apply congrArg₂ TM.Tape.mk
  · rfl
  · funext i
    change (if i+m.shift=0 then blend d x y else blend d (a.view (i+m.shift)) (b.view (i+m.shift)))=
      blend d (if i+m.shift=0 then x else a.view (i+m.shift)) (if i+m.shift=0 then y else b.view (i+m.shift))
    split <;> simp_all

theorem combine_step {k s : ℕ} (p : Table k s) (data : Fin k → Bool) (ok : safe p data=true)
    {a b x y : TM.Config Letter (Fin (s+1)) (Fin k)} (eq : project data a=project data b)
    (hx : TM.advance (rule p) a=some x) (hy : TM.advance (rule p) b=some y) :
    TM.advance (rule p) (combine data a b)=some (combine data x y) := by
  have pc := congrArg (fun c : TM.Config Letter (Fin (s+1)) (Fin k) => c.pc) eq.symm
  change b.pc=a.pc at pc
  have view (i : Fin k) : erase (data i) ((a.tape i).view 0)=erase (data i) ((b.tape i).view 0) :=
    congrArg (fun c => (c.tape i).view 0) eq
  unfold TM.advance at hx hy ⊢
  rw [pc] at hy
  cases ha : rule p a.pc (fun i => (a.tape i).view 0) with
  | none => rw [ha] at hx; contradiction
  | some z =>
    rcases z with ⟨q,oa⟩
    rw [ha] at hx
    cases hx
    cases hb : rule p a.pc (fun i => (b.tape i).view 0) with
    | none => rw [hb] at hy; contradiction
    | some w =>
      rcases w with ⟨t,ob⟩
      rw [hb] at hy
      cases hy
      obtain ⟨_,moves,mix⟩ := rule_pair p data ok a.pc _ _ view ha hb
      change ((rule p a.pc (fun i => blend (data i) ((a.tape i).view 0) ((b.tape i).view 0))).map _)=_
      rw [mix]
      apply congrArg some
      apply congrArg (TM.Config.mk q)
      funext i
      have e := blend_apply (data i) (a.tape i) (b.tape i) (oa i).1 (ob i).1 (oa i).2
      have pairB : ((ob i).1,(oa i).2)=ob i := Prod.ext rfl (moves i)
      exact e.trans (congrArg (fun v => blendTape (data i) ((a.tape i).apply (oa i)) ((b.tape i).apply v)) pairB)

/-- The actual fixed tables act linearly on all occupied binary data at every size.
    Metadata, marker symbols, PC and head positions have their shared common value. -/
theorem superposition {k s : ℕ} (p : Table k s) (data : Fin k → Bool) (ok : safe p data=true)
    {a b z : TM.Config Letter (Fin (s+1)) (Fin k)} {n : ℕ}
    (eq : project data a=project data b) (tr : Trace (TM.advance (rule p)) a n z) :
    ∃ w, Trace (TM.advance (rule p)) b n w ∧ project data z=project data w ∧
      Trace (TM.advance (rule p)) (combine data a b) n (combine data z w) := by
  induction tr generalizing b with
  | nil a => exact ⟨b,.nil _,eq,.nil _⟩
  | @cons x y z n hx rest ih =>
    have derived := advance_projection p data ok x
    rw [hx,eq,← advance_projection p data ok b] at derived
    cases hb : TM.advance (rule p) b with
    | none => rw [hb] at derived; contradiction
    | some w =>
      rw [hb] at derived
      obtain ⟨out,ret,same,merged⟩ := ih (Option.some.inj derived)
      exact ⟨out,.cons hb ret,same,.cons (combine_step p data ok eq hx hb) merged⟩

theorem combine_traces {k s : ℕ} (p : Table k s) (data : Fin k → Bool) (ok : safe p data=true)
    {a b x y : TM.Config Letter (Fin (s+1)) (Fin k)} {n : ℕ}
    (eq : project data a=project data b)
    (ta : Trace (TM.advance (rule p)) a n x) (tb : Trace (TM.advance (rule p)) b n y) :
    Trace (TM.advance (rule p)) (combine data a b) n (combine data x y) := by
  obtain ⟨w,tw,_,sum⟩ := superposition p data ok eq ta
  have he := trace_endpoint_unique tw tb
  exact he ▸ sum

/-- At any finite occupied geometry, exact original traces on the zero word and all
    singleton inputs certify the prescribed linear output map on every bit word. -/
theorem basis_suffices {k s v : ℕ} (p : Table k s) (data : Fin k → Bool) (ok : safe p data=true)
    (load out : (Fin v → Bool) → TM.Config Letter (Fin (s+1)) (Fin k)) (clock : ℕ)
    (common : ∀ a b, project data (load a)=project data (load b))
    (loadAdd : ∀ a b, combine data (load a) (load b)=load (fun i => a i != b i))
    (outAdd : ∀ a b, combine data (out a) (out b)=out (fun i => a i != b i))
    (zero : Trace (TM.advance (rule p)) (load (fun _ => false)) clock (out (fun _ => false)))
    (units : ∀ j : Fin v, Trace (TM.advance (rule p)) (load (fun i => decide (i=j))) clock
                                            (out (fun i => decide (i=j))))
    (mask : Fin v → Bool) : Trace (TM.advance (rule p)) (load mask) clock (out mask) := by
  let part := fun (j : ℕ) (i : Fin v) => if i.val<j then mask i else false
  have all (j : ℕ) (hj : j≤v) : Trace (TM.advance (rule p)) (load (part j)) clock (out (part j)) := by
    induction j with
    | zero => simpa [part] using zero
    | succ j ih =>
      have lt : j<v := by omega
      let a : Fin v := ⟨j,lt⟩
      have prior := ih (by omega)
      cases selected : mask a with
      | false =>
        have unchanged : part (j+1)=part j := by
          funext i
          by_cases same : i=a
          · subst i; simp [part,a] at selected ⊢; exact selected
          · have diff : i.val≠j := fun h => same (Fin.ext h)
            have equal : i.val<j+1 ↔ i.val<j := by omega
            simp [part,equal]
        rw [unchanged]
        exact prior
      | true =>
        have updated : part (j+1)=(fun i => part j i != decide (i=a)) := by
          funext i
          by_cases same : i=a
          · subst i; simp [part,a] at selected ⊢; exact selected
          · have diff : i.val≠j := fun h => same (Fin.ext h)
            have equal : i.val<j+1 ↔ i.val<j := by omega
            simp [part,equal,same]
        rw [updated,← loadAdd,← outAdd]
        exact combine_traces p data ok (common _ _) prior (units a)
  have done : part v=mask := by
    funext i
    simp [part,i.isLt]
  simpa [done] using all v (by omega)

end S008.LinearTapes
