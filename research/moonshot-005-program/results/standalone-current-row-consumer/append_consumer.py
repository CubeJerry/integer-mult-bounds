#!/usr/bin/env python3
"""Compose B7+24 original-column consumption with the pinned standalone Q."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def need(q,m):
    if not q:raise ValueError(m)

def main(a):
    ev=HERE/'source-evidence';ep=ev/'extract_rail.py'
    need(sha(ep.read_bytes())=='7eba542316bfb1a0ae70fee8f2201b7b15abfcfa3cb59f84014f3331608ec372','exact standalone replay engine')
    spec=importlib.util.spec_from_file_location('consumer_rail_exact',ep);e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
    qb=(ev/'rail-repaired.json.gz').read_bytes();cb=(ev/'B7-COORDINATE-CHOICE.json').read_bytes()
    need(sha(qb)=='90440c9115da1b98242113832c296faf314caf0ab7e0743119275dbfc372c9d2','exact standalone Q')
    need(sha(cb)=='24fc794c72895918eb810225a0b8c9f1d7d0266a70073e322861b084d05596b2','exact B7+24 choice')
    q=json.loads(gzip.decompress(qb));choice=json.loads(cb);J=choice['J']
    sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();need(sha(sb)==e.SOURCE_PIN,'exact native')
    s=json.loads(gzip.decompress(sb));roles={int(k):v for k,v in q['source_role_map'].items()}
    host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])}
    spaces=list(map(e.span,q['frames']));basis={i:{i:F(1)} for i in range(400)}
    before,loc,bill=e.run(q['program'],q['initial'],400,q['owned_fields'],spaces,basis)
    H=list(host);M={i:{j:F(i==j)+before[roles[host[i][0]]].get(roles[host[j][1]],F(0)) for j in H} for i in H}
    patch=[];temp=400;life=[]
    for j in J:
        d=roles[host[j][1]];facet=loc[d]
        need(before[d]=={d:F(1)} and facet==s['final'][host[j][1]],'authentic original D at actual final facet')
        start=len(patch);patch.extend([['INIT',temp,facet],['ADD',temp,d,'1',facet],['MOVE',temp,facet,127,True]])
        for i in H:
            if M[i][j]:
                b=roles[host[i][0]];need(loc[b]==127,'actual current B consumer at Hub')
                patch.append(['ADD',b,temp,str(-M[i][j]),127])
        patch.append(['CLEAR',temp,127]);life.append({'port':j,'field':temp,'facet':facet,'begin':len(q['program'])+start,'end':len(q['program'])+len(patch)})
    w=copy.deepcopy(q);w['program']+=patch;w['schema']='moonshot-S010-standalone-cyclic-column-consumer-v1'
    w['consumer']={'source_rail_sha256':sha(qb),'selected_return_ports':J,'begin':len(q['program']),'end':len(w['program']),'lifetimes':life,'one_reused_owned_slot':400,'formula':'subtract each actual residual column from all96 current B outputs'}
    after,al,newbill=e.run(w['program'],w['initial'],400,w['owned_fields'],spaces,basis)
    need(al==loc,'every400 final chart preserved');expected={}
    for i in H:
        delta={roles[host[j][1]]:-M[i][j] for j in J if M[i][j]};b=roles[host[i][0]]
        if delta:expected[b]=delta
    need(all(after[i]==e.plus(before[i],expected.get(i,{})) for i in range(400)),'all400 coefficients match entire actual-column subtraction')
    sys.path.insert(0,str(a.repo/'research/moonshot-005-program/results/joint-current-row-codes/review-star'))
    from engine import rank
    R=[[F(i==j)+after[roles[host[i][0]]].get(roles[host[j][1]],F(0)) for j in H] for i in H]
    completed=[i for i,row in zip(H,R) if not any(row)]
    need(rank(R)==58 and completed==choice['completed_original_B'],'rank58 and all24 intended original endpoints')
    need(newbill['instructions']==5242 and newbill['counts']['ADD']-bill['counts']['ADD']==370,'exact new rail instruction/ADD count')
    need(newbill['moves'][1]-bill['moves'][1]==31 and all(newbill['moves'].get(k,0)==v for k,v in bill['moves'].items() if k!=1),'exact31 new rank1 calls')
    need(newbill['peak']==29 and newbill['lifetimes']==402,'all402 lifetimes retired and original peak29 retained')
    need(all(after[i]==before[i] for i in range(400) if i not in expected),'every original forward and all other endpoint row unchanged')
    controls=[]
    for kind in ['omit_actual_column_entry','omit_original_D_copy','wrong_owned_flag']:
        z=copy.deepcopy(w);start=len(q['program'])
        if kind=='omit_actual_column_entry':ix=next(k for k in range(start,len(z['program'])) if z['program'][k][0]=='ADD' and z['program'][k][1]<400);z['program'][ix][3]='0'
        elif kind=='omit_original_D_copy':ix=start+1;z['program'][ix][3]='0'
        else:ix=start+2;z['program'][ix][4]=False
        try:
            rr,ll,_=e.run(z['program'],z['initial'],400,z['owned_fields'],spaces,basis);rejected=rr!=after or ll!=al;reason='all400-input endpoint map differs'
        except (AssertionError,ValueError) as ex:rejected=True;reason=str(ex)
        need(rejected,'actual rail negative control '+kind);controls.append({'name':kind,'event':ix,'rejected':True,'reason':reason})
    pb=(a.repo/'research/moonshot-005-program/results/joint-current-row-codes/cyclic-dual/WORD.json.gz').read_bytes();need(sha(pb)==e.CYCLIC_PIN,'exact chart inheritance parent')
    p=json.loads(gzip.decompress(pb));pairs={(o[2],o[3]):k for k,o in enumerate(p['program']) if o[0]=='MOVE'}
    maps=[{'new_rail_event':len(q['program'])+k,'from':o[2],'to':o[3],'rank':1,'inherited_parent_event':pairs.get((o[2],o[3]))} for k,o in enumerate(patch) if o[0]=='MOVE']
    need(all(x['inherited_parent_event'] is not None for x in maps),'all new maps literally inherited from pinned global source')
    payload=(json.dumps(w,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0)
    a.output.mkdir(parents=True,exist_ok=True);(a.output/'rail-consumer.json.gz').write_bytes(blob)
    receipt={'status':'PASS_EXACT_STANDALONE_B7_24_CONSUMER','source_rail_sha256':sha(qb),'native_source_sha256':e.SOURCE_PIN,'cyclic_chart_parent_sha256':e.CYCLIC_PIN,'choice_sha256':sha(cb),'word_sha256':sha(blob),'word_payload_sha256':sha(payload),'input_directions':400,'ordinary_bill':newbill,'ordinary_increment':{k:newbill['counts'].get(k,0)-bill['counts'].get(k,0) for k in newbill['counts'].keys()|bill['counts'].keys()},'selected_return_ports':J,'hosted_reverse_residual_rank':58,'completed_original_hosted_reverse_ports':completed,'new_move_profile':{1:31},'all400_coefficients_checked':True,'original_forward_rows_unchanged':True,'maps':maps,'negative_controls':controls,'complete_endpoint':False,'scope':'Exact400-input partial native Q extension; remaining forward/reverse duties, uniform suppliers, physical compiler and all five foundations remain.'}
    (a.output/'RAIL-CONSUMER-RESULT.json').write_text(json.dumps(e.clean(receipt),sort_keys=True,indent=2)+'\n')
    print(json.dumps(e.clean({k:receipt[k] for k in ['status','word_sha256','ordinary_bill','hosted_reverse_residual_rank','ordinary_increment']}),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
