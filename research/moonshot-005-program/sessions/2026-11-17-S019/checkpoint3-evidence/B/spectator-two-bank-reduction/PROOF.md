# An exact two-bank reduction with the Gaussian1 job already isolated

**A source-compatible algebraic construction and a universal restricted-catalogue gate. Independent review pending. No full421 caller and no new κ.**

The spectator-swap bridge supplies ordinary kernels for both K and Ka. The first interface can be simplified further: only its active top bank needs the spectator projector. A fixed C and a prescribed completion of any ordinary two-bank R isolate a complete Gaussian1 job. The unresolved part is one exact two-bank transformation problem.

## 1. Universal noncommutative identity

Let a be any invertible operator on a D-dimensional field, let T be any ordinary idempotent, and put N=I-T. In this section no source transport identity or commutativity between a and T is assumed. Retain

    L=[[a,0,0],[I,a,0],[0,0,I]],
    U=[[a,-a²,0],[0,a,0],[0,0,I]],
    L2=[[a,0],[I,a]].

Define actual ordinary units

    C_T=[[T,N,0],[0,I,I],[N,T,0]],
    Y=[[I,0,0],[0,I,I],[0,0,I]].                     (1)

C_T routes the first two inputs through the involution [[T,N],[N,T]] into output banks0,2, and places their second input plus the original third input in bank1. Its inverse is

    C_T^-1=[[T,0,N],[N,0,T],[-N,I,-T]].              (2)

For any ordinary two-bank unit R=(rij), define

    Q_R=[[r00,r01,0],[r10,r11,0],
         [-r00-r10,-r01-r11,I]].                    (3)

This is an ordinary unit: Q_R=F diag(R,I), with

    F=[[I,0,0],[0,I,0],[-I,-I,I]],
    F^-1=[[I,0,0],[0,I,0],[I,I,I]].

Thus its inverse is exactly diag(R^-1,I) F^-1. No algebraic or physical inverse has been omitted.

Set

    B_T=[[a T a, -a T a²+a N a],
         [N a,   -N a²+T a]],
    E_R=B_T R L2.                                  (4)

Then the exact noncommutative identity is

    Y L C_T U Q_R L
       =[[E_R00,E_R01,0],
          [0,0,a],
          [E_R10,E_R11,0]].                         (5)

**Proof.** Direct block multiplication gives

    Y L C_T U
       =[[B_T00,B_T01,0],
          [a,a,a],
          [B_T10,B_T11,0]].

The middle row of its product with Q_R is `(0,0,a)` because the three block rows of Q_R sum to `(0,0,I)`. The other rows become `(B_T R,0)`. Right multiplication by L acts as L2 on their first two input columns and fixes the third. This proves(5) without moving a past T or any rij. The checker also expands both sides as exact noncommutative polynomials in six independent symbols a,t,r00,r01,r10,r11. ∎

B_T itself is invertible, with the exact factorization

    B_T=diag(a,I) [[T,N],[N,T]] diag(a,a) [[I,-a],[0,I]].  (6)

Its inverse is obtained by reversing these four factors and inverting each. Thus a candidate singular R cannot be admitted merely because its output class equations look favorable.

## 2. Exact consequence for the complex supplier

Now take the pinned four-bit source a=A^tensor V and the collective spectator projector

    Ts=SWAP_cd,
    T=(I+Ts^tensor V)/2,  N=(I-Ts^tensor V)/2,
    D=16^V.

The previously verified identities give

    a^-1 Ts^tensor V a=S_ad^tensor V,
    a^-2 Ts^tensor V a²=S_ab^tensor V.

Write R1plus/minus=(I±S_ad^tensor V)/2 and R2plus/minus=(I±S_ab^tensor V)/2. Then(4) can be written

    B_T=[[a² R1plus, -a³ R2plus+a² R1minus],
         [a R1minus, -a² R2minus+a R1plus]].         (7)

The new first two C entries are simply C00=T,C10=0. Their source column is `(a T a,0,0)^T`, of rank `(D+8^V)/2`, with ordinary right kernels R1minus and R2minus before and after the extra a. The aligned four-source component remains

    -a T a³=-(a⁴+B2)/2,
    B2=A³ SWAP_ab A lifted collectively,             (8)

so its rank4 and rank2 pieces are each full rankD. There is no F/J split in this reduced first interface.

