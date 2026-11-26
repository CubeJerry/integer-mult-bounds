import «compiler-unary»
import «compiler-indexed-transfer»

/-! A complete binary-addressed memory instruction, including conversion and private erasure. -/

namespace S008.Compiler.Binary

open OAI.Computability.IntegerMultiplication

inductive Port where
  | bank | digits | value | index | work
  deriving DecidableEq, Repr, Inhabited

instance : Fintype Port := Fintype.ofList [.bank,.digits,.value,.index,.work] (by intro x; cases x <;> decide)

inductive Stage where
  | prepare (p : Unary.Phase) | useWord (q : Transfer.Stage)
  | erase | back | done
  deriving DecidableEq, Repr, Inhabited

instance : Fintype Stage := Fintype.ofList
  [.prepare .read,.prepare (.first false),.prepare (.first true),
   .prepare (.second false),.prepare (.second true),.prepare .restore,.prepare .suffix,
   .prepare (.home .before),.prepare (.home .after),.prepare (.home .finalOutput),
   .prepare (.home .finalDigits),.prepare .done,
   .useWord (.seek .check),.useWord (.seek .scan),.useWord (.seek .done),.useWord .copy,
   .useWord (.home .bank),.useWord (.home .index),.useWord (.home .value),.useWord .done,
   .erase,.back,.done] (by
   intro k
   cases k with
   | prepare p =>
      cases p with
      | first b => cases b <;> decide
      | second b => cases b <;> decide
      | home h => cases h <;> decide
      | _ => decide
   | useWord q =>
      cases q with
      | seek p => cases p <;> decide
      | home h => cases h <;> decide
      | _ => decide
   | _ => decide)

structure Wiring (I : Type) where
  localPort : Port → Option I
  ambient : I → Port
  inverse : ∀ i, localPort (ambient i) = some i

def preparation : Wiring Unary.Port where
  localPort
    | .digits => some .digits | .index => some .output | .work => some .work | _ => none
  ambient
    | .digits => .digits | .output => .index | .work => .work
  inverse i := by cases i <;> rfl

def access : Wiring Transfer.Port where
  localPort
    | .bank => some .bank | .index => some .index | .value => some .value | _ => none
  ambient
    | .bank => .bank | .index => .index | .value => .value
  inverse i := by cases i <;> rfl

def bridge {I Q : Type} (small : TM.Rule Letter Q I) (w : Wiring I) (tag : Q → Stage)
    (after : Q → Option Stage) (q : Q) (r : Port → Letter) :
    Option (Stage × (Port → Letter × TM.Move)) :=
  match small q (fun i => r (w.ambient i)) with
  | some (go,a) => some (tag go, fun j => match w.localPort j with
    | some i => a i
    | none => (r j,.stay))
  | none => (after q).map (fun go => (go,fun j => (r j,.stay)))

def prepared : Unary.Phase → Option Stage
  | .done => some (.useWord (.seek .check)) | _ => none

def used : Transfer.Stage → Option Stage
  | .done => some .erase | _ => none

def onIndex (r : Port → Letter) (op : Letter × TM.Move) (t : Port) : Letter × TM.Move :=
  if t = .index then op else (r t,.stay)

def rule (store : Bool) : TM.Rule Letter Stage Port := fun q r =>
  match q with
  | .prepare p => bridge Unary.rule preparation .prepare prepared p r
  | .useWord p => bridge (Transfer.rule store) access .useWord used p r
  | .erase => match r .index with
    | .count => some (.erase,onIndex r (.blank,.right))
    | .delimiter => some (.back,onIndex r (.blank,.left))
    | _ => none
  | .back =>
     if r .index = .home then some (.done,onIndex r (.home,.right))
     else some (.back,onIndex r (r .index,.left))
  | .done => none

def embed {I Q : Type} (w : Wiring I) (tag : Q → Stage) (retained : Port → TM.Tape Letter)
    (x : TM.Config Letter Q I) : TM.Config Letter Stage Port :=
  ⟨tag x.pc, fun t => match w.localPort t with
    | some i => x.tape i | none => retained t⟩

