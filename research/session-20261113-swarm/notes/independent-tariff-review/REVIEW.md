# Independent review of the selected large-width tariff family

**Outcome: APPROVE WITH QUALIFICATIONS.** Approve the admitted joint family
and the failure of the present serial-column implementation to meet the
selected monomial-record tariff on that family. Approve the stronger layer
comparison only with the explicitly stated unchanged-schedule premise below.
Do not treat this as a lower bound for other adapters, the retained framework,
or integer multiplication. No standalone PR or new graph is proposed.

This review is complementary to A's graph/body-write audit. I did not repeat
that audit. I take its separately checked executed lower bound as a premise:
the present serial CNOT performs at least fV payload writes on every legal
successful call, including zero payloads. This review checks source-domain
admissibility, normalization, recurrence and limitations independently.
Prepared with substantial OpenAI Codex assistance, Apache-2.0; no human or
formal-kernel acceptance is asserted. Earlier B packages were not changed.

## 1. Exact scope and source pins

All canonical sources below are at
e54523517d0f03e58352e647c403a5af3e525a57. SOURCES.json records the complete
paths, byte counts, SHA256 and Git blobs of15 independently read sources.
The principal ones are:

| Source | Git blob | Relevant statement |
|---|---|---|
|docs/research/pr-intake-evidence/pr7000-application/PROOF-REVIEW.md|3dd1af2285e597676725e85ad4f65e7ad326d695|§§2/5/6: full factors, linear width, separate record/child invoice; §3: current stock atom.|
|research/final4610-independent-admission/SPECIALIZATION.md|7ee84b30892f7354e1c36611f1a5e9b082dc6147|§3: fixed template before f varies, f<=e<=floor(b_in^epsilon), p=6b_in eventually.|
|research/kappa-rebuild/transfer-audit/OUTER-TRANSFER-AUDIT.md|e8b7ef8956ece5bd493cbf52113916e5dc288535|§5: current support-local replacement, product stock, deferred reserves and restored padding.|
|capped-phase-fusion/SUPPLIER-SUPPORT-AUDIT.md|72404c42d77d4267105e8528cecff3327dfdd38c|§§2–4/6/8: global complete calls, K=128G, finite guard, invocation-local stop, large groups.|
|capped-phase-fusion/TENSOR-COMPILER.md|19efb9cb1c5a738e57caadf2dd6f5611af1bc78a|Same data volume, full global H calls, no2^g expansion, paid scan/table work.|
|capped-phase-fusion/OUTER-AUDIT.md|974b8db67f4f556bddd55904f47ec145c629f1e6|V=Theta(n),p=Theta(log n), grouped Gaussian row and whole-global calls.|

The abbreviated capped-phase-fusion paths have prefix
research/kappa-observation-integration/release-work/current/package/vendor/pr1673/.
Their older numerical example parameters are not substituted for the current
point. Current parameters are bound by shared-wire-split-composition's
INDEPENDENT-SOURCES.json → full_verify.py → interval_gate.py: full_verify
passes the manifest's claim/tested values to the gate, whose lines101–105
construct the exact exponents and functional tests. This does not import its
older command-line defaults. The old OUTER-TRANSFER example stock exponent
0.003 is likewise replaced by the current application §3 exponent1/250.

Reviewed A checkpoint: README SHA256
c096bbeeb7d78f23ded1895b166f7ad70df6f7e2c46831071ec97bb9db2d24b2,
SOURCES SHA25690664ef8096bd5a42bf4c07c470adeb3329713cfd7ec8ac4c36173c3b86f5648,
PARAMETERS SHA256f527c99f8670bc1f42096eabdf103a2cb44c765d592be96d0423a5e3ec9407d0.

## 2. The family fits the actual source domain

Use delta=10^-14 to avoid confusing the margin with the group width. The
current exact point has epsilon=1-delta, group exponent beta=1-3delta,
eta=delta, a=kappa+4delta, tau=1-a, sigma=1-(kappa+5delta),
q=kappa+3delta. All are fixed rational constants before p varies.

The retained outer family has d=Theta(p^epsilon), original axis bitlength
ell=Theta(p/d)=Theta(p^(1-epsilon)), and groups of
t=Theta(p^beta) selected original axes. Since0<beta<epsilon<1, these
groups exist eventually. At the first deferred phase of such an invocation,
h=t and e=h-R(h)>=15h/16. The stop test uses this invocation's t, not always
the largest d. With fixed carrier N=2^H_C,
H_C=14174600000000000000, eventually t^eta>=2N; thus every nonleaf of this
growing group family satisfies

f=floor(e_node/N)>=e_node/(2N)>=t^eta/(2N).

At the first active root, f=Theta(t). Finite remainders below N alter these
comparisons only by fixed constants and add their separately retained O(V)
work. Native occurrences inside a fixed compiled template may have fixed
additional dilation factors; those do not change any p exponent. Since
e<=d=Theta(b_in^epsilon) and p=6b_in eventually, f<=p holds after one fixed
cutoff, also after any such fixed dilation.

