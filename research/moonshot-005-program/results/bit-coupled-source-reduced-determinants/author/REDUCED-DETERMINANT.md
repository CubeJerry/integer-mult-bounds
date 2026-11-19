# Reduced foreign determinants and an eight-bit source field

**The full covariant source exists over GF(256), as do the five coupled
three-matrix components with the extra coupling constraints. This is a
source theorem, not a decoder or a new κ. Existing GF(512) coefficient
files retain their actual nine-bit field and invoices.**

## The exact restriction criterion

Fix an actual foreign receiver i and donor j. Let S=F^16, and put
`N_i=gamma(i)+I`. In characteristic two, `N_i^2=0` and N_i has rank8.
For example choose a nonorthogonal root k; the nilpotents
`N_i=gamma(i)+I` and `N_k=gamma(k)+I` satisfy
`N_i N_k+N_k N_i=I`, implying im(N_i)=ker(N_i) and rank8.

For r matrix copies define the input and output nilpotents by

```
D(X_1,...,X_r) = (N_i X_1,...,N_i X_r),
E((y_H,a)) = (N_i y_H,a) over all sixteen visible H and r copies.
```

Both spaces have dimension256r; both nilpotents have rank128r and their
image equals their kernel. Every visible quotient commutes with N_i,
because N_i commutes with its local Clifford algebra A_H. Consequently
the complete unframed visible map Q satisfies `QD=EQ`.

**Lemma.** Q is invertible if and only if its restriction
`Q_0:ker(D)->ker(E)` is invertible.

The forward implication is immediate. Conversely, if Qv=0, then
QDv=EQv=0. Since Dv is in ker(D), injectivity of Q_0 gives Dv=0.
Now v itself is in ker(D), so v=0. Equal finite dimensions make Q
invertible. In bases made from a basis of im(N_i) followed by chosen
preimages, an intertwining Q has block form `[A B;0 A]`. Thus the full
determinant is a nonzero constant times det(A)^2; removing the repeated
factor preserves the exact nonvanishing condition.

This is an algebraic equivalence. It changes neither physical costs nor
an acceptance threshold. The restricted map has size128-by-128 for one
matrix copy and384-by-384 for three coupled copies.

## Why parameter rank drops from eight to four

For a visible plane H, write S=F^2 tensor F^8 so its four matrix units
are E_ab tensor I_8. Since N_i commutes with this full local matrix algebra,
it has the form I_2 tensor T, with T of rank4. Therefore

```
ker(N_i) = F^2 tensor ker(T),
dim ker(T)=4.
```

Each local matrix unit has rank4 on this kernel. A scalar source parameter
acts on one original matrix column, one input copy and one output copy.
Its update in Q_0 therefore has rank4. This remains true in the full
576-parameter three-copy family; coupling does not increase that rank.

The kernel bases are chosen using only the fixed binary Clifford matrices,
not the source parameters, so restriction leaves matrix entries linear
in the same variables. Every reduced foreign determinant is a nonzero
polynomial: any nonzero full determinant witness gives a nonzero reduced
determinant by the lemma.

Frames are deliberately excluded from this step. A chosen early frame
need not commute with N_i. Foreign-view invertibility can be checked in
the abstract unframed quotient coordinates, since each completed frame
is invertible. The genuine early determinant remains the original full
256r-by-256r determinant, with rank8 parameter updates. No early rank
or early cost is divided by two.

## Revised simultaneous field bounds

A source parameter occurs in at most36 reduced foreign determinants
and one full genuine early determinant. Its degree in their product is
at most `4*36+8=152`.

For the original full64 family, the noncommutator entry contributes at
most2, giving individual degree at most154. For the five coupled
components, retain the conservative coupling-factor allowance from
`PROOF.md`:54 for the adjugate word determinant,1 for det(A),8 for four
trace-separation factors and2 for the noncommutator condition. The safe
individual bound is consequently

```
152+54+1+8+2 = 217 < 256.
```

All factors are nonzero polynomials over F_2. The original source witnesses,
direct-sum witnesses for the larger family and independent coupling
specializations prove their individual nonzeroness. Their product is
nonzero in the polynomial ring. The finite-grid lemma therefore yields
one common assignment over GF(256). Early-frame and additional-row
variables still have individual degree at most1. One explicit field is
`F_2[z]/(z^8+z^4+z^3+z+1)`.

This strengthens the existential field bounds. It does not reinterpret
an already emitted GF(512) source as an eight-bit source. New eight-bit
constants, source-frame compilation and any changed invoices must be
identified separately. Shared H/D/K transport, complete suppliers,
recursive accounting and all five foundational assumptions remain open.

## Numerical interface and controls

`numerical.py` constructs an8-column binary basis K for ker(N_i), together
with a binary left inverse R. It checks `R K=I` and, for every required
local coefficient C, `C K=K(R C K)` and rank(R C K)=4. A visible source
matrix is then assembled directly with these8-by-8 coefficients. No
large matrix inverse or quotient basis depending on source parameters
is used.

The constrained source selector uses these exact384-dimensional checks
and separately checks the full768-dimensional genuine early map. Its
optional full-check mode also verifies every unreduced768-dimensional
foreign matrix, providing a direct finite check of the restriction
implementation. Negative controls must retain the distinction between
a deficient foreign restriction and an unrelated early-frame defect.

Credit @CubeJerry, the retained Clifford/source authors, and S028's
coupled-source construction. Developed by Worker B with substantial
OpenAI assistance. Apache-2.0. No new complete κ.
