# Independent review: stacked active-first interface gate

Worker B reviewed root's final proof with SHA256
`3035b08b1ce557b2de528e2e842e38a83778ceebdcad2144a7d05f7742fa9367`.
The theorem and its stated quantifiers pass mathematical review.

The idle row forces q21=q22=0 by ordinary/rank1 separation. The resulting
rank1 image of input0 has an invertible last-output projection, so the other
two input columns must have zero rank1 component when its total rank is D.
The full active2-by2 prefix, with neither triangularity nor individual-unit
pivots, has last-column rank3 part exactly -[T_w;T_g;0]q12. All other words
there have at most two source A factors. Thus the stack-injectivity premise
forces q12=0, and Q's full invertibility forces q02 to be a unit.

The next stripping step is valid term by term: pi1(a g a)a^-1 consists of
selected A G words, all pure rank1. It cannot cancel ordinary w. Hence w=0;
there is no need to assume w was individually invertible. Invertibility of
the active first interface now forces g,v to be units. The last endpoint
column is a unit supported only on the middle output bank, and the target
class restrictions make it wholly rank2. The total rank2 image therefore
fills precisely that bank. The top block a v a q11 a in input column1 is a
unit; its rank1 and rank2 components must vanish, while its words have at
most three A factors and cannot have rank4. Every other class is prohibited.
This final contradiction correctly uses wordwise support and faithful tensor
components, not a false bound on the support of an arbitrary finite sum.

The q11-unit argument remains valid even when q00,q01 are unrestricted:
a vector in its kernel would give the exhibited kernel vector of Q after
using q02^-1. Every inversion used for cancellation is a consequence of the
complete ordinary matrices and finite dimensionality, not division by a
sector projector. The positive complementary-projector control proves the
stack condition is strictly broader than either individual pivot condition.
The ordinary clock control genuinely fails the stack premise and is not
misrepresented as an endpoint.

The separate checker review_active_first_gate.py imports no root checker.
It reuses B's independently written free noncommutative-polynomial ring,
extracts the entire last-column degree3 part directly, and verifies the full
idle row and the final zero-w block identities. It constructs the literal A
from the INPUT phase abd and its two output amplitudes. For the complementary
projectors it proves the stronger exact identity T_w* T_w+T_g* T_g=I,
checks both projector traces are8 and the conditional bank swap is an
involution, and verifies the unit-clock failed-hypothesis support4 control.
Results are in ACTIVE-FIRST-INDEPENDENT-REVIEW.json.

The theorem applies for each fixed finite template after its own faithful
width V0, including stripped word products and actual tensor phases. It does
not exclude arbitrary isolated small-width factorizations, noninjective
stacks or a first interface that mixes the idle role. No new ordinary service,
Gaussian discount, supplier admission or kappa follows. Credit root's two
extensions, B's original proof and stack sharpening, @CubeJerry and retained
source/component contributors; substantial OpenAI assistance.
