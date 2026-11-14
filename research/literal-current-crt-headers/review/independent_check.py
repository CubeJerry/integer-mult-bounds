"""Independent sparse-tape/grammar audit of the frozen leaf-header graph.

Only the offline compiler is loaded. No author verifier, interpreter, fixture,
decoding helper, expected-cost helper or native source provider is executed.
Default is read-only; --write explicitly saves a deterministic receipt.
"""
from pathlib import Path
from hashlib import sha1, sha256
import argparse
import ast
import copy
import json
import sys
import types

PROOF_SHA = '67f6312067c1eb7f41888c9a425eda36331e16c16bd66c1e3580a4905321acb9'
HEADERS_SHA = '9c270a0b6af2f1eb53e5246acf1df85202ca029493b2cd2ae81776d75baee78f'
GRAPH_SHA = '267752d474d8b1565ceb0415609b34e75797d8c6b735600242ceb410613b0508'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(path, name):
    module = types.ModuleType(name); module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module


class Tape:
    def __init__(self, origin, default='_', prior=73):
        self.origin = self.head = origin
        self.cells = {}; self.default = default
        self.low, self.high = origin - 17, origin + prior
        self.visited = [origin, origin]; self.writes = []

    def at(self, position):
        return self.cells.get(position, self.default)

    def put(self, tokens, position=None):
        if position is None:
            position = self.origin
        for at, value in enumerate(tokens, position):
            self.cells[at] = value

    def state(self):
        return {p: s for p, s in self.cells.items() if s != self.default}


def execute(code, entry, tapes, stop=None, limit=2000000):
    need(len(tapes) == 27 and len({id(t.cells) for t in tapes}) == 27, 'distinct owners')
    pc, count = entry, 0
    actions, visits = [0]*27, {}
    for t in tapes:
        t.visited = [t.head, t.head]
    while True:
        if stop is not None and pc == stop:
            return dict(status='CHILD_ENTRY', steps=count, actions=actions, visits=visits)
        op, *args = code[pc]; count += 1
        need(count <= limit, 'bounded sparse execution')
        visits[pc] = visits.get(pc, 0) + 1
        if op in ('R', 'W', 'M'):
            role = args[0]; t = tapes[role]; actions[role] += 1
            if op == 'R':
                symbol = t.at(t.head)
                need(symbol in args[1], 'out-of-alphabet read')
                pc = args[1][symbol]
            elif op == 'W':
                t.cells[t.head] = args[1]; t.writes.append(t.head); pc += 1
            else:
                need(args[1] in (-1, 1), 'unit move')
                t.head += args[1]; pc += 1
            t.visited = [min(t.visited[0], t.head), max(t.visited[1], t.head)]
            t.low, t.high = min(t.low, t.head), max(t.high, t.head)
        elif op == 'J':
            pc = args[0]
        elif op == 'H':
            return dict(status=args[0], steps=count, actions=actions, visits=visits)
        else:
            raise ValueError('unknown instruction')


def little(value, width):
    return [str((value >> i) & 1) for i in range(width)]


def fixture(widths, s=None, a=None, old=137, payload=False):
    h, u, m = widths[-1], widths[-2], len(widths)-2
    p, U, W = u+h+1, sum(widths[:-1]), max(widths[:-1])
    need(m >= 1 and p >= 4, 'local typed extent')
    s = (1 << h)-1 if s is None else s
    a = s-1 if a is None else a
    need(1 <= s < 1 << h and 0 <= a < s, 'supplied admitted numerical values')
    tapes = [Tape(-401+17*r, '0' if r == 21 else '_', old) for r in range(27)]
    for r, t in enumerate(tapes):
        t.put(['OPAQUE_LEFT'], t.origin-2)
        t.put(['OPAQUE_RIGHT'], t.origin+max(old+3, 3*sum(widths)+4*len(widths)+30))
    source = []
    for j, w in enumerate(widths):
        modulus = s if j == len(widths)-1 else ((1 << w)-1)
        value = (j+3) % (1 << w)
        source += ['ROOT']+['1']*w+['WE']+little(modulus, w)+['WE']+little(value, w)+['RE']
    source += ['R']
    bodies = (source, ['1']*m+['STEP','1','R'], ['1']*p,
              ['ROOT']+little(a,p)+['WE','PAIR','RETURN','1','R'], [])
    for r, body in zip(range(22,27), bodies):
        t=tapes[r]; t.put(['L'], t.origin-1); t.put(body)
    if payload:
        data = little(5,13)
        for i in range(1 << h):
            value=(0,4095,171,2730)[i%4]
            data += little(4096+value,13)
            for bit in range(h-1,-1,-1):
                data += little(2+(((1 << h)-1-i) >> bit & 1),13)
        data += little(6,13)
        tapes[21].cells = {}
        tapes[21].put(['1','1','0','1'], tapes[21].origin-5)
        tapes[21].put(data)
        tapes[21].put(['1','0','1'], tapes[21].origin+len(data)+1)
    params=dict(h=h,u=u,m=m,p=p,U=U,W=W,s=s,a=a)
    return tapes, params


