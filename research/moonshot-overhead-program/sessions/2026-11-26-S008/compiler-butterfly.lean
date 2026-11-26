import «compiler-controller»
import OAI.Computability.NearSquareRoot.VisitedCells

/-! One fused, home-restoring modular sum and difference in the original tape semantics. -/

namespace S008.Compiler.Butterfly

open OAI.Computability.IntegerMultiplication

def val : Bool → ℕ | false => 0 | true => 1

def plus (a b c : Bool) : Bool × Bool :=
  (xor (xor a b) c, (a && b) || (a && c) || (b && c))

def minus (a b c : Bool) : Bool × Bool :=
  (xor (xor a b) c, (!a && (b || c)) || (b && c))

private theorem plus_correct (a b c : Bool) :
    val (plus a b c).1 + 2*val (plus a b c).2 = val a + val b + val c := by
  cases a <;> cases b <;> cases c <;> decide

private theorem minus_correct (a b c : Bool) :
    val (minus a b c).1 + val b + val c = val a + 2*val (minus a b c).2 := by
  cases a <;> cases b <;> cases c <;> decide

structure Words where
  a : ℕ → Bool
  b : ℕ → Bool
  m : ℕ → Bool

structure Flags where
  sc : Bool
  db : Bool
  sb : Bool
  dc : Bool
  deriving DecidableEq, Repr

structure Candidates where
  sum : Bool × Bool
  diff : Bool × Bool
  deriving DecidableEq, Repr

def bitStep (f : Flags) (a b m : Bool) : Flags × Candidates :=
  let s := plus a b f.sc
  let d := minus a b f.db
  let sr := minus s.1 m f.sb
  let dr := plus d.1 m f.dc
  (⟨s.2,d.2,sr.2,dr.2⟩,⟨(s.1,sr.1),(d.1,dr.1)⟩)

def flags (s : Words) : ℕ → Flags
  | 0 => ⟨false,false,false,false⟩
  | i+1 => (bitStep (flags s i) (s.a i) (s.b i) (s.m i)).1

def candidates (s : Words) (i : ℕ) : Candidates :=
  (bitStep (flags s i) (s.a i) (s.b i) (s.m i)).2

def number (bits : ℕ → Bool) : ℕ → ℕ
  | 0 => 0
  | i+1 => number bits i + 2^i * val (bits i)

theorem number_lt (bits : ℕ → Bool) (w : ℕ) : number bits w < 2^w := by
  induction w with
  | zero => simp [number]
  | succ i ih =>
    cases hb : bits i <;> simp [number,hb,val,Nat.pow_succ] <;> omega

private theorem prove_add (a b out c : ℕ → Bool) (h0 : c 0 = false)
    (hs : ∀ i, val (out i)+2*val (c (i+1))=val (a i)+val (b i)+val (c i)) (n : ℕ) :
    number out n + 2^n*val (c n) = number a n + number b n := by
  induction n with
  | zero => simp [number,h0,val]
  | succ i ih =>
    have hi := congrArg (fun k : ℕ => 2^i*k) (hs i)
    simp only [Nat.mul_add] at hi
    simp only [number,Nat.pow_succ,Nat.mul_assoc]
    omega

private theorem prove_sub (a b out c : ℕ → Bool) (h0 : c 0 = false)
    (hs : ∀ i, val (out i)+val (b i)+val (c i)=val (a i)+2*val (c (i+1))) (n : ℕ) :
    number out n + number b n = number a n + 2^n*val (c n) := by
  induction n with
  | zero => simp [number,h0,val]
  | succ i ih =>
    have hi := congrArg (fun k : ℕ => 2^i*k) (hs i)
    simp only [Nat.mul_add] at hi
    simp only [number,Nat.pow_succ,Nat.mul_assoc]
    omega

def choose (f : Flags) : Bool × Bool := (f.sc || !f.sb, f.db)
def select (useSecond : Bool) (v : Bool × Bool) : Bool := if useSecond then v.2 else v.1

private theorem choose_number (v : ℕ → Bool × Bool) (c : Bool) (w : ℕ) :
    number (fun j => select c (v j)) w =
      if c then number (fun j => (v j).2) w else number (fun j => (v j).1) w := by
  cases c <;> rfl

