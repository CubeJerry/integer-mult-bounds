# Independent diagonal-code and actual receiver-95 review

The [literal candidate](../../bit-coupled-fifth-s033/wave3/PENCIL-CANDIDATE.json.gz)
passes independent GF(64) reconstruction:

| Quantity | Exact result |
| --- | ---: |
| Donor contrast rank | 24 |
| Joined donor-image rank | 28 |
| Common response rank on K | 4 |
| Rank of eight actual receiver-95 rows on native inputs | 8 |
| Actual receiver-95 contrast response | 0 |
| Receiver-48/73 native row-space intersection dimension | 2 |
| Native contrast annihilator dimension | 8 |
| Independently checked native-donor/geometric-receiver sections | 132 |
| Independently checked local source systems | 44 |

Both physical phase blocks retain ranks 19 and 16. The candidate therefore
gives an actual common injective receiver-95 readout on the whole forced
four-space, with six independent common rows outside the previously studied
two-receiver intersection. It disproves the proposed universal equality
between that intersection and the contrast annihilator.

The reviewer checks the diagonal-code identities on all 35 physical inputs.
Writing G and H for receivers 48 and 73, Q for actual receiver95, and Delta
for the saved diagonal, the identities are

    H = P G Delta,
    Q = N G (I+Delta^(-1))^(-1).

P and N are invertible and every diagonal entry is different from zero and
one. The frozen four-input profile is independently reconstructed as
Dalpha=diag(53,53,58,58), with
Delta_F=diag(11,11,59,59) and Delta_F(I+Dalpha)=Dalpha.
The source interpolation formula then gives the actual response

    Q B(j) = N G_F Dalpha H0

for every native donor j. The checker verifies this identity directly as
well as through the displayed factorization. Mutating one actual output
coefficient or one transfer diagonal breaks the relevant identity.

This does not establish a fifth whole receiver. The independent physical
proper-record audit finds forced off-D leakage ranks two at donors
0,45,62,100; four at32,35,38,68,69,90; and zero at61. The canonical local
source extension and the valid full source-gauge lift agree exactly on all
sixteen parent off-D rows. The stronger [universal isolation proof](ISOLATION-GATE.md)
now shows that no source/D retuning under the fixed H processing and retained
receiver-48/73 fibre subspaces can complete this receiver-95 continuation.
That theorem covers full 30-row source changes and invertible common D
readout rebasing; it is not merely a failure of this particular extension.

## Reproduction

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-coupled-fifth-review-s033/wave3/check.py \
  --repo . --out /tmp/s033-independent-pencil-review \
  --candidate research/moonshot-005-program/results/bit-coupled-fifth-s033/wave3/PENCIL-CANDIDATE.json.gz \
  --gauges research/moonshot-005-program/results/bit-coupled-fifth-review-s033/wave3/PENCIL-GAUGES.json.gz
```

Expected status: `PASS_INDEPENDENT_PENCIL_ACTUAL95_AND_ISOLATION_REVIEW`.
The checker imports only the reviewer's own finite-field arithmetic; author
matrices and inherited physical labels are pinned data. The full geometric
144-section execution remains the author's separate evidence. Full-source
validity follows from the reviewed gauge theorem; no complete supplier or
physical cost is inferred from these linear identities.

Credit @CubeJerry, the S031/S032 source/H/D and geometry/compiler lineage,
the S033 construction worker and root's source-gauge theorem. Substantial
OpenAI assistance. No new complete kappa. Apache-2.0.
