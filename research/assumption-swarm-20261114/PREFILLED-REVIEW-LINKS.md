# Prefilled review links

Each link opens a pull-request comparison against `CrocSwap/integer-mult-bounds:main` with the original title and a substantive description already filled in. Expand the preview to read the exact prefilled body. The pinned full draft contains the complete proof, dependency attribution, source pins and validation details.

These descriptions summarize the existing published packages; their scientific results, branches and pinned drafts are unchanged. Validation statements below report the packages' recorded evidence, not new scientific replays performed for this editorial update. All 27 URLs were checked for exact title/body encoding and unchanged comparison targets. The signed-in PR form has not been rendered for these expanded URLs; no upstream PR was submitted.

## 1. Determine exact ordinary Toeplitz generator counts for tensor Gaussian kernels and their inverses

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/tensor-gaussian-displacement-rank-20261114?quick_pull=1&title=Determine+exact+ordinary+Toeplitz+generator+counts+for+tensor+Gaussian+kernels+and+their+inverses&body=%23%23%20Contribution%20and%20significance%0A%0AFlattening%20a%20separable%20Gaussian%20tensor%20does%20not%20preserve%20a%20short%20ordinary%20Toeplitz%20generator%20representation.%20For%20normalized%20shifted%20factors%20of%20dimensions%20n_i%3E%3D2%2C%20total%20dimension%20T%20and%20fastest%20axis%20f%2C%20both%20the%20tensor%20and%20its%20inverse%20have%20exact%20ordinary%20Sylvester%20and%20Stein%20displacement%20rank%202T%2Fn_f.%20This%20is%20also%20the%20exact%20minimum%20number%20of%20L(u)U(v)%20terms%3B%20the%20best%20lexicographic%20axis%20order%20gives%202T%2Fmax(n_i).%0A%0AExplicit%20boundary%20minors%2C%20matching%20support%20bounds%20and%20inverse%20identities%20prove%20the%20result.%20This%20adds%20the%20flattened%20representation%20calculation%20to%20the%20retained%20shallow-inverse%20mechanism%20and%20the%20one-axis%20contracts%20of%20%235566%2F%235571%2F%236905.%20It%20does%20not%20repackage%20the%20serial%20factor-of-axes%20budget%20as%20a%20new%20result.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Ftensor-gaussian-displacement-rank%60%0A%0ARecorded%20checks%20cover%2048%20generic%20forward%20cases%2C%2047%20generic%20inverse%20cases%2C%2011%20Gaussian%20tensors%2C%2022%20exact%20generator%20reconstructions%2C%20six%20axis%20orders%20and%20six%20scope%20controls.%20Rational%20elimination%20and%20independent%20Bareiss%20determinants%20corroborate%20PROOF.md%3B%20a%20separate%20proof%20review%20is%20included.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AArbitrary%20coordinate%20permutations%2C%20approximate%20rank%2C%20paid%20gauges%20and%20the%20complete%20recovery%20budget%20are%20outside%20this%20theorem.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F326844a3e0c570fdafa4f3737095cd37154743a6%2Fresearch%2Ftensor-gaussian-displacement-rank%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/326844a3e0c570fdafa4f3737095cd37154743a6/research/tensor-gaussian-displacement-rank/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

Flattening a separable Gaussian tensor does not preserve a short ordinary Toeplitz generator representation. For normalized shifted factors of dimensions n_i>=2, total dimension T and fastest axis f, both the tensor and its inverse have exact ordinary Sylvester and Stein displacement rank 2T/n_f. This is also the exact minimum number of L(u)U(v) terms; the best lexicographic axis order gives 2T/max(n_i).

Explicit boundary minors, matching support bounds and inverse identities prove the result. This adds the flattened representation calculation to the retained shallow-inverse mechanism and the one-axis contracts of #5566/#5571/#6905. It does not repackage the serial factor-of-axes budget as a new result.

## Verification

`python3 -B scripts/research_package.py --package research/tensor-gaussian-displacement-rank`

Recorded checks cover 48 generic forward cases, 47 generic inverse cases, 11 Gaussian tensors, 22 exact generator reconstructions, six axis orders and six scope controls. Rational elimination and independent Bareiss determinants corroborate PROOF.md; a separate proof review is included.

## Scope and remaining obligations

Arbitrary coordinate permutations, approximate rank, paid gauges and the complete recovery budget are outside this theorem.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/326844a3e0c570fdafa4f3737095cd37154743a6/research/tensor-gaussian-displacement-rank/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 2. Implement the complete old-format native packing bridge with literal strided transport and restored owners

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/selected-move-packed-codec-20261114?quick_pull=1&title=Implement+the+complete+old-format+native+packing+bridge+with+literal+strided+transport+and+restored+owners&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20native%20providers%20require%20packed%20Gamma6%20packets%2C%20while%20the%20older%20caller%20supplies%20a%2023-field%20descriptor%20and%20three-bit-coded%20numerical%20records.%20%237578%20supplies%20the%20semantic%20correspondence%20but%20leaves%20the%20physical%20conversion%20and%20strided%20transport%20open.%0A%0AThis%20package%20implements%20the%20complete%20entrance%20and%20inverse%20return%20as%20one%20input-independent%206%2C003-location%2C%2043-tape%20graph.%20It%20parses%20all%20old%20fields%2C%20infers%20width%20and%20coefficient%20multiplicity%2C%20gathers%20all%209f%20selected%20bits%2C%20preserves%20spectators%20and%20stages%20the%20result%20before%20committing%20to%20the%20original%20owner.%20Successful%20execution%20restores%20every%20private%20body%20and%20head.%20Complete%20time%20is%20at%20most%202%5E20((9f%2B1)V%2BE%2B1)%2C%20with%20added%20history%20at%20most%2064(V%2BE%2B1).%0A%0AThe%20contribution%20is%20the%20paid%20format%2Ftransport%20boundary%3B%20the%20semantic%20permutation%2C%20old%20positive%20service%20and%20packed%20arithmetic%20remain%20credited%20predecessor%20work.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fselected-move-packed-codec%60%0A%0ARecorded%20normal%2Foptimized%20checks%20cover%20four%20full%20f%3D1%20packets%2C%20five%20strided%20subprogram%20cases%2C%20owner%2Fhead%20retirement%2C%20thirteen%20fault%20controls%20and%20ten%20source%20mutations.%20Complete%20f%3E1%20and%20K%3E1%20packets%20are%20unrun%3B%20these%20codec%20fixtures%20do%20not%20execute%20native%20C.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0ASupplied%20legal%20geometry%2C%20blank%20banks%20and%20a%20successful%20same-width%20service%20return%20remain%20premises.%20Caller%2FHOME%20integration%2C%20failure%20cleanup%20and%20accelerated%20nonleaf%20costs%20remain%20open.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F30497f40d89f2a137a4bc31a4fee1229b9af1440%2Fresearch%2Fselected-move-packed-codec%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/30497f40d89f2a137a4bc31a4fee1229b9af1440/research/selected-move-packed-codec/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The native providers require packed Gamma6 packets, while the older caller supplies a 23-field descriptor and three-bit-coded numerical records. #7578 supplies the semantic correspondence but leaves the physical conversion and strided transport open.

This package implements the complete entrance and inverse return as one input-independent 6,003-location, 43-tape graph. It parses all old fields, infers width and coefficient multiplicity, gathers all 9f selected bits, preserves spectators and stages the result before committing to the original owner. Successful execution restores every private body and head. Complete time is at most 2^20((9f+1)V+E+1), with added history at most 64(V+E+1).

The contribution is the paid format/transport boundary; the semantic permutation, old positive service and packed arithmetic remain credited predecessor work.

## Verification

`python3 -B scripts/research_package.py --package research/selected-move-packed-codec`

Recorded normal/optimized checks cover four full f=1 packets, five strided subprogram cases, owner/head retirement, thirteen fault controls and ten source mutations. Complete f>1 and K>1 packets are unrun; these codec fixtures do not execute native C.

## Scope and remaining obligations

Supplied legal geometry, blank banks and a successful same-width service return remain premises. Caller/HOME integration, failure cleanup and accelerated nonleaf costs remain open.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/30497f40d89f2a137a4bc31a4fee1229b9af1440/research/selected-move-packed-codec/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 3. Supply uniform typed initialization and complete retirement for every selected raw-native owned lifetime

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/selected-owned-gamma-init-20261114?quick_pull=1&title=Supply+uniform+typed+initialization+and+complete+retirement+for+every+selected+raw-native+owned+lifetime&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20permanent%20HOME%20dispatcher%20and%20native%20packet%20services%20lacked%20a%20uniform%20typed-zero%20initializer.%20A%20fixed%20four-tape%20graph%20now%20initializes%20an%20exclusively%20inactive%20owned%20body%20from%20a%20live%20common-format%20header%20donor%2C%20preserves%20donor%20values%20and%20retires%20all%20private%20guides.%20Arbitrary%20correlated%20inactive%20contents%20are%20overwritten%20completely.%0A%0AZero-frame%20covariance%20allows%20the%20donor%20to%20have%20a%20different%20frame.%20The%20source%20audit%20binds%20the%20graph%20to%20all%2054%20INIT%2FCLEAR%20lifetimes%20on%2051%20raw%20labels%2C%20with%20donor0%20live%20at%20each%20INIT.%20INIT%20costs%20at%20most%204F%2B8%20transitions%3B%20complete%20CLEAR%20costs%202F%2B4.%20Reservation%2C%20delivery%2C%20copies%2C%20restoration%20and%20earlier%20history%20remain%20charged.%0A%0AThis%20closes%20the%20local%20typed-initialization%20interface%20left%20by%20%237565%2F%237567%2C%20while%20retaining%20%237564's%20distinct%20nonzero-transform%20domain.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fselected-owned-gamma-init%60%0A%0ARecorded%20checks%20include%20a%20complete%20f%3D2%20packet%20with%20524%2C300%20body%20bits%2C%20widths%201%2F2%2F3%2F17%2C%20a%202%2C049-bit-length%20cutoff%20and%20a%20nonzero%20SUB%20join.%20Controls%20cover%20ownership%2C%20aliasing%2C%20malformed%20Gamma%2C%20wrong%20frames%20and%20partial%20CLEAR.%20Separate%20sparse-tape%2Fsource-inventory%20review%20includes%20a%20missing-write%20control.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AAn%20already%20valid%20common-format%20boundary%20remains%20required.%20Root%20production%2C%20packing%2C%20precision%2C%20full%20chronological%20execution%20and%20compiler%20closure%20are%20not%20established.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F28fc921807f867302b2f43cb0696645f18094307%2Fresearch%2Fselected-owned-gamma-init%2FPR-BODY.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/28fc921807f867302b2f43cb0696645f18094307/research/selected-owned-gamma-init/PR-BODY.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The permanent HOME dispatcher and native packet services lacked a uniform typed-zero initializer. A fixed four-tape graph now initializes an exclusively inactive owned body from a live common-format header donor, preserves donor values and retires all private guides. Arbitrary correlated inactive contents are overwritten completely.

Zero-frame covariance allows the donor to have a different frame. The source audit binds the graph to all 54 INIT/CLEAR lifetimes on 51 raw labels, with donor0 live at each INIT. INIT costs at most 4F+8 transitions; complete CLEAR costs 2F+4. Reservation, delivery, copies, restoration and earlier history remain charged.

This closes the local typed-initialization interface left by #7565/#7567, while retaining #7564's distinct nonzero-transform domain.

## Verification

`python3 -B scripts/research_package.py --package research/selected-owned-gamma-init`

Recorded checks include a complete f=2 packet with 524,300 body bits, widths 1/2/3/17, a 2,049-bit-length cutoff and a nonzero SUB join. Controls cover ownership, aliasing, malformed Gamma, wrong frames and partial CLEAR. Separate sparse-tape/source-inventory review includes a missing-write control.

## Scope and remaining obligations

An already valid common-format boundary remains required. Root production, packing, precision, full chronological execution and compiler closure are not established.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/28fc921807f867302b2f43cb0696645f18094307/research/selected-owned-gamma-init/PR-BODY.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 4. Prove that Cp-bit rounding preserves the ordinary generator obstruction for normalized Gaussian tensors

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/gaussian-generator-rounding-margin-20261114?quick_pull=1&title=Prove+that+Cp-bit+rounding+preserves+the+ordinary+generator+obstruction+for+normalized+Gaussian+tensors&body=%23%23%20Contribution%20and%20significance%0A%0AExact%20rank%20alone%20cannot%20exclude%20shorter%20representations%20after%20rounding.%20This%20package%20supplies%20explicit%20forward%20and%20inverse%20approximation%20margins%20for%20the%20normalized%20Gaussian%20tensor's%20Stein%20boundary%20minor%3A%20approximations%20within%20those%20margins%20still%20require%20at%20least%202T%2Fn_fast%20ordinary%20Toeplitz%20generator%20terms.%0A%0AThe%20forward%20threshold%20is%201%2F(2K)%2C%20using%20an%20explicit%20boundary%20inverse-norm%20bound.%20Schur%20factorizations%20and%20persymmetry%20give%20the%20inverse%20threshold.%20Under%20polynomial%20local%20dimensions%2C%20a%20phase%20gap%20bounded%20below%20by%20a%20constant%20times%20p%5E-2%20and%20g%3C%3Dp%5Ebeta%20with%20fixed%20beta%3C1%2C%20both%20logarithmic%20margin%20costs%20are%20O(g%20log%20p)%3Do(p).%20The%20inequalities%20cover%20direct%20entry%20rounding%2C%20factor-table%20rounding%20and%20exact%20inverses%20of%20rounded%20factors.%0A%0AThis%20adds%20conditioning%20and%20the%20Cp-bit%20precision%20bridge%20to%20the%20exact%20boundary-minor%20predecessor%2C%20preserving%20the%20retained%20accretivity%20and%20fine-prime%20credits.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fgaussian-generator-rounding-margin%60%0A%0ARecorded%20checks%20cover%2027%20arbitrary-A%20fixtures%2C%20six%20Gaussian%20tensors%2C%2039%20rational%20PSD%20gap%20certificates%2C%2039%20perturbations%2C%2039%20direct%20roundings%20and%20six%20factor-table%20roundings.%20Six%20controls%20include%20actual%20low-precision%20rank%20loss%2C%20forged%20gaps%2C%20beta%3D1%20and%20zero%20half-shift%20gap.%20Separate%20review%20checks%20inverse%20and%20precision%20arguments.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AThese%20are%20representation%20bounds%20for%20the%20stated%20normalized%20kernels%2C%20not%20runtime%20or%20arbitrary-order%20bounds.%20Actual%20periodic%20matrices%2C%20paid%20gauges%20and%20full%20source%20conversion%20remain%20open.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F575491d5fc353eac26010e45e9ced60fc9870017%2Fresearch%2Fgaussian-generator-rounding-margin%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/575491d5fc353eac26010e45e9ced60fc9870017/research/gaussian-generator-rounding-margin/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

