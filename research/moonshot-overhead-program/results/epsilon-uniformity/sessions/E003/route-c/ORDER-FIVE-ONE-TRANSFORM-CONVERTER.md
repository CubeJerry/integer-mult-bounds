# Order-five gates give one-transform spectral converters

Status: **proved finite full-rate construction and explicit call recurrence;
independent review pending**. No stronger complete multiplication envelope
is claimed. The compact polynomial local executor is a separate supplier;
the finite algebra and call identities here do not assume that supplier.

The retained characteristic-two order-three gate uses two target transforms
for each spectral conversion. A different symmetric gate over F16 uses one.
Its ordinary swap word also uses two target powers, compared with three in
the earlier construction. This changes the recursive repair mechanism, not
just a concentration constant. It does not change the current label
incidence exponent, and no asymptotic whole-input saving follows merely
from the shorter words.

## 1. Field and exact two-by-two identities

Let `K=F2[alpha]/(alpha^4+alpha+1)`. The polynomial is irreducible: it has
no F2 root, and the only irreducible quadratic is `X^2+X+1`, whose square
does not equal it. Encode `sum_i b_i alpha^i` by the integer `sum_i b_i 2^i`.
All integers in the matrices below denote these field elements, not
ordinary scalar integers reduced modulo two.

Let `zeta=alpha^3` (encoding 8), a primitive fifth root, and set

    lambda=zeta=8,   mu=zeta^-1=15,   tau=lambda+mu=7.

Then `tau^2+tau+1=0`. Define

    a=mu^2/tau=9,     b=lambda^2/tau=14,
    C=[[a,tau],[tau,b]],       Q=[[0,1],[1,0]].

Since `a+b=tau` and `ab+tau^2=1`, the characteristic polynomial of C is
`X^2+tau X+1=(X-lambda)(X-mu)`. Its roots are distinct, so `C^5=I` and
its eigenvalues have order five. Explicitly,

    C   = [[ 9,7],[7,14]],     C^2 = [[11,6],[6,13]],
    C^3 = [[13,6],[6,11]],     C^4 = [[14,7],[7, 9]].        (O5-1)

Put

    A=diag(1,10),       B=diag(14,1),
    E=diag(12,8),       D=diag(1,12),
    S=[[7,7],[1,6]].

Direct multiplication in K gives

    S=A C B,       S^-1 C S=diag(lambda,mu),
    Q=E C D C^2.                                           (O5-2)

For a symbolic check of the first identity, use eigenbasis
`S=[[tau,tau],[lambda+a,mu+a]]`, set
`A=diag(1,(mu+a)/b)` and `B=diag(tau/a,1)`, and substitute the displayed
a,b,tau values. For the second identity, `C D C^2` has zero diagonal
and off-diagonal entries `10,15`, whose inverses are `12,8`.
Both off-diagonal entries must be nonzero because its factors are invertible.

On an equal-field fixed point define **all** of C,Q,A,B,E,D,S as the
identity. Every word in O5-2 is then also the identity. On each nontrivial
two-element orbit use the smaller/larger-address order of the source.
This convention is required: applying an arbitrary pair diagonal to a
fixed point would change the target.

## 2. Simultaneous converters and swap reconstruction

For m disjoint field pairs, write subscripts j for the corresponding
local operators, put `F_r=product_j C_j^r`, and put a capital Delta before
a diagonal letter for its product over j. Operators at different indices
commute. Consequently

    mathcal S=Delta_A F_1 Delta_B,
    mathcal S^-1=Delta_B^-1 F_4 Delta_A^-1,                 (O5-3)
    product_j Q_j=Delta_E F_1 Delta_D F_2.                 (O5-4)

The forward spectral converter is `mathcal S^-1` and the inverse is
`mathcal S`. Each requires **one** complete target transform, respectively
F4 or F1, plus pointwise diagonal scans. The closed family of targets
needed is `{F1,F2,F4}`: the converter children always use F1/F4, and
the final swap word additionally uses F2.

All pointwise diagonals have fixed K coefficients. Their products are
computed from the m smaller/equal/larger comparisons in the actual
physical layout. The source fixed-parameter comparison scans apply;
no diagonal is commuted across a changing address basis without proof.

Every power C^r has a constant off-diagonal entry `gamma_r`, equal to 7
for r=1,4 and 6 for r=2,3. Therefore

    C_j^r = gamma_r Q_j + M_(j,r),                         (O5-5)

where M is pointwise diagonal: its pair values are the diagonal of C^r,
and its fixed-point value is `1-gamma_r`. Thus an order-five affine pencil

    A_0+sum_j sum_(r=1)^4 A_(j,r) C_j^r

uses one shared-swap pencil with coefficients
`sum_r gamma_r A_(j,r)`, plus pointwise comparison masks in the original
layout. The characteristic-two label geometry is unchanged. The scalar
field grows from F4 to F16, which is a fixed factor in its binary encoding.

### Why the corresponding order-three choice cannot do this

