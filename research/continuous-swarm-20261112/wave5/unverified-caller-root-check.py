"""Independent contact/lifecycle/serialization and outer-operator review.
Prepared for CubeJerry with OpenAI assistance. Apache-2.0.
No author verifier, source mapping helper or paid-digest function is used.
"""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import gzip
import hashlib
import importlib.util
import itertools
import json
import sys

def need(ok,message):
    if not ok: raise AssertionError(message)

def bank(owner):
    return owner[:2] if owner[0]=='aux' else owner[:3] if owner[0]=='owned' else owner

def bits(v):
    if type(v) is int:return max(1,abs(v).bit_length())
    if isinstance(v,dict):return max([1]+[bits(x) for x in v.values()])
    if isinstance(v,(list,tuple)):return max([1]+[bits(x) for x in v])
    return 1

def productive(word,caller):
    out={}
    for ty,d in caller['types'].items():
        for i,diagonal in enumerate(d['diagonal']):
            for port in d['ports']:
                out[('main',port,d['offset']+i)]=abs(diagonal[0])+8*sum(diagonal[2:])
    public_main=set(word['live'])|{x+112 for x in word['live']}
    public_main.update(word['hosted']['X2']);public_main.update(word['hosted']['Y2'])
    for ci,event in enumerate(caller['events']):
        if event[0]=='J':
            for slot in range(word['public']):
                if slot not in public_main:
                    out[('helper',ci,slot)]=len(word['frames'][word['final'][slot]])-len(word['frames'][word['initial'][slot]])
    need(len(out)==23392 and all(r>0 for r in out.values()),'actual productive fields')
    return out

def audit(records,word,caller,serialize=True):
    targets=productive(word,caller)
    state={o:['target-input',r] for o,r in targets.items()}
    occupied={bank(o):o for o in state}
    counts=Counter();paid=Counter();births=Counter();peak=Counter();active=Counter()
    digest=hashlib.sha256();pdigest=hashlib.sha256(b'[')
    size=maximum=largest=number=pc=0
    native_counts=Counter();last_source=None;expected_parts=[];observed_parts=[]
    last_ci=-1
    def close_group():
        if expected_parts:need(observed_parts==expected_parts,'complete native expansion in source order')
    for r in records:
        source=r['source'];owner=tuple(r['owner']);op=r['op'];raw=r['raw'];part=r['part']
        need(r['ambient']==153,'full ambient factor')
        if source[0]!='root':
            ci=source[0]
            need(last_ci<=ci<=last_ci+1,'chronological caller coverage');last_ci=ci
            if type(source[1]) is int:
                ni=source[1];key=(ci,ni)
                need(caller['events'][ci][0]=='J' and raw==word['program'][ni],'native raw source')
                if key!=last_source:
                    close_group();need(ni==native_counts[ci],'native source index chronology');native_counts[ci]+=1
                    expected_parts=['move-right','move-child','move-left'] if raw[0]=='MOVE' else ['native']
                    observed_parts=[];last_source=key
                observed_parts.append(part)
            else:
                need(raw==caller['events'][ci],'outer or boundary raw source')
                if source[1]=='outer':need(source[2] in caller['types'][raw[0]]['ports'],'actual replicated port')
        if op=='INIT':
            need(bank(owner) not in occupied and r['chart_in']=='inactive','distinct inactive lifetime bank')
            need(owner[0] in ('aux','owned'),'productive input is not scratch')
            occupied[bank(owner)]=owner;state[owner]=r['chart_out'];births[owner[0]]+=1;active[owner[0]]+=1
            peak[owner[0]]=max(peak[owner[0]],active[owner[0]])
        else:
            need(owner in state and occupied[bank(owner)]==owner,'current exact owner lifetime')
            need(state[owner]==r['chart_in'],'complete operation contact continuity')
            if op=='ADD':
                other=tuple(r['from_owner'])
                need(other!=owner and other in state and state[other]==state[owner],'distinct same-chart ADD source')
            if op=='SWAP':
                other=tuple(r['other_owner'])
                need(other!=owner and other in state and state[other]==state[owner],'complete distinct SWAP banks')
            if op=='CLEAR':
                need(owner[0] in ('aux','owned') and r['chart_out']=='inactive','retire only live owned lifetime')
                del state[owner];del occupied[bank(owner)];active[owner[0]]-=1
            else:state[owner]=r['chart_out']
        if op in ('ADD','SCALE','GAUSSIAN_INTEGER'):
            need(r['scalar_scope']=='outside-tensor','ordinary scalar outside tensor')
            if op!='GAUSSIAN_INTEGER':
                a,b=r['coefficient'];q=Fraction(a,b)
                need(q.denominator==b and q.numerator==a,'canonical exact rational encoding')
        if op=='C':
            need(r['completed_return'] is True and r['axes']==list(range(r['rank'])),'positive complete canonical child return')
            data=json.dumps(r['projection'],separators=(',',':'),sort_keys=True).encode()
            if pc:pdigest.update(b',')
            pdigest.update(data);pc+=1;paid[r['rank']]+=1
        if serialize:
            data=json.dumps(r,separators=(',',':'),sort_keys=True).encode()+b'\n'
            digest.update(data);size+=len(data);maximum=max(maximum,len(data));largest=max(largest,bits(r))
        number+=1;counts[op]+=1
    close_group();pdigest.update(b']')
    need(last_ci==len(caller['events'])-1,'complete caller suffix')
    need(native_counts=={i:len(word['program']) for i,e in enumerate(caller['events']) if e[0]=='J'},'all eighteen complete native calls')
    need(state=={o:['target-output',r] for o,r in targets.items()},'all productive final contacts and no private lifetimes')
    need(pc==117612 and pdigest.hexdigest()=='7ab145efbbc8d72e1893f6143a57dd45244237e912057a30291d74bf1603f376','exact accepted paid chronology')
    return {'records':number,'jsonl_bytes':size,'maximum_record_bytes':maximum,'largest_integer_bits':largest,'stream_sha256':digest.hexdigest(),'paid_positions':pc,'paid_digest':pdigest.hexdigest(),'operation_counts':dict(counts),'births':dict(births),'peak_active':dict(peak)}