Exact rank alone cannot exclude shorter representations after rounding. This package supplies explicit forward and inverse approximation margins for the normalized Gaussian tensor's Stein boundary minor: approximations within those margins still require at least 2T/n_fast ordinary Toeplitz generator terms.

The forward threshold is 1/(2K), using an explicit boundary inverse-norm bound. Schur factorizations and persymmetry give the inverse threshold. Under polynomial local dimensions, a phase gap bounded below by a constant times p^-2 and g<=p^beta with fixed beta<1, both logarithmic margin costs are O(g log p)=o(p). The inequalities cover direct entry rounding, factor-table rounding and exact inverses of rounded factors.

This adds conditioning and the Cp-bit precision bridge to the exact boundary-minor predecessor, preserving the retained accretivity and fine-prime credits.

## Verification

`python3 -B scripts/research_package.py --package research/gaussian-generator-rounding-margin`

Recorded checks cover 27 arbitrary-A fixtures, six Gaussian tensors, 39 rational PSD gap certificates, 39 perturbations, 39 direct roundings and six factor-table roundings. Six controls include actual low-precision rank loss, forged gaps, beta=1 and zero half-shift gap. Separate review checks inverse and precision arguments.

## Scope and remaining obligations

These are representation bounds for the stated normalized kernels, not runtime or arbitrary-order bounds. Actual periodic matrices, paid gauges and full source conversion remain open.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/575491d5fc353eac26010e45e9ced60fc9870017/research/gaussian-generator-rounding-margin/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 5. Produce typed owned zero packets directly from the retained OLD23 source with complete linear costs

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/old-source-owned-zero-20261114?quick_pull=1&title=Produce+typed+owned+zero+packets+directly+from+the+retained+OLD23+source+with+complete+linear+costs&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20preceding%20typed-zero%20initializer%20requires%20a%20live%20already-packed%20Gamma6%20donor.%20This%20package%20removes%20that%20local%20premise%20by%20producing%20a%20separate%20charged%20owned%20zero%20directly%20from%20the%20retained%20OLD23%20field%20and%20context.%0A%0AA%20fixed%204%2C803-location%2C%2043-tape%20graph%20parses%20the%20actual%20descriptor%2C%20infers%20width%2C%20derives%20coefficient%20multiplicity%2C%20validates%20the%20old%20frontier%20and%20emits%20the%20exact%20Gamma6%20header%20and%20scientific%20zero.%20Old%20field%2Fcontext%20receive%20no%20writes%3B%20heads%2C%20guides%20and%20exteriors%20are%20restored.%20Time%20is%20at%20most%202%5E20(V_old%2BE_old%2B1)%2C%20with%20added%20history%20at%20most%2064(V_old%2BE_old%2B3).%20CLEAR%20erases%20the%20full%20packet%20while%20retaining%20its%20physical%20owner%20and%20historical%20backing.%0A%0AThe%20graph%20reuses%20the%20paid%20codec's%20unchanged%20parsing%20primitives.%20Zero%20invariance%20makes%20its%20nonzero%20permutation%2Freturn%20passes%20unnecessary%3B%20those%20predecessor%20results%20are%20not%20claimed%20anew.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fold-source-owned-zero%60%0A%0ARecorded%20primary%20checks%20cover%20five%20full%20packets%2C%20fresh%20and%20correlated%20inactive%20HOME%20bodies%2C%20nonzero%20dirty%20CLEAR%20and%20fifteen%20controls.%20Separate%20hardware%2Faccounting%20review%20checks%20two%20full%20packets%20and%20a%20successful-but-wrong%20missing-overwrite%20mutant.%20Complete%20f%3E1%20packets%20are%20explicitly%20unrun.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AAccessible%20valid%20OLD23%20input%2C%20disjoint%20guarded%20windows%2C%20native%20stock%2Fview%20admission%20and%20later%20service%20domains%20remain%20external.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F1ce8a1622b89f925a81815f8158eb8fc95977868%2Fresearch%2Fold-source-owned-zero%2FPR-BODY.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/1ce8a1622b89f925a81815f8158eb8fc95977868/research/old-source-owned-zero/PR-BODY.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The preceding typed-zero initializer requires a live already-packed Gamma6 donor. This package removes that local premise by producing a separate charged owned zero directly from the retained OLD23 field and context.

A fixed 4,803-location, 43-tape graph parses the actual descriptor, infers width, derives coefficient multiplicity, validates the old frontier and emits the exact Gamma6 header and scientific zero. Old field/context receive no writes; heads, guides and exteriors are restored. Time is at most 2^20(V_old+E_old+1), with added history at most 64(V_old+E_old+3). CLEAR erases the full packet while retaining its physical owner and historical backing.

The graph reuses the paid codec's unchanged parsing primitives. Zero invariance makes its nonzero permutation/return passes unnecessary; those predecessor results are not claimed anew.

## Verification

`python3 -B scripts/research_package.py --package research/old-source-owned-zero`

Recorded primary checks cover five full packets, fresh and correlated inactive HOME bodies, nonzero dirty CLEAR and fifteen controls. Separate hardware/accounting review checks two full packets and a successful-but-wrong missing-overwrite mutant. Complete f>1 packets are explicitly unrun.

## Scope and remaining obligations

Accessible valid OLD23 input, disjoint guarded windows, native stock/view admission and later service domains remain external.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/1ce8a1622b89f925a81815f8158eb8fc95977868/research/old-source-owned-zero/PR-BODY.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 6. Selected MOVE24472: join the paid old-coded bridge and actual all-column positive C leaf in one 70-tape service

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/selected-move-old-coded-c-20261114?quick_pull=1&title=Selected+MOVE24472%3A+join+the+paid+old-coded+bridge+and+actual+all-column+positive+C+leaf+in+one+70-tape+service&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20paid%20OLD23%20bridge%20previously%20used%20an%20abstract%20same-width%20continuation.%20This%20package%20joins%20it%20to%20the%20actual%20unchanged%20%237429%20positive%20C%20graph%3A%20one%20uninterrupted%2012%2C829-instruction%2C%2070-tape%20program%20parses%20the%20old%20ABI%2C%20executes%20all%20f%20C%20axes%20and%20returns%20the%20result%20to%20the%20original%20old-coded%20owner.%0A%0AThe%20composition%20reconciles%20alphabets%2C%20header%2Fdata%20ports%2C%20added%20owners%2C%20guards%20and%20return%20continuations.%20Rows%2C%20coefficient%20multiplicity%2C%20spectators%2C%20common%20quantum%20and%20absolute%20phase%20are%20preserved%20without%20an%20intervening%20host%20callback.%20Complete%20time%20is%20at%20most%202%5E24(f%20V_old%2BE%2B1)%2C%20with%20added%20history%20at%20most%20128(V_old%2BE%2B1)%2C%20including%20codecs%2C%2018f%20address%20passes%2C%20arithmetic%2C%20staging%20and%20cleanup.%0A%0AThe%20new%20contribution%20is%20the%20physical%20composition%20and%20complete%20central%20return%3B%20codec%20and%20C%20arithmetic%20are%20retained%20predecessor%20results.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fselected-move-old-coded-c%60%0A%0ARecorded%20checks%20include%20three%20full%20f%3D1%20packets%20against%20a%20direct%20old-address%20integer%20oracle%2C%20thirteen%20source%20mutations%2C%20domain%20and%20linkage%20controls%2C%20and%20a%20separate%20sparse-CPU%2Fexact-complex%20replay.%20The%20f%3D2%20endpoint%20obstruction%20is%20algebraic%3B%20no%20complete%20f%3E1%20joined%20replay%20is%20claimed.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AThis%20is%20the%20central%20C%20service%2C%20not%20a%20complete%20MOVE.%20Every-prefix%20integrality%2Frange%2C%20blank%20windows%2C%20monomials%2C%20source%20binding%20and%20recursive%20returns%20remain%20explicit.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2Fb5e3cfbb67b6c908f0eb605a9f872af807c86dcf%2Fresearch%2Fselected-move-old-coded-c%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/b5e3cfbb67b6c908f0eb605a9f872af807c86dcf/research/selected-move-old-coded-c/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The paid OLD23 bridge previously used an abstract same-width continuation. This package joins it to the actual unchanged #7429 positive C graph: one uninterrupted 12,829-instruction, 70-tape program parses the old ABI, executes all f C axes and returns the result to the original old-coded owner.

The composition reconciles alphabets, header/data ports, added owners, guards and return continuations. Rows, coefficient multiplicity, spectators, common quantum and absolute phase are preserved without an intervening host callback. Complete time is at most 2^24(f V_old+E+1), with added history at most 128(V_old+E+1), including codecs, 18f address passes, arithmetic, staging and cleanup.

The new contribution is the physical composition and complete central return; codec and C arithmetic are retained predecessor results.

## Verification

`python3 -B scripts/research_package.py --package research/selected-move-old-coded-c`

Recorded checks include three full f=1 packets against a direct old-address integer oracle, thirteen source mutations, domain and linkage controls, and a separate sparse-CPU/exact-complex replay. The f=2 endpoint obstruction is algebraic; no complete f>1 joined replay is claimed.

## Scope and remaining obligations

This is the central C service, not a complete MOVE. Every-prefix integrality/range, blank windows, monomials, source binding and recursive returns remain explicit.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/b5e3cfbb67b6c908f0eb605a9f872af807c86dcf/research/selected-move-old-coded-c/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 7. Selected MOVE24472: execute the complete frozen native move through a paid old-coded entrance and original-owner return

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/selected-move-old-coded-full-20261114?quick_pull=1&title=Selected+MOVE24472%3A+execute+the+complete+frozen+native+move+through+a+paid+old-coded+entrance+and+original-owner+return&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20full%20selected%20MOVE24472%20already%20existed%20on%20a%20supplied%20packed%20field.%20This%20package%20supplies%20its%20paid%20OLD23%20entrance%20and%20original-owner%20return%20by%20joining%20the%20bridge%20to%20the%20unchanged%20complete%20core%20in%20one%2088%2C816-instruction%2C%2072-tape%20program.%0A%0AIt%20executes%20both%20monomials%2C%20translation%20and%20all%20central%20C%20axes%20for%20selected%20event%20%5BMOVE%2C415%2C3%2C99%2Cfalse%5D%2C%20preserving%20rows%2C%20coefficients%2C%20spectators%2C%20quantum%20and%20absolute%20phase.%20All%20heads%20return%20and%20private%20bodies%2Ftemporary%20guards%20retire.%20Time%20is%20at%20most%202%5E25(f%20V_old%2BE%2B1)%2C%20with%20added%20history%20at%20most%202048(V_old%2BE%2B1).%0A%0AThe%20proof%20establishes%20admission%20before%20the%20right%20monomial%20from%20the%20selected%20complete-root%20invariant.%20A%20separate%20counterexample%20shows%20endpoint%20fit%20alone%20permits%20an%20overflowing%20phase%20negation.%20This%20adds%20the%20complete%20old%20physical%20boundary%20to%20%237563%2C%20rather%20than%20a%20new%20packed%20MOVE%20algorithm.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fselected-move-old-coded-full%60%0A%0ARecorded%20full%20packets%20take%2040%2C936%2C214%20and%20109%2C257%2C735%20transitions%20against%20a%20direct%20source-frame%20oracle.%20Controls%20cover%20phase%20overflow%2C%20nonintegrality%2C%20truncation%2C%20aliases%2C%2032%20source%20mutations%20and%20physically%20returning%20phase%2Ftranslation%20deletions.%20Separate%20admission%2Fcomposition%20review%20is%20included%3B%20full%20f%3E1%20and%20K%3E1%20joins%20are%20unrun.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AOnly%20one%20MOVE%20boundary%20is%20closed.%20Initial%20owners%2Fdescriptors%2C%20root%20provenance%2C%20frame%20dispatch%2C%20stock%2C%20failure%20retirement%20and%20full%20recursive%2Fnonleaf%20closure%20remain%20open.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F6c76eaa184bb59724ac5bfdc5aa35a80afca73ae%2Fresearch%2Fselected-move-old-coded-full%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/6c76eaa184bb59724ac5bfdc5aa35a80afca73ae/research/selected-move-old-coded-full/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The full selected MOVE24472 already existed on a supplied packed field. This package supplies its paid OLD23 entrance and original-owner return by joining the bridge to the unchanged complete core in one 88,816-instruction, 72-tape program.

It executes both monomials, translation and all central C axes for selected event [MOVE,415,3,99,false], preserving rows, coefficients, spectators, quantum and absolute phase. All heads return and private bodies/temporary guards retire. Time is at most 2^25(f V_old+E+1), with added history at most 2048(V_old+E+1).

The proof establishes admission before the right monomial from the selected complete-root invariant. A separate counterexample shows endpoint fit alone permits an overflowing phase negation. This adds the complete old physical boundary to #7563, rather than a new packed MOVE algorithm.

## Verification

`python3 -B scripts/research_package.py --package research/selected-move-old-coded-full`

Recorded full packets take 40,936,214 and 109,257,735 transitions against a direct source-frame oracle. Controls cover phase overflow, nonintegrality, truncation, aliases, 32 source mutations and physically returning phase/translation deletions. Separate admission/composition review is included; full f>1 and K>1 joins are unrun.

