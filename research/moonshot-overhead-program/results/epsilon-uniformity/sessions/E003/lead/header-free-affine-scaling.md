# Header-free rational scaling on tapes

Status: **written component proof, independently reviewed by Route A**.
The exact finite replay and separate review are recorded in
`../route-a/REVIEW-HEADER-FREE-SCALING.md`; neither is a full tape-machine
execution or formal refinement.

This strengthens the space bound of E002's height-priced affine stream
theorem (HS). Source: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`,
November `interchange.tex`, the elementary ordered-affine interface, and
E002 `route-a/HEIGHT-PRICED-AFFINE-STREAMS.md`. Euclidean floor sums and
stable radix sorting are standard; the contribution is their header-free
composition with that run decomposition. This is not a multiplication theorem.

## 1. Statement

An arbitrary finite-alphabet array occupies `[P] x [Q] x [B]` in
lexicographic order, with `V=PQB`. Positive integer descriptors are binary.
Let `c` be a nonzero integer coprime to `Q`, and
`h=ceil(log2(2+|c|))`.

**Theorem HFS.** One fixed deterministic finite-alphabet multitape program
implements `(p,y,t) -> (p,c*y mod Q,t)` and its inverse in

\[
 O(V(1+h)^C)\text{ actual steps},\qquad
 O(V)+(1+h+\log(2V))^C\text{ cells ever visited},                 \tag{1}
\]

for an absolute integer `C`. The constant multiplying `V` in the space
bound is independent of all parameters. A rational unit `c/d` has the
same conclusion with its combined numerator/denominator height, by
composition. Coefficient preparation and additive control space are
charged; there is no free random access or empty address field.

## 2. Euclidean counting and selection

For nonnegative `N,A,B` and positive `M`, define

\[
 S(N,M,A,B)=\sum_{v=0}^{N-1}\lfloor(Av+B)/M\rfloor.              \tag{2}
\]

Reduce `A,B` modulo `M`, adding
`floor(A/M) N(N-1)/2 + floor(B/M) N` to the answer. For `0<=A,B<M`,
put `Y=AN+B`. If `Y<M`, the residual sum is zero. Otherwise `A>0` and

\[
 S(N,M,A,B)=S(\lfloor Y/M\rfloor,A,M,Y\bmod M).                 \tag{3}
\]

Proof: the left side counts pairs `0<=v<N`, `1<=z<=(Av+B)/M`.
Put `N'=floor(Y/M)`, `B'=Y mod M`, `v'=N'-z`, `z'=N-v`.
The new inequality is `1<=z'<=(Mv'+B')/A`, with `0<=v'<N'`.
Conversely its upper bound is less than `N`, because
`Mv'+B'<=AN+B-M<AN`. These substitutions are inverse bijections.

The reduced moduli follow the Euclidean algorithm. For inputs bounded
by `2^{O(h)}`, all registers have `O(h)` bits, and schoolbook bit arithmetic
gives polynomial time and space in `h`; conservative bounds `O(h^4)`
time and `O(h^2)` space suffice. For `0<=R<=M`,

\[
 C_R(N;M,A,B)=\#\{v<N:(Av+B)\bmod M<R\}
 =N+S(N,M,A,B)-S(N,M,A,B+M-R).                                  \tag{4}
\]

The difference of the latter two floors indicates a residue at least `R`.
The formula includes `R=0` and `R=M`.

## 3. Header-free stable sorting of modular keys

There are `a>=2` equal-length run records, initially indexed by `r in [a]`.
Their implicit destination keys are `t_r=kappa*r mod a`, where
`gcd(kappa,a)=1`. Write `lambda=kappa^{-1} mod a`.

After `k` stable least-significant-bit passes, order is increasing
`t_r mod 2^k`, and increasing original `r` within a tie. To reconstruct
the original position from its current bucket and ordinal, put `d=2^k`.
Bucket `b in [d]` contains keys `t=b+d v<a`; its size is zero for
`b>=a` and otherwise `N_b=1+floor((a-1-b)/d)`. Its original positions are

\[
 r_v=(\lambda d\,v+\lambda b)\bmod a,\qquad v\in[N_b].          \tag{5}
\]

They are distinct. For ordinal `s in [N_b]`, binary search for the least
`R in [1,a]` satisfying

