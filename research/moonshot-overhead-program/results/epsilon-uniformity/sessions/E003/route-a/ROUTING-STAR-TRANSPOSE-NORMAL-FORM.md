# The exact star-transposition kernel inside a free Walsh transfer

Status: **proved source-specific normal form and restricted representation
obstruction; independent review pending**. This is an investigation of the
middle-query routing problem left by the E003 two-scale construction. It
does not improve the admitted multiplication bound or establish a tape
running-time lower bound.

The source is OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`,
Fourier `build/kernel.tex`, especially the product of queries,
`eq:kernel-routing-block`, and the complete endpoint-transform subsection;
also `build/binary.tex`. The rational Newton coefficients are those of
programme `routes/B/pairwise-newton-division.md`, B2. The physical comparison
uses the complete tape `build/walsh.tex` and E003
`RATIONAL-WALSH-CONSTANT-SPACE.md`. These three primary files and the cited
programme note were read in full for this investigation.

## 1. A pair register and its query

Let a pair register contain two f-bit slots, and put Q=2^(2f). Its basis
is indexed by `(x,y)` in `(F_2^f)^2`. Define the real matrix C_f by

    C_f[(s,t),(x,y)] = 2^(-f) (-1)^((x+s) dot (t+y)).       (S1)

This is precisely the normalized ordinary kernel of the source query
whose spectral multiplier is `(-1)^(X dot Z)`. Expanding its exponent
shows that C_f is the normalized Walsh transform on the two slots, with
the source's initial/final quadratic signs and exchange of the halves.
Alternatively, conjugating its ±1 spectral multiplier by normalized
Walsh proves directly that

    C_f^T=C_f,       C_f^2=I.                            (S2)

Use m distinguished pair registers numbered 1,...,m and one auxiliary
pair register numbered 0. Write C_j for C_f on register j, and P_j for
the permutation exchanging entire registers 0 and j. All other complete
coordinates remain spectators. In particular

    P_j C_0 = C_j P_j,       C_j C_0=C_0 C_j.            (S3)

P_j exchanges two f-bit slots with their two corresponding auxiliary
slots. It does not interchange individual numerical values with their
address encodings.

## 2. The smallest free pair already contains a star sum

Take the source's binary Gram space of dimension two with ordinary dot
product. Choose one source direction `d_v=e_1` and destination direction
`d_w=e_2`. Both have self-pairing one, and they are orthogonal. This is a
legal free source/destination pair. For example, the native binary label
Gram matrix at q=2 has exactly this two-dimensional quotient: its direction
depends on label parity, and opposite parities are orthogonal.

Choose source coordinates in the order `(e_1,e_2)` and destination
coordinates in the order `(e_2,e_1)`, in both halves. The input common
coordinate map is the identity, the output map exchanges the distinguished
and auxiliary slots, and the common kernel is C_j C_0. Therefore the
off-diagonal transfer in `eq:kernel-routing-block` is

    O_j = P_j C_j C_0 = C_0 P_j C_0.                    (S4)

The second equality follows from S2--S3. Crucially, the same C_0 occurs
on both sides for every j. It is an auxiliary endpoint transform. After
sharing those two endpoints, the exact middle operator of a weighted
pencil is

    sum_j b_j O_j = C_0 (sum_j b_j P_j) C_0.             (S5)

Thus the residual problem is a weighted sum of star transpositions,
with the auxiliary register as the common centre. This is an identity
on arbitrary independent data, not a statement only about basis vectors
of low weight or inputs invariant under register permutations.

The coefficients may also be matrices on an independent row coordinate:

    sum_j B_j tensor O_j
      = (I tensor C_0) [sum_j B_j tensor P_j] (I tensor C_0).

They commute with the auxiliary endpoint. In the rational Newton pencil,
each B_j is diagonal, with entries proportional to
`(-1)^(a_j dot seed)`. Those entries are nonzero for every query and
every seed. The stationary term in the Newton update is a separate
pointwise term; it is not silently placed in S5.

## 3. Every individual free pair has the same kernel after auxiliary changes

The preceding example is not a coincidence of dimension two. Let v,w
be any pair with self-pairings one and `<d_v,d_w>=0` in the source's
nondegenerate binary Gram space D. Their span U is a nondegenerate
two-dimensional plane, and

    D = U direct-sum U^perp.

Choose any basis of U^perp in one half and its paired dual in the other.
At source v, the auxiliary directions can be changed to
`d_w` followed by that basis. At destination w, they can be changed to
`d_v` followed by the corresponding basis. These changes act entirely
on auxiliary axes, so they are independent of j. Let U_v and U_w denote
the resulting fixed auxiliary coordinate permutations, and let C_R be
the product of the pair kernels on the remaining D-2 auxiliary pairs.

In these adapted coordinates, the source transfer has the form

    U_w^(-1) P_j C_j C_0 C_R U_v
      = [U_w^(-1) C_0] P_j [C_0 C_R U_v].              (S6)

Every bracket is independent of j and uses only auxiliary axes. The
same derivation works with a degenerate restriction on a larger free
rectangle's destination span: S6 uses only the nondegenerate plane
spanned by this individual orthogonal pair, not that larger span.

The left bracket uses two one-axis Fourier calls and the right bracket
uses 2(D-1), apart from their auxiliary monomial changes. This is the
same total 2D for an individual pair. It is not a replacement for the
source rectangle schedule: executing S6 separately for all pairs can
destroy sharing across labels and increase the incidence invoice.
The normal form is a diagnostic for the remaining middle operation,
not an uncharged new multi-label executor.

## 4. Why merging all queries into a few monomial terms cannot work

**Theorem S (monomial-sum obstruction).** Let a register alphabet have
at least two letters. Let every b_j, 1<=j<=m, be nonzero over a field,
and let

    S_b = sum_(j=1)^m b_j P_j

act on all `(m+1)`-register arrays. Any representation of S_b as a sum
of r monomial matrices has r>=m. The same holds if the allowed summands
are arbitrary weighted partial permutations, or merely have at most
one nonzero entry in each row. Multiplication on the left and right by
invertible monomial matrices does not change the conclusion.

**Proof.** Choose different letters a and b, and inspect the output
address `(a,b,...,b)`. Under P_j its source address has b at the centre,
a in position j, and b at every other position. These m source addresses
are distinct. Thus this row of S_b has exactly m nonzero entries, one
with coefficient b_j at each such address. No cancellation between
different j is possible in this row. A sum of r matrices with at most
one nonzero entry per row has at most r nonzero entries in every row,
proving r>=m. Invertible monomial multiplication only permutes and
rescales rows and columns, preserving the maximum row support. QED.

The original m swaps attain the bound, so the minimum is exactly m.
For diagonal row coefficients with all entries nonzero, the proof
applies within any one fixed row of the original independent batch.
Allowing a larger monomial permutation that mixes row indices cannot
reduce the support requirement for that chosen output row.

Consequently one cannot obtain an O(sqrt(m))-term middle schedule simply
by finding a better list of common coordinate permutations, including
arbitrary nonzero pointwise weights and common monomial coordinate
gauges. The already shared Fourier endpoints leave a middle operator
whose literal number of independent monomial summands is linear in m.

This is a representation theorem, not an operation-count lower bound.
A factorization may reuse intermediate sums or route several terms
together. A product of sums can expand to many monomial terms while
having few factors. Additional nonmonomial transforms may change the
support argument. No inference from r>=m to Omega(m) physical passes,
Omega(m sqrt(f)) time, or an integer-multiplication lower bound is valid
without an additional explicitly stated model.

## 5. The remaining physical question

The source elementary coordinate changes use f-bit slots, with the
other slots as complete spectators. A conservative executor can therefore
price their interchanges at I(f,k), instead of using the coarser I(a,k)
where a=A f. This improves constants and powers in a local invoice but
does not by itself remove a positive polynomial-arity toll. For example,
separately routing the m star terms gives a sufficient charge of order

    m V [1+I(f,k)]

for this individual-pair middle operation, with a fixed number of
payload arrays. With an ideal I(f,k)=O(sqrt(f)), dividing this retained
charge by V sqrt(a), where A=Theta(m), leaves order sqrt(m). The full
predictor also has Theta(sqrt(m)) successive pencils. Its exact total
charge must still account for rectangles, roles, endpoint calls and
finite repair; S5 alone does not price those operations.

Theorem S establishes that the separate-term list cannot be shortened
below m. It does not establish that the displayed sufficient charge is
necessary. A faster algorithm must share physical movement or intermediate
arithmetic across different P_j, use another algebraic representation,
or change the labels and endpoint factorization. These are genuine
mechanism changes outside the retained equality-invoice barrier in
`../route-b/WALSH-TOLL-INVOICE-BARRIER.md`.

## 6. Finite evidence and open next questions

`ROUTING-verify-star-transpose.py` checks S1 against independent spectral
summation, involution and normalized-Walsh identities, then checks the
shared-endpoint identity on complete finite arrays. It also verifies the
exact m-support witness for signed coefficients and includes controls
that fail after omitting an endpoint, confusing one-slot and pair swaps,
or allowing a zero coefficient in the asserted m-support claim. The
receipt records its exact scope and source hashes. These are finite
algebra checks; no full tape multiplier is executed.

Open questions:

1. Can the weighted star sum on full arrays be evaluated by a shared
   tape-routing procedure whose cost is substantially below m separate
   interchanges, while retaining a fixed number of payload arrays?
2. Do the structured signs `(-1)^(a_j dot seed)` permit a useful common
   row transform before or after the star sum? Its cost and the inverse
   transform must be included.
3. Can an individual-pair sharing mechanism be lifted to whole free
   rectangles without paying for every source/destination pair?

Credits: @CubeJerry; the pinned OpenAI Fourier endpoint construction;
programme pairwise/Newton and E003 physical predecessors; substantial
ChatGPT assistance. No exhaustive literature-priority check, formal
kernel refinement, human refereeing, or improved complete H is claimed.
