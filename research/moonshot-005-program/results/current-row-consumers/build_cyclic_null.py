#!/usr/bin/env python3
"""Genuine affine nulls on cyclic22 current rows; no raw route reset."""
import argparse, copy, gzip, json, sys
from pathlib import Path

def main(a):
    base=a.repo/'research/moonshot-005-program/results'
    sys.path.insert(0,str(base/'joint-current-row-codes/review-star'))
    from engine import Q, add, interpret, interval, load, need, rank, root9, sha
    source=a.repo/'research/shared-wire-split-composition/data/final.json.gz'
    parent=base/'joint-current-row-codes/cyclic-dual'
    SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
    PPIN='ca493a06385fc55a1b1b2d30ddb638c7f5b021d19459aa6b0b8c85e3797510d2'
    need(sha((base/'joint-current-row-codes/review-star/engine.py').read_bytes())=='126c5cc00d2347fce1e81278b9e9563e5958f8899580d9bdba0dd8799e4e9d81','exact reused engine pin')
    need(sha(source.read_bytes())==SPIN,'exact native pin')
    need(sha((parent/'WORD.json.gz').read_bytes())==PPIN,'exact cyclic22 pin')
    s,p,prior=load(source),load(parent/'WORD.json.gz'),load(parent/'RESULT.json')
    raw={int(k):v for k,v in p['private_role_map'].items()}
    host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])}
    groups=p['cyclic_dual']['source_groups'];modes=[j for g in groups for j in g['B']]
    selected=modes[:a.modes];need(1<=a.modes<=8,'one through eight modes')
    K=[j for g in groups for kind in ['B','S','T'] for j in g[kind]]
    roots={j:root9(s['frames'][s['initial'][j]][0]) for j in host}
    G=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))/2
    need(all(G(i,j)==Q(i==j) for i in modes for j in modes),'real orthogonal mode frame')
    first=1880+p['owned_fields'];ghosts={j:first+k for k,j in enumerate(selected)}
    returns={j:first+len(selected)+k for k,j in enumerate(selected)}
    insert,births={},[]
    for j in selected:
        b=host[j][0];C=next(g['single_charts']['B'] for g in groups if j in g['B'])
        hits=[i for i,o in enumerate(p['program']) if o==['MOVE',raw[b],s['initial'][b],C,False]]
        need(len(hits)==1,'unique actual initial-to-C3 arrival');at=hits[0]+1
        cut=copy.deepcopy(p);cut['marks']['common_starts']=at;R,L=interpret(s,cut)
        need(R[raw[b]]=={raw[b]:Q(1),b:Q(-1)} and L[raw[b]]==C,'authentic current b at birth')
        insert.setdefault(at,[]).extend([['INIT',ghosts[j],C],['ADD',ghosts[j],raw[b],'-1',C],['MOVE',ghosts[j],C,127,True]])
        births.append({'port':j,'parent_boundary':at,'chart':C,'field':ghosts[j],'parent_move':hits[0],'rank':6})
    finish=[]
    for j in selected:
        b,d=host[j];F=s['final'][d]
        finish.extend([['ADD',ghosts[j],raw[b],'1',127],['INIT',returns[j],F],['ADD',returns[j],raw[d],'1',F],['MOVE',returns[j],F,127,True],['ADD',ghosts[j],returns[j],'1',127]])
    observation_offset=len(finish)
    for i in K:
        for j in selected:
            if G(i,j):finish.append(['ADD',raw[host[i][0]],ghosts[j],str(-G(i,j)),127])
    for j in selected:finish.extend([['CLEAR',ghosts[j],127],['CLEAR',returns[j],127]])
    insert.setdefault(p['marks']['common_starts'],[]).extend(finish)
    ops,lineage,bound=[],[],{};finish_begin=None
    for i,o in enumerate(p['program']):
        if i==p['marks']['common_starts']:finish_begin=len(ops)
        extra=insert.get(i,[]);ops.extend(extra);lineage.extend([None]*len(extra));bound[i]=len(ops)
        ops.append(copy.deepcopy(o));lineage.append(i)
    bound[len(p['program'])]=len(ops);w=copy.deepcopy(p)
    w.update(schema='moonshot-S010-cyclic-affine-null-projector-v1',program=ops,owned_fields=p['owned_fields']+2*len(selected),parent_word_sha256=PPIN,parent_event_of_output=lineage,marks={k:bound[v] for k,v in p['marks'].items()},native_event_to_physical=[bound[i] for i in p['native_event_to_physical']])
    w['parent_cyclic_dual_provenance']=w.pop('cyclic_dual')
    w['cyclic_null_projector']={'selected_modes':selected,'closed_ports':K,'births':births,'ghost_fields':ghosts,'return_fields':returns,'finish_begin':finish_begin,'observation_boundary':finish_begin+observation_offset,'finish_end':w['marks']['common_starts'],'formula':'h_j=-b_initial+b_current+d_j=G[j,K]d_K; b_i-=G[i,j]h_j'}
    before,bl=interpret(s,p);after,al=interpret(s,w)
    need(bl==al and set(before)==set(after),'every old live row and chart retained')
    qd={j:{raw[host[j][1]]:Q(1),host[j][1]:Q(-1)} for j in K};H={j:{} for j in selected}
    for j in selected:
        for k in K:H[j]=add(H[j],qd[k],G(j,k))
    expected={}
    for i in K:
        delta={}
        for j in selected:delta=add(delta,H[j],-G(i,j))
        if delta:
            b=host[i][0];expected[raw[b]]=delta
            current={int(k):Q(v) for k,v in w['paired_reverse_corrections'].get(str(b),[])}
            for k in K:
                c=-sum(G(i,j)*G(j,k) for j in selected)
                d=host[k][1];current[d]=current.get(d,Q(0))+c
            w['paired_reverse_corrections'][str(b)]=[[k,str(v)] for k,v in sorted(current.items()) if v]
    need(all(after[r]==add(row,expected.get(r,{})) for r,row in before.items()),'all1880 columns have exactly projector delta')
    for i,(b,d) in host.items():
        declared={raw[b]:Q(1),b:Q(-1)}
        for k,v in w['paired_reverse_corrections'].get(str(b),[]):
            declared=add(declared,{raw[k]:Q(1),k:Q(-1)},Q(v))
        need(after[raw[b]]==declared,'current reverse metadata equals actual full-input row')
    cut=copy.deepcopy(w);cut['marks']['common_starts']=finish_begin+observation_offset;R,L=interpret(s,cut)
    need(all(L[ghosts[j]]==127 and R[ghosts[j]]==H[j] for j in selected),'each actual Hub observer has complete pure-D row')
    need(w['program'][w['marks']['common_starts']:]==p['program'][p['marks']['common_starts']:],'literal native/common suffix')
    for r in expected:
        original=next(i for i,v in raw.items() if v==r)
        uses=[o for o in w['program'][w['marks']['common_starts']:] if o[1]==r or o[0] in ['ADD','COPY'] and o[2]==r]
        need(uses==[['ADD',r,original,'1',s['final'][original]]],'changed private row only feeds own final recoupling')
        need(add(after[r],expected[r],Q(-1))==before[r],'information inverse from authentic retained d')
    projection=[o for o in w['program'] if o[1]<first and not(o[0] in ['ADD','COPY'] and o[2]>=first)]
    need(projection==p['program'],'every parent instruction retained literally and in order')
    order=list(host)
    M=[[Q(i==j)+after[raw[host[i][0]]].get(raw[host[j][1]],Q(0)) for j in order] for i in order]
    residual_rank=rank(M);need(residual_rank==82-len(selected),'actual reverse rank loses one per orthogonal mode')
    completed=[i for i,row in zip(order,M) if not any(row)];need(all(j in completed for j in selected),'selected original reverse endpoints complete')
    w['newly_completed_hosted_reverse_ports']=completed
    outside=[j for j in order if j not in K]
    need(all(M[order.index(i)][order.index(j)]==Q(i==j) for i in outside for j in outside),'outside identity block retained')
    need(all(M[order.index(i)][order.index(j)]==0 for i in K for j in outside),'no outside-K d nuisance')
    bill,fin=interpret(s,w,True);oldbill,oldfin=interpret(s,p,True)
    need(fin==oldfin,'all1880 original final public charts retained')
    ordinary={k:bill['opcode_counts'].get(k,0)-oldbill['opcode_counts'].get(k,0) for k in bill['opcode_counts'].keys()|oldbill['opcode_counts'].keys()}
    dm={k:bill['move_rank_histogram'].get(k,0)-oldbill['move_rank_histogram'].get(k,0) for k in bill['move_rank_histogram'].keys()|oldbill['move_rank_histogram'].keys()};dm={k:v for k,v in dm.items() if v}
    need(dm=={1:len(selected),6:len(selected)},'every new rank1/rank6 call charged')
    need(bill['raw_histogram']==oldbill['raw_histogram'],'all original raw MOVEs retained');need(bill['peak_owned']<=43,'owned peak43 retained')
    P={int(k):v for k,v in prior['conditional_caller']['P_partial'].items()};T={int(k):v for k,v in prior['conditional_caller']['T4'].items()}
    for k,n in dm.items():P[k]=P.get(k,0)+18*n
    lo,hi=interval({k:T.get(k,0)-P.get(k,0) for k in T.keys()|P.keys()});lo,hi=lo/18,hi/18
    bad=copy.deepcopy(w);needle=['ADD',ghosts[selected[0]],returns[selected[0]],'1',127]
    hit=next(i for i in range(finish_begin,w['marks']['common_starts']) if bad['program'][i]==needle);bad['program'][hit][3]='0';br,_=interpret(s,bad)
    need(any(br[r]!=after[r] for r in after),'omitted original-d return changes source map')
    payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();blob=gzip.compress(payload,mtime=0,compresslevel=9)
    a.output.mkdir(parents=True,exist_ok=True);(a.output/'WORD.json.gz').write_bytes(blob)
    r={'status':'PASS_CYCLIC_AFFINE_NULL_PROJECTOR','source_sha256':SPIN,'parent_word_sha256':PPIN,'word_sha256':sha(blob),'word_payload_sha256':sha(payload),'independent_input_columns':1880,'selected_modes':selected,'actual_observation_rows':{j:[[k,str(v)] for k,v in sorted(H[j].items())] for j in selected},'hosted_reverse_residual_rank':residual_rank,'completed_hosted_reverse_ports':completed,'closed_principal_rank':8-len(selected),'bill':bill,'ordinary_increment':ordinary,'new_owned_move_histogram':dm,'new_owned_moment_expression':f'{len(selected)}*(6^(199/200)+1)','forward_duties':{'unchanged_from_cyclic22':True,'residual_changed_basis':prior['forward_residual_count_in_preconditioned_basis'],'residual_original_basis':prior['forward_residual_count_in_original_difference_basis']},'conditional_caller':{'T4':T,'P_partial':P,'paid_positions':sum(P.values()),'target_positions':sum(T.values()),'rank_surplus':sum(k*(T.get(k,0)-P.get(k,0)) for k in T.keys()|P.keys()),'remaining_moment_per_native_lower':str(lo),'remaining_moment_per_native_upper':str(hi),'remaining_moment_per_native_decimal':float(lo),'positive_target_minus_paid':lo>0},'negative_controls':{'omitted_original_d_return_changes_source_map':True},'scope':'Actual finite source extension with all1880 inputs, all old endpoint duties, all lifetimes and full conditional H4 invoice. Global forward/supplier obligations and all five foundations remain; no new kappa.'}
    r['source_git_commit']='cbc210ca0eb82c74a021b4f1b744e2e07e07e00b'
    (a.output/'RESULT.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ['status','selected_modes','hosted_reverse_residual_rank','completed_hosted_reverse_ports','ordinary_increment','conditional_caller']},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--modes',type=int,default=4);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
