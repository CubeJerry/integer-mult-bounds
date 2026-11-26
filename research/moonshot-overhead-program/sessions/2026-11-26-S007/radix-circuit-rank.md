# Dyadic ranks of the trace-radix conversion and the cost of ordered XORs

The inverse trace-radix map already forces a linear rank at each remaining scale. This rules out a faster crossing by circuits which share sums but preserve their least participating input index at every XOR. It also measures the cancellations an unrestricted XOR circuit must provide. The same obstruction holds separately for the forward map. This is a lower bound for stated circuits on this particular representation conversion; the full binary CRT can bypass this intermediate representation.

## The actual matrix

Let \(b=3c\), \(a=2^c\), \(q=a^3\), \(v=2a^2\), \(m=c-1\), and \(r=\min(m,\lfloor\sqrt b\rfloor)\). Set \(d=m-r\). Assume \(c\ge2\); if \(d=0\) the bounds below are vacuous. Over \(\mathbf F_2\), the polynomial in the S006 split is
\[
 D(X)= X^{v}+X^{v/2}+X^{2a}+X^a+X^2+X .
\]
Starting from the priced depth-\(r\) output, there are \(2^r\) consecutive independent polynomials of length \(v2^d\). Complete expansion of each gives \(2^d\) successive base-\(D\) digits, each of length \(v\). Write \(M\) for the inverse, from these final digits back to the depth-\(r\) output. For each prefix its \((vj+k)\)-th column is the coefficient vector of \(X^kD^j\), \(0\le j<2^d,\ 0\le k<v\), in increasing ordinary degree order. It has a 1 at row \(vj+k\) and zeros at all larger indices. This monic triangularity gives invertibility, identifies the complete canonical ordering, and proves every lower-digit subblock spans all polynomials of its stated length. Independent bits may be chosen at either endpoint. The whole matrix is the direct sum over prefixes in their original order.

Fix a prefix. For \(0\le i<d\), put \(z=2^i\), \(h=vz\), and consider any aligned interval \(I=[2ph,2(p+1)h)\) inside that prefix, in prefix-relative addresses. Let \(L,R\) be its two halves in increasing order. Then, in both directions,
\[
      \operatorname{rank}_{\mathbf F_2} M[L,R]
       =\operatorname{rank}_{\mathbf F_2} M^{-1}[L,R]= h-z. \tag{1}
\]
Only the source and target coordinate ranges are restricted in (1); their meaning is the literal input/output order above.

**Proof.** The input columns in \(R\) give exactly
\[
        D^{(2p+1)z} B(X),\qquad \deg B<h.
\]
Indeed the lower \(i\) radix digits and the within-leaf coefficient index provide an invertible triangular change of the \(h\) independent columns of \(B\). The exponent starts at \(2ph/v+z\). Write \(E=D^z\), \(V(Z)=Z^h E(Z^{-1})\). The constant term of \(V\) is 1 and every remaining term has exponent at least \(h/2\). On positions \(0,\ldots,2h-1\) define an upper triangular Toeplitz operator \(U\) by sending the basis vector at \(s\) to \(\sum_{j=0}^s[Z^j]V\,e_{s-j}\). This is multiplication by \(V\) modulo \(Z^{2h}\) when positions are reversed. For an input monomial \(B=X^k\), the actual coefficient at output \(2ph+u\), \(0\le u<h\), is
\[
     [Z^{h+k-u}]V^{2p+1}.
\]
All indices on the right lie between 1 and \(2h-1\). Thus the upper-right block of \(U^{2p+1}\) gives the actual off-diagonal map in ordinary \(B\) coordinates. In characteristic two, \(V^4=1\pmod{Z^{2h}}\), since every nonconstant term of \(V\) has degree at least \(h/2\). Hence \(U^{2p+1}\) equals \(U\) for even \(p\) and \(U^{-1}\) for odd \(p\).

