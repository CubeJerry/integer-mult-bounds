#!/usr/bin/env python3
"""Construct a pure400 rail with the cyclic partial endpoint, plus exact controls."""
import argparse, gzip, hashlib, importlib.util, json
from pathlib import Path
from fractions import Fraction as F
spec=importlib.util.spec_from_file_location('rail_extraction',Path(__file__).resolve().parent/'extract_rail.py')
engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)
load,span,run,clean=engine.load,engine.span,engine.run,engine.clean
SOURCE_PIN,CYCLIC_PIN=engine.SOURCE_PIN,engine.CYCLIC_PIN

def backward_row(ops, target, start, end):
    grad = {target:F(1)}
    for op in reversed(ops[start:end]):
        typ, dst = op[:2]
        if typ in ('INIT','CLEAR'): grad.pop(dst,None)
        elif typ in ('ADD','COPY'):
            src,c = op[2:4]; a = grad.get(dst,F(0))*F(c)
            if a:
                grad[src] = grad.get(src,F(0))+a
                if not grad[src]: del grad[src]
        elif typ == 'SCALE' and dst in grad: grad[dst] *= F(op[2])
        elif typ != 'MOVE' and typ != 'SCALE': raise ValueError(typ)
    return grad

def main(args):
    ROOT,HERE=args.repo,args.output
    source = load(ROOT/'research/shared-wire-split-composition/data/final.json.gz',SOURCE_PIN)
    parent = load(ROOT/'research/moonshot-005-program/results/joint-current-row-codes/cyclic-dual/WORD.json.gz',CYCLIC_PIN)
    base = json.loads(gzip.decompress((HERE/'rail-base.json.gz').read_bytes()))
    audit = json.loads((HERE/'EXTRACTION.json').read_text())
    spaces = list(map(span, base['frames'])); end = len(parent['program'])-400
    rawmap = {int(k):v for k,v in parent['private_role_map'].items()}
    assert parent['program'][end:] == [['ADD',rawmap[r],r,'1',source['final'][r]] for r in sorted(rawmap)]
    # At cut400 each private field is an independent difference coordinate.
    taint = {i: i < 1480 for i in range(1880)}
    for op in parent['program'][400:end]:
        typ,dst=op[:2]
        if typ=='INIT': taint[dst]=False
        elif typ=='CLEAR': del taint[dst]
        elif typ in ('ADD','COPY'): taint[dst] |= taint[op[2]]
    contaminated=[i for i in range(1480,1880) if taint[i]]
    exact_common_checks={}
    for dst in contaminated:
        grad=backward_row(parent['program'],dst,400,end)
        bad={i:a for i,a in grad.items() if i<1480 and a}
        assert not bad, (dst,bad)
        exact_common_checks[dst]={'nonzero_common_derivatives':0,'private_support':len(grad)}
    ops=list(base['program']); added=[]; temp=base['public']
    for key,repair in audit['repairs'].items():
        dst=int(key); expr={int(k):F(v) for k,v in repair['expression'].items()}
        assert not repair['unrepresented'] and expr
        facet=repair['facet']; assert spaces[facet]<spaces[127] and len(spaces[facet])==256
        block=[['INIT',temp,127]]
        block += [['ADD',temp,r,str(c),127] for r,c in sorted(expr.items())]
        block += [['MOVE',temp,127,facet,True],['ADD',dst,temp,'1',facet],['CLEAR',temp,facet]]
        added.append({'source_role':repair['source_role'],'destination':dst,'facet':facet,'expression':expr,'ops':block}); ops += block
    word=dict(base);word['program']=ops;word.pop('parent_event',None)
    word['extraction_parent_sha256']=CYCLIC_PIN;word['repair_manifest']=clean(added)
    word['scope']='Exact standalone400-input cyclic partial difference map; no complete E endpoint or supplier.'
    actual,loc,bill=run(ops,word['initial'],400,word['owned_fields'],spaces,{i:{i:F(1)} for i in range(400)})
    qrows={i:({i-1480:F(1)} if i>=1480 else {}) for i in range(1880)}
    expected,eloc,_=run(parent['program'],parent['initial'],1880,parent['owned_fields'],spaces,qrows)
    assert all(not expected[r] for r in range(1480))
    assert all(actual[i]==expected[i+1480] and loc[i]==eloc[i+1480] for i in range(400))
    original_pairs={(op[2],op[3]) for op in source['program'] if op[0]=='MOVE'}
    parent_pairs={(op[2],op[3]) for op in parent['program'] if op[0]=='MOVE'}
    maps=[{'from':127,'to':x['facet'],'in_source':(127,x['facet']) in original_pairs,'in_parent':(127,x['facet']) in parent_pairs} for x in added]
    payload=(json.dumps(word,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0)
    (HERE/'rail-repaired.json.gz').write_bytes(blob); controls={}
    for j,rep in enumerate(added):
        bad=list(ops); start=len(base['program'])+sum(len(x['ops']) for x in added[:j])
        bad[start+1]=list(bad[start+1]);bad[start+1][3]=str(-F(bad[start+1][3]))
        mutant,_,_=run(bad,word['initial'],400,word['owned_fields'],spaces,{i:{i:F(1)} for i in range(400)})
        assert any(mutant[i]!=actual[i] for i in range(400));controls[str(rep['source_role'])]='wrong coefficient rejected'
    result={'status':'PASS_EXACT_STANDALONE_CYCLIC_RAIL','parent_source_pin':CYCLIC_PIN,'native_source_pin':SOURCE_PIN,'inputs':400,'exact_common_taint_candidates':contaminated,'exact_common_derivative_checks':exact_common_checks,'ordinary_bill':bill,'repair_count':len(added),'repair_rank_histogram':{'1':len(added)},'repairs':clean(added),'maps':maps,'word_sha256':hashlib.sha256(blob).hexdigest(),'word_payload_sha256':hashlib.sha256(payload).hexdigest(),'negative_controls':controls,'all_volume_scope':'Scalar rational identities tensor identity_V, conditional on chart/primitive contracts.','complete_native':False,'independent_review':'pending'}
    (HERE/'PURE-RAIL-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','inputs','repair_count','ordinary_bill','maps','word_payload_sha256','negative_controls']},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args())
