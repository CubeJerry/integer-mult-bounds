# Chart318 common-dependent swap obstruction

The full receiver189 history response, rather than only its old null relations, factors through final common fields129,150,189,215 for controls at charts16,35,127,318. Restoring those common outputs leaves all original receiver observations unchanged, including under common-dependent replacements, retained donor records and feedback within this station scope.

The independent direction is deliberately left open: new receiver records, different receiver routes, or additional source-control charts require a new analysis. In particular, the direct checker fails when chart901 is silently added.

`SWAP-SCREEN.json` records the24-cut changed-matrix screen: two individually neutral cuts, neither with any receiver response; five nonneutral cuts expose pure q but leave common errors. `FULL-HISTORY-FACTOR.json` records the stronger all-cut factorization. `DIRECT-CHECK.json` verifies its explicit four-endpoint dual by a separate implementation. `PROOF.md` gives the actual detour, record interpretation, identity and scope.

```sh
python3 -B probe.py --source /path/to/native/final.json.gz --output /tmp/swap-screen.json
python3 -B full_history_factor.py --source /path/to/native/final.json.gz --output /tmp/full-factor.json
python3 -B check_full_dual.py --source /path/to/native/final.json.gz \
  --certificate /tmp/full-factor.json --output /tmp/full-dual-check.json
```

All checks use exact rational arithmetic and remain active under `python3 -O`. This is source-authored evidence pending independent review, not a new complete multiplication bound. Prepared with OpenAI assistance.
