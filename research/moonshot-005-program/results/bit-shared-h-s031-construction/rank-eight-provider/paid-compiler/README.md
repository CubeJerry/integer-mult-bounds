# Literal one-complement compiler and exact movement screen

This is an application of the independently reviewed
`bit-paid-deficient-h-repair` local compiler to the independently reviewed
rank-eight H642 provider. It adds a literal binary word and an exact price
screen. It does not assert that the full bank or late endpoint is built.

The reviewer supplies a10-by10 field matrix T with first nine columns
[P;c], where rank(P)=8 and c selects the first donor input. Starting with
nine real input fields and one owned zero, T produces the nine requested
signals Px and the complement cx. Its inverse restores the nine inputs
and the zero. The complement travels directly from rank2 H to rank8 Hub,
at paid gap6, and is available before canonical formation and the Y phase.
The original input owners are restored and the extra owner is cleared.
This follows the chronology and ownership proof in the retained compiler.

Polynomial-basis expansion gives a60-by60 binary invertible matrix.
The recorded elementary reduction uses1474 ADDs, with each row swap
expanded into three ADDs. Reversing this sequence implements T; the
forward sequence implements its inverse. The checker propagates all54
original symbolic bit variables and six initialized zeros through both
directions, verifying every output, restored input and final zero exactly.

Sixteen copies therefore use47168 replacement ADDs and96 binary INIT,
MOVE and CLEAR operations each. There are16 extra field exports at gap6.
These are gross replacement costs, not a claimed net full-supplier saving.
The general local compiler already supplies the legality proof; this
application does not infer arbitrary-width source existence from the matrix.

At bank3840 and m870, the retained necessary movement screen is

    q + e (6/8)^(199/200) < 34688.0018887478... .

For e=16 it gives the exact strict integer cap q<=34675, leaving115
above the abstract return floor34560. The checker certifies both signs
with outward rational bounds for integer200th roots. If d denotes the
sum of component deficiencies, each separately exported in16 copies,
then at the floor this compiler permits at most d=10 for m870 and d=11
in the limiting screen. These are bounds for separate complement exports;
they do not exclude joint coding of losses under a different proved compiler.
They also do not pay all other changes, construct the return, or establish
either strict supplier.

Run from the repository root:

    OPENBLAS_NUM_THREADS=1 python -I -B research/moonshot-005-program/results/bit-shared-h-s031-construction/rank-eight-provider/paid-compiler/check.py --repo . --out FRESH

Expected receipt:

    PASS_LITERAL_RANK_EIGHT_PAID_COMPILER_AND_PRICE 1474 47168 96 34675

The application reuses the retained independent field and exact-price
primitives. Its own symbolic forward/inverse replay is a new root check;
it is not labelled a second independent implementation. Source pins bind
the literal T, P and the earlier general compiler proof. No new complete
kappa; substantial OpenAI assistance.
