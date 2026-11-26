# Why the positive Weyl batching does not automatically batch star transpositions

Status: **proved operator-family comparison and scoped applicability
obstruction**. This preserves the positive E002 result while locating
the extra mechanism needed to use it on the exposed E003 middle maps.
It is not a running-time lower bound or a rejection of all common-basis
methods.

Read remote E002 `batching/WEYL-STAR-BATCHING.md` after reconciliation
through `b979d2e9bd31d6d00d80ff70fb1a9929ad945db9`. Reviewed file
SHA-256: `8472657f7ac8307c1fa99908918a45ba3901048cd31f3a757111ea0c01a4bb02`.
The E003 comparison uses A's
`ROUTING-STAR-TRANSPOSE-NORMAL-FORM.md`, whose exact source derivation
comes from OpenAI math `3344da59991ed94f9ba711217b29c1d760badfa6`.

## 1. What the positive component actually supplies

E002's query operator changes only field x_j and leaves common parameter
fields s,xi fixed:

```
(W_j F)(x)=(-1)^(xi dot x_j) F(x_1,...,x_j+s,...,x_m).
```

For i!=j, W_i and W_j commute. The parameter controls are unchanged,
and the two operators act on different query fields.

For s!=0, choose a nonzero coordinate t of s, put
`epsilon_j=(x_j)_t`, and `u_j=x_j+epsilon_j s`. This is a full-rate
bijection: the omitted zero coordinate of u_j is replaced by the
independent epsilon bit. With `delta=xi dot s`, the transformed query
is `(-1)^(xi dot u_j) Z_j^delta X_j`.

The source's two-by-two identity checks directly:

```
D_delta^(-1) Z^delta X D_delta=i^delta X,
G_delta=D_delta H,
G_delta^(-1) Z^delta X G_delta=i^delta Z.
```

Thus one common basis makes every W_j diagonal. Row matrices independent
of these query coordinates commute with that basis. Reusing it for a
whole sequence of pencils with the **same operator family** is valid.
The physical whole-active-width controlled layout is the expensive part;
its single charge and the polynomial-m ordinary arithmetic are both
explicit. The theorem's numerical norm growth is polynomial in m on a
logarithmic scale, as required by the existing precision compiler.

In particular this is a real example of sharing physical movement.
An m-term monomial representation by itself cannot prove m separately
routed interchanges are necessary.

## 2. The exposed star family fails the required commutation

E003's middle maps P_j exchange a shared auxiliary register 0 with
query register j. For i!=j,

```
P_i P_j != P_j P_i.
```

Their products are oppositely directed 3-cycles on `{0,i,j}`.
Coordinate-permutation action on Omega^(m+1) is faithful whenever
Omega has at least two letters: a single exceptional letter detects
any nontrivial coordinate permutation. Hence this is an operator
inequality on full arbitrary arrays, including the smallest source
pair alphabet `|Omega|=4`.

Conjugation preserves commutators. Therefore no one invertible change
of basis can turn all P_j into the E002 commuting W_j family or into
diagonal operators when m>=2. The dimension-two free-pair family
`O_j=C_0 P_j C_0`, with `C_0^2=I`, has the same obstruction.
The retained Newton signs are all nonzero; adding them to individual
operators does not remove noncommutation.

This comparison concerns an operator family, not a chosen weighted
sum of that family.

## 3. Even unrelated input and output bases have a precise limitation

Suppose invertible U,V made every `U P_j V` diagonal. Choosing P_1
as a reference would imply that all

```
(U P_1 V)^(-1)(U P_j V)=V^(-1)P_1 P_j V
```

are diagonal and commute. For m>=3 this is impossible: the relative
products `P_1 P_2` and `P_1 P_3` do not commute. As coordinate
permutations their products send coordinate 0 to 3 and 2 in the two
orders, respectively. Thus arbitrary two-sided linear equivalence
does not simultaneously diagonalize the star family once m>=3.

If the identity operator is included, the impossibility already holds
for m>=2. Diagonality of UIV=UV lets us rescale one side so the
remaining condition becomes ordinary simultaneous conjugation.

The qualification matters. For two operators without the identity,
this particular two-sided argument reduces to one relative operator
and does not prove impossibility. The large-arity source family is
well within the m>=3 regime.

A's general individual-pair normal form is `L P_j R`, with the same
invertible left/right maps for every j. The relative-product argument
is invariant under these maps, so it also applies to that full family,
not only to the two-dimensional example.

## 4. What remains open

A fixed real weighted sum `sum_j b_j P_j` is symmetric and therefore
has an orthonormal eigenbasis. Its powers, including consecutive Newton
factors formed from that one sum, share that eigenbasis. The preceding
commutator does **not** rule out using it. What is missing is a
source-compatible construction whose basis generation, physical
application, numerical heights and full-rate interface are cheaper than
the retained routing bill. Diagonalizing a matrix of the entire array
dimension is not such a construction.

Likewise, one may enlarge the row state or move part of the operator
dependence into row matrices. That changes the interface and requires
its own generation, row-volume, arithmetic and spatial-call accounting.
The E002 component does not supply those changes automatically.

There is a second independent issue: a predictor is a polynomial of the
complete pencil, including all rectangle contributions. Evaluating a
separate polynomial in each rectangle and then adding them would omit
mixed products. Even a useful diagonalization for one free pair does
not justify stage reuse across the complete retained pencil.

The current constructive target is therefore a joint physical router,
a priced basis for the appropriate complete pencil, or a new full-rate
factorization that handles these noncommuting exchange terms. The E002
common-parameter construction provides a positive test case, while the
E003 exact normal form explains why renaming its registers is insufficient.

Credits: @CubeJerry; E002's positive Weyl batching construction; pinned
OpenAI endpoint maps; E003 A's exact star normal form; substantial
ChatGPT multi-agent assistance. No global lower bound or new complete
multiplication exponent is claimed.
