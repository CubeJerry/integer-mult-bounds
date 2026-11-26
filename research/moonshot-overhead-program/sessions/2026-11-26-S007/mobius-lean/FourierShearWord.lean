import MobiusLean.Word

/-!
Check the ternary Fourier letters in the two-bit Pascal word over F₁₆.
This wrapper uses the finite matrices and twelve-slot word in
Swapnil-jain/mobius-x1, 00ffede3d650d434ebba869cafab4d334edc6d4d,
lean/MobiusLean/Word.lean. The matrices multiply on the left.
-/

namespace Moonshot.FourierShearWord
open Mob.W

/-- Entries ω^(i*j) in the source polynomial representation of F₁₆. -/
def dft3 : Mat := [[1,1,1], [1,6,7], [1,7,6]]

/-- Project a C′ letter to tagged Fourier and monomial letters. -/
def expand (A : Mat) : List (Bool × Mat) :=
  if A == Cp then [(true,dft3), (false,diag [1,6,6]), (true,dft3), (false,P23)]
  else [(false,A)]

def forwardSlots : List (Bool × Mat) := factors.flatMap fun f =>
  ((slots3 f).flatMap expand).map fun s => (s.1,embed s.2 f.coords)

/-- Reverse coordinates to conjugate S⊗S into its transpose U⊗U. -/
def reverse4 : Mat := perm [3,2,1,0]

def shearSlots : List (Bool × Mat) := [(false,reverse4)] ++ forwardSlots ++ [(false,reverse4)]

def pascalUpper : Mat := (List.range 4).map fun i => (List.range 4).map fun j =>
  if i / 2 ≤ j / 2 && i % 2 ≤ j % 2 then 1 else 0

def supportedFourier (A : Mat) : Bool :=
  factors.any fun f => A == embed dft3 f.coords

theorem dft_positive : mmul dft3 dft3 = P23 ∧
    prod [dft3, diag [1,6,6], dft3, P23] 3 = Cp := by decide +kernel

/-- Every tag denotes its stated type, and the actual product is U⊗U. -/
theorem four_coordinate_word :
    (shearSlots.filter Prod.fst).length = 24 ∧
    (shearSlots.all fun a => if a.1 then supportedFourier a.2 else isMono a.2) = true ∧
    prod (shearSlots.map Prod.snd) 4 = pascalUpper := by decide +kernel

#print axioms dft_positive
#print axioms four_coordinate_word
end Moonshot.FourierShearWord
