# Reproduce the scoped results

Run from repository root. Python3.12 was used; primary capacity uses NumPy2.3.5.
The four temporal verifiers and independent capacity/endpoint checks use the
standard library. Receipts do not establish unimplemented suppliers.

```sh
P=research/moonshot-005-program
S=research/shared-wire-split-composition/data/final.json.gz
python3 -B "$P/results/shared-core-temporal/verify.py" --source "$S"
python3 -B "$P/results/shared-core-temporal/verify_two_switch.py" --source "$S"
python3 -B "$P/results/shared-core-temporal/verify_endpoint_repair.py" --source "$S"
python3 -B "$P/results/shared-core-temporal/verify_coded_lift.py"
python3 -B "$P/results/owned-cut-capacity/verify.py" --source "$S"
python3 -I -B "$P/results/owned-cut-capacity/review/independent.py" --source "$S" --certificate "$P/results/owned-cut-capacity/CERTIFICATE.json"
python3 -I -B "$P/results/shared-core-temporal/review-endpoint/independent.py" --source "$S"
```

Expected JSON PASS markers establish the scoped checks. Key values: residual
rank≥275, two-switch all-cut nullity sum≤260, endpoint deficiency208, public
rank1479, main-on-main rank338, owned-only complement7, balanced full-input
complement63, arbitrary-helper lower bound62. The coded-interface check covers
algebra and negative controls, not an all-event observation witness. Normal
and optimized receipts are preserved beside each verifier.

The independent temporal [review README](results/shared-core-temporal/review/README.md)
documents its optional denser NumPy sweep. The
[BIT package](results/bit-selector-boundary-floor/) has its author replay and
separate lead reverse-source/Newton-root check. Imported packages retain their
own reproduction instructions. [VERIFICATION.md](VERIFICATION.md) records actual
executions; session receipts are in `sessions/2026-11-11-S001/`.

[PROVENANCE.json](PROVENANCE.json) binds imported files. SCIENTIFIC-FILES.json
freezes new scientific evidence; integrity checks do not prove mathematics.
No complete selected supplier cold replay, formal kernel or physical multiplier
was run this session.


For a fast read-only check of imported bytes, scientific manifests and reviewed
hashes, run `python3 -B research/moonshot-005-program/verify_checkpoint.py`.
Capture its stdout outside this tree before saving a new receipt here, so the
JSON syntax check does not inspect a file concurrently being written.

## S002 causal arrival theorem

```sh
python3 -B research/moonshot-005-program/results/causal-arrival-floor/verify.py
python3 -I -B research/moonshot-005-program/results/causal-arrival-floor/review/review_deliveries.py --author-certificate research/moonshot-005-program/results/causal-arrival-floor/CERTIFICATE.json
```

Expected: 984 innovations, complete record agreement and explicit payload controls.
Normal and optimized receipts are retained in the package.


## S002 encoded-state and calendar packages

```sh
python3 -B research/moonshot-005-program/results/encoded-prefix/verify_prefix.py
python3 -B research/moonshot-005-program/results/encoded-prefix/verify_demand_prefix.py
python3 -I -B research/moonshot-005-program/results/encoded-prefix/review-demand/review_demand_prefix.py --source research/shared-wire-split-composition/data/final.json.gz --transcript research/moonshot-005-program/results/encoded-prefix/demand-prefix.json.gz --author-receipt research/moonshot-005-program/results/encoded-prefix/DEMAND-PREFIX-RESULT.json
python3 -B research/moonshot-005-program/results/decoder-calendar-capacity/scan.py
python3 -B research/moonshot-005-program/results/decoder-calendar-capacity/weaker_demands.py
python3 -B research/moonshot-005-program/results/owned-difference-delivery/verify.py
python3 -B research/moonshot-005-program/results/owned-difference-delivery/budget.py
python3 -I -B research/moonshot-005-program/results/owned-difference-delivery/review/independent_rows.py --source research/shared-wire-split-composition/data/final.json.gz --certificate research/moonshot-005-program/results/owned-difference-delivery/CERTIFICATE.json
```

The demand review takes the compiler's DEMAND-PREFIX-RESULT.json, not the
separate author replay receipt. Calendar commands print3144/3111 and913/902,
106/106,0/0 respectively. Normal/-O records are provided; zero is no feasibility
claim. Independent calendar review scripts take explicit --source/--author paths.

## S002 final-wave acquisition and read-deadline checks

The frozen package READMEs document author commands. Use explicit paths for
portable independent reproduction (from repository root); store output outside
the frozen result tree.

