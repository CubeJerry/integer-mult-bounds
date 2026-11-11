# Wave 4 quantitative rank closure: preimplementation checkpoint

UNVERIFIED proof outline; no executable implementation yet.
Base e54523517d0f03e58352e647c403a5af3e525a57. Track 54/76.
Source-port dependency bd63147b1a193f68b5713e5814ac3b2c743beff8.

## Approved pivot and exact predecessors

Width-only closure is already solved: #5071 finite bit bounds, #4638
plateau-product width divisor, #5962 multiplicative-rank refinement, and
#6612 homogeneous exact widths. These are premises, not new work here.
#4586 README explicitly leaves time to generate every smaller program open.
#5071 section 4 charges P^G class/profile records. The new target is exact
all-rank width, leaf and mixed-unit metadata without path/slot enumeration;
no native scalar word or physical semantics is generated.

Canonical blobs: FINITE-PRECOMPILATION 4badb40f0919c515823cb07e44c6470d4d6469ca;
#5071 PROOF 6702d6aba2ad4149f9efc8570012a66aae640c8c;
#4507 README c85304a601f858774f425d5f3869ac0a6f85ec29;
#4638 width README 7548fd2060e41cf5b58485126d14b4dec936406a;
#4586 growth README 006711acd611b65a65555d2ae21563bdc33951a3.
These and named overlap texts are in reference/. Bounded PR searches found
no same generation theorem; arbitrary diffs/unpublished work are not covered.

## Proposed recurrence

Fix target histogram (k,W_k), 2<=k_min<=k<=m=max k; paid histogram (r,P_r),
1<=r<=r_max<k_min. Multiplicities positive; d,q count distinct ranks;
W=sum W_k, P=sum P_r. Paid occurrences remain separate chronological cuts.
Let T_g(c), R_h(rho) count ordered target-role and paid-position words.
At n>=m let G=floor(log_kmin(floor(n/m))). For h+g=G, m*rho*c<=n, set
v=R_h(rho)*T_g(c). Add v to U_n, add W_k*v at true rank rho*c*k, and if
h<G subtract P_r*v at rank rho*c*r. Separation matches every nondeepest
paid job, so nonnegative differences are fresh-source counts S_s.
Deepest exit multiplicities are E_e=R_(G+1)(e); each original cut has t=1.

```
a_n = lcm({B_(n-s)/gcd(B_(n-s),S_s):s<n,S_s>0} union {B_e:E_e>0})
B_n = a_n*sum_s S_s
P_n = sum_(s<n) (a_n*S_s/B_(n-s))*P_(n-s)
      + sum_e E_e*(a_n/B_e)*P_e
O_n = a_n*U_n + sum_(s<n) (a_n*S_s/B_(n-s))*O_(n-s)
      + sum_e E_e*(a_n/B_e)*O_e
```

Base B_n=1,P_n=n,O_n=0 for 1<=n<m. s=n has no complement; no B_0 invoked.
E_e aggregates additive cost only, never a gcd denominator. O counts
expanded native-unit occurrences, not physical live fields or bank extent.

## Universal derivation to finish before coding

Pascal matching consumes each nondeepest paid demand because r<k_min.
All source ranks s exceed n/m: root degree G+1 exceeds the cap; a nonroot
fresh source has a missing parent above that cap. Thus n-s<(m-1)n/m.
Every exit has e<=r_max*n/m<=(m-1)n/m. All child ranks contract by
alpha=(m-1)/m, with alpha^m<1/2.

Normalize X_n=B_n+P_n+O_n by B_n. Put Ubar=(G+1)*max(W,P)^G,
F=1+(W+1)*Ubar+P^(G+1), D=m*bit_length(N). The recurrence gives
X_n/B_n<=F*max_child(X_q/B_q), with base ratio <=m. Therefore
X_n<=B_n*m*F^D for all n<=N, without positive rank surplus.
The cited plateau divisor bounds log2 B_n by an explicit beta; all exact
binary outputs then have <=beta+log2(m)+D*log2(F)+O(1) bits. Include rule
bits, product keys and temporary numerators in a common explicit cap Z.
No factorization or shared unevaluated expression DAG is proposed.

## Optimistic full budget

At maximum height G, target-product records M_T=binomial(G+d,d),
paid-product records M_R=binomial(G+q+1,q), rank-local product pairs
V=binomial(G+d+q-1,d+q-1), signed source contributions <=(d+q)V,
and exit records E=binomial(G+q,q-1). Sort and aggregate deterministically;
charge all zero-count candidates and all distinct recursive ranks.

K=O(d*M_T+q*M_R+N*((d+q+2)*V+E+G+1)). Intended indexed metadata
bit work O(K*Z^3), with schoolbook arithmetic and Euclidean gcd, is
N*polylog N for fixed rule. This is not polynomial in log N: N rows
are output. All widths, leaf counts and unit counts are evaluated integers.

A separate fixed-tape companion scans at most N library records per lookup,
scans/inserts through all local records, and charges arithmetic, copying,
rewinds and erasure. Intended conservative bound is
O(K*(N*Z+L_local^2+Z^3))=O(N^2*polylog N) for fixed rule, with explicit
L_local. Python random access is not that machine. All output and retained
backing are charged. Actual native-word size requires independent local
word/adapter production bounds and is not inferred from rank counts.

## Verification and stop

After the derivation is secure, compare all exact library rows against an
independent literal role-word/path oracle on bounded fixtures. Include
product collisions, repeated paid positions, s=n, equality boundaries,
gcd cancellation and an exit-denominator pooling mutant. Tape worker
reviews full cost and cuts. Stop after this one approved pivot if superseded
or unproved. No selected astronomical library or 1920-fold word is emitted;
no new kappa or foundational assumption discharge follows.