## Scope and remaining obligations

Only one MOVE boundary is closed. Initial owners/descriptors, root provenance, frame dispatch, stock, failure retirement and full recursive/nonleaf closure remain open.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/6c76eaa184bb59724ac5bfdc5aa35a80afca73ae/research/selected-move-old-coded-full/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 8. Construct orbit orderings with superpolynomial Gaussian tensor generator savings and explicit cost limits

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/gaussian-orbit-generator-order-20261114?quick_pull=1&title=Construct+orbit+orderings+with+superpolynomial+Gaussian+tensor+generator+savings+and+explicit+cost+limits&body=%23%23%20Contribution%20and%20significance%0A%0ALexicographic%20Gaussian%20rank%20bounds%20leave%20arbitrary%20simultaneous%20row%2Fcolumn%20orders%20open.%20This%20package%20constructs%20symmetry-orbit%20orders%20with%20smaller%20ordinary%20Stein%20generator%20bounds%20for%20forward%20matrices%20and%20exact%20inverses.%0A%0AFor%20repeated%20n-by-n%20factors%2C%20disjoint%20odd-prime%20coordinate%20rotations%20with%20product%20P%20give%20exactly%20c%3D(T%2FP)%20product(1%2B(p_i-1)n%5E(1-p_i))%20orbits%2C%20at%20most%20exp(8%2F9)T%2FP%2C%20and%20at%20most%202c%20generator%20terms.%20A%20uniform%20Bertrand-prime%20choice%20yields%20superpolynomial%20savings%20in%20the%20number%20of%20axes%20for%20fixed%20n.%20A%20complementary%20centrosymmetric%20construction%20gives%20a%20T%2Fell%20bound%20and%20an%20explicit%2016-point%20rank-four%20example.%0A%0AThe%20contribution%20is%20the%20generator%20consequence%2C%20exact%20kernel%20scope%20and%20paid%20precision%2Fcost%20boundary.%20Necklace%20counting%2C%20prime%20existence%20and%20complemented-rotation%20facts%20retain%20their%20classical%20attribution.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fgaussian-orbit-generator-order%60%0A%0ARecorded%20checks%20compare%20cycle%20enumeration%20with%20Burnside%2Fproduct%20counts%2C%20reconstruct%20rational%20generators%2C%20check%20a%20256-point%20finite-field%20inverse%20and%20test%20Bertrand%20families%20through%20d%3D4096.%20Fifteen%20primary%20controls%20and%20a%20separate%20Cartesian-necklace%20checker%20address%20false%20symmetry%2C%20period%20and%20correction%20claims.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0ADense%20materialization%20still%20uses%20Theta(T%5E2%2FP)%20slots.%20Order%20generation%2C%20layout%20changes%2C%20access%20and%20restoration%20remain%20paid%3B%20unmatched%20shifts%20and%20a%20complete%20source%20caller%20are%20not%20admitted.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F8f1a09fb4f696bd5f20e1953210936308571416e%2Fresearch%2Fgaussian-orbit-generator-order%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/8f1a09fb4f696bd5f20e1953210936308571416e/research/gaussian-orbit-generator-order/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

Lexicographic Gaussian rank bounds leave arbitrary simultaneous row/column orders open. This package constructs symmetry-orbit orders with smaller ordinary Stein generator bounds for forward matrices and exact inverses.

For repeated n-by-n factors, disjoint odd-prime coordinate rotations with product P give exactly c=(T/P) product(1+(p_i-1)n^(1-p_i)) orbits, at most exp(8/9)T/P, and at most 2c generator terms. A uniform Bertrand-prime choice yields superpolynomial savings in the number of axes for fixed n. A complementary centrosymmetric construction gives a T/ell bound and an explicit 16-point rank-four example.

The contribution is the generator consequence, exact kernel scope and paid precision/cost boundary. Necklace counting, prime existence and complemented-rotation facts retain their classical attribution.

## Verification

`python3 -B scripts/research_package.py --package research/gaussian-orbit-generator-order`

Recorded checks compare cycle enumeration with Burnside/product counts, reconstruct rational generators, check a 256-point finite-field inverse and test Bertrand families through d=4096. Fifteen primary controls and a separate Cartesian-necklace checker address false symmetry, period and correction claims.

## Scope and remaining obligations

Dense materialization still uses Theta(T^2/P) slots. Order generation, layout changes, access and restoration remain paid; unmatched shifts and a complete source caller are not admitted.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/8f1a09fb4f696bd5f20e1953210936308571416e/research/gaussian-orbit-generator-order/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 9. Selected owned1526: join literal OLD23 initialization, all six scientific contacts and dirty erasure on one permanent HOME

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/selected-owned-lifetime-protocol-20261114?quick_pull=1&title=Selected+owned1526%3A+join+literal+OLD23+initialization%2C+all+six+scientific+contacts+and+dirty+erasure+on+one+permanent+HOME&body=%23%23%20Contribution%20and%20significance%0A%0AThis%20package%20joins%20all%20eight%20contacts%20of%20the%20selected%20owned1526%20lifetime%20on%20one%20permanent%20HOME%3A%20OLD23%20typed-zero%20initialization%2C%20four%20SUBs%2C%20rank-two%20MOVE28141%2C%20outgoing%20ADD28159%20and%20dirty%20CLEAR37618.%20The%20fixed%20table%20has%20121%2C322%20states%20on%2044%20tapes.%0A%0AIt%20composes%20the%20published%20zero%20producer%20with%20unchanged%20signed%20arithmetic%20and%20the%20actual%20rank-two%20child%2C%20paying%20donor-bank%20scans%2C%20work%20copies%2C%20delivery%20and%20retirement.%20Complete%20local%20time%20is%20bounded%20by%202%5E20(V_old%2BE_old%2B1)%2B2%5E24(fV%2BE_gamma%2B1)%2B32768(F%2B1)%2B128%3B%20continuation%20time%2Fhistory%20are%20additional%20and%20erased%20backing%20is%20never%20refunded.%0A%0AThis%20closes%20the%20local%20contact%20protocol%2C%20not%20the%20full%20source%20interval%3A%20its%209%2C574%20intervening%20events%20still%20require%20actual%20donor%20production%2C%20frame%20changes%20and%20receiver%20initialization.%20The%20source%20chronology%20is%20retained%20explicitly.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fselected-owned-lifetime-protocol%60%0A%0ARecorded%20nonzero%20f%3D1%20replay%20uses%2034%2C069%2C475%20transitions%20and%20checks%20every%20head%2C%20owner%2C%20receiver%20update%20and%20dirty%20erase.%20Controls%20cover%20phase%2Fsign%2C%20overflow%2C%20cutoff%2C%20headers%2C%20aliases%20and%20stale%20continuations.%20Independent%20interface%20review%20and%20full%20interval%20re-extraction%20are%20recorded%3B%20no%20f%3D2%20or%20actual-gap%20execution%20is%20claimed.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0ASource%20acquisition%2C%20gap%20implementations%2C%20stock%20admission%2C%20dispatch%2C%20rejection%20cleanup%20and%20accelerated%20nonleaf%20cost%20remain%20open.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F53e0a6d689d8c3a840a055eedc59f7f2e9c14022%2Fresearch%2Fselected-owned-lifetime-protocol%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/53e0a6d689d8c3a840a055eedc59f7f2e9c14022/research/selected-owned-lifetime-protocol/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

This package joins all eight contacts of the selected owned1526 lifetime on one permanent HOME: OLD23 typed-zero initialization, four SUBs, rank-two MOVE28141, outgoing ADD28159 and dirty CLEAR37618. The fixed table has 121,322 states on 44 tapes.

It composes the published zero producer with unchanged signed arithmetic and the actual rank-two child, paying donor-bank scans, work copies, delivery and retirement. Complete local time is bounded by 2^20(V_old+E_old+1)+2^24(fV+E_gamma+1)+32768(F+1)+128; continuation time/history are additional and erased backing is never refunded.

This closes the local contact protocol, not the full source interval: its 9,574 intervening events still require actual donor production, frame changes and receiver initialization. The source chronology is retained explicitly.

## Verification

`python3 -B scripts/research_package.py --package research/selected-owned-lifetime-protocol`

Recorded nonzero f=1 replay uses 34,069,475 transitions and checks every head, owner, receiver update and dirty erase. Controls cover phase/sign, overflow, cutoff, headers, aliases and stale continuations. Independent interface review and full interval re-extraction are recorded; no f=2 or actual-gap execution is claimed.

## Scope and remaining obligations

Source acquisition, gap implementations, stock admission, dispatch, rejection cleanup and accelerated nonleaf cost remain open.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/53e0a6d689d8c3a840a055eedc59f7f2e9c14022/research/selected-owned-lifetime-protocol/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 10. Implement canonical padded-rotation switch queries as a restored fourteen-tape program with quadratic bit cost

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/literal-canonical-rotation-switch-20261114?quick_pull=1&title=Implement+canonical+padded-rotation+switch+queries+as+a+restored+fourteen-tape+program+with+quadratic+bit+cost&body=%23%23%20Contribution%20and%20significance%0A%0A%237504%20gives%20canonical%20padded-rotation%20Bene%C5%A1%20switch%20formulas%20but%20leaves%20their%20literal%20fixed-tape%20implementation%20open.%20This%20package%20implements%20that%20interface%20in%20one%20input-independent%202%2C096-location%2C%20fourteen-tape%20program.%0A%0AFor%20legal%20encoded%20h%2Cs%2Ca%2Cj%2Cx%2C%20it%20returns%20the%20canonical%20row-j%20bit%20at%20the%20current%20wire%20x%20in%20at%20most%201024(h%2B3)%5E2%20transitions%2C%20adding%20at%20most%2016(h%2B4)%20historical%20cells.%20It%20preserves%20five%20borrowed%20descriptors%2C%20restores%20all%20heads%20and%20retires%20eight%20private%20bodies%2C%20leaving%20one%20owned%20Boolean.%20Domain%20validation%20precedes%20identity%20shortcuts.%0A%0AThe%20new%20work%20is%20the%20physical%20lowering%20and%20full%20ownership%2Fcost%20proof.%20Nick%20Petalas's%20formulas%20and%20the%20original%20%234100%20canonical%20compiler%20retain%20their%20credit%3B%20the%20latter%20supplies%20an%20independent%20expected-bit%20oracle.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fliteral-canonical-rotation-switch%60%0A%0ARecorded%20checks%20cover%201%2C566%20queries%20across%2049%20small%20networks%2C%20all%20544%20h%3D5%2Cs%3D17%2Cj%3D6%20entries%2C%20malformed%20domains%2C%20graph%20mutants%20and%20depths%20through%20h%3D129.%20Independent%20sparse%20interpretation%20and%20a%20parity-union-find%20network%20oracle%20reproduce%20the%20queries%20and%20detect%20a%20returning%20wrong-bit%20mutation.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0ADescriptors%20and%20working%20windows%20are%20supplied.%20Current%20CRT%20production%2C%20payload%20consumption%20and%20full%20routing%20are%20separate%3B%20repeated%20queries%20retain%20their%20quadratic%20bill.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F56335a406469fad85e88ff72820d506d8bea6f63%2Fresearch%2Fliteral-canonical-rotation-switch%2FPR-BODY.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/56335a406469fad85e88ff72820d506d8bea6f63/research/literal-canonical-rotation-switch/PR-BODY.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

#7504 gives canonical padded-rotation Beneš switch formulas but leaves their literal fixed-tape implementation open. This package implements that interface in one input-independent 2,096-location, fourteen-tape program.

For legal encoded h,s,a,j,x, it returns the canonical row-j bit at the current wire x in at most 1024(h+3)^2 transitions, adding at most 16(h+4) historical cells. It preserves five borrowed descriptors, restores all heads and retires eight private bodies, leaving one owned Boolean. Domain validation precedes identity shortcuts.

The new work is the physical lowering and full ownership/cost proof. Nick Petalas's formulas and the original #4100 canonical compiler retain their credit; the latter supplies an independent expected-bit oracle.

## Verification

`python3 -B scripts/research_package.py --package research/literal-canonical-rotation-switch`

Recorded checks cover 1,566 queries across 49 small networks, all 544 h=5,s=17,j=6 entries, malformed domains, graph mutants and depths through h=129. Independent sparse interpretation and a parity-union-find network oracle reproduce the queries and detect a returning wrong-bit mutation.

## Scope and remaining obligations

