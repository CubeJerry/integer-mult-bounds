# A uniform block-rank gap for sparse actual BIT fittings

**Author theorem, independent review pending. No new complete kappa.**

This is a quantitative successor to S011 saturated-star rigidity. It proves
a gap proportional to arbitrary block width, rather than only excluding the
exact minimum rank. No common invariant subspace, commuting block model,
scalar replication, or physical availability of a code is assumed.

## 1. Exact statements

Use the actual 111-port BIT graph from native SHA256
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
A fitting `A` has `V` by `V` identity diagonal blocks, zero blocks at all
prescribed noncontacts, and arbitrary remaining blocks. The value field has
characteristic two and `V` is any positive integer. Set

    r = rank A = 9V + h,  h >= 0.

The existing all-width minrank theorem supplies `h>=0`. For row `i`, let
`support_i` count foreign source roles `j` whose entire block `A_ij` is
nonzero, whether or not it is invertible. Define

    ell_i(A) = 1[support_i > 36] + 1[support_i > 52].

**Theorem 1 (reciprocity stability).** The exact finite certificate supplies
3,019 unordered actual contacts `{i,j}` for which every such fitting satisfies

    rank(I_V - A_ij A_ji) <= 3h,
    rank(A_ij) >= V-3h,   rank(A_ji) >= V-3h.

The coefficient `3` follows from a general complete-seven-star inequality,
proved below. The certificate has 275 explicitly listed configurations.
They are witnesses; completeness of their search is not a premise.

**Theorem 2 (arrival-sparse fitting gap).** If `sum_i ell_i(A)<=196`, then

    rank A >= 9V + ceil(V/3) = ceil(28V/3).

Indeed, if `h<V/3`, all 3,019 certified contacts remain nonzero in both
orders. Each row then has at least 41 certified foreign contacts, and 86
rows have at least 53. Hence `sum ell_i>=111+86=197`, a contradiction.

This is an arbitrary-block theorem, not `rank>=10V`. For `V=1,2,3`, its
integer lower bounds are respectively 10,19,28. For general `V` the leading
ratio is `28/3`. The stronger source-specific rank-16 statement for one
particular class target is a different result and is not replaced by this
one.

**Corollary 3 (declared monotone source interface).** In the admitted actual
history normalization with arbitrary cocharted original-Y feedback,

    sum_i ell_i(A) <= 111 + q + a,

where `q` is the number of persistent whole-`V` descending packet lifetimes
and `a` counts separately paid additional upward facet arrivals. If
`q+a<=85`, the actual normal-form fitting and its actual historical
X-coefficient span satisfy

    rank A >= ceil(28V/3),
    rank(G_x) >= ceil(28V/3),
    sum_C nu_C >= ceil(28V/3) - qV.

In particular, for the specified q8 route model with at most three extra
whole-record facet arrivals, `sum ell<=122`; therefore

    rank A >= 9V+ceil(V/3),
    sum_C nu_C >= V+ceil(V/3) = ceil(4V/3).

The corollary is a necessary information/history condition. It creates no
packet, no local observer, no free historical mode, no restoration word and
no new movement-to-covered-BIT conversion. The source still owes the actual
cell image equations, all 222 endpoints, complete chronology and every cost.

## 2. Credited star inequality and its variables

Use the normalized point-frame factorization described in S011
`block-rigidity/PROOF.md`, itself building on DreamingOfClouds PR #7114 at
`fc90dc68b54d613a0600e5bddd8e4f557a4b4eda`, Proposition 10 (LR).
For an edge role `e={a,b}` define

    alpha_e(a)=C_ea R_ea,
    S_e=C_e,last R_e,last,
    gamma_e(a)=alpha_e(a)+S_e,
    g_e(a)=rank gamma_e(a),
    G_a=sum_{e incident to a} g_e(a).

The edge diagonal gives `alpha_e(a)+alpha_e(b)+S_e=I`, so

    gamma_e(b)=I-alpha_e(a).                           (1)

At complement dimension `j=V+h`, the all-field LR inequality reads

    G_a <= h + 2(g_e(a)+g_e(b))                         (2)

for every incident edge `e={a,b}`. It is a rank statement over an arbitrary
field with unrestricted matrix blocks. Its full elementary proof is retained
in the saturated-star package; no numerical optimizer or finite solver is
used as a premise here.

## 3. Complete-seven-star defect lemma

**Lemma.** If the selected edge graph is `K7`, every endpoint defect obeys
`g_e(a)<=3h`.

Fix an edge `{a,b}` and let `W` be its other five point vertices. Put

    x = g_ab(a),
    Q_a = sum_{c in W} g_ac(c),
    Q_b = sum_{c in W} g_bc(c),
    T = sum_{c in W} sum_{d in W, d != c} g_cd(c).

Thus `sum_{c in W}G_c=Q_a+Q_b+T`. Sum (2) over all 20 oriented edges
`c -> d` within the five-vertex complete graph on `W`. Every `G_c` appears
four times, and every internal endpoint defect appears four times on the
right. Therefore

    4(Q_a+Q_b+T) <= 20h+4T,
    Q_a+Q_b <= 5h,  hence Q_a<=5h.                     (3)

Now sum (2) at `a` over its five edges `{a,c}`, `c in W`. Their `a`-end
defects sum to `G_a-x`. Consequently

    5G_a <= 5h+2(G_a-x+Q_a),
    3G_a+2x <= 5h+2Q_a <= 15h.

