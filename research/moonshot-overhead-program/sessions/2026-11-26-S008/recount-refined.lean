import S008.RecountSharp

namespace S008.Recount.Refined

open S008.NumericalCutoff S008.Recount.Sharp
set_option exponentiation.threshold 6000

def Z : ℕ := 8931714897907030
def den : ℕ := 98304
def historyCap : ℕ := 1160000000000

/-- Compute the actual integral-height 29 breakpoints at the common denominator. -/
def cap (j l : ℕ) : ℕ := 240*(l*(3*j+(3*j+2).log2+3)*8^j+2)

def edges : List (ℕ×ℕ) :=
  [(0,den/2),(240*(2^17+2),17*den/64)] ++
  (List.range 10).flatMap fun k =>
    let j := k+4
    ([(cap j 1, 17*den/(4*2^j)),(cap j 2,11*den/(3*2^j)),(cap j 4,10*den/(3*2^j))] :
      List (ℕ×ℕ)).filter fun p => decide (240*(2^17+2)<p.1 ∧ p.1≤Z+2)

def heights : ℕ → ℕ → ℕ → List (ℕ×ℕ) → List (ℕ×ℕ)
  | _,_,_,[] => []
  | p,s,h,(v,t)::es =>
    let h' := h + (v-p)*s
    (v,h')::heights v t h' es

def nodes := heights 0 0 0 edges

theorem exact_weights : nodes.length=29 ∧
    nodes.getLast?=some (6201245580657120, 6181211607280*den) ∧
    edges.getLast?=some (6201245580657120,17*den/32768) ∧
    (6181211607280*den-6201245580657120*(17*den/32768))*1024=3035148971130625*den := by decide

noncomputable def α : ℝ := 17/32768
noncomputable def β : ℝ := 3035148971130625/1024
noncomputable def A (x : ℝ) : ℝ := 183+4*logTwo (x+2)+β+α*(x+2)
noncomputable def movement (x : ℝ) : ℝ := A x+(33/4)*phi (x+2)

private noncomputable def u2 : ℝ := 52+(5129255230574657314728974059794661+1:ℝ)/2^112
private noncomputable def u4 : ℝ := 52+(5129255230574658992100232380384526+1:ℝ)/2^112
private noncomputable def l1 : ℝ := 52+(5129255230574656476043344899499587:ℝ)/2^112
private noncomputable def l3 : ℝ := 52+(5129255230574658153414603220089640:ℝ)/2^112

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
private theorem upper_2 : logTwo (Z+2:ℝ) ≤ u2 := by
  rw [show (Z:ℝ)+2=8931714897907032 by norm_num [Z]]
  apply certify Q (first 8931714897907032 52) 8931714897907032 52 5129255230574657314728974059794661
  all_goals decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
private theorem upper_4 : logTwo (Z+4:ℝ) ≤ u4 := by
  rw [show (Z:ℝ)+4=8931714897907034 by norm_num [Z]]
  apply certify Q (first 8931714897907034 52) 8931714897907034 52 5129255230574658992100232380384526
  all_goals decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
private theorem lower_1 : l1 ≤ logTwo (Z+1:ℝ) := by
  rw [show (Z:ℝ)+1=8931714897907031 by norm_num [Z]]
  apply certify_lower Q (first 8931714897907031 52) 8931714897907031 52 5129255230574656476043344899499587
  all_goals decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
private theorem lower_3 : l3 ≤ logTwo (Z+3:ℝ) := by
  rw [show (Z:ℝ)+3=8931714897907033 by norm_num [Z]]
  apply certify_lower Q (first 8931714897907033 52) 8931714897907033 52 5129255230574658153414603220089640
  all_goals decide

theorem passing : movement Z + 246303/10^9 ≤ (Z:ℝ)/1000 := by
  let rem : ℝ := (Z:ℝ)/1000-183-4*u2-β-α*((Z:ℝ)+2)-246303/10^9
  have hr : 0≤rem := by norm_num [rem,Z,u2,α,β]
  have hh : logTwo (((Z:ℝ)+2)+2) ≤ u4 := by
    rw [show (Z:ℝ)+2+2=(Z:ℝ)+4 by ring]
    exact upper_4
  have hl : (33/4)*phi ((Z:ℝ)+2)≤rem := by
    apply le_of_pow_le_pow_left₀ (by decide : (3:ℕ)≠0) hr
    rw [mul_pow,phi_cube (by positivity)]
    calc
      (33/4:ℝ)^3 * (((Z:ℝ)+2)^2 * logTwo (((Z:ℝ)+2)+2)) ≤ (33/4)^3 * (((Z:ℝ)+2)^2*u4) :=
        mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left hh (sq_nonneg _)) (by norm_num)
      _ ≤ _ := by norm_num [rem,Z,u2,u4,α,β]
  unfold movement A
  dsimp [rem] at hl
  linarith only [hl,upper_2]

