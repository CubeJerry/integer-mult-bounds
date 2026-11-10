"""Lead-written target-only review of the complete-row finite graph."""
from pathlib import Path
from types import ModuleType
from hashlib import sha256
import argparse,json,random
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--package-root',type=Path,default=Path(__file__).resolve().parent.parent)
parser.add_argument('--write-result',action='store_true')
args=parser.parse_args(); package=args.package_root.resolve()
raw=(package/'rows.py').read_bytes(); mod=ModuleType('reviewed_rows')
exec(compile(raw,str(package/'rows.py'),'exec'),mod.__dict__)
def need(ok,label):
    if not ok: raise RuntimeError(label)
class CellTape:
    def __init__(self,body,marker,port):
        self.origin=7+3*port
        self.data={i:(i+port)%7 for i in range(self.origin-1)}
        self.data[self.origin-1]=marker
        self.data.update({self.origin+i:x for i,x in enumerate(body)})
        self.head=self.origin; self.low=self.origin
        self.prefix={i:self.data[i] for i in range(self.origin)}
    def body(self):
        result=[]; cursor=self.origin
        while self.data.get(cursor,6)!=6:
            result.append(self.data[cursor]); cursor+=1
        return tuple(result)
    def replace(self,body):
        for i in list(self.data):
            if i>=self.origin: self.data[i]=6
        self.data.update({self.origin+i:x for i,x in enumerate(body)})
def run(code,entry,tapes):
    state=entry; count=0
    while count<4000000:
        row=code[state]; count+=1; op=row[0]
        if op=='halt':
            for t in tapes:
                need(t.head==t.origin,'restored translated origin')
                need(all(t.data[i]==v for i,v in t.prefix.items()),'buried prefix preserved')
                need(t.low>=t.origin-1,'no crossing buried origin')
            return row[1],count
        if op=='reject': raise ValueError(row[1])
        t=tapes[row[1]]
        if op=='read': state=row[2].get(t.data.get(t.head,6),row[3])
        elif op=='write': t.data[t.head]=row[2]; state=row[3]
        elif op=='move': t.head+=row[2]; state=row[3]
        else: raise RuntimeError('unexpected instruction')
        t.low=min(t.low,t.head)
    raise RuntimeError('bounded review nontermination')
def codeword(symbol): return (symbol//4,(symbol//2)%2,symbol%2)
def encoded_row(widths,bits):
    output=[]; at=0
    for width in widths:
        for bit in bits[at:at+width]: output.extend(codeword(bit))
        output.extend(codeword(2)); at+=width
    need(at==len(bits),'independent row shape')
    return tuple(output)
def bank(w,guide,fields,bridge=(),header=()):
    return [CellTape(body,2 if i<=w else 5,i)
            for i,body in enumerate([*fields,guide,bridge,header])]
rng=random.Random(20261110); cases=steps=state_checks=0
for w in (*range(2,10),17,65):
    code,entry=mod.compile_rows(w)
    need(len(code)==273*w+125,'independent state census'); state_checks+=1
    for widths in ((1,),(2,3),(1,4,2,3)):
        guide=encoded_row(widths,[0]*sum(widths)); B=len(guide)
        for cycles in (1,2,3):
            R=w*cycles
            source_rows=[encoded_row(widths,[rng.randrange(2) for _ in range(sum(widths))]) for _ in range(R)]
            source=sum(source_rows,()); L=len(source)
            parent=bank(w,guide,[source]*w)
            kind,c=run(code,entry['classify'],parent)
            need(kind=='inner' and c==8*B+9,'derived classifier equation'); steps+=c
            _,c=run(code,entry['prepare'],parent)
            need(parent[-1].body()==guide and c==9*B+8,'derived format copy equation'); steps+=c
            child=bank(w,(),[()]*w,source,guide)
            _,c=run(code,entry['install'],child)
            need(c==13*L+4*R+R//w+9*B+3*w+12,'derived installation equation'); steps+=c
            for port in range(w):
                need(child[port].body()==sum(source_rows[port::w],()),'independent stripe permutation')
            need(child[w].body()==guide and child[-2].body()==source and child[-1].body()==guide,'guide/source preservation')
            # Change every numerical result before collection: returning saved
            # ingress instead of actual returned fields must fail.
            returned=[encoded_row(widths,[rng.randrange(2) for _ in range(sum(widths))]) for _ in range(R)]
            for port in range(w): child[port].replace(sum(returned[port::w],()))
            child[-2].replace(()); child[-1].replace(())
            _,c=run(code,entry['collect'],child)
            need(c==13*L+4*R+R//w+4*w+4,'derived collection equation'); steps+=c
            need(child[-2].body()==sum(returned,()),'collector consumes returned fields')
            for port in range(w):
                need(child[port].body()==sum(returned[port::w],()),'collection borrows complete results')
            need(child[w].body()==guide,'collection preserves format'); cases+=1
w=3; code,entry=mod.compile_rows(w)
guide=encoded_row((2,1),[0,0,0]); row=encoded_row((2,1),[1,0,1]); controls=[]
for name,fields in [('extra_last_field',[row,row,row+row]),('short_middle_field',[row,(),row])]:
    try: run(code,entry['collect'],bank(w,guide,fields))
    except ValueError: controls.append(name)
    else: raise RuntimeError('accepted malformed returned field')
for name,malformed in [('empty_component_guide',(0,1,0)),('same_length_wrong_delimiters',encoded_row((1,2),[0,0,0]))]:
    try: run(code,entry['classify'],bank(w,malformed,[row]*w))
    except ValueError: controls.append(name)
    else: raise RuntimeError('accepted wrong component shape')
record={'status':'PASS_INDEPENDENT_CODED_ROWS','cases':cases,'state_counts':state_checks,
        'target_transitions':steps,'controls':controls,'seed':20261110,
        'reviewed_rows_sha256':sha256(raw).hexdigest(),
        'source_executor_imported':False,'author_verifier_imported':False,'numerical_child_replayed':False}
receipt=Path(__file__).resolve().parent/'RESULT.json'
if args.write_result: receipt.write_text(json.dumps(record,indent=2)+'\n')
else: need(json.dumps(json.loads(receipt.read_text()),sort_keys=True)==json.dumps(record,sort_keys=True),'typed frozen receipt')
print('PASS_INDEPENDENT_CODED_ROWS',cases,state_checks,len(controls))
