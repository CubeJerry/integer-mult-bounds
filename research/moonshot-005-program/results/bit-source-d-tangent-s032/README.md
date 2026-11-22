# Full source/D tangent and exact local parameter lift

**Exact tangent dimension and actual coupled quotient/D interpolation. Full source validity, a fifth whole receiver and a new κ remain unproved.**

This package linearizes all 44 local systems of bit-source-d-interpolation-s032 at the original four-receiver D1509 word. Previous packages remain unchanged.

## Full tangent space

The 35-by-35 word has a 19/16 early/late split, leaving 921 legal coefficient variables. Exactly 561 occur in retained sections for receivers 6, 9, 48 and 73 on the eleven donors; 360 leave all retained sections unchanged.

For each local system write X=[C,L], let N span ker X, and let N_r be its receiver parts. Put S(j,r)=T[O(r),I(j)] and M(j,h,r)=B(j,h,r)^(-1)E(j,h,r). In characteristic two, d(S^(-1))=S^(-1)(dS)S^(-1). The local tangent equation is

    sum_r M(j,h,r) S(j,r)^(-1) dT[O(r),I(j)] S(j,r)^(-1) N_r = 0.

All 44 systems, after dropping zero scalar equations, give a **944-by-561 matrix of rank 88** over GF64. Its saved complete kernel has dimension **473**. Together with 360 invisible directions, the full tangent space has dimension **833** inside 921 phase-legal coefficients.

The 473 visible directions change some required source quotient image. For every donor/receiver, stacking the four parent maps M has rank 8, checked exactly. Thus zero derivative of all parent images implies zero derivative of the inverse section. Inversion has an invertible derivative, and the section union covers the 561 visible coefficients. Tangency alone is a first-order condition.

## Exact coupled lift

The first visible basis direction changes only physical D coefficient (0,0) by 1. At t=1, T'=T+Delta has both phase blocks and all 144 geometric D sections invertible. All 44 exact local interpolation equations hold. The saved 6-by-96 source corrections change twelve quotients: the four D parents of donors 0, 32 and 35. They preserve the prescribed native H images and four D identity readouts exactly.

The relative changes are not all square-zero. For a rank-one section change E, put alpha=trace(S^(-1)E). The rank-one inverse formula gives

    (S+tE)^(-1) = S^(-1) + t/(1+t alpha) S^(-1) E S^(-1).

In each local kernel relation, the derivative coefficients grouped by equal alpha vanish separately. The saved zero matrices certify the full rational relation for every t away from its poles. A fixed linear extension operator for X then supplies compatible rational quotient maps F(t), with F(0)=F_old.

The full 144-section family excludes the nine nonzero GF64 parameters 2,7,21,36,37,45,48,53,60. Phase invertibility additionally excludes 46. Thus **53 nonzero parameters**, including 1, preserve all D phases and sections and satisfy all local interpolation equations.

At t=1, the fixed forced four-space K still has contrast rank 30 and augmented rank 32: its common response has rank **2**, not 4. This lift does not solve the fifth-receiver obstruction.

## Evidence and limits

CERTIFICATE.json.gz contains the exact tangent matrix, pivots, full visible kernel and literal t=1 D/source corrections. RESULT.json records dimensions and the finite lift. LIFT-RESULT.json records all section checks, parent-map ranks and parameters; LIFT-CERTIFICATE.json.gz saves grouped rational coefficients. SOURCE-PINS.json and MANIFEST.json bind inputs and outputs.

Controls include the reviewed original source/D base point, exact multiplication of the full tangent kernel, each finite correction on every input generator, all 144 finite section ranks, and grouped rational identities. The separate independent tangent review confirms the complete tangent and finite t=1 interpolation; the rational extension has a separate proof review.

Complete source-view ranks, source early-phase invertibility, strict nonsaturation and a chronological source compiler invoice remain unchecked. Prescribed parameter images alone do not prove exact dimensions of entire inverse fibres. Fifth-receiver isolation, other source stars, return and both strict suppliers remain open. No new complete κ.

## Reproduction and next equations

From the repository root, copy tangent.py and lift.py into an empty temporary directory. Run the copied lift.py with python3 -B while keeping the repository root as current directory. It invokes the copied tangent generator and writes beside itself. Only the first nullspace direction was used.

The next problem is a combination in the 473-dimensional visible tangent space with an exact lift that changes the forced-K common-response rank. The nonlinear equations remain Y(T') ker[C,L]=0 for all 44 systems, with nonzero section determinants. Full source validity and compiler conditions are required before any local interpolation replaces an admitted source word.

Credit preceding S031/S032 constructions and independent reviewers, @CubeJerry, and inherited geometry/compiler contributors. Substantial OpenAI assistance. Apache-2.0.
