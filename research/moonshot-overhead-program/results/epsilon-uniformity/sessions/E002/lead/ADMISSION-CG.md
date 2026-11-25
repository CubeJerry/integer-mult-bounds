# Admission: optimal-order covers and their scalar rank failure

Status: **accepted source-specific geometric construction and scoped algebraic
obstruction**. There is no improved unconditional multiplier or tape-runtime
lower bound in this admission.

The complete proof is [overlapping-cover-rank-gap.md](overlapping-cover-rank-gap.md).
For the retained characteristic-two geometry it constructs a deterministic
finite cover with

    log2(1+lambda)=O(d²+dt).

Together with the independently reviewed NC incidence lower bound, this
matches the order of the optimal covering incidence under the explicit
within-side k=0 condition. The construction uses simultaneous separating
cuts, all orientations, and the separately attributed opposite single-pin
component. Covers may overlap; their scalar sums need not equal the target.

At d=Theta((log m)^(1/3)) and the least t satisfying the source rank guard,
its total rectangle count instead obeys

    R/N <= 2^(−log2 m+O((log2 m)^(2/3))) -> 0.

The exact desired off-diagonal coefficient matrix F=P*−I has rank at least
N(1−1/m). Any scalar-weighted sum of the R supplied rectangle matrices,
even with separable row/column weights, has rank at most R. Hence this
particular family cannot supply the required exact pencil identity for
large parameters. Reweighting or duplicating its matrices cannot fix this.
New independent rectangle directions or a different operator representation
remain possible.

## Review binding and finite evidence

Independent review A accepted the full mathematical snapshot
`7229b37ee2e7b5aace2346f89ee97e49d6b99d64e1ab21fd20f7e506f9929b38`.
The reviewer explicitly discloses authorship of the supplied opposite-pin
lemma; the new greedy-cover/rank composition is the lead's separate argument.
The independent review is
[REVIEW-OVERLAPPING-COVER-RANK.md](../review-a/REVIEW-OVERLAPPING-COVER-RANK.md).

Only the opening status was subsequently changed. The admitted proof is
`2728651746db385a3cedd86fa671978a81ac451a58222c1a9172466a1bb10ad6`;
reversing that status change gives the reviewed hash exactly.

The lead's exact checker and the independent isolated replay both passed
seven finite cases and four exact balanced-parameter rank inequalities.
For q=4 and two remaining unequal coordinates, three cut tuples give twelve
rectangles covering all 144 required pairs, while the target matrix has
rank sixteen and is outside their span. For q=8 in one coordinate, six
rectangles cannot span rank eight. A q=4 single-coordinate case fails the
actual matrix-span test even though its rectangle count equals target rank.
The q=2 cases provide successful exact-identity controls. These checks do
not prove the asymptotic statements; the deterministic greedy construction
and rank proof do.

## Relation to prior work and the positive research target

Cover/partition separation and rank bounds are established methods. The
focused primary-source check in
[COVER-PARTITION-LITERATURE.md](../COVER-PARTITION-LITERATURE.md) records
Pinto's biclique work and the separate Boolean/binary rank conventions in
Ghosal--Karrenbauer. This admission makes no priority claim for those methods
or for the general distinction. It concerns the explicit retained matrix
and quantitative construction in the present programme.

The new exact cross-pinned **partition** is different: its unique coverage
retains the scalar identity and modestly improves counts. It keeps the same
optimized asymptotic overhead order. The low-incidence **cover** studied here
reaches a better incidence scale but fails that identity. Future work must
satisfy both algebra and physical delivery, or replace their current roles
by a separately proved construction. Theorem V remains the unconditional
result; RV-I and RV-W remain open local hypotheses.

Credits: @CubeJerry; the pinned OpenAI source and characteristic-two
adaptation; original Route A's NC theorem; reviewer A's opposite-pin
construction; the lead and independent review; substantial ChatGPT
multi-agent assistance. No formal proof, human refereeing, full-machine
execution or physical lower bound is claimed.
