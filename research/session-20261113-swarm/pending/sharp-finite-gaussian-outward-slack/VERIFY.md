# Verification record

Environment: Python standard library only; no third-party packages.

Commands run from this directory:

```sh
python3 -B replay.py
python3 -O -B replay.py
python3 -B verify.py
python3 -O -B verify.py
```

All four commands passed. Both verifier modes produced the same canonical
receipt recorded in `RESULT.json`. The default replay and verifier commands
write no files. The checker uses explicit `require` checks, so optimized mode
does not disable validation.

The checker expands the pinned certificate, enumerates all 3,121 points of
\(S_5\), validates every injection edge using integer arithmetic, enumerates
all error-one output candidates for each of the 1,692 Hall inputs, recomputes
the exact strict-\(\beta\) neighborhood, and checks the signed-permutation
identity. It also exercises certificate-corruption, duplicate-output,
omitted-neighbor, strict-error, and threshold-tie negative controls.
