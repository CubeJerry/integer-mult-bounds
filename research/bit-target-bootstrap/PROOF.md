# Exact target reachability for the completed ordinary BIT wrapper

**Scoped conditional interface theorem. No new κ.** Target κ★=1/200;
canonical base `e54523517d0f03e58352e647c403a5af3e525a57`; selected #7000/#7001
κ=363005817/100000000000. No new covered supplier is constructed here.

## 1. Quantified source contract and full cost

Fix rational `0<=b<C<1/2`. C is a supplied **covered BIT saving**, after
finite compilation and paid cover loss. b is a **completed ordinary** backend
saving. The latter must accept arbitrary widths and complete chunks, preserve
complete spectators, acquire/restore its internal ROW stock, and meet the
retained radix and fixed-tape contracts. A bare scalar saving is insufficient.

Source: `research/kappa-rebuild/bit/DELAYED-COVER-BRIDGE.md` §8, finite acyclic
replacement in `research/bit-finite-ordinary-bootstrap/PROOF.md` §§2–4,
and the selected application review §3. For fixed rational `0<rho<1`,
`w=ceil(e^rho)`, the complete retained root upper bound is

```
O(K V [e^(1-rho)
       + e^((1-rho)*(1-C)+rho*(1-b))
       + e^rho log(e)]).
```

K is a fresh finite constant containing raw/compiled scalar work, whole-job
routes and normalization, two completed body calls, three bank additions,
parking, initialization/erasure, predecessor constants and high-part exchange.
Full stock is `W(w)^D_stock(e) S_old`, where
`W(w)=B |GL_N(F_q)| q^(N^2(w-1))` and
`D_stock(e)=2+ceil(log_N(max(1,ceil(e/w))))`. High digits are
`O_fixed(w log e)`; their actual coefficient and all primitive fit conditions
determine a fresh threshold. No term is deleted by optimizing rho.

Put `A_rho(b)=(1-rho)C+rho*b`. The strict certificate studied here is

```
b < b' < A_rho(b) < rho < 1-A_rho(b).             (S)
```

The original delayed-cover proof requires the last two strict comparisons;
`C<rho` in later receipts is a convenient sufficient choice. Under (S), all
three powers lie strictly below `1-b'`; the stock logarithm is paid by a
positive gap. Freeze constants/thresholds before varying e; use the completed
predecessor below threshold. Backend calls decrease a fixed stage index and
coarse calls decrease atom count. Finitely many stages give finitely many
algorithms, with no cyclic oracle or input-dependent number of tapes.

Necessity below concerns certification by this **strict three-term cost
interface**, not lower bounds for all algorithms or a different cost law.
Changed rho requires application of the retained arbitrary-width primitive,
stock and threshold contracts at that rho; no physical validation is supplied
merely by a new exponent. All five foundational assumptions remain.

## 2. Sharp one-stage result

Define `F_C(b)=C/(1+C-b)`.

**Theorem 1.** The supremum of improved b' admitted by (S), over rational
rho, is F_C(b), and it is not attained. Every rational `b<B<F_C(b)` is
admitted by some rational rho.

**Proof.** Write d=C-b>0. The decreasing envelope `A=C-rho*d` crosses rho
at `rho*=C/(1+d)=F_C(b)`. Thus A<rho exactly when rho>rho*, and
`b'<A<F_C(b)`. Conversely choose rational rho in

```
F_C(b) < rho < min((C-B)/(C-b), (1-C)/(1-C+b)).
```

The first upper endpoint exceeds F_C(b) exactly when B<F_C(b). At rho*,
A=rho*<C<1/2, so the stock gap is positive and the second endpoint also
exceeds rho*. These inequalities give `B<A<rho<1-A`. Finally
`F_C(b)-b=(C-b)(1-b)/(1+C-b)>0`. ∎

The weaker ledger `b'<min(rho,A,1-rho)` has the same supremum: left of
rho* its minimum is at most rho*, and right of rho* it is at most A<=rho*.
Thus the ceiling is not an artifact of the stronger separator (S).

For desired `b<B<1/2`, one stage can certify B iff

`C > B(1-b)/(1-B)`,

subject to `b<C<1/2`. Equality supplies no slack.

## 3. Exact optimal finite depth

Let h>=1 be fixed independently of input size. Put s0=b and
`s_j=F_C(s_(j-1))`. Each actual stage can use its own fixed rational rho_j
and positive relaxation but the same supplied C.

**Theorem 2.** The h-stage supremum is s_h. Every rational b<B<s_h is
attainable in at most h improving stages; s_h is not attainable in h stages.
Exactly,

```
y_h=C^h(C-b)/(1-b),     s_h=(C-y_h)/(1-y_h).
```

**Proof.** F_C is increasing, with derivative `C/(1+C-x)^2>0`, so
Theorem 1 gives the strict upper bound inductively. For attainability,
continuity permits a predecessor x<s_(h-1) with B<F_C(x) whenever the
last stage is needed; apply the induction hypothesis and Theorem 1. If
B<s_(h-1), fewer stages suffice. The identity

`(C-F_C(x))/(1-F_C(x))=C(C-x)/(1-x)`

proves the closed form by induction. Denominators are positive since
`b<s_h<C<1/2`. ∎

For `b<B<C`, the exact finite-depth target criterion is

`C^h(C-b)/(1-b) < (C-B)/(1-B)`.                (D)

Equality is rejected. This is a universal theorem about the specified
interface, not extrapolation from finite tests. It optimizes exponent prices;
finite constants and thresholds can be enormous.