Descriptors and working windows are supplied. Current CRT production, payload consumption and full routing are separate; repeated queries retain their quadratic bill.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/56335a406469fad85e88ff72820d506d8bea6f63/research/literal-canonical-rotation-switch/PR-BODY.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 11. Classify Gaussian tensor symmetries and prove the optimal scale of orbit certificates with explicit rounding and materialization limits

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/gaussian-orbit-certificate-scale-20261114?quick_pull=1&title=Classify+Gaussian+tensor+symmetries+and+prove+the+optimal+scale+of+orbit+certificates+with+explicit+rounding+and+materialization+limits&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20preceding%20orbit%20construction%20left%20open%20the%20best%20possible%20savings%20within%20its%20global-symmetry%20mechanism.%20This%20package%20classifies%20every%20exact%20vertex-permutation%20symmetry%20of%20the%20homogeneous%20Gaussian%20kernel%20H_xy%3Dq%5E(%7C%7Cx-y%7C%7C%C2%B2)v%5E(sum(x-y))%3A%20coordinate%20permutations%20for%20v!%3D1%2C%20and%20signed%20coordinate%20permutations%20for%20v%3D1.%20The%20inverse%20has%20the%20same%20group.%0A%0AWith%20g(d)%20the%20maximum%20permutation%20order%2C%20the%20optimal%20cycle%20count%20is%20Theta(T%2Fg(d))%2C%20with%20explicit%20constants%20and%20prime-power%20constructions.%20The%20specified%20dense%20boundary-vector%20format%20consequently%20has%20size%20Theta(T%C2%B2%2Fg(d))%3DT%5E(2-o(1))%20for%20fixed%20local%20dimension.%20Selector%2C%20enumeration%20and%20both%20layout%20permutations%20are%20paid.%0A%0AExplicit%20separation%20conditions%20extend%20containment%20to%20perturbed%20tables%3B%20a%20common%20rounding%20rule%20preserves%20the%20construction.%20Classical%20Landau%20and%20necklace%20results%20are%20credited.%20This%20resolves%20the%20certificate-class%20optimum%2C%20not%20the%20all-order%20displacement-rank%20problem.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fgaussian-orbit-certificate-scale%60%0A%0ARecorded%20checks%20include%207%2C337%20partitions%2C%20770%20signed%2Funsigned%20orbit%20fixtures%2C%20768%20constructions%2C%20594%20correction%20cases%2C%20thirteen%20small%20automorphism%20searches%20and%20ten%20controls.%20Independent%20enumeration%2Fknapsack%2Forbit%20checks%20corroborate%20the%20written%20proof%20and%20expose%20false%20finite-cycle%20and%20rounding%20extensions.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AThe%20lower%20bound%20is%20specific%20to%20full-cycle%20certificates%20in%20the%20dense%20format.%20Implicit%20generators%2C%20actual%20source%20matching%2C%20inverse%20conditioning%20and%20complete%20recovery%20remain%20open.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F2ae2fa14eeefe301652f62313b137a97036ab13d%2Fresearch%2Fgaussian-orbit-certificate-scale%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/2ae2fa14eeefe301652f62313b137a97036ab13d/research/gaussian-orbit-certificate-scale/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The preceding orbit construction left open the best possible savings within its global-symmetry mechanism. This package classifies every exact vertex-permutation symmetry of the homogeneous Gaussian kernel H_xy=q^(||x-y||²)v^(sum(x-y)): coordinate permutations for v!=1, and signed coordinate permutations for v=1. The inverse has the same group.

With g(d) the maximum permutation order, the optimal cycle count is Theta(T/g(d)), with explicit constants and prime-power constructions. The specified dense boundary-vector format consequently has size Theta(T²/g(d))=T^(2-o(1)) for fixed local dimension. Selector, enumeration and both layout permutations are paid.

Explicit separation conditions extend containment to perturbed tables; a common rounding rule preserves the construction. Classical Landau and necklace results are credited. This resolves the certificate-class optimum, not the all-order displacement-rank problem.

## Verification

`python3 -B scripts/research_package.py --package research/gaussian-orbit-certificate-scale`

Recorded checks include 7,337 partitions, 770 signed/unsigned orbit fixtures, 768 constructions, 594 correction cases, thirteen small automorphism searches and ten controls. Independent enumeration/knapsack/orbit checks corroborate the written proof and expose false finite-cycle and rounding extensions.

## Scope and remaining obligations

The lower bound is specific to full-cycle certificates in the dense format. Implicit generators, actual source matching, inverse conditioning and complete recovery remain open.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/2ae2fa14eeefe301652f62313b137a97036ab13d/research/gaussian-orbit-certificate-scale/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 12. Connect current CRT offset leases to restored direct switch queries and the original payload radix mover

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/current-crt-direct-switch-consumer-20261114?quick_pull=1&title=Connect+current+CRT+offset+leases+to+restored+direct+switch+queries+and+the+original+payload+radix+mover&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20literal%20switch%20predicate%20previously%20consumed%20supplied%20descriptors%20and%20returned%20an%20unused%20Boolean.%20This%20package%20connects%20it%20to%20the%20actual%20%237388%20encoded%20CRT%20leaf%3A%20paid%20source%2Fheader%20scans%20prepare%20the%20query%2C%20and%20the%20physical%20output%20updates%20the%20current%20wire%20before%20the%20original%20key%2Fradix%20path%20consumes%20it.%0A%0AA%20fixed%202%2C500-instruction%2C%20twenty-tape%20adapter%20preserves%20borrowed%20descriptors%20and%20restores%20fourteen%20private%20owners.%20Its%20exact%20added%20overhead%20is%2030p%2B74h%2B6%20bit_length(h)%2B10k%2B261.%20Including%20the%20unchanged%20predicate%2C%20time%20is%20at%20most%201024(h%2B3)%5E2%2B128(p%2Bh%2B3)%2C%20with%20added%20history%20at%20most%20p%2B16(h%2B4).%0A%0AThe%20contribution%20is%20the%20representation%2Fconsumption%20adapter%20and%20actual%20source%20substitution.%20Canonical%20formulas%2C%20CRT%20arithmetic%20and%20radix%20remain%20predecessor%20work.%20Literal%20and%20outer%20symbol-action%20costs%20remain%20separate.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fcurrent-crt-direct-switch-consumer%60%0A%0ARecorded%20coverage%20includes%201%2C566%20small%20canonical%20entries%2C%20544%20required%20row%20points%2C%20a%202%2C049-bit%20precision%2Fhistory%20case%2C%20five%20actual%20roundtrips%20and%20fourteen%20controls.%20Independent%20sparse%20interpretation%20checks%20current-offset%2Fwire%20freshness%2C%20consumption%20and%20exact%20source%20restoration%3B%20retained%20numerical%2Fradix%20providers%20are%20not%20independently%20reimplemented.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AAcquisition%2C%20grants%2C%20source%20geometry%20and%20outer%20source%2Frow%20controllers%20remain%20supplied.%20There%20is%20no%20common%20whole-caller%20tariff%20or%20amortized%20ROM%20speedup%20theorem.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2Fb12dfb5acc7fdf7d23bce671df0b97228be9ed87%2Fresearch%2Fcurrent-crt-direct-switch-consumer%2FPR-BODY.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/b12dfb5acc7fdf7d23bce671df0b97228be9ed87/research/current-crt-direct-switch-consumer/PR-BODY.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The literal switch predicate previously consumed supplied descriptors and returned an unused Boolean. This package connects it to the actual #7388 encoded CRT leaf: paid source/header scans prepare the query, and the physical output updates the current wire before the original key/radix path consumes it.

A fixed 2,500-instruction, twenty-tape adapter preserves borrowed descriptors and restores fourteen private owners. Its exact added overhead is 30p+74h+6 bit_length(h)+10k+261. Including the unchanged predicate, time is at most 1024(h+3)^2+128(p+h+3), with added history at most p+16(h+4).

The contribution is the representation/consumption adapter and actual source substitution. Canonical formulas, CRT arithmetic and radix remain predecessor work. Literal and outer symbol-action costs remain separate.

## Verification

`python3 -B scripts/research_package.py --package research/current-crt-direct-switch-consumer`

Recorded coverage includes 1,566 small canonical entries, 544 required row points, a 2,049-bit precision/history case, five actual roundtrips and fourteen controls. Independent sparse interpretation checks current-offset/wire freshness, consumption and exact source restoration; retained numerical/radix providers are not independently reimplemented.

## Scope and remaining obligations

Acquisition, grants, source geometry and outer source/row controllers remain supplied. There is no common whole-caller tariff or amortized ROM speedup theorem.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/b12dfb5acc7fdf7d23bce671df0b97228be9ed87/research/current-crt-direct-switch-consumer/PR-BODY.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 13. Selected owned1526: produce donor1349's actual frame137 image and feed the unchanged first SUB after returning the same physical owner

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/selected-first-donor-producer-20261114?quick_pull=1&title=Selected+owned1526%3A+produce+donor1349%27s+actual+frame137+image+and+feed+the+unchanged+first+SUB+after+returning+the+same+physical+owner&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20owned1526%20contact%20protocol%20assumes%20the%20transformed%20first%20donor.%20This%20package%20replaces%20that%20premise%20with%20actual%20MOVE28039%3A%20donor1349%20moves%20from%20frame3%20to%20frame601%2C%20returns%20to%20the%20same%20physical%20field%20and%20feeds%20unchanged%20SUB28041.%20The%20INIT%2Fproducer%2FSUB%20graph%20has%2071%2C524%20states%20on%2044%20tapes.%0A%0AThe%20source-specific%20circuit%20D%2CG%5E-1%2CC0%2CG%2CD%20includes%20the%20correct%20absolute%20phase%20and%20preserves%20the%20owned%20HOME%20and%20borrowed%20capabilities.%20Admission%20requires%20matching%20geometry%2C%20quantum%20and%20current%20frames%2C%20f%3C%3Dcutoff%2C%20safe%20phase%20negations%2C%20integral%2Frange-safe%20C%20prefixes%20and%20a%20fitting%20SUB.%20Endpoint%20fit%20alone%20is%20insufficient.%0A%0AThe%20new%20result%20is%20production%20of%20this%20donor%20at%20its%20actual%20source%20boundary%3B%20generic%20C%2C%20signed%20arithmetic%20and%20the%20later%20rank-two%20MOVE%20remain%20credited%20predecessor%20work.%20ADD28038%20and%20ADD28040%20are%20still%20charged%20external%20continuations.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fselected-first-donor-producer%60%0A%0ARecorded%20bounded%20nonzero%20execution%20is%20complemented%20by%20independent%20derivation%20of%20all%20512%20source%20columns%2C%20comparison%20of%2075%2C391%20relocation%20instructions%2C%20owner%2Fcost%20proofs%20and%20authenticated%20source%20chronology.%20Review%20includes%20an%20endpoint-fit%2Fphase-overflow%20family.%20Later%20rank-two%20admission%20is%20explicitly%20not%20inferred%20from%20first-SUB%20success.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0APre-MOVE%20packet%20acquisition%2C%20the%20two%20public%20ADDs%2C%20other%20donors%2C%20stock%2C%20failure%20cleanup%20and%20full%20dispatch%20remain%20open.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2Fa94e3f2ee0360202943b577ff8cd76245f6aa9ed%2Fresearch%2Fselected-first-donor-producer%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/a94e3f2ee0360202943b577ff8cd76245f6aa9ed/research/selected-first-donor-producer/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The owned1526 contact protocol assumes the transformed first donor. This package replaces that premise with actual MOVE28039: donor1349 moves from frame3 to frame601, returns to the same physical field and feeds unchanged SUB28041. The INIT/producer/SUB graph has 71,524 states on 44 tapes.

The source-specific circuit D,G^-1,C0,G,D includes the correct absolute phase and preserves the owned HOME and borrowed capabilities. Admission requires matching geometry, quantum and current frames, f<=cutoff, safe phase negations, integral/range-safe C prefixes and a fitting SUB. Endpoint fit alone is insufficient.

The new result is production of this donor at its actual source boundary; generic C, signed arithmetic and the later rank-two MOVE remain credited predecessor work. ADD28038 and ADD28040 are still charged external continuations.

## Verification

`python3 -B scripts/research_package.py --package research/selected-first-donor-producer`

Recorded bounded nonzero execution is complemented by independent derivation of all 512 source columns, comparison of 75,391 relocation instructions, owner/cost proofs and authenticated source chronology. Review includes an endpoint-fit/phase-overflow family. Later rank-two admission is explicitly not inferred from first-SUB success.

## Scope and remaining obligations

Pre-MOVE packet acquisition, the two public ADDs, other donors, stock, failure cleanup and full dispatch remain open.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/a94e3f2ee0360202943b577ff8cd76245f6aa9ed/research/selected-first-donor-producer/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 14. Retained Gaussian interiors: classify heterogeneous tensor symmetries and rule out long-orbit dense certificate savings under fine-prime widths

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/heterogeneous-gaussian-symmetries-20261114?quick_pull=1&title=Retained+Gaussian+interiors%3A+classify+heterogeneous+tensor+symmetries+and+rule+out+long-orbit+dense+certificate+savings+under+fine-prime+widths&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20homogeneous%20orbit%20savings%20require%20interchangeable%20factors.%20This%20package%20classifies%20every%20exact%20simultaneous%20permutation%20symmetry%20of%20normalized%20heterogeneous%20Gaussian%20tensors%3A%20only%20signed%20coordinate%20permutations%20preserving%20dimensions%2C%20widths%20and%20signed%20shifts%20are%20possible.%0A%0ADistinct%20widths%20leave%20only%20zero-shift%20reflections%2C%20so%20each%20symmetry%20has%20order%20at%20most%20two%20and%20at%20least%20T%2F2%20cycles.%20If%20every%20shift%20is%20nonzero%2C%20only%20the%20identity%20remains.%20The%20inverse%20has%20the%20same%20group%2C%20and%20the%20proof%20gives%20the%20exact%20minimum%20cycle%20count.%0A%0AThe%20retained%20fine-prime%20broad%2Fnarrow%20widths%20are%20distinct%2C%20closing%20the%20specific%20transfer%20question%20for%20that%20normalized%20source%20family.%20Explicit%20colored-edge%20separation%20conditions%20extend%20symmetry%20containment%20to%20sufficiently%20accurate%20stored%20tables.%20This%20is%20a%20restriction%20on%20the%20dense%20symmetry-cycle%20mechanism%2C%20not%20an%20all-order%20rank%20theorem.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fheterogeneous-gaussian-symmetries%60%0A%0ARecorded%20primary%20searches%20inspect%20243%2C414%20vertex%20permutations%2C%20with%20rigorous%20dyadic%20rounding%20checks.%20Independent%20rational-entry%20review%20covers%20888%2C560%20permutations%2C%20inverse%20elimination%20and%20eight%20controls.%20Equal-width%20cycles%2C%20coarse%20rounding%2C%20tiny%20shifts%20and%20broken%20gap%20guards%20are%20tested.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AIdentification%20is%20restricted%20to%20matching%20square%20normalized%20grids.%20Actual%20caller%2Ferror%20admission%2C%20implicit%20alternatives%20and%20general%20runtime%20bounds%20remain%20open.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2Fbe76d6ae53fc887f977a04ceaa6ef56bb9e98fb7%2Fresearch%2Fheterogeneous-gaussian-symmetries%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/be76d6ae53fc887f977a04ceaa6ef56bb9e98fb7/research/heterogeneous-gaussian-symmetries/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The homogeneous orbit savings require interchangeable factors. This package classifies every exact simultaneous permutation symmetry of normalized heterogeneous Gaussian tensors: only signed coordinate permutations preserving dimensions, widths and signed shifts are possible.

