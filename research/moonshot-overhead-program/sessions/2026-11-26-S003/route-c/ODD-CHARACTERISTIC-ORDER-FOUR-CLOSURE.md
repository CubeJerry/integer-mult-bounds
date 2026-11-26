# An order-four closure in every odd characteristic

Status: **proved finite component; exact checks passed; independently accepted by Route A** in `../route-a/review-order-four-closure.md`. This note gives an odd-characteristic counterpart of the programme's order-three closure. It is not a new complete multiplication bound. In particular it does not assign a uniform polynomial cost to the remaining odd-characteristic label compiler.

**Subsequent syntax improvement:** `TELESCOPING-PRIME-ARY-CARRY.md` replaces the binary-tree m^{O(log p)} count grammar used below by an absolute polynomial-m grammar. It preserves the order-four identities and the top length L<=pD. This does not supply the remaining complete physical address compiler or improve the admitted global multiplier bound.

## O4.1. Constant-size identities

Let p be any odd prime. In F_(p²), choose r and i with r²=2 and i²=-1. Both exist because every element of F_p is a square in F_(p²). Put

    a=i/r, H=[[1,1],[1,-1]], C=aH, E=diag(1,-1),
    Q=[[0,1],[1,0]], R=i(r+1).

Then C²=-I, C⁴=I and C E C=-Q. Define

    A=diag(-2,-2i),
    B=diag((R+1)/2,(R-1)/2),
    J=diag(R^(-1),1),
    S=A C B C J=[[1,1],[r-1,-r-1]].                   (O4-1)

The columns of S are eigenvectors of H with eigenvalues r and -r. Consequently

    T=S^(-1),  T C S=diag(i,-i),
    T=J^(-1) C^(-1) B^(-1) C^(-1) A^(-1).            (O4-2)

All diagonals are invertible in every odd characteristic. Indeed r and r±1 are nonzero, R=i(r+1) is nonzero, and

    R²-1=-2r(r+1)

is nonzero. The inverse S is explicitly

    T=(1/4)[[2+r,r],[2-r,-r]].                       (O4-3)

For direct verification of O4-1, H B H=[[R,1],[1,R]], a²=-1/2, and R(r-1)=i. Only division by units is used; characteristic three is included.

## O4.2. Physical orbits and shared pencils

For a pair of physical fields order each two-element swap orbit by its smaller/larger address. Apply the displayed 2-by-2 matrices on that orbit. At equal-field fixed points define C,Q,S,T and **each individual diagonal word factor** to be identity. This fixed-point convention is part of the construction.

Let U,L be the smaller/larger pointwise projectors, and K the equality projector. With E=U-L+K, one has on the full physical array

    C=a Q+a(U-L)+(1-a)K,
    C²=-I+2K,
    C³=-C+2K.                                       (O4-4)

Thus a pencil involving I,C_j,C_j²,C_j³ becomes one shared-swap pencil plus pointwise terms in the original layout. No comparison mask is moved through a label-dependent address change. The source's three consecutive comparison runs compute U,L,K on occupied fields with amortized tape scans.

Explicitly, for arbitrary scalar row matrices A_0,A_(j,1),A_(j,2),A_(j,3), put B_j=A_(j,1)-A_(j,3). The shared-swap portion is

    (A_0-sum_j A_(j,2)) I + sum_j a B_j Q_j.

The separately computed pointwise portion is

    sum_j a B_j (U_j-L_j)
       + [(1-a)B_j+2A_(j,2)+2A_(j,3)] K_j.           (O4-4a)

Every coefficient in the shared-swap portion is independent of physical address. A row matrix commutes with these spatial projectors. Preserve the original input while computing the two portions, then add them. This uses a constant number of payload arrays; the arithmetic/description cost of those row matrices still has to be charged.

For m disjoint pairs put F=product_j C_j. Products of the diagonal factors over j are pointwise. Operators belonging to different pairs commute, hence

    product_j S_j = A_all F B_all F J_all,
    product_j T_j = J_all^(-1) F^(-1) B_all^(-1)
                   F^(-1) A_all^(-1).               (O4-5)

