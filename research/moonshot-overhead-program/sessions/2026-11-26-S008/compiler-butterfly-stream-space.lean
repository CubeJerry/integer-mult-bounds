import «compiler-butterfly-stream»

/-! Exact visited-cell intervals for a complete modular butterfly stream. -/

namespace S008.Compiler.ButterflyStream

open OAI.Computability.IntegerMultiplication OAI.Computability.NearSquareRoot
open Butterfly (Words Banks Origins Port)

def low (o : Origins) (n : ℕ) : Port → ℤ
  | .m => if n=0 then o .m else o .m-1
  | t => o t-2

def high (o : Origins) (n w : ℕ) : Port → ℤ
  | .m => if n=0 then o .m else o .m+w
  | t => o t+pos w n

private def safe (o : Origins) (n w : ℕ) (C : TM.Config Letter Stage Port) : Prop :=
  ∀ t, low o n t≤(C.tape t).pos ∧ (C.tape t).pos≤high o n w t

private theorem pos_nn (w n : ℕ) : 0≤pos w n := by unfold pos; positivity

private theorem pos_le (w i j : ℕ) (h : i≤j) : pos w i≤pos w j := by
  unfold pos
  exact mul_le_mul_of_nonneg_right (by exact_mod_cast h) (by positivity)

private theorem safe_normal (q d o n w x) (lo : -2≤x) (hi : x≤pos w n) : safe o n w (config q d o x) := by
  intro t
  by_cases z : n=0
  · subst n
    cases t <;> simp [low,high,config,heads,atPos] <;> omega
  · cases t <;> simp [low,high,config,heads,atPos,z] <;> omega

private structure Report (P : TM.Config Letter Stage Port → Prop) (C : TM.Config Letter Stage Port)
    (k : ℕ) (D : TM.Config Letter Stage Port) : Prop where
  path : Trace (TM.advance rule) C k D
  covered : ∀ j, j≤k → ∃ X, Trace (TM.advance rule) C j X ∧ P X

private theorem Report.trans {P C k D m F} (a : Report P C k D) (b : Report P D m F) : Report P C (k+m) F := by
  refine ⟨a.path.trans b.path,?_⟩
  intro u hu
  by_cases first : u≤k
  · exact a.covered u first
  · obtain ⟨x,hx,hp⟩ := b.covered (u-k) (by omega)
    refine ⟨x,?_,hp⟩
    simpa only [show k+(u-k)=u by omega] using a.path.trans hx

private theorem report_one {P C D} (step : TM.advance rule C=some D) (a : P C) (b : P D) : Report P C 1 D := by
  refine ⟨Trace.single step,?_⟩
  intro u hu
  rcases show u=0 ∨ u=1 by omega with rfl|rfl
  · exact ⟨C,.nil _,a⟩
  · exact ⟨D,Trace.single step,b⟩

private theorem report_zero {P C} (h : P C) : Report P C 0 C := by
  refine ⟨.nil _,?_⟩
  intro u hu
  obtain rfl : u=0 := by omega
  exact ⟨C,.nil _,h⟩

private theorem take_trace {X : Type} {m : X → Option X} {start finish k}
    (path : Trace m start k finish) (t : ℕ) (h : t≤k) : ∃ c, Trace m start t c := by
  induction path generalizing t with
  | nil x =>
    obtain rfl : t=0 := by omega
    exact ⟨x,.nil _⟩
  | @cons a b c k first _ ih =>
    cases t with
    | zero => exact ⟨a,.nil _⟩
    | succ t =>
      obtain ⟨y,rest⟩ := ih t (by omega)
      exact ⟨y,by simpa only [Nat.add_comm 1 t] using Trace.cons first rest⟩

