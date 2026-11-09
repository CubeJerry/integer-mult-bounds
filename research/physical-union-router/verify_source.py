"""Cold exact-source/page construction and complete physical union replay."""
from pathlib import Path
import argparse
import json
import sys
PACKAGE=Path(__file__).resolve().parent
sys.path[:0]=[str(PACKAGE),str(PACKAGE/'retained/inverse_window')]
from runtime_sources import authenticate,physical_runtime
from fixture_tools import need
from verify_transport import stable
import reference_source,source_window


def run(case):
    raw=authenticate()
    reference=reference_source.make_reference(raw,(61,3,2,1,3,32))
    if case=='admitted4':
        window=source_window.make_window(reference,length=4,interior_blocks=((1,2),),cap=2)
    elif case=='sparse8':
        window=source_window.make_window(reference,length=8,interior_blocks=((1,2,3,4),),cap=4,block=2)
    else:
        raise ValueError('known source fixture')
    print('EXACT_SOURCE_READY '+case,file=sys.stderr,flush=True)
    with physical_runtime():
        from records import Tape
        import source_fixture
        tapes=[];original=Tape.__init__
        def tracked(tape):
            original(tape);tapes.append(tape)
        Tape.__init__=tracked
        try:
            result=source_fixture.run(raw,window,reference,tapes)
            result['fixture_case']=case
            result['partition_scope']='explicit same-Reference admitted partition; retained production carve is a separate source test'
            return stable(result)
        finally:
            Tape.__init__=original
            reference_source.clear_reference(reference)


def main():
    sys.set_int_max_str_digits(0)
    parser=argparse.ArgumentParser();parser.add_argument('--case',choices=('admitted4','sparse8'),default='sparse8')
    parser.add_argument('--write-result',action='store_true');parser.add_argument('--emit',action='store_true')
    args=parser.parse_args();result=run(args.case)
    target=PACKAGE/('SOURCE-'+args.case.upper()+'-RESULT.json')
    if args.write_result:
        target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    elif not args.emit:
        need(result==json.loads(target.read_text()),'exact stable cold source/whole-router receipt')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
