"""Bounded primary exact-integer checks; no claim of independent verification."""
from pathlib import Path
import types,sys,json,random

HERE=Path(__file__).resolve().parent
def load(path,name):
    m=types.ModuleType(name);m.__file__=str(path);sys.modules[name]=m
    exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
def need(x,s):
    if not x:raise ValueError(s)

class Tape:
    def __init__(self,cells,head):self.cells=list(cells);self.head=head;self.actions=0
    def read(self):self.actions+=1;return self.cells[self.head]
    def write(self,s):self.actions+=1;self.cells[self.head]=s
    def step(self,d):
        need(d in(-1,1) and 0<=self.head+d<len(self.cells),'physical owned frame')
        self.actions+=1;self.head+=d

def bits(x,p):return [str((x>>i)&1) for i in range(p)]
def fixture(hardware,p,n,d,slots=(18,9,20,14),history=0):
    ns,ds,qs,rs=slots
    ports=[Tape(['L']+['_']*(p+1)+['_']*history+['EXTERIOR'],1) for _ in range(64)]
    for slot,value in((ns,n),(ds,d)):ports[slot].cells[1:p+2]=bits(value,p)+['R']
    # Every other incoming live word can carry unrelated arbitrary data.
    for slot in(0,1,2,3,4,5,6,7):
        if slot not in slots:ports[slot].cells[1:p+2]=bits((slot*17+3)%2**p,p)+['R']
    selectors=[Tape(list('10101010')+['_']*history+['OUTSIDE'],0) for _ in range(4)]
    ports.extend(hardware.GrantedSelector(t,granted_extent=8) for t in selectors)
    return ports

