# A dyadic ground preload with an actual proper-chart dirty relay

## Status and purpose

**Proved source-specific partial construction. No new kappa.** Two literal
400-coordinate words acquire a new preload from the actual original inputs,
restore respectively 20 and 44 original D fields at proper subcharts of their
final facets, keep every public field monotone, and never send an owned field
to any hosted final facet. All original input directions survive the owned
retirements. This is a genuine nonlocal proper-chart import mechanism.

The 44-output word already exceeds the complete inherited movement allowance
at t=199/200. The 20-output word has positive remaining allowance, but leaves
76 original D restorations and all forward corrections unresolved. Neither
word is a completed native source, a compatible paired source, or a supplier.
The previous omitted-line seed and parity compiler are not composed with it.

This is a **changed preload**. The frozen augmented-decoder package studied
r=(-I+G/12)(d_H,0_U), and its scoped terminal-tour theorem is not applied here.
Here the actually acquired rows are r=(G-I)(d_H,0_U), with exactly dyadic
coefficients. The construction realizes the proper-chart import escape that
was excluded by the older terminal-locality hypothesis; it does not contradict
the correctly restricted theorem.

## 1. Pinned native geometry and algebra

Native gzip SHA256:
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
The 400-coordinate interface parent SHA256 is
`a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc`.

Let P be the actual104 native ports, H its96 hosted ports, and
U=[17,19,30,38,40,47,52,60] its eight coupled ports. Their binary normals v_h
have odd weight3 or7. L_h=<v_h> is the original X/B line; F_h=v_h^perp is the
prescribed rank8 Y/D facet. The canonical real root rho(v) has entries2 at
the three ones and -1 elsewhere when |v|=3; when |v|=7 it is3(e_i-e_j), where
i<j are the two zero positions. Every root has squared norm18.

Use the actual omitted orthogonal frame

    Z=[7,25,42,52,76,82,97,127].

Define g_hi=<rho(v_h),rho(Z_i)>/18 and G_hj=sum_i g_hi g_ji.
Every g_hi is0 or +/-1/2. Exact source arithmetic checks that this is the
entire normalized104-root Gram matrix, not an independently selected fitting.

Let d=(d_h)_{h in H} denote the arbitrary original D inputs. At the ground
chart, eight zero-born temporary owned fields actually acquire

    q_i=sum_{h in H} g_hi d_h.

The public D fields are then changed in place to

    r_h=-d_h+sum_i g_hi q_i,          h in H.             (1)

Seven further stationary owned fields acquire

    r_u=sum_i g_ui q_i,              u in M,             (2)
    M=[19,30,38,40,47,52,60].

Only then are the eight temporary q fields retired. All ADD and SCALE
operations are included in the words. No q or r value is granted as a free
input. All introduced coefficients are exactly dyadic. The r17 row is
redundant: rho17-rho19-rho38+rho40=0, so it is not acquired as an additional
moving record.

The seven roots indexed by M are independent and span rho(448)^perp inside
the real eight-dimensional root space. For every target h below, the exact
rational coefficients beta_hu satisfy

    rho(v_h)=sum_{u in M} beta_hu rho(v_u).

Consequently the actual data identity is

    d_h=-r_h+sum_{u in M} beta_hu r_u.                    (3)

The beta rows are stored in each word and independently checkable from the
root vectors. They are dyadic. This identity is valid for arbitrary original
D data; no extra constraint is imposed on d.

## 2. A general one-active-record relay lemma

Fix a binary bank chart C. Suppose a target cycle T=(h_0,...,h_{k-1}) has:

- L_h contained in C for all h in T;
- seven stationary mode records (2) available at C and identity (3) for
  each h in T;
- C_h=C intersect F_h a proper subchart of F_h, of codimension one in C;
- L_{h_{i+1}} contained in C_{h_i}, with cyclic indices.

Assign the original public carrier ending at F_h the payload r_next(h) at
L_next(h). Such assignment is performed by explicit ground swaps below. An
owned zero record initialized at L_h0 copies r_h0 from the public carrier
currently holding it and moves upward to C. This is the sole active relay.

