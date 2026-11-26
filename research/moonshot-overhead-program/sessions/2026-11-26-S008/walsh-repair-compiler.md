# An integer compiler for the frequency-dependent Walsh correction

At an actual spectral address let \(J\) be the defective seeds, \(F=(W-1)!\), and \(G=G_m\) the product of possible nonzero gap magnitudes in the [denominator proof](walsh-aligned-denominators.md). For each \(i\in J\), let

\[
 d_i=\prod_{j\in J\setminus\{i\}}(i-j),\quad
 P_i(X)=\prod_{j\in J\setminus\{i\}}(WX-j),\quad
 L_{ir}=(F/d_i)[X^r]P_i(X).
\]

The division is exact. The entire matrix from a difference of check words to its corrected check words has denominator \(C=F^2G\), with signed integer numerator at \((r,s)\)

\[
             N_{rs}=\sum_{i\in J} L_{ir}L_{is}(G/g_i).
\]

This follows by multiplying the Lagrange rows in \(V_J^{-\mathsf T}\operatorname{diag}(1/g_i)V_J^{-1}\). The zero-sized table and padded rows/columns have zero output. The two check arms and the output duplication add signs depending on the common target \(z\). The integer mantissa word receives the possibly unreduced coefficient \(N_{rs}/C\); \(C\mid U\) gives the required aligned scalar precondition immediately. Intermediate numerators, including all partial prefix sums with either sign, remain within \(H=8W^2(y+2)\) magnitude bits by the absolute-sum estimates in the denominator proof. In particular one may multiply the two Lagrange integers before multiplying by \(G/g_i\). Since \(|L_{ir}|\le F(2W)^{|J|-1}\), every individual triple product and the sum of their absolute values fit. Exact short arithmetic uses a double-width temporary before copying its result to a checked \(H\)-digit value register.

## Executable finite-tape instructions

The following program emits one requested numerator and its denominator from the \(m\)-bit frequency key. The polynomial sign at seed \(t\) is \((-1)^{u_0-\sum_j\beta_j(t)}\). The target sign is \((-1)^{\operatorname{popcount}(key)}\). Rows and arguments are zero-based; the nonzero binary vectors used to generate the seed masks are numbered \(1,\ldots,m\).

```text
for each count c = 0,...,m
    p[c] = 1; choose = 1; power = 1
    for h = 1,...,degree
        choose = exact_quotient(choose*(c-low-h+1),h)
        power = -2*power
        p[c] += choose*power
F = m!; G = 1
for c = 0,...,m and both signs gamma and z
    if gamma*p[c]-z is nonzero, multiply G by its magnitude
for each seed t = 0,...,W-1
    c = 0; parity = 0
    for j = 1,...,m
        bit = parity_of_bitwise_AND(t,j)
        c += key[j-1] XOR bit
        parity ^= bit
    g = sign(low modulo 2 XOR parity)*p[c] - target_sign
    append (t,g) to J precisely when nonzero
if r or s is outside J's rank range, return zero over 1
N = 0
for (i,g) in J
    coefs[0] = 1; all other coefs = 0; degree_so_far = 0; divisor = 1
    for (j,_) in J with j distinct from i
        divisor *= i-j
        for h descending from degree_so_far+1 through 0
            coefs[h] = W*coefs[h-1] - j*coefs[h]   (coefs[-1] means zero)
        degree_so_far += 1
    multiplier = exact_quotient(F,divisor)
    left = multiplier*coefs[r]; right = multiplier*coefs[s]
    N += left*right*exact_quotient(G,g)
return signed N and positive F*F*G
```

In the sign instruction \(\operatorname{sign}(0)=1\) and \(\operatorname{sign}(1)=-1\). The degree is \(2\lceil2\sqrt m\rceil+1\); find its radius by increasing an integer until its square reaches \(4m\). Every Euclidean division in this program is exact, including the step for generalized binomials of a negative integer. For polynomial construction the denominator \(d_i\), temporary coefficients, and the product preceding a binomial quotient have logarithms at most \((2m+2)(y+2)\). The final \(F^2G\) divides \(D_m\). The table \(p[c]\), \(F\) and \(G\) may be prepared once per arity. The following bill allows rebuilding them per coefficient.

Here is a simple translation and deliberately generous numerical bound. Store all program arrays and scalar counters in a single file with \(S=64W+128\) signed \(H\)-digit slots. The key bits, \(p[c]\), the list of at most \(W\) pairs, and the coefficient array take at most \(5W\) slots; fewer than 64 fixed scalar, index and temporary slots suffice for the displayed instructions. Obtain a unary ruler for \(W\) by copying the given key's extent and appending one cell. Its binary length minus one gives \(y\). Construct the \(H\)-digit ruler by eight enumerations of the \(W\)-by-\(W\) grid with \(y+2\) cells per pair. Lay out all \(S\) slots by copying and rewinding that ruler. Even charging \(64(H+4)\) operations per cell built, initialization costs at most \(2^{10}(S+1)(H+4)^2\). Length, index and loop counters are stored on tapes. Input and output words for the wide scalar use separate marked banks.

