# Sign-history stabilizer and completeness of PR6166's gauge pruning

This is an independent audit of the implication in Matarener's PR6166,
`PROOF.md` section 3, and of `Model.canonical` / `Model.merged` at
`f7d6431080b375914216d76a8a6426f50c524471`. The predecessor already argues
completeness. The contribution here is an explicit stabilizer proof, a separate
finite group-action oracle, and checks against the exact retained source.
No defect was found in this pruning step. This is not a proof of the whole
uniqueness search or of the multiplication theorem.

## 1. Domain and action

Work over F3. Conflict means distinct ports whose binary labels have dot
product one; the diagonal is not a prescribed zero. The eight clique indices are
`T = [1,5,18,20,80,85,100,103]`. The clique decoding rows restrict to the
identity on T. Write their other entries as X[t,m]. A non-clique decoding row
has coefficients a[j,t] supported in its four-element block T_j, and is the
linear combination of the clique rows with these coefficients. Its diagonal
equation is 1, so its coefficient vector is nonzero. Zeros in that vector are
allowed throughout this audit.

For independent signs d_l in {1,-1} at all 104 coordinates, let D be diagonal.
The action on decoding rows is w'_l = d_l^(-1) w_l D. It preserves the
diagonal ones and every prescribed zero, and acts as

    a'[j,t] = d_j^(-1) a[j,t] d_t,
    X'[t,m] = d_t^(-1) X[t,m] d_m.

The clique identity stays the identity. Each product in the equation at (j,m)
transforms by d_j^(-1)d_m. The right hand side is zero when m conflicts with j,
and is one when m=j, where the multiplier is one. Consequently the full
equation system is covariant. This is an algebraic identity, not an inference
from sampled values or the certificate's reported solution.

## 2. Exact stabilizer of a coefficient history

Fix any finite history of chosen nonzero coefficient rows at **distinct
non-clique ports**, as in a search that assigns each remaining port once.
Form the hypergraph
on T with one edge supp(a_j) for each earlier row, and let P be its connected
component partition. We stabilize the **literal coefficient history**, allowing
the unknown X entries to transform; we do not claim each partial X assignment
is fixed.

For a previously chosen row j, a'[j,t]=a[j,t] at all its nonzero coordinates
holds if and only if d_t=d_j throughout its support. This follows by cancelling
the nonzero a[j,t]. Therefore d_t must be constant on each hyperedge, hence on
each component of P. Conversely, any independent choice of one sign per
component extends to a stabilizing action: assign an earlier port j the common
sign of its support. A one-element support imposes no relation between distinct
pivots. Unassigned non-clique coordinate signs remain free.

Distinct port indices matter: if one tried to fix two different rows at the
same port, with disjoint singleton supports {t1} and {t2}, their one shared d_j
would force d_t1=d_t2 even though those two hyperedges do not connect. That is
outside the one-row-per-port model and is not allowed by this lemma.

Thus P describes precisely the allowable pivot signs for this diagonal action.
No assumption that all four coefficients are nonzero is justified or needed.
After fixing a new row with support S, the new stabilizer is obtained by joining
exactly the components of P that meet S. It is graph connectivity after adding
the hyperedge S. This proves the update performed by `merged`, including zero
coefficients and supports meeting only one old component.

## 3. One representative in every residual orbit

Consider a nonzero candidate a on a four-element block B. Let S be its support,
k=|S| and r the number of old components meeting S. Component signs can flip
the entries of each of those r components independently. The free sign d_j
adds a global flip, which is already the simultaneous flip of all active
components. Thus each raw coefficient orbit has exactly 2^r elements: no flip
of an active component fixes a nonzero coefficient in F3.

In each active component, make its first nonzero entry (in the inherited order
on B) equal to 1. There is exactly one such representative. Relative signs
inside a component are invariant and must be retained. These representatives
are also the lexicographic minima of the raw orbits, using 0<1<2. There are
2^(k-r) orbits for a fixed support, and the total number is

    N(P|B) = sum over nonempty S subset B of 2^(|S| - number of P-components meeting S).

The source's OPT list first fixes the first nonzero entry globally to 1.
Its `canonical` then checks the first nonzero entry in each *additional*
component. Together these implement precisely the representative rule above.
It would be wrong to require every nonzero entry to be 1 once old components
have joined; it would retain duplicate representatives to check only the global
first entry when components are still separate.

