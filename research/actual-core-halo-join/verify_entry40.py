"""Entry40 fallback: complete actual Core/first-face halo execution.

Same full geometry and physical services as verify.py; a distinct admitted
Reference precision and output keep this execution separately identifiable.
Observers only record data.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import time
from unittest.mock import patch
from halo_core_sources import HERE, core_sources, halo_sources, need


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--preflight',action='store_true')
    parser.add_argument('--probe',action='store_true')
    parser.add_argument('--output',default=str(HERE/'PHYSICAL-ENTRY40-RESULT.json'))
    args=parser.parse_args();started=time.monotonic()
    source=core_sources();halo=halo_sources()
    q,normalizer,radius_in,radius_carrier=28,1,1,2
    with source.numerical() as runtime:
        from admitted_context import AdmittedPartition
        from prepared_join import build_numeric,prepare_banks
        from core_layout import Layout
        reference=runtime.reference.Reference(runtime.raw,15,1,2,1,3,40)
        reference.require_narrow_gap()
        layout=Layout((4,),(0,),3)
        family=[[AdmittedPartition(runtime,reference,'narrow',
            layout.core_starts(c)[0],8,1,((7,),))] for c in range(layout.labels)]
        programs,windows,actions,blocks,plan=build_numeric(runtime,family,
            target=2,initial_radius_bits=2,incoming=q)
        types=(runtime.global_compiler.Hadamard,runtime.global_compiler.Diagonal)
        need(plan['R0']**2>=16*radius_in**2,'whole-field input radius')
        need((1<<normalizer)*reference.narrow_gap>=1,'actual source normalization')
        halo_plan=halo.M.Plan(16,2,q,1,normalizer,reference.narrow_gap,radius_carrier)
        for r in range(16):
            for c in range(16):
                if min((r-c)%16,(c-r)%16)>halo_plan.halfwidth:
                    need(halo.S.source_entry(reference,r,c)==0,'complete actual cyclic source bandwidth')
        shape=halo.Shape(3,(1,),0,1,0,2*halo_plan.data_width)
        bill=halo.M.Bill()
        table,height=halo.M.prepare_table(halo_plan,
            lambda r,c:halo.S.source_entry(reference,r,c),reference.description_hash,bill)
        archive=halo.T.pack_tables((table,),bill)
        workspace=halo.T.TensorWorkspace.create(bill)
        source_inventory=halo.S.source_receipt(reference)
        source_Q=[[w.H for w in row] for row in windows]
        need(all(p.matrices[0][0][0].re==1 and p.matrices[0][0][0].im==0
                 for row in family for p in row),'labelled identity scalar interior fixture')
        preflight=dict(allocation=plan,blocks=blocks,
            source=dict(parameters=list(reference.spec.__dict__.values()),
                reference_sha256=reference.description_hash,
                origins=[row[0].first for row in family],interior=[7],layout=layout.record()),
            halo=dict(q=q,terms=1,halfwidth=2,boundary=1,halo=0,
                normalizer_shifts=[normalizer],input_radius=radius_in,
                carrier_radius=radius_carrier,gap=str(reference.narrow_gap),
                data_width=halo_plan.data_width,full_source_band_checked=True),
            complete_dense_events=2*programs[0].stages+programs[1].stages,
            setup_source_inventory=source_inventory)
        print('PREFLIGHT '+json.dumps(preflight,sort_keys=True),flush=True)
        if args.preflight:
            Path(args.output).write_text(json.dumps(dict(status='PASS_PREFLIGHT',**preflight),indent=2,sort_keys=True)+'\n')
            return
    with source.physical():
        from records import Tape
        from cardinal_counts import Count
        from physical_controls import PreparedFull
        from original_layout import PreparedRoutes
        from attachment import AttachedCore
        from fixture_tools import body,snapshot,integer
        from check_support import no_decode
        from session import erase_marker
        from words import BLANK
        from word_product import WordProduct
        import check_composed
        if args.probe:
            width=max(p.data_width for p in programs)
            first,second=(1<<(width-1))-13,(1<<(width-1))-33
            ports=[Count.literal(x) for x in (first,second,width)]
            product=WordProduct(leaf_bits=64);start=time.monotonic()
            with no_decode():returned=product.run(*ports)
            elapsed=time.monotonic()-start
            need(integer(body(returned))==first*second,'actual required-width product probe')
            returned.clear();erase_marker(returned)
            for port in ports:port.close()
            receipt=dict(status='PASS_ACTUAL_WORD_PRODUCT_COST_PROBE',**preflight,
                product_width=width,product_seconds=elapsed)
            Path(args.output).write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
            print('PROBE '+json.dumps(receipt,sort_keys=True),flush=True)
            return
        execute(args,started,source,halo,reference,layout,family,programs,windows,actions,
            blocks,plan,types,halo_plan,shape,bill,table,height,archive,workspace,
            source_Q,preflight,q,normalizer,radius_in,prepare_banks)


def execute(args,started,source,halo,reference,layout,family,programs,windows,actions,
            blocks,plan,types,halo_plan,shape,bill,table,height,archive,workspace,
            source_Q,preflight,q,normalizer,radius_in,prepare_banks):
    from records import Tape
    from cardinal_counts import Count
    from physical_controls import PreparedFull
    from original_layout import PreparedRoutes
    from attachment import AttachedCore
    from fixture_tools import body,snapshot,integer
    from check_support import no_decode
    from session import erase_marker
    from words import BLANK
    import check_composed
    all_tapes=[];original_init=Tape.__init__
    def tracked(self,*a,**kw):
        original_init(self,*a,**kw);all_tapes.append(self)
    def meter():
        return tuple(sum(getattr(t.meter,k) for t in all_tapes) for k in ('reads','writes','moves'))
    def difference(before):return tuple(a-b for a,b in zip(meter(),before))
    with patch.object(Tape,'__init__',tracked):
        prepared=[PreparedFull(program,Tape,Count,types) for program in programs]
        print('DENSE_CONTROLS_PREPARED',flush=True)
        ibank,fbank,keys=prepare_banks(family,windows,actions,blocks,plan)
        print('SPARSE_BANKS_PREPARED',flush=True)
        root,_=check_composed.fixture('standard',False)
        observations={};bridge_observations={};width=plan['width'];P=plan['P']
        def values(tape):
            raw=body(tape)
            need(len(raw)%(2*width)==0,'complete native complex field')
            return tuple((integer(raw[i:i+width]),integer(raw[i+width:i+2*width]))
                         for i in range(0,len(raw),2*width))
        def observe(stage,phase,tape):
            observations.setdefault(stage,{})[phase]=values(tape)
            print('STAGE '+stage+' '+phase+' '+str(time.monotonic()-started),flush=True)
        def observe_bridge(name,tape):
            bridge_observations[name]=(tape.inspect() if name in
                ('normalized_source','saved_original_halo') else values(tape))
        owner=AttachedCore(root,halo,observe=observe,observe_bridge=observe_bridge)
        routes=PreparedRoutes(layout,family,width)
        def normalized(tape):return bytes(tape.cells).rstrip(bytes((BLANK,)))
        initial_private={id(t):normalized(t) for t in owner.forbidden()}
        inputs=tuple(((((17*i+3)%19)-9)*(1<<(q-8))+(2*i+1),
                      (((11*i+5)%23)-11)*(1<<(q-8))+(2*i+3)) for i in range(16))
        need(max(sum(abs(x) for x in pair) for pair in inputs)<=(1<<q)*radius_in,
             'actual pointwise complex-l1 input radius')
        external=''.join(''.join(halo.sigmag(v,halo_plan.data_width) for v in pair)+'#' for pair in inputs)
        transport=halo.B.Program(external,'&@0#000;','01000','00001','00000')
        up=tuple(Count.literal(x) for x in (1,8,3,1,width,P))
        bridge_ports=tuple(Count.literal(x) for x in (halo_plan.data_width,width,q,P,P+normalizer-q))
        data=(prepared[0].code,prepared[1].code,ibank,fbank,keys)
        ports=(*data,routes.forward,routes.inverse,*(x.tape for x in
            (*prepared[0].parameters,*prepared[1].parameters,*up,*routes.parameters,*bridge_ports)))
        saved=snapshot(ports);native_setup_actions=meter();online_started=time.monotonic()
        online_roles=len(all_tapes);private_ids=tuple(map(id,owner.forbidden()))
        folded=source.load('attached_certified_floors',source.COHORT/'fixture_tools.py')
        bases={1,2,width,width+1,width+2,*(p.data_width for p in programs),
               *(p.data_width+1 for p in programs),*(p.data_width+2 for p in programs)}
        with folded.certified_floors(bases) as (_,calls,misses):
            with no_decode():
                codec=owner.run(transport,shape,archive,workspace,bill,routes,*data,
                    prepared[0].parameters,prepared[1].parameters,up,*bridge_ports)
            need(not misses,'declared finite metadata floor specialization')
        native_online_actions=difference(native_setup_actions)
        need(snapshot(ports)==saved,'all borrowed native source and metadata ports restored')
        need(transport.saved.inspect()==bridge_observations['saved_original_halo'],
             'original saved halo is immutable through complete Core and consumer')
        need(len(all_tapes)==online_roles and tuple(map(id,owner.forbidden()))==private_ids,
             'no new native online Tape or private role')
        expected_lift=tuple(tuple(x<<(P-q) for x in pair) for pair in inputs)
        need(bridge_observations['lifted_input']==expected_lift,'exact literal input lift')
        current=expected_lift
        for stage in ('D_Ainv_1','T1','D_A','T2','D_Ainv_2'):
            need(observations[stage]['input']==current,'actual current field at every stage')
            current=observations[stage]['output']
        need(current==bridge_observations['original_core_return'],'complete original Core return')
        norm_words=bridge_observations['normalized_source'].split('#')[:-1]
        normalized_values=tuple(halo.decode_word(word,halo_plan.data_width) for word in norm_words)
        drop=P+normalizer-q
        exact_return=tuple(tuple((-1 if x<0 else 1)*(abs(x)>>drop) for x in pair) for pair in current)
        need(normalized_values==exact_return,'literal toward-zero normalized return')
        final_words=transport.final.inspect().split('#')[:-1]
        final_values=tuple(halo.decode_word(word,halo_plan.data_width) for word in final_words)
        need(len(final_values)==16,'complete original-coordinate merged field')
        need(all(final_values[i]==normalized_values[i] for i in range(16) if 0<i%8<7),
             'all current Core kept rows survive actual halo merge')
        pre_erase=halo.literal_totals(transport);transport.erase_work()
        need(all(t.live_bits==0 and t.head==0 for t in workspace.roles),
             'halo workspace cleared after each rectangle')
        native_backing=sum(len(t.cells) for t in owner.forbidden())
        initial_marker=bytes((2,))
        need(all(t.head==1 and (normalized(t) in (b'',initial_private[id(t)])
            if initial_private[id(t)] in (b'',initial_marker)
            else normalized(t)==initial_private[id(t)]) for t in owner.forbidden()),
             'native dynamic backing erased and initial configurations preserved')
        receipt=dict(status='PASS_ACTUAL_COMPLETE_CORE_HALO_JOIN',**preflight,
            scope='Full actual L8/N16/K2/g1 narrow Core and J1 first-face halo; scalar interior A identity, complete Q coupled.',
            dense_programs=[p.record() for p in programs],
            source_Q=[[[[str(x) for x in row] for row in matrix] for matrix in context] for context in source_Q],
            initial=inputs,returned=final_values,core_normalized=normalized_values,
            observations=observations,bridge_observations=bridge_observations,
            codec=codec.receipt(),native_setup_actions=native_setup_actions,
            native_online_actions=native_online_actions,native_owned_retained_cells=native_backing,
            native_all_constructed_cells=sum(len(t.cells) for t in all_tapes),
            native_tape_roles=len(all_tapes),online_new_native_tapes=len(all_tapes)-online_roles,
            fixed_native_private_inventory=len(private_ids),transport=halo.literal_totals(transport),
            transport_before_erase=pre_erase,consumer_bill=bill.record(),consumer_source_height=height,
            consumer_retained_binary_cells=sum(t.extent for t in (*workspace.roles,archive.tape,table.tape)),
            complete_sparse_calls=[owner.core.core.inverse.child.calls,owner.core.core.forward.child.calls],
            metadata_bases=sorted(bases),metadata_calls=len(calls),
            saved_original_unchanged=True,kept_current_core_unchanged=True,
            seconds=time.monotonic()-started,online_seconds=time.monotonic()-online_started,no_new_kappa=True)
        Path(args.output).write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
        print('PASS '+args.output,flush=True)
        archive.tape.readonly=False;archive.tape.clear()
        table.tape.readonly=False;table.tape.clear()
        routes.close()
        for prepared_source in prepared:prepared_source.close()
        for value in (*up,*bridge_ports):value.close()
        for tape in (ibank,fbank,keys):tape.clear();erase_marker(tape)


if __name__=='__main__':main()