/-- The selected words are the canonical residues of a+b and a-b for every positive
    representable modulus with reduced inputs. No inverse or power-of-two modulus is needed. -/
theorem arithmetic (s : Words) (w : ℕ) (ha : number s.a w < number s.m w)
    (hb : number s.b w < number s.m w) :
    number (fun j => select (choose (flags s w)).1 (candidates s j).sum) w =
      (if number s.m w ≤ number s.a w + number s.b w
       then number s.a w + number s.b w - number s.m w else number s.a w + number s.b w) ∧
    number (fun j => select (choose (flags s w)).2 (candidates s j).diff) w =
      (if number s.b w ≤ number s.a w then number s.a w - number s.b w
       else number s.a w + number s.m w - number s.b w) := by
  let sl := fun i => (candidates s i).sum.1
  let sr := fun i => (candidates s i).sum.2
  let dl := fun i => (candidates s i).diff.1
  let dr := fun i => (candidates s i).diff.2
  have hs := prove_add s.a s.b sl (fun i => (flags s i).sc) rfl
    (fun i => plus_correct (s.a i) (s.b i) (flags s i).sc) w
  have hd := prove_sub s.a s.b dl (fun i => (flags s i).db) rfl
    (fun i => minus_correct (s.a i) (s.b i) (flags s i).db) w
  have hsr := prove_sub sl s.m sr (fun i => (flags s i).sb) rfl
    (fun i => minus_correct (sl i) (s.m i) (flags s i).sb) w
  have hdr := prove_add dl s.m dr (fun i => (flags s i).dc) rfl
    (fun i => plus_correct (dl i) (s.m i) (flags s i).dc) w
  have bounds := And.intro (number_lt sl w) (And.intro (number_lt sr w)
    (And.intro (number_lt dl w) (And.intro (number_lt dr w) (number_lt s.m w))))
  rw [choose_number,choose_number]
  change (if (flags s w).sc || !(flags s w).sb then number sr w else number sl w) = _ ∧
    (if (flags s w).db then number dr w else number dl w) = _
  constructor
  · cases cs : (flags s w).sc <;> cases bs : (flags s w).sb <;>
      simp [cs,bs,val] at hs hsr ⊢ <;> split <;> omega
  · cases bd : (flags s w).db <;> cases cd : (flags s w).dc <;>
      simp [bd,cd,val] at hd hdr ⊢ <;> split <;> omega

inductive Port where
  | a | b | m | sum | diff
  deriving DecidableEq, Repr

instance : Fintype Port := Fintype.ofList [.a,.b,.m,.sum,.diff] (by intro t; cases t <;> decide)

inductive Stage where
  | forward (carry : Flags)
  | returning (sumSecond diffSecond : Bool)
  | halt
  deriving DecidableEq, Repr

def flagsList : List Flags := do
  let a ← [false,true]
  let b ← [false,true]
  let c ← [false,true]
  let d ← [false,true]
  pure ⟨a,b,c,d⟩

instance : Fintype Flags := Fintype.ofList flagsList (by
  rintro ⟨a,b,c,d⟩
  cases a <;> cases b <;> cases c <;> cases d <;> decide)

instance : Fintype Stage := Fintype.ofList (flagsList.map .forward ++
  [.returning false false,.returning false true,.returning true false,.returning true true,.halt]) (by
    intro s
    cases s with
    | forward f =>
      rcases f with ⟨a,b,c,d⟩
      cases a <;> cases b <;> cases c <;> cases d <;> decide
    | returning a b => cases a <;> cases b <;> decide
    | halt => decide)

def packed : Bool × Bool → Letter
  | (false,false) => .blank
  | (false,true) => .count
  | (true,b) => .bit b

def unpack : Letter → Option (Bool × Bool)
  | .blank => some (false,false)
  | .count => some (false,true)
  | .bit b => some (true,b)
  | _ => none

@[simp] theorem unpack_packed (v : Bool × Bool) : unpack (packed v) = some v := by
  rcases v with ⟨i,j⟩
  cases i <;> cases j <;> rfl

