# Conditional log-free two-thirds overhead from rectangle-volume delivery

Status: **complete conditional implication, independently reviewed and admitted**.
The physical delivery hypotheses below are open. Exact rectangle counts
do not establish them. This is not a new unconditional multiplication bound.
The admitted unconditional result remains Theorem V with its logarithmic
factor. All logarithms are binary.

## 1. The proposed local change and its obligations

The existing shared-pencil executor pays for every endpoint incidence.
A rectangle can contain many endpoints but produces one aggregate row.
The proposal is to execute those common-coordinate aggregates with a
recursive-transform bill controlled by rectangle count, while preserving
the source cancellation and arbitrary independent payloads. It is a local
physical routing problem, not a hypothesis that the full multiplier
already has the desired runtime.

Use the pinned OpenAI source at
3344da59991ed94f9ba711217b29c1d760badfa6 and all already reviewed E002
finite predictors, compatible radix, common-field, numerical arithmetic
and outer exact assembly. Let V0 denote encoded input bit volume of one
pencil batch. All programs below must be uniformly generated from their
finite integer parameters by one fixed interpreter and use a fixed finite
alphabet and tape count. Head moves, descriptor scans and erasure count.
One fixed integer K bounds their polynomial description, coefficient-height
and ordinary operation degrees. Effective additive construction may be as
large as 2^{m^K}(1+log(2V0))^K, with compact descriptions retained after
validation. The invoices hold uniformly beyond a sufficient polynomial
m^K bound on required address-field logarithmic widths and numerical
precision parameters, together with the explicitly tested source shape
guards. An unknown fixed-m applicability threshold is not permitted.
Enlarging K and choosing the later arity exponent sufficiently small
pays these local guards; smaller widths retain direct base branches.

**RV-I (exact shared-pencil delivery).** For the retained two-level
characteristic-two label matrix with N labels, rank r*, rational dimension
D and R canonical directed rectangles, assume a correct physical pencil
processor whose actual sum of recursively swapped child bit volumes,
divided by V0, is at most

    C D^K (1+R/N)(1+m r*/N).                           (RV1)

Its nonrecursive time is at most `C m^K s^K V0` plus additive preparation,
where s is the unchanged root-field bit degree. Its endpoint,
query-accumulator and temporary payload workspace is contained in reused
marked contiguous regions whose total union of visited bit cells is at most

    C V0 D^K (1+R/N),                                  (RV2)

plus compact polynomial(m,s) descriptors. Require the same complete-field,
arbitrary spectator and occupied-reserve interfaces as the admitted exact
pencil: metadata stripped before children, unchanged child fields and
restored auxiliaries, and main arrays cleared before reserve descent.
In particular retain the original individual binary main-child volume
bound 16 V0/N (with N>=64), reserve-volume inflation at most eight,
and the completed finite exact-repair contraction at most 1/16 in its
local padded layout, or prove explicit bounds at least as strong. These
are separate requirements on batch and spectator volumes; unchanged
address-field widths alone do not imply them.
Both free-rectangle and low-rank delivery must satisfy the bounds; improving
only the free summation does not establish RV-I. Existing ordinary compact
scalar/repair work remains separately charged.

**RV-W (numerical shared-pencil delivery).** For the binary Fourier label
construction with N=q^L labels, dimension D_F, R_f free rectangles and R_c
charged rectangles, assume a correct physical replacement for the shared
endpoint portion whose number of f-bit Fourier-axis calls per input row
is at most

    C D_F^K (1+R_f/N+m R_c/N).                         (RV3)

It retains the source normalized binary template, exact row cancellation,
input batch and recursive child layouts. All its other work consists of
at most m^K ordinary scalar/row operations and at most m^K of the already
proved address primitives on widths no larger than the active width.
Coefficients have m^K bit height, intermediate ordinary arrays number at
most m^K and occupy reused marked contiguous regions with their total
visited volume bounded by the corresponding array invoice, and setup
has the same fixed-degree effective bound. Thus their
actual numerical tape costs and precision follow from the existing E002
suppliers; address rearrangements are not free in RV-W. The power-of-two
batch, finite repair volume contractions and full independent occupancy
must be preserved, or supplied with equally strong explicit invoices.

