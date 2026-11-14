# Independent review of common-head rank conservation

**Disposition: accepted within the exact G192/H24 common-body interface.** This is a universal scoped obstruction, not a finite-search failure or a lower bound for all multiplication architectures. No new kappa.

Worker C independently reviewed the universal proof and wrote the accompanying exact matrix controls for @CubeJerry, with OpenAI assistance. Credit Worker B's signed/two-sided construction and root's kernel extension, projection details and all-t price argument.

## Materials and scope

The reviewed author proof is Git blob `5a82f920439b78a6aa891933c5d45757fc2097ae`, checker `d8d8621df874021d40bdb0ee85c595bcb0c9fcf7`, receipt `ccf633a5bb778ccd3f8fde2036ffedfc91ba79f6`, in CubeJerry/integer-mult-bounds. The intended programme package is `results/complex-common-head-conservation/`.

I read the complete frozen proof. Its source is the published common-cubic half at commit `4bf5bc1f28c87fe6120bd053d8202e40b425d6fb`, proof blob `04bbc16a5076cb2306c3f98aa1ecf171da1d6d01`. The signed/tensor dependencies were independently reviewed in my prior review blob `93a95938326bdf3b51aadb4012c95216df4a45a9`. That review includes an independent width-six Gram determinant32 modulo137, establishing faithful tensor separation at all widths at least6.

The theorem permits arbitrary invertible ordinary role matrices over C[H24], both native orientations and coupling signs, odd rank-one and Z queries, and even nonalternating rank-two queries. A query is in-place or a distinct-role Gaussian shear. The complete endpoint retains every arbitrary input bank and is ordinary-equivalent to independent rank-zero, one or two Gaussian jobs.

The larger ordinary Clifford phase group, changed source/body incidence, discarded banks, approximate limits, and arbitrary query primitives are not included. These restrictions are required by the proof.

## 1. The right common kernel

With actual prefixes on the right and theta suffixes on the left, the exact telescope is

`Delta M = sum theta(suffix_j) Delta F_j actual(prefix_j)`.

All nonzero factors have rank2D for a native and D for an odd query. The right kernel of each native difference is its inactive-bank coordinate space. An odd in-place query selects its bank; an odd shear selects its source bank. Both the actual gate and its theta image act as identity on that local kernel.

Even queries contribute no theta difference. Adding a zero-source/affected-bank condition at each such query is therefore essential. These additional constraints have rank at most D each after the actual prefix. They ensure that every nonordinary gate fixes the state it receives.

Chronological induction then identifies the augmented common kernel with coordinate constraints pulled back through ordinary-only prefixes. The ordinary matrix algebra is star-closed. If B stacks these constraints, the orthogonal projection at the zero eigenvalue of B*B is a polynomial in B*B and belongs to the ordinary algebra. This is an existence statement inside a finite-dimensional algebra; no physical free projection is inserted.

If there are h0 ordinary endpoint jobs, the ordinary component pi0(M) has rank exactly h0D. Indeed, the Gaussian rank components are ordinary bimodules, so ordinary outer encodings carry pi0(M) to the block diagonal ordinary endpoint part. On the augmented kernel M agrees with the product of the ordinary gates. Consequently the augmented kernel has dimension at most h0D. Removing the w extra constraints increases it by at most wD. The claimed right codimension bound follows.

This is the correct mixed-endpoint replacement for the stronger zero-kernel claim when all target jobs have rank two.

## 2. The left common kernel

This is the potentially delicate step. It is valid with the frozen convention.

Taking adjoints gives terms of the form

`actual(prefix_j)* Delta F_j* theta(suffix_j)*`.

Read this as reverse chronology with the **theta trajectory** on the right. Both F_j* and theta(F_j)* fix the kernel of their local difference adjoint. For a native, it is again the inactive banks. For a shear, the selected coordinate is the original destination. The destination requirement is different from the right source requirement.