Distinct widths leave only zero-shift reflections, so each symmetry has order at most two and at least T/2 cycles. If every shift is nonzero, only the identity remains. The inverse has the same group, and the proof gives the exact minimum cycle count.

The retained fine-prime broad/narrow widths are distinct, closing the specific transfer question for that normalized source family. Explicit colored-edge separation conditions extend symmetry containment to sufficiently accurate stored tables. This is a restriction on the dense symmetry-cycle mechanism, not an all-order rank theorem.

## Verification

`python3 -B scripts/research_package.py --package research/heterogeneous-gaussian-symmetries`

Recorded primary searches inspect 243,414 vertex permutations, with rigorous dyadic rounding checks. Independent rational-entry review covers 888,560 permutations, inverse elimination and eight controls. Equal-width cycles, coarse rounding, tiny shifts and broken gap guards are tested.

## Scope and remaining obligations

Identification is restricted to matching square normalized grids. Actual caller/error admission, implicit alternatives and general runtime bounds remain open.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/be76d6ae53fc887f977a04ceaa6ef56bb9e98fb7/research/heterogeneous-gaussian-symmetries/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 15. Execute complete forward and inverse CRT wire routes with a fixed twenty-owner controller and exact costs

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/literal-current-wire-row-controller-20261114?quick_pull=1&title=Execute+complete+forward+and+inverse+CRT+wire+routes+with+a+fixed+twenty-owner+controller+and+exact+costs&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20direct%20point%20query%20was%20literal%2C%20but%20the%20per-wire%20row%20loop%20still%20used%20outer%20symbol-action%20control.%20This%20package%20replaces%20that%20loop%20with%20a%20fixed%2010%2C123-instruction%2C%20twenty-owner%20graph%20with%20forward%20and%20inverse%20entries.%0A%0AExactly%202h-1%20unchanged%20point%20calls%20operate%20on%20the%20current%20physical%20address.%20Row%20initialization%2Fupdates%2C%20cursor%20movement%2C%20calls%2C%20returns%20and%20retirement%20are%20literal.%20Additional%20controller%20costs%20are%2014p%2B36h-12-7%20popcount(2h-2)%20forward%20and%2014p%2B72h-38-14%20popcount(2h-2)%20inverse%3B%20every%20point-call%20bill%20remains%20additional.%20Private%20history%20is%20a%20fixed%20per-owner%20O(p%2Bh)%20union.%0A%0AThe%20graph%20joins%20the%20actual%20%237388%20route_address%20seam%20and%20original%20payload%2Fradix%20path.%20This%20adds%20complete%20row%20control%20and%20its%20invoice%3B%20point%20arithmetic%20and%20canonical%20routing%20formulas%20remain%20predecessor%20results.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fliteral-current-wire-row-controller%60%0A%0ARecorded%20checks%20cover%201%2C764%20full%20routes%2C%20large%20precision%2Fhistory%20boundaries%2C%20seventeen%20controls%20and%20two%20actual%20roundtrips.%20Separate%20sparse%20interpretation%20checks%20fifty%20routes%2C%20366%20calls%20and%20returning%20semantic%20corruptions.%20All%20embedded%20instructions%20and%20return%20edges%20are%20compared%20with%20the%20pinned%20predecessor.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0ANumerical%2Fheader%20production%2C%20all-wire%20enumeration%2C%20grants%20and%20remaining%20payload%2Fradix%20providers%20remain%20external.%20No%20full%20CRT%20or%20common%20complete%20tariff%20is%20claimed.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F4ccf407db96c7797dc3c83d90b033551f7d52c76%2Fresearch%2Fliteral-current-wire-row-controller%2FPR-BODY.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/4ccf407db96c7797dc3c83d90b033551f7d52c76/research/literal-current-wire-row-controller/PR-BODY.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The direct point query was literal, but the per-wire row loop still used outer symbol-action control. This package replaces that loop with a fixed 10,123-instruction, twenty-owner graph with forward and inverse entries.

Exactly 2h-1 unchanged point calls operate on the current physical address. Row initialization/updates, cursor movement, calls, returns and retirement are literal. Additional controller costs are 14p+36h-12-7 popcount(2h-2) forward and 14p+72h-38-14 popcount(2h-2) inverse; every point-call bill remains additional. Private history is a fixed per-owner O(p+h) union.

The graph joins the actual #7388 route_address seam and original payload/radix path. This adds complete row control and its invoice; point arithmetic and canonical routing formulas remain predecessor results.

## Verification

`python3 -B scripts/research_package.py --package research/literal-current-wire-row-controller`

Recorded checks cover 1,764 full routes, large precision/history boundaries, seventeen controls and two actual roundtrips. Separate sparse interpretation checks fifty routes, 366 calls and returning semantic corruptions. All embedded instructions and return edges are compared with the pinned predecessor.

## Scope and remaining obligations

Numerical/header production, all-wire enumeration, grants and remaining payload/radix providers remain external. No full CRT or common complete tariff is claimed.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/4ccf407db96c7797dc3c83d90b033551f7d52c76/research/literal-current-wire-row-controller/PR-BODY.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 16. Execute selected INIT28037 through SUB28041 in one literal first-gap graph with paid signed halving and public-owner restoration

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/selected-complete-first-gap-20261114?quick_pull=1&title=Execute+selected+INIT28037+through+SUB28041+in+one+literal+first-gap+graph+with+paid+signed+halving+and+public-owner+restoration&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20first-donor%20producer%20leaves%20two%20public%20ADDs%20as%20continuations.%20This%20package%20implements%20both%20and%20joins%20all%20five%20consecutive%20events%20INIT28037%20through%20SUB28041%20in%20one%2071%2C793-state%2C%2045-tape%20graph.%0A%0AA%20paid%20signed%20half-copy%20prepares%20the%20actual%201%2F2%20contact%2C%20retires%20its%20guides%20and%20invokes%20unchanged%20signed%20ADD%3B%20the%20second%20ADD%20consumes%20updated212.%20For%20initial%20A%3D212%2C%20B%3D449%2C%20C%3D124%20and%20X%3D1349%2C%20outputs%20are%20212%3DA%2BB%2F2%2C%20124%3DC%2BA%2BB%2F2%2C%20449%3DB%2C%201349%3DT137%5E(tensor%20f)X%20and%201526%3D-T137%5E(tensor%20f)X.%20Physical%20owners%20and%20all%20heads%20return.%0A%0ANew%20half-copy%2FADD%2Fdelivery%20work%20costs%20at%20most%2012334F%2B12370%3B%20the%20complete%20prefix%20invoice%20also%20includes%20OLD23%20INIT%20and%20donor%20production.%20All%20predecessor%20states%20are%20retained%20except%20two%20declared%20return%20edges.%20This%20closes%20one%20actual%20chronological%20gap%2C%20not%20the%20full%20lifetime.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fselected-complete-first-gap%60%0A%0ARecorded%20uninterrupted%20positive%20execution%20takes%2021%2C858%2C749%20transitions.%20Five%20half-packet%20and%2024%20bank%20cases%20supplement%20public-output%2C%20parity%2C%20overflow%20and%20returning-corruption%20controls.%20Independent%20sparse%20review%20checks%20arithmetic%20seams%2C%20exact%20embeddings%20and%20the%20uniform%20cost%20proof.%20Later%20failure%20does%20not%20roll%20back%20earlier%20committed%20events.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AEven%20B%20components%2C%20fitting%20sums%2C%20valid%20frames%2Fgrid%20and%20original%20MOVE%2FSUB%20admission%20remain%20required.%20Later%20lifetime%2C%20acquisition%20and%20complete%20dispatcher%20obligations%20remain%20open.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F5584607a0a19c62173841df712e655ff8c0d6160%2Fresearch%2Fselected-complete-first-gap%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/5584607a0a19c62173841df712e655ff8c0d6160/research/selected-complete-first-gap/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The first-donor producer leaves two public ADDs as continuations. This package implements both and joins all five consecutive events INIT28037 through SUB28041 in one 71,793-state, 45-tape graph.

A paid signed half-copy prepares the actual 1/2 contact, retires its guides and invokes unchanged signed ADD; the second ADD consumes updated212. For initial A=212, B=449, C=124 and X=1349, outputs are 212=A+B/2, 124=C+A+B/2, 449=B, 1349=T137^(tensor f)X and 1526=-T137^(tensor f)X. Physical owners and all heads return.

New half-copy/ADD/delivery work costs at most 12334F+12370; the complete prefix invoice also includes OLD23 INIT and donor production. All predecessor states are retained except two declared return edges. This closes one actual chronological gap, not the full lifetime.

## Verification

`python3 -B scripts/research_package.py --package research/selected-complete-first-gap`

Recorded uninterrupted positive execution takes 21,858,749 transitions. Five half-packet and 24 bank cases supplement public-output, parity, overflow and returning-corruption controls. Independent sparse review checks arithmetic seams, exact embeddings and the uniform cost proof. Later failure does not roll back earlier committed events.

## Scope and remaining obligations

Even B components, fitting sums, valid frames/grid and original MOVE/SUB admission remain required. Later lifetime, acquisition and complete dispatcher obligations remain open.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/5584607a0a19c62173841df712e655ff8c0d6160/research/selected-complete-first-gap/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 17. Generate every padded CRT destination key with one fixed physical pass and a paid payload-head return

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/literal-all-wire-crt-keys-20261114?quick_pull=1&title=Generate+every+padded+CRT+destination+key+with+one+fixed+physical+pass+and+a+paid+payload-head+return&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20current%20CRT%20caller%20still%20enumerates%20payload%20records%20and%20emits%20keys%20through%20a%20host%20loop.%20This%20package%20lowers%20that%20prepare_keys%20seam%20into%20a%20fixed%2021%2C135-instruction%20graph%20on%20twenty-two%20roles%2C%20invoking%20the%20unchanged%20whole-row%20controller%20and%20writing%20actual%20original%20key%20cells.%0A%0AFor%20N%3D2%5Eh%2C%20forward%2Finverse%20entries%20execute%20N%20complete%20routes%20and%20N(2h-1)%20point%20queries.%20Beyond%20the%20unchanged%20route%20bills%2C%20cost%20is%20N(156h%2B126)%2B18h%2B203%3B%20exactly%2013Nh%20key%20writes%20are%20validated.%20Opaque%20payloads%2C%20heads%20and%20historical%20unions%20are%20preserved.%0A%0AThe%20scope%20is%20the%20fixed%20thirteen-bit%20codeword%20with%20arbitrary%20twelve-bit%20payload%20ABI.%20Inverse%20keys%20do%20not%20undo%20arbitrary%20overwritten%20keys%3A%20sorted%20roundtrip%20restoration%20requires%20the%20original%20physical-position%20invariant.%20This%20adds%20all-wire%20physical%20control%20to%20the%20retained%20point%2Frow%2Fradix%20lineage.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fliteral-all-wire-crt-keys%60%0A%0ARecorded%20checks%20cover%20112%20full%20passes%2C%201%2C008%20routes%2C%206%2C096%20point%20queries%2C%2020%2C246%20embedded%20instructions%20and%20two%20source%2Fpayload%20roundtrips.%20Separate%20sparse%20review%20executes%20ten%20passes%20and%2039%20width%2Fcarry%20cases%2C%20plus%20semantic%2Fcleanup%20controls%20and%20exact%20invoice%20checks.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AGeneral%20payload%20widths%2C%20source%2Fheader%20acquisition%2C%20grants%20and%20remaining%20radix%2Fsource%20orchestration%20are%20outside%20scope.%20No%20common%20complete%20caller%20tariff%20or%20rollback%20guarantee%20is%20asserted.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2Ff789e7318ef89b26c2e358c4c1eb09ce93d21f73%2Fresearch%2Fliteral-all-wire-crt-keys%2FPR-BODY.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/f789e7318ef89b26c2e358c4c1eb09ce93d21f73/research/literal-all-wire-crt-keys/PR-BODY.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The current CRT caller still enumerates payload records and emits keys through a host loop. This package lowers that prepare_keys seam into a fixed 21,135-instruction graph on twenty-two roles, invoking the unchanged whole-row controller and writing actual original key cells.

For N=2^h, forward/inverse entries execute N complete routes and N(2h-1) point queries. Beyond the unchanged route bills, cost is N(156h+126)+18h+203; exactly 13Nh key writes are validated. Opaque payloads, heads and historical unions are preserved.

The scope is the fixed thirteen-bit codeword with arbitrary twelve-bit payload ABI. Inverse keys do not undo arbitrary overwritten keys: sorted roundtrip restoration requires the original physical-position invariant. This adds all-wire physical control to the retained point/row/radix lineage.

## Verification

`python3 -B scripts/research_package.py --package research/literal-all-wire-crt-keys`

Recorded checks cover 112 full passes, 1,008 routes, 6,096 point queries, 20,246 embedded instructions and two source/payload roundtrips. Separate sparse review executes ten passes and 39 width/carry cases, plus semantic/cleanup controls and exact invoice checks.

## Scope and remaining obligations

