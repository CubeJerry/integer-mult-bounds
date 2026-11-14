# Quadratic spectral query gate

Read ADMISSION.md and author/PROOF.md for exact quantifiers and scope. No new kappa.

The checker is a dependency-free JavaScript function. From this directory run:

```sh
node -e 'const fs=require("fs"),vm=require("vm");vm.runInThisContext(fs.readFileSync(process.argv[1],"utf8"));process.stdout.write(JSON.stringify(runQuadraticSignChecks(),null,2)+"\n")' author/check_body.js
```

Expected status: PASS_EXACT_QUADRATIC_SPECTRUM_GAUSSIAN_RANK_AND_MAJORIZATION_CONTROLS. The same exact function body was executed in orchestration V8 during the local-workspace outage; a post-outage local Node run is not claimed. Finite dimensions2,3,4 supplement the written universal proof. The independent review is mathematical text review, not a separately executed second checker.