**Portfolio corollary.** An acyclic wrapper tree using covered prices
`C_j<=C_max<1/2` and completed seeds at most b<C_max cannot certify a saving
>=C_max. If every improving chain has at most h stages, its price is below
`F_(C_max)^h(b)`. F_C(x) increases in both arguments, and the one-stage
envelope is a convex combination of C and a completed predecessor. Changing
the coupled recurrence or primitive cost law is outside this corollary.

## 4. Exact requirements at κ★=1/200

The selected ordinary backend is `b0=.00385248`, with fixed covered
certificate `C_sel=.0038525298`. No number of wrappers retaining this
C_sel can reach 1/200. Separately, selected `rho=1/250` caps any newly
certified saving below 1/250 even if a stronger covered supplier is assumed.
These statements concern the frozen supplied prices, not an upper bound on
every possible analysis of the raw word or every possible BIT architecture.

One stage from b0 exceeds 1/200 iff

`C>3112961/621875000=.005005766432160804...`.

A hypothetical covered C=.0050001 has one-stage supremum
`250005/50057381=.00499436836...<1/200`, and two-stage supremum
`2502919107381/500576679107381=.00500007134...>1/200`.
Two stages therefore suffice and one cannot under this interface. A
conservative witness even keeps rho>C:

| Stage | Old b | rho | New b' | A-b' |
|---|---:|---:|---:|---:|
|1|.00385248|.0051|.00499424|3569/500000000000|
|2|.00499424|.0051|.00500007|57/500000000000|

All remaining (S) gaps are positive. These are **hypothetical sufficient
supplier inputs**. The covered native construction at C=.0050001 is open.

## 5. Join to the selected outer ledger

Nick Petalas's prior `outer-ledger-kappa-region/PROOF.md` establishes
feasibility of the 54 strict plus four functional rows exactly when

`OLD_BASELINE<κ<min(U,B,1/32)`.

This is credited prior work. U is uniform complex saving and B is completed
ordinary BIT saving. The current selected `interval_gate.py` uses that
explicit family: `b=κ+5g`, `a=κ+4g`, `q=κ+3g`, `epsilon=1-g`,
`beta=1-3g`, `stop=layout=g`, `r0=g/10`, and uniform complex `U=κ+6g`.
It has a constant positive row 11/2 instead of the prior proof's 7/2;
that difference does not affect feasibility.

At κ=1/200, hypothetical complex tested price `κ+7*10^-8`, uniform
`U=κ+6*10^-8`, g=10^-8 and the ordinary witness B=.00500007 pass the
current source's complete outer section. The verifier extracts that source
section and checks all 54+4 rows. This proves only an **arithmetic join**:
no complex moment, tail strictification, compiler, endpoint or physical
admission at those hypothetical prices is supplied. In this architecture,
U>1/200 and B>1/200 are separate required constructions; no historic
`a/(1+a)` loss is imported.

## 6. Retained input-lift guard at the target

The selected source also retains the signed input-lift gain

`H(k)=7^(1-k)+3^(1-k)+5^(1-k)-9^(1-k)-4^(1-k)-2`.

Its old sufficient curvature test fails at k=1/200. The construction is
unchanged, and failure of that sufficient test is not a counterexample to
the gain. For every real `0<k<=51/10000`, we instead prove

`H(k)>(9/100)k>0`.

Indeed H(0)=0, and throughout that interval

```
H'(k) >= 9^(1-51/10000) log 9 + 4^(1-51/10000) log 4
          -7 log 7 -3 log 3 -5 log 5 >9/100.
```

The last strict inequality follows from the explicit rational logarithm
and alternating-exponential remainder bounds in [LIFT-GUARD.md](LIFT-GUARD.md),
which give the full source-bound proof. Integrating proves the claim.
This removes only that sufficient arithmetic guard from a future target
assembly; it provides no covered supplier, complex moment or native endpoint.

## 7. Limits, next questions and credit

The five canonical assumptions remain unchanged: `native_all_columns`,
`owned_erasure`, `compiler`, `precision_tape`, `analytic_recovery`.
The present theorem uses their completed interfaces and proves none of them.
Standard-library Fraction checks corroborate the universal written proof;
source-byte and AST checks bind it to the stated cost and outer contracts.
They are not a whole-supplier cold replay or formal-kernel acceptance.

Open next questions: construct and admit covered BIT C>1/200; produce a
compatible uniform complex U>1/200 with full tail/precision/ownership
admission; and optimize actual constants jointly with the atom exponent.
Each requires a changed construction or full physical proof, not more
iterations on C_sel. The first useful step is a complete changed signed
moment invoice and its arbitrary-input native endpoint.

Finite replacement is Rohan Arun's #185 lineage (#199/#204); delayed covers,
compiler and current source accounting retain zxv, Cinna Davis, Jacob Alan
Sussman, DreamingOfClouds, @CubeJerry and all original notices. Nick Petalas
proved the outer region using zxv's #4359 ledger. Isaac Grannis (@BagMan9),
#768 (`bootstrap-depth-audit`), already proves optimistic finite-depth
envelopes with independently varying levels and an inverse starting-supplier
threshold for the older tied recurrence `a_j=s_j(1-s_j+a_(j-1))`;
`t37-bootstrap-depth-seed60` reuses that method. The finite-depth envelope
method itself is therefore prior. The new result is the decoupled
covered-C/atom-rho stage-optimal frontier `C/(1+C-b)`, its exact Möbius
depth inverse, and the current source-bound 1/200 requirement.
Prepared for @CubeJerry with substantial OpenAI assistance.
Apache-2.0. No independent human or proof-kernel acceptance is represented.