Each spectral conversion therefore uses exactly two F or F^(-1) transforms and pointwise maps. Its spectral exponent k_j modulo four is 0 at equality, 1 at the smaller member, and 3 at the larger member. Define M to be -I on each nontrivial orbit and identity at equality. The physical swap also satisfies

    Q=M C E C,
    product_j Q_j=M_all F E_all F.                  (O4-6)

This extracts the desired complete physical permutation using two F transforms. Every displayed word preserves arbitrary occupied spectator fields. The identities operate on all input rows, not only a distinguished entry.

## O4.3. Compatibility with the p-power count compiler

This paragraph specifies a finite algebraic interface, without asserting an unpriced physical executor. Choose a pairwise-independent shift family beta_j(t) in Z/4Z by taking distinct projective directions in F_4^r and mapping their values bijectively to {0,1,2,3}. For every spectral tuple, each shifted exponent is uniform on these four integers and pairs are independent. The number of seeds is B=4^r=O(m); there are (4^r-1)/3 available directions.

The ordinary count c=sum_j(k_j+beta_j mod 4) has mean 3m/2 and variance 5m/4. With b=ceil(7 sqrt(m)), u=floor(3m/2-b), v=ceil(3m/2+b), the outside-window fraction is at most 5/196<1/32. Put D=v-u<=14 sqrt(m)+3. For sufficiently large m, D<=m, as required by the p-power compiler. B is divisible by 32 once r>=3.

The four spectral indicators are affine expressions in I,C_j,C_j²,C_j³, by the order-four Fourier projector formula; division by four is a unit for every odd p. For p>=5 the shifted digit is in {0,1,2,3}<p. For p=3, give the value 3 its correct two base-p digits: its high digit is its spectral indicator, not zero. Both digit expressions are affine in the same query powers, and padding the high digit to budget p is legitimate. The balanced carry proof and p-power addition budgets therefore apply without dropping a carry.

The predictor is

    P_beta=i^(u-sum_j beta_j)
        sum_(h=0)^D (i-1)^h binom(c-u,h).             (O4-7)

It equals the target multiplier z=i^(sum_j k_j) on the window, by the binomial theorem. The p-power formula factorization has L stages, where L is the least p-power at least D, so L<=pD. Its succinct grammar still costs m^{O(1+log p)}; this exponent is not replaced by an absolute constant when p grows. The independent module may be exponential, and is retained as an independent-row factor.

For F^(-1), construct a separate predictor for the query family C_j^(-1)=C_j³, replacing each k_j by -k_j modulo four. It has the same dimensions, formula budgets and physical pencil price. The simultaneous finite-depth induction uses these two target families. It does not compute the inverse by running F three times or assume an inverse implementation for free. A common unsimplified formula grammar with uniform padding supplies the same independent row factor w at every seed.

One can choose a scalar field K=F_(p^e), where e is the least positive even integer with p^e>=B. Then K contains the required roots and B distinct check nodes, and p^e<p²B. For 3<=p<=m, its bit width is O(log m), and exhaustive finite-field construction can be bounded by a fixed polynomial in m. In particular no prime-to-p roots are introduced by the sum gates. The cyclic-family and masked-grade proofs remain separate from the physical label-transfer compiler.

## O4.4. Finite repair closure and exact phase fractions

Use a Vandermonde check H_0 with s=B/32 rows and B columns, tensored with the identity on the independent factor w. Let J be the outside-window containing set and V its square Vandermonde submatrix from the first |J| check rows. Some rows in J may have zero actual gap g_beta=p_beta-z. The predictor values and z lie in F_(p²), so use the total function

    h(g)=g^(p²-2),  h(0)=0.