No new algebraic identity is presumed for the unchanged predictors or
repair. The two open hypotheses concern how their existing shared pencils
are physically delivered and retained. They allow ordinary polynomial-m
work; they prohibit hiding extra recursive calls or an incidence-sized
retained array in the asserted better bill.

## 2. Exact geometry without the incidence logarithm

Let d>=2 be a power of two, h=2d-1, q=2^t and N=q^(h^2), using
exactly the retained two-level labels. The rank guard is
`q^(d^2)>=2^(2d^2-2)m`, so minimal integer t has
`t<=3+(log m)/d^2` and m r*/N<=1. C's exact canonical counts give

    R/N=binom(h,d)^(d+1) 2^(d(d-1))
         q^d (1-1/q)^(d^2).                          (RV4)

One can also derive RV4 directly by multiplying the nonempty inner
rectangle count `binom(h,d)2^(d-1)[q(q-1)]^d` across d outer positions
and fixing all other positions. This counts aggregate outputs, not the
source/destination incidences of those rectangles.

Writing z=log m, the dimension bound D<=2+h q^h and RV4 imply

    log D=O(dt+log d),
    log(1+R/N)=O(d^2+dt),
    log[D^K(1+R/N)]=O(z/d+d^2).                       (RV5)

Choose d by integer comparisons within a factor two of z^(1/3).
It follows that the normalized pencil invoice and its payload-space
coefficient are both at most `2^{C z^(2/3)}`. We still have
N<=m^(4+o(1)), D=m^o(1), and polynomial-m finite dictionaries.
The variable interchanger's complete finite predictor and repair multiply
the recursive mass by at most C sqrt(m), including their existing
constant padding and reserve charges. Under RV-I, therefore,

    Lambda_I(m)<=C sqrt(m) 2^{C (log m)^(2/3)}.         (RV6)

The improved retained-space coefficient is required by RV2; a better time
count alone would not permit the subsequent common-space wrapper.

## 3. The corresponding binary Fourier count

Use the source binary label parameter L even, q=2^t and N=q^L. Its
charged polynomial has degree L/2 in the match indicators. Its free
support consists exactly of odd Hamming distances. A one-coordinate
first-differing-bit partition has 2(q-1) nonempty directed rectangles.
Thus the exact free rectangle count is

    R_f = [(3q-2)^L-(2-q)^L]/2,                       (RV7)

by summing `binom(L,k) q^(L-k)[2(q-1)]^k` over odd k. In particular
R_f/N<=3^L. Independently, expansion in the match-subset basis gives

    R_c<=sum_(j<=L/2) binom(L,j) q^j<=2^L q^(L/2).     (RV8)

The binary Gram matrix is the constant matrix plus a sum of L equality
matrices, so D_F<=1+Lq. Choose the least power of two q with
`q^(L/2)>=2^L m`. Then q is within a factor two of 4m^(2/L),
m R_c/N<=1, and log D_F=O(z/L+log L+1). Therefore RV-W gives

    log[D_F^K(1+R_f/N+m R_c/N)]
          =O(z/L+L+log L).                            (RV9)

Choose an even integer L within a fixed factor of sqrt(z), using exact
integer square-root comparison. This makes the logarithmic pencil bill
O(sqrt(z)). The original rational predictor has O(sqrt(m)) stages and
the completed finite repair has its existing contraction. Consequently
its full normalized numerical call mass satisfies

    sigma_m/W_m<=C sqrt(m) 2^{C sqrt(log(m+2))}.        (RV10)

The completed input batch remains a power of two and is polynomial m:
q^L<=m^2 2^{O(L)}, the shift seed count is polynomial m, and the
finite contraction is unrolled only O(log m) times. The underlying
coefficient dimensions and bit heights remain polynomial m. These facts
are needed for tape preparation, exact batching and absolute precision.

