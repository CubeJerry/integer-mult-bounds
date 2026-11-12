# Joint endpoint rank gate

Read `PROOF.md` for the general identity and the exact distinction between
no new baseline and an actually supplied Gram baseline. `NOTE-REVIEW.json`
pins the separately authored pivot-piggyback note reviewed here.

```sh
python verify.py --repo /path/to/integer-mult-bounds --output output
```

Expected: `PASS_EXACT_JOINT_Y2_ENDPOINT_GATE no K: 96 with G best:88`.
The checker reads only the two pinned source artifacts, reconstructs the
current hosted map from exact rows, and corroborates every pivot-overlap
value from zero through eight. Its own interpreter is included locally.
No proposed pivot-preconditioned word is generated or admitted here.
