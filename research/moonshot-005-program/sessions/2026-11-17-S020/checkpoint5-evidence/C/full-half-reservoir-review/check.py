#!/usr/bin/env python3
"""Independent source, local-information and tariff verification of the reservoir."""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
import argparse,hashlib,importlib.util,json

BASE=Path('/workspace/scratch/2a62370e4336')
PINS={
 'native':'8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e',
 'word':'6f1bd8465c7a4fa5b7b59888fb5dbd9bbbb88dc3306c984bd71497fd4be7d980',
 'source_review':'37d995575ad179e524c0de505e5d56f45749b5da73ce3750244c5594e41a9402',
 'arithmetic':'41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565',
 'entropy_review':'582f534eefdac53c4b4a284c01ce24454969327e13014c8d56270ce75b875e23',
 'mapped':'67b8f94d20704d20e5a609755b692d0bcc85cb264c67a346c01b099a17e2b20e'}

def need(value,message):
    if not value:raise ValueError(message)

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
    ap=argparse.ArgumentParser()
    defaults={'native':'workers/C/native.json','word':'workers/A/full-half-reservoir/WORD.json',
      'source_review':'workers/C/proper-query-export-review/check.py','arithmetic':'workers/C/four-plane-review/check.py',
      'entropy_review':'workers/C/entropy54-review/check.py','mapped':'workers/R/fresh-transcript-nine/output/MAPPED-DUAL.json'}
    for key,path in defaults.items():ap.add_argument('--'+key.replace('_','-'),type=Path,default=BASE/path)
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output');a=ap.parse_args()
    for key,pin in PINS.items():need(hashlib.sha256(getattr(a,key).read_bytes()).hexdigest()==pin,'authenticated '+key)
    R=json.loads(a.native.read_bytes())['native_roots'];w=json.loads(a.word.read_bytes())
    source=module(a.source_review,'independent_reservoir_source');source.geo=source.load_arithmetic(a.arithmetic);geo=source.geo
    charts={n:geo.chart(z)for n,z in w['charts'].items()}
    E=tuple(tuple(int(i==j)for j in range(8))for i in range(8))
    need(charts['zero']==()and charts['Hub']==E,'ground and Hub')
    for i,r in enumerate(R):
        need(charts[f'L{i}']==geo.basis((tuple(r),)),'native line')
        need(charts[f'F{i}']==geo.kernel((tuple(r),)),'native facet')
    N=[sum(1<<j for j,s in enumerate(R)if sum(x*y for x,y in zip(r,s))==0)for r in R]
    K=[n^(1<<i)for i,n in enumerate(N)]
    expected=[1<<i if i<8 else N[i]&255 for i in range(111)]
    need(w['Y_correction_rows_hex']==list(map(hex,expected)),'independent coordinate/preload targets')
    need(sum(x.bit_count()for x in expected[8:])==412,'412 foreign axis coefficients')
    stats,cv,ca=source.replay(w,charts,expected,check_cut=False)
    need(w['carrier_interface_before_operation']==1893 and len(cv)==406,'actual cut and complete field count')
    need(stats['counts']=={'INIT':184,'ADD':1356,'MOVE':464,'CLEAR':184},'full primitive invoice')
    need(stats['movement_profile']=={1:139,2:103,4:103,7:119},'full move profile')
    need(stats['owned_downward_profile']=={1:36}and stats['dirty_CLEAR']==stats['peak_owned']==184,'paid exports and retirements')
    for i in range(111):
        need(cv[f'X{i}']==1<<i and ca[f'X{i}']=='Hub','raw original at Hub')
        need(cv[f'Y{i}']==(1<<(111+i))^expected[i]and ca[f'Y{i}']=='zero','all arbitrary Y columns retained at ground')
        need(cv[f'NATIVE_{i}']==1<<i and ca[f'NATIVE_{i}']==f'L{i}','stationary actual native snapshot')
    for i in range(8):need(cv[f'AXIS_{i}']==1<<i and ca[f'AXIS_{i}']=='zero','actual known axis owner')
    groups=defaultdict(list)
    for i,r in enumerate(R[8:],8):groups[tuple(j for j,x in enumerate(r)if x)].append(i)
    need(len(groups)==14,'14 actual coordinate supports')
    observed_groups={tuple(g['support']):g for g in w['construction']['quartets']}
    need(set(observed_groups)==set(groups),'exact quartet partition')
    rows=[];all_halves=[];owner_names=set();group_cert=[];direct=paid=0
    for support,roles in groups.items():
        g=observed_groups[support];G=g['quartet_chart'];modes=g['modes']
        need(g['roles']==roles and len(modes)==4,'actual role sets and four selected modes')
        need(charts[G]==geo.basis(tuple(E[j]for j in support))and len(charts[G])==4,'real coordinate quartet')
        local=[];partition=[]
        for k,z in enumerate(modes):
            x,y=z['pair'];sgn=z['sign'];S=[i for i in roles if R[i][x]==sgn*R[i][y]]
            need(x in support and y in support and x<y and sgn in(-1,1),'literal pair equality')
            row=sum(1<<i for i in S);H=z['chart'];owner=z['owner']
            need(z['roles']==S and int(z['row_hex'],16)==row,'half row from original roots')
            need(charts[H]==geo.basis(tuple(tuple(R[i])for i in S))and len(charts[H])==3,'actual half source span')
            need(cv[owner]==row and ca[owner]==H,'pure half owner at its actual plane')
            need(owner not in owner_names,'distinct live owned half');owner_names.add(owner)
            births=[op for op in w['operations'][:1893]if op[:2]==['INIT',owner]]
            moves=[op for op in w['operations'][:1893]if op[:2]==['MOVE',owner]]
            if k<2:
                need(births==[['INIT',owner,H]]and not moves,'direct actual capture at H')
                partition+=S;direct+=1
            else:
                need(births==[['INIT',owner,G]]and moves==[['MOVE',owner,H]],'one paid proper export G to H')
                paid+=1
            local.append(row);rows.append(row)
        need(sorted(partition)==roles and len(partition)==len(set(partition)),'first two actual halves partition the source')
        local_all=[]
        for x,y in combinations(support,2):
            for sgn in(-1,1):local_all.append(sum(1<<i for i in roles if R[i][x]==sgn*R[i][y]))
        need(len(source.binary_basis(local))==len(source.binary_basis(local+local_all))==4,'complete local half span rank4')
        all_halves+=local_all
        group_cert.append({'support':list(support),'roles':roles,'mode_rows_hex':list(map(hex,local)),'rank':4})
    need(direct==paid==28 and len(rows)==56,'direct and paid mode counts')
    need(len(source.binary_basis(rows))==len(source.binary_basis(rows+all_halves))==56,'all56 actual half directions')
    need(len(source.binary_basis(rows+[1<<i for i in range(8)]+K))==64,'axes+halves rank64 contains full canonical code')
    canonical=[]
    for z in w['construction']['canonical_Hub_basis']:
        i=z['role'];name=z['owner'];row=K[i]
        need(int(z['row_hex'],16)==cv[name]==row and ca[name]=='Hub','canonical row gathered at Hub')
        canonical.append(row)
    need(len(canonical)==9 and len(source.binary_basis(canonical))==len(source.binary_basis(canonical+K))==9,'actual complete canonical bank')
    need(all(v>>111==0 for n,v in cv.items()if not n.startswith('Y')),'no Y term in any current X or owner')
    # Strong side-information audit: every unknown coefficient is an actual
    # native neighbour, not merely different from the receiver's own index.
    xmask=(1<<111)-1;locality=[]
    for i in range(8,111):
        inside=[name for name in cv if geo.contained(charts[ca[name]],charts[f'F{i}'])]
        for name in inside:need(cv[name]&xmask&~255&~N[i]==0,'no forbidden unknown coefficient inside facet')
        locality.append({'receiver':i,'inside_field_count':len(inside),'unknown_support_mask_hex':hex(N[i]&~255)})
    need(w['operations'][1893:2004]==[['MOVE',f'Y{i}',f'F{i}']for i in range(111)],'direct minimum public closure')
    need(all(op[0]=='CLEAR'for op in w['operations'][2004:]),'only explicit retirements after public closure')
    # Independently select source operations; the author's semantic index table
    # is not used by these omission controls.
    predicates={
      'axis_capture':lambda o:o==['ADD','X0','AXIS_0'],
      'axis_descent':lambda o:o==['MOVE','AXIS_0','zero'],
      'axis_preload':lambda o:o[0]=='ADD'and o[1].startswith('AXIS_')and o[2].startswith('Y')and int(o[2][1:])>=8,
      'source_half_arrival':lambda o:o[0]=='MOVE'and o[1].startswith('X')and o[2].startswith('RESERVOIR_H'),
      'source_encoding':lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('X'),
      'direct_half_capture':lambda o:o[0]=='ADD'and o[2].startswith('HALF_')and o[2].endswith('_0'),
      'paid_half_gather':lambda o:o[0]=='ADD'and o[2].startswith('HALF_')and o[2].endswith('_2'),
      'paid_half_descent':lambda o:o[0]=='MOVE'and o[1].startswith('HALF_'),
      'canonical_gather':lambda o:o[0]=='ADD'and o[2].startswith('CANONICAL_')}
    controls={}
    for label,pred in predicates.items():
        k=next(i for i,o in enumerate(w['operations'][:1893])if pred(o));alt=json.loads(json.dumps(w))
        del alt['operations'][k];alt['carrier_interface_before_operation']-=1
        try:
            _,bv,ba=source.replay(alt,charts,expected,check_cut=False)
            need((bv,ba)==(cv,ca),'complete actual cut, including unused owners')
        except (ValueError,AssertionError)as e:controls[label]=str(e)
        else:raise ValueError('accepted omitted essential source operation '+label)
    # The inverse is a separate occurrence of the first encoding ADD.
    k0=next(i for i,o in enumerate(w['operations'][:1893])if predicates['source_encoding'](o))
    k1=next(i for i in range(k0+1,1893)if w['operations'][i]==w['operations'][k0]);alt=json.loads(json.dumps(w))
    del alt['operations'][k1];alt['carrier_interface_before_operation']-=1
    try:
        _,bv,ba=source.replay(alt,charts,expected,check_cut=False);need((bv,ba)==(cv,ca),'inverse cut')
    except (ValueError,AssertionError)as e:controls['source_inverse']=str(e)
    else:raise ValueError('accepted omitted source inverse')
    entropy=module(a.entropy_review,'independent_reservoir_entropy')
    entropy.CORE=[61,82,83,20,18,71,70,69,74,76,63];entropy.ISO=[65,109,107]
    entropy_result=entropy.review_dual(json.loads(a.mapped.read_bytes()),R)
    Q=geo.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in geo.moment(gate));room=(ceiling[0]-Q[1],ceiling[1]-Q[0])
    result={'status':'PASS_INDEPENDENT_FULL_HALF_RESERVOIR_AND_LOCALITY','pins':PINS,'cut':1893,
      'stats':stats,'all222_columns':True,'all111_raw_X_Hub':True,'all111_Y_ground':True,
      'completed_coordinate_outputs':8,'foreign_axis_coefficients':412,'proper_half_rank':56,
      'axis_plus_half_rank':64,'actual_canonical_Hub_rank':9,'direct_captures':direct,'paid_exports':paid,
      'groups':group_cert,'all103_unknown_facets_native_local':locality,
      'entropy_review':entropy_result,'future_whole_record_downward_moves_lower_bound':9,
      'moment':source.record(Q),'necessary_limiting_room':source.record(room),
      'negative_controls':controls,
      'scope':'Actual partial source for all characteristic-two fields and block widths. Nine future descents follows for fixed-schedule finite-alphabet zero-error continuations with monotone public routes and arbitrary paid nested owned routes. No free global half bank, completed103 unknown outputs, or supplier.'}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    (a.out/'INDEPENDENT-CUT.json').write_text(json.dumps([{'name':n,'chart':ca[n],'rank':len(charts[ca[n]]),'row_hex':hex(v)}for n,v in sorted(cv.items())],indent=2)+'\n')
    print(result['status'],'all222,406 current fields,56 physical proper half modes,10 controls,9 future descents')

if __name__=='__main__':main()
