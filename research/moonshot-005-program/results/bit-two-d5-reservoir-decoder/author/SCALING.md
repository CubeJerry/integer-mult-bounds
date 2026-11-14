# A single paired reservoir direction changes only receiver72

Let k be any field of characteristic two, V>=1, C the native nine-dimensional canonical binary code extended to k, and d=1_D1+1_D2=a+b. Let S=C+kd, of dimension ten.

For every block fitting matrix H whose rows lie in S tensor k^V, there is a V-by-V matrix Z over k such that
H_i=K_i tensor I_V for every i !=72,
H_72=K_72 tensor I_V+(K_72+A_72) tensor Z,
where A_72=e_72+1_L is the acquired proper-supported row.

No commutativity among block coefficients is assumed. In particular, the acquired quotient direction d cannot change any second receiver's fitting row within this stated reservoir. This is a rowspace theorem, not a lower bound on every possible physical protocol.

## Proof

For receiver i, restrict codewords to its forbidden off-diagonal coordinates: j!=i with r_i dot r_j !=0. The exact rank certificate gives rank(C restricted)=8 for every i. The nonzero row K_i vanishes there, so the restriction kernel in C is precisely k K_i.

For all i!=72, adjoining d raises the restriction rank to nine. Since dim S=10, its restriction kernel still has dimension one and equals k K_i. Each scalar row of a block fitting matrix belongs to this kernel tensored with k^V. The own-coordinate identity condition therefore forces the whole block row to be K_i tensor I_V.

At i=72 the enlarged restriction rank stays eight. Its kernel has dimension two, with independent basis K_72,A_72. Both have own coefficient one. Thus a general fitting block row is K_72 tensor M+A_72 tensor N with M+N=I_V. Taking Z=N yields the expression above in characteristic two.

Every rank is certified over F_2. A binary matrix's nonzero minors remain nonzero in every characteristic-two extension, while its binary nullspace relations remain valid. The ranks and kernel bases therefore extend to all such fields. Applying them to all block entries is valid for arbitrary, possibly noncommuting coefficient matrices.

## Exact rank and support extension

The110 canonical rows other than72 still span C, as the exact checker verifies. They contribute rank9V. The exceptional row contributes precisely rank(Z) new row directions modulo C tensor k^V because Delta=K_72+A_72 is not in C. Consequently

rank(H)=9V+rank(Z).

The target A_72 has17 supported coordinates, all within the59-coordinate support of K_72. On those17 blocks H_72 is I_V; on the remaining42 canonical coordinates it is I_V+Z. Thus its whole-block support is canonical unless Z=I_V, when it is exactly A_72. Using the programme's established canonical proper-cover gate, the unsplit whole-block support statistic is chi222 for Z!=I_V and chi220 for Z=I_V.

The word "unsplit" is material: if a permitted physical model decomposes a projection Z into smaller independent width blocks, its identity and zero summands may be priced separately. The whole-block support assertion alone does not exclude fractional weighted savings under such splitting.

## Evidence and next obligation

scaling-check.js reconstructs all111 canonical rows from the authenticated root recovery and verifies global ranks9 and10, rank9 after deleting row72, all111 canonical restriction ranks8, the110 enlarged ranks9, the exceptional rank8, target containment and the exceptional kernel basis. SCALING.json records every restriction rank.

The author separately enumerated all512 canonical choices at each of111 receivers and found exactly one fitting with nonzero d coefficient: A_72. The proof uses the restriction ranks, not an extrapolation from enumeration. The orchestrator independently reproduced the111 ranks and supplied the exact block-rank extension, which Worker A reviewed algebraically.

Further proper-support improvements require at least one genuinely new quotient direction beyond d, or a construction outside this fixed history space. This does not assert one new direction per receiver in a larger code; several directions may combine to serve many receivers.

No complete supplier, no new kappa.
