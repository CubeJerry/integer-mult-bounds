import OAI.Computability.NearSquareRoot.VisitedCells

/-! A finite literal width dispatcher in the original fixed multitape machine model. -/

namespace S008.WidthDispatch

open OAI.Computability.IntegerMultiplication
open OAI.Computability.NearSquareRoot

/-- The scan control remembers the number of input digits seen, up to the literal H.
    The return control remembers only a bounded number of left moves and the answer. -/
inductive PC (H : ℕ) where
  | scan (j : Fin (H+1))
  | back (answer : Bool) (j : Fin (H+1))
  | done (answer : Bool)
  deriving DecidableEq

instance (H : ℕ) : Finite (PC H) := by
  classical
  let encode : PC H → Fin (H+1) ⊕ (Bool × Fin (H+1)) ⊕ Bool
    | .scan j => .inl j
    | .back b j => .inr (.inl (b,j))
    | .done b => .inr (.inr b)
  apply Finite.of_injective encode
  intro x y h
  cases x <;> cases y <;> simp_all [encode]

def index {H : ℕ} (j : ℕ) (hj : j ≤ H) : Fin (H+1) := ⟨j, by omega⟩

def returning {H : ℕ} (answer : Bool) (j : Fin (H+1)) : PC H :=
  if j.val=0 then .done answer else .back answer j

def next {H : ℕ} (q : PC H) (digit : Bool) : Option (PC H × TM.Move) :=
  match q with
  | .scan j =>
    if h : j.val < H ∧ digit = true then
      some (.scan (index (j.val+1) (by omega)), .right)
    else
      some (returning (decide (j.val=H) && digit) j, .stay)
  | .back b j =>
    if j.val=0 then some (.done b, .stay)
    else some (returning b (index (j.val-1) (by have := j.isLt; omega)), .left)
  | .done _ => none

/-- Only the head's scanned symbol and the finite control enter the literal step. -/
def rule {A : Type} (H : ℕ) (isDigit : A → Bool) : TM.Rule A (PC H) Unit :=
  fun q cells => (next q (isDigit (cells ()))).map
    fun (s,m) => (s,fun i => (cells i,m))

def shiftTape {A : Type} (t : TM.Tape A) (d : ℤ) : TM.Tape A :=
  ⟨t.pos + d, fun i => t.view (i+d)⟩

@[simp] theorem shift_zero {A : Type} (t : TM.Tape A) : shiftTape t 0 = t := by
  cases t
  simp [shiftTape]

theorem shift_apply {A : Type} (t : TM.Tape A) (d : ℤ) (mv : TM.Move) :
    (shiftTape t d).apply ((shiftTape t d).view 0,mv) = shiftTape t (d+mv.shift) := by
  unfold TM.Tape.apply shiftTape
  dsimp only
  congr 1
  · omega
  · funext i
    split
    · rename_i h
      congr 1
      omega
    · congr 1
      omega

def config {A : Type} {H : ℕ} (t : TM.Tape A) (q : PC H) (d : ℤ) :
    TM.Config A (PC H) Unit := ⟨q, fun _ => shiftTape t d⟩

theorem step_of_next {A : Type} {H : ℕ} (isDigit : A → Bool)
    (t : TM.Tape A) (d : ℤ) (q s : PC H) (mv : TM.Move)
    (hn : next q (isDigit (t.view d)) = some (s,mv)) :
    TM.advance (rule H isDigit) (config t q d) = some (config t s (d+mv.shift)) := by
  unfold TM.advance rule config
  simp only [shiftTape, zero_add, hn, Option.map_some]
  congr 2
  funext i
  simpa only [shiftTape,zero_add] using shift_apply t d mv

@[simp] theorem stop_is_halt {A : Type} {H : ℕ} (isDigit : A → Bool)
    (t : TM.Tape A) (answer : Bool) (d : ℤ) :
    TM.advance (rule H isDigit) (config t (.done answer) d) = none := rfl

theorem right_step {A : Type} {H : ℕ} (isDigit : A → Bool) (t : TM.Tape A)
    (j : ℕ) (hj : j < H) (hd : isDigit (t.view j)=true) :
    TM.advance (rule H isDigit) (config t (.scan (index j (by omega))) j) =
      some (config t (.scan (index (j+1) (by omega))) (j+1)) := by
  have h := step_of_next (H:=H) isDigit t (j : ℤ) (.scan (index j (by omega)))
    (.scan (index (j+1) (by omega))) .right (by simp [next,index,hj,hd])
  exact h

