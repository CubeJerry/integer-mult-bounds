# Numerical overhead for the full integer product

Jerry Chen (@CubeJerry) directed this research session with substantial ChatGPT research and verification assistance. It used the final slot of the joint S006–S008 contribution campaign. The proof, code and reproduction commands are on the programme branch of the fork.

## Results

One deterministic finite-alphabet multitape machine reads two arbitrary most-significant-first \(n\)-bit strings on a single marked input, allows leading zeros, and writes exactly \(2n\) product bits to a fresh tape. Put \(L=1+\log_2 n,\ x=\log_2 L,\ \Phi(x)=(x^2\log_2(x+2))^{1/3}\). Its worst-case transitions and cumulative physical space satisfy
\[
 T(n)\le n\sqrt L\,2^{63\Phi(x)} \quad(n\ge2),\qquad
 T(1)\le4096,\qquad S(n)\le2^{32}n\quad(n\ge1).
\]
Here \(S(n)\) counts distinct tape/address pairs over the entire run, including cells later erased. Writing \(T\le n\sqrt L\,H\) and \(G=\log_2 H\), the proved allowances are \(H\le2^{63\Phi(x)}\), \(G\le63\Phi(x)\). Thus the excess exponent above \(1/2\) is bounded by \(63(\log_2(x+2)/x)^{1/3}\) at every \(n\ge2\). [All-length construction](all-lengths.md) · [Numerical constant 63](address-native-staircase.md) · [Physical space](routing-outer-space.md)

For the same fixed machine let \(t=\log_2\log_2 n\) and \(\ell=\log_2 n\).

| Guaranteed time | Sufficient range |
|---|---:|
| \(2T(n)\le n\sqrt\ell\,2^{60\Phi(t)}\) | \(t\ge1{,}572{,}864{,}480\) |
| \(2T(n)\le n\sqrt\ell\,2^{53\Phi(t)}\) | \(t\ge2^{69110}\) |
| \(T(n)\le n(\ln n)^{501/1000}\) | \(t\ge7{,}519{,}517{,}465{,}920{,}988\) |

The last row includes a unit leading coefficient. A numerical input threshold means \(n\ge2^{2^{t_0}}\) bits per operand. A calculation over all earlier arity changes finds that an earlier width still determines the limiting term at this endpoint. Independent interval arithmetic verifies that its predecessor misses the stated upper estimate by more than 0.000325836 binary logarithmic units; the displayed cutoff passes by more than 0.000053248. Determining the earliest length where the algorithm meets this time bound is a separate question. The [fixed-exponent table](all-exponents.md) computes sufficient lengths for any rational target of the form \(1/2+1/q,\ q\ge2\). [Coefficient 60](profile-limit.md) · [Effective coefficient 53](coefficient-53.md) · [Structured threshold](routing-label-walsh.md)

## What changed

