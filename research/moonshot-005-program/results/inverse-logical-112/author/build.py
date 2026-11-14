#!/usr/bin/env python3
"""Literal reversible source, with an explicit descending public interface."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
SOURCE='c06724af5a2c414e62887ea78124d268cad2cabf500f9963ad5d0e9758c8a336'
PINS={'dynamic':'3845c44744ee0a05300bc237e9b9d10b45ca1272262f09f11e8a3ac2313a9e04',
 'engine':'045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e'}
def need(c,m):
    if not c:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def module(path,key):
    need(sha(path.read_bytes())==PINS[key],'exact engine pin '+key)
    s=importlib.util.spec_from_file_location('inverse112_'+key,path);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m);return m
def span(vs):
    S={0}
    for v in vs:S|={x^v for x in S}
    return S
def add(a,b,c):
    d=a.copy()
    for j,x in b.items():
        v=d.get(j,F(0))+c*x
        if v:d[j]=v
        else:d.pop(j,None)
    return d
def replay(word,ascending,rows=None,locations=None):
    n=word['public'];S=list(map(span,word['frames']));counts=Counter();moves=Counter()
    rows={i:{i:F(1)}for i in range(n)}if rows is None else copy.deepcopy(rows)
    loc=dict(enumerate(word['initial']))if locations is None else locations.copy()
    need(loc==dict(enumerate(word['initial'])),'literal input boundary')
    for op in word['program']:
        ty,d=op[:2];need(0<=d<n,'no owned or extra field');counts[ty]+=1
        if ty=='MOVE':
            a,b,owned=op[2:];need(owned is False and loc[d]==a,'genuine raw input location')
            need(S[a]<S[b]if ascending else S[b]<S[a],'declared strict public orientation')
            loc[d]=b;moves[abs(len(word['frames'][a])-len(word['frames'][b]))]+=1
        elif ty=='ADD':
            s,c,at=op[2:];need(d!=s and 0<=s<n and loc[d]==loc[s]==at,'actual cochart read')
            need(F(c)in(F(1,2),F(-1,2)),'literal dyadic half coefficients');rows[d]=add(rows[d],rows[s],F(c))
        else:raise ValueError('irreversible or unsupported source opcode')
    need(loc==dict(enumerate(word['final'])),'complete output boundary')
    return rows,loc,{'counts':dict(counts),'moves':dict(moves),'instructions':len(word['program']),'owned_fields':0,'lifetimes':0,'peak':0}
def main(args):
    raw=args.source.read_bytes();need(sha(raw)==SOURCE,'actual forward minimal word')
    old=json.loads(gzip.decompress(raw));need(old['public']==448 and old['owned_fields']==0,'source is genuinely owned-free')
    ops=[]
    for op in reversed(old['program']):
        if op[0]=='MOVE':need(op[4]is False,'no owned erasure premise');ops.append(['MOVE',op[1],op[3],op[2],False])
        elif op[0]=='ADD':ops.append(['ADD',op[1],op[2],str(-F(op[3])),op[4]])
        else:raise ValueError('source operation has no admitted literal inverse')
    d=old['logical_involution'];word={'schema':'moonshot-S012-full112-descending-inverse-source-v1','public':448,'owned_fields':0,
      'initial':old['final'],'final':old['initial'],'frames':old['frames'],'program':ops,
      'inverse_source':{'forward_sha256':SOURCE,'ports':d['ports'],'role_map':d['role_map'],'forward_R_rows':d['R_rows'],
        'public_orientation':'strictly descending','forward_ascent_only_schema_admitted':False,
        'requires_reversed_whole_job_boundary_interface':True,'all448_inputs_independent':True,'no_erasure_inverted':True,
        'physical_caller_admitted':False}}
    rows,loc,bill=replay(word,False);forward,floc,fbill=replay(old,True)
    n=448;P=d['ports'];role={k:{int(h):v for h,v in m.items()}for k,m in d['role_map'].items()};R={int(h):{int(j):F(x)for j,x in m.items()}for h,m in d['R_rows'].items()}
    want={i:{i:F(1)}for i in range(n)}
    for h in P:
        for j,c in R[h].items():
            want[role['Y'][h]]=add(want[role['Y'][h]],{role['X'][j]:F(1)},-c)
            want[role['B'][j]]=add(want[role['B'][j]],{role['D'][h]:F(1)},c)
    need(rows==want,'all448 independent inverse target columns')
    need(all(rows[role['Y'][h]].get(role['X'][j],F(0))+rows[role['B'][j]].get(role['D'][h],F(0))==0 for h in P for j in P),'all12544 adjoint entries')
    clean={i:{i:F(1)}for i in range(n)}
    a,_,_=replay(word,False,forward,floc);b,_,_=replay(old,True,rows,loc)
    need(a==b==clean,'literal forward/inverse composition in both orders')
    need(bill==fbill and Counter(bill['moves'])==Counter({2:224,3:224,5:224,6:224}),'exact same full source tariff')
    engine=module(args.engine,'engine');dyn=module(args.dynamic,'dynamic')
    try:dyn.replay(word,word['program'],engine);rejected=False
    except ValueError as err:rejected=str(err)=='nested MOVE'
    need(rejected,'retained ascent-only checker really rejects raw descents')
    controls=[]
    for name in('wrong_inverse_add_sign','wrong_inverse_raw_direction','wrong_inverse_input_boundary'):
        bad=copy.deepcopy(word)
        if name=='wrong_inverse_add_sign':
            op=next(op for op in bad['program']if op[0]=='ADD');op[3]=str(-F(op[3]))
        elif name=='wrong_inverse_raw_direction':
            op=next(op for op in bad['program']if op[0]=='MOVE');op[2],op[3]=op[3],op[2]
        else:bad['initial']=old['initial']
        try:rr,_,_=replay(bad,False);failed=rr!=want
        except ValueError:failed=True
        need(failed,'semantic inverse control '+name);controls.append(name)
    blob=gzip.compress((json.dumps(word,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0)
    args.output.mkdir(parents=True,exist_ok=True);(args.output/'WORD.json.gz').write_bytes(blob)
    result={'status':'PASS_EXACT_DESCENDING_OWNED_FREE_INVERSE','word_sha256':sha(blob),'forward_sha256':SOURCE,
      'all448_inputs_and_outputs_checked':True,'all12544_adjoint_entries_checked':True,'both_literal_compositions_identity':True,
      'source_bill':bill,'all896_raw_moves_strict_descents':True,'all896_adds_dyadic':True,
      'retained_ascent_only_checker_rejects':True,'reversed_boundary_interface_required':True,
      'no_erasure_or_clean_scratch_premise':True,'negative_controls':controls,'physical_caller_admitted':False,
      'scope':'Exact inverse map at reversed boundaries, same movement ranks. Descending raw interface is explicit; no claim of admission by the old ascent-only native schema or of a new kappa.'}
    (args.output/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--dynamic',type=Path,required=True)
    p.add_argument('--engine',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
