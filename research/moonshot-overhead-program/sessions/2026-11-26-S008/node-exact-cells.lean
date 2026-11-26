import NodeSymbolic

/-! Exact cardinalities of the original physical visited sets for accepted finite-table runs. -/

namespace S008.ExactCells

open OAI.Computability.IntegerMultiplication OAI.Computability.NearSquareRoot
open S008.Recount (Letter)
open S008.NodeSource

def precise {k s : ℕ} (r : Runtime k s) : Prop :=
  ∀ i : Fin k, r.low[i]=r.windows[i].pos ∧ r.high[i]=r.windows[i].pos

theorem precise_fenced {k s : ℕ} {r : Runtime k s} (h : precise r) : fenced r := by
  intro i
  rw [(h i).1,(h i).2]
  exact ⟨le_rfl,le_rfl⟩

private theorem last_move {k s : ℕ} (p : Table k s) {r d : Runtime k s}
    (h : step p r=some d) (i : Fin k) :
    d.low[i]=min r.low[i] d.windows[i].pos ∧
    d.high[i]=max r.high[i] d.windows[i].pos ∧
    r.windows[i].pos-1≤d.windows[i].pos ∧ d.windows[i].pos≤r.windows[i].pos+1 := by
  unfold step at h
  rcases hr : rule p r.pc (fun j => r.windows[j].atHead) with _ | qr
  · rw [hr] at h
    contradiction
  rcases qr with ⟨q,op⟩
  rw [hr] at h
  cases h
  simp
  cases hm : (op i).2 <;> simp [S008.Recount.Window.apply] <;> omega

private theorem prefix_fence {k s : ℕ} (p : Table k s) {r d : Runtime k s}
    {n u : ℕ} (h : run p r n=some d) (hf : fenced r) (hu : u≤n)
    {c : TM.Config Letter (Fin (s+1)) (Fin k)}
    (hc : Trace (TM.advance (rule p)) (physical r) u c) (i : Fin k) :
    d.low[i]≤(c.tape i).pos ∧ (c.tape i).pos≤d.high[i] := by
  have eq : u+(n-u)=n := by omega
  have both := run_add p r u (n-u)
  rw [eq,h] at both
  cases e : run p r u with
  | none => rw [e] at both; contradiction
  | some w =>
    rw [e] at both
    have q := trace_endpoint_unique hc (sound p e)
    subst c
    obtain ⟨hl,hh⟩ := (run_fenced p hf e) i
    obtain ⟨ll,gg⟩ := extrema_run p both.symm i
    exact ⟨le_trans ll hl,le_trans hh gg⟩

theorem visited_iff {k s : ℕ} (p : Table k s) {r d : Runtime k s} {n : ℕ}
    (h : run p r n=some d) (hr : precise r) (i : Fin k) (z : ℤ) :
    (i,z)∈visitedCells (rule p) (physical r) n ↔ d.low[i]≤z ∧ z≤d.high[i] := by
  constructor
  · rintro ⟨u,hu,c,hc,hz⟩
    change (c.tape i).pos=z at hz
    rw [← hz]
    exact prefix_fence p h (precise_fenced hr) hu hc i
  intro inside
  induction n generalizing d with
  | zero =>
    have e : r=d := Option.some.inj h
    subst d
    refine ⟨0,le_rfl,physical r,.nil _,?_⟩
    change r.windows[i].pos=z
    have ⟨a,b⟩ := hr i
    omega
  | succ n ih =>
    have both := run_add p r n 1
    rw [h] at both
    cases e : run p r n with
    | none => rw [e] at both; contradiction
    | some w =>
      rw [e] at both
      have last : step p w=some d := by simpa [run] using both.symm
      by_cases mid : w.low[i]≤z ∧ z≤w.high[i]
      · obtain ⟨u,hu,c,hc,ez⟩ := ih e mid
        exact ⟨u,by omega,c,hc,ez⟩
      · have curr := (run_fenced p (precise_fenced hr) e) i
        have ⟨l,u,lb,ub⟩ := last_move p last i
        have same : d.windows[i].pos=z := by
          omega
        exact ⟨n+1,le_rfl,physical d,sound p h,same⟩

theorem cardinality {k s : ℕ} (p : Table k s) {r d : Runtime k s} {n : ℕ}
    (h : run p r n=some d) (hr : precise r) :
    (visitedCells (rule p) (physical r) n).ncard =
      ∑ i : Fin k, (d.high[i]+1-d.low[i]).toNat := by
  classical
  let cells (i : Fin k) := (Finset.Icc d.low[i] d.high[i]).map (Function.Embedding.sectR i ℤ)
  have whole : visitedCells (rule p) (physical r) n=((Finset.univ.biUnion cells : Finset (Fin k × ℤ)) : Set (Fin k × ℤ)) := by
    ext ⟨i,z⟩
    rw [visited_iff p h hr]
    constructor
    · intro hz
      exact Finset.mem_biUnion.mpr ⟨i,Finset.mem_univ _,
        Finset.mem_map.mpr ⟨z,Finset.mem_Icc.mpr hz,rfl⟩⟩
    · intro hz
      rcases Finset.mem_biUnion.mp hz with ⟨j,_,hj⟩
      rcases Finset.mem_map.mp hj with ⟨x,hx,e⟩
      have ej : j=i := congrArg Prod.fst e
      have ex : x=z := congrArg Prod.snd e
      subst j; subst x
      exact Finset.mem_Icc.mp hx
  rw [whole,Set.ncard_coe_finset,Finset.card_biUnion]
  · simp [cells,Int.card_Icc]
  · intro i _ j _ ne
    apply Finset.disjoint_left.mpr
    intro z hi hj
    rcases Finset.mem_map.mp hi with ⟨x,_,hx⟩
    rcases Finset.mem_map.mp hj with ⟨y,_,hy⟩
    exact ne (congrArg Prod.fst (hx.trans hy.symm))

theorem symbolic_exact {k s : ℕ} (p : Table k s) (entry : Fin (s+1))
    (a : Array (List S008.Symbolic.Glyph)) (clock cells : ℕ)
    (expected : Vector S008.Symbolic.WindowS k) (v : ℕ → Bool)
    (h : S008.Symbolic.check p entry a clock cells expected=true) :
    (visitedCells (rule p) (physical ((S008.Symbolic.initial entry a).eval v)) clock).ncard=cells := by
  cases ht : S008.Symbolic.run p (S008.Symbolic.initial entry a) clock with
  | none => simp [S008.Symbolic.check,ht] at h
  | some d =>
    simp only [S008.Symbolic.check,ht,decide_eq_true_eq] at h
    have pre : precise ((S008.Symbolic.initial (k:=k) entry a).eval v) := by
      intro i
      simp [S008.Symbolic.initial,S008.Symbolic.State.eval,S008.Symbolic.WindowS.eval]
    have e := cardinality p (S008.Symbolic.run_eval v p ht) pre
    exact e.trans h.2.1

end S008.ExactCells
