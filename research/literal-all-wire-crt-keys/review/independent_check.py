"""Independent sparse-cell review of the literal all-wire key pass.

No contributor verifier or execution engine is imported. Frozen compiler
tables are the executable object; expected rotations are direct integers.
Default is read-only; --write explicitly stores the computed result.
"""
from pathlib import Path
from hashlib import sha1,sha256
import argparse
import ast
import copy
import json
import sys
import types


def need(value,reason):
    if not value:
        raise ValueError(reason)


def load(path,name):
    module=types.ModuleType(name)
    module.__file__=str(path)
    sys.modules[name]=module
    exec(compile(path.read_bytes(),str(path),'exec'),module.__dict__)
    return module


class Tape:
    def __init__(self,origin,default='_'):
        self.origin=self.head=origin
        self.cells={}
        self.default=default
        self.low=self.high=origin
        self.newlow=self.newhigh=origin
        self.writes=[]

    def at(self,index):
        return self.cells.get(index,self.default)

    def install(self,values,offset=0):
        for index,value in enumerate(values,self.origin+offset):
            self.cells[index]=str(value)

    def state(self):
        return {k:v for k,v in self.cells.items() if v!=self.default}


def word(value,width):
    return ['L']+[str((value>>j)&1) for j in range(width)]+['R']


def codeword(value):
    return [str((value>>j)&1) for j in range(13)]


def execute(code,entry,tapes,*,blocks=(),route_entries=(),limit=20000000):
    need(len({id(t.cells) for t in tapes})==len(tapes),'distinct physical owners')
    pc=entry
    steps=inside=payload_actions=0
    visits=[]
    while True:
        if pc in route_entries:
            visits.append((tapes[20].state(),tapes[18].state(),tapes[21].head))
        instruction=code[pc]
        op=instruction[0]
        steps+=1
        need(steps<=limit,'bounded independent run')
        inside+=any(lo<=pc<hi for lo,hi in blocks)
        if op in ('R','W','M'):
            role=instruction[1]
            tape=tapes[role]
            payload_actions+=role==21
            if op=='R':
                symbol=tape.at(tape.head)
                need(symbol in instruction[2],'outside-symbol or exterior read')
                pc=instruction[2][symbol]
            elif op=='W':
                tape.cells[tape.head]=instruction[2]
                tape.writes.append(tape.head)
                pc+=1
            else:
                need(instruction[2] in (-1,1),'nonunit movement')
                tape.head+=instruction[2]
                tape.low=min(tape.low,tape.head)
                tape.high=max(tape.high,tape.head)
                pc+=1
            tape.newlow=min(tape.newlow,tape.head)
            tape.newhigh=max(tape.newhigh,tape.head)
        elif op=='J':
            pc=instruction[1]
        elif op=='H':
            return {'status':instruction[1],'steps':steps,'route_steps':inside,
                    'payload_actions':payload_actions,'visits':visits}
        else:
            raise ValueError('unknown opcode')


def markers(h,p,*,index=None,address=None):
    tapes=[Tape(-37+3*t) for t in range(21)]
    grants=[p+2]+[h+3]*4+[3,h.bit_length()+3]+[h+4]*7
    for t in range(14):
        tapes[t].install(['OPAQUE-LEFT'],-1)
        tapes[t].install(['OPAQUE-RIGHT'],grants[t])
        # Larger old retained history is independent of current blank extent.
        tapes[t].high=tapes[t].origin+max(grants[t]-1,79)
    for t,value,width in ((14,h,p),(15,1,p),(17,(1<<p)-1,p),(19,(1<<h)-1,h)):
        tapes[t].install(word(value,width))
    tapes[16].install(word(0,p)[:-1]+['|','R'])
    if index is not None:tapes[20].install(word(index,h))
    if address is not None:tapes[18].install(word(address,h))
    for t,width in ((14,p+2),(15,p+2),(16,p+3),(17,p+2),(18,h+2),(19,h+2),(20,h+2)):
        tapes[t].install(['OPAQUE-LEFT'],-1)
        tapes[t].install(['OPAQUE-RIGHT'],width)
        tapes[t].high=tapes[t].origin+max(width-1,97)
    return tapes,grants


