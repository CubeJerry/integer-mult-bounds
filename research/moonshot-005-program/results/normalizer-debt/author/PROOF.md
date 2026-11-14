# Every omitted post-normalizer leaves a real defect in the retained short caller

**Proved source-specific omission theorem, plus a separately scoped class-row tariff. No new κ.**

The full112 R0 source is complete for its paired coefficient shear, but its actual retained stage adapters require a paid bank normalizer. The root and Worker A identify the same stage-independent service

\[
N=Q^{-1}R_0Q,\qquad Q=\operatorname{diag}_h C_{q_h}^{\otimes V},
\]

on112 arbitrary coindexed arrays. Two independent bank services are required per native invocation. The scalar identity N²=I suggests carrying encoded banks between invocations. This note proves that merely deleting any nonempty subset of the postservices from the existing caller cannot realize that idea, even on a physical subspace where all stage route differences disappear. A changed encoding schedule or a genuinely shared service remains open.

## 1. Exact retained schedule and the omission question

Use Worker A's parity-uniform E-free caller with a>=1 arms,2a HOST2 stages,4a+2 arbitrary roles, four QUERY calls and the credited whole-idle schedule. Its two chains have roles

`A,F1,...,Fa,H1,...,Ha` and `B,G1,...,Ga,J1,...,Ja`.

At each stage the literal HOST2 mains, in the actual temporary stage basis, are `X=1,Y=0,U=2a+1,V=2a+2`. The exact paid repair applies a post-normalizer to Y and V. Pre-normalizers and ordinary stage/caller operations are retained. An *omission pattern* chooses any subset of those4a postservices to delete, leaving every other operation unchanged.

The theorem is not about arbitrary schedules of N gates, conjugated row operations, extra encoded roles, or restructured source histories. Those are new constructions. It also does not claim a lower bound for the cost of one N service.

**Theorem.** For every a>=1, every width V>=1 and every nonempty omission pattern, the resulting retained caller fails its stated diagonal endpoint on some legitimate input. In particular no pair, collection or even all of its existing postservices can simply be dropped by invoking N²=I.

## 2. A genuine all-width physical invariant subspace

Use the Fourier character with frequency zero in every head and fresh body coordinate. Equivalently, each input array is constant in its spatial argument. At this character every C_q, every fresh Gaussian D_s, every route permutation, every ordinary translation and every lambda correction has value1. This remains true after any number V of columns. It is an actual available character, not an arbitrary phase assignment to native labels.

On this subspace N=R0. Since R0=I−D and D²=2D, a nonzero vector v=D e_h satisfies R0v=−v. The pinned literal R0 source supplies such a dyadic vector; `RESULT.json` records it and checks every one of its112 coordinates. Restrict every caller-role bank to a scalar multiple of this same v. All ordinary role operations preserve this port eigenspace. On it, each omitted Y or V postservice negates that particular HOST2 output. A present postservice restores the intended output.

The corrected stage at this character has X'=X,Y'=Y+X,U'=U−V,V'=V. Omitting Y replaces Y' by−(Y+X); omitting V replaces V' by−V, without changing U'. All stage symbols and idles are identity. The four-query paired middle, being the proved E-free middle at S=1, is exactly identity on arbitrary role inputs, including already corrupted inputs. Thus the two chains may be analyzed separately.

## 3. Four invariant witnesses

We use chronological stage order, with left sites1,...,a followed by right sites1,...,a. Their exact ordinary bases are pinned in `source/short-build.py` and explained in `source/short-PROOF.md`. Write e_A for the root coordinate functional and e_Fi,e_Hi for the leaf coordinate functionals.

For the first chain, a deleted Y postservice makes its active temporary coordinates `(u0,u1)` undergo `(−u0−2u1,u1)` after the retained ordinary ADD. In the original chain coordinates its left-site map is

\[
I-2x_i e_A,\quad x_i=A+F_i+2\sum_{j<i}F_j.
\]

The right-site map is

\[
I-2x'_i(e_A+2e_{H_i}),\quad
x'_i=-A+H_i+2\sum_{j>i}H_j.
\]

A present postservice gives the identity site at this character.

For the second chain, a deleted V postservice makes the active coordinates undergo `(u0+2u1,−u1)`. Its left-site map is

\[
I+2G_i(e_B-e_{G_i}),
\]

and its right-site map is

\[
I+2(-2B+J_i+4\sum_{j>i}J_j)(e_B+e_{J_i}).
\]

These formulas are direct conjugations by the actual stage basis; they use no commuting assumption about general physical N operators.

| Omitted service | Exact final defect, independent of every other omission |
|---|---|
| Left Y at i | coefficient from initial A to final F_i is2 modulo4 |
| Right Y at i | final H_i coefficient on its own input is−3 |
| Left V at i | final G_i coefficient on its own input is−1 |
| Right V at i | final J_i coefficient on its own input is3 |

For the first line, the root before any left site is ±A. At the omitted site the new F_i root coefficient changes by±2. Earlier left sites do not touch F_i. Every later omitted left site changes that coefficient by a multiple of4. Right sites never change an F leaf, so it remains2 modulo4. For the other three lines, earlier sites introduce no dependence on a future leaf into the root or current leaf. The displayed site formulas therefore set the selected leaf's own-input coefficient to−3,−1 or3. Subsequent sites never touch that leaf. The identity middle cannot change any witness.

Every nonempty pattern contains at least one listed omission. Each witness differs from the intended identity endpoint, proving the theorem. This proof is uniform in the arm count and in width; finite pattern tests are controls, not its justification.

## 4. Concrete twelve-stage counterexample

With all postservices omitted, give only the first chain's H_a bank the input v above and every other role the zero array. All prior sites leave that bank alone, and the final right site sends4v into the root A. The required root output is zero. Thus this one simple input disproves dropping all postservices for every a>=1 and every V.

More fully, the first-chain root row with all services omitted is

\[
A_{\rm out}=\frac{4(-1)^a-5^a}{3}A_{\rm in}
  +4\sum_{i=1}^a(-5)^{a-i}H_{i,\rm in}.
\]

Indeed after the left sites A_0=(-1)^a A_in. Before right site i, every later H leaf has changed by−2(A_(i−1)−A_0), so `A_i=−5A_(i−1)+8A_0+4H_i,in`. Solving this recurrence gives the formula. At a=6 the authentic26-role literal replay gives

`A_out=−5207A−12500H1+2500H2−500H3+100H4−20H5+4H6`.

This is a failure of the unchanged schedule, not a proof that encoded-bank propagation is impossible. A successful propagation construction must alter actual interfaces or role operations so that these witnesses no longer apply, and must preserve the four queries, independent productive targets and complete cost ledger.
