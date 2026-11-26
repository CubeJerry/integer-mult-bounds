# A characterization of fixed endpoint preparations with triangular tails

Status: **proved local characterization and constructive reuse compiler; independent review requested**. This is a different physical organization of the existing endpoint mechanism. It gives a precise condition for sharing preparations between rectangles, and a falsifier for one universal preparation. It does not construct a better compatible cover or prove RV-I.

Source: OpenAI math `3344da59991ed94f9ba711217b29c1d760badfa6`, tape `interchange.tex`, “Preparing one layout for all queries at an endpoint” and the following rectangle/low-rank delivery. Use the retained rational Gram geometry

`<x_v,x_w>=<y_v,y_w>=1-k(v,w)/d`,
`<x_v,y_w>=<y_v,x_w>=k(v,w)/d`.

The address algebra is rational; the scalar data may have characteristic two. All distinguished and reserved fields remain occupied by independent data.

## 1. The fixed-preparation strategy

Fix any finite family of source-compatible directed rectangles and partition that family into subfamilies. Each subfamily has its own copies of all oriented endpoint vertices S_v and T_v; the same label may therefore receive a separate prepared array in several subfamilies. In each subfamily make an incidence graph with one vertex for each rectangle and its oriented endpoint copies, joining a rectangle to all its endpoints. Split the subfamily into the connected components of this graph. Those components are the reuse groups. Thus a label may belong to many groups, and rho below counts its group copies rather than components of one unsplit global graph.

At each source vertex S_v, permit one arbitrary invertible rational change of the early and late reserved fields. At T_v permit a separate such change. Each is fixed throughout its reuse group and is independent of query j. It does not mix a distinguished query field into the reserved fields. Each rectangle may choose its own complete common address basis. After preparation, require its remaining source maps and inverse destination maps to be lower triangular in the physical field order, with only shifts controlled by earlier fields, as in the source endpoint proof.

Thus the model allows arbitrary, label-dependent and orientation-dependent reserve preparations, different common bases for different rectangles, and unrestricted linear triangular tails. It is more general than choosing one universal coordinate basis for all source variation spaces. It is less general than a new executor that mixes query fields during preparation, uses nontriangular middle maps, or shares transformations algebraically without a fixed prepared endpoint array.

For a reuse component let I be its union of source labels and K its union of destination labels. Call it **Gram-compatible** when

`k(v,v')=0 for v,v' in I`,
`k(w,w')=0 for w,w' in K`,
`k(v,w)=d for v in I,w in K`.                         (ER1)

The geometric superrectangle I x K need not be a subset of the scalar P* support. It will be used only to choose a common layout; the original scalar rectangle transfers remain unchanged.

## 2. A necessary suffix flag

Fix one query j. In the common address space extend the source rational space D by the late spare fields and all inactive query fields, treating those extra coordinates as independent spectator directions. Pair x_v and y_v with only the D component.

At S_v the distinguished columns are x_v at H_j and y_v at N_j. The reserved columns lie in

`W_v=<x_v,y_v>^perp direct-sum (late spare space)`.

A preparation on reserved fields does not change either distinguished column and keeps its reserved columns inside W_v. Consider the suffix of physical positions strictly after H_j. Its image under the prepared source basis is a subspace F(S_v). It contains y_v, because N_j follows H_j, and is annihilated by pairing with x_v. Other query coordinates in this suffix are spectators and have zero pairing. Thus

`y_v in F(S_v) subset x_v^perp`.                      (ER2)

At T_w the distinguished columns are reversed. The corresponding suffix satisfies

`x_w in F(T_w) subset y_w^perp`.                      (ER3)

An invertible lower-triangular coordinate matrix preserves every suffix subspace: its columns after any cut span precisely the same suffix. Therefore all prepared endpoints of one rectangle have the same suffix subspace as that rectangle's common basis. A fixed prepared endpoint shared by two rectangles identifies their suffixes. Connectivity consequently forces one common F for every endpoint of a reuse component.

Applying ER2 to two sources gives `<x_v,y_v'>=0`, hence k(v,v')=0. Applying ER3 to two destinations gives k(w,w')=0. Applying ER2 to a destination vector x_w in F gives `<x_v,x_w>=0`, hence k(v,w)=d. Therefore ER1 is necessary.

This is a statement in the actual rational Gram quotient: self-pairings are one, and the displayed pairings distinguish all vectors used in the argument. It does not assume a larger formal independent vector for each label. The proof also allows nonlinear implementations of the tails whose net maps are the required linear triangular coordinate maps; it does not assign them a physical lower cost.

## 3. Sufficiency and an explicit local execution contract

**Theorem ER.** A reuse component admits the fixed-preparation strategy of Section 1 if and only if its endpoint unions satisfy ER1.

Necessity was proved above. For sufficiency orient every source as (x_v,y_v) and every destination as (y_w,x_w). ER1 says that every mutual oriented Gram block is I2. Apply the actual source endpoint construction to this entire oriented set: choose a reference pair, form its difference space E, choose a complement C, lift C to each endpoint orthogonal complement, and move E into late spare fields. It gives one reserve preparation per oriented endpoint, independent of j, with all remaining maps lower triangular to one common basis. Every original rectangle in the component can use this same basis. This proves sufficiency without demanding that E be coordinate in a previously chosen global basis.

The source proof prices a preparation and its inverse by O(D) recursive field-swap calls per prepared endpoint. In a finite grouping let rho bound the number of reuse components containing any label on either specified side. Let V0 be the original batch volume. Then all endpoint preparations and returns have normalized recursive volume