theorem scan_prefix {A : Type} {H : ℕ} (isDigit : A → Bool) (t : TM.Tape A)
    (j : ℕ) (hj : j ≤ H) (hd : ∀ i < j, isDigit (t.view i)=true) :
    Trace (TM.advance (rule H isDigit))
      (config t (.scan (index 0 (Nat.zero_le H))) 0)
      j (config t (.scan (index j hj)) j) := by
  induction j with
  | zero => exact .nil _
  | succ n ih =>
    exact (ih (by omega) (by intro i hi; exact hd i (by omega))).trans
      (Trace.single (right_step isDigit t n (by omega) (hd n (by omega))))

theorem left_step {A : Type} {H : ℕ} (isDigit : A → Bool) (t : TM.Tape A)
    (b : Bool) (j : ℕ) (hj : j+1 ≤ H) :
    TM.advance (rule H isDigit)
      (config t (returning b (index (j+1) hj)) (j+1)) =
      some (config t (returning b (index j (by omega))) j) := by
  have h := step_of_next (H:=H) isDigit t (j+1 : ℤ)
    (returning b (index (j+1) hj)) (returning b (index j (by omega))) .left
    (by simp [returning,next,index]; rfl)
  simpa [TM.Move.shift] using h

theorem return_prefix {A : Type} {H : ℕ} (isDigit : A → Bool) (t : TM.Tape A)
    (b : Bool) (start steps : ℕ) (hs : start ≤ H) (hl : steps ≤ start) :
    Trace (TM.advance (rule H isDigit))
      (config t (returning b (index start hs)) start) steps
      (config t (returning b (index (start-steps) (by omega))) (start-steps : ℕ)) := by
  induction steps with
  | zero => exact .nil _
  | succ v ih =>
    have hp : start-v = (start-(v+1))+1 := by omega
    have h := left_step isDigit t b (start-(v+1)) (H:=H) (by omega)
    have hb := ih (by omega)
    let w := start-(v+1)
    have hw : w+1=start-v := hp.symm
    have h' : TM.advance (rule H isDigit)
        (config t (returning b (index (start-v) (by omega))) (start-v : ℕ)) =
        some (config t (returning b (index (start-(v+1)) (by omega))) (start-(v+1) : ℕ)) := by
      convert h using 2; simp_all [config, index]
    exact hb.trans (Trace.single h')

theorem stop_step {A : Type} {H : ℕ} (isDigit : A → Bool) (t : TM.Tape A)
    (n : ℕ) (hd : ∀ i < n, isDigit (t.view i)=true) (he : isDigit (t.view n)=false) :
    let p := min n H
    TM.advance (rule H isDigit)
      (config t (.scan (index p (Nat.min_le_right _ _))) p) =
      some (config t (returning (decide (H<n)) (index p (Nat.min_le_right _ _))) p) := by
  dsimp only
  have hs : next (.scan (index (min n H) (Nat.min_le_right n H)))
      (isDigit (t.view (min n H : ℕ))) =
      some (returning (decide (H<n)) (index (min n H) (Nat.min_le_right n H)), TM.Move.stay) := by
    by_cases h : H<n
    · simp [next,index,Nat.min_eq_right (Nat.le_of_lt h),hd H h,h]
    · simp [next,index,Nat.min_eq_left (Nat.le_of_not_gt h),he,h]
  have step := step_of_next (H:=H) isDigit t (min n H : ℕ)
    (.scan (index (min n H) (Nat.min_le_right n H)))
    (returning (decide (H<n)) (index (min n H) (Nat.min_le_right n H))) .stay hs
  simpa [TM.Move.shift] using step

/-- Literal threshold test, exact clock, exact recovery of the input tape, and halt. -/
theorem dispatch {A : Type} (H : ℕ) (isDigit : A → Bool) (t : TM.Tape A)
    (n : ℕ) (hd : ∀ i < n, isDigit (t.view i)=true) (he : isDigit (t.view n)=false) :
    let p := min n H
    let start := config t (.scan (index 0 (Nat.zero_le H))) 0
    let finish := config t (.done (decide (H<n)) : PC H) 0
    Trace (TM.advance (rule H isDigit)) start (2*p+1) finish ∧
      TM.advance (rule H isDigit) finish = none ∧ finish.tape () = t := by
  dsimp only
  let p := min n H
  have sp := scan_prefix (H:=H) isDigit t p (Nat.min_le_right _ _)
    (by intro i hi; exact hd i (lt_of_lt_of_le hi (Nat.min_le_left _ _)))
  have stop := stop_step (H:=H) isDigit t n hd he
  have back := return_prefix (H:=H) isDigit t (decide (H<n)) p p
    (Nat.min_le_right _ _) (le_refl _)
  have total := (sp.trans (Trace.single stop)).trans back
  have eqTime : p+1+p=2*p+1 := by omega
  have result := show Trace (TM.advance (rule H isDigit))
      (config t (.scan (index 0 (Nat.zero_le H))) 0) (2*p+1)
      (config t (.done (decide (H<n))) 0) by
    simpa [eqTime,returning,index] using total
  exact ⟨result, rfl, shift_zero _⟩

/-- At each earlier step, an explicit reference prefix gives the current head position.
    The result counts the union of cells ever visited, including the entries and halt. -/
theorem dispatch_visits {A : Type} (H : ℕ) (isDigit : A → Bool) (t : TM.Tape A)
    (n : ℕ) (hd : ∀ i < n, isDigit (t.view i)=true) (he : isDigit (t.view n)=false) :
    let p := min n H
    let start := config t (.scan (index 0 (Nat.zero_le H))) 0
    VisitsAtMost (rule H isDigit) start (2*p+1) (p+1) := by
  dsimp only
  let p := min n H
  let start := config t (.scan (index 0 (Nat.zero_le H))) 0
  have hpH : p≤H := Nat.min_le_right _ _
  have hpn : p≤n := Nat.min_le_left _ _
  have fence : ∀ u ≤ 2*p+1, ∀ c : TM.Config A (PC H) Unit,
      Trace (TM.advance (rule H isDigit)) start u c →
        ∀ i, t.pos ≤ (c.tape i).pos ∧ (c.tape i).pos ≤ t.pos+p := by
    intro u hu c hc i
    by_cases small : u≤p
    · have known := scan_prefix (H:=H) isDigit t u (le_trans small hpH)
        (by intro j hj; exact hd j (by omega))
      have ec := trace_endpoint_unique hc known
      rw [ec]
      change t.pos ≤ t.pos+u ∧ t.pos+u ≤ t.pos+p
      omega
    · let diff := u-(p+1)
      have hdif : diff≤p := by dsimp [diff]; omega
      have hs := scan_prefix (H:=H) isDigit t p hpH (by intro j hj; exact hd j (by omega))
      have hm := stop_step (H:=H) isDigit t n hd he
      have hb := return_prefix (H:=H) isDigit t (decide (H<n)) p diff hpH hdif
      have known := (hs.trans (Trace.single hm)).trans hb
      have cen : p+1+diff=u := by dsimp [diff]; omega
      rw [cen] at known
      have ec := trace_endpoint_unique hc known
      rw [ec]
      change t.pos ≤ t.pos+((p-diff : ℕ):ℤ) ∧ t.pos+((p-diff : ℕ):ℤ) ≤ t.pos+p
      omega
  have v := visitsAtMost_of_tape_fences (m:=rule H isDigit) (init:=start)
    (steps:=2*p+1) (fun _ => t.pos) (fun _ => t.pos+p) fence
  have card0 : t.pos+(p:ℤ)+1-t.pos=(p:ℤ)+1 := by omega
  have card1 : ((p:ℤ)+1).toNat=p+1 := by omega
  simpa only [Finset.sum_const,Finset.card_univ,Fintype.card_unit,one_smul,card0,card1] using v

/-- A canonical binary numeral has Nat.log 2 e + 1 cells, including its
    single-letter representation of zero. The threshold is positive. -/
theorem canonical_answer (H e : ℕ) (hH : 0<H) :
    H < Nat.log 2 e + 1 ↔ 2^H ≤ e := by
  cases e with
  | zero =>
    constructor
    · intro h
      change H < 0+1 at h
      omega
    · intro h
      have hp : 0<2^H := by positivity
      omega
  | succ e =>
    rw [Nat.lt_succ_iff]
    exact Nat.le_log_iff_pow_le (by decide) (Nat.succ_ne_zero _)

section Ambient

variable {A Q I : Type} [DecidableEq I]

/-- Install any single-head rule on one dedicated tape of an arbitrary fixed arena. -/
def liftRule (port : I) (m : TM.Rule A Q Unit) : TM.Rule A Q I :=
  fun q cells => (m q (fun _ => cells port)).map fun (q',ops) =>
    (q', fun i => if i=port then ops () else (cells i,TM.Move.stay))

def install (port : I) (parked : I → TM.Tape A) (c : TM.Config A Q Unit) :
    TM.Config A Q I :=
  ⟨c.pc, fun i => if i=port then c.tape () else parked i⟩

theorem same_stay (t : TM.Tape A) : t.apply (t.view 0,TM.Move.stay)=t := by
  simpa [TM.Move.shift] using shift_apply t 0 TM.Move.stay

theorem lift_advance (port : I) (parked : I → TM.Tape A) (m : TM.Rule A Q Unit)
    (c : TM.Config A Q Unit) :
    TM.advance (liftRule port m) (install port parked c) =
      (TM.advance m c).map (install port parked) := by
  have cells : (fun i : Unit => (c.tape i).view 0)=(fun _ : Unit => (c.tape ()).view 0) := by
    funext i
    cases i
    rfl
  unfold TM.advance liftRule install
  simp only [ite_true, cells]
  rcases e : m c.pc (fun _ => (c.tape ()).view 0) with _ | z
  · rfl
  rcases z with ⟨q,ops⟩
  simp only [Option.map_some]
  congr 2
  funext i
  by_cases hi : i=port
  · simp [hi]
  · simp [hi,same_stay]

theorem lift_trace (port : I) (parked : I → TM.Tape A) (m : TM.Rule A Q Unit)
    {c d : TM.Config A Q Unit} {n : ℕ} (h : Trace (TM.advance m) c n d) :
    Trace (TM.advance (liftRule port m)) (install port parked c) n (install port parked d) := by
  induction h with
  | nil c => exact .nil _
  | cons hx _ ih =>
    exact .cons (by rw [lift_advance,hx]; rfl) ih

theorem lift_halt (port : I) (parked : I → TM.Tape A) (m : TM.Rule A Q Unit)
    {c : TM.Config A Q Unit} (h : TM.advance m c=none) :
    TM.advance (liftRule port m) (install port parked c)=none := by
  rw [lift_advance,h]
  rfl

private theorem prefix_exists {X : Type} {step : X → Option X} {x z : X} {n u : ℕ}
    (h : Trace step x n z) (hu : u≤n) : ∃ y, Trace step x u y := by
  induction h generalizing u with
  | nil x =>
    have h0 : u=0 := by omega
    subst u
    exact ⟨x,.nil _⟩
  | @cons x y z n hxy hyz ih =>
    cases u with
    | zero => exact ⟨_,.nil _⟩
    | succ v =>
      obtain ⟨w,hw⟩ := ih (by omega : v≤n)
      exact ⟨w,by simpa [Nat.add_comm] using Trace.cons hxy hw⟩

/-- The only additional visits are the initial parked head positions. -/
theorem lift_visits [Fintype I] (port : I) (parked : I → TM.Tape A)
    (m : TM.Rule A Q Unit) {c d : TM.Config A Q Unit} {n cells : ℕ}
    (run : Trace (TM.advance m) c n d) (cap : VisitsAtMost m c n cells) :
    VisitsAtMost (liftRule port m) (install port parked c) n (cells+Fintype.card I) := by
  classical
  obtain ⟨source,hsize,contains⟩ := cap
  let active := source.image (fun a : Unit × ℤ => (port,a.2))
  let idle := Finset.univ.image (fun i : I => (i,(parked i).pos))
  refine ⟨active ∪ idle, ?_, ?_⟩
  · calc
      (active ∪ idle).card ≤ active.card + idle.card := Finset.card_union_le _ _
      _ ≤ source.card + Fintype.card I := Nat.add_le_add (Finset.card_image_le)
        (by exact (Finset.card_image_le).trans (by simp))
      _ ≤ cells + Fintype.card I := Nat.add_le_add_right hsize _
  · intro u hu endpoint hpartial i
    obtain ⟨y,hy⟩ := prefix_exists run hu
    have eq := trace_endpoint_unique hpartial (lift_trace port parked m hy)
    subst endpoint
    by_cases hi : i=port
    · subst i
      apply Finset.mem_union_left
      have keep := contains u hu y hy ()
      exact Finset.mem_image.mpr ⟨((),(y.tape ()).pos),keep,by simp [install]⟩
    · apply Finset.mem_union_right
      exact Finset.mem_image.mpr ⟨i,Finset.mem_univ _,by simp [install,hi]⟩

end Ambient

end S008.WidthDispatch
