#!/usr/bin/env python3
"""Independent all-column, real-chart and invoice replay of query exports."""
from pathlib import Path
from collections import Counter
from decimal import Decimal,localcontext
import argparse,hashlib,importlib.util,json

BASE=Path('/workspace/scratch/2a62370e4336')
NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
WORD='4d4e0a4163483d35741505c747981a2bc8b8da1bc373bb0cb8d10f0aa651f96c'
PARENT='c77823c87362a56ed3c3f10f9808995285dd3f454e11443531f069075f59f4fe'
ARITHMETIC_PIN='41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565'
geo=None

def load_arithmetic(path):
    assert hashlib.sha256(path.read_bytes()).hexdigest()==ARITHMETIC_PIN
    spec=importlib.util.spec_from_file_location('own_fraction_geometry',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def need(b,msg):
    if not b:raise ValueError(msg)

def binary_basis(rows):
    B={}
    for v in rows:
        while v:
            p=v.bit_length()-1
            if p in B:v^=B[p]
            else:B[p]=v;break
    return list(B.values())

def derive(roots,w):
    charts={n:geo.chart(z)for n,z in w['charts'].items()}
    E=tuple(tuple(int(i==j)for j in range(8))for i in range(8))
    need(charts['zero']==()and charts['Hub']==E,'literal public ground and Hub')
    for i,r in enumerate(roots):
        need(charts[f'L{i}']==geo.basis((tuple(r),)),'native line')
        need(charts[f'F{i}']==geo.kernel((tuple(r),)),'native facet')
    configs=[([0,1,6,7],[0,1],[6,7],[2,3]),([2,3,4,5],[2,4],[3,5],[0,1]),
             ([0,1,4,5],[0,5],[1,4],[]),([0,2,5,7],[0,7],[2,5],[])]
    correction=[0]*111;served=set();sources=set();expected_exports=[]
    for k,(support,ab,cd,couriers)in enumerate(configs):
        g=w['construction']['gadgets'][k];tag=f'G{k}'
        need(g['support']==support and g['pair_partition']==[ab,cd]and g['courier_Y_roles']==couriers,'independent gadget configuration')
        signs=[i for i,r in enumerate(roots)if[j for j,x in enumerate(r)if x]==support]
        need(len(signs)==8,'eight source signs')
        local=set(signs+(support if couriers else[]));need(not(sources&local),'source originals disjoint');sources|=local
        need(charts[tag]==geo.basis(tuple(E[i]for i in support)),'quartet chart')
        for s in [1,-1]:
            for letter,xy,other in [('A',ab,cd),('B',cd,ab)]:
                x,y=xy;q=f'{tag}_{letter}{s}';I=[i for i in signs if roots[i][x]==s*roots[i][y]]
                need(len(I)==4 and charts[q]==geo.basis(tuple(tuple(roots[i])for i in I))and len(charts[q])==3,'four-sign query plane')
                candidates=[i for i,r in enumerate(roots)if[j for j in support if r[j]]==sorted(xy)and r[x]==-s*r[y]]
                receivers=[i for i in candidates if i not in served]
                need(g['query_roles'][q]==receivers,'ordered first-compatible receiver assignment')
                row=sum(1<<i for i in I+(other if couriers else[]))
                need(int(g['query_rows_hex'][q],16)==row,'exact query correction row')
                for i in receivers:
                    need(not correction[i]and geo.contained(charts[q],charts[f'F{i}']),'receiver can really reach plane')
                    need(all(sum(a*b for a,b in zip(roots[i],roots[j]))==0 for j in range(111)if row>>j&1),'foreign orthogonal correction')
                    correction[i]=row
                if letter+str(s)in ['A1','A-1','B1']:
                    P,info=next((P,z)for P,z in g['oriented_pairs'].items()if z['early']==q)
                    late=next(z for z in g['oriented_pairs'].values()if z['late']==q)
                    expected_exports.append({'query':q,'representative_Y':receivers[0],'pair_chart':P,
                                             'carrier_X':info['roles'][1],'sum_carriers':[info['roles'][0],late['roles'][0]],
                                             'sign_row':sum(1<<i for i in I)})
        aa,bb=ab;cc,dd=cd
        for s in [1,-1]:
            for t in [1,-1]:
                P=f'{tag}_PAIR_{s}_{t}'
                I=[i for i in signs if roots[i][aa]==s*roots[i][bb]and roots[i][cc]==t*roots[i][dd]]
                need(len(I)==2 and g['oriented_pairs'][P]['roles']==I,'independent pair source roles')
                need(charts[P]==geo.basis(tuple(tuple(roots[i])for i in I))and len(charts[P])==2,'actual pair chart')
                early=f'{tag}_A{s}'if s==t else f'{tag}_B{t}'
                late=f'{tag}_B{t}'if s==t else f'{tag}_A{s}'
                need(g['oriented_pairs'][P]['early']==early and g['oriented_pairs'][P]['late']==late,'oriented cycle')
        served.update(g['served_receivers'])
    need(served==set(range(8,111))and len(sources)==40,'all103 receivers and40 disjoint sources')
    need(w['Y_correction_rows_hex']==list(map(hex,correction)),'full expected correction map')
    need(sum(v.bit_count()for v in correction)==528,'528 foreign coefficients')
    byq={z['query']:z for z in w['construction']['query_exports']}
    need(len(byq)==len(expected_exports)==12,'twelve distinct actual queries')
    for e in expected_exports:
        z=byq[e['query']]
        for key in ['representative_Y','pair_chart','carrier_X']:need(z[key]==e[key],'query export selection')
        need(z['unchanged_sum_carriers']==e['sum_carriers']and int(z['sign_query_row_hex'],16)==e['sign_row'],'literal inverse source pair sums')
    return charts,correction,expected_exports

def replay(w,charts,correction,check_cut=True):
    v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
    at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    owned=set();born=set();counts=Counter();profile=Counter();down=Counter();peak=dirty=0;cut=None
    for k,(op,n,*args)in enumerate(w['operations']):
        if k==w['carrier_interface_before_operation']:cut=(v.copy(),at.copy(),owned.copy())
        counts[op]+=1
        if op=='INIT':
            need(n not in v and n not in born and args[0]in charts,'fresh zero owned birth')
            v[n]=0;at[n]=args[0];owned.add(n);born.add(n)
        elif op=='ADD':
            dest=args[0];need(n in v and dest in v and n!=dest,'live distinct ADD operands')
            need(charts[at[n]]==charts[at[dest]],f'actual cochart ADD at {k}')
            v[dest]^=v[n]
            if dest.startswith('X'):need(v[dest]>>111==0,f'no original-Y contamination in X at {k}')
        elif op=='MOVE':
            need(n in v and args[0]in charts,'live movement source and chart')
            A,B=charts[at[n]],charts[args[0]];gap=abs(len(A)-len(B))
            need(gap>0,'strictly positive movement')
            need(geo.contained(B,A)if n in owned else geo.contained(A,B),f'legal real chart direction at {k}')
            if n in owned:down[gap]+=1
            profile[gap]+=1;at[n]=args[0]
        elif op=='CLEAR':
            need(n in owned,'only owned fields retire');dirty+=bool(v[n]);owned.remove(n);del v[n],at[n]
        else:raise ValueError('unknown operation')
        peak=max(peak,len(owned))
    need(cut is not None and len(v)==222 and not owned,'closed public endpoint and actual cut')
    for i in range(111):
        need(v[f'X{i}']==1<<i and at[f'X{i}']=='Hub','all original X restored')
        need(v[f'Y{i}']==(1<<(111+i))^correction[i]and at[f'Y{i}']==f'F{i}','all original Y columns and proper correction')
    cv,ca,co=cut
    if check_cut:
        need(len(cv)==363 and len(co)==141,'complete source inventory')
        for i in range(111):
            need(cv[f'Y{i}']==(1<<(111+i))^correction[i],'all arbitrary Y coefficients restored at cut')
            need(cv[f'NATIVE_{i}']==1<<i and ca[f'NATIVE_{i}']==f'L{i}','actual stationary native snapshots')
        need(len(binary_basis(cv[f'X{i}']for i in range(111)))==111,'full independent original-X bank')
    return {'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),
            'owned_downward_profile':dict(sorted(down.items())),'peak_owned':peak,'dirty_CLEAR':dirty,
            'cut_fields':len(cv),'cut_owned':len(co)},cv,ca

def record(interval):
    with localcontext()as c:
        c.prec=55
        return {'rational':list(map(str,interval)),'decimal':[str(Decimal(v.numerator)/Decimal(v.denominator))for v in interval]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--native',type=Path,default=BASE/'workers/C/native.json')
    ap.add_argument('--word',type=Path,default=BASE/'workers/A/proper-query-exports/WORD.json')
    ap.add_argument('--parent',type=Path,default=BASE/'workers/A/low-retention-corrections/WORD.json')
    ap.add_argument('--arithmetic',type=Path,default=BASE/'workers/C/four-plane-review/check.py')
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output')
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    global geo
    geo=load_arithmetic(a.arithmetic)
    native=a.native.read_bytes();need(hashlib.sha256(native).hexdigest()==NATIVE,'native pin')
    raw=a.word.read_bytes();need(hashlib.sha256(raw).hexdigest()==WORD,'word pin')
    parent=a.parent.read_bytes();need(hashlib.sha256(parent).hexdigest()==PARENT,'actual parent word pin')
    roots=json.loads(native)['native_roots'];w=json.loads(raw);need(w['construction']['parent_word_sha256']==PARENT,'declared parent')
    charts,correction,exports=derive(roots,w)
    stats,cv,ca=replay(w,charts,correction)
    need(stats['counts']=={'INIT':141,'ADD':539,'MOVE':520,'CLEAR':141},'complete primitive invoice')
    need(stats['movement_profile']=={1:187,2:111,3:4,4:111,5:16,6:16,7:75},'full movement profile')
    need(stats['owned_downward_profile']=={1:12}and stats['peak_owned']==stats['dirty_CLEAR']==141,'all owned charges')
    export_rows=[];payloads=[]
    for e in exports:
        z=next(z for z in w['construction']['query_exports']if z['query']==e['query'])
        row=e['sign_row'];n=z['export_field'];X=f"X{e['carrier_X']}";P=e['pair_chart']
        need(cv[n]==row and ca[n]==P and len(charts[P])==2,'pure query field at actual rank-two pair')
        need(cv[X]==(1<<e['carrier_X'])^row and ca[X]==P and cv[X].bit_count()==3,'actual three-term coded original at pair')
        support=tuple(tuple(roots[j])for j in range(111)if cv[X]>>j&1)
        need(len(geo.basis(support))==3 and not geo.contained(geo.basis(support),charts[P]),'genuinely nonlocal payload')
        export_rows.append(row);payloads.append({'query':e['query'],'carrier':X,'pair_chart':P,'export_row_hex':hex(row),
                                               'coded_original_row_hex':hex(cv[X]),'native_support_rank':3})
    K=[(1<<i)^sum(1<<j for j in range(111)if sum(a*b for a,b in zip(roots[i],roots[j]))==0)for i in range(111)]
    need(len(binary_basis(export_rows))==12 and len(binary_basis(K+export_rows))==21,'twelve independent new directions')
    union=0
    for r in export_rows:union|=r
    need(union.bit_count()==32,'actual exported input union')
    controls={}
    for label in ['actual_early_Y_baseline','actual_axis_delivery_snapshot','actual_corrected_Y_read','remove_actual_axis_delivery',
                  'one_rank_proper_export','actual_Y_baseline_unmask','actual_coded_original_load','actual_coded_original_inverse']:
        alt=json.loads(json.dumps(w));k=alt['semantic_operation_indices'][label][0]
        del alt['operations'][k]
        if k<alt['carrier_interface_before_operation']:alt['carrier_interface_before_operation']-=1
        try:replay(alt,charts,correction)
        except ValueError as err:controls[label]=str(err)
        else:raise ValueError('missing essential operation accepted: '+label)
    Q=geo.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in geo.moment(gate));room=(ceiling[0]-Q[1],ceiling[1]-Q[0])
    result={'status':'PASS_INDEPENDENT_ALL222_PROPER_QUERY_EXPORT_SOURCE','native_sha256':NATIVE,'word_sha256':WORD,'parent_sha256':PARENT,
            'cut':938,'stats':stats,'exported_rank':12,'canonical_plus_exported_rank':21,'exported_union':32,
            'original_X_rank':111,'corrected_Y_count':103,'foreign_coefficients':528,'completed_diagonal_outputs':0,
            'moment':record(Q),'necessary_limiting_room':record(room),'exports':payloads,'negative_controls':controls,
            'scope':'Actual twelve one-rank exports and ordered Hub inverse on all222 arbitrary columns, every characteristic-two field and whole-record width. No free global query bank or completed supplier.'}
    dest=a.out
    (dest/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    (dest/'INDEPENDENT-CUT.json').write_text(json.dumps([{'name':n,'chart':ca[n],'rank':len(charts[ca[n]]),'row_hex':hex(v)}for n,v in sorted(cv.items())],indent=2)+'\n')
    print(result['status'],'cut938,12 genuine nonlocal rank2 exports, all222 columns and inverses verified')

if __name__=='__main__':main()
