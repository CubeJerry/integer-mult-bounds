# Current-row compensation and coordinate returns

Status: exact algebra and source-projected finite certificates. Literal whole-source words and independent source review are separate. No new complete kappa.

Source pins: native gzip `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`; cyclic gzip `ca493a06385fc55a1b1b2d30ddb638c7f5b021d19459aa6b0b8c85e3797510d2`, programme baseline `cbc210ca0eb82c74a021b4f1b744e2e07e07e00b`. Coefficients/ranks below are over characteristic zero, tensoring the identity at every positive whole-field volume.

## 1. Exact observation and compensation lemma

Let current Hub data be z=b+Rd for independent original b,d, with original target b-d and residual M=I+R. A real cocharted snapshot y=Bb+Dd, followed by a true zero observer initialized to -y and transported to the Hub, gives the exact pure observation (BR-D)d after adding Bz. All operands must actually be available; this identity grants no source access or route.

If the Hub genuinely acquires observation rows Nd and Zd, then arbitrary linear consumption can achieve minimum residual rank

    rank([M;N;Z])-rank([N;Z])
      =rank(M)-dim(row(M) intersect row([N;Z])).

The upper bound is attained by choosing a basis of the rowspace intersection and subtracting its observation representations from the corresponding target rows. The lower bound follows by quotienting all rows by the acquired observation space. This is valid for arbitrary block operators and every field: no scalar extension or invertible decoder-block hypothesis is used. It does not supply the physical observations, restore unrelated endpoints or discharge storage/erasure/ordinary/compiler costs.

In particular, compensation of rank r can improve rank credit by at most r beyond what N already supplies. If row(N) intersects row(M) trivially, at least g independent compensating coordinates are necessary for g rank credit. The actual cyclic C3 B-family nulls have that zero-intersection property. Acquiring all eight B-family nulls and their eight own-d returns supplies the K22 Gram space but costs 8*(6^(199/200)+1), which is dominated by returning all22 original K d coordinates.

## 2. Whole-column physical consumer

For a chosen original d_j still at its source-prescribed final facet F_j and all authentic b outputs cocharted at the Hub, a new owned zero field g can execute

    INIT g at F_j; g+=d_j; MOVE g F_j->Hub;
    z_i-=M_ij*g for every nonzero M_ij; CLEAR g at Hub.

The original d_j remains at F_j. The entire actual column is consumed, including off-principal entries. Repeating for J yields exactly M with columns J set to zero; it completes original endpoint i precisely when supp(M_i*) is contained in J. It uses |J| new rank1 MOVEs and |J| lifetimes, one reusable owned slot, and 4|J|+sum_j nnz(M[:,j]) scalar/lifecycle instructions. Source placement, owned-slot availability, phase maps and erasure contracts require their own literal-word audit.

The minimum possible residual rank from these returned coordinates is exactly

    rank(M[:,J^c])
      =rank(M)-dim(row(M) intersect F^J).

For field volume V every rank is multiplied by V, including under arbitrary Hub coordinate mixing. This proves why rank(K-G) alone is insufficient and supplies an actual current-row consumer representation outside the fixed scalar fitting-space theorem.

With unchanged cyclic H4 histogram the complete recursive moment is exactly its parent moment minus |J| per native: 31.556561901356545...-|J|. Thus31 rank1 returns fit strictly and32 do not, with every other caller item fixed. A changed m-copy caller requires its own substitution, not this ceiling.

## 3. Exact cyclic residual and endpoint/rank tradeoff

Ordering the22 closed ports K first gives

    M=[[G_KK,0],[L,I74]], rank(M)=82.

Let B=[5,56,65,69,77,96,100,103]. The actual source-projected replay verifies that every outside L row is supported on B and equals the E8 root's coordinates in this orthogonal B frame; all74 have exactly four entries +-1/2. Consequently, for J contained in the74 outside ports,

    rank(M[:,J^c])=82-|J|+rank(L_J).

The proof eliminates the untouched outside identity columns. The remaining additional L_J rows have zero intersection with the K Gram rowspace, since they are supported only on B whereas the S frame is a second full orthogonal basis.

Two exact31-return alternatives are:

* K22 plus nine outside returns: rank65 and31 individual original B endpoints complete (construction worker source word).
* B7=B without5 plus24 outside roots perpendicular to a5: rank58 and24 individual original B endpoints complete. Explicit J is in COORDINATE-RESULT.json. The construction worker emitted and checked its1880-input word independently of these support calculations.

All first-family duties, outside reverse duties, uniform suppliers and five foundations remain visible. The second alternative has a smaller residual rank; the first has more completed original endpoints. Neither is a complete native.

## 4. Exact finite coordinate-support certificates

`verify_coordinate.py` reconstructs all400 private columns of the pinned cyclic word and extracts a14-column rational kernel basis Z of actual M. It asserts that all hosted b rows depend only on their own b and the96 original d variables, and all d rows are unchanged; the actual96-by96 matrix and its canonical SHA256 are saved in COORDINATE-RESULT.json. A supported codeword on J exists iff the rows Z_J are dependent. Every one of the96 Z rows is nonzero and every projective pair is distinct, ruling out support1 or2. An exact dependent triple supplies the matching upper bound. Thus the first coordinate-return rank gain costs exactly3 within this coordinate-return interface. For example J=[1,4,105] has dependency coefficients [1,-1,-1]. Three returns yield rank81; this does not complete an individual original B endpoint.

Each11-root restricted Gram block has exact generalized support weights (5,8,10,11), by complete2048-subset enumeration. These are not the full96-row weights.

`verify_e6_d6_census.py` enumerates every pair among the120 full E8 root normals and deduplicates their exact perpendicular root sets. The1120 distinct E6/A2-perpendicular flats intersect the74 outside ports in at most26 points; the D6/A1^2-perpendicular flats have at most24. Including B gives an82-point E8 base; E6 intersections have at most29 and D6 at most27. These finite families are exact, but their enumeration alone is not a universal classification of arbitrary rank-six subsets. No unrestricted optimum is claimed from these witness-family censuses without a separately proved root-subsystem or matroid completeness argument.

## 5. Negative controls and open questions

Exact rank witnesses, all pair nonproportionality checks, wrong-coefficient source controls and unchanged columns distinguish original endpoints from algebraic rank.

Next questions: classify the full coordinate-return matroid or prove its low-rank flat bounds; find an earlier jointly encoded observation that improves total completion cost; and complete the actual first-family and reverse duties in one compatible word with the entire invoice. None of these follow from a numerical rank decrease.

## Reproduction

Run both checkers without Python -O:

    python3 -I -B verify_coordinate.py --repo REPO --output OUT
    python3 -I -B verify_e6_d6_census.py --repo REPO --output OUT

The checkers read only pinned source files and write only to explicit OUT. Exploratory null screens and withdrawn two-extension sketches are excluded from this accepted-package manifest.
