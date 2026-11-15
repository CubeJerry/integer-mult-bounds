#!/usr/bin/env python3
"""Independent exact replay of the three mixed-cache descents; no author imports."""
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from check import SOURCE_SHA,dot,kernel,need,price,rank2,rref
from coupled_history_check import replay as replay_prefix
from partial_invoice import check as invoice
from eight_check import combine,separator,solve_combination

HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent
REPO=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
PREFIX=BASE/'worker-a/two-receiver-output/COUPLED-WORD.json'
SOURCE=REPO/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
NAMES=['DC1_1','DC1_2','DC2_1']
FRAME=[0,15,31,35,40,41,106,110]
DUALS=[49,90,146]
TARGETS=[17,34]

def run(word,prefix,prior,roots):
    n=len(prefix['operations'])
    need(word['operations'][:n]==prefix['operations'],'literal two-output prefix unchanged')
    need({k:v for k,v in word['charts'].items() if k!='SHARED5'}==prefix['charts'],'old charts unchanged')
    need(word['charts']['SHARED5']=={'kind':'ann','rows':prefix['charts']['D6']['rows']+[roots[0]]},'exact shared chart normal rows')
    charts={k:kernel(v['rows']) if v['kind']=='ann' else rref(v['rows']) for k,v in word['charts'].items()}
    need(len(charts['SHARED5'])==5,'shared chart dimension five')
    expected=[['MOVE',name,'SHARED5'] for name in NAMES]
    need(word['operations'][n:n+3]==expected,'three actual owned-cache descents')
    R={name:[v['chart'],int(v['coefficient_hex'],16),v['owned']] for name,v in prior['actual_handoff'].items()}
    counts=Counter(prior['operations']);profile=Counter({int(k):v for k,v in prior['movement_profile'].items()})
    drops=[];handoff=None
    def outputs(closed):
        for j in range(111):
            need(R[f'X{j}'][:2]==['Hub',1<<j],'original X restored')
            value=(1<<(111+j))^((1<<j) if j in TARGETS else 0)
            chart=f'F{j}' if closed or j in TARGETS else 'zero'
            need(R[f'Y{j}'][:2]==[chart,value],'all222 original output coefficients/charts')
    for at,(kind,name,*args) in enumerate(word['operations'][n:],n):
        counts[kind]+=1
        if kind=='MOVE':
            old,value,owned=R[name];new=args[0]
            outer,inner=(old,new) if owned else (new,old)
            need(len(rref(charts[outer]+charts[inner]))==len(charts[outer]),'exact monotone chart inclusion')
            drop=abs(len(charts[new])-len(charts[old]));need(drop>0,'positive paid rank')
            if owned:
                need(at<n+3 and name in NAMES,'only three extra owned descents')
                drops.append(drop)
            profile[drop]+=1;R[name][0]=new
        elif kind=='CLEAR':
            if handoff is None:
                outputs(False);handoff={k:{'chart':v[0],'coefficient_hex':hex(v[1]),'owned':v[2]} for k,v in R.items()}
            need(name in R and R[name][2],'owned CLEAR');del R[name]
        else:raise ValueError('unexpected suffix primitive or new owner')
    outputs(word['closed_partial'])
    need(drops==[2,1,2],'exact shared-export movement ranks')
    if handoff is None:handoff={k:{'chart':v[0],'coefficient_hex':hex(v[1]),'owned':v[2]} for k,v in R.items()}
    for name,expected in word['expected_owned_at_handoff'].items():
        need(handoff[name]['chart']==expected['chart'] and handoff[name]['coefficient_hex']==expected['value_hex'],'actual retained cache endpoint')
    need(sum(v[2] for v in R.values())==(0 if word['closed_partial'] else 168),'complete owned lifecycle')
    if word['closed_partial']:
        need(dict(counts)=={'INIT':168,'ADD':670,'MOVE':436,'CLEAR':168},'complete closed counters')
        need(dict(profile)=={1:143,2:21,3:49,4:66,5:22,6:22,7:112,8:1},'complete shared-export profile')
    T=[int(handoff[f'P{i}']['coefficient_hex'],16) for i in range(8)]
    G=T+[1<<i for i in [16,19,38,49,50,56,57]]
    Z=[int(handoff[name]['coefficient_hex'],16) for name in NAMES]
    def restrict(v):return sum(((v>>j)&1)<<k for k,j in enumerate(FRAME))
    signatures=[sum(((restrict(v)&z).bit_count()%2)<<k for k,z in enumerate(DUALS)) for v in Z]
    need(signatures==[5,3,1] and rank2(signatures)==3,'three independent actual frame-cut quotient signatures')
    need(rank2([restrict(v) for v in G])==5 and rank2([restrict(v) for v in G+Z])==8,'frame information rank raised from five to eight')
    remaining_frame=[0,22,23,30,32,60,61,107]
    need(not set(remaining_frame)&set(TARGETS),'remaining frame unserved')
    need(all(dot(roots[i],roots[j])!=0 for i in remaining_frame for j in remaining_frame),'remaining frame nonorthogonal')
    remainder_rows=[sum(((v>>j)&1)<<k for k,j in enumerate(remaining_frame)) for v in G+Z]
    need(rank2(remainder_rows)==5,'remaining frame rank-five restriction')
    remainder_duals=[]
    for z in range(1,256):
        if all((z&v).bit_count()%2==0 for v in remainder_rows) and rank2(remainder_duals+[z])>len(remainder_duals):remainder_duals.append(z)
    need(len(remainder_duals)==3,'three remaining independent duals')
    global_fit=[];chart_fit=[];terminal_fit=[];access=[];duals={};certificates={}
    for i in range(111):
        outside=sum(1<<j for j in range(111) if dot(roots[i],roots[j])!=0)
        can_read=all(dot(row,roots[i])==0 for row in charts['SHARED5'])
        if can_read:access.append(i)
        for label,rows,out in [('global',G+Z,global_fit),('chart_aware',G+(Z if can_read else []),chart_fit),('terminal_only',T+Z,terminal_fit)]:
            projected=[v&outside for v in rows]
            coefficients=solve_combination(projected,1<<i)
            if coefficients is not None:
                out.append(i);fitting=combine(rows,coefficients)
                need(fitting&outside==1<<i,'exact fitting row')
                certificates.setdefault(label,[]).append({'receiver':i,'coefficient_mask':coefficients,'fitting_hex':hex(fitting)})
            else:
                duals.setdefault(label,[]).append({'receiver':i,'dual_hex':hex(separator(projected,1<<i,outside))})
    return {'status':'PASS_INDEPENDENT_THREE_MIXED_CACHE_DESCENTS','all_222_columns_replayed':True,
            'closed_partial':word['closed_partial'],'completed_targets':TARGETS,'new_completed_targets':[],
            'operations':dict(sorted(counts.items())),'movement_profile':dict(sorted(profile.items())),
            'rank_length':sum(k*v for k,v in profile.items()),'moment':price(profile),
            'peak_owned':168,'new_owners':0,'extra_owned_descents':3,'extra_owned_rank':5,
            'moving_owned_records':18,'unchanged_packet_history_rank':37,'unchanged_pure_W_history_dimension':15,
            'actual_export_rows_hex':[hex(v) for v in Z],'quotient_signatures':signatures,
            'frame_rank_before':5,'frame_rank_after':8,'global_relaxation_rank':rank2(G+Z),
            'remaining_frame':remaining_frame,'remaining_frame_rank':5,'remaining_frame_duals':remainder_duals,
            'global_relaxation_feasible_roles':global_fit,'shared_chart_reachable_roles':access,
            'terminal_and_exports_without_global_donor_grant_feasible_roles':terminal_fit,
            'chart_aware_donor_global_relaxation_feasible_roles':chart_fit,
            'fitting_certificates':certificates,'failed_role_duals':duals,
            'actual_handoff':handoff,'new_complete_kappa':False}

