"""Bounded actual caller joins, counterfactual owner relations, meter audit."""
from pathlib import Path
import json,sys,types
from hashlib import sha256
HERE=Path(__file__).resolve().parent
def load(path,name):
    m=types.ModuleType(name);m.__file__=str(path);sys.modules[name]=m
    exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
def need(x,s):
    if not x:raise ValueError(s)
def active(cells,right):
    at=cells.index(right,1);return bytes(cells[:at+1])

def observer(m,old_div,records):
    pending={}
    def inspect(stage,binder,a,n,d,outputs):
        if stage=='before':
            before={slot:(bytes(a.words[slot].cells),a.words[slot].head,id(a.words[slot].cells),
                          id(a.words[slot].port),a.words[slot].port.head) for slot in a.live}
            clone=object.__new__(m.w.Arena)
            clone.capacity,clone.bits,clone.meter=64,a.bits,m.w.Meter()
            clone.words,clone.available,clone.live=[],list(a.available),set(a.live)
            for source in (*a.words,a.template):
                target=object.__new__(m.w.Word);target.arena=clone;target.slot=source.slot
                target.cells=bytearray(source.cells);target.head=source.head
                if source is a.template:clone.template=target
                else:clone.words.append(target)
            oq,orr=old_div(m.w.Unsigned(clone),clone.words[n.slot],clone.words[d.slot])
            pending.update(before=before,clone=clone,old_outputs=(oq,orr),
                           meter=sum(a.meter.record()[k] for k in('reads','writes','moves')),
                           port_meters=sum(sum(word.port.meter.record()[k] for k in('reads','writes','moves')) for word in a.words),
                           program_numeric=binder.program.numeric_actions,
                           fingerprint=[n.slot,d.slot,*a.available[-5:]],
                           previous_heads=[word.port.head for word in a.words])
        else:
            q,r=outputs;oq,orr=pending['old_outputs'];clone=pending['clone'];before=pending['before']
            bijection={slot:slot for slot in before};bijection.update({oq.slot:q.slot,orr.slot:r.slot})
            bijection.update(zip(clone.available,a.available))
            need(len(bijection)==len(set(bijection.values()))==64,'post-divmod free-stack/live bijection')
            for oldslot,newslot in bijection.items():
                ow,nw=clone.words[oldslot],a.words[newslot]
                need((oldslot in clone.live)==(newslot in a.live),'live relation')
                need(ow.head==nw.head==1,'related returned heads')
                if oldslot in clone.live:need(active(ow.cells,m.w.RIGHT)==active(nw.cells,m.w.RIGHT),'related live values')
                else:need(all(x==m.w.BLANK for x in nw.cells[1:]),'actual free entire retained history blank')
            for slot,snapshot in before.items():
                word=a.words[slot]
                need((bytes(word.cells),word.head,id(word.cells),id(word.port),word.port.head)==snapshot,
                     'incoming bytes/backing/object/head identities preserved')
            new_numeric=binder.program.numeric_actions-pending['program_numeric']
            arena_delta=sum(a.meter.record()[k] for k in('reads','writes','moves'))-pending['meter']
            port_delta=sum(sum(word.port.meter.record()[k] for k in('reads','writes','moves')) for word in a.words)-pending['port_meters']
            need(arena_delta==new_numeric and port_delta==0,'HostedWord actions charged exactly once to arena only')
            records.append({'entry_fingerprint':pending['fingerprint'],'new_outputs':[q.slot,r.slot],
                            'old_outputs':[oq.slot,orr.slot],'free_stack_bijection':sorted(bijection.items()),
                            'live_input_count':len(before),'numeric_actions':new_numeric,
                            'arena_action_delta':arena_delta,'backing_port_action_delta':port_delta})
    return inspect

