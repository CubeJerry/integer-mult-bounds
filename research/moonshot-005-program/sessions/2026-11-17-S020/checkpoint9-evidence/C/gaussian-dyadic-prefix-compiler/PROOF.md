# Exact Gaussian-dyadic compilation on a fixed finite prefix

Worker C, S020. Independently reasoned algebraic classification and literal
primitive certificate, 17 November 2026.

## 1. Precise statement and scope

Put R = Z[i,1/2] and pi = 1+i. Fix a positive integer d and b >= 2 banks,
each with d prefix coordinates and the same arbitrary positive tail dimension N.
The target is M tensor I_N, where M belongs to GL_(bd)(R). The following are
the exact admitted primitives in this statement:

* whole-bank ADD: one bank is added to a different bank;
* whole-bank SCALE by an element of R's unit group;
* a fixed-prefix root-four monomial on one bank, tensored with the tail identity.
  This means a permutation of the d prefix coordinates and independent phases
  from {1,-1,i,-i}. In particular, coordinate transpositions and a minus sign
  on one prefix coordinate are available.

The compiler uses these b banks only. All input bank values are arbitrary.
There is no initialized zero bank, erasure, measurement, or coordinate-selective
ADD/SCALE primitive. Intermediate values may couple the banks.

**Theorem.** There is an exact finite primitive word for M tensor I_N if and
only if

    d divides v_pi(det M).

When the condition holds, one fixed word works for every N. Its length may depend
on M and d. This is a classification for the stated finite-prefix ring and
primitive class, not a claim of uniform quantitative compilation as d, the
coefficient heights, or the prefix choice vary.

**Restored-borrower corollary.** For A in GL_d(R), A tensor I_N on one bank,
with one arbitrary equal-width borrowed bank restored exactly, is realizable
if and only if d divides v_pi(det A). This is the theorem for diag(A,I_d).
One borrowed bank suffices; any number of restored borrowed banks cannot remove
the determinant obstruction. With d=1 and one bank, every scalar unit is already
an allowed SCALE. For d>1 this proof does not assert the one-bank classification
without a borrowed bank.

The theorem requires the stated monomial availability. Restricting MONO to a
smaller catalogue requires a separate verification that the selectors below can
be synthesized. Allowing nonunit scalar scalings, unequal bank widths, zero
workspace not restored, noninvertible erasure, or a larger coefficient ring
changes the model. None is silently admitted here.

## 2. The ring and its units

The Gaussian integers admit Euclidean division: round each coordinate of a/b
to an integer to obtain q, and the remainder has strictly smaller squared norm
than b. Thus they are a Euclidean domain. Since 2 = -i*pi^2 and
pi^-1 = (1-i)/2, localizing at 2 is the same as localizing at pi.

Consequently

    R^* = { i^e pi^k : e modulo 4, k an integer }.

For completeness, write a nonzero r as (a+ib)/2^h with a,b integral. Divide its
Gaussian-integer numerator by pi until this is no longer possible. Division is
integral precisely when a and b have the same parity, and replaces (a,b) with
((a+b)/2,(b-a)/2). If r is a unit in R, the remaining numerator divides a power
of 2 in Z[i], so it must be a Gaussian unit. Conversely such a remainder gives
an explicit inverse in R. This also computes v_pi(r), subtracting 2h for the
denominator. In particular, a unit of valuation zero is a root-four unit.

All coefficients of a matrix in GL_(bd)(R), and its determinant inverse, are in
R. Equivalently for a square matrix over this commutative ring, its determinant
is an R-unit: one direction follows by determinants, and the other by the
adjugate formula. This elementary commutative statement is not a statement
about units in any noncommutative ordinary-operator algebra.

## 3. Necessity, including arbitrary restored borrowers

Compute the determinant of each full b*d*N dimensional primitive.

* ADD has determinant 1.
* MONO has determinant a root-four unit, hence pi-valuation zero.
* SCALE by u on one bank has determinant u^(dN), hence valuation in dN Z.

