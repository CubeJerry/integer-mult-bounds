# On-demand spectral repair without an exponential table

Status: proposed source-specific component; independent review pending. This is not a complete multiplier bound.

Sources: OpenAI math@3344da59991ed94f9ba711217b29c1d760badfa6, tape build/interchange.tex, subsec:swap-spectrum, and Fourier build/repair.tex. Programme predecessors: S002 routes/A/characteristic-two-count-formula.md, routes/A/power-two-degree-predictor.md, routes/B/structured-shift-check-refinement.md, routes/B/characteristic-two-order-three-interchange.md (O3-6a).

The component replaces the literal list of all 3^m spectral cases by a polynomial computation from current spectral labels. The paid forward and inverse conversion words remain.

## 1. Closed all-count predictor formula

For m>=4096 let B=3^r be the pairwise shift count, where r is least with (3^r-1)/2>=m. Then 2m+1<=B<6m+3. Select the m projective normals explicitly to include a basis. Set b=5 ceil(sqrt m), choose T=2^t minimally with T>=2b+1, D=T-1 and u=m-floor(D/2). For k in {0,1,2}^m write

    c_beta = sum_j ((k_j+beta_j) mod 3),
    z = omega^(sum_j k_j),       omega^2+omega+1=0 over F2.

Use the polynomial-coordinate field E=F_(4^e), e=ceil(log_4 B). Its bounded constructor is polynomial in B. Let v be the arbitrary independent module width.

**Lemma SR1.** At every spectral tuple, including negative c_beta-u, the power-two-window predictor is

    p_beta = omega^(u-sum_j beta_j + ((c_beta-u) mod T)).       (SR1)

The residue is least nonnegative.

**Proof.** In F2[[X]], (1+X)^T=1+X^T. Every positive or negative integer power of this series equals 1 modulo X^T. For any integer a=qT+r, 0<=r<T, the degree-<T truncation of (1+X)^a is exactly the finite polynomial (1+X)^r. Evaluate at X=omega-1 and multiply by the retained phase. The predecessor's count-bit formulas compute those same truncated coefficients. This evaluates a finite polynomial, not an infinite series. QED.

For q=floor((c_beta-u)/T),

    p_beta/z = omega^(-T q).                                 (SR2)

Indeed c_beta-sum beta_j-sum k_j is divisible by three. The actual defect condition is therefore q nonzero modulo three. The containing set J={beta: c_beta outside [u,u+D]} can include zero-gap rows. The repair below never divides by those gaps.

Enumeration of B=O(m) seeds and m dot products on O(log m) ternary digits, the counts and powers in SR1 takes m^{O(1)} actual bit operations and cells. All integers have O(log m) bits. There is no 3^m table access.

## 2. A computed small check-space map

Put s=floor(B/32) and use the s-by-B Vandermonde matrix

    H_(i,beta)=alpha_beta^i,       0<=i<s,

on distinct nodes of E. Pairwise independence gives variance 2m/3 and outside-window fraction at most 2/75. For B>=219 this implies |J|<=s. Take v=32w, where w is the predictor module width, so R=Bv and S=R/32 are integers. The active check map is H tensor I_v, with s*v rows. Append S-s*v zero rows to reach exactly S checks. These are paid internal coordinates, not independent parent inputs. The correction map ignores these added input coordinates and returns zero in its added outputs. Consequently each forward/inverse phase has exactly 2S=R/16 rows, including the padding.

Put ell=|J|, with J in fixed seed order. Let V_J be the first ell rows of H restricted to J. Its determinant is a product of distinct-node differences, so it is invertible. For ell=0 all correction maps are zero, with no inverse computation. Given a=H Xhat and b=H P Xhat, compute

    delta = (b-z a)_[0:ell],
    e_J = V_J^(-1) delta,
    w = diag((p_beta-z)^2 : beta in J) e_J,
    y_[0:ell] = (V_J^T)^(-1) w,    y_[ell:s]=0.                (SR3)

The small spectral map sends (a,b) to (y,z y).

**Lemma SR2.** With Zhat=H^T y, on all B arbitrary independent input rows,

    P Xhat + P Zhat + z Zhat = z Xhat.                        (SR4)

Tensoring all maps with I_v preserves the identity on every independent module coordinate.

