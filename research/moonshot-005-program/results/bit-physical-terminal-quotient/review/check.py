"""Independent physical-array and rank audit of the free-terminal return restriction."""
import argparse
import ctypes
import gzip
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np


BEFORE=[71,4,52,9,66]
AFTER=[13,54,88]
ROWS=[73,12,56]
COLS=[15,20,33,34,39,44]


def assert_that(ok,message):
    if not ok:raise ValueError(message)


def prepare_rank(folder):
    target=folder/'rank.so';src=Path(__file__).with_name('rank.cpp')
    subprocess.run(['c++','-std=c++17','-O3','-fPIC','-shared',str(src),'-o',str(target)],check=True)
    lib=ctypes.CDLL(str(target));fn=lib.dimension
    fn.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t];fn.restype=ctypes.c_size_t
    def rank(mat):
        a=np.array(mat,dtype=np.uint8,order='C',copy=True)
        assert_that((a<64).all(),'all entries in GF(64)')
        return fn(a.ctypes.data,*a.shape)
    return rank


def census(repo,arrays,rank):
    folder=repo/'research/moonshot-005-program/results'
    raw=gzip.decompress((folder/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes())
    assert_that(hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','native layout')
    q=json.loads(raw);roots=np.array(q['root_table'][:111],dtype=np.int64);foreign=roots@roots.T==0
    levels=[([i],[i]) for i in BEFORE]+[(ROWS,COLS)]+[([i],[i]) for i in AFTER]
    rr=[i for rows,cols in levels for i in rows];cc=[j for rows,cols in levels for j in cols]
    assert_that(len(set(rr))==len(rr) and len(set(cc))==len(cc),'coordinate injectivity')
    for t,(rows,cols) in enumerate(levels):
        for earlier,prevcols in levels[:t]:
            assert_that(all(i!=j and not foreign[i,j] for i in rows for j in prevcols),'lower-zero separation')
    assert_that(foreign[np.ix_(ROWS,COLS)].all(),'entire central array is foreign')
    out={}
    for kind in ('spread','mixed'):
        d={}
        for i in ROWS:
            for j in COLS:
                data=np.load(arrays/f'{kind}-{i}-{j}.npz');d[i,j]=(data['E'],data['Y'])
                assert_that(data['Y'].shape==(480,480) and data['E'].shape[1]==480,'true source bank')
        early=np.block([[d[i,j][0] for j in COLS] for i in ROWS]);late=np.block([[d[i,j][1] for j in COLS] for i in ROWS]);joint=np.vstack((early,late))
        e=rank(early);both=rank(joint)
        assert_that((e,both)==(1035,2430),'original ranks and cut')
        assert_that(rank(early[:,::-1])==e,'pivot convention reversal control')
        out[kind]={'free_terminal_rank_lower_per_body':both-e,'rank_E':e,'rank_EY':both,'shape_E':list(early.shape),'shape_Y':list(late.shape),
                   'E_bytes':hashlib.sha256(early.tobytes()).hexdigest(),'Y_bytes':hashlib.sha256(late.tobytes()).hexdigest()}
    return {'before_native_diagonals':BEFORE,'after_native_diagonals':AFTER,'core_native_rows':ROWS,'core_native_columns':COLS,
            'actual_own_diagonal_blocks':8,'bank':3840,'variants':out,'rank_lower':8*(8*480+1395),'excess_over_9banks':8*(8*480+1395)-9*3840}


def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--arrays',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--author-result',type=Path);a=p.parse_args()
    with tempfile.TemporaryDirectory() as tmp:result=census(a.repo,a.arrays,prepare_rank(Path(tmp)))
    if a.author_result:
        author=json.loads(a.author_result.read_bytes())['native_self_diagonal']['variants']
        for kind,record in result['variants'].items():
            assert_that(author[kind]['early_payload_sha256']==record['E_bytes'] and author[kind]['late_payload_sha256']==record['Y_bytes'],'all raw bytes match independent construction')
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RANK.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result)


if __name__=='__main__':main()
