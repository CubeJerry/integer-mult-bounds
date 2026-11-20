# Minimum stationary storage for all formal D cuts

A single GF(64) map at each of the 3,150 native D charts preserves the rank of all 388,200 specified donor/receiver cuts at once. The word uses the smallest possible stationary early-to-late message at each chart in the formal independent-input model. The conclusion concerns physical D words. A specified endpoint also imposes shared decoder equations.

## Physical boundary

Work over F = GF(2)[z]/(z^6+z+1). At a D chart there are m original early X owners and n original late Y owners, including the actual early closures and late births. The incoming and outgoing indices within each phase are the same set of physical owners, sorted by native owner ID. No new MOVE is introduced. Each donor j in D has a formal set of eight input coordinates on its four incident H flags. Each receiver i in the perpendicular D has eight output coordinates on its four incident K flags. Let e_j and t_i count early coordinates in these two sets. Enumeration on the authenticated 106,560 routes gives e_j at least t_i for every such pair.

Hold all other inputs fixed, and vary the e_j early coordinates independently. The receiver must distinguish all of them, using its t_i early outputs and the only surviving early-to-late message. If that message has r field symbols, cardinality gives r at least e_j minus t_i. This argument allows nonlinear local processing. With s independent body copies the bound scales by s. The minimum at D is therefore at least r_D = max over j,i of (e_j−t_i). Correlated proper inputs or a changed interface need a fresh lower-bound argument.

## One map attaining the maximum for every pair

Use the Cauchy entries C(a,b)=1/(a+(32+b)), with integer labels denoting polynomial basis elements of F. For a chart with r=r_D, use the top m rows of an (m+r)-by-m Cauchy matrix as its early map A, and the additional r rows as V. Use the first n columns of an n-by-(n+r) Cauchy matrix as its late map C, and the last r columns as U. The row and column node sets are disjoint. Both pure maps are invertible.

For early and late inputs x,y, capture Vx into r stationary fields before early departure. Apply A to the early owners. Apply C to the late owners and add U diag(w) Vx on their actual chart. The vectors w are fixed per chart. Their entries are nonzero. The receipt provides all 3,150 choices. The local map is a bijection on the entire physical tuple, including arbitrary original Y baselines.

For a pair with d=e_j−t_i, expand the determinant of its eight-by-eight restriction through the r cache lanes. Only subsets S of size d can contribute. In characteristic two the term for S is the product of w_s over S, times a square minor of [A;V_S] on the early inputs, times a square minor of [C,U_S] on the late outputs. This follows by block expansion or Cauchy–Binet on the two phase factors. The signs vanish. Every individual Cauchy minor is nonzero. At d=0 and d=r a single term suffices. The other determinants can have cancellations. The selector sets w_0=1 for r>0 (homogeneity) and uses exactly evaluated field arithmetic to find weights making all the remaining polynomials nonzero. The largest search used 65 weight tuples. No inference about an infinite sequence depends on this search. The fixed finite list supplies the same local witness at every replication.

The minimum cache sizes zero through four occur at 386, 1,138, 1,136, 428 and 62 charts. Their sum is 4,942 field symbols per bank-480 body. This sum counts separate allocations. Actual simultaneous liveness belongs to a complete schedule.

## Binary bill and use

Each field is six binary native copies. Compile a pure block by Gaussian elimination, charging a swap as three XORs and reversing the resulting list for forward application. Charge both the forward and pure inverse words. Capture and delivery charge every nonzero entry in the actual scalar multiplication matrices. No diagonal rescaling, coefficient product, cache or owner change is free. At bank 3,840 (eight bodies) the price is 545,966,328 whole-record ADDs, 237,216 INITs and 237,216 dirty CLEARs. The surrounding atlas still pays its movement and must schedule the pure inverses at Hub/Ground. The inverse reserve normalizes the two pure phase maps. It does not reverse the desired early contribution to the late output.

For fixed i,j, these D maps transfer full rank across the sixty common D charts if their corresponding H boundary already distinguishes the original input. The precondition and subsequent routing at K and F are distinct. No exact low-return endpoint, strict supplier, new multiplication exponent or discharge of a foundational assumption follows here.

The separate reviewer recomputed every restriction by ordinary field elimination, with a differently implemented multiplication table. Its mutations distinguish storage rank from simultaneous correctness. Run the commands in the admission from the repository root.

Credit @CubeJerry and the asymmetric atlas, shared-middle and orthogonal-spread contributors. The local construction, computations and separate review used OpenAI assistance.
