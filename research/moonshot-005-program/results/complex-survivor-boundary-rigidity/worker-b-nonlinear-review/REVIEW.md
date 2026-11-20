# Review of the nonlinear extension

**Accepted as a scoped mathematical argument**, conditional on the exact finite identities independently reconstructed in the root review.

Reviewed file: `root-review/NONLINEAR-PROOF.md`
Reviewed SHA-256: `a4707a953c1762d94787d8da7ee2d81bcd7a85a67413e7ac1c7d3f71ad4c9bf0`

I checked the universal argument rather than inferring it from the width-two controls. The following implications are valid.

1. The additive-response identity remains valid when the injected perturbations are arbitrary functions of the original inputs. Since `H=0`, every changed message still receives exactly its original pre-payload `P_j x`.
2. Global bijectivity forces `A_0` to be bijective. The surjectivity proof uses `Q_0 B_0=1`; the injectivity proof varies inputs along `R_0`, for which `P R_0=e_0`. Neither step requires zero-preservation or surjectivity of all five rows of `P` together.
3. The proposed inverse is verified in both composition orders using `P R=diag(1,0,0,0,0)`. No commutation, continuity, measurability, or linearity of the five maps is needed.
4. At each bank-zero witness, a zero scalar product for an unwanted channel means one of its two scalar factors is zero. Thus that channel cannot contribute dependence on the varied coordinate even through a nonlinear correction. The isolated nonzero factors let the varied coordinate range over all of `K^V`, forcing the named correction to be constant.
5. Independent boundary-bank bijections preserve functional independence. Therefore all five corrections must be constant, which is equivalent to five translations. Conversely, their endpoint offset `B c` is removable by separate translations within the original output banks.

The resulting iff-translations theorem and its zero-preserving iff-identity corollary are correct within the stated frozen-surrounding-word and fixed-bank scope. They do not imply rigidity under coupled recoding of other internal forms or under added communication.

No mathematical flaw was found. This review does not certify the still-running independent source checker or replace its eventual receipt. I authored the preceding linear five-message result; this is an independent review of root's new all-functions extension, not an assertion of independent authorship of the original finite witnesses. Prepared for @CubeJerry with substantial OpenAI assistance.
