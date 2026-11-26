import «compiler-controller»

/-! A physical binary-to-unary index converter with normalized work banks. -/

namespace S008.Compiler.Unary

open OAI.Computability.IntegerMultiplication

inductive Port where
  | digits | output | work
  deriving DecidableEq, Repr, Inhabited

instance : Fintype Port := Fintype.ofList [.digits,.output,.work] (by intro x; cases x <;> decide)

inductive Home where
  | before | after | finalOutput | finalDigits
  deriving DecidableEq, Repr, Inhabited

inductive Phase where
  | read | first (d : Bool) | second (d : Bool) | restore | suffix | home (p : Home) | done
  deriving DecidableEq, Repr, Inhabited

instance : Fintype Phase := Fintype.ofList [.read,.first false,.first true,.second false,.second true,
  .restore,.suffix,.home .before,.home .after,.home .finalOutput,.home .finalDigits,.done] (by
    intro q
    cases q with
    | first b => cases b <;> decide
    | second b => cases b <;> decide
    | home x => cases x <;> decide
    | _ => decide)

def active : Home → Port
  | .finalDigits => .digits
  | _ => .output

def nextHome : Home → Phase
  | .before => .restore
  | .after => .read
  | .finalOutput => .home .finalDigits
  | .finalDigits => .done

def endMove (p : Home) (t : Port) : TM.Move :=
  if t = active p then .right else if p = .before ∧ t = .work then .left else .stay

def readOnly (r : Port → Letter) (moves : Port → TM.Move) (t : Port) : Letter × TM.Move :=
  (r t,moves t)

def rule : TM.Rule Letter Phase Port := fun q r =>
  match q with
  | .read => match r .digits with
    | .bit d => some (.first d, readOnly r (fun t => if t = .digits then .right else .stay))
    | .delimiter => some (.suffix,readOnly r (fun _ => .stay))
    | _ => none
  | .first d => match r .output with
    | .count => some (.second d, fun
      | .digits => (r .digits,.stay)
      | .output => (.blank,.right)
      | .work => (.count,.right))
    | .blank => some (.home .before,fun t =>
      if d ∧ t = .work then (.count,.right) else (r t,.stay))
    | _ => none
  | .second d => some (.first d, fun t => if t = .work then (.count,.right) else (r t,.stay))
  | .restore => match r .work with
    | .count => some (.restore,fun
      | .digits => (r .digits,.stay)
      | .output => (.count,.right)
      | .work => (.blank,.left))
    | .home => some (.home .after,readOnly r (fun t => if t = .work then .right else .stay))
    | _ => none
  | .suffix => match r .output with
    | .count => some (.suffix,readOnly r (fun t => if t = .output then .right else .stay))
    | .blank => some (.home .finalOutput, fun t => if t = .output then (.delimiter,.stay) else (r t,.stay))
    | _ => none
  | .home p =>
    if r (active p) = .home then some (nextHome p,readOnly r (endMove p))
    else some (.home p,readOnly r (fun t => if t = active p then .left else .stay))
  | .done => none

abbrev Data := Port → ℤ → Letter
abbrev Heads := Port → ℤ

def cfg (q : Phase) (d : Data) (h : Heads) : TM.Config Letter Phase Port :=
  ⟨q,fun t => atPos (d t) (h t)⟩

def triple {α : Type} (a b c : α) : Port → α
  | .digits => a | .output => b | .work => c

/-- Scratch cells between the lower and upper offsets store unary marks. -/
def un (lo hi : ℕ) (z : ℤ) : Letter :=
  if z = -1 then .home else if (lo:ℤ) ≤ z ∧ z < (hi:ℤ) then .count else .blank

def closed (n : ℕ) (z : ℤ) : Letter :=
  if z = (n:ℤ) then .delimiter else un 0 n z

private theorem see (a : ℤ → Letter) (p : ℤ) : (atPos a p).view 0 = a p := by simp [atPos]

