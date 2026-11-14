# Reproduction and exact scope

Run with Python3 and standard-library rational arithmetic:

```sh
python3 -I -B check.py --native NATIVE --output reproduced.json
python3 -I -B price.py --full FULL-RESULT.json --engine dependencies/interval.py --output reproduced-price.json
```

NATIVE is the pinned `shared-wire-split-composition/data/final.json.gz`.
The full caller and native hashes are checked by the programs and stated in
PROOF.md. The dependency interval.py retains the independently authored
directed200th-root engine from S011, SHA256
`82634fc558ec4eef0bb675b44c2eacb88f2e551d8093262ccbb004b7ef86eff1`.

Expected decoder output: PASS_EXACT_AUGMENTED_DECODER_FREEDOM, coupled Gram
rank7, exact facet kernel census {0:87,1:9}. All96 hosted decoder restrictions
are unchanged by legal zero-aux constraints and their hosted source normals
span their complete rank8 facets. Three negative controls reject.

The monotone104-carrier closed decoder is impossible: every96 final facet
needs an auxiliary visit, whereas eight monotone auxiliary paths can visit
only eight distinct facets. The separate terminal-tour extension has an
explicit proper-chart locality invariant; its additional lower price is176.
Its optimistic complete caller limit is149.83284941086256..., giving strict
deficit26.1671505891374... and necessary terminal-trajectory count22 even
with all first visits free.

**The176 statement is not an unrestricted arbitrary-auxiliary theorem.**
Preterminal nonlocal auxiliary imports can violate the required support
invariant and are an explicit live escape. Nonmonotone original fields,
other-bank dirty relays, more moving trajectories and another preload are
also outside the result. No new supplier or kappa.

MANIFEST.json freezes the author package. Root's independent review belongs
in a separate artifact and is not supplied by repeated execution here.
