# A source-authentic relay requires the fused observable U

The correct owned1481 payload has 59 terms. It is not half the three-term entry value of helper151. The local four-port block gives r=(−A−B+M+G)/2 and changes actual main130 to M+A+B. Rewriting with b=(q55−q101)/2 reduces those two outputs to r=(U−b)/2 and M_new=W+b, with U and W explicitly unprovided.

- [PROOF.md](PROOF.md): corrected identities, exact acquisition reduction, all 13 reads, scoped rank control and remaining tasks.
- [SOURCE-ROWS.json](SOURCE-ROWS.json): exact rows, source lifetime and two counterexamples.
- [CONDITIONAL-PREFIX.json](CONDITIONAL-PREFIX.json): typed 15-instruction local four-port prefix producing three charged owned records.
- [verify.py](verify.py), [RESULT.json](RESULT.json), [RESULT-OPTIMIZED.json](RESULT-OPTIMIZED.json): exact reproduction.

Run from the integrated repository root:

```sh
python3 -B research/moonshot-005-program/results/authentic-relay-interface/verify.py \
 --source research/shared-wire-split-composition/data/final.json.gz \
 --output /tmp/authentic-relay-interface.json
```

Expected status: `PASS_EXACT_AUTHENTIC_RELAY_REDUCTION`. The prefix assumes actual A,B,M,G at 541; no oracle is added to a global1880-input word. Inputs, receiver-state continuation and owned retirement remain open. **No new κ.**