private theorem tape_write (a : ℤ → Letter) (p : ℤ) (w : Letter) (m : TM.Move) :
    (atPos a p).apply (w,m) = atPos (Function.update a p w) (p + m.shift) := by
  unfold atPos TM.Tape.apply
  congr 1
  funext k
  by_cases z : k + m.shift = 0
  · have z' : p + m.shift + k = p := by omega
    simp [z,z']
  · have eqp : p + m.shift + k = p + (k + m.shift) := by omega
    simp [z,Function.update_of_ne,eqp]

private theorem tape_same (a : ℤ → Letter) (p : ℤ) (m : TM.Move) :
    (atPos a p).apply (a p,m) = atPos a (p + m.shift) := by rw [tape_write,Function.update_eq_self]

private theorem cfg_ext {q : Phase} {f g : Port → TM.Tape Letter} (h : ∀ t, f t = g t) :
    (TM.Config.mk q f) = (TM.Config.mk q g) := congrArg (TM.Config.mk q) (funext h)

private theorem plain (d : Data) (h : Heads) (q q' : Phase) (mv : Port → TM.Move)
    (r : rule q (fun t => d t (h t)) = some (q',readOnly (fun t => d t (h t)) mv)) :
    TM.advance rule (cfg q d h) = some (cfg q' d (fun t => h t + (mv t).shift)) := by
  unfold TM.advance cfg
  simp only [see,r,readOnly,Option.map_some,Option.some.injEq]
  apply cfg_ext
  intro t
  exact tape_same _ _ _

private theorem home_left (p : Home) (d : Data) (h : Heads)
    (hx : d (active p) (h (active p)) ≠ .home) :
    TM.advance rule (cfg (.home p) d h) = some (cfg (.home p) d
      (Function.update h (active p) (h (active p)-1))) := by
  have a := plain d h (.home p) (.home p) (fun t => if t = active p then .left else .stay)
    (by simp [rule,hx])
  convert a using 2
  apply congrArg (cfg _ d)
  funext t
  by_cases e : t=active p <;> simp [e,Function.update_of_ne,TM.Move.shift]
  omega

def returned (p : Home) (h : Heads) : Heads :=
  fun t => if p = .before ∧ t = .work then h t-1 else h t

private theorem home_turn (p : Home) (d : Data) (h : Heads)
    (zero : h (active p) = 0) (mark : d (active p) (-1) = .home) :
    TM.advance rule (cfg (.home p) d (Function.update h (active p) (-1))) =
      some (cfg (nextHome p) d (returned p h)) := by
  have a := plain d (Function.update h (active p) (-1)) (.home p) (nextHome p) (endMove p)
    (by simp [rule,mark])
  convert a using 2
  apply congrArg (cfg _ d)
  funext t
  cases p <;> cases t <;> simp_all [returned,endMove,active,Function.update,TM.Move.shift]
  omega

private theorem home_tour (p : Home) (d : Data) (h : Heads) (n : ℕ) (zero : h (active p)=0)
    (mark : d (active p) (-1) = .home)
    (occupied : ∀ j : ℕ, j≤n → d (active p) j ≠ .home) :
    Trace (TM.advance rule) (cfg (.home p) d (Function.update h (active p) (n:ℤ))) (n+2)
      (cfg (nextHome p) d (returned p h)) := by
  induction n with
  | zero =>
    have a := home_left p d h (by rw [zero];exact occupied 0 (by omega))
    have b := home_turn p d h zero mark
    rw [zero] at a
    simpa [← zero] using (Trace.single a).trans (Trace.single b)
  | succ n ih =>
    have a := home_left p d (Function.update h (active p) (↑(n+1:ℕ))) (by simpa using occupied (n+1) (by omega))
    have e : (↑(n+1 : ℕ) : ℤ)-1 = n := by omega
    simp only [Function.update_self,Function.update_idem,e] at a
    simpa [Nat.add_assoc,Nat.add_left_comm,Nat.add_comm] using
      Trace.cons a (ih (fun j hj => occupied j (by omega)))


private theorem empty (k : ℕ) : un k k = un 0 0 := by
  funext z
  unfold un
  split_ifs <;> first | rfl | omega

private theorem un_home (a b : ℕ) : un a b (-1) = .home := by simp [un]

private theorem un_nohome (a b j : ℕ) : un a b (j:ℤ) ≠ .home := by
  simp [un]
  split_ifs <;> decide

private theorem un_inside (a b j : ℕ) (h : a≤j) (e : j<b) : un a b (j:ℤ) = .count := by
  simp [un,h,e]

private theorem un_end (a b : ℕ) : un a b (b:ℤ) = .blank := by simp [un]

private theorem take_first (a b : ℕ) :
    Function.update (un a b) (a:ℤ) .blank = un (a+1) b := by
  funext z
  by_cases e : z=(a:ℤ)
  · subst z
    simp [un]
  · rw [Function.update_of_ne e]
    unfold un
    split_ifs <;> first | rfl | omega

private theorem put_end (n : ℕ) :
    Function.update (un 0 n) (n:ℤ) .count = un 0 (n+1) := by
  funext z
  by_cases e : z=(n:ℤ)
  · subst z
    simp [un]
  · rw [Function.update_of_ne e]
    unfold un
    split_ifs <;> first | rfl | omega

private theorem take_end (n : ℕ) :
    Function.update (un 0 (n+1)) (n:ℤ) .blank = un 0 n := by
  funext z
  by_cases e : z=(n:ℤ)
  · subst z
    simp [un]
  · rw [Function.update_of_ne e]
    unfold un
    split_ifs <;> first | rfl | omega

private theorem shut (n : ℕ) :
    Function.update (un 0 n) (n:ℤ) .delimiter = closed n := by
  funext z
  by_cases e : z=(n:ℤ) <;> simp [e,closed,Function.update_of_ne]

def frame (q : Phase) (d : ℤ → Letter) (p : ℤ)
    (a b : ℕ) (u : ℤ) (n : ℕ) (v : ℤ) : TM.Config Letter Phase Port :=
  cfg q (triple d (un a b) (un 0 n)) (triple p u v)

private theorem double_first (digit : Bool) (d : ℤ → Letter) (p : ℤ) (a b n : ℕ) (h : a<b) :
    TM.advance rule (frame (.first digit) d p a b a n n) =
      some (frame (.second digit) d p (a+1) b (a+1:ℕ) (n+1) (n+1:ℕ)) := by
  unfold TM.advance frame cfg
  simp only [see,rule,triple,un_inside a b a (by omega) h,Option.map_some,Option.some.injEq]
  apply cfg_ext
  intro t
  cases t with
  | digits => simp [tape_same,TM.Move.shift]
  | output => simp [tape_write,take_first a b,TM.Move.shift]
  | work => simp [tape_write,put_end,TM.Move.shift]

private theorem double_second (digit : Bool) (d : ℤ → Letter) (p : ℤ) (a b n : ℕ) :
    TM.advance rule (frame (.second digit) d p a b a n n) =
      some (frame (.first digit) d p a b a (n+1) (n+1:ℕ)) := by
  unfold TM.advance frame cfg
  simp only [rule,Option.map_some,Option.some.injEq]
  apply cfg_ext
  intro t
  cases t <;> simp [triple,see,tape_same,tape_write,put_end,TM.Move.shift]

private theorem double_all (digit : Bool) (d : ℤ → Letter) (p : ℤ) (k : ℕ) :
    Trace (TM.advance rule) (frame (.first digit) d p 0 k 0 0 0) (2*k)
      (frame (.first digit) d p k k k (2*k) (2*k:ℕ)) := by
  suffices go : ∀ j : ℕ, j≤k →
      Trace (TM.advance rule) (frame (.first digit) d p 0 k 0 0 0) (2*j)
        (frame (.first digit) d p j k j (2*j) (2*j:ℕ)) from go k (by omega)
  intro j hj
  induction j with
  | zero => simp; exact .nil _
  | succ j ih =>
    have left := double_first digit d p j k (2*j) (by omega)
    have right := double_second digit d p (j+1) k (2*j+1)
    have both := (Trace.single left).trans (Trace.single right)
    have path := (ih (by omega)).trans both
    have eqn : 2*(j+1)=2*j+1+1 := by omega
    simpa only [eqn] using path

def valueBit (d : Bool) : ℕ := if d then 1 else 0

private theorem double_end (digit : Bool) (d : ℤ → Letter) (p : ℤ) (k n : ℕ) :
    TM.advance rule (frame (.first digit) d p k k k n n) =
      some (frame (.home .before) d p 0 0 k (n+valueBit digit) (n+valueBit digit:ℕ)) := by
  unfold TM.advance frame cfg
  simp only [see,rule,triple,un_end,Option.map_some,Option.some.injEq]
  apply cfg_ext
  intro t
  cases digit <;> cases t <;> simp [valueBit,tape_same,tape_write,put_end,empty,TM.Move.shift]


private theorem before_restore (d : ℤ → Letter) (p : ℤ) (k n : ℕ) :
    Trace (TM.advance rule) (frame (.home .before) d p 0 0 k n n) (k+2)
      (frame .restore d p 0 0 0 n ((n:ℤ)-1)) := by
  have tr := home_tour .before (triple d (un 0 0) (un 0 n)) (triple p 0 (n:ℤ)) k rfl
    (un_home 0 0) (fun j _ => un_nohome 0 0 j)
  unfold frame
  convert tr using 1 <;> apply congrArg (cfg _ _) <;> funext t <;> cases t <;>
    simp [active,triple,Function.update,returned]

private theorem restore_one (d : ℤ → Letter) (p : ℤ) (j n : ℕ) :
    TM.advance rule (frame .restore d p 0 j j (n+1) n) =
      some (frame .restore d p 0 (j+1) (j+1:ℕ) n ((n:ℤ)-1)) := by
  unfold TM.advance frame cfg
  simp only [see,rule,triple,un_inside 0 (n+1) n (by omega) (by omega),Option.map_some,Option.some.injEq]
  apply cfg_ext
  intro t
  cases t with
  | digits => simp [tape_same,TM.Move.shift]
  | output => simp [tape_write,put_end,TM.Move.shift]
  | work => simp [tape_write,take_end,TM.Move.shift]; congr 1

private theorem restore_all (d : ℤ → Letter) (p : ℤ) (j n : ℕ) :
    Trace (TM.advance rule) (frame .restore d p 0 j j n ((n:ℤ)-1)) n
      (frame .restore d p 0 (j+n) (j+n:ℕ) 0 (-1)) := by
  induction n generalizing j with
  | zero => simp; exact .nil _
  | succ n ih =>
    have path := Trace.cons (restore_one d p j n) (ih (j+1))
    have front : (↑(n+1:ℕ):ℤ)-1 = n := by omega
    simpa only [front,Nat.add_assoc,Nat.add_left_comm,Nat.add_comm] using path

private theorem restore_end (d : ℤ → Letter) (p : ℤ) (k : ℕ) :
    TM.advance rule (frame .restore d p 0 k k 0 (-1)) =
      some (frame (.home .after) d p 0 k k 0 0) := by
  have tr := plain (triple d (un 0 k) (un 0 0)) (triple p (k:ℤ) (-1)) .restore (.home .after)
    (fun t => if t=.work then .right else .stay) (by simp [rule,triple,un_home])
  unfold frame
  convert tr using 2
  apply congrArg (cfg _ _)
  funext t
  cases t <;> simp [triple,TM.Move.shift]

private theorem after_restore (d : ℤ → Letter) (p : ℤ) (k : ℕ) :
    Trace (TM.advance rule) (frame (.home .after) d p 0 k k 0 0) (k+2)
      (frame .read d p 0 k 0 0 0) := by
  have tr := home_tour .after (triple d (un 0 k) (un 0 0)) (triple p 0 0) k rfl
    (un_home 0 k) (fun j _ => un_nohome 0 k j)
  unfold frame
  convert tr using 1 <;> apply congrArg (cfg _ _) <;> funext t <;> cases t <;>
    simp [triple,active,Function.update,returned]

private theorem read_bit (d : ℤ → Letter) (p : ℤ) (k : ℕ) (digit : Bool) (hb : d p = .bit digit) :
    TM.advance rule (frame .read d p 0 k 0 0 0) =
      some (frame (.first digit) d (p+1) 0 k 0 0 0) := by
  have tr := plain (triple d (un 0 k) (un 0 0)) (triple p 0 0) .read (.first digit)
    (fun t => if t=.digits then .right else .stay) (by simp [rule,triple,hb])
  unfold frame
  convert tr using 2
  apply congrArg (cfg _ _)
  funext t
  cases t <;> simp [triple,TM.Move.shift]

private theorem bit_step (d : ℤ → Letter) (p : ℤ) (k : ℕ) (digit : Bool) (hb : d p = .bit digit) :
    Trace (TM.advance rule) (frame .read d p 0 k 0 0 0) (7*k+2*valueBit digit+7)
      (frame .read d (p+1) 0 (2*k+valueBit digit) 0 0 0) := by
  let n := 2*k+valueBit digit
  have a := (Trace.single (read_bit d p k digit hb)).trans (double_all digit d (p+1) k)
  have b := a.trans (Trace.single (double_end digit d (p+1) k (2*k)))
  have c := b.trans (before_restore d (p+1) k n)
  have rev := restore_all d (p+1) 0 n
  simp only [Nat.zero_add] at rev
  have rest := (c.trans rev).trans (Trace.single (restore_end d (p+1) n))
  have all := rest.trans (after_restore d (p+1) n)
  convert all using 1
  dsimp [n]
  omega


def eval (k : ℕ) : List Bool → ℕ
  | [] => k
  | d :: ds => eval (2*k+valueBit d) ds

def cost (k : ℕ) : List Bool → ℕ
  | [] => 0
  | d :: ds => 7*k+2*valueBit d+7 + cost (2*k+valueBit d) ds

def ones : List Bool → ℕ
  | [] => 0
  | d :: ds => valueBit d + ones ds

def wordAt (d : ℤ → Letter) (p : ℤ) : List Bool → Prop
  | [] => True
  | x :: xs => d p = .bit x ∧ wordAt d (p+1) xs

private theorem prefix_scan (d : ℤ → Letter) (p : ℤ) (k : ℕ) (xs : List Bool) (word : wordAt d p xs) :
    Trace (TM.advance rule) (frame .read d p 0 k 0 0 0) (cost k xs)
      (frame .read d (p+xs.length) 0 (eval k xs) 0 0 0) := by
  induction xs generalizing p k with
  | nil => simpa [cost,eval] using (Trace.nil (step := TM.advance rule) (frame .read d p 0 k 0 0 0))
  | cons x xs ih =>
    have start := bit_step d p k x word.1
    have tail := ih (p+1) (2*k+valueBit x) word.2
    simpa [cost,eval,add_assoc,add_left_comm,add_comm] using start.trans tail

theorem cost_value (k : ℕ) (xs : List Bool) :
    cost k xs+5*ones xs+7*k = 7*eval k xs+7*xs.length := by
  induction xs generalizing k with
  | nil => simp [cost,ones,eval]
  | cons x xs ih =>
    have ha := ih (2*k+valueBit x)
    simp only [cost,ones,eval,List.length_cons]
    omega

private theorem matches_nohome (d : ℤ → Letter) (p : ℤ) (xs : List Bool)
    (word : wordAt d p xs) (j : ℕ) (small : j<xs.length) : d (p+j) ≠ .home := by
  induction xs generalizing p j with
  | nil => simp at small
  | cons x xs ih =>
    cases j with
    | zero => simp; rw [word.1]; cases x <;> decide
    | succ j =>
      have t := ih (p+1) word.2 j (by simpa using small)
      simpa [add_assoc,add_left_comm,add_comm] using t

private theorem read_end (d : ℤ → Letter) (p : ℤ) (k : ℕ) (stop : d p = .delimiter) :
    TM.advance rule (frame .read d p 0 k 0 0 0) = some (frame .suffix d p 0 k 0 0 0) := by
  unfold frame
  simpa [TM.Move.shift] using
    plain (triple d (un 0 k) (un 0 0)) (triple p 0 0) .read .suffix (fun _ => .stay)
      (by simp [rule,triple,stop])

private theorem final_next (d : ℤ → Letter) (p : ℤ) (k j : ℕ) (small : j<k) :
    TM.advance rule (frame .suffix d p 0 k j 0 0) =
      some (frame .suffix d p 0 k (j+1:ℕ) 0 0) := by
  have a := plain (triple d (un 0 k) (un 0 0)) (triple p (j:ℤ) 0) .suffix .suffix
    (fun t => if t=.output then .right else .stay)
    (by simp [triple,rule,un_inside 0 k j (by omega) small])
  unfold frame
  convert a using 2
  apply congrArg (cfg _ _)
  funext t
  cases t <;> simp [triple,TM.Move.shift]

private theorem final_scan (d : ℤ → Letter) (p : ℤ) (k : ℕ) :
    Trace (TM.advance rule) (frame .suffix d p 0 k 0 0 0) k (frame .suffix d p 0 k k 0 0) := by
  suffices scan : ∀ j : ℕ, j≤k → Trace (TM.advance rule) (frame .suffix d p 0 k 0 0 0) j
      (frame .suffix d p 0 k j 0 0) from scan k (by omega)
  intro j sj
  induction j with
  | zero => exact .nil _
  | succ j ih => exact (ih (by omega)).trans (Trace.single (final_next d p k j (by omega)))

private theorem end_write (d : ℤ → Letter) (p : ℤ) (k : ℕ) :
    TM.advance rule (frame .suffix d p 0 k k 0 0) =
      some (cfg (.home .finalOutput) (triple d (closed k) (un 0 0)) (triple p (k:ℤ) 0)) := by
  unfold TM.advance frame cfg
  simp only [see,rule,triple,un_end,Option.map_some,Option.some.injEq]
  apply cfg_ext
  intro t
  cases t <;> simp [tape_same,tape_write,shut,TM.Move.shift]

private theorem closed_home (k : ℕ) : closed k (-1) = .home := by simp [closed,un_home]

private theorem closed_nohome (k j : ℕ) : closed k j ≠ .home := by
  unfold closed
  split <;> first | decide | exact un_nohome 0 k j


private theorem final_output (d : ℤ → Letter) (p : ℤ) (k : ℕ) :
    Trace (TM.advance rule)
      (cfg (.home .finalOutput) (triple d (closed k) (un 0 0)) (triple p (k:ℤ) 0)) (k+2)
      (cfg (.home .finalDigits) (triple d (closed k) (un 0 0)) (triple p 0 0)) := by
  have tr := home_tour .finalOutput (triple d (closed k) (un 0 0)) (triple p 0 0) k rfl
    (closed_home k) (fun j _ => closed_nohome k j)
  convert tr using 1 <;> apply congrArg (cfg _ _) <;> funext t <;> cases t <;>
    simp [triple,active,Function.update,returned]

private theorem final_digits (d : ℤ → Letter) (p k : ℕ) (home : d (-1) = .home)
    (span : ∀ j : ℕ, j≤p → d (j:ℤ) ≠ .home) :
    Trace (TM.advance rule)
      (cfg (.home .finalDigits) (triple d (closed k) (un 0 0)) (triple (p:ℤ) 0 0)) (p+2)
      (cfg .done (triple d (closed k) (un 0 0)) (triple 0 0 0)) := by
  have tr := home_tour .finalDigits (triple d (closed k) (un 0 0)) (triple 0 0 0) p rfl home span
  convert tr using 1 <;> apply congrArg (cfg _ _) <;> funext t <;> cases t <;>
    simp [triple,active,Function.update,returned]

/-- A canonical binary address may have leading zero padding. Its external tape is preserved. -/
structure Input (d : ℤ → Letter) (xs : List Bool) : Prop where
  home : d (-1) = .home
  digits : wordAt d 0 xs
  stop : d (xs.length:ℤ) = .delimiter

/-- The computed unary value and all three heads are returned in canonical positions.
    The theorem charges the actual deterministic machine through its halting state. -/
theorem binary_to_unary (d : ℤ → Letter) (xs : List Bool) (bin : Input d xs) :
    Trace (TM.advance rule) (frame .read d 0 0 0 0 0 0)
      (9*eval 0 xs+8*xs.length+6-5*ones xs)
      (cfg .done (triple d (closed (eval 0 xs)) (un 0 0)) (triple 0 0 0)) := by
  let k := eval 0 xs
  let n := xs.length
  have good : ∀ j : ℕ, j≤n → d (j:ℤ) ≠ .home := by
    intro j hj
    by_cases e : j=n
    · subst j
      rw [bin.stop]
      decide
    · simpa using matches_nohome d 0 xs bin.digits j (by dsimp [n] at hj e; omega)
  have prep := prefix_scan d 0 0 xs bin.digits
  simp only [Int.zero_add] at prep
  have a := prep.trans (Trace.single (read_end d n k bin.stop))
  have b := a.trans (final_scan d n k)
  have c := b.trans (Trace.single (end_write d n k))
  have all := (c.trans (final_output d n k)).trans (final_digits d n k bin.home good)
  convert all using 1
  have eqn := cost_value 0 xs
  dsimp [k,n]
  omega

theorem binary_to_unary_halts (d : ℤ → Letter) (xs : List Bool) :
    TM.advance rule (cfg .done (triple d (closed (eval 0 xs)) (un 0 0)) (triple 0 0 0)) = none := rfl

theorem mark_at (n j : ℕ) (small : j<n) : closed n (j:ℤ) = .count := by
  have ne : (j:ℤ) ≠ n := by omega
  simp [closed,ne,un_inside 0 n j (by omega) small]

theorem stop_at (n : ℕ) : closed n (n:ℤ) = .delimiter := by simp [closed]

theorem home_at (n : ℕ) : closed n (-1) = .home := closed_home n

#print axioms binary_to_unary
#print axioms binary_to_unary_halts
#print axioms mark_at

end S008.Compiler.Unary