C's independent `fourier-free-rectangle-counts.md` records these exact
counts against the pinned kernel proof. Counts RV4 and RV7 are proved
combinatorics. Replacing the actual endpoint bill by those output counts
is precisely the unproved physical part RV-I/RV-W.

## 4. Complete conditional transfer

**Theorem RV.** Under RV-I and RV-W, one fixed exact deterministic
finite-alphabet multitape full-product machine has, at every input length,

    T(n)=O(n sqrt(L(n)) 2^{C x^(2/3)}),
    cells ever visited=O(n),
    L(n)=1+log_2 n, x=log_2 L(n).                      (RV11)

This is a complete implication with open local physical hypotheses. No
claim of their implementation is made by the theorem.

**Exact interchange.** Choose m(u)=Theta(u^gamma) by the same odd
integer-root selector as V, with fixed gamma>0 smaller than every
compiler/guard reciprocal. Use the same compatible radix, lower child-width
check and single root field. Children have v<=u/m+2 and logarithmic
widths decreasing geometrically. RV6 gives, after square-root normalization,

    F_I(log u)<=poly(s)+2^{C (log u)^(2/3)}F_I(log v).

The sum of (log u_i)^(2/3) along the chain is O((log U)^(2/3)).
Root field degree, direct bases, depth and constant reserve inflation
contribute only powers of log U. RV2 and the original child-volume
contractions give the same envelope for parked payload space. Thus

    Time_I<=V0 sqrt(U+1) 2^{C (log(U+2))^(2/3)},
    Space_I<=V0 2^{C (log(U+2))^(2/3)}.                (RV12)

Actual compact preparation is at most 2^{U^eta} poly(log(2V0)), eta<1,
which the two complete U-bit fields absorb as before. Source routing
wrappers substitute RV12 in their bounded call lists and add only fixed
powers of log k. The proof order remains noncircular.

**Numerical Walsh.** At active width a let y=ceil(log(a+2)), choose the
largest integer h with h^3<=y^2, and set m=2^h+1. Then
log m=Theta(y^(2/3)), m=a^o(1), and the even child rule gives
`y_child<=y-c y^(2/3)`. The product of the unchanged power-of-two
batch divisors remains at most (a+2)^C, by telescoping sum log m_i.
It divides the root spectator count eventually and is tested exactly.

RV-W's ordinary address operations call the completed RV12 interchanger.
They cost at most

    V m^K sqrt(a+1) 2^{C (log(a+2))^(2/3)} polylog(k),

including initial scalar preparation/application, masks and head returns.
The global selected-position gather remains once at the layer root;
internal children have contiguous active slots. After square-root
normalization the local term is at most 2^{C2 y^(2/3)} times the one
common polylog(k) factor. RV10 gives recursive multiplier at most
2^{C3 y^(1/3)}. A monotone envelope therefore obeys

    F_W(y)<=2^{C2 y^(2/3)}
             +2^{C3 y^(1/3)}F_W(y-c y^(2/3)).          (RV13)

For large y,
`y^(2/3)-(y-c y^(2/3))^(2/3)>=c' y^(1/3)` by the mean value theorem
on [y/2,y]. Taking B>C2 and Bc'>C3 with strict slack makes
`F_W(y)<=2^{B y^(2/3)}` an inductive majorant for both terms. Enlarge
the finite base and decrease c to cover integer rounding. Visible fixed
powers of log k fit this envelope.

Local numerical space is V times 2^{O(y^(2/3))}. Exact V/W child
volumes and finite repair contraction make parked arrays a geometric
series; sibling and stage regions are reused. Logarithmic path norm gain
is at most `log(k+2) 2^{C(log(k+2))^(2/3)}=k^o(1)`. Branch counts are
polynomial k because sum log m_i=O(log k). The existing computed
gain/event-count guard therefore supplies one absolute O(k)-bit format
with the source fixed norm/error allowances. Failed guards retain the
correct direct numerical branch. No desired global precision statement
is inserted as an unproved new premise.

