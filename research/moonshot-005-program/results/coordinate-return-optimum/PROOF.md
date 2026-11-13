# The exact optimum for thirty-one whole-coordinate returns

**Proof programme: the lattice argument below is complete; admission requires
the accompanying exact source decomposition and flat-census certificate.**
This extends the same cyclic current-row consumer. It is a scoped source
optimality theorem, not a lower bound for every distributed decoder.

## Proposition and exact finite premises

Let M be the actual 96-by-96 cyclic reverse residual over Q, of rank82, and
let Z be any 96-by-14 full-column-rank kernel matrix, MZ=0. The source
certificates establish the following decomposition of its evaluation rows:

1. Eight B rows span an eight-dimensional subspace U. The B rows and the
   74 outside-K rows give 82 distinct projective E8 root directions in U.
2. The remaining14 rows have nonzero, pairwise nonproportional images in
   Q^14/U.
3. Every E6 flat in the full E8 root configuration contains at most29 of
   the indicated82 projective directions. The finite enumeration considers
   all perpendicular complements of pairs of nonorthogonal E8 roots.
4. The specified set B7+24 has31 rows and rank7.

Then every set J of31 original coordinate returns leaves reverse residual
rank at least58, and the supplied B7+24 consumer attains58. For every
positive field volume V, a choice of31 whole original coordinate fields
leaves rank at least58V under arbitrary subsequent Hub linear consumption.
This statement does not cover fragmented coordinate returns, mixed packets,
changed earlier raw words, or additional distributed side information.

## 1. Source rank reduces the question to root geometry

For the coordinate-return interface, the exact minimum remaining rank is
rank(M[:,J^c]) = 82-|J|+rank(Z_J). To see this, row(M)=ker(Z^T).
Its subspace supported on J is the kernel of the restricted evaluation
map Z_J^T, of dimension |J|-rank(Z_J). Quotienting row(M) by this subspace
gives the displayed rank. Deleting the returned columns physically attains
the quotient rank, as the full-column consumer proves.

Thus it remains to prove rank(Z_J)>=7 whenever |J|=31. The witness in
premise4 then gives equality and 82-31+7=58. Only the source-decomposition
premises above, not a numerical rank heuristic, enter the proof below.

## 2. Why the A2-perpendicular enumeration covers every E6 flat

Use the eight-dimensional hyperplane sum(x_i)=0 in R^9. Let A8 be the
integer lattice in it, and let

    w=(2,2,2,-1,-1,-1,-1,-1,-1)/3,
    Lambda=A8+Z w.

The lattice A8 has determinant9, w has norm squared2, its inner products
with A8 are integral, and 3w lies in A8. Therefore Lambda is an even
integral lattice of index3 over A8 and determinant1. It is unimodular.
Its norm-squared-two vectors are exactly the72 signed differences e_i-e_j
and the168 signed vectors with three coordinates2/3 and six coordinates
-1/3. Indeed the integer coset has only the differences at norm2; in either
fractional coset a coordinate of absolute value at least4/3 already forces
squared norm at least23/9, and the zero-sum condition then fixes the three
positive coordinates. These are exactly the source's240 E8 roots.

Let S be an E6 root subsystem spanning a six-dimensional real subspace F,
and let L0 be its root lattice. The E6 Cartan determinant is3. Its
saturation L=Lambda intersect F has finite index k over L0 and determinant
3/k^2. Since L is integral, this determinant is an integer. Hence k=1:
L0 is already primitive in Lambda.

Put K=Lambda intersect F-perpendicular. Both L and K are primitive. In a
unimodular lattice the orthogonal projection Lambda -> L* is surjective:
any integer homomorphism on primitive L extends to Lambda, and the
unimodular inner product realizes it by a vector of Lambda. Its kernel is
K, so Lambda/(L+K) is isomorphic to L*/L. Applying the same argument to K
gives det(K)=det(L)=3.

An even positive-definite rank-two lattice of determinant3 is A2. For a
shortest primitive basis vector e and a reduced companion f, write its
Gram matrix [[2a,b],[b,2c]], with a<=c and |b|<=a. Then
3=4ac-b^2>=3a^2, whence a=1; integrality forces c=1 and b=+/-1.
The two basis vectors are E8 roots, nonorthogonal, and span F-perpendicular.
Consequently every E6 flat F is exactly the perpendicular complement of
an A2 root pair. The finite source enumeration in premise3 is complete
for all E6 flats, rather than just a convenient family of examples.

## 3. Root counts in dimensions at most six

For a subspace F spanned by E8 roots, the E8 roots lying in F form a
finite simply-laced root system: reflection in any of those roots
preserves both Lambda and F. Choose its simple-root basis. Each connected
Cartan graph has diagonal2 and off-diagonal0 or-1 and is positive definite.
For rank at most6, the graph is a tree, has no vertex of degree4, and has
at most one vertex of degree3. A cycle, a four-arm unit star, or a tree
with two forks contains a non-positive-definite affine subdiagram.

Without a fork the type is A_r. For three arms of lengths a<=b<=c,
positive definiteness is equivalent to

    1/(a+1)+1/(b+1)+1/(c+1)>1.

With a+b+c+1<=6 this gives D_r, with arms(1,1,r-3), or E6, with
arms(1,2,2). The numbers of projective root lines are r(r+1)/2 for A_r,
r(r-1) for D_r and36 for E6. The A and D formulas follow from their
coordinate models; E6's Cartan diagram and determinant are fixed by its
six simple roots. Reducible systems add these counts across their ranks.
It follows that a rank-at-most6 root subsystem with at least31 root lines
must be E6. Rank-at-most5 has at most20 lines, and rank-at-most4 at most12.
No assertion about arbitrary real unit vectors with unrelated angles is
being made here; every vector is a root of the pinned lattice.

## 4. Excluding thirty-one evaluation rows in rank six

Suppose rank(Z_J)<=6 and |J|=31. Let q be the dimension of the image of
span(Z_J) in the quotient Q^14/U.

If q=0, all31 rows belong to the82-point E8 part, because each exceptional
row has nonzero quotient image. Their root span has rank at most6 and
at least31 lines, hence is an E6 flat. Sections2 and premise3 bound the
number of source roots there by29, a contradiction.

If q=1, at most one exceptional row lies in J, since their quotient
projective directions are pairwise distinct. The base root rows have rank
at most5 and number at most20. Thus |J|<=21.

If q>=2, the base root rows have rank at most4, so number at most12.
Even granting all14 exceptional rows gives |J|<=26.

Every case contradicts |J|=31. Therefore rank(Z_J)>=7. The explicit
31-return source attains rank7 and residual58, completing the theorem
once the four finite premises are authenticated.

## Consequence and limits

Within whole-coordinate returns, further selection search at price31
cannot improve on the current rank58 source. A lower residual at that
price must change the observation type, earlier source word, or another
stated premise. Twenty-four completed original endpoints are separately
verified for the supplied witness; residual rank alone does not imply an
equal number of individually completed endpoints. Neither the optimum
nor its proof completes the outstanding forward or reverse obligations.
