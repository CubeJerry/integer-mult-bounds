# Literal radix padding obstructs a natural variable-template endpoint route

Status: **proved scoped negative result for a specified implementation**, independent of the weighted-search certificate barrier. It is not a lower bound on interchange or multiplication.

## 1. Exact source interface

At `openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`:

- Fourier `build/repair.tex`, `thm:repair` and `lem:matrix-root`, assigns every binary shift in `{0,1}^m` equally often and gives each shift an independent nonempty block. Its literal binary repair batch has at least `2^m` rows. Expansion in a scalar-extension basis can only increase the count.
- Tape `build/interchange.tex`, “Spectral conversion and the choice of constants”, uses repair width `R`, label count `N`, total width `W=RN`, and chooses one compatible **prime radix `b>W`** after fixing the template. Consequently `b>W>=2^m` for this literal family.
- The final paragraph of `thm:interchange` changes binary fields of width `u` to radix-`b` fields, taking the least `e` with `b^e>=2^u` and padding both address ranges to `b^e`. The volume becomes
  \[
  V_{\rm pad}=V\left(\frac{b^{\lceil u/\log_2b\rceil}}{2^u}\right)^2. \tag{P1}
  \]
  The paper's bound `b^2 V` is valid with fixed `b`, but is not uniform in a growing template.

The result below concerns **literal materialization** of the complete padded grid, one record per address. Encodings that avoid storing these entries, different binary interfaces, and length-dependent radices with separately proved costs are outside its scope.

## 2. A finite interval lemma

For integers `b>=2,u>=0`, put

\[
 P_b(u)=b^{\lceil u/\log_2 b\rceil}/2^u.
\]

**Lemma P1.** On any consecutive integer interval `u_0,...,u_0+D`, `D>=0`,

\[
 \max_{0\le h\le D}P_b(u_0+h)\ge\min(2^D,b/2). \tag{P2}
\]

No irrationality or equidistribution hypothesis on `log_2 b` is needed.

**Proof.** Write `e(u)` for the least nonnegative integer with `b^e>=2^u`. If it is constant on the interval, the ratio drops by exactly `2^D` between endpoints, and its final value is at least one. Otherwise some adjacent `u,u+1` have `e(u+1)>=e(u)+1`, giving

\[
 P_b(u+1)\ge(b/2)P_b(u)\ge b/2.
\]

One of the two cases holds. ∎

Two-field volume inflation is therefore at least `min(4^D,b^2/4)` somewhere in the interval. If radices and the lengths of the intervals on which they remain fixed both tend to infinity, full-grid padding has no common linear-space constant.

## 3. Power-selected arities

Consider `m(u)=floor(u^(1/r))` for a fixed integer `r>=2`. Each `m` selects one fixed template and radix `b_m>W_m>=2^m`. At every selected input width, execute the source's binary-to-radix padding literally.

**Theorem P2.** For every `m>=2`, some integer `m^r<=u<=(m+1)^r-1` has padded volume at least `4^(m-1) V`. Thus the scheme fails a uniform `O(V)` visited-cell bound.

**Proof.** The interval diameter is

\[
 D=(m+1)^r-m^r-1\ge2m\ge m-1.
\]

Every width selects the same radix. Lemma P1 makes the two-field inflation at least

\[
 \min(4^D,b_m^2/4)\ge4^{m-1}.
\]

Materializing that many padded records visits that many cells, up to a fixed record-format factor. As `m` is unbounded, no common linear constant exists. All spectator ranges may be set to one. ∎

This rules out transplanting the **literal fixed-radix binary padding** into this natural power-selected scheme while retaining common linear space. It is independent of recursive call counts, coefficient choices or fast template generation. The paper's abort-and-chunk wrapper still preserves its own common cap; this result does not lower-bound its actual runtime or assert that capped attempts succeed at all lengths.

### Sparse-menu coverage

