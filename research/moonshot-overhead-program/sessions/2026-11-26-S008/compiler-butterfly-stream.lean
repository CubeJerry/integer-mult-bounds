import «compiler-butterfly»
import «compiler-binary-space»

/-! Run the certified modular butterfly on a complete stream of paired records. -/

namespace S008.Compiler.ButterflyStream

open OAI.Computability.IntegerMultiplication
open Butterfly (Words Banks Origins Port)

inductive Stage where
  | dispatch | call (part : Butterfly.Stage) | skip | marker | rewind | origin | done
  deriving DecidableEq, Repr

def stages : List Stage := [.dispatch,.skip,.marker,.rewind,.origin,.done] ++
  ((Butterfly.flagsList.map Butterfly.Stage.forward ++
    ([.returning false false,.returning false true,.returning true false,.returning true true,.halt] : List Butterfly.Stage)).map .call)

instance : Fintype Stage := Fintype.ofList stages (by
  intro s
  cases s with
  | call q =>
    cases q with
    | forward f =>
      rcases f with ⟨a,b,c,d⟩
      cases a <;> cases b <;> cases c <;> cases d <;> decide
    | returning a b => cases a <;> cases b <;> decide
    | halt => decide
  | _ => decide)

def stepMove (m : TM.Move) : Port → TM.Move
  | .m => .stay
  | _ => m

def travel (r : Port → Letter) (m : TM.Move) : Port → Letter × TM.Move := fun t => (r t,stepMove m t)

def rule : TM.Rule Letter Stage Port := fun q r =>
  match q with
  | .dispatch => match r .a with
    | .bit _ | .delimiter => some (.call (.forward ⟨false,false,false,false⟩), travel r .stay)
    | .count => some (.rewind,travel r .left)
    | _ => none
  | .call k => match Butterfly.rule k r with
    | some (j,op) => some (.call j,op)
    | none => match k with
      | .halt => some (.skip,travel r .stay)
      | _ => none
  | .skip => match r .a with
    | .bit _ => some (.skip,travel r .right)
    | .delimiter => some (.marker,travel r .right)
    | _ => none
  | .marker => match r .a with
    | .home => some (.dispatch,travel r .right)
    | _ => none
  | .rewind => match r .a with
    | .count => some (.origin,travel r .right)
    | _ => some (.rewind,travel r .left)
  | .origin => some (.done,travel r .right)
  | .done => none

def embed (C : TM.Config Letter Butterfly.Stage Port) : TM.Config Letter Stage Port := ⟨.call C.pc,C.tape⟩

private theorem lift_step {C D : TM.Config Letter Butterfly.Stage Port}
    (row : TM.advance Butterfly.rule C=some D) : TM.advance rule (embed C)=some (embed D) := by
  unfold TM.advance at row ⊢
  change (match Butterfly.rule C.pc (fun t => (C.tape t).view 0) with
    | some (j,op) => some (Stage.call j,op)
    | none => match C.pc with | .halt => some (.skip,travel (fun t => (C.tape t).view 0) .stay) | _ => none).map _ = _
  cases eq : Butterfly.rule C.pc (fun t => (C.tape t).view 0) with
  | none => simp [eq] at row
  | some result =>
    rcases result with ⟨q,op⟩
    simp only [eq,Option.map_some,Option.some.injEq] at row
    subst D
    rfl

theorem lift {C D steps} (row : Trace (TM.advance Butterfly.rule) C steps D) :
    Trace (TM.advance rule) (embed C) steps (embed D) := by
  induction row with
  | nil => exact .nil _
  | cons h _ rest => exact .cons (lift_step h) rest

def heads (o : Origins) (x : ℤ) : Origins
  | .m => o .m
  | t => o t+x

def pos (w j : ℕ) : ℤ := j*(w+2:ℕ)

def config (q : Stage) (raw : Banks) (o : Origins) (x : ℤ) : TM.Config Letter Stage Port :=
  ⟨q,fun t => atPos (raw t) (heads o x t)⟩

private theorem read_at (a : ℤ → Letter) (p : ℤ) : (atPos a p).view 0 = a p := by simp [atPos]

