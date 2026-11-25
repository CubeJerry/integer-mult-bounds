# Variable local arity with a charged tape recurrence

Status: **new recurrence and proposed physical composition, awaiting
independent review**. Admission requires the sharper space proof in
variable-interchanger-space.md and the numerical/outer source audit.

This changes the local template during recursion. The two schedules
differ because numerical Walsh column changes call the already-proved
interchanger. Source pin: OpenAI math
3344da59991ed94f9ba711217b29c1d760badfa6, November tape interchange.tex,
walsh.tex, permutations.tex and integers.tex. Programme predecessors:
characteristic-two-label-geometry.md, growing-arity-circuit-candidate.md,
and fixed-field-extraction-theorem.md. Suppliers: E002 compact execution
components, composite-radix-padding.md and polynomial-walsh-precision.md.

All logarithms are binary. Put
\[
 \Phi(y)=(y+1)^{2/3}(\log_2(y+2))^{1/3}.
\]

## 1. Input-to-radix interface

At binary width u, a template at odd m has batch width W, rational-unit
product Q and reserve dimension \(a=D_m-2\), with
\(\log Q,\log W\le m^{C_0}\) and \(D_m=m^{o(1)}\).
The composite-radix construction selects H,e,b by integer arithmetic:
\[
 e=\lfloor u/H\rfloor,\quad b>W,\quad \log b=O(H),\quad
 1\le b^e/2^u\le1+1/[4(u+1)].                       \tag{V1}
\]
Use the source one-leading-digit partition, with
\[
 f=\left\lfloor{e-1\over m+2a}\right\rfloor,\qquad
 v=\lceil\log_2(b^f)\rceil\le u/m+2.                 \tag{V2}
\]
Test \(f\ge1\) and all source guards. Present the raw child fields on
two complete binary ranges of width v, paying a factor less than four
in their total payload. The child chooses its own radix and discards
its known padding on return. Occupied reserves are restored.
For all sufficiently large u under the chosen polynomial-arity schedule,
\(a\le m/2\), \(\log b\le2H+2\), and \(u\ge32m(H+1)\).
The floor in V2 then also gives
\[
 f\log_2 b\ge u/(m+2a)-2\log_2b\ge u/(4m).
\]
Retain this lower-width guard as an exact integer test if needed.
It supplies the long complete target fibres used to amortize rational
run headers in the companion space proof.

Moving a b-valued digit directly costs O(V log b): pad that coordinate
to a power of two, use ordinary binary split/merge moves, and delete
padding after the complete move. Two-coordinate temporary volume is
less than four. Neither these moves nor height-priced rational maps
have a polynomial-in-numeric-b toll.

## 2. Exact interchange: polynomial local arity

Choose one sufficiently large fixed integer M and use
\[
 m(u)=2\left\lfloor{\lfloor u^{1/M}\rfloor\over2}\right\rfloor+1.
                                                               \tag{V3}
\]
Integer comparisons compute the root. Thus \(m=\Theta(u^\gamma)\),
\(\gamma=1/M\). Choose the distance by integer rounding at
\((\log m/\log\log m)^{1/3}\). The accepted geometry and completed
four-child repair give actual normalized recursive mass
\[
 \Lambda_m\le C\sqrt m\,2^{C\Phi(\log m)}.             \tag{V4}
\]
C includes child binary padding, leading padding, the larger predictor
window and all reserve calls. Grouping module rows preserves mass.

Keep one root coefficient field E of bit degree \(s=O(\log(U+2))\).
Choose its F4 generator once by testing
\(\omega^2+\omega+1=0\); enumerating the root field costs polynomial
in the root m and is part of finite preparation.
It supplies enough check nodes for every smaller m; no child embeds
the payload again. Polynomial(m,s) arithmetic, row sorts, grouped
comparison labels, height-priced maps, dispatch and head returns give
a complete ordinary local bill \(C m^K s^K V\).

Every child at one spatial depth has the same v in V2. Prepare the
finite width/parameter/radix chain once at the root and reuse compact
plans; validate and discard optional expanded archives. Taking M
larger than all finite compiler degrees makes whole-chain preparation
\(2^{U^\eta}\operatorname{poly}(\log(2V))\) for a fixed eta<1.
Since \(V\ge2^{2U}\), this is additive O(V) work and space.

