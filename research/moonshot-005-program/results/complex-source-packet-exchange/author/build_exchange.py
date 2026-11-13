#!/usr/bin/env python3
"""Actual funded complex packet/raw-B exchange, with restored ascending B."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def need(q,m):
    if not q:raise ValueError(m)
def main(a):
    ep=HERE/'source-evidence/extract_rail.py';need(sha(ep.read_bytes())=='7eba542316bfb1a0ae70fee8f2201b7b15abfcfa3cb59f84014f3331608ec372','exact source engine');sp=importlib.util.spec_from_file_location('complex_exchange_engine',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e);qb=(HERE/'source-evidence/rail-consumer.json.gz').read_bytes();need(sha(qb)=='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc','parent Q');q=json.loads(gzip.decompress(qb));s=e.load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',e.SOURCE_PIN);roles={int(k):v for k,v in q['source_role_map'].items()};host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};dual_public={roles[r] for pair in host.values() for r in pair};uf=list(range(400));current={i:i for i in range(400)};nodes=[]
    def find(x):
        while uf[x]!=x:uf[x]=uf[uf[x]];x=uf[x]
        return x
    def union(x,y):
        x,y=find(x),find(y)
        if x!=y:uf[y]=x
    for o in q['program']:
        typ,r=o[:2]
        if typ=='INIT':n=len(uf);uf.append(n);current[r]=n
        node=current[r];nodes.append(node)
        if typ in ['ADD','COPY']:union(node,current[o[2]])
        if typ=='CLEAR':del current[r]
    colors={}
    for i in range(400):colors.setdefault(find(i),set()).add('D' if i in dual_public else 'P')
    need(all(len(v)==1 for v in colors.values()),'original banks independent by real lifetime');color=lambda n:next(iter(colors.get(find(n),{'P'})));P=[(i,o) for i,o in enumerate(q['program']) if color(nodes[i])=='P'];D=[(i,o) for i,o in enumerate(q['program']) if color(nodes[i])=='D']
    begin=next(i for i,o in P if o==['INIT',451,127]);down=next(i for i,o in P if i>begin and o==['MOVE',451,127,3,True]);end=next(i for i,o in P if i>down and o==['CLEAR',451,3]);target=next((i,o) for i,o in D if o[0]=='MOVE' and o[1]<400 and o[3]==127 and len(q['frames'][o[2]])==8);bt,bo=target;carrier=bo[1];facet=bo[2];need((begin,down,end,bt,carrier,facet)==(3462,3528,3594,578,209,132),'exact source boundary and carrier')
    def renamed(o):
        z=list(o)
        if z[1]>=400:z[1]+=q['owned_fields']
        if z[0] in ['ADD','COPY'] and z[2]>=400:z[2]+=q['owned_fields']
        return z
    spaces=list(map(e.span,q['frames']));basis={i:{i:F(1)} for i in range(400)};before,bl,oldbill=e.run(q['program'],q['initial'],400,q['owned_fields'],spaces,basis);ops=[];rows=copy.deepcopy(basis);loc=dict(enumerate(q['initial']));cache=400+2*q['owned_fields']
    def emit(o):
        ops.append(copy.deepcopy(o));typ,r=o[:2]
        if typ=='INIT':need(r not in loc,'real cache lifetime');loc[r]=o[2];rows[r]={}
        elif typ=='CLEAR':need(loc[r]==o[2],'actual clear chart');del loc[r];del rows[r]
        elif typ=='MOVE':need(loc[r]==o[2],'actual move source');loc[r]=o[3]
        elif typ in ['ADD','COPY']:need(loc[r]==loc[o[2]]==o[4],'actual cochart');rows[r]=e.plus(rows[r],rows[o[2]],F(o[3]))
        elif typ=='SCALE':rows[r]={k:F(o[2])*v for k,v in rows[r].items()}
    for i,o in P:
        if i<begin:emit(o)
    need(all(loc[roles[j]]==127 and rows[roles[j]]==before[roles[j]] for j in s['live']),'ALL104 actual primal donors restoredHub before funded encoder')
    for i,o in D:
        if i<bt:emit(renamed(o))
    need(loc[carrier]==facet,'genuine ascending carrier paused after its last facet read');h=dict(rows[carrier]);encoder_begin=len(ops)
    for i,o in P:
        if begin<=i<down:emit(o)
    p0=dict(rows[451]);emit(['INIT',cache,127]);emit(['ADD',cache,451,'1',127]);exchange_begin=len(ops);emit(['MOVE',451,127,facet,True]);emit(['ADD',carrier,451,'1',facet]);emit(['ADD',451,carrier,'-1',facet]);need(rows[451]=={k:-v for k,v in h.items()} and rows[carrier]==e.plus(h,p0),'singular packet-through exchange(B+P,-B) exactly')
    emit(bo);need(loc[carrier]==127,'same old raw ascent used');restore_event=len(ops);emit(['ADD',carrier,cache,'-1',127]);need(rows[carrier]==h,'rawB exact old row restored before every old Hub use');emit(['CLEAR',cache,127]);emit(['MOVE',451,facet,3,True]);need(rows[451]=={k:-v for k,v in h.items()},'actual dirtyB packet arrives0')
    for i,o in P:
        if i>down:emit(o)
    for i,o in D:
        if i>bt:emit(renamed(o))
    w=copy.deepcopy(q);w['schema']='moonshot-S010-complex-funded-mode-exchange-v1';w['program']=ops;w['owned_fields']=2*q['owned_fields']+1;w['parent_consumer_provenance']=w.pop('consumer');w['mode_exchange']={'parent_sha256':sha(qb),'original_encoder_range':[begin,down],'original_packet_clear':end,'original_B_MOVE_event':bt,'carrier':carrier,'facet':facet,'packet':451,'Hub_controller_cache':cache,'encoder_begin':encoder_begin,'exchange_begin':exchange_begin,'restore_event':restore_event,'old_Hub_packet':p0,'old_facet_B_row':h,'new_packet_at0':{k:-v for k,v in h.items()},'local_matrix':[[1,1],[-1,0]],'packet_through_block':0,'packet_decoder_preserved_with_explicit_changed_payload':True,'old_forward_packet_delivery_restored':False}
    after,al,bill=e.run(ops,q['initial'],400,w['owned_fields'],spaces,basis);need(after==rows and al==loc==bl,'exact all400 final rows and charts, every owned lifetime retired');beta={}
    for i in range(down+1,end):
        o=q['program'][i];need(o[0]=='ADD' and o[2]==451 and o[4]==3,'literal old first-packet recipients');beta[o[1]]=beta.get(o[1],F(0))+F(o[3])
    shift=e.plus({k:-v for k,v in h.items()},p0,-1)
    for r in range(400):need(after[r]==e.plus(before[r],shift,beta.get(r,F(0))),'only exact rank1 mixed forward payload change at old recipients')
    # The change is an invertible output shear: h and p0 are functions of
    # unchanged X/B/D outputs, so information has not been erased.
    frozen={roles[j] for j in s['live']}|dual_public;expr,left=e.coordinate_expression(shift,[(r,before[r]) for r in sorted(frozen)]);need(not left,'explicit information inverse uses unchanged outputs only')
    dm={k:bill['moves'].get(k,0)-oldbill['moves'].get(k,0) for k in bill['moves'].keys()|oldbill['moves'].keys()};need({k:v for k,v in dm.items() if v}=={1:1,8:1,9:-1},'funded rank9 descent subdivided1+8 and no other movement');need(bill['lifetimes']==oldbill['lifetimes']+1 and bill['peak']<=43,'one genuine controller cache, full peak charged')
    controls=[]
    for kind in ['wrong_complex_exchange_sign','omit_Hub_carrier_restore']:
        z=copy.deepcopy(w);ix=exchange_begin+2 if kind=='wrong_complex_exchange_sign' else restore_event;z['program'][ix][3]='1' if kind=='wrong_complex_exchange_sign' else '0';ar,aa,_=e.run(z['program'],q['initial'],400,z['owned_fields'],spaces,basis);need(ar!=after,'exchange negative control rejected '+kind);controls.append({'name':kind,'event':ix,'rejected':True})
    ideal=lambda i:{roles[i]:F(1,2) if i not in host else F(1),roles[i+112]:F(1,2) if i not in host else F(1)};errors={i:e.plus(after[roles[i+112]],ideal(i),-1) for i in s['live']};oldpairs={(o[2],o[3]) for o in q['program'] if o[0]=='MOVE'};newpairs=sorted({(o[2],o[3]) for o in ops if o[0]=='MOVE'}-oldpairs)
    w['scope']='Actual singular complex packet/rawB exchange using funded independent carrier; all X/B/D endpoints unchanged, firstY rank1 mixed debt explicitly changed. Not full old Gram delivery or either strict supplier.';payload=(json.dumps(e.clean(w),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0);a.output.mkdir(parents=True,exist_ok=True);(a.output/'rail-exchange.json.gz').write_bytes(blob)
    result={'status':'PASS_ACTUAL_COMPLEX_FUNDED_SINGULAR_EXCHANGE','parent_sha256':sha(qb),'word_sha256':sha(blob),'payload_sha256':sha(payload),'input_directions':400,'bill':bill,'ordinary_increment':{k:bill['counts'].get(k,0)-oldbill['counts'].get(k,0) for k in bill['counts'].keys()|oldbill['counts'].keys()},'paid_move_increment':{1:1,8:1,9:-1},'new_chart_pairs':newpairs,'packet_through_block':0,'local_matrix':[[1,1],[-1,0]],'local_determinant':1,'actual_B_facet_row':h,'actual_old_P0':p0,'new_packet_at0':{k:-v for k,v in h.items()},'output_shear_inverse_expression_on_unchanged_outputs':expr,'new_original_input_forward_debt':sum(map(len,errors.values())),'old_forward_debt':4920,'all_X_B_D_outputs_exact_parent':True,'same_all400_final_charts':True,'negative_controls':controls,'scope':w['scope']+' Full forward source/acquisition, new mode decoder, compiler/precision and five foundations remain.'};(a.output/'RESULT.json').write_text(json.dumps(e.clean(result),sort_keys=True,indent=2)+'\n');print(json.dumps(e.clean({k:result[k] for k in ['status','word_sha256','bill','ordinary_increment','new_chart_pairs','new_original_input_forward_debt']}),indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
