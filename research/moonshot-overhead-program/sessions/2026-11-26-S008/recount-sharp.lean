import S008.NumericalCutoff

namespace S008.Recount.Sharp
open S008.NumericalCutoff

set_option exponentiation.threshold 1000

def factor : Bool → ℕ
  | false => 1
  | true => 2

def digit : Bool → ℕ
  | false => 0
  | true => 1

abbrev Edge := Bool × ℕ

/-- Each rounded upper mantissa dominates its normalization after squaring. -/
def upperOK (q a : ℕ) : List Edge → Bool
  | [] => decide (0 < a ∧ a ≤ 2*q)
  | (b,c) :: es => decide (0 < a ∧ 0 < c ∧ a*a ≤ factor b*c*q) && upperOK q c es

def weight : List Edge → ℕ
  | [] => 0
  | (b,_)::es => digit b * 2^es.length + weight es

/-- Generate a checkable upper bracket from the supplied binary digit word. -/
def emit (q a bits : ℕ) : ℕ → List Edge
  | 0 => []
  | n+1 =>
    let b := bits.testBit n
    let den := factor b * q
    let c := (a*a+den-1)/den
    (b,c)::emit q c bits n

private theorem logTwo_two : logTwo 2 = 1 := by
  unfold logTwo
  exact div_self (ne_of_gt (Real.log_pos (by norm_num)))

private theorem digit_factor (b : Bool) : logTwo (factor b : ℝ) = (digit b : ℝ) := by
  cases b with
  | false => simp [factor,digit,logTwo]
  | true => simpa only [factor,digit,Nat.cast_ofNat,Nat.cast_one] using logTwo_two

private theorem log_squaring_step (v w : ℝ) {b : Bool} (hv : 0<v) (hw : 0<w)
    (h : v*v ≤ (factor b : ℝ)*w) :
    2*logTwo v ≤ (digit b : ℝ)+logTwo w := by
  have hb : 0 < (factor b : ℝ) := by cases b <;> norm_num [factor]
  have z := logTwo_mono (mul_pos hv hv) h
  have hadd (j l : ℝ) (hj : 0<j) (hl : 0<l) :
      logTwo (j*l) = logTwo j + logTwo l := by
    unfold logTwo
    rw [Real.log_mul hj.ne' hl.ne']
    ring
  rw [hadd _ _ hv hv, hadd _ _ hb hw, digit_factor] at z
  linarith

