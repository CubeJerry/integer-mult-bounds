"""Independent source-contract audit using the earlier independent interpreter.

No current author builder, helpers, rank code, or invoices are imported.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--word',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args()
    module=a.repo/'research/moonshot-005-program/sessions/2026-11-17-S019/checkpoint3-evidence/C/portable/audit_cp6.py'
    spec=importlib.util.spec_from_file_location('independent_prior',module)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    need=m.insist
    word=json.loads(a.word.read_text())
    raw=a.repo/word['source_path']
    need(m.sha(raw)==word['source_sha256']=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','native source pin')
    source=json.loads(raw.read_text());roots=source['native_roots']
    cut=word['carrier_interface_before_operation']
    stats,snap,charts,events=m.replay(word,source,[cut])
    values,locations=snap[cut]
    known=set(word['targets']);unknown=set(range(111))-known
    need(len(known)==57 and len(unknown)==54,'57/54 split')
    old=a.repo/'research/moonshot-005-program/sessions/2026-11-16-S018/checkpoint5-evidence/R/initial-chart-cut/control/NATIVE-CACHED57-WORD.json'
    need(m.sha(old)=='7df1fc8f696545185c417c6df4161b324869bf084b503138506425510e841fa2','known-set source pin')
    need(known==set(json.loads(old.read_text())['targets']),'same57 known set')
    need(cut==1269 and len(values)==408,'actual new source cut')
    c=word['construction'];pairs=c['pairs'];used=set()
    need({p['unknown'] for p in pairs}==unknown and len(pairs)==54,'one proxy per unknown')
    for p in pairs:
        u,k,H=p['unknown'],p['known'],p['chart']
        need(k in known and k not in used,'injective known pairing');used.add(k)
        expected=m.chart({'kind':'span','rows':[roots[u],roots[k]]})
        need(charts[H]==expected and len(expected)==2,'exact pair chart')
        need(values[f'X{u}']=={u} and charts[locations[f'X{u}']]==expected,'held actual raw unknown')
        need(values[f'X{k}']=={u,k} and locations[f'X{k}']=='Hub','actual masked proxy at Hub')
    for i in range(111):
        need(values[f'NATIVE_{i}']=={i} and locations[f'NATIVE_{i}']==f'L{i}','all111 native caches')
        need(values[f'Y{i}']==({111+i,i} if i in known else {111+i}),'every initial Y column retained')
        need(locations[f'Y{i}']==(f'F{i}' if i in known else 'zero'),'actual Y source locations')
    need(len(known-used)==3 and all(values[f'X{i}']=={i} and locations[f'X{i}']==f'L{i}' for i in known-used),'three unused known originals remain native')
    need(len(m.binary_basis(values[f'X{i}'] for i in range(111)))==111,'original transformation invertible')
    need(len(m.binary_basis(values[f'X{k}'] & unknown for k in used))==54,'actual unknown quotient at Hub')
    for i in known:
        need(values[f'GROUND_{i}']=={i} and locations[f'GROUND_{i}']=='zero','actual ground known source')
    neighbours={i:{j for j in unknown if sum(x*y for x,y in zip(roots[i],roots[j]))==0} for i in unknown}
    canonical={i:{i}^neighbours[i] for i in unknown}
    code=[]
    for h,g,i in zip(c['Hub_source_fields'],c['ground_correction_fields'],c['masked_canonical_basis_roles']):
        need(locations[h]=='Hub' and locations[g]=='zero','code and correction have distinct actual custody')
        need(values[g]<=known,'ground correction uses only known values')
        need(values[h]^values[g]==canonical[i],'actual canonical payload identity')
        code.append(values[h]^values[g])
    basis=m.binary_basis(code)
    need(len(code)==9 and len(basis)==9 and all(m.in_span(r,basis) for r in canonical.values()),'all54 canonical equations span exact9')
    # Reconstruct every receiver source from every live field, without names.
    access={i:set() for i in unknown}
    for name,row in values.items():
        for i in unknown:
            if m.subset(charts[locations[name]],charts[f'F{i}']):access[i]|=row&unknown
    need(access==neighbours,'all408 fields give exactly native unknown side information')
    frame=[52,82,98,101,106,107,57,85]
    need(set(frame)<=unknown and all(sum(x*y for x,y in zip(roots[i],roots[j]))!=0 for i in frame for j in frame),'independent eight-frame')
    inside=[n for n in values if any(m.subset(charts[locations[n]],charts[f'F{i}']) for i in frame)]
    need(all(not(values[n]&set(frame)) for n in inside),'fresh nonlinear downset zero-source premise')
    expected={'INIT':186,'ADD':861,'MOVE':387,'CLEAR':186}
    need(stats['counts']==expected and stats['dirty_clear']==186,'complete closed partial-word operation bill')
    need(stats['movement_profile']=={1:165,6:108,7:114},'directly reconstructed movement bill')
    need(sum(e[-1] for e in events)==57,'only57 original known descents; every other owned record stationary')
    q=m.moment(stats['movement_profile'])
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in m.moment(gate));room=(ceiling[0]-q[1],ceiling[1]-q[0])
    controls=[]
    for label in ['native_capture','known_capture','known_endpoint','known_proxy_encoding','masked_source_read','known_correction_read','actual_proxy_inverse']:
        index=word['semantic_operation_indices'][label][0]
        bad=copy.deepcopy(word);bad['operations'].pop(index)
        position=cut-(index<cut)
        try:
            _,bs,_,_=m.replay(bad,source,[position])
            need(bs[position][0]==values and bs[position][1]==locations,'source contract changed')
        except (ValueError,KeyError) as ex:controls.append({'removed':label,'index':index,'rejected':str(ex)})
        else:raise ValueError('omission control accepted: '+label)
    out={'status':'PASS_INDEPENDENT_ALL54_HELD_SOURCE','word_sha256':m.sha(a.word),'interpreter_sha256':m.sha(module),'source_sha256':m.sha(raw),'cut':cut,'live_fields':len(values),'stats':stats,'canonical_rank':9,'unknown_Hub_rank':54,'source_native_access_exact':True,'eight_lifetime_nonlinear_premise':{'frame':frame,'inside_fields':len(inside),'all_projection_zero':True},'moment':m.interval_json(q),'necessary_room':m.interval_json(room),'negative_controls':controls,'scope':'Exact source and full closed partial-word bill; every positive record width in characteristic2. No actual code delivery, complete supplier, or new kappa.'}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    (a.out/'ACCESS.json').write_text(json.dumps({str(i):sorted(v) for i,v in access.items()},indent=2,sort_keys=True)+'\n')
    print(out['status']);print(out['moment']['decimal']);print(out['necessary_room']['decimal'])

if __name__=='__main__':main()
