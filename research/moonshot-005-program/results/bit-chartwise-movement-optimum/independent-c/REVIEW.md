# Independent review: uniform-chart movement optimum

**Accepted within its explicit fixed-cut transverse target scope.**

I read the principal proof without using its checker as mathematical evidence.
The lower bound is valid with dependent and redundant messages. After the
cost-reducing normalization, n counts all arrivals, q those with a nonzero Hub
part, and l direct Hub arrivals. The three inequalities are sound: q>=c
follows from K intersect D=0; n-l>=t follows because held projections are
chart supported; n>=c+t-p follows from the joint arrival span and K intersect
H. The coefficient on l is nonpositive and the remaining n,q coefficients are
positive under 0<B<A<=B+C, so all substitutions have the stated direction.
This gives (c-p)A+pB+tC with no packet independence assumption. The previously
proved explicit quotient-complement construction attains it.

Transversality is material. The displayed two-generator counterexample has a
held-only difference and permits cheaper direct-Hub plus proper-born delivery
when A<2B. Earlier point helpers also change the fixed-source premise: genuine
access at their earlier charts is precisely the mechanism in the contemporary
incidence-funnel source. The two theorems are compatible.

I independently implemented a different finite optimization. For every binary
ambient subspace it computes a cheapest admissible vector basis by weighted
basis exchange/greedy, then minimizes over all superspaces containing the
target. This differs from the author's Dijkstra traversal. Four dimension and
partition cases with four price triples give560 transverse cases including
zero (544 nonzero); all agree. Nontransverse failures are retained. The
optimizer uses the proposed formula only at the final comparison.

No correction is requested. Algebraic arbitrary-field and block-dimension
bounds do not provide free scalar implementations; the author's fixed binary
whole-record attainment and explicit implementation caveat are necessary and
present. Costs outside acquisition and all five foundations remain.

Reproduce:

    python3 check.py --proof /path/to/author/PROOF.md --out output

The reviewed proof SHA256 is in output/RESULT.json. Credit @CubeJerry,
root's theorem and earlier query-repair authors, Worker C's independent proof
review and finite optimizer; OpenAI assistance. No new kappa.
