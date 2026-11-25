# A second gate after improving geometric routing

Status: **accepted in the separate NT, JR-I and NT+ scopes after independent C and lead review**. AQ remains the unconditional frontier. This note identifies a numerical cost that must improve even if the geometric routing logarithm is removed. Its lower statement concerns a specified positive majorant, not actual runtime. See `../route-c/REVIEW-NUMERICAL-TOLL-GATE.md` and the concurrent update below: NT+ is no longer the strongest available conditional implication.

Put F(x)=(x²log₂(x+2))^(1/3), psi(y)=sqrt(y log₂(y+2)). Source and AQ dependencies are pinned in `adaptive-extraction.md`.

## 1. Arbitrary arities in the retained numerical majorant

Let x_0,...,x_r be decreasing logarithmic active widths, ending at x_r<=X for a fixed base. Choose y_i>=1 with

    0<x_i-x_(i+1)<=C y_i.                              (NT1)

Consider a positive evaluated cost certificate B_i with fixed a,b,C>0:

    B_r>=1,
    B_i>=2^(a y_i)+2^(b psi(y_i)) B_(i+1).              (NT2)

The intended certificate evaluates the retained m^K-times-routing local upper bill after dividing by sqrt(active width), even if routing is hypothetically ideal. Here y_i=log₂m_i. The binary recursive penalty is billed at its declared psi scale. NT2 defines this positive majorant: an actual template call mass need not have such a lower bound. A sharper count can leave the certificate class.

**Theorem NT.** Every such certificate has log₂B_0>=c F(x_0) for all sufficiently large x_0, where c depends only on a,b,C,X. The arities may vary arbitrarily.

**Proof.** Put Y=max_i y_i. Recursive factors are at least one, so

    log₂B_0>=aY,   log₂B_0>=b sum_i psi(y_i).           (NT3)

The ratio psi(y)/y decreases: the derivative of log(y+2)/y has the sign of y/(y+2)-ln(y+2)<0. Thus sum psi(y_i)>=(sum y_i)psi(Y)/Y. Telescoping NT1 gives sum y_i>=(x_0-X)/C>=x_0/(2C) eventually. If Y>=F(x_0), the first bound proves the assertion. Otherwise the second is at least

    (b/(2C)) x_0 sqrt(log₂(F(x_0)+2)/F(x_0))
     =(b/(2C)) F(x_0)
        sqrt(log₂(F(x_0)+2)/log₂(x_0+2)).               (NT4)

For x>=2, F(x)>=x^(2/3) and log₂(x+2)<=2log₂x. The last square root is at least1/sqrt(3). Take c=min(a,b/(2C sqrt(3))). QED.

The order is attained by this majorant: choose y=Theta(F(x)) and x_child=x-Theta(y) above a fixed base. AQ4 pays psi(y), and a sufficiently large multiple of F pays the local term. NW supplies the discrete floor/ceiling version. Thus its retained numerical majorant is2^(Theta(F(x))) even with an ideal routing oracle.

This is not a lower bound on a numerical program. It does not prove polynomially many address changes necessary, nor lower-bound the actual binary call count by a convenient upper envelope. It shows that a better geometric routing theorem inserted into this unchanged majorant cannot certify a smaller order. A local, routing or recursive-price estimate must also improve.

## 2. The independent joint-rectangle hypothesis

S004's `../../2026-11-26-S004/lead/joint-rectangle-transfer.md` defines JR: one constant c permits an exact directed rectangle partition of the k-fold inequality relation on[q]^k, q=2^t, with local load at most c^k(t+1)^c. Exact multiplicity and both endpoint loads matter; covers and fractional partitions do not suffice. JR is open. More precisely, for any fixed integer c witnessing JR, the conditional constructor below is explicit relative to c; this constant is fixed in the program, not supplied as input-length advice.

S004 proves, with x=log₂m and power-of-two distance d,

    log₂[D_g(1+lambda)]
       <=3x/d+O_c(d²+d log₂(4+x/d²)).                  (NT5)

Returned rectangle lists have polynomial-m bit length. Bounded search takes2^(m^K) time but polynomial-m workspace/retained description. Inner sides need not be Cartesian; outer rectangles remain products with disjoint nontrivial sides, the condition in S003's explicit dyadic bases. These are explicit S004 dependencies, not conclusions from its finite experiments.

