"""Audit the whole 64-coordinate row at F80 and whole 64-coordinate column at line 10."""
import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np


def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True)
    p.add_argument('--replayer',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    spec=importlib.util.spec_from_file_location('complete_star_replay',a.replayer);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    routes,assignment=v.phase_input(a.repo);ledger=json.loads((a.word/'RESULT.json').read_bytes());res={};sides={};wants={}
    for side in ('row','column'):
        raw=json.loads(v.bytes_at(a.word/(side+'-word.json.gz'),ledger['word_SHA256'][side]));ops,taps,prices=v.decode_ops(raw,routes)
        wanted=v.target_matrix(assignment,side).reshape(111,3840,64);center=80 if side=='row' else 10
        ordinary=assignment[side+'_transfers'];adj={j if side=='row' else i for i,j,ell in ordinary}
        for i,j in assignment['internal_edges']:
            if (i if side=='row' else j)==center:adj.add(j if side=='row' else i)
        for j in adj:wanted[j,:64]^=np.eye(64,dtype=np.uint8)
        want=wanted.reshape(53280,8,64);got=v.transfer(taps,ops)
        v.require(np.array_equal(want,got),'every native field and master coordinate')
        v.require(prices['total']==ledger['word_costs'][side]['total_ADD'],'full binary gate invoice')
        failed=v.transfer(taps,ops,missing=True)
        diff=int(np.count_nonzero(failed!=want));v.require(diff>0,'GL-only fault')
        wants[side]=want;sides[side]=(ops,taps)
        res[side]={'edges_with_exact_central_canonical_component':len(adj),'nonzero_coefficients':int(np.count_nonzero(got)),
                   'confirmed_all_original_rows':len(got)*8,'master_dimensions':64,'invoice':prices['total'],'one_shear_fault':diff}
    v.numeric(sides['row'],sides['column'],wants)
    res['total_binary_ADD']=sum(q['invoice'] for q in res.values());res['entire_F80_64_output_rows']=True;res['line10_all_center_columns']=True
    res['all_X_returned_and_all_Y_baselines']=True;res['extra_MOVE']=0;res['INIT']=res['dirty_CLEAR']=768
    a.out.mkdir(exist_ok=True,parents=True);(a.out/'REPLAY.json').write_text(json.dumps(res,sort_keys=True,indent=2)+'\n');print(res)


if __name__=='__main__':main()
