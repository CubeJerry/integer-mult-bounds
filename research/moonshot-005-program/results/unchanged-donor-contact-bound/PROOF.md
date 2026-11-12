# Global direct-contact obstruction for unchanged donor routes

## Result and scope

Fix the 104 ports of `research/shared-wire-split-composition/data/final.json.gz`, compressed SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`. They are odd binary vectors of weight three or seven in W=F2^9. Donor j begins on L_j=<v_j> and ends at W; receiver i begins at zero and ends on F_i=v_i^perp. Consider one monotone nested-subspace trajectory per original donor and one per receiver. Permit arbitrary intermediate binary subspaces, retiming, and stationary caches of an unchanged donor at subspaces its trajectory visits.

A direct contact is a pair (i,j) for which the unchanged original donor value can be added to receiver i at a subspace visited by both trajectories. Rescaling or adding the same value repeatedly creates no additional distinct pair. No donor recoding, extra moving copy, interreceiver relay, receiver-written cache later used elsewhere, or extra coded carrier is included. Each receiver may retain its own accumulator and use all eight E8 packets at its final chart.

**Analytic theorem.** Such trajectories cover at most 2,786 distinct direct-contact pairs. In the source E8 endpoint interface every receiver requires all 48 geometric side pairs, totaling4,992. At least2,206 required pairs therefore lie outside this grammar. The theorem permits every binary intermediate subspace, not only source charts.

An independent exact integer rectangle certificate sharpens the contact bound to2,768, leaving2,224 pairs. Neither number is a paid-MOVE or coded-instruction lower bound: one aggregate can represent many missing pairs. The result supports the current reversible-encoding construction, which is outside this grammar. No new kappa is claimed.

## 1. Chart populations constrain direct contacts

At a common chart C of dimension d, donors have v_j in C and receiver normals have v_i in C^perp. Let a_C,b_C count their trajectories. There are at most a_C*b_C contacts at C. Summing may count a pair repeatedly and remains an upper bound.

Each monotone trajectory visits at most one chart of a given dimension. For each d, sum a_C<=104 and sum b_C<=104. Only dimensions1 through8 host contacts. The odd affine slice of a d-space has either zero or2^(d-1) points. Thus a_C<=2^(d-1), b_C<=2^(8-d), giving level bound104*min(2^(d-1),2^(8-d)). At levels1,2,3 and6,7,8 this is104,208,416 and416,208,104.

## 2. Quadratic geometry of the full120-port superset

Write b(x,y)=sum x_i*y_i, ell(x)=sum x_i, and q(x)=sum_(i<j)x_i*x_j=binom(weight(x),2) modulo2. Among odd vectors, q=1 holds exactly at weights3 and7. Therefore Omega={ell=1,q=1} has120 elements and contains the104 selected ports. The polar form is B(x,y)=b(x,y)+ell(x)*ell(y).

Let w=(1,...,1) and E=w^perp, the eight-dimensional even subspace. We have q(w)=0, B(w,x)=0, and q(w+x)=q(x). On E, B=b is nondegenerate alternating: its radical is E intersect<w>=0 because w is odd. Counting even weights gives136 zeros and120 ones of q. Hence

    sum_(e in E) (-1)^q(e)=16,
    sum_(e in E) (-1)^(q(e)+B(e,z))=16*(-1)^q(z).

The second identity follows by translating e by z.

## 3. Dimension-four inequality

Let dim C=4. If C or C^perp has no odd vector, its contact product is zero. Otherwise U=C intersect E has dimension3, w is not in C, and C=<w+h,U> for h in E outside U. Odd vectors of C correspond to h+U; odd vectors of C^perp correspond to {e in U^perp within E:B(e,h)=1}, a16-element affine set.

Set S_U=sum_(u in U)(-1)^q(u) and S_D=sum_(u in U)(-1)^q(h+u). The full donor population is D=(8-S_D)/2. Insert the character indicators for U^perp and B(e,h)=1 and use the Fourier identity. The receiver character sum is

    S_R=16/(2*|U|)*(S_U-S_D)=S_U-S_D.

Consequently R=|Omega intersect C^perp|=(16-S_U+S_D)/2=12-D-S_U/2.

The alternating form B on U has rank0 or2. At rank0, q|U is linear, so S_U is0 or8 and S_D is0,8,or-8. At rank2, summing over the one-dimensional radical shows both sums belong to {0,4,-4}. A nontrivial radical character gives zero; otherwise the two-dimensional symplectic sum is+2 or-2, multiplied by2. All15 allowed cases satisfy

    5*D*R <= 8*D+24*R.

Their positive pairs are coordinatewise dominated by (2,12),(4,10),(6,8),(8,4). Overgranting some jointly unrealizable cases only strengthens the bound. Any subsets0<=a<=D,0<=b<=R satisfy the same inequality: the bilinear expression5ab-8a-24b has a maximum at a rectangle corner and all corners are nonpositive.

Summing gives at most3328/5, hence665 integer contacts at level4. Orthogonal complementation swaps D,R and gives5ab<=24a+8b at level5, again665. The analytic total is

    104+208+416+665+665+416+208+104=2786.

This holds for every permitted path family. The discovery census of all8,283,458 binary subspaces is not a premise of this proof.

## 4. Decoder weights are forced; all4,992 pairs remain necessary

Let a_i in Z^8 be the source E8 row, a_i dot a_i=8, and packet k contain s_k=sum_j a_(j,k)*x_j. For each i, exactly55 other j have b(v_i,v_j)=1. They cannot contact receiver i under any monotone itinerary since L_j is not contained in F_i.

These55 root rows lie in a_i^perp and span it. The independent source verifier supplies a7-by-7 nonzero minor for every receiver, with determinant a signed power of2. Rank7 therefore holds over every coefficient field of characteristic different from2. Any linear combination of packets introducing no inaccessible columns must have weights lambda*a_i. The self donor is also inaccessible, because b(v_i,v_i)=1; its required coefficient1 forces lambda=1/8.

This argument includes arbitrary V-by-V linear maps on the packets at any positive coordinate volume V. Applying the same seven independent equations to each matrix entry forces the packet maps to equal a_(i,k)/8 times a common map; the self coefficient makes that map the identity.

Exactly48 remaining j have b(v_i,v_j)=0 and inner product a_i dot a_j=+4 or-4. Their forced packet coefficients are nonzero+1/2 or-1/2. Each requires cancellation by direct access in the restricted grammar. The source certificate verifies all104*48=4992 demands. The programme's characteristic-zero setting is included.

## 5. Exact finite integer sharpening

For dimension4, let P be the positive integer profiles below (2,12),(4,10),(6,8),(8,4). Let F(A,B) maximize the sum of products over any multiset of profiles using at most resources A,B. This overgrants every physical chart itinerary. The exhaustive finite recurrence is

    F(A,B)=max(0, max_(a,b in P; a<=A,b<=B)
                           [a*b+F(A-a,B-b)]).

Both resources decrease strictly. The independent checker evaluates every state through(104,104), checks a forward exact-resource recurrence, and obtains F(104,104)=656. An abstract witness is ten(6,8), five(8,4), and one(4,4), using104,104 resources and value656. No physical schedule is asserted. Level5 has the transposed same optimum. Replacing665 by656 twice gives2768.

The analytic2786 theorem is independent of this computation. The sharpening is exact finite verification of a fully specified relaxation, with the recurrence proof stating its implication for arbitrary paths.

## 6. Legitimate escape mechanisms and limits

Coded donor combinations, extra moving copies, interreceiver relays, receiver-written records exported elsewhere, or a different packet span are outside this theorem. They require actual-row, chart, ownership, precision and full recursive accounting.

If there are N unchanged donor trajectories but still104 receiver paths, the coarse level argument gives sum_(d=1)^8 min(N*2^(8-d),104*2^(d-1)). Its values at N=252 and253 are4988 and4995. Thus at least253 trajectories are necessary in this relaxed grammar. This does not mean149 extra paid MOVEs; creation, copying, path length and ranks must be charged separately.

No universal algorithmic lower bound or supplier impossibility is proved. All five foundational assumptions and both compatible uniform supplier obligations remain open. No new kappa.

## Provenance

Prepared for @CubeJerry with substantial OpenAI assistance, Apache-2.0. Root developed the all-chart population argument and discovery census. The bridge worker independently checked its signs and scope, closed the decoder loophole with explicit minors, and supplied the integer sharpening. Credit the existing programme E8 representation and all native source authors. Fresh reruns of a checker count as reproduction, not a second independent mathematical review.