private theorem cfg_ext {q : Stage} {f g : Port → TM.Tape Letter} (h : ∀ t, f t = g t) :
    (TM.Config.mk q f) = (TM.Config.mk q g) := congrArg (TM.Config.mk q) (funext h)

private theorem still (v : TM.Tape Letter) : v.apply (v.view 0,.stay) = v := by
  cases v with
  | mk a f =>
    simp only [TM.Tape.apply,TM.Move.shift,Int.add_zero]
    congr 1
    funext j
    by_cases e : j=0 <;> simp [e]

private theorem simulate_one {I Q : Type} (small : TM.Rule Letter Q I) (big : TM.Rule Letter Stage Port)
    (w : Wiring I) (tag : Q → Stage) (after : Q → Option Stage)
    (run : ∀ q r, big (tag q) r = bridge small w tag after q r)
    (f : Port → TM.Tape Letter) {x y : TM.Config Letter Q I} (step : TM.advance small x = some y) :
    TM.advance big (embed w tag f x) = some (embed w tag f y) := by
  have raw : (fun i => ((embed w tag f x).tape (w.ambient i)).view 0) =
      fun i => (x.tape i).view 0 := by
    funext i
    simp [embed,w.inverse]
  unfold TM.advance at step ⊢
  change (big (tag x.pc) (fun t => ((embed w tag f x).tape t).view 0)).map _ = _
  rw [run]
  unfold bridge
  rw [raw]
  cases hs : small x.pc (fun i => (x.tape i).view 0) with
  | none => simp [hs] at step
  | some pair =>
    rcases pair with ⟨go,a⟩
    simp only [hs,Option.map_some,Option.some.injEq] at step
    subst y
    simp only [Option.map_some,Option.some.injEq]
    apply cfg_ext
    intro t
    cases h : w.localPort t with
    | some i => simp [embed,h]
    | none => simpa [embed,h] using still (f t)

private theorem simulate {I Q : Type} (small : TM.Rule Letter Q I) (big : TM.Rule Letter Stage Port)
    (w : Wiring I) (tag : Q → Stage) (after : Q → Option Stage)
    (run : ∀ q r, big (tag q) r = bridge small w tag after q r)
    (f : Port → TM.Tape Letter) {x y : TM.Config Letter Q I} {n : ℕ}
    (trace : Trace (TM.advance small) x n y) :
    Trace (TM.advance big) (embed w tag f x) n (embed w tag f y) := by
  induction trace with
  | nil => exact .nil _
  | cons step _ tail => exact .cons (simulate_one small big w tag after run f step) tail


def withIndex (q : Stage) (f : Port → TM.Tape Letter) (a : ℤ → Letter) (p : ℤ) :
    TM.Config Letter Stage Port := ⟨q, fun t => if t = .index then atPos a p else f t⟩

private theorem read_at (a : ℤ → Letter) (p : ℤ) : (atPos a p).view 0 = a p := by simp [atPos]