theorem upper_chain {q a : ℕ} (hq : 0<q) (es : List Edge) (h : upperOK q a es) :
    (2:ℝ)^es.length * logTwo ((a:ℝ)/q) ≤ (weight es : ℝ)+1 := by
  induction es generalizing a with
  | nil =>
    have hh : 0<a ∧ a ≤ 2*q := of_decide_eq_true h
    have hq' : (0:ℝ)<q := by exact_mod_cast hq
    have hv : (0:ℝ)<a := by exact_mod_cast hh.1
    have ha : (a:ℝ)/q ≤ 2 := by
      rw [div_le_iff₀ hq']
      exact_mod_cast hh.2
    have z := logTwo_mono (div_pos hv hq') ha
    simpa [weight, logTwo_two] using z
  | cons e es ih =>
    rcases e with ⟨b,c⟩
    simp only [upperOK, Bool.and_eq_true, decide_eq_true_eq] at h
    obtain ⟨⟨ha,hc,hh⟩, he⟩ := h
    have hq' : (0:ℝ)<q := by exact_mod_cast hq
    have ha' : (0:ℝ)<a := by exact_mod_cast ha
    have hc' : (0:ℝ)<c := by exact_mod_cast hc
    have hraw : (a:ℝ)*a ≤ (factor b:ℝ)*c*q := by exact_mod_cast hh
    have hv : ((a:ℝ)/q)*((a:ℝ)/q) ≤ (factor b:ℝ)*((c:ℝ)/q) := by
      field_simp [hq'.ne']
      nlinarith only [hraw]
    have hstep := log_squaring_step _ _ (div_pos ha' hq') (div_pos hc' hq') hv
    have hw := mul_le_mul_of_nonneg_left hstep (show 0≤(2:ℝ)^es.length by positivity)
    have hr := ih he
    simp only [List.length_cons, pow_succ, weight, Nat.cast_add, Nat.cast_mul,
      Nat.cast_pow, Nat.cast_ofNat]
    nlinarith only [hw,hr]


private theorem log_mul {v w : ℝ} (hv : 0<v) (hw : 0<w) :
    logTwo (v*w) = logTwo v + logTwo w := by
  unfold logTwo
  rw [Real.log_mul hv.ne' hw.ne']
  ring

/-- A closed integer certificate bounds the real binary logarithm. -/
theorem certify (q a n j bits : ℕ)
    (ha : 0<a) (hq : 0<q) (rep : n*q=2^j*a)
    (check : upperOK q a (emit q a bits 112))
    (len : (emit q a bits 112).length=112) (wgt : weight (emit q a bits 112)=bits) :
    logTwo (n:ℝ) ≤ (j:ℝ) + ((bits:ℝ)+1)/2^112 := by
  have hq' : (0:ℝ)<q := by exact_mod_cast hq
  have ha' : (0:ℝ)<a := by exact_mod_cast ha
  have rr : (n:ℝ)=(2:ℝ)^j*(a/q) := by
    field_simp [hq'.ne']
    exact_mod_cast rep
  have hz := upper_chain hq (emit q a bits 112) check
  rw [len,wgt] at hz
  have hz' : logTwo ((a:ℝ)/q) ≤ ((bits:ℝ)+1)/2^112 := by
    rw [le_div_iff₀ (by positivity)]
    linarith
  have hh : logTwo ((2:ℝ)^j) = (j:ℝ) := by
    simpa only [Real.rpow_natCast] using logTwo_two_rpow (j:ℝ)
  rw [rr,log_mul (by positivity) (div_pos ha' hq'),hh]
  linarith

def Q : ℕ := 2^448

def first (n j : ℕ) : ℕ := n*2^(448-j)

def Z : ℕ := 18536127975009233

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
theorem log_5121 :
    logTwo 5121 ≤ 12+(1673009159486381451201902226974135+1:ℝ)/2^112 := by
  apply certify Q (first 5121 12) 5121 12 1673009159486381451201902226974135
  all_goals decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
theorem log_two :
    logTwo (Z+2:ℝ) ≤ 54+(213867737802515390075695897754305+1:ℝ)/2^112 := by
  rw [show (Z:ℝ)+2=18536127975009235 by norm_num [Z]]
  apply certify Q (first 18536127975009235 54) 18536127975009235 54 213867737802515390075695897754305
  all_goals decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
theorem log_four :
    logTwo (Z+4:ℝ) ≤ 54+(213867737802516198324423866283223+1:ℝ)/2^112 := by
  rw [show (Z:ℝ)+4=18536127975009237 by norm_num [Z]]
  apply certify Q (first 18536127975009237 54) 18536127975009237 54 213867737802516198324423866283223
  all_goals decide


noncomputable def invoice (x : ℝ) : ℝ :=
  169 + logTwo 5121 + 4*logTwo (x+2) + 70*phi (x+2)

private noncomputable def p0 : ℝ := 12+(1673009159486381451201902226974135+1:ℝ)/2^112
private noncomputable def p2 : ℝ := 54+(213867737802515390075695897754305+1:ℝ)/2^112
private noncomputable def p4 : ℝ := 54+(213867737802516198324423866283223+1:ℝ)/2^112

theorem endpoint : invoice Z ≤ (Z:ℝ)/1000 := by
  have h0 : logTwo 5121 ≤ p0 := log_5121
  have h2 : logTwo (Z+2:ℝ) ≤ p2 := log_two
  have h4 : logTwo (((Z:ℝ)+2)+2) ≤ p4 := by
    rw [show (Z:ℝ)+2+2=(Z:ℝ)+4 by ring]
    exact log_four
  have hnon : 0 ≤ (Z:ℝ)/1000 -169-p0-4*p2 := by norm_num [Z,p0,p2]
  have hoff : 70*phi ((Z:ℝ)+2) ≤ (Z:ℝ)/1000 -169-p0-4*p2 := by
    apply le_of_pow_le_pow_left₀ (by norm_num : (3:ℕ) ≠ 0) hnon
    rw [mul_pow, phi_cube (by positivity)]
    calc
      (70:ℝ)^3 * (((Z:ℝ)+2)^2 * logTwo (((Z:ℝ)+2)+2)) ≤ 70^3 * (((Z:ℝ)+2)^2 * p4) :=
        mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left h4 (sq_nonneg _)) (by norm_num)
      _ ≤ _ := by norm_num [Z,p0,p2,p4]
  unfold invoice
  linarith

private theorem log_two_half : (1/2:ℝ) ≤ Real.log 2 := by
  have h := Real.log_le_sub_one_of_pos (show (0:ℝ)<1/2 by norm_num)
  rw [Real.log_div (by norm_num) (by norm_num), Real.log_one] at h
  linarith

private theorem real_nonneg {v : ℝ} (h : 1≤v) : 0≤logTwo v := by
  unfold logTwo
  exact div_nonneg (Real.log_nonneg h) (Real.log_nonneg (by norm_num))

private theorem phi_nonneg {v : ℝ} (hv : 0≤v) : 0≤phi v := by
  unfold phi
  exact Real.rpow_nonneg (mul_nonneg (sq_nonneg _) (real_nonneg (by linarith))) _

/-- All logarithms outside the cubic power have decreasing normalized ratios. -/
private theorem log_ratio {T x c : ℝ} (ht : 4≤T) (hx : T≤x) (hc : 0≤c) :
    T*logTwo (x+c) ≤ x*logTwo (T+c) := by
  have htc : 0<T+c := by linarith
  have hxc : 0<x+c := by linarith
  have hbase : 1≤Real.log (T+c) := by
    have hh := Real.log_le_log (show (0:ℝ)<2^2 by norm_num) (show (2:ℝ)^2≤T+c by nlinarith)
    rw [Real.log_pow] at hh
    push_cast at hh
    linarith [log_two_half]
  have hlog := Real.log_le_sub_one_of_pos (div_pos hxc htc)
  rw [Real.log_div hxc.ne' htc.ne'] at hlog
  have rr : (x+c)/(T+c)-1 = (x-T)/(T+c) := by
    field_simp
    ring
  rw [rr] at hlog
  have hm := (le_div_iff₀ htc).mp hlog
  have hd : 0 ≤ Real.log (x+c)-Real.log (T+c) :=
    sub_nonneg.mpr (Real.log_le_log htc (by linarith))
  have hscalar : T*Real.log (x+c) ≤ x*Real.log (T+c) := by
    nlinarith only [hm,mul_nonneg hc hd,mul_nonneg (sub_nonneg.mpr hx) (sub_nonneg.mpr hbase)]
  unfold logTwo
  rw [← mul_div_assoc, ← mul_div_assoc, div_le_div_iff_of_pos_right (Real.log_pos (by norm_num : (1:ℝ)<2))]
  exact hscalar

private theorem phi_ratio {T x : ℝ} (ht : 4≤T) (hx : T≤x) :
    T*phi (x+2) ≤ x*phi (T+2) := by
  have ht0 : 0≤T := by linarith
  have hx0 : 0≤x := by linarith
  have hlog := log_ratio (c:=4) ht hx (by norm_num)
  have hpos : T*(x+2) ≤ x*(T+2) := by nlinarith only [hx]
  have hsq : (T*(x+2))^2 ≤ (x*(T+2))^2 := by
    nlinarith only [mul_nonneg (sub_nonneg.mpr hpos) (show 0≤x*(T+2)+T*(x+2) by positivity)]
  have hmul := mul_le_mul hsq hlog
    (mul_nonneg ht0 (real_nonneg (show 1≤x+4 by linarith))) (sq_nonneg _)
  apply le_of_pow_le_pow_left₀ (by norm_num : (3:ℕ) ≠ 0)
    (mul_nonneg hx0 (phi_nonneg (by linarith)))
  rw [mul_pow,mul_pow, phi_cube (show 0 ≤ x+2 by linarith), phi_cube (show 0≤T+2 by linarith)]
  rw [show x+2+2=x+4 by ring,show T+2+2=T+4 by ring]
  nlinarith only [hmul]

theorem all_real_sizes {x : ℝ} (hx : (Z:ℝ)≤x) : invoice x ≤ x/1000 := by
  have ht : 4 ≤ (Z:ℝ) := by norm_num [Z]
  have hx0 : 0 ≤ x := by linarith
  have hlog := log_ratio (c:=2) ht hx (by norm_num)
  have hp := phi_ratio ht hx
  have hfixed : 0≤169+logTwo 5121 := by linarith [real_nonneg (show (1:ℝ)≤5121 by norm_num)]
  have hr : (Z:ℝ)*invoice x ≤ x*invoice Z := by
    unfold invoice
    nlinarith only [hlog,hp,mul_nonneg (sub_nonneg.mpr hx) hfixed]
  have hscaled := mul_le_mul_of_nonneg_left endpoint hx0
  apply le_of_mul_le_mul_left (a:=(Z:ℝ)) ?_ (by norm_num [Z])
  nlinarith only [hr,hscaled]

private theorem transfer (P : ℝ → ℝ) (T : ℝ) (hprofile : ∀ x, T≤x → P x ≤ x/1000) (n cost : ℝ)
    (hn : (2:ℝ)^((2:ℝ)^T) ≤ n)
    (hclock : cost ≤ n * Real.sqrt (logTwo n) * (2:ℝ)^(P (logTwo (logTwo n)))) :
    cost ≤ n * (logTwo n) ^ (501 / 1000 : ℝ) := by
  have hpos := lt_of_lt_of_le (Real.rpow_pos_of_pos (show (0:ℝ)<2 by norm_num) _) hn
  have hl := logTwo_mono (Real.rpow_pos_of_pos (show (0:ℝ)<2 by norm_num) _) hn
  rw [logTwo_two_rpow] at hl
  have hlpos : 0 < logTwo n := lt_of_lt_of_le (Real.rpow_pos_of_pos (by norm_num) _) hl
  have hs := hprofile _ (length_gate n _ hn)
  have hp := Real.rpow_le_rpow_of_exponent_le (show (1:ℝ) ≤ 2 by norm_num) hs
  have hpow : (2:ℝ)^(logTwo (logTwo n) / 1000) = (logTwo n)^(1/1000:ℝ) := by
    rw [div_eq_mul_one_div, Real.rpow_mul (by norm_num : (0:ℝ) ≤ 2), two_log_cancel hlpos]
  rw [hpow] at hp
  calc
    cost ≤ n * Real.sqrt (logTwo n) * (2:ℝ)^(P (logTwo (logTwo n))) := hclock
    _ ≤ n * Real.sqrt (logTwo n) * (logTwo n)^(1/1000:ℝ) :=
      mul_le_mul_of_nonneg_left hp (mul_nonneg hpos.le (Real.sqrt_nonneg _))
    _ = n * (logTwo n) ^ (501 / 1000 : ℝ) := by
      rw [show (501/1000:ℝ) = 1/2+1/1000 by norm_num,
        Real.sqrt_eq_rpow, Real.rpow_add hlpos, mul_assoc]

/-- A leading-one inequality under the full prefactor, in original input length. -/
theorem sharp_multiplication (n cost : ℝ)
    (hn : (2:ℝ)^((2:ℝ)^(Z:ℝ)) ≤ n)
    (hclock : cost ≤ n * Real.sqrt (logTwo n) * (2:ℝ)^(invoice (logTwo (logTwo n)))) :
    cost ≤ n * (logTwo n) ^ (501 / 1000 : ℝ) :=
  transfer invoice Z (fun _ h => all_real_sizes h) n cost hn hclock

/-- The lower mantissa certificates are used only for the adjacent failed invoice. -/
def lowerOK (q a : ℕ) : List Edge → Bool
  | [] => decide (q ≤ a)
  | (b,c) :: es => decide (0 < a ∧ 0 < c ∧ factor b*c*q ≤ a*a) && lowerOK q c es

def lowerEmit (q a bits : ℕ) : ℕ → List Edge
  | 0 => []
  | n+1 =>
    let b := bits.testBit n
    let c := a*a/(factor b*q)
    (b,c)::lowerEmit q c bits n

theorem lower_chain {q a : ℕ} (hq : 0<q) (es : List Edge) (h : lowerOK q a es) :
    (weight es : ℝ) ≤ (2:ℝ)^es.length * logTwo ((a:ℝ)/q) := by
  induction es generalizing a with
  | nil =>
    have hh : q ≤ a := of_decide_eq_true h
    have hq' : (0:ℝ)<q := by exact_mod_cast hq
    have ha : 1≤(a:ℝ)/q := by
      rw [le_div_iff₀ hq',one_mul]
      exact_mod_cast hh
    simpa [weight] using real_nonneg ha
  | cons e es ih =>
    rcases e with ⟨b,c⟩
    simp only [lowerOK, Bool.and_eq_true, decide_eq_true_eq] at h
    obtain ⟨⟨ha,hc,hh⟩, he⟩ := h
    have hq' : (0:ℝ)<q := by exact_mod_cast hq
    have ha' : (0:ℝ)<a := by exact_mod_cast ha
    have hc' : (0:ℝ)<c := by exact_mod_cast hc
    have hraw : (factor b:ℝ)*c*q ≤ (a:ℝ)*a := by exact_mod_cast hh
    have hv : (factor b:ℝ)*((c:ℝ)/q) ≤ ((a:ℝ)/q)*((a:ℝ)/q) := by
      field_simp [hq'.ne']
      nlinarith only [hraw]
    have hb : (0:ℝ) < factor b := by cases b <;> norm_num [factor]
    have rz := logTwo_mono (mul_pos hb (div_pos hc' hq')) hv
    rw [log_mul hb (div_pos hc' hq'),log_mul (div_pos ha' hq') (div_pos ha' hq'),digit_factor] at rz
    have hw := mul_le_mul_of_nonneg_left rz (show 0≤(2:ℝ)^es.length by positivity)
    have hr := ih he
    simp only [List.length_cons, pow_succ, weight, Nat.cast_add, Nat.cast_mul,
      Nat.cast_pow, Nat.cast_ofNat]
    nlinarith only [hw,hr]

theorem certify_lower (q a n j bits : ℕ)
    (ha : 0<a) (hq : 0<q) (rep : n*q=2^j*a)
    (check : lowerOK q a (lowerEmit q a bits 112))
    (len : (lowerEmit q a bits 112).length=112) (wgt : weight (lowerEmit q a bits 112)=bits) :
    (j:ℝ) + (bits:ℝ)/2^112 ≤ logTwo (n:ℝ) := by
  have hq' : (0:ℝ)<q := by exact_mod_cast hq
  have ha' : (0:ℝ)<a := by exact_mod_cast ha
  have rr : (n:ℝ)=(2:ℝ)^j*(a/q) := by
    field_simp [hq'.ne']
    exact_mod_cast rep
  have hz := lower_chain hq (lowerEmit q a bits 112) check
  rw [len,wgt] at hz
  have hz' : (bits:ℝ)/2^112 ≤ logTwo ((a:ℝ)/q) := by
    rw [div_le_iff₀ (by positivity)]
    nlinarith only [hz]
  have hh : logTwo ((2:ℝ)^j) = (j:ℝ) := by
    simpa only [Real.rpow_natCast] using logTwo_two_rpow (j:ℝ)
  rw [rr,log_mul (by positivity) (div_pos ha' hq'),hh]
  linarith

def ZP : ℕ := 11665715140844862

private noncomputable def upperP : ℝ := 53+(1937371972144530065443799258072521+1:ℝ)/2^112
private noncomputable def lowerP : ℝ := 53+(1937371972144529423314205127675621:ℝ)/2^112
private noncomputable def caller : ℝ := 2^25+220
private noncomputable def D : ℝ := 2220000000000
private noncomputable def α : ℝ := 17/32768
private noncomputable def β : ℝ := 4112174977105665/1024

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
theorem piecewise_log_upper : logTwo (ZP+4:ℝ) ≤ upperP := by
  rw [show (ZP:ℝ)+4=11665715140844866 by norm_num [ZP]]
  apply certify Q (first 11665715140844866 53) 11665715140844866 53 1937371972144530065443799258072521
  all_goals decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
theorem piecewise_log_lower : lowerP ≤ logTwo (ZP+3:ℝ) := by
  rw [show (ZP:ℝ)+3=11665715140844865 by norm_num [ZP]]
  apply certify_lower Q (first 11665715140844865 53) 11665715140844865 53 1937371972144529423314205127675621
  all_goals decide

/-- Two explicit cubings at the sharp upper endpoint of the historical and movement invoice. -/
theorem piecewise_endpoint :
    caller + D + 48*phi (ZP+2:ℝ) ≤ (ZP:ℝ)/1000 ∧
    caller + β + α*((ZP:ℝ)+2) + (33/4)*phi (ZP+2:ℝ) ≤ (ZP:ℝ)/1000 := by
  have hh : logTwo (((ZP:ℝ)+2)+2) ≤ upperP := by
    rw [show (ZP:ℝ)+2+2=(ZP:ℝ)+4 by ring]
    exact piecewise_log_upper
  have h (c b : ℝ) (hc : 0≤c) (hr : 0 ≤ (ZP:ℝ)/1000-b)
      (hs : c^3 * (((ZP:ℝ)+2)^2 * upperP) ≤ ((ZP:ℝ)/1000-b)^3) :
      b+c*phi ((ZP:ℝ)+2) ≤ (ZP:ℝ)/1000 := by
    have hl : c*phi ((ZP:ℝ)+2) ≤ (ZP:ℝ)/1000-b := by
      apply le_of_pow_le_pow_left₀ (by norm_num : (3:ℕ) ≠ 0) hr
      rw [mul_pow,phi_cube (by positivity)]
      exact (mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left hh (sq_nonneg _))
        (pow_nonneg hc 3)).trans hs
    linarith
  constructor
  · apply h <;> norm_num [ZP,caller,D,upperP]
  · apply h <;> norm_num [ZP,caller,β,α,upperP]

/-- At the preceding integer the sharp movement inequality strictly fails. -/
theorem piecewise_predecessor :
    ((ZP:ℝ)-1)/1000 < caller+β+α*(((ZP:ℝ)-1)+2)+(33/4)*phi (((ZP:ℝ)-1)+2) := by
  have hh : lowerP ≤ logTwo ((((ZP:ℝ)-1)+2)+2) := by
    rw [show (ZP:ℝ)-1+2+2=(ZP:ℝ)+3 by ring]
    exact piecewise_log_lower
  let x : ℝ := (ZP:ℝ)-1
  let w : ℝ := x/1000-caller-β-α*(x+2)
  have hcube : w^3 < ((33/4)*phi (x+2))^3 := by
    rw [mul_pow,phi_cube (by dsimp [x]; norm_num [ZP])]
    calc
      w^3 < (33/4)^3 * ((x+2)^2 * lowerP) := by norm_num [w,x,ZP,caller,β,α,lowerP]
      _ ≤ _ := mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left hh (sq_nonneg _)) (by norm_num)
  have h : w < (33/4)*phi (x+2) := by
    by_contra! hc
    have hnon : 0 ≤ (33/4)*phi (x+2) :=
      mul_nonneg (by norm_num) (phi_nonneg (by dsimp [x]; norm_num [ZP]))
    have hu := pow_le_pow_left₀ hnon hc 3
    linarith only [hcube,hu]
  dsimp [w,x] at h
  linarith

