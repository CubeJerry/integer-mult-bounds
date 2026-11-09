"""Encoded e=Nf+r geometry, selected-plane descriptors and source events."""
from pathlib import Path
import importlib.util
import sys


def load(name):
    path=Path(__file__).resolve().parent/(name+".py")
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    exec(compile(path.read_bytes(),str(path),"exec"),module.__dict__)
    return module


r=load("row_programs")
f=load("fixture_tools")


def reject(call):
    try:call()
    except ValueError:return
    raise ValueError("negative geometry control accepted")


def execute_header(program,parent):
    ports=f.ports(r.FIRST_ROLE,shifted=True)
    raw=f.encode_header(r.SCHEMA,parent)
    ports[r.HEADER].load(raw)
    steps=r.run(program,ports)
    child=f.decode_header(r.SCHEMA,ports[r.CHILD_HEADER].word())
    r.need(ports[r.HEADER].word()==raw,"parent complete encoded descriptor preserved")
    r.need(all(t.head==t.marker+1 for t in ports),"descriptor heads")
    r.need(all(not t.word() for i,t in enumerate(ports)
               if i not in (r.HEADER,r.CHILD_HEADER)),"descriptor scratch erased")
    return child,steps


def extent_checks():
    program=r.compile_row_extent()
    count=0
    for a in range(13):
        for b in range(1,18):
            ports=f.ports(r.FIRST_ROLE)
            ports[16].load(f.binary(a));ports[17].load(f.binary(b))
            steps=r.run(program,ports)
            r.need(ports[r.ROWBITS].word()==f.binary(b*(1<<a)),"literal physical row length")
            r.need(steps<=512*(b*(1<<a)+a+len(f.binary(b))+1),"row extent complete preparation invoice")
            count+=1
    return count


def geometry_checks():
    count=0
    maximum=0
    for n in (2,3,5,7):
        program=r.compile_prepare(2,rank=n)
        for requested in (n+1,n*n+2,7*n+3,10**20+17):
            for k,rho in ((1,0),(2,1),(7,3)):
                parent=f.values(r.SCHEMA,rows=12,stock=12,row_bits=8)
                parent.update(f=requested,selected_axes=n*requested+1,
                              entry_start=2,active_start=2+k,K=k,rho=rho,cutoff=n,
                              remainder=1)
                child,steps=execute_header(program,parent)
                expected=dict(parent,rows=6,stock=6,selected_axes=requested,
                              f=requested//n,remainder=requested%n,
                              entry_start=parent['active_start'],
                              active_start=parent['active_start']+(requested%n)*k)
                r.need(child==expected,"actual rank-one ordinary child geometry")
                r.need(child['active_start']+n*child['f']*k
                       ==child['entry_start']+child['selected_axes']*k,
                       "complete remainder plus canonical child span")
                maximum=max(maximum,steps);count+=1
    return count,maximum


