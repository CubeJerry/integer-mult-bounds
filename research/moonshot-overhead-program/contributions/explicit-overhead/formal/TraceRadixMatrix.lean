import TraceRadixRank
import Mathlib.LinearAlgebra.Matrix.Rank

/-!
# Ordered trace digits and their inverse matrix

Rows and columns are ordinary increasing addresses. Column `j` is the
coefficient vector of `X^(j % v) * D^(j / v)`.
-/
namespace Moonshot.TraceRadixMatrix
open Polynomial Matrix
open scoped Polynomial BigOperators

variable {F : Type*} [Field F]

/-- Literal radix synthesis of the column with flattened address `j`. -/
noncomputable def digitColumn (D : F[X]) (v j : ℕ) := X^(j%v)*D^(j/v)

/-- The square portion with rows starting at `s`, columns at `t`, width `h`. -/
noncomputable def digitBlock (D : F[X]) (v h s t : ℕ) : Matrix (Fin h) (Fin h) F :=
  fun i j => (digitColumn D v (t+j.val)).coeff (s+i.val)

private theorem column_monic (D : F[X]) (v j : ℕ) (hD : D.Monic) :
    (digitColumn D v j).Monic := (monic_X_pow _).mul (hD.pow _)

private theorem column_degree (D : F[X]) (v j : ℕ) (hD : D.Monic) (hd : D.natDegree = v) :
    (digitColumn D v j).natDegree = j := by
  rw [digitColumn, natDegree_mul (pow_ne_zero _ X_ne_zero) (pow_ne_zero _ hD.ne_zero),
    natDegree_X_pow, natDegree_pow, hd, Nat.mul_comm (j/v) v, Nat.mod_add_div]

private theorem digit_triangular (D : F[X]) (v h : ℕ) (hD : D.Monic) (hd : D.natDegree=v) :
    (digitBlock D v h 0 0).IsUpperTriangular := by
  intro i j hij
  apply coeff_eq_zero_of_natDegree_lt
  simpa [column_degree D v _ hD hd] using hij

private theorem digit_det (D : F[X]) (v h : ℕ) (hD : D.Monic) (hd : D.natDegree=v) :
    (digitBlock D v h 0 0).det = 1 := by
  rw [Matrix.det_of_isUpperTriangular (digit_triangular D v h hD hd)]
  have diag (i : Fin h) : digitBlock D v h 0 0 i i = 1 := by
    simpa [digitBlock, column_degree D v _ hD hd] using (column_monic D v i hD).coeff_natDegree
  simp [diag]

private theorem shifted_column (D : F[X]) (v j u : ℕ) (hv : 0 < v) :
    digitColumn D v (v*u+j) = D^u * digitColumn D v j := by
  unfold digitColumn
  rw [Nat.add_comm (v*u) j, Nat.add_mul_mod_self_left, Nat.add_mul_div_left _ _ hv, pow_add]
  ring

