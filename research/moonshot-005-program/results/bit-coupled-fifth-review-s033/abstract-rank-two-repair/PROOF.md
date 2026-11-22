# Rank two is the exact abstract repair threshold

**Proved linear-algebra target for the next interface redesign. No compatible
H word, changed source construction, physical operation count or new exponent
is supplied.**

Let M be the independently checked sixteen-by-sixteen donor-32 off-D map from
the [universal isolation gate](../wave3/ISOLATION-GATE.md). It has rank twelve,
and its four-dimensional kernel has rank-two projections onto each of the
two eight-coordinate blocks. A desired frame C has four columns and both
eight-by-four projections of rank four.

## 1. Universal lower bound

The isolation proof gives rank(MC)>=2 for every such C. If an arbitrary
matrix update Delta satisfies

    (M+Delta) C = 0,

then Delta C=-MC, so

    rank Delta >= rank(Delta C) = rank(MC) >= 2.

Thus rank zero or one cannot repair the gate, even if the four-space is chosen
after the update. This is a universal matrix-rank statement rather than a
failed search over coefficient choices.

## 2. An explicit rank-two construction

Write U=pi48(ker M) and V=pi73(ker M), each of dimension two. Since ker M
has dimension four and is contained in the four-dimensional direct sum
U direct-sum V, equality holds:

    ker M = U direct-sum V.

Choose bases u1,u2 and v1,v2. The two paired vectors (u1,v1),(u2,v2) lie
in ker M and project independently onto both blocks. Extend u1,u2 to four
independent vectors u1,...,u4 in the first eight-space, and do the same for
v1,...,v4 in the second. Let C have columns (ui,vi), and let X be its last
two columns. Both projections of C have rank four.

The first two columns of MC vanish, and the lower bound above forces the
last two to have rank exactly two. Thus Y=MX has rank two. The columns of X
are independent modulo ker M. There exists a two-by-sixteen map L such that

    L ker M = 0,   L X = I2.

The checker constructs L by exact linear extension from the six independent
columns spanning ker M plus im(X). Set

    Delta = -Y L.

Over GF(64), minus and plus agree. Then Delta has rank exactly two, preserves
the entire old kernel, and (M+Delta)X=0. Therefore (M+Delta)C=0.

The new kernel contains ker M plus im(X), of dimension six. The rank-two
perturbation bound also gives rank(M+Delta)>=12-2=10. Hence the new map has
rank exactly ten and kernel dimension exactly six. Each new kernel projection
has dimension four. The repair raises both deficient projections from two
to four while retaining the old kernel pointwise.

`output/CERTIFICATE.json` contains the literal C, X, L, Delta and repaired M.
Their identities and exact ranks are independently replayed from the frozen
gate certificate. This construction is not merely an existence count.

## 3. Negative control and coefficient scope

Keeping only the first rank-one factor of Delta leaves rank-one leakage on
the displayed four-space C. This explicit negative control agrees with the
universal lower bound and distinguishes a partial reduction from a repair.

All identities persist under coefficient-field extensions. For k repeated
copies, the old kernel projections have dimension 2k and a suitable frame has
projection ranks 4k. The same argument gives rank Delta>=2k even when changes
mix copies arbitrarily. Tensoring the displayed construction with Ik attains
rank exactly 2k. This is a linear-algebra statement under the repeated
interface, not a priced native-word realization.

## 4. What this does and does not require physically

The next changed H/interface map must alter this normalized off-D map by rank
at least two to evade the present obstruction, and abstract rank two is
sufficient if all matrix coefficients may be chosen freely. This gives a
sharp target for a proposed redesign.

Rank two is not a count of new messages, moved fields, changed owners, changed
coefficients or paid operations. The displayed update may fail phase legality,
physical H owner constraints, other H/D sections, retained H actions, source
nonsaturation or cost limits. No such compatibility is asserted. Its chosen
four-space also has not been bound to the simultaneously prescribed inverse
D sections of a full construction. Those requirements remain separate.

## Reproduction

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-coupled-fifth-review-s033/abstract-rank-two-repair/check.py \
  --repo . --out /tmp/s033-abstract-rank-two-repair
```

Expected status: `PASS_OPTIMAL_ABSTRACT_RANK_TWO_REPAIR`.

Credit @CubeJerry, the root's isolation-rank observation, the independent
gate certificate and S031/S032 sources. Substantial OpenAI assistance.
Apache-2.0. No new complete kappa.
