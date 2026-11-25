# Lead review of the adaptive invoice and common-preparation obstructions

Decision: **accepted in their stated restricted scopes**. These are mathematical obstructions to specified certificates or geometric preparations. They do not lower-bound actual interchange time or integer-multiplication time.

## 1. Convergent A/C invoice proofs

I read A's `nonstationary-invoice-barrier.md`, C's `NONSTATIONARY-LITERAL-INVOICE-BARRIER.md`, and B's independent application review. They import A's previously reviewed exact nested-label theorem N. Their claims concern its actual rational Gram rank, actual rank fraction (or a proved lower witness), and prescribed directed product rectangles. They do not assume that the source upper invoice is an operation-count lower bound.

A's inversion is sound. For x=log₂m>=4096 and J=(1024x/log₂x)^(1/3), J>=64, and the theorem-N consequence x>=J³log₂J/128 contradicts log₂J>=log₂x/6. The displayed1/16 large-range coefficient and1/128 uniform coefficient both have slack. The bounded range is covered by the explicit D>=23, lambda>=27. C's independent split at b=x^(3/4) gives a weaker uniform constant but covers m>=2. Neither argument requires a rank-occupancy upper bound.

For g(x)=(x²log₂(x+2))^(1/3), I independently differentiated with natural L=ln(x+2). The numerator of g''/g after multiplying by9x²(x+2)²L² is

    -2[(x+2)L-x]²-3x²L,

which is strictly negative. This expands to C's quadratic expression. Thus global concavity, continuity at zero and sum g(x_i)>=g(sum x_i) follow. A's separate decreasing-ratio proof is also valid and suffices for the accumulation result.

The normalization restriction is essential. The actual AI split has ell<=e/4, A=m+2a<=3m, and e/A>=4 above a fixed base, hence f>=e/(6m). The declared predictor budget Dp=T-1 is at least2b>=sqrt(m), and the retained term8DpRpen pays more than the square-root normalization constant. Consequently the normalized positive invoice retains the geometric I(m) factor. C's theorem applies. A's slightly looser factor8 split also applies and supplies its explicit terminal factor.

The fast descent f=e/m² is a correct countermodel to the weaker inference from logarithmic width drop alone. It need not be implementable; its role is to show why that weaker set of numerical hypotheses cannot imply the claimed normalized product. Both notes maintain this distinction.

These are two corroborating proofs of one consequence: within the retained literal positive invoice and regular split, arbitrary varying arities, unequal distances and additional nesting cannot improve the order2^(Theta(g(log e))) of that certificate. This does not certify optimality of the implemented algorithm, a tape lower bound, or a universal2/3 multiplication barrier.

## 2. B's common isotropic preparation counterexample

I read `common-isotropic-preparation-obstruction.md`, its checker and B2.7 in `explicit-dyadic-geometry.md`. The exact endpoint difference is g_a=-z_l-z_k(a), matching B2.7's -2z minus its two anchor-feature sums. The constructed inner words differ in exactly d positions. Therefore the outer far-count between k(a),k(b) equals their tuple Hamming distance. Expanding all four pairings gives

    <g_a,g_b>=-4 dist(a,b)/d,

including zero when a=b. Distinct vectors cannot belong to one totally isotropic rational subspace. Because d is a power of two, reduction modulo3^f with3^f>d preserves every nonzero pairing. The data field's characteristic two is not substituted into the rational address geometry.

For the high-half subfamily, the source subsets really are identical members of the prescribed first-differing-bit rectangles: the frozen first source letter is zero, the other d-1 differing source letters lie in the low half, and all unchanged coordinates are zero. Each chosen destination anchor lies in its corresponding high-half target subset. Thus the(q/2)^d same-source obstruction follows and does not merely compare unrelated source arrays.

The generic per-query conversion count also checks algebraically. An inner rectangle has q^(h-d) choices for equal coordinates, q(q-1) for its distinguished ordered unequal pair, and[2(q-1)]^(d-1) choices for the other prefix rectangles. With h=2d-1 this is exactly binom(h,d)2^(d-1)q^d(q-1)^d. Its normalized outer count is at least one, so repeating a conversion for every query incurs at least m normalized calls. That particular replacement cannot supply a sqrt(m) subexponential invoice.

The conclusion only defeats a single common totally isotropic late-reserve preparation, or the specified independent per-query repair. Nonisotropic layouts, prefix sharing, aggregate identities and different labels remain outside it. It does not establish that distinct isotropic spaces force equally many expensive physical passes.

## 3. Evidence

The lead isolated replays are under `lead/replays/adaptive/invoice-a/`, `invoice-c/`, and `isotropic/`. Their receipt files contain exact copied-source hashes, commands, exit codes and output. A's invoice witnesses are exact rational values with90-digit Decimal logarithmic comparisons; C's discriminants, cubic cases and normalization cases are exact, while its partition diagnostics use100-digit Decimal arithmetic. B's sparse Gram pairings are exact rational/modular calculations. Decimal diagnostics are not interval-certified asymptotic proofs. The written algebra and calculus establish the unbounded statements.

Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance. A/C convergence, B's independent application audit and B's protected failed sharing construction retain their separate provenance. No full tape run, Lean build or human referee certification is claimed.
