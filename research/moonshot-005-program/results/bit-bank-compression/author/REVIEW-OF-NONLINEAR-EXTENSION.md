# Independent review of the finite-field nonlinear strengthening

**PASS, with the root theorem's stated finite-alphabet, fixed-side-information scope.** This receipt independently reviews the proof in `work-root/four-bank-compression-review/REVIEW.md`, SHA256 `d940a220d6db1459b233812cddfb7449306ddd559fda26d9adcc0276409f9e4c`. The original linear author proof remains unchanged.

The extension fixes a finite characteristic-two field F_q, width V, exactly B80 or B88 as side information S, and the four declared bank spaces. Each encoder is an arbitrary function of its own U_j x and Sx, with output alphabet of size at most q^(ell_j). The common decoder must recover the canonical C9 measurements exactly. These are the premises needed for the counting argument.

For each bank j, the already independently verified cut certificate gives d_j binary perturbations lambda_t which annihilate S and every other bank, while their selected canonical values form an identity matrix. For arbitrary records t_1,...,t_(d_j), set x=sum_t lambda_t tensor t_t. All other encoder arguments are now exactly(0,0), so all their messages are fixed constants regardless of their nonlinearity. The selected canonical outputs vary over every tuple(t_1,...,t_(d_j)), giving q^(d_j V) different required outputs. Therefore the remaining bank's message must distinguish at least that many cases, and ell_j>=d_j V.

The perturbation families used for different banks need not be the same: every fixed encoder alphabet must meet each bank's own worst-case requirement. Summing the four alphabet bounds is therefore valid. The binary linear constructions already attain the same totals13V and9V, so these are sharp for the finite-field nonlinear model too.

No injectivity assumption on U_j x is needed: if its observed values could not distinguish some of these target tuples, that would only make exact decoding impossible. No statistical or finite-experiment inference is used. The explicit cut identities establish the entire family of inputs at every positive width and every finite characteristic-two field.

The following limits are essential and are correctly retained by the root theorem:

- The alphabet bound is an actual bound on the number of possible messages. Uncharged length labels or an unrestricted output alphabet cannot be added.
- The encoder is confined to its fixed bank observations and S. Interactive acquisition of new measurements is a changed model.
- The rank88 case grants only the previously known83 points before encoding; fresh point feedback after these messages is excluded.
- The target is C9 at the common decoder, not arbitrary receiver-specific noncanonical completion.
- Arbitrary maps over infinite fields are outside the counting theorem. The original linear theorem remains valid there by rank.
- The result is an information-dimension bound, not a movement, owner, retirement, or complete-supplier cost.

The review finds no missing assumption or invalid inference within those boundaries. Root's separate certificate check is supporting computational verification; this receipt's independent acceptance is based on the perturbation/counting proof and the already checked dual identities, not another execution of that checker.

Credit @CubeJerry; root for the nonlinear counting extension; Worker B for the original linear cut/construction and this independent mathematical review; Worker C and predecessor source/envelope contributors. Substantial OpenAI assistance. **No new kappa.**