def main():
    need(hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_SHA,'authenticated native root source')
    need(hashlib.sha256(PREFIX.read_bytes()).hexdigest()=='506b2e5be90448548e5e71d9757028962ed3c74806b328792e6e0b69a8f20ba5','frozen two-output prefix pin')
    roots=json.loads(SOURCE.read_text())['native_roots'];prefix=json.loads(PREFIX.read_text())
    prior=replay_prefix(prefix,roots,localized=True,second_receiver=True)
    receipts={};hashes={}
    for name in ['WORD.json','CLOSED-WORD.json']:
        path=BASE/'worker-a/shared-export-output'/name
        word=json.loads(path.read_text());receipts[name]=run(word,prefix,prior,roots)
        hashes[name]=hashlib.sha256(path.read_bytes()).hexdigest()
    original=json.loads((BASE/'worker-a/shared-export-output/WORD.json').read_text())
    controls={}
    for index,name in enumerate(NAMES):
        bad=copy.deepcopy(original);del bad['operations'][len(prefix['operations'])+index]
        try:run(bad,prefix,prior,roots)
        except(ValueError,KeyError) as exc:controls['omit_'+name]={'rejected':True,'reason':str(exc)}
        else:raise ValueError('accepted omitted owned descent')
    bad=copy.deepcopy(original);bad['charts']['SHARED5']['rows'][-1]=roots[1]
    try:run(bad,prefix,prior,roots)
    except(ValueError,KeyError) as exc:controls['wrong_receiver_facet']={'rejected':True,'reason':str(exc)}
    else:raise ValueError('accepted changed source facet')
    result={'status':'PASS_INDEPENDENT_SHARED_EXPORT_SUFFIX','source_sha256':SOURCE_SHA,'word_sha256':hashes,
            'prefix_freshly_replayed_by_independent_engine':True,'receipts':receipts,'negative_controls':controls,'new_complete_kappa':False}
    (HERE/'SHARED-SUFFIX-RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    prices=invoice({int(k):v for k,v in receipts['CLOSED-WORD.json']['movement_profile'].items()})
    (HERE/'SHARED-SUFFIX-PRICE.json').write_text(json.dumps(prices,indent=2,sort_keys=True)+'\n')
    r=receipts['CLOSED-WORD.json']
    print(json.dumps({k:r[k] for k in ['status','operations','quotient_signatures','global_relaxation_feasible_roles','shared_chart_reachable_roles','chart_aware_donor_global_relaxation_feasible_roles']},indent=2))

if __name__=='__main__':main()
