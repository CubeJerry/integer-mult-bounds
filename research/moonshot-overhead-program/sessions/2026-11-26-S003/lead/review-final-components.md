# Lead review of the final finite components

Status: **accepted in the scopes below**. These results do not improve the unconditional AQ envelope. The lead read each complete proof, its independent A review and the full checker, then replayed isolated copies. Sources and output receipts are in `replays/final-components/`.

## 1. Prime-power-only count compiler

C's `P-POWER-ONLY-COUNT-COMPILER.md` rewrites the digit carry so every actual sum-factor budget is a p-power. The previous carry appears twice, and the unfolded size recurrence pays that duplication. At digit i the propagated product has length `(p-1)p^i+p^i=p^(i+1)`; constructing the carry indicator first and rounding it would exceed this budget. The output digit stays at p^i. The proof uses factor lengths, not only reduced polynomial degree.

The balanced-tree recurrence sums `2^(k-i) S_i`; substitution gives one final2^k factor through the hockey-stick identity, rather than a fresh factor per level. The resulting syntax is `m^{O(1+log p)}`. This is polynomial for fixed p and is not assigned an absolute polynomial exponent when p grows. Generalized Lucas handles negative offsets through formal-series residues. No factorial at least p is inverted. The unused final carry is omitted, so the Newton top budget is at most pD.

For the sum factorization, the two graded operators act on separate tensor components over a commutative polynomial coefficient ring and commute. Every cyclic child product is a scalar, so their d-th powers are scalar on every grade. With d a p-power, Frobenius makes the d-th power of their sum `(P+Q)I`. Restricting total-grade slices gives a whole-row identity on every starting slice. Identity padding, scalar constants and tensor-extended products preserve that invariant. This removes auxiliary roots for these sum gates only; it supplies neither the spectral converter nor the complete odd-characteristic physical pipeline.

Root replay passed504 formulas,47,544 count digits,47,544 offset digits,24,924 Newton values,30,244 actual addition-budget checks,742 actual size bounds,936 recurrence majorants,96 sum cyclic products and21 formal polynomial cyclic products covering3,225 entries. Old-budget, wrong-phase and non-p-power controls rejected the intended failures. The formal coefficient tests are distinct from finite-field point evaluation. Source hash: `ff83527440f20499e75553633484edbdd348b201150504bf0f7dd982b78dff97`.

## 2. Joint star pencil and regular lift

A and B independently identify one common monomial conjugation taking the signed middle query operators to ordinary star transpositions. The lead checked that conjugation directly: the auxiliary sign is carried to the queried sign by the permutation, while reversing the auxiliary pair changes a crossed swap into an ordinary pair swap. It is a paid constant number of physical field operations, not a free identification.

B's regular lift realizes the weighted sum on one input by embedding it into m correlated row fibres. The actual star operators are linearly independent: apply them to an address with a nonzero central symbol and zero leaves. Their images are distinct basis addresses. This makes coefficient comparison legitimate without treating the operators as independent formal variables.

In the stated additive scalar-pre/post compression model, each lifted call contributes rank at most one to each star coefficient matrix. A target coefficient `b_j I_R`, or a full-rank seed-dependent diagonal coefficient, therefore requires at least R calls. Each call queries m physical fibres, giving normalized volume at least m. The matching R-call construction verifies sharpness in that restricted model. Products of lifted calls, non-scalar physical mixing and direct orbit methods remain outside it. This is an occupancy/query-volume obstruction to the proposed lift, not a runtime lower bound for the joint sum.

Root replay passed9,360 signed conjugations,5,439 cyclic conjugations,10 actual independence witnesses,2,426 partial outputs,16,982 matching independent-row outputs and16,982 varying-seed outputs. It rejected all256 one-call scalar encodings/decodings tested for m=R=2 over F2. Source hash: `9155a95b0a9b585c4ab208e049cecafc99905e24ac5ab7569bceee9df12927a7`.

## 3. Updated address conjugation receipt

The initial source-operation audit remains independently accepted by C. A's later common-conjugation addendum is the same exact identity used above. Root read the code delta and replayed the updated checker:256 kernel entries,217,872 complete address outputs and another217,872 conjugation comparisons, with the original35 controls and80 cancellation checks. These are comparisons on the same finite examples, not additional independent large cases. Updated checker hash: `a1f630dab1db53bd5755044e3477b223e1c34517e33db1cbe5002bc7c6069350`.

The checkpoint5 receipt retains its earlier source hash and remains a valid historical snapshot. The new receipt does not retroactively change that binding. No full multiplier, asymptotic tape implementation, formal-kernel build or human referee review was performed. Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance; standard Frobenius, Lucas and tensor constructions retain their established provenance.

## 4. Every-odd-characteristic order-four closure

The lead read C's complete O4.1–O4.9 proof, A's independent review, and the final checker. All units are valid for every odd prime: r²=2, i²=-1, and R²-1=-2r(r+1) exclude all zero denominators, including at p=3. Direct multiplication proves the two-phase spectral word and its inverse. The fixed-point identity convention applies to every individual factor.