A short integer instruction may use three loads and one store. Form at most two scalar address offsets for an indirect array operand, charging them as separate arithmetic instructions. For a load or store start at the file origin and copy the index to a decrementing counter. Skip one complete slot and decrement until zero, transfer the chosen digits, and rewind both tapes. The cost is at most \(128(S+1)(H+4)\): a skipped slot's zero test, decrement, scan and testing cost at most \(70(H+4)\), and the return walk crosses no more than the same file. The controller uses the [single-symbol integer loops](../../contributions/explicit-overhead/modular-scalar-machine.mjs) for copies, signed addition/subtraction after magnitude comparison, and unsigned school multiplication or exact long division. Signs occupy a finite register/slot cell. A product has a \(2H+1\)-bit target, costing at most \(256(H+2)(2H+3)\); division uses at most \(160(2H+3)(H+3)\). Parity of a bitwise AND reads two words in parallel with one two-state parity flag. Any single comparison, branch/loop test, add, multiplication, exact quotient, bit operation, load/store or counter update in this register notation is thus realizable within \(8192(H+4)^2\) transitions including up to four file accesses, since \(S+1\le H\) for \(W\ge64\). The tapes for the double-width temporary, signs, condition and counters have fixed multiplicity. Head-free finite transitions can be folded into the symbol actions.

| Part | Number of charged integer instructions |
|---|---:|
| Radius, factorial, sign, initial key conversion and loop limits | \(64W^2\) |
| All \(p[c]\), four gap choices per count and their product | \(64W^2\) |
| All seed/label parities, shifted counts, defect tests and list insertion | \(64W^2\) |
| Per-row polynomial factors, descending coefficient updates and summation | \(128W^3\) |

For the last row there are at most \(W^3\) coefficient updates. Each uses at most two indexed reads, one indexed write, two products, one subtraction, at most six index calculation/check/update actions and two loop transfers. Clearing a row and multiplying its denominator across at most \(W\) factors use fewer than \(20W^2\) other instructions per distinguished index. The displayed 128 covers both and the two final scaled entries. In the seed loop a seed/label iteration has one parity-of-AND on the integer labels, one indexed key read, one parity update, one shifted-bit sum and fewer than ten address/counter/branch instructions. A generalized-binomial step uses two products, one signed exact division, two sums and fewer than twelve index, copy and loop actions. This proves, including the ruler and file setup, an upper bound

\[
             2^{24} W^3 (H+4)^2
\]

on physical transitions for one complete coefficient from its key, plus copying the two result words to their scalar homes, which already fits the slack. Signed matrix entries can be computed successively using this one file and one set of tapes. Summands at different data addresses need no common rank or subset. The [finite replay](walsh-repair-check.py) compares this compiler with an independent exact matrix inverse.

## Reading the actual frequency word

The binary source has \(d_0=m+D_F-1\le 2m\) pairs of slots, each of \(f\) bits, and common spectral coordinates \(X_{cj},Z_{cj}\). For each slot pair make a sequential pass over two copies of the current \(k\)-bit address. Starting each head at its designated slot, scan the \(f\) digits on the two heads in parallel, accumulating \(\sum_c X_{cj}Z_{cj}\pmod2\), and rewind. The active piece/slot is consecutive in the numerical caller. If the source strided variant is used, two monotone length-\(k\) masks enumerate the same column order with one pass per slot pair. The common auxiliary parity is computed once. XOR it into each of the \(m\) distinguished bits. This forms the true key in at most \(2^{12}W(k+2)\) transitions when the two masks per pair are supplied in slot order. One need not scan an \(f\)-column map of size exponential in \(A\). A general signed phase quadratic in the columns uses at most \(A^2+A+1\) such parity passes. [Actual frequency coordinates](https://github.com/openai/math/blob/3344da59991ed94f9ba711217b29c1d760badfa6/preprints/The-logarithmic-exponent-of-finite-Fourier-transforms-November-24-2026/build/kernel.tex)

To form the consecutive-slot masks, enumerate the \(k\) address positions for each slot and compare against its begin/end offsets. A school multiplication/division at \(k+1\) bits for every position even permits the stated regular strides, and costs less than \(2^{16}W(k+4)^3\) altogether. This is a setup cost for the current template position. At one data address a sequential scan through the complete table of these \(O(Wk)\) mask bits suffices. Within a quadratic phase, use at most \(A^2+A+1\) scans through this table if masks are needed out of order. When weighting a whole complete row, retain a current counter for its prefix and spectral address; copying and rewinding the counter fits \(64(k+2)\) per record at \(k\)-bit precision.

The arithmetic and frequency steps have a common physical accounting. At the global guard in [the width proof](walsh-aligned-denominators.md#width-at-the-integer-caller), \(H\le k^{1/3}\), and the physical record width obeys \(k\le K\le100k\) at the integer caller. One can charge \(2^{27}W^4 K\) transitions for a scalar application from the actual key, including building the coefficient, applying its sign, reading the frequency bits, clearing scratch and adding into a destination via one reduced modular addition. This follows from \((H+4)^2\le4k\), the numerical eleven-head program, and \(H+3\le W^4\). Quadratic phases fit this allowance too. Transfers between the relevant coarse array roles, complete layout changes, the count of ordinary steps and genuine spatial children have their separate invoices.
