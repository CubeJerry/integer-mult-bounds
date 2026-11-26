import «compiler-controller»

/-! A complete indexed load/store on the original deterministic finite-tape machine. -/

namespace S008.Compiler.Transfer

open OAI.Computability.IntegerMultiplication

inductive Port where
  | bank | index | value
  deriving DecidableEq, Repr, Inhabited

instance : Fintype Port := Fintype.ofList [.bank,.index,.value] (by intro t; cases t <;> decide)

inductive Stage where
  | seek (q : S008.Compiler.Phase)
  | copy | home (t : Port) | done
  deriving DecidableEq, Repr, Inhabited

instance : Fintype Stage := Fintype.ofList
  [.seek .check,.seek .scan,.seek .done,.copy,.home .bank,.home .index,.home .value,.done] (by
    intro q
    cases q with
    | seek p => cases p <;> decide
    | home t => cases t <;> decide
    | _ => decide)

def project (s : Port → Letter) : Bool → Letter := fun i => if i then s .index else s .bank

def liftAction (s : Port → Letter) (a : Bool → Letter × TM.Move) : Port → Letter × TM.Move
  | .bank => a false
  | .index => a true
  | .value => (s .value,.stay)

def nextHome : Port → Stage
  | .bank => .home .index
  | .index => .home .value
  | .value => .done

def rule (store : Bool) : TM.Rule Letter Stage Port := fun q s =>
  match q with
  | .seek p =>
      match S008.Compiler.rule p (project s) with
      | some (go,a) => some (.seek go,liftAction s a)
      | none => match p with
        | .done => some (.copy, fun t => (s t,.stay))
        | _ => none
  | .copy => match s .value, s .bank with
    | .bit v, .bit b => some (.copy, fun
       | .bank => (.bit (if store then v else b), .right)
       | .value => (.bit (if store then v else b), .right)
       | .index => (s .index,.stay))
    | .delimiter, .delimiter => some (.home .bank, fun t => (s t,.stay))
    | _, _ => none
  | .home t =>
      if s t = .home then some (nextHome t, fun u => (s u,if u=t then .right else .stay))
      else some (.home t, fun u => (s u,if u=t then .left else .stay))
  | .done => none

def embed (x : TM.Config Letter S008.Compiler.Phase Bool) (v : TM.Tape Letter) :
    TM.Config Letter Stage Port := ⟨.seek x.pc, fun
      | .bank => x.tape false
      | .index => x.tape true
      | .value => v⟩

private theorem cfg_ext {q : Stage} {f g : Port → TM.Tape Letter} (h : ∀ t, f t = g t) :
    (TM.Config.mk q f) = (TM.Config.mk q g) := congrArg (TM.Config.mk q) (funext h)

private theorem stay (v : TM.Tape Letter) : v.apply (v.view 0,.stay) = v := by
  cases v with
  | mk a f =>
    simp only [TM.Tape.apply,TM.Move.shift,Int.add_zero]
    congr 1
    funext k
    by_cases h : k=0 <;> simp [h]

private theorem embed_reads (x : TM.Config Letter S008.Compiler.Phase Bool) (v : TM.Tape Letter) :
    project (fun t => ((embed x v).tape t).view 0) = fun b => (x.tape b).view 0 := by
  funext b
  cases b <;> rfl

private theorem lift_step (store : Bool) (v : TM.Tape Letter)
    {x z : TM.Config Letter S008.Compiler.Phase Bool}
    (h : TM.advance S008.Compiler.rule x = some z) :
    TM.advance (rule store) (embed x v) = some (embed z v) := by
  unfold TM.advance at h ⊢
  have hr := embed_reads x v
  change (match S008.Compiler.rule x.pc (project (fun t => ((embed x v).tape t).view 0)) with
    | some (go,a) => some (Stage.seek go,liftAction (fun t => ((embed x v).tape t).view 0) a)
    | none => match x.pc with
      | .done => some (.copy, fun t => (((embed x v).tape t).view 0,TM.Move.stay))
      | _ => none).map _ = _
  rw [hr]
  cases hh : S008.Compiler.rule x.pc (fun b => (x.tape b).view 0) with
  | none => simp [hh] at h
  | some pair =>
    rcases pair with ⟨go,a⟩
    simp only [hh,Option.map_some,Option.some.injEq] at h
    subst z
    simp only [Option.map_some,Option.some.injEq]
    apply cfg_ext
    intro t
    cases t with
    | bank => rfl
    | index => rfl
    | value => exact stay v