**Exact multiplication and common space.** Substitute the completed
interchange and Walsh bounds into the already audited source guarded
permutations, CRT, occupied short Fourier transforms and final recovery.
They add only fixed logarithmic powers and fixed-degree preparation.
The separate outer short-axis prime cutoff and tested shape conditions
remain unchanged. Phase streams and pointwise products still use the
source fixed O(k log k) short multiplier. Thus the v-bit digit processor
has time `v sqrt(L(v)) 2^{C(log L(v))^(2/3)}` and visited space
`v 2^{C(log L(v))^(2/3)}`. The unitary-boundary error induction, integer
rounding and carries still return the exact full product.

Combined optional preparation is 2^{k^eta'} for a fixed eta'<1, not a
per-record lookup charge. Prepare the polynomial-size set of compact root
plans once. Global cache access occurs only at external invocation
boundaries; spatial descendants retain their local chain/current descriptor.
This is the same verified cache interface as V.

Select r=2^(C4 h+C5), where h is an integer ceiling cube root of y^2
and y=x+O(1) comes from input bit lengths. Take v=ceil(n/r), with an
r<=n guard. Choose fixed C4,C5 large enough for the digit space factor.
Preflight has an n/16 actual-step/visited allowance; the candidate has
one fixed O(n) marked space allowance and a quadratic actual-step clock.
Abort before a forbidden head move, clear scratch and use exact schoolbook
on any failure. Inputs, outputs, clocks and assembly are all charged.

Eventually log r=O(x^(2/3))=o(x), the digit core occupies at most n/4,
and 2^{L(n)^eta'}=n^o(1) preparation fits its cap. All shape/precision
guards pass. The r^2 products and O(nr) positional assembly have total
cost at most `n sqrt(L(n)) 2^{C' x^(2/3)}`, below the quadratic cap.
The remaining finite input range is covered by exact fallback and one
larger absolute time constant. Reused marked intervals bound the union
of visited cells, proving RV11 under precisely RV-I and RV-W. QED.

## 5. What has and has not been supplied

The rank estimates, exact rectangle counts, parameter choices, two physical
recurrence implications, precision/threshold absorption and common-cap
composition above are the conditional proof. RV-I and RV-W remain open.
They must actually deliver the source/destination arrays in their required
common address layouts, preserve off-diagonal cancellation, price all
recursive transforms, and return every occupied auxiliary coordinate.
Forming formal rectangle sums before making those address changes is not
a proof of the hypotheses.

For RV-I, time and workspace both matter: the current canonical partition
has exact incidence lambda, and retaining one array per incidence defeats
RV2 even if a smaller transform count were shown. For RV-W, its true
spectral/Fourier call bill must improve; a faster exact interchanger alone
leaves the old numerical certificate's square-root-logarithmic kernel
excess and its Phi-scale barrier. The separate numerical-invoice note
explains that distinction.

The condition is stronger than an output-count observation and weaker
than postulating a near-root multiplier. It is a pair of finite-parameter
shared-pencil execution contracts, admitting separate constructive tests,
counterexamples or replacements. Current coordinate-basis obstructions
exclude only particular simple implementations, not these hypotheses.

If both hypotheses are established, RV11 gives log-free beta=2/3. It still
does not give H polynomial in x, H bounded, or the exact square-root
endpoint. No kappa_ov is assigned. The unconditional programme result
continues to be V until every stronger physical gate has an actual proof.

Credits: @CubeJerry; pinned OpenAI shared-pencil and binary kernel proofs;
prior characteristic-two geometry; E002 C's exact canonical and Fourier
rectangle counts; E002 A/B/C compact suppliers and variable transfer;
and substantial ChatGPT multi-agent assistance. This conditional theorem
has no claim of literature priority, full execution or formal refinement.