Take d=Theta(x^(1/3)) within the power-of-two choices. NT5 becomes O_c(x^(2/3)); its d log(4+x/d²) term is smaller. Rank occupancy, label-size and reserve guards still hold above a fixed base.

**Conditional JR-I.** JR and the admitted S003 interfaces imply exact interchange in

    C V sqrt(1+u) 2^[C(log₂(u+2))^(2/3)],              (NT6)

with C V visited cells and a uniform actual constructor.

Fix delta=1/R after all compiler/search degrees. At native width e choose m comparable to e^delta, with delta K<=1/8. Every call has two complete native fields, so V>=3^(2e). The new search time2^(m^K)<=2^(e^(1/8)) is at most V eventually. Its polynomial workspace also fits. JR guarantees success in the bounded list space; rejected trials are paid. Rebuilding at each actual node is charged locally, not hidden in precomputation.

AI's leading/field packing, two-pass constant payload, repair and reserve ownership otherwise persist. Descriptor width stays polynomial(m). After sqrt(e) normalization, local polynomial tolls are summable, and geometric logarithmic width contraction sums(log m)^(2/3) to O((log e_root)^(2/3)). This proves NT6 conditionally. It improves interchange; Theorem NT shows why this alone is not an improved integer theorem.

## 3. A precise separate numerical routing hypothesis

Retain NW's existing normalized rational finite template at odd arity m, with A_m=Theta(m), power-of-two W_m<=m^K and

    sigma_m/W_m <= C sqrt(m) E_m,
    E_m=2^[C sqrt(log₂(m+2)log₂log₂(m+4))].             (NT7)

Its polynomial-m height, norm, ordinary scalar work and actual branching bounds remain the proved CW/NW ones. The independently meaningful new hypothesis is the following local physical execution claim.

**SN (separated numerical address bill).** One fixed processor executes each *nonrecursive* numerical template at active width a, using any completed exact interchange primitive of per-volume cost J(u) and an absolute O(V) visited-cell coefficient, with time

    C V [m^K+E_m(1+J(a))](1+log₂(k+2))^b
       +poly(m,k),                                    (NT8)

for absolute C,K,b, arbitrary independent Theta(k)-bit records and the source occupied-spectator layout. Generation, comparisons, affine/XOR operations, rewinds and returns are included. It keeps an absolute number of full payload arrays plus polynomial(m,k) scalar/descriptor data. It preserves the actual shared recursive call count and does not repeat endpoint transforms per query. Its height/norm/event bounds are the existing polynomial-m ones. The constants/degrees are uniform, with an actual finite guard/constructor.

SN separates the polynomial-m ordinary work from the address bill. It replaces NW's present polynomial-m coefficient on J(a) by E_m, not by a free address oracle. It is a statement about one finite local template with a specified address interface, not an assumption about a complete numerical transform or integer multiplier. No proof of SN is claimed. A fresh physical count or a new shared compiler is needed; replacing J(a) by J(f) without tracking its multiplicity is insufficient.

## 4. Complete conditional log-free two-thirds transfer

**Theorem NT+.** JR and SN, together with the named proved source/S003 interfaces, imply one fixed exact full-product multitape machine with

    T(n)=O(n sqrt(L(n)) 2^[O(s(n)^(2/3))]),
    all visited cells O(n),                           (NT9)

where L=1+log₂n and s=log₂L. JR and SN are the only additional hypotheses. This improves the logarithmic factor of AQ conditionally; it proves neither polynomial-s nor constant overhead.

**Proof.** JR-I supplies J(u)=sqrt(1+u)2^[C(log₂(u+2))^(2/3)]. Fix a sufficiently small delta=1/R after all numerical degrees. At active width a take m=2^j-1, where 2^j is the largest power of two not exceeding the integer R-th root of a. Above a fixed base m is within an absolute factor of a^delta. This choice stays in NW's actual minus-one family. Set f to the largest even integer at most a/A_m and pay its bounded remainder with the ordinary term of NT8.

