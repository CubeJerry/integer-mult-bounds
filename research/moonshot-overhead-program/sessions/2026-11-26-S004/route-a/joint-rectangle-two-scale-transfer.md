# Joint rectangle partitions improve both adaptive recurrences

Status: **admitted complete conditional transfer under JR alone**.
The lead and Route C independently accepted the Section 9 compatibility
argument after reading the actual suppliers and source endpoint proof.
Route C's receipt is `REVIEW-JOINT-RECTANGLE-TWO-SCALE.md`; its reviewed
snapshot has SHA-256
`2a2478259b54ef41477098ea77ae6100316f5db78755554771cc4841e0fbb71f`.
This admission changes status only; JR itself remains unproved.
Sections 1--8 first proved the component/recurrence transfer through E003's
then-open executor gates. Section 9 replaces those physical conditions by
the now-admitted E002 variable-profile suppliers. The finite partition
hypothesis JR remains open. No unconditional new multiplier bound is asserted.

This extends S004's lead `joint-rectangle-transfer.md`. It also uses the
concurrent E003 `route-b/TWO-SCALE-RECURSION.md`, which independently supplies
the two different adaptive arity schedules and the complete charged physical
transfer. Its source/physical premises are retained, not inferred from this
graph calculation. The independent derivation of the same two-scale idea in
this route is acknowledged without a priority claim.

Source pins: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, complete
Fourier `build/kernel.tex` and tape `build/interchange.tex` read; programme
compact geometry at `c65aac1156a46d10c0ef2aa36fd846c7a93518e1`; E003
two-scale and physical suppliers at `df91e4c8e31b1020e05056db5b0eb16169ef3421`.

## 1. The same finite graph hypothesis

For q=2^t and k>=1, let C(q,k) have left and right copies of `[q]^k`, with
an edge precisely when every coordinate differs. A rectangle has arbitrary
subsets as its two sides, each cross pair an edge; it need not itself be a
coordinate product.

**JR.** There is one absolute integer c>=2 such that every C(2^t,k) has
a disjoint rectangle partition of per-side vertex load at most

    c^k (t+1)^c.                                             (JRT1)

Root's anchored construction already proves that JR replaces the
interchange label invoice's `d(d-1) log t` term by `O_c(d log(t+1))`.
The additional observation here is that JR applies to the **different
binary Fourier label geometry too**. Both profiles need improvement to
remove the logarithm from the two-scale result.

## 2. Fourier free rectangles with arbitrary correlated sides

Use even L, labels `[q]^L`, and Hamming distance Delta. The exact source
objects for prime radix two are

    Gamma(v,w)=1-Delta(v,w) in F2,
    p(k)=product_(r=1)^(L/2) (1-k/(2r)), k an integer.         (JRT2)

The values p(k) and the coefficients in the source's binomial basis
`binom(L-k,j)` are dyadic. This is not a coefficientwise assertion about
p in the ordinary monomial basis: for example, at L=6 its leading
coefficient is -1/48.

The binary bilinear representation of Gamma has dimension
`D_F<=1+Lq`. Expanding p in the binomial basis gives at most

    N_ch <= sum_(j=0)^(L/2) binom(L,j) q^j <= 2^L q^(L/2)     (JRT3)

charged rectangles in total. A fixed label belongs to at most `2^L` of
them on each side. These charged rectangles and all their coefficients
remain unchanged.

The off-diagonal difference `I-p(Delta)` is supported only at odd distances:
p(0)=1 and p(2r)=0 for 1<=r<=L/2. Fix an odd unequal-position set S of
size k and the common letters outside S. Use JR on its k differing
coordinates. Weight each resulting rectangle by `-p(k)`. Its every cross
pair has distance k, hence Gamma=0. The position set and outside letters
are unique for each edge; disjointness within the JR piece therefore
preserves exact multiplicity one across the full free decomposition.

**Lemma JRT-F.** For each label, the free endpoint load is at most

    sum_(k odd) binom(L,k) c^k(t+1)^c
      <= (1+c)^L(t+1)^c.                                    (JRT4)

Including the charged endpoint incidences increases this by at most a
factor two. No extra factor q^L or number of common outside words enters
the load of a *fixed* vertex: its outside common word is determined.

The source endpoint proof needs only cross orthogonality. With destination
side J, `H=span{d_w:w in J}` lies in `d_v^perp` for every source v.
It does not require the sides to be Cartesian products, nor the restricted
form on H to be nondegenerate. Thus arbitrary JR sides satisfy exactly its
stated common-coordinate and shared-endpoint conditions. The changes of
representatives remain paid binary linear maps on polynomially many slots.
The rational predictor/check coefficients are not interpreted in F2.

