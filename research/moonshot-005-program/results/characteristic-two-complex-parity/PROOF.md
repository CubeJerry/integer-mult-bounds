# Characteristic-two rank9V obstruction on the complex native support graph

Status: proved from the explicit nine-frame parity certificate; independent review pending. This is a fixed graph/interface theorem, not a BIT or multiplication impossibility. The actual BIT native is a distinct source and is not identified with this graph.

Let H be the96 hosted roots of the pinned complex native gzip SHA2562b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883. Prescribe a zero at (i,j) whenever their characteristic-zero E8 roots are orthogonal. For any characteristic-two field F and any V>=1, suppose K has V-by-V blocks, K_ii=I_V, and all prescribed zeros. No symmetry, positivity, commuting coefficients or scalar-tensor assumption is made.

**Theorem.** rank_F(K)>=9V. The same lower bound holds on the full104 source by principal restriction to H. In characteristic zero the same prescribed-zero graph has rank8V Gram fittings, as the independently proved minimum-rank theorem establishes. Thus this exact eight-field graph interface has a quantitative characteristic separation. No rank9V attainment in characteristic two is claimed here.

The certificate lists nine actual source8-frames. Every pair of distinct roots in each frame is orthogonal over Q; all roots are hosted source members. Across the nine frames every used root occurs an even number of times. There are34 used roots,32 with multiplicity2 and2 with multiplicity4, for72 total incidences. These are exact statements about the original source graph, not a reduction of the dyadic Gram coefficients modulo2.

Put r=rank(K) and choose an arbitrary rank factorization K=CR with C of size96V by r and R of size r by96V. Write C_i,R_i for the V-row and V-column blocks. For a frame f, stacking C_i and concatenating R_i gives C_f R_f=K_ff=I_(8V). Hence

    P_f=R_f C_f=sum_(i in f) R_i C_i

is an idempotent of rank8V. In particular r>=8V. Let Q_f=I_r-P_f; it is an idempotent of rank d=r-8V. In characteristic two, even source multiplicities and the odd number nine give

    sum_f P_f=0,
    sum_f Q_f=9I_r-0=I_r.

Rank subadditivity therefore implies

    r=rank(I_r)<=sum_f rank(Q_f)=9(r-8V),

so8r>=72V and r>=9V, proving the theorem. The argument applies at every volume without assuming r is a multiple of V.

More generally any odd q-frame parity certificate gives r>=8q/(q-1)V by the same proof. The explicit q9 source witness gives the exact integer coefficient9 in the present bound. An even collection would not yield the identity sum; the verifier removes one frame as a negative control. It also rejects a repeated root within a frame and a single incidence alteration.

Reproduce without Python -O:

    python3 -I -B verify.py --repo REPO --output OUT

CERTIFICATE.json records frames by immutable native role and by binary root normal, all multiplicities and source pin. The verifier checks all576 ordered frame Gram entries exactly over integers, including all72 diagonal norms and all504 offdiagonal zeros. The characteristic-two conclusion is the general factorization/idempotent proof above.

This establishes a limitation of porting the complex source's rank8 fitting graph unchanged to characteristic two. It says nothing against a higher-rank or changed-source characteristic-two design. In particular the distinct actual BIT native's contact relation and caller invoice require their own source proof. All physical, compiler, erasure, precision, analytic and strict-supplier obligations remain; no new complete kappa follows.

Credit: @CubeJerry programme and native authors; root's general odd-frame rank argument; worker B's exact source parity search/certificate and verification; OpenAI-assisted mathematical research. No earlier copy of this characteristic-two parity theorem was found in the programme markdown search; no broader novelty claim is made.
