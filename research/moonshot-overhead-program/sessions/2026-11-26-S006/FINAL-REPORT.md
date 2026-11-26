# S006 research report

**The complete multiplication envelope is unchanged.** Let $L=1+\log_2 n$, $x=\log_2 L$ and $\Phi(x)=(x^2\log_2(x+2))^{1/3}$. The [assembled contribution](../../contributions/explicit-overhead/README.md) gives one deterministic machine with a fixed finite alphabet, fixed tapes and one head per tape. For every pair of unsigned $n$-bit inputs it writes their exact $2n$-bit product contiguously in the prescribed order. Its worst-case cost is
$$
 T(n)=O(n\sqrt L\,H(n)),\qquad
 H(n)=2^{O(\Phi(x))},\qquad
 \mathrm{space}(n)=O(n)
$$
where space counts all tape cells visited through halt. Thus $G=\log_2 H=O(\Phi(x))$ and the excess logarithmic exponent $\delta=G/x=O((\log_2(x+2)/x)^{1/3})$ asymptotically. The full result is the independently reconstructed S003 written proof. E002 and E003 give same-order constructions. Human refereeing and a formal refinement of the complete machine are open. OpenAI’s theorem gives an unspecified vanishing excess. Literature priority for this explicit envelope remains unestablished.

## What changed in the full proof

| Dependency | Result admitted in S006 |
|---|---|
| Short cyclic axes | An elementary combinatorial sieve certifies the released downward gcd search with its original $20\lceil\log_2 k\rceil$ widths and at least half the padded volume. The explicit eventual cutoff $k\ge2^{2^{100}}$ applies to this search. It replaces the use of the short-interval-prime or quadratic Jacobsthal theorem at this one edge. [Proof](../../contributions/explicit-overhead/coprime-axes.md) |
| Interchange and outer arithmetic | The sum of main and reserve child potentials is at most a quarter of the parent potential after fixing one absolute constant. Full-volume calls reuse their marks and parking contracted payloads gives a geometric space bound. Fixed Toom-3 covers all outer full-width products in $o(Nk^{3/2})$ for $N=2^k$. [Head schedule](../../contributions/explicit-overhead/AQ-P.md) · [Arithmetic review](review-axes-and-arithmetic.md) |
| Adaptive Walsh core | The rational instructions specialize exactly to a common composite modulus. Every source denominator, including actual Newton gaps, has support in its construction. One centered lift recovers the signed Walsh sum under the bank magnitude bound; normalized output is rounded once. This removes the recursive floating-error obligation. The modulus, physical short-division implementation and all remaining wide products have explicit costs. [Modular proof](../../contributions/explicit-overhead/modular-walsh.md) · [Fixed-head scalar](../../contributions/explicit-overhead/modular-scalar-machine.md) |
| Native instruction language | Every matrix entry of every published native plan is dyadic. The actual singleton repair at arity 63 has a reduced denominator divisible by 73, so it cannot act on arbitrary independent inputs through this instruction language alone. The exact modular executor supplies a distinct realization. [Source-linked Lean theorem](../../contributions/explicit-overhead/formal/RepairDyadic.lean) |

## How far the binary CRT experiment reached

Let $q=2^b$. Writing separate scalar Frobenius representatives for the standard four-point transform can require at least $qd/16$ bits when $b\ge16$, where $d$ is the degree of the second direction. Full-degree directions rule out that particular scalar layout in linear space. The session used its single alternative on whole four-point blocks with arbitrary invertible internal field-linear changes. The finest compatible grouping consists of the cosets of the span of all conjugate directions. [Scalar obstruction](four-point-all-degrees.md) · [Grouping theorem](four-point-bundle-coarsening.md)

At every $b=3c$, a full-degree two-mark direction gives the stable subspace $V=\ker\operatorname{Tr}_{K/\mathbf F_{2^c}}\oplus\mathbf F_2$, with $K=\mathbf F_{2^b}$. The quotient is a length-$c$ binary word modulo complementation. Charging for all words of each retained representative gives $(3+o(1))q$ bits. Increasing the integer caller’s degree by at most two gives such a field at every sufficiently large input length and increases $q$ by at most four. The two attained transforms have these precise endpoints.

