# Quiet helper-route coding primitive

This package contains a complete typed source word implementing one reversible
loan of an existing helper route. It proves a seven-ADD local coding primitive
with no extra Gaussian MOVE or owner, and explicitly shows that the raw example
is replaceable by an earlier direct ADD. It does not implement the complete
second native action and establishes **No new κ**.

Read `PROOF.md` for the exact source window, arbitrary dirty-helper algebra,
positive scalar/lifecycle accounting, temporary common-state unavailability and
the raw-contact redundancy census. `quiet-loan.json.gz` contains all 73,378 typed
instructions. `RESULT.json` records all-input verification and three rejected
mutations. The two additional checkers independently establish the missing
current common row and the 354-window raw-contact limitation.

All code uses only Python's standard library and authenticates the original
compressed source SHA256. From this directory, replace SOURCE with the actual
source file path:

```sh
python -B build_and_verify.py --source SOURCE --transcript quiet-loan.json.gz --output RESULT.json
python -O -B build_and_verify.py --source SOURCE --output RESULT-OPTIMIZED.json
python -B raw_contact_audit.py --source SOURCE --output RAW-CONTACT-AUDIT.json
python -O -B raw_contact_audit.py --source SOURCE --output RAW-CONTACT-AUDIT-OPTIMIZED.json
python -B borrowed_common_check.py --source SOURCE --output BORROWED-COMMON-CHECK.json
```

Expected results: exact reference outputs on 1,880 entering columns; the single
coded shear q977←q977+q907; seven added loan ADDs; zero new MOVEs or lifetimes;
354 single-MOVE quiet windows and 35,921 eligible recipient contacts, of which
61 are deadline-critical but already cochart at entry; and a dirty-input dual
witness that common449 is temporarily unavailable at chart594.

The quiet-route pattern was identified by research worker B. Worker C constructed
the complete typed word and checked all entering input columns, added the
independent contact census and the dirty-input dual witness, and recorded the
raw-example limitation. Worker A reviewed the signed-swap argument and found a
distinctness clarification that is included in the proposition. Independent
review artifacts are maintained separately by the integrating lead.

Prepared for @CubeJerry with substantial OpenAI assistance. The source credit
and all five inherited foundational assumptions remain in force. This package
supports the same persistent research programme; it is not a separate branch
or complete target theorem.
