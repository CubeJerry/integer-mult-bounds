# Independent review of the native D-chart mixers

On the pinned bank-480 atlas all 3,150 matrices preserve the 388,200 required eight-input/eight-output restrictions over GF(64). The early-to-late state widths are sharp for the **isolated chart with independent input coordinates**. This is a local transport result. Identifying the desired low-return endpoint, recovering its physical realization and closing the suppliers are separate obligations.

## Lower bound and attainment

Fix a chart, a native donor and a native receiver. Allow its eight supported input fields to vary independently with all other chart inputs fixed. Write $e$ for the number of early input coordinates and $t$ for its early observed outputs. With the late inputs fixed, the $|F|^e$ possible early inputs must be distinguished. The $t$ visible early fields and $r$ stored fields have at most $|F|^{t+r}$ distinct joint states. Every visible late output is determined by the fixed late inputs and this stored state. Thus exact injectivity on the eight-input slice forces $r\geq e-t$. The argument allows nonlinear maps and any encoding in the snapshot. It scales to $s(e-t)$ field units on $s$ independent simultaneous copies. Allowing other early information to re-enter the chart, changing the input support, or demanding only a proper correlated slice changes the hypothesis.

The emitted block map has upper-right block zero. Its two diagonal maps are square and invertible, preserving arbitrary original late baselines. The lower-left map factors through the reported $r$ fields. Eliminating the early- and late-only input variables in a native restriction leaves a deficit of $e-t$. More explicitly, Cauchy–Binet expands its determinant into a sum over cache subsets of size $e-t$. Each summand is a product of a Cauchy minor on the early side, one on the late side and the selected weights. This explains the selector without presuming arbitrary nonzero weights succeed simultaneously. Direct elimination using the published choices checks that they do. Each chart uses the maximum $e-t$ attained by its pairs.

The minima have histogram $386,1138,1136,428,62$ for widths zero through four. The sum is 4,942 allocated field symbols at bank 480. It is an aggregate under separate chart memories. A global simultaneous-peak lower bound would also require a common liveness cut. The proof does not transfer to an arbitrary correlated global algorithm.

## Independent calculation

The checker authenticates the decompressed layout, routes and weight certificate; reconstructs every orthogonal D chart from root dot products; and verifies all original-owner IDs and H/D/K incidences. Using the primitive 63-element orbit of $z$ modulo $z^6+z+1$, it forms each full field matrix from the certificate. Ordinary Gaussian elimination tests each actual 8-by-8 submatrix, all full matrices and the ranks of all cross-phase maps. It does not evaluate the selector, use its determinant shortcut or import its field code.

The pure phase prices are reproduced using literal binary XOR words with full-basis forward and inverse checks for every size that occurs. The snapshot and delivery prices follow from the binary matrices of multiplication by the actual field coefficients. At bank 3,840 the forward and inverse pure work each costs 261,025,824 ADDs. The 11,901,048 capture and 12,013,632 delivery ADDs give 545,966,328 in total. There are 237,216 INITs and the same number of dirty CLEARs. The existing movement and the timings of the pure inverses remain charged to the surrounding atlas/caller.

Four tests at D0 distinguish rank, coefficients, labels and causality. Dropping one of four cache directions takes a maximizing pair from rank eight to seven. Replacing all four weights by one preserves cross rank four but makes three native minors singular. Swapping the first two early physical outputs keeps each phase invertible but makes two cuts singular. Swapping an early and a late output preserves total invertibility but introduces illegal late-to-early dependence.

Run `python -B check.py --repo REPO --charts CHARTS.json.gz --out FRESH` with NumPy. The immutable payload hashes and the exact receipt are in output/RESULT.json.

Separate OpenAI-assisted review for @CubeJerry. No new complete κ or foundational discharge.
