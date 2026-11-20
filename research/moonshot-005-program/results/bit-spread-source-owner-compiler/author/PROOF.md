# A binary source word for the 3,840-field H263 construction

The three H263 donors now have explicit source words at their genuine X and Y addresses. Including the original-X inverse, they cost 130,692,472 binary ADDs. Replacing exactly these entries in the 111-donor singleton-aware background gives 457,788,616 source ADDs including all source inverses. This source supplies H263's 33 native inverse fibres and the separate singleton-aware ranks. The prescribed endpoint at every receiver, its return and the strict recursive suppliers remain open.

## Coordinates and ownership

Each of donors 0, 61 and 62 has 3,840 fields, indexed by native coordinate c and copy 0 through 7. An X field at role j has ID 3840j+8c+copy. Y IDs add 111·3840. Use the six polynomial basis bits of GF(2)[z]/(z^6+z+1) in ascending order. At each special donor the marked component occupies original ordinals 0 through 767, the unmarked one 768 through 3839. Within a component scalar column s and spinor lane t have ordinal 16s+t. This fixes the original coordinate gauge used by the three equal inverse lifts.

Pair spinor lanes (0,8) through (7,15). For k=3 or 12 one pair has 32k fields. At each half-early plane compose its actual k-by-2k early matrix with the block diagonal of its two ordinary source quotients. At a full-early donor incidence keep both quotient blocks. Stack these rows in ascending plane order. This gives six invertible matrices of sizes 96 and 384, each repeated on its eight disjoint spinor pairs. HOLDER-WORDS supplies every original X address.

The outgoing order depends on timing. At a full early H with 16 X owners per port, present k degrees with 16 lanes each. At a mixed H where the donor contributes a full early bundle, present 2k degrees with eight lanes each. At a half-early incidence use k degrees with eight lanes. For both phases use ascending actual owner ID within each donor/H group, with the 9-port component first. A paid in-place permutation implements the required X placements. Every source and destination occurs exactly once, and the generator checks the swap cycles on all labels. H263 then receives its two unframed Vandermonde inputs. The H package charges its own local permutation and matrix.

## Binary compilation

Elimination records field row additions, swaps and changes of scalar. A row addition with coefficient c costs one binary ADD per 1 in the six-by-six scalar multiplication matrix. A field swap costs eighteen binary ADDs. Each scalar change uses a six-bit in-place addition circuit. Reverse the reduction's binary ADDs for the forward map. Forward and inverse therefore have equal length. The compiler reduces each matrix to identity and executes the inverse field stream on every basis column. It also checks all 63 nonzero scalar multipliers on binary basis inputs. A field-linear identity expanded in this basis acts correctly on all six-bit inputs at every replicated whole-record width.

Each chosen late coordinate is an explicit parity in one spinor lane. Before any genuine X departs, INIT six stationary bits and compute the specified parity from its original X owners. When the corresponding true Y arrives, add in those six bits and pay dirty CLEAR. An arbitrary Y baseline is preserved. There are 8,640 distinct Y destinations. The 51,840 binary cache lifetimes are charged and the word adds zero MOVE. The inverse source word can execute at Hub once the downstream pure early word is reversed in its actual order. The full transport and its costs are separate.

| Three special donor operations | Binary count |
| --- | ---: |
| All eight repeats of each early basis word | 59,084,936 ADD |
| Genuine X owner permutations | 204,624 ADD |
| Early production of late parities | 12,061,512 ADD |
| Injection into actual Y | 51,840 ADD |
| Pure inverse including permutations | 59,289,560 ADD |
| Forward plus inverse | 130,692,472 ADD |
| Cache INIT and dirty CLEAR | 51,840 each |

## Other donors and replay

The singleton-aware source manifest supplies the remaining 108 entries. It charges 111,965,016 early basis ADDs, 7,440,696 permutation ADDs, 85,796,400 late evaluation ADDs and 2,488,320 snapshot-copy ADDs, with the same number of INITs and dirty CLEARs. It counts 119,405,712 pure inverse ADDs. The combined source costs 279,093,344 forward ADDs, 178,695,272 pure inverse ADDs, 2,540,160 INITs and the same number of dirty CLEARs. At most 2,540,160 extra binary owners suffice across all donors if every cache lifetime overlaps. The background stores original values for late evaluation while the three special donors store computed late parities. Each method pays its own cache count.

The receipt binds the coefficient table, per-donor background prices, native routes, layout and spread. Rebuild with Python 3 and NumPy:

    python -B compile_source.py --repo REPO --coefficients COEFFICIENTS.json.gz --background PER-DONOR-COSTS.json --out FRESH

Run `python -B expand.py --word-dir FRESH --donor 0 --stage early --limit 100` for the first 100 literal owner-level ADDs. Omitting the limit streams the whole stage. Other stages are prepare, deliver and inverse. The compressed outputs retain all field row primitives and holder addresses. Execute the stages at their actual source visits or original-X recovery site, including the intervening existing movement. All H/D/K operators, final output, return bill, strict suppliers and five foundations retain separate obligations.

Credit @CubeJerry and the source, native atlas, spread, H263 and singleton-aware source contributors. The source compiler used OpenAI assistance. No new complete kappa.