theorem preceding : ((Z:ℝ)-1)/1000 + 133976/10^9 < movement ((Z:ℝ)-1) := by
  let x : ℝ := (Z:ℝ)-1
  let rem : ℝ := x/1000-183-4*l1-β-α*(x+2)+133976/10^9
  have hh : l3 ≤ logTwo ((x+2)+2) := by
    dsimp [x]
    rw [show (Z:ℝ)-1+2+2=(Z:ℝ)+3 by ring]
    exact lower_3
  have h2 : l1 ≤ logTwo (x+2) := by
    dsimp [x]
    rw [show (Z:ℝ)-1+2=(Z:ℝ)+1 by ring]
    exact lower_1
  have hc : rem^3 < ((33/4)*phi (x+2))^3 := by
    rw [mul_pow,phi_cube (by dsimp [x]; norm_num [Z])]
    calc
      rem^3 < (33/4)^3*((x+2)^2*l3) := by norm_num [x,rem,Z,l1,l3,α,β]
      _ ≤ _ := mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left hh (sq_nonneg _)) (by norm_num)
  have hpos : 0≤(33/4)*phi (x+2) := by
    apply mul_nonneg (by norm_num)
    unfold phi
    apply Real.rpow_nonneg _ _
    apply mul_nonneg (sq_nonneg _)
    unfold logTwo
    apply div_nonneg (Real.log_nonneg _) (Real.log_nonneg (by norm_num))
    norm_num [x,Z]
  have hl : rem < (33/4)*phi (x+2) := by
    by_contra! hn
    exact (not_lt_of_ge (pow_le_pow_left₀ hpos hn 3)) hc
  change x/1000+133976/10^9 < movement x
  unfold movement A
  dsimp [rem] at hl
  linarith only [hl,h2]

def earlierOK (p : ℕ×ℕ) : Bool :=
  let (v,h) := p
  let q := ((v+2)^64).log2
  decide (h≤historyCap*den ∨ ((2:ℕ)^q≤(v+2)^64 ∧
    64*(4*(h-historyCap*den))^3 ≤ 159^3*v^2*q*den^3))

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
theorem historical_cubics : nodes.all earlierOK = true := by decide

private theorem nonnegPhi {v : ℝ} (hv : 0≤v) : 0≤phi v := by
  unfold phi logTwo
  exact Real.rpow_nonneg (mul_nonneg (sq_nonneg _)
    (div_nonneg (Real.log_nonneg (by linarith)) (Real.log_nonneg (by norm_num)))) _

private theorem log_from_power (v q : ℕ) (h : 2^q≤(v+2)^64) :
    (q:ℝ) ≤ 64*logTwo ((v:ℝ)+2) := by
  have h' : (2:ℝ)^q≤((v:ℝ)+2)^64 := by exact_mod_cast h
  have hz := logTwo_mono (by positivity) h'
  have hl : logTwo ((2:ℝ)^q)=(q:ℝ) := by
    simpa only [Real.rpow_natCast] using logTwo_two_rpow (q:ℝ)
  have hr : logTwo (((v:ℝ)+2)^64)=64*logTwo ((v:ℝ)+2) := by
    unfold logTwo
    rw [Real.log_pow]
    push_cast
    ring
  rwa [hl,hr] at hz

theorem current_above_history {v : ℝ} (vlo : (Z:ℝ)+1≤v) (vhi : v≤(Z:ℝ)+2) :
    (historyCap:ℝ)<β+α*v-(159/4)*phi v := by
  have hv : 0≤v := by norm_num [Z] at vlo; linarith
  have hlog := (logTwo_mono (show 0<v+2 by linarith)
      (show v+2≤(Z:ℝ)+4 by linarith)).trans upper_4
  have hlog0 : 0≤logTwo (v+2) := by
    unfold logTwo
    exact div_nonneg (Real.log_nonneg (by linarith)) (Real.log_nonneg (by norm_num))
  have hsq := pow_le_pow_left₀ hv vhi 2
  have hprod := mul_le_mul hsq hlog hlog0 (sq_nonneg _)
  let r : ℝ := β+α*((Z:ℝ)+1)-historyCap
  have hr : 0≤r := by norm_num [r,Z,α,β,historyCap]
  have hc : ((159/4)*phi v)^3 < r^3 := by
    rw [mul_pow,phi_cube hv]
    calc
      (159/4:ℝ)^3 * (v^2*logTwo (v+2)) ≤ (159/4)^3 * (((Z:ℝ)+2)^2*u4) :=
        mul_le_mul_of_nonneg_left hprod (by norm_num)
      _ < _ := by norm_num [r,Z,α,β,historyCap,u4]
  have hl : (159/4)*phi v<r := by
    by_contra! hn
    exact (not_lt_of_ge (pow_le_pow_left₀ hr hn 3)) hc
  have hm := mul_le_mul_of_nonneg_left vlo (show 0≤α by norm_num [α])
  dsimp [r] at hl
  linarith only [hl,hm]

#print axioms passing
#print axioms preceding
#print axioms historical_cubics
#print axioms current_above_history
end S008.Recount.Refined
