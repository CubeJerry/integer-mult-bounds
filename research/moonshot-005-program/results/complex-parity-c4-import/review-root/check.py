#!/usr/bin/env python3
"""Independent C4 chronology, complete source map and tariff review.

Source replay and arithmetic helpers are credited earlier root code.
No author builder, checker, interval engine or codec compiler is imported.
"""
import argparse, copy, gzip, hashlib, importlib.util, json, sys
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path
import engine
from helpers import need, rank, determinant, root_vector
from interval_helpers import add, moment

def read(path, pin=None):
    raw=path.read_bytes()
    if pin:need(hashlib.sha256(raw).hexdigest()==pin,'frozen source '+str(path))
    return json.loads(gzip.decompress(raw) if path.suffix=='.gz' else raw)

def main():
    parser=argparse.ArgumentParser()
    for s in ['package','repo','output']:parser.add_argument('--'+s,type=Path,required=True)
    args=parser.parse_args();p=args.package;prog=args.repo/'research/moonshot-005-program/results'
    need(hashlib.sha256((p/'PROOF.md').read_bytes()).hexdigest()=='0ca673d3c07db694d24180c992ec73c19975594717a50ac4fc1cbeafcd8e04ce','frozen reviewed proof')
    native=read(p/'dependencies/native.json.gz','2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883')
    seed=read(prog/'complex-omitted-line-gram/author/output/WORD.json.gz','6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc')
    old=read(prog/'complex-parity-half-layer/author/output/WORD.json.gz','f72c890e06437c3b6a177c71019f56e60f30712e5c09c1e241c893c1f180e42d')
    base=engine.replay(seed);old_result=engine.replay(old)
    role={int(k):v for k,v in seed['source_role_map'].items()};live=native['live']
    pair={live[i]:(role[b],role[d]) for i,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2'])}
    coupled=sorted(set(live)-set(pair));need(17 in coupled and len(coupled)==8,'authentic coupled import port')
    roots={h:root_vector(native['frames'][native['initial'][h]][0]) for h in live}
    labels={h:native['frames'][native['initial'][h]][0] for h in live}
    G={(h,j):F(sum(x*y for x,y in zip(roots[h],roots[j])),18) for h in live for j in live}
    modes=[root_vector(v) for v in seed['duplex']['omitted_frame']]
    g=[{h:F(sum(x*y for x,y in zip(v,roots[h])),18) for h in live} for v in modes]
    classes=defaultdict(list)
    for h in live:classes[tuple(i for i in range(8) if g[i][h])].append(h)
    need(len(classes)==14 and all(len(k)==4 for k in classes),'independently derived14 four-mode classes')
    class_id={h:k for k,hs in classes.items() for h in hs}
    halves={}
    for k,hs in classes.items():
        for sign in [-1,1]:
            selected=[h for h in hs if ((-1)**sum(g[i][h]<0 for i in k))==sign]
            need(len(selected) in [3,4],'authentic parity half size')
            for h in selected:halves[h]=frozenset(selected)
    K={(h,j):(G[h,j] if class_id[h]!=class_id[j] else F(0)) for h in live for j in live}
    a={h:base[0][role[h]] for h in live};c={h:F(1) if h in pair else F(1,2) for h in live}
    forward=[];reverse=[]
    for i in range(8):
        f={};r={}
        for h in live:f=engine.plus(f,a[h],g[i][h])
        for h in pair:r=engine.plus(r,{pair[h][1]:F(1)},g[i][h])
        forward.append(f);reverse.append(r)
    need(rank(forward)==8 and rank(forward+[a[17]])==9,'specified exported Gram/import span')
    original_expected={}
    for h in live:
        original_expected[role[h]]=a[h]
        y={role[h+112]:F(1)}
        for j in live:y=engine.plus(y,a[j],c[h]*(F(h==j)+K[h,j]))
        original_expected[role[h+112]]=y
    for j,(b,d) in pair.items():
        row={b:F(1)}
        for h in pair:row=engine.plus(row,{pair[h][1]:F(1)},-F(h==j)-K[h,j])
        original_expected[b]=row;original_expected[d]={d:F(1)}
    need(old_result[0]==original_expected,'credited parity full map rederived from native roots')
    phase_path=prog/'complex-omitted-line-gram/author/dependencies/native_verify.py'
    phase_pin='3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'
    need(hashlib.sha256(phase_path.read_bytes()).hexdigest()==phase_pin,'retained phase interpreter pin')
    spec=importlib.util.spec_from_file_location('root_c4_retained_phase_interpreter',phase_path)
    phase_engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=phase_engine;spec.loader.exec_module(phase_engine)
    all_variants=[]
    for variant,pin,extra in [('base','24962e2c3ee68dac4398bd6e5d63ce0607805ed164219d205b33455cf9691718',0),('imported','ffb3b895a928c13dc62e9ce73cf41e7db821cdb24eb5f8769369ebb20571120c',1)]:
        path=p/f'output/{variant}/WORD.json.gz';w=read(path,pin);meta=w['C4_compiler'];spaces=[engine.span(f) for f in w['frames']]
        need(meta['import_port']==(17 if extra else None),'declared actual import')
        expected=copy.deepcopy(original_expected)
        if extra:
            for h in live:expected[role[h+112]]=engine.plus(expected[role[h+112]],a[17],-c[h]*K[h,17])
        groups=meta['groups'];need(len(groups)==14 and {frozenset(q['ports']) for q in groups}=={frozenset(v) for v in classes.values()},'complete literal classes; hosted-first codec ordering retained separately')
        dets=[]
        for q in groups:
            oldq=next(x for x in seed['duplex']['groups'] if x['ports']==q['ports'])
            for key in ['M_D','M_Y']:
                need(q[key]==oldq[key],'full old codec retained literally')
                val=determinant(q[key]);need(val!=0,'invertible full old codec');dets.append(str(val))
        cache={int(h):v for h,v in meta['cache_roles'].items()};need(set(cache)==set(live),'one stationary correction cache per port')
        cache_values={};geo=[]
        for half in meta['halves']:
            hs=half['ports'];opposite=sorted(set(classes[class_id[hs[0]]])-set(hs));C3=half['C3'];C4=half['C4']
            need(frozenset(hs)==halves[hs[0]] and opposite==half['opposite_ports'],'independent full parity partition')
            need(len(w['frames'][C3])==3 and len(w['frames'][C4])==4,'minimal station dimensions')
            required=set(spaces[C3])
            for j in opposite:required|={v^labels[j] for v in tuple(required)}
            need(spaces[C4]==required,'C4 is exactly old reunion plus required source lines')
            source=[j for j in live if labels[j] in spaces[C4]]
            receivers=[h for h in live if spaces[C4]<=spaces[base[1][role[h+112]]]]
            need(source==opposite and receivers==hs,'complete actual source and receiver incidence')
            need(all(spaces[C3]<spaces[C4]<spaces[base[1][role[h+112]]] for h in hs),'proper chart nesting for every receiver')
            for h in hs:
                v={}
                for j in opposite:v=engine.plus(v,a[j],-c[h]*G[h,j])
                cache_values[cache[h]]=v
            geo.append(dict(half=hs,sources=source,receivers=receivers,rank=4))
        before_checks=Counter();after_checks=Counter();private_direction={};private_mass=Counter();d_c3={};y_c3={};half_ready={}
        for q in groups:
            d_c3[q['markers']['D_restored_at_C3']]=q
            y_c3[q['markers']['full_class_Y_decoded_at_C3']]=q
        for q in meta['halves']:half_ready[q['markers']['actual_source_caches_ready']]=q
        ev=meta['events'];evsets={k:set(v) for k,v in ev.items() if isinstance(v,list)};marks=meta['markers']
        def hook(t,when,o,rows,loc):
            if when=='before':
                if t in evsets.get('correction_sources',set()):need(rows[o[2]]==a[next(h for h in live if role[h]==o[2])],'cache reads actual original a');before_checks['correction_sources']+=1
                if t in evsets.get('local_reverse_reads',set()):need(rows[o[2]]=={o[2]:F(1)},'paired local read uses original D');before_checks['local_reverse']+=1
                if t in evsets.get('old_reverse_consumers',set()):need(rows[o[2]]==reverse[o[2]-400],'old reverse consumer has actual mode');before_checks['reverse_consumers']+=1
                if t in evsets.get('old_forward_reads',set()):need(rows[o[2]]==forward[o[2]-400],'old forward consumer has actual mode');before_checks['forward_consumers']+=1
                if t in evsets.get('correction_reads',set()):need(rows[o[2]]==cache_values[o[2]],'actual correction cache final read');before_checks['cache_reads']+=1
                if t in evsets.get('import_receiver_reads',set()):need(rows[o[2]]==a[17] and loc[o[2]]==w['initial'][role[17+112]],'paid import actually at ground');before_checks['ground_import_reads']+=1
                return
            if o[0]=='MOVE' and not o[-1]:
                _,i,C,D,_=o;direction=1 if spaces[C]<spaces[D] else -1
                need(private_direction.get(i,direction)==direction,'every public route remains monotone')
                private_direction[i]=direction;private_mass[i]+=abs(len(w['frames'][D])-len(w['frames'][C]))
            if t in d_c3:
                q=d_c3[t];need(all(rows[pair[h][1]]=={pair[h][1]:F(1)} and loc[pair[h][1]]==q['C'] for h in q['hosted']),'original D restored at class reunion');after_checks['D_class_restore']+=1
            if t in y_c3:
                q=y_c3[t]
                for h in q['ports']:
                    want={role[h+112]:F(1)}
                    for j in live:want=engine.plus(want,a[j],c[h]*G[h,j])
                    if extra:want=engine.plus(want,a[17],-c[h]*K[h,17])
                    need(rows[role[h+112]]==want and loc[role[h+112]]==q['C'],'full-class original-Y decode before half split')
                after_checks['Y_class_decode']+=1
            if t in half_ready:
                q=half_ready[t];need(all(rows[cache[h]]==cache_values[cache[h]] and loc[cache[h]]==q['C4'] for h in q['ports']),'local cache formed at real C4');after_checks['half_caches']+=1
            if t==marks['all_original_D_at_C4_and_old_reverse_modes_acquired']:
                need(all(rows[400+i]==reverse[i] for i in range(8)),'eight old reverse modes exact')
                need(all(rows[d]=={d:F(1)} for b,d in pair.values()),'all D original at C4');after_checks['reverse_bank']+=1
            if t==marks['all_XB_at_Hub_and_D_original_at_endpoints']:
                need(all(rows[role[h]]==a[h] for h in live),'all X unaltered through C4')
                need(all(rows[d]=={d:F(1)} and loc[d]==base[1][d] for b,d in pair.values()),'original D final endpoints');after_checks['X_D_endpoints']+=1
            if t==marks['all_old_forward_modes_at_lines']:
                need(all(rows[400+i]==forward[i] and loc[400+i]==meta['lines'][i] for i in range(8)),'old forward bank physically available');after_checks['forward_bank']+=1
            if extra:
                if t==marks['all_coupled_a_created_before_import']:need(all(rows[role[h]]==a[h] for h in coupled),'all coupled entries precede shifted Y');after_checks['all_coupled_entries']+=1
                if t==marks['entry_owner_contains_original_x']:need(rows[400]=={role[17]:F(1)} and loc[400]==w['initial'][role[17]],'actual x17 pickup at line');after_checks['original_x_pickup']+=1
                if t==marks['imported_original_a_at_ground']:need(rows[400]==a[17] and loc[400]==w['initial'][role[17+112]],'actual a17 restored at ground');after_checks['ground_a']+=1
        result=engine.replay(w,hook=hook)
        need(result[0]==expected and result[1]==base[1],'all400 rows and exact endpoint IDs')
        need(rank(result[0].values())==400,'all400 independent arbitrary inputs preserved')
        need(len(private_mass)==400 and sum(private_mass.values())==3200,'all400 public route masses retained')
        need(result[2]=={1:312,2:112,3:288,4:200,5:200} and result[3]=={1:8+extra,8:16},'actual complete raw and owned profiles')
        need(result[5]==112 and result[6]==128 and len(result[8])==128 and all(row for _,_,_,row in result[8]),'all nonzero retirements and exact peaks/lifetimes')
        paired=0
        for h in pair:
            for j in pair:
                need(result[0][pair[j][0]].get(pair[h][1],F(0))+result[0][role[h+112]].get(role[j],F(0))==0,'all hosted adjoint coefficients')
                paired+=1
        residual=[engine.plus(engine.plus(result[0][b],{b:F(1)},-1),{d:F(1)},1) for b,d in pair.values()]
        need(rank(residual)==56,'credited hosted residual rank unchanged')
        deleted=[h for h in live if K[h,17]];need(len(deleted)==44,'complete imported cross-class column size')
        debt=sum(bool(K[h,j]) for h in live for j in live)-(44 if extra else 0)
        original_debt=0
        for h in live:
            target=engine.plus({role[h+112]:F(1)},a[h],c[h])
            original_debt+=len(engine.plus(result[0][role[h+112]],target,-1))
        need(debt==(4564 if extra else 4608) and original_debt==(4874 if extra else 4962),'actual residual coefficient counts')
        for o in w['program']:
            if o[0] in ['ADD','SCALE']:
                den=F(o[3] if o[0]=='ADD' else o[2]).denominator;need(den&(den-1)==0,'emitted dyadic coefficients')
        negatives=[]
        for key in ['correction_sources','local_reverse_reads','old_reverse_consumers','old_forward_reads','correction_reads']+(['entry_pickup','import_cleanup','import_receiver_reads'] if extra else []):
            indices=ev[key];idx=indices[0] if isinstance(indices,list) else indices;bad=copy.deepcopy(w);need(bad['program'][idx][0]=='ADD','semantic mutant target');bad['program'][idx][3]='0'
            need(engine.replay(bad)[0]!=expected,'omitted actual source changes full map '+key);negatives.append(key)
        if extra:
            bad=copy.deepcopy(w);del bad['program'][ev['import_move']]
            try:engine.replay(bad)
            except ValueError as e:need('chart' in str(e),'missing import rejected by chart dependency');negatives.append('actual_import_move')
            else:raise ValueError('missing import MOVE erroneously accepted')
        oldpairs={(o[2],o[3]) for o in seed['program'] if o[0]=='MOVE'};newpairs={(o[2],o[3]) for o in w['program'] if o[0]=='MOVE'}-oldpairs
        phase=read(p/f'output/{variant}/PHASES.json');need(len(newpairs)==(265 if extra else 264)==phase['map_count'],'all introduced chart-pair counts')
        recs=phase['recipes'];need(len(recs)==len(newpairs) and {(q['source'],q['target']) for q in recs}==newpairs,'exact complete recipe pair coverage')
        for q in recs:
            C,D=q['source'],q['target'];f0,f1=w['frames'][C],w['frames'][D]
            need(q['source_frame']==f0 and q['target_frame']==f1 and q['rank']==abs(len(f1)-len(f0))==q['recipe']['rank'],'actual source/target recipe frames and rank')
            phase_engine.equal(phase_engine.recipe(q['recipe']),phase_engine.adjoint(phase_engine.frame(f0,9))+phase_engine.frame(f1,9),'retained-interpreter C4 recipe reproduction')
        badphase=copy.deepcopy(recs[0]);badphase['recipe']['left']['phase']=(badphase['recipe']['left']['phase']+1)%4
        try:phase_engine.equal(phase_engine.recipe(badphase['recipe']),phase_engine.adjoint(phase_engine.frame(badphase['source_frame'],9))+phase_engine.frame(badphase['target_frame'],9),'wrong global phase')
        except ValueError:pass
        else:raise ValueError('wrong global phase was not rejected')
        author=read(p/f'output/{variant}/RESULT.json')
        need(result[4]==author['source_bill']['counts'],'independent full ordinary-operation counts')
        all_variants.append(dict(variant=variant,word_sha256=pin,all400_rows=True,all_endpoint_ids=True,input_rank=400,paired_entries=paired,raw=result[2],owned=result[3],counts=result[4],peak=result[5],lifetimes=result[6],dirty_retirements=len(result[8]),geometric_stations=geo,codec_determinants=dets,before_chronology_checks=dict(before_checks),after_chronology_checks=dict(after_checks),current_a_debt=debt,original_coordinate_debt=original_debt,hosted_residual_rank=56,specified_exported_history_rank=8+extra,new_ordered_chart_pairs=len(newpairs),phase_reproduction=dict(interpreter_sha256=phase_pin,wrong_global_phase_rejected=True,classification='retained interpreter reproduction, not a new independent phase algorithm'),negative_controls=negatives))
    full=read(p/'dependencies/FULL-RESULT.json','d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7')
    slope=add((F(1,18),full['invoice']['T']),(F(-1,18),full['invoice']['P']));penalty=moment(add((-1,slope)))
    seedQ=add((1,base[2]),(1,base[3]));oldQ=add((1,old_result[2]),(1,old_result[3]))
    capacity=add((1,slope),(1,full['native']['paid']),(-1,full['native']['helpers']));seedroom=moment(add((1,capacity),(-1,seedQ)))
    prices=[];author_price=read(p/'output/PRICE.json')
    for v,extra in zip(all_variants,[0,1]):
        Q=add((1,v['raw']),(1,v['owned']));delta=add((200+extra,{1:1}),(200,{3:1,4:1}),(-200,{8:1}))
        need(add((1,Q),(-1,seedQ))==delta,'independently recounted delta formula')
        inc=moment(delta);room=moment(add((1,capacity),(-1,Q)));first=next(m for m in range(2,1000) if room[0]>penalty[1]/(m-1))
        need(room[1]<penalty[0]/(first-2),'preceding fixed m rigorously fails')
        previous=author_price['variants'][extra]
        for val,key in [(inc,'increment_from_seed'),(room,'limiting_room')]:
            lo,hi=map(F,previous[key]);need(val[0]<=lo<=hi<=val[1],'independent200th-power enclosure')
        need(first==previous['first_positive_fixed_m'],'exact first fixed m')
        prices.append(dict(variant=v['variant'],increment=list(map(str,inc)),limiting_room=list(map(str,room)),room_decimal=float(room[0]),first_positive_m=first))
    refund=moment(add((1,oldQ),(-1,add((1,all_variants[0]['raw']),(1,all_variants[0]['owned'])))))
    need(refund[0]>0,'real tariff refund from changed chronology')
    two=moment(add((1,capacity),(-1,add((1,all_variants[0]['raw']),(1,all_variants[0]['owned']))),(-2,{1:1})))
    need(two[1]<0,'two genuine unit imports exceed retained room')
    report=dict(status='PASS_INDEPENDENT_C4_AND_REAL_IMPORT_REVIEW',proof_sha256=hashlib.sha256((p/'PROOF.md').read_bytes()).hexdigest(),variants=all_variants,prices=prices,finite_m_penalty=list(map(str,penalty)),seed_room=list(map(str,seedroom)),refund_from_old_parity=list(map(str,refund)),two_extra_unit_returns_room=list(map(str,two)),scope='Independent exact source chronology and complete paired maps, universal vector-linear proof review and independent integer-power prices. Phase interpretation is separate retained-engine reproduction. All foundations and remaining cross-class source completion retained; no new kappa.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n');print(report['status'])

if __name__=='__main__':main()