For \(U\), projecting from the upper half onto the lower half gives multiplication by \(E-X^h\) in \(\mathbf F_2[X]/(X^h)\). Its least-degree term is \(X^z\), with coefficient 1. This multiplication has image the ideal \((X^z)\) modulo \(X^h\), of dimension \(h-z\), since the remaining factor after removing \(X^z\) is a unit. For every block upper triangular invertible matrix \(\begin{pmatrix} A & B_0 \\0&C\end{pmatrix}\) with invertible diagonal blocks, its inverse has upper-right block \(-A^{-1}B_0C^{-1}\), which has the same rank. This proves the result for both parities of \(p\). Finally, for any contiguous principal interval of an invertible upper triangular matrix with nonzero diagonal, the corresponding principal block of its inverse is the inverse of that principal block. Partition all indices as before, inside and after the interval and use block upper triangular multiplication. Apply the preceding two-block identity to \(M[I,I]\) to obtain (1) for the forward conversion as well. \(\square\)

## Charging arbitrary shared sums

Consider any acyclic two-input XOR circuit over \(\mathbf F_2\), with the \(q\) canonical input bits, unlimited fanout, and wires to the required output coordinates. Every signal has a homogeneous linear form. Gates producing or consuming a constant zero form may be simplified away without increasing the size; this does not change any surviving nonzero form. Write \(p(x)\) for the least index of a nonzero input coefficient in a nonzero signal. Let \(G\) be the number of XOR gates, and \(P\) the number with equal operand minima and nonzero output. These gates cancel that minimum. All other nonzero additions preserve the smaller operand minimum, including gates that cancel many other coordinates.

For either complete converter, every such circuit satisfies
\[
       G+dP\ \ge\ \frac{qd}{2}(1-1/v). \tag{2}
\]
In particular, a circuit with no such cancellations needs at least \(qd(1-1/v)/2\) XOR gates. This includes cancellation-free circuits as customarily defined. If \(G=o(qb)\) at this depth, then \(P\ge(1/2-o(1))q\). The count concerns the least **original input** index of a form, irrespective of wire ordering, fanout, or the gates used to build it.

**Proof.** For an interval \(I=L\cup R\) of the preceding dyadic forest, project a signal onto its \(R\) input coefficients. The projections of all signals with minimum in \(L\) lie in the span of the following vectors:

1. The projected operand with minimum in \(R\) at each gate combining minima in \(L\) and \(R\).
2. The projected signal at each gate whose output minimum lies in \(L\) and whose two operand minima coincide strictly before the start of \(I\).

Indeed an input coordinate in \(L\) has zero projection. For an unequal-minimum gate with result minimum in \(L\), its smaller operand is already covered by induction. The other either lies in \(L\), supplies an item of type 1, or has minimum above \(R\) and zero projection. At an equal-minimum gate with output minimum in \(L\), the common old minimum is either in \(L\), where induction covers both operands, or before \(I\), which gives type 2. This topological induction accounts for arbitrary sharing. The output row at index \(s\in L\) has minimum precisely \(s\), by triangularity. Therefore the rank of the entire off-diagonal block is at most the listed vector count for this interval.

An unequal-minimum gate supplies type 1 at most once over the forest, at the least common dyadic ancestor of its two operand minima if such a selected ancestor exists. A gate cancelling its minimum supplies type 2 at most once at each of the \(d\) levels, since its output minimum is fixed. There are \(q/(2h)\) intervals at level \(i\). Formula (1) gives exactly \((q/2)(1-1/v)\) for their rank sum. Summing proves (2); the sharper count \((G-P)+dP\) also suffices after eliminating zero forms. \(\square\)

## How far a cancelled minimum must move

