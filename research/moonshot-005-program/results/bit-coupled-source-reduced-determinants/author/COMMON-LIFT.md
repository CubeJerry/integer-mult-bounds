# The fixed nine-spinor common lift cannot realize H263's inverse graphs

Fix the five nine-port classes at actual H263 and the field GF(512) with
polynomial z^9+z^4+1. In each class use V9[p,t]=(p+1)^t, for p,t=0..8.
The three donors are0,61,62. Every one of the33 joint-tight receivers
sees three ports in each class. For one class, let M_(i,j) be its3-by-3
Vandermonde submatrix in donor j's three columns, tensored with I_16.
It is invertible. Put

```
T_i = vstack(M_(i,0)^-1, M_(i,61)^-1, M_(i,62)^-1),
```

where vstack means vertical stacking of the three48-by-48 blocks, so T_i
has144 rows and48 columns.

Suppose the three donor source views are invertible, and their desired
inverse fibres satisfy `U_(i,j,H)=L_i M_(i,j)` at H=263. For the source
quotient maps F_(j,H), the inverse relations require

```
F_(j,H) L_i = M_(i,j)^-1,
F_(j,H') L_i = 0 whenever H' != H is visible to i through j.
```

**Theorem.** There is no realization of these inverse equations with one
linear map `J:F^144 -> F^768` and `L_i=J T_i` for all33 receivers.
This obstruction applies even to arbitrary linear source maps; covariance
or early-phase restrictions are not needed. It is specific to the displayed
native V9 data. General receiver-dependent lifts are not excluded.

## Proof from complete exact scalar spans

For each of the five classes, each donor j and each of its27 other planes
H', the3-column scalar matrices underlying T_i, over receivers i also
seeing H', jointly span F^9. `SPAN-WITNESSES.json` gives nine independent
columns for every one of these405 cases. `check.py` reconstructs each
matrix from actual port visibility, nodes1..9 and exact finite-field
inversion, and verifies rank9. Tensoring with I_16 gives span F^144.

The displayed annihilation equations imply F_(j,H') J T_i=0 for every
relevant i, so the complete span forces F_(j,H') J=0 for each H' other
than H. On the other hand, stack the three F_(j,H) into C. The first
inverse equations give C J T_i=T_i. The same full-span fact yields
C J=I_144, hence J is injective; injectivity was not assumed separately.

Choose any one joint-tight receiver. Its source view for any one of the
three donors is invertible and has16 quotient blocks. Restricted to im J,
the15 blocks away from H vanish, leaving rank at most48 through H. But
im J has dimension144, so the source view is not injective there. This
contradicts the source-view hypothesis and proves the theorem.

The first one-receiver matrix has only scalar rank3. It does not establish
the full-span premise by itself, and is retained as a scope control. Thus
the theorem does not contradict the independently constructed single
H/receiver alignment point.

## Exact remaining kernel-lift problem

For a general candidate, let C stack the three H quotients. The inverse
equations and the same T_i span force C to be surjective. Choose any
right inverse J and a basis map K for its624-dimensional kernel.
Every candidate lift has the form

```
L_i = J T_i + K Z_i,        Z_i:F^48 -> F^624.
```

The remaining equations are exactly

```
F_(j,H') K Z_i = F_(j,H') J T_i
```

for every required donor/plane/receiver incidence. For fixed source maps
these are finite linear systems in each Z_i. Source selection, full foreign
invertibility, covariance and actual early rows remain simultaneous
constraints on the same source coefficients.

The theorem shows that zero corrections do not work. More generally the
corrections cannot all factor as Z_i=Z T_i through one common Z, because
that would replace J by J+KZ and restore the forbidden common-lift form.
No lower bound on a physical repair fee or rank(I+B) is inferred from this.

## Reproduction and scope

```
python check.py --repo /path/to/repository --out /new/output
```

The check supplies405 exact span witnesses,165 scalar inverse graph
matrices, all native/route/partition pins and the separate coupling controls.
The finite field constants are part of the theorem. Other node choices,
different H words, noncommon kernel corrections and changed source/target
interfaces require fresh analysis.

Credit @CubeJerry, the retained native partition authors, S028 Worker A's
nine-port inverse-graph specification and S028 Worker B's source preflight.
Substantial OpenAI assistance. Apache-2.0. No new complete κ.
