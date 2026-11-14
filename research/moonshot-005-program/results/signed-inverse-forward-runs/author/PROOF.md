# Signed fresh-stage chains and exact alternating Gaussian endpoints

**Proved structural classification and positive target interface.** For the actual R0 port geometry, a signed chain of r distinct fresh-stage G kernels has per-path Gaussian rank8m−r+2p, where p is its number of positive runs. An odd chain reaches the desired rank8m+1 only through the strict chronological pattern +,−,+,...,+. Those alternating endpoints have exact ordinary decoders: odd prefixes expose QD_tot through an ordinary output map, and even prefixes expose D_tot through an ordinary input map. This is an interface for a new chronological caller, not a caller or a complete supplier. No new κ.

## 1. Actual source and notation

The source pins, matrix R0 and exact ordinary M_s,O_s routes are the same as the separately verified fresh-inverse endpoint-rank package. For each stage s, define

R_s=M_s^-1 R0 M_s,
R'_s=O_s R0 O_s^-1,
G_s=R'_s Q.

Both R_s and R'_s are actual ordinary involutions. The physical normalization gives

D_s R_s D_s^-1=Q^-1 R'_s Q,

and R_s commutes with every other fresh D_t. Thus with D_tot=product_(s=1..m) D_s,

D_tot R_s D_tot^-1=Q^-1 R'_s Q.                 (1)

The source-specific signs, translations and canonical-frame adapters are retained in these exact operator identities. No assertion that Q commutes with R0 or R'_s is made. The only cancellation used below is a literal adjacent Q Q^-1.

For distinct stages s_1,...,s_r, and chronological signs σ_i∈{+1,−1}, consider

W=G_(s_r)^(σ_r) ... G_(s_1)^(σ_1).

Every scalar port path in W D_tot is a signed single-column Gaussian map tensor-lifted to width V, multiplied by actual R0 coefficients outside the tensor power. We classify these paths. Merely writing W does not establish a native caller that produces it while preserving all other original inputs.

## 2. Exact signed rank transition

Let F be the projection onto all8m fresh body axes. In the Gaussian-convolution factor of a path, track a symmetric idempotent kernel K and its current input-port eigenstate

K q_j=e q_j,   e∈{0,1}.

Initially K=F and e=0. An actual edge j→h in fresh stage s has q_h·q_j=0 and route permutation P=P_(s,h)P_(s,j). Before the new rank-one update, K'=P K P^T satisfies K'q_h=q_h, since P^Tq_h lies in the untouched fresh-s block.

For an inverse edge G_s^-1, the Gaussian update adds q_hq_h^T. It removes one unit eigenvector, drops the rank by1 and sets the new current-port state to e=0. This is the earlier fresh-inverse lemma.

For a forward edge G_s, move its right-hand C_(q_j) through P. Its update vector is

v=P q_j=P_(s,h)q_j,

which lies in the fresh-s block and is perpendicular to q_h. Also K'v=P Kq_j=e v. Adding vv^T therefore raises the rank by1 if e=0, and lowers it by1 if e=1. Because v is perpendicular to q_h, the updated kernel still satisfies K_new q_h=q_h: every forward edge sets e=1.

Both updates preserve the projection property. Their net rule is consequently:

- Inverse edge: rank−1, state0.
- Forward edge following state0: rank+1, state1.
- Forward edge following state1: rank−1, state1.

If p is the number of positive runs in the chronological sign word, exactly p steps have the +1 transition. All other r−p steps have the −1 transition. Hence every authentic path has

rank(K)=8m−r+2p.                              (2)

This holds for arbitrary distinct fresh stages and every authentic port path. No path-disjointness or no-cancellation assumption is used.

For odd r, the maximal possible p is(r+1)/2. Equality holds only for the strict chronological pattern +,−,+,...,+. Therefore that pattern is the unique signed-chain pattern with per-path rank8m+1. Every other odd pattern has rank at most8m−1. The path count is at most4^r, so the earlier row-support argument gives a2V asymptotic support deficit for those nonalternating odd patterns under fixed or sublinear ordinary branching. This conclusion is specific to the signed fresh G-chain family.

## 3. Full kernels for alternating prefixes

The stronger path statement is also exact. Let E_s be the fresh-s subspace. The permutation P_(s,j) maps E_s⊕<q_j> to the full nine-dimensional head, and P_(s,h) maps that head to E_s⊕<q_h>. Both fix the other fresh stages. Therefore

P(F+q_jq_j^T)P^T=F+q_hq_h^T.

Starting from K=F, a forward edge gives K_new=F+q_hq_h^T. Starting from K=F+q_jq_j^T, an inverse edge gives K_new=F. Thus every path of a strictly alternating prefix starting positive has exactly

K=F+q_hq_h^T for an odd prefix,
K=F for an even prefix.

These kernels are independent of all internal port choices. Exact phases still matter for the complete operator; they are handled by the following direct identities, rather than inferred from equal kernels.

## 4. Exact ordinary Gaussian target adapters

Relabel the selected distinct stages in their chronological order. For odd r and a strict positive-start alternating word,

