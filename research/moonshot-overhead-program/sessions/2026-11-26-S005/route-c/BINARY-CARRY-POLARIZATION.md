# The first CRT carry is a quadratic refinement

Status: **exact algebraic identity; no fast-supplier claim**. This sharpens
the first new-digit gate in UC5 without computing its missing linear data.
All vector products below are coordinatewise over F2. Canonical lifts of
binary vectors to Z/4 are denoted by brackets.

Let E2 be the UC CRT matrix over Z/4, let E1 be its reduction over F2,
and define K(x) by

    E2([x]) = [E1(x)] + 2[K(x)] modulo 4.

Then, for every pair of full binary coefficient vectors x and y,

    K(x+y)+K(x)+K(y) = E1(x) E1(y) + E1(xy).       (CP1)

This includes all factor residue coordinates; no irreducible-degree or
support restriction is imposed on the inputs.

## Proof by canonical carries

The binary carry identity is

    [x]+[y] = [x+y]+2[xy].

Apply the Z/4-linear map E2. Expanding its values using K, and applying
the same canonical carry identity to E1(x),E1(y), makes the low binary
vectors equal because E1 is linear. Equality of the high digits then
gives CP1. The term E1(xy) is necessary because [x]+[y] and [x+y]
are different lifts when their supports intersect.

An equivalent coordinate formula follows by writing the literal matrix
representatives of E2 as A0+2A1, with binary matrices A0,A1:

    K(x)_r = sum_i A1[r,i] x_i
       + sum_(i<j) A0[r,i] A0[r,j] x_i x_j.        (CP2)

Indeed the high bit of the sum of binary terms is the parity of the
number of pairs of selected terms. The first term includes the actual
high digits of the CRT matrix; it must not be dropped.

## What the identity determines, and what it leaves open

CP1 is a bilinear polarization, so K is a quadratic Boolean map.
Its polarization is computable using binary transforms and componentwise
products if those operations are supplied at their actual cost. That
does not by itself evaluate K on a given vector. A quadratic refinement
also needs its linear part. In CP2 that part is A1 x, equivalently the
values K(e_i) on all coefficient basis vectors.

Any two Z/4-linear lifts of the same E1 have carry maps with the same
polarization. Their difference is F2-linear. A circuit made of binary
addition gates can be lifted gate by gate to addition modulo 4 with a
constant number of binary operations per gate. However, the resulting
Z/4 matrix need not be the actual CRT matrix. Its difference from E2,
divided by 2 and reduced modulo 2, is another linear map that still
needs an actual supplier. This is the precise correction omitted by
the unsupported step of replacing XOR by integer addition.

For disjoint-support x,y, the E1(xy) term vanishes. Recursive support
splitting can therefore assemble K using cross-products of E1-images,
but the multiplicity and data movement of those images remain real
costs. No improved asymptotic invoice is asserted by this observation.

The finite replay in verify_crt_independent.py checks CP1 and CP2
against actual modulo-4 remainders, with arbitrary and overlapping
supports. Its matrices are dense test oracles and are not a physical
compiler for E1, A1 or K.