private theorem safe_inner (s raw o n w j) (good : Valid s n w raw o) (hj : j<n) :
    Report (safe o n w) (config (.call (.forward (Butterfly.flags (s j) 0))) (after s raw o w j) o (pos w j))
      (2*w+2) (config (.call .halt) (after s raw o w (j+1)) o (pos w j)) := by
  refine ⟨inner_run s raw o n w j good hj,?_⟩
  intro u hu
  let p := heads o (pos w j)
  let d := after s raw o w j
  have valid := valid_current s raw o n w j good hj
  have all := Butterfly.butterfly (s j) d p w valid
  obtain ⟨C,current⟩ := take_trace all u hu
  refine ⟨embed C,by simpa only [p,d,at_origin] using lift current,?_⟩
  intro t
  have bound := (Butterfly.visited_iff (s j) d p w valid t (C.tape t).pos).mp ⟨u,hu,C,current,rfl⟩
  have nn := pos_nn w j
  have upper := separated w j n hj
  have nonempty : n≠0 := by omega
  cases t <;> simp [p,heads,embed,low,high,nonempty] at bound ⊢ <;> omega

private theorem safe_block (s raw o n w j) (good : Valid s n w raw o) (hj : j<n) :
    Report (safe o n w) (config .dispatch (after s raw o w j) o (pos w j)) (3*w+6)
      (config .dispatch (after s raw o w (j+1)) o (pos w (j+1))) := by
  let d := after s raw o w (j+1)
  have nn := pos_nn w j
  have bound := pos_le w (j+1) n (by omega)
  have current := pos_le w j n (by omega)
  have stop := separated w j n hj
  have next : pos w j+w+2≤pos w n := by simpa only [pos_next] using bound
  have keep : d .a=raw .a := (sources s raw o w (j+1)).1
  have start := report_one (block_start s raw o n w j good hj) (safe_normal _ _ o n w _ (by omega) current)
    (safe_normal _ _ o n w _ (by omega) current)
  have a := start.trans (safe_inner s raw o n w j good hj)
  have b := a.trans (report_one (return_from d o (pos w j)) (safe_normal _ d o n w _ (by omega) current)
    (safe_normal _ d o n w _ (by omega) current))
  have scan : Report (safe o n w) (config .skip d o (pos w j)) w (config .skip d o (pos w j+w)) := by
    refine ⟨tour_right s raw o n w j good hj d keep w le_rfl,?_⟩
    intro i hi
    exact ⟨_,tour_right s raw o n w j good hj d keep i hi,safe_normal _ _ o n w _ (by omega) (by omega)⟩
  have ending : d .a (heads o (pos w j+w) .a) = .delimiter := by
    simpa only [heads,keep,add_assoc] using (good.row j hj).endA
  have marker : d .a (heads o (pos w j+w+1) .a) = .home := by
    simpa only [heads,keep,add_assoc] using good.gap j hj
  have endStep := moving .skip .marker d o (pos w j+w) .right (by simp only [rule,ending])
  have markStep := moving .marker .dispatch d o (pos w j+w+1) .right (by simp only [rule,marker])
  have c := (b.trans scan).trans (report_one endStep (safe_normal _ _ o n w _ (by omega) (by omega))
    (safe_normal _ _ o n w _ (by simp [TM.Move.shift]; omega) (by simp [TM.Move.shift]; omega)))
  have e := c.trans (report_one markStep (safe_normal _ _ o n w _ (by simp only [TM.Move.shift]; omega) (by simp only [TM.Move.shift]; omega))
    (safe_normal _ _ o n w _ (by simp [TM.Move.shift]; omega) (by simp [TM.Move.shift]; omega)))
  change Report _ _ (1+(2*w+2)+1+w+1+1) (config .dispatch d o (pos w j+w+1+1)) at e
  rwa [show 1+(2*w+2)+1+w+1+1=3*w+6 by omega,show pos w j+w+1+1=pos w (j+1) by rw [pos_next]; omega] at e

private theorem safe_issuing (s raw o n w) (good : Valid s n w raw o) (j : ℕ) (hj : j≤n) :
    Report (safe o n w) (config .dispatch raw o 0) (j*(3*w+6)) (config .dispatch (after s raw o w j) o (pos w j)) := by
  induction j with
  | zero => simpa [pos,after] using report_zero (safe_normal .dispatch raw o n w 0 (by omega) (pos_nn w n))
  | succ j ih => simpa only [Nat.succ_mul] using (ih (by omega)).trans (safe_block s raw o n w j good (by omega))

