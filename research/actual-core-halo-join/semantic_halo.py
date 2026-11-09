"""J2 semantic Core with two coupled A2 blocks, then actual bridge/halo.

The Core is explicitly semantic. The literal format bridge and inherited
halo consumer execute on their real tape hardware. Prepared for @CubeJerry
with substantial OpenAI assistance. Apache-2.0.
"""
import argparse
import json
from pathlib import Path
import time
from halo_core_sources import HERE,CORE,core_sources,halo_sources,load,need


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default=str(HERE/'SEMANTIC-RESULT.json'))
    args=parser.parse_args();started=time.monotonic();core=core_sources();halo=halo_sources()
    q,u,Rin,Rhalo=56,1,1,2
    with core.numerical() as runtime:
        from admitted_context import AdmittedPartition
        from prepared_join import build_numeric
        from core_layout import Layout
        ref=runtime.reference.Reference(runtime.raw,31,1,4,1,3,192)
        ref.require_narrow_gap();layout=Layout((5,),(0,),4)
        family=[[AdmittedPartition(runtime,ref,'narrow',layout.core_starts(c)[0],16,2,((1,2),))]
                for c in range(layout.labels)]
        programs,windows,actions,blocks,plan=build_numeric(runtime,family,target=4,
            initial_radius_bits=3,incoming=q)
        P=plan['P'];width=plan['width']
        need(all(p.matrices[0][0][1].re!=0 and p.matrices[0][1][0].re!=0
                 for row in family for p in row),'two nonidentity coupled A2 interiors')
        hp=halo.M.Plan(32,2,q,2,u,ref.narrow_gap,Rhalo)
        for r in range(32):
            for c in range(32):
                if min((r-c)%32,(c-r)%32)>hp.halfwidth:
                    need(halo.S.source_entry(ref,r,c)==0,'complete actual cyclic source bandwidth')
        bill=halo.M.Bill()
        table,height=halo.M.prepare_table(hp,lambda r,c:halo.S.source_entry(ref,r,c),ref.description_hash,bill)
        archive=halo.T.pack_tables((table,),bill);workspace=halo.T.TensorWorkspace.create(bill)
        shape=halo.Shape(4,(1,),0,3,2,2*hp.data_width)
        inputs=tuple(((((17*i+3)%19)-9)*(1<<(q-8))+(2*i+1),
                      (((11*i+5)%23)-11)*(1<<(q-8))+(2*i+3)) for i in range(32))
        need(max(sum(abs(x) for x in pair) for pair in inputs)<=(1<<q)*Rin,'pointwise input radius')
        incoming=tuple(tuple(x<<(P-q) for x in pair) for pair in inputs)
        interpreter=load('inherited_complete_semantics',CORE/'check_source_join.py')
        source=load('semantic_attached_inverse_source',core.INVERSE/'source_window.py')
        forward=load('semantic_attached_forward_source',core.FORWARD/'pages.py')
        current=incoming;observations={};counts=[];sparse_calls=[]
        for stage in ('D_Ainv_1','T1','D_A','T2','D_Ainv_2'):
            observations[stage]={'input':current}
            if stage in ('D_Ainv_1','D_A','D_Ainv_2'):
                current,count=interpreter.dense_replay(runtime,programs[1 if stage=='D_A' else 0],current)
                counts.append(count)
            else:
                current,count=interpreter.sparse_replay(windows,current,P,source,forward,stage=='T2')
                sparse_calls.append(count)
            observations[stage]['output']=current
        source_Q=[[w.H for w in row] for row in windows]
        from independent_numerics import check_complete_return
        exact=check_complete_return(source_Q,incoming,P,current,P,4)
        preflight=dict(allocation=plan,source=dict(parameters=list(ref.spec.__dict__.values()),
            reference_sha256=ref.description_hash,origins=[row[0].first for row in family],
            interior=[1,2],layout=layout.record()),
            halo=dict(q=q,terms=2,halfwidth=2,boundary=3,halo=2,normalizer_shifts=[u],
                input_radius=Rin,carrier_radius=Rhalo,gap=str(ref.narrow_gap),
                data_width=hp.data_width,full_source_band_checked=True),
            complete_dense_events=sum(c['events'] for c in counts),dense_counts=counts,
            sparse_line_semantic_calls=sparse_calls,dense_programs=[p.record() for p in programs],
            independent_finite_core_target=exact,nonidentity_A2_interiors=2)
    with core.physical():
        from format_bridge import FormatBridge
        from cardinal_counts import Count
        from physical_controls import emit_signed
        from records import Tape
        from fixture_tools import body,integer
        from session import erase_marker
        bridge=FormatBridge(halo.B)
        params=[Count.literal(x) for x in (hp.data_width,width,q,P,P+u-q)]
        external=''.join(''.join(halo.sigmag(v,hp.data_width) for v in pair)+'#' for pair in inputs)
        transport=halo.B.Program(external,'&@0#0000;','010000','000011','000010')
        transport.gather();transport.sort(transport.saved);saved=transport.saved.inspect()
        lifted=bridge.lift(transport.source,*params[:4]);raw=body(lifted)
        got=tuple((integer(raw[i:i+width]),integer(raw[i+width:i+2*width]))
                  for i in range(0,len(raw),2*width))
        need(got==incoming,'literal semantic-fixture incoming lift')
        # Explicit semantic Core boundary: these values are NOT a physical result.
        result=Tape()
        for pair in current:
            for value in pair:emit_signed(result,value,width)
        result.rewind()
        bridge.normalized_return(result,transport.source,params[0],params[1],params[4])
        normalized_source=transport.source.inspect()
        normalized=tuple(halo.decode_word(word,hp.data_width) for word in normalized_source.split('#')[:-1])
        result.clear();erase_marker(result);bridge.clear_input();transport.phase='core'
        codec=halo.Codec(transport,shape,archive,workspace,bill);codec.run()
        need(saved==transport.saved.inspect(),'saved original stream unchanged')
        transport.merge_returns()
        final=tuple(halo.decode_word(word,hp.data_width) for word in transport.final.inspect().split('#')[:-1])
        need(all(final[i]==normalized[i] for i in range(32) if 3<=i%16<13),
             'semantic Core kept values survive actual halo merge')
        transport.erase_work()
        receipt=dict(status='PASS_SEMANTIC_CORE_ACTUAL_J2_HALO',**preflight,
            physical_core_executed=False,semantic_core_executed=True,
            literal_bridge_and_actual_halo_executed=True,
            source_Q=[[[[str(x) for x in row] for row in matrix] for matrix in context] for context in source_Q],
            initial=inputs,returned=final,core_normalized=normalized,observations=observations,
            bridge_observations=dict(lifted_input=incoming,original_core_return=current,
                normalized_source=normalized_source,saved_original_halo=saved),
            codec=codec.receipt(),transport=halo.literal_totals(transport),consumer_bill=bill.record(),
            source_height=height,seconds=time.monotonic()-started,no_new_kappa=True)
        Path(args.output).write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
        print('PASS '+args.output)
        for value in params:value.close()
        archive.tape.readonly=False;archive.tape.clear();table.tape.readonly=False;table.tape.clear()


if __name__=='__main__':main()
