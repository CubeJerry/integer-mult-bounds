# Pentagon-cut conservation in the dihedral ordinary family

**Proved scoped theorem, pending independent admission.** Every common-body caller with pentagonal native halves, dihedral Gaussian queries and invertible ordinary encodings in C[T] conserves total head rank. Its complete Gaussian invoice fails strictly for every 0<t<1. This proof uses no H24 parity. Full ordinary Clifford maps outside C[T] remain open. **No new kappa.**

## 1. Exact family

Use B^5=I, T^2=I, TBT=B^-1 from `PROOF.md` and `DIHEDRAL-ORDINARY-INVERTER.md`. Gaussian ranks of B^k T^e are r_k=(0,1,2,2,1). Collective tensor operators faithfully represent the ten-element group algebra for every V>=2. Thus every all-width exact caller implies an identity in C[D10], retaining scalar phases.

Ordinary encodings are invertible bank matrices over C[T], allowing finite linear combinations of I and the actual ordinary inverter T. Native halves are

    N_(sigma,epsilon,c)
      = [[B^sigma, c B^(sigma+epsilon)], [0,B^sigma]],

where sigma,epsilon,c in {+1,-1}. Paid head queries are one-bank in-place calls or distinct-bank additive shears with coefficient B^k T^e, including inverses and nonzero fixed scalars. Let q1,q2 count rank-one/rank-two queries. Endpoints, up invertible ordinary encodings, are independent dihedral Gaussian jobs with total head rank H. All banks are arbitrary and retained. Other ordinary phases or non-dihedral Gaussian queries are excluded.

## 2. Two exact representations

Label five adjacent-pair cuts {j,j+1} of Z/5Z by j. Define permutation matrices

    R e_j=e_(j+1), J e_j=e_(-j-1),
    P=diag(1,-1,-1,-1,1).

R^5=I, J^2=I, JRJ=R^-1 define rho(B)=R and rho(T)=J. Set rho_0=rho and rho_1=P rho P. P selects the two cuts containing vertex zero. J preserves that set, so P commutes with J. The representations therefore agree on all of C[T].

The difference R^k-P R^k P is a permutation times a diagonal whose nonzero entries are exactly the symmetric difference of {0,4} and its k-shift. Consequently

    rank(rho_0(B^k)-rho_1(B^k))=(0,2,4,4,2)_k=2r_k.       (1)

Multiplication by J preserves this rank, so the same identity holds for B^k T^e.

## 3. Native and query ranks

Put U=rho_0(B^sigma), V=rho_1(B^sigma), E=U-V; rank(E)=2. If epsilon=-sigma, the native cross difference vanishes and its difference is diag(E,E), rank four. If epsilon=sigma, its difference is

    [[E,c(U^2-V^2)],[0,E]]=[[E,c(UE+EV)],[0,E]].

Left multiplication by [[I,-cU],[0,I]] and right multiplication by [[I,-cV],[0,I]] reduce it to diag(E,E). Thus every native has difference rank four. An in-place rank-r query or a distinct-bank shear has difference rank 2r. Nonzero scalar factors do not change rank.

A product difference telescopes; ordinary factors have zero difference. Subadditivity and ordinary outer invariance therefore give 2H<=4m+2q1+4q2, or

    H <= 2m+q1+2q2.                               (2)

All orientations, signs, query modes, finite inventories and gate orderings are covered. This is a universal proof in the declared finite algebra, not a failed-search inference.

## 4. Complete common-body invoice

Let m>=1 stages each introduce seven fresh body axes. Every one of R roles receives each body; the m(R-2) rank-seven idles are paid. For [r]=r^t, 0<t<1, put d=[8]-[7], so 0<d<1. The Gaussian price is

    P=mR[7]+(m+q1)[1]+m d+q2[2].

The target ranks are 7m+r_i, with r_i in {0,1,2} and sum r_i=H. Concavity bounds the target moment by mR[7]+dH. Hence (2) yields

    P-target >= (m+q1)(1-d)+q2([2]-2d)>0.

The first term is positive. Also d<=2^t-1 and 2(2^t-1)<2^t, so the second coefficient is positive. Ordinary gauge, layout, precision and compiler expenses cannot repair the failure.

This excludes the one-native/three-rank-one-query and three-native/one-query/four-role proposals within C[T], as well as every other common-body inventory there. It does not exclude full monomial Clifford interleavings using S, D_CZ or another ordinary outside C[T], changed body incidence, changed inputs, approximations or different sources.

## 5. Continuation, verification and credit

The explicit order-five source remains valid. Its old parity obstruction disappears, while the natural single-inverter enlargement has this different conservation law. Future construction must use a larger ordinary family than C[T] or change source/body incidence. Repeating scalar C5 or dihedral caller searches is unnecessary.

`check_pentagon_gate.py` checks all ten group elements, 100 products, both representations, all eight native orientations/signs, query modes and a sharp two-native control. Finite checks supplement the universal proof. Root review is separate.

Credit @CubeJerry, the native/compiler authors, S013 representation and common-body accounting, and S014 Worker B with substantial OpenAI assistance. All five foundations remain retained. No new kappa.