def replaceOutputs (old : Port → Letter) (sum diff : Letter) : Port → Letter
  | .sum => sum
  | .diff => diff
  | t => old t

def action (s : Port → Letter) (m : TM.Move) : Port → Letter × TM.Move := fun t => (s t,m)

def rule : TM.Rule Letter Stage Port := fun q r =>
  match q with
  | .forward f => match r .a,r .b,r .m with
    | .bit a,.bit b,.bit m =>
      let (g,out) := bitStep f a b m
      some (.forward g, action (replaceOutputs r (packed out.sum) (packed out.diff)) .right)
    | .delimiter,.delimiter,.delimiter =>
      some (.returning (choose f).1 (choose f).2,action r .left)
    | _,_,_ => none
  | .returning s d => match r .a with
    | .bit _ => match unpack (r .sum),unpack (r .diff) with
      | some u,some v => some (.returning s d,
          action (replaceOutputs r (.bit (select s u)) (.bit (select d v))) .left)
      | _,_ => none
    | .home => some (.halt,action r .right)
    | _ => none
  | .halt => none

abbrev Banks := Port → ℤ → Letter
abbrev Origins := Port → ℤ

structure Valid (s : Words) (w : ℕ) (raw : Banks) (o : Origins) : Prop where
  home : raw .a (o .a-1) = .home
  endA : raw .a (o .a+w) = .delimiter
  endB : raw .b (o .b+w) = .delimiter
  endM : raw .m (o .m+w) = .delimiter
  bitA : ∀ i : ℕ, i<w → raw .a (o .a+i) = .bit (s.a i)
  bitB : ∀ i : ℕ, i<w → raw .b (o .b+i) = .bit (s.b i)
  bitM : ∀ i : ℕ, i<w → raw .m (o .m+i) = .bit (s.m i)

def emit (s : Words) (choice : Bool × Bool) (isPaired : Bool) (base : Letter)
    (t : Port) (i : ℕ) : Letter :=
  match t with
  | .sum => if isPaired then packed (candidates s i).sum else .bit (select choice.1 (candidates s i).sum)
  | .diff => if isPaired then packed (candidates s i).diff else .bit (select choice.2 (candidates s i).diff)
  | _ => base

/-- `extent` cells have received candidates. The suffix from `pending` has been resolved. -/
def stageData (s : Words) (raw : Banks) (o : Origins) (choice : Bool × Bool)
    (extent pending : ℕ) : Banks := fun t z =>
  if o t ≤ z ∧ z < o t+extent then
    emit s choice (decide (z<o t+pending)) (raw t z) t (z-o t).toNat
  else raw t z

def frame (q : Stage) (d : Banks) (o : Origins) (pos : ℤ) : TM.Config Letter Stage Port :=
  ⟨q,fun t => atPos (d t) (o t+pos)⟩

private theorem read_at (a : ℤ → Letter) (p : ℤ) : (atPos a p).view 0 = a p := by simp [atPos]

private theorem write_at (a : ℤ → Letter) (p : ℤ) (v : Letter) (m : TM.Move) :
    (atPos a p).apply (v,m) = atPos (Function.update a p v) (p+m.shift) := by
  unfold atPos TM.Tape.apply
  congr 1
  funext i
  by_cases h : i+m.shift=0
  · have h₁ : p + m.shift + i = p := by omega
    simp [h,h₁]
  · have h₁ : p + m.shift + i = p+(i+m.shift) := by omega
    simp [h,h₁,Function.update_of_ne]