def fixture(h,p,s,a,*,values=None,keys=None):
    tapes,grants=markers(h,p)
    tapes[15].install(word(s,p))
    tapes[16].install(word(a,p)[:-1]+['|','R'])
    N=1<<h
    values=values if values is not None else [(4095,0,5,6,170,340)[i%6] for i in range(N)]
    keys=keys if keys is not None else [N-1-i for i in range(N)]
    data=codeword(5)
    for value,key in zip(values,keys):
        data+=codeword(4096+value)
        for digit in range(h-1,-1,-1):data+=codeword(2+((key>>digit)&1))
    data+=codeword(6)
    payload=Tape(-11,'0')
    payload.install(data)
    payload.install(['1','1','0','1'],-4)
    payload.install(['1','0','1'],len(data)+1)
    payload.high=payload.origin+len(data)+100
    tapes.append(payload)
    return tapes,values,keys,grants,len(data)


def read_integer(mapping,origin,width):
    return sum((mapping.get(origin+1+j)=='1')<<j for j in range(width))


def decoded_keys(tape,h):
    values=[]
    for i in range(1<<h):
        at=tape.origin+13*(2+i*(h+1))
        value=0
        for digit in range(h):
            code=sum((tape.at(at+13*digit+j)=='1')<<j for j in range(13))
            need(code in (2,3),'valid allocated output key')
            value=2*value+code%2
        values.append(value)
    return values


def check_endpoint(tapes,before,h,p,expected,*,check_heads=True,check_index=True):
    for t,tape in enumerate(tapes[:-1]):
        old=dict(before[t])
        if t==17:
            for j in range(p):old[tape.origin+1+j]='0'
        if t==20 and not check_index:continue
        need(tape.state()==old,'complete marker contents/retirement '+str(t))
        if check_heads:need(tape.head==tape.origin,'marker head return')
    payload=tapes[21]
    old=dict(before[21])
    allowed=[]
    for i,key in enumerate(expected):
        at=payload.origin+13*(2+i*(h+1))
        for digit in range(h):
            out=codeword(2+((key>>(h-1-digit))&1))
            for j,value in enumerate(out):
                where=at+13*digit+j
                allowed.append(where)
                if value=='0':old.pop(where,None)
                else:old[where]=value
    need(payload.state()==old,'full payload/key/exterior oracle')
    need(payload.writes==allowed,'only allocated key cells, exactly once')
    if check_heads:need(payload.head==payload.origin,'paid payload head return')


def fail(action,label):
    try:action()
    except ValueError:return label
    raise ValueError('missed negative control: '+label)


def static(package,key,code,labels,meta):
    original,_,route_meta=key.route_source().compile_controller()
    need(len(code)==21135 and key.digest(code)=='8f5ae62b89de8308eb021920185269d884f07f625a5b3ee10b39f27aee5a393b',
         'exact complete graph')
    need(set(row[1] for row in code if row[0] in ('R','W','M'))==set(range(22)),'22 fixed roles')
    def embedding(candidate):
        for mode,block in meta['route_copies'].items():
            start=block['start']
            need(block['length']==10123,'whole route extent')
            for offset,row in enumerate(original):
                if row[0]=='R':expected=('R',row[1],{s:start+v for s,v in row[2].items()})
                elif row[0]=='J':expected=('J',start+row[1])
                elif row==('H','DONE'):expected=('J',block['return'])
                else:expected=row
                need(candidate[start+offset]==expected,'complete exact route relocation')
    embedding(code)
    broken=list(code)
    offset=next(i for i,r in enumerate(original) if r==('H','DONE'))
    broken[meta['route_copies']['FORWARD']['start']+offset]=('H','DONE')
    control=fail(lambda:embedding(broken),'missing-child-return')
    join=load(package/'join.py','_independent_key_join_text')
    raw=(package/'inputs/route/inputs/point/caller.py').read_text()
    before,tail=raw.split('def prepare_keys(',1)
    _,after=tail.split('def run_leg(',1)
    adapted=before+join.REPLACEMENT+'def run_leg('+after
    old_ast,new_ast=ast.parse(raw),ast.parse(adapted)
    old_nodes={n.name:ast.dump(n,include_attributes=False) for n in old_ast.body if isinstance(n,ast.FunctionDef)}
    new_nodes={n.name:ast.dump(n,include_attributes=False) for n in new_ast.body if isinstance(n,ast.FunctionDef)}
    need(set(old_nodes)==set(new_nodes),'no added/deleted caller functions')
    need([name for name in old_nodes if old_nodes[name]!=new_nodes[name]]==['prepare_keys'],
         'exactly one caller AST seam')
    need(not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='route_address'
                 for n in ast.walk(new_ast)),'obsolete host route loop called')
    return {'exact_route_instructions':2*len(original),'outer_locations':len(code)-2*len(original),
            'entries':meta['entries'],'graph_sha256':key.digest(code),'controls':[control],
            'only_caller_AST_change':'prepare_keys'}