By section 2, the signs used for this normalization can be extended to all
earlier non-clique ports while preserving every earlier coefficient choice.
By section 1, the same transformation carries a feasible X completion to a
feasible completion. Thus every feasible candidate has a feasible canonical
representative at the current node. The update in section 2 makes the statement
applicable at the next node. Induction proves the pruning implication for any
finite history of distinct assigned ports and any next-port order, including
an adaptive order.

This implication is conditional on correct modeling of decoding constraints,
exact consistency decisions, and complete traversal of the retained options.
The audit does not prove those other parts of the search. Local orbit uniqueness
also does not establish that the full search has one leaf.

## 4. Independent finite checks and precise coverage

The oracle constructs raw orbits by breadth-first traversal under individual
component flips. It does not call or translate the source's `canonical` rule.
There are 15 induced partitions on a four-element block. For each one, all 80
nonzero ternary vectors are included, orbit sizes and the formula above agree,
and the source-retained set equals the set of independently obtained minima.

The source comparison covers all 4,140 partitions of eight pivots and all
70 ordered-by-T four-subsets: 289,800 states and 11,592,000 normalized option
checks. This includes all 14 actual P104 blocks, as well as states that may be
unreachable or inconsistent in the original search. It makes no claim that
every tested state is a reachable search node.

For merging, a graph-connectivity oracle computes 670,680 distinct
(partition, nonempty support of size at most four) results. Every one of the
11,592,000 source option updates is compared with those results, including all
normalized sign patterns and all positions of zeros. For each eight-point
partition, a signed spanning-tree history realizes it abstractly; all 256 pivot
sign assignments are checked against its coefficient equations. This gives
1,059,840 finite stabilizer checks. The all-history assertion follows from the
written proof, not from enumeration of these representative histories.

Separately, the audit transforms the source's actual encoded linear equations
for every one of its 96 non-clique ports, all 40 normalized coefficient options,
and each of eight pivot-sign generators: 30,720 cases. The transformed option
is normalized, including the resulting sign on column j. It compares complete
multisets of linear rows, including the nonzero right hand side. Gaussian
elimination and the search certificate are never executed. These checks audit
covariance of the equations as encoded, not completeness of the encoding.

## 5. Counterfactual controls

1. If all entries are forced to 1 inside a connected component, the orbit
   {(1,2,0,0),(2,1,0,0)} is lost. The oracle rejects this stronger prune.
2. With singleton components, (1,1,0,0) and (1,2,0,0) lie in one orbit but both
   survive global-first-entry normalization. The oracle rejects this weaker
   rule as a transversal; the issue is duplicate coverage, not lost solutions.
3. Omitting the merge after choosing support {0,1} allows a relative sign flip
   taking the old row (1,2) to (1,1), which is not the old row or its negative.
   The connectivity check rejects the state. Merging all untouched components
   is also rejected as an incorrect stabilizer; this control alone does not
   show an unsound exclusion.
4. Omitting the induced column-j sign changes a diagonal equation c*x=1 into
   2=1. This is detected both in a two-scalar witness and in the actual source
   equation transformation checks.

The package reports five controls, counting the two different merge faults
separately. These controls demonstrate that the checker distinguishes the
specific failure modes; they are not claims that PR6166 contains those faults.

## 6. Dependency boundary

The exact subject source and original proof are retained byte for byte in
`inputs/`, with commit, original Git blob, SHA256 and credit in UPSTREAM.json.
The selected PR6030 word supplies only its 104 live initial one-dimensional
frames, not a newly audited circuit. SOURCES.json pins that input at the base.
The oracle and proof are newly written; the source methods and encoded equations
are the objects being tested, not independent evidence for themselves.

Unreviewed here: the finite search's equation-model completeness, elimination,
DFS token coverage, the unique-code assertion, weight distribution, rational
reduction, delivery decomposition, frame capacity and cost corollary. No Lean
kernel proof, full selected replay, supplier admission or new kappa is claimed.
The five selected framework assumptions remain unchanged. Credit Matarener for
PR6166, DreamingOfClouds for PR6030/5907, Ali Romman for the P104 word/checker
lineage, and Brett Halligan (@burntout76) for the distinct PR1212 rigidity work.

Prepared by Jerry Chen (@CubeJerry) with substantial OpenAI Codex assistance in
reasoning, implementation, verification and writing. Apache-2.0.
