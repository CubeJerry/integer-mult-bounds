# Rational address heights and a bounded finite constructor

Status: **accepted for the stated source-extraction contract after independent review**. The finite-generator gate is recorded in `../C/REVIEW-A-BOUNDED-GENERATOR.md`; the physical and end-to-end gates are recorded in `../../verification/S002/lead-review-physical-compiler.md` and `../../verification/S002/lead-review-explicit-extraction.md`. This is an AI-assisted mathematical audit, not a formal build or execution of the complete multiplier.

Sources: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, November
tape `interchange.tex`, Fourier `kernel.tex` and `repair.tex`, and September
tape `sections/04-swap.tex` (constructive triangular factorization).

## 1. An elementary uniform height bound

Define rational height as the maximum bit length of the reduced numerator
and positive denominator. For a matrix with dimensions at most K and entry
heights at most H, clearing all denominators costs at most K^2 H bits.
Every minor of the resulting integer matrix has at most
K(K^2 H+log2 K+2) bits, by the determinant expansion. Inverses, canonical
solutions, kernel bases, and coordinates in a selected column basis are
ratios of minors. A loose common height bound is K^6(H+log2 K+2).
Greedy column selection, fraction-free elimination, and appending standard
unit vectors compute bases and complements in polynomial time at these
heights. They do not search through arbitrary rational vectors.

For the source ordered Bruhat factorization, follow its prescribed pivots:
topmost active nonzero row, then its rightmost nonzero entry. Clear left
by column operations, clear below by row operations, and normalize.
Active entries and elimination multipliers are ratios of original minors
(Schur complement identities). There are O(K^2) elementary factors. Take
Q to be the product of all their denominators. Its bit length is polynomial
in K,H. Products of the factors have denominator dividing Q^{O(K^2)};
their numerator norms are bounded by products of row-sum norms. This also
handles inverse elementary factors. Thus K^10(H+log2 K+2), with an absolute
constant enlargement, bounds all final factors and inverses. Every pivot
reciprocal and diagonal unit is included. This establishes a polynomial
height bound without assuming that arbitrary rational elimination has
free intermediate cancellation.

## 2. Applying it to every source layout

The constructor explicitly guards that interchange has at most m^5 labels,
Fourier at most m^3, p<=m, and prediction degree <=m. Increase the absolute lower starting
value of m as necessary. Let K=4m^6 bound all local matrix dimensions.
The rational Gram entries have height O(log m); their only nonintegral
factor is 1/p. The dependency chain at each label/endpoint is:

1. Select independent columns J of the symmetric Gram matrix G. The
   principal matrix G[J,J] is nonsingular because those columns represent
   a basis of the nondegenerate quotient by the radical. Represent a
   generator v by G[J,J]^{-1}G[J,v], retaining G[J,J] as the pairing.
2. Compute the kernel of the two functionals defined by x_v,y_v. This
   constructs their orthogonal complement. They are orthonormal, so it
   has the required dimension and is a direct complement to their span.
3. At a rectangle select a basis of the differences spanning E. Append
   the reference pair, and then standard unit vectors to obtain C. Basis
   selection discards columns and does not compound their heights.
4. Lift each C vector by subtracting its projections onto the endpoint
   pair. Combine these lifts with the E basis. Obtain transition maps
   and their inverses by matrix products and solving in these bases.
5. Compute triangular factors and inverses for every required conversion.
   Conversions between two selected layouts require one inverse/product.

Each endpoint is constructed independently. The generator retains the
elementary instruction sequence; it does not compose every query and
endpoint into one ever-growing matrix. Fewer than one hundred applications
of the preceding operation bound cover this chain, even counting the
products and inverses separately. Hence, for sufficiently large m, every
listed rational height is at most

    m^10000.                                                    (AG1)

Every nonzero numerator/denominator therefore has numeric magnitude at
most 2^{m^10000}. This includes explicitly retained determinants, pivot
reciprocals, inverse maps, and every required diagonal unit. Complete the
entire list before choosing a radix prime above its maximum and the batch
width. This guarantees compatibility modulo every power of that prime.

