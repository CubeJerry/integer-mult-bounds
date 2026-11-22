# Independent full-tangent and exact local-lift review

Session `2026-11-22-S032`. Both the complete projected D tangent and the saved finite local interpolation lift are accepted. These are separate statements; neither establishes a complete changed source word or fifth whole fibre.

## Independent operator reconstruction

The audit consumes the 44 local systems already independently reconstructed in `bit-source-d-interpolation-s032-independent`. Those systems derive their six-by-six H restrictions from raw owners and physical H maps, and their constraint spaces from native retained H fibres. No new author executable is imported.

For a retained section \(C_{jr}=T[O_r,I_j]\), the required quotient image is \(M_{jhr}C_{jr}^{-1}\). Over the dual numbers \(\mathbb F_{64}[\epsilon]/(\epsilon^2)\), its variation under a phase-legal change \(\Delta T\) is

\[
\dot Y_{jhr}=M_{jhr}C_{jr}^{-1}
             \Delta T[O_r,I_j]C_{jr}^{-1}.
\]

The usual minus sign equals plus in characteristic two. Literal native H preservation has zero derivative. Therefore the complete local first-order compatibility conditions are \(\dot Y_{jh}N_{jh}=0\), where \(N_{jh}\) is a basis of the relations among the fixed H generators and four common source frames.

The independent checker builds all coefficients from its own 44 systems. It obtains 1,152 raw scalar equations, of which 944 are nonzero, in 561 retained-section-visible D entries. The rank is **88**. The author's saved 473-column basis has rank 473 and is annihilated by this independent operator. Stacking the independent and author operators still has rank 88, confirming identical row spaces despite independent H bases.

| Space | Dimension over GF64 |
|---|---:|
| All phase-legal D entries | 921 |
| Entries visible in retained sections | 561 |
| Entries invisible in every retained section | 360 |
| Compatible visible D tangent | 473 |
| Complete compatible D tangent | **833** |

The four parent ingress-to-quotient maps stack to a \(24\times8\) matrix of rank 8 for every native donor and retained receiver. Consequently a nonzero visible section variation changes some required quotient image. This justifies distinguishing the 473 visible compatible directions from the 360 invisible coordinate directions.

The dimension 833 concerns the **D-coordinate projection after eliminating the local source variations**. It is not the dimension of the full joint source/D parameter space, which also includes source-extension freedoms. It is a formal first-order statement; it does not imply that every tangent direction has a finite lift.

## Exact saved finite lift

The first visible basis direction is the single-entry perturbation

\[
\Delta T=E_{00},\qquad T'=T+E_{00}.
\]

The checker verifies the literal saved matrix and all 44 supplied protected source deltas. Using exact inverses of the changed sections, it checks

\[
(F_{jh}+\Delta F_{jh})[C_H,L]
  =[F_{jh}C_H,\;M_{jh6}(C'_{j6})^{-1},\ldots,
                     M_{jh73}(C'_{j73})^{-1}].
\]

Thus all native H values and all four prescribed local D source-frame images are preserved exactly. Twelve source quotients change, belonging to donors 0, 32 and 35. The other 32 local deltas vanish.

The saved candidate additionally has invertible 19/16 D phase blocks and **all 144 geometric D sections** have rank 8. The relative section variations are not all square-zero. Exact finite feasibility is therefore established by direct inversion and all 44 finite equations, not by extrapolating the tangent calculation or applying a nilpotence shortcut.

This positive example does not contradict the previous 128-shear screen: changing one matrix coefficient is a different candidate family from adding one entire output row to another.

## Remaining rank and implementation limits

On the same literal forced four-space \(K\), the checker reconstructs the changed ingress implied by the finite section inverses. Its all-donor contrast rank remains **30**, and its augmented rank remains **32**. The common linear response rank therefore remains **2**. This candidate does not remove the forced-four-space readout deficiency.

The checker does not claim full protected source-view ranks, source nonsaturation, an invertible executable source phase, a changed compiler invoice, or a common fifth whole fibre. The exact finite result concerns the specified protected six-row local interpolation family. Any later source-word admission requires those additional checks. No conclusion about other finite directions follows from this one successful local lift.

## Reproduction

Exact consumed artifacts are bound in `SOURCE-PINS.json`. `output/INDEPENDENT-TANGENT-MATRIX.json.gz` contains the independently assembled operator; `output/RESULT.json` records its rank, complete kernel verification, finite interpolation checks and all-section check.

```sh
python3 -B research/moonshot-005-program/results/bit-source-d-tangent-s032-independent/check.py --out /tmp/s032-tangent-independent
```

Expected status: `PASS_INDEPENDENT_FULL_TANGENT_AND_EXACT_LOCAL_LIFT`. The exact audit takes approximately two seconds in this environment.
