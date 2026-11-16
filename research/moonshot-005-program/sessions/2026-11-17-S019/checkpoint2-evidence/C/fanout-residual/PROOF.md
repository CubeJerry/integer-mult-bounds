# The ground canonical source still needs new native exposure

**Proved within the stated fixed-source scopes. No complete supplier or new kappa.**
The source is A's independently reviewed common-carrier-six word, SHA256
`f5acfcb454d6d50dfdb7d66acd2c33980e4aed17826afafbb67fbeb2168f58c1`,
at the cut before operation 1502. Native roots have SHA256
`8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`.
The result preserves this six-output construction and identifies what its
105-output continuation must add.

## Exact physical source

Let T={1,3,73,76,77,80} and U={0,...,110}\T. All 111 X originals are raw at
Hub; six completed Y originals are at their final facets; 105 unfinished Ys
are raw at ground. Nine canonical records are actually at ground. Each x_j
also has an owned raw copy at native line L_j. Twenty further pure-X owners
are at the six-output construction's common, cohort or selected-facet charts.

The exact root calculation checks that none of those twenty proper-chart
owners lies below any unfinished F_i. Completed receiver facets are also
incomparable with all unfinished facets. The verifier exhausts every live
field, so there is no omitted source owner. X originals at Hub cannot return
to an unfinished facet by an ascending path.

Let N_i={j:L_j subset F_i} and let C be the binary span of the nine actual
ground records. It has rank nine and contains K_i=e_i+sum_(j in N_i)e_j.
For all 105 unfinished i, exact certificates give

    C intersect span{e_j:j in N_i} = {0};                 (1)
    |support(c) outside N_i| >=18 for c in C\{0,K_i}.    (2)

The verifier enumerates the entire 512-element code from the actual rows,
checks every i, and checks (1) independently by rank. This is a complete
finite certificate for this pinned nine-dimensional source, not sampling or
an asymptotic extrapolation. Its global minimum nonzero code weight is 48.
Binary ranks remain valid over every characteristic-two field and tensor
with I_V at every positive whole-record width.

## Functional indispensability, including nonlinear decoding

Fix i in U and j in N_i. Suppose e_i were in the span of C and all e_k for
k in N_i\{j}. Adding K_i would produce a nonzero codeword supported on N_i,
contradicting (1). Consequently there is a binary difference h such that

    C h=0, h_k=0 for k in N_i\{j}, h_i=h_j=1.             (3)

The verifier independently solves and checks such h for each of the 111
native sites, using receivers {0,2,4,5}; their neighborhoods cover all sites.
The full differences are in output/RESULT.json. Inputs x and x+h give the
same allowed observations and different desired x_i. Adding any fixed
nonzero record vector times h gives the same collision at every field and
width. Fix every arbitrary original Y input equally in the two runs.
No local nonlinear postprocessing can distinguish these observations.

## The no-further-owned-MOVE theorem

Consider a completion from this exact cut with a fixed, input-independent
schedule, arbitrary local nonlinear processing and interactions between
original Ys, ascending originals, and no further owned MOVE. Information
paths are then ascending or stationary. A source affecting F_i must start
below F_i. No proper-chart owner or completed Y of this source is eligible
for an unfinished i. We freely grant the entire ground code and all original
Y inputs when reasoning about distinguishability.

A raw native value can leave L_j only through a visit by an unfinished Y
original. New stationary owners at L_j cannot carry it away. X originals
are already at Hub. A completed Y cannot leave its final facet and later
return. By following local dependencies backwards, the information arriving
at unfinished F_i is a function of C, the arbitrary Ys, and the raw values
of visited native sites in N_i. A visit to a nonorthogonal line cannot
contribute later to F_i through an ascending path.

If some native site is never visited, its collision (3) makes the associated
receiver impossible. Thus all 111 sites must be visited. There are only 105
movable Y originals, and an ascending chain can visit at most one distinct
one-dimensional native line. This is a contradiction.

