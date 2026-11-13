# Freeze record

This is a bounded mathematical supplement for review in the #6509 exact-sum
Gaussian-rounding branch. It is frozen at the canonical analysis base
`e54523517d0f03e58352e647c403a5af3e525a57`; predecessor source pins and
credit are recorded in `SOURCES.json` and `NOTICE.md`.

## Claim

The stated integer map is a bijection on Gaussian pairs, preserves the
complex sum exactly, commutes with global multiplication by `i` and wire
swap, has combined Euclidean error at most one relative to `C_+`, and has
bilateral pair-radial supremum exactly `1/sqrt(2)`. The upper bound is
proved for this map; the lower bound applies to every exact-sum map with
error at most one. Conjugation intertwines the map with its inverse. The
map is not generally conjugation-equivariant and has no fourth-power
identity; exact controls are recorded in `RESULT.json`.

The claim does not include a physical implementation, tariff, multiplication
bound, or global result beyond the pair-rounding contract.

## Reproduction

From this directory, run:

```sh
python3 -I -B check.py > /tmp/complex-map-result.json
cmp /tmp/complex-map-result.json RESULT.json
python3 -I -O -B check.py > /tmp/complex-map-result-optimized.json
cmp /tmp/complex-map-result-optimized.json RESULT.json
sha256sum -c CHECKSUMS.sha256
```

The checker uses exact integer arithmetic and explicit `require` failures;
it does not depend on Python `assert` statements. It exhausts 625 pairs in
the coordinate box `[-2,2]^4` and checks 20 additional examples through
scale `2^512`. General claims are established by the algebra in
`PROOF.md`, not by these finite samples.

## Frozen files

`CHECKSUMS.sha256` covers the proof, source pins, checker, recorded result,
notice, README, and this freeze record. Replay is read-only and does not
rewrite the committed result.
