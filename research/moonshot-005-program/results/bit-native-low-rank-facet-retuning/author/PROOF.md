# Four native endpoint gauges save two full return banks

For the actual all-Reed–Solomon terminal source/H/D/K/F word, the true labelled return fitting initially has rank 111b=426,240 GF(64) symbols. Leave every earlier source map, transport, stationary capture, K and proper terminal calculation fixed. Change only outputs at native roles **0, 1, 2, 3** by invertible linear gauges inside these genuine existing facets. The new fitting has exact rank **109b=418,560**. Thus it removes 7,680 field symbols, or 46,080 moved bits, from the required return dimension. The 6,470 foreign pair blocks retain full rank. All 111 native own-map targets and all independent ground inputs remain present.

## Native Schur reduction

Let A=I+B be the frozen genuine fitting for one native 96- or 384-field component, and let U be eight anchors, roles 0 through 7. Propagate columns from the other 103 original owners through the true chronological source/H/D/K/F word, and quotient the 111w-dimensional codomain by their image. In both sectors the resulting quotient has dimension 8w. Its coordinates consist of the free pivots in an exactly reduced native source matrix. Let Q be the map to the quotient, A_U the untouched anchor columns and E_U the pure owner-coordinate embeddings. Both Q E_U matrices are invertible. Thus the anchored square operator in ordinary owner coordinates is K=(Q E_U)^−1 Q A_U. Changing against the true owner identity on one anchor changes only the matching diagonal K block. Four untouched anchors 4 through 7 form an invertible principal submatrix. Eliminate them exactly to obtain a four-role matrix b=(b_ij).

Suppose W_i is the actual newly applied local proper-output gauge at one of the four final facets. The new fitting is I+diag(W_i)B. Multiplying its rows by block diagonal diag(W_i^−1) gives B+diag(W_i^−1). Its only change from the frozen A is thus on the true donor-owner diagonal submatrix. In a pair of originally independent replicas the effective off-diagonal entries are b_ij⊕b_ij. Replacing a local effective diagonal by Y_i means setting the physical W_i^−1=Y_i+(b_ii⊕b_ii)+I. Each tested W_i^−1 is invertible. Pairing replicas is an ordinary gate operation at the same physical facet. Every proper foreign input remains invertible after the gauge.

## A pair of replicas supplies an invariant graph

Use one-based positions 1,2,3,4 for the four original roles in the following equations. We seek a kernel in paired-replica 4-vectors of the form (u,v,P u+Q v,R u+S v), where u and v are independent d-vectors and d=2w. Temporarily suppress the direct doubles on the b entries. The first two off-diagonal equations force R=A+B P and S=C+D Q, where

    A=b24^−1 b21,  B=b24^−1 b23,  C=b14^−1 b12,  D=b14^−1 b13.

Set E=b31+b34 A, F=b34 B, G=b32+b34 C, H=b34 D. With Y3=Z, the third row is satisfied by P=(Z+F)^−1 E and Q=(Z+H)^−1 G. The fourth row must have the same Y4 upon construction using either independent input. It becomes equality of two linear fractional transformations of Z. In one replica write

    L = [[u,u F+b43],[v,v F+B]],     u=b41 E^−1, v=A E^−1,
    T = [[u',u' H+b43],[v',v' H+D]], u'=b42 G^−1, v'=C G^−1.

The action of a block matrix [[a,b],[c,d]] on a graph Z is (a Z+b)(c Z+d)^−1 wherever this chart is defined. For example the expression (b41+b43 P)(A+B P)^−1 is represented by L, by multiplying numerator and denominator on the right by E^−1(Z+F). The other fourth-row expression is represented by T. It suffices to find an invariant balanced graph for M=T^−1 L. Every matrix M commutes with each positive power N=M^p, so the graph of z↦Nz in two replicas is invariant for M⊕M. With each replica's former top/bottom variables grouped together, the graph has chart

    Z = [[I,0],[N11,N12]] · [[0,I],[N21,N22]]^−1.

For the native roles 0,1,2,3 and p=1 every denominator shown is invertible in both native components. Set Y1=b13 P+b14 R, Y2=b23 Q+b24 S, Y3=Z and Y4=(b41+b43 P)R^−1. Every displayed formula is over GF(64), hence addition is also subtraction. These explicit updates annihilate the full 2d-dimensional kernel. The off-diagonal 2d-square submatrix from the last two chosen donors to the first two chosen receivers is invertible after eliminating the unmodified anchors. This proves exact rank 2d for the four-role effective matrix. Including the other 107 roles gives a rank of 109d for this pair of replicas. Across four pairs each in both sectors this is 109b.

The verification step reconstructs all eight anchor equations directly from Q A_U and Q E_U, lifts the 2d candidate kernel coordinates through all four untreated anchors, checks all equations on all kernel columns, checks an unmodified full cross minor, and multiplies each W_i against W_i^−1. It also compiles each true W_i on two local copies at once. The four modified small charts cost 10,635,716 local binary ADDs over four pairs in a forward application, and the four large charts cost 169,882,032. The matching ground-side inverse doubles this to **361,035,496 incremental binary ADDs**. The gate words introduce no MOVE, INIT, CLEAR or extra stationary records. The full repaired return still has separate formation, movement, preload and retirement invoices. Its measured rank is far above the required 9b+128 boundary in the source conditional calculation.

## Full movement and ordinary bill

The rank-resolved physical MOVE counts are 12,818,880 of grade one, 10,386,720 of grade two, 552,960 of grade four and 2,511,360 of grade eight. After division by 23,040 lanes these are 4451/8, 7213/16, 24 and 109. The one-way rank is exact. A realized binary rank factorization may incur additional binary ADDs when forming and preloading its messages. For M=2,557,440 original bits on each side and C=2,511,360 return bits, cost the two dense products at 2MC≤12,845,305,036,800 ADDs and allocate/retire all C stationary return messages. No fixed original Y is lost, since the matching ground inverse is included.

The literal source, H, D, K and terminal stage receipts include 2,794,107,640 forward and reserved endpoint-inverse ADDs before the four new gauges. They charge 5,067,072 stationary INITs and the same number of dirty CLEARs. After the gauges and conservative arbitrary true return, the total for these stages plus return is at most 12,848,460,179,936 ADDs, with 7,578,432 INITs and dirty CLEARs each. The existing peak bound 7M+C is 20,413,440 records. These bounds account for this measured native word; the normalized recurrence uses the ordered 18-repetition caller and its own further transitions. Its productive-minus-paid rank sum at zero saving is 14562−13809m. In particular the candidate fails the target movement test even before the supplier and analytic outer contracts.

## Replay

Use the package-level `python -I -B verify.py --repo REPO --out FRESH`. The verifier reconstructs every finite gauge from two immutable four-role Schur matrices. Its independent block-multiplication implementation evaluates every corrected kernel column and uses exact field elimination on the unaltered cross minor. The separate heavy verification, enabled by `--heavy`, omits all four original donors, streams all 107 unmodified genuine source banks, and computes the unique Schur on exactly these four anchors. Its agreement with the initial eight-anchor route verifies Schur associativity in the full physical realization. Pass `--emit-gauges` to retain all matrices. The default replay requires Python, NumPy and a C compiler; the largest heavy state is about one gigabyte. Independent input pins are checked in the original source/H/D/K constructor.

Credit @CubeJerry and the native S/H/D/K/facet authors. OpenAI assistance was used.
