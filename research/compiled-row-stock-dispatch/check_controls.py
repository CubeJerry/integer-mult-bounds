"""Literal coded complete rows and source-composition counterexamples."""
from pathlib import Path
import importlib.util
import sys


def load(relative,name):
    path=Path(__file__).resolve().parent/relative
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    exec(compile(path.read_bytes(),str(path),"exec"),module.__dict__)
    return module


r=load("row_programs.py","control_row_programs")
f=load("fixture_tools.py","control_fixture")
hardware=load("vendor/continuation_stack.py","control_hardware")


def raw(word="",marker=2,offset=0,retained=0):
    tape=hardware.Tape(tuple((i+1)%2 for i in range(offset)),marker)
    tape.cells.extend(int(bit) for bit in word)
    tape.cells.extend([6]*retained)
    return tape


def text(tape):
    result=[]
    at=tape.floor+1
    while at<len(tape.cells) and tape.cells[at]!=6:
        r.need(tape.cells[at] in (0,1),"observer contiguous raw bit word")
        result.append(str(tape.cells[at]));at+=1
    r.need(all(v==6 for v in tape.cells[at:]),"observer no hidden live suffix")
    return "".join(result)


def run(table,words,base_ports=()):
    tapes=[raw(words.get(i,""),5 if i in base_ports else 2,offset=1+i%5,retained=7+i%3)
           for i in range(r.FIRST_ROLE+7)]
    initial_prefix=[tuple(t.cells[:t.floor+1]) for t in tapes]
    ports=[r.PhysicalPort(t,5 if i in base_ports else 2) for i,t in enumerate(tapes)]
    steps=r.run(table,ports)
    for t,prefix in zip(tapes,initial_prefix):
        r.need(tuple(t.cells[:t.floor+1])==prefix,"raw adapter preserves buried ancestors")
        r.need(t.head==t.floor+1,"raw adapter returns every local head")
    return {i:text(t) for i,t in enumerate(tapes)},steps,sum(t.counts.total for t in tapes)


def code(symbol):
    return format(symbol,"03b")


def component(value,width=3):
    unsigned=value%(1<<width)
    return "".join(code((unsigned>>j)&1) for j in range(width))+code(2)


def complete_row(outer,row):
    # Address bits0,1 are complete front fields, bit2 the selected block,
    # bit3 the complete back field. Each Gaussian coefficient has two signed
    # components and exact COMPONENT=010 delimiters.
    return "".join(component((outer+row+address)%7-3)
                   +component((3*outer+2*row+address)%7-3)
                   for address in range(16))


def coded_checks():
    report=[]
    for g,rows in ((2,6),(3,9),(5,15),(7,21)):
        c=2;j=len(complete_row(0,0));record=j//16
        parent=f.values(r.SCHEMA,outer=c,rows=rows,stock=g,row_bits=j)
        parent.update(within_bits=4,record_bits=record,K=1,H=1,rho=0,
                      entry_start=2,active_start=2,back_start=3,selected_axes=1,q0=4)
        prepared,_,_=run(r.compile_prepare(g),{r.HEADER:f.encode_header(r.SCHEMA,parent)},(r.CHILD_HEADER,))
        child=f.decode_header(r.SCHEMA,prepared[r.CHILD_HEADER])
        r.need(child==dict(parent,rows=3,stock=1),"nonbinary child count retains fixed within-row geometry")
        payload="".join(complete_row(a,u) for a in range(c) for u in range(rows))
        split,steps,physical=run(r.compile_router(g),{r.HEADER:prepared[r.CHILD_HEADER],r.SOURCE:payload},
                                 (r.HEADER,r.SOURCE))
        returned={r.HEADER:prepared[r.CHILD_HEADER]}
        for w in range(g):
            expected="".join(complete_row(a,g*b+w) for a in range(c) for b in range(3))
            r.need(split[r.FIRST_ROLE+w]==expected,"every coded record and full control fibre copied")
            word=split[r.FIRST_ROLE+w]
            changed=[]
            for begin in range(0,len(word),j):
                row=word[begin:begin+j]
                changed.append("".join(row[(a^4)*record:((a^4)+1)*record] for a in range(16)))
            returned[r.FIRST_ROLE+w]="".join(changed)
        merged,more,ops=run(r.compile_router(g,True),returned,(r.OUTPUT,))
        expected="".join(payload[begin+(a^4)*record:begin+((a^4)+1)*record]
                         for begin in range(0,len(payload),j) for a in range(16))
        r.need(merged[r.OUTPUT]==expected,"completed rowwise operation returns at exact source row")
        r.need(all(not merged[r.FIRST_ROLE+w] for w in range(g)),"literal role retirement")
        report.append(dict(divisor=g,parent_rows=rows,child_rows=3,row_bits=j,
                           physical_bits=len(payload),table_steps=steps+more,physical_ops=physical+ops))
    return report