`O(D(1+rho))`,                                      (ER4)

and their retained endpoint and accumulator arrays occupy `O((1+rho)V0)` bits, apart from the inherited encoding/padding constants and compact polynomial descriptors. Ordinary copies, triangular maps, scalar accumulation and masks are charged by their full polynomial-parameter volume bound. All endpoint arrays are retained through the queries and reused across the component's rectangles; no per-query endpoint recomputation is hidden.

The same grouping also improves the low-rank conversion count. Process groups serially. For a fixed basis row i and query j, form one accumulator in the current group layout from precisely the original rectangle terms whose destination side contains i; add no term merely because i belongs to the geometric superrectangle. All these terms already have that common layout. Convert the one accumulator to the fixed low-rank layout, add it to the retained basis-row accumulator, and clear/reuse the temporary before the next i or group. The singleton remains separate. Thus at most 1+rho conversions are required per basis row and query. After the central rank matrix and A_j act, return symmetrically: for each basis column and group convert its intermediate vector once, distribute it only through the original rectangle terms and masks, accumulate in the prepared destination arrays, then clear the temporary. No array for every rectangle is retained. Consequently the entire shared-pencil call invoice is

`O(D(1+rho)(1+mr*/N))`.                              (ER5)

Prepared endpoint copies, temporary group accumulators and their ordinary scans use reused marked contiguous regions, with union of visited payload cells `O((1+rho)V0)` up to the inherited encoding/padding constants. Low-rank accumulators occupy their existing `O((mr*/N)V0)` additional visited volume and reuse their marked regions across stages. Compact descriptors and matrix buffers remain separately charged. This is a visited-region bound, not merely a live-data count. Coefficient/rectangle membership calculations are finite tables or compact algorithms with the declared fixed polynomial degree; the original families have polynomial-m descriptions and counts. If a proposed new grouping lacks such a uniform description, (ER5) alone does not supply its uniform tape compiler.

The component does not replace the original sum of rectangle matrices by the all-ones matrix on I x K. In particular it never introduces the extra scalar edges that may lie in the geometric superrectangle. All original row masks and weights are still evaluated, now in one shared address order. This distinction permits geometric enlargement for preparation without changing cancellation.

For a global application, individual child-volume bounds, metadata removal, compatibility and finite-repair/visited-region requirements remain those of the E002 suppliers. ER4–ER5 identify exactly what a good compatible grouping would improve; they do not assert that its rho is as small as the output-count target.

## 4. A triangle forbids one universal preparation

For any d>=2 and q>=3, take inner words u_a with their first d letters equal to a and all remaining letters zero, for a=0,1,2. Take outer labels v_a with their first d inner coordinates equal to u_a and every remaining coordinate equal to the all-zero word.

For a!=b the two labels differ in exactly d outer coordinates, with inner distance d in each. Thus they are actual far neighbors in the retained P* support and k(v_a,v_b)=d. Every directed pair belongs to one rectangle of any exact partition of that support.

The six directed far edges connect the six oriented vertices S_0,S_1,S_2,T_0,T_1,T_2 in the endpoint-incidence graph. One fixed reserve preparation at every label/orientation for the whole rectangle family would therefore force a common suffix F containing both x_(v0) and y_(v0), while ER2 says F is annihilated by x_(v0). This contradicts `<x_(v0),x_(v0)>=1`.

Hence a universal per-label preparation cannot make all retained rectangle tails triangular. Allowing a different common basis for each rectangle does not avoid the contradiction. This is a falsifier of the defined reuse strategy, not a lower bound on physical data movement or on other architectures.

## 5. A finite lower count in this reuse model

There is also a simple alphabet-sensitive consequence. For alpha in [q]^d, let v_alpha have d selected outer coordinates, with its i-th selected inner word equal to alpha_i on d fixed letter positions and zero elsewhere; other outer coordinates are all zero. Then

`k(v_alpha,v_beta)=number of coordinates i with alpha_i!=beta_i`.

A Gram-compatible source or destination union intersects this q^d-label grid in at most one label. For a fixed alpha, exactly (q-1)^d grid labels beta are far neighbors, so covering those transfers requires at least (q-1)^d distinct reuse components incident to its source occurrence. Thus any grouping of this specified kind has

`rho >= (q-1)^d`.                                   (ER6)

This does not reintroduce the canonical t^(d(d-1)) factor. It leaves room for a better grouping or a new compatible rectangle family. It also does not imply that each component must incur an independent expensive transform under a different executor: that positive charging is part of the fixed-preparation model, not a universal runtime premise.

## 6. Current discovery and limits

The useful positive result is that a compatible superrectangle supplies an explicit shared preparation even when the relevant variation spaces are not coordinate in one fixed basis. The useful obstruction is that arbitrary reuse is impossible: triangular tails propagate a concrete suffix flag, forcing the full Gram compatibility ER1. Finding a uniform compatible cover/grouping with substantially smaller rho is therefore a precise constructive problem.

The four-line source-variation obstruction and the present theorem address different attempted simplifications. This theorem permits bases chosen from the whole compatible component; it rejects the stronger claim that one such preparation can serve the entire far-pair graph. It leaves nontriangular batched maps, query-touching preparations, additional transforms, cancellations before preparation, changed kernels, and other representations open.

Credits: @CubeJerry; the pinned rational endpoint construction; E002's exact geometry and physical supplier work; the present suffix-flag characterization and reuse invoice; substantial ChatGPT multi-agent assistance. No full multiplier execution, formal refinement, improved global rate, runtime lower bound or literature-priority claim is made.