Inductively suppose it holds r_h at C. SCALE by -1 and add the seven mode
combination from (3); it now holds the **original** d_h. The public carrier
for h moves from L_next(h) to C_h. The active owner descends one rank from C
to C_h. Four cochart operations implement an exact swap:

    D_h += active;
    active -= D_h;
    D_h += active;
    active *= -1.

After these operations D_h=d_h and active=r_next(h). D_h moves upward to its
prescribed F_h. Except after the last target, the owner moves upward one rank
back to C, establishing the induction. After the last swap it holds the
original r_h0 and is retired at the proper C_hlast. The seven mode fields may
also be retired after their last use; their actual nonzero retirements are
recorded. This lemma does not presume that retirement is clean uncomputation.

Every public route is upward. The active owner visits only C and its proper
subcharts C_h, and it imports d_h to a chart where the initial payloads local
to that chart need not determine d_h. There is no final-facet return hidden in
the relay. The active trajectory costs one acquisition ascent plus exactly
2k-1 rank1 transitions; all seven mode acquisitions are charged separately.

For arbitrary field volume V, tensor every displayed scalar operation with
I_V. The same exact algebra, restoration and route statements follow for all
V>=1 over characteristic zero. This proves the scalar circuit construction
for arbitrary input field contents; it is not a uniform physical compiler
or precision theorem for the whole multiplication algorithm.

## 3. The two actual cycles and their proper stops

For the44-target word, C=F_63 has rank8. The targets are exactly the44 hosted
roots orthogonal to rho(448). Their source lines all lie in C. The exact
cycle is stored in WORD.json.gz and reproduced literally by build.py; every
successor normal v_next is binary-orthogonal to v_h. Thus its public path is

    ground(rank0) -> L_next(rank1) -> C_h(rank7) -> F_h(rank8).

The bank C is not any hosted final facet, and each C_h has rank7. The relay
therefore makes zero visits to all96 final hosted facets, while restoring44
original D fields before they arrive at those facets.

For the20-target word, C is the rank7 binary span of the eight coupled
normals. Its actual basis is recorded in the word. Exactly20 hosted normals
lie in it; their real roots lie in the span of M. Its selected adjacent cycle
has C_h of rank6, so the public paths are0->1->6->8. Again neither C nor any
C_h equals a hosted final facet.

The complement of each target set is assigned its own explicitly checked
cycle. Its public carrier for h ends with r_next(h), not d_h, and follows
0->1->8. These remaining carriers are moved to the required final charts to
make the endpoint defect explicit. A later design may defer their final
MOVEs, but must provide an actual replacement decoder and invoice.

At every proper relay stop, the checker establishes that the root coefficient
rows g_j for hosted j!=h whose initial lines are outside that stop span all
of k^8. This certifies that d_h cannot have been obtained solely from the
initial r rows local to that stop, including coupled r rows. Indeed any such
combination has the form

    -sum_{i in H_local} c_i d_i + t^T g_H^T d

for some t in k^8. The output coefficients outside H_local, except h, would
force t to annihilate a spanning set of k^8, hence t=0. Since h itself is not
local to its proper stop, the desired coefficient1 at h is then impossible.
Thus the imported information is genuinely nonlocal; it does not merely
rename a local decoder. The same argument applies entrywise to any nonzero
functional of a V-component output.

## 4. Exact400-input source and remaining paired obligation

The full word retains the actual eight coupled entry operations, so current
X data are a_h=x_h for hosted h and a_u=x_u-y_u for coupled u. It then gives
each hosted B_h a real cocharted read of r_h at L_h. The complete endpoint
map is

    X_h=a_h,
    Y_h=y_h,
    B_h=b_h-d_h+sum_{j in H}G_hj d_j,
    D_h=d_h                       for h in T,
    D_h=r_next(h)                 for h outside T.       (4)

