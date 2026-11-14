# All-width decomposable quotient capacity

Two source-specific theorems give V*S<=17r for decomposable quotient bases:
(1) V>=2 and r<=V+1, with repeated value lines handled by scalar projection;
(2) MDS value rows and r<2V. Scalar generators may be dependent. The MDS
class requires r>=ceil(28V/17) for the target28 savings. Neither statement
prices physical availability or establishes a new kappa.

```bash
python3 -I -B check.py --native NATIVE.json.gz --output RESULT.json
python3 -I -O -B check.py --native NATIVE.json.gz --output /tmp/capacity-optimized.json
```

Expected PASS_DECOMPOSABLE_QUOTIENT_CAPACITY_CONTROLS:8192 binary coefficient
cases,4096 MDS right inverses over F4, further width controls and actual
native quotients V+1 at V=2,3,4,8,17. All native controls have cardinality
charge216; they are neither target constructions nor physical sources.
The repeated-value and r=2V MDS controls demonstrate the exact scope of
the matrix-independence arguments. Normal and optimized receipts match.

Independent review pending. Mathematical premises and frozen predecessor
pins are in SOURCES.json. Prepared for @CubeJerry with OpenAI assistance;
root and predecessor credit are retained in the proof.