Therefore every exact primitive word has determinant valuation in dN Z. The
target determinant is (det M)^N, of valuation N v_pi(det M). Cancellation of
the positive integer N proves the necessary divisibility by d.

This reasoning allows all intermediate coupling and any number of arbitrary
restored equal-width borrowed banks. A restored bank contributes determinant
one to the final target. For example diag(pi,1,...,1) on one d-dimensional
prefix is invertible over R but cannot be so compiled when d>1. For d=4,
diag(2,1,1,1) also fails: its valuation is 2, not a multiple of 4.

## 4. Cross-bank selectors from actual primitives

Let X and Y be distinct banks, and let U be an admitted prefix monomial.
For a scalar unit c in R, perform, in this chronological order:

    Y <- c Y
    Y <- U Y
    X <- X + Y
    Y <- U^-1 Y
    Y <- c^-1 Y.

The result is X <- X + c U Y, with Y restored for every initial value. These
are literal SCALE, MONO, ADD, MONO, SCALE operations. No coefficient cU is
being declared a new primitive.

Every r in R is a finite sum of scalar units. Write r=(a+ib)/2^h. Expand the
binary digits of |a| and |b|, using the signs of a and b. Each nonzero term is
one of +/-2^k or +/-i*2^k, with k an integer, hence an R-unit. Zero requires
no terms. In particular r itself may be a nonunit, such as 3 or (3+5i)/8;
no SCALE by r or r^-1 is used.

Let D_a be the prefix monomial that is -1 on coordinate a and +1 elsewhere.
Let P_ab swap coordinates a and b, with P_aa = I. Then

    E_ab = (P_ab - D_a P_ab)/2.

For each unit term c of r, synthesize the two preceding cross-bank additions
with coefficients c/2 and -c/2 and monomials P_ab and D_a P_ab. Both scalar
coefficients are units. Their combined effect is

    X <- X + r E_ab Y,

with Y restored. Additions with the same source and target add their
coefficient matrices, because the source is restored after each term. Thus
every cross-bank coordinate elementary shear is now a literal primitive word.

## 5. Within-bank shears with an arbitrary existing bank restored

Fix distinct prefix coordinates a and b in one bank A, and use any other
existing bank B as a temporary borrowed bank. Put P = r E_ab and Q = E_bb.
Then QP=0 and PQ=P. Execute four compiled cross-bank transvections:

    B <- B + Q A
    A <- A + P B
    B <- B - Q A
    A <- A - P B.

For arbitrary initial vectors (x,y), the first two steps give

    B = y+Qx,       A = (I+P)x+Py.

The third gives B=y because QP=0. The fourth then gives A=(I+P)x.
Thus the exact full map is diag(I+rE_ab,I) on these two banks. The temporary
bank is restored before another elementary shear is begun. Section 4 expands
all four transvections into the original primitive alphabet, even when r is
not a unit. Negative coefficients are decomposed into units just as positive
ones are; subtraction is not an additional primitive.

If an elementary shear involves coordinates in different banks, Section 4
already implements it directly. Hence every elementary matrix I+rE_uv on
the bd prefix coordinates, u!=v, is implementable using only the original b
banks, with all coordinates other than u transformed exactly as specified.

## 6. Elementary generation over R, with explicit denominator handling

We prove that every A in SL_m(R), m>=2, is a product of elementary matrices.
This section is a mathematical factorization; clearing a common denominator
is an algebraic device for choosing row operations, not an extra machine
operation or a possibly nonunit SCALE primitive.

First consider a unimodular column x in R^q, q>=2. Choose h>=0 such that
y=2^h x has all entries in Z[i]. Apply Gaussian-integer Euclid to pairs of
entries of y. A quotient subtraction is an elementary row operation. A row
interchange with one sign is also elementary, since

    [[0,1],[-1,0]] = E12(1) E21(-1) E12(1),

