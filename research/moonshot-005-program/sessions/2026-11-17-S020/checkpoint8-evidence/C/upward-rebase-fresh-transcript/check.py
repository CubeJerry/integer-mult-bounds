#!/usr/bin/env python3
"""Parent-map verification and same87-input dual after the paid owned ascent."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,importlib.util,json
BASE=Path('/workspace/scratch/2a62370e4336')
PINS={'native':'8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e',
 'word':'581266484817956c8f6b1dc279291a362ddf00a4c580f25a35f3fe56670c7729',
 'parent':'91d4a24a995a18ed306b6c657e76e9cac1f14c8077b4143aae94581b50e2eb6e',
 'mapped_dual':'e8cce0c701912e3be111603447ec1b0f95daee1b84a783cce15a5fe730b10e92',
 'source_review':'37d995575ad179e524c0de505e5d56f45749b5da73ce3750244c5594e41a9402',
 'arithmetic':'41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565',
 'entropy_review':'582f534eefdac53c4b4a284c01ce24454969327e13014c8d56270ce75b875e23'}
def need(x,s):
    if not x:raise ValueError(s)
def module(p,n):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
    ap=argparse.ArgumentParser();defaults={'native':'workers/C/native.json','word':'workers/C/owned-upward-half-rebase/output/WORD.json',
      'parent':'workers/A/proper-half-service/WORD.json','mapped_dual':'workers/C/shared-half-fresh-transcript/output/MAPPED-DUAL.json',
      'source_review':'workers/C/proper-query-export-review/check.py','arithmetic':'workers/C/four-plane-review/check.py',
      'entropy_review':'workers/C/entropy54-review/check.py'}
    for k,p in defaults.items():ap.add_argument('--'+k.replace('_','-'),type=Path,default=BASE/p)
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output');a=ap.parse_args()
    for k,pin in PINS.items():need(hashlib.sha256(getattr(a,k).read_bytes()).hexdigest()==pin,'authenticated '+k)
    R=json.loads(a.native.read_bytes())['native_roots'];w=json.loads(a.word.read_bytes());parent=json.loads(a.parent.read_bytes());dual=json.loads(a.mapped_dual.read_bytes())
    m=module(a.source_review,'parent_source_map');m.geo=m.load_arithmetic(a.arithmetic);g=m.geo
    C={n:g.chart(z)for n,z in w['charts'].items()};PC={n:g.chart(z)for n,z in parent['charts'].items()}
    D=[int(x,16)for x in parent['Y_correction_rows_hex']];ps,V,P=m.replay(parent,PC,D,check_cut=False)
    stage=json.loads(json.dumps(parent));stage['carrier_interface_before_operation']=1921;_,SV,SP=m.replay(stage,PC,D,check_cut=False)
    N=[sum(1<<j for j,r in enumerate(R)if sum(x*y for x,y in zip(R[i],r))==0)for i in range(111)]
    for i in range(111):
        baseline=(1<<(111+i))^((1<<i)if i<8 else N[i]&255)
        need(SV[f'Y{i}']==baseline and SP[f'Y{i}']=='zero','actual independent ground baselines at1921')
        need(V[f'Y{i}']>>111==1<<i,'parent Y-to-Y map is identity')
    need(all(v>>111==0 for n,v in SV.items()if not n.startswith('Y'))and all(v>>111==0 for n,v in V.items()if not n.startswith('Y')),'non-Y fields independent of all initial Y')
    before=[['ADD','Y20','Y96'],['ADD','Y96','Y20']]
    owner='HALF_SERVICE_EXPORT_2';H=P['Y96'];J='UPWARD_HALF_REBASE_J'
    after=[['MOVE',owner,H],['ADD',owner,'Y96'],['MOVE','Y20',J],['MOVE','Y96',J],['ADD','Y96','Y20'],['ADD','Y20','Y96']]
    need(w['operations']==parent['operations'][:1921]+before+parent['operations'][1921:2089]+after+parent['operations'][2089:],'exact two earlier plus six later operations')
    # The checked identity baseline map propagates the two complete changed
    # baseline rows to only those same public fields at the parent cut.
    changed=SV.copy()
    for _,s,d in before:changed[d]^=changed[s]
    for name in['Y20','Y96']:V[name]^=changed[name]^SV[name]
    for op,n,d in after:
        if op=='ADD':need(C[P[n]]==C[P[d]],'actual cochart new ADD');V[d]^=V[n]
        else:
            A,B=C[P[n]],C[d];need(len(B)>len(A)and g.contained(A,B),'all new moves strict ascents');P[n]=d
    need(w['carrier_interface_before_operation']==2097 and len(V)==420,'new420-field cut')
    expected=[int(x,16)for x in w['Y_correction_rows_hex']]
    for i in range(111):
        need(V[f'Y{i}']==(1<<(111+i))^expected[i],'all222 coefficients via parent map')
        need(V[f'X{i}']==1<<i and P[f'X{i}']=='Hub','all X raw at Hub')
    places={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};owned=set();born=set()
    counts=Counter();profile=Counter();up=Counter();down=Counter();atcut=None
    for ix,(op,n,*args)in enumerate(w['operations']):
        if ix==2097:atcut=places.copy()
        counts[op]+=1
        if op=='INIT':need(n not in places and n not in born,'fresh owner');places[n]=args[0];owned.add(n);born.add(n)
        elif op=='ADD':need(n!=args[0]and C[places[n]]==C[places[args[0]]],'every actual cochart ADD')
        elif op=='MOVE':
            A,B=C[places[n]],C[args[0]];delta=len(B)-len(A);need(delta!=0,'positive movement')
            need(g.contained(A,B)if delta>0 else g.contained(B,A),'nested actual charts')
            if n in owned:(up if delta>0 else down)[abs(delta)]+=1
            else:need(delta>0,'all public moves upward')
            profile[abs(delta)]+=1;places[n]=args[0]
        elif op=='CLEAR':need(n in owned,'owned retirement');owned.remove(n);del places[n]
    need(atcut==P and len(places)==222 and not owned,'all current and final places')
    need(up=={2:1}and down=={1:40}and profile=={1:200,2:123,3:22,4:103,7:96},'complete actual movement invoice')
    need(counts=={'INIT':198,'ADD':1466,'MOVE':544,'CLEAR':198},'full primitive counts')
    need(all(places[f'Y{i}']==f'F{i}'for i in range(111)),'all Y endpoints')
    E=[22,23,26,27,42,43,44,45,73,74,75,76,77,78,79,80];U=sorted(set(range(8,111))-set(E));mask=sum(1<<i for i in U)
    need(set(dual['roles']+dual['isolates'])<=set(U),'same witness among87 unknowns')
    checks=[];leaks=[];nonaxis=((1<<111)-1)^255
    for i in range(8,111):
        inside=[n for n in V if g.contained(C[P[n]],C[f'F{i}'])]
        for n in inside:
            bad=V[n]&nonaxis&~N[i]
            if bad:leaks.append({'receiver':i,'field':n,'forbidden_mask_hex':hex(bad)})
            need(V[n]&mask&~N[i]==0,'actual conditional native locality')
        if i in U:checks.append({'receiver':i,'inside_fields':inside})
    need(len(checks)==87 and len(leaks)==56,'new56 rather than old66 leaks')
    h=module(a.entropy_review,'same_exact_dual');h.CORE=dual['roles'];h.ISO=dual['isolates'];exact=h.review_dual(dual,R)
    future=dict(profile);future[1]+=9;lower=g.moment(future);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in g.moment(gate));room=(ceiling[0]-lower[1],ceiling[1]-lower[0])
    result={'status':'PASS_SAME87_WITNESS_AFTER_LITERAL_OWNED_ASCENT','pins':PINS,'cut':2097,'live_fields':420,
      'parent_map_based_all222_source_check':True,'complete_literal_extension_reconstructed':True,'all_current_fields_derived':True,
      'counts':dict(counts),'profile':dict(profile),'owned_upward_profile':dict(up),'owned_downward_profile':dict(down),
      'explicit_conditioning_roles':E,'all87_actual_field_audits':checks,'unconditioned_leaked_incidences':leaks,
      'same_core':dual['roles'],'same_isolates':dual['isolates'],'exact_dual':exact,'future_owned_downward_moves_lower_bound':9,
      'remaining_necessary_limiting_room_after_future9':m.record(room),
      'scope':'Same87-input conditional graph and106-term dual survive after a separately reconstructed paid owned-ascent word. Actual2097 cut,56 current leaks handled explicitly; no mapping search. Nine future descents in fixed-schedule finite-alphabet zero-error monotone-public/arbitrary-paid-owned model. No cost dominance or new completed output.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    (a.out/'INDEPENDENT-CUT.json').write_text(json.dumps([{'name':n,'chart':P[n],'rank':len(C[P[n]]),'row_hex':hex(v)}for n,v in sorted(V.items())],indent=2)+'\n')
    print(result['status'],'all222/420 via parent map,56 leaks,87 facets,9 future descents,room',m.record(room)['decimal'][0])
if __name__=='__main__':main()