private theorem move_at (a : ℤ → Letter) (p : ℤ) (m : TM.Move) :
    (atPos a p).apply (a p,m) = atPos a (p+m.shift) := by
  unfold atPos TM.Tape.apply
  congr 1
  funext i
  by_cases e : i+m.shift=0
  · simp only [e,ite_true]
    congr 1
    omega
  · simp only [e,ite_false]
    congr 1
    omega

theorem moving (q q' : Stage) (d o) (x : ℤ) (m : TM.Move)
    (step : rule q (fun t => d t (heads o x t)) = some (q',travel (fun t => d t (heads o x t)) m)) :
    TM.advance rule (config q d o x) = some (config q' d o (x+m.shift)) := by
  unfold TM.advance config
  simp only [read_at,step,Option.map_some,Option.some.injEq]
  apply congrArg (TM.Config.mk q')
  funext t
  simp only [travel,move_at]
  cases t <;> simp [heads,stepMove,TM.Move.shift,add_assoc]

structure Valid (s : ℕ → Words) (n w : ℕ) (raw : Banks) (o : Origins) : Prop where
  row : ∀ j, j<n → Butterfly.Valid (s j) w raw (heads o (pos w j))
  gap : ∀ j, j<n → raw .a (o .a+pos w j+w+1) = .home
  entryHome : raw .a (o .a-1) = .home
  start : raw .a (o .a-2) = .count
  finish : raw .a (o .a+pos w n) = .count

def after (s : ℕ → Words) (raw : Banks) (o : Origins) (w : ℕ) : ℕ → Banks
  | 0 => raw
  | j+1 => Butterfly.output (s j) (after s raw o w j) (heads o (pos w j)) w

theorem sources (s raw o w j) :
    after s raw o w j .a=raw .a ∧ after s raw o w j .b=raw .b ∧ after s raw o w j .m=raw .m := by
  induction j with
  | zero => exact ⟨rfl,rfl,rfl⟩
  | succ j ih =>
    have h := Butterfly.retained (s j) (after s raw o w j) (heads o (pos w j)) w
    exact ⟨h.1.trans ih.1,h.2.1.trans ih.2.1,h.2.2.trans ih.2.2⟩

theorem valid_current (s raw o n w j) (good : Valid s n w raw o) (hj : j<n) :
    Butterfly.Valid (s j) w (after s raw o w j) (heads o (pos w j)) := by
  have r := good.row j hj
  have h := sources s raw o w j
  exact ⟨by simpa only [h.1] using r.home,by simpa only [h.1] using r.endA,
    by simpa only [h.2.1] using r.endB,by simpa only [h.2.2] using r.endM,
    fun i hi => by simpa only [h.1] using r.bitA i hi,
    fun i hi => by simpa only [h.2.1] using r.bitB i hi,
    fun i hi => by simpa only [h.2.2] using r.bitM i hi⟩

theorem at_origin (q : Butterfly.Stage) (d o x) :
    embed (Butterfly.frame q d (heads o x) 0) = config (.call q) d o x := by simp [embed,Butterfly.frame,config]

theorem block_start (s raw o n w j) (good : Valid s n w raw o) (hj : j<n) :
    TM.advance rule (config .dispatch (after s raw o w j) o (pos w j)) =
      some (config (.call (.forward (Butterfly.flags (s j) 0))) (after s raw o w j) o (pos w j)) := by
  let d := after s raw o w j
  let x := pos w j
  have r := valid_current s raw o n w j good hj
  have cmd : rule .dispatch (fun t => d t (heads o x t)) =
      some (.call (.forward (Butterfly.flags (s j) 0)),travel (fun t => d t (heads o x t)) .stay) := by
    by_cases zero : w=0
    · have ee : after s raw o w j .a (heads o (pos w j) .a)=.delimiter := by
        have e := r.endA
        rwa [show (w:ℤ)=0 by omega,add_zero] at e
      simp only [rule,d,x,ee,Butterfly.flags]
    · have bits := r.bitA 0 (by omega)
      simp only [CharP.cast_eq_zero,add_zero] at bits
      simp only [rule,d,x,bits,Butterfly.flags]
  simpa [TM.Move.shift] using moving _ _ d o x .stay cmd

theorem inner_run (s raw o n w j) (good : Valid s n w raw o) (hj : j<n) :
    Trace (TM.advance rule) (config (.call (.forward (Butterfly.flags (s j) 0))) (after s raw o w j) o (pos w j))
      (2*w+2) (config (.call .halt) (after s raw o w (j+1)) o (pos w j)) := by
  have a := lift (Butterfly.butterfly (s j) (after s raw o w j) (heads o (pos w j)) w
    (valid_current s raw o n w j good hj))
  simpa only [at_origin,after] using a

theorem return_from (d o x) : TM.advance rule (config (.call .halt) d o x) = some (config .skip d o x) := by
  simpa [TM.Move.shift] using moving (.call .halt) .skip d o x .stay (by simp [rule,Butterfly.rule])

theorem pos_next (w j : ℕ) : pos w (j+1)=pos w j+w+2 := by
  simp [pos,add_mul,add_assoc]

theorem tour_right (s raw o n w j) (good : Valid s n w raw o) (hj : j<n) (d : Banks) (keep : d .a=raw .a)
    (i : ℕ) (h : i≤w) :
    Trace (TM.advance rule) (config .skip d o (pos w j)) i (config .skip d o (pos w j+i)) := by
  induction i with
  | zero => simpa using Trace.nil (step:=TM.advance rule) (config .skip d o (pos w j))
  | succ i ih =>
    have mark : d .a (heads o (pos w j+i) .a) = .bit ((s j).a i) := by
      simpa only [heads,keep,add_assoc] using (good.row j hj).bitA i (by omega)
    have one := moving .skip .skip d o (pos w j+i) .right (by simp only [rule,mark])
    simpa [TM.Move.shift,add_assoc] using (ih (by omega)).trans (Trace.single one)

private theorem block (s raw o n w j) (good : Valid s n w raw o) (hj : j<n) :
    Trace (TM.advance rule) (config .dispatch (after s raw o w j) o (pos w j)) (3*w+6)
      (config .dispatch (after s raw o w (j+1)) o (pos w (j+1))) := by
  let d := after s raw o w (j+1)
  have keep : d .a=raw .a := (sources s raw o w (j+1)).1
  have bits := tour_right s raw o n w j good hj d keep w le_rfl
  have ending : d .a (heads o (pos w j+w) .a) = .delimiter := by
    simpa only [heads,keep,add_assoc] using (good.row j hj).endA
  have marker : d .a (heads o (pos w j+w+1) .a) = .home := by
    simpa only [heads,keep,add_assoc] using good.gap j hj
  have endStep := moving .skip .marker d o (pos w j+w) .right (by simp only [rule,ending])
  have markStep := moving .marker .dispatch d o (pos w j+w+1) .right (by simp only [rule,marker])
  have path := (((((Trace.single (block_start s raw o n w j good hj)).trans (inner_run s raw o n w j good hj)).trans
    (Trace.single (return_from d o (pos w j)))).trans bits).trans (Trace.single endStep)).trans (Trace.single markStep)
  change Trace _ _ (1+(2*w+2)+1+w+1+1) (config .dispatch d o (pos w j+w+1+1)) at path
  rwa [show 1+(2*w+2)+1+w+1+1=3*w+6 by omega,show pos w j+w+1+1=pos w (j+1) by rw [pos_next]; omega] at path

theorem issuing (s raw o n w) (good : Valid s n w raw o) (j : ℕ) (hj : j≤n) :
    Trace (TM.advance rule) (config .dispatch raw o 0) (j*(3*w+6))
      (config .dispatch (after s raw o w j) o (pos w j)) := by
  induction j with
  | zero => simpa [after,pos] using Trace.nil (step:=TM.advance rule) (config .dispatch raw o 0)
  | succ j ih =>
    simpa only [Nat.succ_mul] using (ih (by omega)).trans (block s raw o n w j good (by omega))

theorem back_step (d o x) (notEnd : d .a (heads o x .a) ≠ .count) :
    TM.advance rule (config .rewind d o x) = some (config .rewind d o (x-1)) := by
  apply moving _ _ _ _ _ .left
  cases tag : d .a (heads o x .a) <;> simp [rule,tag] at notEnd ⊢

private theorem tour_left (s raw o n w j) (good : Valid s n w raw o) (hj : j<n) (d : Banks) (keep : d .a=raw .a)
    (i : ℕ) (h : i≤w) :
    Trace (TM.advance rule) (config .rewind d o (pos w j+i-1)) i (config .rewind d o (pos w j-1)) := by
  induction i with
  | zero => simpa using Trace.nil (step:=TM.advance rule) (config .rewind d o (pos w j-1))
  | succ i ih =>
    have mark : d .a (heads o (pos w j+i) .a) = .bit ((s j).a i) := by
      simpa only [heads,keep,add_assoc] using (good.row j hj).bitA i (by omega)
    have one := back_step d o (pos w j+i) (by simp [mark])
    have path := Trace.cons one (ih (by omega))
    rw [show pos w j+(↑(i+1):ℤ)-1=pos w j+i by omega]
    simpa only [Nat.add_comm 1 i] using path

private theorem rewind_block (s raw o n w j) (good : Valid s n w raw o) (hj : j<n) (d : Banks) (keep : d .a=raw .a) :
    Trace (TM.advance rule) (config .rewind d o (pos w (j+1)-1)) (w+2)
      (config .rewind d o (pos w j-1)) := by
  have ending : d .a (heads o (pos w j+w) .a) = .delimiter := by
    simpa only [heads,keep,add_assoc] using (good.row j hj).endA
  have marker : d .a (heads o (pos w j+w+1) .a) = .home := by
    simpa only [heads,keep,add_assoc] using good.gap j hj
  have a := back_step d o (pos w j+w+1) (by simp [marker])
  have b := back_step d o (pos w j+w) (by simp [ending])
  have c := tour_left s raw o n w j good hj d keep w le_rfl
  rw [show pos w j+w+1-1=pos w j+w by omega] at a
  have path := Trace.cons a (Trace.cons b c)
  rw [show pos w (j+1)-1=pos w j+w+1 by rw [pos_next]; omega]
  simpa only [show 1+(1+w)=w+2 by omega] using path

theorem rewind_blocks (s raw o n w) (good : Valid s n w raw o) (d : Banks) (keep : d .a=raw .a)
    (j : ℕ) (hj : j≤n) :
    Trace (TM.advance rule) (config .rewind d o (pos w j-1)) (j*(w+2)) (config .rewind d o (-1)) := by
  induction j with
  | zero => simpa [pos] using Trace.nil (step:=TM.advance rule) (config .rewind d o (-1))
  | succ j ih =>
    have path := (rewind_block s raw o n w j good (by omega) d keep).trans (ih (by omega))
    simpa only [Nat.succ_mul,Nat.add_comm (w+2) (j*(w+2))] using path

/-- The complete stream, including nested physical-word execution, issue, record advance,
    file-end recognition, all four moving heads' rewind and the preserved modulus head. -/
theorem batch (s raw o) (n w : ℕ) (good : Valid s n w raw o) :
    Trace (TM.advance rule) (config .dispatch raw o 0) (n*(4*w+8)+4)
      (config .done (after s raw o w n) o 0) := by
  let d := after s raw o w n
  have keep : d .a=raw .a := (sources s raw o w n).1
  have endFile : d .a (heads o (pos w n) .a)=.count := by simpa only [heads,keep] using good.finish
  have finish := moving .dispatch .rewind d o (pos w n) .left (by simp only [rule,endFile])
  have rew := rewind_blocks s raw o n w good d keep n le_rfl
  have pre : d .a (heads o (-1) .a)=.home := by simpa only [heads,keep,sub_eq_add_neg] using good.entryHome
  have left := back_step d o (-1) (by simp [pre])
  have origin : d .a (heads o (-2) .a)=.count := by simpa only [heads,keep,sub_eq_add_neg] using good.start
  have cap := moving .rewind .origin d o (-2) .right (by simp only [rule,origin])
  have final := moving .origin .done d o (-1) .right (by simp only [rule])
  have path := (((((issuing s raw o n w good n le_rfl).trans (Trace.single finish)).trans rew).trans
    (Trace.single left)).trans (Trace.single cap)).trans (Trace.single final)
  change Trace _ _ (n*(3*w+6)+1+n*(w+2)+1+1+1) (config .done d o 0) at path
  rw [show 4*w+8=(3*w+6)+(w+2) by omega,Nat.mul_add]
  simpa only [show n*(3*w+6)+1+n*(w+2)+1+1+1=n*(3*w+6)+n*(w+2)+4 by omega] using path

theorem batch_halts (d o) : TM.advance rule (config .done d o 0)=none := rfl

theorem separated (w r j : ℕ) (h : r<j) : pos w r+w < pos w j := by
  have order : pos w (r+1) ≤ pos w j := by
    unfold pos
    exact mul_le_mul_of_nonneg_right (by exact_mod_cast Nat.succ_le_of_lt h) (by positivity)
  rw [pos_next] at order
  omega

private theorem fixed (s raw o w) (r n : ℕ) (p : Port) (moving : p≠.m) (i : ℕ)
    (hwidth : i<w) (inFile : r<n) :
    after s raw o w n p (heads o (pos w r) p+i) =
      Butterfly.output (s r) (after s raw o w r) (heads o (pos w r)) w p (heads o (pos w r) p+i) := by
  induction n with
  | zero => omega
  | succ j ih =>
    by_cases last : r=j
    · subst r
      rfl
    · have h : r<j := by omega
      have gap := separated w r j h
      have outside : heads o (pos w r) p+i < heads o (pos w j) p := by
        cases p <;> simp [heads] at moving ⊢ <;> omega
      rw [after,Butterfly.exterior _ _ _ _ _ _ (Or.inl outside)]
      exact ih h

private theorem config_cell (q : Stage) (d o x t z) : ((config q d o x).tape t).absolute z=d t z := by
  simp [config,TM.Tape.absolute,atPos]

/-- The two returned banks have the mathematical modular butterfly at each original
    record position, simultaneously for every record of the actual finite stream. -/
theorem batch_numbers (s raw o n w) (r : ℕ) (hr : r<n)
    (ha : Butterfly.number (s r).a w<Butterfly.number (s r).m w)
    (hb : Butterfly.number (s r).b w<Butterfly.number (s r).m w) :
    let C := config .done (after s raw o w n) o 0
    let p := heads o (pos w r)
    let a := Butterfly.number (s r).a w
    let b := Butterfly.number (s r).b w
    let m := Butterfly.number (s r).m w
    Butterfly.readWord C .sum (p .sum) w=(a+b)%m ∧ Butterfly.readWord C .diff (p .diff) w=(a+m-b)%m := by
  let p := heads o (pos w r)
  let d := Butterfly.output (s r) (after s raw o w r) p w
  let last := Butterfly.frame .halt d p 0
  let C := config .done (after s raw o w n) o 0
  have copied (t : Port) (ht : t≠.m) : Butterfly.readWord C t (p t) w = Butterfly.readWord last t (p t) w := by
    apply Butterfly.number_agrees
    intro i hi
    simp only [C,last,config_cell,Butterfly.frame_cell]
    congr 1
    simpa [d,p] using fixed s raw o w r n t ht i hi hr
  have genuine := Butterfly.output_numbers (s r) (after s raw o w r) p w ha hb
  exact ⟨(copied .sum (by decide)).trans genuine.1,(copied .diff (by decide)).trans genuine.2⟩

theorem batch_sources (s raw o w n) :
    after s raw o w n .a=raw .a ∧ after s raw o w n .b=raw .b ∧ after s raw o w n .m=raw .m :=
  sources s raw o w n

theorem batch_exterior (s raw o w n) (p : Port) (z : ℤ)
    (unrelated : ∀ j, j<n → z<heads o (pos w j) p ∨ heads o (pos w j) p+w ≤ z) :
    after s raw o w n p z = raw p z := by
  induction n with
  | zero => rfl
  | succ j ih =>
    rw [after,Butterfly.exterior _ _ _ _ _ _ (unrelated j (by omega))]
    exact ih (fun i hi => unrelated i (by omega))

open OAI.Computability.NearSquareRoot

theorem batch_visits (raw o n w) :
    VisitsAtMost rule (config .dispatch raw o 0) (n*(4*w+8)+4) (5*(n*(4*w+8)+5)) := by
  have bound := Binary.covers_by_elapsed rule (config .dispatch raw o 0) (n*(4*w+8)+4)
  simpa [Butterfly.port_count,Nat.mul_comm] using bound

theorem batch_homes (s raw o w n) (t : Port) : ((config .done (after s raw o w n) o 0).tape t).pos=o t := by
  cases t <;> simp [config,atPos,heads]

theorem stage_count : Fintype.card Stage=27 := by decide

end S008.Compiler.ButterflyStream
