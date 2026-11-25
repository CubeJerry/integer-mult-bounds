# A matching row bound for the unreduced multilinear formula recipe

Status: **proved reduction to a published formula lower bound; independently reviewed by Route A and the lead**. This is a lower bound for a specified representation recipe, not for all matrix roots, the multiplication problem, or the stronger MR target.

The new formula construction has row dimension
`exp(exp(O(log^2 m)))`. The result below shows that changing the
degree-preserving multilinear formula alone cannot reduce this to
`exp(poly(m))` while retaining the same unreduced cyclic composition
rules and the source central window.

## 1. The published input and the precise family

Pavel Hrubeš and Amir Yehudayoff, *Homogeneous formulas and symmetric
polynomials*, Theorem 1(i), prove that, over any field and for `m>=2D`,
every homogeneous multilinear arithmetic formula for `e_D` in `m`
variables has at least

\[
 mD^{c\log_2 D}                                  \tag{L1}
\]

leaves, for an absolute `c>0` and sufficiently large `D`. Their size
convention counts variable and scalar leaves. Primary author manuscript:
<https://users.math.cas.cz/~hrubes/PDFs/SymPoly.pdf>, page 3,
Theorem 1(i); also <https://arxiv.org/abs/0907.2621>.

We consider binary formulas over a characteristic-zero field containing
the required cyclotomic coefficients, with arbitrary affine leaves and
scalar constants, satisfying all of the following.

1. The formula is syntactically multilinear: at every product, the
   variable supports of its two children are disjoint.
2. Its syntactic degree is `D`: affine leaves have degree one, products
   add degrees, and sums take a maximum. The output is the source
   integral predictor `P_(m,u,v)` formally, with `D=v-u`.
3. It is compiled by the exact unreduced rules of
   `FORMULA-FACTORIZATION-COMPRESSION.md`: products multiply ranks,
   and a sum of common length `d` has rank `d K_1 K_2`.
   Constants and scalar multiplications use the stated rank-one
   convention. No invariant-summand selection, matrix compression,
   shared subformula computation, or different addition construction
   is permitted after this compilation.

Scalar simplification and replacement of a degree-one subtree by its
affine output are allowed before compilation. The lower bound holds
even if their coefficients are supplied free. This makes it a
representation obstruction independent of coefficient-generation costs.

Let `s` be the number of sum nodes whose assigned syntactic degree is
at least two. With rank-one leaves the literal factor rank is

\[
 K=\prod_{\text{sum nodes }v}d_v\ge2^s.           \tag{L2}
\]

The final cyclic-block encoding and regular representation only enlarge
this rank. Additions of degree one contribute factor one in (L2), so an
unweighted formula-size lower bound alone would not establish a row
bound. The next lemma deals with that distinction.

## 2. Compressing the inexpensive portions of a formula

**Lemma L.** A nonzero homogeneous multilinear formula of degree at most
`D` with `s` sum nodes of degree at least two, allowing arbitrary linear
leaves, can be rewritten as an ordinary homogeneous multilinear formula
with at most

\[
 C(m+1)D(s+1)                                    \tag{L3}
\]

leaves. The field constants may change, but no new expensive sum node
is needed.

**Proof.** Remove zero subtrees and evaluate or absorb all scalar-only
parts. Replace every maximal degree-one subtree by its computed linear
form. It is homogeneous, so it has no constant term. Now remove the `s`
remaining sum vertices from the underlying binary tree. There are at
most `2s+1` connected components. Each component is a product context:
its boundary leaves are either linear forms or holes occupied by one
of the removed sum nodes. Constants can be combined into one scalar
per component.

Every positive-degree boundary leaf contributes at least one to the
component's root degree, which is at most `D`. Thus each component has
at most `D` such boundary leaves and, in particular, at most `D` actual
linear-form leaves. Across all components there are at most
`D(2s+1)` linear forms. Expand each as the sum of at most `m` scalar
multiples of variables, using at most `2m` ordinary leaves. One extra
scalar leaf per component covers its scalar multiplier. Reattach the
removed sum vertices. This gives (L3). Products still use disjoint
variable supports, and all nodes remain homogeneous. QED.