**Proof.** The errors are supported in J, so the first inverse recovers e_beta=(p_beta-z)Xhat_beta there. The transpose inverse ensures Zhat_J=w. A nonzero gap belongs to F4* and has cube one; hence Zhat_beta=(p_beta-z)^3 Xhat_beta=Xhat_beta. A zero gap needs no correction. In characteristic two the output error in SR4 is (p_beta-z)(Xhat_beta+Zhat_beta), which vanishes. The proof is coordinatewise and uses no zero-initialization of independent input rows. QED.

The transpose inverse is essential. Writing a sparse error into all B spectral rows and converting them back would lose the small phase bill.

**Lemma SR3.** From k,a,b one fixed finite-tape program evaluates SR3 in m^{O(1)} actual bit operations and visited cells, or constructs the whole small matrix of its action within that bound.

**Proof.** B,s=O(m), and a field element has O(log m) bits. Schoolbook polynomial field arithmetic and exponentiation to invert a nonzero element take polynomial bit work. Construct the Vandermonde entries and use deterministic Gaussian elimination with tested pivots and charged row swaps. Even scanning the whole polynomial-size stored array on every access leaves a fixed polynomial-in-m tape bound. The determinant proves termination. SR1 supplies all gaps in polynomial work. No random-access or unit-cost field model is assumed. QED.

## 3. The physical streaming boundary

**Proposition SR4.** Suppose the source converters return aligned rows in physical address order, with k_j the equality/smaller/larger label of the jth pair as in the order-three construction. The nonconversion work of this structured repair component uses m^{O(1)} V actual tape steps and m^{O(1)} V visited cells on encoded bit volume V. The proportional factor is independent of 3^m and of the module width v.

**Proof.** Generate the m comparison masks with the source's actual scan construction. For one earlier field value, the later field and suffix split into three consecutive runs. Their length arithmetic is paid by the complete fibre. Prefix spectators advance by amortized counters, rather than being reread per symbol. Appending all m labels to each encoded data record takes polynomially many full scans and adds O(m) bits per record.

There are only B=O(m) shift roles. Each contains the same module and physical-address order. Extract and merge one role at a time. To compute an output role, scan each input role, compute its coefficient from the attached labels using SR3, and accumulate into an aligned output stream. O(B^2) scans suffice for H, H^T and the small spectral map. Recomputing the entire small coefficient matrix per record is a safe overcount and remains polynomial in m. Tensoring with I_v means no module-index permutation or lookup is needed.

Source copies, masks, accumulators and scalar work arrays occupy reused marked intervals of polynomial-in-m volume. Forward conversion of (HPX,HX) and inverse conversion of (y,zy) remain the separately paid source phases. The predecessor's padding still makes each phase R/16 rows and the four-child mass 1/4. This component changes no recursive pencil or conversion counts. QED.

A different row layout needs its own conversion bill. The proposition uses the specified aligned-row and comparison-mask interface; it does not claim an arbitrary succinct diagonalizer is physically cheap.

## 4. Consequence and open next questions

The number of spectral cases need not multiply the execution or space cost of structured F4 repair. Still separate: predictor module-index movement, rational endpoint maps, radix/batch padding, numerical Walsh arithmetic and precision, and common visited-space uniformization. No new complete bound follows from this component alone.

Next establish and combine the actual succinct-factor executor, small-radix batching and numerical branch, keeping each interface and all costs explicit. Finite checks support the identities; the proof, not those checks, establishes the universal statement.

Credit: Jerry Chen (@CubeJerry), the cited OpenAI manuscripts and S002/E001 predecessors, and substantial ChatGPT assistance. No human referee verification, Lean build or full multiplier execution is claimed.

## 5. Finite verification

The exact checker verify_spectral_repair.py passed 2,310 signed truncation identities, 6,930 phase cases and 23,664 full-basis small repair identities over F16. It included 1,020 containing sets with zero gaps. Negative controls detected 2,766 wrong-transpose failures, 2,328 missing-gap-square failures and all 96 chosen gaps outside F4. Full-basis checks certify those finite linear maps for arbitrary field inputs, not the universal family. The JSON receipt records the field and scope. No physical machine or asymptotic theorem was checked by execution.
