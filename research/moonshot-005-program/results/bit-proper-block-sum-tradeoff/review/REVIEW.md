# Independent review of the proper decoder/payload sum bound

**PASS.** The finite bound and the extension to arbitrary record width are
sound for one paid copy and exactly nine receiver-downset events. Ground
events are allowed. The independent checker uses a separate set-intersection
census and low-pivot elimination; it neither imports nor executes the author's
checker. No formation or movement tariff, or scaling to multiple copies,
follows from this result alone.

## Independent finite certificate

The proper set P is read from the authenticated induced95 full-support
certificate. For each independent selected subset D of P, the checker builds
the proper common kernel by intersecting binary orthogonality sets. The
proper candidates for evaluation at the i-th coordinate unit are the vectors
orthogonal to all selected directions except i and nonorthogonal to i.
This gives the number s(D) of available units and the rank r(D) of the proper
common-kernel vectors without using the author's evaluation-loop code.

The independent results reproduce every histogram and count:

| Selected directions | All subsets checked | Independent subsets | Maximum s+r |
|---:|---:|---:|---:|
| 3 | 2,300 | 2,300 | 7 |
| 4 | 12,650 | 12,545 | 7 |
| 5 | 53,130 | 50,925 | 6 |
| 6 | 177,100 | 154,864 | 5 |

The estimate s+r is exact for each fixed independent D. Any proper opposite
direction in a dual basis must evaluate to zero or a coordinate unit. A
coordinate unit can occur at most once, while the selected zero-evaluation
proper vectors are independent and therefore number at most r. Conversely,
choose one proper representative for each available coordinate unit, any
representative for each missing unit, and a basis of the proper common-kernel
span. Extend the last group to a basis of the whole kernel. Evaluation proves
that the resulting nine vectors are independent. Their dual basis begins
with D. Missing-unit representatives cannot be proper by definition, and
kernel extension vectors cannot be proper after the entire proper kernel
span is included. Thus the completion has exactly s+r proper members.

Every displayed author's completion is independently verified by all 81
binary dot products and both basis ranks. A sharp sum-eleven example is

    decoder: [59,87,367,431,464,236,111,509,372]
    payload: [234,206,367,91,31,199,274,3,40].

The bases are dual. The decoder has four proper members and the payload
has seven. This is an algebraic witness; it is not a complete physical
continuation word.

The table and symmetry exclude every count pair whose sum exceeds eleven.
If the smaller count is at most two, the sum is already at most eleven.
If it is three, four, or five, the larger count is at most seven, seven,
or six. If both counts are at least six, selecting six proper directions on
one side forces the opposite count to be at most five, a contradiction.

## Whole-block extension, including noncommuting gauges

At nine width-V events, the actual fitting factorization has rank 9V.
After choosing a canonical internal coordinate system its factors have

    A_i=U_i (xi_i^T tensor I_V) S,
    C_j=S^-1 (xi_j tensor I_V) U_j^-1,

where all U_i and S are invertible. For an event with proper decoder support,
its V columns lie in one shortening lambda tensor k^V. The event block is
therefore lambda tensor G, with G square and invertible: otherwise these V
columns could not be independent. A proper payload event similarly has a
square invertible factor H in a unique proper direction mu. Here proper
means that the support of the entire record block has real span seven. It
does not mean that selected coordinate lanes individually have that span.

The scalar directions of the proper decoder blocks are independent. A
scalar relation among them, combined with the inverses of their G factors,
would give a nonzero dependence among columns of S. The same argument for
rows of S^-1 proves independence of the proper payload directions. Binary
rank agrees with rank over every characteristic-two extension field.

The inverse product of proper payload event e and decoder event f is

    (mu_e dot lambda_f) H_e G_f = delta_(e,f) I_V.

For distinct events the binary scalar must be zero, since H_e G_f is
invertible. For the same event it must be one. Thus evaluations of proper
payload directions on any selected proper decoder directions are distinct
coordinate units or zero, exactly the finite statement above. Matrix
multiplication order is preserved; no factors are commuted. Exchanging the
two proper direction sets gives the symmetric bound directly, without
requiring a physical operation that transposes the network.

Let p_star count all proper decoder blocks and q all proper payload blocks.
The table proves p_star+q<=11. The equality-destination theorem says every
nonzero-line event has proper decoder support; a ground event may also have
proper support. Hence the physical nonzero-line count p satisfies p<=p_star
and therefore p+q<=11 as asserted.

The equivalent conclusion

    (number of ground events) + (number of full-support payload blocks) >=7

is a sum of two category counts. An event can contribute to both. It does
not assert that at least seven distinct events satisfy one of the conditions,
and it does not separately charge seven formation or delivery payments.

## Scope of the review

For b>1, a width-V event's factor inside a bV-dimensional proper shortening
is rectangular. The invertibility step, and thus the scalar dual-basis
reduction used here, is unavailable. This review grants no scaled eleven-b
or other multi-copy formula. More than nine receiver-downset events also
changes the premise. Payload support is not identified with its formation
location; paid prior descents and recoding remain possible.

The complete sharp sum bound, every listed finite histogram, and all four
completed witnesses pass independent review. The original two-million-subset
discovery census is not used. Source construction, caller accounting and
physical realization of the sharp algebraic witness remain separate duties.

Run `python -B check.py --support ../induced95-rigidity/FULL-SUPPORT-CERTIFICATE.json
--author ../../R/proper-basis-tradeoff --out output` from this directory.