def root_checks():
    count=0
    for n in (2,3,5):
        program=r.compile_prepare(2,rank=n,root=True)
        for e in (n+1,n*n+2):
            for k,rho in ((1,0),(2,1)):
                a=3+e*k
                parent=f.values(r.SCHEMA,rows=24,stock=12,row_bits=1)
                parent.update(selected_axes=e,entry_start=2,K=k,rho=rho,
                              within_bits=a,record_bits=12,back_start=2+e*k,
                              f=0,remainder=0,active_start=0,cutoff=n)
                child,_=execute_header(program,parent)
                expected=dict(parent,rows=12,stock=6,row_bits=12*(1<<a),
                              f=e//n,remainder=e%n,active_start=2+(e%n)*k)
                r.need(child==expected,"root consumes rows but keeps root active width")
                r.need(child['active_start']+n*child['f']*k==parent['back_start'],
                       "root complete front/active/back separation")
                count+=1
    return count


def leaf_checks():
    count=0
    for n in (2,3,5,7):
        program=r.compile_leaf(n)
        for cutoff in (n,n+3,2*n):
            for width in range(1,3*n+6):
                parent=f.values(r.SCHEMA)
                parent.update(f=width,cutoff=cutoff)
                ports=f.ports(r.FIRST_ROLE)
                raw=f.encode_header(r.SCHEMA,parent);ports[r.HEADER].load(raw)
                leaf,_=r.run_choice(program,ports)
                r.need(leaf==(width<=cutoff),"source boundary f<=floor(s)")
                r.need(ports[r.HEADER].word()==raw,"leaf predicate preserves metadata")
                r.need(all(not t.word() for i,t in enumerate(ports) if i!=r.HEADER),"leaf scratch closes")
                count+=1
    return count


def occurrence_checks():
    cases=0
    for n,requests in ((4,((2,0),(1,3))), (6,((0,3),(5,2))), (7,((5,1,3),(2,6,0)))):
        word,layouts=r.compile_occurrence(("owner-a","owner-b"),n,requests,n)
        native=[event for event in word if event[0]=="native"]
        r.need(native==[("native",("owner-a","owner-b"))],"one complete native word with actual fields")
        r.need(all(x['row_divisor']==1 and x['kind']==r.MATCHED for x in layouts),"matched fields preserve stock")
        for multiplicity in (1,2,3):
            k,rho,start=3,1,4
            live={field:[1<<i for i in range(start+n*multiplicity*k+4)] for field in ("owner-a","owner-b")}
            original={field:tuple(bits) for field,bits in live.items()}
            for event in word:
                if event[0]=="native":
                    for field,layout in zip(event[1],layouts):
                        for block in range(n):
                            for j in range(multiplicity):
                                at=start+(block*multiplicity+j)*k+rho
                                expected=start+(layout['order'][block]*multiplicity+j)*k+rho
                                r.need(live[field][at]==1<<expected,"actual complete selected-column chart")
                        selected={start+(a*multiplicity+j)*k+rho for a in range(n) for j in range(multiplicity)}
                        r.need(all(live[field][i]==original[field][i] for i in range(len(live[field])) if i not in selected),
                               "full controls and other bit planes stay spectators")
                    continue  # explicit identity native fixture; geometry only
                _,field,source,target=event
                for j in range(multiplicity):
                    a=start+(source*multiplicity+j)*k+rho
                    b=start+(target*multiplicity+j)*k+rho
                    # Independent linear-mask oracle for each selected-bit XOR.
                    live[field][b]^=live[field][a]
            for field in live:
                r.need(tuple(live[field])==original[field],"literal inverse whole-field return")
            cases+=1
    return cases


def controls():
    parent=f.values(r.SCHEMA,rows=12,stock=12)
    parent.update(f=8,selected_axes=25,entry_start=2,active_start=4,K=2,
                  cutoff=3,remainder=1)
    reject(lambda:execute_header(r.compile_prepare(2,rank=3),dict(parent,cutoff=2)))
    reject(lambda:execute_header(r.compile_prepare(2,rank=3),dict(parent,f=3)))
    reject(lambda:r.compile_prepare(2,kind=r.MATCHED))
    reject(lambda:r.compile_occurrence(("same","same"),3,((0,),(1,)),2))
    saved=r.Builder.derive_geometry
    try:
        r.Builder.derive_geometry=lambda self,rank,child:None
        mutant=r.compile_prepare(2,rank=3)
    finally:r.Builder.derive_geometry=saved
    changed,_=execute_header(mutant,parent)
    reject(lambda:r.need(changed['selected_axes']==parent['f'] and changed['f']==parent['f']//3,
                         "actual mutant leaves ordinary geometry unchanged"))
    return ["cutoff_below_final_rank","recursive_call_at_leaf_boundary",
            "matched_occurrence_consumes_rows","aliased_matched_fields",
            "deleted_actual_geometry_program"]


def check():
    extents=extent_checks();geometry,maximum=geometry_checks()
    roots=root_checks();leaves=leaf_checks();negative=controls();occurrences=occurrence_checks()
    return {"extent_cases":extents,"child_geometry_cases":geometry,
           "root_geometry_cases":roots,"leaf_boundary_cases":leaves,"occurrence_routes":occurrences,
           "maximum_child_steps":maximum,"rejections":negative}


def main():
    print(check())
    print("PASS_ENCODED_CHILD_GEOMETRY")


if __name__=="__main__":main()