For a nontrivial symmetric two-by-two order-three gate over a
characteristic-two field containing omega, normalize its eigenvalues to
omega,omega^2. A one-gate diagonal factorization of an eigenbasis would
require equality of the diagonal-scaling cross ratios. The equation
forces the top-left entry to be omega or omega^2 and the off-diagonal
entry to vanish. That is not a nontrivial shared-swap gate. For the
specific earlier gate `[[0,1],[1,1]]`, the same obstruction is immediate:
one C or C^-1 between invertible diagonals retains a zero entry, while
every eigenbasis has four nonzero entries. Order five avoids this
degeneracy. This is a statement about these diagonal words, not arbitrary
spectral converters or arbitrary local gates.

## 3. Two-predictor repair over any fixed finite field

The earlier four-element discrepancy trick extends directly to K=F16.
More generally, let all predictor eigenvalues p_i and target eigenvalues
z lie in a finite subfield `K=F_Q` of the common coefficient algebra,
with z nonzero. Suppose p_i=z outside a known set J of size at most s,
and an s-by-R check matrix H has an invertible column minor on every
such J. The source Vandermonde checks have this property.

Form PX and the 2s checks `HPX,HX`; convert those checks to the common
spectral basis. They determine `e_i=(p_i-z) Xhat_i` on J. The spectral
table chooses a lift a satisfying

    (H^T a)_i=(p_i-z)^(Q-2) e_i  for i in J.               (O5-6)

It returns the pair a,za. After inverse conversion form ordinary rows
Z,F_r Z by H^T and output

    PX-PZ+F_r Z.                                           (O5-7)

Its error on row i is `(p_i-z)(Xhat_i-Zhat_i)`. If the gap is nonzero,
its `(Q-1)`st power is one and O5-6 gives `Zhat_i=Xhat_i`; if the gap
is zero the error is zero regardless of the lift. The formula therefore
uses **two** predictor applications and a spectral table on 2s rows.
In characteristic two the signs in O5-7 are additions.

For K=F16 the exponent in O5-6 is 14. Predictor values remain in K even
if the Vandermonde nodes are taken in a larger finite extension. All
nonzero gaps are units there. There is no assumption that an arbitrary
element of the extension has fifteenth power one.

## 4. Explicit constant-tail predictor and finite data

For a fixed target F_r, r in {1,2,4}, use all m order-five query powers.
At a spectral tuple q_j=zeta^(k_j), shifts beta in F5^m give ordinary
digits `b_j=(r k_j+beta_j) mod5` in `{0,...,4}`, and count `c=sum_j b_j`.
One may use all shifts, or the following explicit small family.

Let `B0=5^v` be the least power with `(5^v-1)/4>=m`. Choose m nonzero
linear forms on F5^v representing distinct one-dimensional subspaces;
enumerate all B0 seeds. These shifts are pairwise independent and uniform
in F5 at every fixed spectral tuple. Hence

    4m+1<=B0<20m+5,    E[c]=2m,    Var(c)=2m.             (O5-8)

Let `b_win=6 ceil(sqrt m)`, T the least power of two at least
`2 b_win+1`, `D_pred=T-1`, and `u=2m-floor(D_pred/2)`. The interval
`[u,u+D_pred]` contains `[2m-b_win,2m+b_win]`. Chebyshev gives

    Pr[c outside the interval] <=1/18<1/16.                (O5-9)

For `m>=4096`, `D_pred<=25 sqrt(m)<=m`. The source integral formula is

    P_beta=zeta^(u-sum_j beta_j)
        sum_(h=0)^D_pred (zeta-1)^h binom(c-u,h),           (O5-10)

where the binomial is represented in the individual query variables,
not by dividing by h!. On the interval it equals
`zeta^(r sum_j k_j)`, the required multiplier.

Every binary bit of a digit b_j is an affine combination of the five
spectral indicators and thus of the individual query powers. The three
input bits have degree budgets 1,2,4. The accepted characteristic-two
ripple-carry formula (B1--B7 of `characteristic-two-count-formula.md`)
therefore applies without change: it gives polynomial-m-size copied
formulas for the required low count bits, degree budget 2^i for bit i,
and total syntactic degree at most h for each binomial coefficient.
The power-of-two budget version gives every addition a power-of-two
factor length. The characteristic-two cyclic full-rate factorization
then uses no additional odd-order roots and yields D_pred affine pencils
on a power-of-two row module of dimension w with `log2 w=poly(m)`.
Every one of its w coordinates is an independent input.

The construction is uniform in beta and r: keep the same expression
shape, bit budgets and zero leaves for all shifts and targets. The final
predictor values are in K. Direct-sum over the B0 shifts and duplicate
by 16, giving `R=16 B0 w`. Its exceptional set occupies less than R/16
rows at each frequency. Use the inflated budget `s=R/16=B0 w`.

