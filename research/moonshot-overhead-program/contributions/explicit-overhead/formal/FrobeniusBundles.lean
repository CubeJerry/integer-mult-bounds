import Mathlib.Algebra.Group.Equiv.Basic
import Mathlib.Algebra.Group.Subgroup.Basic

/-! # Frobenius-compatible bundles of complete cosets
The finest partition that contains each translate of the initial directions
and is permuted by the automorphism is its invariant subgroup's coset partition.
The application takes the additive group of a binary extension field. -/
namespace Moonshot.FrobeniusBundles
variable {G : Type*} [AddCommGroup G]

inductive Direction (F : G ≃+ G) (U : Set G) : G → Prop
  | zero : Direction F U 0
  | seed {u : G} : u ∈ U → Direction F U u
  | add {u v : G} : Direction F U u → Direction F U v → Direction F U (u + v)
  | neg {u : G} : Direction F U u → Direction F U (-u)
  | forward {u : G} : Direction F U u → Direction F U (F u)
  | backward {u : G} : Direction F U u → Direction F U (F.symm u)

def invariantSpan (F : G ≃+ G) (U : Set G) : AddSubgroup G where
  carrier := Direction F U
  zero_mem' := .zero
  add_mem' := .add
  neg_mem' := .neg

/-- Parts may have unequal sizes. The automorphism permutes them. -/
structure StablePartition (F : G ≃+ G) (U : Set G) where
  partition : Setoid G
  transports : ∀ {x y}, partition.r x y ↔ partition.r (F x) (F y)
  complete_cosets : ∀ u ∈ U, ∀ x, partition.r x (x + u)

theorem forced_translation {F : G ≃+ G} {U : Set G}
    (B : StablePartition F U) {v : G} (h : Direction F U v) :
    ∀ x, B.partition.r x (x + v) := by
  induction h with
  | zero =>
      intro x
      simpa using B.partition.refl x
  | seed hu => exact B.complete_cosets _ hu
  | add hu hv ihu ihv =>
      intro x
      simpa only [add_assoc] using B.partition.trans (ihu x) (ihv _)
  | @neg u hu ih =>
      intro x
      simpa only [add_assoc, neg_add_cancel, add_zero] using
        B.partition.symm (ih (x + -u))
  | forward hu ih =>
      intro x
      simpa using B.transports.mp (ih (F.symm x))
  | backward hu ih =>
      intro x
      apply B.transports.mpr
      simpa using ih (F x)

def cosetPartition (F : G ≃+ G) (U : Set G) : StablePartition F U where
  partition := {
    r := fun x y => Direction F U (y - x)
    iseqv := {
      refl := fun x => by simpa only [sub_self] using (Direction.zero (F := F) (U := U))
      symm := fun {x y} h => by simpa only [neg_sub] using Direction.neg h
      trans := fun {x y z} hxy hyz => by
        simpa only [sub_add_sub_cancel] using Direction.add hyz hxy
    }
  }
  transports := by
    intro x y
    constructor
    · intro h
      simpa only [map_sub] using Direction.forward h
    · intro h
      simpa only [map_sub, AddEquiv.symm_apply_apply] using Direction.backward h
  complete_cosets := by
    intro u hu x
    change Direction F U (x + u - x)
    simpa only [add_sub_cancel_left] using (Direction.seed (F := F) hu)

theorem finest_stable_partition (F : G ≃+ G) (U : Set G) (x y : G) :
    y - x ∈ invariantSpan F U ↔ ∀ B : StablePartition F U, B.partition.r x y := by
  constructor
  · intro h B
    have h' := forced_translation B h x
    simpa only [add_sub_cancel] using h'
  · intro h
    exact h (cosetPartition F U)

theorem one_bundle_of_top {F : G ≃+ G} {U : Set G}
    (htop : invariantSpan F U = ⊤) (B : StablePartition F U) (x y : G) :
    B.partition.r x y := by
  apply (finest_stable_partition F U x y).mp _ B
  rw [htop]
  exact AddSubgroup.mem_top _

#print axioms finest_stable_partition
#print axioms one_bundle_of_top
end Moonshot.FrobeniusBundles