/-- The two-branch majorant including the unfrozen logarithmic caller overhead. -/
noncomputable def piecewiseInvoice (x : ℝ) : ℝ :=
  2^25 + 4*logTwo (x+2) + max (D+48*phi (x+2)) (β+α*(x+2)+(33/4)*phi (x+2))

private theorem profile_global {T x : ℝ} (ht : 4≤T) (hx : T≤x) (c a k r : ℝ)
    (hc : 0≤c) (hk : 0≤k) (hr : 0≤r)
    (bound : c+a*T+k*logTwo (T+2)+r*phi (T+2) ≤ T/1000) :
    c+a*x+k*logTwo (x+2)+r*phi (x+2) ≤ x/1000 := by
  have hlog := mul_le_mul_of_nonneg_left (log_ratio (c:=2) ht hx (by norm_num)) hk
  have hp := mul_le_mul_of_nonneg_left (phi_ratio ht hx) hr
  have hfixed := mul_nonneg (sub_nonneg.mpr hx) hc
  have hx0 : 0≤x := by linarith
  have hscaled := mul_le_mul_of_nonneg_left bound hx0
  apply le_of_mul_le_mul_left (a:=T) ?_ (by linarith only [ht])
  nlinarith only [hlog,hp,hfixed,hscaled]

theorem piecewise_all_real {x : ℝ} (hx : (ZP:ℝ)≤x) : piecewiseInvoice x ≤ x/1000 := by
  have ht : 4≤(ZP:ℝ) := by norm_num [ZP]
  have hlog := logTwo_mono (show (0:ℝ)<ZP+2 by positivity)
    (show (ZP:ℝ)+2≤(2:ℝ)^55 by norm_num [ZP])
  have h55 : logTwo ((2:ℝ)^55) = 55 := by
    rw [← Real.rpow_natCast,logTwo_two_rpow]
    norm_num
  rw [h55] at hlog
  have hc : (2:ℝ)^25+4*logTwo (ZP+2:ℝ) ≤ caller := by
    unfold caller
    linarith only [hlog]
  have hHist := piecewise_endpoint.1
  have hMove := piecewise_endpoint.2
  have l1 : (2:ℝ)^25 + D + 0*(ZP:ℝ) + 4*logTwo (ZP+2:ℝ) + 48*phi (ZP+2:ℝ) ≤ (ZP:ℝ)/1000 := by
    linarith only [hc,hHist]
  have l2 : (2:ℝ)^25 + β+2*α + α*(ZP:ℝ) + 4*logTwo (ZP+2:ℝ) + (33/4)*phi (ZP+2:ℝ) ≤ (ZP:ℝ)/1000 := by
    linarith only [hc,hMove]
  have t1 := profile_global ht hx (2^25+D) 0 4 48 (by norm_num [D]) (by norm_num) (by norm_num) l1
  have t2 := profile_global ht hx (2^25+β+2*α) α 4 (33/4) (by norm_num [β,α]) (by norm_num) (by norm_num) l2
  unfold piecewiseInvoice
  rcases le_total (D+48*phi (x+2)) (β+α*(x+2)+(33/4)*phi (x+2)) with hh|hh
  · rw [max_eq_right hh]
    linarith only [t2]
  · rw [max_eq_left hh]
    linarith only [t1]

/-- The sharp piecewise caller sufficient bound in original input length. -/
theorem piecewise_multiplication (n cost : ℝ)
    (hn : (2:ℝ)^((2:ℝ)^(ZP:ℝ)) ≤ n)
    (hclock : cost ≤ n * Real.sqrt (logTwo n) * (2:ℝ)^(piecewiseInvoice (logTwo (logTwo n)))) :
    cost ≤ n * (logTwo n) ^ (501 / 1000 : ℝ) :=
  transfer piecewiseInvoice ZP (fun _ h => piecewise_all_real h) n cost hn hclock

#print axioms sharp_multiplication
#print axioms piecewise_multiplication
#print axioms piecewise_predecessor
end S008.Recount.Sharp