private theorem safe_left_bits (s raw o n w j) (good : Valid s n w raw o) (hj : j<n) (d : Banks)
    (keep : d .a=raw .a) (i : ℕ) (h : i≤w) :
    Report (safe o n w) (config .rewind d o (pos w j+i-1)) i (config .rewind d o (pos w j-1)) := by
  have nn := pos_nn w j
  have upper := separated w j n hj
  induction i with
  | zero => simpa using report_zero (safe_normal .rewind d o n w (pos w j-1) (by omega) (by omega))
  | succ i ih =>
    have tag : d .a (heads o (pos w j+i) .a) = .bit ((s j).a i) := by
      simpa only [heads,keep,add_assoc] using (good.row j hj).bitA i (by omega)
    have one := report_one (back_step d o (pos w j+i) (by simp [tag]))
      (safe_normal _ d o n w _ (by omega) (by omega)) (safe_normal _ d o n w _ (by omega) (by omega))
    rw [show pos w j+(↑(i+1):ℤ)-1=pos w j+i by omega]
    simpa only [Nat.add_comm 1 i] using one.trans (ih (by omega))

private theorem safe_back_block (s raw o n w j) (good : Valid s n w raw o) (hj : j<n) (d : Banks) (keep : d .a=raw .a) :
    Report (safe o n w) (config .rewind d o (pos w (j+1)-1)) (w+2) (config .rewind d o (pos w j-1)) := by
  have nn := pos_nn w j
  have upper := pos_le w (j+1) n (by omega)
  rw [pos_next] at upper
  have endA : d .a (heads o (pos w j+w) .a)=.delimiter := by simpa only [heads,keep,add_assoc] using (good.row j hj).endA
  have gap : d .a (heads o (pos w j+w+1) .a)=.home := by simpa only [heads,keep,add_assoc] using good.gap j hj
  have a := report_one (back_step d o (pos w j+w+1) (by simp [gap]))
    (safe_normal _ d o n w _ (by omega) (by omega)) (safe_normal _ d o n w _ (by omega) (by omega))
  have b := report_one (back_step d o (pos w j+w) (by simp [endA]))
    (safe_normal _ d o n w _ (by omega) (by omega)) (safe_normal _ d o n w _ (by omega) (by omega))
  rw [show pos w j+w+1-1=pos w j+w by omega] at a
  have path := (a.trans b).trans (safe_left_bits s raw o n w j good hj d keep w le_rfl)
  rw [show pos w (j+1)-1=pos w j+w+1 by rw [pos_next]; omega]
  simpa only [show 1+1+w=w+2 by omega] using path

private theorem safe_rewinding (s raw o n w) (good : Valid s n w raw o) (d : Banks) (keep : d .a=raw .a)
    (j : ℕ) (hj : j≤n) :
    Report (safe o n w) (config .rewind d o (pos w j-1)) (j*(w+2)) (config .rewind d o (-1)) := by
  induction j with
  | zero => simpa [pos] using report_zero (safe_normal .rewind d o n w (-1) (by omega) (by have := pos_nn w n; omega))
  | succ j ih =>
    have path := (safe_back_block s raw o n w j good (by omega) d keep).trans (ih (by omega))
    simpa only [Nat.succ_mul,Nat.add_comm (w+2) (j*(w+2))] using path

