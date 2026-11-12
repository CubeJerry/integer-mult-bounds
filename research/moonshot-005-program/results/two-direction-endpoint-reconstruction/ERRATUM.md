# Correction to the reconstructed S007 endpoint invoice

The preserved S007 ROOT-ENDPOINT-CANDIDATE.md correctly records 42,480 paid positions, 27,344 targets and rank surplus 1,888. Its written formula is ambiguous and incorrect under its own definitions: it calls C_native the old common-public routes and R_old the old owned routes, but does not subtract the 1,710 original raw-main routes that the replacement also removes.

The reconstruction now takes the literal difference between complete native words:

    P_new = P4 + 18 * (P_candidate - P_common_native - P_raw_main).

Here P_common_native includes all old common-public and owned MOVEs; P_raw_main contains the separate 1,710 raw-main MOVEs. The new candidate contains all 1,880 public routes and 32 owned rank-nine packets.

Equivalently, with C_direct the 1,480 direct common-public routes, C_public the 6,263 old common-public routes, O_old the 47 old owned routes and R_raw the 1,710 old raw-main routes:

    P_new = P4 + 18*(C_direct - C_public - O_old + 400{8} - R_raw + 32{9}).

All sets and histograms are reconstructed from the pinned source. This yields exactly the recorded numerical result. It does not alter the S007 reported numbers; it prevents an erroneous reuse of the incomplete displayed formula.

Per-native MOVE counts: old common native 6,310; old raw main 1,710; replacement 1,912. Thus 152,424 + 18*(1,912 - 6,310 - 1,710) = 42,480.

At t=199/200 the exact remaining paid-moment allowance per native is enclosed by the fractions in output/RESULT.json and is approximately 14.812385620139944. This is the allowance for an incomplete endpoint map. Its 19,968 residual coefficients remain duties, and no new kappa is claimed.

