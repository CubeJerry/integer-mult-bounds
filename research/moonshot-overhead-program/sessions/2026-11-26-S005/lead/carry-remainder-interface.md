# The first carry map of the exact polynomial CRT

Status: **exact interface algebra; no fast carry supplier claimed**.
This sharpens UC5's constructive next task. It neither lower-bounds
arbitrary CRT implementations nor completes UC-GATE. Independent
review is recorded separately.

## 1. Fix the actual integer lift

Use UC's literal monic binary factors and output order. Monic division
over Z defines an integer matrix A with q columns and q rows: column
j concatenates the remainders of X^j modulo all factors. Reducing A
modulo 2^H is exactly E_(b,H). This is a mathematical definition, not
a proposal to materialize q squared entries or obtain them for free.

Let E=A mod 2, with entries in {0,1}, and D=(A-E)/2 mod 2. Negative
integer entries cause no ambiguity: D is the high bit of canonical A
modulo 4. On Boolean x, K_1(x) is the high bit of A x modulo 4. All
following additions and products are over F2; odot is coordinatewise
product of vectors.

## 2. Quadratic formula and polarization

Writing E_i for column i, the exact formula is

    K_1(x)=D x+sum_(i<j)(E_i odot E_j)x_i x_j.          (KC1)

For one row write A_ri=E_ri+2D_ri modulo 4. The low-bit contributions
have ordinary count s=sum_i E_ri x_i. The high bit of this count is
floor(s/2) mod 2, equal to binom(s,2) mod 2. Expanding that count gives
KC1; the 2D terms give its linear part. No positivity assumption on A
is needed.

For arbitrary Boolean u,v it follows that

    K_1(u+v)+K_1(u)+K_1(v)
      = E(u) odot E(v)+E(u odot v).                    (KC2)

Expanding KC1 cancels D and the pure quadratic terms. The remaining
off-diagonal products are exactly the first term on KC2's right after
its diagonal sum is canceled by E(u odot v).

Thus the binary transform determines the quadratic part. The actual
integer lift determines the linear part. Replacing A by A+2R leaves
E unchanged and changes K_1 by R x. A characteristic-two implementation
must preserve or explicitly correct this information.

## 3. What an explicitly lifted XOR circuit provides

Suppose a linear circuit computes E from input bits, zero, copies and
binary XOR gates. Replacing XOR by addition modulo 4, without changing
the graph, defines an integer matrix C with C mod 2=E. Its low output
is E(x); call its high output K_1^C(x). A gate on two-bit pairs uses

    low = low_left+low_right,
    high = high_left+high_right+low_left low_right.      (KC3)

This has constant-factor arithmetic gate overhead. It also has
constant-factor physical overhead if the original fixed-tape schedule
is supplied and every bit is replaced by a fixed two-bit record. An
abstract circuit alone supplies no tape schedule; an arbitrary binary
algorithm is not assumed to be an input-independent linear circuit.

Since A-C is even entrywise,

    K_1(x)=K_1^C(x)+R_C x,
    R_C=(A-C)/2 mod 2.                                  (KC4)

This is a positive reduction: a fast physical binary CRT circuit plus
a fast implementation of its particular linear correction R_C supplies
K_1 with the displayed extra work. That correction must be generated
and executed. It is not free because A and C agree modulo 2, and is
not claimed sparse or local to the current orbits. Simply replacing
XOR by addition proves a statement about C, not necessarily A.

## 4. Literal four-coordinate control

For b=2, order factors X, X+1, X^2+X+1 and inputs (f_0,f_1,f_2,f_3).
Integer remainders give

    A = [[1, 0, 0, 0],
         [1,-1, 1,-1],
         [1, 0,-1, 1],
         [0, 1,-1, 0]].

Its four carry coordinates are

    0,
    f_1+f_3+sum_(i<j)f_i f_j,
    f_2+f_0 f_2+f_0 f_3+f_2 f_3,
    f_2+f_1 f_2.                                       (KC5)

For F=X, the actual remainder at X+1 is -1=3 modulo 4, with high bit
one. The circuit XORing the selected binary coefficients, lifted to
positive addition, returns 1, with high bit zero. For F=1+X the
actual remainder is zero while that positive-sum lift returns 2.
These cases distinguish the required linear correction from an
uncorrected mod-two substitution.

## 5. Canonical carry at higher precision

For canonical t-bit input vectors x,y put z=(x+y) mod 2^t and define
componentwise ordinary carry vectors

    c_in=floor((x+y)/2^t),
    c_out=floor((lift(E_t(x))+lift(E_t(y)))/2^t).

The two carries have entries zero or one. The exact higher-precision
identity is

    K_t(z)=K_t(x)+K_t(y)+c_out-E_t(c_in) mod 2^t.       (KC6)

To prove it, apply E_(2t) to x+y=z+2^t c_in. Splitting the left side
into canonical low output digits and high digits produces c_out;
splitting the right side produces K_t(z)+E_t(c_in). Their low parts
agree, so cancellation and division by 2^t give KC6. At t=1 the input
and output carries are the coordinate products in KC2.

Likewise, for any integer C congruent to A modulo 2^t, the carry
map of C on canonical inputs differs by the explicit linear correction

    K_t^A(x)=K_t^C(x)+((A-C)/2^t mod 2^t)x mod 2^t.    (KC7)

This follows directly from Ax=Cx+2^t((A-C)/2^t)x and their common low
digits. The correction and circuit generation still require payment;
neither identity supplies a fast general precision-lifting algorithm.
Route A supplied KC6 during the review window; the lead independently
reconstructed the canonical-digit argument.

## 6. Constructive continuation and provenance

UC5 already uses the same forward carry map for inversion. KC1--KC4
isolate the first precision step. A concrete next approach is a fast
binary circuit whose integer lift has a cheap correction, or a joint
compiler for both maps. Higher precision still requires UC6's costs,
uniform factor access and absolute visited space. None is inferred
from these identities, and the unconditional frontier is unchanged.

The lead derived this interface while reviewing UC. Route A reported
the same polarization and circuit-lift correction independently during
its next-gate analysis; this overlap is credited, with no priority claim.
Route B independently reconstructed the literal b=2 matrix and is
reviewing the complete note. Credits: elementary binary addition and
monic division; Jerry Chen (@CubeJerry); substantial ChatGPT assistance.
