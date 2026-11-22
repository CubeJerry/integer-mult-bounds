# Independent proof review B: coupled D1509 repair

**Accepted within the stated frozen-ingress scope.** The positive construction repairs the literal readout of one vector while preserving the four existing receiver interfaces. The separate rank theorem excludes an injective common readout on the entire forced four-space for every linear D-only word with the ingress fixed. The coordinate-change corollary is valid and does not imply a message, route or MOVE lower bound.

Review date: 2026-11-22. This review does not alter the author package. It complements the independent physical reconstruction and compiler replay in [the independent package](../bit-d1509-coupled-repair-s032-independent/).

## 1. Exact statement and quantifiers

Work over \(F=\operatorname{GF}(64)\). For each of the eleven native donors, let
\[
 P_j:F^{96}\longrightarrow F^{35}
\]
be the frozen actual D ingress. Let \(K:F^4\hookrightarrow F^{96}\) be the same injective frame at every donor. Set
\[
 Q_j=P_jK,\qquad B=Q_{61},\qquad
 Z=[\,Q_j-Q_{61}\,]_{j\ne61}.
\]
The order of the contrast blocks is immaterial to the theorem.

A common linear D readout means **one** linear map
\[
 R:F^{35}\longrightarrow F^m
\]
for any output dimension \(m\), satisfying
\[
 RQ_j=RQ_{61}\quad\hbox{for every native donor }j.
\]
Thus the same parameter \(z\in F^4\) is compared at every donor. The desired response must also be injective as a function of \(z\).

This class contains all legal D-only linear coefficient changes on the fixed inputs. It also permits maps with no phase constraint, no invertibility requirement and no requirement to retain the four old readouts. Proving impossibility in this larger class therefore excludes every legal D-only candidate. A cache or intermediate variable computed linearly from the same inputs supplies no additional information and still yields such a final map.

The theorem keeps the ingress and the literal common parameterization of \(K\) fixed. A simultaneous common change of basis in \(K\) leaves the ranks unchanged. Donor-specific parameter changes or donor-specific output maps are different contracts and are not inferred impossible by this statement.

## 2. Why the certified ranks imply impossibility

The supplied matrices satisfy
\[
 \operatorname{rank}K=\operatorname{rank}B=4,\quad
 \operatorname{rank}Z=30,\quad
 NZ=0,\quad
 \operatorname{rank}N=5,\quad
 \operatorname{rank}(NB)=2.
\]
Here \(N\) is \(5\times35\). Its five independent rows span the full left annihilator of \(Z\), because the ambient dimension is 35.

Common donor readouts give \(RZ=0\). Every row of \(R\) is therefore in the row space of \(N\), so \(R=CN\) for some matrix \(C\), regardless of \(m\). Consequently
\[
 \operatorname{rank}(RB)
 =\operatorname{rank}(CNB)
 \leq \operatorname{rank}(NB)=2<4.
\]
No such response is injective on \(K\).

The number 5 alone would not prove this conclusion: an annihilator of dimension 5 could, in principle, transmit a rank-4 response. The decisive certificate is the induced rank 2 on \(B\). Likewise, the rank-4 individual ingress \(B\) does not imply rank-4 information common to all donors.

An equivalent basis-free calculation explains both ranks. Write
\[
 U=\operatorname{im}Z,\qquad V=F^{35}.
\]
The induced image of \(B\) in \(V/U\) has dimension
\[
 q=\dim(U+\operatorname{im}B)-\dim U
   =\operatorname{rank}[Z\ B]-\operatorname{rank}Z
   =32-30=2.
\]
Every common linear readout factors through \(V/U\). The rank-4 image of \(B\) meets \(U\) in dimension 2, so at least two dimensions of \(K\) vanish under every common readout. This is an exact obstruction, independent of any search budget.

### Arbitrary binary-linear D words are also excluded

