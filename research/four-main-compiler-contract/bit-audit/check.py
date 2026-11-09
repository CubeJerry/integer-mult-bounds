#!/usr/bin/env python3
"""Independent BIT integral transfer, transpose, invoice and ambient arithmetic.
No predecessor scientific imports; elementary functions come from the lead's
independent moment checker. @CubeJerry, OpenAI assistance, Apache-2.0.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import argparse,copy,gzip,hashlib,importlib.util,json
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('lead_moments',HERE/'rational.py')
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
def need(x,s):
    if not x:raise ValueError(s)
def read(p):
    raw=p.read_bytes();return json.loads(gzip.decompress(raw) if p.suffix=='.gz' else raw)
def add(dst,src,coefficient=1,q=0,stage=0,mod2=False):
    for (output,head,body),value in src.items():
        key=(output,head^(q%2),body+stage);z=dst.get(key,0)+coefficient*value
        if mod2:z%=2
        if z:dst[key]=z
        else:dst.pop(key,None)
def shift(row,stages=(),q=0,mod2=False):
    r={};add(r,row,q=q,stage=sum(1<<(6*(s-1)) for s in stages),mod2=mod2);return r
def caller(w,mod2=False,binary=False):
    n,L=w['roles'],w['stages'];occ=Counter()
    for e in w['events']:
        if e[0]=='LOCAL':occ[e[1]]+=1
        elif e[0]=='IDLE':occ.update(e[3])
        elif e[0]=='IDLE_ONE':occ.update(e[2])
    need(all(1<=s<=L and k<64 for s,k in occ.items()),'stage exponent bound')
    rows=[{(i,0,0):1} for i in range(n)]
    for e in reversed(w['events']):
        op=e[0]
        if op=='ADD':
            a=Q(1) if binary else Q(e[3]);need(a.denominator==1,'integrality before reduction')
            add(rows[e[2]],rows[e[1]],int(a),mod2=mod2)
        elif op=='SCALE':
            a=Q(e[2]);need(a in (-1,1),'unimodular scaling');rows[e[1]]={k:int(a)*v for k,v in rows[e[1]].items()}
        elif op=='SWAP':rows[e[1]],rows[e[2]]=rows[e[2]],rows[e[1]]
        elif op=='QUERY':
            q=1 if binary else e[3];need(q in (-1,1),'odd central query');add(rows[e[2]],rows[e[1]],q=q,mod2=mod2)
        elif op=='LOCAL':
            s,x,y=e[1:];a=shift(rows[x],[s],mod2=mod2);add(a,shift(rows[y],[s],q=1,mod2=mod2),mod2=mod2)
            rows[x],rows[y]=a,shift(rows[y],[s],mod2=mod2)
        elif op in ('IDLE','IDLE_ONE'):
            roles=e[1:3] if op=='IDLE' else e[1:2];stages=e[3] if op=='IDLE' else e[2]
            for r in roles:rows[r]=shift(rows[r],stages,mod2=mod2)
        elif op=='LAMBDA':
            need(not binary and e[2] in (-1,1),'lambda specialization')
            # First q^2=1 in characteristic zero: ((1+si)+(1-si)q^2)/2=1.
            # Only then reduce integral coefficients. No division by2 in F2.
        else:raise ValueError(op)
    for i,d in enumerate(w['diagonal']):
        if binary:q,stages=d['q'],d['stages']
        else:
            q,z,*mask=d;need(z==0 and len(mask)==L,'source target schema');stages=[j+1 for j,x in enumerate(mask) if x]
        want={(i,q%2,sum(1<<(6*(s-1)) for s in stages)):1}
        need(rows[i]==want,'exact polynomial endpoint '+str(i))
    return {'entries':n*n,'ring':'F2[q,D]/(q^2-1)' if mod2 else 'Z[q,D]/(q^2-1)','free_stages':L}
def reduction(source,binary):
    events=[]
    for e in source['events']:
        if e[0]=='LAMBDA':continue
        if e[0]=='SCALE':need(Q(e[2]) in (-1,1),'unit scale');continue
        if e[0]=='ADD':
            a=Q(e[3]);need(a.denominator==1,'integer ADD')
            if a.numerator%2:events.append(e[:3])
        elif e[0]=='QUERY':need(e[3] in (-1,1),'odd q');events.append(e[:3])
        else:events.append(e)
    diagonal=[{'q':d[0]%2,'stages':[s for s,x in enumerate(d[1:]) if x]} for d in source['diagonal']]
    need(events==binary['events'] and diagonal==binary['diagonal'],'exact reduction payload')
    need((source['roles'],source['stages'])==(binary['roles'],binary['stages']),'same inputs/stages')
def native(w):
    n=w['public'];N=n+w['owned_fields'];rows=[1<<i for i in range(n)]+[0]*(N-n)
    for e in reversed(w['program']):
        op=e[0];a=e[1]
        if op=='ADD':rows[e[2]]^=rows[a]
        elif op=='SWAP':rows[a],rows[e[2]]=rows[e[2]],rows[a]
        elif op in ('INIT','CLEAR'):rows[a]=0
        elif op!='MOVE':raise ValueError(op)
    want=[1<<i for i in range(n)]+[0]*(N-n)
    for i in range(111):want[i]^=1<<(i+111)
    need(rows==want,'exact native transpose')
    return {'public':n,'owned_labels':N-n,'entries':n*n,'events':len(w['program'])}
def invoice(w,c):
    dim={int(k):f['dim'] for k,f in w['frames'].items()}
    helper=Counter(abs(dim[a]-dim[b]) for a,b in zip(w['start'][222:],w['final'][222:]))
    paid=Counter(abs(dim[e[2]]-dim[e[3]]) for e in w['program'] if e[0]=='MOVE')
    need(min(helper)>0 and min(paid)>0,'positive ranks');T=Counter();P=Counter();stages=[]
    for e in c['events']:
        if e[0]=='LOCAL':T.update(helper);P.update(paid);stages.append(e[1])
        elif e[0]=='QUERY':P[1]+=111
        elif e[0]=='IDLE':P[7*len(e[3])]+=222
        elif e[0]=='IDLE_ONE':P[7*len(e[2])]+=111
    need(sorted(stages)==list(range(1,19)),'one native per stage')
    for d in c['diagonal']:T[d['q']+7*len(d['stages'])]+=111
    need(sum(T.values())==11640 and sum(P.values())==56673,'complete inventory')
    need(sum(k*v for k,v in T.items())-sum(k*v for k,v in P.items())==753,'rank surplus')
    return T,P
def log_rat(x):
    a,b=M.log_bounds(x.numerator);c,d=M.log_bounds(x.denominator);return a-d,b-c
def cap(saving,A,v,c,b,gap):
    t=1-saving;den=2
    while not c**den<b**(den-1):den+=1
    theta=Q(den-1,den);la=M.log_bounds(A);lt=log_rat(t);lh=log_rat(theta);l2=M.log_bounds(2)
    eta=(lt[0]-v*saving*la[1],lt[1]-v*saving*la[0])
    def margin(p):return eta[0]-p*lh[1],eta[1]-p*lh[0]
    p=1
    while margin(p)[0]<=0 or p*l2[0]-v*saving*la[1]<=0:p+=1
    need(margin(p-1)[1]<0,'prior logarithm power fails')
    need(2*c**(v*den)<=A**(v*(den-1)),'shifted exit')
    step=gap.denominator
    def passes(j):return (step*j+1)**p<2**j
    lo,hi=1,2
    while not passes(hi):lo,hi=hi,2*hi
    while hi-lo>1:
        k=(lo+hi)//2
        if passes(k):hi=k
        else:lo=k
    need(passes(hi) and not passes(hi-1),'compiler integer grid')
    return {'ambient':A,'maximum_target':127,'product_power':v,'theta':str(theta),'logarithm_power':p,'grid_index':hi,'H':step*hi,'positive_log_margin_diagnostic':[float(x) for x in margin(p)],'prior_power_log_margin_diagnostic':[float(x) for x in margin(p-1)],'source596_log_margin_diagnostic':[float(x) for x in margin(596)],'exact_inequalities':True}
def reject(fn):
    try:fn()
    except ValueError:return True
    return False
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',default=str(HERE/'retained'));ap.add_argument('--output');a=ap.parse_args();s=Path(a.source)
    for row in json.loads((HERE/'RETAINED.json').read_text())['files']:
        blob=(HERE/row['path']).read_bytes()
        need(len(blob)==row['size'] and hashlib.sha256(blob).hexdigest()==row['sha256'],'retained byte identity')
        need(hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest()==row['git_blob'],'retained Git blob identity')
    pins={'two-fragment/CONTROLLER.json':'543b8728e659561b95e127dad7bd7534645996d7d2c61602bb5d89c89a73944c','bit/FRAGMENT-CALLER.json.gz':'32b1bd9f8df940a78b0e65360fa0ef3729291e285e4629bcbbcc1e4f8db39e02','bit/retained/root/inputs/BIT-NATIVE-WORD.json.gz':'51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','bit/FRAGMENT-BIT-ADMISSION.json':'86955dcd74bc3fa1a940419474d45054fa7b0366b71b242568680366923d9311'}
    for path,sha in pins.items():need(hashlib.sha256((s/path).read_bytes()).hexdigest()==sha,'source pin '+path)
    integral=read(s/'two-fragment/CONTROLLER.json');binary=read(s/'bit/FRAGMENT-CALLER.json.gz');word=read(s/'bit/retained/root/inputs/BIT-NATIVE-WORD.json.gz');receipt=read(s/'bit/FRAGMENT-BIT-ADMISSION.json')
    result={'source_pins':pins,'integral_identity':caller(integral),'binary_identity':caller(binary,True,True),'native_transpose':native(word)}
    reduction(integral,binary);result['literal_reduction']=True
    T,P=invoice(word,binary);need(dict(T)=={int(k):v for k,v in receipt['targets'].items()} and dict(P)=={int(k):v for k,v in receipt['paid'].items()},'independent invoice equals pinned receipt')
    signed=Counter(T);signed.subtract(P);logs={k:M.log_bounds(k) for k in signed};moments={}
    for label,value in [('tested','.00376670'),('raw_lower','.0037667234775'),('raw_upper','.0037667234776')]:
        x,y=M.signed_moment(signed,Q(value),logs);need(y<0 if label=='raw_upper' else x>0,'exact BIT moment sign '+label);moments[label]={'saving':value,'interval_diagnostic':[float(x),float(y)],'exact_sign':-1 if y<0 else 1}
    result['moments']=moments;result['targets']=dict(sorted(T.items()));result['paid']=dict(sorted(P.items()))
    result['conservative_compiler_cap']=cap(Q('.00376670'),134,768,15,16,Q(1,10**10))
    ops=Counter(e[0] for e in binary['events']);ports=111;roles=binary['roles'];stages=binary['stages'];thin=ops['QUERY'];idles=ops['IDLE']+ops['IDLE_ONE']
    basis=ports*8*(ops['ADD']+3*ops['SWAP'])
    visible=stages*10**7+basis+256*ports*(stages+thin+roles)
    rc=4*(sum(P.values())+sum(T.values()))+8*ports*stages+8*ports*idles
    owned=stages*word['owned_fields']+2*ports*roles*len(binary['events'])+16*ports*(stages+thin+roles)
    need(rc==receipt['whole_job_route_count'] and visible==receipt['ordinary_visible_records'] and owned==receipt['owned_bank_bound'],'independent literal source tariff census')
    need(owned<10**7,'fresh raw owned reserve')
    frame=word['frames'];ambient_native=len(next(iter(frame.values()))['A'][0]);need(ambient_native==8,'native index dimension')
    for i in range(ports):
        need(frame[str(word['start'][i])]['dim']==1 and frame[str(word['final'][i])]['dim']==8,'X interface dimensions')
        need(frame[str(word['start'][i+ports])]['dim']==0 and frame[str(word['final'][i+ports])]['dim']==7,'Y interface dimensions')
    physical_ambient=ambient_native+7*stages;need(physical_ambient==134,'native axes plus distinct stage axes')
    routes=8*(10*physical_ambient**2+10*physical_ambient)*rc
    need(visible+routes<10**12,'actual134-axis route allowance')
    result['conservative_route_invoice']={'ambient':134,'route_count':rc,'routes':routes,'visible':visible,'total':routes+visible,'allowance':10**12,'owned_reserve':owned,'owned_allowance':10**7,'event_counts':dict(ops)}
    previous=Q('.0034');covered=Q('.00376670')-Q(2,10**10);atom=Q('.004');wrappers=[]
    for admitted in [Q('.00376523'),Q('.00376669')]:
        envelope=(1-atom)*covered+atom*previous
        need(atom>envelope>admitted>previous and atom<1-envelope,'wrapper arithmetic')
        wrappers.append({k:str(v) for k,v in {'previous':previous,'covered':covered,'atom':atom,'envelope':envelope,'admitted':admitted,'margin':envelope-admitted}.items()});previous=admitted
    result['wrapper_arithmetic_from_canonical_admission']=wrappers
    controls={}
    for op in ['LOCAL','QUERY','IDLE','IDLE_ONE']:
        bad=copy.deepcopy(binary);del bad['events'][next(i for i,e in enumerate(bad['events']) if e[0]==op)]
        controls['delete_'+op]=reject(lambda:caller(bad,True,True))
    bad=copy.deepcopy(binary);j=next(i for i,e in enumerate(bad['events']) if e[0]=='IDLE_ONE');bad['events'][j][2]+=bad['events'][j][2]
    controls['body_involution_shortcut']=reject(lambda:caller(bad,True,True))
    bad=copy.deepcopy(word);j=next(i for i in range(len(bad['program'])-1,-1,-1) if bad['program'][i][0]=='ADD');del bad['program'][j]
    controls['native_last_add']=reject(lambda:native(bad))
    bad=copy.deepcopy(integral);j=next(i for i,e in enumerate(bad['events']) if e[0]=='ADD');bad['events'][j][3]='3/2'
    controls['nonintegral_before_reduction']=reject(lambda:caller(bad))
    need(all(controls.values()),'nonrejecting BIT controls');result['controls']=controls
    result['scope']='Independent exact algebra/invoice and conservative ambient-cap arithmetic. Generic cap theorem, physical/native contracts and ordinary-wrapper theorem remain separate proof dependencies; not automatic BIT admission.'
    if a.output:Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
    else:need(json.loads(json.dumps(result))==json.loads((HERE/'RESULT.json').read_text()),'complete mathematical receipt')
    print(json.dumps({k:result[k] for k in ['integral_identity','binary_identity','native_transpose','moments','conservative_compiler_cap','conservative_route_invoice','controls']},indent=2));print('PASS_INDEPENDENT_BIT_DEPENDENCY_AUDIT')

if __name__=='__main__':main()
