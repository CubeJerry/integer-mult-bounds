#!/usr/bin/env python3
"""Check exact rank-difference signs in the frozen 1,066 receipt."""
from collections import Counter
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
RESULT = HERE / "ALL-ONE-RELATION-PRICES.json"


def need(condition, label):
    if not condition:
        raise AssertionError(label)


def run():
    doc = json.loads(RESULT.read_text())
    need(doc["status"] == "FRESH_EXACTQ_ALL_PUBLIC_SINGLE_RELATION_PRICE_SCREEN",
         "frozen paired-screen receipt status")
    rows = doc["records"]
    need(len(rows) == 1066, "all public main-history-hit records present")
    counts = Counter()
    debit_ranks = set()
    for row in rows:
        target = row["target_rank"]
        debit = row["minimum_enabling_relation_rank"]
        need(target > 0 and debit is not None and debit > 0,
             "all target and minimum helper ranks positive")
        debit_ranks.add(debit)
        if target == debit:
            sign = "equal"
        elif target > debit:
            sign = "positive"
        else:
            sign = "negative"
        counts[sign] += 1
        expected_price_class = {
            "equal": "zero_or_interval_overlap",
            "positive": "positive",
            "negative": "negative",
        }[sign]
        need(row["saving_0038"]["classification"] == expected_price_class,
             "rank sign matches certified .0038 price interval class")
        if sign == "equal":
            profile = Counter({target: 1})
            profile[debit] -= 1
            profile = {rank: amount for rank, amount in profile.items() if amount}
            need(not profile and row["saving_0038"]["exact"] == ["0", "0"],
                 "equal-rank f(r)-f(r) cancels exactly")
    need(counts == Counter({"positive":376,"equal":437,"negative":253}),
         "all profile sign counts")

    # Executed negative control: a dict literal with a repeated rank collapses
    # to a one-term negative profile and would falsely price equal-rank rows.
    witness = next(row for row in rows if row["target_rank"] ==
                   row["minimum_enabling_relation_rank"])
    rank = witness["target_rank"]
    bad_profile = {rank: -1}
    price_path = (HERE.parent.parent /
                  "joint-review-worktree/research/p104-joint-helper-cache-funding-bound/verifier/integer_prices.py")
    spec = importlib.util.spec_from_file_location("wave52_profile_sign_prices", price_path)
    prices = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = prices
    spec.loader.exec_module(prices)
    bad_interval = prices.moment(bad_profile)
    need(bad_interval != (Q(0),Q(0)) and
         witness["saving_0038"]["exact"] == ["0","0"],
         "dict-collision mutant is distinguishable from equal-rank receipt")

    result = {
        "status": "PASS_EXACT_PROFILE_SIGN_CROSSCHECK",
        "all_candidates": len(rows),
        "counts": dict(sorted(counts.items())),
        "minimum_debit_ranks": sorted(debit_ranks),
        "zero_profiles_are_exact_equal_rank_cancellations": True,
        "sign_for_kappa_in_[0,1)": "sign(target_rank - minimum_debit_rank)",
        "at_kappa_1": "all profiles are zero because target and debit ranks are positive",
        "executed_negative_control": {
            "name": "repeated-rank dict-literal collision",
            "equal_rank": rank,
            "mutant_profile": bad_profile,
            "mutant_interval": [str(x) for x in bad_interval],
            "rejected": True},
        "source_receipt_sha256": __import__("hashlib").sha256(RESULT.read_bytes()).hexdigest(),
    }
    (HERE / "PROFILE-SIGN-VALIDATION.json").write_text(
        json.dumps(result, sort_keys=True, indent=2)+"\n")
    return result


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