For a gate counted by \(P\), let \(\Delta_g=p(\text{output})-p(\text{operand})>0\), and put
\[
  \psi_d(\Delta)=\tfrac12\sum_{i=0}^{d-1}\min\!\left(1,\frac{\Delta}{v2^i}\right).
\]
Every such circuit satisfies the scale-sensitive inequality
\[
         G+\sum_{g\in P}\psi_d(\Delta_g)\ \ge\ qd/64. \tag{3}
\]
The constant in (3) is chosen for simplicity. In particular, if every \(\Delta_g\le v b^K\) for some fixed \(K\), both directions require \(\Omega_K(qb/\log(b+2))\) gates for unbounded \(c\). More generally a circuit of size \(O(q\sqrt b(1+\log b)^C)\), for fixed \(C\), needs at least \(q/64\) minimum jumps with \(\Delta_g/v\ge2^{\Omega(\sqrt b/(1+\log b)^C)}\) for sufficiently large \(c\).

**Proof.** Extend the matrix by identity wires, in the same scalar order, on both sides of the input interval, far enough for all windows below. This extension requires no extra gates; every output still has its own least input index. Translate one common nested grid of intervals by a uniform integer in \([0,q)\). This randomization only averages a deterministic circuit inequality. At level \(i\) the offset modulo \(2h\) is uniform. With probability at least \(1/16\) it belongs to \([0,\lfloor h/8\rfloor]\). On this event, each original window has a translated grid window offset to its right by at most \(h/8\). Intersecting their two row ranges and two column ranges removes at most \(h/8\) rows and \(h/8\) columns from the original block. The translated block has rank at least \(h-z-h/4\ge h/2\), since \(v\ge4\). This includes windows straddling an original prefix boundary: only the retained common submatrix matters. The expected sum of ranks is at least \((q/(2h))(h/2)/16=q/64\) per level, hence at least \(qd/64\) overall.

The same charging proof applies on each translated grid. A type 1 gate is counted at most once. A type 2 gate at scale \(h\) requires that the grid places a left endpoint strictly after its old minimum and no later than its new one and that the new minimum lies in the left half. The number of residues modulo \(2h\) for this event is at most \(\min(h,\Delta_g)\): the distance of the new minimum from the left endpoint is in \([0,\min(h,\Delta_g)-1]\). Taking expectations proves (3). To obtain the consequences, split the defining sum for \(\psi_d\) at \(2^i\approx\Delta/v\). It is at most \((3+\log_2^+(\Delta/v))/2\), where \(\log_2^+ y=\max(0,\log_2 y)\). For \(L\ge0\), let \(N_L\) count jumps with \(\Delta_g/v\ge2^L\). Each shorter jump contributes at most \((L+3)/2\), and each longer jump contributes at most \(d/2\). As there are at most \(G\) jumps, (3) gives
\[
       N_L \ge q/32 - (L+5)G/d,\qquad d>0 .
\]
Write \(G\le Kq s\), with \(s=\sqrt b(1+\log b)^C\) and constant \(K>0\). Take \(L=\lfloor d/(128Ks)\rfloor\). Since \(d=\Theta(b)\) and \(s=o(d)\), eventually \((L+5)G/d\le q/64\). This proves the linear count of long jumps. \(\square\)

The classical triangular-block rank method for cancellation-free sums appears in work of Grigoriev and in Jukna's *Linear Boolean Operators*, Theorem 3.18. Boyar and Find used a related decomposition for the Sierpinski matrix. The application here is to monic trace-radix columns at the actual S006 endpoints; the exceptional-minimum and translated-grid accounts distinguish cancellation size from location. The proof does not need a priority claim for the generic circuit technique. [Jukna, triangular block bound](https://web.vu.lt/mif/s.jukna/Knizka/linear.pdf) · [Boyar and Find, 2015](https://doi.org/10.1016/j.tcs.2014.10.014) · [Coxon, 2021, additive basis conversion](https://doi.org/10.1016/j.jsc.2020.10.002)

A scalar fixed-alphabet tape implementation which explicitly evaluates only a bounded number of two-input XOR gates per step inherits the applicable gate lower bound. General tape programs may use input-dependent control, nonlinear operations, or arbitrary cancellations; (2) and (3) do not lower-bound their time. They also do not preclude fusing this conversion with another endpoint. Binary CRT, the factor directory and all integer carry levels keep the same resource obligations.
