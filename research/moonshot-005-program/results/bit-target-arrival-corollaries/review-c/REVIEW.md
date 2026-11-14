# Independent scope review of the target arrival and sparse-change corollaries

**PASS as stated below. No new kappa.** Root proposed both corollaries; Worker C
checked their mathematical deductions and exact endpoint arithmetic separately.
These are consequences of the reviewed packet cap, actual-history arrival
normalization, uniform fitting-rank gap and deletion-robust fitting theorem.
They do not extend those inputs to other source models.

## 1. Extra ascending facet arrivals throughout the retained target range

Use the retained paired caller and monotone whole-record source model. Let
`q` count persistent Hub-to-zero packet lifetimes and let `a` count positive
facet-arriving MOVEs of additional ascending records. These records are
distinct from the111 original X and111 original Y records already charged
in the baseline. A zero birth at a facet is not a positive arrival; its
eventual local information must still come from actual arriving records.

For `0<=t<=199/200`, concavity/subadditivity gives each original X path cost
at least `7^t`, each original Y path at least `7^t`, and each packet at least
`8^t`, allowing arbitrary unsplit monotone jumps. Every counted additional
arrival has positive integer rank and therefore costs at least1. Thus

    Q_t >= 222*7^t + q*8^t + a.                         (1)

All other operations are still owed. The reviewed complete-caller allowance
is `B_m=B_inf+S/(m-1)` for fixed even `m>=2`, with `S<0` throughout this
interval. Normalize the limiting margin in (1) by `7^t`. The reviewed
derivative argument proves that the normalized margin without `a` increases
for `q<=11`. The new term `-a/7^t` has derivative
`a*7^(-t)*log(7)>=0`, so it preserves this monotonicity. Therefore a negative
endpoint margin excludes the same `(q,a)` at every retained target exponent
`k=1-t>=1/200`, including all finite fixed even multiplicities.

Independent exact interval arithmetic gives the limiting endpoint margins
before subtracting `a`:

| q | Limiting margin at t=199/200 | Largest possible integer a |
|---|---:|---:|
|8|19.4592599784...|19|
|9|11.5420067271...|11|
|10|3.6247534757...|3|

Each interval lies strictly between the displayed integer and its successor.
These bounds are necessary and may be loose at finite m or after other
expenses. Together with the independently proved packet interval `8<=q<=10`,
the actual-history arrival normalization yields

    sum_i ell_i(A) <=111+q+a <=138.

This is below196, the sufficient threshold in the uniform fitting-rank-gap
theorem. Consequently every source in THIS retained target model satisfies

    rank(A) >= ceil(28V/3),   rank(G_x) >= ceil(28V/3).

The conclusion is now uniform across q8/q9/q10 and arbitrary monotone jumps;
it is no longer limited to the former unit-rank q8 invoice. It remains a
necessary source-history condition, not a lower bound for every possible
integer-multiplication architecture or a claim of supplier existence.

## 2. At most nine atomic block-column changes cannot repair an eight-mode code

Let `I` be any at most nine native port indices. Write `E_I` for all row
vectors supported on their complete original-X block columns. Let `M` be
ANY subspace of dimension at most `8V`, with arbitrary operator-valued rows.
Suppose a full native fitting `A` has row space in `M+E_I`.

Delete both rows and columns indexed by I. The remaining principal fitting
has rank at most `dim M<=8V`, because restricting columns kills E_I. But the
independently proved deletion certificate gives

    rank(A_(I complement)) >= (9-|I|/10)V >= (81/10)V >8V.

This contradiction proves the stated code-containment obstruction. No
commutation, scalar replication, special initial packet seeds or dimension
assumption on E_I was used. Algebraically it does not require q=8; q8 is
the intended source application when M is the span of eight whole-V modes.

In particular, adding at most one atomic port-block direction to each of
eight seed modes cannot suffice IF the actual normalized fitting/history
remains contained in M plus those atomic columns. The containment hypothesis
must be verified for the complete history. It does not follow merely from
how initial seeds are written: packet/Y feedback or other local operations
can introduce further historical rows. Such an escaped history lies outside
this theorem's premise and is not excluded by the corollary.

## Evidence and attribution

`check.py` uses only independently reviewed dyadic intervals and fresh
integer-power brackets for8^(199/200). It checks all three exact integer
arrival caps, the ell bound and the d=0,...,9 strict deletion inequalities.
Those finite arithmetic checks accompany the universal deductions above.

Credit Root for the two proposed corollaries; the packet-cap, normalization,
uniform-rank-gap, parity-projector and robust-deletion authors retain their
respective proof credit. Prepared for @CubeJerry with OpenAI assistance.