def snapshots(tapes):
    return [(t.state(),t.head,t.low,t.high) for t in tapes]


def headers(params):
    h,p,s,a=(params[k] for k in ('h','p','s','a'))
    return {14:['L']+little(h,p)+['R'],15:['L']+little(s,p)+['R'],
            16:['L']+little(a,p)+['|','R'],17:['L']+['0']*p+['R'],
            19:['L']+['1']*h+['R']}


def boundary(tapes, before, params, retired=False, keys=None):
    expected=headers(params)
    for r,t in enumerate(tapes):
        wanted=dict(before[r][0])
        if r in expected and not retired:
            wanted.update({t.origin+i:s for i,s in enumerate(expected[r])})
        if r == 21 and keys is not None:
            h=params['h']
            for i,key in enumerate(keys):
                at=t.origin+13*(2+i*(h+1))
                for digit in range(h):
                    code=little(2+((key >> (h-1-digit)) & 1),13)
                    for k,s in enumerate(code):
                        where=at+13*digit+k
                        if s=='0':wanted.pop(where,None)
                        else:wanted[where]=s
        need(t.state()==wanted,'complete contents role '+str(r))
        need(t.head==before[r][1],'head return role '+str(r))
        need(t.low<=before[r][2] and t.high>=before[r][3],'historical extent retained')


def check_case(code, metadata, widths, **kwargs):
    tapes,p=fixture(widths,**kwargs); old=snapshots(tapes)
    b=execute(code,metadata['entries']['BUILD'],tapes)
    need(b['status']=='HEADERS','successful literal headers')
    boundary(tapes,old,p)
    h,w,m,U,W=(p[k] for k in ('h','p','m','U','W'))
    bill=6*w*h+53*w+41*U+57*m+42*h+199-h.bit_count()
    need(b['steps']==bill,'complete BUILD bill')
    native=(12*U+17*m+12*h+41,4*m+8,16*w+20,4*w+14,18*U+26*m+30)
    need(tuple(b['actions'][22:])==native,'per-native overlap counts')
    Q=3*U+4*m+3*h+9
    for r,length in zip(range(22,27),(Q,m+1,w+1,w+3,W+2)):
        origin=tapes[r].origin-1
        need(tapes[r].visited==[origin,origin+length],'exact native history role '+str(r))
    r=execute(code,metadata['entries']['RETIRE'],tapes)
    need(r['status']=='RETIRED' and r['steps']==28*w+7*h+53,'complete retirement bill')
    need(sum(r['actions'][22:])==0,'retirement does not access closed native roles')
    boundary(tapes,old,p,retired=True)
    return dict(widths=list(widths),p=w,build=b['steps'],retire=r['steps'],native=sum(native),
                max_skipped_width=W,source_extent=Q,scratch_extent=W+3,
                prior_history=kwargs.get('old',137))