private theorem lift_trace (store : Bool) (v : TM.Tape Letter) {x z n}
    (h : Trace (TM.advance S008.Compiler.rule) x n z) :
    Trace (TM.advance (rule store)) (embed x v) n (embed z v) := by
  induction h with
  | nil => exact .nil _
  | cons step _ rest => exact .cons (lift_step store v step) rest


abbrev BankData := Port → ℤ → Letter
abbrev Heads := Port → ℤ

def cfg (q : Stage) (d : BankData) (h : Heads) : TM.Config Letter Stage Port :=
  ⟨q,fun t => atPos (d t) (h t)⟩

private theorem see (a : ℤ → Letter) (p : ℤ) : (atPos a p).view 0 = a p := by simp [atPos]

private theorem write_at (a : ℤ → Letter) (p : ℤ) (w : Letter) (m : TM.Move) :
    (atPos a p).apply (w,m) = atPos (Function.update a p w) (p + m.shift) := by
  unfold atPos TM.Tape.apply
  congr 1
  funext k
  by_cases z : k + m.shift = 0
  · have z' : p + m.shift + k = p := by omega
    simp [z,z']
  · have eqp : p + m.shift + k = p + (k + m.shift) := by omega
    simp [z,Function.update_of_ne,eqp]

private theorem same_at (a : ℤ → Letter) (p : ℤ) (m : TM.Move) :
    (atPos a p).apply (a p,m) = atPos a (p + m.shift) := by
  rw [write_at,Function.update_eq_self]

private theorem read_step (mode : Bool) (d : BankData) (h : Heads) (q q' : Stage)
    (moves : Port → TM.Move)
    (hr : rule mode q (fun t => d t (h t)) = some (q',fun t => (d t (h t),moves t))) :
    TM.advance (rule mode) (cfg q d h) = some (cfg q' d (fun t => h t + (moves t).shift)) := by
  unfold TM.advance cfg
  simp only [see,hr,Option.map_some,Option.some.injEq]
  apply cfg_ext
  intro t
  exact same_at _ _ _

private theorem home_step (mode : Bool) (d : BankData) (h : Heads) (t : Port)
    (hr : d t (h t) ≠ .home) : TM.advance (rule mode) (cfg (.home t) d h) =
      some (cfg (.home t) d (Function.update h t (h t-1))) := by
  have step := read_step mode d h (.home t) (.home t) (fun u => if u=t then .left else .stay)
    (by simp [rule,hr])
  convert step using 2
  apply congrArg (cfg _ d)
  funext u
  by_cases z : u=t <;> simp [z,Function.update_of_ne,TM.Move.shift]
  omega

private theorem home_turn (mode : Bool) (d : BankData) (h : Heads) (t : Port)
    (hr : d t (h t) = .home) : TM.advance (rule mode) (cfg (.home t) d h) =
      some (cfg (nextHome t) d (Function.update h t (h t+1))) := by
  have step := read_step mode d h (.home t) (nextHome t) (fun u => if u=t then .right else .stay)
    (by simp [rule,hr])
  convert step using 2
  apply congrArg (cfg _ d)
  funext u
  by_cases z : u=t <;> simp [z,Function.update_of_ne,TM.Move.shift]

private theorem same_update {α β : Type} [DecidableEq α] (f : α → β) (t : α) (x y : β) :
    Function.update (Function.update f t x) t y = Function.update f t y := by
  funext u
  by_cases e : u=t <;> simp [e,Function.update_of_ne]

private theorem home_tour (mode : Bool) (d : BankData) (h : Heads) (t : Port) (n : ℕ)
    (marker : d t (h t-1) = .home)
    (occupied : ∀ j : ℕ, j ≤ n → d t (h t+j) ≠ .home) :
    Trace (TM.advance (rule mode)) (cfg (.home t) d (Function.update h t (h t+n))) (n+2)
      (cfg (nextHome t) d h) := by
  induction n with
  | zero =>
    have a := home_step mode d h t (by simpa using occupied 0 (by omega))
    have b := home_turn mode d (Function.update h t (h t-1)) t (by simpa using marker)
    simp at b
    simpa using (Trace.single a).trans (Trace.single b)
  | succ n ih =>
    have a := home_step mode d (Function.update h t (h t+↑(n+1 : ℕ))) t
      (by simpa using occupied (n+1) (by omega))
    have eqp : h t+↑(n+1 : ℕ)-1 = h t+n := by omega
    simp only [Function.update_self,same_update,eqp] at a
    have tail := ih (fun j hj => occupied j (by omega))
    simpa [Nat.add_assoc,Nat.add_left_comm,Nat.add_comm] using Trace.cons a tail


/-- The destination after exactly n consecutive digits, including unrestricted exterior cells. -/
def window (a b : ℤ → Letter) (p q : ℤ) (n : ℕ) (z : ℤ) : Letter :=
  if q ≤ z ∧ z < q+n then a (p+(z-q)) else b z

private theorem window_next (a b : ℤ → Letter) (p q : ℤ) (n : ℕ) :
    window a b p q n (q+n) = b (q+n) := by simp [window]

private theorem window_zero (a b : ℤ → Letter) (p q : ℤ) :
    window a b p q 0 = b := by
  funext z
  simp [window]

private theorem window_succ (a b : ℤ → Letter) (p q : ℤ) (n : ℕ) :
    Function.update (window a b p q n) (q+n) (a (p+n)) = window a b p q (n+1) := by
  funext z
  by_cases e : z=q+n
  · subst z
    simp [window]
  · have eqi : (q ≤ z ∧ z < q+↑(n+1 : ℕ)) ↔ (q ≤ z ∧ z < q+n) := by omega
    simp only [Function.update_of_ne e,window,eqi]

/-- The bank or register is overwritten according to the fixed instruction opcode. -/
def copied (store : Bool) (d : BankData) (h : Heads) (n : ℕ) : BankData
  | .bank => if store then window (d .value) (d .bank) (h .value) (h .bank) n else d .bank
  | .value => if store then d .value else window (d .bank) (d .value) (h .bank) (h .value) n
  | .index => d .index

def advanced (h : Heads) (n : ℕ) : Heads
  | .bank => h .bank+n
  | .value => h .value+n
  | .index => h .index

private theorem copied_zero (store : Bool) (d : BankData) (h : Heads) : copied store d h 0 = d := by
  funext t
  cases t <;> cases store <;> simp [copied,window_zero]

private theorem advanced_zero (h : Heads) : advanced h 0 = h := by
  funext t
  cases t <;> simp [advanced]

private theorem copy_one (store : Bool) (d : BankData) (h : Heads) (n : ℕ) (v b : Bool)
    (hv : d .value (h .value+n) = .bit v) (hb : d .bank (h .bank+n) = .bit b) :
    TM.advance (rule store) (cfg .copy (copied store d h n) (advanced h n)) =
      some (cfg .copy (copied store d h (n+1)) (advanced h (n+1))) := by
  cases store <;> unfold TM.advance cfg <;>
    simp only [see,rule,copied,advanced,Bool.false_eq_true,ite_false,ite_true,window_next,hb,hv,
      Option.map_some,Option.some.injEq] <;> apply cfg_ext <;> intro t <;> cases t <;>
    simp only [TM.Move.shift,Int.add_zero,Int.natCast_succ,write_at]
  · rw [← hb,Function.update_eq_self]
    simp [add_assoc]
  · rw [Function.update_eq_self]
  · rw [← hb,window_succ]
    simp [add_assoc]
  · rw [← hv,window_succ]
    simp [add_assoc]
  · rw [Function.update_eq_self]
  · rw [← hv,Function.update_eq_self]
    simp [add_assoc]

private theorem copy_all (store : Bool) (d : BankData) (h : Heads) (n : ℕ)
    (vb : ∀ j : ℕ, j<n → ∃ b, d .value (h .value+j) = .bit b)
    (bb : ∀ j : ℕ, j<n → ∃ b, d .bank (h .bank+j) = .bit b) :
    Trace (TM.advance (rule store)) (cfg .copy d h) n
      (cfg .copy (copied store d h n) (advanced h n)) := by
  induction n with
  | zero => simpa [copied_zero,advanced_zero] using
      (Trace.nil (step := TM.advance (rule store)) (cfg .copy d h))
  | succ n ih =>
    obtain ⟨v,hv⟩ := vb n (by omega)
    obtain ⟨b,hb⟩ := bb n (by omega)
    have prev := ih (fun j hj => vb j (by omega)) (fun j hj => bb j (by omega))
    exact prev.trans (Trace.single (copy_one store d h n v b hv hb))

private theorem copy_end (store : Bool) (d : BankData) (h : Heads) (n : ℕ)
    (ve : d .value (h .value+n) = .delimiter) (be : d .bank (h .bank+n) = .delimiter) :
    TM.advance (rule store) (cfg .copy (copied store d h n) (advanced h n)) =
      some (cfg (.home .bank) (copied store d h n) (advanced h n)) := by
  have hr : rule store .copy (fun t => (copied store d h n) t ((advanced h n) t)) =
      some (.home .bank,fun t => ((copied store d h n) t ((advanced h n) t),TM.Move.stay)) := by
    cases store <;> simp only [rule,copied,advanced,Bool.false_eq_true,ite_false,ite_true,window_next,ve,be]
  simpa [TM.Move.shift] using read_step store (copied store d h n) (advanced h n) .copy
    (.home .bank) (fun _ => .stay) hr


/-- All cells except the indicated occupied word prefixes may contain arbitrary letters. -/
structure Canonical (d : BankData) (o : Heads) (b i : ℕ) : Prop where
  homes : ∀ t, d t (o t-1) = .home
  bank : ∀ j : ℕ, j ≤ i → recordAt (d .bank) (o .bank+↑(j*(b+1) : ℕ)) b
  marks : ∀ j : ℕ, j < i → d .index (o .index+j) = .count
  stop : d .index (o .index+i) = .delimiter
  value : recordAt (d .value) (o .value) b

def slot (o : Heads) (b i : ℕ) : Heads
  | .bank => o .bank+↑(i*(b+1) : ℕ)
  | .index => o .index+i
  | .value => o .value

private theorem record_nohome (a : ℤ → Letter) (p : ℤ) (b n : ℕ)
    (h : recordAt a p b) (hn : n ≤ b) : a (p+n) ≠ .home := by
  by_cases e : n=b
  · subst n
    rw [h.2]
    decide
  · obtain ⟨c,hc⟩ := h.1 n (by omega)
    rw [hc]
    cases c <;> decide

private theorem bank_nohome (a : ℤ → Letter) (p : ℤ) (b i : ℕ)
    (records : ∀ j : ℕ, j ≤ i → recordAt a (p+↑(j*(b+1) : ℕ)) b) :
    ∀ n : ℕ, n ≤ i*(b+1)+b → a (p+n) ≠ .home := by
  induction i with
  | zero =>
    intro n hn
    exact record_nohome _ _ _ _ (by simpa using records 0 (by omega)) (by simpa using hn)
  | succ i ih =>
    intro n hn
    by_cases e : n ≤ i*(b+1)+b
    · exact ih (fun j hj => records j (by omega)) n e
    · have hlow : (i+1)*(b+1) ≤ n := by
        rw [Nat.succ_mul]
        omega
      let j := n-(i+1)*(b+1)
      have hj : j ≤ b := by dsimp [j]; omega
      have pair := record_nohome a (p+↑((i+1)*(b+1) : ℕ)) b j (records (i+1) (by omega)) hj
      have eqn : (i+1)*(b+1)+j = n := by dsimp [j]; omega
      have eqp : p+↑((i+1)*(b+1) : ℕ)+↑j = p+n := by
        rw [add_assoc,← Int.natCast_add,eqn]
      rwa [eqp] at pair

private theorem window_home (a b : ℤ → Letter) (p q : ℤ) (n : ℕ)
    (ra : recordAt a p n) (rb : recordAt b q n) (z : ℤ) :
    window a b p q n z = .home ↔ b z = .home := by
  by_cases inside : q ≤ z ∧ z < q+n
  · let j := (z-q).toNat
    have jp : (j:ℤ) = z-q := Int.toNat_of_nonneg (by omega)
    have small : j<n := by omega
    obtain ⟨x,hx⟩ := ra.1 j small
    obtain ⟨y,hy⟩ := rb.1 j small
    have qj : q+(j:ℤ)=z := by omega
    rw [qj] at hy
    rw [jp] at hx
    simp [window,inside,hx,hy]
  · simp [window,inside]

private theorem copied_home (store : Bool) (d : BankData) (h : Heads) (n : ℕ)
    (v : recordAt (d .value) (h .value) n) (b : recordAt (d .bank) (h .bank) n)
    (t : Port) (z : ℤ) : copied store d h n t z = .home ↔ d t z = .home := by
  cases t <;> cases store <;> simp only [copied,Bool.false_eq_true,ite_false,ite_true] <;>
    first | exact Iff.rfl | exact window_home _ _ _ _ _ v b _ | exact window_home _ _ _ _ _ b v _

private theorem embed_config (d : BankData) (h : Heads) (q : S008.Compiler.Phase) :
    embed (S008.Compiler.config q (d .bank) (d .index) (h .bank) (h .index))
      (atPos (d .value) (h .value)) = cfg (.seek q) d h := by
  apply cfg_ext
  intro t
  cases t <;> rfl

private theorem seek_port (store : Bool) (d : BankData) (o : Heads) (b i : ℕ)
    (c : Canonical d o b i) :
    Trace (TM.advance (rule store)) (cfg (.seek .check) d o) (i*(b+2)+1)
      (cfg (.seek .done) d (slot o b i)) := by
  have tr := lift_trace store (atPos (d .value) (o .value))
    (indexed_seek (d .bank) (d .index) (o .bank) (o .index) b i
      (fun j hj => c.bank j (by omega)) c.marks c.stop)
  rw [← embed_config d o .check,← embed_config d (slot o b i) .done]
  exact tr

private theorem start_copy (store : Bool) (d : BankData) (h : Heads) :
    TM.advance (rule store) (cfg (.seek .done) d h) = some (cfg .copy d h) := by
  simpa [TM.Move.shift] using
    read_step store d h (.seek .done) .copy (fun _ => .stay) (by rfl)


private theorem return_all (store : Bool) (d : BankData) (o : Heads) (b i : ℕ)
    (c : Canonical d o b i) :
    Trace (TM.advance (rule store))
      (cfg (.home .bank) (copied store d (slot o b i) b) (advanced (slot o b i) b))
      ((i*(b+1)+b+2)+(i+2)+(b+2))
      (cfg .done (copied store d (slot o b i) b) o) := by
  let d' := copied store d (slot o b i) b
  let hB : Heads := fun
    | .bank => o .bank
    | .index => o .index+i
    | .value => o .value+b
  let hI : Heads := fun
    | .bank => o .bank
    | .index => o .index
    | .value => o .value+b
  have nh (t : Port) (z : ℤ) : d' t z = .home ↔ d t z = .home :=
    copied_home store d (slot o b i) b c.value (c.bank i (by omega)) t z
  have B := home_tour store d' hB .bank (i*(b+1)+b)
    ((nh _ _).2 (c.homes _)) (fun j hj bad =>
        (bank_nohome (d .bank) (o .bank) b i c.bank j hj) ((nh _ _).1 bad))
  have I := home_tour store d' hI .index i ((nh _ _).2 (c.homes _)) (by
    intro j hj bad
    have bad' := (nh _ _).1 bad
    change d .index (o .index+j) = .home at bad'
    by_cases eq : j=i
    · subst j
      rw [c.stop] at bad'
      contradiction
    · rw [c.marks j (by omega)] at bad'
      contradiction)
  have V := home_tour store d' o .value b ((nh _ _).2 (c.homes _))
    (fun j hj bad => record_nohome _ _ _ _ c.value hj ((nh _ _).1 bad))
  have eB : Function.update hB .bank (hB .bank+↑(i*(b+1)+b : ℕ)) =
      advanced (slot o b i) b := by
    funext t
    cases t <;> simp [hB,advanced,slot,Function.update,add_assoc]
  have eI : Function.update hI .index (hI .index+↑i) = hB := by
    funext t
    cases t <;> simp [hB,hI,Function.update]
  have eV : Function.update o .value (o .value+↑b) = hI := by
    funext t
    cases t <;> simp [hI,Function.update]
  rw [eB] at B
  rw [eI] at I
  rw [eV] at V
  exact (B.trans I).trans V

/-- Both literal instructions act on the selected occupied word, consume the exact number
    of simultaneous head steps shown, and finish with all three heads at their entry positions. -/
theorem indexed_access (store : Bool) (d : BankData) (o : Heads) (b i : ℕ)
    (c : Canonical d o b i) :
    Trace (TM.advance (rule store)) (cfg (.seek .check) d o) (i*(2*b+4)+3*b+9)
      (cfg .done (copied store d (slot o b i) b) o) := by
  have a := seek_port store d o b i c
  have b0 := Trace.single (start_copy store d (slot o b i))
  have rb := c.bank i (by omega)
  have transfer := copy_all store d (slot o b i) b c.value.1 rb.1
  have endword := Trace.single (copy_end store d (slot o b i) b c.value.2 rb.2)
  have all := ((((a.trans b0).trans transfer).trans endword).trans (return_all store d o b i c))
  convert all using 1
  rw [show 2*b=b+b by omega]
  simp only [Nat.mul_add]
  omega

theorem indexed_access_halts (store : Bool) (d : BankData) (o : Heads) :
    TM.advance (rule store) (cfg .done d o) = none := rfl

theorem loaded_bit (d : BankData) (o : Heads) (b i j : ℕ) (small : j<b) :
    copied false d (slot o b i) b .value (o .value+j) =
      d .bank (o .bank+↑(i*(b+1) : ℕ)+j) := by
  have inside : o .value≤o .value+↑j ∧ o .value+↑j<o .value+↑b := by omega
  simp [copied,window,slot,inside]

theorem stored_bit (d : BankData) (o : Heads) (b i j : ℕ) (small : j<b) :
    copied true d (slot o b i) b .bank (o .bank+↑(i*(b+1) : ℕ)+j) =
      d .value (o .value+j) := by
  simp [copied,window,slot,small]

theorem store_other (d : BankData) (o : Heads) (b i : ℕ) (z : ℤ)
    (outside : ¬(o .bank+↑(i*(b+1) : ℕ)≤z ∧ z<o .bank+↑(i*(b+1) : ℕ)+↑b)) :
    copied true d (slot o b i) b .bank z = d .bank z := by simp only [copied,ite_true,slot,window,ite_eq_right outside]

theorem load_other (d : BankData) (o : Heads) (b i : ℕ) (z : ℤ)
    (outside : ¬(o .value≤z ∧ z<o .value+↑b)) :
    copied false d (slot o b i) b .value z = d .value z := by simp [copied,window,slot,outside]

#print axioms indexed_access
#print axioms indexed_access_halts
#print axioms loaded_bit
#print axioms stored_bit
#print axioms store_other
#print axioms load_other

end S008.Compiler.Transfer
