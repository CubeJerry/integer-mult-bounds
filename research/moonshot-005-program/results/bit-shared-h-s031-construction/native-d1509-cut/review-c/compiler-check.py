"""Independent bit-packed reconstruction of all supplied phase words and cache bills."""
import argparse,gzip,hashlib,json,struct
from pathlib import Path
import numpy as np

def need(x,m):
    if not x:raise AssertionError(m)
def read(p):return json.loads(gzip.decompress(p.read_bytes()))if p.suffix=='.gz'else json.loads(p.read_text())
def mul(x,y):
    z=0
    for bit in range(6):
        if y>>bit&1:z^=x
        x<<=1
        if x&64:x^=67
    return z
TABLE=np.array([[mul(x,y)for y in range(64)]for x in range(64)],dtype=np.uint8)
def binary(A):
    A=np.asarray(A,dtype=np.uint8);n,m=A.shape;C=TABLE[A[:,:,None],(1<<np.arange(6))[None,None,:]];return((C[:,:,None,:]>>np.arange(6)[None,None,:,None])&1).transpose(0,2,1,3).reshape(6*n,6*m).astype(np.uint8)
WEIGHT=np.array([int(binary(np.array([[v]],dtype=np.uint8)).sum())for v in range(64)],dtype=np.uint64)
def eliminate(A):
    B=binary(A);n=len(B);packed=np.packbits(B,axis=1,bitorder='little');rows=[int.from_bytes(r.tobytes(),'little')for r in packed];digest=hashlib.sha256();buffer=bytearray();count=0
    def add(t,s):
        nonlocal count
        need(t!=s,'distinct owned ADD records');rows[t]^=rows[s];buffer.extend(struct.pack('<II',t,s));count+=1
        if len(buffer)>=32768:digest.update(buffer);buffer.clear()
    for q in range(n):
        bit=1<<q
        if not rows[q]&bit:
            p=next(r for r in range(q+1,n)if rows[r]&bit);add(q,p);add(p,q);add(q,p)
        for r in range(n):
            if r!=q and rows[r]&bit:add(r,q)
    need(rows==[1<<q for q in range(n)],'binary matrix eliminated exactly');digest.update(buffer)
    return {'field_dimension':len(A),'binary_dimension':n,'ADD_per_direction':count,'elimination_word_uint32le_sha256':digest.hexdigest()}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--package',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();base=args.repo.resolve()/'research/moonshot-005-program/results';p=args.package;s=read(p/'output/SOURCES.json.gz');early=read(p/'output/EARLY.json.gz');hs=read(p/'output/H-PHYSICAL.json.gz');d=read(p/'output/D-WORD.json.gz');receipts=read(p/'output/PHASE-COMPILER-RECEIPTS.json.gz');bill=read(p/'output/COMPILER-RESULT.json');old=read(base/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/COEFFICIENTS.json.gz');routes=[json.loads(r)for r in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines()]
    for name,digest in json.loads((Path(__file__).resolve().parent/'SOURCE-PINS.json').read_text())['files'].items():need(hashlib.sha256((args.repo.resolve()/name).read_bytes()).hexdigest()==digest,'frozen compiler pin '+name)
    total={'phase_forward_inverse_ADD':0,'source_parity_cache_INIT':0,'source_parity_form_ADD':0,'source_parity_inject_ADD':0,'source_parity_dirty_CLEAR':0,'H_early_cache_INIT':0,'H_early_cache_copy_ADD':0,'H_late_cross_ADD':0,'H_early_cache_dirty_CLEAR':0};source_records=[];Hrecords=[];all_holder_labels=set()
    for j,e in sorted(early.items(),key=lambda t:int(t[0])):
        phase=eliminate(np.array(e['physical_matrix'],dtype=np.uint8));got=receipts['sources'][j];need(phase==got['early'],'full source binary elimination receipt');total['phase_forward_inverse_ADD']+=2*phase['ADD_per_direction'];P=np.vstack([np.array(M,dtype=np.uint8).reshape(-1,480)for M in s['late_parities'][j].values()]);n=6*len(P);weight=int(WEIGHT[P].sum());bindings=[]
        for h,M in s['late_parities'][j].items():
            visits=sorted([r for r in routes if r[0]=='Y'and r[3]==int(h)and r[6]==int(j)],key=lambda r:(r[1],r[2]));need(len(visits)==len(M),'each parity has one actual Y visit')
            for q,r in enumerate(visits):
                label=f'source-parity/{j}/{h}/{q}';need(label not in all_holder_labels,'no source holder alias');all_holder_labels.add(label);bindings.append({'H':int(h),'Y_owner':[r[1],r[2]],'row':q,'cache_label':label})
        need(got['cache_bindings']==bindings and got['actual_late_field_parities']==len(P)and got['stationary_parity_bits']==n and got['exact_parity_form_ADD']==weight and got['actual_Y_injection_ADD']==n,'all source cache ownership and exact counts')
        total['source_parity_cache_INIT']+=n;total['source_parity_form_ADD']+=weight;total['source_parity_inject_ADD']+=n;total['source_parity_dirty_CLEAR']+=n;source_records.append({'donor':int(j),'phase':phase,'parity_fields':len(P),'formation_ADD':weight});print('COMPILER_SOURCE',j,phase['ADD_per_direction'],weight,flush=True)
    for h,data in sorted(hs.items(),key=lambda t:int(t[0])):
        E=np.array(data['early'],dtype=np.uint8);B=np.array(data['late'],dtype=np.uint8);G=np.array(data['cross'],dtype=np.uint8);paid=int(h)==642
        if paid:E=np.array(old['H']['642']['physical']['extension'],dtype=np.uint8)
        er=eliminate(E);br=eliminate(B)if len(B)else None;got=receipts['H'][h];need(got['early']==er and got['late']==br and got['paid_H642_extension']==paid,'all H phase ADD words reconstructed');n=6*len(data['X_owners'])if np.any(G)else 0;weight=int(WEIGHT[G].sum())if len(G)else 0;bindings=[[r[1],r[2]]for r in data['X_owners']]if n else[];need(got['stationary_original_early_cache_bits']==n and got['exact_late_cross_ADD']==weight and got['cache_bindings']==bindings,'actual H cache owners and exact cross cost');need(len(set(map(tuple,bindings)))==len(bindings),'distinct H cache input bindings')
        total['phase_forward_inverse_ADD']+=2*(er['ADD_per_direction']+(br['ADD_per_direction']if br else 0));total['H_early_cache_INIT']+=n;total['H_early_cache_copy_ADD']+=n;total['H_late_cross_ADD']+=weight;total['H_early_cache_dirty_CLEAR']+=n;Hrecords.append({'H':int(h),'early':er,'late':br,'cache_bits':n,'cross_ADD':weight})
        if int(h)in [263,642,947]:print('COMPILER_H',h,er['ADD_per_direction'],br['ADD_per_direction']if br else 0,weight,flush=True)
    need(total==bill['base_counts'],'complete independent base compiler count vector');dc=d['compiler'];base_add=total['phase_forward_inverse_ADD']+total['source_parity_form_ADD']+total['source_parity_inject_ADD']+total['H_early_cache_copy_ADD']+total['H_late_cross_ADD']+dc['including_pure_inverse_ADDs'];base_init=total['source_parity_cache_INIT']+total['H_early_cache_INIT']+dc['INIT']+12;base_clear=total['source_parity_dirty_CLEAR']+total['H_early_cache_dirty_CLEAR']+dc['dirty_CLEAR']+12;need(8*base_add==bill['fullbank_ADD_including_phase_inverses']==313198856 and 8*base_init==8*base_clear==bill['fullbank_INIT']==bill['fullbank_dirty_CLEAR']==134928,'exact eight-lane replacement bill');need(bill['fullbank_extra_field_exports']==16 and bill['fullbank_extra_MOVE_binary_records']==96 and bill['extra_MOVE_gap']==6 and bill['global_reverse_phase_compiler_dependency'],'paid H642 exports and global reverse dependency')
    result={'status':'PASS_INDEPENDENT_D1509_FULL_PREFIX_COMPILER_COUNTS','source_words':len(source_records),'H_words':len(Hrecords),'base_counts':total,'fullbank_ADD_including_pure_phase_inverses':8*base_add,'fullbank_INIT':8*base_init,'fullbank_dirty_CLEAR':8*base_clear,'fullbank_paid_field_exports':16,'source_parity_bindings':len(all_holder_labels),'all_author_elimination_digests_match':True,'author_executable_imports':False,'global_return_replayed':False,'full_supplier_invoice':False};args.out.mkdir(parents=True,exist_ok=True);(args.out/'COMPILER-REVIEW.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');payload=(json.dumps({'source':source_records,'H':Hrecords},sort_keys=True,separators=(',',':'))+'\n').encode();(args.out/'REBUILT-PHASE-RECEIPTS.json.gz').write_bytes(gzip.compress(payload,mtime=0));print(result['status'],313198856,134928,16,flush=True)
if __name__=='__main__':main()
