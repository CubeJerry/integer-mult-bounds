# Sharp bank-separated cost of completing the canonical quotient

**Proved fixed-interface algebraic theorem. No physical source or delivery construction, supplier, or new kappa.** One scalar combination per bank cannot directly complete the canonical quotient. The sharp total is nine messages after the existing point-feedback grant and thirteen without that grant.

## 1. Exact data and two different side-information spaces

Use the reviewed twenty-seven-output word, SHA256 `d28b6ae55b9d3c3cab440c24af971babbe7fb2413180ec1cb3d5e2fa4c77bb71`, native root data SHA256 `8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`, and private-bank envelope result SHA256 `5bd89e3a32a0649fd3b3c1adf68ebd857100aa653aa2ee4cb1273cfd3f1fc5f0`.

Let `k_i=e_i+sum_(j:r_i dot r_j=0)e_j` and let C be the span of all111 such canonical rows. Its dimension is9. Let B80 be the reviewed global common/ground grant plus all six private raw banks. Let B88 additionally contain the83 raw point rows already recoverable in that envelope and announced globally for free.

|Side information|Rank|Missing C dimensions|Canonical quotient basis|
|---|---:|---:|---|
|B80|80|4|k_0,k_1,k_2,k_4|
|B88|88|3|k_0,k_1,k_2|

The three-dimensional target therefore uses B88, not B80. Neither global grant is asserted to be physically delivered.

Let U_0,U_1,U_2,U_3 be all five actual filtered rows at C1,C3,C4,Extra6, from source groups5,7,9,11. Denote their committed rows by u_(i,0),...,u_(i,4): group g has H(g)_0,H(g)_1,H(g)_2,H(g)_3,Hnew(g)_1. The exact names and rows are recorded in RESULT.json. Their dimensions modulo B80 are(4,4,4,5), jointly16; modulo B88 they are(4,4,4,4), jointly14. All twenty rows remain available in the lower-bound calculation.

## 2. Quantified optimization problem and theorem

Fix B=B80 or B88. Bank i may emit linear messages from its own U_i and the already shared B. Delivery is free. The target is direct canonical recovery:

    C subset B+M_0+M_1+M_2+M_3,    M_i subset B+U_i.

For every characteristic-two field and every positive whole-record width V, arbitrary linear block encodings of the available V-wide records are allowed. Cost is total scalar output dimension. The sharp message dimensions per bank are

    B88: (2V,2V,2V,3V), total9V;
    B80: (3V,3V,3V,4V), total13V.

The bounds are simultaneously attained by the recipes below. In particular one V-wide message from each bank cannot meet either target.

This is a static, fixed-side-information C9 inclusion theorem. It does not optimize arbitrary noncanonical fitting codes, nor allow newly decoded points after the new messages to become additional free broadcasts. B88 grants the previously established83 points at the start. No new source observation or cross-bank acquisition is supplied.

## 3. Cut proof valid for every field and block width

For each i generously reveal all other bank spaces and put

    W_i=B+sum_(j!=i)U_j,   d_i=dim((W_i+C)/W_i).

In the quotient by W_i every other bank's message vanishes. Hence the image of C, of dimension d_i, must be carried by bank i alone. Its linear message dimension is at least d_i. Tensoring with I_V gives d_i V even for arbitrary mixing of record coordinates.

|Side information|Omitted bank|rank W_i|rank(W_i+C)|d_i|
|---|---|---:|---:|---:|
|B80|C1,C3,C4, individually|93|96|3|
|B80|Extra6|92|96|4|
|B88|C1,C3,C4, individually|100|102|2|
|B88|Extra6|99|102|3|

The certificate supplies d_i binary covectors per cut. They annihilate every row of W_i and evaluate to an identity matrix on d_i listed canonical rows. These twenty-two exact dual witnesses certify the lower bounds; binary identities remain valid over every characteristic-two extension field. Their tensor lifts give identity blocks of rank d_i V. The proof uses these explicit ranks and duals, not extrapolation from sampled coefficients.

## 4. Nine actual rows attain the B88 bound

Each of C1,C3,C4 sends its first two rows u_(i,0),u_(i,1). Extra6 sends its first three rows u_(3,0),u_(3,1),u_(3,2). Thus there are nine bank-separated messages, with no cross-bank acquisition. Exact congruences modulo B88 are

    k_0 = sum_(i=0..3)(u_(i,0)+u_(i,1)),
    k_1 = u_(0,1)+u_(1,1)+u_(2,1)+u_(3,0)+u_(3,2),
    k_2 = sum_(i=0..3)u_(i,0).

RESULT.json gives actual binary coefficients for every common correction, and direct witnesses for all111 canonical rows in B88 plus these messages. The recipe attains every cut bound simultaneously over every characteristic-two field and width. Given C, each native receiver recovers e_i using k_i and its geometrically granted raw locals; this remains an optimistic information statement rather than a transport implementation.

## 5. Thirteen local combinations attain the B80 bound

Within each bank put

    p_i=u_(i,2)+u_(i,3),
    q_i=u_(i,0)+u_(i,2),
    r_i=u_(i,0)+u_(i,1).

Each pair bank sends p_i,q_i,r_i. Extra6 sends p_3,q_3,r_3 and s=u_(3,4). The following congruences hold modulo B80:

    k_0 = sum_i p_i,
    k_1 = sum_i q_i,
    k_2 = sum_(i=0..2)(p_i+q_i)+p_3+s,
    k_4 = sum_i(p_i+r_i).

All common corrections and all111 canonical decoders are certified. This attains(3,3,3,4). Extra6's fifth row is correctly retained: its extra quotient dimension before the83 point announcements cannot be silently discarded.

## 6. Verification and scope of the next construction

Run:

```sh
python check.py --repo REPO --envelope-result ENVELOPE/output/RESULT.json \
  --word TWENTYSEVEN/WORD.json --out output
```

Expected status is `PASS_EXACT_BANK_SEPARATED_CANONICAL_COMPRESSION`. The certificate includes full source/side-information rows, eight cut-rank pairs, twenty-two cut duals, both message lists,222 canonical reconstruction identities and seven compact quotient-basis decoders. The cut duals reject one-message-per-bank and every proposal below a mandatory bank dimension. The B80/B88 comparison detects incorrectly using a three-dimensional quotient before the old point-feedback grant.

The exploratory sixteen/sixty-four binary-section enumeration in probe.py helped find the recipes, but it is not the proof and does not support an extrapolation to fields. The exact cut argument and matching binary constructions give the universal result.

This isolates the next canonical task: three missing quotient dimensions require nine bank-local messages under the fixed B88 interface. Greater direct canonical compression must change the side information or combine independent bank information before emitting final messages, with actual source visits, ownership, shared-original restoration and complete charges. A noncanonical code or new feedback protocol is a separate possible interface requiring its own analysis.

No minimum physical packet count, movement lower bound, nonlinear encoding bound, or complete-caller impossibility is asserted here. The actual source is unchanged. All foundational assumptions, compatible strict suppliers, precision and recursive expenses remain. Credit @CubeJerry, the private-bank/source authors and reviewers; Worker B with substantial OpenAI assistance. **No new kappa.**
