"""Physical row/lifecycle ABI join on source-generated finite words.

Native/coordinate fixtures here are not Gaussian providers. Coordinate route
meaning is independently checked by check_compiler. This joins real row
tables, stack/lifecycle, encoded headers and finite value-changing tables.
"""
from pathlib import Path
import importlib.util
import sys


def load(relative,name):
    path=Path(__file__).resolve().parent/relative
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    exec(compile(path.read_bytes(),str(path),"exec"),module.__dict__)
    return module


r=load("row_programs.py","join_rows")
f=load("fixture_tools.py","join_fixtures")
services=load("services.py","join_row_services")
routes=load("compiler_routes.py","join_routes")
ir=load("vendor/lifecycle_source_ir.py","join_ir")
source=load("vendor/lockstep_executor.py","join_compiler")
m=load("vendor/lifecycle_machine.py","join_machine")
hardware=load("vendor/continuation_stack.py","join_hardware")


def raw(word="",marker=2,offset=0,retained=0):
    t=hardware.Tape(tuple(i%2 for i in range(offset)),marker)
    t.cells.extend(int(x) for x in word)
    t.cells.extend([6]*retained)
    return t


def current_word(t):
    at=t.head;out=[]
    while at<len(t.cells) and t.cells[at]!=6:
        r.need(t.cells[at] in (0,1),"observer at complete current body")
        out.append(str(t.cells[at]));at+=1
    return "".join(out)


def code(value):return format(value,"03b")


def field(rows,within_bits,seed):
    records=[]
    for i in range(rows*(1<<within_bits)):
        for value in ((seed+i)%8,(3*seed+i)%8):
            records.append("".join(code((value>>j)&1) for j in range(3))+code(2))
    return "".join(records)


def zero_format(word):
    symbols=[int(word[i:i+3],2) for i in range(0,len(word),3)]
    r.need(all(x in (0,1,2) for x in symbols),"oracle canonical components")
    return "".join(code(2 if x==2 else 0) for x in symbols)


def add_words(left,right):
    def decode(word):
        words=[];digits=[]
        for i in range(0,len(word),3):
            value=int(word[i:i+3],2)
            if value==2:
                r.need(digits,"oracle positive signed width")
                unsigned=sum(bit<<j for j,bit in enumerate(digits))
                words.append((unsigned-(1<<len(digits)) if digits[-1] else unsigned,len(digits)))
                digits=[]
            else:
                r.need(value in (0,1),"oracle value bit");digits.append(value)
        r.need(not digits,"oracle complete component")
        return words
    a,b=decode(left),decode(right)
    r.need(len(a)==len(b),"oracle equal complete format")
    out=[]
    for (x,w),(y,v) in zip(a,b):
        value=x+y
        r.need(w==v and -(1<<(w-1))<=value<(1<<(w-1)),"oracle signed headroom")
        out.append("".join(code((value>>j)&1) for j in range(w))+code(2))
    return "".join(out)


def rotate_value(word):return word[6:9]+word[:6]+word[9:]


def leaf_table():
    """Literal fixture: cyclically rotate first three numeric symbols."""
    out=[]
    def read_prefix(prefix):
        index=len(out);out.append(None);targets=[]
        for bit in (0,1):
            targets.append((bit,len(out)))
            if len(prefix)<2:
                out.append(("move",0,1));read_prefix(prefix+(bit,))
            else:
                a,b,c=prefix+(bit,)
                out.extend((("move",0,-1),("move",0,-1),("write",0,c),
                            ("move",0,1),("write",0,a),("move",0,1),
                            ("write",0,b),("halt",)))
        out[index]=("branch",0,tuple(targets),-1)
    read_prefix(())
    reject=len(out);out.append(("reject","fixture expects three value symbols"))
    return tuple((row[0],row[1],row[2],reject) if row[0]=="branch" else row for row in out)


def raw_unit():
    return ir.Unit("joined-control-fixture",(("x",2),("y",3)),("o",),
                   (ir.Event("INIT",("o",)),ir.Event("COPY",("o","x")),
                    ir.Event("PAID",("o",),("fixture-paid",),1),
                    ir.Event("CLEAR",("o",)))).check()


