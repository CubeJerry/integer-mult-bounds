"""Independent full-grid oracle versus literal whole-router executions."""
from pathlib import Path
from contextlib import contextmanager
from itertools import product
import argparse
import ast
import json
import sys
import time
PACKAGE=Path(__file__).resolve().parent
sys.path.insert(0,str(PACKAGE))
from runtime_sources import physical_runtime
from fixture_tools import need,emit,body,snapshot,frame,bank,integer,digest,nonlinear_oracle

CASES=[
    (1,2,((0,1),),4,17),
    (2,4,((0,1,3),(1,3)),7,17),
    (3,4,((0,1,3),(1,2,3),(0,2,3)),8,513),
    (2,5,((0,1,2,3,4),(0,1,2,3,4)),8,17),
    (4,3,((0,),(),(0,2),(0,1,2)),8,33),
    (3,3,((),(),()),6,65),
    (6,2,((0,),)*6,5,17),
    (2,3,((0,2),(1,)),8,4097),
]


def stable(value):
    if isinstance(value,dict):
        return {k:stable(v) for k,v in value.items() if k!='seconds'}
    if isinstance(value,(tuple,list)):
        return [stable(v) for v in value]
    return value


def check_static():
    files=('physical_router.py','union_bits.py','union_catalogue.py','union_fields.py')
    counts={}
    for name in files:
        tree=ast.parse((PACKAGE/name).read_text())
        for node in ast.walk(tree):
            if isinstance(node,ast.Attribute):
                need(node.attr not in ('cells','head','to_int','decode','value'),
                     'no host tape/index decoding in '+name)
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Name):
                need(node.func.id not in ('sorted','eval','exec','getattr'),
                     'no host sorting/evaluation in '+name)
                if node.func.id=='range':
                    need(len(node.args)==1 and isinstance(node.args[0],ast.Constant)
                         and node.args[0].value in (8,19),'fixed constructor inventory range')
                if node.func.id=='int':
                    need(len(node.args)==1 and isinstance(node.args[0],ast.Name)
                         and node.args[0].id in ('member','keep'),'only finite boolean int conversion')
        counts[name]=sum(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) for n in ast.walk(tree))
    return dict(no_host_index_or_sort=True,fixed_constructor_ranges=True,functions=counts)


def meter(tapes):
    return tuple(sum(getattr(t.meter,k) for t in tapes) for k in ('reads','writes','moves'))


def difference(tapes,before):
    return tuple(a-b for a,b in zip(meter(tapes),before))


