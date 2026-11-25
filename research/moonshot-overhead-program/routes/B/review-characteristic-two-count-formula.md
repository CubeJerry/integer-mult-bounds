# Independent review of the characteristic-two count formula

Review result: **PASS for A's finite construction B1--B11 and its
admission to the previously reviewed IP4 interface**. This is a mathematical
review with finite exact corroboration, not execution of a giant template
or formal verification of a tape machine.

Reviewed file: `../A/characteristic-two-count-formula.md`, read in full
on November 25, 2026 during session S002.

## 1. Formula size and degree

The characteristic-two carry expression `xy+(x+y)c` is the correct Boolean
carry and contains the predecessor carry once. Counting all copied x/y
subtrees gives exactly the recurrence used in B2. Iterating the cumulative
sum, instead of replacing each summand by the maximum, gives
`S_(r,k)<=8^r binom(r+k,k)`. Since both r and k are O(log m), this is
polynomial. A prefix serialization with no reference opcodes was checked
independently below; the proof does not silently use circuit sharing.

For each k, carry and output bit have syntactic degree at most 2^k.
The ternary digit's bit one is an affine query indicator of actual degree
one and is safely assigned budget two. The degree argument remains valid
when an intermediate polynomial contains repeated original variables.
That is precisely why the restricted multilinear-formula barrier does
not apply.

Adding the constant residue of -u adds one balanced-size bound, even when
c-u is negative. The formal-series identity modulo T^(2^t) is valid for
negative powers because 1+T is a unit. With 2^t>D, the selected-bit product
for coefficient h has degree at most h. The scalar
`omega^(u-sum beta_j)` is present, so every spectral value agrees with the
source order-three predictor, including its global phase.

## 2. Full-rate construction and actual finite data

The formula has polynomially many nodes and degree D=O(sqrt m). The cyclic
formula compiler therefore gives D affine factors on `2^{m^C}` rows.
The entire product is scalar on every row, and all shifts have the same
architecture and degree budgets. The direct sum over 3^m shifts and fixed
duplication preserve that bound and give normalized active pencil volume D.

The single algebra `F4[Z]/Phi_(M0*tau)` is valid: M0 is an odd common
multiple of all odd factor lengths, tau is a power of three at least the
pre-expansion batch, and the F4 copy of omega remains in the base. Every
needed sum root is supplied by a power of Z. Check-node differences are
units by the explicit product equal to three, hence to one in
characteristic two. No field-factorization search or alphabet truth table
is required.

M, the formula module, and every coordinate/list dimension are bounded by
`2^{m^C}`. The specified cyclotomic constructor is polynomial in numeric M;
all algebra operations, table inverses and 3^m spectral evaluations fit the
same type of envelope. The small range with D>m has a correct directly
tested baseline. This is an actual generation bound, not only a bound on
the final output description.

## 3. Admission to the physical IP4 bridge

The accepted order-three closure uses the completed F4 multipliers, known
exception sets, full row occupancy and routed affine pencils. These are
exactly the supplied objects. Its two-P repair, common algebra, label
preserving regrouping and final three-transform swap word require no
different local representation. Basis expansion multiplies independent
rows and recursive calls equally; all coordinates and finite scalar work
are retained in the `2^{m^C}` envelope.

The physical address geometry uses rational maps and odd address radices;
its characteristic-two label factorization is extended to the common
coefficient algebra. This does not identify the address radix with the
data characteristic. Every recursive call uses the same fixed data algebra
for that candidate.

The rational Walsh family is the already separate numerical component.
Its fixed rational coefficients are approximated during charged setup at
the chosen precision; norms, rounding and all actual column movements
are in the previously reviewed numerical/physical ledger. No integral
specialization from Z[1/2] to characteristic two is asserted. Replacing
the hypothetical IP4 constructor by B1--B11 changes its finite envelope,
not the previously checked two-component physical interface.

## 4. Independent exact checks

`verify_characteristic_two_carry_formula.py` passed and saved
`characteristic-two-carry-formula-verification.json`. It checked:

* 5,460 binary-addition truth cases;
* 137,214 shifted Lucas coefficients, including negative exponents;
* 120 evaluations of actual unfolded, serialized bit formulas, with
  no reuse instructions and maximum tested size 633 nodes;
* 525 actual size/degree recurrence cases;
* 45,864 F4 predictor cases, checking every central-window target and
  the scalar phase on the tested tuples.

Omitting the carry-generation term or the scalar phase fails its negative
control. These tests distinguish the pivotal finite identities; the
general polynomial-size proof and whole-input cost remain mathematical
arguments. The complete theorem and final gate are recorded separately.

## 5. Why the literal multilinear obstruction is avoided

For four Boolean inputs a,b,c,d, pairing (a,b) and (c,d), the carry into
bit two is the formal polynomial

    abcd + (ab+cd)(a+b)(c+d).                            (CB1)

It has syntactic degree four. Its second term is a nonzero formal
polynomial with repeated variables, but vanishes on Boolean inputs:
`ab(a+b)=a^2b+ab^2` reduces to zero, and likewise for cd. Thus this bit
formula agrees with e_4 in the Boolean quotient while escaping the
homogeneous multilinear-formula lower bound. The cyclic compiler permits
these nonmultilinear intermediates and retains its entire-row identity.

For the actual queries, q_j^3-1 has three distinct roots in F4 with unit
differences, also after the common algebra extension. Joint evaluation
therefore gives the direct-product decomposition of
`E[q_1,...,q_m]/(q_j^3-1)`. Equality at every permitted tuple implies
equality of the commuting query operators exactly. This is not a
statistical use of the quotient or a loss of independent row occupancy.

Credits: A's carry/formula derivation; the source predictor and physical
interfaces; Jerry Chen (@CubeJerry); AI-assisted independent review.
