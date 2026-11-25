# A nonstationary numerical Walsh and integer transfer

Status: **historical conditional research draft, superseded by `adaptive-extraction.md` and `ADMISSION-AQ.md`**. Its then-open uniform-payload suppliers have since been proved and reviewed. Its plus-one numerical arity is not the minus-one constructor used by the final NW/AQ proof. The text below preserves the draft reasoning and its original conditional scope.

Let g(t)=(1+t)^(2/3)(log₂(t+2))^(1/3). We derive a tape consequence from two independently testable physical interfaces. Their field/index/array statements are stronger than the current polynomial-coefficient interface; neither assumes a whole multiplication algorithm.

## 1. Exact interfaces

**AI: adaptive exact interchange.** One fixed finite-alphabet multitape processor interchanges two equal u-bit binary address fields, with arbitrary complete prefix, gap and suffix ranges and arbitrary encoded payloads, in

    C V sqrt(1+u) 2^(C g(log₂(u+2)))

actual steps and C V cells ever visited. All generation, descriptions, padding, encoding, head returns and cleanup are included. C is absolute. There is no per-level alphabet inflation. B's nonstationary characteristic-two construction aims to establish AI.

**AW: uniform numerical payload.** For every sufficiently large odd m, the S002 binary-label rational template has A_m in[2m,4m], power-of-two W_m<=m^C, and

    q_m=sigma_m/W_m
       <=sqrt(m)2^(C sqrt(log₂(m+2)log₂log₂(m+4))).    (AW1)

Its independent row identities, Newton/division repair and shared endpoint schedule are the established S002 ones. Ordinary work, descriptions, coefficient heights and logarithmic norm gain are bounded by a fixed power of m. Using AI for address changes, nonrecursive work on V bits of Theta(k)-bit numerical records is at most

    m^C V[1+sqrt(1+a)2^(C g(log₂(a+2)))](1+log₂(k+2))
       +poly(m,k),                                  (AW2)

for a=Af active bits and full address width k. Payload workspace uses at most C full-volume arrays plus poly(m,k) description/scalar workspace. Constants and degrees are absolute. Parent frames have this same coefficient; geometric children and siblings reuse marked regions. Metadata does not inflate children. A constant-array rectangle schedule must supply this stronger space clause. CW supplies the rational arithmetic and norm/height bounds.

AW2 charges polynomially many binary coordinate operations and pointwise passes. It retains the physical interchange toll omitted by the arithmetic-only growing-arity theorem. Optimized source binary labels give AW1: even distance v≈sqrt(log m/loglog m), a suitable power-of-two q, and log R_m=O(sqrt(log m loglog m)).

## 2. Explicit variable arities and actual batching

At active width a let t=floor(log₂(a+2)), z=ceil(log₂(t+2)), y=ceil((t²z)^(1/3)), computed by integer cube-root comparisons, and m=2^y+1. Above an effective fixed base,

    y=Theta(g(t)),  y<=t/2,  m=a^o(1),  A_m<=a/4.

Take f=2floor(a/(2A_m)), r=a-A_mf. Then f is even and0<=r<2A_m. Apply the template on Af bits and direct normalized butterflies on r remainder bits. At an odd root first use one direct one-bit butterfly. Remainder work is polynomial(m)V(1+log k), included in AW2. Bounded widths use the direct routine.

The next logarithmic width t' satisfies

    c y<=t-t'<=C y,                                  (AW3)

since a/(2A)<=f<=a/A and2m<=A<=4m, after increasing the base. Branch shapes use one deterministic plan; arity does not depend on input data.

For a<=c₀k/log(k+2), root leading spectators number at least2^(k/2) at large k. Since log₂W_m=O(y) and sum y=O(log(a+2)) by AW3, the product of all path batch widths is at most(a+2)^C. All W_m are powers of two, so leading spectator bits supply each batch exactly. No accumulating padding factor is needed. Shape chains/batch products have polynomial(k) construction cost and workspace, charged explicitly.

## 3. Nonstationary recurrence with the address toll

