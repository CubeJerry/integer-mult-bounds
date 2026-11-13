#!/usr/bin/env python3
"""Fresh exact-Q audit of the u=-e1459-e705+e885 history circuit."""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import gzip
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORD_PATH = ROOT / "reference/pr7481/WORD.json.gz"
AUTHOR_RESULT = ROOT / "worker-b/public-relation885/RESULT.json"
WORD_SHA = "acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9"
U = {1459: Q(-1), 705: Q(-1), 885: Q(1)}
EXPECTED_EVENT = 40710


def need(condition, label):
    if not condition:
        raise AssertionError(label)


def add(dst, src, factor=Q(1)):
    for coordinate, value in src.items():
        result = dst.get(coordinate, Q(0)) + factor * value
        if result:
            dst[coordinate] = result
        else:
            dst.pop(coordinate, None)


def reduce_with_expression(row, basis, expressions):
    value = row.copy()
    expression = {}
    for pivot in sorted(basis):
        coefficient = value.get(pivot)
        if coefficient:
            add(value, basis[pivot], -coefficient)
            add(expression, expressions[pivot], coefficient)
    return value, expression


def insert_with_expression(basis, expressions, row, row_index):
    value = row.copy()
    expression = {row_index: Q(1)}
    for pivot in sorted(basis):
        coefficient = value.get(pivot)
        if coefficient:
            add(value, basis[pivot], -coefficient)
            add(expression, expressions[pivot], -coefficient)
    if not value:
        return False
    pivot = min(value)
    scale = value[pivot]
    basis[pivot] = {h: q/scale for h,q in value.items()}
    expressions[pivot] = {i:q/scale for i,q in expression.items()}
    return True


def quotient_by_u(row):
    value = row.copy()
    coefficient = value.pop(1459, Q(0))
    if coefficient:
        add(value, {885: Q(1), 705: Q(-1)}, coefficient)
    return value


def encode(row):
    return {str(h): str(value) for h, value in sorted(row.items()) if value}