def main():
    prior=load(HERE/'inputs/headers/verify.py','B10_headers_verify')
    _,previous,base,m,headers,header_hw,caller,code,labels,meta,_=prior.modules()
    headjoin=load(HERE/'inputs/headers/join.py','B10_header_join')
    divider=load(HERE/'divider.py','B10_divider');hardware=load(HERE/'hardware.py','B10_hardware')
    binding=load(HERE/'binding.py','B10_binding');dc,dl,dm=divider.compile_divider()
    caller_raw=(HERE/'inputs/headers/inputs/keypass/inputs/route/inputs/point/caller.py').read_bytes()
    need(sha256(caller_raw).hexdigest()==headjoin.CALLER_SHA,'exact original current caller')
    baseline_leg=caller.run_leg;old_div=m.w.Unsigned.divmod;cases=[];relations=[]
    for left,value in((2,0),(2,2),(5,1),(5,5),(7,6),(8,7)):
        moduli=(17,19,left,3);values=(1,2,value,1)
        m.fixture=dict(m.fixture,widths=[5,5,max(left.bit_length(),value.bit_length()),2],moduli=list(moduli),initial=list(values))
        old_source,old_payload,fields=base.initial_fixture(m)
        baseline_point=header_hw.Program(code,labels,meta)
        baseline_native=baseline_point.native_actions
        baseline_forward_receipt,_=baseline_leg(m,base,baseline_point,old_source,old_payload,False)
        baseline_forward_receipt['remaining_source_symbol_actions']=baseline_forward_receipt['encoded_source_symbol_actions']-(baseline_point.native_actions-baseline_native)
        baseline_forward=(bytes(old_source.cells),dict(old_payload.cells))
        baseline_native=baseline_point.native_actions
        baseline_inverse_receipt,_=baseline_leg(m,base,baseline_point,old_source,old_payload,True)
        baseline_inverse_receipt['remaining_source_symbol_actions']=baseline_inverse_receipt['encoded_source_symbol_actions']-(baseline_point.native_actions-baseline_native)
        source,payload,fields=base.initial_fixture(m)
        original=(bytes(source.cells),source.head,dict(payload.cells),payload.head)
        point=header_hw.Program(code,labels,meta);legs=[];owned=[]
        for reverse in(False,True):
            machine=hardware.Program(dc,dl,dm)
            binder=binding.Binding(machine,hardware,observer(m,old_div,relations))
            changed,_=binding.join(headjoin,caller,binder,caller_raw)
            before_native=point.native_actions
            receipt,stock=changed.run_leg(m,base,point,source,payload,reverse)
            header_native=point.native_actions-before_native
            need(binder.replacements==2,'two actual one-left/one-right current leaf boundaries')
            need(binder.granted_extra_cells==28,'four explicit backed grant enlargements')
            need(machine.numeric_actions==sum(x['numeric_actions'] for x in binder.calls),'setter/acquire no numeric action')
            receipt['remaining_source_symbol_actions']=receipt.pop('encoded_source_symbol_actions')-header_native-machine.numeric_actions
            receipt['remaining_outer_adapter_symbol_actions']=receipt.pop('outer_adapter_symbol_actions')-machine.selector_actions
            need(receipt['remaining_source_symbol_actions']>=0 and receipt['remaining_outer_adapter_symbol_actions']==14,'exact disjoint overlap subtraction')
            receipt.update(literal_divider_instructions=machine.total,literal_numerical_actions=machine.numeric_actions,
                           literal_selector_actions=machine.selector_actions,boundary_query_actions=binder.boundary_actions,
                           finite_binding_invoice=binder.finite_control_invoice,explicit_grant_extra_cells=binder.granted_extra_cells,
                           finite_source_raw_calls=binder.raw_calls,finite_source_invocations=binder.invocations,
                           actual_division_calls=binder.calls)
            need(binder.finite_control_invoice==256+32*binder.invocations+16*binder.raw_calls+16384*binder.replacements,
                 'complete declared finite-source control tariff')
            legs.append(receipt);owned.extend(stock[0])
            if not reverse:need((bytes(source.cells),dict(payload.cells))==baseline_forward,'complete exact original forward source/payload')
        need((bytes(source.cells),source.head,dict(payload.cells),payload.head)==original,'complete actual source/payload/key roundtrip')
        need(len(owned)==len({id(x) for x in owned})==200,'same200 physical source/adapter histories')
        cases.append({'moduli':moduli,'values':values,'directions':legs,
                      'baseline_B9_directions':[baseline_forward_receipt,baseline_inverse_receipt],
                      'retained_symbol_cells':sum(map(len,owned)),
                      'source_payload_roundtrip':True})
    fingerprints=sorted({tuple(x['entry_fingerprint']) for x in relations})
    need(len(fingerprints)>=3,'several source allocator states')
    print(json.dumps({'status':'PASS','graph':divider.digest(dc),'actual_cases':cases,
                      'counterfactual_relations':relations,'distinct_fingerprints':fingerprints},indent=2,sort_keys=True))

if __name__=='__main__':main()