def run_case(divider,hardware,code,labels,meta,p,n,d,slots,history=0):
    ports=fixture(hardware,p,n,d,slots,history);before=[(list(t.cells),t.head) for t in ports[:64]]
    program=hardware.Program(code,labels,meta)
    need(program.run(ports,'ACQUIRE')['status']=='READY','paid acquisition')
    hardware.setters(program,ports,slots)
    result=program.run(ports)
    need(result['status']=='DONE','literal arithmetic accepts')
    need(result['logical_instructions']==18*p*p+36*p+458+(12*p+9)*(n//d).bit_count(),
         'exact logical instruction formula')
    q,r=slots[2:]
    for slot,expected in((q,n//d),(r,n%d)):
        need(ports[slot].cells[1:p+2]==bits(expected,p)+['R'],'exact Euclidean output')
    for slot in range(64):
        need(ports[slot].head==1,'all numeric heads return')
        if slot not in(q,r):need((ports[slot].cells,ports[slot].head)==before[slot],'all incoming bytes unchanged')
        else:need(ports[slot].cells[p+2:]==before[slot][0][p+2:],'numeric exterior unchanged')
    for t in ports[64:]:need(t.head==0 and t.cells[:8]==['_']*8 and t.cells[-1]=='OUTSIDE','selector retirement/exterior')
    hardware.setters(program,ports,slots)
    retired=program.run(ports,'RETIRE')
    need(retired['status']=='RETIRED' and retired['logical_instructions']==14*p+131,'literal output retirement bill')
    for slot in(q,r):need(ports[slot].cells[1:p+2]==['_']*(p+1),'complete output erase including delimiter')
    need(program.total<=16384*(p+2)**2,'universal conservative full lifecycle bill')
    return {'p':p,'n':n,'d':d,'slots':list(slots),'history':history,'instructions':program.total,
            'division_instructions':result['instructions'],'numeric_actions':program.numeric_actions,
            'selector_actions':program.selector_actions}

def main():
    divider=load(HERE/'divider.py','b10_divider');hardware=load(HERE/'hardware.py','b10_hardware')
    code,labels,meta=divider.compile_divider();cases=[]
    for n in range(16):
        for d in range(1,8):cases.append(run_case(divider,hardware,code,labels,meta,4,n,d,(18,9,20,14)))
    rng=random.Random(7388)
    for p in(5,9,17,33):
        for _ in range(3):
            slots=tuple(rng.sample(range(8,64),4))
            cases.append(run_case(divider,hardware,code,labels,meta,p,rng.randrange(1<<p),rng.randrange(1,1<<(p-1)),slots,257))
    controls=[]
    for name,slots,n,d in(('alias',(18,9,20,20),7,3),('zero',(18,9,20,14),7,0),('high_margin',(18,9,20,14),7,8)):
        ports=fixture(hardware,4,n,d,slots);program=hardware.Program(code,labels,meta);program.run(ports,'ACQUIRE')
        hardware.setters(program,ports,slots)
        need(program.run(ports)['status']=='MALFORMED',name+' rejects');controls.append(name)
    ports=fixture(hardware,4,7,3);program=hardware.Program(code,labels,meta);program.run(ports,'ACQUIRE');hardware.setters(program,ports,(18,9,20,14))
    ports[64].cells[3]='|';need(program.run(ports)['status']=='MALFORMED','descriptor digit rejects');controls.append('descriptor_digit')
    for extent in(0,7):
        try:hardware.GrantedSelector(Tape(['_']*extent,0),granted_extent=extent)
        except ValueError:controls.append('explicit_grant_'+str(extent))
        else:raise ValueError('missing descriptor grant escaped')
    # Returning controls: clean status/head return alone is insufficient.
    mutations=[]
    qpc=meta['logical_labels']['QBIT_1'];lo=meta['logical_to_physical'][qpc];hi=meta['logical_to_physical'][qpc+1]
    bad=list(code)
    for pc in range(lo,hi):
        if bad[pc][0]=='W' and bad[pc][1]<64:bad[pc]=('W',bad[pc][1],'0')
    mutations.append(('returning_wrong_quotient',bad))
    bad=list(code)
    done=next(i for i,row in enumerate(bad) if row==('H','DONE'))
    bad[done]=('J',len(bad));bad.extend((('W',0,'0'),('H','DONE')))
    mutations.append(('returning_live_corruption',bad))
    for name,bad in mutations:
        ports=fixture(hardware,4,7,3);before=[list(t.cells) for t in ports]
        program=hardware.Program(bad,labels,meta);program.run(ports,'ACQUIRE');hardware.setters(program,ports,(18,9,20,14))
        need(program.run(ports)['status']=='DONE' and all(t.head==1 for t in ports[:64]),'returning control completes')
        correct=(ports[20].cells[1:6]==bits(2,4)+['R'] and ports[14].cells[1:6]==bits(1,4)+['R'] and ports[0].cells==before[0])
        need(not correct,name+' detected by full state oracle');controls.append(name)
    ports=fixture(hardware,4,7,3);program=hardware.Program(code,labels,meta);program.run(ports,'ACQUIRE')
    hardware.setters(program,ports,(0,9,20,14))
    need(program.run(ports)['status']=='DONE','stale but well-formed descriptor returns')
    need(ports[20].cells[1:6]!=bits(2,4)+['R'],'stale live numerical source detected');controls.append('returning_stale_descriptor')
    ports=fixture(hardware,4,7,3);program=hardware.Program(code,labels,meta);program.run(ports,'ACQUIRE')
    hardware.setters(program,ports,(18,9,20,14));need(program.run(ports)['status']=='DONE','retirement control input')
    hardware.setters(program,ports,(18,9,20,14));bad=list(code)
    logical,_=divider.logical_graph();retire=meta['logical_labels']['RETIRE']
    erased=next(i for i in range(retire,len(logical)) if logical[i]==('W',2,'_'))
    for pc in range(meta['logical_to_physical'][erased],meta['logical_to_physical'][erased+1]):
        if bad[pc][0]=='W' and bad[pc][1]<64:bad[pc]=('W',bad[pc][1],'0')
    failed=hardware.Program(bad,labels,meta).run(ports,'RETIRE')
    need(failed['status']=='RETIRED' and ports[20].head==1 and ports[20].cells[1:5]!=['_']*4,
         'returning incomplete output erase detected');controls.append('returning_incomplete_retirement')
    out={'status':'PASS','graph':divider.digest(code),'locations':len(code),'cases':len(cases),
         'instructions':sum(x['instructions'] for x in cases),'samples':cases[-12:],'controls':controls}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
