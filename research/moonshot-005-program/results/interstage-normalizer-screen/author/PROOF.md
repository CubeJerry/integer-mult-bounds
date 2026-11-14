# The two orientations of actual interstage transport

**Proved source-bound identities and an all-width fixed-ordinary-template obstruction.** One orientation of the actual stage transport is ordinary; the other has growing support even after every intermediate-port cancellation. This does not exclude a redesigned encoded-role caller or a new paid shared service. No new κ.

## 1. Exact inherited interface

Use the112-port R0 word and the literal retained routes authenticated in `source/`. The companion physical-involution-interface proof, SHA256 `d7c9374323ba3e4fdb2cc4781b1b3c41ad7890426db308328946d327968022d8`, establishes for every column multiplicity V>=1

\[
A_s=M_s^{-1}(Q R_0)M_s=Q R_s,
\qquad R_s=M_s^{-1}R_0M_s,\qquad R_s^2=I.
\]

Here Q=diag_h C_(q_h)^(tensor V), M_s is the actual block diagonal ordinary route/translation, and R0 acts on whole arrays, outside tensor powers. Every R_s is an actual fixed ordinary bank circuit. Different stages use disjoint fresh eight-axis blocks. All extra stage axes are fixed spectators.

For any distinct s,t the two orders have different interfaces:

\[
\boxed{A_s^{-1}A_t=R_sR_t\quad\text{is ordinary},} \tag{1}
\]

whereas

\[
A_sA_t^{-1}=Q R_sR_tQ^{-1}. \tag{2}
\]

Equation(1) follows without Q/R commutation: A_s^-1=R_s Q^-1, so the adjacent Q^-1 Q cancel. It gives a legitimate ordinary change of encoded roles. It does not say the existing caller can omit its postservices. Those services have independent baselines and productive final duties, and a changed role schedule must establish its entire endpoint map and invoice.

The rest of this proof studies(2) for the exact two-stage adapter family pinned here. It does not quantify over alternative adapter choices. By renaming the fresh axes the same result applies to any distinct stages using this family.

## 2. Sum every intermediate port before testing covariance

Write the one-column spatial route as M_(s,h)=X_(tau_s,h)P_(s,h), with the exact translations and orthogonal involutions in `source/ROUTES.json`. For an output port h and input port j,

\[
(R_sR_t)_{hj}
=\sum_k R_{hk}R_{kj}
 M_{s,h}^{-1}M_{s,k}M_{t,k}^{-1}M_{t,j}. \tag{3}
\]

There are four nonzero intermediate ports k when h,j lie in the same four-port halfclass; otherwise the block is zero. The four coefficients are ±1/4. The checker reconstructs R from every literal ADD, derives every term's complete affine monomial from the actual M recipes, groups equal monomials and sums their coefficients before any conclusion.

In the Fourier convention a term is

\[
(L_k\widehat f)(z)=(-1)^{\ell_k\cdot z}\widehat f(F_k z),
\]

where F_k is orthogonal. Its actual signed formula is obtained by setting

\[
u=P_{s,h}z,\qquad v=P_{t,k}P_{s,k}u,
\]

then F_k z=P_(t,j)v and

\[
\ell_k\cdot z=(\tau_{s,h}+\tau_{s,k})\cdot u
 +(\tau_{t,k}+\tau_{t,j})\cdot v.
\]

All arithmetic in these formulas is binary. The check yields448 nonzero blocks, with four distinct nonzero signed monomial terms in each. It then evaluates actual Fourier rows, combining all terms that reach the same input frequency. In every block a remaining nonzero coefficient has q_h·z unequal to q_j·F_k z. Thus the summed R_sR_t fails Q-covariance, not merely its individual terms. A zero-frequency spectator in every other column lifts each witness to every V.

The same-stage control is essential: when s=t, the checker sums all paths and obtains the exact112-by112 bank identity. It therefore detects the genuine R_s² cancellation rather than labeling every multiport sum nonordinary.

## 3. Exact disjoint support gives an all-width theorem

Failure of Q-covariance alone would not prove(2) nonordinary. We instead retain explicit affine-support certificates. Because F_k is orthogonal, the spatial term is

\[
(L_k f)(x)=f(F_k(x+\ell_k)).
\]

At output row x the Gaussian-conjugated term C_(q_h)L_k C_(q_j)^-1 has input support

\[
F_k(x+\ell_k)+\operatorname{span}\{F_kq_h,q_j\}. \tag{4}
\]

The two generators are independent in every term, so this is a four-point affine plane. Every coefficient has magnitude1/2 before the scalar R_hk R_kj. The statement follows directly from the four translations in the product of the two C gates. It includes the actual affine displacement; omitting route translations would change the row certificate.

For every output port h, `RESULT.json` gives one explicit spatial row x_h. At that row, for each of the four input ports j, the four planes(4) are pairwise disjoint. The checker stores all their actual points. Different input ports are already disjoint coordinates. Thus all sixteen terms in the full output row have disjoint supports after their entire sum.

At width V, use the repeated output coordinate(x_h,...,x_h). Each term has support the V-fold Cartesian product of its four-point plane, containing4^V points. The term supports remain disjoint: they were disjoint in the first column. Its coefficient R_hk R_kj is ±1/4 **once**, because the port matrix acts on whole arrays; it is not tensor-powered. Therefore this full row of(2) has exactly

\[
\boxed{16\,4^V\text{ nonzero entries, each of magnitude }2^{-V-2}.} \tag{5}
\]

The squared norm is16·4^V·2^(-2V-4)=1, consistent with the complete unitary bank operator. This is a universal statement for every positive V, proved from explicit finite geometric certificates. It is not extrapolation from finite matrix experiments.

A fixed ordinary circuit made of coordinate monomials, scalar additions and finite owned zero workspaces has at most2^L original-coordinate paths in any output row when it uses L scalar additions. Monomials preserve the path count, and each addition at most doubles the maximum. Erasing workspace cannot increase an output row's original-input support. Equation(5) therefore requires

\[
L\ge 2V+4. \tag{6}
\]

In particular no V-independent ordinary template realizes the actual transport(2), including through nonunitary scalar additions or fixed clean workspace. Under the retained full-array-pass tariff, hiding Omega(V) whole-field passes as a negligible ordinary correction is not permitted at positive saving.

This is not a Gaussian moment lower bound. A changed productive-helper interface, a paid shared circuit, an implementation with new accounted work, other source adapters, or a redesigned chronological caller may escape this particular obstruction. Equation(1) remains available for such a redesign.

## 4. Reproduction, controls and classification

Run:

```sh
python check.py
python -O check.py --out RESULT-OPTIMIZED.json
```

The receipts are byte-identical. The script authenticates the two source files, reconstructs all exact scalar rows, forms all four-path products, sums duplicate affine monomials, evaluates448 actual covariance failures, and verifies112 full-row support separators. It also sums every same-stage block, obtaining exactly identity. Removing one actual path loses1/16 of squared row norm; incorrectly tensoring the scalar R coefficients yields only1/16 of the required squared norm already at V2. These controls distinguish the full bank tensor convention and necessary path cancellation from favorable independent-term accounting.

The source word and signed adapter recipes have separate independent reviews; this checker is author evidence, not an independent review of itself. The universal result is the tensor support argument and ordinary path bound; the finite certificate binds it to this exact source and route family. All compiler, native physical execution, precision, ordinary tape and analytic foundations remain. A new complete κ is not established.

Credit the full112 source to Worker B, the actual boundary and stage interface to Worker A/root, and the independently reviewed retained Gaussian/Clifford conventions to their original authors. This investigation was conducted for @CubeJerry with OpenAI assistance.
