# Independent review of the numerical toll gate

Decision: **accepted in three distinct scopes**: Theorem NT is a proved lower bound for its specified positive majorant; JR-I is an exact-interchange implication conditional on JR; NT+ is a complete multiplier implication conditional on both JR and SN. Neither open hypothesis is proved by this review, and AQ remains the unconditional frontier.

I read the complete `lead/numerical-toll-gate.md`, the complete S004 `lead/joint-rectangle-transfer.md`, and the entire new checker. I reread the final edits making SN's supplied interchange space bound explicit and fixing a JR witness c as a program constant. AI, NW and the actual outer source caller were independently reviewed in the preceding C records.

## 1. The discrete positive-majorant theorem

For a sufficiently long nonempty chain, let Y=max y_i. NT2's positive local terms and multipliers at least one imply both

    log₂B_0>=aY,
    log₂B_0>=b sum_i psi(y_i).

The ratio psi(y)/y decreases because log₂(y+2)/y does. Therefore sum psi(y_i)>=(sum y_i)psi(Y)/Y. NT1 supplies sum y_i>=(x_0-X)/C. If Y>=F(x_0), the first bound proves the assertion. Otherwise monotonicity of the ratio gives NT4. Its displayed equality follows exactly from F(x)^3=x²log₂(x+2). For x>=2, log₂(F(x)+2)>=2log₂x/3 and log₂(x+2)<=2log₂x, so the final ratio is at least1/3 before the square root. The proposed constant is valid after the fixed initial range is excluded.

The proof permits arbitrary uneven arities, rather than only the particular NW schedule. The matching upper order follows by the same discrete decrement estimates used in NW. The retained local m^K-times-routing charge becomes2^{K log m} after normalization even under ideal square-root routing, while the retained recursive majorant uses psi(log m). This explains the balancing obstruction.

The qualification is essential: NT2 defines a positive evaluated certificate. A convenient upper estimate for a template's actual call count is not thereby an operation-count lower bound. The note states that distinction, and it allows a sharper local or recursive count to leave the certificate class. The result therefore does not prove SN impossible or show that polynomially many address changes are necessary.

## 2. JR geometry and the exponential search

I checked the actual S004 dependency rather than inferring a constructor from JR's existence. For a fixed witness c, the candidate list contains polynomially many rectangles with polynomial-length bit-vector sides. Support, exact multiplicity and both endpoint loads can be checked using polynomial workspace. A binary counter enumerates candidate lists one at a time and the same workspace is reused. Thus time2^{m^K} and polynomial-m workspace/retained description are compatible. No archive of all rejected lists is stored.

The non-Cartesian inner JR sides do fit the explicit endpoint construction. The first changed coordinate is fixed to distinct source and destination anchors; each side therefore varies in at most d-1 positions and has no internal far pair. The outer sides remain products with disjoint inner sides. Those are the hypotheses of the explicit star-basis construction. The label matrix, scalar rank bound and rational Gram form are unchanged, so occupancy and the two-pass low-rank schedule remain valid. Arbitrary covers, overlapping multiplicities or fractional decompositions would not meet this interface.

The new incidence estimate gives3x/d+O_c(d²+d log(4+x/d²)). With a power-of-two d of order x^(1/3), this is O_c(x^(2/3)). The remaining label, reserve and list-size guards are polynomial-m above a fixed base.

At a native call of width e, choose the fixed power arity only after fixing the search and compiler exponent K. If delta K<=1/8, then

    2^{m^K}<=2^{e^(1/8)}<=3^(2e)<=V

above the stated fixed guard. The last bound uses two complete native fields and does not rely on an extra spectator promise. The search is therefore an actual local O(V) charge at every call. After sqrt(e) normalization it contributes at most e^(-1/2), covered by the summable local term. Rebuilding at every node is permitted; there is no free root precomputation or missing total-node multiplier.

Its polynomial workspace is additive and fits the existing descriptor cap. Main payload still contracts, full-volume reserve calls transfer ownership after clearing, and native fields retain their radix. Geometric logarithmic-width contraction sums(log m)^(2/3) to O((log e_root)^(2/3)). Thus JR-I is valid conditional on JR. The fixed witness c determines a fixed constructor and constants; it is not advice depending on the input length.

