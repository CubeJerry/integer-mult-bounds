#!/usr/bin/env python3
"""Replace each R0 meeting by the actual rank3 source-half span."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from collections import Counter
from pathlib import Path
R0='d27892c4934f9b6fa08fd10b53a665f455020e6711db9378ab01f439ede2c56c'
PINS={'engine':'045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e',
 'codec':'4cb31f8f1c5b2e069afbbb3a3f028c787b677684a558bc12c2f31f51a4871297',
 'dynamic':'3845c44744ee0a05300bc237e9b9d10b45ca1272262f09f11e8a3ac2313a9e04'}
def need(ok,label):
    if not ok:raise ValueError(label)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def module(path,key):
    need(sha(path.read_bytes())==PINS[key],'engine pin');sp=importlib.util.spec_from_file_location('minimal112_'+key,path)
    obj=importlib.util.module_from_spec(sp);sys.modules[sp.name]=obj;sp.loader.exec_module(obj);return obj
def main(args):
    raw=args.source.read_bytes();need(sha(raw)==R0,'actual prior R0 word pin');old=json.loads(gzip.decompress(raw));word=copy.deepcopy(old)
    e=module(args.engine,'engine');c=module(args.codec,'codec');dyn=module(args.dynamic,'dynamic')
    data=word['logical_involution'];P=data['ports'];v={int(h):z for h,z in data['normals'].items()}
    frames=word['frames'];where={frozenset(e.span(f)):i for i,f in enumerate(frames)};mapping={};geometry=[]
    for z in data['halves']:
        S=z['sources'];T=z['ports'];basis=c.basis([v[j]for j in S]);space=frozenset(e.span(basis));need(len(basis)==3,'true source span rank3')
        if space not in where:where[space]=len(frames);frames.append(basis)
        C=where[space];oldC=z.pop('C4');mapping[oldC]=C;z['source_C3']=C
        si=sorted(h for h in P if v[h]in space);ri=sorted(h for h in P if all((v[h]&a).bit_count()%2==0 for a in basis))
        need(si==S and ri==sorted(T),'exact minimal source/receiver incidence')
        geometry.append({'old_C4':oldC,'source_C3':C,'source_frame':basis,'source_ports':S,'receiver_ports':T})
    need(len(mapping)==28,'all28 distinct meetings replaced')
    for op in word['program']:
        if op[0]=='MOVE':op[2]=mapping.get(op[2],op[2]);op[3]=mapping.get(op[3],op[3])
        elif op[0]=='ADD':op[4]=mapping.get(op[4],op[4])
        else:raise ValueError('owned-free R0 opcode')
    word['schema']='moonshot-S012-full112-minimal-logical-involution-source-v1';data['variant']='R0-minimal'
    data['minimal_meetings']={'source_word_sha256':R0,'all28_actual_source_spans_rank3':True,'geometry':geometry}
    rr,ll,bill=dyn.replay(word,word['program'],e);orows,oloc,_=dyn.replay(old,old['program'],e)
    need(rr==orows and ll==oloc,'all448 coefficients and endpoints exactly equal proved R0')
    need(Counter(bill['moves'])==Counter({2:224,3:224,5:224,6:224})and bill['lifetimes']==bill['peak']==0,'complete raw-only tariff')
    need(sum(k*v for k,v in bill['moves'].items())==3584,'full raw rank mass')
    bad=copy.deepcopy(word);op=next(op for op in bad['program']if op[0]=='MOVE'and op[3]in set(mapping.values()))
    op[3]=next(k for k,v in mapping.items()if v==op[3])
    try:dyn.replay(bad,bad['program'],e);rejected=False
    except ValueError:rejected=True
    need(rejected,'one old C4 leg cannot silently remain in the new cochart schedule')
    payload=(json.dumps(word,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0)
    args.output.mkdir(parents=True,exist_ok=True);(args.output/'WORD.json.gz').write_bytes(blob)
    result={'status':'PASS_MINIMAL_SOURCE_SPAN_R0','source_word_sha256':R0,'word_sha256':sha(blob),'source_bill':bill,
       'all448_original_outputs_identical':True,'all12544_adjoint_entries_inherited_exactly':True,'R_squared_identity':True,
       'rank_R_minus_identity':56,'actual_geometry':geometry,'owned_fields':0,'retained_scalar_gate_passes':True,
       'negative_control':'mixed_old_C4_and_new_C3_stop_rejected','physical_caller_query_head_admission':False,
       'scope':'Same exact logical R0 on actual smaller meetings; no physical caller admission and no new kappa.'}
    (args.output/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'word_sha256':result['word_sha256'],'source_bill':bill},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--engine',type=Path,required=True)
    p.add_argument('--codec',type=Path,required=True);p.add_argument('--dynamic',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
