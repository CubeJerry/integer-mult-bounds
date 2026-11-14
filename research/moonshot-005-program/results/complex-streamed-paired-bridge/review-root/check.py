#!/usr/bin/env python3
"""Independent stream chronology review. Apache-2.0; @CubeJerry/OpenAI."""
import argparse,copy,gzip,hashlib,importlib.util,json
from fractions import Fraction as F
from pathlib import Path

def need(x,s):
    if not x:raise ValueError(s)

def load_engine():
    p=Path(__file__).with_name('engine.py')
    spec=importlib.util.spec_from_file_location('root_rational_replay',p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def rank(rows):
    b={}
    for source in rows:
        row=dict(source)
        for j in sorted(b):
            if j in row:
                c=row[j]
                for k,v in b[j].items():
                    z=row.get(k,F(0))-c*v
                    if z:row[k]=z
                    else:row.pop(k,None)
        if row:
            j=min(row);c=row[j];b[j]={k:v/c for k,v in row.items()}
    return len(b)

def main():
    p=argparse.ArgumentParser();p.add_argument('--package',type=Path,required=True);p.add_argument('--native',type=Path,required=True);p.add_argument('--seed',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    eng=load_engine()
    nr=a.native.read_bytes();sr=a.seed.read_bytes()
    need(hashlib.sha256(nr).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','native pin')
    need(hashlib.sha256(sr).hexdigest()=='6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc','seed pin')
    native=json.loads(gzip.decompress(nr));seed=json.loads(gzip.decompress(sr));parent=eng.replay(seed)
    role={int(k):v for k,v in seed['source_role_map'].items()};live=native['live']
    pairs={live[i]:(role[b],role[d])for i,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2'])}
    J=[1,6,32,33,48,49,50,73,74,75,82,83,84,85,98];T=[0,7]
    def root(h):
        bits=native['frames'][native['initial'][h]][0];on=[i for i in range(9)if bits>>i&1]
        if len(on)==3:return [2 if i in on else -1 for i in range(9)]
        off=[i for i in range(9)if not(bits>>i&1)]
        return [3*(int(i==off[0])-int(i==off[1]))for i in range(9)]
    P=[[ -F(sum(x*y for x,y in zip(root(h),root(j))),18)for j in J]for h in T]
    need(all(abs(v)==F(1,2)for row in P for v in row),'native dyadic rectangle')
    primal=[{role[j]:v for j,v in zip(J,row)if v}for row in P]
    need(rank(primal)==2,'rank-two target block')
    expected=copy.deepcopy(parent[0])
    for i,h in enumerate(T):
        for j,c in zip(J,P[i]):
            expected[role[h+112]]=eng.plus(expected[role[h+112]],{role[j]:F(1)},c)
            expected[pairs[j][0]]=eng.plus(expected[pairs[j][0]],{pairs[h][1]:F(1)},-c)
    reports=[]
    for mode in ['streaming','independent']:
        folder=a.package/mode;raw=(folder/'WORD.json.gz').read_bytes()
        w=json.loads(gzip.decompress(raw));meta=w['streaming'];relay=meta['relay']
        relays={relay}
        if mode=='independent':relays.add(meta['independent_return_relay'])
        need([[F(x)for x in row]for row in meta['P']]==P,'stored factor equals native block')
        crossing=[];initials=[];retired=[];bentry={}
        def hook(t,when,o,rows,loc):
            if when=='before':
                if o[0]=='CLEAR' and o[1] in relays:
                    need(not rows[o[1]] and loc[o[1]]==meta['D'],'actual clean retirement atD')
                    retired.append(o[1])
                if meta['markers']['begin']<=t<meta['markers']['end'] and o[0]=='ADD' and o[2] in [pairs[h][1]for h in T]:
                    need(rows[o[2]]=={o[2]:F(1)} and loc[o[2]]==meta['D'],'authentic adjoint source retained atD')
                return
            if o[0]=='INIT' and o[1] in relays:initials.append(o[1])
            if o[0]=='MOVE' and o[1] in relays:
                need({o[2],o[3]}=={meta['C'],meta['D']},'true station crossing')
                crossing.append(dict(rows[o[1]]))
            if t==meta['markers']['begin']:
                bentry.update({j:dict(rows[pairs[j][0]])for j in J})
            for phase in meta['phases']:
                i=phase['factor']
                if t==phase['pure_primal']:need(rows[relay]==primal[i],'pure primal at declared point')
                if t==phase['primal_zero']:need(not rows[relay] and loc[relay]==meta['D'],'actual output-based zero cleanup')
                if t==phase['adjoint_consumed']:
                    need(bool(bentry),'actual B entry state captured')
                    for j in J:
                        want=dict(bentry[j])
                        for k in range(i+1):want=eng.plus(want,{pairs[T[k]][1]:F(1)},-P[k][J.index(j)])
                        need(rows[pairs[j][0]]==want,'current B prefix invariant')
                if mode=='streaming' and t==phase['arrival']:
                    want=dict(primal[i])
                    if i:want=eng.plus(want,{pairs[T[i-1]][1]:F(1)},F(1))
                    need(rows[relay]==want,'transported mixed primal/previous-adjoint state')
        r=eng.replay(w,mode,hook=hook)
        need(r[0]==expected and r[1]==parent[1],'all400 public rows and final charts')
        need(len(crossing)==(5 if mode=='streaming' else 6),'all charged carrier crossings')
        need(len(initials)==len(retired)==(1 if mode=='streaming' else 4),'true moving owner lifetimes')
        need(rank(crossing)==4,'transported boundary-mode rank')
        author=json.loads((folder/'RESULT.json').read_text())
        need({str(k):v for k,v in r[2].items()}==author['raw_histogram'],'raw profile')
        need({str(k):v for k,v in r[3].items()}==author['owned_histogram'],'owned profile')
        need(r[4]==author['source_bill']['counts'] and r[5]==author['source_bill']['peak'] and r[6]==author['source_bill']['lifetimes'],'ordinary and owner invoice')
        negatives=[]
        if mode=='streaming':
            for label,index in [('previous_adjoint',meta['phases'][1]['previous_adjoint_subtraction']),('final_cleanup',meta['markers']['final_cleanup_subtraction'])]:
                bad=copy.deepcopy(w);need(bad['program'][index][0]=='ADD','mutation instruction')
                bad['program'][index][3]='0'
                if label=='final_cleanup':need(eng.replay(bad,mode)[0]==expected,'dirty-retirement mutation preserves public endpoints')
                try:
                    eng.replay(bad,mode,hook=hook);rejected=False
                except ValueError:rejected=True
                need(rejected,'missing '+label+' must fail')
                negatives.append(label+' omission rejected')
        reports.append(dict(mode=mode,word_sha256=hashlib.sha256(raw).hexdigest(),all400_rows=True,all_final_charts=True,
            raw=r[2],owned=r[3],ordinary_counts=r[4],peak=r[5],lifetimes=r[6],crossings=5 if mode=='streaming' else 6,
            moving_lifetimes=1 if mode=='streaming' else 4,transported_boundary_rank=4,negative_controls=negatives))
    need(reports[1]['ordinary_counts']['MOVE']-reports[0]['ordinary_counts']['MOVE']==1,'one actual MOVE saved')
    need(reports[1]['lifetimes']-reports[0]['lifetimes']==3,'three actual owner lifetimes saved')
    out=dict(status='PASS_INDEPENDENT_STREAMING_PAIRED_SOURCE_REVIEW',native_sha256=hashlib.sha256(nr).hexdigest(),seed_sha256=hashlib.sha256(sr).hexdigest(),author_proof_sha256=hashlib.sha256((a.package/'PROOF.md').read_bytes()).hexdigest(),variants=reports,
        scope='Root rational interpreter reused with new chronology hooks; no author builder/engine imported. Universal and global-rank arguments reviewed separately; no new kappa.')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])

if __name__=='__main__':main()
