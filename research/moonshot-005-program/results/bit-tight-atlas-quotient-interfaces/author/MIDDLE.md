# Exact test for an active plane's common 45 physical outputs

**Proved for the H output layer.** Fix any separated native source satisfying the additive-quotient and receiver-alignment conclusions of SOURCE.md. Suppose its quotient spaces and lifts are linear over a finite field F_q. Over the native binary bank, F_q=F_2 always works. A rank inequality for every subset of the 15 visible ports is necessary even for nonlinear middle functions. It is also sufficient for simultaneous linear H encoders after extension to any F_{q^e} with q^e>12. This tests the actual 45 shared H-to-D slots jointly. It does not supply viable source subspaces or solve the remaining D-to-E6 and terminal transfers.

Let p≥1 be the F_q dimension of one physical port and s=15p the dimension of a full emitted H bundle. For each active H write Z_H for the direct sum of the emitted native quotient spaces G/K_{j,H}, one for each j on H. For i with H inside F_i, let T_i:Z_H→L_{i,H} be the sum of the inverse quotient maps for its donors, as in SOURCE.md. This is surjective of rank s. Let W_i be its s-dimensional row space in Z_H*. Each of the 45 actual D ports above H is received by every native i for which D lies in F_i if the receiver is granted its whole available cut. Define

    W_D = intersection of W_i over native i with D contained in F_i.

All 45 ports have at least one such receiver. For each fixed i seeing H, let P_i be its 15 actual D ports.

**Necessity.** With the 15 other bundle coordinates per donor fixed for this receiver, Z_H ranges freely. The function of its 15 observed H outputs must distinguish every different value of T_i. The codomain holds exactly q^s tuples and T_i takes exactly q^s values, so the tuple is a bijective relabelling of T_i. The H outputs depend only on Z_H and previously fixed source constants by the plane-local, monotone port hypothesis. Each individual D output is therefore a function of every T_i whose receiver sees D. It is invariant under translations in every ker T_i and hence under their sum. The dual of the resulting quotient of Z_H is exactly W_D. This holds for deterministic nonlinear choices at H and arbitrary downstream processing. The original kernel result also holds in finite abelian groups before converting to vector spaces.

For any subset J of P_i the J outputs take all q^{p|J|} possible values. This follows from the surjectivity of the full 15-tuple. Their values factor through the linear forms in the sum of W_D for D in J. The required inequalities are therefore

    dim(sum of W_D over D in J) >= p |J|     for every i and J ⊆ P_i.      (1)

In particular every single port needs p common independent linear forms. Positive dimension of each individual W_D does not suffice when their sums are deficient.

**Sufficiency at the H cut.** For fixed i repeat each W_D exactly p times, once for each component of its single p-dimensional output. By (1) the span of any sublist of these spaces has dimension at least the number of slots in that sublist. Indeed its support is a subset J of P_i and it has at most p|J| slots. The linear independent-representatives criterion now chooses one vector in each listed space, jointly independent. For completeness, if a nonempty proper subset of a list has span of dimension equal to its length, first choose its representatives by induction. Mod out by that span and apply the inequalities to unions with the tight subset for the remaining list. If every nonempty proper subset has one dimension of slack, fix one arbitrary nonzero vector from the last space and pass to its quotient. Each remaining sublist loses at most one dimension and still satisfies its inequality. The one-space case is immediate. These choices give one basis of W_i for this i.

To satisfy all i at once, give each of the p slots of each D a vector with formal independent coefficients in a fixed F_q basis of W_D. For each i form the determinant of its 15p selected rows in a fixed basis of W_i. The single-receiver result gives a specialization in F_q with nonzero determinant, so its polynomial is nonzero. Their product is nonzero because the polynomial ring is an integral domain. One coefficient variable for D occurs in only one row of each determinant, and only for receivers seeing D. Each native D has at most 12 receivers, as checked from literal normal incidence. The product has individual degree at most 12 in every variable, regardless of p. A nonzero polynomial of degrees less than a field's cardinality in every variable cannot vanish on the entire field grid, by induction using the univariate root bound. Thus over F_{q^e} with q^e>12 a common specialization works. Ports for distinct H have independent selectors. The receiver's visible 15p rows span W_i and reconstruct T_i by a linear map.

Field extension corresponds to e independent native blocks with coordinate mixing if the base source is binary linear. At most four-fold repetition suffices over F_2. This assertion keeps normalized true port capacity and native atlas incidence, but every actual local arithmetic operation, interchart transfer and caller condition still needs physical realization. Over an already sufficiently large base field no extra block repetition enters this interpolation argument.

The small controls in check.py include four scalar ports, one common two-dimensional target and all six two-port receivers. Every per-receiver instance admits an independent pair, yet no simultaneous choice over F_2 exists because it has only three nonzero directions. Four distinct projective rows over F_4 solve it. Replacing both available common spaces for one receiver by the same line passes the two singleton checks and violates (1) on their pair. The other control checks every pair of two- and four-element subsets of F_2^3 attaining equal minimal sumset size.

Reproduce the native census and controls with

    python check.py <S013-cloud/SOURCE-RECOVERY.json> <S022-global-ports/LAYOUT.json.gz>

The emitted certificate is deterministic. Its SHA-256 pins, 3108 clean-flag distribution, 3150 D visibility distribution and 45-port multiplicity checks distinguish this literal architecture from uncharged receiver-specific channels. No new κ.

Credit @CubeJerry, native and atlas source authors, the S022 gluing and physical-layout investigations, and substantial OpenAI assistance. S022 worker B developed this rank reduction alongside independent derivation by the lead researcher.
