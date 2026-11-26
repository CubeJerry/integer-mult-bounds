# Lead admission of the final state-tree and graph refinements

Disposition: **accept both results in their stated models**. The lead
read both complete proofs and B's independent state-tree review. Exact
reviewed proof hashes are:

* `route-a/ROUTING-STATE-TREE-SHARING.md`:
  `4958f7396176546c8929ee4a6e8d1faf4e4c471a9781e41415c993115b25c6b8`.
* `route-c/ONE-GAUGE-GRAPH-CLASSIFICATION.md`:
  `975bfd042b9956564ced3758146f5cec059a7fe72430c1265ec5b12050a8a397`.

## State-tree mechanism

The lead proposed the threshold-component construction after the Gray
schedule. A and B independently derived and checked its proof. An edge
of weight at most w cannot change a symbol whose size exceeds w.
Conversely the remaining active symbols can reset to the last level
one coordinate at a time; double zero/last-level flips then connect
all patterns of the required parity. The all-high assignments are
vertices only at odd L. This proves the exact component count, including
the absence of mergers at intermediate non-power-of-two weights.

The Kruskal sum therefore is the minimum spanning-tree weight. Summation
by parts also gives the equivalent formula

    M=lambda+2^(t-1)[sum_(j=1)^(t-1) C_L(j)/2^j-1].

The infinite moment bound pays the initial lambda term explicitly via
`lambda<=C_L(t)`. The rising-factorial inequality and its generating
sum give the claimed absolute factorial constants. No unbounded sum is
required to generate the actual finite tree or execute the algorithm.

A closed traversal adds each state's contribution once and uses inverse
changes on return visits. Its source and final destination ranks are one
and D-1, so the boundary is 2D. The exact free bill is 2D+8M. Only
discrete finite control is retained on the traversal stack; numerical
collections remain fixed in number. The independently reviewed state
transition supplies the phase, full-rate and precision interfaces.

The lead read the verifier and independently replayed three complete
graphs: (t,L)=(2,4),(3,3),(4,4). Their 40, 36 and 272 states give tree
weights 53, 75 and 629. The receipt `state-tree-replay.json` contains
all 38,266 tested edges and the exact closed traversals. It does not
claim to repeat A's whole fifteen-case suite. The separate invoice
comparison file evaluates four larger parameter choices by exact integer
formulas, not by enumerating their state graphs.

Tree optimality does not imply the doubled closed tree is the cheapest
open visiting walk, or that every endpoint executor uses these states.
The retained positive subinvoice and separate routing-toll qualification
remain as in B's review. The complete asymptotic envelope is unchanged.

## Directed gauge graph

Assign U_v to each input copy and V_w-perp to each output copy. The
edge equations make these assignments one common W on each nontrivial
component. Input restrictions give W subset span(A)-perp; output
restrictions give span(B) subset W. The interval is nonempty precisely
when all cross Gram entries vanish. This proves necessity, sufficiency
and the full parametrization without a search over subspaces.

For bidirected graphs the two-copy graph is connected across both color
roles exactly when an odd cycle is present, causing the norm-one
contradiction. In the bipartite case it has the two asserted components.
The example 1,2,13,7 has odd self-pairings and precisely the path
orthogonality graph; its first and last directions pair to one. It is
therefore a valid triangle-free failure of complete cross orthogonality.

This extends the already source-reviewed individual monomial-cross-kernel
criterion, not its model. It does not prohibit residual Fourier work,
several gauges, synthesizing a kernel as a sum of paths, or arbitrary
nonmonomial bases. The lead reviewed the universal argument and this
explicit example; C's larger finite assignment checker is attributed to
C rather than claimed as an independent replay here.

Both admissions are AI-assisted mathematical reviews with the stated
finite evidence. No full multiplier, runtime lower bound, formal proof
kernel or human refereeing is asserted.
