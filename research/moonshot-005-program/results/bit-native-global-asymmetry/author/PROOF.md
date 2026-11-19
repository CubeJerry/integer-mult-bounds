# Global source gluing needs at least 71 asymmetric planes

## Result and retained interface

This strengthens the admitted local odd-witness obstruction into simultaneous
conditions on one global native source atlas. No new supplier, MOVE tariff,
foundational discharge, or kappa is claimed.

Retain the S022 balanced native routes, the 111 original donors, the ordinary
A2-plane quotient emissions, and the tight source cuts. Write
`f_(j,H):G -> Q_(j,H)` for an ordinary additive quotient after a bijective
relabelling, where `dim G=16p`, `dim Q_(j,H)=p`, and `p>0`. Work over any
characteristic-two field for which these maps are linear. In particular the
binary linear maps forced by the admitted deterministic quotient theorem
qualify. Nonlinear downstream functions and bijective quotient labels are
allowed within the retained interface. Singleton emissions are not counted.

An ordinary plane is **asymmetric** when two native donors have different
source kernels `ker f_(j,H)`. An unordered donor-pair flag is asymmetric
when its two kernels differ. These are global source properties, independent
of receiver or decoder basis.

**Theorem.** Every complete source in this exact quotient interface has:

1. At least **71 distinct asymmetric ordinary planes**.
2. At least **152 distinct asymmetric unordered donor-pair flags**.
3. With `delta_(H,j,k)=rank([f_(j,H);f_(k,H)])-p`,

   `sum delta >= (134487693944/937265625) p > 143.48941256 p`,

   summing over all 2,870 ordinary unordered donor-pair flags. At p=360
   this integer sum is at least **51,657**. Binary expansion and body
   multiplicity scale p; this normalization must not be discarded.
4. At receiver 80, let q count relevant visible planes with an asymmetric
   pair among its tight donors, and t count planes with three tight donors
   whose kernels are pairwise different. Then `2q+t>=68`. Hence `q>=23`,
   and q=23 requires t>=22. At least 52 distinct unequal tight-donor pairs
   occur at that receiver.

A repair of at most 70 common-kernel planes therefore cannot solve global
gluing in this model. In particular one 17-plane simplex patch cannot meet
all constraints at receiver80. This does not contradict the sharp abstract
17-term family for one individual odd witness.

## 1. Receiver-independent discrepancy rank

The admitted source saturation theorem supplies this interface. At a tight
receiver i, donor j's sixteen visible quotients jointly give coordinates on
G. Fixing the other fifteen coordinates gives a p-dimensional fibre
`L_(i,H)`. Saturation forces the same actual fibre for any two tight donors
j,k in H. The inverse-coordinate projections `E_(i,j,H)` have this image,
kernel `K_(j,H)=ker f_(j,H)`, and sum to I over a donor's sixteen planes.

For projections E,F onto the same p-dimensional image L, with kernels K,K',

`ker(E-F)=L direct_sum (K intersect K')`.

Indeed Ex=Fx=l implies x-l lies in both kernels; the converse and directness
follow because both maps are identity on L. Consequently

`rank(E-F)=dim G-p-dim(K intersect K')=rank([f;f'])-p`.

This depends only on the fixed source kernels, not receiver i or its common
fibre. It is between zero and p, and vanishes exactly when K=K'. Moreover
`N=E+F` is square-zero: `EF=F`, `FE=E`, and the characteristic is two.
The common-image premise is essential.

## 2. Every odd witness constrains the same source

An odd witness at i is an odd set S of tight donors such that every visible
A2 plane meets S in zero or two donors. Let P_w be its paired planes with
their unique donor pairs, and let `m_w=|P_w|`. Summing the source projection
identities gives `I_G=sum_(P_w) N_(i,H,j,k)`.

Write `R_w=sum rank N` and `r_w=max rank N`. Removing any N leaves I+N,
which is invertible. Thus `R_w>=16p+r_w`. In particular at least seventeen
terms are nonzero. Let a_H and a_(H,j,k) be the respective global zero-one
asymmetry indicators. Every witness gives

`sum_(H in P_w) a_H>=17`,

`sum_((H,j,k) in P_w) a_(H,j,k)>=17`.

