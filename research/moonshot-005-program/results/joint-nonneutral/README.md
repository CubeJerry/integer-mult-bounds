# Joint prescribed nonneutral-pulse screen

The 58 distinct departure cuts underlying the predecessor's 103 pulse/donor cases have full offhub response rank58. The 30 unit-payload cuts have rank30. The 31 admitted single-pulse historical decoders acquire a joint mismatch of rank30 after their actual gains and chronological feedback are retained. **No new kappa; no global controller or message-count lower bound.**

From this directory, use the pinned source and predecessor files:

```bash
python verify.py --source /path/to/final.json.gz --cases /path/to/itinerary-control-obstruction/CERTIFICATE.json --observations /path/to/active-helper-observation/OBSERVATIONS.json --output RESULT.json.gz
python -O verify.py --source /path/to/final.json.gz --cases /path/to/itinerary-control-obstruction/CERTIFICATE.json --observations /path/to/active-helper-observation/OBSERVATIONS.json --output RESULT-OPTIMIZED.json.gz
```

Expected ranks: all58→58; admitted31→31; unit30→30; admitted-unit17→17; decoder mismatch→30. COPY guard response support is0. The gzip payload records H,L,Z,B,T, every cut, and the exact pivot certificates.

Read `PROOF.md` for the full quantified intervention class, the distinction between independent impulse slots and donor channels, and why a debt rank is not by itself a price lower bound with receiver side information. Preserve independent review separately. The unit17 initial-precorrection continuation is not part of the frozen 58-slot receipt.
