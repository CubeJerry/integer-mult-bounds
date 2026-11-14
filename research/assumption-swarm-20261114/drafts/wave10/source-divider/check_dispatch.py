"""Read-only exhaustive fixed-table selector/port linkage certificate.

This checks each generated numerical access for every slot, independently
of numerical division replay. It is a structural author check, not the
separate reviewer's mathematical or interpreter check.
"""
from pathlib import Path
from hashlib import sha256,sha1
import json,sys,types
HERE=Path(__file__).resolve().parent
def load(path,name):
    m=types.ModuleType(name);m.__file__=str(path);sys.modules[name]=m
    exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
def need(x,s):
    if not x:raise ValueError(s)

def check(code,meta,logical):
    count=0
    for index,row in enumerate(logical):
        if row[0] not in('R','W','M') or row[1]>=4:continue
        selector=64+row[1]
        for slot in range(64):
            tape=['L']+[str((slot>>k)&1) for k in range(6)]+['R'];head=0
            pc=meta['logical_to_physical'][index];steps=0
            while True:
                op,*a=code[pc];steps+=1
                if op in('R','W','M') and a[0]<64:
                    need((op,a[0])==(row[0],slot) and head==0,'exact physical port and returned selector')
                    if op=='R':
                        need(a[1]=={s:meta['logical_to_physical'][target] for s,target in row[2].items()},'complete logical read continuations')
                        need(steps==30,'exact physical read dispatch cost')
                    else:
                        need(a[1]==row[2] and code[pc+1]==('J',meta['logical_to_physical'][index+1]),'exact literal effect and return')
                        need(steps+1==31,'exact physical write/move dispatch cost')
                    count+=1;break
                need(steps<32,'bounded fixed dispatcher')
                if op=='R':need(a[0]==selector,'only selected descriptor read');pc=a[1][tape[head]]
                elif op=='M':
                    need(a[0]==selector and a[1] in(-1,1),'only selected descriptor moves')
                    head+=a[1];need(0<=head<8,'exact eight-cell selector window');pc+=1
                elif op=='J':pc=a[0]
                else:raise ValueError('unexpected selector write/halt')
    return count

def main():
    d=load(HERE/'divider.py','B10_static_divider');code,_,meta=d.compile_divider();logical,_=d.logical_graph()
    count=check(code,meta,logical)
    for op,*a in code:
        need(op in('R','W','M','J','H'),'fixed opcode alphabet')
        if op in('R','W','M'):need(type(a[0]) is int and 0<=a[0]<68,'literal fixed physical role')
        if op=='M':need(a[1] in(-1,1),'unit move')
        targets=a[1].values() if op=='R' else(a[0],) if op=='J' else()
        need(all(type(t) is int and 0<=t<len(code) for t in targets),'closed fixed continuations')
    bad=list(code);at=next(i for i,row in enumerate(code) if row[0]=='R' and row[1]<64)
    bad[at]=('R',(bad[at][1]+1)%64,bad[at][2])
    try:check(bad,meta,logical)
    except ValueError:pass
    else:raise ValueError('wrong physical port mutant escaped')
    pins=json.loads((HERE/'SOURCE-PINS.json').read_text())['files']
    for pin in pins:
        raw=(HERE/pin['local']).read_bytes()
        need(len(raw)==pin['bytes'] and sha256(raw).hexdigest()==pin['sha256'],'exact input byte pin')
        need(sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==pin['git_blob'],'exact input Git blob')
    print(json.dumps({'status':'PASS','graph':d.digest(code),'locations':len(code),
                      'numerical_dispatch_slot_instances':count,'exact_source_objects':len(pins),
                      'wrong_physical_port_mutant_rejected':True},sort_keys=True,indent=2))

if __name__=='__main__':main()
