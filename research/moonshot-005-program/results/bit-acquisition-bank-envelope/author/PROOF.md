# Exact acquisition-bank envelopes for the six-retention source

**Status:** proved finite native linear-algebra obstruction, with explicit dual certificates. No new kappa, no completed covered-BIT supplier, and no cost lower bound is asserted here.

## Source and retained interface

The source is the actual 27-output word of `six-retentions`, SHA256 `d28b6ae55b9d3c3cab440c24af971babbe7fb2413180ec1cb3d5e2fa4c77bb71`. Its native data is `research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json`, SHA256 `8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`. The literal source, all 222 columns, real-chart containment, source custody, restoration and invoice were separately reviewed by the root and `/root/bit_bridge`. This checker reconstructs the information available at that verified word's seed cut; it does not replace the literal-word verifier.

Write e_j for the raw X_j coordinate and F_i for receiver i's real orthogonal facet. For every receiver, grant all raw e_j whose native line lies in F_i, even if no literal record makes them available. Retain all actual pure-X stationary and ground values visible in F_i. In particular, retain the six first principal-retention values and the **paid Q1, Q3 and Q4 fields at M1**. The second retained fields at the six native lines are replaced by the enlarged banks described below. No field is silently identified with a linear combination of noncontemporaneous histories.

The three h0 ports are L7,L11,L12, below C0; the three h1 ports are L0,L28,L44, below M1. At the cut the actual bank of values cocharted with C0 has binary rank 8 and that cocharted with M1 has rank 11. Include every such value, including all first retentions. This is an optimistic grant: the banks need not have been simultaneously available at an earlier principal visit.

The literal raw visitors comprise 20 originals at C0 and 10 at M1. Grant their separate raw values, not just the combinations actually captured. The enlarged bank ranks are 23 and 16. Exact rational native geometry additionally proves that C0 contains precisely 20 native lines, M1 contains 20, and their union equals these 30 raw visitor indices. Thus the enlarged pair of banks already includes **every native raw coordinate geometrically below either acquisition chart**; taking a previously unused native point below one of these two charts adds no further information to the global version of the envelope.

## Quantified envelope theorem

For every positive whole-record width V and every field of characteristic two, consider the fixed receiver interfaces above. Grant an entire bank to receiver i whenever at least one of its corresponding three port lines lies in F_i. In the global version, grant both banks to every receiver without any delivery or movement cost. Keep the actual other visible stock and all raw geometric locals. The following table gives the exact set sizes for which e_i lies in the resulting linear information span, and the exact closure when any already recoverable raw e_i may subsequently be revealed globally at no cost.

| Bank grant | Initially fitting receivers | Closure under free point feedback |
| --- | ---: | ---: |
| Actual retained banks, six fixed ports | 51 | 51 |
| All raw-visitor enlarged banks, six fixed ports | 51 | 51 |
| All raw-visitor enlarged banks, globally | 54 | 54 |
| Enlarged banks, six fixed ports, plus global e8,e9,e20 | 54 | 54 |
| Enlarged banks, globally, plus global e8,e9,e20 | 57 | 57 |

The full index sets and all dual witnesses are in `output/RESULT.json`. These cardinalities are **optimistic information upper bounds**, not claims that six single-record retained values can simultaneously deliver every listed receiver.

In particular, choosing different locally acquired h rows for the same six transported fields cannot complete all 111 receivers. Even granting all the enlarged banks globally still leaves 57 receiver demands unresolved. Progress beyond this global 54-receiver envelope requires information or access outside the specified fixed interface, for example altered first preloads that transport a new higher-chart source row. Changing a first preload changes the envelope: the old and new values must not both be granted without justification.

## Exact proof and extension of scalars

For each i, the checker constructs the explicit list R_i of allowed binary rows from the pinned literal inventory, exact rational chart containment, the requested bank grant and the raw local rows. Gaussian elimination computes membership of e_i in span(R_i). For every excluded i it constructs lambda_i with

    lambda_i[i] = 1,     dot(lambda_i,r) = 0 for every r in R_i.

Every equation is independently checked over F2. The checker then repeatedly adjoins all recoverable point rows to every receiver. In these five cases the first fitting sets are already fixed points. It constructs another explicit lambda_i annihilating R_i together with all globally revealed point rows for every receiver outside the closure. There are 576 checked dual witnesses across the five initial and closed instances.

The dual is a binary vector, so the same annihilation equations hold in every characteristic-two field. For a positive block width choose any nonzero record z, and change the source by lambda_i tensor z. Every allowed record remains identical, whereas X_i changes by z. This proves nonrecoverability even for arbitrary nonlinear processing of the granted records, not only scalar linear decoders. Conversely, the reported fitting rows have binary linear reconstruction coefficients, which remain valid after scalar extension and tensoring with an identity record map. No inference from sampled field sizes is used.

For feedback, suppose an excluded point were the first newly recovered point outside the recorded closed set. Before that recovery only points in the closed set have been revealed. Its closure dual makes all those revelations and all its allowed records unchanged while changing the demanded point, a contradiction. This statement allows free revelation of **completed raw point values**; it does not grant new arbitrary nonpoint messages or new carrier interactions.

The 111 arbitrary original Y columns of the literal source are independent nuisances. Actual completed Y values do not provide a free raw X value without the nuisance being removed. Our closure generously grants the completed raw X values themselves. For the impossibility proof one may fix all Y inputs to zero; the dual perturbation then changes only the X source. Hence the upper bound cannot be weakened by omitting the nuisance from the optimistic linear information calculation.

## Canonical comparison and scope

The common global code consisting of actual ground values, both enlarged banks and their raw visitors has rank 47. Its intersection with the canonical nine-dimensional code has rank 5. Adjoining the missing four canonical directions therefore gives a **four-direction completion upper bound** in this optimistic information model. It is not a lower bound for arbitrary fitting extensions, and it is not a physically acquired four-record completion. The positive control grants C9 and verifies all 111 fitting identities.

The theorem fixes the existing source preloads and the other retained stock. A new higher-chart capture, a changed first-retention row, a new nonlocal carrier interaction or a new global row outside the banks may escape it. Its fixed-port version also does not exclude changing port geometry. The global-bank version already removes the cost and geometry of delivering the two banks, so relocating only those same bank values cannot overcome that version.

## Reproduction and credit

Run from the repository or scratch root, replacing paths as appropriate:

```bash
python check.py --repo /path/to/programme --word /path/to/six-retentions/output/WORD.json --out /tmp/channel-envelope
```

Expected bank ranks are 8/11 and 23/16; the five fitting/closure counts are 51,51,54,54,57; common rank 47, canonical intersection 5, and 576 dual equations sets pass. The root independently reconstructed all five envelopes and all dual checks from the native geometry and source word. This package was developed by `/root/bit_construction` with independent review by `/root`, in the cumulative @CubeJerry programme, using AI assistance. It incorporates the actual nonlocal retentions developed jointly with `/root/bit_bridge`.
