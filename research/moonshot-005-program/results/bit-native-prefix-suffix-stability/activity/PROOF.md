# Near-optimal return requires at least 3,036 active middle charts

Each proper contact traverses 60 different native middle charts. Eight body holders in eight copies give each section room for 64 fields. These capacities sum to the original 3,840 fields. A wholly disabled section loses all 64 on each of its contacts, even when other chart maps are changed within the same routing and capacities.

The [Clebsch marginal bound](../../bit-native-directed-arc-gap/ADMISSION.md) limits the deficit to 7h/5 on 6,462 contacts. At excess h=128 or 134 they can each lose at most two sections. The eight exceptional contacts have weight zero in our supplied nonnegative cover. Across all proper contacts their total weight is 571,622,576. Every middle chart has incident weight at least 10,000,032. Double-counting bounds the number of fully disabled charts by floor(2 × 571,622,576 / 10,000,032) = 114. Thus 3,036 of 3,150 charts must carry donor information. A chart can meet this condition with its current map. The incidence count does not require that an active chart be modified or that it incur a specific extra cost.

[Root incidence and weights](check.py) · [Independent reconstruction of 106,560 physical holders](../activity-review/REVIEW.md). Credit @CubeJerry and the native atlas and entropy contributors.
