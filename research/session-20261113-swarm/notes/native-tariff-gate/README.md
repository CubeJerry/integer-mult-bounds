# Gate for using the literal adapters in the selected recursion

This is a source-pinned implementation handoff, not a new multiplication
bound or a proposed general native compiler. Canonical main is
`e54523517d0f03e58352e647c403a5af3e525a57`. No frozen core, endpoint or
once-rounded package was changed. The selected kappa and its five assumptions
remain unchanged.

**Decision.** Do not expand the current serial-column CNOT mechanism into
all selected nonleaf recipes. Its actual executed cost fails the elementary
monomial-record tariff on the admitted joint parameter family. Existing
direct stopping leaves remain a possible budgeted use. A different complete
schedule might succeed; this argument concerns the present literal graphs
and their unchanged concatenation into source occurrences.

The positive central C child is paid separately. No lower bound on that child
is used to reject an adapter-only allowance.

## 1. Exact sources and the joint regime

`SOURCES.json` gives commit, path, Git blob, byte count and SHA256 for every
source below. The primary current application review has Git blob
`3dd1af2285e597676725e85ad4f65e7ad326d695`.

The current #7000 application review sections 2, 5 and 6 retains:

* One positive rank-rf child with two complete monomial adapters for each
  nested quotient. A fixed number of elementary records implements each
  fixed binary matrix, phase or translation.
* An elementary record allowance
  `C_move V ((f log p)^tau+1)`, including controls, return and setup. This is
  not the allowance for the whole MOVE or for the positive C child.
* Root selected dimension at most `d=Theta(p^epsilon)`, fixed
  `0<epsilon<1`, and a common exact grid before one final truncation.
  The actual component width is `w_sel=p+h+2D+3=Theta(p)`, with `h=O(d)`
  and `D<=d`; temporary rows have 26 additional bits. It is not a
  `Theta(log p)`-bit coefficient format.
* A fixed, input-independent complex carrier `N=2^H_C`,
  `H_C=14174600000000000000`. Finite word/role counts, coefficients,
  cutoffs and physical constants are chosen before p varies.

The binding from INDEPENDENT-SOURCES.json through full_verify.py to the
current interval_gate.py, not that script's older command-line defaults,
gives the exact values in PARAMETERS.json:

```
g=10^-14, epsilon=1-g, eta=stop=g,
a=kappa+4g, tau=1-a=0.99636994182996,
b=kappa+5g, sigma=1-b=0.99636994182995,
q=kappa+3g, lambda_prime=1-q=0.99636994182997.
```

Here eta is the recursive stopping exponent. The outer group exponent
`beta=1-3g` is a different parameter. The actual layer relation is
`d<=floor(b_in^epsilon)` with `p=6 b_in` eventually, as retained in the
physical specialization; the root family has d of that polynomial order.
For a node of width e in a supplier invocation of top width t, strip its
bounded remainder modulo the fixed carrier, put `f=floor(e/N)`, and stop
when `e<t^eta`. The support-local audit explicitly keeps that invocation's
top width in its stopping test; it is not always the largest outer d.
For any invocation with polynomial top width t, a nonleaf consequently has,
eventually,

```
t^eta >= 2N,   f >= e/(2N) >= t^eta/(2N),   f<=e<=d<=p.
```

The address/record qualifications are substantive: complete rectangular
ranges, global address length `A=O(p)`, descriptors of fixed polynomial
degree in A, full arbitrary spectators and distinct actual owners. The
retained coefficient record fibre is `2^(Omega(p^(1-epsilon)))`, hence
exceeds every fixed power of p. Shape metadata and record-paid phase/offset
work are covered at a fresh fixed cutoff, not made free.

The actual retained outer layout is the support-local, deferred wrapper.
It must not be restricted by the obsolete `K=floor(d^c)` layout. Its explicit
choice is

```
G=4 ceil(log2 p)+6,   K=128G.
```

The old sufficient wording `K/log p -> infinity` is replaced by the proved
finite guard `K>=G+4 ceil(log2 p)+10`. This is stated explicitly in the
support audit section 4 and in OUTER-TRANSFER-AUDIT section 5. Each original
axis has `Theta(p/d)=Theta(p^(1-epsilon))` bits, so K fits eventually.
At a phase with h selected bits, all compact and row fields are assembled
from complete neighborhoods in the global tensor. Reserved bits are
deferred. Above a fixed polylogarithmic tail their total R(h) is at most
h/16; active width is at least 15h/16. The updated current BIT stock has
atom exponent 1/250 and a sublinear stock bound, as required in application
review section 3 and the current functional outer checks. Do not substitute
the earlier 0.003 atom for that update.

