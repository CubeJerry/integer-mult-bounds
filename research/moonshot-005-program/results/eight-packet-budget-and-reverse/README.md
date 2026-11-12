# H4-only tariff and reverse-eight macro

```sh
python -B verify.py --source /path/final.json.gz --invoice INVOICE-SOURCE.json --output RESULT.json
python -O -B verify.py --source /path/final.json.gz --invoice INVOICE-SOURCE.json --output RESULT-OPTIMIZED.json
```

Expected status: PASS_H4_ONLY_EXACT_TARIFF_AND_CONDITIONAL_REVERSE_EIGHT.
The output includes exact intervals, paid/target histograms, strict route
ceilings, source hashes and the conditional macro hash. The macro is
regenerated deterministically. INVOICE-SOURCE.json is an exact copied source
artifact whose original SHA256 is checked; it is not a new complete word.
The separate independent prefix review is in the parent directory.