Over F_p and F_2 the rank factorizations and direction bases retain O(log p)
and one-bit entries. Fourier rectangle weights come from a triangular
interpolation system of size at most L+1; the same determinant argument
bounds their dyadic heights polynomially in m. These are numerical row
coefficients, not address maps requiring further radix compatibility.

## 3. Counts, scalar letters, and program representation

Finite tuple enumeration constructs all labels and rectangle incidences.
Even inspecting all label pairs is polynomial in m in the chosen range.
Retaining every endpoint basis, factored map and local call instruction
adds fixed polynomial factors. The scalar construction is detailed in
`scalar-template-growth.md`: R<=2^{2^{2m+1}}, cyclotomic degree <=R,
expanded matrix dimensions and coefficient heights polynomial in R,
and all 2^m frequency tables explicitly listed.

No flat truth table of the possible algebra elements is generated. Over
the odd characteristic p, one letter is a fixed block of <=R coordinates
with O(log p) bits each. A scalar multiplication uses its coordinate-linear
matrix or ordinary modular arithmetic in polynomial R work/space. The
same algebra is used at every recursive depth. A child receives already
encoded letters; it does not extend or repack that algebra again. Thus
there is no hidden R^{depth} alphabet expansion. Initial bits embed as the
two constant algebra elements and are decoded only at the top boundary.

Walsh descent gives dyadic row matrices. The one odd selected bit outside
the even-width recursion uses only the fixed number 1/sqrt(2), prepared
by certified bisection; it introduces no growing algebraic degree.

## 4. One explicit common finite envelope

For definiteness use the deliberately extravagant absolute choice

    Rhat(m)=2^{2^{m^100000}}.                                  (AG2)

All finite dimensions, table lengths, numerical coefficient bit heights,
rational address numeric magnitudes, and expanded program size fit a fixed
power of Rhat. Bertrand bounds a compatible radix prime by twice the
maximum of the completed numerator/denominator list and total batch width,
with an absolute adjustment to make it odd. Trial division through this
range takes a fixed polynomial in Rhat. The actual constructor does not
materialize Rhat: it operates on the finite lists; Rhat bounds its cost.

Compile to a common number of tapes using binary arithmetic processors,
stored finite tables, and serialized stream roles. Loop bounds/constants
are binary data. No instruction expands all possible encoded letters into
machine states. The transition list and role counts fit a fixed polynomial
in the expanded data size. Even scanning the whole transition list per
interpreted step costs a fixed polynomial in Rhat, while coded work tapes
use the same fixed block format throughout a candidate execution.

## 5. A bounded constructive certificate check

Optional exact verification can recompute ranks and the low-rank matrix
factorizations; check rectangle partition and incidence data; verify every
rational layout, inverse, Gram block and triangular-factor identity; and
test the chosen radix against the completed list of units/denominators.
It can verify cyclotomic inverse products, matrix-root identities, and
all 2^m Hermite tables in the explicit coordinate ring, then enumerate the
actual call lists and test both strict contractions by integer powers.

For a dense matrix-root check, expansion through degree b has at most
(m+b+1)^b monomials, bounded by a fixed power of R. Every matrix dimension,
ring degree, integer bit length and loop in these constructions/checks
fits a fixed power of Rhat. Schoolbook arithmetic suffices for finite setup.
Consequently the actual constructor, check and retained description satisfy

    generation time, generation space, description size <= Rhat(m)^C  (AG3)

for one absolute C. The O(log(j+2)) failed smaller trials are absorbed by
another fixed power since m dominates j. With p and L fixed during a search,
their q, label counts and scalar dimensions are monotone in trial m, so
even failed trials that do not pass the polynomial-m guards are bounded
by the final accepted dimensions. This is a bound for the specified
finite algorithms, not a runtime inferred from output size alone.

These checks verify finite source identities and call invoices. Correctness
and physical costs at unbounded input lengths still require the source
primitive/recursion proofs and the separately audited physical ledger.

The independent finite-generator review is complete; the common-cap theorem is assembled in `explicit-extraction-theorem.md`. Credits:
the cited OpenAI constructions, @CubeJerry, AI-assisted reconstruction.