The displayed matrix factorization uses \(F\)-linearity, but the conclusion extends to an arbitrary \(\operatorname{GF}(2)\)-linear map on the 210 input bits. Suppose
\[
 R_2:F^{35}\longrightarrow \operatorname{GF}(2)^m
\]
is only binary-linear and \(R_2Q_jz=R_2Bz\) for every \(j\) and **every** \(z\in F^4\).

Then \(R_2\) kills each additive image \(\operatorname{im}_F(Q_j-B)\), and hence their additive sum \(U=\operatorname{im}_F Z\). It factors through the additive quotient \(V/U\). The image of \(B\) in that quotient has binary dimension \(6q=12\), whereas \(F^4\) has binary dimension 24. Thus the induced binary-linear response cannot be injective either. This covers arbitrary linear binary ADD words on the same information; it does not silently require the new word to retain a GF64-linear instruction pattern.

The premise is equality on the whole four-space. Equality on the selected vector alone does not force annihilation of \(U\), and permits the positive construction.

For fixed identity repetitions, the same quotient dimensions are \(2k\) versus \(4k\) over \(F\), or \(12k\) versus \(24k\) over GF(2). Allowing arbitrary linear mixing of those fixed copies does not change the obstruction. Field extension of the same matrices also preserves the ranks. These statements do not cover redesigned ingress information.

## 3. The coordinate-change corollary is sharp in its stated metric

For matrices \(A,B\) with common row labels, define
\[
 q(A,B)=\operatorname{rank}[A\ B]-\operatorname{rank}A.
\]
Suppose old and new matrix pairs differ only at a set of \(k\) coordinate-row positions, with the same column parameterization.

Let \(\pi\) delete those rows. The projected pair is identical before and after the change; call its quotient dimension \(q_{\rm drop}\). With \(U=\operatorname{im}A\), \(W=U+\operatorname{im}B\), and \(E=\ker\pi\), the quotient map gives
\[
 q(A,B)-q_{\rm drop}
 =\dim(W\cap E)-\dim(U\cap E).
\]
Since \(U\subseteq W\) and \(\dim E=k\), this difference lies between 0 and \(k\). Both the old and the new value therefore belong to
\[
 [q_{\rm drop},q_{\rm drop}+k].
\]
In particular, the increase is at most \(k\). This verifies the author's delete-and-reinsert proof; there is no extra factor of two.

Here the old value is 2 and an injective common response on the same \(K\) needs value 4. At least two distinct actual D input coordinate positions must therefore change. The positions are the fixed 35 row labels, taking the union over all donor ingress functions. Changing one donor's row may change several contrast blocks, but still only that one coordinate row of the combined pair.

This is a necessary support condition. It neither proves that two positions suffice nor supplies a construction. One source or H edit can affect multiple positions. It counts neither source coefficients nor D output rows, calls, fields, routes or MOVEs. Changing \(K\), changing the common parameterization donor by donor, or changing the information/isolation contract requires a fresh argument.

## 4. Positive construction and remaining whole-fibre failure

The positive result and the obstruction are compatible. The saved phase-legal word changes exactly six output rows, has delta rank 6, retains early/late ranks 19 and 16, and gives the selected nonzero \(v\) the common response
\[
 (14,5,63,1,1,49,6,27)
\]
at all eleven donors. This is injective on the one-dimensional span of \(v\), which needs only rank 1.

The independent physical checker separately confirms all 44 retained whole fibres and oriented readouts, all 144 geometric section ranks, and the literal compiler binding. Thus retaining the four fibres is supported by actual off-D isolation and section checks, not merely by the final equalities on one vector.

The fifth receiver has two distinct unresolved issues:

* With source/H fixed, the selected vector has nonzero off-D leakage at every native donor except 61. A new D word cannot remove those unchanged off-D responses.
* The donor-0 and donor-61 whole fifth-fibre spaces each have dimension 8 and their join has dimension 14. They are not the same whole fibre. Equal D outputs of one leaking vector cannot establish that interface.

The rank theorem is an additional obstruction even if one temporarily ignores the off-D failure and asks only for an injective common D response on all of \(K\).

