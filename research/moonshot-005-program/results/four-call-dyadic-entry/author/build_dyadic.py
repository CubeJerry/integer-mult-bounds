#!/usr/bin/env python3
"""Replace8 coupled entry calls by4 true rank1 calls and dyadic Y coding."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def need(q,m):
    if not q:raise ValueError(m)
def main(a):
    ep=HERE/'source-evidence/extract_rail.py';need(sha(ep.read_bytes())=='7eba542316bfb1a0ae70fee8f2201b7b15abfcfa3cb59f84014f3331608ec372','exact400-input source engine')
    sp=importlib.util.spec_from_file_location('dyadic_entry_exact',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
    qb=(HERE/'source-evidence/rail-consumer.json.gz').read_bytes();need(sha(qb)=='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc','exact parent Q')
    q=json.loads(gzip.decompress(qb));sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();need(sha(sb)==e.SOURCE_PIN,'native source');s=json.loads(gzip.decompress(sb));roles={int(k):v for k,v in q['source_role_map'].items()}
    U=[17,19,30,38,40,47,52,60];u={17:F(1),19:F(-1),38:F(-1),40:F(1)};yp=roles[129]
    oldentry=[]
    for i in U:
        L=s['initial'][i];oldentry.extend([['INIT',400,3],['ADD',400,roles[i+112],'1',3],['MOVE',400,3,L,True],['ADD',roles[i],400,'-1',L],['CLEAR',400,L]])
    need(q['program'][:40]==oldentry,'literal eight-entry parent convention')
    prefix=[]
    for i,c in u.items():
        L=s['initial'][i];prefix.extend([['INIT',400,3],['ADD',400,yp,'1',3],['MOVE',400,3,L,True],['ADD',roles[i],400,str(-c),L],['CLEAR',400,L]])
    for i in U:
        if i!=17:prefix.append(['SCALE',roles[i+112],'1/2',3])
    for i,c in u.items():
        if i!=17:prefix.append(['ADD',roles[i+112],yp,str(c/2),3])
    need(len(prefix)==30,'four packets plus seven half-scales and three pivot reads')
    w=copy.deepcopy(q);w['program']=prefix+q['program'][40:];w['schema']='moonshot-S010-four-call-dyadic-coupled-preconditioner-v1';w['parent_rail_sha256']=sha(qb)
    for k in ['begin','end']:w['consumer'][k]-=10
    for lifetime in w['consumer']['lifetimes']:
        for k in ['begin','end']:lifetime[k]-=10
    w['dyadic_entry']={'coupled_ports':U,'kernel_vector':[1,-1,0,-1,1,0,0,0],'affected_X_ports':list(u),'pivot_Y_port':17,'prefix_end':30,'a':'x-u*y17','physical_c':'(I+u*e17^T)y/2','required_coupled_reverse_correction':'(I-u*e17^T)y','rank_correction':7,'all_coupled_Y_stay_at0_for_every_forward_packet':True,'entry_rank1_calls':4,'observer_for_correction':'NOT_GRANTED'}
    spaces=list(map(e.span,q['frames']));basis={i:{i:F(1)} for i in range(400)}
    before,bl,oldbill=e.run(q['program'],q['initial'],400,q['owned_fields'],spaces,basis);after,al,bill=e.run(w['program'],w['initial'],400,w['owned_fields'],spaces,basis)
    # Mathematical parent-input substitution; the actual new prefix above
    # realizes the corresponding post-entry rows at their genuine charts.
    T=copy.deepcopy(basis)
    for i in U:
        x,y=roles[i],roles[i+112];c=u.get(i,F(0))
        T[y]={y:F(1,2)};T[y]=e.plus(T[y],{yp:F(1)},c/2)
        T[x]=e.plus({x:F(1)},{y:F(1)},F(1,2));T[x]=e.plus(T[x],{yp:F(1)},-c/2)
    expected,el,_=e.run(q['program'],q['initial'],400,q['owned_fields'],spaces,T)
    need(after==expected and al==el==bl,'all400 coefficients equal exact invertible parent precomposition')
    for i in U:
        c=u.get(i,F(0));want=e.plus({roles[i]:F(1)},{yp:F(1)},-c)
        need(after[roles[i]]==want,'actual coupled X row x-u*y17')
    host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])}
    for x,y in host.values():need(after[roles[x]]==before[roles[x]] and after[roles[y]]==before[roles[y]],'every hosted reverse/D row unchanged')
    sys.path.insert(0,str(a.repo/'research/moonshot-005-program/results/joint-current-row-codes/review-star'))
    from engine import rank,root9
    pre,pl,_=e.run(prefix,q['initial'],400,q['owned_fields'],spaces,basis)
    for i in U:
        c=u.get(i,F(0));x,y=roles[i],roles[i+112]
        need(pl[x]==q['initial'][x] and pl[y]==3,'no raw X or Y route changed before forward reads')
        need(e.plus(pre[y],pre[yp],-c/2)=={y:F(1,2)},'actual physical c=(I+u*vT)y/2')
        need(e.plus({k:2*v for k,v in pre[y].items()},pre[yp],-c)=={y:F(1)},'input inverse y=2c-u*c17')
        need(e.plus(pre[x],pre[yp],c)=={x:F(1)},'input inverse x=a+u*c17')
    ideal=lambda i: {roles[i]:F(1,2) if i in U else F(1),roles[i+112]:F(1,2) if i in U else F(1)}
    oldH={};oldErrors={};newErrors={}
    for i in s['live']:
        oldErrors[i]=e.plus(before[roles[i+112]],ideal(i),-1);newErrors[i]=e.plus(after[roles[i+112]],ideal(i),-1)
        row={j:oldErrors[i].get(roles[j],F(0)) for j in s['live']};oldH[i]={j:v for j,v in row.items() if v}
        old_rebuilt={};new_rebuilt={}
        for j,c in oldH[i].items():
            av={roles[j]:F(1)}
            if j in U:av=e.plus(av,{roles[j+112]:F(1)},-1)
            old_rebuilt=e.plus(old_rebuilt,av,c)
            av=e.plus({roles[j]:F(1)},{yp:F(1)},-u.get(j,F(0)))
            new_rebuilt=e.plus(new_rebuilt,av,c)
        need(old_rebuilt==oldErrors[i] and new_rebuilt==newErrors[i],'actual forward error equals unchanged H times actual new a')
    old_count=sum(len(r) for r in oldErrors.values());new_count=sum(len(r) for r in newErrors.values());basis_count=sum(len(r) for r in oldH.values())
    need(basis_count==4569 and old_count==4920,'pinned old forward residual census')
    reverse=[]
    for i,(x,y) in host.items():reverse.append(e.plus(after[roles[x]],{roles[x]:F(1),roles[y]:F(-1)},-1))
    host_rank=rank([[r.get(k,F(0)) for k in range(400)] for r in reverse]);need(host_rank==58,'hosted reverse rank unchanged')
    coupled=[]
    for i in U:coupled.append(e.plus(after[roles[i]],{roles[i]:F(1),roles[i+112]:F(-1)},-1))
    coupled_rank=rank([[r.get(k,F(0)) for k in range(400)] for r in coupled]);need(coupled_rank==7,'actual coupled reverse correction rank7')
    joint_rank=rank([[r.get(k,F(0)) for k in range(400)] for r in reverse+coupled]);need(joint_rank==65,'actual whole reverse residual rank65')
    K=[[F(i==j)-u.get(i,F(0))*F(j==17) for j in U] for i in U];roots={i:root9(s['frames'][s['initial'][i]][0]) for i in U};G=[[sum(x*y for x,y in zip(roots[i],roots[j]))/2 for j in U] for i in U]
    need(rank(G+K)==rank(G)==7,'coupled correction rows lie in native coupled Gram span, without granting those observations')
    physicalC=[[pre[roles[i+112]].get(roles[j+112],F(0)) for j in U] for i in U]
    schur=[[K[i][j]-sum(G[i][k]*physicalC[k][j] for k in range(8)) for j in range(8)] for i in range(8)]
    need(rank(schur)==7,'unchanged canonical cross blocks would still have a7-dimensional condensed debt')
    need(bill['instructions']==5232 and bill['lifetimes']==398 and bill['peak']==29,'exact complete source count and lifetimes')
    dm={k:bill['moves'].get(k,0)-oldbill['moves'].get(k,0) for k in bill['moves'].keys()|oldbill['moves'].keys()};need({k:v for k,v in dm.items() if v}=={1:-4},'exact saving of4 rank1 calls, with every other MOVE unchanged')
    controls=[]
    for kind in ['wrong_rank1_entry_sign','missing_half_scale','missing_physical_pivot_add']:
        z=copy.deepcopy(w)
        if kind=='wrong_rank1_entry_sign':ix=next(k for k,o in enumerate(prefix) if o[0]=='ADD' and o[1]==roles[19]);z['program'][ix][3]='-1'
        elif kind=='missing_half_scale':ix=next(k for k,o in enumerate(prefix) if o[0]=='SCALE');z['program'][ix][2]='1'
        else:ix=next(k for k,o in enumerate(prefix) if o[0]=='ADD' and o[1]==roles[131] and o[4]==3);z['program'][ix][3]='0'
        rr,rl,_=e.run(z['program'],z['initial'],400,z['owned_fields'],spaces,basis);need(rr!=after,'rejected dyadic-entry mutant '+kind);controls.append({'name':kind,'rejected':True,'event':ix})
    oldpairs={(o[2],o[3]) for o in q['program'] if o[0]=='MOVE'};newpairs={(o[2],o[3]) for o in w['program'] if o[0]=='MOVE'};need(newpairs<=oldpairs,'all chart map pairs inherited')
    den=sorted({F(o[3] if o[0] in ['ADD','COPY'] else o[2]).denominator for o in w['program'] if o[0] in ['ADD','COPY','SCALE']});need(all(d&(d-1)==0 for d in den),'purely dyadic scalar word')
    w['scope']='Actual partial400-input source with4 coupled entry calls. Coupled reverse correction rank7 remains unpaid; no complete endpoint or supplier.'
    payload=(json.dumps(e.clean(w),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0);a.output.mkdir(parents=True,exist_ok=True);(a.output/'rail-dyadic.json.gz').write_bytes(blob)
    r={'status':'PASS_ACTUAL_FOUR_CALL_DYADIC_ENTRY','native_sha256':e.SOURCE_PIN,'parent_rail_sha256':sha(qb),'word_sha256':sha(blob),'word_payload_sha256':sha(payload),'input_directions':400,'bill':bill,'ordinary_increment':{k:bill['counts'].get(k,0)-oldbill['counts'].get(k,0) for k in bill['counts'].keys()|oldbill['counts'].keys()},'paid_move_increment':{1:-4},'all_raw_paths_and_forward_packet_reads_literal':True,'all_coupled_Y_at0_for_packet_reads':True,'scalar_denominators':den,'information_inverse':'y=2c-u*c17; x=a+u*c17','forward_residual_a_basis':basis_count,'old_forward_residual_original_inputs':old_count,'new_forward_residual_original_inputs':new_count,'completed_firstY_ports':[i for i in s['live'] if not newErrors[i]],'hosted_reverse_residual_rank':host_rank,'coupled_reverse_residual_rank':coupled_rank,'joint_reverse_residual_rank':joint_rank,'completed_coupled_reverse_ports':[i for i,row in zip(U,coupled) if not row],'coupled_reverse_correction_matrix':K,'coupled_correction_visible_in_Gram_rowspace':True,'pure_coupled_Gram_observation_supplied':False,'all_hosted_reverse_D_rows_unchanged':True,'new_chart_pairs':[],'negative_controls':controls,'scope':w['scope']+' Both strict suppliers and all five foundations remain.'}
    r['conditional_canonical_cross_condensed_rank']=7;r['conditional_canonical_cross_joint_rank']=15;r['canonical_cross_actions_constructed']=False
    (a.output/'RESULT.json').write_text(json.dumps(e.clean(r),sort_keys=True,indent=2)+'\n');print(json.dumps(e.clean({k:r[k] for k in ['status','word_sha256','bill','ordinary_increment','forward_residual_a_basis','new_forward_residual_original_inputs','hosted_reverse_residual_rank','coupled_reverse_residual_rank','joint_reverse_residual_rank','completed_coupled_reverse_ports']}),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