def full_cases(code,meta):
    blocks=[(b['start'],b['start']+b['length']) for b in meta['route_copies'].values()]
    entries=[b['start']+meta['route_metadata']['entries'][mode] for mode,b in meta['route_copies'].items()]
    reports=[]
    for h,p,s,a in ((1,2,2,1),(2,3,3,2),(3,7,5,3),(2,97,4,3),(2,5,1,0)):
        for mode,sign in (('FORWARD',1),('INVERSE',-1)):
            tapes,_,_,grants,L=fixture(h,p,s,a)
            before=[t.state() for t in tapes]
            result=execute(code,meta['entries'][mode],tapes,blocks=blocks,route_entries=entries)
            need(result['status']=='DONE','successful whole key pass')
            expected=[(i+sign*a)%s if i<s else i for i in range(1<<h)]
            need(decoded_keys(tapes[21],h)==expected,'independent direct rotation oracle')
            check_endpoint(tapes,before,h,p,expected)
            need(len(result['visits'])==1<<h,'all and only N current indices')
            for i,(index,address,position) in enumerate(result['visits']):
                need(read_integer(index,tapes[20].origin,h)==i==read_integer(address,tapes[18].origin,h),
                     'physical current index and fresh address')
                need(position==tapes[21].origin+13*(2+i*(h+1)),'physical record address')
            need(result['steps']-result['route_steps']==(1<<h)*(156*h+126)+18*h+203,'exact added instruction bill')
            need(result['payload_actions']==(1<<h)*(117*h+66)+156,'payload action bill already included')
            need(all(tapes[t].low>=tapes[t].origin for t in range(22)),'no exterior-left visit')
            need(sum(grants)==p+11*h+h.bit_length()+48,'fixed private-window formula')
            for t,length in enumerate(grants+[p+2,p+2,p+3,p+2,h+2,h+2,h+2]):
                need(tapes[t].newlow==tapes[t].origin and tapes[t].newhigh<tapes[t].origin+length,
                     'actual fixed per-owner invocation window '+str(t))
            need(tapes[21].newlow==tapes[21].origin and tapes[21].newhigh==tapes[21].origin+L,
                 'complete payload frame plus exactly one visited right frontier')
            need(tapes[21].high==tapes[21].origin+L+100,'old larger payload history retained')
            reports.append({'h':h,'p':p,'s':s,'a':a,'mode':mode,'steps':result['steps'],
                            'outer':result['steps']-result['route_steps'],'payload_actions':result['payload_actions']})
    return reports