The lemma also applies after extracting a top homogeneous component
from a syntactic-degree-`D` multilinear formula. At a product use the
top components of the two children. At a sum discard the child of
smaller assigned degree, or add both top components when the degrees
agree. Replace an affine leaf by its linear part. This creates no new
sum node; zeros are removed afterwards. The extracted formula remains
syntactically multilinear and homogeneous.

## 3. Applying the lemma to the exact-window predictor

The top homogeneous component of the formal predictor in query variables
`X_1,...,X_m` is

\[
 [P_{m,u,v}]_D=(-1)^u e_D(X_1,\ldots,X_m).        \tag{L4}
\]

The degree-`D` term in the indicator variables is
`(-1)^u(-2)^D e_D((1-X)/2)`; selecting its degree-`D` part cancels the
two signs and powers of two. Lower elementary symmetric terms do not
contribute. Alternatively one may work directly with the homogeneous
polynomial `e_D` in the independent indicator variables; its scalar
coefficient `(-1)^u(-2)^D` is nonzero in characteristic zero.

Extract (L4) from a syntactic-degree-`D` formula in the stated family.
The resulting homogeneous multilinear formula has at most `s` sum
nodes of degree at least two. Lemma L and the published bound give

\[
 C(m+1)D(s+1)\ \ge\ mD^{c\log_2D}.
\]

After decreasing the absolute constant and increasing the fixed lower
cutoff on `D`, this implies

\[
 s\ge D^{c'\log_2D},\qquad
 K\ge2^{D^{c'\log_2D}}
   =2^{\,2^{c'(\log_2D)^2}}.                    \tag{L5}
\]

This lower bound permits arbitrary scalar constants over an extension
field, so restricting them to dyadics cannot weaken it. Coefficient
heights, generator time and regular-representation enlargement are
unnecessary for this lower bound; they only add expense.

For the source window `D=Theta(sqrt(m log m))`, `m>=2D` eventually and
`log D=Theta(log m)`. The smallest possible literal row rank in this
family therefore has matching upper and lower orders

\[
 \boxed{\quad K=\exp\!\bigl(\exp(\Theta((\log m)^2))\bigr).\quad} \tag{L6}
\]

The upper bound is the balanced construction; the lower bound is (L5).
Thus this family cannot meet `K<=exp(m^C)` for any fixed `C` by
optimizing its multilinear formula alone. This is a fixed-window
row-representation result, not an optimality theorem for the final
global envelope or its arity choice.

## 4. What must change to improve this representation scale

The obstruction is narrower than a general matrix-root lower bound.
It leaves concrete alternatives:

- A degree-preserving **nonmultilinear** formula of smaller size can
  use cancellations not admitted in (L1). Its coefficient ring,
  heights, syntactic degree and actual generator still need bounds.
- A Boolean-quotient construction can use nonmultilinear intermediates
  and quotient relations. A quotient identity for an already
  multilinear formula does not help: its multilinear representative
  is unique and must equal the same formal predictor.
- A smaller factorization obtained by certified invariant-summand
  decomposition, a different addition rule or shared computations is
  outside (L2). It must still act on every independent input row and
  provide a uniform coefficient/basis generator.
- A changed window or repair protocol changes `D` and possibly the
  polynomial. Its separate normalized call, conversion, precision and
  tape-space invoice must be established anew.

S002's flat formal Chow barrier and (L5) concern different specified
families. The nested formula construction avoids the flat family; this
note then locates a matching limitation of the nested unreduced
multilinear recipe. Neither statement precludes MR in general.

No finite tests are used to prove this asymptotic obstruction. The
essential input is the published homogeneous multilinear lower bound;
the reduction here prices the high-degree sum nodes that the actual
factorization rank charges. Developed with GPT-6 Astra Pro assistance;
credit to Hrubeš--Yehudayoff for (L1), the pinned OpenAI predictor, the
matrix-factorization literature and @CubeJerry.

## Independent review receipt

Route A independently checked the primary author manuscript's Theorem 1(i)
and the entire reduction; its record is
`../route-a/FORMULA-RECIPE-REVIEW.md`. On 2026-11-25 the lead also read
this proof and that review and found no blocker. Both audits checked
the restriction to degree-at-least-two sums, the `2s+1` component count,
the positive-degree boundary-leaf bound, (L4)'s coefficient and sign,
top-component extraction, and the precise unreduced-composition scope.
