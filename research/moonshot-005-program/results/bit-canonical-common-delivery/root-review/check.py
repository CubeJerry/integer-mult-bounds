#!/usr/bin/env python3
"""Independent native-word, custody and invoice review of canonical lowering."""
from pathlib import Path
from fractions import Fraction
import argparse,copy,hashlib,importlib.util,json
from optimize_word import independent_replay
from review_leaf_capacity import chart_basis,echelon,binary_basis

BASE='7d2fea44d7bdf8b3a63807f88371cad28f9303649db66b7d4ccbb56e9c180ada'
PINS=['72317dffe82063e4db958c7b4025c490276d8339cbf11fd7041bc183ba991155','d2be3d2eb240377c3b42b4535fcf2b2977ef49b3a26f80dc5c296727fe72bd56']
CASES=[('P5','ZFIRST5','P5_RET','P5_K',[45,48,49]),('P4','ZFIRST4','P4_RET','P4_K',[29,40,42])]

def trace(w):
    v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};out=[]
    for op,n,*q in w['operations']:
        out.append((v.copy(),at.copy()))
        if op=='INIT':v[n]=0;at[n]=q[0]
        elif op=='ADD':v[q[0]]^=v[n]
        elif op=='MOVE':at[n]=q[0]
        elif op=='CLEAR':del v[n],at[n]
    return out