def macros(key):
    Builder=key.route_source().point_source().Builder
    results=[]
    for h in (1,2,3,7,17,257):
        for helper,name,expected in ((key.initialize_index,'initialize',11*h+17),
                                     (key.copy_index,'copy',11*h+15),
                                     (lambda b:key.clear_word(b,20),'clear',7*h+9)):
            b=Builder();helper(b);b.op('H','DONE');b.mark('ADAPTER_FAIL');b.op('H','MALFORMED')
            code,_=b.finish()
            tapes,_=markers(h,h+1,index=None if name=='initialize' else (1<<h)-1)
            result=execute(code,0,tapes)
            need(result['status']=='DONE' and result['steps']-1==expected,'exact '+name+' macro count')
            results.append((h,name,expected))
        for c in sorted({0,min(1,h),h-1,h}):
            b=Builder();key.increment_index(b,'MORE','COMPLETE');b.mark('MORE');b.op('H','MORE');b.mark('COMPLETE');b.op('H','COMPLETE');b.mark('ADAPTER_FAIL');b.op('H','MALFORMED')
            code,_=b.finish()
            tapes,_=markers(h,h+1,index=(1<<c)-1)
            result=execute(code,0,tapes)
            expected=7*h+8 if c==h else 7*c+9
            need(result['steps']-1==expected and result['status']==('COMPLETE' if c==h else 'MORE'),
                 'literal index carry/overflow and exact bill')
            need(read_integer(tapes[20].state(),tapes[20].origin,h)==((1<<c)%(1<<h)),'index increment residue')
            need(tapes[20].head==tapes[20].origin,'complete increment return')
            results.append((h,'carry'+str(c),expected))
    return {'cases':len(results),'widths':[1,2,3,7,17,257],
            'checksum':sha256(json.dumps(results).encode()).hexdigest()}


def controls(code,labels,meta):
    h,p,s,a=2,5,3,2
    correct=[2,0,1,3]
    results=[]
    # Returning output-key complement: all guards/retirement remain valid.
    changed=list(code)
    lo,hi=labels['FORWARD_ROUTE_RETURN'],labels['FORWARD_INDEX_INCREMENT']
    writes=[i for i in range(lo,hi) if code[i][:2]==('W',21)]
    for i in (writes[0],writes[13]):changed[i]=('W',21,str(1-int(code[i][2])))
    tapes,*_=fixture(h,p,s,a);before=[t.state() for t in tapes]
    result=execute(changed,meta['entries']['FORWARD'],tapes)
    actual=decoded_keys(tapes[21],h)
    need(result['status']=='DONE' and actual!=correct,'returning complemented keys')
    check_endpoint(tapes,before,h,p,actual)
    results.append('returning-key-complement')
    # New returning control: corrupt an opaque payload bit while keeping alignment.
    changed=list(code);at=labels['FORWARD_RECORD'];old=code[at]
    need(old==('M',21,1),'first opaque payload advance')
    changed[at]=('J',len(changed));changed.extend((('W',21,'0'),old,('J',at+1)))
    tapes,*_=fixture(h,p,s,a);before=[t.state() for t in tapes]
    result=execute(changed,meta['entries']['FORWARD'],tapes)
    need(result['status']=='DONE' and decoded_keys(tapes[21],h)==correct,'opaque corruption returns correct keys')
    results.append(fail(lambda:check_endpoint(tapes,before,h,p,correct),'returning-opaque-payload-corruption'))
    for label,modify in (
        ('returning-unpaid-payload-rewind',lambda c:c.__setitem__(labels['FORWARD_PAYLOAD_REWIND'],('J',labels['FORWARD_INDEX_RETIRE']))),
        ('returning-dirty-index-origin',lambda c:c.__setitem__(max(i for i in range(labels['FORWARD_INDEX_RETIRE'],labels['INVERSE']) if c[i]==('W',20,'_')),('W',20,'0'))),
    ):
        changed=list(code);modify(changed)
        tapes,*_=fixture(h,p,s,a);before=[t.state() for t in tapes]
        result=execute(changed,meta['entries']['FORWARD'],tapes)
        need(result['status']=='DONE','mutation must return')
        results.append(fail(lambda:check_endpoint(tapes,before,h,p,correct),label))
    alias,*_=fixture(h,p,s,a);alias[20]=alias[18]
    results.append(fail(lambda:execute(code,meta['entries']['FORWARD'],alias),'physical-owner-alias'))
    return results