def source_checks(package, compiler, code, metadata):
    pins=json.loads((package/'SOURCE-PINS.json').read_text())['files']
    for pin in pins:
        raw=(package/pin['local']).read_bytes()
        need(len(raw)==pin['bytes'] and sha256(raw).hexdigest()==pin['sha256'],'retained exact bytes')
        need(sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==pin['git_blob'],'retained Git blob')
    key=compiler.key_source(); child,_,_=key.compile_pass(); start=metadata['key_start']
    need(len(child)==21135 and len(code)==21513 and start==378,'complete child extent')
    for i,(op,*args) in enumerate(child):
        if op=='R':wanted=(op,args[0],{s:start+t for s,t in args[1].items()})
        elif op=='J':wanted=(op,start+args[0])
        else:wanted=(op,*args)
        need(code[start+i]==wanted,'unchanged relocated child '+str(i))
    need(not any(row[0]=='W' and row[1] in range(22,26) for row in code),'borrowed source write target')
    need({row[1] for row in code if row[0] in ('R','W','M')}==set(range(27)),'exact role inventory')
    for op,*args in code:
        need(op in ('R','W','M','J','H'),'literal instruction set')
        if op=='M':need(args[1] in (-1,1),'only unit moves')
    tree=ast.parse((package/'join.py').read_bytes())
    constants={node.targets[0].id:ast.literal_eval(node.value) for node in tree.body
               if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name)
               and node.targets[0].id in ('OLD_BUILD','NEW_BUILD','OLD_RETIRE','NEW_RETIRE')}
    caller=package/'inputs/keypass/inputs/route/inputs/point/caller.py'
    raw=caller.read_bytes(); text=raw.decode()
    need(sha256(raw).hexdigest()=='055e86590e1cb03555f9ef6f1d585f8c23453a4cc10cd7feda7362c77f7bce1c','source caller pin')
    function='def run_leg('+text.split('def run_leg(',1)[1]
    for name in ('BUILD','RETIRE'):
        need(function.count(constants['OLD_'+name])==1,'unique original seam')
    adapted=function.replace(constants['OLD_BUILD'],constants['NEW_BUILD']).replace(constants['OLD_RETIRE'],constants['NEW_RETIRE'])
    restored=adapted.replace(constants['NEW_BUILD'],constants['OLD_BUILD']).replace(constants['NEW_RETIRE'],constants['OLD_RETIRE'])
    need(restored==function,'no source edits beyond two explicit seams')
    positions=[adapted.index(s) for s in ('literal = point.run(', 'base.literal_radix(', 'endpoint.stage(lease)',
               'lease.close()', 'endpoint.commit()', "point.run(ports, 'RETIRE')")]
    # The caller also closes earlier skipped leases, before the selected one.
    positions[3]=adapted.index('lease.close()',positions[2])
    need(positions==sorted(positions),'current lease/radix/commit/retirement chronology')
    scope=adapted[adapted.index('ports = ('):adapted.index('literal = point.run(')]
    for expression in ('_NativePort(iterator.source)','_NativePort(iterator.counters[\'axis\'])',
                       '_NativePort(lease.actual.guide)','_NativePort(result)',
                       '_NativePort(iterator.counters[\'width\'])'):
        need(expression in scope,'actual physical native binding')
    need('emit_headers(' not in adapted and 'prepare_keys(' not in adapted,'old host header/key loops removed')
    return dict(retained_byte_blob_pins=len(pins),child_instructions=len(child),new_locations=start,
                source_seams=2,source_function_sha256=sha256(function.encode()).hexdigest(),
                adapted_function_sha256=sha256(adapted.encode()).hexdigest(),
                remote_reauthentication='Not rerun here; exact retained bytes and blobs independently checked.')


def controls(code, labels, metadata):
    rows=[]; outer=metadata['key_start']
    mutation_points={
        'height':(labels['HEIGHT_INCREMENT'],('J',labels['HEIGHT_COUNTED'])),
        'offset':(next(i for i,x in enumerate(code[:outer]) if x==('W',16,'1')),('W',16,'0')),
        'scratch':(next(i for i in range(labels['LEFT_RECORD'],labels['RIGHT_HEADERS']) if code[i]==('W',26,'_')),None),
        'head':(max(i for i in range(labels['HEADERS_READY']) if code[i]==('M',25,1)),None),
        'retirement':(next(i for i in range(labels['RETIRE'],outer) if code[i]==('W',16,'_')),None)}
    for name,(pc,replacement) in mutation_points.items():
        bad=list(code);bad[pc]=replacement if replacement is not None else ('J',pc+1)
        tapes,p=fixture((3,3,2,2),s=3,a=2);before=snapshots(tapes)
        out=execute(bad,metadata['entries']['BUILD'],tapes)
        need(out['status']=='HEADERS','returning '+name+' mutant')
        retired=name=='retirement'
        if retired:
            out=execute(bad,metadata['entries']['RETIRE'],tapes)
            need(out['status']=='RETIRED','returning retirement mutant')
        try:boundary(tapes,before,p,retired=retired)
        except ValueError as error:rows.append(dict(name=name,returned=out['status'],detected=str(error)))
        else:raise ValueError('returning mutant escaped '+name)
    for name in ('short_prefix','wrong_root','dirty_width','short_result','shifted_head','alias'):
        tapes,p=fixture((3,3,2,2),s=3,a=2)
        if name=='short_prefix':tapes[22].cells[tapes[22].origin+5]='WE'
        elif name=='wrong_root':tapes[22].cells[tapes[22].origin]='PAIR'
        elif name=='dirty_width':tapes[26].cells[tapes[26].origin]='1'
        elif name=='short_result':tapes[25].cells[tapes[25].origin+2]='WE'
        elif name=='shifted_head':tapes[22].head+=1
        else:tapes[25]=tapes[24]
        try:out=execute(code,metadata['entries']['BUILD'],tapes)
        except ValueError as error:
            need(name=='alias' and str(error)=='distinct owners','expected physical binding rejection')
            rows.append(dict(name=name,rejected='owner binder'));continue
        need(out['status']=='MALFORMED','malformed '+name+' rejection')
        rows.append(dict(name=name,rejected=out['status'],rollback_claimed=False))
    return rows