Every one of the400 final chart identifiers matches the retained source
interface, and all400 original input directions survive. For the last claim,
let S=H\T. After fixing the restored D_T rows and permuting the remaining
rows, the remaining D block is G_SS-I. The matrix determinant lemma gives

    det(G_SS-I)=(-1)^|S| det(I8-g_S^T g_S).

The exact right-hand determinants are24387048 for |T|=20 and480000 for
|T|=44. They are nonzero. The X/Y block is invertible because it only performs
the stated coupled shears; each B still has its independent original b
coordinate. Thus the entire400-input map has rank400. The checker also
replays and tests this rank with exact rational elimination.

The reverse residual relative to B=b-d is G_HH, of rank8. **Y is unchanged**,
so the word has no paired forward progress. The full hosted transpose
obligation for the B increment G-I is the forward coefficient I-G.
An additional compatible paired Gram operation could then complete the
diagonal shear, but no such complete forward/restoration assembly is supplied.
The104 forward endpoint equations remain unresolved (112 nonzero original
coordinate debt coefficients, because eight coupled targets involve both x
and y). The52 or76 un-restored original D fields are a separate obligation.

## 5. Literal accounting and target screen

All stationary ground records are counted: eight temporary q lifetimes and
seven coupled-mode lifetimes. With eight coupled-entry lifetimes and the
single active relay, each source has24 INIT/CLEAR lifetimes, peak15. Every
one of the24 retirements has a nonzero actual input-dependent payload; this
is explicitly checked and recorded. There is no discarded unknown original
input because the final map has rank400, as proved above.

The exact MOVE histograms are:

| Restored targets | Public histogram | Owned histogram |
|---|---|---|
|20|1:96, 2:20, 5:20, 7:76, 8:304|1:47, 6:1, 7:7|
|44|1:140, 6:44, 7:52, 8:304|1:95, 7:1, 8:7|

Both public histograms have rank mass3200, the original400 paths of total
rank8. The20 word has2187 instructions:24INIT,1338ADD,571MOVE,24CLEAR,
230SCALE. The44 word has2468 instructions:24INIT,1499ADD,643MOVE,24CLEAR,
278SCALE. These actual counts include the ground permutation, preload,
unknown coupled entry data, seven-mode acquisition, all active reversals,
and the remaining public final-route MOVEs.

The retained full-caller invoice, with P,T, native/helper terms and the
finite-m correction unchanged, has at t=199/200

    R_m = R_infinity - K/(m-1),
    K = 31.5397783670854... .

The directed interval engine certifies:

- 20 source: R_infinity=46.50801152301453..., positive already at m=2;
- 44 source: R_infinity=-9.584891544029109..., negative for every m>=2.

These are **remaining movement allowances for incomplete sources**, not
complete kappa certificates. In the44 case even granting every missing
mathematical operation zero additional movement cannot rescue the unchanged
profile in this caller. It needs removed/replaced paid movement. In the20
case76 D restorations, all forward work, any final residual cancellation,
and all composition expenses must fit the remaining allowance before any
supplier claim could be made. Old-source paid-route credits cannot be added.

The independent-target relay is not a plausible96-output extension at this
price: its one-rank down/up service already tends to192 owned moves, or176
even if eight free first services are granted, before mode acquisition. This
is a bound for that repeated-service mechanism, not a no-go theorem for
multi-output visits, different codes, proper-chart branching generally, or
work replacing existing paid movement.

## 6. Verification and retained limits

The builder checks all400 exact endpoint rows, all400 final chart identifiers,
every actual active-owner original value and displaced next payload, public
monotonicity, zero owned final-facet visits, all20/44 proper-stop exclusion
ranks, all coefficients, both full input ranks, the literal instruction/MOVE
invoice and five semantic mutants for each source. The phase checker verifies
430 introduced chart maps for44 and358 for20, including the down/up relay
maps, with exact Clifford recipes and a wrong-global-phase negative control.

These are exact finite source and chart statements, with a tensor extension
for the stated scalar circuit. They retain the programme's computational
model, physical-cost, uniform supplier, precision, complete paired interface,
recursive source and foundational obligations. No new complete multiplication
bound is established.
