# Frozen validation and source scope

Source #7481 head `89eaa9d8cae37c1540de98f2d29a3abaabb96a2b` and native
gzip SHA256 `acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9`
are pinned in `verify.py`. The exact retained Clifford compiler and full
17-call signed invoice are independently pinned there. All retained sources
were read-only. Relevant inherited attribution remains in
`reference/pr7481/NOTICE`; this worker package has no source archive copy.

Executed from `/workspace/scratch/19b21bdb3d72`:

```sh
python3 -B worker-a/public-cache-interface/verify.py --out worker-a/public-cache-interface/RECEIPT.json
python3 -B -O worker-a/public-cache-interface/verify.py --out worker-a/public-cache-interface/RECEIPT-O.json
```

Both return `PASS_SCOPED_FIXED_HISTORY_PREPARATION_OBSTRUCTION`; the JSON
receipts compare exactly. They replay all 40710 strict-prefix events on the
constraint-satisfying probe, reject two out-of-scope source mutations, and
check three physical child recipes for both signed tableau and absolute phase.
The verifier uses explicit exceptions, including under `-O`. `CHECKS.json`
records all current code, proof, receipt and operative-contract hashes.

The complete complex moment upper fails at all three requested comparator
points after granting every unpriced ordinary/retag/cache service free. There
is no emitted native word, physical zero-reframe admission, new compiler,
precision or outer invoice, BIT change, or new κ claim. This is a finite
source replay plus a scoped path-tariff proof; it is not a universal lower
bound on changed-history or changed-producer algorithms.