Time per encoded bit volume, omitting absorbed preparation, satisfies
\[
 I_s(u)\le C m^K s^K+
   C\sqrt m\,2^{C\Phi(\log m)}I_s(v),\quad v\le u/m+2.
                                                               \tag{V5}
\]
Direct bit moves handle bounded u, failed guards and
\(u<K\log_2(s+2)\). Fix M with \(\gamma K<1/4\), including all shape
degrees. Above the base, \(v\le u^{1-\gamma/2}\).
After dividing by \(\sqrt{u+1}\), the local term is at most \(Cs^K\);
the recursive factor is at most \(2^{C'\Phi(\log(u+2))}\).

The logarithmic widths \(y_i=\log_2(u_i+2)\) decrease geometrically,
so
\[
 \sum_i\Phi(y_i)\le C_\gamma\Phi(\log_2(U+2)).         \tag{V6}
\]
Bound their logarithmic factors by the root's and sum the geometric
\(y_i^{2/3}\) terms. Depth, terminal direct cost and one-time field
embedding are polynomial in log U. Iteration proves the proposed
uniform exact-interchange time
\[
 \operatorname{Time}_I(U,V)
 \le V\sqrt{U+1}\,2^{C\Phi(\log_2(U+2))}.             \tag{V7}
\]
The separate refined-space proof must supply
\[
 \operatorname{Space}_I(U,V)\le
 V\,2^{C\Phi(\log_2(U+2))}.                          \tag{V8}
\]
The older \(m^K V\) space estimate would not suffice.

## 3. Walsh needs a slower arity schedule

A numerical node calls the completed interchanger for its column
changes. Taking \(m=a^\gamma\) would give a local \(m^K\sqrt a\)
toll and already lose a fixed power. The predecessor's arithmetic-only
recurrence does not price these tape column changes.

For even active width a put \(y=\lceil\log_2(a+2)\rceil\),
\(\ell=\lceil\log_2(y+2)\rceil\). Let h be the largest integer with
\(h^3\le y^2\ell\), and set \(m(a)=2^h+1\). Thus
\(\log m=\Theta(\Phi(y))\) and \(m=a^{o(1)}\).
The rational template has
\[
 2m\le A_m\le4m,\quad W_m\le m^{C_1},\quad
 {\sigma_m\over W_m}\le
 C\sqrt m\,2^{C\sqrt{\log(m+2)\log\log(m+4)}}.        \tag{V9}
\]
Its exact W_m is a power of two. Take f as the largest even integer
at most \(a/A_m\), apply the template to Af bits, and transform the
even remainder \(a-A_m f<2A_m\) by direct four-point butterflies.
This has polynomial-m ordinary cost. Odd widths add the source's
one direct normalized butterfly; bounded widths use direct transforms.
Above a fixed threshold, logarithmic child width satisfies
\[
 y_{\rm child}\le y-c\Phi(y)                         \tag{V10}
\]
for an absolute c>0. Integer rounding and the remainder are paid.

## 4. Actual batching, precision and local Walsh costs

For N=2^k records and selected width \(a\le c_0 k/\log(2+k)\), the
source initially gathers the selected bits, leaving q=2^(k-a) leading
spectator rows. Along the deterministic active-width chain,
\[
 \sum_i\log W_{m_i}\le C\sum_i\log m_i
                  \le C'\log(a+2).                 \tag{V11}
\]
The last inequality telescopes \(f_i\le a_i/(2m_i)\). The entire
leading batch divisor is therefore at most \((a+2)^{C'}\). For large
k it is at most q, and, since both are powers of two, divides q.
Preflight tests this exact divisor. No multiplicative leading padding
is hidden at successive levels. Failed shape tests use correct direct
Walsh, and occur only below a fixed threshold.
The initial gather and final undo are paid once at the selected-layer
root using the full address width k. Internal calls receive one already
contiguous f-bit slot with prefix/gap/suffix descriptors; they do not
repeat a permutation of all k positions. Their local column changes
therefore use fields of width at most a, as required by V12.

The on-demand rational table has polynomial-m heights and operation
count. Exact short-rational scaling on an O(k)-bit grid costs
polynomial(m)*k; general short products use the source O(k log k)
routine. Polynomially many column changes use V7--V8, including
packed XOR and bit-position wrappers. Their full one-level cost is
\[
 V m^K\sqrt{a+1}\,2^{C\Phi(\log_2(a+2))}
              (1+\log(2+k))^K,                     \tag{V12}
\]
and their space is at most
\[
 V m^K\,2^{C\Phi(\log_2(a+2))}.                      \tag{V13}
\]
These bills include movement, temporary field encoding/decoding,
coefficient generation, dispatch and metadata removal before children.

The local logarithmic norm gain is polynomial(m). Along a path it is
at most
\[
 O(\log k)\,2^{C\Phi(\log_2(k+2))}=k^{o(1)}.          \tag{V14}
\]
Branches per template are polynomial m. V11 bounds the complete
arithmetic-node count per independent spatial record by polynomial k.
The source common-ancestor error argument, input norm \(2^{Lk}\),
and required absolute error \(2^{-Dk}\) consequently need only absolute
O(k) integer and fractional bits above a fixed threshold.
A block-diagonal spectral map uses its maximum block norm, not the
number of spectral cases times that norm.
The actual plan computes an upper bound on the sum of local logarithmic
gains and on the logarithmic node count, and requires it to be at most
a fixed fraction of k. Choose fixed precision margins for L,D and this
allowance. A failed precision guard invokes the direct normalized Walsh
routine, whose butterfly norms and O(k) precision are independently
bounded. V14 proves eventual success uniformly over all a<=k; no
uncomputable threshold is used to choose a format.

The Walsh template setup is \(2^{k^{o(1)}}\), even if optional exponential
validation runs once per distinct width:
\(\max m^K=2^{O(\Phi(\log k))}=k^{o(1)}\), and V11 bounds the
number of physical node types. This is absorbed by N=2^k.
Only compact executable descriptions are retained. Interchanger
invocations also have the fixed-power preparation from Section 2:
at root width U<=k this can be \(2^{k^\eta}\), for a fixed eta<1,
and cannot be relabelled \(2^{k^{o(1)}}\). There are polynomially many
numerical calls after V11 and polynomial-m ordinary operation counts.
Allowing repeated interchange preparation at all of them gives the
safe combined bound \(2^{k^{\eta'}}\), for a fixed eta<eta'<1 and
all sufficiently large k. It remains absorbed by N=2^k.

## 5. Solve the actual numerical recurrence

Divide time by \(V\sqrt{a+1}\), keeping the common
\((1+\log(2+k))^K\) factor. A monotone envelope F at logarithmic
active width y satisfies
\[
 F(y)\le2^{C_2\Phi(y)}
       +2^{C_3\Psi(y)}F(y-c\Phi(y)),\quad
 \Psi(y)=(y+1)^{1/3}(\log_2(y+2))^{2/3}.             \tag{V15}
\]
Here \(\log(m^K)=O(\Phi(y))\) is in the local term, while
\(\sqrt{\log m\log\log m}=O(\Psi(y))\) is in the recursive term.

For large y,
\[
 \Phi(y)-\Phi(y-c\Phi(y))\ge c'\Psi(y).               \tag{V16}
\]
Indeed \(\Phi'(t)\) is at least an absolute positive multiple of
\(t^{-1/3}(\log(t+2))^{1/3}\); the interval has length c Phi(y),
and lower endpoint at least y/2. Choose a constant B larger than
C2 and C3/c', increase the bounded base, and substitute
\(F(y)\le2^{B\Phi(y)}\). V16 absorbs the recursive term with strict
slack for the additive term. This is an inductive majorant, not only
an integral estimate.

The resulting proposed selected-bit Walsh bounds are
\[
 \operatorname{Time}_W\le
 V\sqrt{k+1}\,2^{C\Phi(\log_2(k+2))},\qquad
 \operatorname{Space}_W\le
 V\,2^{C\Phi(\log_2(k+2))}.                          \tag{V17}
\]
Visible fixed powers of log k fit the exponential. Numerical children
have volume 1/W_m, W_m>=2, so parked arrays sum geometrically using
the largest local coefficient in V13. Finite repair retains its
strict volume contractions. Siblings reuse the same marked intervals.

## 6. Outer transfer and actual common cap

The outer permutations, short transforms and integer assembly are now
supplied by two independent source-specific substitutions:

- Route A, ../route-a/VARIABLE-OUTER-SUBSTITUTION.md, including its
  local-active-width supplement; snapshot SHA-256
  782ccc6677a2343a7797eaf72c4e27c50b25b722d4ec4fd2207a2ccba0408602.
- Route C, ../route-c/variable-arity-outer-transfer.md; snapshot SHA-256
  f619af12d0cca53531049b2ba4aa6e0d3024c1abc9eba1e2d8f3c795cbd4eb0b.

They retain every fixed power of log k and separately use the exact
interchanger and numerical Walsh suppliers. Route B also checked the
A substitution against the full source in
review-variable-outer-substitution.md. With V7/V8/V17, these outer
proofs give the digit profile
\[
 \tau(v)\le v\sqrt{L(v)}\,2^{C\Phi(\log_2L(v))},\quad
 \operatorname{space}(v)\le v\,2^{C\Phi(\log_2L(v))}.
                                                               \tag{V18}
\]
This clause depends on those source substitutions and does not assume
its own conclusion. The source's absolute prime-shape threshold remains
a tested fixed exception.

For a fully proved V18, a concrete common-cap wrapper sets
\[
 r=2^{\lceil C_4\Phi(\lceil\log_2L(n)\rceil)\rceil},
 \qquad v=\lceil n/r\rceil,                         \tag{V19}
\]
with C4 larger than the proved space constant. Use the integer
cube-root rule for h to implement this scale within a fixed factor
in the exponent. Preparation and actual guards have an n/16
step/visited-space budget. Retain compact plans and execute the
r^2 chunk products in reusable marked regions. Cap the entire
attempt at n^2 actual steps. Any cap or guard failure cleans scratch
and uses a fixed exact schoolbook multiplier.
One concrete preflight may overprepare every integer active width
U<=k for interchange and every a<=k for numerical Walsh, where
k=Theta(log v) is the digit record parameter. Each retained entry
contains its compact local chain or an explicit direct-base branch.
There are only polynomially many such entries and their construction
still fits the combined \(2^{k^{\eta'}}\) envelope. At call boundaries,
locate the required entry by a charged sequential scan and copy its
compact descriptor to the active interpreter. No global plan cache is
scanned per data record. All r^2 equal-width chunk products reuse the
same prepared shapes and field descriptions.

For large n, \(\log r=O(\Phi(\log L(n)))=o(\log L(n))\), and
\(\log v=\log n-O(\Phi(\log L(n)))\). Digits remain long enough for
all guards, core space is at most n/4, and the combined preparation
of size \(2^{L(n)^{\eta'}}=n^{o(1)}\), for one fixed eta'<1,
fits its budget. The source positional
wrapper costs O(nr); its r^2 digit calls cost at most
\(n r\sqrt{L(n)}\,2^{C\Phi(\log L(n))}\).
This would give the review-dependent target
\[
 T(n)\le n\sqrt{L(n)}
   2^{O((\log_2L(n))^{2/3}
             (\log_2\log_2L(n))^{1/3})},\qquad
 \text{visited cells}=O(n).                         \tag{V20}
\]
The algorithm is input-length-aware with exact fallback. No search
weight multiplies its digit-runtime bill. All retained plans, clocks,
inputs, outputs, chunks and fallback reuse a common fixed set of
marked linear regions, bounding the union of visited cells.

## 7. Admission gates and falsifiers

At writing time V20 is not yet an admitted programme result.
Final whole-profile reviews must bind the sharper space construction,
the growing-arity numerical wrappers, and the now-completed outer V18
substitutions to the exact source snapshots.
The exact endpoint \(O(n\sqrt{\log n})\) is not claimed.

A genuine per-child inflation \(m_i^\delta\), at
\(u_{i+1}\approx u_i/m_i\), multiplies to approximately
\(u_0^\delta\) and can destroy the desired overhead. Keeping
polynomial-m tags through a child, repeatedly embedding the field,
or using only fixed-prime b^2 padding would therefore invalidate
the corresponding recurrence. A loose polynomial upper bound is
not itself such a lower bound; the actual physical invoice decides.

The conditional recurrence also fails if column changes are priced
as arithmetic word operations, if arbitrary precision scalar
application is claimed polynomial m with no record-width factor,
or if finite generation runs once per data symbol. Each of these
costs is explicitly retained above.

Credits: @CubeJerry, pinned source constructions and predecessor
variable-arity circuit, E002 component authors, and substantial
ChatGPT multi-agent assistance. No complete machine execution or
Lean proof is asserted.
