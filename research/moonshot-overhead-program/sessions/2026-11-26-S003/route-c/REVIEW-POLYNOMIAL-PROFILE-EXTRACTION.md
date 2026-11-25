# Independent Route C review of the complete polynomial profile

Decision: **accepted as a complete written theorem in the stated tape model**, with the dependency boundaries and scope qualifications below. This accepts PP1–PP8 in `lead/polynomial-profile-extraction.md`; it does not certify an implemented full multiplier, a kernel-checked proof, human refereeing, or priority.

The reviewed statement is

\[
T(n)=O\!\left(n\sqrt{L(n)}\,
2^{O(s(n)^{3/4}(\log_2(s(n)+2))^{1/4})}\right),
\qquad L(n)=1+\log_2n,\quad s(n)=\log_2L(n),
\]

for exact full-product multiplication on one fixed deterministic finite-alphabet multitape machine, with head movement charged and one absolute O(n) bound on all cells ever visited. The proof uses the stated pinned OpenAI source results and explicit S002/S003 replacements. It introduces no additional finite-representation hypothesis.

## 1. Review basis and the two interfaces

I read the complete PP draft and checker, the actual pinned source `permutations.tex` and relevant `integers.tex` shape, precision and assembly sections, and the normalization proof in Fourier `binary.tex`. I also read CW completely and the lead's separate CW review. Earlier independent C reviews accepted B1's masked module rotations, B2/B3's explicit endpoint and shared-call composition, PB's packed leading rows, the nested label obstruction, and both local and concurrent E002 repair/affine components. These prior reviews are supporting records; the global deductions below were checked independently.

The source pin is `openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`; the predecessor programme pin is `0607d044d1d09489580da0e5828588820e1a6775`. This acceptance concerns the S003 compact route. It does not assume that the preceding expanded matrix/table constructor had polynomial cost.

The exact characteristic-two construction is an address-permutation processor. It receives encoded numerical bits as arbitrary independent data. The rational Walsh construction evaluates rational/complex numerical operations on those records. Normalized numerical coefficients are not interpreted in characteristic two. This separation is maintained through the call and precision arguments.

## 2. Complete call margin with the new endpoint constant

For clarity, the coarse old dimension in PP is

    D_old = 2+(2d-1)q^(2d-1),
    Dg = 2D_old.

It need not equal the minimal rank of the rational Gram matrix. The coarse quantity is the one used by the explicit hyperbolic realization and by the preceding upper bound. A lower bound for the exact quotient dimension is not substituted into this invoice.

Let J=2^h, h>=2, and let d be the least power of two at least100J. Then d=128J, and the weaker interval100J<=d<200J suffices. Put x=log₂m and x0=2^60 J³h. The prescribed m=2^u+1, with u the next power of two at or above x0, obeys

    x0 <= u < x <= u+1 <=2x0+1.

The occupancy bound mr*/N<=1 and the new Cg=2^20 give

    Rpen <=2^22 D_old(1+lambda).

Together with Dp<=24sqrt(m) and4^(-ceil(x/4))<=m^(-1/2), this bounds8DpRpen+3m4^(-ceil(x/4)) by2^31sqrt(m)D_old(1+lambda). Consequently2Qm+2(Dg-2) is below2^33sqrt(m)D_old(1+lambda). PP's additive40 in its logarithmic estimate therefore safely includes the endpoint inflation, doubled dimension, direct leaves, padding and occupied-reserve terms.

The inherited label upper bound is

    log₂[D_old(1+lambda)] <=3x/d+10d²log₂(4x).

At x0, log₂(4x0)=62+3h+log₂h<=40h for h>=2. Moreover log₂(4x)/x decreases for x>=x0. Thus the quadratic-distance term, including the stated constant slack, is less than x/(4J), since

    400002 J² log₂(4x0)
      <=16000080 J²h <2^58 J²h=x0/(4J).

The linear term is at most0.03x/J. Adding the extra bit for the half-margin still gives less than x/(2J). Hence the complete CI4 inequality holds with eta=1/2 and rho=1/2+1/(2J). This is a margin for the full swap template, including reserve descent, rather than only for its predictor.

The auxiliary labels are polynomially bounded: log₂N<=(2d-1)²(3+x/d²)<=4x+12d²<=5x at this threshold. The coarse Gram dimension and rectangle incidence satisfy the same absolute-degree regime. The Fourier family with even v>=100J has lower loss order2x/v+vlog₂(3x)+log₂(3v)+O(1); at the same threshold its strict quarter-margin holds. The finite checker verifies a conservative integral upper majorant for this margin, including16 constant bits. No floating-point logarithm test is used to accept a candidate.

## 3. Why the compact profile has absolute polynomial exponents

