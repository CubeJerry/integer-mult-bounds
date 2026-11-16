# Gaussian-component augmentation excludes the middle-oriented singular prefix

**Universal scoped obstruction and a sharper continuation interface. Independent review pending. No new κ.**

This result closes the apparently surviving `T0=SWAP_ab Z_c` first-column orientation in the companion ordinary-kernel bridge. That bridge's exact source transport and nonzero ordinary kernel remain valid. The new obstruction uses how each Gaussian component acts on the ordinary trivial character, rather than denying the kernel's existence.

## 1. The fixed-catalogue interface and a component character

Work in the retained three-bank literal four-bit source contract. A one-column ordinary monomial is a permutation matrix with entries in `{1,i,-1,-i}`. At width V it is lifted as `g^tensor V`. An ordinary block is a finite linear combination of these collective lifts, with exterior scalar coefficients; an ordinary unit and its actual inverse have finite such descriptions. The finite catalogue is fixed before V grows. Exterior scalars remain exterior scalars. This is the exact scope of the existing finite tensor-word separation theorem.

Fix a complete finite catalogue containing every source word and every word needed for the ordinary endpoint encoders, decoders, and their inverses. At all sufficiently large faithful widths, projectively distinct words in this catalogue are linearly independent after tensor lifting. Restrict below to V divisible by4.

For an expression X in this catalogue, define `Phi_r(X)` by summing its exterior coefficients on words that are exact Gaussian rank-r operators up to ordinary monomial gauges. Apply this entrywise to block matrices. `Phi_0` is ordinary augmentation. A root-four scalar in a literal one-column word becomes1 after tensor lifting at these widths; its projective normalization therefore does not change this sum. A scalar outside the tensor lift is retained.

This is a well-defined map on the actual operators at sufficiently large faithful widths. Any projectively equal unitary source words U=lambda W over `Z[i,1/2]` have a root-four phase. For any fixed column k, unitarity gives `lambda=sum_j U[j,k] conjugate(W[j,k])`, so lambda belongs to `Z[i,1/2]`; its modulus is1, and every unit-modulus Gaussian dyadic is a fourth root of unity. This covers canceled non-Gaussian projective classes as well as Gaussian ones. Faithful tensor separation then rules out all other ambiguities. The threshold depends on the complete fixed catalogue, not on a numerical experiment.

For ordinary blocks B,D, with augmentation epsilon,

    Phi_r(B X D) = epsilon(B) Phi_r(X) epsilon(D).      (1)

Indeed left or right multiplication by a monomial preserves exact Gaussian rank, and the statement follows by distributing the finite sums. It also applies to classes that do not occur in the desired endpoint: their Phi value is zero. This is an ordinary-bimodule map, not a multiplicative evaluation of arbitrary source products.

If E has independent Gaussian endpoints (4,2,1), with ordinary invertible input/output interfaces, then

    Phi_4(E)=U P4 W,
    Phi_2(E)=U P2 W,
    Phi_1(E)=U P1 W,                                  (2)

where U,W are invertible scalar3x3 matrices and P4,P2,P1 are the three distinct coordinate projectors. In particular the three nonzero image lines in(2) are independent. All forbidden Gaussian-component maps, including Phi_0 and Phi_3, vanish. This follows directly from(1), since each canonical normalized Gaussian head has Phi equal to1 in its own class and0 in the others.

At small widths these maps need not be well-defined. For example the one-column A itself is a linear combination of two ordinary monomials, although its exact Gaussian rank is1. The all-width proof therefore requires the faithful finite-catalogue qualification and must not identify Phi with a numerical projection at V=1.

## 2. A general middle-sector obstruction

Write an arbitrary ordinary-unit first interface as

    C=[[s,b,c],[t,d,e],[u,f,g]],

and let Q=(qij) be any ordinary unit. Retain the native L,U of the source programme and E=L C U Q L. Define

    K=(a s a,a t a,0)^T,
    W=(0,s,u)^T,
    Z=(a b a,b a+a d a,f a)^T,
    Fcol=(a c,c+a e,g)^T.

The exact source expansion is

    L C U=[K+W a, -K a-W a²+Z, Fcol].                 (3)

Suppose the following fixed-catalogue hypotheses hold:

1. K is pure Gaussian rank2 and K a is pure Gaussian rank3.
2. `epsilon(s)=0` and `epsilon(t) != 0`.
3. An ordinary idempotent Pi fixes K and satisfies `epsilon(Pi)=diag(0,1,0)`, where D=16^V.

Then E cannot have independent (4,2,1) endpoints for any choice of the other C blocks and any ordinary-unit Q, at every sufficiently large faithful V divisible by4.

**Proof.** Only the four-source term

    -K a [q10 a,q11 a,0]

can contain Gaussian rank4: every other term in the expanded circuit has at most three source factors and one-column support at most8. Ordinary monomial gauges preserve Gaussian rank, so class extraction commutes with Pi. Since Pi K=K, Pi fixes E4. By(1), `Phi_4(E)=epsilon(Pi)Phi_4(E)`. Its rank is1 by(2), so its image is exactly the middle scalar line. No physical-rank assumption on Pi or physical-image equality is needed.