General payload widths, source/header acquisition, grants and remaining radix/source orchestration are outside scope. No common complete caller tariff or rollback guarantee is asserted.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/f789e7318ef89b26c2e358c4c1eb09ce93d21f73/research/literal-all-wire-crt-keys/PR-BODY.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 18. Prove diagonal-gauge and inverse-error bounds for symmetry cycles of physical fine-prime Gaussian blocks

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/gauged-physical-gaussian-symmetries-20261114?quick_pull=1&title=Prove+diagonal-gauge+and+inverse-error+bounds+for+symmetry+cycles+of+physical+fine-prime+Gaussian+blocks&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20heterogeneous%20symmetry%20theorem%20covers%20normalized%20ideal%20kernels.%20This%20package%20extends%20the%20scoped%20analysis%20to%20diagonal%20gauges%2C%20physical%20capped%20blocks%20and%20inverse-entry%20error%2C%20while%20retaining%20conditioning%20and%20storage%20costs.%0A%0AFor%20G%3DLHR%2C%20normalized%20pair%20products%20recover%20the%20Gaussian%20metric.%20The%20monomial%20centralizer%20is%20cAPA%5E-1%2C%20with%20P%20preserving%20that%20metric%20and%20actual%20diagonal%20products.%20Distinct%20widths%20force%20reflection%20permutations%3B%20their%20minimum%20cycle%20count%20across%20gauges%20is%20ceil(T%2F2)%2C%20requiring%20at%20least%202T%20ceil(T%2F2)%20slots%20in%20the%20specified%20dense%20format.%20This%20bounds%20vertex%20cycles%2C%20not%20weighted%20monomial%20order.%0A%0AExplicit%20physical%20entry%2Fdiagonal%20bounds%20support%20ratio%20error%2024M%20epsilon%2Fdelta%C2%B2.%20Dimension-paid%20inverse%20transfer%20gives%20forward%20error%20at%20most%202T%C2%B3M%C2%B2epsilon%20under%20stated%20conditions.%20Classical%20diagonal%20invariants%20and%20Neumann%20identities%20remain%20credited%20ingredients.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fgauged-physical-gaussian-symmetries%60%0A%0ARecorded%20primary%20checks%20include%2081%2C464%20permutations%20per%20forward%2Finverse%20target%2C%20922%20physical%20exponent%20pairs%20and%20eleven%20controls.%20Separate%20rational-complex%20review%20checks%20commutators%2C%201%2C252%20source%20identities%2C%20precision%20inequalities%20and%20ten%20controls%20without%20author%20mathematical%20imports.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AOnly%20matching%20square%20all-broad%2Fall-narrow%20blocks%20with%20stated%20phase%20conditions%20are%20covered.%20Actual%20table%20production%2C%20periodic%2Fcross-cell%20interfaces%2C%20caller%20admission%20and%20access%20costs%20remain%20open.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F85c29864062620f16e428c12f291f63632dd5a66%2Fresearch%2Fgauged-physical-gaussian-symmetries%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/85c29864062620f16e428c12f291f63632dd5a66/research/gauged-physical-gaussian-symmetries/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The heterogeneous symmetry theorem covers normalized ideal kernels. This package extends the scoped analysis to diagonal gauges, physical capped blocks and inverse-entry error, while retaining conditioning and storage costs.

For G=LHR, normalized pair products recover the Gaussian metric. The monomial centralizer is cAPA^-1, with P preserving that metric and actual diagonal products. Distinct widths force reflection permutations; their minimum cycle count across gauges is ceil(T/2), requiring at least 2T ceil(T/2) slots in the specified dense format. This bounds vertex cycles, not weighted monomial order.

Explicit physical entry/diagonal bounds support ratio error 24M epsilon/delta². Dimension-paid inverse transfer gives forward error at most 2T³M²epsilon under stated conditions. Classical diagonal invariants and Neumann identities remain credited ingredients.

## Verification

`python3 -B scripts/research_package.py --package research/gauged-physical-gaussian-symmetries`

Recorded primary checks include 81,464 permutations per forward/inverse target, 922 physical exponent pairs and eleven controls. Separate rational-complex review checks commutators, 1,252 source identities, precision inequalities and ten controls without author mathematical imports.

## Scope and remaining obligations

Only matching square all-broad/all-narrow blocks with stated phase conditions are covered. Actual table production, periodic/cross-cell interfaces, caller admission and access costs remain open.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/85c29864062620f16e428c12f291f63632dd5a66/research/gauged-physical-gaussian-symmetries/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 19. Prove a uniform generic Stein-rank floor for every ordering of binary Gaussian tensors and their exact inverses

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/arbitrary-order-binary-gaussian-rank-20261114?quick_pull=1&title=Prove+a+uniform+generic+Stein-rank+floor+for+every+ordering+of+binary+Gaussian+tensors+and+their+exact+inverses&body=%23%23%20Contribution%20and%20significance%0A%0AEarlier%20rank%20results%20fixed%20lexicographic%20order%3B%20orbit%20results%20fixed%20a%20symmetry%20mechanism.%20This%20package%20proves%20a%20generic%20rank%20floor%20for%20every%20simultaneous%20vertex%20order%20of%20the%20unshifted%20binary%20tensor%20H%3Dtensor_i%5B%5B1%2Cq_i%5D%2C%5Bq_i%2C1%5D%5D.%0A%0AFor%20N%3D2%5Ed%2C%20one%20proper%20real%20algebraic%20exceptional%20set%20suffices%20so%20that%20every%20ordered%20forward%20matrix%20and%20exact%20inverse%20has%20Stein%20rank%20at%20least%202%20ceil((N%2B3)%2F5).%20Good%20tuples%20are%20dense%20and%20full-measure%20in%20(0%2C1)%5Ed.%20XOR%20translation%20matchings%20supply%20isolated%20unit-minor%20coefficients%3B%20complementary%20cycle%20counts%20give%20the%20floor%2C%20and%20a%20Schur%20identity%20handles%20inverses.%0A%0AAn%20exact%20ordinary%20lower%2Fupper%20Toeplitz%20sum%20needs%20at%20least%20that%20many%20terms%2C%20yielding%20Omega(N%C2%B2)%20slots%20when%20both%20full%20generator%20vectors%20are%20stored.%20This%20closes%20an%20arbitrary-order%20loophole%20for%20the%20stated%20generic%20family.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Farbitrary-order-binary-gaussian-rank%60%0A%0ARecorded%20checks%20enumerate%205%2C047%20normalized%20orders%20and%2035%2C299%20masks%2C%20unit%20minors%2C%20characteristic-two%20ranks%2C%20polynomial%20coefficients%20and%20eleven%20controls.%20Separate%20symbolic%2Frational%20review%20checks%20expanded%20minors%2C%20larger%20graphs%20and%20exceptional%20determinants.%20Written%20proof%20establishes%20the%20universal%20claim.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AActual%20fine-prime%20tuples%20are%20not%20proved%20generic%2C%20and%20full%20rank%20is%20not%20universal.%20Physical%20phases%2C%20rounding%20margins%2C%20implicit%20representations%20and%20general%20runtime%20remain%20outside%20scope.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F085b30f8e036f69421d5953d0993ac4974ec3f24%2Fresearch%2Farbitrary-order-binary-gaussian-rank%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/085b30f8e036f69421d5953d0993ac4974ec3f24/research/arbitrary-order-binary-gaussian-rank/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

Earlier rank results fixed lexicographic order; orbit results fixed a symmetry mechanism. This package proves a generic rank floor for every simultaneous vertex order of the unshifted binary tensor H=tensor_i[[1,q_i],[q_i,1]].

For N=2^d, one proper real algebraic exceptional set suffices so that every ordered forward matrix and exact inverse has Stein rank at least 2 ceil((N+3)/5). Good tuples are dense and full-measure in (0,1)^d. XOR translation matchings supply isolated unit-minor coefficients; complementary cycle counts give the floor, and a Schur identity handles inverses.

An exact ordinary lower/upper Toeplitz sum needs at least that many terms, yielding Omega(N²) slots when both full generator vectors are stored. This closes an arbitrary-order loophole for the stated generic family.

## Verification

`python3 -B scripts/research_package.py --package research/arbitrary-order-binary-gaussian-rank`

Recorded checks enumerate 5,047 normalized orders and 35,299 masks, unit minors, characteristic-two ranks, polynomial coefficients and eleven controls. Separate symbolic/rational review checks expanded minors, larger graphs and exceptional determinants. Written proof establishes the universal claim.

## Scope and remaining obligations

Actual fine-prime tuples are not proved generic, and full rank is not universal. Physical phases, rounding margins, implicit representations and general runtime remain outside scope.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/085b30f8e036f69421d5953d0993ac4974ec3f24/research/arbitrary-order-binary-gaussian-rank/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 20. Construct current CRT leaf headers from encoded source streams with paid prefix scans, exact retirement, and the unchanged complete key pass

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/literal-current-crt-headers-20261114?quick_pull=1&title=Construct+current+CRT+leaf+headers+from+encoded+source+streams+with+paid+prefix+scans%2C+exact+retirement%2C+and+the+unchanged+complete+key+pass&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20actual%20CRT%20caller%20obtains%20five%20query%2Fcontroller%20headers%20through%20emit_headers.%20This%20package%20lowers%20that%20source%20controller%20and%20joins%20its%20output%20to%20the%20unchanged%20complete%20key%20pass%20in%20a%20fixed%2021%2C513-instruction%2C%2027-role%20graph.%0A%0AIt%20reads%20the%20encoded%20source%2C%20axis%20cursor%2C%20precision%20guide%20and%20numerical%20result%3B%20emits%20height%2C%20modulus%2C%20offset%2C%20zero-row%20and%20unary-width%20streams%3B%20restores%20borrowed%20heads%3B%20and%20retires%20all%20five%20outputs%20after%20the%20retained%20continuation.%20No%20decoded%20host-selected%20header%20or%20query%20loop%20is%20supplied.%0A%0AFor%20prefix%20count%20m%2C%20skipped-width%20sum%20U%2C%20current%20width%20h%20and%20precision%20p%2C%20BUILD%20costs%206ph%2B53p%2B41U%2B57m%2B42h%2B199-popcount(h)%3B%20retirement%20costs%2028p%2B7h%2B53.%20Prior%20scratch%20width%2Fhistory%20remains%20charged%20even%20when%20larger%20than%20p.%20This%20adds%20source-bound%20header%20control%20and%20exact%20accounting%2C%20not%20new%20source%20arithmetic%20or%20routing.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fliteral-current-crt-headers%60%0A%0ARecorded%20checks%20cover%2061%20packets%2C%20wide-prefix%2Flow-precision%20boundaries%2C%20two%20actual%20roundtrips%20and%2021%20controls.%20Independent%20sparse%20review%20checks%20fourteen%20header%20cases%2C%20four%20uninterrupted%20child%20joins%20and%20exact%20source%20seams.%20The%20meter%20audit%20confirms%20the%20predecessor%20already%20charged%20all%20592%20old%20header%20actions.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0ANumerical%20results%2C%20leases%2C%20grants%2C%20commit%20and%20radix%20remain%20providers.%20Fixed%20thirteen-bit%20payload%20encoding%20and%20matching%20actual%20precision%20guide%20remain%20requirements.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F4c7cee36538bb48dc2598806af2ca42554fa63c0%2Fresearch%2Fliteral-current-crt-headers%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/4c7cee36538bb48dc2598806af2ca42554fa63c0/research/literal-current-crt-headers/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The actual CRT caller obtains five query/controller headers through emit_headers. This package lowers that source controller and joins its output to the unchanged complete key pass in a fixed 21,513-instruction, 27-role graph.

It reads the encoded source, axis cursor, precision guide and numerical result; emits height, modulus, offset, zero-row and unary-width streams; restores borrowed heads; and retires all five outputs after the retained continuation. No decoded host-selected header or query loop is supplied.

For prefix count m, skipped-width sum U, current width h and precision p, BUILD costs 6ph+53p+41U+57m+42h+199-popcount(h); retirement costs 28p+7h+53. Prior scratch width/history remains charged even when larger than p. This adds source-bound header control and exact accounting, not new source arithmetic or routing.

## Verification

`python3 -B scripts/research_package.py --package research/literal-current-crt-headers`

Recorded checks cover 61 packets, wide-prefix/low-precision boundaries, two actual roundtrips and 21 controls. Independent sparse review checks fourteen header cases, four uninterrupted child joins and exact source seams. The meter audit confirms the predecessor already charged all 592 old header actions.

## Scope and remaining obligations

Numerical results, leases, grants, commit and radix remain providers. Fixed thirteen-bit payload encoding and matching actual precision guide remain requirements.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/4c7cee36538bb48dc2598806af2ca42554fa63c0/research/literal-current-crt-headers/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 21. Remove the generic-parameter premise for all-order Stein-rank bounds at exact fine-prime narrow-core widths

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/fine-prime-binary-core-rank-20261114?quick_pull=1&title=Remove+the+generic-parameter+premise+for+all-order+Stein-rank+bounds+at+exact+fine-prime+narrow-core+widths&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20generic%20all-order%20theorem%20does%20not%20establish%20nonvanishing%20at%20prescribed%20source%20parameters.%20This%20package%20removes%20that%20premise%20for%20exact%20unshifted%20fine-prime%20narrow%20cores%20q_i%3Dexp(-pi%20alpha%C2%B2%20t_i%2Fs_i)%2C%20with%20distinct%20odd%20primes%2C%20dyadic%20targets%20and%20positive%20integer%20alpha.%0A%0AEvery%20ordering%20of%20the%20N%3D2%5Eg%20tensor%20and%20exact%20inverse%20has%20Stein%20rank%20at%20least%20min(2%20ceil((N%2B3)%2F5)%2C%20min(s_i)-1).%20Trimmed%20principal%20minors%20obey%20individual%20degree%20guards%3B%20CRT%20separates%20their%20monomials%20in%20a%20common%20transcendental%20base.%20Each%20order%20is%20specialized%20separately%2C%20avoiding%20a%20product%20of%20N!%20minors%20that%20would%20lose%20the%20guard.%20No%20coprimality%20between%20alpha%20and%20s_i%20is%20needed.%0A%0AThis%20makes%20the%20predecessor%20floor%20pointwise%20up%20to%20an%20explicit%20prime%20cap.%20The%20full%20linear%20floor%20holds%20when%20N%3Cmin(s_i)%3B%20the%20physical%20shift%20and%20chirp%20are%20not%20silently%20restored.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Ffine-prime-binary-core-rank%60%0A%0ARecorded%20checks%20cover%2013%2C689%20exponent-box%20vectors%2C%20219%20trimmed%20minors%2C%20twelve%20symbolic%20specializations%2C%2048%20source%20identities%20and%20thirteen%20controls.%20Independent%20review%20checks%2053%20symbolic%20minors%2C%20119%20trims%20and%20eleven%20controls.%20No%20numerical%20transcendence%20oracle%20is%20used.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0ADiagonal%20similarity%20can%20change%20Stein%20rank.%20Physical%2Frounded%20transfer%2C%20minor%20magnitudes%2C%20larger%20sections%2C%20coefficient%20production%20and%20complete%20costs%20remain%20open.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2Fda06a3d10e06870a0279e33dd5056ded8d7e7a38%2Fresearch%2Ffine-prime-binary-core-rank%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/da06a3d10e06870a0279e33dd5056ded8d7e7a38/research/fine-prime-binary-core-rank/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The generic all-order theorem does not establish nonvanishing at prescribed source parameters. This package removes that premise for exact unshifted fine-prime narrow cores q_i=exp(-pi alpha² t_i/s_i), with distinct odd primes, dyadic targets and positive integer alpha.

