#!/usr/bin/env python3
"""Re-use genuine down-forward packets as mixed up-return packets."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(q,m):
    if not q:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def inverse(A):
    n=len(A);R=[list(r)+[F(i==j) for j in range(n)] for i,r in enumerate(A)]
    for k in range(n):
        z=next((i for i in range(k,n) if R[i][k]),None);need(z is not None,'nonsingular observation pivot')
        R[k],R[z]=R[z],R[k];c=R[k][k];R[k]=[x/c for x in R[k]]
        for i in range(n):
            if i!=k:
                c=R[i][k];R[i]=[x-c*y for x,y in zip(R[i],R[k])]
    return [r[n:] for r in R]

def main(a):
    need(1<=a.modes<=8,'one through eight actual packet cycles')
    ev=HERE/'source-evidence';eb=(ev/'extract_rail.py').read_bytes()
    need(sha(eb)=='7eba542316bfb1a0ae70fee8f2201b7b15abfcfa3cb59f84014f3331608ec372','exact400-input replay engine')
    spec=importlib.util.spec_from_file_location('packet_cycle_exact',ev/'extract_rail.py');e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
    qb=(ev/'rail-consumer.json.gz').read_bytes();need(sha(qb)=='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc','exact current Q pin')
    q=json.loads(gzip.decompress(qb));sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();need(sha(sb)==e.SOURCE_PIN,'native source pin');s=json.loads(gzip.decompress(sb))
    roles={int(k):v for k,v in q['source_role_map'].items()};host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};H=list(host)
    dual_public={roles[r] for pair in host.values() for r in pair};need(len(dual_public)==192,'distinct192 hosted dual public inputs')
    # Owned labels are split into real lifetimes before dependency colouring.
    uf=list(range(400));current={i:i for i in range(400)};nodes=[];lives=0
    def find(x):
        while uf[x]!=x:uf[x]=uf[uf[x]];x=uf[x]
        return x
    def union(x,y):
        x,y=find(x),find(y)
        if x!=y:uf[y]=x
    for op in q['program']:
        typ,r=op[:2]
        if typ=='INIT':need(r not in current,'real lifetime begins');node=len(uf);uf.append(node);current[r]=node;lives+=1
        node=current[r];nodes.append(node)
        if typ in ['ADD','COPY']:union(node,current[op[2]])
        if typ=='CLEAR':del current[r]
    need(set(current)==set(range(400)),'all old lifetimes retire')
    colors={}
    for i in range(400):colors.setdefault(find(i),set()).add('D' if i in dual_public else 'P')
    need(all(len(v)==1 for v in colors.values()),'no primal/hosted-dual raw bank mixing or alias')
    color=lambda node:next(iter(colors.get(find(node),{'P'})))
    primal=[(i,o) for i,o in enumerate(q['program']) if color(nodes[i])=='P']
    dual=[(i,o) for i,o in enumerate(q['program']) if color(nodes[i])=='D']
    spaces=list(map(e.span,q['frames']));basis={i:{i:F(1)} for i in range(400)}
    before,loc,oldbill=e.run(q['program'],q['initial'],400,q['owned_fields'],spaces,basis)
    reordered=[o for _,o in primal+dual];rr,rl,rb=e.run(reordered,q['initial'],400,q['owned_fields'],spaces,basis)
    need(rr==before and rl==loc and rb['moves']==oldbill['moves'] and rb['counts']==oldbill['counts'],'exact all400-input bank retiming with no new movement')
    packet=[]
    for i,o in primal:
        if o[0]!='MOVE' or o[2:4]!=[127,3]:continue
        r=o[1];start=max(k for k in range(i) if q['program'][k][:2]==['INIT',r]);end=next(k for k in range(i+1,len(q['program'])) if q['program'][k][:2]==['CLEAR',r])
        enc=q['program'][start+1:i];need(all(z[0]=='ADD' and z[1]==r and z[4]==127 for z in enc),'literal known forward nuisance at Hub')
        coeff={x:F(0) for x in s['live']}
        for z in enc:
            x=next((x for x in s['live'] if roles[x]==z[2]),None);need(x is not None,'all packet source values are actual first-X Hub rows');coeff[x]+=F(z[3])
        packet.append({'field':r,'begin':start,'down_event':i,'old_clear':end,'encoder':coeff,'old_encoder_ops':enc})
    need(len(packet)==8,'all eight exact original forward packet lifetimes')
    sys.path.insert(0,str(a.repo/'research/moonshot-005-program/results/joint-current-row-codes/review-star'))
    from engine import rank,root9
    roots={i:root9(s['frames'][s['initial'][i]][0]) for i in s['live']}
    G=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))/2
    need(all(sum(p['encoder'][i]*p['encoder'][j] for p in packet)/8==G(i,j) for i in s['live'] for j in s['live']),'actual eight packet forms reproduce full native Gram')
    need(rank([[p['encoder'][j] for j in H] for p in packet])==8,'hosted packet encoder rank8')
    U=[j for j in s['live'] if j not in host]
    coupled_rank=rank([[p['encoder'][j] for j in U] for p in packet]);need(coupled_rank==7,'actual coupled columns have rank7, not an orthogonal frame')
    selected=packet[:a.modes];J=q['consumer']['selected_return_ports']
    M=[[F(i==j)+before[roles[host[i][0]]].get(roles[host[j][1]],F(0)) for j in H] for i in H]
    echelon={}
    for vector in M:
        row={j:v for j,v in zip(H,vector) if v}
        while row:
            j=min(row);c=row[j]
            if j not in echelon:echelon[j]={k:v/c for k,v in row.items()};break
            row=e.plus(row,echelon[j],-c)
    frame=[5,56,65,69,77,96,100,103];remainders=[]
    for u in frame:
        row={j:G(u,j) for j in H if j not in J and G(u,j)}
        for j in sorted(echelon):
            if row.get(j):row=e.plus(row,echelon[j],-row[j])
        remainders.append(row)
    need(rank([[r.get(j,F(0)) for j in H] for r in remainders])==1,'actual Gram quotient has exactly one nuisance direction')
    j0=min(next(r for r in remainders if r));b0=min((k for k,r in enumerate(remainders) if r),key=lambda k:abs(remainders[k].get(j0,F(0))))
    up=[];up_modes=[];mode_data=[]
    for k,u in enumerate(frame):
        if k==b0:continue
        c=remainders[k].get(j0,F(0))/remainders[b0][j0]
        need(remainders[k]=={j:c*v for j,v in remainders[b0].items() if c*v},'all quotient rows exactly proportional')
        mode_data.append((abs(c),u,c))
    for _,u,c in sorted(mode_data):
        up.append({j:G(u,j)-c*G(frame[b0],j) for j in H});up_modes.append({'root':u,'reference_root':frame[b0],'coefficient':str(c)})
    up.append({j:G(frame[b0],j) for j in H});up_modes.append({'root':frame[b0],'reference_root':None,'coefficient':'0'})
    up,up_modes=up[:a.modes],up_modes[:a.modes];up_ports=[m['root'] for m in up_modes]
    first=400+q['owned_fields'];caches={k:first+k for k in range(a.modes)}
    by_clear={p['old_clear']:k for k,p in enumerate(selected)};core=[];events=[]
    for old,op in primal:
        if old not in by_clear:core.append(copy.deepcopy(op));continue
        k=by_clear[old];p=selected[k];r=p['field'];begin=len(core)
        for j in H:
            if up[k][j]:core.append(['ADD',r,roles[host[j][1]],str(up[k][j]),3])
        core.append(['MOVE',r,3,127,True])
        for z in p['old_encoder_ops']:core.append(['ADD',r,z[2],str(-F(z[3])),127])
        core.extend([['INIT',caches[k],127],['ADD',caches[k],r,'1',127],['CLEAR',r,127]])
        events.append({'mode':k,'old_clear':old,'begin':begin,'end':len(core),'cache':caches[k],'true_original_forward_encoder':p['old_encoder_ops']})
    clear_to_port={x['end']-1:x['port'] for x in q['consumer']['lifetimes']}
    for old,op in dual:
        if old in clear_to_port:
            j=clear_to_port[old];need(op==['CLEAR',400,127],'actual original-return lifetime end')
            for k,p in enumerate(selected):
                if up[k][j]:core.append(['ADD',caches[k],400,str(-up[k][j]),127])
        core.append(copy.deepcopy(op))
    N=[{roles[host[j][1]]:up[k][j] for j in H if j not in J and up[k][j]} for k in range(a.modes)]
    # A typed observable probe verifies all cache rows without weakening the
    # inherited interpreter's requirement that every owned lifetime retire.
    probe_B=[5,56,69,100,65,77,96,103][:a.modes];probe=list(core)
    for k,j in enumerate(probe_B):probe.append(['ADD',roles[host[j][0]],caches[k],'1',127])
    probe.extend([['CLEAR',r,127] for r in caches.values()])
    observed,ol,pbill=e.run(probe,q['initial'],400,q['owned_fields']+a.modes,spaces,basis)
    for i in range(400):
        k=next((k for k,j in enumerate(probe_B) if roles[host[j][0]]==i),None)
        want=e.plus(before[i],N[k]) if k is not None else before[i]
        need(observed[i]==want and ol[i]==loc[i],'each actual mixed-return cache equals its pure hosted-D formula on all400 inputs')
    M=[[F(i==j)+before[roles[host[i][0]]].get(roles[host[j][1]],F(0)) for j in H] for i in H]
    all_NN=[[n.get(roles[host[j][1]],F(0)) for j in H] for n in N];need(rank(all_NN)==a.modes,'independent actual observations after selected-coordinate subtraction')
    useful=min(a.modes,7);NN=all_NN[:useful]
    print(json.dumps({'current_residual_rank':rank(M),'actual_observation_rank':rank(all_NN),'stack_rank':rank(M+all_NN),'rank_credit':rank(M)+rank(all_NN)-rank(M+all_NN)}),flush=True)
    need(rank(M+NN)==rank(M),'actual observation rows belong to current residual rowspace')
    candidates=sorted(range(len(H)),key=lambda t:(sum(bool(r[t]) for r in M)!=1,t));T=[]
    for t in candidates:
        if rank([[r[z] for z in T+[t]] for r in NN])>len(T):T.append(t)
        if len(T)==useful:break
    need(len(T)==useful,'real observation pivot columns');P=inverse([[r[t] for t in T] for r in NN])
    C=[[sum(M[i][t]*P[k][l] for k,t in enumerate(T)) for l in range(useful)] for i in range(len(H))]
    finish=[]
    for i,j in enumerate(H):
        for k,c in enumerate(C[i]):
            if c:finish.append(['ADD',roles[host[j][0]],caches[k],str(-c),127])
    finish.extend([['CLEAR',r,127] for r in caches.values()])
    w=copy.deepcopy(q);w['schema']='moonshot-S010-source-cotangent-packet-cycle-v1';w['program']=core+finish;w['owned_fields']+=a.modes
    w['parent_column_consumer_provenance']=w.pop('consumer')
    w['packet_cycles']={'source_rail_sha256':sha(qb),'modes':a.modes,'useful_modes':useful,'upward_Gram_ports':up_ports,'upward_mode_basis':up_modes,'events':events,'primal_parent_events':[i for i,_ in primal],'dual_parent_events':[i for i,_ in dual],'retiming_input_banks':{'primal':208,'hosted_dual':192},'coupled_packet_column_rank':coupled_rank,'observations':N,'selected_coordinate_strip_ports':J,'pivot_ports':[H[t] for t in T],'consumer_coefficients':C,'consumer_begin':len(core),'actual_forward_offdiagonal_acquisition_still_incomplete':True,'eight_coupled_entry_calls_retained':True}
    after,al,bill=e.run(w['program'],w['initial'],400,w['owned_fields'],spaces,basis)
    need(al==loc,'all400 final charts preserved')
    expected={}
    for i,j in enumerate(H):
        delta={}
        for k,c in enumerate(C[i]):delta=e.plus(delta,N[k],-c)
        if delta:expected[roles[host[j][0]]]=delta
    need(all(after[i]==e.plus(before[i],expected.get(i,{})) for i in range(400)),'all400 coefficients equal exact mixed-packet column projection')
    R=[[F(i==j)+after[roles[host[i][0]]].get(roles[host[j][1]],F(0)) for j in H] for i in H]
    wantR=[[M[i][j]-sum(C[i][k]*NN[k][j] for k in range(useful)) for j in range(len(H))] for i in range(len(H))]
    need(R==wantR and rank(R)==58-useful,'exact actual reverse rank reduction')
    completed=[i for i,row in zip(H,R) if not any(row)];oldcomplete=[i for i,row in zip(H,M) if not any(row)]
    need(set(oldcomplete)<=set(completed),'every earlier original endpoint completion retained')
    dm={k:bill['moves'].get(k,0)-oldbill['moves'].get(k,0) for k in bill['moves'].keys()|oldbill['moves'].keys()};dm={k:v for k,v in dm.items() if v}
    need(dm=={9:a.modes},'all new up-return calls charged exactly')
    need(bill['peak']<=43 and bill['lifetimes']==oldbill['lifetimes']+a.modes,'all true lifetimes and peak charged')
    scalar_denominators=sorted({F(o[3] if o[0] in ['ADD','COPY'] else o[2]).denominator for o in w['program'] if o[0] in ['ADD','COPY','SCALE']})
    if a.modes==1:need(all(d&(d-1)==0 for d in scalar_denominators),'one-cycle source keeps purely dyadic scalar coefficients')
    controls=[]
    def mutant(name,predicate,change,lo=0,hi=None):
        z=copy.deepcopy(w);ix=next(i for i in range(lo,hi or len(z['program'])) if predicate(z['program'][i]));change(z['program'][ix])
        try:
            ar,aa,_=e.run(z['program'],z['initial'],400,z['owned_fields'],spaces,basis);rejected=ar!=after or aa!=al;reason='actual400-input output differs'
        except (AssertionError,ValueError) as ex:rejected=True;reason=str(ex)
        need(rejected,'packet mutant rejected '+name);controls.append({'name':name,'event':ix,'rejected':True,'reason':reason})
    ev0=events[0]
    mutant('missing_actual_D_encoder',lambda o:o[0]=='ADD' and o[1]==selected[0]['field'] and o[4]==3,lambda o:o.__setitem__(3,'0'),ev0['begin'],ev0['end'])
    mutant('missing_known_forward_nuisance_cancellation',lambda o:o[0]=='ADD' and o[1]==selected[0]['field'] and o[4]==127,lambda o:o.__setitem__(3,'0'),ev0['begin'],ev0['end'])
    mutant('wrong_up_return_ownership',lambda o:o[0]=='MOVE' and o[2:4]==[3,127],lambda o:o.__setitem__(4,False),ev0['begin'],ev0['end'])
    mutant('omit_selected_coordinate_strip',lambda o:o[0]=='ADD' and o[1] in caches.values() and o[2]==400,lambda o:o.__setitem__(3,'0'))
    mutant('omit_real_packet_consumer',lambda o:o[0]=='ADD',lambda o:o.__setitem__(3,'0'),len(core),len(core)+len(finish))
    firstD=next(j for j in H if up[0][j]);oldclear=selected[0]['old_clear'];bad=q['program'][:oldclear]+[['ADD',selected[0]['field'],roles[host[firstD][1]],str(up[0][firstD]),3]]
    try:e.run(bad,q['initial'],400,q['owned_fields'],spaces,basis);raise ValueError('stale original ordering was accepted')
    except AssertionError:controls.append({'name':'without_bank_retiming_D_has_already_departed','rejected':True,'reason':'actual source cochart failure before observation read'})
    payload=(json.dumps(e.clean(w),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0);a.output.mkdir(parents=True,exist_ok=True);(a.output/'rail-cycle.json.gz').write_bytes(blob)
    r={'status':'PASS_ACTUAL_COTANGENT_PACKET_CYCLE','source_rail_sha256':sha(qb),'native_sha256':e.SOURCE_PIN,'word_sha256':sha(blob),'word_payload_sha256':sha(payload),'input_directions':400,'cycles':a.modes,'useful_modes':useful,'upward_Gram_ports':up_ports,'upward_mode_basis':up_modes,'scalar_denominators':scalar_denominators,'primal_operations':len(primal),'dual_operations':len(dual),'bank_retiming_all400_coefficients_identical':True,'actual_observation_rows':N,'observation_rank':a.modes,'observation_rowspace_intersection_rank':useful,'hosted_reverse_residual_rank':rank(R),'completed_original_hosted_reverse_ports':completed,'bill':bill,'ordinary_increment':{k:bill['counts'].get(k,0)-oldbill['counts'].get(k,0) for k in bill['counts'].keys()|oldbill['counts'].keys()},'new_paid_move_profile':dm,'actual_coupled_packet_columns_rank':coupled_rank,'eight_coupled_entry_calls_retained':True,'forward_rows_unchanged':True,'negative_controls':controls,'scope':'Actual400-input source packet reuse and mixed current-row consumption. Full forward offdiagonal acquisition remains incomplete; no absorption of coupled8, no complete supplier or kappa. All five foundations remain.'}
    (a.output/'RESULT.json').write_text(json.dumps(e.clean(r),sort_keys=True,indent=2)+'\n');print(json.dumps(e.clean({k:r[k] for k in ['status','word_sha256','cycles','hosted_reverse_residual_rank','bill','ordinary_increment','primal_operations','dual_operations']}),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--modes',type=int,default=1);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
