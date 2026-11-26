import S008.PiecewiseDensity

namespace S008.Piecewise.Refined
open S008.NumericalCutoff S008.Piecewise

abbrev D : ℝ := 1160000000000
abbrev a₀ : ℝ := 338099825541600
abbrev a₁ : ℝ := 725677674332640
abbrev a₂ : ℝ := 1451355348664800
abbrev a₃ : ℝ := 2902710697329120
abbrev a₄ : ℝ := 6201245580657120

private theorem lower_log (x p q : ℕ) (hq : 0 < q) (hn : 2^p ≤ (x+2)^q) :
    (p:ℝ)/(q:ℝ) ≤ logTwo ((x:ℝ)+2) := by
  have h : (2:ℝ)^p ≤ ((x:ℝ)+2)^q := by exact_mod_cast hn
  have hl := logTwo_mono (by positivity) h
  rw [← Real.rpow_natCast,logTwo_two_rpow] at hl
  have hr : logTwo (((x:ℝ)+2)^q) = (q:ℝ)*logTwo ((x:ℝ)+2) := by
    unfold logTwo
    rw [Real.log_pow]
    ring
  rw [hr] at hl
  rw [div_le_iff₀ (show (0:ℝ) < (q:ℝ) by exact_mod_cast hq)]
  linarith only [hl]

private theorem corner_arithmetic {a h l : ℝ} (ha : 0 ≤ a) (hlog : l ≤ logTwo (a+2))
    (hc : (4*(h-D))^3 ≤ 159^3*a^2*l) : h-(159/4:ℝ)*phi a ≤ D := by
  have hh : 4*(h-D) ≤ 159*phi a := by
    apply le_of_pow_le_pow_left₀ (by norm_num : (3:ℕ) ≠ 0) (mul_nonneg (by norm_num) (phi_nonneg ha))
    rw [show (159*phi a)^3=159^3*(phi a)^3 by ring,phi_cube ha]
    nlinarith only [hc,mul_nonneg (sq_nonneg a) (sub_nonneg.mpr hlog)]
  linarith only [hh]

private theorem corner₀ : 813844664560-(159/4:ℝ)*phi a₀ ≤ D := by
  have h := phi_nonneg (by norm_num [a₀] : 0 ≤ a₀)
  unfold D
  linarith only [h]

private theorem corner₁ : 1444667986160-(159/4:ℝ)*phi a₁ ≤ D :=
  corner_arithmetic (by norm_num [a₁]) (lower_log 725677674332640 49 1
    (by decide) (by decide +kernel)) (by norm_num [a₁,D])

private theorem corner₂ : 2197629440240-(159/4:ℝ)*phi a₂ ≤ D :=
  corner_arithmetic (by norm_num [a₂]) (lower_log 1451355348664800 50 1
    (by decide) (by decide +kernel)) (by norm_num [a₂,D])

private theorem corner₃ : 3496857047280-(159/4:ℝ)*phi a₃ ≤ D :=
  corner_arithmetic (by norm_num [a₃]) (lower_log 2902710697329120 51 1
    (by decide) (by decide +kernel)) (by norm_num [a₃,D])

private theorem corner₄ : 6181211607280-(159/4:ℝ)*phi a₄ ≤ D :=
  corner_arithmetic (by norm_num [a₄]) (lower_log 6201245580657120 839 16
    (by decide) (by decide +kernel)) (by norm_num [a₄,D])

/-- The five explicitly named rational affine supports, following the end of
    the j=11,a=4 knot. Every later bend may remain in the actual native shape. -/
def supports (H : ℝ → ℝ) : Prop :=
  Monotone H ∧ H a₀ ≤ 813844664560 ∧
  (∀ x, H x ≤ 8433663352295/32+(5/3072)*x) ∧
  (∀ x, H x ≤ 354153744424705/512+(17/16384)*x) ∧
  (∀ x, H x ≤ 114995434649545/128+(11/12288)*x) ∧
  (∀ x, H x ≤ 72616002206695/64+(5/6144)*x) ∧
  (∀ x, H x ≤ 3035148971130625/1024+(17/32768)*x)

private theorem bridge {a b x p q ha hb : ℝ} (h0 : 0<a) (hax : a ≤ x) (hxb : x ≤ b)
    (hl : ha-(159/4:ℝ)*phi a ≤ D) (hr : hb-(159/4:ℝ)*phi b ≤ D)
    (hca : p+q*a=ha) (hcb : p+q*b=hb) : p+q*x-(159/4:ℝ)*phi x ≤ D := by
  apply affine_surplus h0 hax hxb
  · rwa [hca]
  · rwa [hcb]

/-- A source-independent end frame: the old immutable vertices can be certified
    at once even if the native schedule keeps bending far beyond the endpoint. -/