For even queries, add the corresponding destination/affected-bank constraint in the reverse theta trajectory. Reverse induction replaces all remaining nonordinary gates by identity and the suffix by its ordinary-only suffix. The resulting left-kernel projection is ordinary by the same star-algebra argument.

Equivalently, working directly with row states, the projection P_l satisfies

`P_l theta(M) = P_l O`.

Taking its ordinary rank component and using invertibility shows that its rank is at most h0D. Thus the same codimension bound holds on the left. No assumption that the ordinary interleavings are unitary is needed: their adjoints stay ordinary because the algebra is star-closed, and their invertibility is preserved.

The proof would fail if one silently used the original source coordinate for a left shear or mixed an actual suffix with the chosen theta-suffix telescope. The frozen proof does neither.

## 3. Factorization and conservation

Factor each nonzero telescope term minimally as X_j Y_j. Horizontal concatenation and vertical stacking give Delta M=XY, with inner dimension

`s=(2m+x+z)D`.

The column rank of X is the codimension of the common left kernel; the row rank of Y is the codimension of the common right kernel. This follows because X_j has full column rank and Y_j full row rank in a minimal factorization.

Sylvester's inequality therefore gives

`(h1+hZ)D >= 2(R-h0-w)D - (2m+x+z)D`.

Writing Htot=h1+2hN+2hZ yields

`Htot-hZ <= 2m+x+z+2w`.

The independent signed-representation inequality is

`Htot+hZ <= 2m+x+3z+2w`.

Their sum proves Htot at most2m+x+2z+2w. Every query is charged by its appropriate physical rank on the right. The parity difference rank is only an intermediate proof quantity.

The all-count quantifiers are established by these matrix arguments. No bounded enumeration of query inventories is needed. The theorem also permits m=0 for conservation; the strict common-body invoice statement separately assumes m at least1.

## 4. The all-t invoice

The price proof is valid and preserves the common-body contract. Let f(r)=r^t for0<t<1 and d=f(8)-f(7). For a target head rank r in{0,1,2},

`f(7m+r) <= f(7m)+r*d <= m*f(7)+r*d`.

The actual Gaussian price is

`mR*f(7)+(m+x)*f(1)+m*d+(z+w)*f(2)`.

Using conservation, paid minus target is at least

`(m+x)*(1-d)+(z+w)*(f(2)-2*d)`.

The first term is strictly positive for m at least1. Concavity gives d at most f(2)-f(1), and for0<t<1 this implies f(2)-2d>0. The conclusion is strict at every such t, including199/200.

The explicit marginal estimate is necessary: equal total ranks alone would not compare arbitrary concave invoices. Here it works because all roles receive the same7m body, every inactive rank-seven idle is paid, and each native retains its full [1]+[7]+[8] source profile. A changed body transport scheme is outside this proof.

## 5. Independent controls

I wrote the accompanying checker separately, without importing the author checker. It uses prime137, a3-dimensional signed representation and five public roles. Forty finite words include noncommuting ordinary role/head-permutation shears, both native orientations, an even query, and an odd in-place or shear query.

For every word it checks the actual-prefix/theta-suffix telescope, right ordinary-prefix constraints, reverse left ordinary-suffix constraints, both local identity-on-kernel statements, the one-D allowance for the even query, and the Sylvester inner-dimension inequality.

It obtains21 rejections when the left shear uses the wrong bank and39 rejections when the even-query condition is omitted. These are active negative controls, not merely hard-coded inequalities. The finite signed representation is not faithful and is not used to infer the universal endpoint projection theorem. That theorem was checked mathematically above.

Run `node check.mjs` in this review directory. The checker actually ran in the cloud JavaScript runtime; no local executor run is claimed.

## Result and next boundary

The frozen theorem is accepted within its stated source, ordinary algebra, query and common-body contracts. The earlier favourable invoices remain correct conditional arithmetic; the claimed endpoints are now excluded within this architecture. The proof does not exclude a larger ordinary coordinate-phase algebra, noncommon body transport, or a genuinely changed source interface.

No complete supplier, complete conditional multiplication improvement, or new kappa is established by this package.