private theorem frame_step (q q' : Stage) (d d' : Banks) (o : Origins) (pos : ℤ)
    (written : Port → Letter) (m : TM.Move)
    (command : rule q (fun t => d t (o t+pos)) = some (q',action written m))
    (data : ∀ t, Function.update (d t) (o t+pos) (written t) = d' t) :
    TM.advance rule (frame q d o pos) = some (frame q' d' o (pos+m.shift)) := by
  unfold TM.advance frame
  simp only [read_at,command,Option.map_some,Option.some.injEq]
  apply congrArg (TM.Config.mk q')
  funext t
  simp [action,write_at,data,add_assoc]

private theorem frame_move (q q' : Stage) (d : Banks) (o : Origins) (pos : ℤ) (m : TM.Move)
    (command : rule q (fun t => d t (o t+pos)) = some (q',action (fun t => d t (o t+pos)) m)) :
    TM.advance rule (frame q d o pos) = some (frame q' d o (pos+m.shift)) :=
  frame_step q q' d d o pos _ m command (fun t => Function.update_eq_self (o t+pos) (d t))

private theorem stage_hit (s raw o choice) (extent pending i : ℕ) (t : Port) (h : i<extent) :
    stageData s raw o choice extent pending t (o t+i) =
      emit s choice (decide (i<pending)) (raw t (o t+i)) t i := by
  simp [stageData,h]

private theorem stage_edge (s raw o choice) (extent pending : ℕ) (t : Port) :
    stageData s raw o choice extent pending t (o t+extent) = raw t (o t+extent) := by simp [stageData]

private theorem sourceA (s raw o choice u j z) : stageData s raw o choice u j .a z = raw .a z := by
  simp [stageData,emit]

private theorem sourceB (s raw o choice u j z) : stageData s raw o choice u j .b z = raw .b z := by
  simp [stageData,emit]

private theorem sourceM (s raw o choice u j z) : stageData s raw o choice u j .m z = raw .m z := by
  simp [stageData,emit]

private theorem forward_cells (s raw o choice) (i : ℕ) (t : Port) :
    Function.update (stageData s raw o choice i i t) (o t+i)
      (replaceOutputs (fun u => stageData s raw o choice i i u (o u+i))
        (packed (candidates s i).sum) (packed (candidates s i).diff) t) =
      stageData s raw o choice (i+1) (i+1) t := by
  funext z
  by_cases eq : z=o t+i
  · subst z
    rw [Function.update_self,stage_hit _ _ _ _ _ _ _ _ (by omega)]
    simp only [Nat.lt_succ_self,decide_true]
    cases t <;> simp [emit,replaceOutputs,sourceA,sourceB,sourceM]
  · rw [Function.update_of_ne eq]
    have bnd : z<o t+(↑(i+1:ℕ):ℤ) ↔ z<o t+i := by omega
    simp only [stageData,bnd]

private theorem backward_cells (s raw o choice) (w i : ℕ) (t : Port) (h : i<w) :
    Function.update (stageData s raw o choice w (i+1) t) (o t+i)
      (replaceOutputs (fun u => stageData s raw o choice w (i+1) u (o u+i))
        (.bit (select choice.1 (candidates s i).sum)) (.bit (select choice.2 (candidates s i).diff)) t)
      = stageData s raw o choice w i t := by
  funext z
  by_cases eq : z=o t+i
  · subst z
    rw [Function.update_self,stage_hit _ _ _ _ _ _ _ _ h]
    simp only [Nat.lt_irrefl,decide_false]
    cases t <;> simp [emit,replaceOutputs,sourceA,sourceB,sourceM]
  · rw [Function.update_of_ne eq]
    have bnd : z<o t+(↑(i+1:ℕ):ℤ) ↔ z<o t+i := by omega
    simp only [stageData,bnd]

private theorem forward_step (s : Words) (raw : Banks) (o : Origins) (choice : Bool × Bool)
    (w i : ℕ) (good : Valid s w raw o) (h : i<w) :
    TM.advance rule (frame (.forward (flags s i)) (stageData s raw o choice i i) o i) =
      some (frame (.forward (flags s (i+1))) (stageData s raw o choice (i+1) (i+1)) o (i+1:ℕ)) := by
  let d := stageData s raw o choice i i
  let written := replaceOutputs (fun t => d t (o t+i)) (packed (candidates s i).sum)
    (packed (candidates s i).diff)
  have cmd : rule (.forward (flags s i)) (fun t => d t (o t+i)) =
      some (.forward (flags s (i+1)),action written .right) := by
    simp only [rule,d,sourceA,sourceB,sourceM,good.bitA i h,good.bitB i h,good.bitM i h]
    rfl
  simpa only [TM.Move.shift,Int.natCast_succ] using
    frame_step _ _ d _ o i written .right cmd (forward_cells s raw o choice i)

private theorem forward_tour (s raw o choice w) (good : Valid s w raw o) (i : ℕ) (h : i≤w) :
    Trace (TM.advance rule) (frame (.forward (flags s 0)) (stageData s raw o choice 0 0) o 0)
      i (frame (.forward (flags s i)) (stageData s raw o choice i i) o i) := by
  induction i with
  | zero => exact .nil _
  | succ j ih =>
    exact (ih (by omega)).trans (Trace.single (forward_step s raw o choice w j good (by omega)))

private theorem end_turn (s raw o w) (good : Valid s w raw o) :
    let ch := choose (flags s w)
    let d := stageData s raw o ch w w
    TM.advance rule (frame (.forward (flags s w)) d o w) =
      some (frame (.returning ch.1 ch.2) d o ((w:ℤ)-1)) := by
  dsimp only
  apply frame_move _ _ _ _ _ .left
  simp [rule,sourceA,sourceB,sourceM,good.endA,good.endB,good.endM]

private theorem backward_step (s raw o) (choice : Bool × Bool) (w i : ℕ)
    (good : Valid s w raw o) (h : i<w) :
    TM.advance rule (frame (.returning choice.1 choice.2) (stageData s raw o choice w (i+1)) o i) =
      some (frame (.returning choice.1 choice.2) (stageData s raw o choice w i) o ((i:ℤ)-1)) := by
  let q := Stage.returning choice.1 choice.2
  let d := stageData s raw o choice w (i+1)
  let wr := replaceOutputs (fun t => d t (o t+i))
    (.bit (select choice.1 (candidates s i).sum)) (.bit (select choice.2 (candidates s i).diff))
  have cmd : rule q (fun t => d t (o t+i)) = some (q,action wr .left) := by
    simp [q,rule,d,wr,good.bitA i h,stage_hit _ _ _ _ _ _ _ _ h,emit]
  exact frame_step q q d _ o i wr .left cmd (fun t => backward_cells s raw o choice w i t h)

private theorem backward_tour (s raw o) (choice : Bool × Bool) (w : ℕ) (good : Valid s w raw o)
    (j : ℕ) (h : j≤w) :
    let q := Stage.returning choice.1 choice.2
    Trace (TM.advance rule) (frame q (stageData s raw o choice w j) o ((j:ℤ)-1))
      j (frame q (stageData s raw o choice w 0) o (-1)) := by
  dsimp only
  induction j with
  | zero => exact .nil _
  | succ i ih =>
    have start := backward_step s raw o choice w i good (by omega)
    have path := Trace.cons start (ih (by omega))
    simpa [Nat.add_comm] using path

private theorem home_turn (s raw o) (choice : Bool × Bool) (w : ℕ) (good : Valid s w raw o) :
    let d := stageData s raw o choice w 0
    TM.advance rule (frame (.returning choice.1 choice.2) d o (-1)) = some (frame .halt d o 0) := by
  dsimp only
  have cmd : rule (.returning choice.1 choice.2) (fun t => stageData s raw o choice w 0 t (o t+(-1))) =
    some (.halt,action (fun t => stageData s raw o choice w 0 t (o t+(-1))) .right) := by
    simp only [rule,sourceA,show o .a + -1 = o .a - 1 by omega,good.home]
  exact frame_move _ _ _ _ _ .right cmd

def output (s raw o w) := stageData s raw o (choose (flags s w)) w 0

private theorem initial (s raw o choice) : stageData s raw o choice 0 0 = raw := by
  funext t z
  simp [stageData]

/-- Five independently movable ports. Both arithmetic destinations may initially contain
    arbitrary symbols. Their exterior tapes and all three full sources survive exactly. -/
theorem butterfly (s : Words) (raw : Banks) (o : Origins) (w : ℕ) (good : Valid s w raw o) :
    Trace (TM.advance rule) (frame (.forward (flags s 0)) raw o 0) (2*w+2)
      (frame .halt (output s raw o w) o 0) := by
  let ch := choose (flags s w)
  have path := (((forward_tour s raw o ch w good w le_rfl).trans
    (Trace.single (end_turn s raw o w good))).trans (backward_tour s raw o ch w good w le_rfl)).trans
    (Trace.single (home_turn s raw o ch w good))
  rw [initial] at path
  change Trace _ _ (w+1+w+1) (frame .halt (output s raw o w) o 0) at path
  simpa only [show w+1+w+1=2*w+2 by omega] using path

theorem butterfly_halts (d : Banks) (o : Origins) : TM.advance rule (frame .halt d o 0) = none := rfl

theorem sum_cell (s raw o w) (i : ℕ) (h : i<w) :
    output s raw o w .sum (o .sum+i) = .bit (select (choose (flags s w)).1 (candidates s i).sum) := by
  simp [output,stage_hit _ _ _ _ _ _ _ _ h,emit]

theorem diff_cell (s raw o w) (i : ℕ) (h : i<w) :
    output s raw o w .diff (o .diff+i) = .bit (select (choose (flags s w)).2 (candidates s i).diff) := by
  simp [output,stage_hit _ _ _ _ _ _ _ _ h,emit]

theorem retained (s raw o w) :
    output s raw o w .a = raw .a ∧ output s raw o w .b = raw .b ∧ output s raw o w .m = raw .m := by
  exact ⟨funext (fun z => sourceA _ _ _ _ _ _ z),funext (fun z => sourceB _ _ _ _ _ _ z),
    funext (fun z => sourceM _ _ _ _ _ _ z)⟩

theorem exterior (s raw o) (w : ℕ) (t : Port) (z : ℤ) (h : z<o t ∨ o t+w≤z) :
    output s raw o w t z = raw t z := by
  simp only [output,stageData]
  rw [ite_eq_right (by omega)]

private theorem backward_part (s raw o) (ch : Bool × Bool) (w : ℕ) (good : Valid s w raw o)
    (j n : ℕ) (bound : j+n≤w) :
    let q := Stage.returning ch.1 ch.2
    Trace (TM.advance rule) (frame q (stageData s raw o ch w (j+n)) o ((j+n:ℕ)-1:ℤ))
      n (frame q (stageData s raw o ch w j) o ((j:ℤ)-1)) := by
  dsimp only
  induction n with
  | zero => exact .nil _
  | succ n ih =>
    rw [show j+(n+1)=j+n+1 by omega]
    rw [show (↑(j+n+1:ℕ):ℤ)-1 = ↑(j+n:ℕ) by omega]
    simpa only [Nat.add_comm 1 n] using Trace.cons
      (backward_step s raw o ch w (j+n) good (by omega)) (ih (by omega))

private theorem returning_prefix (s raw o) (w : ℕ) (good : Valid s w raw o)
    (j n : ℕ) (eq : j+n=w) :
    let ch := choose (flags s w)
    Trace (TM.advance rule) (frame (.forward (flags s 0)) raw o 0)
      (w+1+n) (frame (.returning ch.1 ch.2) (stageData s raw o ch w j) o ((j:ℤ)-1)) := by
  dsimp only
  let ch := choose (flags s w)
  have a := (forward_tour s raw o ch w good w le_rfl).trans (Trace.single (end_turn s raw o w good))
  rw [initial] at a
  have b := backward_part s raw o ch w good j n (le_of_eq eq)
  dsimp only at b
  rw [eq] at b
  exact a.trans b

open OAI.Computability.NearSquareRoot

private theorem fences (s raw o) (w : ℕ) (good : Valid s w raw o)
    (t : ℕ) (h : t≤2*w+2) (C : TM.Config Letter Stage Port)
    (trace : Trace (TM.advance rule) (frame (.forward (flags s 0)) raw o 0) t C) (p : Port) :
    o p-1 ≤ (C.tape p).pos ∧ (C.tape p).pos ≤ o p+w := by
  by_cases endtime : t=2*w+2
  · subst t
    rw [trace_endpoint_unique trace (butterfly s raw o w good)]
    change o p-1 ≤ o p+0 ∧ o p+0≤o p+w
    omega
  by_cases forward : t≤w
  · have path := forward_tour s raw o (choose (flags s w)) w good t forward
    rw [initial] at path
    rw [trace_endpoint_unique trace path]
    change o p-1≤o p+t ∧ o p+t≤o p+w
    omega
  · let j := 2*w+1-t
    let n := t-(w+1)
    have eq : j+n=w := by dsimp [j,n]; omega
    have time : w+1+n=t := by dsimp [n]; omega
    have path := returning_prefix s raw o w good j n eq
    rw [time] at path
    rw [trace_endpoint_unique trace path]
    change o p-1≤o p+((j:ℤ)-1) ∧ o p+((j:ℤ)-1)≤o p+w
    omega

/-- Characterizes every physical tape/address position reached up to halt, including the
    initial and final configurations and the one-cell turn at the left marker. -/
theorem visited_iff (s raw o) (w : ℕ) (good : Valid s w raw o) (p : Port) (z : ℤ) :
    (p,z) ∈ visitedCells rule (frame (.forward (flags s 0)) raw o 0) (2*w+2) ↔
      o p-1≤z ∧ z≤o p+w := by
  constructor
  · rintro ⟨t,h,C,ht,hp⟩
    change (C.tape p).pos = z at hp
    rw [← hp]
    exact fences s raw o w good t h C ht p
  · intro h
    by_cases first : z=o p-1
    · have path := returning_prefix s raw o w good 0 w (Nat.zero_add _)
      refine ⟨w+1+w,by omega,_,path,?_⟩
      change o p+((0:ℤ)-1)=z
      omega
    · let j := (z-o p).toNat
      have hj : j≤w := by dsimp [j]; omega
      have path := forward_tour s raw o (choose (flags s w)) w good j hj
      rw [initial] at path
      refine ⟨j,by omega,_,path,?_⟩
      change o p+j=z
      dsimp [j]
      omega

theorem port_count : Fintype.card Port=5 := by decide

theorem visits (s raw o) (w : ℕ) (good : Valid s w raw o) :
    VisitsAtMost rule (frame (.forward (flags s 0)) raw o 0) (2*w+2) (5*(w+2)) := by
  have bound := visitsAtMost_of_tape_fences (fun p => o p-1) (fun p => o p+w)
    (fences s raw o w good)
  have span (p : Port) : (o p+w+1-(o p-1)).toNat=w+2 := by omega
  simpa [span,port_count] using bound

def readBit : Letter → Bool
  | .bit b => b
  | _ => false

def readWord {Q : Type} (C : TM.Config Letter Q Port) (t : Port) (p : ℤ) (w : ℕ) : ℕ :=
  number (fun j => readBit ((C.tape t).absolute (p+j))) w

theorem number_agrees (a b : ℕ → Bool) (w : ℕ) (h : ∀ i, i<w → a i=b i) :
    number a w = number b w := by
  induction w with
  | zero => rfl
  | succ j ih => simp only [number,ih (fun i hi => h i (by omega)),h j (by omega)]

theorem frame_cell (q : Stage) (d o j z t) : ((frame q d o j).tape t).absolute z = d t z := by
  simp [frame,TM.Tape.absolute,atPos]

private theorem number_sum (a b m : ℕ) (ha : a<m) (hb : b<m) :
    (if m≤a+b then a+b-m else a+b) = (a+b)%m := by
  by_cases le : m≤a+b
  · rw [ite_eq_left le,Nat.mod_eq_sub_mod le,Nat.mod_eq_of_lt (by omega)]
  · simp [le,Nat.mod_eq_of_lt (by omega : a+b<m)]

private theorem number_diff (a b m : ℕ) (ha : a<m) (hb : b<m) :
    (if b≤a then a-b else a+m-b) = (a+m-b)%m := by
  by_cases le : b≤a
  · have id : a+m-b = (a-b)+m := by omega
    simp [le,id,Nat.mod_eq_of_lt (by omega : a-b<m)]
  · simp [le,Nat.mod_eq_of_lt (by omega : a+m-b<m)]

/-- Literal cells of the halting configuration encode the modular butterfly, in canonical
    nonnegative representatives. The two outputs have arbitrary, separately chosen origins. -/
theorem output_numbers (s raw o w) (ha : number s.a w < number s.m w) (hb : number s.b w < number s.m w) :
    let C := frame .halt (output s raw o w) o 0
    readWord C .sum (o .sum) w = (number s.a w + number s.b w) % number s.m w ∧
    readWord C .diff (o .diff) w = (number s.a w + number s.m w - number s.b w) % number s.m w := by
  dsimp only [readWord]
  simp only [frame_cell]
  have sumEq : number (fun j => readBit (output s raw o w .sum (o .sum+j))) w =
      number (fun j => select (choose (flags s w)).1 (candidates s j).sum) w :=
    number_agrees _ _ w (fun i hi => by simp only [sum_cell s raw o w i hi,readBit])
  have diffEq : number (fun j => readBit (output s raw o w .diff (o .diff+j))) w =
      number (fun j => select (choose (flags s w)).2 (candidates s j).diff) w :=
    number_agrees _ _ w (fun i hi => by simp only [diff_cell s raw o w i hi,readBit])
  have ar := arithmetic s w ha hb
  exact ⟨sumEq.trans (ar.1.trans (number_sum _ _ _ ha hb)),diffEq.trans (ar.2.trans (number_diff _ _ _ ha hb))⟩

theorem resources (s raw o w) (good : Valid s w raw o) (ha : number s.a w < number s.m w)
    (hb : number s.b w < number s.m w) :
    let begin := frame (.forward (flags s 0)) raw o 0
    ∃ C, Trace (TM.advance rule) begin (2*w+2) C ∧ TM.advance rule C=none ∧
      (∀ p, (C.tape p).pos=o p) ∧
      readWord C .sum (o .sum) w=(number s.a w+number s.b w)%number s.m w ∧
      readWord C .diff (o .diff) w=(number s.a w+number s.m w-number s.b w)%number s.m w ∧
      VisitsAtMost rule begin (2*w+2) (5*(w+2)) := by
  dsimp only
  let C := frame .halt (output s raw o w) o 0
  have out := output_numbers s raw o w ha hb
  exact ⟨C,butterfly s raw o w good,butterfly_halts _ _,fun p => by simp [C,frame,atPos],
    out.1,out.2,visits s raw o w good⟩

private def locate (o : Origins) (w : ℕ) : (Port × Fin (w+2)) ↪ (Port × ℤ) where
  toFun x := (x.1,o x.1-1+x.2.val)
  inj' := by
    rintro ⟨p,i⟩ ⟨q,j⟩ eq
    obtain rfl : p=q := congrArg Prod.fst eq
    have hj : o p-1+(i.val:ℤ)=o p-1+(j.val:ℤ) := congrArg Prod.snd eq
    have e : i=j := Fin.ext (by omega)
    simp [e]

/-- The cardinality itself is sharp, including the extreme cell on every tape. -/
theorem exact_space (s raw o w) (good : Valid s w raw o) :
    (visitedCells rule (frame (.forward (flags s 0)) raw o 0) (2*w+2)).ncard=5*(w+2) := by
  let covered := (Finset.univ : Finset (Port × Fin (w+2))).map (locate o w)
  have eq : visitedCells rule (frame (.forward (flags s 0)) raw o 0) (2*w+2) = (covered : Set (Port × ℤ)) := by
    ext ⟨p,z⟩
    rw [visited_iff s raw o w good]
    change (_ ∧ _) ↔ (p,z) ∈ (Finset.univ.map (locate o w))
    rw [Finset.mem_map]
    constructor
    · intro h
      let j : Fin (w+2) := ⟨(z-(o p-1)).toNat,by omega⟩
      refine ⟨(p,j),Finset.mem_univ _,?_⟩
      change (p,o p-1+(j.val:ℤ))=(p,z)
      dsimp [j]
      congr 1
      omega
    · rintro ⟨⟨q,j⟩,_,same⟩
      change (q,o q-1+(j.val:ℤ))=(p,z) at same
      obtain rfl : q=p := congrArg Prod.fst same
      have hj : o q-1+(j.val:ℤ)=z := congrArg Prod.snd same
      omega
  rw [eq,Set.ncard_coe_finset]
  simp [covered,port_count]

theorem stage_count : Fintype.card Stage=21 := by decide

end S008.Compiler.Butterfly
