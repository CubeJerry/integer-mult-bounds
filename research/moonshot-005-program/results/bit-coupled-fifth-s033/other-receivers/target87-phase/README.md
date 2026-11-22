# Receiver87 exact phase requirement

Receiver87's parent isolation conditions put retained row-block columns27 and31 into the physical two-plane P spanned by columns4 and5. The retained receiver9 and73 output rows each have four early and four late coordinates. Since27 is late, its column has zero early projection. Native section invertibility requires this column to be nonzero; therefore dim of the early projection of P is at most1.

The native donor0 input set is [0,3,4,5,15,19,20,22]: five early and three late inputs. Its three late columns are independent in the four dimensional late output space. If P had zero early projection, columns4 and5 would provide two further independent vectors there, contradicting invertibility. Consequently the early projection of P has rank at least1. Combining the bounds gives exactly1, for each of retained receivers9 and73.

This is a necessary condition under arbitrary common readout rebasing, not an impossibility result. The claim that donor0 has a4/4 input split and forces early rank2 is false. The other native donors containing both4 and5 are61 (six early, two late) and62 (five early, three late); neither repairs that premise.

The literal old profile has early rank2 and therefore cannot satisfy receiver87 isolation while retaining literal readouts and physical phases. Common readout rebasing can change this profile projection. The saved eight by eight permutation example has donor0's actual5/3 input split, output4/4 split, full rank8 and profile early rank1. It demonstrates that the local phase requirement is consistent; it is not a global D matrix, glued row design, all-native section solution, or source construction.

check.py verifies the actual input/output chronology, exact membership of coordinate27 in the previously certified forced input union, old profile ranks, and the local permutation control. SOURCE-PINS.json authenticates inputs. No search, whole fifth receiver, compiler invoice or new kappa is claimed.

```sh
python research/moonshot-005-program/results/bit-coupled-fifth-s033/other-receivers/target87-phase/check.py --repo . --out /tmp/s033-phase87
```

Authorship: @CubeJerry, with substantial OpenAI assistance. Apache-2.0.