Capacity permits h=d as a large interface family, with e=Theta(d):
`d K=O(p^epsilon log p)=o(p)`, the complete neighborhoods and larger
`O(d log^2 p)` routing reservoirs fit in the full `Theta(p)`-bit tensor,
and the original axes each contain their own neighborhood. This capacity
statement alone does not identify a literal scheduled main stage. The
explicitly scheduled Gaussian groups instead have top width
`t=g_group=Theta(p^beta)`, with `beta=1-3g<epsilon`; their first phase
still has e=Theta(t). No condition
requires all controls to fit in one original axis. A fixed coarse-label
microbox alone is not an admitted complete-field call.

## 2. An executed lower bound for the actual monomial adapters

The literal #7430 source is pinned at
`39b40c465f7636a4bb6d70af28595fe8f70f4f3f`, paths
research/literal-selected-linear-maps/{linear.py,PROOF.md,README.md}.
Its right and left fixed G words have 19 and 27 CNOTs, respectively.
Its proof already calls the result a direct-leaf implementation; no new
identity or faster primitive is claimed here.

Consider one call to linear.py's `cnot_columns`. Its F tape has f marks.
For column j the generated geometry is

```
[A_j] x [2] x [M] x [2] x [B_j],   4 A_j M B_j=V.
```

For each of the A_j prefixes and M middle positions, the program emits
all four B_j-bit chunks and then merges the two complete output halves
into the other bank. In particular the merge alone executes at least
`4 A_j M B_j=V` actual payload WRITE instructions. The column_done branch
advances F once and continues until all f marks have been consumed. The
payload symbol zero is distinct from BLANK and has its own branch; there
is no zero-value shortcut. Thus **one literal CNOT executes at least fV
payload writes on every successful legal input**. The complete right and
left programs execute at least 19fV and 27fV such writes. Their upper
bound is the separately proved `65536(fV+E+1)`.

Take all-zero Gaussian coefficients, any positive packed P,S,r and
`w=Theta(p)>=2`, and the valid source header/window/owner boundary. These
are legal successful adapter inputs for every f. All-zero values also meet
the exact common-grid numerical domain and survive any surrounding unit
phases and positive C children. The lower bound is independent of numerical
overflow, carries or failure paths. This is an executed-step lower bound
for an elementary monomial adapter, not merely failure to absorb an upper
estimate, and not a bound taken from the C stages.

The current graph uses a packed nine-slot interface; selected production
uses spaced selected bits and additional controls. Even granting a free,
exact packing and owner bridge would leave this fV cost. Such a free bridge
is only an optimistic comparison, not a claimed admitted operation.

## 3. Comparing the actual f,p regime

For p>=2 and f>=1, within fixed factors,

```
f / ((f log2 p)^tau+1) = Theta(f^(1-tau)/(log2 p)^tau).
```

Hence a Theta(fV) adapter can meet the stated record rate on a family
exactly when

```
f=O((log p)^(tau/(1-tau))).
```

Fixed f and sufficiently slow growing f are therefore compatible. The exact
selected logarithmic threshold exponent is about 274.47767918798417.
Comparing f only with f^tau would miss these compatible joint regimes.

At nonleaves of this admitted Gaussian-group first phase, the lower
cutoff instead gives

```
f / ((f log2 p)^tau+1)
 >= c p^(beta*eta*(1-tau)) / (log2 p)^tau -> infinity,
```

where c>0 depends only on fixed source parameters. Here
`beta*eta*(1-tau)>0`, about `3.630058170039891e-17` for the selected
point. Its tiny size changes thresholds, not the unbounded limit. Enlarging
one fixed cutoff or finite constant cannot bound it. Thus the current
serial-column CNOT cannot implement that monomial-record interface on all
selected nonleaves. For another polynomial top width `t=Theta(p^zeta)`,
replace beta by zeta in the same comparison. Small or polylogarithmic
phases are not claimed to violate it.

## 4. Whole recurrence, separate child bill, and permitted leaves

For the proposed unchanged occurrence-by-occurrence substitution, make the
schedule premise explicit: at least one nontrivial serial adapter is
executed at this root on a role stream whose volume is a fixed positive
multiple of the current node volume. The local graph lower bound alone
does not prove this schedule fact. A literal expansion retaining a whole
raw source invocation has this property; no independent full mapping of
the unmaterialized completed carrier word is delivered here. An optimized
schedule could require a separate argument. Dilation inside the finite
carrier and all role fractions are fixed constants. Under this premise, at the first
Gaussian-group phase with e=Theta(p^beta), the writes proved above therefore
cost Omega(V p^beta) already at the root occurrence. The source requires H
supplier calls on the whole complete global tensor, not on a fixed
coarse-label microbox; this is the full call volume V. The separately billed
recursive C children, scalar contacts, exposure, helper retirement and
suspended storage add nonnegative work. The retained layer target is
`O(V t^(1-q) polylog p)` for top width t. Even granting the larger
`O(V d^(1-q) polylog p)` allowance would not absorb the group root:

```
beta - epsilon*(1-q) = epsilon*q - 2g > 0.
```

The outer Gaussian row is `O(V p^(epsilon-q*beta) polylog p)` after its
group count; a single such direct group root already exceeds it since
`beta-(epsilon-q*beta)=beta*q-2g>0`. It also exceeds the global target
`O(V p^(1-kappa))` because `beta-(1-kappa)=kappa-3g>0`.
These comparisons use the explicit group family and do not assume h=d is
an actually scheduled stage. They concern the same full-volume call
normalization retained by the support wrapper.

This conclusion concerns the concatenated serial schedule. It does not
forbid optimizing away particular records, using different recurrences,
amortizing a different actual schedule, or constructing faster adapters.

An optimistic recurrence reaches the same scoped answer. Write
`M_s=sum_j omega_j alpha_j^s<1` for the retained sigma moment of children,
where omega_j are their genuine volume weights and `0<alpha_j<1` are
their fixed width contractions. Then `M_1<=M_sigma<1`. Granting all
interfaces and replacing internal adapter work by O(e) per logical volume
would give

```
F_dir(e) <= sum_j omega_j F_dir(floor(alpha_j e)) + C e.
```

The total normalized internal direct work is O(e/(1-M_1)); the root lower
bound makes this Theta(e) for the unchanged schedule. Recursive C work is
represented by the recursive terms; it has not been charged as part of an
adapter record or counted twice. The improved stopped exponent is lost.

Direct stopping leaves have a different bill. For widths `e_u<d^eta`,
the retained weighted-tree proof gives

```
sum_leaves (V_u/V_root) e_u
 <= d^(eta*(1-sigma)) e_root^sigma
 <= d^(sigma+eta*(1-sigma)).
```

The exponent is strictly below `1-q`; the exact positive slack is in
PARAMETERS.json. A fixed recipe constant and linear helpers can be charged
there. A fixed band near the stopping threshold could likewise be charged
through an explicit weighted-tree bound; it need not meet the nonleaf
record interface. The polylogarithmic support tail is separately permitted
by the retained wrapper.

This cost permission alone does not bind the packed literal service to a
selected caller. Exact entry production, complete spectators/controls,
codec and owner transport, child boundary, original grid, successful return,
full scratch/history and cutoff must still be supplied. The once-rounded
service is outside the exact-layer-before-one-truncation route; interior
substitution requires a separate accumulated-error/caller proof.

## 5. Width, helpers, recovery gate and novelty

For fixed rank rho<=9, the physical scale wrappers enlarge width by
O(rho f)+O(1). In the selected family f<=d=o(p), so
`w_enlarged=Theta(p)` and `V_enlarged/V=1+O(d/p)=1+o(1)`.
A fixed number of complete helper banks and their copies, resets, returns
and history change constants. Metadata E=O(p) is dominated by the retained
record fibre. These observations do not improve the fV lower bound.
They also do not identify local erased backing with fresh free storage.

The smallest enabling faster routing contract is the already stated
compact-control selected-bit CNOT, for both physical source orders, with
two front and one back arbitrary complete dirty fields of width
`(f-1)G`, actual descriptor production, exact bad-set repair and complete
restoration at `O(V((f log p)^tau+1))`. A literal implementation must pay
its at most twelve arbitrary-width chunk interchanges and ten controlled
rotations using the completed BIT backend and its full restored stock.
An oracle callback to that backend is not a literal implementation.
One useful first dependency is a literal version of the arbitrary-width
equal-chunk interchange/record-paid rotation at this exact ABI. Then a
finite G word composes a fixed number of calls; the positive C child still
needs its separately paid recursive contract.

The current linear predecessor already states O(fV) direct-leaf scope and
leaves faster nonleaf work open. The canonical compact-control and
weighted-tree notes already contain the faster target and permitted direct
leaf budget. This note adds an explicit executed adapter lower bound and
the actual selected joint/cutoff comparison, including the newer logarithmic
K wrapper. It is a recovery gate, not a claim of a new lower bound for
multiplication, an assumption discharge or a reason to expand all 3,057 maps.

All mathematical, compact-control, BIT, native-word and compiler credit
remains with the pinned sources and their notices. Prepared with substantial
OpenAI assistance; this is an agent-authored audit, not independent human or
proof-kernel acceptance. No implementation or publication was performed.
