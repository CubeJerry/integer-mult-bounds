# Exact dyadic continuation after the recovered proper-chart relay

**Proved, source-specific continuation obstruction and sharp arithmetic retention bounds. No new κ.** This note supplements the independent review of the two recovered words. It does not contradict their rational full-rank statement or rule out precision-aware division, new correlated records, a changed source, or a general multiplication algorithm.

## 1. Precise continuation proposition

Let R=Z[1/2], and let M be the exact matrix of the terminal 400 public values of either pinned recovered word, in common input coordinates. All owned records have been retired. Consider any subsequent finite linear computation over R, or over R[i], that starts with exactly these values and any fresh zero or independent auxiliary inputs. It may mix coordinates, choose arbitrary charts, discard data, and use arbitrary matrices over the stated coefficient ring. It has no access to a separately retained correlated function of the old inputs. Then this continuation cannot output all 96 original D inputs exactly, for arbitrary old inputs.

The assertion remains valid after tensoring every source field with I_V for every positive integer V. For the 20-output word, any augmented starting state permitting such exact recovery needs at least 2V additional scalar coordinates carrying old-input information. For the 44-output word it needs at least 4V. These are lower bounds on retained information, not movement prices.

### Proof

For each odd prime p, reduction maps R to F_p. The ring R[i] maps to a field K containing F_p and a square root of −1; use F_p when available and F_(p²) otherwise. Thus any proposed exact continuation gives a linear continuation after reduction. A right-kernel vector of the reduced M remains invisible after every linear operation; extending it by zero on independent auxiliary inputs preserves this property. If that kernel vector has a nonzero original D component, exact D recovery is impossible. Field extension from F_p to K does not change the rank of M.

The public X/Y rows have 208 independent original X/Y pivots. The 96 B rows have independent original B pivots. After eliminating these pivots, the remaining matrix is the 96×96 public D coefficient matrix N. For every v in ker(N mod p), extend to the full original-input vector by setting D=v, X=Y=0, and B=−(G_HH−I)v. This is an explicit right-kernel vector for all 400 actual endpoint rows and has nonzero D when v is nonzero.

The independent replay and prime-field elimination give:

| Word | p | rank N mod p | Full public rank | Lost scalar dimensions |
|---|---:|---:|---:|---:|
| 20 restored | 3 | 94 | 398 | 2 |
| 20 restored | 7 | 95 | 399 | 1 |
| 20 restored | 127 | 94 | 398 | 2 |
| 44 restored | 3 | 95 | 399 | 1 |
| 44 restored | 5 | 92 | 396 | 4 |

`RESULT.json` stores explicit full 400-input kernel bases and the D pivot columns; the checker evaluates every kernel vector against every actual endpoint row. Under tensoring by I_V, the corresponding kernel dimensions multiply by V. Each added scalar coordinate can remove at most one kernel dimension. This proves the continuation obstruction and the stated lower bounds. ∎

The existing physical chart interpreter is explicitly Gaussian dyadic: its rank-one C gate uses coefficients (1±i)/2, and its other generators are signed coordinate permutations and powers of i. Those maps are covered by R[i]. This observation does not assert that every conceivable future supplier is restricted to that ring.

## 2. The rational construction remains valid

After restoring D_T and permuting the complement cycle, the un-restored D block is −I+G_SS. Sylvester's determinant identity reduces its determinant, up to sign, to det(I_8−g_S^T g_S). Exact rational elimination gives

- 20 outputs: 24,387,048 = 2³·3³·7·127²;
- 44 outputs: 480,000 = 2⁸·3·5⁴.

Both are nonzero. Consequently the public map has rank 400 over Q. The recovered proof's statement that all input directions survive is correct over Q. It must not be promoted to dyadic continuation or to a physical full source: the determinants are not units of R.

The distinction is operational. Rational inversion could introduce odd denominators; a future precision theorem might permit them at an explicitly justified cost. This note makes no claim about rounded computation or such a replacement. The source as currently frozen provides neither that continuation nor its accounting.

