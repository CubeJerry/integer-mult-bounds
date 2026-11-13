# Classify the entire two-dimensional relation space at the cheapest public cache

Working proof for independent review; not yet a published contribution.
Prepared for Jerry Chen / CubeJerry with substantial OpenAI assistance.

## Source, inherited certificates and exact scope

Use the unchanged #7481 word with SHA256
`acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9`.
Write g=e885-e705, h=e1459 and L=span(g,h). Consider exactly the scalar-linear
helper promises whose annihilator R is a subspace of L. Main inputs remain
arbitrary and independent. All other inputs range over the full kernel of R.
Instructions, event clocks, physical coframes and whole MOVE targets stay
fixed. Histories contain only strict earlier original observations.

Two independently checked predecessor facts are used explicitly:

1. Every final coframe observation family is independent over Q:7,780 rows
   across979 coframes, including all6,279 MOVE arrivals. This is the published
   all-history theorem at fork commit
   `fdbb41450a98594bdf1f5fe4535e77d2466adb4f`.
2. For the singleton promise h=0, the only newly history-reconstructible MOVE
   is event52236, a public rank-one MOVE on763 from189 to127. No MOVE is zero.
   This is one case of the separately checked six-helper census; its final
   publication pin and portable replay must be added before this proof is
   published. It is not assumed from a numerical moment.

## A support isolation lemma replaces an expensive parameter census

Owner885 has exactly four original touches:

| Event | Instruction |
| --- | --- |
|30780|ADD into885 from943, coefficient1/2, frame3|
|40710|MOVE885 from3 to189|
|40711|ADD into885 from705, coefficient-1/2, frame189|
|41698|ADD into885 from943, coefficient-1/2, frame189|

It is never an ADD/COPY donor. Induction on the source instructions implies
that no other field ever acquires a nonzero e885 coefficient. Thus the only
original history generators containing e885 are its initial row in frame3
and its arrival at40710 in frame189. Frame3 has no MOVE arrivals at all; its
history consists solely of its1,060 original coordinate units. Neither705
nor1459 initially has frame3 (their frames are105 and189).

Consequently, a vector g+lambda*h cannot lie in any final coframe span other
than189: every other frame except3 lacks e885 entirely, and frame3 lacks the
mandatory e705 coefficient. This is uniform over every scalar lambda. It is
not inferred from checking a finite list of parameters.

Exact source replay gives the frame189 rows

    r_initial1459 = h,
    r40708 = e705+e943,
    r40710 = e885+e943.

Therefore

    g+lambda*h = r40710-r40708+lambda*r_initial1459.

The full frame189 family is independent, so this representation is unique.
Its latest nonzero support member is always40710, including lambda=0.

## One-circuit criterion and every one-dimensional promise

Let B be an independent chronological observation family and let a nonzero
relation u belong to span(B). Its unique expression in B is the only new
dependency after quotienting by span(u). A MOVE arrival becomes recoverable
from strict earlier observations exactly when it is the latest nonzero
support member of that expression. A row vanishes individually exactly when
the expression has singleton support. If u is outside the final span, no
prefix changes rank at all.

Apply this to u=g+lambda*h. The sole new cached MOVE is40710, of rank8; no
MOVE is zero. The actual decoder identity under the promise is

    r40710 = r40708-lambda*r_initial1459.

All providers are strictly earlier and in the exact same physical frame189.
There are no exceptional finite lambda values creating another cache. The
remaining projective direction, span(h), is the singleton predecessor case
with only event52236 and rank-one credit.

## The full two-dimensional promise

For any other coframe P, every vector in P intersect L has zero g coefficient,
because g has the isolated e885 coefficient. Thus P intersect L is contained
in span(h); frame3 has zero intersection with L. The only effects outside189
are therefore the already certified effects of h=0, namely event52236.

Inside189, h is an initial generator and g=r40710-r40708. Quotienting by L
kills that initial h generator and makes40710 equal40708. Independence of the
full original family excludes every other new dependency. No MOVE row lies
in L: among the relevant generators only the initial h does. Hence R=L
enables exactly the two nonzero cached MOVEs40710 and52236, of ranks8 and1,
and no zero MOVE. R=0 changes no target. This exhausts every subspace of L.

## Exact original-target funding

The original helper target ranks are R705=R885=8 and R1459=1. Retain only
original coordinate targets, and fully debit every helper not retained. For
surjectivity onto the retained coordinates, a rank-one relation must have at
least one nonzero coefficient on a debited coordinate. For R=L, the two
relation rows must remain independent on the debited columns. This forces
loss of1459 and at least one of705 or885. Extra debits cannot improve the
budget. Write f(r)=r^(1-kappa),0<=kappa<=1, with f(0)=0.

| Annihilator R | Newly cached MOVE events | Least target debit | Optimistic native gain |
| --- | --- | --- | --- |
|0|none|0|0|
|span(g)|40710|f(8)|0|
|span(g+lambda*h),lambda nonzero|40710|f(1)|f(8)-f(1)|
|span(h)|52236|f(1)|0|
|L|40710,52236|f(8)+f(1)|0|

These are information-relaxation prices with free correlated initialization,
history backing, ordinary processing and zero reframing. They are not
physical savings or an assembled exponent. In particular the positive line
cannot be dismissed merely by deleting1459's final target credit: the exact
cache decoder uses1459's initial value.

## Conditional preparation conclusion

Add the explicit access contract that retained original885 and705 are given
at their original entrances while the correlated demoted1459 value is not a
free input resource and must be constructed or separately charged. Freeze
the original producer histories and require new whole-field dependency
transport to use paid nested native MOVEs. For lambda nonzero the probe

    x885=1, x705=0, x1459=-1/lambda, all other inputs zero

satisfies the relation. After excluding the demoted initial slot, the only
available nonzero dependence before40710 is in885 at empty frame3. It must
reach dimension-eight frame189. Every such new path has total integer rank
at least8, hence price at least f(8) by increasing subadditivity. The
cheapest-target line then has net gain at most-f(1). Choosing an expensive
pivot705 or885 instead already loses at least f(8), so its information
budget is at mostzero even before preparation. All other rows of the table
also have nonpositive gain before preparation.

Thus no scalar subspace of this particular L improves the native moment
under that additional access/transport contract. The unchanged17-call
comparison cannot reach.0038 from this modification. This is not an
unconditional preparation lower bound, and does not rule out supplied
correlated inputs, changed producers, other helper relations, cross-call
encodings, ordinary alternative frame algorithms or newly priced target
interfaces. Public zero-reframing still needs its own admitted contract.

## Verification and limitations

The stopped general intersection-census attempt is retained as an unfinished
checkpoint; it is not counted as evidence. The proof above instead reduces
the infinite family to exact donor isolation, the absence of frame3
arrivals, three source rows, original-family independence and the separately
verified singleton h result. A portable verifier must check those precise
dependencies and fail on an added885 donor, an unaccounted frame3 arrival,
a wrong row sign or an omitted/latest circuit member.

This proves a scoped source-bound relation classification and conditional
budget obstruction. It removes no global foundational assumption and gives
no new kappa. Prior source, all-history, singleton-zero, public-price and
preparation results retain their authorship and exact dependency pins.