A uniform construction of R, with its actual ordinary inverse and complete bill, that makes E_R have independent Gaussian(4,2) endpoints therefore supplies independent Gaussian(4,2,1) endpoints for the ORIGINAL three-native L C U Q L word. Indeed apply(5), exchange output banks1,2, and extend the two-bank endpoint interfaces by the identity on the third bank. The third job is the actual source a, not an omitted or hypothetical Gaussian1 map.

This is a sufficient constructive reduction. It does not assert that E_R already has those two endpoints, that arbitrary algebraic R can be implemented at the required price, or that all possible421 callers are of this form.

## 3. A necessary rank-changing coefficient channel

The lower output bank of E_R has no rank4 term: every one of its literal words has at most three source factors. Therefore, if E_R has independent Gaussian(4,2) endpoints, that lower row must contain only rank2 components. In particular its rank3 component vanishes.

Suppose both second-row entries r10,r11 of R lie in a fixed finite coefficient catalogue such that EVERY literal monomial g in that catalogue makes A² g A exact Gaussian rank3. The first-row entries may be arbitrary ordinary.

The only possible rank3 terms in the two lower output blocks are respectively

    -N a² r10 a,
    -N a² r11 a.                                    (9)

All other terms have at most two source factors. Under the stated catalogue hypothesis, each expression in(9) is pure rank3, since ordinary N preserves that class. Vanishing therefore gives

    N a² r10=N a² r11=0.

By N a²=a² R2minus, this is

    R2minus r10=R2minus r11=0.                       (10)

But R2minus is nonzero: its exact rank is `(D-8^V)/2` at every positive width. Hence the nonzero row `(0,R2minus)` annihilates R, contradicting its invertibility. This is a universal fixed-catalogue obstruction, not a failed finite search.

A successful R must therefore use second-row coefficient words outside this uniformly rank3 class. It need not come from a particular historically named group or a particular inverse coset. A useful explicit outside channel is

    g0=R2^-1,    g1=R2^-1 D_b,

where R2 is the pinned source square monomial gauge and D_b multiplies basis vectors by i^b. The exact sources A²g0A and A²g1A have Gaussian ranks1 and2 respectively, with full monomial gauges emitted by the checker. Thus the gate's scope is sharp at the source level. These controls are not a completed R, and a rank1 term would itself require cancellation before an independent(4,2) endpoint could be admitted.

## 4. Actual fixed words and retained costs

The primitive convention remains the retained ADD/SCALE/MONO convention on the same three arbitrary banks. No new owner, zero bank, borrowed contents, or free restoration is introduced.

C_T has an explicit word: add bank1 into bank2, exchange banks1,2, then apply the controlled route R02^-(Ts). Its inverse reverses these operations with an actual subtraction. The verified costs are8 ADD,7 SCALE,1 MONO forward and8 ADD,9 SCALE,1 MONO inverse. Ts is a literal coordinate swap.

Q_R is the actual R word on banks0,1 followed by F. F uses2 ADD and2 SCALE; F^-1 uses2 ADD. Y uses1 ADD and its inverse1 ADD plus2 SCALE. The final bank1/bank2 exchange has an explicit3 ADD,3 SCALE word and inverse. Endpoint normalization and the unknown R/R^-1 remain separate charged obligations. Prefix bounds and omitted-ADD controls are recorded in the verification output.

The three-native optimistic Gaussian invoice remains `3[1]+6[7]+3[8]` against `[25]+[23]+[22]`. This reduction changes no selected certificate or supplier price. Every remaining source, compiler, owner, precision, tape and recursive expense stays in the complete target theorem.

## 5. The next precise obligation

Find a uniform actual ordinary two-bank unit R and ordinary endpoint units U,V such that

    U B_T R L2 V = diag(G4,G2),                      (11)

where G4,G2 are the retained normalized Gaussian heads, with all literal monomial gauges and exterior scales recorded, and prove their full costs and inverses. The second row of R must use the rank-changing coefficient channel identified in Section3. The noncommuting ordinary projectors R1± and R2± now describe the two kernel contracts exactly.

Finite exact-word filters and modular matrix ranks, if run, are discovery tools only. No finite-width success or failure substitutes for(11), its uniform endpoint interfaces, or its bill.

Credit @CubeJerry, the retained literal source and S018 native/coset work, S019 complex construction and independent review, and substantial OpenAI assistance. All five foundational assumptions remain.
