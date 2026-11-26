import «compiler-controller»
import OAI.Computability.NearSquareRoot.VisitedCells

/-! A four-head source-model scan for one arbitrary pair of staged Fourier masks. -/
namespace Moonshot.AlignedWalsh.KeyTape

open OAI.Computability.IntegerMultiplication
open S008.Compiler (Letter atPos)

inductive Port where | x | z | mx | mz deriving DecidableEq, Repr
instance : Fintype Port := Fintype.ofList [.x,.z,.mx,.mz] (by intro t; cases t <;> decide)

inductive Stage where
  | first (p : Bool) | second (p x : Bool) | finishZ (p : Bool) | back (p : Bool) | done (p : Bool)
  deriving DecidableEq, Repr
instance : Fintype Stage := Fintype.ofList
  [.first false,.first true,.second false false,.second false true,.second true false,.second true true,
   .finishZ false,.finishZ true,.back false,.back true,.done false,.done true] (by
    intro q
    cases q with
    | second p x => cases p <;> cases x <;> decide
    | _ p => cases p <;> decide)

abbrev Banks := Port → ℤ → Letter
abbrev Origins := Port → ℤ

def offset (x z mx mz : ℤ) : Port → ℤ
  | .x => x | .z => z | .mx => mx | .mz => mz

def motions (x z mx mz : TM.Move) : Port → TM.Move
  | .x => x | .z => z | .mx => mx | .mz => mz

def keep (r : Port → Letter) (m : Port → TM.Move) : Port → Letter × TM.Move := fun t ↦ (r t,m t)

def readRule : TM.Rule Letter Stage Port := fun q r =>
  let first := motions .right .stay .right .stay
  let second := motions .stay .right .stay .right
  let still := motions .stay .stay .stay .stay
  let backward := motions .left .left .stay .stay
  let forward := motions .right .right .stay .stay
  match q with
  | .first p => match r .x, r .mx with
    | .bit _,.bit false => some (.first p,keep r first)
    | .bit x,.bit true => some (.second p x,keep r first)
    | .delimiter,_ => some (.finishZ p,keep r still)
    | _,_ => none
  | .second p x => match r .z,r .mz with
    | .bit _,.bit false => some (.second p x,keep r second)
    | .bit z,.bit true => some (.first (xor p (x&&z)),keep r second)
    | _,_ => none
  | .finishZ p => match r .z with
    | .bit _ => some (.finishZ p,keep r second)
    | .delimiter => some (.back p,keep r backward)
    | _ => none
  | .back p => match r .x with
    | .bit _ => some (.back p,keep r backward)
    | .home => some (.done p,keep r forward)
    | _ => none
  | .done _ => none