def joined_cases(code,metadata):
    rows=[]; key_start=metadata['key_start']; key_meta=metadata['key_metadata']
    for h,s,a in ((2,3,2),(3,5,4)):
        for direction in ('FORWARD','INVERSE'):
            tapes,p=fixture((3,3,2,h),s=s,a=a,payload=True);before=snapshots(tapes)
            prefix=execute(code,metadata['entries'][direction],tapes,
                           stop=key_start+key_meta['entries'][direction])
            need(prefix['status']=='CHILD_ENTRY','uninterrupted fixed child entry')
            B=6*p['p']*h+53*p['p']+41*p['U']+57*p['m']+42*h+199-h.bit_count()
            need(prefix['steps']==B+2,'joined header prefix bill')
            boundary(tapes,before,p)
            # Resume the same physical state; the stop merely observes the seam.
            child=execute(code,key_start+key_meta['entries'][direction],tapes)
            need(child['status']=='DONE','unchanged complete key child')
            values=[(i+(a if direction=='FORWARD' else -a))%s if i<s else i for i in range(1<<h)]
            boundary(tapes,before,p,keys=values)
            retired=execute(code,metadata['entries']['RETIRE'],tapes)
            need(retired['status']=='RETIRED','joined retirement')
            boundary(tapes,before,p,retired=True,keys=values)
            direct,p2=fixture((3,3,2,h),s=s,a=a,payload=True)
            whole=execute(code,metadata['entries'][direction],direct)
            need(whole['status']=='DONE' and whole['steps']==prefix['steps']+child['steps'],
                 'one uninterrupted literal run equals observed seam run')
            boundary(direct,before,p2,keys=values)
            rows.append(dict(h=h,s=s,a=a,direction=direction,header_steps=prefix['steps'],
                             key_steps=child['steps'],retire_steps=retired['steps'],
                             uninterrupted_steps=whole['steps'],destinations=values))
    return rows


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--package',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--write',type=Path); args=parser.parse_args(); package=args.package
    need(sha256((package/'headers.py').read_bytes()).hexdigest()==HEADERS_SHA,'frozen compiler')
    need(sha256((package/'PROOF.md').read_bytes()).hexdigest()==PROOF_SHA,'frozen proof')
    compiler=load(package/'headers.py','_independent_B9_compiler')
    code,labels,metadata=compiler.compile_headers()
    need(sha256(json.dumps(code,sort_keys=True,separators=(',',':')).encode()).hexdigest()==GRAPH_SHA,'frozen graph')
    source=source_checks(package,compiler,code,metadata)
    cases=[]
    for h in (1,2,3,7,8,15,16,31,65):
        cases.append(check_case(code,metadata,(2,2,h)))
    for widths in ((1009,1,2,2),(*([1]*61),2,3),(7,257,2,3),(3,3,257,2)):
        cases.append(check_case(code,metadata,widths))
    cases.append(check_case(code,metadata,(2,2,2),old=32771))
    result=dict(status='PASS_INDEPENDENT_LEAF_HEADERS',proof_sha256=PROOF_SHA,graph_sha256=GRAPH_SHA,
                method='Separate sparse-dictionary CPU and direct record/header/key oracle; no author runtime or verifier.',
                source_checks=source,header_cases=cases,returning_and_domain_controls=controls(code,labels,metadata),
                joined_cases=joined_cases(code,metadata),
                limits='No heavy retained numerical source/radix replay; static exact seams and already-reviewed child preserved.')
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.write:args.write.write_text(text)
    print(text,end='')


if __name__=='__main__':main()