The older K=floor(d^c) reservation is not a further current constraint.
It remains in the upstream prototype and old compact layout estimate, but
the retained support-local audit expressly changes that layout. It uses
G=4ceil(log2 p)+6 and K=128G, defers the reserved selected bits, and proves
the sufficient finite guard K>=G+4ceil(log2 p)+10. The compact-movement
proof uses its older K/log p→infinity condition to obtain precisely this
finite guard; it is not valid to say128G satisfies that stronger limit.
Neither the old power-width c restriction nor the old prototype's guard
condition epsilon*C1<1 with C1=20 is imposed on the current linear guard.

All remaining capacity and address checks are compatible eventually:

* Each original axis contains its K+O(log p) neighborhood because
  p^(1-epsilon)/log p→infinity.
* The entire selected-neighborhood and router support has
  O(t log^2 p)=o(p) bits. Even the generic h=d capacity case fits because
  d log^2 p=o(p). The reservoirs are concatenations of complete neighborhoods;
  no one axis must contain hG bits.
* The untouched log^2 p suffix can be chosen outside the support. The full
  address has Theta(p) bits and its ratio to the support times any fixed
  logarithmic factor diverges. The retained full-span fallback handles the
  bounded regime, not the eventual polynomial-width family.
* Product stock remains sublinear. For the current rho=1/250, stock at
  width O(h log^2 p) has an h^rho times fixed-polylog reserve, with the
  complex stock and nesting factors included. A fixed polylog threshold
  H(p) makes R(h)<=h/16. Both t and t^eta eventually exceed H(p).
* Complete rectangle addresses have A=O(p). Padding adds fewer than one
  address bit; fixed field/owner inventories change constants. The full
  polynomial record has2^(Omega(p^(1-epsilon))) bits, exceeding every
  fixed power of p, so the source's polynomial descriptor setup is allowed.
* The current exact format has signed width p+h_height+2D+3=Theta(p),
  D<=d and h_height=O(d), plus26 temporary bits. The selected dimension
  bound d=o(p) and any fixed-rank O(f) scale extension preserve Theta(p).
  This is not a logarithmic-width coefficient model. Zero arrays satisfy
  the grid, magnitude and exact-return promises for every member of the family.

These are eventual statements for the one fixed rational point. They do not
give practical cutoffs, bounds uniform as epsilon approaches1, or a promise
for arbitrary independently varying f,p and address geometry.

## 3. Rate comparison and what it proves without a schedule hypothesis

The current elementary monomial-record allowance is
C_move V*((f log p)^tau+1). The positive C child has its own invoice; it
cannot be used to enlarge the allowance for that elementary adapter record.
The graph lower bound being reviewed is Omega(fV), not merely an O(fV)
upper estimate. For p>=2,f>=1,

f/((f log p)^tau+1)=Theta(f^(1-tau)/(log p)^tau).

Consequently serial work meets this tariff only on joint families with
f=O((log p)^(tau/(1-tau))). At the current point the exponent is exactly
24909248545749/90751454251, about274.48. Fixed f and many slowly growing
families therefore are countercases to a blanket rejection of serial maps.

On the admitted group nonleaves the ratio is at least a fixed positive
multiple of

p^(beta*eta*(1-tau))/(log p)^tau → infinity.

The exponent is strictly positive; EXACT-COMPARISONS.json retains its exact
rational value. Its very small size changes the enabling cutoff, not the
limit. Fixed N, matrix size, row width, adapter count and machine constants
cannot absorb it. At the first active group root the stronger lower
f=Theta(p^beta) is available. Thus the unchanged serial implementation fails
the required *uniform per-record interface* even without proving that a full
compiled supplier actually executes a particular adapter there. This is the
unconditional interface conclusion, conditional only on the separately
audited graph lower bound and the selected source promises.

## 4. Volume normalization and the stronger schedule conclusion

The comparison uses the same V in the lower and upper bounds:

* The formal layer's logical bit volume is2Mrw, with all coefficients and
  both complex components. Current w=Theta(p); no p-bit coefficient is
  being counted as a constant-size word on one side only.
* SUPPLIER-SUPPORT-AUDIT §2 and OUTER-AUDIT lines48–52 explicitly execute
  each H call on the whole globally complete tensor across coarse labels.
  A fixed coarse-label microbox is expressly excluded as a supplier call.
  TENSOR-COMPILER says the tensorization uses the same data volume and no
  2^g padding factor. Its stage count and coefficient scans are separately
  paid and do not divide that volume.
* Complete row padding is less than a factor two and is removed before the
  next deferred phase. Compact layout and batched rows give each role
  exactly1/W of its parent's volume with every within-row spectator range
  intact. W is fixed before p varies. Repeated source occurrences and a
  fixed number of helper banks change constants; they do not produce a
  factor1/f volume credit.
