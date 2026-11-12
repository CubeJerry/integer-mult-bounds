# Global unchanged-donor contact bound

The analytic proof bounds arbitrary monotone original-value path arrangements by2,786 contacts. The independently checked finite integer refinement gives2,768. Source rank witnesses force the standard eight-packet decoder and all4,992 side pairs, leaving at least2,224 pairs outside this grammar. This is not a paid-MOVE bound; coded aggregates and relays remain open. No new kappa.

PROOF.md states the complete scope. review/REVIEW.md independently checks it and supplies decoder witnesses and the finite recurrence; receipts are under review/output/. The optional all-chart census is discovery evidence, not a premise of the analytic proof. check_discovery.py authenticates every census witness and independently evaluates the integer relaxation.

```sh
PKG=research/moonshot-005-program/results/unchanged-donor-contact-bound
SRC=research/shared-wire-split-composition/data/final.json.gz
python3 -B "$PKG/review/check.py" --source "$SRC" --output /tmp/contact-review
python3 -B "$PKG/check_discovery.py" --source "$SRC" --ports "$PKG/PORTS.txt" \
  --census "$PKG/ALL-CHART-POPULATIONS.json" --output /tmp/contact-discovery.json
g++ -std=c++17 -O3 -Wall -Wextra "$PKG/enumerate.cpp" -o /tmp/enumerate-source-charts
/tmp/enumerate-source-charts "$PKG/PORTS.txt" > /tmp/source-chart-census.json
```

Markers: `PASS_INDEPENDENT_CONTACT_AND_UNIQUE_DECODER_AUDIT` and `PASS_SOURCE_BOUND_DISCOVERY_AND_RECTANGLE_REVIEW`. The optional8,283,458-subspace census hash is pinned in CENSUS-REPRODUCTION.json. Reruns are reproduction, not additional independent review. Prepared for @CubeJerry with substantial OpenAI assistance, Apache-2.0; preserve native/E8 credit.