where Euv(r) denotes I+rE_uv. Euclidean remainders strictly decrease squared
Gaussian norm, so finitely many such operations reduce y to
(g0,0,...,0). Applying precisely the same operations to x reduces it to
(g,0,...,0), where g=g0/2^h. Since the original column entries generate R,
and elementary row operations preserve that ideal, g is an R-unit.

Normalize this first coordinate to 1 by the paired determinant-one diagonal
diag(g^-1,g) acting on the first two of these q rows. This paired scaling is
itself elementary, not a forbidden coordinate-selective SCALE. For any unit u,
define

    w(u) = E12(u) E21(-u^-1) E12(u)
         = [[0,u],[-u^-1,0]].

Then w(u) w(-1) = diag(u,u^-1), a product of six elementary matrices. Set
u=g^-1. The zero in the second column entry remains zero during the final
paired diagonal map; no assumption on the other matrix entries is made.

Now reduce A by row operations. Its first column is unimodular because A has
an inverse over R. The preceding procedure makes that column e1. The remaining
(m-1)-square lower-right block has determinant 1. Repeat inside its remaining
rows, using paired normalization whenever at least two rows remain. Previous
columns remain fixed because their entries in these rows are zero. For the last
single row, the last pivot is already 1 by the determinant-one condition, so no
unpaired scaling is required. The resulting matrix is upper triangular with
all diagonal entries 1. Back substitution by elementary row additions clears
the entries above the diagonal.

This produces a finite sequence of elementary left multipliers taking A to I.
Their inverses are elementary (replace r by -r), so A is an elementary product.
The argument uses neither division by a nonunit as an admitted primitive nor
an unexplained claim of stable generation. Every elementary factor is compiled
by Sections 4 and 5 using the existing b>=2 banks.

## 7. Sufficiency for a general b-bank matrix

Write det M = i^e pi^n and suppose n=dk. Let S scale the entire first bank by
pi^-k, so det S = pi^-dk. Let D be a root-four prefix monomial on that bank
with phase i^-e on one coordinate and phase 1 elsewhere. Then

    A = D S M

has determinant 1. Section 6 gives an elementary factorization of A, and
Sections 4 and 5 give a literal primitive word for each factor, using no bank
beyond the existing b. Finally apply D^-1 and S^-1 to obtain M. Both are
admitted primitives. This proves sufficiency and completes the classification.

All identities act only on the fixed finite prefix. Tensoring every primitive
with I_N preserves the identities for every tail size N, and the same word
works without any dependence on N. The proof does not presume zero input data
in a helper or inspect individual tail entries.

## 8. Exact certificate and reproducibility

Run:

    python -B check.py --out CERTIFICATE.json

The checker uses independent standard-library Fraction arithmetic for Gaussian
rationals and replays the complete primitive matrices on all arbitrary input
columns. It does not import root's independent compiler review or any earlier
complex compiler. It verifies:

* internal and cross-bank shears for d=2,3,4 and b=2,3, including nonunit
  coefficients 3, (3+5i)/8, and (1+2i)/4;
* every actual SCALE coefficient is an R-unit, and every MONO phase is root-four;
* restoration of arbitrary existing helper banks, including all their columns;
* admissible composed targets of positive and negative determinant valuation;
* literal reversed inverse words, using source -1 scales around inverse ADDs;
* the six-shear paired unit normalization both within and across banks;
* actual Gaussian-integer Euclid on a determinant-one matrix with nonunit first
  pivot 3*pi and unit column gcd pi, followed by compilation of every resulting
  elementary factor and an exact inverse replay;
* rejection when a necessary ADD is omitted;
* the exact valuation obstructions above and a tail-identity control at N=2.

These finite checks certify the explicit identities and distinguish illegal
nonunit SCALE from legal nonunit shear coefficients. They are not an exhaustive
finite search proving the theorem. Sections 2--7 provide the all-d, all-b and
all-N proof. The broader compiler foundation, more general ordinary-operator
units, uniform resource charges, endpoint interfaces, and any multiplication
exponent improvement remain open and are not asserted by this package.
