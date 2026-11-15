# A zero-ordinary two-native middle has no ordinary left kernel at rank one

**Proved source-bound structural lemma; independent review pending.** This
explains why the first literal four-K target fails and gives the exact boundary
change needed next. It does not exclude four native calls with changed ordinary
endpoint encodings or mixed native orientations. No new κ.

Work in the admitted faithful Gaussian-rank group algebra, with ordinary
subalgebra O, source a of rank one, and a² of rank two. Set

    K=[[I,0,a−I],[a,0,−a],[I,I,−I]],
    τ(q)=π₀(a q a),   q∈O.

For each r=0,1,2, coefficient selection in the ordinary group basis defines
q_r∈O with `π_r(a q a)=a q_r a`. These are algebraic support projections,
not free physical services. Let Q∈GL₃(O) and M=KQK.

## 1. Exact classification of π₀(M)=0

Write `K=K₀+aK₁`, with scalar role matrices

    K₀=[[1,0,−1],[0,0,0],[1,1,−1]],
    K₁=[[0,0,1],[1,0,−1],[0,0,0]].

Ordinary bimodularity gives

    π₀(KQK)=K₀QK₀+K₁τ(Q)K₁.

Expanding this linear equation shows that π₀(M)=0 holds exactly when

    Q=[[r−s,q+u,c],[s,d,0],[r,q,c]],
    s=τ(q),   τ(r)=τ(u)=τ(s)=0.                         (1)

Here r,q,u,c,d∈O may fail to commute and may individually be singular.
Subtract the third row from the first, then add that new first row to the
second. The resulting block matrix is

    [[−s,u,0],[0,d+u,0],[r,q,c]].

Since Q is invertible on the finite represented spaces, its triangular
diagonal blocks force s, D=d+u, and c to be invertible. Their inverses lie
in O by finite-dimensional inverse closure. This conclusion is forced; it
does not assume cancellation in an arbitrary ring with zero divisors.

## 2. Rank-one ordinary left-kernel theorem

**Theorem.** Under (1), if α,β,γ∈O and

    (α,β,γ) π₁(M)=0,

then α=β=γ=0.

Direct multiplication gives

    KQ=[[a r−s,a q+u,a c], [−a s,a u,0], [0,D,0]].

The second column of M is therefore `(a c,0,0)ᵀ`, which is pure rank one
and invertible in its first block. The kernel equation forces α=0.
The third row of M is `(D a,0,−D a)`, also pure rank one. Write
`π₁(a u a)=a u₁ a` using the ordinary coefficient selection above. The first
column of the remaining kernel equation is

    β(−a s+a u₁ a)+γD a=0.

Because s=τ(q)=a q₀ a is a unit, q₀=a⁻¹s a⁻¹ is an ordinary unit. Multiply
the displayed equation on the right by a⁻¹ to obtain

    −β a²q₀ + β a u₁ + γD =0.                            (2)

The three terms belong respectively to E₂, E₁ and E₀. Their sum is direct.
The E₂ component gives βa²q₀=0, hence β=0 because a²q₀ is invertible.
The E₀ component then gives γ=0. This proves the theorem. It concerns an
ordinary-coefficient left kernel, not the unrestricted physical matrix rank.

## 3. A genuine constructed zero-ordinary middle

The condition π₀(M)=0 is achievable; it is not itself the obstruction.
For the actual source `a=(C_b S)^{⊗V}`, take

    h=(S⁻¹)^{⊗V},   s=(X_b S)^{⊗V}=a h a.

Then a s a has Gaussian rank two: at one column it is
`C_b C_c X_a`, and the identity tensors literally. Thus τ(h)=s and τ(s)=0.
Also τ(I)=0 since a² has rank two. For any ordinary r,u with τ(r)=τ(u)=0,
the matrix

    Q(r,u)=[[r−s,h+u,I],[s,I−u,0],[r,h,I]]                (3)

is an ordinary unit: the row operations in Section 1 give triangular
diagonal `(−s,I,I)`. Consequently KQ(r,u)K is an actual two-native word
with no ordinary Gaussian component. This includes r=u=I.

An explicit inverse for r=u=0 is

    Q(0,0)⁻¹=[[-s⁻¹,0,s⁻¹],[I,I,−I],[−h,−h,I+h]].

Every coefficient h,s is an actual ordinary coordinate permutation; no
Gaussian inverse or new clean role is being granted. The complete supplier
invoice and remaining physical contracts are still owed before this seed
could be used as a construction component.

For example Q(I,I) has the explicit in-place implementation

    z←z+x;  z←z+h y;  x←s x;  y←y+z;  y←y−x;  swap(x,y).

The h-weighted addition is implemented by applying h to y, adding into z,
and restoring y with h⁻¹. Thus this uses four ordinary additions/subtractions,
three head-permutation services and one role swap, with no extra field or
erasure. All signs are field-level coefficients. The two K factors each
retain their native ADD, three source head gauges, and the two ADDs/role cycle
implementing T. For two fresh bodies and three retained roles, both inactive
rank-seven jobs are paid: the Gaussian profile is `2[1]+4[7]+2[8]`.
The endpoint is the displayed non-Gaussian intermediate, not three completed
independent Gaussian jobs. No supplier price is inferred from this profile.

Despite that positive cancellation, Section 2 says that its rank-one part
has no nonzero ordinary left annihilator. A small physical rank by itself
does not supply the ordinary frame required by the next native.

## 4. Consequence for the first four-native literal target

The initial proposal was

    K P₃ K P₂ K P₁ K = a³ I₃,

with all three P_i ordinary units. Rearranging with K³=a²I gives

    P₃ (K P₂ K) P₁ = K⁻¹(a³I)K⁻¹ = aK.

The right side has zero E₀ component. Hence M=KP₂K satisfies Section 1.
But π₁(aK) has zero second row, so ordinary equivalence would give a nonzero
ordinary left annihilator of π₁(M), contradicting Section 2. Therefore this
literal target has no solution, even with unrestricted full ordinary
interstages and all the actual scalar phases retained.

This does not exclude the endpoint `a³C` for an invertible scalar role
matrix C, which is equally useful after an ordinary endpoint recoding.
Indeed `K⁻¹a³CK⁻¹` can have a nonzero E₀ component. Such a boundary matrix,
or genuinely mixed native orientations, is the next concrete construction
attempt; widening the coefficient catalogue for C=I cannot help.

Credit @CubeJerry and the retained actual three-head source/rank-component
authors; Worker B's source-bound middle classification, constructive ordinary
unit, and ordinary-kernel obstruction, with OpenAI assistance.
