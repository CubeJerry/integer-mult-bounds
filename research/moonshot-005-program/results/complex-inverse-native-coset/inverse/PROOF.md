# Exact inverse-native closure for the four nonlinear sign sources

**Proved algebraic construction; physical admission is conditional on the retained fixed-table monomial compiler and its existing foundations. No profitable caller and no new kappa.**

## 1. Source, convention, and statement

Fix one canonical odd three-bit sign source

    f(a,b,c)=J c+B b c+a b c,    J,B in {0,1},
    S=D_f P,    A=C_b S,

where P sends the input bits (a,b,c) to (b,c,a), D_f has diagonal entry (-1)^f, and C_b=(I+i I+(1-i)X_b)/2. The four truth-table masks are 128,64,112,176 for (J,B)=(0,0),(0,1),(1,0),(1,1). The admitted family proof supplies actual ordinary square and cube gauges. In particular A and A^-1 are rank-one Gaussian units, while A² and A^-2 are rank-two Gaussian units.

Let Q swap the address bits a,c, and let Z be the diagonal sign (-1)^(a+b+c+B a c). Define the actual monomial T=Z Q S. Then

    T A^-1 T^-1 = -i A.                                      (1)

For every positive tensor width V, put a=A^tensor V and t=T^tensor V. With the exact scalar lambda=(-i)^V, equation (1) gives

    a^-1=lambda t^-1 a t.                                    (2)

There is no phase quotient or omitted width dependence. The inverse table is retained explicitly; in this canonical case T is an involution.

## 2. Proof and literal tables

First S A^-1 S^-1=C_b^-1 S^-1. Conjugation by Q fixes C_b and reverses P; it therefore gives

    Q S A^-1 S^-1 Q = C_b^-1 D_g P,
    g(a,b,c)=f(b,a,c)=J c+B a c+a b c.

The total-parity sign Z_0=(-1)^(a+b+c) commutes with every diagonal D_g and with P. Since Z_0 C_b^-1 Z_0=-i C_b, conjugation by Z_0 gives -i A_g. Finally the sign Z_1=(-1)^(Bac) commutes with C_b and changes g by B(ac+bc), because (P^-1 x)_a(P^-1 x)_c=bc. Thus Z_1 A_g Z_1=A_f. Since Z=Z_1 Z_0, (1) follows.

For a direct compiler interface, T simply swaps b,c and applies the sign

    (-1)^[(J+1)a+b+c+B(ab+ac)+abc]

on the original input address. Its permutation, input-indexed in the order a+2b+4c, is

    [0,1,4,5,2,3,6,7].

The input-indexed powers of i for its signs are:

| Source mask | Phase exponents |
|---|---|
| 128 | 0,2,2,0,2,0,0,0 |
| 64 | 0,2,2,2,2,2,0,0 |
| 112 | 0,0,2,2,2,2,0,2 |
| 176 | 0,0,2,0,2,0,0,2 |

The sign polynomial is symmetric in b,c. The inverse therefore uses the same swap and the same sign table, and T²=I exactly.

## 3. Literal native inversion

Use the already admitted head-only native orientations

    N0(a)=[[a,0],[I,a]],
    N2(a)=[[a,-a²],[0,a]].                                  (3)

The square cross in N2 is essential: one N2 path can contain two rank-one head factors. Treating every native path as one head factor would be incorrect.

Write D_lambda=diag(lambda I,I), E_lambda=diag(I,lambda I), and T2=diag(t,t). For either s=0 or s=2,

    N_s(lambda a)=D_lambda N_s(a) E_lambda,
    N_s(a^-1)=T2^-1 D_lambda N_s(a) E_lambda T2.              (4)

The first formula has the off-diagonal factor lambda² in orientation2, as required. If J2 swaps the two bank roles, direct multiplication gives

    N0(a)^-1=J2 N2(a^-1) J2,
    N2(a)^-1=J2 N0(a^-1) J2.                               (5)

Combining (4) and (5) realizes the exact inverse head native with one native of the opposite orientation and actual ordinary wrappers. No Gaussian query, erased input, clean auxiliary owner, or new independent bank is introduced.

## 4. Complete local invoice and body distinction

The one native still pays its original ADD and its source boundary monomial services. Its Gaussian profile remains [1]+[7]+[8]. An explicit, uncompressed additional wrapper invoice is:

* four three-bit monomial services t or t^-1, one on each of two roles before and after the native;
* two unit scalar multiplications by lambda=(-i)^V;
* two swaps of the two bank roles.

Each t service can be lowered as one coordinate SWAP and one fixed sign-table pass. Alternatively each lambda can be fused into an adjacent fixed three-bit table by multiplying its one-column entries by -i; the four tensor monomial services then implement both width scalars exactly. This fusion removes separate scalar passes, not their phase or their coefficient cost. All constants and movement services remain in the ordinary/compiler invoice.

Equations (3)--(5) concern the head matrix. The physical native also delivers a fresh rank-seven body F, acting on its active roles. The wrapped source therefore realizes **F times the inverse head**, which is the useful forward-body primitive for a fresh-body caller. It does not automatically cancel or invert a previously paid body. If a literal inverse of the full F times N_s(a) source is needed, use F^-1=X_body F, where X_body is the translation on all seven Gaussian body coordinates, on each active role. Those two extra body monomial services must be paid, and any resulting body cancellation must be reflected in the endpoint invoice. No body is counted twice or silently retained after cancellation.

The fixed-table bridge requires the fixed three-bit source and its inverse recipe before the unbounded width/input scale. It supplies the same retained eventual O(volume*((f_width log p)^tau+1)) monomial tariff, with constants and dirty-work restoration charged as in that bridge. It is not a growing arbitrary table lookup. Precision, layout, native admission, recursive supplier admission, and all five global foundations remain separate obligations.

## 5. Verification and implication

The attached exact dyadic Gaussian-integer checker verifies all four one-column witnesses, full tensor widths1 and2, both native inverse identities, every scalar phase sector, the input-indexed tables, and negative controls dropping lambda or deleting the sign gauge Z. It checks algebra, not an end-to-end multiplication certificate.

This expands the admitted ordinary wrapper grammar to actual backwards head natives. A caller using it still needs an exact independent Gaussian endpoint and a positive complete invoice. In particular inversion closure alone proves no new supplier saving. The separate non-Clifford two-native obstruction explains why three native calls remain the next relevant no-query inventory in this fixed tensor interface.

Credit @CubeJerry; the retained native, tensor-separation, and compiler contributors; the nonlinear Boolean source family developed in this session; Worker B with substantial OpenAI assistance. All claims are subject to independent review.