For compact structured checks one may take
`E=F_(16^e)`, `e=ceil(log_16 B0)`, with Vandermonde checks on the B0
shift positions tensored with the identity on the duplicate/module rows.
There are at most `floor(B0/16)` bad shifts. Pad the genuine check rows
to exactly s. A polynomial-in-m finite-field constructor and the inherited
on-demand spectral repair can process these checks without listing w
rows; that compact execution remains a separately reviewed supplier.

Without any compact-executor assumption, an entirely explicit expanded
finite construction is still available: use enough finite-field nodes
for all R rows, enumerate the affine matrices and the finite spectral
tables, and use the accepted formula-size bound. Because
`R<=2^(m^K)` for an absolute K and field extension degree is O(log R),
the elementary list-and-arithmetic constructor costs `2^(m^K')` time
and space for an absolute K'. Exhaustive irreducible search of degree
O(log R) over F16 is within that budget. Thus the component has a
bounded, unconditional finite constructor; polynomial local tape costs
are not inferred from its description size alone.

## 5. Finite full-rate closure and its exact call invoice

Let N be the retained label count and let `R_pencil(m)` denote the
source's shared-pencil recursive-swap call bound per independent row.
For a total repair depth h start with

    W_h=N R 8^h

independent E-valued rows, retaining the label. A repair node for any
of F1,F2,F4 has exactly two child phases: one F4 in the forward converter
and one F1 in the inverse. Each phase processes `2s=R/8` rows per base
batch. For each group of eight parent copies, the conversion rows have
coordinates `(copy8,half2,check_B0,module_w)`; combine the first two
into the 16-valued duplicate coordinate to obtain one canonical child
batch `(shift_B0,dup16,module_w)`. This is a bijection of occupied rows;
no input row is dropped or assumed zero. Reverse it after the child.

At finite leaves compute each C_j^r directly by O5-5, using at most m
ordinary swaps per row. With `a_m=2 D_pred R_pencil(m)`, induction gives

    sigma_(r,h)/W_h
      <= a_m sum_(j=0)^(h-1) 4^-j +m 4^-h
      <= (4/3)a_m+m 4^-h.                                (O5-11)

The two children each have volume fraction 1/8, so their total mass
is 1/4. They execute sequentially in the actual converter order; the
table is computed after the forward word and before the inverse word.

Use O5-4 to compute the final ordinary swap product with two target
transforms sequentially on the same full batch. Then

    sigma_(Q,h)/W_h
      <= (16/3) D_pred R_pencil(m)+2m 4^-h.                (O5-12)

For `h=ceil(log2(m)/4)`, the leaf term is at most `2 sqrt m`, while

    8^h<=8m^(3/4),     sigma_(Q,h)/W_h=O(sqrt m(R_pencil+1)).

The same label geometry and occupied reserves are used. In a depth-first
implementation finite-repair parked payload is bounded geometrically by
the child ratio 1/8; siblings and the two final target words reuse marked
regions. The spatial recursion and binary field packing still require
their own ordinary source/supplier arguments. No infinite self-call is
hidden in O5-11: the displayed depth is finite and every leaf is direct.

## 6. Profile consequence and next gates

The local asymptotic call profile remains

    sqrt m * 2^{O((log m)^(2/3)(log log m)^(1/3))}

under the retained label invoice. The converter shortening changes its
finite word, recursion and constants; it does not remove the label
factor or establish a tighter global H(n). It must not be reported as
a new exponent for integer multiplication.

Every E002 compact operation that is algebraic over a fixed
characteristic-two base field has the same polynomial-m shape here:
F16 rather than F4 is constant size, B0=O(m), count inputs have three
bits rather than two, and on-demand gap inversion has fixed exponent
14. Rational address geometry is identical. A full compact physical
composition nevertheless needs an explicit review of the scalar
executor, spectral check batching, local metadata and binary packing.

Open next questions:

1. Independently check the complete polynomial local executor under this
   order-five substitution. It is an applicability claim, not granted
   merely by the finite word identities.
2. Can converted check rows be retained and shared across several repair
   uses, reducing even the two-conversion port invoice? A zero-query
   diagonal-only converter cannot diagonalize a nondiagonal C, so the
   one-transform word is minimal within this diagonal-word model.
3. Can the smaller converter branching interact with a rank-sensitive
   second predictor to reduce actual spatial-call cost? This would change
   the remaining invoice premise and needs a new full-rate proof.

## Sources and credit

Pinned source: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`,
Fourier `build/repair.tex` and tape `build/interchange.tex`.
Programme imports: characteristic-two label geometry, cyclic full-rate
factorizations (with its matrix-factorization literature credits),
power-two degree-budget count formulas, and the earlier order-three
repair/word construction. Source state at the start of E003 was
`a2d9c4b00c02dadf7bdc970acf9190dfabf9ec32`.

The two-by-two gate was obtained by solving the diagonal-equivalence
cross-ratio condition. Root independently derived the general symmetric
reciprocal-eigenvalue condition and checked the order-five specialization.
Credits: Jerry Chen (@CubeJerry), the source authors and programme
predecessors, and substantial AI-assisted E003 construction and review.
No literature-priority, full-machine execution or Lean claim is made.
