# Prefilled cumulative review link

No pull request has been opened. This package is prepared for community mathematical review at the written-proof level stated below.

[Review the prefilled comparison](https://github.com/CrocSwap/integer-mult-bounds/compare/main...CubeJerry:research/moonshot-overhead-program?expand=1&title=Quantify+square-root+multiplication+overhead+and+isolate+routing+barriers&body=%23%23+Result+and+scope%0A%0AWritten+unconditional+constructions+give+T%28n%29%3DO%28n+sqrt%28L%29+2%5E%7BO%28s%5E%282%2F3%29%28log%28s%2B2%29%29%5E%281%2F3%29%29%7D%29%2C+L%3D1%2Blog2+n%2C+s%3Dlog2+L%2C+for+one+fixed+exact+full-product+multitape+machine+with+O%28n%29+cells+ever+visited.+S003+supplies+direct+absolute-space+components%3B+E002%2FE003+retain+separate+same-scale+proofs.+S004+proves+the+log-free+two-thirds+scale+conditional+on+JR+exact+rectangle+partitions.+JR+and+the+constant-overhead+endpoint+remain+open.%0A%0A%5BS003+proof%5D%28https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2Fresearch%2Fmoonshot-overhead-program%2Fresearch%2Fmoonshot-overhead-program%2Fsessions%2F2026-11-26-S003%2Flead%2Fadaptive-extraction.md%29+%7C+%5BAdmission+and+independent+reviews%5D%28https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2Fresearch%2Fmoonshot-overhead-program%2Fresearch%2Fmoonshot-overhead-program%2Fsessions%2F2026-11-26-S003%2Flead%2FADMISSION-AQ.md%29+%7C+%5BVerification%5D%28https%3A%2F%2Fgithub.com%2FCubeJerry%2Finteger-mult-bounds%2Fblob%2Fresearch%2Fmoonshot-overhead-program%2Fresearch%2Fmoonshot-overhead-program%2FVERIFICATION.md%29%0A%0AReproduce+a+finite+check+from+the+repository+root%3A%0A%60%60%60sh%0Apython3+-I+-B+research%2Fmoonshot-overhead-program%2Fsessions%2F2026-11-26-S003%2Froute-a%2Fverify_nonstationary_walsh.py%0A%60%60%60%0AFinite+checks+support+written+proofs%3B+no+full+multiplier%2C+formal+refinement%2C+practical+cutoff+or+priority+certification+is+claimed.+Scoped+obstructions+are+not+runtime+lower+bounds.%0A%0A%23%23+Credits%0A%40CubeJerry%3B+pinned+OpenAI+manuscripts+and+predecessors%3B+preserved+S002%2FE001+and+concurrent+E002%2FE003%2FS004+contributions%3B+substantial+ChatGPT+multi-agent+assistance.+Full+attribution+is+in+the+programme.%0A)

## Validation

GitHub compare API accepted canonical base `main` and fork head `CubeJerry:research/moonshot-overhead-program`. Initial check: ahead33, behind0; base and merge base `e54523517d0f03e58352e647c403a5af3e525a57`; confirmed fork snapshot `72ad1c4e9259b43ff0ea8f76e6d4e2001d3c3ebe`. A refreshed pre-final comparison at00:13 UTC was ahead36, behind0, with the same base and merge base. Title/body were encoded once and decoded back exactly. This prepares a review page; it does not submit a PR.

## Title

Quantify square-root multiplication overhead and isolate routing barriers

## Proposed description

## Result and scope

Written unconditional constructions give T(n)=O(n sqrt(L) 2^{O(s^(2/3)(log(s+2))^(1/3))}), L=1+log2 n, s=log2 L, for one fixed exact full-product multitape machine with O(n) cells ever visited. S003 supplies direct absolute-space components; E002/E003 retain separate same-scale proofs. S004 proves the log-free two-thirds scale conditional on JR exact rectangle partitions. JR and the constant-overhead endpoint remain open.

[S003 proof](https://github.com/CubeJerry/integer-mult-bounds/blob/research/moonshot-overhead-program/research/moonshot-overhead-program/sessions/2026-11-26-S003/lead/adaptive-extraction.md) | [Admission and independent reviews](https://github.com/CubeJerry/integer-mult-bounds/blob/research/moonshot-overhead-program/research/moonshot-overhead-program/sessions/2026-11-26-S003/lead/ADMISSION-AQ.md) | [Verification](https://github.com/CubeJerry/integer-mult-bounds/blob/research/moonshot-overhead-program/research/moonshot-overhead-program/VERIFICATION.md)

Reproduce a finite check from the repository root:
```sh
python3 -I -B research/moonshot-overhead-program/sessions/2026-11-26-S003/route-a/verify_nonstationary_walsh.py
```
Finite checks support written proofs; no full multiplier, formal refinement, practical cutoff or priority certification is claimed. Scoped obstructions are not runtime lower bounds.

## Credits
@CubeJerry; pinned OpenAI manuscripts and predecessors; preserved S002/E001 and concurrent E002/E003/S004 contributions; substantial ChatGPT multi-agent assistance. Full attribution is in the programme.