Every ordering of the N=2^g tensor and exact inverse has Stein rank at least min(2 ceil((N+3)/5), min(s_i)-1). Trimmed principal minors obey individual degree guards; CRT separates their monomials in a common transcendental base. Each order is specialized separately, avoiding a product of N! minors that would lose the guard. No coprimality between alpha and s_i is needed.

This makes the predecessor floor pointwise up to an explicit prime cap. The full linear floor holds when N<min(s_i); the physical shift and chirp are not silently restored.

## Verification

`python3 -B scripts/research_package.py --package research/fine-prime-binary-core-rank`

Recorded checks cover 13,689 exponent-box vectors, 219 trimmed minors, twelve symbolic specializations, 48 source identities and thirteen controls. Independent review checks 53 symbolic minors, 119 trims and eleven controls. No numerical transcendence oracle is used.

## Scope and remaining obligations

Diagonal similarity can change Stein rank. Physical/rounded transfer, minor magnitudes, larger sections, coefficient production and complete costs remain open.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/da06a3d10e06870a0279e33dd5056ded8d7e7a38/research/fine-prime-binary-core-rank/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 22. Retain physical phase and chirp in all-order binary Stein-rank bounds at a positive density of source indices

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/selected-phase-binary-rank-20261114?quick_pull=1&title=Retain+physical+phase+and+chirp+in+all-order+binary+Stein-rank+bounds+at+a+positive+density+of+source+indices&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20exact%20core%20specialization%20leaves%20phase%2Fchirp%20transfer%20open.%20This%20package%20works%20directly%20with%20selected%20adjacent%20same-cell%20pairs%20of%20the%20retained%20column-normalized%2C%20unrounded%2C%20alias-deleted%20physical%20array%2C%20preserving%20phase%2Fchirp%20and%20the%20finite%20period.%0A%0AFor%20even%202%3C%3Dr%3C%3DR_N%3D2%20ceil((N%2B3)%2F5)%2C%20each%20axis%20has%20at%20least%20s-1-delta-2r%C2%B2-r%20good%20starting%20indices%20when%20positive.%20Every%20combination%20of%20selected%20pairs%20has%20Stein%20rank%20at%20least%20r%20in%20every%20order%2C%20and%20the%20same%20holds%20for%20its%20exact%20inverse.%20Under%20the%20retained%20fine-gap%20regime%2C%20r%3Dmin(R_N%2C2%20floor(sqrt(s_min)%2F4))%20permits%20at%20least%20s%2F3-1%20good%20indices%20per%20axis.%0A%0ADirected-degree%20collision%20exclusion%2C%20CRT%20and%20transcendence%20specialize%20the%20matching%20minors%20without%20assuming%20rank%20survives%20diagonal%20similarity.%20A%20sequential%20selector%20has%20an%20explicit%20paid%20polynomial%20bit-work%20bound%20and%20emits%20indices%20only.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fselected-phase-binary-rank%60%0A%0ARecorded%20checks%20cover%2093%20bounded%20cases%2C%206%2C680%20residues%2C%20184%2C488%20exponent-box%20values%2C%202%2C402%20source%20pairs%20and%20fourteen%20controls.%20Independent%20review%20checks%20135%20cases%2C%2048%20directed%20determinants%20and%20source%20fixtures.%20Finite%20evidence%20corroborates%20the%20written%20nonvanishing%20argument.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AArbitrary%20phases%2C%20larger%20tiles%2C%20periodic%20aliases%2C%20rounded%20storage%20and%20Cp-bit%20margins%20remain%20open.%20The%20selected%20tensor%20inverse%20is%20not%20a%20section%20of%20a%20larger%20inverse.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F0a6315b71a47b37a4faa2a4f555c5bc4e9e87811%2Fresearch%2Fselected-phase-binary-rank%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/0a6315b71a47b37a4faa2a4f555c5bc4e9e87811/research/selected-phase-binary-rank/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The exact core specialization leaves phase/chirp transfer open. This package works directly with selected adjacent same-cell pairs of the retained column-normalized, unrounded, alias-deleted physical array, preserving phase/chirp and the finite period.

For even 2<=r<=R_N=2 ceil((N+3)/5), each axis has at least s-1-delta-2r²-r good starting indices when positive. Every combination of selected pairs has Stein rank at least r in every order, and the same holds for its exact inverse. Under the retained fine-gap regime, r=min(R_N,2 floor(sqrt(s_min)/4)) permits at least s/3-1 good indices per axis.

Directed-degree collision exclusion, CRT and transcendence specialize the matching minors without assuming rank survives diagonal similarity. A sequential selector has an explicit paid polynomial bit-work bound and emits indices only.

## Verification

`python3 -B scripts/research_package.py --package research/selected-phase-binary-rank`

Recorded checks cover 93 bounded cases, 6,680 residues, 184,488 exponent-box values, 2,402 source pairs and fourteen controls. Independent review checks 135 cases, 48 directed determinants and source fixtures. Finite evidence corroborates the written nonvanishing argument.

## Scope and remaining obligations

Arbitrary phases, larger tiles, periodic aliases, rounded storage and Cp-bit margins remain open. The selected tensor inverse is not a section of a larger inverse.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/0a6315b71a47b37a4faa2a4f555c5bc4e9e87811/research/selected-phase-binary-rank/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 23. Implement the actual current CRT leaf division with literal owner dispatch and a proved allocator continuation

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/literal-current-crt-divmod-20261114?quick_pull=1&title=Implement+the+actual+current+CRT+leaf+division+with+literal+owner+dispatch+and+a+proved+allocator+continuation&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20encoded%20CRT%20division%20algorithm%20did%20not%20supply%20a%20literal%20call%20at%20changing%20physical%20allocator%20slots.%20This%20package%20binds%20one%20336%2C150-location%2C%2068-role%20divider%20to%20the%20actual%20singleton%20leaf's%20sixth%20raw%20division%2C%20identified%20as%20left%20modulus%20divmod%20right%20modulus.%0A%0AEight%20borrowed%20guards%2C%2056%20owned%20Word%20ports%20and%20four%20paid%20six-bit%20descriptors%20implement%20literal%20dispatch.%20The%20source%20precision%20guide%20establishes%20the%20unsigned%20high-bit%20margin.%20Setup%2C%20division%20and%20output%20retirement%20cost%20at%20most%202%5E14(P%2B2)%C2%B2%3B%20finite%20metadata%20and%20allocation%20remain%20separately%20charged.%0A%0AReplacing%20the%20call%20changes%20allocation%20events.%20A%20weak%20live%2Ffree-slot%20bijection%20proves%20the%20unchanged%20source%20continuation%20and%20unordered%20cleanup%2C%20charging%20histories%20on%20actual%20physical%20owners.%20The%20contribution%20is%20this%20actual-call%2Fownership%20interface%3B%20restoring%20division%20and%20CRT%20arithmetic%20remain%20predecessor%20results.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fliteral-current-crt-divmod%60%0A%0ARecorded%20checks%20cover%20every%20numerical%20access%20at%20all%2064%20slots%2C%20124%20arithmetic%20cases%20and%20six%20actual%20roundtrips%20with%2024%20allocator%20counterfactuals.%20Independent%20sparse%20review%20covers%2022%2C272%20dispatch%20paths%2C%20full%20lifecycles%2C%20two%20roundtrips%20and%20twelve%20bijections.%20Returning%20corruption%20and%20retirement%20faults%20are%20detected.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AOnly%20one%20numerical%20call%20is%20replaced.%20Other%20arithmetic%2C%20source%20control%2C%20metadata%20binding%2C%20grants%20and%20a%20common%20source%2Fradix%20tariff%20remain%20external.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2Fc4ab5dab6914a04cb86d1fe54eb763b35cc7eeb1%2Fresearch%2Fliteral-current-crt-divmod%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/c4ab5dab6914a04cb86d1fe54eb763b35cc7eeb1/research/literal-current-crt-divmod/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The encoded CRT division algorithm did not supply a literal call at changing physical allocator slots. This package binds one 336,150-location, 68-role divider to the actual singleton leaf's sixth raw division, identified as left modulus divmod right modulus.

Eight borrowed guards, 56 owned Word ports and four paid six-bit descriptors implement literal dispatch. The source precision guide establishes the unsigned high-bit margin. Setup, division and output retirement cost at most 2^14(P+2)²; finite metadata and allocation remain separately charged.

Replacing the call changes allocation events. A weak live/free-slot bijection proves the unchanged source continuation and unordered cleanup, charging histories on actual physical owners. The contribution is this actual-call/ownership interface; restoring division and CRT arithmetic remain predecessor results.

## Verification

`python3 -B scripts/research_package.py --package research/literal-current-crt-divmod`

Recorded checks cover every numerical access at all 64 slots, 124 arithmetic cases and six actual roundtrips with 24 allocator counterfactuals. Independent sparse review covers 22,272 dispatch paths, full lifecycles, two roundtrips and twelve bijections. Returning corruption and retirement faults are detected.

## Scope and remaining obligations

Only one numerical call is replaced. Other arithmetic, source control, metadata binding, grants and a common source/radix tariff remain external.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/c4ab5dab6914a04cb86d1fe54eb763b35cc7eeb1/research/literal-current-crt-divmod/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 24. Prove a uniform rounding margin for all 24 orders of two selected source factors

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/extremal-phase-two-axis-margin-20261114?quick_pull=1&title=Prove+a+uniform+rounding+margin+for+all+24+orders+of+two+selected+source+factors&body=%23%23%20Contribution%20and%20significance%0A%0AExact%20nonvanishing%20at%20selected%20source%20phases%20does%20not%20provide%20a%20rounding%20margin.%20This%20package%20resolves%20a%20deterministic%20two-axis%20extremal-phase%20case%2C%20retaining%20physical%20phase%2Fchirp%20and%20matched%20periodic%20aliases.%0A%0AFor%20the%20stated%20fine-prime%20family%20with%20p%3E%3D4096%2C%20put%20a%3Dpi%20alpha%C2%B2%20and%20w%3Dexp(-2a).%20All%2024%20vertex%20orders%20have%20Stein%20determinant%20magnitude%20at%20least%20w%C2%B2%2F16%3B%20smallest%20singular%20values%20are%20at%20least%202%5E-10%20w%C2%B2%20forward%20and%202%5E-19%20w%C2%B2%20for%20the%20inverse.%20Factor%20entry%20errors%20at%20most%202%5E-34%20w%C2%B2%20preserve%20full%20rank.%20The%20explicit%20precision%20requirement%20is%20met%20by%20p%20bits%20in%20the%20admitted%20regime.%0A%0ALex%2FGray%20classes%2C%20continuous%20parameter%20inequalities%20and%20charged%20inverse%20perturbation%20prove%20the%20claim.%20Matched%20periodization%20fits%20a%20further%20error%20allowance.%20An%20exact%20three-axis%20box%20example%20shows%20this%20argument%20cannot%20simply%20be%20tensorized.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fextremal-phase-two-axis-margin%60%0A%0ARecorded%20checks%20cover%20all%2024%20symbolic%20orders%2C%2072%20rational%20fixtures%2C%20288%20Gram%20certificates%2C%20certified%20source%20tuples%20and%20eleven%20controls.%20Independent%20Bernstein%20verification%20proves%20positivity%20of%2019%2C992%20coefficients%20on%20the%20continuous%20box%20and%20checks%20the%20three-axis%20nonextension.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AArbitrary%20good%20phases%20and%20growing%20dimensions%20remain%20open.%20This%20package%20does%20not%20admit%20a%20table%20producer%3B%20its%20inverse%20concerns%20the%20selected%20sections%2C%20not%20a%20section%20of%20a%20larger%20inverse.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F702c7616667c5f4e583eb73687944d148b7a1ccf%2Fresearch%2Fextremal-phase-two-axis-margin%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/702c7616667c5f4e583eb73687944d148b7a1ccf/research/extremal-phase-two-axis-margin/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

Exact nonvanishing at selected source phases does not provide a rounding margin. This package resolves a deterministic two-axis extremal-phase case, retaining physical phase/chirp and matched periodic aliases.

For the stated fine-prime family with p>=4096, put a=pi alpha² and w=exp(-2a). All 24 vertex orders have Stein determinant magnitude at least w²/16; smallest singular values are at least 2^-10 w² forward and 2^-19 w² for the inverse. Factor entry errors at most 2^-34 w² preserve full rank. The explicit precision requirement is met by p bits in the admitted regime.

Lex/Gray classes, continuous parameter inequalities and charged inverse perturbation prove the claim. Matched periodization fits a further error allowance. An exact three-axis box example shows this argument cannot simply be tensorized.

## Verification

`python3 -B scripts/research_package.py --package research/extremal-phase-two-axis-margin`

Recorded checks cover all 24 symbolic orders, 72 rational fixtures, 288 Gram certificates, certified source tuples and eleven controls. Independent Bernstein verification proves positivity of 19,992 coefficients on the continuous box and checks the three-axis nonextension.

## Scope and remaining obligations

