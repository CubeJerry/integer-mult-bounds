# Sharp invertible column realization at a real shared chart

**Proved linear-algebraic interface, with finite adversarial checks and one actual source application. No new κ.** Prepared for @CubeJerry with OpenAI assistance. The actual source application is the separate two-departure word; this theorem is not a physical uniformity or global compiler certificate.

## 1. Precise proposition

Let F be any field, let A:F^r→F^m be the old quotient coefficient map on r genuinely available shared primal records, and let B:F^d→F^m be a specified list of d coefficient columns that should be assigned to outgoing encoded records. There exists Z∈GL_r(F) such that the first d columns of A Z equal B if and only if

    im(B) ⊆ im(A),          d−rank(B) ≤ r−rank(A).

Here d may exceed r in the stated test; when image containment holds, the second inequality then automatically fails. The r=0 or d=0 cases use their usual empty-space conventions. The result is a statement about invertible coefficient-column realization. It does not say that two records with the same coefficient column contain duplicate input values, or that individual output functions can be copied without acquisition.

When the existing primal and dual records are independent and physically cocharted, the genuine reciprocal encoding is a'=Z^{-1}a and b'=Z^T b. The forward quotient is A a=(A Z)a'. At a later actual common chart the inverse maps are a=Z a' and b=Z^{-T}b'. An arbitrary branch schedule still has to preserve these real records and execute these maps; column feasibility alone supplies no routes.

## 2. Necessity

Let V consist of the first d columns of Z. It is injective, and A V=B. Hence im(B) is contained in im(A). If x∈ker(B), then Vx∈ker(A). Since V is injective, its restriction embeds ker(B) in ker(A). Therefore

    d−rank(B)=dim ker(B) ≤ dim ker(A)=r−rank(A).

This excludes an attempted branch assignment even when its number of columns fits in the available width, if it repeats too many quotient directions for the available kernel capacity.

## 3. Sufficiency and explicit construction

Choose a linear section J:im(A)→F^r of A. Choose a complement U of ker(B) in F^d and an injection H:ker(B)→ker(A), which exists by the second inequality. Let P be the projection of F^d onto ker(B) along U. Define

    V = J B + H P.

Then A V=B. If Vx=0, applying A gives Bx=0, so x∈ker(B), P x=x, and 0=Vx=Hx. Injectivity of H gives x=0. Thus V is injective. Extend its d columns to a basis of F^r, obtaining the desired Z. This construction uses only finite-dimensional vector-space operations and works over every field, including finite fields. Choices of sections and bases require an actual uniform arithmetic implementation in any algorithmic application.

The criterion also applies to several branch subspaces: choose a basis of each demanded subspace and concatenate those desired coefficient columns into B. Their total repeated-dimension deficit is d−rank(B). Existing quotient-kernel directions can distinguish that many repeated outgoing columns inside an invertible full-state transform. The result is invariant under the basis choices within the branch subspaces.

## 4. Sharp additional paired-width requirement

Suppose extra scalar carrier pairs may be initialized to zero at the shared chart, so the extended quotient map is A_s=[A,0_s]. If im(B) is contained in im(A), the exact minimum additional paired width for this invertible column interface is

    s_min = max(0, d−rank(B)−nullity(A)).

This follows immediately because nullity(A_s)=nullity(A)+s. If the image condition fails, adding zero slots never repairs it.

Each added paired slot consists of two real owned fields: one primal and one dual. They are actual initialized zeros, with explicit allocation, routing and final clearing. They are not copies of aliased physical ports. Full-state invertibility is proved on the ambient extended space; the original run occupies its zero-padding subspace. The transformed padding coordinates need not stay zero during the computation. This sharp minimum is restricted to the stated invertible coefficient-column interface, and is not a lower bound on every algorithm with external observations, different endpoint contracts, noninvertible stages or additional channels.

