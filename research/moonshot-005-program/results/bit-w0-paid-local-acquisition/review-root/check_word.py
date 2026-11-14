#!/usr/bin/env python3
"""Independent sparse-set symbolic replay; no author implementation imported."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,gzip,hashlib,json
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(x,s):
    if not x:raise ValueError(s)
def rank(rows):
    a=[list(map(F,r)) for r in rows];p=0
    for c in range(8):
        q=next((i for i in range(p,len(a)) if a[i][c]),None)
        if q is None:continue
        a[p],a[q]=a[q],a[p];z=a[p][c];a[p]=[x/z for x in a[p]]
        for i in range(p+1,len(a)):
            z=a[i][c];a[i]=[x-z*y for x,y in zip(a[i],a[p])]
        p+=1
    return p
def main(a):
    raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');s=json.loads(gzip.decompress(raw))
    packed=a.word.read_bytes();w=json.loads(gzip.decompress(packed));need(w['public']==222,'222 public inputs')
    need(w['start']==s['start'][:222] and w['final']==s['final'][:222],'native endpoint IDs')
    fr={int(k):{'A':[list(map(F,r)) for r in v['A']],'B':[list(map(F,r)) for r in v['B']],'dim':v['dim']} for k,v in w['frames'].items()}
    for v in fr.values():
        need(rank(v['B'])==v['dim'] and rank(v['A'])==8-v['dim'],'chart ranks')
        need(all(sum(x*y for x,y in zip(r,t))==0 for r in v['A'] for t in v['B']),'orthogonal complements')
    pairs={tuple(o[2:]) for o in w['program'] if o[0]=='MOVE'}
    for x,y in pairs:
        need(abs(fr[x]['dim']-fr[y]['dim'])==1 and rank(fr[x]['B']+fr[y]['B'])==max(fr[x]['dim'],fr[y]['dim']),'nested unit MOVE')
    roots=[[F(x) for x in s['frames'][str(s['start'][i])]['B'][0]] for i in range(111)]
    K={i for i in range(111) if i==0 or sum(x*y for x,y in zip(roots[0],roots[i]))==0};L=K^set(range(8))
    need((len(K),len(L))==(57,49),'K0,L0 support');hub=w['hub'];facet=s['final'][111];ground=s['start'][111]
    def replay(ops):
        val={i:{i} for i in range(222)};loc=dict(enumerate(w['start']));born=set();count=Counter();moves=Counter();arr=[];erase=[];states=[];peak=0
        for t,o in enumerate(ops):
            op=o[0];count[op]+=1
            if op=='INIT':
                _,r,c=o;need(r in (222,223) and r not in val and r not in born,'owned lifecycle');born.add(r)
                if r==223:
                    need(c==hub and all(val[i]=={i} and loc[i]==hub for i in range(111)),'X restored before packet birth');need(val[222]==L,'L before Hub read')
                else:need(c==facet,'cache at F0')
                val[r]=set();loc[r]=c;peak=max(peak,len(val)-222)
            elif op=='MOVE':
                _,r,x,y=o;need(r in val and loc[r]==x and (x,y) in pairs,'actual MOVE source')
                need(fr[y]['dim']-fr[x]['dim']==(1 if r<222 else -1),'monotone paths');loc[r]=y;moves[r]+=1
                if r<111 and y==facet:arr.append(r)
                if r==223 and y==ground:need(val[r]==L,'first ground mode')
            elif op=='ADD':
                _,r,q,c=o;need(r!=q and r in val and q in val and loc[r]==loc[q]==c,'live cochart ADD');val[r]^=val[q]
                if 222 in val and loc.get(223)==facet:states.append({'event':t,'cache':sorted(val[222]),'packet':sorted(val[223]),'Y0':sorted(val[111])})
            elif op=='CLEAR':
                _,r,c=o;need(r>=222 and r in val and loc[r]==c,'owned cochart CLEAR');need(val[r]==(K if r==222 else L),'erasure/retained mode')
                erase.append({'field':r,'chart':c,'columns':sorted(val[r])});del val[r];del loc[r]
            else:raise ValueError('unknown opcode')
        need(set(val)==set(range(222)) and all(loc[i]==w['final'][i] for i in val),'final charts and lifetimes')
        need(all(val[i]=={i} for i in range(111)),'restore X');need(val[111]=={0,111},'arbitrary Y0 output')
        need(all(val[111+i]=={111+i} for i in range(1,111)),'110 unchanged Y')
        need(all(moves[i]==7 for i in range(222)) and moves[223]==8,'all path counts')
        need(count=={'MOVE':1562,'ADD':163,'INIT':2,'CLEAR':2},'full invoice');need(sorted(arr)==[7,8,9,12],'F0 arrivals')
        return {'counts':dict(count),'peak_owned':peak,'F0_X_arrivals':arr,'erasure_operands':erase,'exchange_states':states}
    result=replay(w['program']);ops=w['program'];controls=[]
    cuts=[('omit_local_deposit',next(i for i,o in enumerate(ops) if o[:2]==['ADD',222] and o[2]<111)),('omit_old_mode_retention',max(i for i,o in enumerate(ops) if o[:2]==['ADD',222])),('omit_Y_completion',next(i for i,o in enumerate(ops) if o[:3]==['ADD',111,222]))]
    cases=[(name,ops[:idx]+ops[idx+1:]) for name,idx in cuts]
    early=ops[:];idx=next(i for i,o in enumerate(ops) if o[:2]==['ADD',223]);o=early.pop(idx);early.insert(1,o);cases.append(('unavailable_early_Hub_read',early))
    for name,bad in cases:
        try:replay(bad)
        except ValueError as e:controls.append({'name':name,'rejected':True,'reason':str(e)})
        else:raise ValueError('accepted mutant '+name)
    out={'status':'PASS_INDEPENDENT_W0_PARTIAL_WORD','native_sha256':PIN,'word_sha256':hashlib.sha256(packed).hexdigest(),'input_columns':222,'charts_checked':len(fr),'nested_pairs':len(pairs),'result':result,'controls':controls,'scope':'Scalar-F2 logical maps and rational chart chronology. Physical phase/compiler, all-width native, other110 targets and complete supplier remain open.'}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:out[k] for k in ['status','word_sha256','charts_checked','nested_pairs','controls']}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