| Transform | Two-way result and cost |
|---|---|
| From the literal binary coefficient input | The sparse vanishing polynomial $S=T^2+T$, $T=X+X^{2^c}+X^{2^{2c}}$, gives $\min(c-1,\lfloor\sqrt b\rfloor)$ actual contiguous binary radix splits inside $O(q\sqrt b)$ steps and $O(q)$ cells. Each split uses one high-half correction. Splitting and joining accept arbitrary independent coefficients. At full depth its digits identify the actual monomial remainders by simultaneous evaluation at $S(a)$. [Coefficient construction](stable-four-point-bundles.md#the-contiguous-binary-coefficient-input) |
| Inside the stored representatives | $\Theta(\sqrt b/(\log b)^2)$ consecutive ordinary additive levels, forward or inverse, fit the same $O(q\sqrt b)$ time and $O(q)$ space on a shared ordering. Their field-word arithmetic, parent scratch and rewinds are included. The offset of a chosen representative can be nonzero. Preserving that translation recovers the correct conjugate remainder. [Layer proof](stable-four-point-bundles.md) · [Independent review](REVIEW-BUNDLE-LAYERS.md) |

There is now an exact grouped CRT boundary. If $s$ runs over Frobenius orbit representatives in the image of $S$, of lengths $d_s$ and minimal polynomials $m_s$, then $X^q-X=\prod_s m_s(S(X))$. The mixed-basis remainder uses exactly $|V|d_s$ independent binary bits per orbit, hence $q$ bits in total. It is the literal binary polynomial remainder on that product of the original factors. The fast internal schedule currently uses $(3+o(1))q$ bits in a different ordering. [Grouped factor identity](stable-four-point-bundles.md#grouped-binary-remainders)

These two partial transforms do not yet meet. Fast simultaneous evaluation at the relative-trace values, the required monomial/product-basis conversions, literal factor order and the first and higher integer carry maps remain open. Composing all ordinary full-stream passes costs $\Omega(qb)$ even with free arithmetic. The complete coefficient radix algorithm likewise emits $q$ bits at each of $\Theta(b)$ levels. At a budget $O(q\sqrt b(\log b)^C)$, a full $\Theta(b)$-level scheme can afford at most $O(\sqrt b(\log b)^C)$ materialized stream boundaries. This restriction applies to those implementations.

## Verification and attribution

The pinned Lean build and its [precise theorem and axiom receipt](lean-axioms.txt) cover the native plan obstruction, the exact published signed Walsh target under its bank norm bound, the finest compatible coset partition, trace/cycle identities, evaluation and interpolation on arbitrary independent directions, actual reversible Frobenius transport of complete ordered remainders, and ordinary polynomial quotient and remainder for the literal coefficient-side trace radix split. Eight modules compiled with warnings treated as errors, and all 56 named axiom checks passed. The [grouped-division theorem](../../contributions/explicit-overhead/formal/GroupedComposition.lean) proves the actual quotient and remainder over any field without a caller-supplied degree estimate. [Formal coefficient split](../../contributions/explicit-overhead/formal/TraceCoefficientPrefix.lean) [Build script](../../contributions/explicit-overhead/formal/check.sh) · [Dependency-by-dependency evidence](../../contributions/explicit-overhead/verification.md)

Two independent fixed-head scalar harnesses tested 4,633 legal inputs and rejected 2,373 nonunit denominators, for 7,006 cases combined. The signed-Walsh runs checked 21,844 outputs, 16,984 modular divisions, 576 genuine repair coordinates and 2,040 midpoint controls. The independent trace-layout test checked 72,160 intermediate results in 5,456 round trips at seven degrees. Padding was replayed at 67,763 input lengths. The separate coefficient checker compared 99 ordinary long divisions, 283 polynomial identities 5,472 finite-field evaluations and 81 literal grouped binary remainders. [Finite receipt](finite-replay.json)

The three parallel AI research/review assignments covered the binding proof edge, the exact CRT gate and formal/adversarial review. The integrating researcher reran the published tests and Lean sources. Finite runs are regression evidence. The written resource estimates, formal algebra and complete machine have the separate verification scopes above. [Source map](../../SOURCE-AUDIT.md) · [Prior art and attribution](../../EXTERNAL-RESEARCH.md)

## Campaign decision

One of three campaign slots is used; two remain shared between the broad and focused prompts. Freeze separate scalar-orbit materialization and the one-full-pass-per-ordinary-level route to a complete transform. A subsequent discovery slot needs a charged fused conversion between the identified endpoints or a bidirectional conversion to the literal caller format. More local round trips do not change the complete cost. External review of the explicit finite interchange supplier or its physical formal refinement remains a useful contribution independently of endpoint discovery.

The nearer target $G=O(\log(x+2))$ remains conditional on the unconstructed CT-I and CT-W suppliers. The exact CRT route also requires the missing binary and carry costs in UC6. Weak ETH enters only a lower-bound discussion. Neither the retained written upper bound nor either partial transform assumes it. The fixed-$\kappa$ record and the exact square-root endpoint are unchanged. [Open obligations](../../OBLIGATIONS.md)

## Independent check of the coefficient endpoint

A second implementation tested 2,046 forward-first and 1,853 inverse-first cases, 5,709 comparisons with ordinary long division, 3,899 flat polynomial reconstructions and 28,080 coefficients of 90 actual coset remainders. Its 54 grouped remainder comparisons and nine factor products cover 430 literal irreducibles. All 65,814 enumerated scalar coordinate encodings were distinct within their respective fields. An independent review confirmed the exact $q$-bit grouped layout and its open conversion costs. [Independent checker](verify-trace-prefix-independent.js) · [Raw counts](trace-prefix-independent-receipt.json)

All eight compiled modules were also replayed with their imports in fresh Lean kernel environments. The independent coefficient verifier reproduced its complete 2,178-byte receipt. [Kernel transcripts](lean-axioms.txt)

A separate reproduction fetched the published scientific checkpoint, verified 52 file blobs and 93 local link targets, reran all 13 finite-check drivers, and rebuilt all eight Lean modules from the fetched files. All 56 named axiom lists passed. The independent coefficient driver reproduced its raw receipt byte for byte. [Source checkpoint](https://github.com/CubeJerry/integer-mult-bounds/commit/cc75d2b35c1d6828536a0473d5e6de5426ac2ef0)

### S006 completion record

Started at 03:04:51 UTC and closed at 05:04:51 UTC on 26 November 2026, after 7,200 seconds. The requested interval was 7,200 seconds. One of three shared campaign sessions is complete and two remain.
