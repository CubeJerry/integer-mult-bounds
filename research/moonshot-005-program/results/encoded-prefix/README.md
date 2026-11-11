# Encoded prefixes and the next observation contract

**No new κ.** This package supplies literal, exact source-bound prefixes for
the permanent κ=1/200 programme. It changes intermediate main information,
then relaxes an excessive all-live virtual-helper decoder requirement. It
preserves every entering input direction and records why the straightforward
complete extensions still fail the target budget.

Read [PROOF.md](PROOF.md), [RETIREMENT.md](RETIREMENT.md), then
[DEMAND-PROOF.md](DEMAND-PROOF.md). The latter is the useful continuation
interface, subject to the programme's newer departure-demand constraints.

| Packet | Exact scope | Extra paid profile | Owned state at cut |
|---|---|---|---|
| prefix.json.gz | Cut25728; all1480 virtual roles cochart-decodable | P1+8, P2+1 | 11 live |
| retired-prefix.json.gz | Cut26226; all-live decoding with checked dirty retirement | P1+86, P2+6 | 87 live,33 retirements,120 lifetimes |
| demand-prefix.json.gz | Cut25897; all400 current mains decoded and400 entering differences retained | P1+4 | 11 live; second-helper rows explicitly deferred |

These are prefix expenditures, not complete invoices. The eager retirement
rule's next rank-one delivery exceeds the unchanged H4 allowance. The full
fixed demand graph still requires2879 auxiliary arrivals. Neither rule is a
complete target-feasible native. No BIT supplier or assumption discharge is
claimed.

## Reproduction

Use Python3's standard library. The pinned source must exist at
`research/shared-wire-split-composition/data/final.json.gz`; scripts locate it
from the repository or accept `--source`. From the package directory:

```sh
python3 -B verify_prefix.py
python3 -B verify_prefix.py --transcript retired-prefix.json.gz
python3 -B check_retirement.py
python3 -B local_macro.py
python3 -B verify_demand_prefix.py
python3 -B demand_graph.py
```

Expected verification statuses begin with PASS. The graph reports2879 retained
auxiliary arrivals, an exact arithmetic failure for this fixed expression
policy. It does not claim a completed native replay.

Regenerate to temporary paths, preserving frozen evidence:

```sh
python3 -B compile_prefix.py --transcript /tmp/moonshot-prefix.json.gz --output /tmp/moonshot-prefix-result.json
python3 -B compile_prefix.py --cut 31736 --budget-moment 98.39907694 --retire --transcript /tmp/moonshot-retired-prefix.json.gz --output /tmp/moonshot-retired-result.json
python3 -B demand_prefix.py --cut 25897 --transcript /tmp/moonshot-demand-prefix.json.gz --output /tmp/moonshot-demand-result.json
```

Compare decompressed canonical JSON payloads against their recorded SHA256
values. Regenerated gzip container bytes can vary across runtimes. Explicit
exceptions keep the checks active under Python−O.

## Verification and limitations

Author physical replay uses all1880 independent formal inputs and separately
executes both virtual source prefixes. It checks actual ownership annotations,
cochart operations, current decoders, source order and input retention. Wrong
owned-MOVE flags, wrong delivery signs, missing transport, aliased owners and
false input-retention claims are rejecting controls. Separate independent
reviews and exact reviewed-byte pins are supplied with the integration.

Independent review caught a real draft defect: added owned sidecars copied a
public source MOVE's ownership flag. The corrected compiler emits owned=True
for those fields; the verifier rejects the old annotation. All current
transcripts and receipts were regenerated and replayed after this correction.

Rank/span reasoning and dependency pruning are elementary. The contribution
is the precise source-bound construction, typed causal transcripts, quantified
interfaces and scoped paid failure of the naive extensions. New scalar/tape/
precision tariffs, full lifecycles and all five global assumptions remain open.
No cumulative PR readiness is asserted by this package.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit the retained
#7000/#7001 shared-wire source authors and the programme's H4 recovery,
coded-lift and owned-capacity work. Apache-2.0 under the repository license;
predecessor sources retain their existing notices.