/-- Actual lower-digit coefficient columns are a full-rank change of coordinates
for the ordinary middle product. -/
theorem ordered_rank (D : F[X]) (v h s u : ℕ) (hv : 0 < v) (hD : D.Monic)
    (hd : D.natDegree=v) :
    (digitBlock D v h s (v*u)).rank = Module.finrank F (TraceRadixRank.bandMap h s (D^u)).range := by
  let b := Polynomial.degreeLT.basis F h
  let b' := Pi.basisFun F (Fin h)
  let f := TraceRadixRank.bandMap h s (D^u)
  let A := LinearMap.toMatrix b b' f
  let K := digitBlock D v h 0 0
  have factor : digitBlock D v h s (v*u) = A * K := by
    ext i j
    let B := digitColumn D v j.val
    have hB : B ∈ Polynomial.degreeLT F h := by
      apply mem_degreeLT.mpr
      exact degree_le_natDegree.trans_lt (by exact_mod_cast (column_degree D v j hD hd).trans_lt j.isLt)
    let W : Polynomial.degreeLT F h := ⟨B,hB⟩
    have coordinates : (b.repr W : Fin h → F) = K.col j := by
      funext k
      simp [b, W, B, K, digitBlock, Matrix.col_apply]
    have mul := congrFun (LinearMap.toMatrix_mulVec_repr b b' f W) i
    rw [coordinates, Pi.basisFun_repr] at mul
    change (digitColumn D v (v*u+j.val)).coeff (s+i.val) = (A *ᵥ K.col j) i
    rw [shifted_column D v j u hv]
    exact mul.symm
  rw [factor, Matrix.rank_mul_eq_left_of_det_ne_zero K A (by simp [K,digit_det D v h hD hd]),
    Matrix.rank_eq_finrank_range_toLin A b' b, Matrix.toLin_toMatrix]

variable [CharP F 2]

/-- Exact rank with the actual mixed-radix columns, including their ordering. -/
theorem trace_ordered_rank (a i p : ℕ) (ha : 2 ≤ a) :
    let v := a*a*2
    let z := 2^i
    let h := v*z
    (digitBlock (CoefficientPrefix.traceBase (F:=F) a) v h (h*(2*p)) (h*(2*p+1))).rank = h-z := by
  dsimp only
  obtain ⟨hD,hd⟩ := TraceRadixRank.trace_monic_degree (F:=F) a ha
  have hv : 0<a*a*2 := by positivity
  rw [show a*a*2*2^i*(2*p+1) = a*a*2*((2*p+1)*2^i) by ring, ordered_rank _ _ _ _ _ hv hD hd]
  exact TraceRadixRank.trace_power_band_rank a i p ha


/-- The increasing map from an h-wide consecutive block to the full stream. -/
def atOffset {n h : ℕ} (start : ℕ) (bound : start+h ≤ n) : Fin h ↪ Fin n where
  toFun x := ⟨start+x.val, by have := x.isLt; omega⟩
  inj' := by intro x y eq; apply Fin.ext; simpa using congrArg Fin.val eq

private theorem offset_val {n h : ℕ} {s : ℕ} (hs : s+h≤n) (i : Fin h) :
    (atOffset s hs i).val = s+i.val := rfl

private theorem sum_adjacent {R : Type*} [AddCommMonoid R] {n h s : ℕ}
    (hs : s+2*h ≤ n) (f : Fin n → R)
    (outside : ∀ k, k.val<s ∨ s+2*h≤k.val → f k=0) :
    let l := atOffset (h:=h) s (n:=n) (by omega)
    let r := atOffset (h:=h) (s+h) (n:=n) (by omega)
    ∑ k, f k = ∑ j, f (l j) + ∑ j, f (r j) := by
  classical
  dsimp only
  let l := atOffset (h:=h) s (n:=n) (by omega)
  let r := atOffset (h:=h) (s+h) (n:=n) (by omega)
  let L := Finset.univ.map l
  let R := Finset.univ.map r
  have disj : Disjoint L R := by
    apply Finset.disjoint_left.mpr
    intro k hL hR
    obtain ⟨i,_,hi⟩ := Finset.mem_map.mp hL
    obtain ⟨j,_,hj⟩ := Finset.mem_map.mp hR
    have e := congrArg Fin.val (hi.trans hj.symm)
    change s+i.val=s+h+j.val at e
    have := i.isLt
    omega
  have outside' : ∀ k ∈ (Finset.univ : Finset (Fin n)), k ∉ L∪R → f k=0 := by
    intro k _ hk
    apply outside
    by_contra! inside
    apply hk
    by_cases hleft : k.val<s+h
    · apply Finset.mem_union_left R
      refine Finset.mem_map.mpr ⟨⟨k.val-s,by omega⟩, Finset.mem_univ _, Fin.ext ?_⟩
      change s+(k.val-s)=k.val
      omega
    · apply Finset.mem_union_right L
      refine Finset.mem_map.mpr ⟨⟨k.val-(s+h),by omega⟩, Finset.mem_univ _, Fin.ext ?_⟩
      change s+h+(k.val-(s+h))=k.val
      omega
  rw [← Finset.sum_subset (Finset.subset_univ _) outside', Finset.sum_union disj]
  simp [L,R,l,r,Finset.sum_map]

omit [CharP F 2] in
private theorem product_window {n h s : ℕ} (hs : s+2*h≤n)
    (A B : Matrix (Fin n) (Fin n) F) (hA : A.IsUpperTriangular) (hB : B.IsUpperTriangular) :
    let l := atOffset (h:=h) s (n:=n) (by omega)
    let r := atOffset (h:=h) (s+h) (n:=n) (by omega)
    (A*B).submatrix l r = A.submatrix l l * B.submatrix l r + A.submatrix l r * B.submatrix r r := by
  dsimp only
  ext i j
  rw [Matrix.submatrix_apply, Matrix.mul_apply, Matrix.add_apply, Matrix.mul_apply, Matrix.mul_apply]
  apply sum_adjacent hs
  intro k outside
  cases outside with
  | inl hlt =>
    rw [hA (by change k.val < s+i.val; omega), zero_mul]
  | inr hge =>
    rw [hB (by change (s+h+j.val)<k.val; have := j.isLt; omega), mul_zero]

omit [CharP F 2] in
private theorem det_window {n h s : ℕ} (hs : s+h≤n) (A : Matrix (Fin n) (Fin n) F)
    (hA : A.IsUpperTriangular) (hdet : A.det ≠ 0) :
    (A.submatrix (atOffset s hs) (atOffset s hs)).det ≠ 0 := by
  have hd (i : Fin n) : A i i ≠ 0 := by
    rw [Matrix.det_of_isUpperTriangular hA, Finset.prod_ne_zero_iff] at hdet
    exact hdet i (Finset.mem_univ _)
  have hu : (A.submatrix (atOffset s hs) (atOffset s hs)).IsUpperTriangular := by
    intro i j hij
    apply hA
    change s+j.val<s+i.val
    exact Nat.add_lt_add_left hij _
  rw [Matrix.det_of_isUpperTriangular hu, Finset.prod_ne_zero_iff]
  exact fun i _ => hd _

/-- Reversing any invertible upper triangular binary transform preserves the
rank of every off-diagonal block formed by adjacent equal-width intervals. -/
theorem inverse_window_rank {n h s : ℕ} (hs : s+2*h≤n) (A : Matrix (Fin n) (Fin n) F)
    (hA : A.IsUpperTriangular) (hdet : A.det ≠ 0) :
    let l := atOffset (h:=h) s (n:=n) (by omega)
    let r := atOffset (h:=h) (s+h) (n:=n) (by omega)
    (A⁻¹.submatrix l r).rank = (A.submatrix l r).rank := by
  dsimp only
  let l := atOffset (h:=h) s (n:=n) (by omega)
  let r := atOffset (h:=h) (s+h) (n:=n) (by omega)
  have hu : IsUnit A.det := isUnit_iff_ne_zero.mpr hdet
  let _ : Invertible A := Matrix.invertibleOfIsUnitDet A hu
  have hi : A⁻¹.IsUpperTriangular := Matrix.blockTriangular_inv_of_blockTriangular (b:=id) hA
  have hdi : A⁻¹.det ≠ 0 := by rw [Matrix.det_nonsing_inv, Ring.inverse_eq_inv]; exact inv_ne_zero hdet
  have disjoint : (1 : Matrix (Fin n) (Fin n) F).submatrix l r = 0 := by
    ext i j
    have ne : l i ≠ r j := by
      intro eq
      have e := congrArg Fin.val eq
      change s+i.val=s+h+j.val at e
      have := i.isLt
      omega
    simp [ne]
  have top := product_window hs A A⁻¹ hA hi
  change (A*A⁻¹).submatrix l r = A.submatrix l l * A⁻¹.submatrix l r + A.submatrix l r * A⁻¹.submatrix r r at top
  rw [Matrix.mul_nonsing_inv A hu, disjoint] at top
  have cross := eq_neg_of_add_eq_zero_left top.symm
  have neg_matrix (X : Matrix (Fin h) (Fin h) F) : -X = X := by ext i j; exact CharTwo.neg_eq (X i j)
  rw [neg_matrix] at cross
  have ranks := congrArg Matrix.rank cross
  rw [Matrix.rank_mul_eq_right_of_det_ne_zero _ _ (det_window _ A hA hdet),
    Matrix.rank_mul_eq_left_of_det_ne_zero _ _ (det_window _ A⁻¹ hi hdi)] at ranks
  exact ranks


/-- The rank in each direction, on one full coefficient record of length `n`.
The inputs and outputs use the external ordering on both sides. In the S006
prefix, take `n=v*2^(c-1-r)`, and repeat the same matrix for every prefix. -/
theorem trace_both_directions (a i p n : ℕ) (ha : 2 ≤ a)
    (bound : (a*a*2*(2^i))*(2*p) + 2*(a*a*2*(2^i)) ≤ n) :
    let v := a*a*2
    let z := 2^i
    let h := v*z
    let s := h*(2*p)
    let M := digitBlock (CoefficientPrefix.traceBase (F:=F) a) v n 0 0
    let l := atOffset (h:=h) s (n:=n) (by dsimp [s,h,v,z]; omega)
    let r := atOffset (h:=h) (s+h) (n:=n) (by dsimp [s,h,v,z]; omega)
    (M.submatrix l r).rank = h-z ∧ (M⁻¹.submatrix l r).rank = h-z := by
  let v := a*a*2
  let z := 2^i
  let h := v*z
  let s := h*(2*p)
  let D := CoefficientPrefix.traceBase (F:=F) a
  let M := digitBlock D v n 0 0
  have hs : s+2*h≤n := bound
  let l := atOffset (h:=h) s (n:=n) (by omega)
  let r := atOffset (h:=h) (s+h) (n:=n) (by omega)
  change (M.submatrix l r).rank = h-z ∧ (M⁻¹.submatrix l r).rank = h-z
  have submat : M.submatrix l r = digitBlock D v h s (h*(2*p+1)) := by
    ext j k
    simp [M, digitBlock, l, r, atOffset, s, Nat.mul_add]
    rfl
  have forward : (M.submatrix l r).rank = h-z := submat ▸ trace_ordered_rank (F:=F) a i p ha
  obtain ⟨hD,hd⟩ := TraceRadixRank.trace_monic_degree (F:=F) a ha
  have htri := digit_triangular D v n hD hd
  have hdet : M.det ≠ 0 := by simp [M,digit_det D v n hD hd]
  exact ⟨forward, (inverse_window_rank hs M htri hdet).trans forward⟩


/-- Both directions are upper triangular with nonzero diagonal at every input
width. This is the output-order hypothesis in the circuit rank charge. -/
theorem trace_order (a n : ℕ) (ha : 2 ≤ a) (inverse : Bool) :
    let M := digitBlock (CoefficientPrefix.traceBase (F:=F) a) (a*a*2) n 0 0
    let A := if inverse then M⁻¹ else M
    A.IsUpperTriangular ∧ ∀i, A i i≠0 := by
  let M := digitBlock (CoefficientPrefix.traceBase (F:=F) a) (a*a*2) n 0 0
  obtain ⟨hD,hd⟩ := TraceRadixRank.trace_monic_degree (F:=F) a ha
  have htri : M.IsUpperTriangular := digit_triangular _ _ _ hD hd
  have hdet : M.det=1 := digit_det _ _ _ hD hd
  have diag {A : Matrix (Fin n) (Fin n) F} (upper : A.IsUpperTriangular) (det : A.det≠0) (i : Fin n) : A i i ≠ 0 := by
    rw [Matrix.det_of_isUpperTriangular upper, Finset.prod_ne_zero_iff] at det
    exact det i (Finset.mem_univ _)
  have nonzero : M.det ≠ 0 := hdet.trans_ne one_ne_zero
  cases inverse with
  | false => exact ⟨htri,diag htri nonzero⟩
  | true =>
    let _ : Invertible M := Matrix.invertibleOfIsUnitDet M (by simp [hdet])
    have up : M⁻¹.IsUpperTriangular := Matrix.blockTriangular_inv_of_blockTriangular (b:=id) htri
    have inv_nonzero : M⁻¹.det ≠ 0 := by rw [Matrix.det_nonsing_inv, Ring.inverse_eq_inv]; exact inv_ne_zero nonzero
    exact ⟨up,diag up inv_nonzero⟩

#print axioms trace_order
#print axioms inverse_window_rank
#print axioms trace_both_directions
#print axioms trace_ordered_rank
end Moonshot.TraceRadixMatrix
