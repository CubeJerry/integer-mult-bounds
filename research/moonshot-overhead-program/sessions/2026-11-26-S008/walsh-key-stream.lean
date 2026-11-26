import WalshKeyTape

/-! The complete auxiliary and distinguished source-frequency key on six fixed tapes. -/
namespace Moonshot.AlignedWalsh.KeyTape.Stream

open OAI.Computability.IntegerMultiplication
open S008.Compiler (Letter atPos)

inductive Wire where | core (p : Port) | tag | out deriving DecidableEq, Repr
instance : Fintype Wire := Fintype.ofList [.core .x,.core .z,.core .mx,.core .mz,.tag,.out] (by
  intro w; cases w with | core t => cases t <;> decide | _ => decide)

inductive Control where | next (common : Bool) | run (common query : Bool) (stage : Stage) | stop (common : Bool)
  deriving DecidableEq, Repr
private def coreStates : List Stage :=
  [.first false,.first true,.second false false,.second false true,.second true false,.second true true,
   .finishZ false,.finishZ true,.back false,.back true,.done false,.done true]
private theorem core_mem (s : Stage) : s∈coreStates := by
  cases s with
  | second p x => cases p <;> cases x <;> decide
  | _ p => cases p <;> decide
instance : Fintype Control := Fintype.ofList
  ([.next false,.next true,.stop false,.stop true] ++
   [false,true].flatMap (fun g ↦ [false,true].flatMap (fun j ↦ coreStates.map (Control.run g j)))) (by
    intro q
    cases q with
    | next p => apply List.mem_append_left; cases p <;> decide
    | stop p => apply List.mem_append_left; cases p <;> decide
    | run g j s =>
      apply List.mem_append_right
      exact List.mem_flatMap.mpr ⟨g,by cases g <;> decide,List.mem_flatMap.mpr
        ⟨j,by cases j <;> decide,List.mem_map.mpr ⟨s,core_mem s,rfl⟩⟩⟩)

private theorem ext_cfg {q : Control} {a b : Wire → TM.Tape Letter} (h : ∀ i, a i=b i) :
    (TM.Config.mk q a) = (TM.Config.mk q b) := congrArg (TM.Config.mk q) (funext h)

private def widen {α : Type} (c : Port → α) (tag out : α) : Wire → α
  | .core t => c t | .tag => tag | .out => out

def streamRule : TM.Rule Letter Control Wire := fun q r =>
  let hold := fun i ↦ (r i,TM.Move.stay)
  match q with
  | .stop _ => none
  | .next g => match r .tag with
    | .delimiter => some (.stop g,hold)
    | .bit j => some (.run g j (.first g),hold)
    | _ => none
  | .run g j s =>
    match readRule s (fun t ↦ r (.core t)) with
    | some (s',a) => some (.run g j s',widen a (r .tag,.stay) (r .out,.stay))
    | none => match s with
      | .done h => if j then
          some (.next g,widen (fun t ↦ (r (.core t),.stay)) (r .tag,.right) (.bit h,.right))
        else some (.next h,widen (fun t ↦ (r (.core t),.stay)) (r .tag,.right) (r .out,.stay))
      | _ => none

private theorem hold_tape (t : TM.Tape Letter) : t.apply (t.view 0,.stay)=t := by
  cases t with
  | mk pos f =>
    unfold TM.Tape.apply
    simp only [TM.Move.shift,Int.add_zero]
    congr 1
    funext i
    by_cases h : i=0 <;> simp [h]

def wrapped (g j : Bool) (c : TM.Config Letter Stage Port) (tag out : TM.Tape Letter) : TM.Config Letter Control Wire :=
  ⟨.run g j c.pc,widen c.tape tag out⟩

private theorem lift_step {c d : TM.Config Letter Stage Port} (g j : Bool) (tag out : TM.Tape Letter)
    (h : TM.advance readRule c=some d) : TM.advance streamRule (wrapped g j c tag out)=some (wrapped g j d tag out) := by
  rcases c with ⟨s,ts⟩
  cases hr : readRule s (fun t ↦ (ts t).view 0) with
  | none => simp [TM.advance,hr] at h
  | some act =>
    rcases act with ⟨s',a⟩
    simp only [TM.advance,hr,Option.map_some,Option.some.injEq] at h
    subst d
    unfold TM.advance wrapped streamRule
    simp only [widen,hr,Option.map_some,Option.some.injEq]
    apply ext_cfg
    intro t
    cases t <;> simp [widen,hold_tape]