**Proposition P2b.** Let `U>=1`, `1<=M<=U`, and fix a padding cap `C>=1`. A menu of `K` radices with `log_2 b_i>=M` can have one-field padding at most `C` at no more than

\[
 K(\lfloor c\rfloor+1)
 \left(\left\lfloor\frac{U+c}{M}\right\rfloor+1\right),
 \qquad c=\log_2 C, \tag{P2b}
\]

integer widths in `[U,2U]`.

**Proof.** For one radix let `ell=log_2 b`. A good width must have a multiple `h ell` in `[u,u+c]`, and hence lies in `[h ell-c,h ell]`. Relevant multiples lie in `[U,2U+c]`; there are at most `floor((U+c)/ell)+1`. Each interval contains at most `floor(c)+1` integers. Sum over the menu and use `ell>=M`. ∎

For fixed `C` and `M=Theta(U^beta)`, `0<beta<1`, a menu of `K=o(M)` high-arity source templates covers only `o(U)` widths. A logarithmic-size menu therefore cannot guarantee bounded literal padding at all widths in that block if every source arity is at least a fixed positive multiple of `U^beta`. This is an admissibility-coverage obstruction only. Larger menus, other representations, input-dependent radices, chunking and slower candidates outside the high-arity set are outside its scope.

## 4. First-digit batch padding is a different loss

The source also splits the first radix digit's `b` values into batches of `W`. That step has factor

\[
 \rho=W\lceil b/W\rceil/b<1+W/b. \tag{P3}
\]

For any prescribed `0<delta<1`, choosing a compatible prime `b>=W/delta` makes `rho<=1+delta`. Compatibility excludes finitely many prime divisors of nonzero rational numerators and denominators, so arbitrarily large compatible primes exist. Trial-division search terminates; **no useful bound on its cost is asserted here**.

Let `C_main(m)` be the template's exact main-call count divided by `W`, and `a` its reserve width. Its recursive-volume invoice improves from the paper's convenient bound `2 C_main+2a` to

\[
 B=\rho C_{\rm main}+2a. \tag{P4}
\]

The main calls each have relative volume at most `rho/W`; the `2a` reserve calls each use full parent volume. With effective width arity `M=m+2a`, suppose

\[
 C_{\rm main}\le\sqrt m(1+\epsilon_m),\quad \epsilon_m\ge0,
 \qquad a\le C m^{1/2-\tau},\quad \tau>0.
\]

Then

\[
 B/\sqrt M\le(1+\delta)(1+\epsilon_m)+2C m^{-\tau}. \tag{P5}
\]

This uses only `sqrt(M)>=sqrt(m)`. The source's width rounding `f=floor((e-1)/M)` further decreases the normalized mass.

Thus the factor two is not intrinsically an endpoint barrier. A near-critical main computation, a small first-digit padding slack and a sub-square-root reserve would make these particular losses summable. Increasing `b` does not remove Theorem P2's binary padding obstruction, and can increase description, conversion and symbol-representation costs.

The source proves `a=D-2=O_p(m^((2p-1)/p^2))` after its stated choice of `q`. For any **fixed** odd prime `p>=5` the exponent is below `1/2`, so reserve calls alone give a decaying term in (P5). This does not establish near-critical main calls: routing incidences and repair stages remain. If `p` grows with `m`, the `O_p` constants need joint bounds and are not made uniform here.

## 5. Consequential next obligation

A variable-template endpoint route must replace full binary-to-radix padding, retain a bounded radix through a different construction, or supply a compressed representation with all access costs charged. A different input-dependent template/radix selector is also outside Theorem P2, but needs its own complete all-length space and time proof. Improving only the recursive exponent, main-call ratio or first-digit batch factor cannot solve this obligation for the specified power-selected family.

Prepared for @CubeJerry with substantial OpenAI AI assistance. The source construction and fixed-template proof remain credited to the pinned OpenAI manuscripts. The new claim here is the scoped all-length padding obstruction and its distinction from first-digit batching.
