#!/usr/bin/env python3
"""Independent Fraction-chart and full-column review of source-wide triples."""
from pathlib import Path
from fractions import Fraction
import argparse,copy,hashlib,importlib.util,json
from optimize_word import independent_replay
from review_leaf_capacity import chart_basis,echelon

CASES=[('P2',12,39,8,'J22','PRIVATE22','RAW_J39','KEEP_M22',['E77']),('P1',11,38,9,'J23','PRIVATE23','RAW_J38','KEEP_M23',[]),('P0',7,30,36,'J16','PRIVATE16','RAW_J30','KEEP_M16',[])]
PINS=['0fa6fd43de9e1782168ed811f39110cfd58f8035f5e90fc81c92c859fd2df96c','f4a27a72484db22126f93cd7d8544e60b26bf5d6138f734bc66985a5e8c8a75f','6427be84494f45664aa3312ade2955b6d694e7eab475804c4262faf05a4af01a','45479de20faad9d9cd4ace9493057b82fb2c8b6f8baa4ac67134571f2e5cca84']

def snapshot(w,anchor):
    v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
    at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    for op,n,*q in w['operations']:
        if [op,n,*q]==anchor:return v,at
        if op=='INIT':v[n]=0;at[n]=q[0]
        elif op=='ADD':v[q[0]]^=v[n]
        elif op=='MOVE':at[n]=q[0]
        elif op=='CLEAR':del v[n],at[n]
    raise AssertionError(anchor)

def main():
    p=argparse.ArgumentParser()
    for n in ['repo','base','stages','out']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();paths=[a.base]+[a.stages/f'outputs{i}/WORD.json'for i in [44,45,46]]
    words=[];reports=[]
    for path,pin in zip(paths,PINS):
        raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==pin;w=json.loads(raw)
        src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];roots=json.loads(src)['native_roots']
        charts={n:chart_basis(c)for n,c in w['charts'].items()};assert not charts['zero']and len(charts['Hub'])==8
        for i in range(111):
            assert len(charts[f'L{i}'])==1 and len(echelon(charts[f'L{i}']+[roots[i]])[0])==1
            assert len(charts[f'F{i}'])==7 and all(sum(x*y for x,y in zip(row,roots[i]))==0 for row in charts[f'F{i}'])
        words.append(w);reports.append(independent_replay(w))
    price_path=a.repo/'research/moonshot-005-program/results/bit-composed-coded-source/author/price.py';sp=importlib.util.spec_from_file_location('independent_binary_root_price',price_path);price=importlib.util.module_from_spec(sp);sp.loader.exec_module(price)
    results=[]
    for j,case in enumerate(CASES):
        packet,x,b,c,J,private,raw_old,keep,masks=case;old,w=words[j:j+2];before,after=reports[j:j+2]
        assert w['base_word_sha256']==PINS[j]and set(w['targets'])==set(old['targets'])|{c}and c not in old['targets']
        assert not any(o[0]=='ADD'and o[2]==f'X{b}'for o in old['operations'])
        ov,oa=snapshot(old,['INIT','P7','D3_21']);nv,na=snapshot(w,['INIT','P7','D3_21'])
        exceptions={raw_old,f'IMPORT_E{c}',f'X{b}'};count=0
        for name,value in ov.items():
            if name in exceptions:continue
            assert nv[name]==value^((1<<c)if(value>>b)&1 else 0),(j,name)
            count+=1
        fv,fa=snapshot(w,['MOVE','Y16','SH2']);imp=f'IMPORT_E{c}';K=f'{packet}_E{c}_K'
        assert fv[imp]==fv[keep]==(1<<b)^(1<<c)and fa[imp]==J and fa[keep]==K
        code=fv[packet]
        for name in masks:code^=fv[name]
        assert code==(1<<x)^(1<<b)^(1<<c)
        assert all(sum(u*v for u,v in zip(roots[i],roots[k]))==0 for i in [x,b,c]for k in [x,b,c]if i!=k)
        difference={d:after['movement_profile'].get(d,0)-before['movement_profile'].get(d,0)for d in range(1,9)};difference={d:n for d,n in difference.items()if n}
        assert difference=={1:8,2:2,3:-3,4:2,5:2,6:-1,7:-2}
        author=json.loads((a.stages/f'outputs{44+j}/RESULT.json').read_text());bill=price.invoice(after['movement_profile'])
        for key in ['moment','limiting_room']:
            z=author['price'][key];r=bill[key]
            assert Fraction(z['lower_fraction'])<=Fraction(r['lower_fraction'])<=Fraction(r['upper_fraction'])<=Fraction(z['upper_fraction'])
        bad=copy.deepcopy(w);removed=[]
        for destination in author['source_substitution']['actual_Hub_loads_with_extra_c_read']:
            op=['ADD',f'X{c}',destination];assert op in bad['operations'];bad['operations'].remove(op);removed.append(op)
        controls=[]
        try:independent_replay(bad)
        except (AssertionError,KeyError)as error:controls.append({'one_sided_Hub_omissions':removed,'failure':str(error)})
        else:raise AssertionError('Unmatched Hub substitution passed')
        for omitted in [['ADD',f'X{b}',imp],['MOVE',imp,J],['ADD',keep,f'Y{c}']]:
            bad=copy.deepcopy(w);bad['operations'].remove(omitted)
            try:independent_replay(bad)
            except (AssertionError,KeyError)as error:controls.append({'omitted':omitted,'failure':str(error)})
            else:raise AssertionError(('Lost source/decoder accepted',omitted))
        results.append({'word_sha256':PINS[j+1],'base_word_sha256':PINS[j],'triple':[x,b,c],'after':after,'inherited_fields_checked_at_actual_source_cut':count,'exceptions':sorted(exceptions),'actual_import_chart':J,'actual_retention_chart':K,'actual_common_code_hex':hex(code),'signed_movement_difference':difference,'independent_invoice':bill,'negative_controls':controls})
    result={'status':'PASS_ROOT_INDEPENDENT_SOURCEWIDE_TRIPLE_CHAIN','method':'Separate Fraction geometry and all222-column interpreter; binary fixed-point exact200th-root invoice. No author construction/checker imported.','native_source_sha256':words[0]['source_sha256'],'base43_replay':reports[0],'stages':results,'universal_scope':'Written substitution induction and finite literal binary identities lift to every characteristic-two field/width. No all111 source or complete kappa.','new_complete_kappa':False}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])

if __name__=='__main__':main()