theorem refined_frame (H : ℝ → ℝ) (hS : supports H) (t : ℝ) :
    prefixBound phi H t (max (D+48*phi t)
     (3035148971130625/1024+(17/32768)*t+(33/4)*phi t)) := by
  obtain ⟨hmono,h₀,h₁,h₂,h₃,h₄,h₅⟩ := hS
  have hd := (le_max_left (D+48*phi t) (3035148971130625/1024+(17/32768)*t+(33/4)*phi t))
  have hl := (le_max_right (D+48*phi t) (3035148971130625/1024+(17/32768)*t+(33/4)*phi t))
  constructor
  · have hDz : (0:ℝ) ≤ D := by norm_num [D]
    linarith only [hDz,hd]
  intro v hv hvt
  have finished : H v-(159/4:ℝ)*phi v ≤ D →
      48*phi t+H v-(159/4:ℝ)*phi v ≤ max (D+48*phi t)
       (3035148971130625/1024+(17/32768)*t+(33/4)*phi t) := by
    intro hh
    linarith only [hh,hd]
  by_cases ha : v ≤ a₀
  · apply finished
    linarith only [hmono ha,h₀,phi_nonneg hv,show (813844664560:ℝ) ≤ D by norm_num [D]]
  by_cases hb : v ≤ a₁
  · apply finished
    exact (sub_le_sub_right (h₁ v) _).trans (bridge (by norm_num [a₀]) (le_of_not_ge ha) hb
      corner₀ corner₁ (by norm_num [a₀]) (by norm_num [a₁]))
  by_cases hc : v ≤ a₂
  · apply finished
    exact (sub_le_sub_right (h₂ v) _).trans (bridge (by norm_num [a₁]) (le_of_not_ge hb) hc
      corner₁ corner₂ (by norm_num [a₁]) (by norm_num [a₂]))
  by_cases he : v ≤ a₃
  · apply finished
    exact (sub_le_sub_right (h₃ v) _).trans (bridge (by norm_num [a₂]) (le_of_not_ge hc) he
      corner₂ corner₃ (by norm_num [a₂]) (by norm_num [a₃]))
  by_cases hf : v ≤ a₄
  · apply finished
    exact (sub_le_sub_right (h₄ v) _).trans (bridge (by norm_num [a₃]) (le_of_not_ge he) hf
      corner₃ corner₄ (by norm_num [a₃]) (by norm_num [a₄]))
  set limit := max D (3035148971130625/1024+(17/32768)*t-(159/4)*phi t)
  have hleft : D ≤ limit := le_max_left _ _
  have hright : 3035148971130625/1024+(17/32768)*t-(159/4)*phi t ≤ limit := le_max_right _ _
  have hfirst : 3035148971130625/1024+17/32768*a₄-(159/4)*phi a₄ ≤ limit := by
    have eqn : (3035148971130625:ℝ)/1024+17/32768*a₄=6181211607280 := by norm_num [a₄]
    rw [eqn]
    exact corner₄.trans hleft
  have hh := (sub_le_sub_right (h₅ v) _).trans
    (affine_surplus (by norm_num [a₄]) (le_of_not_ge hf) hvt hfirst hright)
  rcases le_total D (3035148971130625/1024+(17/32768)*t-(159/4)*phi t) with h | h
  · rw [show limit = _ from max_eq_right h] at hh
    linarith only [hh,hl]
  · rw [show limit = _ from max_eq_left h] at hh
    exact finished hh

/-- A concrete function dominating the actual native shape. The five lines are
    its last five paid affine continuations through the tested endpoint. -/
noncomputable def upper (x : ℝ) : ℝ :=
  min (8433663352295/32+(5/3072)*x) <| min (354153744424705/512+(17/16384)*x) <|
  min (114995434649545/128+(11/12288)*x) <| min (72616002206695/64+(5/6144)*x)
    (3035148971130625/1024+(17/32768)*x)

theorem upper_supports : supports upper := by
  refine ⟨?_,?_,?_,?_,?_,?_,?_⟩
  · intro x y h
    unfold upper
    repeat' first | apply min_le_min | linarith only [h]
  · exact (min_le_left _ _).trans (by norm_num [a₀])
  · intro x; exact min_le_left _ _
  · intro x; exact (min_le_right _ _).trans (min_le_left _ _)
  · intro x; exact (min_le_right _ _).trans ((min_le_right _ _).trans (min_le_left _ _))
  · intro x
    exact (min_le_right _ _).trans ((min_le_right _ _).trans ((min_le_right _ _).trans (min_le_left _ _)))
  · intro x
    exact (min_le_right _ _).trans ((min_le_right _ _).trans ((min_le_right _ _).trans (min_le_right _ _)))

/-- The maximum over earlier discrete widths is bounded at any covering
    continuous width, retaining the exact native intercept and data coefficient. -/
theorem rounded_frame (H : ℝ → ℝ) (hS : supports H) (x : ℕ) (t : ℝ)
    (hx : (x:ℝ) ≤ t) : envelope (fun j => H (j:ℝ)) x ≤
    max (D+48*phi t) (3035148971130625/1024+(17/32768)*t+(33/4)*phi t) := by
  let B := max (D+48*phi t) (3035148971130625/1024+(17/32768)*t+(33/4)*phi t)
  have h := refined_frame H hS t
  have hh : history (fun j => H (j:ℝ)) x ≤ B-48*phi t := by
    apply history_upper _ (by linarith only [h.1])
    intro j hj
    have hjt : (j:ℝ) ≤ t := (show (j:ℝ) ≤ (x:ℝ) by exact_mod_cast hj).trans hx
    have hwin := h.2 (j:ℝ) (by positivity) hjt
    change 48*phi t+H (j:ℝ)-(159/4:ℝ)*phi (j:ℝ) ≤ B at hwin
    linarith only [hwin]
  have hp := phi_mono_nonneg (by positivity : (0:ℝ) ≤ (x:ℝ)) hx
  change 48*phi (x:ℝ)+history (fun j => H (j:ℝ)) x ≤ B
  linarith only [hh,hp]

end S008.Piecewise.Refined