Unlike the interchange construction, no first-coordinate anchor is needed
in this Fourier application: only cross orthogonality is required. The
interchange anchor remains confined to its own geometry and does not add
any rational Fourier rank, coefficient height or q factor to JRT4.

## 3. Square-root Fourier routing logarithm

Put x=log2 m and choose an even L within an absolute factor of sqrt(x).
Set q=2^t with t=ceil(2+2x/L). Then

    m N_ch/q^L <= m 2^L q^(-L/2) <=1,
    q^L <= 2^(2x+3L)=m^(2+o(1)).                              (JRT5)

The exact source endpoint bill, with its absolute binary-radix constants,
is bounded by

    R_F <= C(1+Lq)[(1+c)^L(t+1)^c+1].                        (JRT6)

Consequently

    log2 R_F <= t + O(log(L+1))
                 + L log2(1+c)+c log2(t+1)+O(1)
              = O_c(sqrt(x)).                                (JRT7)

The rational constant-tail predictor has O(sqrt m) stages, and its finite
two-child closure retains its previous square-root leaf bill and polynomial
batch width. Therefore the completed normalized numerical template obeys

    2m<=A_m<=4m,
    sigma_m/W_m <= sqrt(A_m) 2^{O_c(sqrt(log2 m))}.             (JRT8)

This removes the earlier `sqrt(log m log log m)` factor in the local
logarithmic Fourier loss. It is a consequence of JR, not a proved new
partition construction.

## 4. Interchange profile on the same hypothesis

The root's anchored JR rectangles retain disjoint inner sides and outer
product structure. S003's explicit dyadic star geometry therefore still
supplies fixed address radix 3, reserve-only basis changes and polynomial
local instruction lists. Its dimension changes only the absolute constant.

For x=log2 m choose the power-of-two distance d within a factor two of
x^(1/3), and q minimal with `q^(d^2)>=2^(2d^2-2)m`. The root's formula is

    log2[D_I(1+lambda_I)]
      <=3x/d+O_c(d^2+d log2(4+x/d^2))=O_c(x^(2/3)).           (JRT9)

The complete finite predictor/repair/occupied-reserve invoice then gives

    Lambda_I(m)<=sqrt(m) 2^{O_c((log2 m)^(2/3))}.             (JRT10)

The same polynomial label-count, batch-logarithm and local-height guards
hold eventually. Parameter choices use integer roots, bit lengths and
integer comparisons, so no real optimization oracle is needed.

## 5. Actual generation and runtime descriptions

For Fourier JR pieces, every universe has size `q^k<=q^L<=m^3` above a
fixed cutoff. For interchange the anchored universe has the root's
polynomial bound. Each partition's allowed side load is polynomial m,
so there are polynomially many nonempty rectangles, and every list has
polynomial bit size. Enumerate candidate lists of that bounded length,
verify exact support/coverage/disjointness and both loads, and retain the
first success. JR guarantees termination.

All searches over the finitely many k values fit `2^{m^{C_c}}` actual
time and `m^{C_c}` workspace after increasing one fixed exponent. Only
one candidate and a binary enumeration counter are stored at a time.
The returned rectangle memberships, endpoint maps, rank factors, bases
and scalar/row instructions have polynomial size. No exponential archive
is used per input datum.

Under the E003 interchange schedule `m=e^beta`, choose its fixed beta
smaller if necessary so that `beta C_c<1/2`. Then construction time
`2^{m^{C_c}}` fits `2^{e/2}` for large e and is absorbed by the complete
two-field payload `V>=2^(2e)`. Under the numerical schedule below,
`m=2^{O((log a)^(2/3))}=a^{o(1)}`, so repeated setup and its retained
space satisfy the same `2^{k^{o(1)}}` total bound as E003. Thus the
conditional searches do not restore the removed logarithmic losses.

The graph premise is not an assumption that a fast multiplier exists.
It concerns explicit finite partitions; its certificate, verification,
construction cap and runtime use are all specified separately.

## 6. Two-scale recurrence with the logarithm removed

Retain every E003 physical condition P-I/P-W/P-O, including actual child
volumes, constant-array local storage or its stated charged alternative,
leading-row product padding, finite-alphabet field handling, precision,
setup, erasure, movement and final common cap. Change only the finite
profiles to JRT8 and JRT10 and charge the constructor in Section 5.

### Interchange