private theorem safe_all (s raw o n w) (good : Valid s n w raw o) :
    Report (safe o n w) (config .dispatch raw o 0) (n*(4*w+8)+4) (config .done (after s raw o w n) o 0) := by
  let d := after s raw o w n
  have keep : d .a=raw .a := (sources s raw o w n).1
  have nn := pos_nn w n
  have finish : d .a (heads o (pos w n) .a)=.count := by simpa only [heads,keep] using good.finish
  have last := moving .dispatch .rewind d o (pos w n) .left (by simp only [rule,finish])
  have a := (safe_issuing s raw o n w good n le_rfl).trans (report_one last
    (safe_normal _ d o n w _ (by omega) (by omega))
    (safe_normal _ d o n w _ (by simp only [TM.Move.shift]; omega) (by simp only [TM.Move.shift]; omega)))
  have b := a.trans (safe_rewinding s raw o n w good d keep n le_rfl)
  have pre : d .a (heads o (-1) .a)=.home := by simpa only [heads,keep,sub_eq_add_neg] using good.entryHome
  have c := b.trans (report_one (back_step d o (-1) (by simp [pre])) (safe_normal _ d o n w _ (by omega) (by omega))
    (safe_normal _ d o n w _ (by omega) (by omega)))
  have entry : d .a (heads o (-2) .a)=.count := by simpa only [heads,keep,sub_eq_add_neg] using good.start
  have turn := moving .rewind .origin d o (-2) .right (by simp only [rule,entry])
  have returned := moving .origin .done d o (-1) .right (by simp only [rule])
  have e := c.trans (report_one turn (safe_normal _ d o n w _ (by omega) (by omega))
    (safe_normal _ d o n w _ (by decide) (by simp [TM.Move.shift]; omega)))
  have f := e.trans (report_one returned (safe_normal _ d o n w _ (by simp only [TM.Move.shift]; omega) (by simp only [TM.Move.shift]; omega))
    (safe_normal _ d o n w _ (by decide) (by simp [TM.Move.shift]; omega)))
  change Report _ _ (n*(3*w+6)+1+n*(w+2)+1+1+1) (config .done d o 0) at f
  rw [show 4*w+8=(3*w+6)+(w+2) by omega,Nat.mul_add]
  simpa only [show n*(3*w+6)+1+n*(w+2)+1+1+1=n*(3*w+6)+n*(w+2)+4 by omega] using f

theorem batch_fences (s raw o n w) (good : Valid s n w raw o) (u : ℕ) (h : u≤n*(4*w+8)+4)
    (C : TM.Config Letter Stage Port) (tr : Trace (TM.advance rule) (config .dispatch raw o 0) u C) (t : Port) :
    low o n t ≤ (C.tape t).pos ∧ (C.tape t).pos ≤ high o n w t := by
  obtain ⟨Y,hy,hs⟩ := (safe_all s raw o n w good).covered u h
  rw [trace_endpoint_unique tr hy]
  exact hs t

def space (n w : ℕ) : ℕ := 4*(n*(w+2)+3)+(if n=0 then 1 else w+2)

private theorem sum_spans (o : Origins) (n w : ℕ) :
    (∑ p : Port, (high o n w p+1-low o n p).toNat)=space n w := by
  have all : (Finset.univ : Finset Port)={.a,.b,.m,.sum,.diff} := by decide
  rw [all]
  have span (t : Port) : (o t+pos w n+1-(o t-2)).toNat = n*(w+2)+3 := by
    have e : pos w n = (n*(w+2):ℕ) := by simp [pos]
    rw [e]
    omega
  by_cases zero : n=0
  · subst n
    simp [low,high,space,pos]
  · have md : (o .m+w+1-(o .m-1)).toNat=w+2 := by omega
    simp [low,high,space,zero,span,md]; omega

theorem sharp_visits (s raw o n w) (good : Valid s n w raw o) :
    VisitsAtMost rule (config .dispatch raw o 0) (n*(4*w+8)+4) (space n w) := by
  rw [← sum_spans o n w]
  exact visitsAtMost_of_tape_fences (low o n) (high o n w) (batch_fences s raw o n w good)

private theorem bounded_move {A Q I : Type} (m : TM.Rule A Q I) {C D : TM.Config A Q I}
    (step : TM.advance m C=some D) (t : I) : (D.tape t).pos≤(C.tape t).pos+1 := by
  unfold TM.advance at step
  cases row : m C.pc (fun j => (C.tape j).view 0) with
  | none => simp [row] at step
  | some v =>
    rcases v with ⟨q,op⟩
    simp only [row,Option.map_some,Option.some.injEq] at step
    subst D
    change (C.tape t).pos+(op t).2.shift ≤ (C.tape t).pos+1
    cases e : (op t).2 <;> simp [TM.Move.shift]