## 3. The missing eighth real mode and its exact retirement

Let rho_* = rho(448), and set w_h=<rho_h,rho_*>/18 on the 96 hosted ports. Every target restored by either word is orthogonal to rho_*, as are all eight coupled ports. The native tight-frame identity gives

G_HH w = 13w,     (G_HH−I)w = 12w.

The seven relay modes are the Gram rows of M={19,30,38,40,47,52,60}. They annihilate w. The eighth coupled row indexed17 is redundant:

rho17−rho19−rho38+rho40=0.

It therefore cannot supply the missing direction. In the original orthogonal omitted frame Z=(7,25,42,52,76,82,97,127), with q_i indexed from zero, the missing mode is

q_* = −(q_0+q_1+q_2+q_3)/2.

The eight coefficient rows consisting of the seven bank modes plus q_* have determinant −1/8. Replacing q_* by the single raw mode q_1 gives determinant 1/16. Both are units of R. Thus the missing direction is precisely an eighth real Gram mode, not a missing copy of r17.

At the completed ground-preload step947 all eight q_i and all seven bank modes are live, and the whole current state has rank400 modulo3. The words then clear q_0,q_1,q_2,q_3 in that order. The independent literal replay finds rank400 at completed steps947–950, then rank399 at completed step951 immediately after opcode950 clears q_3. The other four q_i and all seven bank modes are still live. Rank stays399 through completed step955, when the last q_i has retired. This locates a concrete irreversible loss for the stated coefficient ring, before the physical relay begins.

Appending all eight original q_i to the terminal D rows repairs every odd-prime defect in the table. Appending only the seven bank rows repairs the defects at7,127 or5 but leaves rank95 modulo3 in either word. The computations verify both claims from the actual original-D coefficient rows.

## 4. Sharp arithmetic retention controls

The lower bounds 2 and4 are sharp for **global scalar row-module recoverability** of the particular terminal public maps:

| Word | Additional retained scalar rows | Rank after adjoining, at every odd determinant factor |
|---|---|---|
| 20 | q_1, q_4 | 96 at3,7,127 |
| 44 | q_4+q_1, q_5, q_6, q_7 | 96 at3,5 |

These q_i are the eight genuine original-D Gram values acquired by the source, not hypothetical functions granted as free inputs. The checker explicitly constructs their coefficient rows and verifies the displayed ranks. This is an arithmetic control, not a modified closed source word.

To justify sufficiency over R, let L be the R-row-module generated by the terminal D rows and the indicated added rows. Since N has nonzero determinant, R^96/L is a finitely generated torsion module whose odd prime divisors must divide det N. The displayed full-rank reductions exclude every such divisor. Since 2 is invertible in R, the quotient vanishes. Thus L=R^96, and an R-linear left inverse exists. The lower bounds in section1 show that fewer rows cannot suffice. Extending that left inverse to R[i] gives the Gaussian conclusion as well.

No physical claim follows solely from this module argument. A real repair must retain the records through their actual lifetimes, supply them at the needed cocharts, restore or retire every additional owner, and account for the associated recursion, precision and movement. A separate worker is constructing public-pivot retention using a native real orthogonal frame disjoint from the target set; it is not incorporated into this frozen review.

## 5. Provenance and classification

The historical author is the earlier Worker B research package at `proper-chart-relay-frozen`, whose exact proof and source pins appear in `REVIEW.md` and `RESULT.json`. The present continuation theorem, literal retirement diagnosis and minimal arithmetic retention controls were developed by the independent adversarial reviewer during the current session, under @CubeJerry's direction with OpenAI assistance. The historical source bytes are unchanged.

Classification: the linear residue-field proposition and row-module sufficiency are proved. The exact ranks, kernel witnesses, determinants and chronology are computationally verified for both pinned finite sources. Their use in the proposition is conditional only on those explicit, independently reproducible finite facts. No completed native source, complete supplier or new multiplication exponent is established.