## 3. SN is a separate, noncircular local obligation

SN specifies the physical execution of one nonrecursive numerical template, with arbitrary independent records and the source occupied-spectator layout. Its completed interchange primitive has both a per-volume time bill J and an absolute O(V) visited-space coefficient. It preserves the already counted numerical child calls, their sharing order, and the existing height/norm bounds. This is a local compiler requirement, rather than an assumed complete numerical or integer algorithm.

The dependency is acyclic: JR-I is an exact characteristic-two address processor constructed independently of SN. SN may use that completed processor while its own recursive numerical calls remain separately charged. Its proposed improvement is precisely replacing the polynomial-m coefficient on J(a) by E_m while keeping polynomial ordinary work. The actual code or proof supplying that improvement is absent and remains an open premise. Merely calling J at a shorter slot width without paying multiplicity would not establish it.

## 4. The two-hypothesis complete transfer

Under JR and SN, the fixed-power minus-one numerical arity is constructive and remains within a constant factor of a^delta. Choose delta after every ordinary-work, height and norm degree. Normalization by V sqrt(a) makes the ordinary local term at most C a^(-3/8). The address term has logarithm at most

    C sqrt(x log(x+2))+C x^(2/3)=O(x^(2/3)),

where x=log₂(a+2). The normalized child multiplier has only the first square-root-log term. Along the geometric logarithmic chain, the sum of these multiplier logarithms is O(sqrt(x_root log(x_root+2)))=o(x_root^(2/3)). Unfolding pays the local tolls, their preceding multipliers, the finite base and the number of levels within2^{O(x_root^(2/3))}. This is a valid bound for the actual discrete shape rule, not substitution into fixed-m big-O constants.

The exact batching argument persists because sum log m_i<=sum log A_i<=log a_0. The power-of-two batch product is polynomial in a_0 and divides the root spectator supply. Actual numerical branching and total ordinary setup are polynomial in k. Every remaining additive setup term fits the exponentially large numerical arrays. JR's exponential searches occur inside its already charged exact processor, so they neither add uncounted numerical nodes nor numerical rounding errors.

With delta chosen small enough, the sum of polynomial-m height/norm majorants is O(k^(1/8)log k)=o(k). The actual-chain preflight ledger is computable without all-frequency enumeration. The source common-ancestor argument then gives one absolute O(k)-bit numerical format, including coefficient preparation, coordinate rounding and the fixed boundary norm/error requests. Constant-array SN execution, shrinking numerical children and JR-I's absolute space give one C Nk visited-cell cap.

The already audited source shape, CRT, synchronized-short, phase, coordinate-product and carry routines apply unchanged. Their fixed logarithmic powers and polynomial(k) setup fit the target envelope. Exact convolution rounding and output recovery follow from the fixed error target. Guard failures and the absolute prime-shape initial range use an independently correct fallback; the proofs imply eventual acceptance. This establishes NT9 conditional on exactly the two named new hypotheses, relative to the stated proved source/S003 interfaces.

## 5. Independent replay and limits

I ran an isolated copy using `python3 -I -B`. It passed640 irregular exact certificate evaluations,4 omitted-premise controls and5 exact conditional fast-arity paths reaching122 levels. Source SHA256:

    0f958527bef56b923c18a6f138b5e7b8b21058e9f636b92f5a3dd8b4f89f81a7

Copied source and receipt are in `route-c/replays/numerical-toll-gate/`. These tests do not instantiate a JR search, construct the SN compiler, prove the unbounded theorem, or execute a full multiplier. The omitted-log-penalty and fast-descent controls correctly show why the stated certificate premises matter.

The accepted deliverables remain separate: a majorant theorem; a one-hypothesis exact supplier; and a two-hypothesis integer transfer. None promotes the conditional log-free scale to the unconditional frontier. Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance and the source, S003 and S004 credits retained in the reviewed note.