def reject(call):
    try:call()
    except ValueError:return
    raise ValueError("negative composition control accepted")


def controls():
    # A wrong composition may preserve field count, byte count and field size.
    # Existing matched owners00 and11 become01 and01 if treated as one packet.
    header=f.values(r.SCHEMA,outer=1,rows=2,stock=1,row_bits=1)
    wrong,_,_=run(r.compile_router(2),{r.HEADER:f.encode_header(r.SCHEMA,header),r.SOURCE:"0011"})
    wrong_fields=(wrong[r.FIRST_ROLE],wrong[r.FIRST_ROLE+1])
    r.need(tuple(map(len,wrong_fields))==(2,2),"wrong composer preserves nominal shape")
    r.need(wrong_fields==("01","01") and wrong_fields!=("00","11"),
           "actual row split destroys distinct matched owner bindings")
    reject(lambda:r.compile_prepare(2,kind=r.MATCHED))
    # Reusing max(3,3)=3 for two ordinary factors fails although9 rows fit.
    parent=f.values(r.SCHEMA,rows=9,stock=3)
    first,_,_=run(r.compile_prepare(3),{r.HEADER:f.encode_header(r.SCHEMA,parent)})
    reject(lambda:run(r.compile_prepare(3),{r.HEADER:first[r.CHILD_HEADER]}))
    good,_,_=run(r.compile_prepare(3),{r.HEADER:f.encode_header(r.SCHEMA,dict(parent,stock=9))})
    run(r.compile_prepare(3),{r.HEADER:good[r.CHILD_HEADER]})
    # Same encoded shape, but a fresh log2(rows) rebase changes phi. It is not
    # the source's pair (row ordinal, within-row coordinates).
    original=f.values(r.SCHEMA,rows=6,stock=2,row_bits=8)
    original.update(q0=3,K=2,active_start=4,rho=1)
    child_words,_,_=run(r.compile_prepare(2),{r.HEADER:f.encode_header(r.SCHEMA,original)})
    child=f.decode_header(r.SCHEMA,child_words[r.CHILD_HEADER])
    good_phi=child['active_start']+child['rho']
    bad_phi=good_phi+original['q0']*original['K']-(child['rows']-1).bit_length()
    r.need(child['rows']==3 and bad_phi!=good_phi,"wrong arbitrary-row binary rebase changes selected offset")
    # Wrong payload lengths are tested against actual table frontiers.
    short=f.values(r.SCHEMA,rows=1,stock=1,row_bits=3)
    for value in ("01001","0100101"):
        reject(lambda value=value:run(r.compile_router(2),
               {r.HEADER:f.encode_header(r.SCHEMA,short),r.SOURCE:value}))
    return dict(rejections=["matched_event_row_call","max_replaces_repeated_stock_product",
                            "short_complete_packet","extra_complete_packet"],
                counterexamples=["same_shape_matched_owner_mixing","fresh_log_rows_rebases_phi"],
                wrong_matched_outputs=wrong_fields)


def check():
    return dict(coded_complete_rows=coded_checks(),adverse_controls=controls())


if __name__=="__main__":
    print(check())
    print("PASS_COMPLETE_CODED_ROW_CONTROLS")