Write x=log₂(a+2). Then log m=Theta(delta x), and x_f is at most(1-delta/2)x eventually. Normalize numerical time by V sqrt(a) and retain its fixed logarithmic k factor outside the recurrence. The ordinary term is at most C a^(delta K-1/2), summable when delta K<=1/8. NT8's address term is at most

    2^[C sqrt(x log₂(x+2))+C x^(2/3)]
       <=2^[C' x^(2/3)]                               (NT10)

above a fixed base. NT7 and f<=a/A_m bound the normalized child multiplier by2^[C sqrt(x log₂(x+2))]. Along the geometrically decreasing logarithmic widths, the sum of these square-root-log terms is O(sqrt(x_root log(x_root+2)))=o(x_root^(2/3)). The local terms and preceding multipliers therefore sum to2^[O(x_root^(2/3))]; the number of levels and terminal work are absorbed. This is the executed discrete recurrence, not a substitution into O_m notation.

Batching still telescopes: sum log m_i<=sum log A_i<=log a_0. The full power-of-two W_i product is at most a_0^K and divides the source spectator supply2^(k-a_0) eventually. No repeated padding is added. Polynomial branching gives polynomial(k) actual nodes and setup. Choosing delta also small enough for every height/norm degree bounds a path's logarithmic gain by O(k^(1/8)log k)=o(k). The computable CW majorants and source common-ancestor argument then give one fixed p=C0k numerical format, with an actual guard and exact fallback. SN's absolute local arrays, shrinking children and JR-I's absolute space give C Nk visited cells.

The source caller audit applies unchanged: fixed norm/error allowances, controlled-block and synchronized short layers, phase construction, coordinatewise products, exact convolution rounding and carries add a fixed log^4 factor and polynomial(k) setup. With Nk=Theta(n) and log₂k=s+O(1), these fit NT9. Short/rejected shapes use the same independently correct fallback; all guards succeed eventually under JR and SN. The fixed program contains the bounded JR search and local SN constructor; no nonuniform family choice, free minimization or hidden preprocessing is used. QED.

## 5. Scope, evidence and provenance

Theorem NT isolates a lower bound on a coarse positive majorant. Theorem NT+ is conditional on two concrete local/geometric improvements. Neither changes the unconditional frontier. Removing the geometric logarithm alone does not supply SN; SN alone does not supply JR. This distinction is the point of the transfer.

The accompanying exact checker passed640 irregular positive-certificate evaluations, four omitted-premise countermodels and five conditional integer shape/gain paths through122 levels. Its finite scalar/generation exponents are illustrative, and it does not enumerate a JR partition. They cannot establish either open hypothesis or the unbounded machine result. The general balancing principle is elementary and no broad novelty claim is made.

Credits: pinned OpenAI source algorithms, S003 AI/NW/CW and their independent reviews, and concurrent S004's JR hypothesis/geometric/search transfer. Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance. No full multiplier, formal-kernel validation, human refereeing or priority claim is asserted.

## 6. Concurrent stronger conditional implication

At programme commit `af5d7983` the separate S004 session admits **JR alone** implying the log-free two-thirds multiplier bound. Its proof is `../../2026-11-26-S004/route-a/joint-rectangle-two-scale-transfer.md`, Section9 JRT-U, with independent C review and lead admission. S003 lead read that complete proof, its C review and second-wave admission. This is recorded as concurrent evidence, not a fresh S003 review of every E002 physical supplier imported there.

The new observation applies JR to the binary Fourier free rectangles as well as the exact-interchange geometry. It changes the binary recursive loss from `sqrt(y log(y+2))` to `sqrt(y)`. Choosing numerical log arity of order `x^(2/3)` then pays the retained polynomial-m address coefficient and telescopes to `O(x^(2/3))`. Its returned correlated-side lists have polynomial size; search time, basis construction, rational heights and the common-space wrapper are charged in the new compatibility argument.

Theorem NT is consistent with that result because its specified recursive price changes. NT+ remains a valid alternative implication, but SN is **not necessary for every route** to the conditional log-free scale. The current strongest concrete conditional conclusion here is S004's JR-only JRT-U. SN remains an independent local compiler question and is not silently admitted by the better rectangle geometry. No version of JR has been proved in these notes.
