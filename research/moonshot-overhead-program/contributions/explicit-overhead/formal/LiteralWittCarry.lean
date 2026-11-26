import Mathlib.Algebra.CharP.Two
import Mathlib.Algebra.BigOperators.Group.List.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/-! Length-two 2-typical Witt coordinate formulas in residue characteristic two.
The listed binary polynomial coefficients are in increasing degree order. -/
namespace Moonshot.LiteralWittCarry
variable {K : Type*} [Field K] [CharP K 2]

def bit (c : Bool) : K := if c then 1 else 0

def wadd (x y : K × K) : K × K := (x.1+y.1,x.2+y.2+x.1*y.1)
def wmul (x y : K × K) : K × K := (x.1*y.1,x.1^2*y.2+y.1^2*x.2)

theorem twice (x : K × K) : wadd x x=(0,x.1^2) := by
  simp [wadd, CharTwo.add_self_eq_zero, sq]

def eval (z : K) : List Bool → K
  | [] => 0
  | c :: f => bit c + z * eval z f

def deriv (z : K) : List Bool → K
  | [] => 0
  | _ :: f => eval z f + z * deriv z f

def half (z : K) : List Bool → K
  | [] => 0
  | c :: f => z^2 * half z f + bit c * z * eval z f

def weval (z : K × K) : List Bool → K × K
  | [] => (0,0)
  | c :: f => wadd (bit c, 0) (wmul z (weval z f))

def terms (z : K) : List Bool → List K
  | [] => []
  | c :: f => bit c :: (terms z f).map (z * ·)

def unordered : List K → K
  | [] => 0
  | a :: xs => a * xs.sum + unordered xs

omit [CharP K 2] in
private theorem scaled_sum (s : K) (xs : List K) :
    (xs.map (s * ·)).sum = s * xs.sum := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp [ih, mul_add]

omit [CharP K 2] in
private theorem scaled_pairs (s : K) (xs : List K) :
    unordered (xs.map (s * ·)) = s^2 * unordered xs := by
  induction xs with
  | nil => simp [unordered]
  | cons x xs ih => simp only [List.map_cons, unordered, scaled_sum, ih]; ring

omit [CharP K 2] in
theorem sum_terms (z : K) (f : List Bool) : (terms z f).sum=eval z f := by
  induction f with
  | nil => rfl
  | cons c f ih => simp [terms, eval, scaled_sum, ih]

omit [CharP K 2] in
theorem half_is_unordered (z : K) (f : List Bool) : half z f=unordered (terms z f) := by
  induction f with
  | nil => rfl
  | cons c f ih => simp only [half, terms, unordered, scaled_pairs, scaled_sum, sum_terms, ih]; ring

theorem shifted_components (z t : K) (f : List Bool) :
    weval (z,t^2) f = (eval z f,half z f+(t*deriv z f)^2) := by
  induction f with
  | nil => simp [weval, eval, half, deriv]
  | cons c f ih =>
    rw [weval, ih]
    apply Prod.ext
    · rfl
    · simp only [wadd, wmul, half, deriv, zero_add, mul_add, CharTwo.add_sq]
      ring

private theorem from_zero_sum (a b : K) (h : a+b=0) : a=b := by
  calc
    a = a+(b+b) := by simp [CharTwo.add_self_eq_zero]
    _ = b := by rw [← add_assoc, h, zero_add]

theorem literal_root (z t : K) (g : List Bool) (h : weval (z,t^2) g=(0,0)) :
    (t*deriv z g)^2=half z g := by
  rw [shifted_components] at h
  exact (from_zero_sum _ _ (congrArg Prod.snd h)).symm

theorem high_square (z t : K) (f r k : List Bool)
    (h : weval (z,t^2) f = wadd (weval (z,t^2) r)
        (wadd (weval (z,t^2) k) (weval (z,t^2) k))) :
    (eval z k)^2=half z f+half z r+(t*(deriv z f+deriv z r))^2 := by
  rw [twice] at h
  simp only [shifted_components, wadd, mul_zero, add_zero] at h
  have hh := congrArg Prod.snd h
  change half z f+(t*deriv z f)^2=half z r+(t*deriv z r)^2+(eval z k)^2 at hh
  let u := half z r+(t*deriv z r)^2
  calc
    _ = u+(u+(eval z k)^2) := by rw [← add_assoc, CharTwo.add_self_eq_zero, zero_add]
    _ = u+(half z f+(t*deriv z f)^2) := by rw [hh]
    _ = _ := by dsimp [u]; rw [mul_add, CharTwo.add_sq]; ac_rfl

theorem actual_factor_formula (z t : K) (g f r k : List Bool)
    (hg : weval (z,t^2) g=(0,0)) (hd : deriv z g ≠ 0)
    (hr : weval (z,t^2) f = wadd (weval (z,t^2) r)
        (wadd (weval (z,t^2) k) (weval (z,t^2) k))) :
    (eval z k)^2=half z f+half z r+
       (half z g/(deriv z g)^2)*(deriv z f+deriv z r)^2 := by
  rw [high_square z t f r k hr, ← literal_root z t g hg, mul_pow, mul_pow]
  field_simp

theorem sqrt_parity_columns (z ge go pe po : K) (hg : ge^2+z*go^2=0) (hu : go≠0) :
    (pe+(ge/go)*po)^2=pe^2+z*po^2 := by
  rw [CharTwo.add_sq, mul_pow, div_pow, from_zero_sum _ _ hg]
  field_simp

#print axioms half_is_unordered
#print axioms shifted_components
#print axioms literal_root
#print axioms actual_factor_formula
#print axioms sqrt_parity_columns
end Moonshot.LiteralWittCarry
