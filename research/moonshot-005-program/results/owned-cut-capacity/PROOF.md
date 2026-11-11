# Exact information requirements for a shared owned bank at a selected cut

**Proved source-bound linear interface theorem. No new kappa.** This is a
continuation of the H4 shared-core proposal. It distinguishes reconstructing
the old owned fields from preserving enough information for the complete
invertible native endpoint. It constructs no H4 word or physical compression
circuit and changes none of the five global assumptions.

The source is canonical `e54523517d0f03e58352e647c403a5af3e525a57`,
`research/shared-wire-split-composition/data/final.json.gz`, SHA-256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
The cut is immediately **before event 36961**, after event 36960's ADD to
owned role 1529. This timing matters. The next event is its paid MOVE from
frame 541 to 543. There are 400 main inputs, 1080 arbitrary helper inputs,
42 currently live owned fields, and 43 peak live owned fields in the source.
The source has 51 allocated owned labels, not 43 total labels.

## 1. The general rank interface

Work over Q or C. A complete normalized array has dimension V, with V any
positive integer allowed by the inherited source. Current chart operators
on each complete array are invertible; they do not change information rank.
All ranks below concern scalar coefficient matrices tensored with I_V.

Write the normalized public and owned states of one source prefix as

    main = M x + N h,
    helper = C x + D h,
    owned = A x + B h,

where x has m independent main arrays, h has h0 arbitrary helper arrays, and
owned arrays started at zero. Set P = [[M,N],[C,D]], G=[A,B].

For any linear observation E z and desired outputs J z, the smallest number
of additional complete-array linear observations permitting exact recovery
of J z is

    d = rank([E;J]) - rank(E).

Necessity: an encoder with q complete fields increases rank by at most qV;
the desired kernel containment ker([E;encoder]) subset ker(J) requires the
displayed rank increase. Sufficiency in the **abstract linear model** follows
by choosing d rows of J whose residue classes form a basis modulo row(E).
The remaining rows then factor linearly through E and those d observations.
This supplies no common-chart circuit, precision bound, source access or cost.

Now take two independent main inputs x1,x2 but the SAME arbitrary helper h.
Retain both current main banks and ONE balanced current helper bank

    (C x1 + D h + C x2 + D h)/2.

The same conclusions hold if the retained helper bank is the first copy's
state instead: use x1 and x2-x1 in place of the mean and difference below.
For the balanced form, set x+=(x1+x2)/2 and x-=(x1-x2)/2. Invertible input
and output changes identify the retained public observation with

    P (x+,h)  direct-sum  M x-.

It therefore has rank rank(P)+rank(M). Adding both owned banks similarly has
rank rank([P;G])+rank([M;A]). Thus the exact additional information required
to reconstruct just the two old owned banks is

    d_owned = rank([P;G])+rank([M;A])-rank(P)-rank(M).

For an invertible native endpoint on all 2m+h0 entering arrays, preservation
of the whole input instead requires

    d_full = 2m+h0-rank(P)-rank(M).

Any q<d_full complete fields, with no additional data-bearing state or source
rereads, leave a nonzero input direction unobservable. No subsequent linear
computation can turn that state into the prescribed invertible endpoint.
This argument allows arbitrary linear encoding and arbitrary linear future
computation; it does not depend on reproducing each old internal owned field.
Nonlinear packing, access to additional input copies, or a changed prefix
observation contract is outside the claim.

## 2. Exact ranks of the pinned source

At the stated cut the verified ranks over Q are:

| Matrix | Rank | Upper and lower evidence |
|---|---:|---|
| P, all current public fields | 1479 | Modular elimination rank1479 and one exact nonzero left-nullvector |
| [P;G], public plus owned | 1480 | The unique public input-nullmode has nonzero owned1503 response |
| M, current mains on main inputs | 338 | Modular rank338 and62 independent exact rational input-nullvectors |
| [M;A], mains plus owned on main inputs | 344 | Owned response on that62-dimensional kernel has exact rank6 |
| G, owned on all inputs | 26 | Exact rational reverse-prefix rows and elimination |
| A, owned on main inputs | 21 | Exact rational restriction and elimination |

Reduction modulo prime1000003 gives lower bounds only. Every claimed exact
upper bound has the separate rational evidence in the table. All source
coefficients have invertible denominators modulo that prime. A full-row
equality over Q, not a modular coincidence, verifies each stored nullvector.

The exact public dependence is

    p768 -4p60 -4p151 -2p246 -2p623 -p625
         +2p626 +4p628 +4p629 +4p630 = 0.

Its exact lost input mode is

    z = -e130/2 +e214/2 -e627 +e629/2 +e732/4 +e768.

The full source prefix sends z to zero on every public field and to 1 on
owned1503, with every other current owned coordinate zero. It therefore
restores the single missing rank. Exact reverse replay verifies the public
dependence; exact forward replay verifies the lost mode.

The certificate contains62 independent rational main-input nullvectors.
Their designated free coordinates form an identity matrix, so independence
does not depend on a numerical tolerance. Exact forward source execution
kills every current main coordinate. The owned responses have rank6, with
independent rows at owners1480,1481,1484,1505,1507,1509. The response of1503
on this main-only kernel is zero.

## 3. What one shared helper bank can and cannot preserve

There are1880 independent entering arrays in the two-main/shared-helper
experiment. The retained two main banks plus one balanced helper bank have
rank1817. Therefore:

| Recovery requirement | Additional complete fields in the abstract linear model |
|---|---:|
| Both old owned banks only | 7 |
| Complete input / an invertible native endpoint | 63 |

