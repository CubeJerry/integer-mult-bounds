"""Independent asymmetric original-address/source binding review.

Actual retained Layout, AdmittedPartition and encoded PreparedRoutes are used.
No physical Core is executed. Expected axes, source starts, and all addresses
are interpreted independently in the original MSF halo convention.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
import argparse
from hashlib import sha256
import importlib.machinery
import json
from pathlib import Path
import sys
from types import ModuleType


def need(ok,message):
    if not ok:
        raise ValueError(message)


def load(name,path):
    module=ModuleType(name);module.__file__=str(path);sys.modules[name]=module
    exec(compile(path.read_bytes(),str(path),'exec'),module.__dict__)
    return module


def permute(value,mapping):
    # Independent direct output-bit definition, not the producer's destructive
    # mask/update implementation. A source bit occurs exactly once.
    inverse={new:old for old,new in mapping.items()}
    width=max(value.bit_length(),max(inverse,default=-1)+1)
    return sum(((value//2**inverse.get(bit,bit))%2)*2**bit for bit in range(width))


def read_bits(tape,blank):
    result=[]
    while tape.read()!=blank:
        digit=tape.read();need(digit in (0,1),'literal binary metadata')
        result.append(digit);tape.step(1)
    tape.rewind()
    return tuple(result)


def unpack_route(tape,width,blank):
    body=read_bits(tape,blank)
    need(len(body)%(2*width)==0,'complete encoded route pairs')
    def unsigned(word):
        return sum(bit*2**i for i,bit in enumerate(word))
    pairs=[(unsigned(body[i:i+width]),unsigned(body[i+width:i+2*width]))
           for i in range(0,len(body),2*width)]
    need(len(dict(pairs))==len(pairs),'unique encoded support source positions')
    return dict(pairs)


def run(package):
    here=Path(__file__).resolve().parent
    importlib.machinery.SourceFileLoader.get_code=lambda self,name:compile(
        self.get_data(self.get_filename(name)),self.get_filename(name),'exec')
    binding=load('halo_core_sources',package/'halo_core_sources.py')
    source=binding.core_sources()
    halo=binding.halo_sources()
    geometry=load('_review_source_geometry',package/'source_geometry.py')
    geometry_hash=sha256((package/'source_geometry.py').read_bytes()).hexdigest()
    with source.numerical() as runtime:
        from core_layout import Layout
        from admitted_context import AdmittedPartition
        specifications=((15,1,2,1,3,64),(127,1,4,1,3,192))
        references=tuple(runtime.reference.Reference(runtime.raw,*spec) for spec in specifications)
        for reference in references:reference.require_narrow_gap()
        side,periods,spectators=8,(16,128),2
        bill=halo.M.Bill()
        shifts=[]
        for reference in references:
            u=0
            while 2**u*reference.narrow_gap<1:u+=1
            shifts.append(u)
        shifts[1]+=1  # Deliberately unequal, still funded normalizers.
        plans=tuple(halo.M.Plan(n,4,28,1,u,ref.narrow_gap,2)
                    for n,u,ref in zip(periods,shifts,references))
        tables=tuple(halo.M.prepare_table(plan,
            lambda i,j,ref=ref:halo.S.source_entry(ref,i,j),ref.description_hash,bill)[0]
            for plan,ref in zip(plans,references))
        archive=halo.T.pack_tables(tables,bill)
        shape=halo.Shape(3,(1,4),1,1,0,2*plans[0].data_width)
        layout=geometry.layout_for(shape)
        need(layout.lengths==(7,4,1) and layout.selected==(0,1),
             'producer reverses original halo axis widths once')
        contexts={};mismatches=0
        need(layout.n==12 and layout.labels==64 and side>4,'complete admitted geometry')
        mapping=layout.gather
        need(set(mapping)==set(mapping.values()),'complete support permutation')
        for address in range(spectators*periods[0]*periods[1]):
            spectator=address//(periods[0]*periods[1])
            x0=address//periods[1]%periods[0];x1=address%periods[1]
            packed=permute(address,mapping)
            local=(x0%side)*side+x1%side
            need(packed%(side*side)==local,'actual packed local axes retain original MSF order')
            need(permute(packed,layout.inverse)==address,'complete independent inverse route')
            label=packed//(side*side)
            expected=(spectator,x0-x0%side,x1-x1%side)
            need(label not in contexts or contexts[label]==expected,
                 'one original spectator and coarse box for each actual label')
            contexts[label]=expected
            need(layout.coordinates(label)==(expected[2],expected[1],expected[0]),
                 'original base retains low axes and spectator')
            need(layout.core_starts(label)==(expected[2],expected[1]),
                 'actual source starts in low-axis order')
            naive=(label//32,(label//16%2)*side,(label%16)*side)
            mismatches+=int(naive!=expected)
        need(len(contexts)==layout.labels and mismatches>0,'noncanonical coarse-label control')
        cache={}
        def partition(axis,first,reference=None):
            reference=references[axis] if reference is None else reference
            key=axis,first,reference.description_hash
            if key not in cache:
                cache[key]=AdmittedPartition(runtime,reference,'narrow',first,side,1,((7,),))
            return cache[key]
        produced_layout,produced_family=geometry.source_family(runtime,references,shape,archive,
            (1,1),interiors=(((7,),),((7,),)))
        need(produced_layout.record()==layout.record(),'producer uses the checked original layout')
        family=tuple(tuple(row) for row in produced_family)
        def check_source_binding(rows):
            for label,row in enumerate(rows):
                need(len(row)==2,'complete original source axes')
                for axis,p in enumerate(row):
                    need(p.reference.description_hash==references[axis].description_hash,
                         'same intended original halo Reference')
                    need(p.first==contexts[label][axis+1] and p.size==side,
                         'same actual original source window')
                    p.validate()
        check_source_binding(family)
        translated_differences=0;checked_entries=0
        for axis in range(2):
            for first in range(0,periods[axis],side):
                p=next(row[axis] for row in family if row[axis].first==first)
                for i in range(side):
                    for j in range(side):
                        actual=p.reference.entry('narrow',p.first+i,p.first+j).value
                        expected=references[axis].entry('narrow',first+i,first+j).value
                        need(actual==expected,'complete source window uses original coordinates')
                        checked_entries+=1
                        translated_differences+=int(actual!=references[axis].entry('narrow',i,j).value)
        need(translated_differences>0,'regenerating every source at local origin is detected')
        wrong_axis=tuple(tuple(reversed(row)) for row in family)
        wrong_label=tuple((partition(0,(label//16%2)*side),
                           partition(1,(label%16)*side)) for label in range(layout.labels))
        foreign=runtime.reference.Reference(runtime.raw,15,1,4,1,3,192)
        wrong_reference=tuple((partition(0,contexts[label][1],foreign),row[1])
                              for label,row in enumerate(family))
        for name,wrong in (('wrong-axis-order',wrong_axis),('naive-coarse-label',wrong_label),
                           ('same-period-foreign-reference',wrong_reference)):
            try:check_source_binding(wrong)
            except ValueError:pass
            else:raise ValueError('source binding observer accepted '+name)
        production_rejections=[]
        def rejects(name,operation):
            try:operation()
            except ValueError as error:
                production_rejections.append(dict(name=name,reason=str(error)))
            else:raise ValueError('producer metadata admission accepted '+name)
        rejects('producer-foreign-same-period-reference',lambda:geometry.source_family(
            runtime,(foreign,references[1]),shape,archive,(1,1),interiors=(((7,),),((7,),))))
        rejects('producer-reversed-source-list',lambda:geometry.source_family(
            runtime,tuple(reversed(references)),shape,archive,(1,1),interiors=(((7,),),((7,),))))
        narrow_plans=tuple(halo.M.Plan(n,1,28,1,u,ref.narrow_gap,2)
                          for n,u,ref in zip(periods,shifts,references))
        narrow_tables=tuple(halo.M.prepare_table(plan,
            lambda i,j,ref=ref:halo.S.source_entry(ref,i,j),ref.description_hash,bill)[0]
            for plan,ref in zip(narrow_plans,references))
        narrow_archive=halo.T.pack_tables(narrow_tables,bill)
        rejects('producer-uncertified-narrow-band-with-correct-source-id',
                lambda:geometry.source_family(runtime,references,shape,narrow_archive,
                    (1,1),interiors=(((7,),),((7,),))))
        narrow_archive.tape.readonly=False;narrow_archive.tape.clear()
        for table in narrow_tables:table.tape.readonly=False;table.tape.clear()
        allocation=dict(P=64,width=80,R0=64,target=4)
        expected_bridge=(31,80,28,64,64+sum(shifts)-28)
        need(tuple(geometry.bridge_values(plans,allocation))==expected_bridge,
             'producer exact grid and product normalizer values')
        need(sum(shifts)>max(shifts),'multi-axis sum differs from maximum')
        radius=geometry.admit_radii(layout.n,1,2,allocation,plans)
        need(radius['records']==4096 and radius['normalizer']==2**sum(shifts),
             'producer includes all contexts, spectators and normalizers')
        rejects('producer-missing-whole-field-radius',lambda:geometry.admit_radii(
            layout.n,1,2,dict(allocation,R0=32),plans))
        rejects('producer-missing-output-headroom',lambda:geometry.admit_radii(
            layout.n,2,2,dict(allocation,R0=128),plans))
        rejects('producer-insufficient-lift-carrier',lambda:geometry.bridge_values(
            plans,dict(allocation,width=66)))
        rejects('producer-coarser-Core-grid',lambda:geometry.bridge_values(
            plans,dict(allocation,P=27)))
    # Actual physical descriptor generation only, not a Core/data computation.
    with source.physical():
        from original_layout import PreparedRoutes
        from words import BLANK, RIGHT
        routes=PreparedRoutes(layout,family,11)
        position_width=max(1,(layout.n-1).bit_length())
        forward=unpack_route(routes.forward,position_width,BLANK)
        inverse=unpack_route(routes.inverse,position_width,BLANK)
        need(forward==mapping and inverse==layout.inverse,'actual encoded complete route descriptors')
        for address in range(spectators*periods[0]*periods[1]):
            packed=permute(address,forward)
            need(permute(packed,inverse)==address,'encoded-route complete original round trip')
        values=[]
        for count in routes.parameters:
            raw=read_bits(count.tape,RIGHT)
            values.append(sum(bit*2**i for i,bit in enumerate(raw)))
        need(values==[12,13,len(mapping),position_width],'exact route parameter words')
        routes.close()
        bridge_counts=geometry.prepare_bridge_counts(plans,allocation)
        encoded_bridge=[]
        for count in bridge_counts:
            raw=read_bits(count.tape,RIGHT)
            encoded_bridge.append(sum(bit*2**i for i,bit in enumerate(raw)))
        need(tuple(encoded_bridge)==expected_bridge,'actual encoded bridge Count ports')
        for count in bridge_counts:count.close()
        rejected=[]
        for name,wrong in (('wrong-axis-order',wrong_axis),('naive-coarse-label',wrong_label)):
            try:PreparedRoutes(layout,wrong,11)
            except ValueError as error:rejected.append(dict(name=name,reason=str(error)))
            else:raise ValueError('actual route binder accepted '+name)
        # The retained route constructor knows geometry, not the halo archive's
        # expected Reference ID. This foreign source is structurally admissible;
        # the common-source predicate above must remain an explicit admission.
        foreign_routes=PreparedRoutes(layout,wrong_reference,11)
        foreign_routes.close()
    archive.tape.readonly=False;archive.tape.clear()
    for table in tables:table.tape.readonly=False;table.tape.clear()
    need(sha256((package/'source_geometry.py').read_bytes()).hexdigest()==geometry_hash,
         'source producer stable throughout review')
    return dict(status='INDEPENDENT_ASYMMETRIC_AXIS_BINDING_PASS',
        scope='Actual retained source partitions and encoded routes plus exhaustive address semantics; no physical Core or halo execution.',
        original_msf_periods=periods,spectator_count=spectators,side=side,boundary=1,halo=0,
        native_low_axis_widths=layout.lengths,original_addresses=4096,contexts=len(contexts),
        distinct_intended_source_windows=sum(n//side for n in periods),
        original_window_entries=checked_entries,translated_local_origin_mismatches=translated_differences,
        naive_coarse_label_address_mismatches=mismatches,
        actual_route_rejections=rejected,expected_reference_identity_control=True,
        same_period_foreign_reference_is_structurally_accepted=True,
        actual_new_source_producer_rejects_foreign_reference=True,
        producer_rejections=production_rejections,encoded_bridge_counts=encoded_bridge,
        normalizer_shifts=shifts,whole_field_radius=radius,
        reference_sha256=[r.description_hash for r in references],
        route_support=sorted(mapping.items()),encoded_parameters=values,
        source_sha256={name:sha256((package/'retained/core'/name).read_bytes()).hexdigest()
                       for name in ('original_layout.py','admitted_context.py','retained/cohort/core_layout.py')},
        source_geometry_sha256=geometry_hash,
        reviewer_sha256=sha256((here/'axis_binding_review.py').read_bytes()).hexdigest())


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--package',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    args.output.write_text(json.dumps(run(args.package.resolve()),sort_keys=True,indent=2)+'\n')