Since `r_w>=R_w/m_w`, it also gives

`sum_((H,j,k) in P_w) delta_(H,j,k)>=16p*m_w/(m_w-1)`.

Adding these without controlling overlap would overcount source flags. The
following integer weights bound every flag's total load.

## 3. Complete finite native census

The checker reconstructs foreign neighborhoods by integer signed-root dot
products and tight donors by their actual singleton exposure. For each i,
form the binary incidence vectors of visible planes restricted to tight
donors. Odd witnesses are exactly odd-weight vectors in the orthogonal
complement of their span. Binary elimination and enumeration of this finite
nullspace gives **421 witnesses at87 receivers**, with the following counts:

| Odd witnesses at a receiver | 0 | 1 | 2 | 4 | 8 | 16 | 32 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Receivers | 24 | 7 | 27 | 32 | 15 | 5 | 1 |

Every witness has216 or280 paired planes. Each is directly checked against
the source geometry and all sixteen ordinary planes of each selected donor.
The predecessor package retained one witness at each of87 receivers. Its
universal projection proof applies to this complete census as well.

## 4. Exact global dual certificates

PLANE-DUAL.json assigns a nonnegative integer lambda_w to each deterministically
ordered witness, with denominator D=1,000,000. The checker verifies
`sum_(w containing H) lambda_w<=D` for every plane. Hence

`D*sum_H a_H>=17*sum_w lambda_w=70,414,816`.

The integer count exceeds70, proving71. The maximum plane load is999,987.

PAIR-DUAL.json gives separate weights mu_w with the same denominator and
every unordered donor-pair flag's total load at most D. Their sum is8,928,332,
so `D*sum a_(H,j,k)>=151,781,644`, proving152. Maximum pair load is999,993.

The pair weights also give, by nonnegativity of each delta,

`sum delta >= p/D * sum_w mu_w*16*m_w/(m_w-1)
           = (134487693944/937265625) p`.

The checker evaluates this using exact rational arithmetic. An LP discovered
the weights, but no optimizer or floating tolerance is in the verification
path. Feasible duals prove lower bounds; optimality is not asserted.

## 5. A smaller native obstruction at receiver80

Receiver80 has62 tight donors and a six-dimensional nullspace, with32 odd
witnesses. Exactly320 relevant visible planes have three tight donors; each
of their three unordered pairs appears in eight witnesses. Another16 planes
have two tight donors, and their pair appears in sixteen witnesses.

Equality of kernels is an equivalence relation. At a three-donor plane there
are zero, two, or three unequal pairs, contributing respectively0,16,24 to
the sum of the32 witness discrepancy counts. A two-tight-donor plane contributes
0 or16. Thus this total is `16q+8t`. It is at least `32*17=544`, giving
`2q+t>=68`. Since t<=q, q>=23, and q=23 forces t>=22.

For e unequal pair flags, at most16 can have weight16; the others have weight8.
Their total load is at most `8e+128`. The required544 forces e>=52. This grants
all16 heavier pairs without asserting they are jointly realizable.

## Verification, limitations, and next question

Run `python3 -B author/check.py --repo REPOSITORY --out OUTPUT`. It authenticates
the native roots, layout, and balanced factor; reconstructs all421 witnesses;
checks both integer duals; evaluates the rank bound; and checks receiver80.
Small exact projection examples exercise the receiver-independent rank identity.
Negative controls reject an invalid odd witness, overloaded dual, and a false
common-image claim.

This is a necessary condition on the original exact saturated quotient model.
An extra information channel can relax saturation. These conclusions are NOT
transferred to the proposed low-global-rank repair-channel interface without a
separate proof. No source-asymmetry count is interpreted as a MOVE tariff.

Next construct donor-dependent quotient systems satisfying these simultaneous
conditions and the existing early-source rank criterion, then realize their
local and downstream maps. Feasible plane indicators alone are not a source.
Both strict suppliers, the full caller, and all foundations remain open.

Credit @CubeJerry, the native/balanced source authors, and the S023 quotient and
plane-asymmetry packages. This extension uses substantial OpenAI assistance and
programme baseline d8544284cbd0527cd03a0aad576a2d2c6eddcc0e. Independent review is
recorded separately; no formal-kernel or human review is asserted here.
