# Independent review of the full covariant source theorem

**Admit the stated source-existence theorem. Do not infer a shared decoder,
a strict BIT supplier, or a new multiplication exponent.**

Reviewed from programme commit `9e3fa0639d8a2bcf5660a950482af6ce9e0af57c`.
The reviewed author package is
`work-in-progress/2026-11-19-S027/covariant-trace-source`. Its files remain
unchanged by this review. Exact input hashes and decompressed witness hashes
are in `output/REVIEW-RESULT.json`.

## Mathematical review

Let `S=F^16` and let `H` be an actual anisotropic binary plane. For two
distinct roots of H, write `N=gamma(j)+I` and `M=gamma(k)+I`. The identities
`N²=M²=0` and `NM+MN=I` imply that the four displayed matrices are matrix
units for `M_2(F)`. The image/kernel identity for N gives a basis of eight
vectors for its image, followed by their M-images; in that basis the
representation is `F² tensor F⁸`. This argument works in characteristic
two, including the inseparable-looking involutions used here.

The commutant is `I_2 tensor M_8(F)`. As a module for this full matrix
algebra, `End(S)` has32 copies of its simple8-dimensional module and S
has2 copies. The equivariant Hom space therefore has dimension64. The
maps `X -> C_ab X e_t` are independent: fix one input column t, vary that
column arbitrarily, and use independence of the four matrix units.
They thus give exactly the claimed full64-parameter family. Each such
parameter has rank8 as a map from End(S) to S. Covariance with every
visible receiver follows because its gamma commutes with the local
matrix algebra; no claim of covariance of a separately chosen early
frame is needed or justified.

The partial trace in the author witnesses is an alternative coordinate
system on this same Hom space. In the adapted basis,
`[gamma(j),[gamma(k),X]]=I_2 tensor(X_00+X_11)`. Trace pairing on M_2 is
nondegenerate even in characteristic two, so the64 coefficients in the
partial-trace expression do not restrict the family further. The checker
evaluates its nested commutator directly, without importing the author's
conversion into the left/right coefficient basis.

The single foreign witness is sufficient to show that each individual
foreign determinant is a nonzero polynomial. The independently generated
transvection orbit contains all7,560 ordered orthogonal pairs in the
120-root completion, including all6,470 actual foreign pairs. The actual
Clifford matrices implement these permutations by conjugation. Transport
of the witness conjugates the input and changes every output by an
invertible map, so preserves invertibility and the covariant family.
Intermediate nonnative roots in this symmetry proof are algebraic
isomorphisms only; they are not extra physical sources.

For early rows the111 separate certificates use the actual route quotas.
The type24 flags genuinely retain their eight extra rows, and their
fields are included in the256 original early owners per donor. Their
successful determinants are nonzero polynomials in the same source
variables plus independent early-frame/extra-row variables. They do not
need to use the coefficient assignment from the foreign witness.

All factors have binary coefficients. Their nonzero product exists in
the polynomial ring, an integral domain. A given source scalar occurs
in at most36 foreign determinants and one early determinant, with degree
at most8 in each: its matrix update has rank8, including after multiplication
by the variable early frame. An entry of the chosen coefficient commutator
is a nonzero polynomial, witnessed by N and M. Multiplying by it raises
the safe individual degree bound to298. Early-frame and extra-row
variables have degree at most1. The elementary finite-grid nonvanishing
lemma therefore applies over GF(512). Witnesses over GF(16) prove
formal nonzeroness over F_2; GF(16) need not embed in GF(512).

Full early rank forces every selected early block to have independent
rows. Thus an8-row frame can be completed to16 rows, and a16-row frame
is invertible. These completions preserve the abstract quotient, but
their downstream temporal use remains an open requirement.

Direct sums on r matrix copies preserve every asserted property. The
literal bank480 route proportions fit at r=15a, so the first bank is3840.
This repetition argument supplies arbitrary compatible banks; it is not
an extrapolation of a finite rank experiment to a new multiplication
theorem.

## Independent computation and negative controls

`independent.py` imports no author code. It reconstructs the lattice and
hyperbolic coordinates, generates the full transvection orbit from scratch,
checks all actual conjugations, evaluates the nested trace tensors directly,
and computes ranks by Gaussian elimination over GF(16). The author instead
re-expands the tensors in a coefficient basis and computes binary ranks.

All112 determinant witnesses have field rank256. The full plane census,
4,480 rank8 coefficient checks, source quotas,88 extra early fields and
the36-view maximum are confirmed. Removing one whole foreign quotient
reduces its rank to240. Removing actual early groups at donors0,5,77,110
lowers rank by exactly the omitted number of rows. A duplicate-row control
also detects a deficient rank. The GF(512) polynomial is checked by
excluding every monic factor of degrees1 through4, independently of the
author's Frobenius/gcd criterion.

The receipt records exact finite evidence. The universal claim rests on
the preceding module, transport, polynomial and direct-sum arguments.
This is a separate agent's mathematical review and separately implemented
exact computation; it is not human review or formal-kernel verification.

## Source invoice and boundary of admission

At r=15, the nine-bit binary bank has34,560 lanes. There are2,889,000 late
parity caches. For each of111 donors, compiling the forward early map
and its inverse costs at most twice `M²+3M` ADDs. Computing each late
parity from at most M source lanes and injecting it once costs at most
`M+1` ADDs. Hence the reviewed bound is365,025,125,160 ADDs, with
2,889,000 INIT, charged dirty CLEAR and extra stationary peak, and no
additional MOVE. This is the source module's finite upper bound; its
inverse is applicable after any separately paid downstream early inverse.
It does not include missing downstream words, return fields, supplier
admission or recursive computation.

Coefficient selection is a finite setup computation, with no practical
bound in the reviewed author theorem. The existing compiler and owned
erasure assumptions remain visible. Native all-columns, precision tape
and analytic recovery are also retained by the enclosing programme.
The theorem admits source feasibility; it does not admit the same source
as a solution of the shared H/D/K inverse-lift constraints.

## Reproduction and next question

Run from any directory:

```sh
python independent.py --repo /path/to/repository --out /new/output/directory
```

Use `--source` if the unchanged author package is relocated. Expected
status: `PASS_INDEPENDENT_FULL_COVARIANT_SOURCE_REVIEW`.

The next useful finite step is to emit one common coefficient assignment,
then test its actual inverse-lift spaces against the shared H/D/K demands.
Existence of a convenient assignment does not make those extra equations
automatic.

Credit @CubeJerry, the S027 full-covariant-source author and predecessor
native atlas, Clifford and source-compiler contributors. Independent S028
review by Worker B with substantial OpenAI assistance. Apache-2.0.
