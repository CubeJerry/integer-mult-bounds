# Joint additive receiver-history obstruction

This author-verified packet is pending independent review. It concerns
all joint q-derived additive controls at the specified220 charts, all
native times, and receiver189's entire native common history. It does
not concern all possible recodings or all difference-carrier controls.

```sh
python research/moonshot-005-program/results/joint-additive-history-obstruction/verify.py \
  --repository . --output /tmp/joint-additive-history.json
```

Expected: `PASS_220_STATION_ADDITIVE_HISTORY_CERTIFICATE`. The verifier
reconstructs1,065 observations of rank1,056, checks a complete basis of
nine identities, and checks their adjoint insensitivity at every source
time. It uses neither the control-space search nor a predecessor verifier.

Source, exact certificate, proof and author receipt are included. No
newκ; no complete source-native positive channel is claimed.
