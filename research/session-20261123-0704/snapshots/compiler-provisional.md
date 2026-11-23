# Joint native and compiler closure for the selected construction

**Status: proposed source-specific theorem, pending independent review.**
The checks below are complete where their receipts say so; they do not by
themselves establish the universal joint implication.

## Statement and source boundary

Fix canonical main `e54523517d0f03e58352e647c403a5af3e525a57` and the selected
#7000/#7001 raw words. Assume the following three contracts, with the exact
meanings used in `certificates/selected-result.json`:

| ID | Retained statement |
| --- | --- |
| `owned_erasure` | Owned streams and suspended centers obey the retained allocation, erasure and ownership contracts. |
| `precision_tape` | Retained fixed-tape movement and precision/storage prescriptions apply to the new fixed finite template. |
| `analytic_recovery` | Analytic decomposition, fine-prime avoidance and exact integer recovery follow the retained upstream/outer framework. |

The selected raw words then have a constructive alternative implementation
with the same complete conditional bound

\[
T(n)=O\bigl(n(\log n)^{1-\kappa}\bigr),\qquad
\kappa=363005817/100000000000.
\]

The construction below supplies the required `native_all_columns` and
`compiler` instances together. It does not infer their conjunction from the
two implications “native implies compiler” and “compiler implies native.”
It first builds finite syntax using exact operator identities; only after
that syntax has been frozen does it construct the execution by a decreasing
runtime measure. No execution of an unavailable fast query enters the first
construction.

This is an alternative selected-source implementation. Its finite carriers
are larger than the original selected carriers; it is not a claim that the
original unmaterialized transition table has been executed. The selected
certificate remains unchanged. No new κ or unconditional theorem is claimed.

The two principal proof inputs are:

* Ali Romman's single-grade compiler, [#7828 at 03b572b3](https://github.com/aliromman/integer-mult-bounds/blob/03b572b3b9ab72c6ba67762e85e1630cda1daad5/research/single-grade-rank-compiler/PROOF.md), with its [application](https://github.com/aliromman/integer-mult-bounds/blob/03b572b3b9ab72c6ba67762e85e1630cda1daad5/research/single-grade-rank-compiler/APPLICATION.md).
* The exact selected native specialization, [#7840 at adf2e0aa](https://github.com/CubeJerry/integer-mult-bounds/blob/adf2e0aa6777977a280ce50f8938f4a0f4f19b76/research/selected-native-four-premise-specialization/PROOF.md), building on Ali Romman's [#7837](https://github.com/CrocSwap/integer-mult-bounds/pull/7837).

The #7846 uniform proof concerns another mixed-rank construction. Its
enumerated compiler was inspected during this investigation, but its claimed
removal of the five assumptions is not a premise of this result.

## 1. Separate denotation from implementation

Write \(Q_E\) for the positive transform on an indicated set \(E\) of active
axes, tensored with the identity on every other axis of the *same complete
field*. A query is a formal instruction with this specified linear operator
as its denotation. This definition makes no fast-algorithm claim.

For complex fields, the selected one-column chart catalogue gives exact
Gaussian-Clifford operators. Tensor multiplicativity proves their identities
at every positive column multiplicity. A scalar coefficient on a graph edge
acts once on the entire array. An intrinsic phase of a tensor-powered chart
acts once per column. The whole-field LAMBDA is a two-term combination after
taking the whole Q²; it is never distributed as a tensor product of sums.
The selected scalar endpoint and full caller identity therefore give the
required direct-sum input/output identity with formal \(Q_E\) queries.

For binary fields, use the selected rational split projectors. In logical
head/reversed-tail coordinates,

\[
D(P)=\begin{pmatrix}I-P&P\\P&I-P\end{pmatrix}.
\]

For complementary disjoint projectors, \(D(P+Q)=D(P)D(Q)\). Nested differences
and whole image/kernel matchers are exact rational identities. The selected
own-word scalar endpoint has precisely the 111 coupled X-to-Y pairs needed
by its paired common routes; the 437 helper returns are independent. This
proves the binary caller identity with formal positive queries on every
complete field, before choosing a cover prime or executing a route.

These are the denotational parts of #7840 §§2–4 and §8. Their proofs use
finite operator equalities, scalar chronology, full spectator factors and
the owned meanings of INIT/CLEAR. They do not use the finite compiler or an
already fast positive query. In particular, temporarily correlated private
values do not become new independent inputs.

The selected source data are unchanged: ambient 153, 23,392 productive
fields and 117,612 paid occurrences for the complex caller; ambient 134,
19,950 productive fields and 107,352 paid occurrences for the paired binary
caller. The raw binary record's stale 127 is not a working ambient.

## 2. Construct finite syntax without executing a query

Here is the needed parametric compiler lemma. Suppose a fixed raw word has
the direct-sum denotation in §1 at every positive integer multiplicity,
with ambient \(A\), target multiplicities \(W_k\) and its actual ordered
paid requests of ranks \(r_j\). Assume its complete normalizers and its
positive disjoint splits have their stated formal identities. Local owned
storage and scalar instructions keep their declared costs.

For two words U,V, start one U instance for every productive role of V.
Different instances receive distinct arbitrary fields and private tags.
Suspend all U instances at the same paid occurrence. The resulting distinct
owners form precisely the roles of one V invocation. Its role-specific
complete adapter normalizes the requested whole job, executes the formal
V word, and returns before U continues. The working ambient is the product
of the two true ambients. All target/paid ranks multiply, while every
spectator remains part of its original array. This is a finite substitution
of instruction lists; the query denotations prove its correctness.

Take power \(v\), and retain all labelled target paths of one type
\((n_k)_k\), where \(\sum n_k=v\). Their common rank and number are

\[
K=\prod_k k^{n_k},\qquad
B=\frac{v!}{\prod_k n_k!}\prod_k W_k^{n_k}.
\]

Give every other target its own zero input. These fields receive no
productive credit. Run all of their instructions and all of their paid
queries, including a query whose current value is zero. The direct-sum
endpoint implies that each such field returns to zero even though it may
have contained nonzero combinations during the word. Retire it only after
that completed endpoint. Nonzero private clears inside the raw word still
use `owned_erasure`.

Split a paid rank larger than \(J\) into consecutive positive blocks of
size \(J\) and its positive remainder, keeping the *original whole*
input/output adapters outside all these blocks. This produces a homogeneous
word of true ambient \(M=A^v\), B independent targets of rank K, and paid
ranks \(h_i\leq J<K\). It has not called an implementation of any query.

Fix a terminal rank \(N\geq2M\). A homogeneous job of e active axes uses
\(c=\lfloor e/K\rfloor\) copies of every active axis and its first Mc
working axes. Its child ranks are \(h_i c<e\); its residual \(e-Kc\)
axes are one-axis queries. All descendants reuse the original N-axis
field. They allocate no missing tensor factor and turn no spectator into
a separate input. Define

\[
D(e)=0\ (e<K),\qquad
D(e)=1+D(h_{\max}\lfloor e/K\rfloor)\ (e\geq K).
\]

A batch divisible by \(B^{D(e)}\) can be grouped into distinct B-role
instances. At a paid occurrence, each instance lends one actual current
owner. There are no aliases, including when that owner is a private
center. The resulting batch size is divisible by the smaller required
width, since D is nondecreasing and a child has depth at most D(e)−1.
Complete the child and restore the role order before advancing that
occurrence. Induction on e therefore generates a finite chronological
word containing only one-axis queries.

Partition N root axes into consecutive tiles of capacity
\(K\lfloor N/M\rfloor\), with the last positive remainder. Reuse the
same batch of \(B^{D(\mathrm{capacity})}\) independently arbitrary full
fields for every tile. Each field receives all N axes exactly once. The
identity on disjoint factors proves the full-rank endpoint. Different
tiles do not introduce additional productive fields.

This supplies the finite compiler contract under the denotational input
of §1. It does not invoke `native_all_columns` as an efficient algorithm
or invoke the selected `compiler` assumption.

## 3. Independent funding of the selected finite words

Put \(t=1-C\), \(T(t)=\sum W_k k^t\) and
\(P(t)=\sum_j r_j^t\). The included arithmetic check reads the exact selected
histograms, imports no contributor scientific module, and checks the
recorded #7828 types with a separate rational-series engine.

It certifies every exchange inequality for the actual weights
\(a_k=W_k k^t\):

\[
\frac{a_i}{n_i+1}\leq\frac{a_j}{n_j}\quad(n_j>0).
\]

Thus all selected last priorities dominate all unselected next priorities.
The type is a multinomial mode. There are at most \((v+1)^d\) types, so

\[
BK^t\geq T(t)^v/(v+1)^d.
\]

The checks use lower/upper rational enclosures \(T_-\leq T(t)\) and
\(P(t)\leq P_+\), and a strictly positive common bound

\[
\delta\leq1-P_+/T_-,\qquad
\delta\leq\log(T_-/P(1))+C\log8.
\]

For \(v=2^j\), the certificate has
\(v\delta\geq d(j+1)+3\) and \(K\geq16^v\). Splitting at \(J=8^v\)
costs at most \(P(t)^v+2J^{t-1}P(1)^v\). Consequently its paid-to-target
moment ratio is at most

\[
3(v+1)^d e^{-v\delta}<3e^{-3}<3/8.
\]

The finite homogeneous recursion satisfies

\[
F(e)=(e\bmod K)+B^{-1}\sum_iF(h_i\lfloor e/K\rfloor),
\quad F(e)=e\text{ for }e<K.
\]

Induction using the moment ratio below one half gives
\(F(e)\leq2K^{1-t}e^t\). There are at most \(3M/K\) root tiles;
concavity over their lengths yields

\[
P_N/W_N\leq2(3M)^C N^{1-C}.
\]

For \(N=2^H\), the exact checks

\[
H\geq1+v\lceil\log_2 A\rceil,\qquad
H(C-U)>1+C(2+v\lceil\log_2 A\rceil)
\]

therefore give \(P_N/W_N<N^{1-U}\). All introduced zeros, private
lifetimes, split adapters, complete routes and local records stay in the
separate physical bill; they are not additional productive credits.

| Selected source | v | H in N=2^H | Raw C | Uniform U |
| --- | ---: | ---: | ---: | ---: |
| Binary | 68,719,476,736 | 21,179,507,725,498,843,136 | .00385253 | .0038525299 |
| Complex | 281,474,976,710,656 | 817,416,431,103,305,304,760,123,392 | .00363005817007 | .00363005817006 |

For both selected sources, \(W_N\leq N^{15}\). The conservative existing
\(O_{\rm source}(N^{51})\) bound covers pre-cover logical records and
bank occurrences. It counts the entire expanded chronology, not physical
bits or the binary cover. The proof of §2 provides the required constructive
generator even though this enormous finite word has not been materialized.

## 4. Fix the whole template and only then lower the queries

Binary compilation is done over the rationals. After the finite word,
every whole-job matcher, inverse and rank witness have been generated,
choose an odd prime \(q>2^{45}N^5\) outside the complete finite exclusion
list. A raw-frame exclusion list alone would not suffice. On every
\(\mathrm{GL}_N(\mathbb Z/q^w)\), right multiplication by a fixed matcher
is a full-row bijection. Its exact low/high carry and inverse are supplied
by #7840 §4. The role-diagonal compiled endpoint permits independent whole-job
matchers; the coupled raw pairs retain their common matcher.

One common exterior weight conjugates the whole completed binary word.
It may read exposed ancestors and atom indices, and is independent of the
fresh role and cover. Hence it commutes with every fresh right route. New
weights created at a rank-one leaf read the now-exposed parent; they do not
silently become functions of the child's fresh cover.

Only the final one-axis query list is normalized into runtime children.
The full-ring argument supplies one width-f child on a good row and at
most \(32N^2\) children of width at most f on a bad row. The bad fraction
is at most \(2N^3/q\), including every low type and high lift. The resulting
moment factor is less than \(1+64N^5/q\), not one. The separate saving
loss \(d=10^{-10}\) pays it, because

\[
64/2^{45}<d/4,\qquad N^d\geq1+d/2.
\]

The completed covered binary saving is therefore .0038525298, exactly
the rate used by the selected cold ordinary chain.

For the complex template, all split and placement identities retain the
full left and right factors and their absolute phases. The final one-axis
query at outer multiplicity f is one width-f positive complex child; inverse
orientation has its existing ordinary correction. A completed query returns
before any dependent scalar or unscale. No scalar sum is tensor-distributed.

## 5. A well-founded execution, with an elementary base

First implement a radix digit exchange by elementary complete scans. This
has saving zero, restores arbitrary payload, gaps, suffixes and heads, and
requires no compiled fast service. Now construct ordinary stages 1,2,3 in
that order, at savings .0034, .0038507 and .00385248. Fix the previous
stage's algorithm, constants and cutoff before constructing the next.

Within one stage, a recursive native call at active width d has
\(f=\lfloor d/N\rfloor<d\) whenever the uniform word is entered. Its
good and bad normalized children have width at most f. A smaller than N
case and a remainder use elementary completed work. Route interchanges
use the already completed previous ordinary stage, at any required width.
All other newly generated instructions are finite local scans, scalars,
descriptors and ownership services under the retained contracts.

Order calls by the lexicographic pair (stage, active width), with the
elementary stage first. Every same-stage recursive edge strictly decreases
width; every ordinary-control edge strictly decreases stage. This gives
termination and correctness by nested strong induction. It is the required
simultaneous implementation argument, rather than a cycle between two
existence statements.

The exact ordinary recurrence with \(\rho=1/250\) and covered saving b
admits any next saving below \((1-\rho)b+\rho a\), also below \(\rho\)
and \(1-\rho\). The three positive rational gaps are respectively

\[
546399601/1250000000000,\quad
24601/1250000000000,\quad
53101/1250000000000.
\]

After stage 3 is completed, construct the complex service as the next
tier. Its numerical children decrease active width, and its ordinary
movement invokes the completed stage 3. The same lexicographic induction
applies. The .00385248 service exceeds the selected .00376669 movement
requirement. No cold seed assumes the fast operation it is meant to build.

## 6. Verify the new template's admitted boundaries

Changing the finite compiler changes its constants. Use the actual
generated number of owned fields, scalar records, split adapters, whole
routes, full N-dimensional right-route expansions, low-type tables,
descriptor production, parking and retirement. No raw `<10^12` allowance
is substituted for all those new operations. The original fixed-template
stock and tariff prescriptions are applied to their new finite counts;
for example the retained guard is formed from the actual W,P,O,G values.
This is a use of `precision_tape` in its original meaning, not a new proof
of that contract.

The new compiler's unfinished raw-context depth also has an explicit
check. A chronological product has at most v open raw levels, and a
homogeneous recursion has depth at most H/v because every paid child
shrinks by at least \(2^v\). Allowing the caller/native boundary gives

\[
L\leq2v(H/v+1)=2(H+v).
\]

With the selected common-grid factor 356, the two values 356L have bit
lengths 74 and 99, respectively. Both are strictly smaller than their
new N, checked without materializing N. For an outer original root of D
axes and \(\ell=\lfloor\log_ND\rfloor\geq1\),

\[
356L\ell<N\ell\leq N^\ell\leq D.
\]

At \(\ell=0\), elementary base work applies. Thus the original selected
prefix height/mass bounds admit the new stack depth. The entire D-axis
root stays present, completed siblings return their own denominator debt,
and there is no intermediate truncation. The existing common grid,
temporary W+26 allowance and once-only final truncation can be used with
the new finite constants. This does not prove actual fixed-tape storage,
blank grants or erasure: those remain the named retained contracts.

Since the compiler and all catalogues are fixed before operand length
varies, their finite extra constants and polynomial reservations have an
effective eventual threshold in the retained prescription. All smaller
lengths use elementary algorithms. No practical crossover is asserted.

## 7. Apply the unchanged outer price and delimit the progress

The complex uniform saving exceeds the selected κ by exactly \(6\cdot
10^{-14}\). The covered and ordinary binary rates are unchanged. Apply
the source-bound selected outer argument with these rates and the new
permitted fixed-template constants, retaining `analytic_recovery`. This
gives the theorem stated at the beginning.

The new contribution is the explicit joint construction and its selected
source binding. The finite source denotations, product idea, modal funding,
native normalization and cold ordinary formulas retain their predecessor
credit. The separate arithmetic engine checks both selected carrier
certificates and all 493 modal exchange comparisons against actual power
intervals. Finite checks support the arithmetic and implementation; the
universal statement rests on the inductions above and the cited exact raw
identities. This is model-assisted review, not independent human review or
formal-kernel acceptance of the multiplication theorem.

### Open next questions

1. Give a complete physically priced allocator/eraser for the additional
   compiler target zeros together with a real nonzero raw private clear and
   its suspended parent. Endpoint zero alone does not supply fresh backing
   or pay a nonzero clear. This targets `owned_erasure`.
2. Lower a generated N-dimensional binary right matcher through its full
   descriptor, carry, parking and return services at the stated tariff.
   Algebraic bijectivity and an effective finite catalogue do not price the
   actual full-array movement. This targets `precision_tape`.
3. Independently review the retained complete analytic and integer-recovery
   implication at the unchanged outer parameters. The present construction
   does not discharge that separate premise.

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance.
Credit Ali Romman, the selected CubeJerry/DreamingOfClouds raw-word lineage,
Jacob Alan Sussman, zxv, Cinna Davis, and the original source notices.
