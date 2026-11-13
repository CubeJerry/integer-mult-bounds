# Affine-period outward-slack preflight

**Gate: the proposed equality is true for the stated finite-index affine-period class, without injectivity. It gives an exact restricted answer to the outward-slack question, applies fiberwise to #6509, and makes #6758's sharp error bound an exact sharp outward-slack value. It does not settle the unrestricted class in #6619. No new implementation or cost result is made; novelty remains subject to comparison with #6534/#6536.**

## Pinned source boundary

- #6619, head `eaa967e7e8aa12cc53ec246a5fc00c5f8873a50b`, `research/rational-norm-rounding/PROOF.md`, blob `ffb873b2749b1590df9267e802aea5af2c2a6eb5`, 5,884 bytes, SHA-256 `231b1b322b6be2a798d1807f5c0346ac4002323384b45cd4eff2a0ef7210bc00`. Its classification explicitly leaves reversible rounding with outward norm slack outside its hypotheses.
- #6509, head `a4173e810c4d34a1d13b9745af123ad0ec6cfed5`, `research/conservative-gaussian-rounding/PROOF.md`, blob `b7047476aaa5e2bb149c92a8a40a9b2ab444ef73`, 11,768 bytes, SHA-256 `122eff335674d8de1bcba47d28feb0c420be62b2b6d4e84f91c4292383753380`.
- #6758, head `362b20bc934500bc503e850059f0d34daa5dcae3`, `research/four-axis-phase-covariant-grid/PROOF.md`, blob `bd5fb90ec3f064388eda1c1bd8834c26b4464bab`, 15,396 bytes, SHA-256 `dc07dcdf9793b401053738ea7e88c69495967f48f234e8411b8aaaa9858e8632`.

The credited finite-set lemma #2589 is cited in #6619; it is not needed here. Credit the finite-coset precedents #6534, #6536, and #6758. The exact #6758 source is checked below; #6534/#6536 have not been independently audited in this bounded preflight, so novelty remains open.

## Theorem and proof

Let U be a rational orthogonal d-by-d matrix and F: Z^d -> Z^d. Let Lambda be a full-rank sublattice of Z^d and suppose

\[
F(x+\lambda)=F(x)+U\lambda\qquad(x\in\mathbb{Z}^d,\;\lambda\in\Lambda).
\]

Full rank makes Z^d/Lambda finite. Set e(x)=F(x)-Ux. The premise makes e constant on each coset. Then

\[
\sup_{x\in\mathbb{Z}^d}\bigl(\|F(x)\|-\|x\|\bigr)
=\max_{[x]\in\mathbb{Z}^d/\Lambda}\|e(x)\|.
\]

For a fixed coset with error e, orthogonality gives

\[
\|F(x)\|-\|x\|=\|Ux+e\|-\|Ux\|\le\|e\|.
\]

If e=0, equality holds throughout that coset. Otherwise v=U^T e is a nonzero rational vector, since both U and e are rational. Clear its denominators and use finite index: for some integer c>0, lambda=cv lies in Lambda (indeed, a finite-index lattice contains m Z^d for some m). Starting from any representative x_0 in the coset, x_n=x_0+n lambda remains in that coset and tends to infinity along v. Therefore

\[
\|F(x_n)\|-\|x_n\|
=\|x_n+v\|-\|x_n\|\longrightarrow\|v\|=\|e\|.
\]

Thus the supremum on each coset is exactly its error norm. There are finitely many cosets, so the global supremum is their maximum. No injectivity, reversibility, nonexpansion, or numerical “rounder” property is used beyond the displayed affine-period law.

## Check against #6509 on fixed-sum fibers

For #6509's positive pair map, hold the Gaussian sum s=x+y fixed. The fiber is an affine rank-two lattice with difference coordinate d=x-y congruent to s modulo 2. Its tangent lattice is L={(z,-z): z is a Gaussian integer}, full rank in the two real difference coordinates. On that fiber the selected center c(s) is constant, and the map acts as the orthogonal sigma-i rotation of d plus the constant correction, so F(X+lambda)=F(X)+U lambda for lambda in L. The affine-fiber version of the ray proof gives sup on this fiber of (norm(F(X))-norm(X)) equal to norm(e_s): the upper bound is the triangle inequality, while U-transpose times e_s lies in the rational difference subspace and some positive multiple lies in L. The ambient pair norm and ambient pair error are used.

For the specific input s=1, c(1)=1, sigma=+1, the ambient pair error is e_s=((1-i)/2,(-1+i)/2), with norm 1. Its real Euclidean-adjoint direction is U-transpose e_s= (-(1+i)/2,(1+i)/2). Let

\[
(x_t,y_t)=(1-t-it,\;t+it),\qquad t\in\mathbb{Z}_{\ge0}.
\]

The source map sends it to ((1+t-it,\;-t+it)). Directly,

\[
\|(x_t,y_t)\|^2=4t^2-2t+1,\qquad
\|F(x_t,y_t)\|^2=4t^2+2t+1.
\]

Hence the outward norm difference is

\[
\frac{4t}{\sqrt{4t^2+2t+1}+\sqrt{4t^2-2t+1}}\longrightarrow 1.
\]

The candidate increment is exactly 2 U-transpose e_s, so it follows the positive error ray in the fixed-sum fiber. The pair error has squared norm 2|(1-i)c/2|^2=1, and all #6509 center choices have norm 0 on even-sum classes and 1 on odd-sum classes. Thus the supremum for this rounder is exactly 1, matching the candidate fiber ray. This is a check of a restricted example, not an unrestricted lower bound.

## Direct #6758 consequence

The pinned #6758 theorem defines a Gaussian-integer map F on sixteen coordinates with ideal unitary U and error norm at most sqrt(8) in both forward and inverse directions; it states both bounds are sharp. Its constructed native map has full-rank affine period Gamma=D-inverse(Lambda+i Lambda), with index 2^22, and satisfies F(x+lambda)=F(x)+U lambda. Identify Z[i]^16 with Z^32 and apply the theorem above to F. For the inverse, U Gamma is a full-rank sublattice of Z^32: the forward period identity and integer-valued F give U lambda in Z^32, while bijectivity gives F-inverse(y+U lambda)=F-inverse(y)+lambda. Thus the inverse also satisfies the affine-period premise, relative to U-adjoint. Each finite quotient has a coset attaining error norm sqrt(8), so the worst outward norm increment is exactly sqrt(8) for both directions. This is conditional only on #6758's stated native period/error theorem; it is not a new error bound, implementation, or memory result.

## Novelty and cost gate

The result directly quantifies the outward slack of finite-index affine-period rounders, a strict subclass of the outward-slack maps excluded from #6619's theorem. It does not imply a positive minimum slack for every reversible rounder, and it proves no obstruction or optimality outside the affine-period premise. It identifies #6509's fixed-sum fiber supremum as 1 and #6758's forward and inverse global suprema as sqrt(8).

This preflight adds no computation to #6509 or #6758 and no physical cost bound. The sources already have their own implementation statements; binding either implementation to another caller, proving a better tariff, or deriving a selected kappa is outside this result. The finite-coset precedents #6534/#6536 may subsume all or part of the lemma; root review is still needed before treating it as novel or expanding it into a package.
