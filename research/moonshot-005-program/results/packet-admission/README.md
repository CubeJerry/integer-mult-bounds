# Exact packet-admission reduction

`PROOF.md` states and proves the conditional row-containment criterion for initial common debt cancellation and receiver gain correction. `verify.py` checks exact rational controls, four meaningful failure cases, and the H4 optimistic packet ceiling using a pinned tariff receipt. `RESULT.json` and `RESULT-OPTIMIZED.json` are byte-identical. `BUDGET.json` presents the same exact interval margins with decimal displays.

Reproduce from the package parent directory:

```bash
python -B packet-admission/verify.py --tariff eight-packet-budget-and-reverse/RESULT.json --output /tmp/packet-admission.json
python -O -B packet-admission/verify.py --tariff eight-packet-budget-and-reverse/RESULT.json --output /tmp/packet-admission-optimized.json
```

At kappa=1/200 the H4 invoice with all 6310 common and 1710 funded raw MOVEs retained, no second-owned service, and eight new rank-one reverse calls admits **at most ten** new rank-nine packets if there are no other new calls. Ten leave between 1.38241657470217126466095855731 and 1.38241657470217126466095856219 normalized native cost units; eleven have a strictly negative margin. Eight leave 19.1857486498012441003914020. These are conditional Gaussian invoice margins. They do not discharge the other raw endpoint duties, cache costs, ordinary arithmetic, scalar services, uniform complex/BIT interfaces or foundational assumptions. Using eight packets is a design convenience, not the exact invoice ceiling.

The next mathematical obligation is a physically admitted complete family with low stacked rank, not an arbitrary matrix with small algebraic rank. The unit17 literal construction demonstrates a real but unprofitable instance. The fixed E8 donor77 column fails the separate source response dual, so this criterion must be optimized over actually reachable responses.
