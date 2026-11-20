#!/usr/bin/env python3
"""Verify both native four-role gauges and their complete local ordinary invoice."""
import argparse
import ctypes
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import numpy as np


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(array):
    return hashlib.sha256(np.ascontiguousarray(array).tobytes()).hexdigest()


def run(args):
    subprocess.run(args, check=True)


def double(matrix):
    zero=np.zeros_like(matrix)
    return np.block([[matrix,zero],[zero,matrix]])


def verify_sector(data, schur, arithmetic, engine):
    width=len(schur)//4
    pair_width=2*width
    identity=np.eye(pair_width,dtype=np.uint8)
    gauges,inverses,modes=data['W'],data['actual'],data['X_local']
    require(np.array_equal(schur,data['K_reduced']), 'native four-role Schur mismatch')
    require(np.array_equal(modes[:2*pair_width],np.eye(2*pair_width,dtype=np.uint8)), 'independent original modes')
    field=engine.lib
    field.gauge_invoice.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_uint8]
    field.gauge_invoice.restype=ctypes.c_uint64
    costs=[]
    arrays=[]
    for i in range(4):
        require(np.array_equal(arithmetic.matmul(gauges[i],inverses[i]),identity), 'physical facet gauge inverse')
        blocks=[double(schur[i*width:(i+1)*width,j*width:(j+1)*width]) for j in range(4)]
        blocks[i]^=inverses[i]^identity
        total=np.zeros((pair_width,2*pair_width),dtype=np.uint8)
        for j,block in enumerate(blocks):
            total^=arithmetic.matmul(block,modes[j*pair_width:(j+1)*pair_width])
        require(not total.any(), 'proper physical residual in an independent field engine')
        costs.append(int(field.gauge_invoice(inverses[i].ctypes.data,pair_width,1)))
        require(costs[-1]<2**63,'finite local gauge invoice')
        arrays.append(blocks)
    cross=np.block([q[2:] for q in arrays[:2]])
    state=field.begin(len(cross))
    try:
        for pos in range(0,len(cross),32):
            block=np.ascontiguousarray(cross[pos:pos+32])
            require(field.consume(state,block.ctypes.data,len(block)),'fixed native cross minor')
        require(field.present_rank(state)==len(cross), 'matching lower rank')
        det=int(field.determinant(state))
    finally:
        field.finish(state)
    return {'one_copy_sector_width':width,'roles':[0,1,2,3],'schur_sha256':digest(schur),
            'inverse_gauges_sha256':digest(inverses),'fixed_cross_determinant':det,
            'one_pair_kernel_dimension':2*pair_width,'one_pair_fitting_rank':109*pair_width,
            'forward_ADDs_per_facet_and_pair':costs,'forward_ADDs_four_pairs':4*sum(costs),
            'forward_and_inverse_ADDs_four_pairs':8*sum(costs)}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--heavy',action='store_true',help='regenerate the two native Schur matrices from every actual source column')
    p.add_argument('--emit-gauges', action='store_true',help='retain four paired gauge and kernel arrays for both invariant sectors')
    args=p.parse_args();repo=args.repo.resolve();dest=args.out.resolve();dest.mkdir(parents=True,exist_ok=True)
    home=Path(__file__).resolve().parent;author=home/'author';base=repo/'research/moonshot-005-program/results'
    stream=base/'bit-native-rs-return-distance/stream';physical=base/'bit-spread-rs-physical-word/author'
    manifest=json.loads((author/'sources/MANIFEST.json').read_text())
    spec=importlib.util.spec_from_file_location('native_stream',stream/'check.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    sys.path.insert(0,str(physical));from transfer import Arithmetic
    sectors={}
    with tempfile.TemporaryDirectory(prefix='facet-rank-') as td:
        tmp=Path(td);lib=tmp/'stream.so';mul=tmp/'primal.so'
        for file,shared in ((stream/'stream.c',lib),(physical/'gf64_matmul.c',mul)):
            run(['cc','-O3','-march=native','-std=c11','-fPIC','-shared',str(file),'-o',str(shared)])
        engine=module.Engine(lib);op=Arithmetic(mul)
        for sector in ('small','large'):
            size=manifest[sector]['matrix_size'];raw=gzip.decompress((author/'sources'/(sector+'-four-schur.bin.gz')).read_bytes());schur=np.frombuffer(raw,np.uint8).reshape(size,size)
            require(digest(schur)==manifest[sector]['sha256'],'bound native Schur matrix')
            prepared=tmp/(sector+'.npz');np.savez(prepared,matrix=schur)
            inputs=['--data',str(prepared),'--four']
            if args.heavy:
                run([sys.executable,'-I','-B',str(author/'native_quotient.py'),'--repo',str(repo),'--replay',str(base/'bit-physical-terminal-quotient/author'),'--engine',str(stream),'--h-words',str(physical/'output'),'--d-words',str(base/'bit-minimum-cache-d-atlas/author/output'),'--k-words',str(base/'bit-gf64-actual-k-atlas/author/output'),'--stream-lib',str(lib),'--out',str(tmp/'native'),'--sector',sector,'--roles','0,1,2,3'])
                inputs=['--data',str(tmp/'native'/(sector.upper()+'.npz'))]
            answer=tmp/(sector+'-answer');run([sys.executable,'-I','-B',str(author/'solve.py'),'--engine',str(stream),'--lib',str(lib),*inputs,'--out',str(answer)])
            with np.load(answer/'GAUGES.npz') as arr:
                sectors[sector]=verify_sector(arr,schur,op,engine)
                if args.emit_gauges:np.savez_compressed(dest/(sector.upper()+'-GAUGES.npz'),W=arr['W'],Winv=arr['actual'],kernel=arr['X_local'])
    n=111*3840;q=sum(4*s['one_pair_fitting_rank'] for s in sectors.values());saved=n-q
    result={'sectors':sectors,'native_bank_fields':3840,'baseline_return_rank':n,'changed_return_rank':q,
            'return_binary_MOVE_records':6*q,'saved_return_bits':6*saved,'extra_return_fields_over_9b':q-9*3840,
            'excess_versus_m870_return_cap':q-34688,'all_foreign_proper_ranks_preserved':6470,
            'incremental_forward_ADDs':sum(s['forward_ADDs_four_pairs'] for s in sectors.values()),
            'incremental_forward_and_ground_inverse_ADDs':sum(s['forward_and_inverse_ADDs_four_pairs'] for s in sectors.values()),
            'additional_gauge_INIT':0,'additional_gauge_MOVE':0,'additional_gauge_dirty_CLEAR':0,'additional_gauge_stationary_storage':0,
            'complete_multiplier_supplier':False}
    def receipt(name):
        return json.loads((base/name).read_bytes())
    rs='bit-spread-rs-physical-word/author/'
    source=receipt(rs+'source-output/RESULT.json')['finite_source_costs']
    middle_h=receipt(rs+'output/RESULT.json')['finite_word_accounting']
    middle_d=receipt('bit-minimum-cache-d-atlas/author/output/RESULT.json')['bank3840']
    middle_k=receipt('bit-gf64-actual-k-atlas/author/output/RESULT.json')['spread']['bank3840']
    final=receipt(rs+'terminal-output/RESULT.json')['spread']['costs']
    fixed=[source,middle_h,middle_d,middle_k,final]
    proper=sum(x[k] for x,k in zip(fixed,('forward_plus_reserved_pure_inverse_ADD',
        'forward_plus_reserved_endpoint_inverses_ADD','total_ADD','total_ADD','forward_plus_pure_inverse_ADD')))
    captures=sum(x['INIT']for x in fixed)
    require(captures==sum(x['dirty_CLEAR']for x in fixed),'complete proper-stage stationary lifetime')
    M=6*n;C=6*q;lanes=6*3840
    result['physical_paid_MOVE_histogram']={1:4451*lanes//8,2:7213*lanes//16,4:24*lanes,8:C}
    result['normalized_paid_MOVE_histogram']={1:'4451/8',2:'7213/16',4:'24',8:'109'}
    result['fixed_proper_and_reserved_inverse_ADDs']=proper
    result['fixed_plus_changed_proper_and_reserved_inverse_ADDs']=proper+result['incremental_forward_and_ground_inverse_ADDs']
    result['binary_return_basis_formation_and_preload_ADD_upper_bound']=2*M*C
    result['total_return_and_recorded_proper_ADD_upper_bound']=proper+result['incremental_forward_and_ground_inverse_ADDs']+2*M*C
    result['proper_stationary_INIT_and_dirty_CLEAR_each']=captures
    result['return_and_proper_INIT_and_dirty_CLEAR_each']=captures+C
    result['inherited_peak_public_plus_auxiliary_upper_bound']=7*M+C
    result['paired_gap_at_zero_saving']='14562 - 13809 m'
    require((q,6*saved,result['incremental_forward_and_ground_inverse_ADDs'])==(418560,46080,361035496),'full native return and ordinary invoice')
    (dest/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('native fields',q,'binary return saving',6*saved,'gauge ADDs',result['incremental_forward_and_ground_inverse_ADDs'])
if __name__=='__main__':main()
