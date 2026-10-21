# A sharp right-vector cost gap in F2[S3]

This is a written proof in a specified finite group-algebra model, with
executable corroboration. It is not a proof-assistant certificate or a proof
of the multiplication theorem. **No new κ.**

## Statement and cost model

Let `K = F2`, `R = K[S3]`, and use two active registers. A paid factor is

\[
F=I+u y^T,\qquad u\in R^2,\quad y\in K^2.
\]

Every element of `GL2(K)` is free, including maps before, between and after
paid factors. There are no extra registers. This is the right-vector
alphabet of Wentao Li's #4099 and Nick Petalas's #4243/#4265. In particular,
`u` may contain arbitrary group-algebra sums; a factor is **not** asserted
to be one native rank-one supplier call. Ring-valued right vectors and
ring-valued free changes of basis are outside the model.

Define `cost(M)` as the least paid-factor count and

\[
\delta(M)=\min_{T\in GL_2(K)}\dim_K (MT-I)K^2.
\]

We construct an invertible, non-diagonal `M` with

\[
\boxed{\operatorname{cost}(M)=3>2=\delta(M).}
\]

The matrix-algebra target used below is the one in #4265. The new parts are
the explicit full-ring lift, the geometric two-factor exclusion, and a
literal faithful regular-action circuit. No novelty is claimed for the
matrix-algebra counterexample, the right-vector alphabet, the column lower
bound, or the usual three-XOR interchange identity.

## 1. Explicit product decomposition

Write permutations by their images of `0,1,2`, compose right to left, and
order the formal group basis as

\[
(012,021,102,120,201,210)=(1,s,as,a,a^2,a^2s),
\]

where `a = (120)` has order three and `s = (021)` has order two. The relation
is `sas = a^-1`. The assignment seed 01 selects `s`, the first nonidentity
lexicographic permutation, as the presentation's involution.

Let `π:R -> K[C2]` be induced by permutation parity. Let
`ρ:R -> M2(K)` be the natural action of `S3 = GL2(K)` on the three nonzero
vectors `(1,0), (0,1), (1,1)`, in that order. On the ordered basis:

| permutation | π | ρ (rows separated by `;`) |
|---|---|---|
| 012 | 1 | `1 0; 0 1` |
| 021 | s | `1 1; 0 1` |
| 102 | s | `0 1; 1 0` |
| 120 | 1 | `0 1; 1 1` |
| 201 | 1 | `1 1; 1 0` |
| 210 | s | `1 0; 1 1` |

Both are unital algebra homomorphisms. Set

\[
e=1+a+a^2,\qquad f=1+e=a+a^2.
\]

The conjugacy-stable order-three subgroup makes `e` central; directly
`e^2=e`, `f^2=f`, and `ef=0`. The images of `e` and `es` under `(π,ρ)`
are `(1,0)` and `(s,0)`. The following four elements have images `(0,Eij)`:

| element | formal sum | six-bit mask |
|---|---|---:|
| j(E00) | `1 + s + a + a²s` | 43 |
| j(E01) | `as + a + a² + a²s` | 60 |
| j(E10) | `s + as + a + a²` | 30 |
| j(E11) | `1 + s + a² + a²s` | 51 |

These six images form a basis of `K[C2] × M2(K)`. Domain and codomain both
have dimension six, so `(π,ρ)` is an algebra isomorphism. In particular,
the inverse matrix-block map `j` is multiplicative and has identity `f`,
not the full-ring identity `1`. Thus `j(Eij)j(Ekl)=δjk j(Eil)`.
This argument establishes the decomposition directly; it does not invoke
a semisimplicity assumption in characteristic two.

Put `α=j(E01)` and `β=j(E10)`. The relations needed below are
`αβα=α`, `βαβ=β`, and `αβ+βα=f`.

## 2. The complete three-factor word

Define

\[
A=\begin{pmatrix}1&\alpha\\0&1\end{pmatrix},\qquad
B=\begin{pmatrix}1&0\\\beta&1\end{pmatrix}.
\]

Their right-vector parameters are respectively `u=(α,0), y=(0,1)` and
`u=(0,β), y=(1,0)`. Both are involutions. Direct multiplication gives

\[
M=ABA=
\begin{pmatrix}1+\alpha\beta&\alpha\\
\beta&1+\beta\alpha\end{pmatrix}
=\begin{pmatrix}e+j(E_{11})&j(E_{01})\\
j(E_{10})&e+j(E_{00})\end{pmatrix}.
\]

Its four formal masks are `(42,60,30,50)`. The quotient images are

\[
\pi(M)=I_2,\qquad
\rho(M)=P=\begin{pmatrix}E_{11}&E_{01}\\E_{10}&E_{00}\end{pmatrix}.
\]

As a `4 × 4` binary matrix, `P` exchanges coordinates 0 and 3 and fixes
coordinates 1 and 2. Hence `P^2=I`, and the full-ring isomorphism also
gives `M^2=I`. Both active registers may be arbitrary on entry. There is
no zero-initialized helper, borrowed spectator, residual component or
free map in this word. This proves `cost(M) <= 3`.

