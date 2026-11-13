# Parametric ball-core Hall obstruction

The proposed a=2 Hall-containment pattern cannot be extended to any a>=3
by changing only the deletions from B_(4a^2+3). This is a self-contained
negative structural lemma, not a new global rounding lower bound or PR.

Let Z_a=O^+(a,a,a,a+1) and beta_a=sqrt(4a^2+2a+1)-sqrt(4a^2+3).
No N⊂B_(4a^2+3) has N_beta_a(N∪Z_a)⊂N for a>=3. The exact escape is

(a+1,a,a,a) → (2a,1,1,1) → (a+2,a,a-1,a-1).

Both errors under H4/2 are exactly1. The first step is inward. The second
step is strict-beta_a precisely for a>=3 and leaves the ball. The paired
D4 action forces32 middle-orbit points and96 escaped output points. The
complete added-orbit neighborhood has184 points, derived symbolically.

This rules out the same-core target-containment certificate, even with
arbitrary inside-ball deletions. It does not show that every such input
set fails Hall's inequality against a different target set, nor does it
disprove a global lower bound1/2. The original radius-five result remains
unchanged. See PROOF.md for complete geometry, counts and limits.

```sh
python3 -I -W error -B verify.py
python3 -I -O -W error -B verify.py
```

Expected marker: PASS_PARAMETRIC_HALL_BOUNDARY_OBSTRUCTION. `--write`
regenerates RESULT.json. The checker verifies the affine norm/error
identities as polynomials in a, checks D4 generator conjugations and
corroborates the symbolic orbit counts at a=2..64. It uses only the
standard library, imports no predecessor or current search, and runs no
matching solver. Finite cases support the explicit universal proof.

Exact #6509/#6619 and frozen R5/compact pins are in SOURCES.json. No
current C search constructor or proof was read or shared. No multiplier,+kappa, period, conserved-sum or equivariant-rounder claim is made.