At active width e choose `m` within a constant factor of `e^beta` for
one fixed sufficiently small rational beta>0. The logarithmic child widths
decrease geometrically. Normalizing by sqrt(e), the sum of local
logarithmic child losses is

    sum_i O_c((log m_i)^(2/3))=O_c((log e)^(2/3)).             (JRT11)

The polynomial local toll is below sqrt(e) after beta is chosen against
its absolute degree. The same charged source recurrence therefore gives

    I(u)<=sqrt(u) 2^{O_c((log2(u+2))^(2/3))},                 (JRT12)

with the E003 visited-space and common radix/field guarantees unchanged.

### Numerical Walsh

At active width a put y=ceil(log2(a+2)), choose

    z=ceil(cuberoot(y^2)),          m=2^z+1.                  (JRT13)

Then `z=Theta(y^(2/3))=o(y)`, child width has
`log a-log f=z+O(1)`, and the ordinary physical routing coefficient
`m^{C_c}` contributes only `O_c(z)` to its logarithmic cost. Combining
this with JRT12 bounds the normalized local toll by
`poly(log k) 2^{O_c(y^(2/3))}`.

The normalized child coefficient from JRT8 has logarithm O_c(sqrt z).
For `y/2<=y'<y` and `y-y'=Theta(y^(2/3))`, the mean-value bound gives

    y^(2/3)-(y')^(2/3)
      >= c0 (y-y') y^(-1/3)
      >= c1 y^(1/3) >= c2 sqrt z.                            (JRT14)

Thus the child logarithmic losses telescope to O_c(y_root^(2/3)).
Unfolding the full nonnegative recurrence, including the local toll,
gives `sqrt(a) 2^{O_c((log a)^(2/3))} poly(log k)` per numerical volume.
The leading-batch divisibility product remains polynomial in a because
`sum log m_i<=log a`. The total node count, setup and numerical gains
remain `k^{O_c(1)}`, `2^{k^{o(1)}}` and `k^{o(1)}` respectively.
Consequently one absolute O(k) numerical precision still suffices.

### Whole multiplication, conditional statement

**Theorem JRT.** JR together with the separately verified E003 local
physical interfaces implies one fixed exact finite-alphabet multitape
full-product machine with a single O(n) bound on visited cells and

    T(n)=O_c(n sqrt(L(n)) 2^{O_c(s(n)^(2/3))}),
    L(n)=1+log2 n,        s(n)=log2 L(n).                      (JRT15)

The source outer reduction, exact final carries, numerical error budget,
fallback and common-space chunk wrapper are exactly those proved in the
E003 conditional transfer. Their remaining polynomial-s factors are
absorbed into `2^{O(s^(2/3))}`. If E003's executor premises are later
admitted unconditionally, JR is the only additional hypothesis here.
Until then both statuses must be reported explicitly.

## 7. Why changing only one profile is insufficient for this transfer

Keeping the old Walsh local loss `sqrt(log m log log m)` while improving
only interchange to `(log m)^(2/3)` does not yield JRT15 by the current
recurrence. At log m=z=Theta(y^(2/3)), its accumulated Fourier loss is
of order `y^(2/3)sqrt(log y)` in the corresponding positive invoice.
The balance z versus `y sqrt(log z/z)` instead selects
`z=Theta(y^(2/3)(log y)^(1/3))`, restoring the earlier Phi(y) scale.
This is a limitation of that billed transfer, not an algorithmic lower
bound. JR's second use in the Fourier free rectangles is essential to
the displayed conditional log-factor improvement.

## 8. Exact finite checks and their limit

`verify_joint_rectangle_fourier.py` and its JSON receipt check 139,792
weighted identity entries and 64,616 endpoint-span orthogonality conditions.
The positive controls refine the known first-difference partitions by
checksum classes on both sides. They include 3,584 rectangles whose two
sides are both nonproducts, so the test exercises the correlated-side
interface rather than only the original coordinate products. Their actual
loads are measured; they are not claimed to satisfy JR asymptotically.

The checker rejects 66,664 omitted-free contributions and 72,452 positive
even-distance endpoint uses, checks dyadic values and binomial coefficients
by exact rational arithmetic, and verifies the binary Gram rank bounds.
It also passes 61,860 exact integer parameter-majorant profiles and 1,020
integer recurrence-chain smoke tests. These finite checks support the
identities and guards; the asymptotic recurrence proof is the analytic
argument above, and JR remains wholly open.

## 9. Complete conditional transfer through the admitted E002 suppliers

The concurrent programme checkpoint
`8af1911b02c04d0c410dd181597fd160582a78b4` admits E002's complete
variable-parameter theorem with exponent
`s^(2/3)(log(s+2))^(1/3)`. Its admission is recorded in
`results/epsilon-uniformity/sessions/E002/lead/ADMISSION-V.md`, and its
full root composition is `lead/variable-profile-theorem.md`. This is
concurrent progress, not a result newly established by S004.

For the extension below, the following actual proofs were read, not merely
their prior review statuses: E002's full root theorem and admission;
Route B's `variable-arity-transfer.md`, `variable-interchanger-space.md`,
`composite-radix-padding.md`, and `polynomial-walsh-precision.md`;
Route C's `polynomial-interchange-invoice.md`; and Route A's complete
`VARIABLE-OUTER-SUBSTITUTION.md`, including the local-active-width supplement.
The source Fourier endpoint proof was independently read in Section 2.

The needed substitution is not automatic from a better call coefficient.
JR also changes rectangle memberships, basis plans and construction time.
The following checks establish the physical interface for those changes.

### 9.1 Compact plans, heights and address specialization

The label vectors, rank-fraction matrix, target permutation, predictor,
check construction and finite contraction identities are unchanged.
JR changes only the free rectangle lists and their endpoint bases. Both
label universes and every returned list are polynomial in m, as Section 5
proves. A side is stored by a polynomial-size membership string, never by
one new label attached to every scalar record.

In interchange, the first-coordinate anchor gives precisely the within-side
and cross-side Gram conditions of the original endpoint proof. Its outer
product sides also meet the independently reviewed S003 star-basis interface.
One may instead use the admitted E002 generic rational basis construction:
polynomial-dimensional matrices with polynomial bit heights have
polynomial-height fraction-free elimination and inverse minors. This
produces polynomially many elementary rational address maps. Form their
complete required-unit product before applying E002's composite-radix
selection. Its logarithm remains polynomial in m. No old unit list or
old fixed radix is silently reused for a new basis.

In Fourier, arbitrary correlated JR sides only change the binary span H
and its bases. Gaussian elimination over F2 has polynomial-m cost and
produces 0/1 coordinate matrices; their binary phases are signs, +1 or -1.
The shared endpoints use only cross
orthogonality, already proved in Section 2. The charged rational matrix
and its binomial coefficients are unchanged. Free weights are the existing
dyadic numbers -p(k), of bit height O(L log(L+2)); the same bound holds
for the binomial coefficients by finite differences with the common
dyadic denominator. The number of rectangles is polynomial m. The rational row/check coefficients and complete local
norm gains therefore retain a polynomial-m height and operation bound.
There is no factor exponential in numeric q, in the number of spectral
cases, or in the number of independent input records.

### 9.2 Incidence storage and metadata remain correctly billed

Use E002's one root coefficient field of O(log(U+2)) bits. The shift-check
size B=Theta(m) is unchanged, so every descendant uses its original first
B distinct nodes in this field. No field embedding is repeated.

The grouped comparison-role blocks and their B or 32B payload symbols are
also unchanged. Their O(m)-bit masks are stored once per grouped block,
their polynomial-size repair buffer is reused, and all masks are removed
before a child. JR membership is a *finite label/rectangle control*, not
a new address-dependent spectral mask. Endpoint incidence headers apply
to complete module rows. Under the admitted guard u>=m^K, each such row
has exponentially more payload than its polynomial-size header. Serial
membership and coefficient-table access costs polynomial(m) scans and
fits the same local time invoice. It requires no global table lookup once
per small child or extra field bits per datum.

Prepared source endpoints and destination accumulators occupy exactly
`O((1+lambda_I)V)` as before: each label is copied once per incident
rectangle, independent of whether that side is a coordinate product.
The common rectangle sum can be charged to one of its nonempty incident
sides. Low-rank query accumulators still occupy at most V by
`m r/N<=1`. Preserving these endpoint copies retains their sharing across
queries; no paid endpoint is recomputed for every query.

All physical entry factors in the admitted ledger are retained: less-than-
four binary child repadding, main-child fraction at most 16/N with N>=64,
the 1/16 finite-repair contraction, and at most eightfold reserve entry
inflation after clearing parent arrays. The spatial depth is
O(log log(U+4)). Replacing the monotone endpoint envelope by JRT9 therefore
gives, for original binary volume V0,

    Space_I(U,V0)<=V0 2^{C_c(log2(U+2))^(2/3)}.             (JRT16)

The reserve factor 8^depth, one-time root field, descriptors and marked
interval reuse contribute only fixed powers of log(U+2), absorbed above.
This is a union-of-visited-regions bound, not only a live-memory estimate.

### 9.3 Construction is prepared and bounded separately

For a fixed candidate constant c, exhaustive finite list enumeration is
a bounded algorithm: it either returns a verified JR partition or reports
failure after all lists within the explicit certificate bound. It halts
even if JR is false. The output plan is polynomial size; the search takes
at most `2^{m^{C_c}}` time and polynomial retained workspace.

Choose E002's fixed interchange exponent gamma small enough against this
new constructor degree and every enlarged physical degree. At root width
U, all width-chain construction then has bill `2^{U^eta}` times a fixed
polynomial in log(2V0), for some fixed eta<1. The complete U-bit fields
absorb it. Only compact plans are retained. Descendants receive their root
invocation's local tail chain, as required by the admitted cache amendment;
they do not re-enumerate partitions or scan the global preflight cache.

At numerical width a, m=2^{Theta((log a)^(2/3))}, so all its additional JR
searches fit `2^{k^{o(1)}}`. The *combined* preparation remains the honest
`2^{k^{eta'}}` for some fixed eta'<1, including the polynomial number of
exact-interchanger preparations. It is not renamed `2^{k^{o(1)}}`.
All actual search failure and shape failures select the exact fallback.
Under JR, the verified good branch is eventually always available.

### 9.4 Numerical recurrence, batching and final common cap

The complete rational batch width remains a power of two and polynomial
in m. Its factors are the unchanged power-of-two shift/finite-copy counts
and the new label count q^L, also a power of two. Hence E002's product of
batch divisors still divides the source power-of-two spectator count once
its explicit size guard passes. There is no new per-level padding factor.
Selected-bit gathering remains outside the recursion. Internal coordinate
maps use only their active a-bit field, with other fields as spectators.

Replacing the two finite profiles in the actual V5 and V15 recurrences
gives JRT12 and JRT14 with the admitted local physical bills. Numerical
local space is at most `V m^{K_c} 2^{C_c(log a)^(2/3)}`, which is
`V 2^{O_c((log a)^(2/3))}` at the chosen slower schedule. Numerical child
volume V/W contracts by at least two; reused sibling regions and the
monotone root envelope give the same bound on total visited cells.

The local logarithmic norm gain is polynomial in m. Along a path its sum
is at most `O(log k) 2^{C_c(log k)^(2/3)}=k^{o(1)}`. The product of
polynomial-m branching counts is polynomial k because `sum log m_i`
telescopes. E002's computed precision guard consequently retains an
absolute O(k)-bit format and the source common-ancestor error proof.
Thus the unchanged outer substitution gives a core digit machine with

    time(v)<=v sqrt(L(v)) 2^{C_c(s(v)+1)^(2/3)},
    visited(v)<=v 2^{C_c(s(v)+1)^(2/3)}.                     (JRT17)

For the final wrapper take h as the least integer with
`h^3>=(s+1)^2`, using the integer bit-length version of s, and set
`r=2^{C4 h+C5}`. Constants exceed the proved core-space coefficient.
The admitted actual preflight budget, marked visited cap, quadratic-step
cap, exact schoolbook fallback and positional r-by-r chunk assembly
all apply. Preparation is sublinear, `log r=O_c(s^(2/3))=o(s)`, and
`log ceil(n/r)=log n-O_c(s^(2/3))`. Thus the r^2 chunk calls have the
same asymptotic logarithmic width and multiply the core time by at most
another `2^{O_c(s^(2/3))}`. All cells ever visited lie within the same
fixed O(n) marked regions, including failure cleanup and fallback.

**Theorem JRT-U (complete conditional transfer).** Assuming JR for one
absolute integer c, the admitted source model has one fixed exact
deterministic finite-alphabet multitape full-product machine with

    T(n)=O_c(n sqrt(L(n)) 2^{O_c(s(n)^(2/3))}),
    cells ever visited=O(n).                                (JRT18)

JR is the only additional mathematical hypothesis in this updated
composition. No open E003 executor gate is used as a premise. Independent
review of the new compatibility argument has passed in Route C and the
lead's source audit. These reviews do not supply or certify JR itself.

Open next questions: prove or refute JR; obtain further external review
of the compatibility argument; or replace either decisive profile with a better
construction. No optimization of the elementary balance proves the finite
graph premise.

Credits: the OpenAI free-rectangle endpoint proof and tape architecture;
S004 lead JR hypothesis and anchored geometry; E003 two-scale transfer;
E002's independently admitted complete variable-profile physical theorem;
S002/E002 rational predictor, compact execution and verification;
@CubeJerry; substantial ChatGPT research assistance. No priority,
formal-kernel, full-machine or human-referee certification is claimed.
