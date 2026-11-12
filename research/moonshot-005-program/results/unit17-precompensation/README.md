# Unit17 physical precompensation

WORD.json.gz is the actual partial word. RESULT.json pins its compressed
and decompressed bytes and its observation/matrix dependencies. PROOF.md
specifies the full1880-input/output contract and remaining duties.

```sh
python -B build.py --source /path/final.json.gz --observations /path/OBSERVATIONS.json --joint /path/joint-nonneutral/RESULT.json.gz --matrices /path/UNIT17-PRECORRECTION.json --output /tmp/unit17
python -B validate.py --source /path/final.json.gz --word /tmp/unit17/WORD.json.gz --output /tmp/unit17/VALIDATION.json
```

Expected statuses are PASS_TYPED_1880_INPUT_PRECOMPENSATED_UNIT17_PARTIAL_WORD
and PASS_THREE_SEMANTIC_NEGATIVE_CONTROLS. All1880 formal input coordinates
are independent. Repeating the author checker is not independent review.
The map completes17 second-copy shears and the entire common native, not
the full second copy. No new kappa.
