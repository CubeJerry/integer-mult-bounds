# A coefficient-independent class-separation obstruction

## Theorem and exact scope

Fix the native geometry and the pinned five nine-port classes at every left plane H. Let F be a finite field and rho a positive integer. Each H-to-D and D-to-K flag carries rho field records in total across both phases. Every active donor has a common input decomposition X_j in the direct sum of W_0,...,W_4, each of dimension48rho. Its ordinary class-c source quotient has3rho linear coordinates from W_c only, and local plane processing is linear and class-preserving. Stripes may mix arbitrarily within each class.

A selected foreign receiver sees sixteen ordinary source planes per active donor and three ports per class at every such plane. Its required proper output is the sum of the independently varying active donors. No extra varying nonproper information is provided. Downstream processing may be arbitrary deterministic processing, including nonlinear maps and class mixing.

For a visible middle D and donor j in D let n_c(j,D) count its H contained in D for which the H-to-D port is in class c. Every such donor has four H, so sum_c n_c(j,D)=4. A necessary condition for an exact code is

    sum_c max_j n_c(j,D) <= 4.                         (1)

Equivalently, all active donors at D must have identical five-component count vectors. This excludes every source coefficient assignment in the specified fixed class representation. Changed classes, per-plane relabeling, extra information and a changed proper target B remain outside the theorem. This is not a return-bank rank bound.

## Proof

Fix donor j and class c and hold all other varying donors zero. Recovery of its48rho target coordinates from sixteen3rho source quotients forces their stack to be invertible. Every local three-port projection on that donor's quotient must also be invertible. A lost coordinate cannot be recovered at another H because those H correspond to distinct coordinates in the invertible stack.

The visible port tuples of different H are therefore jointly surjective independent variables. A shared H is still surjective: one active donor's invertible local map can vary that tuple freely. The target decoder on this boundary is unique and linear, because source and target are linear and the boundary is surjective. Nonlinear downstream processing must compute this same function.

At D, one donor j's four port blocks are distinct rho-coordinate blocks of its invertible visible source basis. Their inverse decoder columns are independent. The class-c part R_(j,D,c) has dimension rho*n_c(j,D) inside W_c. The full D contribution image R_D contains every such part, with common columns at shared H. Direct-sum output classes imply

    dim R_D >= rho * sum_c max_j n_c(j,D).             (2)

There are exactly four actual outgoing K flags from D that can reach the receiver. Their total alphabet has size |F|^(4rho). After all other independent boundary values are fixed, the target takes |F|^(dim R_D) values as D varies. Thus dim R_D<=4rho, proving(1). Caches, recoding and cross-class/nonlinear downstream maps cannot enlarge the counted transcript. An early Hub closure requires a new informative descent to return; that channel is excluded by the premise.

Every donor count vector sums to four. The sum of coordinatewise maxima is four exactly when all those vectors agree, proving the equivalent statement.

## Exact native witness

For donors29 and36 at D81 and receiver10 the count vectors are respectively

    (0,2,0,2,0), (0,2,0,0,2).

Their coordinatewise-max sum is6. Every exact class-separated source therefore requires at least6rho output dimensions there, exceeding capacity4rho. The old frozen triangle coefficient witness requires7rho; the present weaker6rho bound applies to every coefficient choice in the stated representation.

For triangle donors29,36,77 and receivers10,33,80,95,151 of156 multi-donor receiver/D cuts fail(1), including all39 at receiver10. For all111 roles, retaining each receiver's tight foreign donors,34,425 of34,965 relevant receiver/D comparisons fail, with maximum normalized lower bound11. These finite exact incidence claims support the all-rho theorem and do not prove failure of other representations.

## Controls and open next questions

A common global permutation of class labels preserves(1). Independent per-plane relabeling changes its premise. Earlier unsuccessful relabeling searches are not impossibility evidence.

Matching count vectors are not sufficient: in two four-dimensional classes, spans of(e1,e2,e5,e6) and(e1,e3,e5,e7) both have profile(2,2), but their union has dimension6. A construction must align full donor lift spans and satisfy subsequent K/terminal and causal compatibility.

Run `python3 check.py --repo REPOSITORY --out OUTPUT`. The checker uses only authenticated native geometry and port partitions, with no source/decoder author code. It checks containment, tightness, the four-K capacity, profiles, census and controls.

Next: construct a compatible class relabeling, or mix source coordinates across classes; then solve simultaneous middle/terminal factorization. Low-return-rank robustness needs a separate defect-to-return bridge and is not inferred here.

Credit @CubeJerry and retained native/atlas authors; S026 Worker A for partitions and triangle source; S026 Worker B for frozen triangle cuts. S027 Worker B developed this coefficient-independent strengthening with substantial OpenAI assistance. No new kappa, foundational discharge, human review or formal-kernel claim.