private theorem lift_trace {c d : TM.Config Letter Stage Port} {n : ℕ} (g j : Bool) (tag out : TM.Tape Letter)
    (h : Trace (TM.advance readRule) c n d) :
    Trace (TM.advance streamRule) (wrapped g j c tag out) n (wrapped g j d tag out) := by
  induction h with
  | nil => exact Trace.nil _
  | cons hs _ ih => exact Trace.cons (lift_step g j tag out hs) ih

def advanceTag (t : TM.Tape Letter) := t.apply (t.view 0,.right)
def appendBit (t : TM.Tape Letter) (b : Bool) := t.apply (.bit b,.right)

def advanceMasks (o : Origins) (k : ℕ) : Origins := fun t ↦ match t with
  | .mx | .mz => o t+k
  | _ => o t

def staged (q : Control) (raw : Banks) (o : Origins) (tag out : TM.Tape Letter) : TM.Config Letter Control Wire :=
  ⟨q,widen (fun t ↦ atPos (raw t) (o t)) tag out⟩

private theorem choose_step (g j : Bool) (raw : Banks) (o : Origins) (tag out : TM.Tape Letter)
    (h : tag.view 0=.bit j) :
    TM.advance streamRule (staged (.next g) raw o tag out)=
      some (wrapped g j (scanning (.first g) raw o 0 0) tag out) := by
  unfold TM.advance staged wrapped scanning frame streamRule
  simp only [widen,h,Option.map_some,Option.some.injEq]
  apply ext_cfg
  intro t
  cases t with
  | core t => cases t <;> simp [widen,offset,hold_tape]
  | _ => simp [widen,hold_tape]

private theorem finish_step (g j h : Bool) (raw : Banks) (o : Origins) (k : ℕ) (tag out : TM.Tape Letter) :
    TM.advance streamRule (wrapped g j (returning (.done h) raw o k 0) tag out)=
      some (staged (.next (if j then g else h)) raw (advanceMasks o k) (advanceTag tag)
        (if j then appendBit out h else out)) := by
  cases j <;> unfold TM.advance streamRule staged wrapped returning frame <;>
    simp only [readRule,widen,Bool.false_eq_true,ite_false,ite_true,Option.map_some,Option.some.injEq]
  all_goals
    apply ext_cfg
    intro t
    cases t with
    | core t => cases t <;> simp [widen,offset,advanceMasks,hold_tape]
    | _ => simp [widen,advanceTag,appendBit,hold_tape]

private theorem stop_step (g : Bool) (raw : Banks) (o : Origins) (tag out : TM.Tape Letter)
    (h : tag.view 0=.delimiter) :
    TM.advance streamRule (staged (.next g) raw o tag out)=some (staged (.stop g) raw o tag out) := by
  unfold TM.advance staged streamRule
  simp only [widen,h,Option.map_some,Option.some.injEq]
  apply ext_cfg
  intro t
  cases t <;> simp [widen,hold_tape]

structure Job where
  query : Bool
  pairs : List Pair

def layout (raw : Banks) (o : Origins) (k : ℕ) (tag : TM.Tape Letter) : List Job → Prop
  | [] => tag.view 0=.delimiter
  | j::js => tag.view 0=.bit j.query ∧ Ready raw o k j.pairs ∧ layout raw (advanceMasks o k) k (advanceTag tag) js

def commonAtEnd (g : Bool) : List Job → Bool
  | [] => g
  | j::js => commonAtEnd (if j.query then g else dot g j.pairs) js

def keyBits (g : Bool) : List Job → List Bool
  | [] => []
  | j::js => if j.query then dot g j.pairs::keyBits g js else keyBits (dot g j.pairs) js

def written (o : TM.Tape Letter) : List Bool → TM.Tape Letter
  | [] => o
  | b::bs => written (appendBit o b) bs