def frame (q : Stage) (raw : Banks) (o : Origins) (at' : Port → ℤ) : TM.Config Letter Stage Port :=
  ⟨q,fun t ↦ atPos (raw t) (o t+at' t)⟩

def scanning (q : Stage) (raw : Banks) (o : Origins) (x z : ℤ) := frame q raw o (offset x z x z)
def returning (q : Stage) (raw : Banks) (o : Origins) (k : ℕ) (i : ℤ) := frame q raw o (offset i i k k)

private theorem untouched (A : ℤ → Letter) (p : ℤ) (v : TM.Move) :
    (atPos A p).apply (A p,v) = atPos A (p+v.shift) := by
  unfold atPos TM.Tape.apply
  congr 1
  funext i
  by_cases h : i+v.shift=0 <;> simp only [h,ite_true,ite_false] <;> congr 1 <;> omega

private theorem issue {q q' : Stage} (raw : Banks) (o : Origins) {p p' : Port → ℤ}
    {m : Port → TM.Move}
    (h : readRule q (fun t ↦ raw t (o t+p t))=some (q',keep (fun t ↦ raw t (o t+p t)) m))
    (next : ∀ t, p t+(m t).shift=p' t) :
    TM.advance readRule (frame q raw o p)=some (frame q' raw o p') := by
  unfold TM.advance frame
  have read (t : Port) : (atPos (raw t) (o t+p t)).view 0=raw t (o t+p t) := by simp [atPos]
  simp only [read,h,Option.map_some,Option.some.injEq]
  apply congrArg (TM.Config.mk q')
  funext t
  simp [keep,untouched,add_assoc,next]

private theorem step_first {q q' : Stage} (raw : Banks) (o : Origins) (x z : ℤ)
    (h : readRule q (fun t ↦ raw t (o t+offset x z x z t)) =
      some (q',keep (fun t ↦ raw t (o t+offset x z x z t)) (motions .right .stay .right .stay))) :
    TM.advance readRule (scanning q raw o x z) = some (scanning q' raw o (x+1) z) :=
  issue raw o h (by intro t; cases t <;> simp [offset,motions,TM.Move.shift])

private theorem step_second {q q' : Stage} (raw : Banks) (o : Origins) (x z : ℤ)
    (h : readRule q (fun t ↦ raw t (o t+offset x z x z t)) =
      some (q',keep (fun t ↦ raw t (o t+offset x z x z t)) (motions .stay .right .stay .right))) :
    TM.advance readRule (scanning q raw o x z) = some (scanning q' raw o x (z+1)) :=
  issue raw o h (by intro t; cases t <;> simp [offset,motions,TM.Move.shift])

private theorem walk_first (raw : Banks) (o : Origins) (p : Bool) (x z n : ℕ)
    (h : ∀ i<n, (∃ b,raw .x (o .x+(x+i:ℕ))=.bit b) ∧ raw .mx (o .mx+(x+i:ℕ))=.bit false) :
    Trace (TM.advance readRule) (scanning (.first p) raw o x z) n (scanning (.first p) raw o (x+n:ℕ) z) := by
  induction n with
  | zero => exact Trace.nil _
  | succ n ih =>
    obtain ⟨⟨b,hb⟩,hm⟩ := h n (by omega)
    have st := step_first (q:=.first p) (q':=.first p) raw o (x+n:ℕ) z (by simp only [readRule,offset,hb,hm])
    simpa only [Nat.cast_add,Nat.cast_one,add_assoc] using
      (ih fun i hi ↦ h i (by omega)).trans (Trace.single st)

private theorem walk_second (raw : Banks) (o : Origins) (p a : Bool) (x z n : ℕ)
    (h : ∀ i<n, (∃ b,raw .z (o .z+(z+i:ℕ))=.bit b) ∧ raw .mz (o .mz+(z+i:ℕ))=.bit false) :
    Trace (TM.advance readRule) (scanning (.second p a) raw o x z) n (scanning (.second p a) raw o x (z+n:ℕ)) := by
  induction n with
  | zero => exact Trace.nil _
  | succ n ih =>
    obtain ⟨⟨b,hb⟩,hm⟩ := h n (by omega)
    have st := step_second (q:=.second p a) (q':=.second p a) raw o x (z+n:ℕ) (by simp only [readRule,offset,hb,hm])
    simpa only [Nat.cast_add,Nat.cast_one,add_assoc] using
      (ih fun i hi ↦ h i (by omega)).trans (Trace.single st)

structure Pair where
  leftGap : ℕ
  rightGap : ℕ
  leftBit : Bool
  rightBit : Bool

def leftSize : List Pair → ℕ | [] => 0 | a::xs => a.leftGap+1+leftSize xs
def rightSize : List Pair → ℕ | [] => 0 | a::xs => a.rightGap+1+rightSize xs

def dot (p : Bool) : List Pair → Bool
  | [] => p
  | a::xs => dot (xor p (a.leftBit&&a.rightBit)) xs

/-- In each address copy, a segment skips zero mask bits, then exposes one marked bit. -/
def segments (raw : Banks) (o : Origins) (x z : ℕ) : List Pair → Prop
  | [] => True
  | a::xs => (∀ i<a.leftGap, (∃ b,raw .x (o .x+(x+i:ℕ))=.bit b) ∧ raw .mx (o .mx+(x+i:ℕ))=.bit false) ∧
    (∀ i<a.rightGap, (∃ b,raw .z (o .z+(z+i:ℕ))=.bit b) ∧ raw .mz (o .mz+(z+i:ℕ))=.bit false) ∧
    raw .x (o .x+(x+a.leftGap:ℕ))=.bit a.leftBit ∧ raw .mx (o .mx+(x+a.leftGap:ℕ))=.bit true ∧
    raw .z (o .z+(z+a.rightGap:ℕ))=.bit a.rightBit ∧ raw .mz (o .mz+(z+a.rightGap:ℕ))=.bit true ∧
    segments raw o (x+a.leftGap+1) (z+a.rightGap+1) xs

private theorem across (raw : Banks) (o : Origins) (xs : List Pair) (x z : ℕ) (p : Bool)
    (h : segments raw o x z xs) :
    Trace (TM.advance readRule) (scanning (.first p) raw o x z) (leftSize xs+rightSize xs)
      (scanning (.first (dot p xs)) raw o (x+leftSize xs:ℕ) (z+rightSize xs:ℕ)) := by
  induction xs generalizing x z p with
  | nil => exact Trace.nil _
  | cons a xs ih =>
    obtain ⟨h₁,h₂,hx,hm,hz,hn,hr⟩ := h
    have lx := walk_first raw o p x z a.leftGap h₁
    have one := step_first (q:=.first p) (q':=.second p a.leftBit) raw o (x+a.leftGap:ℕ) z
      (by simp only [readRule,offset,hx,hm])
    have rz := walk_second raw o p a.leftBit (x+a.leftGap+1) z a.rightGap h₂
    have two := step_second (q:=.second p a.leftBit) (q':=.first (xor p (a.leftBit&&a.rightBit)))
      raw o (x+a.leftGap+1:ℕ) (z+a.rightGap:ℕ) (by simp only [readRule,offset,hz,hn])
    have tail := ih (x+a.leftGap+1) (z+a.rightGap+1) (xor p (a.leftBit&&a.rightBit)) hr
    norm_cast at one two
    have a1 := lx.trans (Trace.single one)
    have a2 := a1.trans rz
    have a3 := a2.trans (Trace.single two)
    have a4 := a3.trans tail
    have ht : a.leftGap+1+a.rightGap+1+(leftSize xs+rightSize xs) =
        leftSize (a::xs)+rightSize (a::xs) := by simp only [leftSize,rightSize]; omega
    rw [ht] at a4
    simpa [leftSize,rightSize,dot,Nat.add_assoc] using a4

/-- The true source alphabet on each counter position and its cost-free outer tapes. -/
structure Ready (raw : Banks) (o : Origins) (k : ℕ) (ps : List Pair) : Prop where
  selected : segments raw o 0 0 ps
  leftFits : leftSize ps ≤ k
  rightFits : rightSize ps ≤ k
  xBits : ∀ (i : ℕ), i < k → ∃ b, raw .x (o .x+i)=.bit b
  zBits : ∀ (i : ℕ), i < k → ∃ b, raw .z (o .z+i)=.bit b
  xRest : ∀ (i : ℕ), leftSize ps ≤ i → i < k → raw .mx (o .mx+i)=.bit false
  zRest : ∀ (i : ℕ), rightSize ps ≤ i → i < k → raw .mz (o .mz+i)=.bit false
  xEnd : raw .x (o .x+k) = .delimiter
  zEnd : raw .z (o .z+k) = .delimiter
  xHome : raw .x (o .x-1) = .home

private theorem walk_end (raw : Banks) (o : Origins) (p : Bool) (x z n : ℕ)
    (h : ∀ i<n, ∃ b,raw .z (o .z+(z+i:ℕ))=.bit b) :
    Trace (TM.advance readRule) (scanning (.finishZ p) raw o x z) n (scanning (.finishZ p) raw o x (z+n:ℕ)) := by
  induction n with
  | zero => exact Trace.nil _
  | succ n ih =>
    obtain ⟨b,hb⟩ := h n (by omega)
    have st := step_second (q:=.finishZ p) (q':=.finishZ p) raw o x (z+n:ℕ)
      (by simp only [readRule,offset,hb])
    simpa only [Nat.cast_add,Nat.cast_one,add_assoc] using
      (ih fun i hi ↦ h i (by omega)).trans (Trace.single st)

private theorem go_back (raw : Banks) (o : Origins) (p : Bool) (k i : ℕ)
    (h : ∀ (j : ℕ), j < i → ∃ b,raw .x (o .x+j)=.bit b) :
    Trace (TM.advance readRule) (returning (.back p) raw o k ((i:ℤ)-1)) i
      (returning (.back p) raw o k (-1)) := by
  induction i with
  | zero => exact Trace.nil _
  | succ i ih =>
    obtain ⟨b,hb⟩ := h i (by omega)
    have st : TM.advance readRule (returning (.back p) raw o k (i:ℤ))=
        some (returning (.back p) raw o k ((i:ℤ)-1)) := by
      apply issue (m:=motions .left .left .stay .stay) raw o
      · simp only [readRule,offset,hb]
      · intro t; cases t <;> simp [offset,motions,TM.Move.shift] <;> omega
    have ht := Trace.cons st (ih (fun j hj ↦ h j (by omega)))
    simpa [Nat.add_comm 1 i] using ht

/-- At any width and arbitrary absolute origins or exterior words, the paired mask
scan returns both numeric heads home, positions both mask heads at their following
blocks, and preserves every original tape cell. Its exact clock is 3k+3. -/
theorem paired_scan (raw : Banks) (o : Origins) (k : ℕ) (ps : List Pair) (p : Bool)
    (good : Ready raw o k ps) :
    Trace (TM.advance readRule) (scanning (.first p) raw o 0 0) (3*k+3)
      (returning (.done (dot p ps)) raw o k 0) := by
  let r := dot p ps
  let bx := leftSize ps
  let bz := rightSize ps
  have hx := good.leftFits
  have hz := good.rightFits
  have xend : bx+(k-bx)=k := Nat.add_sub_of_le hx
  have zend : bz+(k-bz)=k := Nat.add_sub_of_le hz
  have first : Trace (TM.advance readRule) (scanning (.first p) raw o 0 0) (bx+bz)
      (scanning (.first r) raw o bx bz) := by
    simpa only [Nat.zero_add,Nat.cast_zero] using across raw o ps 0 0 p good.selected
  have tx := walk_first raw o r bx bz (k-bx) (fun i hi ↦
    ⟨good.xBits (bx+i) (by omega), good.xRest (bx+i) (by dsimp [bx]; omega) (by omega)⟩)
  rw [xend] at tx
  have ex : TM.advance readRule (scanning (.first r) raw o k bz) =
       some (scanning (.finishZ r) raw o k bz) := by
    apply issue (m:=motions .stay .stay .stay .stay) raw o
    · simp only [readRule,offset,good.xEnd]
    · intro t; cases t <;> simp [offset,motions,TM.Move.shift]
  have tz := walk_end raw o r k bz (k-bz) (fun i hi ↦ good.zBits (bz+i) (by omega))
  rw [zend] at tz
  have ez : TM.advance readRule (scanning (.finishZ r) raw o k k) =
       some (returning (.back r) raw o k ((k:ℤ)-1)) := by
    apply issue (m:=motions .left .left .stay .stay) raw o
    · simp only [readRule,offset,good.zEnd]
    · intro t; cases t <;> simp [offset,motions,TM.Move.shift] <;> omega
  have back := go_back raw o r k k good.xBits
  have eh : TM.advance readRule (returning (.back r) raw o k (-1))=
       some (returning (.done r) raw o k 0) := by
    apply issue (m:=motions .right .right .stay .stay) raw o
    · simp only [readRule,offset,←sub_eq_add_neg,good.xHome]
    · intro t; cases t <;> simp [offset,motions,TM.Move.shift]
  have tr := ((((((first.trans tx).trans (Trace.single ex)).trans tz).trans (Trace.single ez)).trans back).trans
    (Trace.single eh))
  have time : bx+bz+(k-bx)+1+(k-bz)+1+k+1=3*k+3 := by omega
  rw [time] at tr
  exact tr

/-- The output control is the actual product of all selected Fourier column signs. -/
def hits : List Pair → ℕ
  | [] => 0
  | a::xs => (if a.leftBit&&a.rightBit then 1 else 0)+hits xs

def sign (p : Bool) : ℤ := if p then -1 else 1

theorem column_sign (p : Bool) (ps : List Pair) : sign (dot p ps)=sign p*(-1:ℤ)^hits ps := by
  induction ps generalizing p with
  | nil => simp [dot,hits]
  | cons a xs ih =>
    rw [dot,ih,hits,pow_add]
    cases a.leftBit&&a.rightBit <;> cases p <;> simp [sign]

/-- A completed dot scan returns its sign in finite control without a further tape step. -/
theorem scan_halts (raw : Banks) (o : Origins) (p : Bool) (k : ℕ) :
    TM.advance readRule (returning (.done p) raw o k 0)=none := rfl

/-- A deterministic trajectory gives one square of a given tape per time index. -/
theorem time_cover {A Q I : Type} [Fintype I] (m : TM.Rule A Q I) (C : TM.Config A Q I) (T : ℕ) :
    OAI.Computability.NearSquareRoot.VisitsAtMost m C T ((T+1)*Fintype.card I) := by
  classical
  let endpoint (u : Fin (T+1)) : TM.Config A Q I :=
    if h : ∃ C', Trace (TM.advance m) C u.val C' then h.choose else C
  let whereAt (v : Fin (T+1) × I) := (v.2,((endpoint v.1).tape v.2).pos)
  refine ⟨Finset.univ.image whereAt,?_,?_⟩
  · have hh := Finset.card_image_le (f:=whereAt) (s:=Finset.univ)
    simpa only [Finset.card_univ,Fintype.card_prod,Fintype.card_fin] using hh
  · intro u hu c htr i
    let v : Fin (T+1) := ⟨u,by omega⟩
    have hh : ∃ c', Trace (TM.advance m) C v.val c' := ⟨c,htr⟩
    have hd : endpoint v=c := by
      dsimp only [endpoint]
      rw [dite_eq_left hh]
      exact OAI.Computability.NearSquareRoot.trace_endpoint_unique hh.choose_spec htr
    exact Finset.mem_image.mpr ⟨(v,i),Finset.mem_univ _,by simp [whereAt,hd]⟩

/-- The local visited-space bound counts all four heads at every time index. -/
theorem pair_visits (raw : Banks) (o : Origins) (k : ℕ) (p : Bool) :
    OAI.Computability.NearSquareRoot.VisitsAtMost readRule (scanning (.first p) raw o 0 0)
      (3*k+3) (12*k+16) := by
  have hc : Fintype.card Port=4 := by decide
  convert time_cover readRule (scanning (.first p) raw o 0 0) (3*k+3) using 1
  rw [hc]
  omega

/-- The remaining consecutive columns after the first selected bit in each slot. -/
def dense (X Z : ℕ → Bool) (i : ℕ) : ℕ → List Pair
  | 0 => []
  | n+1 => ⟨0,0,X i,Z i⟩::dense X Z (i+1) n

def slots (sx sz : ℕ) (X Z : ℕ → Bool) : ℕ → List Pair
  | 0 => []
  | n+1 => ⟨sx,sz,X 0,Z 0⟩::dense X Z 1 n

private theorem dense_sizes (X Z : ℕ → Bool) (i n : ℕ) :
    leftSize (dense X Z i n)=n ∧ rightSize (dense X Z i n)=n := by
  induction n generalizing i with
  | zero => exact ⟨rfl,rfl⟩
  | succ n ih => exact ⟨by simp [dense,leftSize,(ih (i+1)).1,Nat.add_comm],
                              by simp [dense,rightSize,(ih (i+1)).2,Nat.add_comm]⟩

private theorem dense_segments (raw : Banks) (o : Origins) (X Z : ℕ → Bool) (x z i n : ℕ)
    (h : ∀ j<n, raw .x (o .x+(x+j:ℕ))=.bit (X (i+j)) ∧ raw .mx (o .mx+(x+j:ℕ))=.bit true ∧
      raw .z (o .z+(z+j:ℕ))=.bit (Z (i+j)) ∧ raw .mz (o .mz+(z+j:ℕ))=.bit true) :
    segments raw o x z (dense X Z i n) := by
  induction n generalizing x z i with
  | zero => trivial
  | succ n ih =>
    obtain ⟨h₀,h₁,h₂,h₃⟩ := h 0 (by omega)
    dsimp only [dense,segments,Nat.add_zero]
    refine ⟨by omega,by omega,by simpa using h₀,by simpa using h₁,by simpa using h₂,by simpa using h₃,?_⟩
    apply ih
    intro j hj
    simpa only [Nat.add_assoc,Nat.add_comm 1 j] using h (j+1) (by omega)

/-- A consecutive pair of f-bit physical slots, at independently chosen offsets in
its two counter copies. The mask banks are the ordinary staged slot indicators. -/
structure SlotInput (raw : Banks) (o : Origins) (k sx sz f : ℕ) (X Z : ℕ → Bool) : Prop where
  roomX : sx+f ≤ k
  roomZ : sz+f ≤ k
  occupiedX : ∀ (i : ℕ), i < k → ∃ b, raw .x (o .x+i)=.bit b
  occupiedZ : ∀ (i : ℕ), i < k → ∃ b, raw .z (o .z+i)=.bit b
  selectX : ∀ (i : ℕ), i < k → raw .mx (o .mx+i)=.bit (decide (sx ≤ i ∧ i < sx+f))
  selectZ : ∀ (i : ℕ), i < k → raw .mz (o .mz+i)=.bit (decide (sz ≤ i ∧ i < sz+f))
  valueX : ∀ (j : ℕ), j < f → raw .x (o .x+(sx+j:ℕ))=.bit (X j)
  valueZ : ∀ (j : ℕ), j < f → raw .z (o .z+(sz+j:ℕ))=.bit (Z j)
  endX : raw .x (o .x+k)=.delimiter
  endZ : raw .z (o .z+k)=.delimiter
  home : raw .x (o .x-1)=.home

private theorem slot_ready (raw : Banks) (o : Origins) (k sx sz f : ℕ) (X Z : ℕ → Bool)
    (g : SlotInput raw o k sx sz f X Z) : Ready raw o k (slots sx sz X Z f) := by
  have bx := g.roomX
  have bz := g.roomZ
  cases f with
  | zero =>
    refine ⟨trivial,Nat.zero_le _,Nat.zero_le _,g.occupiedX,g.occupiedZ,?_,?_,g.endX,g.endZ,g.home⟩
    · intro i _ hi
      rw [g.selectX i hi,decide_eq_false (by omega)]
    · intro i _ hi
      rw [g.selectZ i hi,decide_eq_false (by omega)]
  | succ n =>
    have hxsize : leftSize (slots sx sz X Z (n+1))=sx+1+n := by simp [slots,leftSize,(dense_sizes X Z 1 n).1]
    have hzsize : rightSize (slots sx sz X Z (n+1))=sz+1+n := by simp [slots,rightSize,(dense_sizes X Z 1 n).2]
    refine ⟨?_,by rw [hxsize]; omega,by rw [hzsize]; omega,g.occupiedX,g.occupiedZ,?_,?_,g.endX,g.endZ,g.home⟩
    · simp only [slots,segments,Nat.zero_add]
      refine ⟨?_,?_,by simpa using g.valueX 0 (by omega),?_,by simpa using g.valueZ 0 (by omega),?_,?_⟩
      · intro i hi
        refine ⟨g.occupiedX i (by omega),?_⟩
        rw [g.selectX i (by omega),decide_eq_false (by omega)]
      · intro i hi
        refine ⟨g.occupiedZ i (by omega),?_⟩
        rw [g.selectZ i (by omega),decide_eq_false (by omega)]
      · rw [g.selectX sx (by omega),decide_eq_true (by omega)]
      · rw [g.selectZ sz (by omega),decide_eq_true (by omega)]
      · apply dense_segments
        intro j hj
        obtain h₁ := g.valueX (1+j) (by omega)
        obtain h₂ := g.valueZ (1+j) (by omega)
        refine ⟨by simpa only [Nat.add_assoc] using h₁,?_,by simpa only [Nat.add_assoc] using h₂,?_⟩
        · rw [g.selectX _ (by omega),decide_eq_true (by omega)]
        · rw [g.selectZ _ (by omega),decide_eq_true (by omega)]
    · intro i he hi
      rw [hxsize] at he
      rw [g.selectX i hi,decide_eq_false (by omega)]
    · intro i he hi
      rw [hzsize] at he
      rw [g.selectZ i hi,decide_eq_false (by omega)]

/-- Column parity is exactly the ordinary current-frequency dot on all f columns. -/
def bitCount (X Z : ℕ → Bool) (i : ℕ) : ℕ → ℕ
  | 0 => 0
  | n+1 => (if X i&&Z i then 1 else 0)+bitCount X Z (i+1) n

private theorem dense_hits (X Z : ℕ → Bool) (i n : ℕ) : hits (dense X Z i n)=bitCount X Z i n := by
  induction n generalizing i with
  | zero => rfl
  | succ n ih => simp only [dense,hits,bitCount,ih]

theorem slot_scan (raw : Banks) (o : Origins) (k sx sz f : ℕ) (X Z : ℕ → Bool) (p : Bool)
    (g : SlotInput raw o k sx sz f X Z) :
    ∃ q, sign q=sign p*(-1:ℤ)^bitCount X Z 0 f ∧
      Trace (TM.advance readRule) (scanning (.first p) raw o 0 0) (3*k+3) (returning (.done q) raw o k 0) ∧
      TM.advance readRule (returning (.done q) raw o k 0)=none ∧
      OAI.Computability.NearSquareRoot.VisitsAtMost readRule (scanning (.first p) raw o 0 0)
        (3*k+3) (12*k+16) := by
  refine ⟨dot p (slots sx sz X Z f),?_,paired_scan _ _ _ _ _ (slot_ready _ _ _ _ _ _ _ _ g),scan_halts _ _ _ _,pair_visits _ _ _ _⟩
  rw [column_sign]
  cases f with
  | zero => rfl
  | succ n => simp only [slots,hits,bitCount,dense_hits]

end Moonshot.AlignedWalsh.KeyTape

#print axioms Moonshot.AlignedWalsh.KeyTape.paired_scan
#print axioms Moonshot.AlignedWalsh.KeyTape.column_sign
#print axioms Moonshot.AlignedWalsh.KeyTape.scan_halts

#print axioms Moonshot.AlignedWalsh.KeyTape.pair_visits

#print axioms Moonshot.AlignedWalsh.KeyTape.slot_scan
