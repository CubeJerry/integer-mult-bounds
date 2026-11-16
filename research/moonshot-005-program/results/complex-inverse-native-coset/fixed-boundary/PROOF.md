# Exact ordinary preimage certificates for two fixed three-call boundaries

**Proved within the fixed monomial tensor interface at all sufficiently large faithful widths. This is a scoped boundary obstruction, not a general three-call impossibility theorem and not a new kappa.**

## 1. Statement and provenance

For each of the four canonical nonlinear heads A_f=C_b D_f P from the Boolean sign-family package, let a=A_f^tensor V and define the exact admitted three-role native step

    K(a)=[[I,0,a-I],[a,0,-a],[I,I,-I]].

Fix H to be the full finite root-four-phase monomial group on the eight one-column addresses, and let O_V be its tensor-span ordinary algebra. Caller templates and monomial tables are fixed before V grows; actual physical ordinary implementations remain paid. Define the two exact boundaries

    D_lit=diag(a³,a²,a²),
    D_can=diag(C_abc^tensor V,C_ab^tensor V,C_ab^tensor V),

where C_ab=C_a C_b and C_abc=C_a C_b C_c in the normalization of the source. For either D, put B=K(a)^-1 D K(a)^-1. Then, for all sufficiently large faithful tensor widths,

    r in O_V³ and B r in O_V³  implies r=0.                (1)

In particular there are no invertible ordinary P,Q satisfying

    K(a) P K(a) Q K(a)=D                                 (2)

for all sufficiently large permitted widths, for either literal boundary.

The retained generic fixed-boundary gate already treats D_lit under its rank/direct-sum premises. Its checks here establish compatibility with the four newly admitted nonlinear sources. The added result is the actual canonical Gaussian boundary D_can and a finite ordinary-module certificate that quantifies over every ordinary monomial coefficient, rather than a bounded word catalogue of candidate interstages.

These boundaries are ordinary-gauge equivalent as collections of Gaussian jobs. That does **not** make them equivalent as fixed identities(2), since arbitrary outer endpoint gauges cannot in general be absorbed into P,Q. This package excludes precisely the two stated boundaries. It does not exclude K P K Q K=L D R with freely chosen ordinary invertible L,R.

## 2. Exact finite coset reduction

The inverse native step is

    K(a)^-1=[[a^-1,a^-1-a^-2,0],
             [0,-a^-1,I],
             [a^-1,-a^-2,0]].                            (3)

Expand each entry of B as a finite sum of fixed one-column unitary words tensor-lifted to V. Partition its nonordinary terms, separately in each output row, by the right cosets U H. Two terms U,W belong to the same coset precisely when U^-1 W is a root-four-phase monomial. If so write W=U h with the **actual** monomial h; its tensor phase is h^tensor V, not a projective substitute.

Right multiplication by an arbitrary element of O_V stays inside that coset. Distinct nonordinary cosets cannot cancel for sufficiently large V: each contains a finite set U H, and the retained finite tensor-word separation theorem applies to their union after exact projective phases are combined. Thus B r ordinary implies one ordinary-coefficient equation per nonordinary right coset. Collect these as

    C r=0.                                                (4)

No enumeration of the unknown r or of a bounded interstage word class is used. The full ordinary algebra is covered. The finite source-dependent work is only computing the coset partition of the finitely many terms in B.

For D_lit there are five equations. Their first three coefficient rows are

    (I,I,I),     (0,I,0),     (I,0,-I).

They immediately give r_2=0, r_1+r_3=0, r_1-r_3=0, and hence r=0 over the characteristic-zero coefficient field. This is the source-specific reproduction of the retained literal gate.

For D_can there are eleven equations for each of the four canonical masks. Among them are the three isolated coefficient rows

    (I,0,0),     (0,-I,0),     (0,0,-I).                  (5)

They occur as zero-indexed equation rows4,1,7 in the deterministic expansion in the attached certificate. Hence each component of r is separately zero. The certificate gives every original coefficient table and an explicit ordinary left inverse E satisfying

    E C=I_3                                               (6)

in the exact monomial group algebra. Equation(6) is a finite algebraic identity and remains valid in every tensor representation and every width phase sector. The large-width hypothesis is needed only to deduce(4) from the physical ordinary-preimage claim.

The four input tables are a complete finite list of the admitted canonical source classes, not a finite approximation to an unbounded family. `CERTIFICATES.json` stores their full coefficients, literal monomial tables, the left inverses, and the three invertible pivot operations. The standard-library verifier reconstructs B from(3), recomputes the cosets by exact Gaussian-dyadic multiplication, and verifies(6) exactly.

## 3. From zero preimage to the caller obstruction

Suppose(2) held and put R=Q^-1, which is ordinary. Multiplying(2) on the left and right by K^-1 gives

    B R=P K.

The second column of K is the ordinary vector(0,0,I)^T. Therefore B times the second block column of R is ordinary. By(1), that column of R vanishes, contradicting invertibility. No new physical inverse operation or free projection is used: these are consequences of an asserted exact identity.

## 4. Meaningful controls and exact limitations

The baseline K³=diag(a²,a²,a²) is not excluded. Replacing either target by this(2,2,2) boundary makes the same coset constraint matrix have a nonzero ordinary kernel, the second coordinate vector. The checker verifies this for all four source masks; it finds only two unit pivots.

Nor does(1) hold at tensor width1 with the full ordinary span. For any address y, the matrix unit projector E_yy=(I-H_y)/2 is ordinary, where H_y is the diagonal sign negative only at y. Multiplying by an ordinary transposition gives E_xy. Thus O_1 is the complete8-by8 matrix algebra and every B maps ordinary vectors to ordinary vectors. The checker constructs all64 matrix units exactly. This control makes the eventual tensor-faithfulness requirement explicit and prevents a one-column table from being promoted to an all-width ordinary-preimage theorem.

The finite certificates are source and boundary specific. They do not rule out actual clock rewinds, mixed native orientations, different independent Gaussian gauges, freely chosen ordinary endpoint encodings, or non-tensor/width-growing ordinary constructions. Those options require their own identities and complete invoices. All body/idles, precision, ownership, compilation and recursive costs remain unchanged as obligations. No complete supplier saving follows.

Credit @CubeJerry; the retained literal three-call boundary gate and tensor-separation argument; the nonlinear Boolean source and fixed-table compiler contributors; Worker B with substantial OpenAI assistance. Independent review is separate from the author's exact verifier.
