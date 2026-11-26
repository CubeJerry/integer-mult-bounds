# Recovering the ordinary divided square with one first-carry call

For a binary $n$-coefficient polynomial $f$ write $Q_f=\sum_{i<j}f_i f_j X^{i+j}$. Assume the literal-factor first-carry supplier $K_1$ at the cubic-extension degrees. One call to this supplier, two complete binary forward transforms and one complete binary inverse transform recover the entire ordinary $Q_f$. The additive fixed-tape time is $O_\eta(n(1+\log n)/(1+\log\log(n+3))^\eta)$ and the additional cumulative visited-cell bound is $O(n)$. The assumption on the carry supplier includes its own time and space. This is a reverse reduction for the first precision stage in the [integer caller](../2026-11-26-S005/route-a/unramified-polynomial-crt-caller.md).

For $n=1$ the answer is zero. Otherwise choose $b$ as the least positive multiple of three with $q=2^b\ge2n-1$. Then $q<8(2n-1)$ and $b=\Theta(1+\log n)$. Pad $f$ to $q$ binary coefficients. For every actual FS1 factor $h$ of $X^q+X$ let $F_h=\mathbf F_2[x]/h$, and take $x$ to be the class of the indeterminate. Put $r=f\bmod h$ and $s=f'\bmod h$. One forward transform each obtains $r$ and $s$; computing the formal derivative costs a single bit-selection and shift pass.

The carry datum is the unique degree-$<\deg h$ word $k$ such that the literal remainder of $\widetilde f$ modulo $\widetilde h$ over $\mathbf Z/4$ equals $\widetilde r+2\widetilde k$. The first-carry identity in $F_h$ gives
$$
k=\sqrt{Q_f(x)+Q_r(x)}+D_h(s+r'(x)),\qquad D_h=\sqrt{Q_h(x)}/h'(x).
$$
Squaring after moving the second term gives the reverse datum
$$u_h=\bigl(k+D_h(s+r'(x))\bigr)^2+Q_r(x)=Q_f(x).$$
The sign is plus in this binary field. The derivative $r'$ is taken on the returned ordinary power-basis polynomial $r$; the input derivative $f'$ was reduced separately. The formulas include $h=X$, $h=X+1$ and all proper-degree factors. To check the premise directly, the sum of Teichmüller monomials satisfies $\widetilde g([x])=[g(x)]+2[\sqrt{Q_g(x)}]$ in $W_2(F_h)$. Taylor expansion at $[x]+2[D_h]$, a root of the literal lift $\widetilde h$, gives the carry identity by subtracting the expansions for $f$ and $r$.

Each local cost is quasi-linear up to factors polynomial in $\log(b+2)$. For $d=\deg h$ compute $Q_h,Q_r$ at short lengths by balanced interval splitting, using $Q_{g_0+X^m g_1}=Q_{g_0}+X^m g_0g_1+X^{2m}Q_{g_1}$ on disjoint halves. Fast short ordinary binary products, monic remainders and extended Euclid use $O(d\operatorname{polylog}(b+2))$ steps, allowing all $O(\log(d+2))$ split levels. An explicit square root avoids a per-factor repetition of $d$ squarings. Write $h=A(X)^2+X B(X)^2$ by separating even and odd positions. Then $h'(x)=B(x)^2\ne0$ by separability and $\sqrt{x}=A(x)/B(x)$. For $w=C(x)^2+xD(x)^2$ read from its power-basis word, $\sqrt{w}=C(x)+\sqrt{x}D(x)$. This applies also at $x=0$. The sum of degrees equals $q$, so all local work, including producing $u_h$ in the known FS1 order, costs $O(q\operatorname{polylog}(b+2))$. A fixed number of stream and return banks occupy $O(q)$ cells and the short polynomial workspace is reused.

One [complete inverse transform](full-plane-crt.md), with the [two-prefix directory](marked-plane-directory.md) or the [one-bit directory](structured-orbit-directory.md), now returns $Q_f\bmod(X^q+X)$ in ordinary coefficient order. Since $\deg Q_f\le 2n-3<q$, this is the ordinary polynomial, with no wrap and all leading zeros available. Its bits are precisely the high bits of ordinary $\widetilde f^2$ modulo four; the low bits are $f_i$ in positions $2i$ and zero otherwise. Thus the first carry and an unrestricted binary-input square modulo four are equivalent at additive complete-binary-transform cost and bounded size expansion. The square at this point has a single binary operand. The next identity gives the same-precision reduction for arbitrary products; higher precisions remain outside the argument.

The [independent replay](verify-half-square-converse.py) uses direct long division over $\mathbf Z/4$ as its carry oracle, independent binary CRT reconstruction, and digit-separated integer squaring as the ordinary comparison. [Deterministic receipts](half-square-converse-cases.json)

## Arbitrary products over the same modulus

In fact the binary-input divided square and *arbitrary two-input multiplication in* $(\mathbf Z/4)[X]$ reduce to each other with a constant number of the same-size-up-to-a-factor-two calls. For binary inputs $f,g$ let $h=fg$ in $\mathbf F_2[X]$. Write their literal ordinary mod-four product as $H=\widetilde h+2\widetilde k$. Compute $H^2$ in two ways. The square of this latter expression is $\widetilde h(X^2)+2\widetilde{Q_h}(X)$ modulo four. On the other hand $H^2=\widetilde f^2\widetilde g^2$, which expands to
$$
\widetilde h(X^2)+2\left(\widetilde k(X^2)
            +f(X^2)Q_g(X)+g(X^2)Q_f(X)\right)\pmod4 .
$$
Here the cross terms multiplied by 2 can be computed over $\mathbf F_2$. The resulting exact identity is
$$
k(X^2)=Q_h(X)+f(X^2)Q_g(X)+g(X^2)Q_f(X)\quad\text{in }\mathbf F_2[X].
$$
The odd-indexed coefficients on the right vanish. Extract the even-indexed ones in one scan to obtain the high digit of *every* ordinary product coefficient. This uses three divided squares (length at most $2n-1$), and three ordinary binary products including the computation of $h$. For general input coefficients $f_0+2f_1,g_0+2g_1$, add $f_0g_1+f_1g_0$ in the high digit by two more binary products. All packet lengths are $O(n)$, and a fixed number of marked work banks are reused. Conversely a single ordinary mod-four product on two copies of a binary list returns its divided square in the high bit, so no extra precision is required in either direction. This gives a three-$K_1$ realization with the preceding reverse identity, and a one-mod-four-product realization of $K_1$ via the forward formula. An independent $K_1$-to-product proof applies the existing first-digit precision-doubling reduction to the complete mod-four CRT, at root degree above the product degree, and uses ordinary short factor-ring products. The three-divided-square identity gives the intermediate equivalence without any factorization assumption.

The argument is an instance of the product law for the difference between squaring and a lifted Frobenius. The proof above also specifies the ordinary coefficient lifts, which determine the actual digit tested here.