def receipt_audit(package):
    primary=json.loads((package/'RESULT.json').read_text())
    prior=json.loads((package/'inputs/route/RESULT.json').read_text())
    fields=('encoded_source_symbol_actions','radix_bit_control_instructions','radix_passes',
            'retained_symbol_roles','retained_symbol_cells','retained_bucket_bits',
            'retained_radix_register_bits','literal_point_instructions','literal_route_instructions')
    cases=[]
    for current in primary['actual_caller_cases']:
        old=next(x for x in prior['actual_caller_cases'] if x['name']==current['name'])
        for new,previous in zip(current['directions'],old['directions']):
            need(all(new[x]==previous[x] for x in fields),'unchanged external source/radix/storage/query costs')
            need(new['payload_bit_actions_included_in_literal_bill']==1356==4*(117*2+66)+156,
                 '1356 payload actions inside the graph exactly once')
            need(new['literal_key_pass_instructions']-new['literal_route_instructions']==1991==4*(156*2+126)+18*2+203,
                 'actual exact added graph bill')
            need(new['remaining_payload_adapter_bit_actions']==156 and new['outer_adapter_symbol_actions']==382,
                 'retained external source/payload setup not dropped')
        cases.append(current['name'])
    return {'actual_source_cases':cases,'unchanged_external_components':list(fields),
            'payload_actions_included_once_per_leg':1356,'external_payload_actions_per_leg':156,
            'external_marker_actions_per_leg':382,
            'scope':'Receipt/seam audit; complete source/radix providers were not independently re-executed.'}


def overwrite_boundary():
    N,s,a=4,3,2
    old=[(i,[3,2,1,0][i]) for i in range(N)]
    forward=sorted(((i,(i+a)%s if i<s else i) for i,_ in old),key=lambda x:x[1])
    inverse=sorted(((original,(position-a)%s if position<s else position)
                    for position,(original,_) in enumerate(forward)),key=lambda x:x[1])
    need([i for i,k in inverse]==list(range(N)) and [k for i,k in inverse]==list(range(N)),
         'permutation restores original physical payloads/identity keys')
    need(inverse!=old,'arbitrary overwritten keys are not recovered')
    return {'original_keys':[3,2,1,0],'final_keys':[k for _,k in inverse],
            'sorts':'Mathematical permutation oracle, not an implemented sorter.',
            'arbitrary_key_rollback_excluded':True}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--package',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--write',type=Path)
    args=parser.parse_args();p=args.package
    expected={'key_pass.py':'3df218d812d47c1e935715c87d716a7acf7a2bf2610c752ba409a9e29014d8f3',
              'PROOF.md':'ea1a6ffb0f282e8805788d5ae2521b2a9658a3e963f00575c794e6c7080fbcd4'}
    for name,digest in expected.items():need(sha256((p/name).read_bytes()).hexdigest()==digest,'reviewed scientific source changed')
    pins=json.loads((p/'SOURCE-PINS.json').read_text())['files']
    for pin in pins:
        raw=(p/pin['local']).read_bytes()
        need(len(raw)==pin['bytes'] and sha256(raw).hexdigest()==pin['sha256'],'retained source hash')
        need(sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==pin['git_blob'],'retained source Git blob')
    key=load(p/'key_pass.py','_independent_reviewed_key_table')
    code,labels,meta=key.compile_pass()
    result={'status':'PASS','reviewed_sha256':expected,'retained_sources':len(pins),
            'static':static(p,key,code,labels,meta),'complete_sparse_passes':full_cases(code,meta),
            'macro_counts':macros(key),'controls':controls(code,labels,meta),
            'inverse_boundary':overwrite_boundary(),'source_cost_vector':receipt_audit(p)}
    text=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.write:args.write.write_text(text)
    print(text,end='')


if __name__=='__main__':main()