The new local D bill is consistent:
\[
 2(6672+4732)+114+4337=27259.
\]
The increment is 263 ADDs per base instance and 2104 over eight lanes. The inherited local source/H/D total is 453939712 ADDs. The independent compiler result records unchanged INIT and dirty CLEAR counts of 279648 each and 16 gap-six field exports. These are local replacement counts, with global inverse placement, canonical return and the complete supplier invoice still open. No complete supplier or new \(\kappa\) follows.

## 5. Evidence checked and limits of this review

I read the actual author proof and README and checked the theorem implications above. I also performed a fresh exact algebra replay from the published ingress and forced-frame data, using the independently written GF64 polynomial-reduction and first-pivot elimination routine from the earlier B partition review. I reconstructed \(Z\) and \(B\), checked the saved annihilator and response identities, and obtained:

| Matrix | GF64 rank | GF2 rank after explicit scalar expansion |
| --- | ---: | ---: |
| \(K\) | 4 | — |
| \(B\) | 4 | 24 |
| \(Z\) | 30 | 180 |
| \(N\) | 5 | — |
| \(NB\) | 2 | — |
| \([Z\ B]\) | 32 | 192 |

The binary expansion replaced each GF64 scalar by its \(6\times6\) multiplication matrix, using \(x^6+x+1\); binary elimination used independent integer bit rows. The response quotient is therefore also explicitly checked as \(192-180=12\). The replay returned PASS_FRESH_B_ALGEBRA_AND_BINARY_EXPANSION.

This algebra replay does not claim a second fresh reconstruction of the physical source/H ingress. That separate task is covered by the pinned independent package, whose checker imports no executable from the new author packages. Its recorded status is PASS_INDEPENDENT_BOUNDED_COUPLED_D_REPAIR and its negative controls reject the old word as an all-donor vector repair and a mutated retained output coefficient.

From the repository root, the independent physical replay is:

~~~sh
python3 -B research/moonshot-005-program/results/bit-d1509-coupled-repair-s032-independent/check.py --out /tmp/s032-coupled-independent
~~~

The following exact SHA256 pins identify the material reviewed. Paths are relative to the results directory.

| Material | SHA256 |
| --- | --- |
| bit-d1509-coupled-repair-s032/PROOF.md | 498ecd44667859a738ca59998812383d9432ac22757c027db01a3269ad32baa1 |
| bit-d1509-coupled-repair-s032/README.md | 4c3c6b71c7b0a07c1a6a44519a280cd0708926f58ecc1959988cb897276e0a47 |
| bit-d1509-coupled-repair-s032/DATA.json.gz | 3781678b97d8ce45d955669d2cd9b069ce7303ea9bab227a81147ad1ccd66aef |
| bit-d1509-coupled-repair-s032/FULL-COLLISION-CERTIFICATE.json.gz | b83f9e7cd587b5406cfc9cfbdd8db01828c488e1ad969a1f3e3f762f472c00ce |
| bit-d1509-coupled-repair-s032/FULL-COLLISION-GATE.json | 15d33c6c0d27fb1b3678c725cfd00579267c6dfcf7756b818abc8089b170db1a |
| bit-d1509-coupled-repair-s032-independent/check.py | cc50ed36e5bf43847ddfb5535e510f0c65ae03da1c040e076d7504e4bca2b6cf |
| bit-d1509-coupled-repair-s032-independent/output/RESULT.json | fc30ed726429baf693682fec936902da3093343cebccbd3a6a13fb6b36472f68 |
| bit-d1509-nonlinear-partition-gate-s032/independent-review-b.py | 0e1d46f96a0fafbf5196c73f997f57e65b186e6da99d93f0c81635ef87a48e46 |

No claim here excludes arbitrary nonlinear D functions, simultaneous changes of source/H/D information, changed fibres or isolation, or a complete supplier with another architecture. The useful next obligation is a changed ingress or forced-space construction preserving the retained interfaces, followed by fresh isolation, chronology and full cost checks.

Credit remains with the author construction and the independent physical/compiler review. This additional proof review and binary-linear extension were produced with substantial OpenAI assistance. Apache-2.0.