private theorem cross_to_right {A Q I : Type} (m : TM.Rule A Q I) {C D : TM.Config A Q I} {k : ℕ}
    (tr : Trace (TM.advance m) C k D) (t : I) (z : ℤ) (lo : (C.tape t).pos≤z) (hi : z≤(D.tape t).pos) :
    ∃ j≤k, ∃ Y, Trace (TM.advance m) C j Y ∧ (Y.tape t).pos=z := by
  induction tr with
  | nil X => exact ⟨0,le_rfl,X,.nil _,by omega⟩
  | @cons X Y Z k step _ ih =>
    by_cases atStart : (X.tape t).pos=z
    · exact ⟨0,by omega,X,.nil _,atStart⟩
    · have next := bounded_move m step t
      obtain ⟨j,hj,T,trace,hp⟩ := ih (by omega) hi
      exact ⟨1+j,by omega,T,.cons step trace,hp⟩

private theorem active_head (o x p) (h : p≠Port.m) : heads o x p=o p+x := by
  cases p <;> simp [heads] at h ⊢

private theorem return_marks (s raw o n w) (good : Valid s n w raw o) :
    ∃ t, t+1≤n*(4*w+8)+4 ∧
      Trace (TM.advance rule) (config .dispatch raw o 0) t (config .rewind (after s raw o w n) o (-1)) ∧
      Trace (TM.advance rule) (config .dispatch raw o 0) (t+1) (config .rewind (after s raw o w n) o (-2)) := by
  let d := after s raw o w n
  have keep : d .a=raw .a := (sources s raw o w n).1
  have finish : d .a (heads o (pos w n) .a)=.count := by simpa only [heads,keep] using good.finish
  have last := moving .dispatch .rewind d o (pos w n) .left (by simp only [rule,finish])
  have path := ((issuing s raw o n w good n le_rfl).trans (Trace.single last)).trans (rewind_blocks s raw o n w good d keep n le_rfl)
  have pre : d .a (heads o (-1) .a)=.home := by simpa only [heads,keep,sub_eq_add_neg] using good.entryHome
  have more := path.trans (Trace.single (back_step d o (-1) (by simp [pre])))
  refine ⟨_,?_,path,more⟩
  have full : n*(4*w+8)=n*(3*w+6)+n*(w+2) := by
    rw [← Nat.mul_add,show 4*w+8=3*w+6+(w+2) by omega]
  rw [full]
  omega

