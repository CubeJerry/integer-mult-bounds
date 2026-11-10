"""Small independent acceptance-domain comparison; no old-code bug alleged."""
import json
from hashlib import sha1, sha256
from pathlib import Path
from types import ModuleType
import sys

HERE=Path(__file__).resolve().parent
for pin in json.loads((HERE/'PINS.json').read_text())['files']:
    raw=(HERE/pin['retained_path']).read_bytes()
    if sha256(raw).hexdigest()!=pin['sha256'] or sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()!=pin['git_blob']:
        raise ValueError('changed comparison input: '+pin['retained_path'])

def load(path,name):
    module=ModuleType(name);module.__file__=str(path)
    sys.modules[name]=module
    exec(compile(path.read_bytes(),str(path),'exec'),module.__dict__)
    return module

old=load(HERE/'predecessor/row_programs.py','overlap_old_rows')
new=load(HERE/'variant/rows.py',
         'overlap_new_rows')

class Tape:
    def __init__(self,body='',marker=2):
        self.cells={0:marker,**{i+1:int(b) for i,b in enumerate(body)}}
        self.head=1
    def read(self): return self.cells.get(self.head,6)
    def write(self,b): self.cells[self.head]=b
    def move(self,d):
        if d not in (-1,1): raise ValueError('unit move')
        self.head+=d
    def body(self):
        i=1;out=[]
        while self.cells.get(i,6)!=6:
            out.append(str(self.cells[i]));i+=1
        return ''.join(out)

guide='000010000010'
values={name:0 for name,_ in old.SCHEMA}
values.update(outer=1,rows=1,stock=1,row_bits=len(guide))
header=''
for name,_ in old.SCHEMA:
    bits=bin(values[name])[2:][::-1]
    header+='1'*len(bits)+'0'+bits

def run_old(fields):
    ports=[old.PhysicalPort(Tape()) for _ in range(old.FIRST_ROLE)]
    output=Tape(marker=5)
    ports[old.OUTPUT]=old.PhysicalPort(output,5)
    ports[old.HEADER]=old.PhysicalPort(Tape(header))
    ports += [old.PhysicalPort(Tape(f)) for f in fields]
    try:
        steps=old.run(old.compile_router(2,True),ports)
    except ValueError as exc:
        return {'accept':False,'error':str(exc),'partial_output_length':len(output.body())}
    return {'accept':True,'output':output.body(),'steps':steps}

def run_new(fields):
    output=Tape(marker=5)
    ports=[*(Tape(f) for f in fields),Tape(guide),output,Tape(marker=5)]
    code,entries=new.compile_rows(2)
    try:
        _,steps=new.execute(code,entries['collect'],ports)
    except ValueError as exc:
        return {'accept':False,'error':str(exc),'partial_output_length':len(output.body())}
    return {'accept':True,'output':output.body(),'steps':steps}

cases={
    'valid':([guide,guide],True,True),
    'same_length_missing_component_separator':([guide,'000000000010'],True,False),
    'same_length_virtual_blank':([guide,'100010000010'],True,False),
    'uniform_extra_complete_rows':([guide*2,guide*2],False,True),
    'only_last_field_extra_row':([guide,guide*2],False,False),
}
result={}
for name,(fields,a,b) in cases.items():
    left,right=run_old(fields),run_new(fields)
    if left['accept']!=a or right['accept']!=b:
        raise ValueError((name,left,right))
    result[name]={'predecessor':left,'guide_variant':right}
expected=json.loads((HERE/'DIFFERENTIAL.json').read_text())
if json.dumps(result,sort_keys=True)!=json.dumps(expected,sort_keys=True):
    raise ValueError('differential receipt mismatch')
print('PASS_ROW_OVERLAP_DIFFERENTIAL',len(result))