W_r=G_r G_(r−1)^-1 ... G_1
    =(R'_r R'_(r−1) ... R'_1) Q.              (3)

For even r,

W_r=G_r^-1 G_(r−1) ... G_1
    =Q^-1(R'_r R'_(r−1) ... R'_1)Q.          (4)

These follow by substituting G_s=R'_s Q and cancelling adjacent Q Q^-1. They hold on arbitrary inputs and at every width, with every actual phase retained. They do not move Q through any R'_s.

For odd r, the actual ordinary output decoder

L_out=R'_1 R'_2 ... R'_r

therefore gives

L_out W_r D_tot=Q D_tot.                     (5)

For even r, applying(1) to the product gives

W_r D_tot=D_tot(R_r R_(r−1) ... R_1).

The actual ordinary input preencoding

L_in=R_1 R_2 ... R_r

therefore gives

W_r D_tot L_in=D_tot.                        (6)

Equations(5)–(6) are constructive target interfaces: an odd alternating coded endpoint is exactly a head-plus-all-bodies Gaussian job after an ordinary output map; an even alternating coded endpoint is exactly the all-bodies job after an ordinary input map. Every map is invertible, so arbitrary original inputs remain independent. If several endpoints occur in one caller, their complete original-input map and compatibility of the individual preencodings still require a joint proof.

The three-stage example is especially simple:

G_3 G_2^-1 G_1 D_tot
 =R'_3 R'_2 R'_1 Q D_tot.

No extra Gaussian normalizer or spectral decoder is needed for that endpoint. The missing step is a legitimate chronological caller that produces this alternating endpoint and all its other required outputs at an affordable complete cost. The all-positive three-half caller established elsewhere produces inverse G endpoints instead, so(5) does not retroactively admit that different word.

## 5. Literal ordinary realization and its invoice

The checker constructs an in-place dyadic recipe for the actual112-by112 R0 matrix by exact row elimination, reverses the elimination and independently replays the resulting recipe on112 arbitrary basis inputs. The emitted recipe contains exactly280 ADDs,58 SCALEs and56 SWAPs. Its scalar set is {−2,−1,−1/2,1/2,1,2}. There is no Gaussian child, temporary input, zero-owned field, erasure, hidden source read or new productive helper.

These are caller-level ordinary operations on the actual array registers. They are not an assertion that arbitrary scalar mixing is free at a native chart with an incompatible label. The surrounding actual monomial maps explicitly determine the requested bank operator:

R_s=M_s^-1 R0 M_s,
R'_s=O_s R0 O_s^-1.

A single use of either map therefore costs the literal R0 recipe and224 ordinary monomial leg applications across112 ports. The length-r decoder or preencoder costs280r ADDs,58r SCALEs,56r SWAPs and224r monomial legs. For r=3 these counts are840,174,168 and672 respectively. All operations must be included in the ordinary/compiler/precision account of any full caller. Their additional recursive Gaussian moment is zero, not their runtime.

The coefficients are dyadic and bounded by2 at each scalar operation. For fixed r and fixed native geometry, any intermediate norm growth from this explicit recipe is a finite constant independent of width. The signed route recipes lift with their actual V-dependent global phases. Existing uniform ordinary implementation, precision-tape and compiler obligations remain; they are not newly discharged by this algebraic target interface. In particular no BIT compatibility follows merely from a complex dyadic recipe.

## 6. Reproduction, controls and remaining obligation

Run python check.py and python -O check.py --out RESULT-OPTIMIZED.json. The checker reconstructs R0 from the actual source rows. It checks all448 one-stage paths for each sign, all1792 two-stage paths for each sign word and all7168 three-stage paths for each of the eight sign words. Every update verifies the current-port eigenstate, the exact signed rank formula and the projection property. The strictly alternating positive prefixes also match the full kernels F+q_hq_h^T or F. The nonalternating ++ kernel is not silently identified with F despite its equal rank.

The exact word check verifies the literal adjacent-Q normal forms through nine prefixes as finite controls; equations(3)–(4) prove the arbitrary fixed-length identities. The112-input in-place R0 recipe is included in RESULT.json and checked against the exact source matrix. Normal and optimized receipts agree byte for byte. These tests instantiate, rather than replace, the universal arguments.

The next central constructive obligation is precise: produce an actual chronological caller from the frozen forward, inverse, independent-half or mixed-slope sources whose complete arbitrary-input endpoint map consists of the alternating odd/even targets above, and account for every other original register, Gaussian query, body idle and ordinary adapter. The signed endpoint identities alone do not supply that chronology. The existing conditional moment surpluses remain conditional until that step is proved. No new complete supplier or κ is claimed.

Credit the root orchestrator for the signed-run transition and full-kernel extension, Worker B and Worker A for independently identifying the direct alternating endpoint cancellation, Worker A for the even-prefix target bridge, literal ordinary realization and exact all-path screen, and the retained physical-source authors for the actual geometry and route identities. Work is for @CubeJerry with OpenAI assistance. No new κ.