def tagsAfter (tag : TM.Tape Letter) : ℕ → TM.Tape Letter | 0 => tag | n+1 => tagsAfter (advanceTag tag) n
def masksAfter (o : Origins) (k : ℕ) : ℕ → Origins | 0 => o | n+1 => masksAfter (advanceMasks o k) k n

/-- One deterministic rule obtains the whole key on actual occupied tapes. Both
address copies stay intact, masks land after the final block, and each query appends
its bit through the output head. Auxiliary parities update only finite control. -/
theorem stream_trace (raw : Banks) (o : Origins) (k : ℕ) (tag out : TM.Tape Letter)
    (jobs : List Job) (g : Bool) (h : layout raw o k tag jobs) :
    Trace (TM.advance streamRule) (staged (.next g) raw o tag out) ((3*k+5)*jobs.length+1)
      (staged (.stop (commonAtEnd g jobs)) raw (masksAfter o k jobs.length) (tagsAfter tag jobs.length)
        (written out (keyBits g jobs))) := by
  induction jobs generalizing o tag out g with
  | nil => exact Trace.single (stop_step g raw o tag out h)
  | cons j js ih =>
    obtain ⟨hta,hr,ht⟩ := h
    have startScan := (Trace.single (choose_step g j.query raw o tag out hta)).trans
      (lift_trace g j.query tag out (paired_scan raw o k j.pairs g hr))
    have joined := startScan.trans (Trace.single (finish_step g j.query (dot g j.pairs) raw o k tag out))
    have rest := ih (advanceMasks o k) (advanceTag tag) (if j.query then appendBit out (dot g j.pairs) else out)
      (if j.query then g else dot g j.pairs) ht
    have full := joined.trans rest
    have ht' : 1+(3*k+3)+1+((3*k+5)*js.length+1)=(3*k+5)*(j::js).length+1 := by simp; ring
    rw [ht'] at full
    cases j with
    | mk query cells => cases query <;> simpa only [List.length_cons,masksAfter,tagsAfter,commonAtEnd,keyBits,written,
      Bool.false_eq_true,ite_false,ite_true] using full

def auxJobs (xs : List (List Pair)) := xs.map (fun a ↦ Job.mk false a)
def queryJobs (xs : List (List Pair)) := xs.map (fun a ↦ Job.mk true a)

def auxParity (g : Bool) : List (List Pair) → Bool
  | [] => g | a::as => auxParity (dot g a) as

def auxHits : List (List Pair) → ℕ | [] => 0 | a::as => hits a+auxHits as

private theorem only_queries (g : Bool) (qs : List (List Pair)) :
    keyBits g (queryJobs qs)=qs.map (fun p ↦ dot g p) := by
  induction qs with
  | nil => rfl
  | cons a xs ih => simpa only [queryJobs,List.map_cons,keyBits,ite_true,List.cons.injEq,true_and] using ih

private theorem phased (g : Bool) (as qs : List (List Pair)) :
    keyBits g (auxJobs as++queryJobs qs)=qs.map (fun p ↦ dot (auxParity g as) p) := by
  induction as generalizing g with
  | nil => exact only_queries g qs
  | cons a as ih => exact ih (dot g a)

private theorem aux_sign (g : Bool) (as : List (List Pair)) : sign (auxParity g as)=sign g*(-1:ℤ)^auxHits as := by
  induction as generalizing g with
  | nil => simp [auxParity,auxHits]
  | cons a as ih => rw [auxParity,ih,column_sign,auxHits,pow_add]; ring

/-- These are Q_j's actual signs when the shared auxiliary pairs precede the
individual distinguished pairs. -/
theorem source_key (as qs : List (List Pair)) :
    (keyBits false (auxJobs as++queryJobs qs)).map sign =
      qs.map (fun ps ↦ (-1:ℤ)^(auxHits as+hits ps)) := by
  rw [phased,List.map_map]
  apply List.map_congr_left
  intro p _
  change sign (dot (auxParity false as) p)=(-1:ℤ)^(auxHits as+hits p)
  rw [column_sign,aux_sign,pow_add]
  simp [sign]

private theorem append_pos (out : TM.Tape Letter) (b : Bool) :
    (appendBit out b).pos=out.pos+1 := rfl

theorem output_position (out : TM.Tape Letter) (bs : List Bool) :
    (written out bs).pos=out.pos+bs.length := by
  induction bs generalizing out with
  | nil => simp [written]
  | cons b bs ih =>
    rw [written,ih,append_pos,List.length_cons,Nat.cast_add,Nat.cast_one]
    omega

/-- Neither occupied originals before the key nor arbitrary cells past its last
position are disturbed. -/
theorem output_exterior (out : TM.Tape Letter) (bs : List Bool) (z : ℤ)
    (h : z<out.pos ∨ out.pos+bs.length ≤ z) : (written out bs).absolute z=out.absolute z := by
  induction bs generalizing out with
  | nil => rfl
  | cons b bs ih =>
    have hc : z<out.pos ∨ out.pos+(bs.length+1:ℕ)≤z := h
    have ht : z < (appendBit out b).pos ∨ (appendBit out b).pos+bs.length ≤ z := by rw [append_pos]; omega
    rw [written,ih (appendBit out b) ht,appendBit,TM.Tape.absolute_apply,ite_eq_right (by omega)]

/-- The bit appended for each distinguished query is at its actual output address. -/
theorem output_digit (out : TM.Tape Letter) (bs : List Bool) (i : ℕ) (hi : i<bs.length) :
    (written out bs).absolute (out.pos+i)=.bit (bs[i]) := by
  induction bs generalizing out i with
  | nil => simp at hi
  | cons b bs ih =>
    cases i with
    | zero =>
      have ht : out.pos<(appendBit out b).pos := by rw [append_pos]; omega
      rw [Nat.cast_zero,Int.add_zero,written,output_exterior _ _ _ (Or.inl ht),appendBit,
        TM.Tape.absolute_apply,ite_eq_left rfl,List.getElem_cons_zero]
    | succ i =>
      have hsmall : i<bs.length := by simpa using hi
      have hloc : out.pos + ((i+1 : ℕ):ℤ) = (appendBit out b).pos+i := by rw [append_pos]; omega
      rw [written,hloc,ih _ _ hsmall,List.getElem_cons_succ]

/-- After the ordinary mask stream, the next available transition is halt. -/
theorem stream_halts (g : Bool) (raw : Banks) (o : Origins) (tag out : TM.Tape Letter) :
    TM.advance streamRule (staged (.stop g) raw o tag out)=none := rfl

theorem stream_counts : Fintype.card Control=52 ∧ Fintype.card Wire=6 := by decide

/-- The complete six-head selector core has a linear cumulative-cell cap on its
actual concatenated descriptors. -/
theorem stream_visits (raw : Banks) (o : Origins) (k d : ℕ) (g : Bool) (tag out : TM.Tape Letter) :
    OAI.Computability.NearSquareRoot.VisitsAtMost streamRule (staged (.next g) raw o tag out)
      ((3*k+5)*d+1) (6*((3*k+5)*d+2)) := by
  have h := time_cover streamRule (staged (.next g) raw o tag out) ((3*k+5)*d+1)
  rw [stream_counts.2] at h
  have ec : (((3*k+5)*d+1)+1)*6=6*((3*k+5)*d+2) := by omega
  rwa [ec] at h

end Moonshot.AlignedWalsh.KeyTape.Stream
#print axioms Moonshot.AlignedWalsh.KeyTape.Stream.stream_trace
#print axioms Moonshot.AlignedWalsh.KeyTape.Stream.source_key
#print axioms Moonshot.AlignedWalsh.KeyTape.Stream.output_position
#print axioms Moonshot.AlignedWalsh.KeyTape.Stream.output_exterior
#print axioms Moonshot.AlignedWalsh.KeyTape.Stream.output_digit
#print axioms Moonshot.AlignedWalsh.KeyTape.Stream.stream_halts
#print axioms Moonshot.AlignedWalsh.KeyTape.Stream.stream_counts

#print axioms Moonshot.AlignedWalsh.KeyTape.Stream.stream_visits
