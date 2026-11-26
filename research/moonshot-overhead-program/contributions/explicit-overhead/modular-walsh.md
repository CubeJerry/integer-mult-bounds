# Exact integer Walsh rows for the adaptive tape multiplier

The selected Walsh layer of AQ can return its exact signed integer numerators. A single rounding at the output then supplies the published fixed-point interface. The argument replaces the propagation-of-rounding-errors estimate through the adaptive rational program. It uses the exact identities, physical routing, and sharing schedule already required by AQ.

## Statement

Fix positive constants $c$ and $C$. Write $N=2^k$, $F(t)=(t^2\log_2(t+2))^{1/3}$, and let $k\ge1$. Select any $s\le\min(k,ck/\log_2(k+2))$ distinct binary address positions. Each input record contains a signed integer $u$ with $|u|<2^w$, where $1\le w\le Ck$. For every setting of the spectator bits, a single deterministic finite-alphabet multitape machine writes the exact signed integers

$$
Z_y=\sum_{x\in\{0,1\}^s}(-1)^{x\cdot y}u_x
$$

in the prescribed address order, in $O(Nk\sqrt{1+k}\,2^{O(F(\log_2(k+2)))})$ steps and $O(Nk)$ cells ever visited. The bit positions and widths are supplied with the input. Constants may depend on the fixed $c,C$. The same algorithm gives the adjoint, since the selected Walsh matrix is symmetric. Real and imaginary mantissas occupy two integer components.

For inputs on a grid $2^{-p}$, the normalized result can be rounded correctly, component by component, back to that grid within the same resource bounds. This is a written refinement of the numerical component. Its application to multiplication retains AQ's exponent.

## Exact denominator support