For nonzero g this is its inverse. The pointwise repair table uses V^(-T) diag(h(g)) V^(-1), embedded in the check coordinates. Applied to H_0(PX-zX), its transpose lift gives Z_beta=X_beta on every nonzero-gap row. Zero-gap rows need no correction, including any lying in J. The two table outputs a,za yield Z,FZ after inverse conversion and lift. Therefore

    PX-PZ+FZ=FX                                      (O4-8)

on all independent rows. No zero gap is inverted.

There are two predictor evaluations. The forward converter in O4-5 has two F^(-1) phases, and the inverse converter has two F phases. Each phase has exactly 2s w=Bw/16 rows. Thus four sequential child phases each have one sixteenth of the parent raw scalar volume, with total normalized mass 1/4. The on-demand table must occur after the complete forward word and before the inverse word. Its order cannot be shortened by commuting it through diagonal factors.

Finite unrolling to depth h ends with direct products of m individual C_j or C_j^(-1), each implemented by one copied physical swap and pointwise maps. If R_swap is the separately proved shared-swap call price per input stream, the finite algebraic call invoice is

    O(L R_swap sum_(ell=0)^(h-1)4^(-ell)+m 4^(-h)).   (O4-9)

For exact dimensions, use base batches of Bw rows and depth-h batches of Bw 16^h rows. Every one of the four phases then groups exactly 16 parent blocks into a depth-(h-1) child batch; its row volume is one sixteenth of the active parent's. This is finite full-rate batching on independent inputs, not an extra claim that a functional helper row is productive data.

The two-target extraction O4-6 changes only an absolute constant. This is a call invoice conditional on that shared physical supplier, not an uncharged tape-time estimate. Descriptor generation, endpoint preparation, row arithmetic, field encoding and absolute visited-space constants require their own compiler bounds. The generic finite-alphabet packing component supplies a constant payload inflation at completed physical-permutation boundaries; it is not a license to repack inside an unfinished F transform.

## Evidence, relation to prior work and limits

`verify_order_four_closure.py` passed 192 exact matrix identities over F_(p²), for p=3,5,7,11,13,17,19,31 and all four choices of the two square roots. It also passed 251,136 complete physical word outputs, 62,784 outputs of the general three-power pencil with arbitrary two-row coefficient matrices, and 48 omitted-phase or incorrect-fixed-point controls. Each physical array has two independent leading rows and a complete suffix spectator of length two. All equal and unequal physical field pairs are present. The result is `order-four-closure-verification.json`.

The final checker also passed 28,600 order-four count/offset/Newton evaluations, 32 actual Fourier projectors, and a control that drops the required initial high base-three digit. Its repair tests passed 6,912 corrected output entries across 96 containing sets with an internal zero-gap row. They include 288 examples with a nonzero lift outside J and 288 rejected wrong-transpose corrections. These are direct finite tests of the additional O4.3–O4.4 seams; the shift-family bound, arbitrary-depth contraction and parameter envelopes remain proved by the written arguments. The final script hash is `a8fb4c5d98a1dec843294438fdf751aa9eb0ce7f520551b1ecd98272739575b8`.

These checks test the finite matrix and physical pencil statements, not a full asymptotic machine. O4.3–O4.4 are written algebraic consequences of the explicit count and Vandermonde interfaces; their generic scalar arithmetic alone does not pay for address routing. The scalar target F is not itself a physical permutation, so the finite-alphabet codec applies after the complete O4-6 word, and not at an arbitrary intermediate factor.

Sources and credits: the source odd-characteristic swap geometry and comparison scans in OpenAI math's November 24 tape `build/interchange.tex` at pin `3344da59991ed94f9ba711217b29c1d760badfa6`; the predecessor characteristic-two order-three closure and its four-phase finite contraction; S003's p-power count compiler and finite-alphabet packing. The elementary Hadamard/eigenvector identities are standard linear algebra. The explicit every-odd-characteristic word, fixed-point convention and retained shared-swap coefficient were developed for Jerry Chen (@CubeJerry) with substantial ChatGPT assistance. No exhaustive novelty search, human-referee verification or formal-kernel proof is claimed.