```sh
P=research/moonshot-005-program
S=research/shared-wire-split-composition/data/final.json.gz
python3 -B "$P/results/read-deadline-capacity/review/review.py" --source "$S" --author "$P/results/read-deadline-capacity/RESULT.json"
python3 -B "$P/results/entry-preload/review/review_entry_preload.py" --source "$S" --certificate "$P/results/historical-owned/WITNESSES.json" --transcript "$P/results/entry-preload/preloaded-rail.json.gz" --author-result "$P/results/entry-preload/RESULT.json"
python3 -B "$P/results/prepaid-historical-budget/review/check.py" --source "$S" --invoice research/shared-core-target-obligations/INVOICE-RESULT.json --current "$P/results/owned-difference-delivery/CERTIFICATE.json" --historical "$P/results/historical-owned/WITNESSES.json" --author "$P/results/prepaid-historical-budget/BUDGET.json"
python3 -B "$P/verify_checkpoint.py"
```

Expected:8494 demand records,106/106 departure floors;71454 typed preload
instructions, five historical helper observations discharged, four later owned
observations retained; paid153090,targets27344,surplus3346,additional rank-one
ceiling3. Normal/-O author and separate reviewer receipts are preserved.
The400-input preload reference rail is not a complete1880-input shared lift.

## S003 initial-only acquisition

From repository root:

```sh
python3 -B research/moonshot-005-program/results/initial-preprocessing/review/review.py --source research/shared-wire-split-composition/data/final.json.gz --packet research/moonshot-005-program/results/initial-preprocessing
```

Expected:105 added arrivals,72073 instructions,400 q inputs,1480 public endpoints,
501ADDs,105INIT/CLEAR pairs,peak44,finalowned0. Repeat with-O. See the package
README for explicit author source/word reconstruction commands.

## S003 integrated packages

Each results/{quotient-history,endpoint-obstruction,temporal-observation-rank,
seven-rewrite}/README.md gives author commands; each review/REVIEW.md gives the
separate independent command and expected status. Use the integrated package
path from repository root. For quotient/history, first generate reverse rows,
then pass that rowfile to history_review.py. Both normal and-O receipts are
stored. No search is needed to check the frozen46 endpoint certificate.

## S003 lifetime and target packages

Use results/{fused-seven-rewrite,lifetime-elimination,bit-query-budget}/README.md
and review/REVIEW.md. The lifetime independent checker reconstructs the source
macros, all4 words and their dependency closures before checking full endpoints
and dyadic prices. The BIT review independently reconstructs both profiles and
certifies the target sign with decimal-grid integer roots. Neither needs
network access. No raw numerical root or finite search is promoted to a theorem.

## S003 loan and authentic relay

```sh
P=research/moonshot-005-program/results
S=research/shared-wire-split-composition/data/final.json.gz
python3 -B "$P/paused-common-loan/review/independent.py" --source "$S" --packet "$P/paused-common-loan" --lifetime "$P/lifetime-elimination" --invoice research/shared-core-target-obligations/INVOICE-RESULT.json --output /tmp/paused-review.json
python3 -B "$P/authentic-relay-interface/review/review.py" --source "$S" --author "$P/authentic-relay-interface" --output /tmp/relay-review.json
```

The selective-refinement review command is in its review/REVIEW.md. Frozen
normal/-O receipts and pins accompany each implementation. The source relay
review checks a conditional input interface, not actual acquisition.

## Actual acquisition and full target prices

```sh
P=research/moonshot-005-program/results
S=research/shared-wire-split-composition/data/final.json.gz
python3 -B "$P/paid-observable-acquisition/review/review.py" --repository . --package "$P/paid-observable-acquisition" --output /tmp/acquisition-review.json
python3 -B "$P/relay-acquisition-budget/verify.py" --repository . --lifetime "$P/lifetime-elimination" --source-rows "$P/authentic-relay-interface/review/SOURCE-ROWS.json" --output /tmp/acquisition-budget.json
python3 -B "$P/relay-acquisition-budget/review/review.py" --source "$S" --invoice research/shared-core-target-obligations/INVOICE-RESULT.json --lifetime-word "$P/lifetime-elimination/eight.json.gz" --author "$P/relay-acquisition-budget" --output /tmp/acquisition-budget-review.json
```

Expected PASS_INDEPENDENT_BOTH_1880_INPUT_ACQUISITION_PREFIXES,
PASS_TWO_ACQUISITION_TARGET_BUDGETS and
PASS_INDEPENDENT_DYADIC_RELAY_ACQUISITION_BUDGET. Normal/-O receipts are frozen.
Acquisition proofs and conditional paid invoices have distinct scopes; neither
is a complete shared multiplication bound.

## S005 chronological screen and five-chart conservation