All ranks are nonnegative, and `G_a>=x`, so `5x<=15h`. This proves the
lemma. The edge and endpoint were arbitrary. The same argument works for
`K_n`, `n>=7`; the seven-point case suffices here.

The constant three is exact for these LR inequalities considered alone.
For `h=1`, set `g_ab(a)=3`, set `g_ac(c)=1` for each of the other five
vertices `c`, and set every other endpoint defect to zero. All instances
of (2) hold. This does not claim that an actual fitting realizes those
abstract defect numbers; it is a negative control against extracting a
coefficient two from the same inequalities without another argument.

## 4. Applying the lemma inside an actual eight-frame

Every listed configuration contains an actual independent eight-frame `F`
and one omitted point index. Normalize the complete eight-frame in a
rank-`9V+h` factorization. There are eight point coordinates of dimension
`V`, plus the complement of dimension `V+h`.

For each of the 21 endpoint pairs among the seven retained points, the
certificate identifies an actual edge role whose contacts with the FULL
eight-frame are precisely that pair. Its factors therefore vanish on all
other six point coordinates, including the omitted eighth coordinate.
This is crucial: the active star has seven point blocks and complement
`j=V+h`. Dropping the unused eighth point does not turn the complement into
`2V+h`, because every selected edge factor has zero in that coordinate.
All shared-endpoint edge pairs are verified actual noncontacts. Thus the
lemma applies to the selected `K7` star.

If actual point role `i` is one endpoint of edge role `j`, frame
normalization gives

    alpha_j(i) = A_ji A_ij.

By (1), its identity defect is the `gamma` at the other endpoint, so
`rank(I-A_ji A_ij)<=3h`. For square matrices `B,C`, the kernels of `I-BC`
and `I-CB` are isomorphic: `C` maps the first to the second, with inverse
`B` on these kernels. Hence their ranks agree, giving the displayed order
in Theorem 1 as well. Finally

    rank(A_ij), rank(A_ji) >= rank(A_ji A_ij)
                          >= V-rank(I-A_ji A_ij) >= V-3h.

No blocks are commuted, and no Schur invertibility is assumed. The complete
certificate covers 3,019 unordered pairs, each in both directions. The
pure fitting rank-gap argument then follows exactly as in Section 1.

## 5. Arrival dependency, scope and source accounting

The source corollary uses the admitted
`results/bit-y-feedback-normalization/author/PROOF.md`, Sections 1–4, and
its `ADMISSION.md`, plus the independently proved E7 support-union bounds.
That normalization explicitly allows every field, every whole-record width,
arbitrary noncommuting block operations, singular packet-through maps and
actual original-Y feedback. It yields `A=Lambda G_x` and
`rank(G_x)<=qV+sum nu_C`.

Its support bound counts original source lines with NONZERO coefficient
blocks. Left multiplication or local mixing cannot create a source column
outside the actual chart. A block of rank one still requires its original
source line in that union; invertibility is not assumed. Therefore the
positive ranks supplied by Theorem 1 are sufficient for its `ell_i` test.
The proper-subspace bound 36 and two-subspace-union bound 52 concern real
source lines, not value-field dimensions or ranks of the coefficient blocks.

Monotone original X/Y routes, persistent descending packets, zero-born
locally generated caches, paid extra ascending records, no uncounted down
traffic, no restarts/nonlocal births, and whole-record accounting are
retained. Changing them requires a new normal form and invoice. The
q8/three-arrival specialization is stated with that explicit allowance;
it does not establish an all-size covered-BIT supplier from movement prices.
No fractional-volume carrier reinterpretation is made.

The five foundational assumptions remain unchanged. No complete new source,
uniform supplier, unconditional multiplier or complete kappa is established.
The rank-16 class-code construction remains possible under this theorem.
The discovery is the first stated uniform proportional rank/history gap
beyond the minimum in the declared arbitrary-block arrival interface.
No global literature-priority claim is made.

## 6. Verification and controls

`verify.py` reads the authenticated native directly. For all 275 witness
configurations it checks the independent eight-frame, exact two-point
contact signatures, all 21 distinct edge roles, every shared-endpoint zero,
and all resulting contact pairs. It recomputes the 111 guaranteed support
counts and the 197 arrival lower bound. It does not require that every
possible eight-frame or seven-star was searched.

The checker also verifies the exact LR summation identities in a formal
coefficient vector space, the coefficient-three defect control, and detects
an invalid frame, missing witness coverage and an overstated arrival count.
The construction/search script is not imported by the verifier. Finite
witness checking supplies source geometry; Sections 2–4 prove every field
and width.

## Open next questions

1. Can the full source geometry strengthen the uniform `28/3` rank floor
   for arrival-sparse fittings? The LR system alone permits endpoint defect
   `3h`, so a stronger individual coefficient needs further information.
2. Can an actual block fitting near this floor satisfy the arrival budget,
   or does the zero pattern force a larger proportional gap? An algebraic
   example still requires a physical source and full costs.
3. Which physically useful higher-rank or changed-mask representations
   exploit the now quantified departure from canonical minimum rank?

Prepared for @CubeJerry with substantial OpenAI assistance. Credit
DreamingOfClouds (#7114/#6933) for the star framework and LR inequality;
the retained BIT source/minrank/geometry/history authors for their exact
premises; Worker C and the root's independent direct-summation derivation
for the complete-seven defect lemma and this exact-source rank/history
application. No human or formal proof-kernel review is claimed.