For owned recovery, seven explicit observation choices are one copy's
owned1503 and the six differences between corresponding owned states at
1480,1481,1484,1505,1507,1509. The copies of each corresponding role have the
same current frame, so forming those six differences itself is an ordinary
cochart scalar operation. This does **not** implement the remaining decoder,
whose mixed-frame accesses, coefficients, inverses and restoration are unbuilt.

Seven is insufficient for a full continuation:56 additional directions are
still missing. They reside in the discarded helper-difference information,
not in the six-dimensional old-owned response. A prefix-averaging scheme
with the old43-field peak loses at least20 complete-array input directions;
even granting all51 allocated source owned labels leaves a deficit12.

This is a sharp **information-capacity** obstruction for the stated prefix
contract, not a Gaussian-price lower bound. Twenty extra fields do NOT imply
twenty extra paid jobs. Coframed parked snapshots might add only scalar and
storage work initially; later transport, reinjection, lifetime and erasure
must be counted. Allowing63 or more fields can remove the dimension objection
without providing a cheap or correct physical shared core.

Giving TWO current helper banks is a different contract. Its public rank is
rank(P)+rank(P restricted to main columns)=1479+400=1879; just one extra
field then suffices abstractly. The second helper bank is not present in H4
and may not be silently granted. Shared entering helper values do not make
their two current states equal after different main inputs have been read.

### Any coding of one helper bank still needs at least62 extra fields

The current main-state map [M,N] has exact rank400: the modular certificate
attains its row-count upper bound. The two frozen main banks together have
rank rank([M,N])+rank(M)=400+338=738. **Any** single1080-field linear helper
bank can add at most1080 to this rank, whether its rows are averaged, chosen
from different copies, or newly coded. It follows that at least

    1880-(738+1080)=62

additional complete fields are necessary for an invertible continuation
while retaining these two main-prefix states. This stronger lower bound
does not assume uniform helper coding. Its deficit is19 at the43-live cap
or11 at the51-label cap. The balanced bank's exact requirement63 has one
additional lost common mode. A future fixed43-field design must change the
main-prefix information or the available field/source contract; choosing
different helper-copy coefficients alone cannot remove the obstruction.
If its all-input main rank stays400, the main-on-main rank must be at least
357, versus the present338. This is an information condition, not a claim
that such an alternative prefix exists or that extra fields imply paid jobs.

## 4. The no-side-information cut and its legitimate escape

If the encoder must represent both original owned banks without any public
side information, their joint rank is rank(G)+rank(A)=26+21=47. Here the
shared helper quotient has dimension5. One convenient basis is

    h623-h768, h607-h770, h728-h1448,
    h723-h1390, h1163-h1397.

With k suitably selected pure helper quotient observations supplied outside
the encoder, the sharp abstract bound is47-min(k,5), down to42. This is not
a contradiction of the seven-field result: the latter retains1880 explicitly
counted public fields, and so has much more side information. Nor does it
grant physical helper rereads for free.

Two quotient observations have simple current cochart realizations:

    h728-h1448 = p728-p1448                    (frame1090),
    h723-h1390 = p723-p1390-p724-p725           (frame243).

The omitted correction p724+p725 in the second expression is essential.
Other useful observations may contain main contributions, use different
frames or require temporal coding. The exploratory direct-observation
search is not a proof that no cheaper delivery exists, and is not needed for
the rank theorem above.

## 5. Next construction and cost obligations

The fixed-prefix averaging route must either retain the63-dimensional
complement, change the main-prefix states as in a temporal code, or provide
additional named source observations. The next useful experiment is to park
the missing difference modes in cochart fields, then prove their actual
delivery and reinjection before the suffix needs them. Every ensuing MOVE,
ordinary operation, owned lifetime, source version and restoration is charged.
No paid rank saving follows from an information-dimension calculation alone.

The certificate gives a concrete63-observation linear interface:62 selected
helper differences plus one copy's owned1503. The62 helper-difference rows
have exact rank62 on ker(M), so they recover all discarded difference modes;
owned1503 recovers the remaining common lost mode. Every selected pair of
corresponding helper fields is cochart at this cut. Given both original
prefix states, extracting these differences into62 zero owned fields uses
62 INITs and124 ordinary ADDs and no additional Gaussian child at the
instant of extraction. Keeping the source fields unchanged is explicit.
The existing1503 field is retained, not recomputed.

This is a local extraction recipe, not a63-field peak-storage implementation.
Both original prefixes must first be produced, the62 destinations coexist
with them during staging, helper averaging/discarding and reconstruction
remain separate, and later reinjection and erasure are unbuilt. The62 exact
current chart labels are pinned in the certificate. Future moves of the
parked fields can be expensive and cannot be omitted from the H4 invoice.
No actual source/tape tariff is assigned to the INIT/ADD/CLEAR work here.

The H4 ideal raw invoice and its13.012927833 per-native owned-saving target
remain separate arithmetic facts. This package supplies neither a price for
the new observations nor a new compiler/supplier admission. Native all-column,
owned erasure, compiler, precision/tape and analytic recovery assumptions all
remain. The source-specific rank facts are finite exact linear certificates;
the linear information theorem holds for every complete array dimension V
under its stated normalized model.

Credit the retained selected native and #7000 shared-wire source authors,
the recovery H4 review, and the source-bound isolated owned-rank theorem.
Rank-nullity and conditional linear compression are elementary linear algebra;
novelty here is the exact source-bound63-versus7 distinction, the sparse lost
mode,62 verified kernel witnesses and the explicitly counted shared-helper
interface. Prepared for @CubeJerry with substantial OpenAI assistance.
