#!/usr/bin/env python3
"""Independent native/custody/cost review of common-meet original-carrier fanout."""
import argparse,copy,hashlib,importlib.util,json
from collections import defaultdict
from pathlib import Path


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--audit-module',type=Path,default=Path(__file__).resolve().parents[1]/'portable'/'audit_cp6.py');a=ap.parse_args()
    spec=importlib.util.spec_from_file_location('own_native_replay',a.audit_module);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);check=m.insist
    raw=a.word.read_bytes();w=json.loads(raw);check(hashlib.sha256(raw).hexdigest()=='f5acfcb454d6d50dfdb7d66acd2c33980e4aed17826afafbb67fbeb2168f58c1','frozen six-output word')
    source=json.loads((a.repo/w['source_path']).read_text());check(m.sha(a.repo/w['source_path'])==w['source_sha256']=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','native source');R=source['native_roots'];T=[1,3,73,76,77,80];check(w['targets']==T,'literal six targets')
    ops=w['operations'];cut=w['carrier_interface_before_operation'];marks=w['milestones'];snapshots=set(marks.values())|{cut}
    assignment=w['fanout']['assignments']
    for k,op in enumerate(ops):
        if op[0]=='ADD'and(op[1].startswith('X')or op[2].startswith('X')):snapshots.add(k);snapshots.add(k+1)
    stats,tr,C,events=m.replay(w,source,snapshots);J='FANOUT_COMMON';check(C[J]==m.chart({'kind':'ann','rows':[R[i]for i in T]})and len(C[J])==5,'actual common rank5 meet')
    G=defaultdict(list)
    for j in range(111):G[tuple(i for i in T if sum(x*y for x,y in zip(R[i],R[j]))==0)].append(j)
    common=G[tuple(T)];mixed={g:ds for g,ds in G.items()if 1<len(g)<len(T)}
    branches={(g,i)for g in mixed for i in g};actual={(tuple(z['group']),z['receiver'])for z in assignment};carriers={z['carrier']for z in assignment}
    check(len(common)==20 and len(mixed)==7 and len(branches)==18,'actual source counts')
    check(actual==branches and len(assignment)==len(carriers)==18 and carriers<=set(common),'one distinct real common original per mixed branch')
    cv,cl=tr[marks['common_raw_capture_end']];check(cv['COMMON_SUM']==set(common)and C[cl['COMMON_SUM']]==C[J],'actual full common row')
    for i in T:
        selected={z['carrier']for z in assignment if z['receiver']==i}
        check(cv[f'MASK_{i}']==selected and C[cl[f'MASK_{i}']]==C[J],('actual mask before carrier mutation',i))
    group_fields={}
    for g,ds in mixed.items():
        H=m.chart({'kind':'ann','rows':[R[i]for i in g]})
        found=[n for n,z in tr[marks['cohort_acquisition_end']][0].items()if n.startswith('COHORT_SUM_')and z==set(ds)and C[tr[marks['cohort_acquisition_end']][1][n]]==H]
        check(len(found)==1,('actual proper cohort sum',g));group_fields[g]=found[0]
    chronology=[]
    for z in assignment:
        g=tuple(z['group']);i=z['receiver'];c=z['carrier'];n=group_fields[g];ds=set(mixed[g]);x=f'X{c}';H=m.chart({'kind':'ann','rows':[R[j]for j in g]})
        inj=ops.index(['ADD',n,x]);deposit=ops.index(['ADD',x,f'FACET_SUM_{i}']);restores=[k for k,op in enumerate(ops)if op[0]=='ADD'and op[2]==x and op[1].startswith('X')]
        iv,il=tr[inj];dv,dl=tr[deposit];check(iv[x]=={c}and iv[n]==ds and C[il[x]]==H,'raw original and actual group at injection')
        check(dv[x]==({c}^ds)and C[dl[x]]==C[f'F{i}'],'actual mixed original at destination facet')
        check(inj<deposit<min(restores)and [int(ops[k][1][1:])for k in restores]==sorted(ds),'chronological explicit donor inverse')
        for k in restores:
            vv,ll=tr[k];donor=int(ops[k][1][1:]);check(vv[f'X{donor}']=={donor}and C[ll[x]]==C[ll[f'X{donor}']]==C['Hub'],'real raw Hub source for inverse')
        check(carriers.isdisjoint(ds),'mask donors disjoint from every used carrier')
        check(tr[restores[-1]+1][0][x]=={c},'original restored at end of its branch')
        chronology.append({'carrier':c,'receiving_target':i,'group':list(g),'inject':inj,'deposit':deposit,'restore_operations':restores})
    rv,rl=tr[marks['all_originals_restored_before_canonical']]
    for i in range(111):check(rv[f'X{i}']=={i}and C[rl[f'X{i}']]==C['Hub'],'every original raw at Hub before first code load')
    v,loc=tr[cut];code_names=[f'CANONICAL_{k}'for k in range(9)];K=[{i}^{j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0}for i in range(111)]
    code_rows=[v[n]for n in code_names];basis=m.binary_basis(code_rows);check(len(basis)==9 and all(m.in_span(row,basis)for row in K),'complete canonical9 rowspace')
    for n in code_names:check(C[loc[n]]==C['zero'],'actual ground code field')
    for i in range(111):check(v[f'NATIVE_RAW_{i}']=={i}and C[loc[f'NATIVE_RAW_{i}']]==C[f'L{i}'],'actual111 stationary native copies')
    for i in T:
        mask={z['carrier']for z in assignment if z['receiver']==i};foreign=K[i]^{i}
        check(v[f'FACET_SUM_{i}']==(foreign^set(common)^mask),'facet sum plus carrier nuisance identity')
        check(v[f'MASK_{i}']==mask,'retained mask identity')
    owned_moves=[e for e in events if e[-1]];check(len(owned_moves)==9 and all(src=='Hub'and dst=='zero'and d==8 for k,n,src,dst,d,owned in owned_moves),'only nine full owned descents')
    check(stats['counts']=={'INIT':140,'ADD':1083,'MOVE':384,'CLEAR':140}and stats['dirty_clear']==140,'complete native operation invoice')
    q=m.moment(stats['movement_profile']);controls=[]
    selected=[('common raw',ops[w['semantic_operation_indices']['common_captures'][0]]),('nuisance mask',ops[w['semantic_operation_indices']['mask_captures'][0]]),('cohort acquisition',ops[w['semantic_operation_indices']['group_captures'][0]]),('carrier coupling',ops[w['semantic_operation_indices']['carrier_injections'][0]]),('carrier facet deposit',ops[w['semantic_operation_indices']['carrier_deposits'][0]]),('Hub restoration',ops[w['semantic_operation_indices']['carrier_restorations'][0]]),('canonical source',ops[w['semantic_operation_indices']['canonical_loads'][0]]),('receiver cancellation',ops[w['semantic_operation_indices']['receiver_reads'][1]])]
    for label,event in selected:
        bad=copy.deepcopy(w);bad['operations'].remove(event)
        try:m.replay(bad,source)
        except (ValueError,KeyError)as exc:controls.append({'control':label,'operation':event,'rejected':str(exc)})
        else:
            if label!='canonical source':raise ValueError('omission escaped endpoint review '+label)
            bad['carrier_interface_before_operation']-=1;st,ss,CC,ee=m.replay(bad,source,[bad['carrier_interface_before_operation']]);bv,bl=ss[bad['carrier_interface_before_operation']];check(any(bv[n]!=v[n]for n in code_names),'code source mutation visible independently of endpoints');controls.append({'control':label,'operation':event,'endpoints_can_pass_but_full_source_rejected':True})
    result={'status':'PASS_INDEPENDENT_COMMON_MEET_SIX_RECEIVER_FANOUT','word_sha256':m.sha(a.word),'source_sha256':w['source_sha256'],'stats':stats,'common_chart_dimension':5,'common_native_roles':common,'target_roles':T,'complete_mixed_cohorts':[{'group':list(g),'inputs':ds}for g,ds in sorted(mixed.items())],'all18_actual_branch_chronologies':chronology,'all111_raw_originals_at_Hub_before_code_acquisition':True,'actual_ground_canonical_rank':9,'actual_native_copies':111,'only_owned_moves_count':9,'only_owned_move_rank':8,'moment':m.interval_json(q),'negative_controls':controls,'scope':'Every characteristic-two field and positive whole-record width for this literal ordinary word. Six completed outputs,105 missing; actual ground code/native/proper sources, no complete supplier or new kappa.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status']);print(stats['counts'],m.interval_json(q)['decimal'])
if __name__=='__main__':main()