/-- Absolute positions reached on every single tape, including the stationary modulus in an empty file. -/
theorem batch_visited_iff (s raw o n w) (good : Valid s n w raw o) (p : Port) (z : ℤ) :
    (p,z)∈visitedCells rule (config .dispatch raw o 0) (n*(4*w+8)+4) ↔ low o n p≤z ∧ z≤high o n w p := by
  constructor
  · rintro ⟨u,h,D,trace,found⟩
    change (D.tape p).pos=z at found
    rw [←found]
    exact batch_fences s raw o n w good u h D trace p
  · intro h
    by_cases modulus : p=.m
    · subst p
      by_cases zero : n=0
      · have hz : z=o .m := by simp [low,high,zero] at h; omega
        exact ⟨0,by omega,_,.nil _,by simp [config,atPos,heads,hz]⟩
      · have first : 0<n := by omega
        let row := heads o (pos w 0)
        have valid := valid_current s raw o n w 0 good first
        have bounds : row .m-1≤z ∧ z≤row .m+w := by simpa [row,heads,low,high,zero] using h
        obtain ⟨u,hu,C,tr,hit⟩ := (Butterfly.visited_iff (s 0) (after s raw o w 0) row w valid .m z).2 bounds
        have a := block_start s raw o n w 0 good first
        have b := lift tr
        simp only [row,at_origin] at b
        have path := (Trace.single a).trans b
        have width : 1*(4*w+8)≤n*(4*w+8) := Nat.mul_le_mul_right _ first
        refine ⟨1+u,by omega,embed C,?_,hit⟩
        simpa [after,pos] using path
    · have lo (h0 : p≠.m) : low o n p=o p-2 := by cases p <;> simp [low] at h0 ⊢
      have hi (h0 : p≠.m) : high o n w p=o p+pos w n := by cases p <;> simp [high] at h0 ⊢
      rw [lo modulus,hi modulus] at h
      by_cases right : o p≤z
      · have path := issuing s raw o n w good n le_rfl
        have beg : ((config .dispatch raw o 0).tape p).pos≤z := by simpa [config,atPos,active_head o 0 p modulus] using right
        have ending : z≤((config .dispatch (after s raw o w n) o (pos w n)).tape p).pos := by
          simpa [config,atPos,active_head o (pos w n) p modulus] using h.2
        obtain ⟨u,hu,Y,tr,hit⟩ := cross_to_right rule path p z beg ending
        have big : n*(3*w+6)≤n*(4*w+8) := Nat.mul_le_mul_left _ (by omega)
        exact ⟨u,by omega,Y,tr,hit⟩
      · obtain ⟨t,bound,a,b⟩ := return_marks s raw o n w good
        rcases show z=o p-1 ∨ z=o p-2 by omega with hz|hz
        · exact ⟨t,by omega,_,a,by simp [config,atPos,active_head o (-1) p modulus,hz,sub_eq_add_neg]⟩
        · exact ⟨t+1,bound,_,b,by simp [config,atPos,active_head o (-2) p modulus,hz,sub_eq_add_neg]⟩

theorem batch_exact_space (s raw o n w) (good : Valid s n w raw o) :
    (visitedCells rule (config .dispatch raw o 0) (n*(4*w+8)+4)).ncard=space n w := by
  classical
  let fiber (p : Port) := (Finset.Icc (low o n p) (high o n w p)).map (Function.Embedding.sectR p ℤ)
  have membership (p t : Port) (z : ℤ) : (p,z)∈fiber t ↔ p=t ∧ low o n t≤z ∧ z≤high o n w t := by
    change (p,z)∈Finset.map _ _ ↔ _
    rw [Finset.mem_map]
    constructor
    · rintro ⟨v,hv,eq⟩
      change (t,v)=(p,z) at eq
      have hp : t=p := congrArg Prod.fst eq
      have hz : v=z := congrArg Prod.snd eq
      subst v
      exact ⟨hp.symm,Finset.mem_Icc.mp hv⟩
    · rintro ⟨rfl,lo,hi⟩
      exact ⟨z,Finset.mem_Icc.mpr ⟨lo,hi⟩,rfl⟩
  have separ : (↑(Finset.univ : Finset Port) : Set Port).PairwiseDisjoint fiber := by
    intro p _ t _ distinct
    apply Finset.disjoint_left.mpr
    rintro ⟨q,z⟩ inP inT
    exact distinct ((membership q p z|>.mp inP).1.symm.trans (membership q t z|>.mp inT).1)
  have cells : visitedCells rule (config .dispatch raw o 0) (n*(4*w+8)+4) =
      ↑((Finset.univ : Finset Port).biUnion fiber) := by
    ext ⟨p,z⟩
    rw [batch_visited_iff s raw o n w good]
    change (_ ∧ _) ↔ (p,z)∈Finset.univ.biUnion fiber
    rw [Finset.mem_biUnion]
    constructor
    · intro h
      exact ⟨p,Finset.mem_univ _,(membership p p z).2 ⟨rfl,h⟩⟩
    · rintro ⟨t,_,member⟩
      obtain ⟨rfl,lo,hi⟩ := (membership p t z).mp member
      exact ⟨lo,hi⟩
  rw [cells,Set.ncard_coe_finset,Finset.card_biUnion separ]
  simpa only [fiber,Finset.card_map,Int.card_Icc] using sum_spans o n w

end S008.Compiler.ButterflyStream
