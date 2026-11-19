# Genuinely coupled three-matrix covariant sources

**Source and genuine early-phase existence over GF(512), including five
inequivalent coupled components. Shared H/D/K transport and both strict
suppliers remain open. No new complete κ.**

## Full family and source witnesses

Let S=F^16 and let C range over the four matrix units of the local
Clifford algebra A_H=M_2(F). On three original matrices define

```
F_(j,H)(X)_a = sum_(b=0..2,C,t=0..15) R_(C,t)[a,b] C X_b e_t.
```

There are 576 independent parameters at each incidence. Under the
commutant M_8, the input is96 copies of the simple8-dimensional module
and the output is6 copies, so this is the full6-by-96 equivariant Hom
space. Independence follows by isolating an input copy, input column
and output copy, then using independence of the four matrix units.
Every parameter changes a rank8 map. Covariance F(LX)=L F(X) holds
for every L commuting with A_H; separate phase frames need not be covariant.

A foreign view has dimension768. Its determinant is a nonzero polynomial:
specialize to three copies of the corresponding S027 256-dimensional
witness. Actual early quotas are24,48 or72. Use24 early quotient rows
in the first case,48 in the second, and48 quotient rows plus24 genuine
extra rows in the third. The quotas sum to768 per donor. Three copies
of its S027 early witness prove that early determinant nonzero too.
These direct-sum witnesses establish formal nonzeroness; the common
assignment below is additionally constrained to have genuine coupling.

A source parameter occurs in at most36 foreign determinants and one
early determinant, with individual degree at most8 in each. The full
source/early product therefore has degree at most296 in that parameter.
Frame and extra-row parameters have individual degree at most1. The
polynomials have binary coefficients; witness fields need not embed
in the eventual GF(512).

## Coupling under separate input/output copy gauges

At donor0/H263, take three3-by-3 coefficient matrices
`A=R_(C00,0), B=R_(C00,1), C=R_(C00,2)`. Put

```
d=det(A), U=adj(A)B, V=adj(A)C,
W=det[vec(U^i V U^j): 0<=i,j<=2].
```

Both d and W are nonzero polynomials: A=I, B=P a three-cycle, and
C=E00 give the nine matrix units in permuted order. If dW is nonzero,
the relative matrices A^-1 B and A^-1 C generate all M_3(F). Their
nine displayed words are independent, since the scalar d is nonzero.
No proper nonzero copy-axis subspace is invariant under both, even
after field extension. Separate input/output copy-axis basis changes
send the relative matrices to simultaneous conjugates, so cannot turn
this coefficient system into smaller independent copy blocks.

This claim concerns the declared copy axis. It does not classify arbitrary
basis changes mixing all matrix entries or assert decoder compatibility.

## Five inequivalent components over one fixed field

Take five independent copies of the576-parameter family. For each c use
d_c,U_c,V_c,W_c above and put n_c=tr(U_c). Include the factors

```
product_c d_c W_c,
product_(c<e) (n_c d_e + n_e d_c).
```

The second product requires pairwise distinct tr(A_c^-1 B_c), an invariant
under separate input/output copy-axis basis changes. Thus the five triples
are inequivalent under those changes. The factors are nonzero: choose
A_c=I, B_c=P+lambda_c I, C_c=E00 with five distinct scalars. Words in
P+lambda I up to degree2 span the same space as words in P, because the
change of polynomial basis is triangular with diagonal1. The nine matrix
words remain independent. This also supplies a simultaneous witness for
all the coupling factors alone.

Optionally include a nonzero entry of a commutator of48-dimensional source
coefficient matrices at two other input columns3 and4. The specialization
R_(N,3)=I_3 and R_(M,4)=I_3 gives commutator I_3 tensor I_16. That factor
is therefore nonzero and ensures that the selected source is outside
the globally commuting coefficient class.

The individual degree remains below512. In W, a determinant monomial
contains27 adjugate factors: sum_(i,j)(i+j+1)=27. A conservative A-entry
bound is54; B-entry and C-entry bounds are18 and9. The determinant d
adds at most1 to an A entry. Four trace-separation factors add at most8.
Including the source/early degree296 gives at most359. Even allowing
an unnecessary further2 for the disjoint commutator factor gives the
safe bound361. Other variables have smaller degrees; frame/extra-row
variables still have degree at most1.

All factors are nonzero polynomials over F_2. Their product is nonzero
in the polynomial ring. The finite-grid nonvanishing lemma consequently
gives a simultaneous assignment over GF(512): every foreign and early
map is invertible, each component has genuine three-copy coupling, the
five components are inequivalent, and the selected source coefficients
do not commute. This is a proved existence theorem. A complete coefficient
file with these additional constraints has not been selected here.

## Actual bank and remaining interface

Each component has bank768 and quotient width48. Five components give
bank3840 and quotient width240, fitting the bank-480 atlas repeated eight
times. The actual early counts become120,240 or360, including all genuine
singleton extras. The late parity count is unchanged. The existing dense
source compiler supplies a finite paid upper bound; no field expansion,
cache, frame or inverse is declared free.

The components vary independently. The theorem supplies no fixed class
assignment across H and D, and does not import the excluded fixed-class
decoder. A coupled source is not itself an escape from every H/D barrier.
The immediate obligation is to impose the exact nine-port inverse graphs
on these same source coefficients and genuine early maps. The accompanying
common-lift theorem excludes one simplification, not the entire family.

Credit @CubeJerry, the S027 source and native/Clifford contributors, and
S028 Worker A's port-divisibility analysis. Developed by S028 Worker B
with substantial OpenAI assistance. Apache-2.0. No new complete κ.