\[
 C_R(N_b;a,\lambda d\bmod a,\lambda b\bmod a)\ge s+1.           \tag{6}
\]

Then `r=R-1` and `t_r=kappa*r mod a`. Equations (4)--(6) reconstruct
each key in polynomial `log a` actual steps and control space.

At pass `k`, enumerate buckets and ordinals in their physical order,
reconstruct each key, and copy its whole run to output stream 0 or 1
according to bit `k`. Concatenate within each prefix fiber. Stable
partition preserves the invariant. After `ceil(log2 a)` passes all
keys are sorted. The total number of examined buckets is less than `2a`,
so empty buckets cost at most another polynomial `log a` per existing
run. No array of keys, counts or original positions is stored. The same
algorithm with multiplier `lambda` sorts inverse keys.

## 4. Applying the sorter to scaling

For `Q=1` the operation is the identity. Otherwise reduce positive `c`
to `1<=a<Q`; `a=1` is trivial. Write `Q=aq+s`,
`q>=1`, `0<=s<a`. E002's exact contiguous runs are

\[
 y_r=\lceil rQ/a\rceil,\quad t_r=(-rQ)\bmod a,\quad
 \ell_r=y_{r+1}-y_r=q+1_{t_r<s},\qquad r\in[a],
\]
\[
 a(y_r+k)\bmod Q=ak+t_r\quad(0\le k<\ell_r).                  \tag{7}
\]

Here `kappa=-Q mod a` is invertible. Scan each original run and pad it
to `q+1` whole `B`-symbol blocks. Sort these equal-length records by
their implicit `t_r` without headers. Pad `a` to the next power of two
`A<2a`, then transpose `[A] x [q+1]` by `ceil(log2 a)` ordinary
one-bit field moves. The padded payload is less than

\[
 PA(q+1)B<4PQB=4V.                                             \tag{8}
\]

Discard rows `t>=a` and, in the last column, entries `t>=s`. The retained
order `ak+t` is exactly increasing target address by (7). Positions,
not data values, determine all padding deletion.

The inverse inserts the same dummy positions, undoes the bit-field moves,
removes dummy rows and sorts the remaining records by `r=lambda*t mod a`
using the inverse header-free sorter. In original run order remove the
last dummy block when `t_r>=s`. Negative `c` adds the source's negation
permutation. Rational units compose these forward and inverse operations.

## 5. Actual costs and cells ever visited

A fixed number of payload arrays of length at most `4V` occupy fixed
reused regions. Each stable pass moves `a(q+1)B` payload cells per prefix
and makes at most `a` key reconstructions. Since `a<=Q` and `B>=1`, their
cost is `V poly(1+h)`. The `O(h)` passes and bit-field moves retain this
form. Initial arithmetic on `h+log Q` bits fits the same bound, using
`(log(2V))^d<=C_d V` for any fixed arithmetic degree `d`.

Low-end binary counters have amortized constant cost per scanned cell.
Resetting a record counter costs `O(log(2(q+1)B))`, paid by that record.
Long prefix counters are advanced and tested rather than fully read per
run. The modular arithmetic registers depend only on `h`. Other control
and descriptor scratch has a fixed polynomial size in `h+log(2V)`.
Rewinds and erasures are charged to scans, and all prefixes and passes
reuse the same absolute regions. This bounds the union of visited cells
and proves (1), rather than merely a live-memory bound.

For a lower-triangular rational map on `D` fields of height at most `H`,
sequential source one-control shifts and HFS scalings consequently use
time `V poly(D,H)` and space `O(V)+poly(D,H,log(2V))`, provided their
polynomial-size finite instruction list is prepared and accessed with
that bill. General rational maps retain the source's paid permutation
calls. No additional interchange is concealed in this corollary.

## Scope, open question and credit

This removes the `h V` header-space factor of one concrete operation.
Other module rows, scalar encodings, numerical records, padding and parked
recursive arrays still require separate proofs. In particular, an efficient
interchanger alone does not establish an efficient Walsh caller or multiplier.
The next question is joint composition with the succinct scalar executor
and a compatible common radix without increasing recursive child volumes.

Credit: @CubeJerry, OpenAI's tape-stream lemmas, E002's run decomposition
and height-priced scaling, classical Euclidean floor sums and stable radix
sorting, and substantial AI-assisted E003 work. No literature-priority or
full-machine verification claim is made.