The `e` terms are essential. Omitting them leaves the same `ρ` image but
sets the entire `π` component to zero. On two regular six-bit banks this
wrong target has rank eight instead of twelve. A check in `M2(K)` alone
would fail to see the lost four-dimensional component.

## 3. Geometric exclusion of every two-factor word

First normalize all free maps to the right. For `S in GL2(K)`,

\[
S(I+uy^T)S^{-1}=I+(Su)(y^TS^{-1})
\]

is again a paid factor. Therefore a word with at most two paid factors is
`F1 F2 S`, padding by an identity paid factor if necessary. This is the
normalization in #4243, repeated here to specify the exact boundary.

Project such a word with `ρ` and view each image as a binary `4 × 4`
matrix. A factor has form `I4 + U(y^T tensor I2)`. For nonzero `y`, it fixes
pointwise one of the following two-dimensional planes in `K^4`:

\[
H_A=K^2\oplus0,\quad H_B=0\oplus K^2,\quad
H_C=\{(v,v):v\in K^2\}.
\]

The identity factor can be assigned any one of them. Distinct planes in
this list intersect only at zero. A free map `S tensor I2` permutes the
three planes.

Suppose `P=F1 F2 (S tensor I2)`. Since `P` and `S tensor I2` are invertible,
both projected factors are invertible. Let `Fi` fix `Hi` from the list.
Writing `Q=P(S^-1 tensor I2)=F1F2`, we have

\[
\dim(QH_2\cap H_1)
=\dim(F_1H_2\cap F_1H_1)
=\dim(H_2\cap H_1)\in\{0,2\}.
\]

But `P` sends each of the three planes to a plane meeting **every** listed
plane in dimension one. The following table gives the nonzero vector in
each intersection (row is `H`, column is `P H'`). Here `ei` are standard
coordinate vectors of `K^4`.

| | P HA | P HB | P HC |
|---|---|---|---|
| HA | e1 | e0 | e0+e1 |
| HB | e3 | e2 | e2+e3 |
| HC | e1+e3 | e0+e2 | e0+e1+e2+e3 |

The free `S^-1` only permutes the columns of this table. Thus
`dim(Q H2 intersect H1)=1`, a contradiction. This excludes all words of
length at most two, including every placement of free maps and every
choice of ring-valued `u`. It is a written geometric proof, not an
inference from failure to find a short word. Together with the explicit
word, it proves `cost(M)=3`.

## 4. The column lower bound is exactly two

The domain of `(MT-I):K^2 -> R^2` has dimension two, so `δ(M) <= 2`.
Suppose a nonzero `x in K^2` belongs to its kernel for some invertible
`T`. Projection gives

\[
P((Tx)\otimes I_2)=x\otimes I_2.
\]

The two columns of these `4 × 2` matrices span two members of the same
three-plane list. The equality would make `P` send a listed plane onto a
listed plane, contradicting the one-dimensional intersections above.
Thus the kernel is zero for every `T`, proving `δ(M)=2`.

## 5. Literal bit realization and limits of its bill

On a regular bank with one bit per group element, a coefficient `γ`
acts by left convolution. Emit `dst[g*h] ^= src[h]` for every supported
group element `g` of `γ` and every address `h`. The source and destination
banks are distinct at each factor, so these are legal in-place XORs and
need no temporary bank. Both `α` and `β` have four supported elements.

The complete `A,B,A` realization therefore uses twelve translated-bank
XORs, or **72 scalar XORs**, with 72 source-bit reads, 72 destination-bit
reads and 72 destination-bit writes. The six-entry address permutations
are compile-time constants. There are no additional frame changes,
copies, allocations, recursive children or cleanup in this finite
random-access bit-circuit model. Executing the inverse to restore the
two **active output banks** is a different requested endpoint and costs
another three paid factors / 72 XORs; it is not free.

The 72-XOR realization is a constructive upper bound, not a minimum.
It does not price routing on fixed tapes, native supplier source maps,
large-parameter frame realization, hosting, precision, or a recursive
moment. Those costs remain uninstantiated, not zero. The formal
three-factor optimum cannot be substituted for three rank-one supplier
children. No diagonal supplier target, selected bit word, outer assembly
or multiplication exponent is changed.

## Credit

Nick Petalas's #4265 supplies the matrix target and explicitly asks for
its lift to `F2[S3]`; #4243 supplies the free-basis normalization and
question. Wentao Li's #4099 supplies the right-vector alphabet and column
bound, following #2513's cyclic-root work. Their exact source pins and
retained original text are in `SOURCES.json` and `references/`.

New lift, proof and implementations prepared for **@CubeJerry** with
substantial **OpenAI Codex assistance**. Both implementations have the
same AI-assisted authorship; separate algorithms are not independent
human review. Apache-2.0.