For example, A=I_2 and B=[e1,e1,e1] require two extra paired slots. A single additional slot raises the width to 3 but gives only one quotient-kernel direction; two are needed to make three requested equal coefficient columns into independent ambient basis columns. Conversely A=[1,0] can realize B=[1,1] without new width because its existing kernel already supplies one degree of freedom. These are coefficient assignments, not assertions about initially equal or unequal encoded scalar contents.

## 5. Honest local invoice and physical gate

The theorem starts with all r existing primal and all r existing dual records at a single chart D. If those records are on separate lines, their acquisition and all affected later routes must be emitted first. Suppose s extra paired slots are used and n=r+s. A direct implementation of each dense linear map on n fields uses n temporary owned snapshots, n INITs, n CLEARs, and `2n+nnz(M)` scalar ADDs: copy each input into its snapshot, subtract that snapshot from its old record, and add the desired matrix row. The real operation is invertible on the retained n fields; discarding the snapshots uses the retained paid owned-erasure contract.

Applying this implementation to the four maps Z^{-1}, Z^T, Z, Z^{-T} uses exactly

    4n INITs, 4n CLEARs,
    8n + 2 nnz(Z) + 2 nnz(Z^{-1}) scalar ADDs,

in addition to the 2s initialized persistent padding fields and their 2s final CLEARs. The peak additional owned fields is at most 2s+n if the four maps execute sequentially. Sparse elementary realizations can be cheaper; the two-departure word uses its explicit three-operation 2-by-2 transforms instead of this generic dense bound.

Every persistent padding field that leaves D must be charged at each real MOVE. If the paired primal and dual fields use the same ascending branch path with ranks rho_e, one padded slot adds `2 sum_e rho_e^t` to the moment, before any compiler, scalar arithmetic, precision or allocation expenses. In particular, the theorem never turns the width deficit into a free duplicate bank. Real initial-chart acquisition, branch destinations, the common inverse chart, all raw refinements and all existing duties remain separate physical proof obligations.

## 6. Actual two-branch source realization

The separate two-departure construction uses the exact old shared columns A83=u and A85=v at their actual dimension-2 binary span. These two columns are independent. The desired outgoing coefficient columns are u+v and −u+v. Their unique change on this two-dimensional span is

    Z = [[1,-1],[1,1]],       Z^{-1} = (1/2)[[1,1],[-1,1]].

Thus d=2, rank(B)=2 and nullity(A)=0 over every field of characteristic other than 2. No added slots are needed. The dimension-2 physical chart contains exactly the two relevant source lines 83 and 85; no third raw donor is silently available there. The two outgoing encoded records move into distinct dimension-3 spans, each nested in its intended new receiver facet and original B cohort. Their true duals move with the reciprocal map. The paired word supplies both old duties and the two new contacts, with all inverse operations and routes emitted.

The specified plus/minus realization is singular in characteristic 2. The generic theorem still holds there: its criterion correctly rejects these two requested columns for A of rank 2 and nullity 0. The actual finite Clifford source is complex; this observation is an algebraic scope statement, not a claimed characteristic-2 implementation.

The exact source instance and inverse matrices appear in CHECK.json. The full finite source word, all-1880-column checks, twelve exact chart receipts, paid profile and immutable source/parent pins are in ../two-departures/. They remain the physical evidence; this theorem does not replace their checks.

## 7. Verification and limits

Run

```sh
python3 -I -B check_branch_column_lifting.py --output branching-gate
```

The checker exhaustively enumerates all relevant A and B and all injective lifts V in the listed small finite-field domains. It compares the actual set `{A V: V injective}` with the theorem's criterion on 89,886 (A,B) pairs. It tests both characteristic 2 and characteristic 3, includes over-width choices, checks failure of image containment, and verifies that repeated quotient columns require the precise extra kernel width. It separately checks the rational two-branch instance and both inverse maps. No imported author source interpreter is used in these finite algebraic checks.

These finite checks are adversarial coverage, not the universal proof. Sections 2 and 3 prove the all-field proposition. Physical, recursive and asymptotic admission remains conditional on the explicit interfaces and all retained foundational assumptions. Independent review of the new theorem and source composition remains required before programme admission.