The former expanded constructor had two genuine exponential objects: the full-rate module's matrices and the full spectral/address-column tables. PP does not merely rename their size. B1 represents coefficient slices by polynomially many masked grade rotations, with polynomial total grade-bit length. The matrices are never listed. SR computes the relevant shift/check table from the current comparison key. CW computes its selectors and rational repair from the actual numerical address. Neither processor enumerates all spectral tuples.

Labels, rectangles, rank factors and endpoint lists have polynomial-m sizes. B2's reserve-only maps and full endpoint maps have explicit small-dyadic factors; fixed radix3 is valid. PB stores the logarithm of the exponential batch width and exposes that batch using leading digits and scans. It does not generate a W-entry instruction list. The polynomial price for each ordinary scan, including description reads, is permitted by the claimed profile.

The recursion-node argument requires **grouped calls**, not merely polynomial normalized call volume. This requirement is met: B3 has polynomially many geometric endpoints, queries, predictor factors and finite repair roles. All module/shift rows undergoing an identical physical map remain one complete spectator prefix. They are not separate child instructions. The exponential w therefore does not multiply the recursion branching number. Distinct maps remain separate; grouping does not change their sum of volumes. With child active width at most e/m and at most m^C grouped calls, the tree has at most m^C(1+e)^C nodes, for an absolute exponent after increasing C. The same reasoning applies to CW because both its batch width and its branch count are polynomial, and its arity A is at least m.

This observation justifies the total descriptor/setup form m^C(1+k)^E with absolute E. It would be false to obtain that conclusion by counting only sigma/W while issuing one call per module coordinate. B3's physical layout and endpoint extraction specifically avoid that error.

The fixed machine reads a compact grammar and binary parameters. Field operations, short-index arithmetic, mask construction, grade rotations and description rescans all have explicit fixed algorithms. Polynomially many logical roles use repeated scans on a fixed number of physical tapes. There is no parameter-dependent alphabet or number of heads. Actual generation and retained storage are therefore bounded by m to an absolute power, rather than only being computable for every fixed m.

## 4. Numerical precision and the outer caller

CW's rational height argument is adequate: polynomial-dimensional Vandermonde inverses, integer Newton values and nonzero gaps have polynomial bit height, as do fraction-free elimination intermediates. The bounded-divisor lemma costs O(B²+pB) when the divisor has B=poly(m) bits. For p=O(k) and k>=poly(m), this costs poly(m)k per record. It does not charge long/long division as a linear-time primitive. The subsequent short-record products use the source's fixed O(k log k) multiplication algorithm and are included in every scalar gate's bill.

The actual Fourier normalization proof supplies the same2D normalized axis factors to common and free kernels. Complete spectral-conversion normalizations commute with the row map and cancel with their inverse factors. Thus the remaining rational coefficient heights do not secretly grow with the slot width f. The isolated one-bit1/sqrt(2) operation is separately prepared. This point is essential to the bounded-divisor argument.

There are polynomially many numerical operations per level and each coefficient has at most polynomial-m logarithmic magnitude. The source common-ancestor argument then bounds logarithmic error propagation by m^C(1+log(k+2)). Completed child transforms are unitary, and completed exact permutations are isometries. The internal finite-field scratch states of the permutation processor are not numerical states subject to rounding. For k above an effectively enlarged polynomial in m, the propagation bound is a fixed fraction of k. The number of rounding events and the Euclidean array factors also fit2^{O(k)} with an absolute constant. Hence the integer caller can request its fixed input-norm allowance and2^(-50k) Walsh error allowance using one absolute numerical width multiple C0k.

I checked the source packed-XOR and controlled-block proof rather than assuming its hidden constants were uniform. Its control/rank functions have fixed polynomial degrees in k. Enlarging the guard coefficient by O(log m) pays polynomial-m coefficients in offset computation and exceptional-record repair. The number of ordinary passes gains a polynomial-m factor; the degree in k stays absolute. Short blocks still have an absolute O(log k) width, and their Beneš table construction has an absolute polynomial degree. The small-width case can use direct bit operations within the same enlarged guard bill.

The source integer packing chooses b=ceil(log₂n), h=ceil(n/b), k=ceil(log₂(4h)), N=2^k. Its prime axes are found by explicit trial division on k to a fixed power, with a shape test and exact fallback; the eventual prime-interval cutoff is absolute and independent of m. CRT tables, synchronized short Fourier phases, borrowed-coordinate schedules, square roots and carries are fixed-degree calculations. The layer boundaries are unitary, so their norm allowances remain absolute. The source proof gives k=Theta(log n), Nk=Theta(n), and exact rounding to every convolution coefficient before writing the full2n-bit product. Nothing in the new interchanger changes these shapes or the exact recovery argument.

For absolute C,E, the setup work m^C(1+k)^E is below2^(k/4) above an effectively enlarged polynomial-m guard. Its storage is bounded by its work. This proves the threshold form U_J<=max(U_abs,2^{m^K}) after harmless enlargement of K and the absolute initial range. It does not require an effective numerical value of the source's eventual prime cutoff: the actual machine tests its finite shape conditions and falls back when they fail.

