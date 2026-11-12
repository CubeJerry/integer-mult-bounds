#!/usr/bin/env python3
"""Compile one complete common-restored observer using the pinned source interpreter."""
import argparse,collections,gzip,hashlib,importlib.util,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,m):
    if not x:raise ValueError(m)
def enc(r):return [[i,str(c)] for i,c in sorted(r.items())]
def build(w,W,z,sel,route):
    M=sorted(set(w['live'])|{j+112 for j in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']))
    qm={j:1480+i for i,j in enumerate(M)};q=qm[77];y=qm[189];cache=1931;tmp=1932
    ops=[];reservations=[];marks={};pre={}
    for j,c in z.items():
        if w['final'][j]!=127:
            need(w['initial'][j]==3,'initial correction access');d=W[j].get(j,F(0));need(d!=0,'same-role initial transfer');pre[j]=-c/d
    need(len(pre)==60 and 77 not in pre,'supported sixty-field precompensation')
    def emit(e):ops.append(e)
    def rawmove(t,e):
        reservations.append({'source_event':t,'physical_event':len(ops),'main_role':e[1]});emit(['MOVE',qm[e[1]],e[2],e[3],False])
    emit(['INIT',cache,71]);emit(['ADD',cache,q,'1',71]);emit(['ADD',q,77,'-1',71])
    if route=='source':
        emit(['INIT',tmp,71]);emit(['ADD',tmp,q,'1',71]);emit(['MOVE',tmp,71,3,True])
    for t,e in enumerate(w['program']):
        if e[0]=='MOVE' and e[1]==77:rawmove(t,e)
    if route=='hub':
        emit(['INIT',tmp,127]);emit(['ADD',tmp,q,'1',127]);emit(['MOVE',tmp,127,3,True])
    marks['precorrection_start']=len(ops)
    for j,c in sorted(pre.items()):emit(['ADD',j,tmp,str(c),3])
    emit(['CLEAR',tmp,3]);marks['initial_history_start']=len(ops)
    reads=collections.defaultdict(list)
    for x in sel['historical_decoder']:reads[x['after_event']].append(x)
    for x in reads[-1]:emit(['ADD',y,x['role'],x['coefficient'],x['chart']])
    for t,e in enumerate(w['program']):
        if e[0]=='MOVE' and e[1]==189:rawmove(t,e)
    marks['native_start']=len(ops)
    for t,e in enumerate(w['program']):
        if t==29098:
            marks['encoder_start']=len(ops)
            emit(['INIT',tmp,71]);emit(['ADD',tmp,cache,'1',71]);emit(['ADD',tmp,287,'-1',71]);emit(['ADD',287,tmp,'1',71]);emit(['CLEAR',tmp,71]);emit(['CLEAR',cache,71])
        f=list(e);f[1]+=400 if f[1]>=1480 else 0
        if f[0] in ('ADD','COPY'):f[2]+=400 if f[2]>=1480 else 0
        emit(f)
        for x in reads[t]:emit(['ADD',y,x['role']+400 if x['role']>=1480 else x['role'],x['coefficient'],x['chart']])
    response={j:z.get(j,F(0))+sum((c*pre.get(i,F(0)) for i,c in W[j].items()),F(0)) for j in range(1480)}
    need(all(not c or w['final'][j]==127 for j,c in response.items()),'all offhub errors canceled')
    marks['hub_correction_start']=len(ops)
    for j,c in sorted(response.items()):
        if c:emit(['ADD',j,q,str(-c),127])
    emit(['ADD',q,77,'1',127]);marks['end']=len(ops)
    need(len(reservations)==7 and len({x['source_event'] for x in reservations})==7,'seven different raw reservations')
    return dict(schema='precorrected-source-observer-word-v1',source_sha256=PIN,packet_route=route,public=1880,owned_fields=53,initial=w['initial']+[w['initial'][j] for j in M],raw_role_map={str(j):qm[j] for j in M},program=ops,raw_reservations=reservations,marks=marks,precorrection=enc(pre),terminal_hub_response=enc({j:c for j,c in response.items() if c}),scope='One raw shear77 to189 completed; all1480 common outputs restored;398 other raw fields retained at initial charts. No complete400-output lift.'),qm
def validate(lib,w,W,word,qm):
    location=dict(enumerate(word['initial']))
    for t,e in enumerate(word['program']):
        op,j=e[:2]
        if op=='INIT':location[j]=e[2]
        elif op=='CLEAR':del location[j]
        elif op=='MOVE':need(location[j]==e[2],'route before event'+str(t));location[j]=e[3]
        elif op in ('ADD','COPY'):need(location[j]==location[e[2]]==e[4],'cochart before event'+str(t)+':'+str(e))
    r,loc,bill=lib.execute(w,word,word['program'])
    for j in range(1480):need(r[j]==W[j] and loc[j]==w['final'][j],'all1480 common endpoints')
    for j,label in qm.items():
        target={label:F(1)}
        if j==189:target[qm[77]]=F(1)
        need(r[label]==target,'all400 raw-input identities')
        need(loc[label]==(w['final'][j] if j in (77,189) else w['initial'][j]),'partial raw interface locations')
    need(bill['final_live_owned']==0,'all owned retired');return bill
def main(a):
    source=a.source.read_bytes();need(hashlib.sha256(source).hexdigest()==PIN,'native pin');w=json.loads(gzip.decompress(source))
    old=a.predecessor
    for name,pin in {'verify.py':'524ed58f8d029efa4bf092a0173f960a75db496b6a3012bdc065cbcfcae1dc16','OBSERVATIONS.json':'03c0dd40c55545892effd8dd8fdd45246a2a22b6eccb1df39f03f76154fb8a83'}.items():need(hashlib.sha256((old/name).read_bytes()).hexdigest()==pin,'pinned predecessor '+name)
    spec=importlib.util.spec_from_file_location('pinned_observer',old/'verify.py');lib=importlib.util.module_from_spec(spec);spec.loader.exec_module(lib)
    cert=json.loads((old/'OBSERVATIONS.json').read_text());W,Z,summary,reads=lib.source_check(w,cert['observations']);i=next(i for i,x in enumerate(cert['observations']) if x['donor']==77);sel=cert['observations'][i]
    expected=[{j:F(1)} for j in range(1480)]
    for k,x in enumerate(w['live']):
        y=x+112
        if k in w['hosted']['Dports']:expected[y]={y:F(1),x:F(1)}
        else:expected[x]={x:F(1),y:F(-1)};expected[y]={x:F(1,2),y:F(1,2)}
    for x,y in zip(w['hosted']['X2'],w['hosted']['Y2']):expected[x]={x:F(1),y:F(-1)}
    need(W==expected,'full native endpoint contract')
    need(sel['hrow']=={'77':'1'} and sel['gain']=='1','unit encoder');word,qm=build(w,W,Z[i],sel,a.route);bill=validate(lib,w,W,word,qm)
    payload=(json.dumps(word,sort_keys=True,separators=(',',':'))+'\n').encode();path=a.packet/('WORD-'+a.route.upper()+'.json.gz')
    if a.write_word:a.packet.mkdir(parents=True,exist_ok=True);path.write_bytes(gzip.compress(payload,mtime=0))
    else:need(gzip.decompress(path.read_bytes())==payload,'exact word reconstruction')
    base=collections.Counter(e[0] for e in w['program']);diff={k:bill['counts'].get(k,0)-base.get(k,0) for k in sorted(set(base)|set(bill['counts']))}
    pre={j:F(c) for j,c in word['precorrection']};j=min(pre);need(pre[j]*W[j][j]!=0,'omission negative control')
    early_error=sum((F(x['coefficient'])*pre.get(x['role'],F(0)) for x in sel['historical_decoder'] if x['after_event']==-1),F(0));need(early_error!=0,'snapshot ordering negative control')
    out=dict(status='PASS_LITERAL_1880_INPUT_PRECORRECTED_COMMON_RESTORATION_AND_ONE_RAW_SHEAR',source_sha256=PIN,packet_route=a.route,predecessor_pins={name:hashlib.sha256((old/name).read_bytes()).hexdigest() for name in ['verify.py','OBSERVATIONS.json']},word_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),word_payload_sha256=hashlib.sha256(payload).hexdigest(),bill=bill,added_to_native_counts=diff,new_paid_moves=[dict(source=127 if a.route=='hub' else 71,target=3,rank=9 if a.route=='hub' else 1,owned=True)],funded_raw_routes=7,unused_raw_reservations=1703,precorrection_fields=60,hub_correction_fields=len(word['terminal_hub_response']),physical_input_directions=1880,common_outputs_restored=1480,raw_shears_completed=1,other_raw_inputs_retained=398,premature_snapshot_error=str(early_error),negative_controls=['omitting one initial preload leaves a nonzero common output error','initial history read before precompensation changes decoder','funded raw reservation multiplicity and physical ownership checked'],scope=word['scope'],new_complete_kappa=None)
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--predecessor',type=Path,required=True);p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--route',choices=['source','hub'],default='source');p.add_argument('--write-word',action='store_true');p.add_argument('--output',type=Path,required=True);main(p.parse_args())