**No completion with zero further owned MOVE exists for this source, even
allowing arbitrary local nonlinear Y feedback under a fixed schedule.**
The argument allows receivers to assist one another; it counts their total
site capacity rather than requiring each receiver to collect its own inputs.
Uncharged information in data-dependent timing or a global control channel
is outside the model.

## A native-line-only quantitative escape

Now allow descending owners, but require every future owned MOVE to start
at an actual native line. Its only strict destination is ground, with price
one. The payload may have been modified locally; it need not remain raw.
Let k be the number of descents and R their distinct native origins, r=|R|.
Grant every x_j for j in R globally at ground. This optimistic grant covers
every allowed payload: by chronological induction a record leaving L_j is a
function of x_j, C, original Ys and previously granted native values.

If r<=17 and i in U\R, (1)--(2) imply

    C intersect span{e_j:j in N_i union R} = {0}.         (4)

The one exceptional nonzero word K_i is excluded because i is not in R;
every other word needs at least 18 coordinates outside N_i. The resulting
binary rank statement is unchanged over extension fields. Alternatively,
expanding finitely many extension coefficients in an F_2 basis would turn
a support counterexample into a binary support counterexample.

For every j in N_i\R, the same uniqueness and collision proof shows that j
must still be visited. Each native j has at least 49 unfinished orthogonal
receivers, verified exactly. Removing at most 17 receivers in R leaves some
i in U\R demanding j. All 111-r native sites outside R must be visited;
105 Ys imply r>=6 and hence k>=6.

Put t=199/200 and delta=1+6^t-7^t. A Y visiting a native line pays at least
1+6^t, versus its baseline direct price 7^t. Additional splitting cannot
reduce this charge because (a+b)^t<=a^t+b^t. Different visited lines require
different Ys. Thus the extra movement above the complete six-output baseline
is at least

    k+(111-r)delta >=6+105delta.                         (5)

For r<=17 use k>=r>=6 and 0<delta<1. If r>=18, the descents alone already
cost more than this floor. Directed rational certificates give

    delta in [0.014263881249522213140545744812606371,
              0.014263881249522213140545744812606373],
    added moment >=7.497707531199832379757303205323668955.

The source's baseline is approximately 1612.955740704517265865. The necessary
limiting movement allowance then leaves only

    [1.2974319754352570013231559528615886241666666666667,
     1.297431975435257001323155952861589374]

of further room. This is a necessary movement screen, not a sufficient strict
supplier condition. No such six-port decoder is constructed.

Only six or seven native-line descents survive this screen. Eight already
cost at least 8+103delta=9.46917976870078795347..., exceeding the available
8.795139506635089... room. With six ports, all 105 Ys must visit different
sites outside R. With seven ports there must be at least 104 such visits
(or 105 if only six distinct origins are used). Erasure, storage, ADD and
strict-supplier expenses remain additional obligations.

## Scope, controls and reproduction

The no-MOVE theorem permits arbitrary Y feedback. The quantitative extension
additionally restricts every descending owner to a native-line source. A
proper-chart mixed source or a changed earlier acquisition history can avoid
that restriction and is not excluded. The result therefore directs attention
to earlier facet acquisition or new proper-chart delivery mechanisms.

All source fields and 222 columns are independently replayed. The exact
functional collisions are checked; granting the omitted raw native coordinate
destroys its collision and restores local reconstruction. Granting an entire
native antichain makes every output algebraically recoverable. These positive
controls prevent confusing physical inaccessibility with global information
insufficiency. The seven-port lower floor remains below the allowance while
the eight-port floor exceeds it, providing both sides of the exact budget
screen.

```
python -B check_residual.py --repo REPOSITORY \
  --word COMMON_CARRIER_SIX_WORD --out output
```

Use --audit-module when relocating C's independent replay. Expected status:
PASS_SOURCE_SPECIFIC_FANOUT_NATIVE_EXPOSURE_GATE.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit A's
common-carrier-six construction, native and canonical-source predecessors,
and retained source-custody conventions. No foundational assumption, complete
strict supplier or new complete kappa is established here.
