# Independent A audit of the outer tape caller

Status: source-specific composition audit. It supplies the remaining outer
routing/assembly interface to a polynomial-m interchanger and the separately
proved rational Walsh numerical processor. It does not reprove the source's
entire short-transform mathematics or claim a formal machine refinement.

Read in full during E002: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`,
November tape `build/permutations.tex`, `build/walsh.tex`,
`build/integers.tex`; Fourier `build/binary.tex`. The local interchanger
supplier is C I1--I7, independently reviewed separately. Numerical supplier
is B W1--W3, also independently reviewed separately. All polynomial degrees
below are fixed by this finite grammar and are independent of m or input.

## 1. Explicit interface

Let rho=1/2+1/(2J), J>=4. Assume the accepted finite parameter family has
log m=O(J^3 log J), a polynomial-m physical interchanger, polynomial-m
rational Walsh row operations and branch count, and strict normalized child
margin at most 1/2. Let k be the source numerical address width, and require
k>=m^K for a sufficiently large absolute K. Numerical records have an
absolute constant multiple of k signed/fractional bits, as supplied by W3.
This constant no longer depends on an expanded finite table.

Then the outer source construction has a polynomial-m volume coefficient,
with only a fixed power of log k remaining. Its additive setup can be bounded
conservatively by 2^(m^C)(1+k)^(m^C). No exponentially expanded transition
list, alphabet truth table or spectral-case list is consulted per datum.

## 2. Bulk XOR and controlled-block guards

A fixed finite grammar of coefficient/index/offset calculations has bill
m^c k^e for absolute c,e; e can be increased to include address tagging
and stable exceptional sorting. Use, for example,

    G=ceil((e+5)log2(2k)+(c+2)log2(m+2)).             (OA1)

Each nonempty guarded target fiber has at least 2^G records, which pays
its prefix offset computation. The exceptional fraction is at most
80k*2^(-G), as in `lem:packed-xor`. Multiplying that fraction by the
m^c k^e destination computation and the O(k^2) tag/radix-sort bill leaves
O(V) work after one fixed enlargement. Counter scans and head returns are
already included in the source primitive.

For k>=m, G=O(log(2k)) with an absolute constant. Alternatively one may
retain the polynomial-m coefficient explicitly; either bound is sufficient.
Short chunks L<G are handled by their at most G direct bit operations,
so no threshold failure appears at deeper narrow slots. Their third borrowed
chunk is restored and all of its coordinates remain occupied.

The fixed number of full-width interchanges in a pass cost
m^{O(1)}V(1+L^rho). There are O(log k) passes. Therefore bulk XOR has
m^{O(1)}V(1+L^rho)(1+log k) plus fixed-degree setup, with its exact
original address action. The same bit-permutation and Beneš-network
construction gives

    m^{O(1)} V(1+k)^rho(1+log k)^3                 (OA2)

for the source controlled small-block permutations. Target blocks have
O(log k) bits of absolute constant width, and the source caller retains
an absolute free-control fraction. Polynomial-m table/control processing
is charged via OA1, not assumed free.

## 3. The numerical Walsh physical caller

The rational finite family has A=Theta(m), W<=m^C and sigma<=m^C after
its finite repair unrolling. Its normalized child bill is sigma/W<=A^rho/2.
Binary elimination of the polynomial-dimensional column maps gives
polynomially many slot exchanges and additions. I7 and OA1 price them with
polynomial-m coefficients. Pointwise signs and spectral tuple functions
can scan the complete O(k)-bit address per numerical record: its Theta(k)
bit width pays this scan. Applying the exact short-rational coefficient
with W1 costs k*poly(m), including long/short multiplication and division.
General k-by-k products still use the source fixed O(k log k) short
multiplier. That primitive is not derived circularly from the new result.

The source `binary.tex` normalization argument was checked explicitly.
At a common kernel, 2D normalized child calls provide the entire 2^(-Df)
factor; the same normalization is supplied across both free endpoints.
Forward/inverse full-converter normalizations cancel around the row table.
Consequently no unpriced f-dependent rational height remains. Replacing
the dyadic source table by the separately audited rational repair does
not change this cancellation.

For s selected bits write floor(s/2) in base A and process its pieces
sequentially. The number of pieces is polynomial m times log k, and the
sum of their active-width rho powers is polynomial m times s^rho. The
leading spectator count is q=2^(k-s)>=2^(k/2) at the source selected-bit
limit s<=c k/log k, for a fixed c and all large k. With depth j<=log_A k,

    W^j <= (m^C)^(log_A k) <= k^{C'}                (OA3)

for an absolute C', since A>=m. Thus padding q to a multiple of W^j
increases it by at most two above an absolute cutoff. This is a quantitative
uniform statement, not a fixed-m O(1) being substituted at growing m.
All complete piece transforms preserve the added spectator rows and they
are removed afterwards.

The one-level recurrence is exactly the source's volume-weighted recurrence,
with polynomial-m nonrecursive coefficient and strict ratio <=1/2.
Geometric summation gives the selected-bit Walsh time

    m^{O(1)} V(1+k)^rho(1+log k)                   (OA4)

plus additive setup. W3 supplies absolute O(k) precision above k>=m^K,
including local intermediate norms and rounding propagation. The numerical
and exact characteristic-two coefficient algebras are never identified.

## 4. Integer shape, short Fourier layers and exact recovery

The integer assembly uses k=Theta(log u), N=2^k and Nk=Theta(u), with
absolute comparison constants above a fixed cutoff. To avoid notation
collision, its radix-2^b_int input digits are distinct from the address
radix b chosen for the interchanger.

The source prime-shape construction, with axes at most 20ceil(log2 k)
bits, is unchanged. Trial division through k^{O(1)} candidates and all
compatibility/shape tests have absolute polynomial degree. Its prime-gap
cutoff U_abs is independent of m and J and remains unspecified; failed
shapes use the source exact fallback. The new small address radix does
not replace or strengthen that separate outer prime-shape assertion.

The balanced CRT tree has O(log k) levels. At each level the controls
occupy at most k/2+O(log k) bits, leaving an absolute positive fraction
free. Each target block has O(log k) bits and its rotation table is
constructible in fixed polynomial k time. OA2 therefore applies without
changing the source CRT map or adding invalid coordinates.

The synchronized short Fourier proof uses blocks of four to seven axes.
Their width and table sizes are fixed polynomial k bounds independent of
m. Its borrowed-coordinate construction is an exact identity on arbitrary
occupied neighboring data. Those borrowed coordinates are restored before
the next batch; they are not zero workspace. Its amplitude-amplification
count and denominators bounded away from zero are absolute. This audit
retains that source theorem rather than claiming a new proof of it.

Each of the O(log k) global layers is a permutation, unit-modulus phase
or selected-bit Walsh layer. The phase tables have additive fixed polynomial
k generation cost at an absolute multiple of k precision. Prefix streaming
writes fewer than 2N products, so full coefficient generation/application
costs O(Nk log k), using the fixed short multiplier. It never scans all
block combinations per coefficient.

Source final allowances are fixed: represented input norm <=2^(13k),
Walsh error <=2^(-50k), phase coefficient/product error <=2^(-70k), and
completed transform error <=2^(-40k). W3 accepts corresponding fixed norm
and error exponents with absolute record-width constants above its polynomial-m
threshold. Thus the same three-transform convolution, sqrt(S) scaling and
nearest-integer recovery proof yields exact coefficients with error <1/2.
The final carry scan and contiguous 2u-bit output are unchanged and linear
in Nk. No approximation remains in the result.

Combining the layers gives the conservative prepared digit-call profile

    time <=m^C u L(u)^rho (1+log2 L(u))^4
             +2^(m^C)L(u)^(m^C),                  (OA5)
    visited cells <=m^C u+2^(m^C)L(u)^C.

Increasing absolute exponents covers descriptor and preparation reuse.
The large terms are additive; per-volume row, address and scalar work is
polynomial m. Absorbing the fourth logarithmic power with the allocated
1/(2J) slack costs only polynomial J<=polynomial m. The additive terms
fit linear time above log2 u>=m^{C'} by B's preparation lemma. Shape and
precision thresholds fit the same guard together with U_abs.

## 5. Fixed machine and visited-space limits

Interchanger calls use one binary coordinate encoding at every depth.
Numerical calls use the one absolute O(k)-bit record format and the source
fixed short-arithmetic processor. A fixed structured dispatcher invokes
compact polynomial-size descriptions directly. It is not an expanded
candidate-specific transition-list interpreter with exponential scan cost.

Walsh main payload descendants shrink by 1/W, finite rational repair by
1/8; grouped exact interchanger calls shrink by at most 2/N_label<=2/3,
and their finite repair by 1/16. Full-volume reserve calls release main
workspace first. Metadata remains paid parent scratch and is stripped
before children. End-access stacks and sibling reuse give polynomial-m
visited volume; descriptors retain the additive setup bound in OA5.
All copies, returns, clearing and phase/coefficient tapes have charged
marked intervals. These are union-of-visited-region bounds.

The digit-call space coefficient is still polynomial in m. The final
uniform O(n) cap therefore needs B's actual chunk wrapper and capped selector;
OA5 alone is not a common-space theorem. Nor does it assert a stronger
exponent than the source fixed-rho caller before that uniform composition.

## 6. Audit conclusion and next gate

No new exponential-in-m proportional cost appears in the unchanged outer
source grammar once I7, W1--W3 and compact dispatch are supplied. The exact
places formerly hiding candidate constants are accounted for above:
controlled guards, column maps/signs, row padding, numerical precision,
finite setup, phase streaming and visited-region reuse. The remaining
whole-theorem check is to bind these interfaces to the same finite parameter
family and apply the common-cap selector without changing any call invoice.

Credits: Jerry Chen (@CubeJerry), the pinned OpenAI outer tape/Fourier
proofs, predecessor finite rational programme, E002 physical/numerical
suppliers, and substantial AI-assisted independent audit.
