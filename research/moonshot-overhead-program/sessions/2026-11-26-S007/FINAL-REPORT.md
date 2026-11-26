# S007 result and campaign decision

**The complete binary factor transform and its first precision lift now run below one full pass per ordinary level.** For $b=3c>0$, $q=2^b$ and any fixed rational $0<\eta<1/2$, the caller's actual forward and inverse transforms over $\mathbf F_2$ and over $\mathbf Z/4$ take $O_\eta(qb/(1+\log_2 b)^\eta)$ time and $O(q)$ cells ever visited. Each is a written construction on a fixed deterministic finite-alphabet multitape Turing machine. The output is the monomial remainder modulo each actual factor, in degree/Lyndon order; the inverse accepts arbitrary independent records. Over $\mathbf Z/4$ each modulus is the literal coefficientwise lift of its binary factor. [Binary theorem](binary-transform-and-product.md) · [First lift](first-witt-carry.md) · [Reverse reduction](first-carry-converse.md)

The result extends to **each fixed coefficient precision** $h\ge1$. Over $\mathbf Z/2^h$, the same ordered forward and inverse take $O_{h,\eta}(qb/(1+\log b)^\eta)$ time and $O_h(q)$ visited cells. Computing truncated Witt coordinates in $\mathbf Z[X]/(X^q-X)$ keeps global polynomials at length $q$. The integer caller needs $h$ growing proportionally to $b$. The current schedule uses up to $h(h+1)/2$ global binary transforms just for its forward coordinate list. Materializing them separately at $h=\Theta(b)$ costs $\Omega(qh^2)=\Omega(nb)$ steps even with free arithmetic. [Fixed-precision proof](fixed-witt-precision.md) · [Independent review](review-macro-and-fixed-witt.md)

**The strongest complete integer multiplication bound is unchanged.** Write $L=1+\log_2 n$, $x=\log_2L$ and $\Phi(x)=(x^2\log_2(x+2))^{1/3}$. The unconditional written bound is $O(n\sqrt L\,2^{O(\Phi(x))})$ with $O(n)$ visited cells. In the programme's notation $H=2^{O(\Phi(x))}$, $G=\log_2H=O(\Phi(x))$ and $\delta=G/x=O((\log_2(x+2)/x)^{1/3})$. The prior conditional transfer to $H=x^{O(1)}$ needs the complete uniformly costed physical suppliers and preflight profile in the [target ledger](../../TARGET-OVERHEAD.md). Weak ETH concerns a published lower bound. Neither the binary result nor its carry formula assumes it.

## What changed

| Gate | Result | Decision |
|---|---|---|
| Paid coefficient prefix to trace fibres | Two binary Pascal transforms complete the relative-trace radix; packing independent short polynomials supplies the actual child CRT. | Retain the bidirectional construction. |
| Actual individual FS1 factors | Two independently checked orderings move between trace planes and the true sorted factors at the same clock, including short orbits and independent inverse input. | Use the [marked-subspace proof](marked-plane-directory.md) for external review, with the [one-bit proof](structured-orbit-directory.md) as a cross-check. |
| First nonbinary remainder digit | Witt arithmetic reduces it to one ordinary divided square and a few binary transforms. A reverse reduction recovers ordinary modulo-four multiplication from first-carry evaluations. | Retain the equivalence and its explicit correction for the literal factors. |
| Higher fixed precisions | Truncated Witt coordinates and literal roots implement both directions at each fixed $h$. | The precision-dependent constant and global transform count require a uniform improvement. |
| Polynomial products | A two-stage Cantor–Kaltofen outer transform feeds polynomially wide ordinary convolution batches; their internal short products use a separate conventional algorithm. | Retain the [finite-ring theorem](macro-triadic-product.md). The high-volume self-recursion through the same CRT stays retired. |
| Integer endpoint | At $b\asymp\log n$, the present normalized clock $b/(\log b)^\eta$ still exceeds $\sqrt b(\log b)^C$ eventually for every fixed $C$. | Keep the previous integer envelope; the growing-precision caller needs its own uniform proof. |

## Evidence and external comparison

The full ordered transform recovered 32,768 independent bits at $b=15$ and matched ordinary polynomial division at all 2,192 factors. The modulo-four tests compared 425,222 binary-input factor records and 262,944 unrestricted two-bit factor records with signed division. At three-bit precision the checker also exhausted all 4,096 independent modulo-eight tuples at degree two. Isolated kernel-checked Lean statements cover the true inventory and product, trace charts, arbitrary CRT lifting, the masked tensor and the literal first-carry identity. The complete physical bounds are written proofs with AI cross-review. Independent human refereeing has yet to take place. [Verification and reproduction](VERIFICATION.md)

For one ordinary polynomial pair the time bound above also yields $O_\eta(n\log n/(1+\log\log n)^\eta)$ over $\mathbf F_2$, with linear visited space. Csizmadia's earlier public manuscript already claims the faster $O(n\log^{1301/1302}n)$ standalone time. Its evidence record identifies the theorem as a written claim awaiting independent review. The specific review contribution here is the reversible ordered interface and its precision lifts. [Exact earlier claim](https://github.com/arpcs/finite-field-polynomial-multiplication/blob/e85bc1f6ca0ec9c13281c94b6a3e88ec2cdb4fc5/papers/03-best-binary/versions/0.2.1/CLAIM.json)

## Campaign decision

S006 and S007 use two of the three shared campaign slots. Use the last slot to prepare the strongest local theorem for external review. The single review task is to reconstruct the complete resource bill from ordinary coefficient input through ordered factor output and back, including actual ring widths, all padding, independent child counts and the union of visited cells. A faster integer endpoint would require quantitatively stronger evidence.

The work was prepared for Jerry Chen (@CubeJerry) with ChatGPT research assistance. The parent [attribution record](../../PR-DESCRIPTION.md#credits) and the linked proofs identify the original authors and inherited constructions.

The released checks cover 23 Lean component modules, 139 named results and 28 numerical certificates. The common time and tape-space bounds remain written results.

The recorded work interval was 05:32:16–08:32:16 UTC on 26 November 2026 (10,800 seconds). The last verified scientific checkpoint before this closing record was [7d84c00d94](https://github.com/CubeJerry/integer-mult-bounds/commit/7d84c00d9422c599119795553a2396155330e3d7). The closing commit itself is visible in the branch history.