def outer_algebra():
    # Characters diagonalize every complete translation. Their f lane
    # parities determine Q=i^h and whole X=Q^2=(-1)^h.
    checked=0
    for f in range(1,9):
        for lane_bits in itertools.product((0,1),repeat=f):
            h=sum(lane_bits);q=complex(0,1)**h;x=(-1)**h
            for sign in (-1,1):
                query=q if sign==1 else x*q
                need(query==complex(0,1)**(sign*h),'QUERY exact complete tensor inverse')
                lam=((1+sign*1j)+(1-sign*1j)*x)/2
                need(lam==(1 if h%2==0 else sign*1j),'LAMBDA whole-translation spectrum')
                checked+=1
    # Explicit non-tensor-mixture witness: two odd lane characters.
    need(((1+1j)+(1-1j)*1)/2==1 and (1j)**2==-1,'two-lane scalar placement witness')
    controls=[]
    for sign in (-1,1):
        z,t=Fraction(1),Fraction(-1)
        real=(z+t)/2;imag=sign*(z-t)/2
        need(real.denominator==imag.denominator==1,'final complete LAMBDA grid')
        need((z/2).denominator==2,'separately halved summand is off-grid')
        controls.append([sign,str(real),str(imag)])
    return {'character_cases':checked,'two_lane_lambda_is_not_tensorized':True,'one_final_half_controls':controls}

def main():
    p=Path(sys.argv[1]).resolve();sys.path.insert(0,str(p))
    spec=importlib.util.spec_from_file_location('stream_subject',p/'emit.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    word=json.loads(gzip.decompress((p/'reference/word.json.gz').read_bytes()));caller=json.loads((p/'reference/caller.json').read_text())
    science={n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in ('emit.py','geometry.py','catalogue.json.gz','PROOF.md')}
    result=audit(m.SelectedStream(p).records(),word,caller)
    controls=[]
    for kind in ('broken-child-return-contact','tensor-powered-scalar','productive-bank-as-private'):
        def modified():
            done=False
            for r in m.SelectedStream(p).records():
                if not done:
                    if kind=='broken-child-return-contact' and r['op']=='C':r=dict(r,completed_return=False);done=True
                    elif kind=='tensor-powered-scalar' and r['op']=='SCALE':r=dict(r,scalar_scope='inside-tensor');done=True
                    elif kind=='productive-bank-as-private' and r['op']=='INIT':r=dict(r,owner=['main',0,0]);done=True
                yield r
        try:audit(modified(),word,caller,False)
        except AssertionError as error:controls.append({'mutation':kind,'detected_by':str(error)})
        else:raise AssertionError('undetected semantic mutation')
    need(science=={n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in science},'frozen scientific bytes')
    print(json.dumps({'status':'PASS_INDEPENDENT_CALLER_STREAM_CONTACTS','scientific_sha256':science,'stream':result,'outer_algebra':outer_algebra(),'negative_controls':controls},sort_keys=True))

if __name__=='__main__':main()
