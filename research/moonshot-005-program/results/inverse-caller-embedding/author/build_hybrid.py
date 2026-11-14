#!/usr/bin/env python3
"""Actual448-input words with independently oriented disjoint source planes."""
import argparse,copy,gzip,hashlib,json
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
def replay(w):
    rows={i:{i:F(1)}for i in range(448)};loc=dict(enumerate(w['initial']));S=list(map(span,w['frames']));bill=Counter();counts=Counter()
    inverse=set(w['hybrid_source']['inverse_roles'])
    for op in w['program']:
        ty,d=op[:2];need(0<=d<448,'all public');counts[ty]+=1
        if ty=='MOVE':
            a,b,owner=op[2:];need(owner is False and loc[d]==a,'literal raw source')
            need(S[b]<S[a]if d in inverse else S[a]<S[b],'declared plane orientation')
            loc[d]=b;bill[abs(len(w['frames'][a])-len(w['frames'][b]))]+=1
        elif ty=='ADD':
            s,c,at=op[2:];need(d!=s and loc[d]==loc[s]==at and(d in inverse)==(s in inverse),'true disjoint-plane cochart')
            need(F(c)in(F(1,2),F(-1,2)),'dyadic source coefficient');rows[d]=add(rows[d],rows[s],F(c))
        else:raise ValueError('nonreversible source instruction')
    need(loc==dict(enumerate(w['final'])),'all448 endpoints')
    return rows,dict(bill),dict(counts)
def main(out):
    pins=json.loads((HERE/'SOURCES.json').read_text())['pins']
    for p,s in pins.items():need(sha((HERE/p).read_bytes())==s,'source pin '+p)
    f=json.loads(gzip.decompress((HERE/'source/FORWARD.json.gz').read_bytes()));iv=json.loads(gzip.decompress((HERE/'source/INVERSE.json.gz').read_bytes()))
    d=f['logical_involution'];P=d['ports'];roles={k:{int(h):v for h,v in m.items()}for k,m in d['role_map'].items()}
    xy=set(roles['X'].values())|set(roles['Y'].values());uv=set(roles['B'].values())|set(roles['D'].values())
    need(xy.isdisjoint(uv)and xy|uv==set(range(448)),'two independent224-field planes')
    R={int(h):{int(j):F(v)for j,v in m.items()}for h,m in d['R_rows'].items()};known={}
    for name,w in(('FORWARD',f),('INVERSE',iv)):
        p=json.loads((HERE/f'source/{name}-PHASES.json').read_text());need(p['word_sha256']==pins[f'source/{name}.json.gz'],'phase word pin')
        need(p['inherited_ordered_maps_used']==0,'complete explicit source map cover')
        for r in p['recipes']:
            need(r['source_frame']==w['frames'][r['source']]and r['target_frame']==w['frames'][r['target']],'signed recipe actual charts')
            known[r['source'],r['target']]=(name,r['rank'])
    need(len(known)==560,'all two-orientation signed recipes')
    out.mkdir(parents=True,exist_ok=True);results={}
    for name,reverse in(('inverse-XY',xy),('inverse-UV',uv)):
        program=[copy.deepcopy(op)for op in iv['program']if op[1]in reverse]+[copy.deepcopy(op)for op in f['program']if op[1]not in reverse]
        w={'schema':'moonshot-S012-full112-hybrid-plane-source-v1','public':448,'owned_fields':0,'frames':f['frames'],
          'initial':[f['final'][i]if i in reverse else f['initial'][i]for i in range(448)],
          'final':[f['initial'][i]if i in reverse else f['final'][i]for i in range(448)],'program':program,
          'hybrid_source':{'variant':name,'inverse_roles':sorted(reverse),'ports':P,'role_map':d['role_map'],
            'forward_R_rows':d['R_rows'],'forward_sha256':pins['source/FORWARD.json.gz'],'inverse_sha256':pins['source/INVERSE.json.gz'],
            'uniform_forward_raw_schema_admitted':False,'standard_same_A_HOST2_claimed':False,'physical_caller_admitted':False}}
        rows,bill,counts=replay(w);want={i:{i:F(1)}for i in range(448)}
        for h in P:
            for j,c in R[h].items():
                want[roles['Y'][h]]=add(want[roles['Y'][h]],{roles['X'][j]:F(1)},-c if reverse==xy else c)
                want[roles['B'][j]]=add(want[roles['B'][j]],{roles['D'][h]:F(1)},c if reverse==uv else -c)
        need(rows==want,'all448 arbitrary-input hybrid target columns')
        need(bill=={2:224,3:224,5:224,6:224}and counts=={'MOVE':896,'ADD':896},'unchanged complete source invoice')
        pairs={(op[2],op[3])for op in program if op[0]=='MOVE'};need(pairs==set(known),'all560 actual signed pairs covered')
        need(all(known[a,b][1]==abs(len(w['frames'][a])-len(w['frames'][b]))for a,b in pairs),'all inverse/forward child ranks retained')
        same=sum(rows[roles['Y'][h]].get(roles['X'][j],F(0))==rows[roles['B'][j]].get(roles['D'][h],F(0))for h in P for j in P)
        need(same==12544,'honest same-sign hybrid coefficient relation')
        bad=copy.deepcopy(w);op=next(op for op in bad['program']if op[0]=='ADD');op[3]=str(-F(op[3]));need(replay(bad)[0]!=want,'wrong mixed-source sign rejected')
        raw=gzip.compress((json.dumps(w,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0);target=out/name;target.mkdir(exist_ok=True);(target/'WORD.json.gz').write_bytes(raw)
        r={'status':'PASS_ACTUAL_INDEPENDENTLY_ORIENTED_PLANES','variant':name,'word_sha256':sha(raw),'all448_independent_inputs_and_endpoints':True,
          'all12544_hybrid_coefficient_entries':True,'old_opposite_adjoint_contract_not_claimed':True,'movement_profile':bill,'counts':counts,
          'raw_ascending_moves':448,'raw_descending_moves':448,'signed_phase_pairs_covered':560,'new_phase_recipe_needed':0,
          'owned_fields':0,'wrong_mixed_sign_rejected':True,'standard_same_A_HOST2':False,'whole_caller_or_new_kappa':False}
        (target/'RESULT.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');results[name]=r
    (out/'HYBRIDS.json').write_text(json.dumps({'status':'PASS_BOTH_ACTUAL_MIXED_BOUNDARY_WORDS','sources':results,'source_pins':pins},sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:{'word':v['word_sha256'],'profile':v['movement_profile']}for k,v in results.items()},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'output');a=p.parse_args();main(a.output)
