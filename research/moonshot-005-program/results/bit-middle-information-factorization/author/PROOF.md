# Exact common-information and causal middle-stage criteria

## Saturated outgoing messages at one chart

Let F be finite. Data x range over F^n. Receiver i requires a linear target T_i x of rank r_i and receives exactly r_i field symbols from this chart. A physical slot a is visible to a fixed audience I_a. Its encoder can observe linear data with row space L_a in(F^n)*. There is one actual value per shared slot. Allow arbitrary deterministic encoders/decoders, including nonlinear ones.

Put V_i=row(T_i), Q_a=L_a intersect(intersection_(i in I_a) V_i), A_i=the r_i slots seen by i, and d=max_a |I_a|. Ignore slots with no intended receiver.

**Theorem1.** Every exact code necessarily satisfies

    dim(sum_(a in S) Q_a) >= |S|                         (H)

for every i and every subset S of A_i. Conversely, if(H) holds and |F|>d, a linear code on the same slots satisfies all receivers simultaneously. Over a smaller F the same conclusion holds over any finite extension E/F with |E|>d; extension costs remain charged.

### Necessity, including nonlinear messages

Receiver i's target has |F|^r_i possible values and its r_i messages have at most that many tuples. Correctness forces the tuple to fill the product alphabet and be a bijective function of T_i x. Each individual message is therefore a function of T_i x.

A function of a linear observation is invariant under translation by its kernel. A common function of several observations is invariant under the sum of their kernels, hence factors through the quotient whose row space is the intersection of their row spaces. Apply this to the available observation and every receiver target sharing slot a. Its message is a function of Q_a x, even if nonlinear.

Any subset S of receiver i's messages has its full product range, because the whole tuple is a bijection. It has |F|^|S| values, while it factors through a quotient of dimension dim(sum_(a in S)Q_a). This proves(H).

### Sufficiency and field size

The independent-representatives lemma states that spaces Q_1,...,Q_r admit independent vectors v_a in Q_a exactly when every sublist spans at least its length. An induction proof splits off a proper tight sublist and passes to the quotient. If no proper tight sublist exists, choose a nonzero vector in the final space and quotient by its line; all remaining inequalities persist.

For each receiver,(H) gives a basis of V_i, one vector per slot. Introduce independent coefficient variables for one vector v_a in each Q_a. The determinant D_i of i's vectors in a fixed V_i basis is a nonzero polynomial, witnessed by its individual representatives. The product of all D_i is nonzero.

A coefficient variable of v_a occurs only for receivers in I_a, and each determinant is linear in that vector. Its individual degree in the product is therefore at most |I_a|<=d. A nonzero polynomial with every individual degree less than |F| cannot vanish on all F^N, by induction from the univariate root bound. Thus |F|>d gives one assignment where every determinant is nonzero. Receivers invert their basis maps.

Ordered finite coefficient enumeration specifies a terminating selection; no efficient search bound or complete physical compiler is claimed.

## Native D stage and causality

D has sixteen outgoing plane flags K. A receiver i sees four, each containing rho symbols in total, so a saturated target has rank4rho. A native K contains at most three receiver lines. Thus d<=3: GF4, GF16 and GF32 already suffice for simultaneous D information decoding.

With all D data available, each flag's packet functions lie in intersection_(i in K) V_i. Separate per-receiver packet choices are not allowed. For the real two-wave interface, let E_D be the early input row space. Early slots use

    Q_(K,early)=E_D intersect intersection_(i in K)V_i;

late slots use intersection_(i in K)V_i when needed early information is retained by paid snapshots. Use the actual slot counts. The theorem applies directly because availability is already a premise.

Slots with the same space and the same receiver audience can be grouped into types with capacities c_t. Native types (K,phase) have this property. Equivalently use per-receiver type capacities when only spaces are grouped. It suffices to check dim(sum_(t in S)Q_t)>=sum_(t in S)c_t for every subset of the types seen by a receiver. These whole-type inequalities imply partial-slot inequalities, since their span is the same and the partial count is no larger. Necessity takes whole types.

This is the D information interface. Source realization, pure early/late public-owner invertibility and downstream K capacity remain separate.

## Exact two-wave compression at K

Let z range over F^N, with early available row space E. A receiver wants Tz, row space V, rank r. It receives at most e early symbols and l late symbols. Late processing can access all z, including paid retained early values.

**Theorem2.** An exact causal code exists if and only if

    r<=e+l,     r-dim(V intersect E)<=l.                 (C)

These conditions are necessary for arbitrary deterministic encoders and sufficient for linear ones over F. The first is the total alphabet bound. Holding early observations fixed leaves |F|^(r-dim(V intersect E)) target values, proving the late bound. For sufficiency emit max(0,r-l) independent coordinates of V intersect E early, extend them to a V basis, and emit the remaining at most l coordinates late. The early count is at most e. Unused abstract slots may carry constants; physical original baselines still require restoration.

## Explicit two-layer construction problem

Suppose a source has a surjective visible H-port boundary at receiver i, partitioned into independent variable groups x_D. Its unique decoder contributions are T_(i,D)x_D, each of saturated rank4rho. Choose simultaneous D packets satisfying Theorem1. The four packets at(i,D) form a bijective linear encoding of that demand. Let A_(i,D,K) be the unique contribution decoder for its packet to K.

Collect actual incoming packets at K into z_K and define

    P_(i,K)z_K=sum_D A_(i,D,K)m_(D,K).

For fixed i, each D's four packets are jointly surjective and different D groups are independent. Therefore the receiver-visible D-packet boundary is surjective too; its K contributions are unique. For this chosen linear D assignment, two-wave information delivery from K to F_i exists exactly when(C) holds for every P_(i,K), with the actual terminal counts and early observations.

A constructor must therefore choose common D packet vectors whose induced K contributions satisfy(C). The(H) tests alone do not guarantee this. Separate generic determinants or individual source-to-receiver mincuts do not solve the coupling of D choices through K ranks and timing.

For nonsaturated D targets, changed source boundaries, nonlinear upstream maps or extra informative returns, rederive the interface. No canonical containment or inexpensive return rank follows. Physical owner restoration, pure-wave invertibility, local ordinary costs, paid snapshots, global source gluing, recursive admission and strict supplier compatibility remain additional obligations.

## Verification and controls

`check.py` enumerates binary subspaces in dimension3 and compares the compression criterion with finite linear encoder choices, checks common-function kernel intersections, tests independent representatives, and provides a small-field constrained-list control repaired over F4. The finite checks support the written general proofs; they are not all-size proofs.

The field bound depends on actual packet fanout, not the whole receiver count. Ignoring shared-message intersection, early availability or K compression changes the interface and can turn a failed test into a false pass.

Credit @CubeJerry and retained source/atlas authors. Independent representatives and the finite-grid argument are classical and already used in the source compiler. S027 Worker B developed the saturated common-information reduction, fanout-bounded simultaneous assignment and explicit causal K bridge with substantial OpenAI assistance. No new complete kappa or foundational discharge is claimed.