def oracle(events,public,width,rows,row_bits,header,numerical,counts):
    values={i:word for i,word in enumerate(public)};live=set()
    for e in events:
        if e.op=="INIT":
            key,=e.fields;values[key]=zero_format(values[0]);live.add(key)
        elif e.op=="CLEAR":
            key,=e.fields;r.need(key in live,"oracle private lifetime")
            del values[key];live.remove(key)
        elif e.op=="COPY":
            a,b=e.fields;values[a]=add_words(values[a],values[b])
        elif e.op=="SERVICE":
            pass  # Explicit identity fixture, not native/geometry admission.
        elif e.op=="PAID":
            key,=e.fields
            leaf=header['f']<=header['cutoff'] if numerical else header['stock']==1
            counts['paid']+=1
            if leaf:
                values[key]=rotate_value(values[key]);counts['leaves']+=1
            else:
                r.need(rows%width==0,"oracle exact row division")
                q=rows//width;packet=values[key]
                children=["".join(packet[(b*width+w)*row_bits:(b*width+w+1)*row_bits]
                                   for b in range(q)) for w in range(width)]
                child=dict(header,rows=q,stock=header['stock']//width)
                if numerical:
                    new_e=header['f'];n=2
                    child.update(selected_axes=new_e,entry_start=header['active_start'],
                                 f=new_e//n,remainder=new_e%n,
                                 active_start=header['active_start']+(new_e%n)*header['K'])
                returned=oracle(events,children,width,q,row_bits,child,numerical,counts)
                values[key]="".join(returned[w][b*row_bits:(b+1)*row_bits]
                                    for b in range(q) for w in range(width))
                counts['children']+=1
    r.need(not live,"oracle closes all private lifetimes")
    return tuple(values[i] for i in range(width))


def one_case(n,numerical=False):
    unit,summary,_=ir.lower(raw_unit(),n,source)
    events,route_report,_=routes.bind(unit,n,3,{"x":2,"y":3})
    width=summary['width'];field_count=width+len(unit.owned)
    rows=1 if numerical else width*width
    a=9 if numerical else 3;j=24*(1<<a)
    header=f.values(r.SCHEMA,rows=rows,stock=rows,row_bits=j)
    header.update(within_bits=a,record_bits=24,cutoff=n,K=1,rho=0,H=1,
                  entry_start=2,active_start=2,back_start=a-1,
                  selected_axes=6 if numerical else n,f=3 if numerical else 1,remainder=0)
    inputs=tuple(field(rows,a,seed=1+i) for i in range(width))
    payloads=[raw(inputs[i] if i<width else field(1,0,seed=2),offset=i%4,retained=11)
              for i in range(field_count)]
    descriptor_index=len(payloads)
    payloads.append(raw(f.encode_header(r.SCHEMA,header),offset=3,retained=9))
    work_first=len(payloads)
    payloads.extend(raw(offset=i%5,retained=20+i) for i in range(r.FIRST_ROLE))
    control,pc,bridge,staged=(raw(marker=5,offset=i+1,retained=23+i) for i in range(4))
    all_tapes=payloads+[control,pc,bridge,staged]
    prefixes=[tuple(t.cells[:t.floor+1]) for t in all_tapes]
    sites={e.token:r.ROW_CHILD for e in events if e.op=="PAID"}
    remainder_count=0
    def remainder(public,descriptor):
        nonlocal remainder_count
        # Counted raw-context read; explicitly an identity fixture, not the
        # elementary Gaussian remainder provider.
        table=(("branch",len(public),((0,1),(1,1)),2),("halt",),
               ("reject","fixture context header"))
        m.execute_table(table,public,(descriptor,));remainder_count+=1
    row_service=services.RowServices(width,payloads[descriptor_index],payloads[work_first:],sites,
                 rank=n if numerical else None,
                 remainder_service=remainder if numerical else None,
                 leaf_decider=None if numerical else services.StockLeafFixture())
    native={e.token:(("halt",),) for e in events if e.op=="SERVICE"}
    native.update({("leaf",)+e.token:leaf_table() for e in events if e.op=="PAID"})
    program=tuple(m.Instruction(e.op,e.fields,e.token) for e in events)+(m.Instruction("RET"),)
    machine=m.Controller(program,width,payloads,control,pc,bridge,staged,row_service,native,
                         hardware.Stack,protected_ports=(descriptor_index,),
                         primitive_context=(descriptor_index,))
    observed_headers=set()
    def observe(when,pc_value,event):
        if when=="before" and event.op=="PAID":
            decoded=f.decode_header(r.SCHEMA,current_word(payloads[descriptor_index]))
            observed_headers.add((decoded['rows'],decoded['stock'],decoded['selected_axes'],
                                  decoded['f'],decoded['entry_start'],decoded['active_start']))
    counts={'paid':0,'leaves':0,'children':0}
    expected=oracle(events,inputs,width,rows,j,header,numerical,counts)
    machine.run(observe)
    r.need(tuple(current_word(t) for t in payloads[:width])==expected,"joined source value oracle")
    r.need(current_word(payloads[descriptor_index])==f.encode_header(r.SCHEMA,header),
           "joined exact parent descriptor")
    r.need(all(not current_word(t) for i,t in enumerate(payloads) if i>=width and i!=descriptor_index),
           "joined all private and row scratch retired")
    r.need(all(not current_word(t) for t in (pc,bridge,staged)),"joined relay retirement")
    first_backing=tuple(len(t.cells) for t in all_tapes)
    expected_again=oracle(events,expected,width,rows,j,header,numerical,
                          {'paid':0,'leaves':0,'children':0})
    machine.run()
    r.need(tuple(current_word(t) for t in payloads[:width])==expected_again,"joined repeated values")
    r.need(tuple(len(t.cells) for t in all_tapes)==first_backing,"joined retained capacity reused")
    for t,prefix in zip(all_tapes,prefixes):
        r.need(tuple(t.cells[:t.floor+1])==prefix,"joined translated ancestor prefix")
    if numerical:
        r.need((1,1,6,3,2,2) in observed_headers and (1,1,3,1,2,3) in observed_headers,
               "actual encoded numerical child geometry in physical continuation")
        r.need(remainder_count==2*counts['children'],"all numerical child remainder fixture sites")
    return dict(rank=n,width=width,source_events=len(unit.events),routed_events=len(events),
                root_rows=rows,row_bits=j,counts_one_run=counts,
                observed_headers=sorted(observed_headers),physical_actions_two_runs=sum(t.counts.total for t in all_tapes),
                retained_cells=sum(first_backing),row_table_steps_two_runs=row_service.observed_steps,
                mode="encoded_numerical_geometry" if numerical else "stock_depth_structural",
                native_fixture="identity native/coordinate services plus cyclic value-bit leaf; not Gaussian admission",
                selected_xor_records=route_report['selected_xor_records'])


def check():
    return dict(joined_cases=[one_case(6),one_case(2,True)])


if __name__=="__main__":
    print(check())
    print("PASS_SOURCE_ROW_LIFECYCLE_JOIN")
