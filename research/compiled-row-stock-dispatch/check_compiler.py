"""Independent coordinate oracle for the source-generated compiler IR.

Native arithmetic stays opaque. Routes are checked against independently
constructed complements, with all selected columns and spectator bits present.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from dataclasses import replace
from pathlib import Path
import importlib.util
import sys


def load(relative,name):
    path=Path(__file__).resolve().parent/relative
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    exec(compile(path.read_bytes(),str(path),"exec"),module.__dict__)
    return module


r=load("row_programs.py","compiler_check_rows")
binder=load("compiler_routes.py","compiler_check_binder")
ir=load("vendor/lifecycle_source_ir.py","compiler_check_ir")
source=load("vendor/lockstep_executor.py","compiler_check_source")


def fixture_unit():
    # A compiler-control fixture, not a proposed native rank-(2,3) identity.
    events=(ir.Event("INIT",("o",)),ir.Event("COPY",("o","x")),
            ir.Event("PAID",("o",),("fixture-paid",),1),ir.Event("CLEAR",("o",)))
    return ir.Unit("route-fixture",(("x",2),("y",3)),("o",),events).check()


def source_scope(event,raw_roles,raw_ambient):
    """Read source grammar without binder layouts or swap words."""
    token=event.token
    tag=token[0] if token else None
    if event.op!="SERVICE":return None
    if tag in ("program-enter","program-return"):
        binding,index=token[1:]
        r.need(binding[2][index]==event.fields[0],"oracle exact source owner")
        kind=binding[1]
        if kind[0]=="source-complement":
            high=kind[1][1];size=kind[2]
            active=tuple(range(high-size,high))
        else:
            r.need(kind[0]=="deepest-exit","oracle named program source")
            size=kind[3];active=tuple(range(size))
        return tag.endswith("enter"),("program",binding,index),active,size
    if tag in ("occurrence-enter","occurrence-return"):
        column,name=token[6],token[8]
        size=raw_roles[name]*column
        return tag.endswith("enter"),("occurrence",token[1:]),tuple(range(size)),raw_ambient*column
    if tag in ("base-axis-enter","base-axis-return"):
        ordinary=token[1:]
        return tag.endswith("enter"),("base-axis",ordinary),(ordinary[-2],),1
    return None


def placement_oracle(unit,events,n,multiplicity,k=3,rho=1,start=5):
    fields={x for x,_ in unit.roles}|set(unit.owned)
    end=start+n*multiplicity*k
    size=end+7
    original=tuple(1<<i for i in range(size))
    actual={field:list(original) for field in fields}
    orders={field:list(range(n)) for field in fields}
    stacks={field:[] for field in fields}
    selected={start+(a*multiplicity+j)*k+rho for a in range(n) for j in range(multiplicity)}
    checks=paid=0

    def compare(field):
        nonlocal checks
        bits=actual[field]
        for axis in range(n):
            for j in range(multiplicity):
                at=start+(axis*multiplicity+j)*k+rho
                before=start+(orders[field][axis]*multiplicity+j)*k+rho
                r.need(bits[at]==1<<before,"source-derived selected coordinate at native boundary")
        r.need(all(bits[i]==original[i] for i in range(size) if i not in selected),
               "complete front/back fields and unselected bit planes unchanged")
        checks+=1

    for event in events:
        tag=event.token[0] if event.token else None
        if event.op=="SERVICE" and tag=="selected-bit-xor":
            field,=event.fields
            a,b=event.token[3:5]
            r.need(0<=a<n and 0<=b<n and a!=b,"literal selected XOR range")
            for j in range(multiplicity):
                source_bit=start+(a*multiplicity+j)*k+rho
                target_bit=start+(b*multiplicity+j)*k+rho
                actual[field][target_bit]^=actual[field][source_bit]
            continue
        scope=source_scope(event,{"x":2,"y":3},3)
        if scope is not None:
            entering,key,active,ambient=scope
            field,=event.fields
            if entering:
                compare(field)
                before=orders[field][:]
                complete=list(active)+[axis for axis in range(n) if axis not in active]
                r.need(len(complete)==n and len(set(complete))==n and ambient<=n,
                       "oracle full ambient permutation")
                stacks[field].append((key,before))
                orders[field]=[before[axis] for axis in complete]
            else:
                r.need(stacks[field] and stacks[field][-1][0]==key,"oracle nested source return")
                _,orders[field]=stacks[field].pop()
                compare(field)
        else:
            for field in event.fields:compare(field)
            if event.op=="PAID":
                field,=event.fields
                r.need(stacks[field] and stacks[field][-1][0]==("base-axis",event.token),
                       "actual PAID uses its canonical selected block")
                paid+=1
    for field in fields:
        r.need(not stacks[field],"all independent source scopes return")
        r.need(tuple(actual[field])==original,"literal coordinate return at complete endpoint")
    return dict(native_boundary_checks=checks,paid=paid)


def rejects(call):
    try:call()
    except ValueError:return
    raise ValueError("negative source-route control accepted")


def controls(unit,events,n):
    axis_id=next(e.token[1] for e in events if e.op=="SERVICE"
                 and e.token[0]=="selected-bit-xor" and e.token[2]=="enter"
                 and e.token[-1][0]=="base-axis-enter")
    missing_axis=tuple(e for e in events if not(e.op=="SERVICE" and e.token[0]=="selected-bit-xor"
                       and e.token[1]==axis_id and e.token[2]=="enter"))
    rejects(lambda:placement_oracle(unit,missing_axis,n,2))
    index=next(i for i,e in enumerate(events) if e.op=="SERVICE"
               and e.token[0]=="selected-bit-xor" and e.token[2]=="return")
    rejects(lambda:placement_oracle(unit,events[:index]+events[index+1:],n,2))
    first=next(i for i,e in enumerate(events) if e.op=="SERVICE" and e.token[0]=="selected-bit-xor")
    e=events[first]
    wrong_field=next(x for x,_ in unit.roles if x!=e.fields[0])
    wrong_owner=events[:first]+(replace(e,fields=(wrong_field,)),)+events[first+1:]
    rejects(lambda:placement_oracle(unit,wrong_owner,n,2))
    routed=ir.Unit(unit.name,unit.roles,unit.owned,events)
    rejects(lambda:binder.bind(routed,n,3,{"x":2,"y":3}))
    old_axis=tuple(e for e in unit.events if not(e.op=="SERVICE"
                   and e.token and e.token[0] in ("base-axis-enter","base-axis-return")))
    rejects(lambda:binder.bind(ir.Unit(unit.name,unit.roles,unit.owned,old_axis),n,3,{"x":2,"y":3}))
    return ["deleted_actual_axis_entry","deleted_actual_inverse_xor",
            "wrong_actual_owner_xor","double_route_binding","missing_source_axis_boundaries"]


def check():
    reports=[]
    negative=None
    for n in range(3,9):
        unit,source_report,_=ir.lower(fixture_unit(),n,source)
        events,report,_=binder.bind(unit,n,3,{"x":2,"y":3})
        routed=ir.Unit(unit.name,unit.roles,unit.owned,events)
        ownership=ir.check_flat_ownership(routed)
        checks=[placement_oracle(unit,events,n,f) for f in (1,2,3)]
        r.need(all(c['paid']==source_report['paid'] for c in checks),"actual paid count retained")
        r.need(report['selected_xor_records']==6*report['entry_swaps'],"actual finite route tariff")
        r.need(report['matched_row_divisors']==0,"no compiler-internal row division")
        reports.append(dict(rank=n,width=source_report['width'],**report,
                            placement_checks=sum(c['native_boundary_checks'] for c in checks),
                            private_borrow_entries=ownership['counts'].get('private_occurrence_entries',0)))
        if n==8:negative=controls(unit,events,n)
    return dict(source_generated_instances=reports,rejections=negative)


if __name__=="__main__":
    print(check())
    print("PASS_SOURCE_COMPILER_ROUTES")
