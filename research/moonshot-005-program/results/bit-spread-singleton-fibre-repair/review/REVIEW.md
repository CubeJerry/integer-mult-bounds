# Independent physical replay of the repaired singleton source inputs

All 16 literal matrices pass a full source-to-H receiver replay. They cover eight affected chart/donor placements at both field widths. I independently assembled the actual square transfer on all 16 visible H planes at every native donor cut seeing its singleton. All 522 matrices have full rank. Every ordinary quotient also retains full rank. On all 300 affected designated receiver/component pairs, I solved for the shared inverse load on a different donor and fed that same original-coordinate load into the complete repaired physical system. Each test gives the prescribed central identity and zero at every other plane.

| Designated H | Donor | Singleton plane | Native cuts seeing singleton | Designated native fibres affected |
| ---: | ---: | ---: | ---: | ---: |
| 187 | 53 | 983 | 34 | 20 |
| 247 | 58 | 1064 | 31 | 18 |
| 335 | 77 | 1008 | 32 | 18 |
| 542 | 31 | 1091 | 33 | 18 |
| 694 | 93 | 1009 | 34 | 20 |
| 750 | 105 | 1118 | 32 | 19 |
| 753 | 105 | 1118 | 32 | 17 |
| 779 | 106 | 1090 | 33 | 20 |

Each line is checked for $k=3$ and $k=12$. One of the overlapping placements has 24 charts and 801 native chart/receiver inverse graphs. Its four singleton-bearing special stars are 53, 58, 93 and 105. The other placement has 23 disjoint chart stars and 770 native chart/receiver inverse graphs. H750 and H753 provide distinct alternatives for donor 105 on the same actual singleton plane.

## Actual readout

The verifier rebuilds every physical local output on the two original spinor lanes. At a full three-donor chart it takes the actual visible Vandermonde minor on the donor's degree group in both spinor lanes. At a mixed three-donor chart it applies each minor to the corresponding early or late coordinate block. The source chooses deterministic complementary late rows at half-early flags. The verifier derives those coordinate rows by descending greedy rank increments, independently of the compiler's pivot implementation.

At a two-donor chart the large donor occupies the first $2k$ early coefficients, so its source contribution consists of values and first derivatives. The small donor supplies the last $k$ early degrees and first $k$ late degrees. At a singleton the verifier applies the value matrix and first-derivative matrix for all $3k$ genuine early coefficients. Every evaluation point is the one-based rank of a visible actual D port in its sorted marked or unmarked H component. All ground Y baselines enter additively outside the source contribution.

The resulting full matrix has $32k$ rows on the $32k$ original fields of a spinor pair. Its first $2k$ rows are the designated centre whenever the receiver sees that centre. The verifier reduces this entire matrix and separately reduces the full ordinary matrix obtained from the first $2k$ singleton coefficients. It solves for the central lift on an unmodified donor and doubles it in original coordinates. Direct multiplication by the actual repaired whole system yields the identity on those first rows and zero everywhere else.

The old central lifts at each affected placement span $15k$ old scalar coordinates and lie in the old singleton kernel. Their aggregate annihilator therefore has dimension $k$. At each of the 16 component cases a genuine extra row has nonzero raw signal on a selected central lift. Rescaling that single extra row by the nonzero field element 2 preserves all ordinary quotient tests and the early-basis rank. Its visible Hermite readout becomes nonzero on the same lift. The receipt records the receiver and row for each test.

The certificate supports physical source-to-H graphs. The global D/K/terminal coefficient solution and a complete recursive bound remain open.

## Replay

From the repository root set `R=research/moonshot-005-program/results` and run

    python -B "$R/bit-spread-singleton-fibre-repair/review/check.py" --repo . --out /tmp/singleton-physical-review

The verifier reads the literal coefficient archive, both base placement parameters, the pinned native roots and routes, and the two independent earlier review modules. The command accepts explicit paths to those inputs. The output retains every native receiver ID, common-lift digest, early rank and mutation witness. Credit @CubeJerry and the source, phase, spread and singleton-repair authors. This independent reconstruction used OpenAI assistance.
