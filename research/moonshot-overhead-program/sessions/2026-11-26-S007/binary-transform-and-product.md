# Three bounds for the complete trace-plane construction

Fix a rational $0<\eta<1/2$. Set $b=3c\ge3$, $a=2^c$, $q=a^3$. FS1 enumerates the distinct monic binary factors of $X^q-X$ by degree and Lyndon word. Each bound below uses a fixed deterministic finite-alphabet multitape machine. Space counts every distinct tape cell visited through halt.

| Map | Worst-case time | Visited cells |
|---|---|---|
| Coefficients to every literal FS1 remainder, or the reverse on $q$ independently chosen bits | $O_\eta(qb/(1+\log_2(b+2))^\eta)$ | $O_\eta(q)$ |
| Coefficients to selected plane values, or the inverse on its image | $O_\eta(qb/(1+\log_2(b+2))^\eta)$ | $O_\eta(q)$ |
| One unreduced polynomial product over $\mathbf F_2$, with two length-$n$ inputs | $O_\eta(n\log_2(n+2)/(1+\log_2\log_2(n+3))^\eta)$ | $O_\eta(n)$ |

These are written time and space proofs. A concrete choice is $\eta=1/4$.

## Paying for the three long-product batches

The [trace-plane construction](full-plane-crt.md) leaves two families of binary chirp products with aggregate operand length $O(q)$. The [independent-batch theorem](lane-packed-convolution.md) multiplies $J$ pairs of length-$D$ binary polynomials in $O_\eta(JD\log D/(1+\log\log D)^\eta)$ time and $O(JD)$ visited cells whenever $D^{3/2}\le J\le D^3$. Its internal short multiplications use the published Harvey–van der Hoeven algorithm. This avoids recursion on the present CRT. [Independent compiler audit](compiler-audit.md)

Let $R$ be the number of Frobenius orbits on $\mathbf F_a/\mathbf F_2$. Store all trace-plane rectangles before processing their axes. Finish the first axis across all planes, transpose each rectangle, and run the second batch. Restore the specified geometric order. Here $2R=(1+o(1))a/c$, including both planes at every twisted orbit. [Orbit count and volumes](chirp-self-recurrence.md)

| Calls per direction | Number $J$ | Binary length $D$ | Limit of $JD/q$ |
|---|---:|---:|---:|
| Smaller CRTs, packed $c$ to a packet | $\lceil a^2/c\rceil$ | $(2c-1)(a-1)$ | $2$ |
| First axis of every plane | $2Ra$ | $(2b-1)(a-1)$ | $6$ |
| Second axis of every plane | $2Ra$ | $(2b-1)(a-1)$ | $6$ |

In each row $J=\Theta(a^2/c)$, $D=\Theta(ac)$ and $J=D^{2-o(1)}$. All sufficiently large $c$ lie in the batch theorem's stated range. The aggregate time is $O_\eta(qb/(1+\log b)^\eta)$. Bounded small inputs use direct polynomial arithmetic. Rewinding a fixed length-$D$ chirp kernel per packet costs $O(q)$ in aggregate. A constant number of outer arrays stays live and every invocation reuses its banks from common origins, giving the common $O(q)$ bound.

The paid relative-trace radix, two-fibre join, short field arithmetic, affine chart and grid transpositions all fit the same clock, including sorting the few wide rows in the smaller $2^c$ factor directory. This proves the geometric transform between the two stated layouts. For the caller's exact FS1 order, the [two-prefix proof](marked-plane-directory.md) groups by a short Frobenius rotation tag before routing each marked subspace using binary affine permutations. Its exceptional inventory includes all proper subfields. The [one-bit orbit proof](structured-orbit-directory.md) independently assembles the same order using three conjugate slices and cyclic prefix windows. Both replace the old short-record sort. The full ordered transform now has the same clock as the geometric one, including arbitrary independent inverse inputs. [Two-prefix counts](marked-directory-cases.json) · [One-bit counts](structured-orbit-directory-receipt.json)

## Multiplication, comparison and integer implications

Choose the least positive multiple of three $b$ such that $q=2^b\ge2n-1$. Then $q<16n$. Transform both inputs to the same selected points, multiply the corresponding field words, and interpolate. These are evaluations of the ordinary product, whose degree is below $q$; Frobenius coverage and uniqueness recover its actual coefficients. This composition omits the final factor-order sort. A second composition through every individual factor serves as an independent numerical check. [Full multiplication proof, prior work and exact check](ordinary-binary-product.md)

Csizmadia's November 2 manuscript already claims the faster standalone time $O(n\log^{1301/1302}n)$ in the same tape time model. Its claim record identifies a written proof awaiting independent review. This session's contribution is the reversible transform to the specified FS1 factor interface and a separate construction with explicit linear visited space. The algorithm works over characteristic two. The integer programme still needs its square-root-scale binary interface and the higher-precision carry suppliers. [Earlier claim](https://github.com/arpcs/finite-field-polynomial-multiplication/blob/e85bc1f6ca0ec9c13281c94b6a3e88ec2cdb4fc5/papers/03-best-binary/versions/0.2.1/CLAIM.json)