def check():
    raw = WORD_PATH.read_bytes()
    need(sha256(raw).hexdigest() == WORD_SHA, "exact #7481 word hash")
    word = json.loads(gzip.decompress(raw))
    frames = word["frames"]
    rows = [{h: Q(1)} for h in range(word["public"])] + [None]*word["owned_fields"]
    charts = list(word["initial"]) + [None]*word["owned_fields"]
    banks = defaultdict(list)
    zero_moves = []
    move_rows = {}
    for owner, frame in enumerate(word["initial"]):
        banks[frame].append({"event": -1, "owner": owner, "frame": frame,
                             "kind": "initial", "row": rows[owner].copy()})
    for event, instruction in enumerate(word["program"]):
        opcode, owner = instruction[:2]
        if opcode == "MOVE":
            source, destination = instruction[2:4]
            need(rows[owner] is not None and charts[owner] == source,
                 "actual MOVE source frame/live value")
            target = rows[owner].copy()
            rank = abs(len(frames[destination])-len(frames[source]))
            need(rank > 0, "all actual MOVE children have positive rank")
            move_rows[event] = target.copy()
            if not quotient_by_u(target):
                zero_moves.append(event)
            banks[destination].append({"event": event, "owner": owner,
                "frame": destination, "kind": "arrival", "row": target.copy()})
            rows[owner] = target
            charts[owner] = destination
        elif opcode == "INIT":
            need(owner >= word["public"] and charts[owner] is None and rows[owner] is None,
                 "owned INIT lifecycle")
            charts[owner], rows[owner] = instruction[2], {}
        elif opcode == "CLEAR":
            need(owner >= word["public"] and charts[owner] == instruction[2] and rows[owner] is not None,
                 "owned CLEAR lifecycle")
            charts[owner], rows[owner] = None, None
        elif opcode == "SCALE":
            factor = Q(instruction[2])
            need(charts[owner] == instruction[3] and rows[owner] is not None and factor,
                 "coframed nonzero SCALE")
            rows[owner] = {h: factor*q for h,q in rows[owner].items() if factor*q}
        elif opcode in ("ADD", "COPY"):
            donor = instruction[2]
            need(owner != donor and charts[owner] == charts[donor] == instruction[4],
                 "coframed ADD/COPY")
            if opcode == "COPY":
                need(owner >= word["public"] and not rows[owner], "COPY into zero owned field")
            add(rows[owner], rows[donor], Q(instruction[3]))
        else:
            raise AssertionError(f"unknown native opcode {opcode}")
    need(charts == word["final"] + [None]*word["owned_fields"], "final owner chart map")
    need(len(move_rows) == 6279 and sum(map(len, banks.values())) == 7780,
         "complete initial plus MOVE-arrival banks")

    full_row_counts = {}
    relation_frames = {}
    exact_expressions = {}
    for frame, bank in banks.items():
        basis = {}
        expressions = {}
        for index, observation in enumerate(bank):
            need(insert_with_expression(basis, expressions, observation["row"], index),
                 f"all exact-Q history rows independent at frame {frame}")
        full_row_counts[frame] = len(bank)
        residual, expression = reduce_with_expression(U, basis, expressions)
        if not residual:
            relation_frames[frame] = len(bank)
            exact_expressions[frame] = expression

    need(len(banks) == 979, "all 979 exact physical frames represented")
    need(relation_frames == {189: 16}, "only exact destination frame 189 contains U")
    expression = exact_expressions[189]
    support = [banks[189][i] for i in expression]
    latest_index = max(expression, key=lambda i: (banks[189][i]["event"], i))
    latest = banks[189][latest_index]
    need(latest["event"] == EXPECTED_EVENT and latest["kind"] == "arrival",
         "latest support is event 40710 arrival")
    q = expression[latest_index]
    providers = []
    for index, coefficient in expression.items():
        if index == latest_index:
            continue
        observation = banks[189][index]
        need(observation["event"] < EXPECTED_EVENT,
             "every other circuit support row strictly precedes latest arrival")
        providers.append({"event": observation["event"], "owner": observation["owner"],
                          "frame": observation["frame"],
                          "coefficient_in_target": str(-coefficient/q),
                          "row": encode(observation["row"])})
    need({p["event"] for p in providers} == {-1, 40708},
         "unique providers are initial 1459 and event 40708")
    need({"1459": "1"} in [p["row"] for p in providers],
         "demoted initial provider is e1459")
    need({"705": "1", "943": "1"} in [p["row"] for p in providers],
         "second provider is e705+e943")
    target = move_rows[EXPECTED_EVENT]
    target_identity = target.copy()
    for provider in providers:
        add(target_identity, {int(h): Q(v) for h,v in provider["row"].items()},
            -Q(provider["coefficient_in_target"]))
    relation_coefficient = Q(1)/q
    need(target_identity == {h: relation_coefficient*v for h,v in U.items()},
         "exact latest-arrival identity target = earlier providers + U")
    wrong_sign = target.copy()
    for index, provider in enumerate(providers):
        sign = Q(provider["coefficient_in_target"])
        add(wrong_sign, {int(h): Q(v) for h,v in provider["row"].items()},
            sign if index == 0 else -sign)
    need(wrong_sign != {h: relation_coefficient*v for h,v in U.items()},
         "wrong provider sign mutant is rejected")
    need(word["program"][EXPECTED_EVENT] == ["MOVE",885,3,189,False],
         "literal target MOVE is public rank eight")
    need(len(frames[189]) == 8 and len(frames[3]) == 0,
         "source/destination dimensions are zero/eight")
    need(not zero_moves, "no whole-zero MOVE rows under U")

    author = json.loads(AUTHOR_RESULT.read_text())
    need(author["source_sha256"] == WORD_SHA and author["coframe_count"] == len(banks),
         "author census uses same source and coframe count")
    need(author["new_history_reconstructible_events"] == [EXPECTED_EVENT] and
         author["zero_MOVE_events"] == [], "author result agrees with independent exact-Q census")
    author_providers = [{"event": p["observation"]["event"],
        "owner": p["observation"]["owner"], "frame": p["observation"]["frame"],
        "coefficient_in_target": p["coefficient"], "row": p["row"]}
        for p in author["hits"][0]["providers"]]
    need(sorted(author_providers, key=lambda p:p["event"]) ==
         sorted(providers, key=lambda p:p["event"]),
         "provider values, owners, and coefficients match the author row")

    return {"status": "PASS_INDEPENDENT_EXACTQ_SINGLE_CIRCUIT_REVIEW",
        "source_sha256": WORD_SHA,
        "promise": encode(U),
        "move_count": len(move_rows),
        "observation_count": sum(map(len,banks.values())),
        "exact_frame_bank_count": len(banks),
        "all_original_history_rows_independent_over_Q": True,
        "promise_span_frames": {str(frame): size for frame,size in relation_frames.items()},
        "zero_MOVE_count": len(zero_moves),
        "newly_reconstructible_MOVE_events": [EXPECTED_EVENT],
        "latest_arrival_event": EXPECTED_EVENT,
        "latest_arrival_coefficient_in_U_expression": str(q),
        "target_identity_relation_coefficient": str(relation_coefficient),
        "providers": providers,
        "one_circuit_lemma": "Because each full exact-frame arrival bank is independent, every row has a unique representation. If U lies in the final bank span, the nonzero term with latest event is unique; only that arrival can be expressed using U and strictly earlier bank rows. Every earlier target would otherwise give a second U representation with later support removed.",
        "scope_warning": "This proves same-promise history coverage and the unique event 40710 circuit, but the circuit's provider uses initial e1459. A separate preparation claim that treats the demoted e1459 initial value as unavailable must justify that model premise before its rank-eight path bound is combined with this history identity.",
        "checks": {"frame189_dimension": 8, "frame3_dimension": 0,
                   "event40710_target_rank": 8, "strict_provider_events": [-1,40708],
                   "wrong_sign_negative_control": wrong_sign !=
                       {h: relation_coefficient*v for h,v in U.items()},
                   "zero_move_control": len(zero_moves)==0}}


if __name__ == "__main__":
    result = check()
    Path(__file__).with_name("ONE-CIRCUIT-REVIEW.json").write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True, indent=2))