Use the actual arithmetic and scheduling from [S003 CW](https://github.com/CubeJerry/integer-mult-bounds/blob/69632d87c99b5a75d0b44a7d964e6550e457e016/research/moonshot-overhead-program/sessions/2026-11-26-S003/route-a/compact-rational-walsh.md) and [S003 NW, §§2–7](https://github.com/CubeJerry/integer-mult-bounds/blob/69632d87c99b5a75d0b44a7d964e6550e457e016/research/moonshot-overhead-program/sessions/2026-11-26-S003/route-a/nonstationary-rational-walsh.md). Even recursive widths make the normalized child matrices dyadic. The common and free kernels supply the same normalization, and the full spectral conversions cancel their normalizations on either side of the row map. The binary phases are signs. These are equalities of matrices over the rationals at every width. The adaptive construction adds rational Newton and repair coefficients. [OpenAI, binary implementations](https://github.com/openai/math/blob/3344da59991ed94f9ba711217b29c1d760badfa6/preprints/The-logarithmic-exponent-of-finite-Fourier-transforms-November-24-2026/build/binary.tex)

At arity $m$, let $W_0$ denote the number of Newton seeds and $d$ the degree. For each $0\le c'\le m$ and $\gamma,z\in\{-1,1\}$, calculate

$$
g(c',\gamma,z)=\gamma\sum_{h=0}^{d}(-2)^h {c'-u_0\choose h}-z ,
$$

where $u_0$ is the lower endpoint of the predictor window. Generalized binomials at negative integers are integers. There are at most $4(m+1)$ candidates. Their bit lengths are $O(d\log(m+d+2)+\log(d+2))$, using the product formula term by term. Include every nonzero absolute gap. The actual defect set uses precisely these nonzero values. Its empty case uses the zero repair map. [S002, pairwise Newton and division repair, §§2–4](https://github.com/CubeJerry/integer-mult-bounds/blob/69632d87c99b5a75d0b44a7d964e6550e457e016/research/moonshot-overhead-program/routes/B/pairwise-newton-division.md)

Form the positive integer $U_m$ by multiplying 2, $\max(W_0,d)!$, the nonzero absolute gaps, and the denominators of the polynomially many ordinary rational constants given explicitly in the local compiler. The exceptional key-dependent table is computed as follows. Its nodes are distinct $i/W_0$, so the determinant of a selected Vandermonde matrix is the product of their pairwise differences. Each inverse Lagrange row consists of coefficients of

$$
\prod_{j\in J,\, j\ne i}\frac{W_0 X-j}{i-j}.
$$

Consequently the coefficients of the matrix, its inverse and inverse transpose have denominators supported on primes dividing $W_0!$. The inverse-gap factors have prime support in the listed gap product. Their sums and products belong to $\mathbb Z[1/U_m]$. The other key-dependent binary phases and row rewirings choose signs, permutations or explicitly generated rational coefficients. Addresses, indices, integer counts and the defect tests are evaluated on their source representations. If the coefficient generator uses rational elimination, reduce its final numerator and denominator over $\mathbb Q$ before modular execution. Its intermediate pivots need no inverse in the residue ring. Construction time and bit length for $U_m$ are $m^{O(1)}$, including the polynomially many elementary integer multiplications. A concrete adverse instance in the replay has $m=63,W_0=64,d=33$, where an actual gap is divisible by 73, a prime beyond the spacing and Newton factors.

Let $m_i$ be the actual arities on the numerical width chain and put $U=2\prod_i U_{m_i}$. A fixed arity's finite repair stages use its same support. NW §§5–7 establish that every spatial call at a given numerical depth has the same active width, the depth is $O(\log(k+2))$, and the largest arity is $2^{O(F(\log_2(k+2)))}=k^{o(1)}$. Hence $\log_2 U\le O(\log(k+2))(1+\max_i m_i)^{O(1)}=k^{o(1)}$ asymptotically, interpreting an empty maximum as zero. Build this one support product in polynomial time in $k$. The factor 2 covers direct four-point leaves, including a call with no adaptive widths.

## Execution on residues and exact recovery

Use the common modulus

$$
M=1+2^{k+w+s+2}U.
$$

It is odd, has $\Theta(k)$ bits, and is coprime to every reduced coefficient denominator. Thus $a/b\mapsto a\,b^{-1}\pmod M$ is a ring homomorphism from $\mathbb Z[1/U]$ to $\mathbb Z/M\mathbb Z$. Cross multiplication proves it is well defined. Apply it entrywise to each finite rational matrix equality, including normalization in the recursively supplied children. Matrix composition, row addition and rearrangement commute with this homomorphism. This argument requires neither division by a nonunit nor a payload-dependent choice of branch.

Set $e=2\lfloor s/2\rfloor$. Shift every signed input mantissa left by $e/2$ bits before encoding it modulo $M$. This shift is an ordinary copy with zeros and its magnitude is below $M/2$. The normalized even program is exactly $2^{-e/2}W_e$ on its active bits. If $s$ is odd, apply one unnormalized integer butterfly to the remaining bit by a split, scan and merge. The resulting residues represent $Z_y$ in every spectator fibre. Since $|Z_y|<2^{w+s}<M/2$, comparing the residue to $M/2$ and subtracting $M$ when necessary recovers the signed answer. Empty selection is the identity. The same argument applies to complex records by acting separately on their two components.

For a reduced scalar $A/b$, let $B=m^{O(1)}$ bound the two bit lengths. Signed multiplication by $A$ needs $O(B)$ modular additions and doublings of $O(k)$-bit residues. Let the result be $0\le z<M$. If $b=1$ return $z$. Otherwise calculate

$$
r=(-z\bmod b)(M\bmod b)^{-1}\bmod b,\qquad v=(z+rM)/b .
$$

The inverse here is computed on small $B$-bit operands. The numerator is divisible by $b$, $0\le v<M$, and $bv=z\bmod M$. Both initial remainders are computed by scanning the long word and retaining a $B$-bit remainder. Shift-and-add multiplication by $r$ and ordinary exact division by $b$ take $O(kB+B^{O(1)})$ total tape steps, including rewinds, with $O(k+B^{O(1)})$ temporary cells. In particular no variable $k$-bit inversion is charged per numerical record. Store the common modulus on a reusable sequential track and rewind it on each use.

The number and widths of calls, rectangle sharing, array extractions, bit-position permutations and the source's repaired packed-XOR operations are unchanged. Records still have $\Theta(k)$ bits. The small-scalar costs are contained in the $k\,m^{O(1)}$ per-record allowance of NW §§4–6 and update only its absolute compiler exponent. Its time induction allows any fixed enlarged exponent. The total setup is polynomial in $k$. The same constant number of parent arrays is parked, sibling calls reuse marked regions, and the common modulus is stored once. The numerical descriptor and scalar areas are bounded by polynomial in $k$, while the root has $N=2^k$ records. NW §7's absolute $O(Nk)$ visited-cell and time arguments apply. Direct integer execution handles the finite exceptional widths.

## Correct rounding and the full-product caller

Write $t=|Z_y|$. The normalized output on the original grid uses the nearest integer to $t2^{-s/2}$, restoring its sign. Choose ties away from zero. Even $s$ requires a shift with its midpoint test. For odd $s$, compute $J=w+s+3$ and $A=\lfloor\sqrt{2^{2J-s}}\rfloor=\lfloor 2^{J-s/2}\rfloor$ once by integer bisection. Then

$$
j=\lfloor tA/2^J+1/2\rfloor
$$

is either the required nearest integer or one below it, because $0\le t2^{-s/2}-tA/2^J<t2^{-J}<1/8$ for $t>0$. The zero case is immediate. Increment $j$ precisely when $4t^2\ge 2^s(2j+1)^2$. This comparison is exact. The multiplication and two squares use $O(k\log(k+2))$ steps per record via the existing short multiplication in the tape paper. Word lengths are $O(k)$. Even charging its entire time as scratch visits for one short product, reuse gives $O(k\log(k+2))$ scratch cells for this final scan, absorbed by $Nk$.

For complex records the Euclidean error from this one correctly rounded boundary is at most $\sqrt{2N}\,2^{-p-1}$. The published caller requests norm allowance $2^{13k}$ and error $2^{-50k}$. Taking $p=52k$ suffices for Walsh alone, and any larger common working width is supported. Unitarity bounds each exact component by the input norm, so $13k+O(1)$ signed integer bits suffice at this boundary. The published phases, pointwise product, inverse scaling and exact carry recovery retain their own precision and work arguments. The lemma replaces NW's internal amplification and coefficient-rounding analysis, including AQ6's Walsh preflight. The numerical gain is confined to Walsh rows. [OpenAI, exact recovery and transform tolerances](https://github.com/openai/math/blob/3344da59991ed94f9ba711217b29c1d760badfa6/preprints/The-logarithmic-exponent-of-integer-multiplication-on-tapes-November-24-2026/build/integers.tex)

## Verification and overlap

The companion check exercises the small-denominator executor, an actual multi-defect Newton/Vandermonde key, the missing-gap control, exact signed recovery on arbitrary finite inputs and the squared midpoint comparison. Its direct finite butterfly implementation checks the residue semantics. The complete routing program has written-proof status. OpenAI's fixed-template paper already proves an exact dyadic arithmetic circuit for even Walsh widths. The step here applies the programme's actual key-dependent rational coefficients to integer mantissas with paid fixed-tape movement and one common word width. Alman's constant-finite-field lookup algorithm and Alman–Rao's arithmetic counts concern different cost models. This is a proof simplification and component strengthening with unestablished priority. [Alman](https://arxiv.org/abs/2211.04643) · [Alman and Rao](https://arxiv.org/abs/2211.06459)

The published Lean `KernelPass.Coefficient` contains an integer numerator and a binary denominator exponent. Its literal interface does not directly express the variable rational repair executor. The proof here is written. An imported Lean implementation of the modular row program, its physical compiler and its attachment to the multiplier are open. [OpenAI, Lean kernel plans](https://github.com/openai/math/blob/3344da59991ed94f9ba711217b29c1d760badfa6/lean/OAI/Computability/NearSquareRoot/KernelPass.lean)
