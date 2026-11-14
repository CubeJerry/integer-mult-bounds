#!/usr/bin/env python3
"""Extract literal independent public planes, checking every arbitrary input."""
import argparse,copy,gzip,hashlib,json,importlib.util
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(c,m):
    if not c:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def span(vs):
    s={0}
    for v in vs:s|={x^v for x in s}
    return s
def add(a,b,c):
    r=a.copy()
    for j,v in b.items():
        z=r.get(j,F(0))+c*v
        if z:r[j]=z
        else:r.pop(j,None)
    return r
def replay(w,rows=None):
    rows={i:{i:F(1)}for i in range(224)}if rows is None else copy.deepcopy(rows)
    loc=dict(enumerate(w['initial']));S=list(map(span,w['frames']));bill=Counter();counts=Counter()
    for op in w['program']:
        ty,d=op[:2];need(0<=d<224,'every field is public');counts[ty]+=1
        if ty=='MOVE':
            a,b,owner=op[2:];need(owner is False and loc[d]==a,'actual raw source chart')
            need(S[b]<S[a]if w['plane']['inverse']else S[a]<S[b],'declared orientation')
            loc[d]=b;bill[abs(len(w['frames'][a])-len(w['frames'][b]))]+=1
        elif ty=='ADD':
            s,c,at=op[2:];need(0<=s<224 and d!=s and loc[d]==loc[s]==at,'genuine local source')
            need(F(c)in(F(1,2),F(-1,2)),'retained dyadic coefficient');rows[d]=add(rows[d],rows[s],F(c))
        else:raise ValueError('external or owned operation')
    need(loc==dict(enumerate(w['final'])),'all224 final charts')
    return rows,dict(bill),dict(counts)
def main(out):
    pins=json.loads((HERE/'SOURCES.json').read_text())['pins']
    for p,s in pins.items():need(sha((HERE/p).read_bytes())==s,'exact pin '+p)
    sources={name:json.loads(gzip.decompress((HERE/f'source/{name}.json.gz').read_bytes()))for name in('FORWARD','INVERSE')}
    f=sources['FORWARD'];d=f['logical_involution'];P=d['ports'];roles={k:{int(h):v for h,v in m.items()}for k,m in d['role_map'].items()}
    R={int(h):{int(j):F(v)for j,v in m.items()}for h,m in d['R_rows'].items()}
    out.mkdir(parents=True,exist_ok=True);words={};results={}
    for orientation,source in sources.items():
        phase=json.loads((HERE/f'source/{orientation}-PHASES.json').read_text())
        need(phase['word_sha256']==pins[f'source/{orientation}.json.gz']and phase['inherited_ordered_maps_used']==0,'complete authenticated physical recipes')
        recipes={(r['source'],r['target']):r for r in phase['recipes']}
        for plane,rr in(('XY',('X','Y')),('UV',('B','D'))):
            name=orientation.lower()+'-'+plane;old=[roles[r][h]for r in rr for h in P];new={v:i for i,v in enumerate(old)}
            need(len(new)==224,'two independent112-field banks')
            ops=[]
            for op in source['program']:
                if op[1]not in new:
                    need(op[0]!='ADD'or op[2]not in new,'no operation elsewhere reads this plane');continue
                q=copy.deepcopy(op);q[1]=new[q[1]]
                if q[0]=='ADD':need(q[2]in new,'no borrowed other-plane input');q[2]=new[q[2]]
                ops.append(q)
            w={'schema':'moonshot-S012-independent224-plane-v1','public':224,'owned_fields':0,'frames':source['frames'],
               'initial':[source['initial'][i]for i in old],'final':[source['final'][i]for i in old],'program':ops,
               'plane':{'name':name,'roles':list(rr),'ports':P,'local_to_original_fields':old,'inverse':orientation=='INVERSE',
                        'source_sha256':pins[f'source/{orientation}.json.gz'],'R_rows':d['R_rows'],
                        'all224_inputs_arbitrary':True,'no_shared_history_or_zero_input':True,
                        'old_native_schema_admission':False,'whole_caller_admission':False}}
            rows,bill,counts=replay(w);want={i:{i:F(1)}for i in range(224)};ix={h:i for i,h in enumerate(P)}
            sign=F(-1 if orientation=='INVERSE'else 1)
            for h in P:
                for j,c in R[h].items():
                    dest,src=(112+ix[h],ix[j])if plane=='XY'else(ix[j],112+ix[h])
                    want[dest]=add(want[dest],{src:F(1)},sign*c*(1 if plane=='XY'else -1))
            need(rows==want,'all224 arbitrary-input target columns')
            need(bill=={2:112,3:112,5:112,6:112}and counts=={'MOVE':448,'ADD':448},'literal half invoice')
            pairs={(op[2],op[3])for op in ops if op[0]=='MOVE'};need(len(pairs)==280 and pairs==set(recipes),'exact280 physical map cover')
            for a,b in pairs:
                r=recipes[a,b];need(r['source_frame']==w['frames'][a]and r['target_frame']==w['frames'][b],'actual signed charts')
                need(r['rank']==abs(len(w['frames'][a])-len(w['frames'][b])),'paid child rank')
            mutated=copy.deepcopy(w);op=next(op for op in mutated['program']if op[0]=='ADD');op[3]=str(-F(op[3]))
            need(replay(mutated)[0]!=want,'wrong source sign rejected')
            target=out/name;target.mkdir(exist_ok=True);raw=gzip.compress((json.dumps(w,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0)
            (target/'WORD.json.gz').write_bytes(raw)
            r={'status':'PASS_LITERAL_INDEPENDENT224_PLANE','name':name,'word_sha256':sha(raw),'all224_input_columns':True,
               'all12544_signal_coefficients':True,'all224_initial_and_final_charts':True,'movement_profile':bill,'counts':counts,
               'new_phase_recipes':0,'authenticated_ordered_phase_pairs':280,'no_owned_fields_or_helpers':True,
               'no_reads_or_writes_of_other_plane':True,'wrong_sign_control_rejected':True,'new_kappa':False}
            (target/'RESULT.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');words[name]=w;results[name]=r
    for plane in('XY','UV'):
        f=words['forward-'+plane];v=words['inverse-'+plane];identity={i:{i:F(1)}for i in range(224)}
        need(f['initial']==v['final']and f['final']==v['initial'],'literal inverse boundaries')
        need(replay(v,replay(f)[0])[0]==identity and replay(f,replay(v)[0])[0]==identity,'both literal plane compositions')
    result={'status':'PASS_FOUR_INDEPENDENT_PLANES','sources':results,'both_inverse_compositions_each_plane':True,
            'arbitrary_order_preserving_interleaving_allowed_by_disjoint_support':True,'source_pins':pins}
    (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({n:r['word_sha256']for n,r in results.items()},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'output');a=p.parse_args();main(a.output)