Arbitrary good phases and growing dimensions remain open. This package does not admit a table producer; its inverse concerns the selected sections, not a section of a larger inverse.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/702c7616667c5f4e583eb73687944d148b7a1ccf/research/extremal-phase-two-axis-margin/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 25. Eliminate every raw division fallback from the current CRT producer using the verified literal core

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/all-current-crt-divisions-20261114?quick_pull=1&title=Eliminate+every+raw+division+fallback+from+the+current+CRT+producer+using+the+verified+literal+core&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20preceding%20literal%20divider%20replaces%20one%20singleton-leaf%20call.%20This%20package%20removes%20every%20raw%20Unsigned.divmod%20fallback%20from%20the%20exact%20admitted%20forward%2Finverse%20CRT%20producers%2C%20including%20nonleaf%20production%20and%20Euclidean%20inversion%2C%20using%20the%20unchanged%20336%2C150-location%20core.%0A%0AFor%20m%20left%20records%2C%20t%20right%20records%2C%20v%20valid%20right%20records%20and%20Euclidean%20lengths%20e_i%2C%20the%20exact%20count%20is%20J%3D3m%2B2t%2Bv%2B2%20sum(e_i)%2C%20bounded%20by%20(P-2)(4P%2B5).%20The%20division%20subset%20costs%20at%20most%2089%2BJ(930P%C2%B2%2B1395P%2B14322)%3C2%5E15(P%2B2)%5E4%20literal%20instructions.%20Metadata%2Fgrants%20remain%20separate.%0A%0AA%20weak%20slot%20bijection%20fixes%20incoming%20live%20values%2C%20composes%20through%20actual%20source%20cleanup%20and%20charges%20real%20physical%20history%20unions.%20This%20adds%20complete%20provider%20elimination%20and%20repeated%20ownership%20accounting%3B%20the%20divider%20algorithm%20and%20numerical%20admission%20remain%20credited%20predecessors.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fall-current-crt-divisions%60%0A%0ARecorded%20source%20checks%20authenticate%2076%20objects%20and%20both%20producer%20call%20sites.%20Replay%20executes%20355%20literal%20divisions%2C%20including%2052%20unit%20divisors%20and%20104%20allocator%20fingerprints%2C%20across%20three%20payload%20roundtrips%20and%20one%20complete%20source-only%20roundtrip.%20Normal%2Foptimized%20receipts%20agree.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AOther%20arithmetic%2C%20Word%20lifecycle%2C%20controllers%2C%20allocator%20metadata%20and%20grants%20remain%20supplied.%20The%20mixed-model%20invoice%20is%20not%20a%20common%20full-caller%20tariff.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F9700fc89e2582a1fb358a4c6d0d0387076192adc%2Fresearch%2Fall-current-crt-divisions%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/9700fc89e2582a1fb358a4c6d0d0387076192adc/research/all-current-crt-divisions/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The preceding literal divider replaces one singleton-leaf call. This package removes every raw Unsigned.divmod fallback from the exact admitted forward/inverse CRT producers, including nonleaf production and Euclidean inversion, using the unchanged 336,150-location core.

For m left records, t right records, v valid right records and Euclidean lengths e_i, the exact count is J=3m+2t+v+2 sum(e_i), bounded by (P-2)(4P+5). The division subset costs at most 89+J(930P²+1395P+14322)<2^15(P+2)^4 literal instructions. Metadata/grants remain separate.

A weak slot bijection fixes incoming live values, composes through actual source cleanup and charges real physical history unions. This adds complete provider elimination and repeated ownership accounting; the divider algorithm and numerical admission remain credited predecessors.

## Verification

`python3 -B scripts/research_package.py --package research/all-current-crt-divisions`

Recorded source checks authenticate 76 objects and both producer call sites. Replay executes 355 literal divisions, including 52 unit divisors and 104 allocator fingerprints, across three payload roundtrips and one complete source-only roundtrip. Normal/optimized receipts agree.

## Scope and remaining obligations

Other arithmetic, Word lifecycle, controllers, allocator metadata and grants remain supplied. The mixed-model invoice is not a common full-caller tariff.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/9700fc89e2582a1fb358a4c6d0d0387076192adc/research/all-current-crt-divisions/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 26. Produce the selected extremal Gaussian tables through four existing encoded scalar calls

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/extremal-pair-coefficient-adapter-20261114?quick_pull=1&title=Produce+the+selected+extremal+Gaussian+tables+through+four+existing+encoded+scalar+calls&body=%23%23%20Contribution%20and%20significance%0A%0AThe%20two-axis%20margin%20theorem%20leaves%20selected%20table%20production%20as%20a%20premise.%20This%20package%20closes%20that%20local%20interface%20through%20four%20calls%20to%20the%20unchanged%20encoded%20scalar%20primitive%20audited%20in%20%236085.%0A%0AFrom%20borrowed%20(p%2Calpha%2Cs1%2Ct1%2Cs2%2Ct2)%2C%20one%20setup%20uses%20P%3Dp%2B8%20and%20F%3D2alpha%C2%B2.%20Four%20exact%20rational%20arguments%20lie%20in%20(0%2CF)%3B%20returned%20factors%20have%20exact%20diagonals%20and%20off-diagonal%20error%20below%202%5E(-p-7).%20For%20the%20admitted%20p%3E%3D4096%20source%20family%2C%20scalar%20and%20omitted-alias%20errors%20meet%20the%20two-axis%20margin%2C%20so%20the%20selected%20tensor%20and%20its%20own%20inverse%20retain%20full%20Stein%20rank%20in%20all%2024%20orders.%0A%0AAll%20borrowed%20bodies%2Fheads%20return%2C%20and%20nine%20distinct%20output%20owners%20remain%20live%20with%20explicit%20retirement%20costs.%20Complete%20local%20time%20is%20O(p%C2%B3%2B(p%2BB)%C2%B2)%3B%20O(p%2BB)%20storage%20requires%20fresh%20or%20bounded%20prior%20histories.%20Reused%20histories%20retain%20their%20actual%20maxima%20and%20sweep%20costs.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fextremal-pair-coefficient-adapter%60%0A%0ARecorded%20encoded%20replay%20performs%20four%20unchanged%20calls%20under%20no-decode%20protection%2C%20checks%20independent%20scalar%20intervals%2C%20arguments%2C%20all%20nine%20outputs%2C%20history%20cleanup%20and%20seven%20invalid%20inputs.%20It%20is%20a%20finite%20small%20packet%2C%20not%20a%20p%3E%3D4096%20execution%3B%20the%20quantified%20source%2Ferror%20result%20is%20proved%20separately.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0ASource%2Fprimality%20admission%2C%20index%20routing%2C%20full%20caller%20integration%20and%20growing%20dimensions%20remain%20open.%20The%20adapter%20does%20not%20repair%20the%20separate%20%236099%20global%20ProductionPlan%20domain.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2F8df9a7c57aaf87873556867f96658c2474518238%2Fresearch%2Fextremal-pair-coefficient-adapter%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/8df9a7c57aaf87873556867f96658c2474518238/research/extremal-pair-coefficient-adapter/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

The two-axis margin theorem leaves selected table production as a premise. This package closes that local interface through four calls to the unchanged encoded scalar primitive audited in #6085.

From borrowed (p,alpha,s1,t1,s2,t2), one setup uses P=p+8 and F=2alpha². Four exact rational arguments lie in (0,F); returned factors have exact diagonals and off-diagonal error below 2^(-p-7). For the admitted p>=4096 source family, scalar and omitted-alias errors meet the two-axis margin, so the selected tensor and its own inverse retain full Stein rank in all 24 orders.

All borrowed bodies/heads return, and nine distinct output owners remain live with explicit retirement costs. Complete local time is O(p³+(p+B)²); O(p+B) storage requires fresh or bounded prior histories. Reused histories retain their actual maxima and sweep costs.

## Verification

`python3 -B scripts/research_package.py --package research/extremal-pair-coefficient-adapter`

Recorded encoded replay performs four unchanged calls under no-decode protection, checks independent scalar intervals, arguments, all nine outputs, history cleanup and seven invalid inputs. It is a finite small packet, not a p>=4096 execution; the quantified source/error result is proved separately.

## Scope and remaining obligations

Source/primality admission, index routing, full caller integration and growing dimensions remain open. The adapter does not repair the separate #6099 global ProductionPlan domain.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/8df9a7c57aaf87873556867f96658c2474518238/research/extremal-pair-coefficient-adapter/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

## 27. Close the current CRT raw arithmetic interface with literal comparison, addition, subtraction and division

[Open prefilled PR](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/all-current-crt-arithmetic-20261114?quick_pull=1&title=Close+the+current+CRT+raw+arithmetic+interface+with+literal+comparison%2C+addition%2C+subtraction+and+division&body=%23%23%20Contribution%20and%20significance%0A%0ADivision%20was%20already%20literal%2C%20but%20the%20current%20CRT%20producer%20still%20called%20raw%20comparison%2C%20addition%20and%20subtraction%20providers.%20This%20package%20closes%20that%20remaining%20interface%2C%20including%20aliased%20doubling%20and%20physical%20output%20ownership.%0A%0AOne%20fixed%201%2C304%2C162-location%2C%2068-role%20graph%20handles%20all%20four%20arithmetic%20operations%3B%20its%20first%20336%2C150%20instructions%20are%20the%20unchanged%20divider.%20New%20entries%20decode%20finite%20handles%2C%20scan%20actual%20P-bit%20Words%2C%20preserve%20borrowed%20contents%2C%20create%20outputs%20and%20erase%20selector%20frames.%20Halt%20tags%20return%20comparison%2Fcarry%2Fborrow%20flags.%20A%20new%20simple%20call%2C%20including%20setters%2C%20costs%20at%20most%20401P%2B1073%3B%20the%20package%20proves%20a%20quartic%20arithmetic-subset%20bill.%0A%0AThe%20source%20binder%20preserves%20the%20weak%20owner%20relation%20with%20eight%20protected%20guards%2C%2056%20owned%20Words%20and%20four%20explicit%20selector%20grants.%20This%20adds%20the%20combined%20source-bound%20alias%2Freturn%2Fallocation%20join%2C%20not%20new%20generic%20binary%20arithmetic.%0A%0A%23%23%20Verification%0A%0A%60python3%20-B%20scripts%2Fresearch_package.py%20--package%20research%2Fall-current-crt-arithmetic%60%0A%0ARecorded%20primary%20source%2Fcore%2Freplay%20checks%20agree%20normally%20and%20under%20optimization.%20The%20registered%20eight-entry%20suite%20includes%20twelve%20checks%20and%20two%20complementary%20independent%20reviews.%20Exact%20source%20authentication%2C%20returning%20semantic%20controls%2C%20ownership%20and%20cost%20evidence%20are%20retained%20in%20the%20package.%0A%0A%23%23%20Scope%20and%20remaining%20obligations%0A%0AWord%20lifecycle%2C%20higher%20controllers%2C%20finite%20live%2Ffree%20metadata%2C%20acquisition%20and%20framing%20remain%20supplied.%20Source-only%20and%20fixed-codeword%20payload%20callers%20have%20distinct%20role%20counts%20and%20bills%3B%20no%20common%20whole-caller%20tariff%20is%20proved.%0A%0ANo%20new%20kappa%3A%20the%20package%20retains%20all%20five%20foundational%20assumptions%20and%20does%20not%20establish%20an%20unconditional%20multiplication%20theorem.%20Finite%20checks%20corroborate%20the%20scoped%20written%20proofs.%0A%0A%23%23%20Provenance%20and%20credit%0A%0ABase%3A%20%60e54523517d0f03e58352e647c403a5af3e525a57%60.%20%5BFull%20PR%20draft%2C%20exact%20dependency%20pins%2C%20review%20and%20predecessor%20credit%5D(https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2Fee6005fe241ab947e511fe9f6d86f5f4fa58478b%2Fresearch%2Fall-current-crt-arithmetic%2FPR-DESCRIPTION.md).%0A%0APrepared%20for%20Jerry%20Chen%20%2F%20%40CubeJerry%20with%20substantial%20OpenAI%20assistance.%20Original%20source%20authors%20and%20predecessor%20results%20retain%20their%20credit.%20Model-assisted%20review%20is%20not%20human%20or%20formal-kernel%20acceptance.) · [Full pinned draft](https://github.com/CubeJerry/integer-mult-bounds/blob/ee6005fe241ab947e511fe9f6d86f5f4fa58478b/research/all-current-crt-arithmetic/PR-DESCRIPTION.md)

<details>
<summary>Preview prefilled description</summary>

## Contribution and significance

Division was already literal, but the current CRT producer still called raw comparison, addition and subtraction providers. This package closes that remaining interface, including aliased doubling and physical output ownership.

One fixed 1,304,162-location, 68-role graph handles all four arithmetic operations; its first 336,150 instructions are the unchanged divider. New entries decode finite handles, scan actual P-bit Words, preserve borrowed contents, create outputs and erase selector frames. Halt tags return comparison/carry/borrow flags. A new simple call, including setters, costs at most 401P+1073; the package proves a quartic arithmetic-subset bill.

The source binder preserves the weak owner relation with eight protected guards, 56 owned Words and four explicit selector grants. This adds the combined source-bound alias/return/allocation join, not new generic binary arithmetic.

## Verification

`python3 -B scripts/research_package.py --package research/all-current-crt-arithmetic`

Recorded primary source/core/replay checks agree normally and under optimization. The registered eight-entry suite includes twelve checks and two complementary independent reviews. Exact source authentication, returning semantic controls, ownership and cost evidence are retained in the package.

## Scope and remaining obligations

Word lifecycle, higher controllers, finite live/free metadata, acquisition and framing remain supplied. Source-only and fixed-codeword payload callers have distinct role counts and bills; no common whole-caller tariff is proved.

No new kappa: the package retains all five foundational assumptions and does not establish an unconditional multiplication theorem. Finite checks corroborate the scoped written proofs.

## Provenance and credit

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. [Full PR draft, exact dependency pins, review and predecessor credit](https://github.com/CubeJerry/integer-mult-bounds/blob/ee6005fe241ab947e511fe9f6d86f5f4fa58478b/research/all-current-crt-arithmetic/PR-DESCRIPTION.md).

Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance. Original source authors and predecessor results retain their credit. Model-assisted review is not human or formal-kernel acceptance.

</details>

