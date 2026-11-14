# Reproduction and dependency pins

Run from an arbitrary working directory using absolute paths assigned below.
Python3.12.14 and NumPy2.3.5 were used. Source hashes are enforced. A regenerated
gzip stream may differ across Python/zlib versions; compare the documented
canonical decompressed payload SHA256 as well as all proof-relevant fields.

Set `PKG` to this package, `REPO` to a checkout containing the pinned native
source, and `PROGRAMME` to the permanent programme checkout. `OUT` must be a
fresh scratch directory. Do not regenerate into frozen evidence directories.

```bash
PKG=/absolute/path/to/transient-recoding-frozen
REPO=/absolute/path/to/integer-mult-bounds
PROGRAMME=/absolute/path/to/permanent-programme-checkout
OUT=/absolute/path/to/fresh-scratch-directory
NATIVE="$REPO/research/shared-wire-split-composition/data/final.json.gz"
PARENT="$PROGRAMME/research/moonshot-005-program/results/complex-compensated-ferries/general/author/source-evidence/rail-consumer.json.gz"
FULL="$REPO/research/shared-wire-split-composition/FULL-RESULT.json"

python3 -I -B "$PKG/balance.py" --native "$NATIVE" --parent "$PARENT" --engine "$PKG/dependencies/replay.py" --output "$OUT/balanced"
python3 -I -B "$PKG/build.py" --native "$NATIVE" --parent "$PARENT" --engine "$PKG/dependencies/replay.py" --output "$OUT/output"
python3 -I -B "$PKG/build.py" --native "$NATIVE" --parent "$PARENT" --engine "$PKG/dependencies/replay.py" --balanced-module "$PKG/balance.py" --output "$OUT/balanced-output"
python3 -I -B "$PKG/check_phases.py" --engines "$PKG/dependencies" --parent "$PARENT" --word "$OUT/output/WORD.json.gz" --output "$OUT/output/PHASES.json"
python3 -I -B "$PKG/check_phases.py" --engines "$PKG/dependencies" --parent "$PARENT" --word "$OUT/balanced-output/WORD.json.gz" --output "$OUT/balanced-output/PHASES.json"
python3 -I -B "$PKG/price.py" --full "$FULL" --interval-engine "$PKG/dependencies/interval.py" --parent-codec "$OUT/output/RESULT.json" --balanced "$OUT/balanced/RESULT.json" --balanced-codec "$OUT/balanced-output/RESULT.json" --output "$OUT/PRICE.json"
```

Expected results:

| Word | Forward debt | Reverse residual rank | Instructions | Owned peak |
|---|---:|---:|---:|---:|
| Retained stripped parent |4920|82|4779|29|
| Parent plus transient codec |4880|83|4917|31|
| Reciprocal-aligned alternative |4928|88|4676|29|
| Aligned alternative plus codec |4888|89|4814|31|

Each codec has five rejected source mutants; each phase run checks25 new maps
and rejects a wrong global phase. The alignment has two rejected invariant
mutants. Its72 deleted actual D reads and six deleted old repair packets are
explicitly listed. All source identities use all400 independent coordinates.

Frozen source inputs:

| Input | SHA256 |
|---|---|
| Native geometry/source |`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`|
| Compensated parent |`a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc`|
| Full caller |`d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7`|
| Retained S011 exact replay |`045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e`|
| Retained S011 moment engine |`82634fc558ec4eef0bb675b44c2eacb88f2e551d8093262ccbb004b7ef86eff1`|
| Retained Clifford engine |`2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962`|
| Retained signed-Pauli engine |`3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38`|

Frozen word container/payload pairs:

- Parent codec: `777be9c2991cb9755e82ee43251d906831d1d08e303d8e2bbf89d53e6962c4be` /
  `a978dff169897fed60646a0dfd9453eae9e80f2821aaefed582477f8fe0baebb`.
- Alignment: `7cfefc12e666f1fa39a311f13ba5e919c307bfb8264d933a71d2abf2b2de55f2` /
  `6311a93117c7fc22b183f66b88452cd274bcd4a776e7cf00e99dd32264a9b340`.
- Aligned codec: `79bf4bd0ce0d6e2c0bd44c3134141314bea0b8c5b77ea486d8496e17ddd7beb3` /
  `17290ab18dedb7f4b40ec8600b9b577105d380ccd1be1a5924b8d9ad3c1cdede`.

The included dependency files are byte-for-byte retained engines; no new
independence is claimed by rerunning them. The phase equality engine is a
separately retained implementation, but this author package still requires
independent mathematical review before programme admission. The repository's
Apache-2.0 source terms and predecessor attributions remain in effect.

## Open next questions

Construct a single monotone schedule in which many receiver-bank recodings
reuse raw-route segments, keep authentic branch values available, and restore
all original D/Y endpoints. Simultaneously price a compatible actual reverse
acquisition scheme. The invariant shows the intended composition; it does not
solve either availability or whole-system cost. No new kappa.