@contextmanager
def fixture(case,changed_context=False,malform=None):
    from records import Tape
    from cardinal_counts import Count
    g,L,E,w,keylen=case;h=(L-1).bit_length();t=g.bit_length()
    context=bytes(((7*i+3)//5)&1 for i in range(keylen))
    catalogue_context=context[:-1]+bytes((1-context[-1],)) if changed_context else context
    values=[(((37*i+11)%(1<<(w-1)))-(1<<(w-2)),((11*i+3)%7)-3) for i in range(L**g)]
    # Small widths still need imaginary values in their signed carrier.
    values=[(a,max(-(1<<(w-1)),min((1<<(w-1))-1,b))) for a,b in values]
    source,cat=Tape(),Tape()
    data=frame(context,values,w)
    masks=tuple((1,)*len(e) for e in E)
    cat_data=bank(catalogue_context,E,masks,(2,)*g,w,h)
    if malform is not None:
        data,cat_data=malform(data,cat_data)
    emit(source,data);emit(cat,cat_data)
    metadata=tuple(Count.literal(x) for x in (g,L,h,t,w,0))
    try:
        yield source,cat,metadata,values,context
    finally:
        for c in metadata:
            c.close()
        source.clear();cat.clear()


def run_case(owner,child,all_tapes,case,pending_control=False):
    from check_support import no_decode
    from words import BLANK
    g,L,E,w,keylen=case
    with fixture(case) as (source,cat,metadata,values,context):
        ports=(source,cat,*(c.tape for c in metadata));saved=snapshot(ports)
        before=meter(all_tapes); started=time.monotonic()
        observations=(owner.rounds,owner.visits,owner.substreams,child.lines)
        with no_decode():
            result=owner.run(source,cat,*metadata)
        actions=difference(all_tapes,before)
        raw=body(result);off=len(context)+1
        need(raw[:off]==context+bytes((5,)),'full context preserved')
        actual=[(integer(raw[i:i+w]),integer(raw[i+w:i+2*w])) for i in range(off,len(raw),2*w)]
        expected,changed=nonlinear_oracle(L,E,values)
        need(actual==expected,'independent ascending-axis nonlinear grid result')
        need(snapshot(ports)==saved,'all borrowed whole-union source bytes/heads restored')
        pending_rejected=False
        if pending_control:
            while result.read()!=BLANK:
                result.step(1)
            for _ in range(7):
                result.step(1)
            try:
                with no_decode():
                    owner.run(source,cat,*metadata)
            except ValueError as error:
                pending_rejected='consume protected' in str(error)
            need(pending_rejected,'pending output protected even beyond its live end')
        consume_before=meter(all_tapes)
        with no_decode():
            owner.consume()
        consume=difference(all_tapes,consume_before)
        need(all(t.head==1 and all(v==BLANK for v in t.cells) for t in owner.forbidden()),
             'all fixed owned roles including blank history erased')
        need(snapshot(ports)==saved,'borrowed source restoration after output consumption')
        rounds,visits,substreams,lines=(a-b for a,b in zip(
            (owner.rounds,owner.visits,owner.substreams,child.lines),observations))
        incidence=sum(len(e)*L**(g-1) for e in E)
        need(visits==incidence,'exact complete incidence count')
        need(lines==sum(bool(e)*L**(g-1) for e in E),'every exposed line exactly once')
        controls=dict(wrong_axis_order_differs=nonlinear_oracle(L,E,values,reverse=True)[0]!=expected,
                      stale_values_differ=nonlinear_oracle(L,E,values,stale=True)[0]!=expected,
                      dropped_axis_differs=any(nonlinear_oracle(L,E,values,drop=i)[0]!=expected for i in range(g)))
        return dict(g=g,L=L,E=E,w=w,context_bits=keylen,rounds=rounds,visits=visits,
                    substreams=substreams,lines=lines,actions=actions,consume_actions=consume,
                    retained_cells=sum(len(t.cells) for t in owner.forbidden()),
                    parent_counter_max_cells=max(len(t.cells) for t in owner.pool.tapes),
                    pool_peak=owner.pool.peak,changed_later_lines=changed,
                    controls=controls,pending_guard=pending_rejected,
                    output_sha256=digest(actual),seconds=time.monotonic()-started)


def expect_failure(owner,case,*,context=False,malform=None,message=None):
    from check_support import no_decode
    from words import BLANK
    with fixture(case,context,malform) as (source,cat,metadata,values,key):
        ports=(source,cat,*(c.tape for c in metadata));saved=snapshot(ports)
        try:
            with no_decode():
                owner.run(source,cat,*metadata)
        except ValueError as error:
            observed=str(error)
        else:
            if owner.pending:
                owner.consume()
            raise ValueError('adverse whole-union control unexpectedly accepted')
        if message is not None:
            need(message in observed,'expected rejecting cause: '+observed)
        need(snapshot(ports)==saved,'failed call restores all borrowed source views')
        need(owner.closed and not owner.pending and not owner.pool.live,
             'failed call returns closed with no protected result')
        need(all(t.head==1 and all(v==BLANK for v in t.cells) for t in owner.forbidden()),
             'failure erases complete fixed-role historical backing')
        return observed


def failures(owner,child):
    import physical_router
    from cardinal_counts import Count
    from router_metadata import owned
    case=CASES[1]
    out={}
    out['different_complete_context']=expect_failure(owner,case,context=True,message='same complete')
    out['truncated_dense_word']=expect_failure(owner,case,malform=lambda d,c:(d[:-1],c),message='binary')
    out['truncated_page_bank']=expect_failure(owner,case,malform=lambda d,c:(d,c[:-3]),message='delimiter')
    duplicate=(2,4,((0,0,3),(1,3)),7,17)
    out['duplicate_exposed_coordinate']=expect_failure(owner,duplicate,message='strict source exposed')
    def bad_mask(data,cat):
        raw=bytearray(cat);at=raw.index(5)+2
        for _ in range(3):
            at=raw.index(3,at)+1
        at=raw.index(5,at)+1;raw[at]=1-raw[at]
        return data,bytes(raw)
    out['wrong_source_mask_count']=expect_failure(owner,case,malform=bad_mask,message='J-mask')
    def bad_count(data,cat):
        raw=bytearray(cat);at=raw.index(5)+2
        at=raw.index(3,at)+1
        raw.insert(raw.index(3,at),0)
        return data,bytes(raw)
    out['noncanonical_second_count']=expect_failure(owner,case,malform=bad_count,message='canonical catalogue count')
    def nonbinary(data,cat):
        raw=bytearray(data);raw[len(raw)//2]=9
        return bytes(raw),cat
    out['nonbinary_dense_payload']=expect_failure(owner,case,malform=nonbinary,message='binary')
    original_run=child.run
    seen=0
    def fail_second(*args,**kwargs):
        nonlocal seen
        result=original_run(*args,**kwargs);seen+=1
        if seen==2:
            raise ValueError('injected after second completed child return')
        return result
    child.run=fail_second
    try:
        out['failure_after_completed_substream']=expect_failure(owner,case,message='injected after second')
    finally:
        child.run=original_run
    def corrupt_header(*args,**kwargs):
        result=original_run(*args,**kwargs)
        result.step(1);result.step(1)
        digit=result.read();need(digit in (0,1),'tamper a header bit')
        result.write(1-digit);result.rewind()
        return result
    child.run=corrupt_header
    try:
        out['changed_return_header']=expect_failure(owner,case)
    finally:
        child.run=original_run
    original_unit=physical_router.unit
    def wrong_chunk(*args):
        lo,size,half,role=original_unit(*args)
        with owned(Count(size)) as (parity,):
            odd=parity.divide_small(2)
        if role and odd:
            half.increment()
        return lo,size,half,role
    physical_router.unit=wrong_chunk
    try:
        out['wrong_nondyadic_chunk']=expect_failure(owner,case)
    finally:
        physical_router.unit=original_unit
    return out


def run():
    static=check_static()
    with physical_runtime():
        from records import Tape
        from control_service import ControlService
        from physical_router import UnionRouter
        tapes=[];original=Tape.__init__
        def tracked(tape):
            original(tape);tapes.append(tape)
        Tape.__init__=tracked
        child=ControlService();owner=UnionRouter(child)
        try:
            rows=[run_case(owner,child,tapes,case,pending_control=(i==0)) for i,case in enumerate(CASES)]
            need(any(r['controls']['wrong_axis_order_differs'] for r in rows),
                 'nonlinear oracle distinguishes swapped axis order')
            need(any(r['controls']['stale_values_differ'] for r in rows),
                 'nonlinear oracle distinguishes stale inputs')
            rejects=failures(owner,child)
            after=run_case(owner,child,tapes,CASES[1])
            return dict(marker='PASS_LITERAL_WHOLE_UNION_TRANSPORT',static=static,cases=rows,
                        rejection_controls=rejects,recovery_after_rejections=after,
                        fixed_owned_roles=len(owner.forbidden()),all_size_proof='PROOF.md',
                        source_scope='synthetic nonlinear service controls; numerical source join is separate',
                        no_new_kappa=True)
        finally:
            if owner.pending:
                owner.consume()
            Tape.__init__=original


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-result',action='store_true')
    parser.add_argument('--emit',action='store_true');args=parser.parse_args()
    result=stable(run());target=PACKAGE/'TRANSPORT-RESULT.json'
    if args.write_result:
        target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    elif not args.emit:
        need(result==json.loads(target.read_text()),'exact stable transport receipt')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