* A fixed-rank O(f) coefficient-width extension changes volume by
  1+O(d/p)=1+o(1). Gamma metadata E=O(p) is counted, but amortizing descriptor
  work does not amortize f separate full-payload writes. Splitting the
  address columns into fictitious independent productive roles, omitting
  spectators, or dividing by a number of tensor columns would change the
  interface and is not a normalization available to the current graph.

The stronger conclusion requires an explicit premise: an unchanged
occurrence-by-occurrence root expansion really executes at least one
nontrivial serial adapter on a fixed positive fraction of that complete
call volume. A finite expansion retaining a whole raw source invocation has
such occurrences. This review does not independently map an emitted full
completed-carrier word; the final physical word is not supplied here. An
optimized or differently compiled schedule must establish its own premise.
The revised A README correctly makes this limitation explicit.

Under that premise, the actual Gaussian group family suffices. Its first
root has e=Theta(t),t=Theta(p^beta), so its adapter writes are
Omega(V p^beta). The intended call bound is O(V t^(1-q) polylog p).
Even the larger O(V d^(1-q) polylog p) allowance fails because

beta-epsilon*(1-q)=epsilon*q-2delta>0.

The current grouped Gaussian cost row has exponent epsilon-q*beta; its
d/g group factor was already included. One such direct group root even
exceeds that aggregate allowance, since

beta-(epsilon-q*beta)=beta*q-2delta>0.

OUTER-AUDIT explicitly fixes V=Theta(n),p=Theta(log n). With this same
normalization and current rebound parameters, the direct group root also
exceeds O(V p^(1-kappa)) because beta-(1-kappa)=kappa-3delta>0.
All three margins were independently recomputed as exact rationals. These
are obstructions to the proposed unchanged implementation, not lower bounds
for multiplication or refutations of the conditional selected result.

The initial h=d wording needs qualification. The support capacity argument
does allow a generic admitted t=Theta(d) invocation; it would give an
Omega(Vd) root under the same schedule premise. Capacity alone does not prove
that a particular grouped outer call has that width. The explicit actual
group family above avoids the inference. It also does not need to count
repeated groups to obtain a contradiction. If a schedule supplies Theta(d/g)
such full-volume roots, their direct work would sum to Omega(Vd), but that
additional schedule assertion is unnecessary here.

## 5. Recurrence, stopping leaves and qualifications

For fixed child contractions alpha_j and genuine volume weights omega_j,
let M_s=sum_j omega_j alpha_j^s. The retained strict sigma moment gives
M_1<=M_sigma<1. An optimistic direct implementation with internal O(e)
work per current logical volume would satisfy

F_dir(e)<=sum_j omega_j F_dir(floor(alpha_j e))+Ce.

Summing the internal linear work gives O(e/(1-M_1)). If the unchanged root
actually incurs its proved Omega(e) adapter charge, its normalized internal
work is Theta(e). The positive child appears in the recursive terms; it is
not counted again as adapter cost. Integer floors/remainders and additional
scalar, setup, parking and erasure work cannot remove the root lower bound.
This explains why the serial internal schedule loses the stopped exponent,
without claiming a lower bound for a different schedule.

Direct leaves remain compatible. For the correct invocation-local stop
e_u<t^eta, the weighted-tree inequality gives

sum_leaves (V_u/V_root)*e_u
 <=t^(eta*(1-sigma))*e_root^sigma
 <=t^(sigma+eta*(1-sigma)).

At the exact selected point,1-q-[sigma+eta*(1-sigma)] is
39927398836599/2000000000000000000000000000>0. Thus direct leaves and their
fixed helper constants fit this cost permission. Small/polylogarithmic
phases and a separately charged threshold band are not rejected by the
nonleaf argument. They still need actual format, owner, grid and restoration
interfaces; cost permission is not caller admission. Once-rounded interiors
are not substituted into the retained exact-layer-before-final-truncation
route without their own accumulated-error proof.

No conclusion is proved here for fused records, a zero-skipping or optimized
caller, a different weighted schedule, input-varying epsilon, a growing
carrier, arbitrary independent f/p, or a faster compact-control primitive.
The raw graph does not itself establish physical routing into the selected
source word. These exclusions are substantive. Without the root occurrence
premise, retain only the per-record interface obstruction in §3.

The unchanged conditional kappa and all five retained assumptions remain.
The appropriate next work is a physical implementation meeting the existing
compact-control selected-bit tariff, or a different fully costed schedule;
expanding the present serial graph to all nonleaf maps will not discharge
that interface on this family.

## 6. Reproduce the independent arithmetic/source check

```sh
python3 -I -W error -B check.py --source-repo /path/to/read-only/repo
python3 -I -O -W error -B check.py --source-repo /path/to/read-only/repo
```

`--write` regenerates EXACT-COMPARISONS.json. The checker authenticates the15
exact canonical sources and recomputes the current exponent margins without
importing scientific modules or A's implementation. It does not execute the
heavy selected gate or repeat the graph audit. Mathematical asymptotic and
normalization checks are the arguments above, not finite size extrapolation.
