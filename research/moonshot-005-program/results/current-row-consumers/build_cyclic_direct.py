#!/usr/bin/env python3
"""Delete selected actual residual columns by genuine rank1 returns."""
import argparse,copy,gzip,json,sys
from pathlib import Path

def main(a):
    base=a.repo/'research/moonshot-005-program/results';sys.path.insert(0,str(base/'joint-current-row-codes/review-star'))
    from engine import Q,add,interpret,interval,load,need,rank,root9,sha
    sp=a.repo/'research/shared-wire-split-composition/data/final.json.gz';parent=base/'joint-current-row-codes/cyclic-dual'
    SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883';PPIN='ca493a06385fc55a1b1b2d30ddb638c7f5b021d19459aa6b0b8c85e3797510d2'
    need(sha(sp.read_bytes())==SPIN and sha((parent/'WORD.json.gz').read_bytes())==PPIN,'exact source/parent pins')
    s,p,pr=load(sp),load(parent/'WORD.json.gz'),load(parent/'RESULT.json')
    raw={int(k):v for k,v in p['private_role_map'].items()};host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])}
    K=[j for g in p['cyclic_dual']['source_groups'] for kind in ['B','S','T'] for j in g[kind]]
    before,loc=interpret(s,p);order=list(host)
    C={i:{j:Q(i==j)+before[raw[host[i][0]]].get(raw[host[j][1]],Q(0)) for j in order} for i in order}
    outside=[i for i in order if i not in K]
    J=[int(x) for x in a.ports.split(',')] if a.ports else K+outside[:a.additional]
    need(J and len(J)==len(set(J)) and set(J)<=set(host),'actual distinct hosted return ports')
    temp=1880+p['owned_fields'];patch=[];lifetimes=[]
    for j in J:
        d=host[j][1];F=s['final'][d]
        need(before[raw[d]]=={raw[d]:Q(1),d:Q(-1)} and loc[raw[d]]==F,'authentic retained original d at actual facet')
        begin=len(patch);patch.extend([['INIT',temp,F],['ADD',temp,raw[d],'1',F],['MOVE',temp,F,127,True]])
        for i in order:
            if C[i][j]:
                need(loc[raw[host[i][0]]]==127,'actual original B output cocharted at Hub')
                patch.append(['ADD',raw[host[i][0]],temp,str(-C[i][j]),127])
        patch.append(['CLEAR',temp,127]);lifetimes.append({'port':j,'field':temp,'facet':F,'local_begin':begin,'local_end':len(patch)})
    at=p['marks']['common_starts'];w=copy.deepcopy(p)
    w.update(schema='moonshot-S010-actual-residual-column-consumer-v1',program=p['program'][:at]+patch+p['program'][at:],owned_fields=p['owned_fields']+1,parent_word_sha256=PPIN,parent_event_of_output=list(range(at))+[None]*len(patch)+list(range(at,len(p['program']))),marks={k:v+(len(patch) if v>=at else 0) for k,v in p['marks'].items()},native_event_to_physical=[v+(len(patch) if v>=at else 0) for v in p['native_event_to_physical']])
    w['parent_cyclic_dual_provenance']=w.pop('cyclic_dual');w['cyclic_direct_returns']={'closed_ports':K,'selected_return_ports':J,'begin':at,'end':at+len(patch),'lifetimes':lifetimes,'one_reused_owned_slot':temp,'formula':'for each j in J return authentic d_j and subtract actual residual column M[:,j]d_j from all96 B outputs'}
    for i in order:
        row={host[j][1]:(Q(0) if j in J else C[i][j])-Q(i==j) for j in order}
        w['paired_reverse_corrections'][str(host[i][0])]=[[k,str(v)] for k,v in row.items() if v]
    after,al=interpret(s,w);need(al==loc and set(before)==set(after),'all old prefix records and locations retained')
    expected={}
    for i in order:
        delta={}
        for j in J:delta=add(delta,{raw[host[j][1]]:Q(1),host[j][1]:Q(-1)},-C[i][j])
        if delta:expected[raw[host[i][0]]]=delta
    need(all(after[r]==add(row,expected.get(r,{})) for r,row in before.items()),'all1880 columns have exactly full actual-column subtraction')
    for i in order:
        b,d=host[i]
        declared={raw[b]:Q(1),b:Q(-1)}
        for k,v in w['paired_reverse_corrections'][str(b)]:declared=add(declared,{raw[k]:Q(1),k:Q(-1)},Q(v))
        need(after[raw[b]]==declared,'all current correction metadata agrees with actual1880-input source row')
        if raw[b] not in expected:continue
        uses=[o for o in w['program'][w['marks']['common_starts']:] if o[1]==raw[b] or o[0] in ['ADD','COPY'] and o[2]==raw[b]]
        need(uses==[['ADD',raw[b],b,'1',s['final'][b]]],'changed b only feeds own final recoupling')
        need(add(after[raw[b]],expected[raw[b]],Q(-1))==before[raw[b]],'explicit source information inverse')
    need(w['program'][w['marks']['common_starts']:]==p['program'][at:],'literal common suffix')
    M=[[Q(i==j)+after[raw[host[i][0]]].get(raw[host[j][1]],Q(0)) for j in order] for i in order]
    want=[[Q(0) if j in J else C[i][j] for j in order] for i in order]
    need(M==want,'entire actual residual matrix equals specified column deletion')
    residual_rank=rank(M);completed=[i for i,row in zip(order,M) if not any(row)]
    w['newly_completed_hosted_reverse_ports']=completed
    if set(K)<=set(J):
        need(residual_rank==96-len(J) and set(completed)==set(J),'K-containing pattern has exact rank and original output completions')
    bill,fl=interpret(s,w,True);oldbill,oldfl=interpret(s,p,True);need(fl==oldfl,'every original final chart preserved')
    need(bill['raw_histogram']==oldbill['raw_histogram'] and bill['peak_owned']<=43,'all raw movements retained and peak43 preserved')
    dm={k:bill['move_rank_histogram'].get(k,0)-oldbill['move_rank_histogram'].get(k,0) for k in bill['move_rank_histogram'].keys()|oldbill['move_rank_histogram'].keys()};need({k:v for k,v in dm.items() if v}=={1:len(J)},'exact selected rank1 call count')
    ordinary={k:bill['opcode_counts'].get(k,0)-oldbill['opcode_counts'].get(k,0) for k in bill['opcode_counts'].keys()|oldbill['opcode_counts'].keys()}
    P={int(k):v for k,v in pr['conditional_caller']['P_partial'].items()};T={int(k):v for k,v in pr['conditional_caller']['T4'].items()};P[1]+=18*len(J)
    lo,hi=interval({k:T.get(k,0)-P.get(k,0) for k in T.keys()|P.keys()});lo,hi=lo/18,hi/18
    bad=copy.deepcopy(w);ix=next(i for i in range(at,at+len(patch)) if bad['program'][i][0]=='ADD' and bad['program'][i][1]<1880);bad['program'][ix][3]='0';br,_=interpret(s,bad);need(br!=after,'missing actual correction rejected')
    need(all(after[i]=={i:Q(1)} and al[i]==w['initial'][i] for i in range(1480)),'all1480 common rows and locations unchanged at common entry')
    payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();blob=gzip.compress(payload,mtime=0,compresslevel=9);a.output.mkdir(parents=True,exist_ok=True);(a.output/'WORD.json.gz').write_bytes(blob)
    r={'status':'PASS_ACTUAL_RESIDUAL_COLUMN_CONSUMER','source_git_commit':'cbc210ca0eb82c74a021b4f1b744e2e07e07e00b','source_sha256':SPIN,'parent_word_sha256':PPIN,'word_sha256':sha(blob),'word_payload_sha256':sha(payload),'independent_input_columns':1880,'completed_hosted_reverse_ports':completed,'hosted_reverse_residual_rank':residual_rank,'bill':bill,'ordinary_increment':ordinary,'new_owned_move_histogram':{1:len(J)},'new_owned_moment_per_native':len(J),'common_entry_boundary':w['marks']['common_starts'],'all1480_common_identity_rows_and_initial_locations':True,'forward_duties':{'unchanged_from_cyclic22':True,'residual_changed_basis':pr['forward_residual_count_in_preconditioned_basis'],'residual_original_basis':pr['forward_residual_count_in_original_difference_basis']},'conditional_caller':{'T4':T,'P_partial':P,'paid_positions':sum(P.values()),'target_positions':sum(T.values()),'rank_surplus':sum(k*(T.get(k,0)-P.get(k,0)) for k in T.keys()|P.keys()),'remaining_moment_per_native_lower':str(lo),'remaining_moment_per_native_upper':str(hi),'remaining_moment_per_native_decimal':float(lo),'positive_target_minus_paid':lo>0},'negative_controls':{'one_omitted_true_correction_changes_source_map':True},'scope':'Actual finite source partial completion, not full forward/reverse native or supplier. All remaining endpoint duties, uniform compiler, ordinary costs and all five foundations remain.'}
    r['selected_return_ports']=J
    r['conditional_caller']['positive_target_minus_paid']=lo>0
    parent_moves={(o[2],o[3]):i for i,o in enumerate(p['program']) if o[0]=='MOVE'}
    maps=[{'new_event':i,'source':o[2],'target':o[3],'rank':1,'parent_event':parent_moves.get((o[2],o[3]))} for i,o in enumerate(w['program']) if at<=i<at+len(patch) and o[0]=='MOVE']
    (a.output/'CHART-INHERITANCE.json').write_text(json.dumps({'word_sha256':sha(blob),'parent_word_sha256':PPIN,'maps':maps,'all_pairs_inherited':all(x['parent_event'] is not None for x in maps)},sort_keys=True,indent=2)+'\n')
    (a.output/'RESULT.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['status','word_sha256','hosted_reverse_residual_rank','ordinary_increment','conditional_caller']},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--ports',default=None);p.add_argument('--additional',type=int,default=0);main(p.parse_args())
