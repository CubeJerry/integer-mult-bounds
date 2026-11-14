# Exact reproduction

Use Python3.12 or compatible Python3 with rational arithmetic. The source
builder needs only the standard library. The retained phase engine uses
its own dependencies documented by the predecessor package. Run from the
package root, replacing NATIVE and PARENT by the pinned existing source files:

```sh
python3 -I -B build.py --native NATIVE --parent PARENT --engine dependencies/replay.py --output reproduced
python3 -I -B check_phases.py --engines dependencies --word reproduced/WORD.json.gz --parent PARENT --output reproduced/PHASES.json
python3 -I -B price.py --full FULL-RESULT.json --engine dependencies/interval.py --receipt reproduced/RESULT.json --output reproduced/PRICE.json
```

Expected word SHA256:

`f72c890e06437c3b6a177c71019f56e60f30712e5c09c1e241c893c1f180e42d`.

Expected source result: PASS_ACTUAL_PARITY_HALF_PAIRED_COMPILER;
rank400, reverse residual rank56, current-a debt4608, original debt4962;
raw profile {1:160,2:280,3:360,5:280}; owned profile {1:8,2:8,6:8,8:8};
4614 operations,136 lifetimes, peak120. Five semantic mutants must fail.

Expected phase result:430 actual new ordered maps; wrong global phase fails.
The retained phase checker's historical status text mentions transient codec;
its inputs and emitted exact recipes are this new word's430 chart maps.

Expected complete actual movement invoice: limiting room
0.9541333063079446... at exponent199/200; first positive fixed m=35.
The source remains incomplete: no new supplier or kappa.

All exact pins, formulas and scope are in PROOF.md. Manifest hashes preserve
these source/proof bytes separately from any root independent review.