private theorem tape_update (a : ℤ → Letter) (p : ℤ) (w : Letter) (m : TM.Move) :
    (atPos a p).apply (w,m) = atPos (Function.update a p w) (p+m.shift) := by
  unfold atPos TM.Tape.apply
  congr 1
  funext j
  by_cases z : j+m.shift=0
  · have z' : p+m.shift+j=p := by omega
    simp [z,z']
  · have p' : p+m.shift+j = p+(j+m.shift) := by omega
    simp [z,Function.update_of_ne,p']

private theorem index_step (store : Bool) (f : Port → TM.Tape Letter) (a : ℤ → Letter)
    (p : ℤ) (q q' : Stage) (w : Letter) (m : TM.Move)
    (hr : ∀ r, r .index = a p → rule store q r = some (q',onIndex r (w,m))) :
    TM.advance (rule store) (withIndex q f a p) =
      some (withIndex q' f (Function.update a p w) (p+m.shift)) := by
  unfold TM.advance
  have e := hr (fun t => ((withIndex q f a p).tape t).view 0) (by simp [withIndex,read_at])
  change (rule store q _).map _ = _
  rw [e]
  simp only [Option.map_some,Option.some.injEq]
  apply cfg_ext
  intro t
  cases t <;> simp [withIndex,onIndex,still,tape_update]

private def erasing (j i : ℕ) (z : ℤ) : Letter :=
  if z=(i:ℤ) then .delimiter else Unary.un j i z

private theorem drop_mark (j i : ℕ) (h : j<i) :
    Function.update (erasing j i) (j:ℤ) .blank = erasing (j+1) i := by
  funext z
  by_cases e : z=(j:ℤ)
  · subst z
    simp [erasing,Unary.un,show (j:ℤ) ≠ i by omega]
  · rw [Function.update_of_ne e]
    unfold erasing Unary.un
    split_ifs <;> first | rfl | omega

private theorem clear_mark (store : Bool) (f : Port → TM.Tape Letter) (j i : ℕ) (h : j<i) :
    TM.advance (rule store) (withIndex .erase f (erasing j i) j) =
      some (withIndex .erase f (erasing (j+1) i) (j+1:ℕ)) := by
  have read : erasing j i (j:ℤ) = .count := by simp [erasing,Unary.un,show (j:ℤ) ≠ i by omega,h]
  have a := index_step store f (erasing j i) j .erase .erase .blank .right
    (fun r hr => by simp [rule,hr,read])
  simpa [drop_mark j i h,TM.Move.shift] using a

private theorem clear_marks (store : Bool) (f : Port → TM.Tape Letter) (i : ℕ) :
    Trace (TM.advance (rule store)) (withIndex .erase f (Unary.closed i) 0) i
      (withIndex .erase f (erasing i i) i) := by
  suffices go : ∀ j : ℕ, j≤i → Trace (TM.advance (rule store))
      (withIndex .erase f (Unary.closed i) 0) j (withIndex .erase f (erasing j i) j)
    from go i (by omega)
  intro j hj
  induction j with
  | zero => exact .nil _
  | succ j ih => exact (ih (by omega)).trans (Trace.single (clear_mark store f j i (by omega)))

private theorem remove_delimiter (i : ℕ) :
    Function.update (erasing i i) (i:ℤ) .blank = Unary.un 0 0 := by
  funext z
  by_cases e : z=(i:ℤ)
  · subst z
    simp [Unary.un]
  · rw [Function.update_of_ne e]
    unfold erasing Unary.un
    split_ifs <;> first | rfl | omega

private theorem cross_end (store : Bool) (f : Port → TM.Tape Letter) (i : ℕ) :
    TM.advance (rule store) (withIndex .erase f (erasing i i) i) =
      some (withIndex .back f (Unary.un 0 0) ((i:ℤ)-1)) := by
  have a := index_step store f (erasing i i) i .erase .back .blank .left
    (fun r h => by simp [rule,h,erasing])
  simpa [remove_delimiter,TM.Move.shift,sub_eq_add_neg] using a

private theorem rewind (store : Bool) (f : Port → TM.Tape Letter) (i : ℕ) :
    Trace (TM.advance (rule store)) (withIndex .back f (Unary.un 0 0) ((i:ℤ)-1)) (i+1)
      (withIndex .done f (Unary.un 0 0) 0) := by
  induction i with
  | zero =>
    have r : Unary.un 0 0 (-1) = .home := by simp [Unary.un]
    have a := index_step store f (Unary.un 0 0) (-1) .back .done .home .right
      (fun v h => by simp [rule,h,r])
    rw [← r,Function.update_eq_self] at a
    simpa [TM.Move.shift] using Trace.single a
  | succ i ih =>
    have r : Unary.un 0 0 (i:ℤ) = .blank := by simp [Unary.un]
    have a := index_step store f (Unary.un 0 0) i .back .back (Unary.un 0 0 i) .left
      (fun v h => by simp [rule,h,r])
    rw [Function.update_eq_self] at a
    have eqp : (↑(i+1:ℕ):ℤ)-1 = i := by omega
    simpa [eqp,TM.Move.shift,sub_eq_add_neg,Nat.add_assoc,Nat.add_left_comm,Nat.add_comm]
      using Trace.cons a ih

private theorem cleanup (store : Bool) (f : Port → TM.Tape Letter) (i : ℕ) :
    Trace (TM.advance (rule store)) (withIndex .erase f (Unary.closed i) 0) (2*i+2)
      (withIndex .done f (Unary.un 0 0) 0) := by
  have path := ((clear_marks store f i).trans (Trace.single (cross_end store f i))).trans (rewind store f i)
  convert path using 1
  omega


def payload (a z : ℤ → Letter) (i : ℕ) : Transfer.BankData
  | .bank => a | .index => Unary.closed i | .value => z

def homes (p q : ℤ) : Transfer.Heads
  | .bank => p | .index => 0 | .value => q

def command (s : Stage) (a d z : ℤ → Letter) (p q : ℤ) : TM.Config Letter Stage Port :=
  ⟨s,fun
    | .bank => atPos a p | .digits => atPos d 0 | .value => atPos z q
    | .index | .work => atPos (Unary.un 0 0) 0⟩

def output (store : Bool) (a z : ℤ → Letter) (p q : ℤ) (b i : ℕ) :
    Transfer.BankData := Transfer.copied store (payload a z i) (Transfer.slot (homes p q) b i) b

structure Input (a d z : ℤ → Letter) (p q : ℤ) (b : ℕ) (xs : List Bool) : Prop where
  binary : Unary.Input d xs
  bankHome : a (p-1) = .home
  valueHome : z (q-1) = .home
  bank : ∀ j : ℕ, j ≤ Unary.eval 0 xs → recordAt a (p+↑(j*(b+1) : ℕ)) b
  value : recordAt z q b

private theorem prepared_valid (a d z : ℤ → Letter) (p q : ℤ) (b : ℕ) (xs : List Bool)
    (h : Input a d z p q b xs) :
    Transfer.Canonical (payload a z (Unary.eval 0 xs)) (homes p q) b (Unary.eval 0 xs) := by
  constructor
  · intro t
    cases t with
    | bank => exact h.bankHome
    | value => exact h.valueHome
    | index => exact Unary.home_at _
  · exact h.bank
  · intro j small
    simpa only [payload,homes,Int.zero_add] using Unary.mark_at (Unary.eval 0 xs) j small
  · simpa only [payload,homes,Int.zero_add] using Unary.stop_at (Unary.eval 0 xs)
  · exact h.value

private theorem next_mode (store : Bool) (x y : TM.Config Letter Stage Port)
    (next : ∀ r, rule store x.pc r = some (y.pc,fun t => (r t,.stay)))
    (same : ∀ t, x.tape t = y.tape t) : TM.advance (rule store) x = some y := by
  cases y with
  | mk q f =>
    unfold TM.advance
    rw [next]
    simp only [Option.map_some,Option.some.injEq]
    apply cfg_ext
    intro t
    exact (still (x.tape t)).trans (same t)

/-- One fixed physical instruction accepts a padded binary address, loads or stores the
    selected arbitrary word, erases the generated address, and restores every head. -/
theorem binary_access (store : Bool) (a d z : ℤ → Letter) (p q : ℤ) (b : ℕ) (xs : List Bool)
    (h : Input a d z p q b xs) :
    let i := Unary.eval 0 xs
    let result := output store a z p q b i
    Trace (TM.advance (rule store)) (command (.prepare .read) a d z p q)
      (i*(2*b+15)+3*b+8*xs.length+19-5*Unary.ones xs)
      (command .done (result .bank) d (result .value) p q) := by
  let i := Unary.eval 0 xs
  let result := output store a z p q b i
  let start := command (.prepare .read) a d z p q
  let finish := command .done (result .bank) d (result .value) p q
  let ubase := Unary.frame .read d 0 0 0 0 0 0
  let uout := Unary.cfg .done (Unary.triple d (Unary.closed i) (Unary.un 0 0)) (Unary.triple 0 0 0)
  let tbase := Transfer.cfg (.seek .check) (payload a z i) (homes p q)
  let tout := Transfer.cfg .done result (homes p q)
  have u := simulate Unary.rule (rule store) preparation .prepare prepared (by intros; rfl)
    start.tape (Unary.binary_to_unary d xs h.binary)
  change Trace _ (embed preparation .prepare start.tape ubase) _ (embed preparation .prepare start.tape uout) at u
  have first : embed preparation .prepare start.tape ubase = start := by
    apply cfg_ext
    intro t
    cases t <;> rfl
  rw [first] at u
  have enter := next_mode store (embed preparation .prepare start.tape uout)
    (embed access .useWord start.tape tbase) (by intros; rfl) (by intro t; cases t <;> rfl)
  have actual := simulate (Transfer.rule store) (rule store) access .useWord used (by intros; rfl)
    start.tape (Transfer.indexed_access store (payload a z i) (homes p q) b i
      (prepared_valid a d z p q b xs h))
  change Trace _ (embed access .useWord start.tape tbase) _ (embed access .useWord start.tape tout) at actual
  have clean := next_mode store (embed access .useWord start.tape tout)
    (withIndex .erase finish.tape (Unary.closed i) 0) (by intros; rfl) (by intro t; cases t <;> rfl)
  have tail := cleanup store finish.tape i
  have last : withIndex .done finish.tape (Unary.un 0 0) 0 = finish := by
    apply cfg_ext
    intro t
    cases t <;> rfl
  rw [last] at tail
  have full := ((((u.trans (Trace.single enter)).trans actual).trans (Trace.single clean)).trans tail)
  change Trace _ start _ finish
  convert full using 1
  have bill := Unary.cost_value 0 xs
  change Unary.cost 0 xs+5*Unary.ones xs+7*0 = 7*i+7*xs.length at bill
  change i*(2*b+15)+3*b+8*xs.length+19-5*Unary.ones xs =
    (9*i+8*xs.length+6-5*Unary.ones xs)+1+(i*(2*b+4)+3*b+9)+1+(2*i+2)
  simp only [Nat.mul_add]
  omega

theorem binary_access_halts (store : Bool) (a d z : ℤ → Letter) (p q : ℤ) :
    TM.advance (rule store) (command .done a d z p q) = none := rfl

#print axioms binary_access
#print axioms binary_access_halts


theorem load_keeps_bank (a z : ℤ → Letter) (p q : ℤ) (b i : ℕ) :
    output false a z p q b i .bank = a := rfl

theorem store_keeps_value (a z : ℤ → Letter) (p q : ℤ) (b i : ℕ) :
    output true a z p q b i .value = z := rfl

theorem load_word (a z : ℤ → Letter) (p q : ℤ) (b i j : ℕ) (h : j<b) :
    output false a z p q b i .value (q+j) = a (p+↑(i*(b+1):ℕ)+j) :=
  Transfer.loaded_bit (payload a z i) (homes p q) b i j h

theorem store_word (a z : ℤ → Letter) (p q : ℤ) (b i j : ℕ) (h : j<b) :
    output true a z p q b i .bank (p+↑(i*(b+1):ℕ)+j) = z (q+j) :=
  Transfer.stored_bit (payload a z i) (homes p q) b i j h

theorem store_preserves_exterior (a z : ℤ → Letter) (p q : ℤ) (b i : ℕ) (x : ℤ)
    (outside : ¬(p+↑(i*(b+1):ℕ)≤x ∧ x<p+↑(i*(b+1):ℕ)+↑b)) :
    output true a z p q b i .bank x = a x :=
  Transfer.store_other (payload a z i) (homes p q) b i x outside

theorem load_preserves_exterior (a z : ℤ → Letter) (p q : ℤ) (b i : ℕ) (x : ℤ)
    (outside : ¬(q≤x ∧ x<q+↑b)) :
    output false a z p q b i .value x = z x :=
  Transfer.load_other (payload a z i) (homes p q) b i x outside

end S008.Compiler.Binary