The decomposition of I,C,C²,C³ leaves one shared-swap pencil with row coefficients independent of spatial address. Comparison projectors remain separate pointwise terms on the original input; they are not moved through a label-dependent layout. The complete extraction word returns the physical permutation on arbitrary occupied records and spectators, so the finite-alphabet codec applies at that boundary.

F4 shift labels are a combinatorial generator, not scalars embedded in an odd-characteristic field. Their ordinary four-valued digits have the stated mean/variance and exceptional fraction below1/32. At p=3, value3 has low digit0 and high digit1, retained by the affine projectors. The p-power compiler gives the formal factorization with its explicit factor-p length and growing-p syntax cost.

The check table uses the first |J| Vandermonde rows and inverse transpose on the lift side. The total function h(g) handles zero gaps. The lift may be nonzero outside J; the original gap is zero there, which is what correction requires. Two forward and two inverse phases each have1/16 of the raw independent-row volume. Inverse targets have their own same-price predictor with inverted exponents and C^-1=C³; coupled finite induction uses no free inverse or triple execution of F. The call invoice remains conditional on a separately priced shared-swap supplier.

Root replay passed192 all-root matrix identities over eight odd primes;251,136 physical word outputs;62,784 arbitrary two-row pencil outputs;28,600 Newton/Lucas cases;32 projectors; and6,912 corrected repair entries. Controls cover the missing base-three high digit,96 containing sets with zero gaps,288 nonzero-outside lifts and288 wrong-transpose failures. Hash: `a8fb4c5d98a1dec843294438fdf751aa9eb0ce7f520551b1ecd98272739575b8`.

Accepted as a finite algebraic closure and explicit conditional physical interface. No complete growing-p label compiler, full odd-characteristic adaptive machine, smaller global H, or absolute visited-space theorem follows from this component alone. The elementary Hadamard identities are standard; the specific application is recorded without a priority claim.


## 5. Products of joint lifted calls with restricted row mixers

The lead read B's full LP proof, C's independent review and the checker, then replayed it in isolation. A free permutation orbit has size M=(m+1)!. For a real weighted star sum A, exact second and fourth traces are M Q and M(2Q^2-sum a_j^4). Cauchy--Schwarz gives rank(A)>=M/2, rank(A-cI)>=M/3, and a constant-fraction singular-value witness. These are actual permutation matrices, not independent formal symbols.

In the specified product architecture each real row mixer is a scalar identity plus rank at most r. Telescoping a product of q joint lifted calls gives rank(O-cB^q)<=M r(q+1). Since B^2=I, the target weighted star sum on every independent row forces r(q+1)>=m/3 exactly, or >=m/12 under the stated operator-norm tolerance. Nonzero varying seed coefficients use the minimum row coefficient in that tolerance. The divided q bounds require r>=1; r=0 is impossible by the undivided inequality. Arbitrary full-rank row mixing and arbitrary intervening physical maps remain outside the theorem.

Root replay passed30,912 short words,21 weighted cases,231 scalar shifts and7 controls. Script hash: `9e760ae35d37c332a57ad7a9803b05df3745ab24055e220aaafa524c43b885de`. Accepted as a restricted architecture obstruction, not a general lower bound for physical joint delivery or integer multiplication.


## 6. Telescoping prime-ary carry and uniform formula size

The lead read the entire TPC proof, A's independent formula review, the PA recurrence and the complete new checker. Rational Vandermonde telescopes the p+1-input carry into p(p-1) products of exactly p affine factors. The intermediate binomial(X,p) terms are never reduced separately. Both final expressions have p-integral coefficients, so their formal identity reduces modulo p. Affine prefix copies cost O(p^4) formula nodes and have budget one; top sums have budget p. This supplies the actual syntax, not merely reduced total degree or a shared circuit.

The p-ary addition depth r=ceil(log_p m), with fixed-power-p local duplication costs, gives A_p^r B_p^k binom(r+k,k). Required digits satisfy k<=r for D<=m; fixed offsets cost a bounded extra level, and p<=m absorbs it into one absolute polynomial exponent. The p=3 high input digit is retained. The top length remains the least p-power at least D, at most pD. Thus the earlier binary grammar's m^{O(log p)} size is superseded by m^K for an absolute K, for3<=p<=m. This is a finite count-grammar improvement; physical maps, complete batching and common visited-space bounds still require a separate odd-characteristic construction.

Isolated root replay passed4 formal coefficient identities over p=2,3,5,7, comparing6,469 nonzero coefficients,223 digit tuples,517 actual sum budgets and8 controls. Unfolded sizes17,101,639,2169 obey8p^4. Script hash `bf0513d59c75929c4ebafd24beca5d28f7f591379c95a4fb853493d467535057`; dependency hash `ff83527440f20499e75553633484edbdd348b201150504bf0f7dd982b78dff97`. Accepted in this finite compiler scope. Standard Vandermonde/telescoping is credited without a priority claim.
