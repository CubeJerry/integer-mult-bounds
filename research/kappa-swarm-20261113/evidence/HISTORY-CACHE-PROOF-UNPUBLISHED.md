# Earlier destination-history filter for the #7481 relocation candidates

No retained source-span candidate can obtain its moving value from an earlier
destination-chart bank. This is a source-history exclusion, not a statement
about imported caches, modified source histories or unrestricted algorithms.

Frozen input: #7481 WORD.json.gz, compressed SHA256
acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9.
The complete exact relocation census found 49 source-span cuts: 18 public and
31 owned. Their ranks are {1:21,2:12,3:5,4:9,5:2}; thus 11 have rank>=4.

For each of their 40 destination subspaces B, define Hist_B(t) to be the span
of all normalized latent rows seen at B strictly before t. It contains every
row in every earlier actual coframed bank. It is initialized with all public
entrance rows at B. Each earlier MOVE arrival at B adds its arriving row.
INIT adds zero, CLEAR adds no information, and coframed ADD/COPY/SCALE creates
only linear combinations of rows already in the historical span. Therefore
these observations exhaust the cumulative history without sampling scalar
event times. The one duplicate frame-space pair is granted ordinary rank-zero
normalization, enlarging rather than narrowing the permitted observations.

filter.py propagates all 1,501 independent public coordinates using exact sparse
Fraction arithmetic through all 76,475 instructions. It also reconstructs the
moving row from each of the 49 independently produced source-span witnesses,
checking those identities against the full exact forward rows.

The 40 histories contain 1,465 independent generators in total. At every one
of the 49 cuts, the current moving row is outside Hist_B(t). There are zero
cumulative-span hits, including both rank5 and all nine rank4 candidates.
The pass completed in 30.24 seconds. FILTER.json records the generator rows,
per-cut ranks/results, source hash and coverage.

If an earlier actual bank could form the required x using coframed linear
operations, then x would belong to that bank's span and hence to Hist_B(t).
Its exclusion from the larger cumulative span rules out that one-cache
provider. No assumption of simultaneous availability of rows from different
times is used for a positive claim, and no several-cache disposal is granted.
The favorable relaxation already fails, so no cache lifetime, public role
transfer or physical provider was emitted.

This does not cover paid imports from other charts, changed earlier source
operations, external input-dependent stock, correlated native inputs, or a
different later repair interface. The owned subset is a source-delta extension
of the #7308 span question; the public-history scope still requires root's
related-work comparison. No changed supplier, kappa or removal of the five
retained assumptions is claimed.

Reproduce with Python 3.12 and the standard library:

```
python3 -I -B worker-b/history-cache/filter.py
```

The only helper import is the frozen standalone relocation kernel module,
whose row arithmetic and bit-subspace enumeration are reused. Source and
output files remain in their scoped directories. Credit #7481 and retained
native authors, the earlier owned-history questions and root's one-cache
research direction. Substantial OpenAI assistance; Apache-2.0. No publication
was authorized or performed.
