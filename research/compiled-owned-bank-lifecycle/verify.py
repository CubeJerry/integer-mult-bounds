#!/usr/bin/env python3
"""Replay the scoped source/lifecycle certificate without cached imports.

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
Default mode is read-only. --write-result regenerates the package receipt.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys
import types

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def need(ok,message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def authenticated(data,row):
    need(digest(data)==row["sha256"],"SHA256 source drift: "+row.get("path",row.get("local_path","")))
    blob=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
    need(blob==row["git_blob"],"Git blob source drift")
    return data


def module(name,path,data):
    result=types.ModuleType(name)
    result.__file__=str(path)
    sys.modules[name]=result
    exec(compile(data,str(path),"exec"),result.__dict__)
    return result


def seed(IR):
    E=IR.Event
    return IR.Unit("lifecycle-seed",(("a",3),("b",5)),("c",),(
        E("INIT",("c",)),E("COPY",("c","a")),E("PAID",("c",),("center",1),1),
        E("SERVICE",("b","c"),("contact",)),E("CLEAR",("c",)),
        E("INIT",("c",)),E("COPY",("c","b")),E("PAID",("c",),("center",2),2),
        E("CLEAR",("c",)),E("PAID",("a",),("public",),1))).check()


def source_grammar(IR,unit):
    left=unit;right=unit
    prod=IR.product(left,right)
    l=Counter(e.op for e in left.events);r=Counter(e.op for e in right.events)
    got=Counter(e.op for e in prod.events)
    expected={op:len(right.roles)*l[op]+l["PAID"]*r[op]
              for op in ("INIT","CLEAR","COPY","SERVICE")}
    expected["SERVICE"]+=2*len(left.roles)*len(right.roles)+2*l["PAID"]*len(right.roles)
    expected["PAID"]=l["PAID"]*r["PAID"]
    need(dict(got)==expected,"complete chronological-product event bill")
    need(len(prod.owned)==len(right.roles)*len(left.owned)+l["PAID"]*len(right.owned),
         "occurrence-path product private inventory")
    passed=IR.completion_split(prod,2,10)
    jobs=[e for e in passed.events if e.op=="PAID"]
    need(any(e.token[1]>0 for e in jobs),"actual nonleading split piece exercised")
    need(any(e.token[-1][0]=="completion" for e in jobs),"actual completion exercised")
    completed=sum(k<10 for _,k in prod.roles)
    pieces=sum((e.rank+1)//2 for e in prod.events if e.op=="PAID")
    pieces+=sum((10-k+1)//2 for _,k in prod.roles if k<10)
    out=Counter(e.op for e in passed.events)
    need(out["PAID"]==pieces and out["SERVICE"]==got["SERVICE"]+2*completed+2*pieces,
         "complete completion/splitting event bill")
    need(all(out[op]==got[op] for op in ("INIT","COPY","CLEAR")),"wrappers retain all physical lifetimes")
    return passed,dict(product=dict(sorted(got.items())),completed_roles=completed,
                       pass_events=dict(sorted(out.items())),owned=len(passed.owned))


def run():
    sources=json.loads((HERE/"SOURCES.json").read_bytes())
    inputs={row["path"]:authenticated((ROOT/row["path"]).read_bytes(),row)
            for row in sources["files"] if row["usage"]=="input"}
    deps=json.loads((HERE/"DEPENDENCIES.json").read_bytes())
    for row in deps["files"]:
        authenticated((HERE/row["local_path"]).read_bytes(),row)
    package={name:(HERE/name).read_bytes() for name in ("machine.py","source_ir.py","checks.py")}
    M=module("bound_lifecycle",HERE/"machine.py",package["machine.py"])
    IR=module("bound_source_ir",HERE/"source_ir.py",package["source_ir.py"])
    C=module("bound_lifecycle_checks",HERE/"checks.py",package["checks.py"])
    sp="research/delimited-continuation-stack/stack.py"
    cp="research/lockstep-completion-pass/executor.py"
    S=module("bound_inherited_stack",ROOT/sp,inputs[sp])
    compiler=module("bound_inherited_compiler",ROOT/cp,inputs[cp])
    word=json.loads(gzip.decompress(inputs["research/p104-helper470-twin-rung-removal/WORD.json.gz"]))
    caller=json.loads(inputs["research/p104-productive-controller/CONTROLLER.json"])
    selected=json.loads(inputs["research/p104-helper470-twin-rung-removal/RESULT.json"])["complete_cost"]
    raw,profile=IR.current_caller(word,caller)
    need(profile["raw_paid"]=={int(k):v for k,v in selected["paid"].items()},"current complete paid profile")
    need(profile["raw_targets"]=={int(k):v for k,v in selected["targets"].items()},"current complete target profile")
    need(len(raw.roles)==selected["productive_fields"]==13444,"current productive width")
    small=seed(IR)
    compiled={};lowerings=[]
    for rank in (5,15,20):
        unit,report,occurrences=IR.lower(small,rank,compiler)
        report["flat_ownership"]=IR.check_flat_ownership(unit)
        compiled[rank]=unit;lowerings.append(report)
    passed,grammar=source_grammar(IR,small)
    unit,report,occurrences=IR.lower(passed,25,compiler)
    report["flat_ownership"]=IR.check_flat_ownership(unit)
    lowerings.append(report)
    physical=[C.fixture(compiled[5],M,S,records=4,depth=2,prefix=17,warm=7,cycles=2),
              C.fixture(compiled[15],M,S,records=10,depth=1,prefix=257,warm=11,cycles=2),
              C.fixture(compiled[20],M,S,records=1,depth=0,prefix=257,warm=11,cycles=2),
              C.fixture(unit,M,S,records=4,depth=1,prefix=17,warm=7,cycles=2),
              C.fixture(raw,M,S,records=1,depth=0,cycles=2)]
    profile["event_counts"]=dict(sorted(Counter(e.op for e in raw.events).items()))
    result=dict(schema_version=1,status="PASS_SOURCE_BOUND_PHYSICAL_LIFECYCLE",
                scope="Relative source-refinement and physical lifecycle; all five selected assumptions retained",
                base_commit=sources["base_commit"],
                package_sha256={name:digest(data) for name,data in package.items()},
                dependency_count=len(inputs)+len(deps["files"]),
                current_source=profile,grammar=grammar,lowerings=lowerings,
                physical_fixtures=physical,arithmetic=C.arithmetic_checks(M,S),
                context=C.context_checks(M,S),boundaries=C.boundary_checks(M,S),
                negative_controls=C.rejection_controls(M,S,IR,compiler,word,small,compiled[5]))
    # Mutations are detected from captured bytes before parsing or executing.
    row=sources["files"][0]
    try:authenticated(inputs[row["path"]]+b"\n",row)
    except ValueError:result["negative_controls"]["source_drift"]="SHA256 source drift before execution"
    else:raise ValueError("source drift accepted")
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-result",action="store_true")
    args=parser.parse_args()
    result=run()
    if args.write_result:
        (HERE/"RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    else:
        expected=json.loads((HERE/"RESULT.json").read_bytes())
        need(json.loads(json.dumps(result))==expected,"committed scientific receipt differs")
    print(json.dumps(dict(status=result["status"],source_events=result["current_source"]["raw_events"],
                          source_lifetimes=result["current_source"]["total_lifetimes"],
                          physical_fixtures=len(result["physical_fixtures"]),
                          negative_controls=len(result["negative_controls"]),
                          result_sha256=digest(json.dumps(result,sort_keys=True).encode())),sort_keys=True))


if __name__=="__main__":
    main()