## 5. Visited-cell coefficients, chunking and the real schedule

The local polynomial-m space coefficient is sufficient at this stage. It is not asserted to be an absolute coefficient before wrapping. In B3, main children have at most one label's volume or the stated finite repair-leaf volume, and padding is less than two. Spectral tags are stripped before recursive converters. In CW, spatial calls and finite repair have the prescribed shrinking volumes. Depth-first execution parks only a polynomial-m multiple of the current volume; the geometric sum preserves that coefficient. Full-volume reserve descents occur after the main arrays have been released and retain only descriptors. Marked areas are reused, so this concerns all cells ever visited and does not count only simultaneous live data.

The common-cap wrapper chooses r as the least power of two at least4c. For

    n>=max(8c,4(c+d),rU),   z=ceil(n/r),

one has4c<=r<8c, r<=n, z>=U and

    cz+d<=cn/r+c+d<=n/2.

The candidate's complete digit work, including return and cleanup, fits the same marks. The retained program is generated once, not once for every chunk pair. Physical diagonal assembly adds O(nr) motion and carries; summing r² digit products gives O((a+1)cnL(n)^theta). The high accumulator counter can be charged amortized, so no unpriced log r factor multiplies every product. Operand copies, output and controller use separate fixed linear regions. The candidate cap plus those regions yields one absolute O(n) visited-cell bound.

The weighted restart scheduler is an actual fixed controller. The prefix lengths obey the displayed Kraft bound, and the number of eligible indices times their quadratic decoding/clock setup stays O(2^s) in round s. Cleanup is charged to executed work. Schoolbook fallback bounds the last round and hence controller descriptor lengths. Enumerating exponent/chunk pairs by diagonals gives the successful-attempt penalty

    O((h+k_J+1)²[1+log₂(h+k_J+1)]²),

where k_J=log₂r_J=O(log m). This is polynomial in log m, not exponential in a parameter-dependent program length. Inadmissibly large parameters are constructed only inside the timed and space-capped attempt. The wrapper therefore makes no free advice selection from the input length.

Absorbing the fixed log-power loss with theta-rho=1/(2J) costs at most C_bJ^b, because the maximum of(1+t)^b2^(-t/(2J)) has that bound. Since J<=m, this stays within an absolute polynomial-m coefficient. The additive generator, dispatch and successful schedule penalties consequently satisfy

    log₂D_J = O(log m)=O(J³log J),
    log₂L(N_J)=O(log m)+O_abs(1)=O(J³log J).

The fixed source cutoff only changes the final absolute constant.

## 6. Eligibility is proved before using the envelope

Let h>=2 be maximal with2^(4h)h<=s and J=2^h. Then

    J⁴h<=s<16J⁴(h+1),

so J=Theta((s/log(s+2))^(1/4)). The bound for the candidate threshold is C2J³h. Its ratio to s is at most C2/J, which tends to zero. Thus the candidate is eventually eligible for every sufficiently large n, even when the hidden profile constant C2 is large. Choosing a constant-scaled smaller J would also work but is unnecessary for this asymptotic argument.

Both the schedule coefficient and the exponent slack are now charged:

    log₂H(n)<=O(1)+C2J³h+s/J
             =O(s^(3/4)(log(s+2))^(1/4)).

This establishes PP1. The bounded excluded range is handled by the exact fallback. The new displayed upper-envelope scale divided by the previous displayed scale tends to zero; this comparison is not a lower bound on either machine's actual overhead. The result implies a pure s^beta exponent for every fixed beta>3/4, but it does not establish beta=3/4 without the logarithmic factor or constant overhead.

## 7. Independent replay and precise limits

I read the entire exact checker and ran an isolated copy with assertions active using `python3 -I -B`. Source SHA256:

    24768e60420037f0ec31c43c55037ac676d43c2691cfeea40ddb32bf849adae3

The replay passed255 parameter-majorant cases through h=256,2,037 dyadic profile/eligibility cases,64 common-cap cases and all3 negative controls. It never constructs the astronomical integer m. The checker and receipts are retained under `route-c/replays/polynomial-profile/`. Its deliberately restricted tests validate finite arithmetic majorants, not the source theorems, asymptotic induction or whole tape execution. The written arguments above supply those separate deductions.

The two clarity improvements requested during review were to define D_old as the coarse dimension and to identify grouped call types in the node count. Both are explained here; neither requires changing the construction or the asymptotic claim. Independent acceptance of PP concerns the written mathematical composition only. No Lean build or full multiplier execution was performed.

Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance. The OpenAI manuscripts and their credited predecessors supply the unchanged source transformations and outer caller. S002 and the three S003 routes supply the new finite and physical components; concurrent E002 work is separately credited and reviewed.
