#!/usr/bin/env python3
"""Two funded packet D ferries preserve every forward row and lower reverse rank."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def need(q,m):
    if not q:raise ValueError(m)
def main(a):
    ep=HERE/'source-evidence/extract_rail.py';need(sha(ep.read_bytes())=='7eba542316bfb1a0ae70fee8f2201b7b15abfcfa3cb59f84014f3331608ec372','pinned replay engine');sp=importlib.util.spec_from_file_location('funded_cross_engine',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e);qb=(HERE/'source-evidence/rail-consumer.json.gz').read_bytes();need(sha(qb)=='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc','exact parent Q');q=json.loads(gzip.decompress(qb));s=e.load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',e.SOURCE_PIN);roles={int(k):v for k,v in q['source_role_map'].items()};host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};H=list(host);dual_public={roles[r] for pair in host.values() for r in pair};uf=list(range(400));current={i:i for i in range(400)};nodes=[]
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
    need(all(len(v)==1 for v in colors.values()),'real lifetime primal/dual independence');color=lambda n:next(iter(colors.get(find(n),{'P'})));P=[(i,o) for i,o in enumerate(q['program']) if color(nodes[i])=='P'];D=[(i,o) for i,o in enumerate(q['program']) if color(nodes[i])=='D'];packets=[]
    for k,o in P:
        if o!=['INIT',451,127]:continue
        down=next(i for i,z in P if i>k and z==['MOVE',451,127,3,True]);end=next(i for i,z in P if i>down and z==['CLEAR',451,3]);left=[z for i,z in P if k<i<down];right=[z for i,z in P if down<i<end];need(all(z[0]=='ADD' and z[1]==451 and z[4]==127 for z in left) and all(z[0]=='ADD' and z[2]==451 and z[4]==3 for z in right),'actual packet encoder/decoder');packets.append({'begin':k,'down':down,'end':end,'alpha':{z[2]:F(z[3]) for z in left},'beta':{z[1]:F(z[3]) for z in right}})
    need(len(packets)==8,'eight literal funded Gram packets');selected=packets[:2];pairs=[{'target_port':1,'D_port':106},{'target_port':106,'D_port':1}];hoisted={}
    for t,p in zip(pairs,selected):
        b,d=host[t['target_port']][0],host[t['D_port']][1];t.update({'B':roles[b],'D':roles[d],'line':q['initial'][roles[b]],'facet':s['final'][d],'packet':p});touches=[(i,o) for i,o in enumerate(q['program']) if o[1]==t['D'] or o[0] in ['ADD','COPY'] and o[2]==t['D']];need(len(touches)==1 and touches[0][1]==['MOVE',t['D'],3,t['facet'],False],'D donor has one direct MOVE and no old reads');t['old_D_MOVE']=touches[0][0];hoisted[t['old_D_MOVE']]=touches[0][1];t['first_old_B_use']=next(i for i,o in enumerate(q['program']) if o[1]==t['B'] or o[0] in ['ADD','COPY'] and o[2]==t['B']);need(t['first_old_B_use'] in [530,534],'B producer untouched before first native ascent')
    need([(t['B'],t['D'],t['line'],t['facet'],t['old_D_MOVE']) for t in pairs]==[(209,394,1,226,4677),(298,305,99,129,4684)],'exact original roles/charts/hoist events')
    spaces=list(map(e.span,q['frames']));basis={i:{i:F(1)} for i in range(400)};before,bl,oldbill=e.run(q['program'],q['initial'],400,q['owned_fields'],spaces,basis);ops=[];lineage=[];rows=copy.deepcopy(basis);loc=dict(enumerate(q['initial']));events=[]
    def emit(o,old=None):
        ops.append(copy.deepcopy(o));lineage.append(old);typ,r=o[:2]
        if typ=='INIT':need(r not in loc,'real lifetime');loc[r]=o[2];rows[r]={}
        elif typ=='CLEAR':need(loc[r]==o[2],'actual clear');del loc[r];del rows[r]
        elif typ=='MOVE':need(loc[r]==o[2],'actual MOVE source');loc[r]=o[3]
        elif typ in ['ADD','COPY']:need(loc[r]==loc[o[2]]==o[4],'actual cochart');rows[r]=e.plus(rows[r],rows[o[2]],F(o[3]))
        elif typ=='SCALE':rows[r]={k:F(o[2])*v for k,v in rows[r].items()}
    for i,o in P:
        if i<40:emit(o,i)
    need(len(ops)==40 and all(loc[roles[j+112]]==3 for j in s['live']),'all eight original entry reads precede receiver compensation')
    precode_begin=len(ops)
    for t in pairs:
        need(rows[t['D']]=={t['D']:F(1)} and loc[t['D']]==3,'actual original D at0 for precode')
        for r,c in t['packet']['beta'].items():emit(['ADD',r,t['D'],str(-c),3])
    precode_end=len(ops);hoist_events=[]
    for old,o in sorted(hoisted.items()):hoist_events.append({'old_event':old,'new_event':len(ops),'op':o});emit(o,old)
    by_down={t['packet']['down']:t for t in pairs}
    for i,o in P:
        if i<40:continue
        if i not in by_down:emit(o,i);continue
        t=by_down[i];need(all(loc[roles[j]]==127 and rows[roles[j]]==before[roles[j]] for j in s['live']),'ALL actual first-X controllers are restoredHub and unchanged by D precode');need(loc[t['B']]==t['line'] and rows[t['B']]=={t['B']:F(1)},'boundary B producer original row at original initial line');need(rows[t['D']]=={t['D']:F(1)} and loc[t['D']]==t['facet'],'actual hoisted unchanged D donor at its original facet');controller=dict(rows[451]);event={'target_port':t['target_port'],'D_port':t['D_port'],'old_down':i,'begin':len(ops),'controller':controller}
        emit(['MOVE',451,127,t['facet'],True]);event['D_pickup']=len(ops);emit(['ADD',451,t['D'],'1',t['facet']]);emit(['MOVE',451,t['facet'],t['line'],True]);event['B_handoff']=len(ops);emit(['ADD',t['B'],451,'-1',t['line']]);emit(['MOVE',451,t['line'],3,True]);need(rows[451]==e.plus(controller,{t['D']:F(1)}),'packet preserves its full old controller plus the actual D donor');event['end']=len(ops);events.append(event)
    P_end=len(ops);need(len(loc)==400,'all primal owned lifetimes retire before native dual lifetime reuse')
    for j in s['live']:need(rows[roles[j]]==before[roles[j]] and rows[roles[j+112]]==before[roles[j+112]],'EVERY first-X/first-Y row exactly parent, including coupled half factors')
    for i,o in D:
        if i not in hoisted:emit(o,i)
    cleanup_begin=len(ops)
    for t,event in zip(pairs,events):need(rows[t['B']]==e.plus(e.plus(before[t['B']],event['controller'],-1),{t['D']:F(1)},-1),'entire native dual suffix transfers only the boundary producer disturbance to its own B endpoint')
    cleanup=[]
    for t in pairs:
        start=len(ops)
        for src,c in t['packet']['alpha'].items():need(loc[src]==127 and rows[src]==before[src],'cleanup source is actual unchanged restored first-X');emit(['ADD',t['B'],src,str(c),127])
        cleanup.append({'target_port':t['target_port'],'begin':start,'end':len(ops)})
    w=copy.deepcopy(q);w['schema']='moonshot-S010-funded-two-packet-cross-D-source-v1';w['program']=ops;w['parent_consumer_provenance']=w.pop('consumer');w['parent_event_of_output']=lineage;w['funded_cross_pair']={'parent_sha256':sha(qb),'ports':[1,106],'pairs':pairs,'precode_range':[precode_begin,precode_end],'hoisted_D_events':hoist_events,'packet_events':events,'primal_end':P_end,'controller_cleanup':cleanup,'all_old_Gram_modes_preserved':True,'B_cross_updates':[(1,106,-1),(106,1,-1)],'old_native_dual_operations_preserved_except_literal_D_hoist':True}
    after,al,bill=e.run(ops,q['initial'],400,q['owned_fields'],spaces,basis);need(after==rows and al==loc==bl,'full400-input exact replay, final charts and every owned retirement')
    for r in range(400):
        t=next((t for t in pairs if t['B']==r),None);want=e.plus(before[r],{t['D']:F(1)},-1) if t else before[r];need(after[r]==want,'ONLY promised two B cross-D endpoint changes on every input column')
    sys.path.insert(0,str(a.repo/'research/moonshot-005-program/results/joint-current-row-codes/review-star'));from engine import rank
    def residual(rr):return [e.plus(rr[roles[b]],{roles[b]:F(1),roles[d]:F(-1)},-1) for b,d in host.values()]
    oldR,newR=residual(before),residual(after);mr=lambda rr:rank([[r.get(k,F(0)) for k in range(400)] for r in rr]);need(mr(oldR)==58 and mr(newR)==57,'actual complete reverse residual58to57');i1,i2=H.index(1),H.index(106);need(newR[i1]=={k:-v for k,v in newR[i2].items()},'new actual residual rows1and106 are exact negatives');oldcomplete=[h for h,r in zip(H,oldR) if not r];newcomplete=[h for h,r in zip(H,newR) if not r];need(newcomplete==oldcomplete and len(newcomplete)==24,'all24 previous endpoint completions retained exactly')
    ideal=lambda i:{roles[i]:F(1) if i in host else F(1,2),roles[i+112]:F(1) if i in host else F(1,2)};debt=sum(len(e.plus(after[roles[i+112]],ideal(i),-1)) for i in s['live']);need(debt==4920,'original-coordinate forward debt unchanged4920, not silently discharged');dm={k:bill['moves'].get(k,0)-oldbill['moves'].get(k,0) for k in bill['moves'].keys()|oldbill['moves'].keys()};need({k:v for k,v in dm.items() if v}=={1:4,7:2,9:-2},'complete paid MOVE profile');need(bill['lifetimes']==402 and bill['peak']==29,'no new owned lifetime or peak')
    # A second, formal two-tag replay of the ORIGINAL dual word certifies the
    # whole suffix transfer, not merely an assumed identity of final B rows.
    tags=[10000,10001];tr={i:{} for i in range(400)};at=dict(enumerate(q['initial']));reads=[]
    for t,tag in zip(pairs,tags):tr[t['B']]={tag:F(1)}
    for old,o in D:
        typ,r=o[:2];source=tr.get(o[2],{}) if typ in ['ADD','COPY'] else {};dest=dict(tr.get(r,{}))
        if source or dest:reads.append({'old_event':old,'op':o,'destination_tags_before':dest,'source_tags_before':dict(source)})
        if typ=='INIT':at[r]=o[2];tr[r]={}
        elif typ=='CLEAR':del at[r];del tr[r]
        elif typ=='MOVE':need(at[r]==o[2],'tag source');at[r]=o[3]
        elif typ in ['ADD','COPY']:need(at[r]==at[o[2]]==o[4],'tag actual cochart');tr[r]=e.plus(tr[r],tr[o[2]],F(o[3]))
        elif typ=='SCALE':tr[r]={k:F(o[2])*v for k,v in tr[r].items()}
    transfer={r:v for r,v in tr.items() if v};need(transfer=={t['B']:{tag:F(1)} for t,tag in zip(pairs,tags)},'exact two formal suffix transfer columns, all other public outputs zero')
    controls=[]
    for kind in ['omit_Y0_precode','omit_actual_D_pickup','wrong_B_handoff_sign','omit_Hub_controller_cleanup','omit_D_hoist']:
        z=copy.deepcopy(w)
        if kind=='omit_Y0_precode':ix=precode_begin
        elif kind=='omit_actual_D_pickup':ix=events[0]['D_pickup']
        elif kind=='wrong_B_handoff_sign':ix=events[0]['B_handoff'];z['program'][ix][3]='1'
        elif kind=='omit_Hub_controller_cleanup':ix=cleanup_begin
        else:ix=hoist_events[0]['new_event'];z['program'].pop(ix)
        if kind not in ['wrong_B_handoff_sign','omit_D_hoist']:z['program'][ix][3]='0'
        try:ar,aa,_=e.run(z['program'],q['initial'],400,q['owned_fields'],spaces,basis);rejected=ar!=after or aa!=al
        except (AssertionError,ValueError):rejected=True
        need(rejected,'meaningful cross-pair negative control '+kind);controls.append({'name':kind,'event':ix,'rejected':True})
    oldpairs={(o[2],o[3]) for o in q['program'] if o[0]=='MOVE'};newpairs=sorted({(o[2],o[3]) for o in ops if o[0]=='MOVE'}-oldpairs);need(all(i in lineage or i in by_down for i in range(len(q['program']))),'every original event retained or exactly replaced packet descent');w['scope']='Actual funded cross-D pair, all forward rows and all original input information preserved; reverse rank57 with24 old completions. Global forward4569/4920 debt and remaining57-dimensional reverse response are unpaid; no complete supplier.';payload=(json.dumps(e.clean(w),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0);a.output.mkdir(parents=True,exist_ok=True);(a.output/'rail-cross-pair.json.gz').write_bytes(blob)
    result={'status':'PASS_ACTUAL_FUNDED_CROSS_D_PAIR_RANK57','parent_sha256':sha(qb),'native_sha256':e.SOURCE_PIN,'word_sha256':sha(blob),'payload_sha256':sha(payload),'input_directions':400,'bill':bill,'ordinary_increment':{k:bill['counts'].get(k,0)-oldbill['counts'].get(k,0) for k in bill['counts'].keys()|oldbill['counts'].keys()},'paid_move_increment':{1:4,7:2,9:-2},'old_reverse_rank':58,'new_reverse_rank':57,'completed_hosted_reverse_ports':newcomplete,'all_firstX_firstY_D_exact_parent':True,'all_old_Gram_modes_preserved':True,'original_forward_debt':4920,'current_a_forward_debt':4569,'primal_end':P_end,'packet_events':events,'precode_range':[precode_begin,precode_end],'hoisted_D_events':hoist_events,'controller_cleanup':cleanup,'suffix_tag_transfer':transfer,'suffix_tagged_reads':reads,'new_chart_pairs':newpairs,'negative_controls':controls,'scope':w['scope']+' Both strict suppliers and all five foundations remain.'};(a.output/'RESULT.json').write_text(json.dumps(e.clean(result),sort_keys=True,indent=2)+'\n');print(json.dumps(e.clean({k:result[k] for k in ['status','word_sha256','bill','ordinary_increment','new_reverse_rank','new_chart_pairs']}),indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
