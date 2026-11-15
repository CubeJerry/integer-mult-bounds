#!/usr/bin/env python3
"""Directed rational 200th-root invoice for the partial source interface."""
from fractions import Fraction as F
from pathlib import Path
from decimal import Decimal, localcontext
import json


def floor_root(a, degree):
    lo, hi = 0, 1 << ((a.bit_length()+degree-1)//degree)
    while hi-lo > 1:
        mid = (hi+lo)//2
        if mid**degree <= a:
            lo = mid
        else:
            hi = mid
    if not lo**degree <= a < (lo+1)**degree:
        raise ValueError("Integer root bracket failed")
    return lo


def power(r):
    scale = 10**45
    n = r**199 * scale**200
    low = floor_root(n, 200)
    return F(low, scale), F(low if low**200 == n else low+1, scale)


def moment(profile):
    lo = hi = F(0)
    for r, c in profile.items():
        a, b = power(r)
        lo += c*(a if c >= 0 else b)
        hi += c*(b if c >= 0 else a)
    return lo, hi


def encode(pair):
    with localcontext() as ctx:
        ctx.prec = 45
        return {"lower": str(pair[0]), "upper": str(pair[1]),
                "lower_decimal": str(Decimal(pair[0].numerator)/Decimal(pair[0].denominator)),
                "upper_decimal": str(Decimal(pair[1].numerator)/Decimal(pair[1].denominator))}


if __name__ == "__main__":
    root = Path(__file__).parent
    profile = {int(k):v for k,v in json.loads((root/"output/RESULT.json").read_text())["preferred_closed"]["movement_profile"].items()}
    # Pinned programme TARGET-005 limiting movement allowance, not admission.
    allowance = {127:F(37,6),64:F(74,6),1:F(-74,6)}
    for j in range(1,9):
        allowance[1+7*j] = allowance.get(1+7*j,F(0))+F(74,6)
        allowance[7*j] = allowance.get(7*j,F(0))-F(74,6)
    room = dict(allowance)
    for r,c in profile.items():
        room[r] = room.get(r,F(0))-c
    six_more = dict(room)
    six_more[8] = six_more.get(8,F(0))-6
    result = {"status":"PASS_DIRECTED_PARTIAL_SOURCE_INVOICE", "t":"199/200",
              "profile":profile, "moment":encode(moment(profile)),
              "limiting_allowance":encode(moment(allowance)),
              "limiting_room":encode(moment(room)),
              "optimistic_room_after_six_additional_bare_full_lifetimes":encode(moment(six_more)),
              "two_donor_line_stops_increment":encode(moment({1:2,6:2,7:-2})),
              "scope":"Closed partial source only; zero completed Y targets. Finite multiplicity is stricter. Ordinary, storage, erasure, decoder, compiler, precision and complete supplier obligations are not inferred from this movement calculation.",
              "new_complete_kappa":False}
    (root/"output/PRICE.json").write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"moment":result["moment"]["lower_decimal"],
                      "room_after_six":result["optimistic_room_after_six_additional_bare_full_lifetimes"]["lower_decimal"]}))