Divide time by bit volume, the fixed factor1+log(k+2), then sqrt(1+a). AW1–AW3 give the normalized bound

    F(t)<=2^(C₁y+C₂g(t))
           +2^(C₃sqrt(y log₂(y+2)))F(t'),             (AW4)

apart from separately charged polynomial(k) setup. The physical address toll remains. Choosing m≈a^delta here would introduce2^(Theta(t)); the subpower choice avoids that loss.

For large t, differentiation gives g'(t)>=c t^(-1/3)(log₂(t+2))^(1/3). Since y=Theta(t^(2/3)(log₂(t+2))^(1/3)), t'>=t/2 and AW3 holds, the mean-value bound yields

    sqrt(y log₂(y+2))<=C[g(t)-g(t')].                (AW5)

Both sides have order t^(1/3)(log₂(t+2))^(2/3), with uniform constants above a fixed base. Logarithmic recursive multipliers therefore telescope to O(g(t_root)). Each additive term, multiplied by preceding recursive factors, is at most2^(C g(t_root)). There are O(1+t_root) levels, absorbed into the same envelope. Thus

    time<=C V sqrt(1+a)2^(C g(log₂(a+2)))(1+log(k+2)), (AW6)

plus two outer position permutations. AI and packed XOR bound those by the same expression with a replaced by k and a fixed extra power of log(k+2).

## 4. Precision and setup

CW gives polynomial(m) coefficient height and logarithmic norm gain. Branching is polynomial(m). Since sum log m_i=O(log(a+2)), node count is a fixed polynomial in a. All setup is polynomial(k), because m_i=k^o(1) and algorithmic degrees are absolute.

Along a common-ancestor propagation path the logarithmic gain is at most

    C(1+log(k+2))2^(C g(log₂(k+2)))=k^o(1).          (AW7)

This is below k/100 above a fixed effective guard. Each polynomial-m coefficient algorithm also fits O(k) scalar workspace. Completed child transforms and intervening complete pieces are unitary; exact address permutations cause no numerical error. The source fault-propagation argument, including on-demand coefficient rounding, then uses an absolute p=C₀k fractional width and absolute O(k) integer width for fixed boundary norm/error exponents. Bounded-divisor preparation costs poly(m)k per coefficient, followed by the charged short product. Certified roots/phases retain fixed-degree setup.

The root has2^k records. The product of path batch widths is polynomial(k), so each numerical array retains at least2^k/poly(k) records. Polynomial(k) total setup and descriptor workspace are absorbed by this volume. Small active slots do not remove the large spectator resource.

## 5. Visited cells and complete integer consequence

AW supplies C payload arrays per frame, independent of m_i. Spatial children have volume at most V/2; finite repair has a fixed strict contraction. Depth-first parked sums form an absolute geometric series. Siblings, rectangles and phases reuse intervals. AI uses the same absolute linear-space guarantee. Section4 absorbs descriptions into these regions. The layer therefore visits O(Nk) cells with an absolute coefficient.

Pinned synchronized short transforms, controlled blocks, CRT, coordinatewise products and carries add a fixed power of log k to AW6 at a=k. Boundary norms are2^(O(k)); Section4 gives absolute precision and exact rounded convolution/product. Accepted shapes have Nk=Theta(n), k=Theta(L(n)). Since log₂k=s(n)+O(1), and log powers fit2^(O(g(s))), AI/AW imply

\[
T(n)=O\!\left(n\sqrt{L(n)}\,2^{O(s(n)^{2/3}(\log_2(s(n)+2))^{1/3})}\right),
\qquad\text{visited cells}=O(n).\tag{AW8}
\]

One fixed machine computes these integer arity/shape plans. Generation and guard checks are charged. Fixed marked regions and exact fallback cover failed shapes, short inputs and the source's absolute prime-shape exceptions. The bounds prove eventual success. With absolute payload constants, no parameter-dependent chunk compression or search penalty is needed.

AW8 remains a **conditional implication on AI and AW's unreviewed space supplier**. A recurrence alone does not establish it. If its suppliers close it improves PP's scale, but gives neither polynomial-s nor constant overhead.

Credits: pinned OpenAI sources; S002 optimized binary-label arithmetic construction with the physical address toll now restored; S003 CW and A/B uniform-payload work; Jerry Chen(@CubeJerry) and substantial ChatGPT assistance. No whole machine execution, formal refinement, human review or novelty certification is claimed.