```sh
python -B research/moonshot-005-program/results/causal-encoder-screen/verify.py --repository . --output /tmp/causal-screen.json
python -B research/moonshot-005-program/results/five-chart-history-conservation/verify.py --source research/shared-wire-split-composition/data/final.json.gz --output /tmp/five-chart.json
python -B research/moonshot-005-program/results/five-chart-history-conservation/review/verify_duals.py --source research/shared-wire-split-composition/data/final.json.gz --certificate research/moonshot-005-program/results/five-chart-history-conservation/CERTIFICATE.json --output /tmp/five-chart-independent.json
```

Author markers: `PASS_CAUSAL_RECOVERABLE_ENCODER_SCREEN` and
`PASS_FIVE_CHART_RANK_ONE_HISTORY_CONSERVATION`. Full independent commands and
compressed receipts are in [review/README.md](results/five-chart-history-conservation/review/README.md).
Repeat with `-O -B` for optimized consistency. These are source identities,
not a new asymptotic supplier or complete theorem.

## S006 source-bound packet prefix and restoration gates

Run from repository root; use a separate scratch output directory when a
checker accepts --output. Do not overwrite frozen receipts merely to test them.

```sh
P=research/moonshot-005-program
S=research/shared-wire-split-composition/data/final.json.gz
python3 -B "$P/results/eight-packet-prefix/verify.py" --source "$S"
python3 -B "$P/results/eight-packet-prefix/review/verify_prefix.py" --source "$S" --prefix "$P/results/eight-packet-prefix/PREFIX.json.gz" --output /tmp/s006-prefix-review.json
python3 -B "$P/results/endpoint-side-information/reproduce.py" --source "$S" --output /tmp/s006-routing.json
python3 -B "$P/results/eight-packet-budget-and-reverse/review/check.py" --source "$S" --invoice "$P/results/eight-packet-budget-and-reverse/INVOICE-SOURCE.json" --author "$P/results/eight-packet-budget-and-reverse/RESULT.json" --macro "$P/results/eight-packet-budget-and-reverse/REVERSE-EIGHT.json.gz" --output /tmp/s006-budget-review.json
python3 -B "$P/results/joint-hub-restoration/verify.py" --output /tmp/s006-restoration.json
python3 -B "$P/results/single-overwrite-loss/verify.py" --source "$S" --neutral "$P/results/endpoint-side-information/RESULT.json.gz"
python3 -B "$P/verify_checkpoint.py"
```

The corresponding independent graph, algebra, joint-restoration and overwrite
checkers are in each package's review directories. Their --help documents
source/certificate arguments. The source-normalized all1480/1880-column
replays, finite controls and mathematical scope are recorded in VERIFICATION.
Compressed certificate comparison uses exact decompressed bytes. No command
above certifies a complete κ or discharges the five foundational assumptions.


## S006 second checkpoint

```sh
P=research/moonshot-005-program
S=research/shared-wire-split-composition/data/final.json.gz
python3 -B "$P/results/unit17-precompensation/review/review.py" --source "$S" --word "$P/results/unit17-precompensation/WORD.json.gz" --output /tmp/unit17-independent.json
python3 -B "$P/results/unit17-precompensation/review-scalars/check.py" --source "$S" --word "$P/results/unit17-precompensation/WORD.json.gz" --output /tmp/unit17-scalars.json
python3 -B "$P/results/precorrected-observer/review/check.py" --source "$S" --packet "$P/results/precorrected-observer" --output /tmp/precorrected-independent.json
python3 -B "$P/results/e8-response-control/review/check.py" --source "$S" --screen "$P/results/e8-response-control/RESULT.json" --output /tmp/e8-dual77.json
python3 -B "$P/verify_checkpoint.py"
```

Other source/fixture arguments are in package READMEs. Unit17 builder takes
MATRICES.json and ../joint-nonneutral/RESULT.json.gz. Keep scratch outputs outside
frozen packages. These checks do not establish the missing complete supplier.

## S007 actual channel, one-term composition and route fusion

Each results/{foreign-history-channel,eight-packet-one-correction,
observation-preserving-route-fusion}/ has a frozen independent checker and
path-only review/run_review.py adapter. Run with
`--repo /path/to/integer-mult-bounds --output /tmp/RECEIPT`.
The output REVIEW-RESULT.json must equal the frozen receipt. CHART-MAPS.md
in the route package gives the exact phase/rank check; inherited compiler
assertions must remain enabled. retargeted-history-control/run_check.py takes
the same flags and reproduces DUAL-CHECK.json. Each package keeps author
reproduction commands, source pins, proof scope and meaningful negative controls.

## S010 fresh-eight independent replay

```
python3 -I -B research/moonshot-005-program/results/fresh-eight-acquisition-optimum/review/check_fresh_eight.py --repo . --output /tmp/fresh-eight-review
```

Expected: exact511-direction distribution487/24, minimum line support43,
minimum pair intersection15, and positive limiting deficit.25311068495571478... .
This reruns the separately written reviewer; it is not a new independent review.