Put `v=(epsilon(s),epsilon(t),0)^T`, a nonzero vector on that same middle line. Purity gives `Phi_2(K)=Phi_3(Ka)=v`: expand s,t in ordinary monomials, and observe that every canceled projective class has coefficient sum0 at these widths by the preceding unitary-dyadic phase lemma. The coefficients retained in the pure class therefore sum to the total ordinary augmentation.

The last input column of E is

    (K+Wa)q02 +(-Ka-Wa²+Z)q12 +Fcol q22.              (4)

Its only rank3 terms are -Ka q12. Hence Phi_3(E)=0 forces `v epsilon(q12)=0`, so epsilon(q12)=0. Equation(1) now removes every term having q12 on its right from every component character, even when Z itself has mixed Gaussian classes.

The rank2 character of(4) is therefore `v epsilon(q02)`. Independence from the Phi_4 image line in(2) forces epsilon(q02)=0. Since epsilon(Q) is invertible, its last column is now `(0,0,epsilon(q22))^T` with epsilon(q22) nonzero.

The ordinary character of(4) is then

    (0,epsilon(c),epsilon(g))^T epsilon(q22).

It must vanish, so epsilon(c)=epsilon(g)=0. Invertibility of epsilon(C) forces epsilon(e) nonzero. Finally the rank1 character of(4) is

    (0,epsilon(e)epsilon(q22),0)^T,

a nonzero middle-line vector. This makes Phi_1 and Phi_4 have the same image line, contradicting(2). Every inverse and ordinary-algebra dependency has been retained. The value of u=C20 never entered the argument. ∎

This theorem does not assume physical injectivity of K, ordinary-column injectivity of K, or the absence of a genuine ordinary kernel for Ka.

## 3. Application to the actual square-transported kernel

Use the literal source controls from the companion package:

    F=Z_a, P=(I+F)/2, M=I-P,
    J=R2^-1 SWAP_ab R2, Fhat=a F a^-1=Z_d,
    T0=SWAP_ab Z_c, T=(I+T0^tensor V)/2,
    Rminus=(I-(J Z_a)^tensor V)/2.

The exact identity `a^-2 T0^tensor V a²=(J Z_a)^tensor V` gives a genuine half-dimensional ordinary kernel `Ka Rminus=0` for

    s=M T, t=J P T.

The companion exact source gauges prove K pure2 and Ka pure3. The ordinary range projector is

    Pi=diag((I-Fhat)/2,(I+Fhat)/2,0).

It has rankD and fixes K. Its epsilon is diag(0,1,0), while epsilon(s)=0 and epsilon(t)=1. Thus all hypotheses of Section2 hold. This entire oriented first-column family is excluded, including arbitrary C20 and arbitrary completions of C and Q. The physical kernel channel is real; it is not sufficient to evade the component-character obstruction.

The earlier ordinary-kernel bridge's “surviving” label meant only surviving its two stated gates. This result supersedes that continuation status without changing the exact source transport, kernel theorem, free ambient range, Gaussian gauges, or physical interface receipts.

## 4. The opposite orientation is a concrete surviving interface

Reverse the two complementary sectors:

    s=P T, t=J M T,
    Pi'=diag((I+Fhat)/2,(I-Fhat)/2,0).                 (5)

Then epsilon(Pi')=diag(1,0,0), and the nonzero prefix character is the first scalar line. The two-source prefix is still singular of rankD/2; its ambient range is still a free ordinary one-bank range, with the explicit controlled-route decoder using the complementary output projector. Its actual Ka kernel is still Rminus, and all rank2/rank3 purity gauges are the same literal source words as before, with only signs changed in their finite combination.

For any successful caller in this opposite orientation, the last-column argument still forces

    epsilon(q12)=epsilon(q02)=0,
    epsilon(q22) != 0,
    epsilon(c)=epsilon(g)=0, epsilon(e) != 0.          (6)

Now the forced Phi_1 image is the middle line, which is disjoint from the first-line Phi_4 image. Hence(6) is compatible with scalar endpoint independence. The untouched controlled-route completion `C_new` has epsilon(g)=1 and is excluded by(6); its last two input columns must be exchanged or otherwise changed before a longer search is warranted.

This is a useful exact orientation constraint, not evidence of a full caller. A scalar toy model with Phi4=e0e0^T, Phi2=e2e1^T and Phi1=e1e2^T passes the necessary independent-image test; it deliberately asserts no source-level lift.

## 5. Cost and verification scope

No extra caller has been admitted. The opposite controlled-route first interface and its inverse use the same numbers of primitives as the preceding family; exchanging the last two columns has an explicit ordinary bank swap and its actual inverse. The checker records every ADD, SCALE and MONO, prefix bounds, omitted-ADD controls, exact Gaussian gauges and source transport identities. The three-native optimistic invoice remains `3[1]+6[7]+3[8]` versus `[25]+[23]+[22]`, before all remaining caller, source, precision, ownership and recursive costs. All five foundational assumptions remain.

The next construction attempt must use the opposite orientation, a completion satisfying(6), an actual nonzero q12 through Rminus, and must cancel the rank2 residue while retaining independent rank2/rank1 endpoints. Finite modular searches are not part of this universal theorem.

Credit @CubeJerry, the four-bit source and S018 source-coset framework, the S019 complex worker, and substantial OpenAI assistance.