def main():
    p=argparse.ArgumentParser()
    for n in ['repo','base','one','two','out']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();base_raw=a.base.read_bytes();assert hashlib.sha256(base_raw).hexdigest()==BASE;old=json.loads(base_raw);baseline=independent_replay(old);src=(a.repo/old['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==old['source_sha256'];roots=json.loads(src)['native_roots']
    C={n:tuple(tuple(z for z in row)for row in echelon(chart_basis(rec))[0])for n,rec in old['charts'].items()}
    for i in range(111):
        assert len(C[f'L{i}'])==1 and len(echelon(list(C[f'L{i}'])+[roots[i]])[0])==1
        assert len(C[f'F{i}'])==7 and all(sum(x*y for x,y in zip(row,roots[i]))==0 for row in C[f'F{i}'])
    canonical=[(1<<i)^sum(1<<j for j in range(111)if sum(x*y for x,y in zip(roots[i],roots[j]))==0)for i in range(111)];cb=binary_basis(canonical);assert len(cb)==9
    oldstates=trace(old);oldcut=next(k for k,o in enumerate(old['operations'])if o[0]=='CLEAR');ov,oa=oldstates[oldcut]
    sp=importlib.util.spec_from_file_location('independent_exact_binary_root_invoice',a.repo/'research/moonshot-005-program/results/bit-composed-coded-source/author/price.py');price=importlib.util.module_from_spec(sp);sp.loader.exec_module(price)
    reports=[]
    for count,(path,pin)in enumerate(zip([a.one,a.two],PINS),1):
        raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==pin;w=json.loads(raw);assert w['base_word_sha256']==BASE and w['charts']==old['charts']and w['targets']==old['targets'];after=independent_replay(w);states=trace(w);cut=next(k for k,o in enumerate(w['operations'])if o[0]=='CLEAR');v,at=states[cut]
        selected=CASES[:count];exceptions={n for case in selected for n in case[:3:2]};checked=0
        for n,row in ov.items():
            if n not in exceptions:assert v[n]==row and C[at[n]]==C[oa[n]];checked+=1
        common=[];controls=[];captures=[]
        for packet,field,ret,chart,points in selected:
            row=ov[field];assert len(binary_basis(cb+[row]))==9
            assert v[packet]==v[ret]==v[field]==row and at[packet]=='zero'and C[at[ret]]==C[chart]and C[at[field]]==C['M1'];common.append(row)
            # The paired reset/load reads must actually occur at M1, from the
            # canonical owner while it is still live, and with zero packet.
            load=['ADD',field,packet];ix=next(k for k in range(len(w['operations'])-1)if w['operations'][k:k+2]==[load,load]);vv,aa=states[ix+1]
            assert vv[packet]==0 and vv[field]==row and C[aa[packet]]==C[aa[field]]==C['M1']
            for i in points:
                owner=f'CANON_OLD_RAW{i}';capture=['ADD',f'X{i}',owner];j=w['operations'].index(capture);cv,ca=states[j]
                assert cv[f'X{i}']==1<<i and cv[owner]==0 and C[ca[f'X{i}']]==C[ca[owner]]==C[f'L{i}'];assert v[owner]==1<<i and at[owner]=='zero';captures.append({'point':i,'source_step':j,'owner':owner})
                for omitted in [capture,['MOVE',owner,'zero'],['ADD',owner,f'Y{i}']]:
                    bad=copy.deepcopy(w);bad['operations'].remove(omitted)
                    try:independent_replay(bad)
                    except(AssertionError,KeyError)as error:controls.append({'omitted':omitted,'rejected':str(error)})
                    else:raise AssertionError(('Accepted omitted paid source',omitted))
            bad=copy.deepcopy(w);del bad['operations'][ix+1];independent_replay(bad);bc=next(k for k,o in enumerate(bad['operations'])if o[0]=='CLEAR');bv,ba=trace(bad)[bc];assert bv[packet]==bv[ret]==0
            controls.append({'omitted':'second M1 read','packet':packet,'endpoints_still_correct':True,'common_and_proper_canonical_source_contract_rejected':True})
            bad=copy.deepcopy(w);bad['operations'].remove(['ADD',packet,ret]);independent_replay(bad);bc=next(k for k,o in enumerate(bad['operations'])if o[0]=='CLEAR');bv,ba=trace(bad)[bc];assert bv[packet]==row and bv[ret]==0
            controls.append({'omitted':'proper retention capture','packet':packet,'endpoints_and_common_row_still_correct':True,'proper_retention_contract_rejected':True})
            probe=copy.deepcopy(w);probe['operations'][cut:cut]=[['ADD',packet,'P6'],['ADD',packet,'P6']];independent_replay(probe)
        assert len(binary_basis(common))==count
        for i in [8,9,36]:assert v[f'IMPORT_E{i}']==1<<i and C[at[f'IMPORT_E{i}']]==C['M1']
        for j in [3,4,5]:assert v[f'ZFIRST{j}']==ov[f'ZFIRST{j}']and C[at[f'ZFIRST{j}']]==C['M1']
        ground=[row for n,row in v.items()if not row>>111 and not C[at[n]]];oldground=[row for n,row in ov.items()if not row>>111 and not C[oa[n]]];known=sum(1<<i for i in w['targets'])
        intersection=lambda rows:len(binary_basis(rows))+9-len(binary_basis(rows+cb))
        assert intersection(oldground)==0 and intersection(ground)==count
        assert len(binary_basis(row&~known for row in oldground))==0 and len(binary_basis(row&~known for row in ground))==count
        diff={d:after['movement_profile'].get(d,0)-baseline['movement_profile'].get(d,0)for d in range(1,9)};diff={d:n for d,n in diff.items()if n};assert diff=={1:-3*count,5:-3*count,7:3*count};invoice=price.invoice(after['movement_profile']);author=json.loads(path.with_name('RESULT.json').read_text())
        for key in ['moment','limiting_room']:
            x=invoice[key];y=author['price'][key];assert Fraction(y['lower_fraction'])<=Fraction(x['lower_fraction'])<=Fraction(x['upper_fraction'])<=Fraction(y['upper_fraction'])
        reports.append({'word_sha256':pin,'all222_replay':after,'actual_live_common_cut':cut,'other_old_fields_checked':checked,'deliberately_changed_old_fields':sorted(exceptions),'actual_canonical_common_rows_hex':[hex(x)for x in common],'canonical_intersection_before_and_after':[0,count],'unfinished_common_quotient_before_and_after':[0,count],'native_raw_capture_custody':captures,'three_M1_canonical_and_three_raw_import_contracts_preserved':True,'real_common_read_unread_probes':count,'exact_signed_movement_difference':diff,'independent_invoice':invoice,'controls':controls})
    result={'status':'PASS_ROOT_INDEPENDENT_CANONICAL_COMMON_LOWERING','base_word_sha256':BASE,'native_source_sha256':old['source_sha256'],'method':'Separate Fraction native geometry and all222 replay, independent actual-source snapshots and binary fixed-point integer-root invoice; author builder/trace/checker not imported.','reports':reports,'scope':'Actual canonical source information is common with all46 old outputs paid and preserved. No additional receiver or complete supplier follows without its real proper correction. Binary identities lift to all characteristic-two fields and positive whole-record widths.','new_complete_kappa':False}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])

if __name__=='__main__':main()