The published November construction gives one exact machine in \(n(1+\log n)^{1/2+o(1)}\) time and linear visited space. The earlier fork gave the explicit **functional order** \(G=O(\Phi)\) of the logarithmic overhead. S008 now bounds the constants, the valid input range and the complete returned integer cost. Both the published upper bound and this construction are unconditional. Variable-count Weak ETH enters the published lower bound. [Source theorem and model](https://github.com/openai/math/tree/3344da59991ed94f9ba711217b29c1d760badfa6/preprints/The-logarithmic-exponent-of-integer-multiplication-on-tapes-November-24-2026) · [Previous fork theorem](../../contributions/explicit-overhead/README.md)

The three physical branches use a 19-state raw schoolbook multiplier at \(n\le2^{48}\), a counted ordinary dyadic transform until the packed address width reaches \(2^{4096}\), and then the coprime-box construction. In the last branch the final program starts its adaptive Walsh routine at \(X=2^{24}\). Earlier checkpoints used \(X=2^{26}\). The improved finite-search bound proves the earlier switch is affordable. At the fixed-exponent cutoffs both versions have identical large-input execution. [Raw rule](schoolbook.md) · [Dyadic branch](address-dyadic-words.md) · [Finite search and full return](integer-clock.md)

Two numerical details mattered. First, large permutation calls have narrower occupied child records than a charge at full parent width assumes. Second, the cost of a packed label depends on its **actual number of bits**. Bounding that length band by band produces a smaller estimate for the same calls. The continuous approximation to this revised estimate has limiting coefficient \(8+240^{1/3}(7+\ln(2)/3)\approx52.9371\). A separate finite calculation supplies the input cutoff for the rounded coefficient 53. [Native and Walsh proof](address-refined-label.md) · [Independent review](compiler-review-refined-label.md)

## Attempt to improve the functional order

A shared traversal reduced the number of endpoint preparations by an unbounded factor on a legal family. At \(d=32,\ t_{\rm label}=1280\) its previous-to-new incidence ratio lies between \(2^{5947}\) and \(2^{5948}\). A source still needs at least \((q-1)^d(t_{\rm label}-1)^{d(d-1)}\) incompatible views in the specified whole-row, prefix-preserving model. Sharing across different boxes and assembling partial outputs fall outside that argument. No faster order for the complete multiplier followed. The pending mathematical question is whether many distinct endpoints can share a data traversal whose physical movement and Walsh repair are both cheaper. [Exact construction and model](routing-cross-anchor.md) · [Independent audit](address-review-cross.md)

## Campaign decision

| Question | Binding change | Decision |
|---|---|---|
| Can the adaptive interchange be priced numerically through its real children? | A fixed \(R=240\) node, its repeated children, full reserves, direct base and physical return all have numerical bills. | Admit the numerical construction. |
| Do those numbers survive the Walsh and whole-integer callers? | The actual slot widths, finite catalogue search, three transforms and fresh carry/output yield an all-length coefficient and a concrete threshold for exponent \(0.501\). | Admit the complete written upper bound and the indicated component proofs. |
| Does sharing a canonical preparation across several anchors remove the logarithmic factor? | A mutually incompatible family forces repeated views in that model. | Freeze this traversal. |
| Can a different partition across anchors lower the full rate? | Pinning the narrowest side reduces endpoint incidences by an unbounded factor, but the remaining data delivery and Walsh charges still have the original order. | Freeze this partition as a route to a better full rate. |

S006, S007 and S008 used all three campaign slots. No new conditional assumptions entered the numerical theorem. The older conditional transfers retain their prior status. Targeted source and PR searches establish no priority claim. Seek **external mathematical review** of the complete numerical construction. The first review question is whether each call on an extracted Walsh bank pays exactly once for moving its occupied payload out and back through the native interchange, while its head extents across all calls satisfy the single claimed space cap. A successful change of functional order would require a new delivery or transform result. [Outstanding obligations](../../OBLIGATIONS.md) · [Source comparison](../../EXTERNAL-RESEARCH.md)

## Proof status and review

The complete time and space estimates are **written mathematical constructions with independent AI review**. The Lean development verifies selected literal tape rules, exact visited-cell bounds, data-independent control, selected Walsh identities, integer recovery and the analytical transfer of numerical supplier bills. Four full-precision box tests, deliberately invoked below the normal transform cutoff, each recovered all 210 coefficients and all 2,000 output bits. The cases included two all-one inputs, a zero operand, isolated one-bits, and a padded dense product. Omitting inverse CRT changed 204 coefficients on the dense reference pair. These tests used host arrays for the transform schedule. Human peer review and an end-to-end Lean theorem for the entire revised machine remain outstanding. [Verification matrix and commands](VERIFICATION.md) · [Complete box test](recount-system-audit.md)

The session began from fork commit 036d2fc958482f9489d4efadf395844ab3b3eb60. The source pins were CrocSwap/integer-mult-bounds e54523517d0f03e58352e647c403a5af3e525a57, OpenAI/math 3344da59991ed94f9ba711217b29c1d760badfa6, and CubeJerry/AI_Prompts d4ff248476b9d814d6dadde546645349fda1e33f. The two routing approaches have completed their decision tests. The programme branch contains the external-review draft; publication upstream is separate. [Session record](SESSION.md) · [Programme state](../../STATE.json) · [Draft contribution description](../../PR-DESCRIPTION.md)
