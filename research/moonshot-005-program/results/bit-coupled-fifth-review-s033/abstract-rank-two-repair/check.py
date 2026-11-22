#!/usr/bin/env python3
"""Exact optimal abstract rank-two repair of the donor32 off95 map."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import numpy as np
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('rank_repair_gf64',HERE.parent/'check.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def extend_four(A):
    columns=[A[:,q] for q in range(A.shape[1])]
    for e in np.eye(8,dtype=np.uint8).T:
        if m.rank(np.column_stack(columns+[e]))>len(columns):columns.append(e)
        if len(columns)==4:break
    out=np.column_stack(columns);m.need(out.shape==(8,4) and m.rank(out)==4,'four independent projected columns')
    return out

def main(repo,out):
    source=HERE.parent/'wave3/isolation-output/CERTIFICATE.json'
    old=m.read(source);M=np.array(old['donor32_matrix'],dtype=np.uint8);N=np.array(old['donor32_kernel'],dtype=np.uint8)
    m.need(M.shape==(16,16) and m.rank(M)==12 and N.shape==(16,4) and m.rank(N)==4,'original map and kernel')
    m.need(not np.any(m.mm(M,N)) and m.rank(N[:8])==m.rank(N[8:])==2,'original kernel projections')
    U=N[:8,m.rref(N[:8])[1]];V=N[8:,m.rref(N[8:])[1]]
    # kerM has dimension4 inside the4-dimensional direct sum imU+imV,
    # so every separately chosen projected pair belongs to kerM.
    diagonal=np.vstack([U,V]);m.need(not np.any(m.mm(M,diagonal)),'two graph directions in old kernel')
    C=np.vstack([extend_four(U),extend_four(V)])
    m.need(m.rank(C[:8])==m.rank(C[8:])==m.rank(C)==4,'desired transverse four-space')
    X=C[:,2:];Y=m.mm(M,X)
    m.need(m.rank(Y)==2 and m.rank(m.mm(M,C))==2,'sharp original leakage')
    joined=np.hstack([N,X]);m.need(m.rank(joined)==6,'two new directions modulo old kernel')
    target=np.hstack([np.zeros((2,4),dtype=np.uint8),np.eye(2,dtype=np.uint8)])
    L=m.solve(joined.T,target.T).T
    m.need(not np.any(m.mm(L,N)) and np.array_equal(m.mm(L,X),np.eye(2,dtype=np.uint8)),'annihilating left inverse')
    delta=m.mm(Y,L);new=M^delta
    m.need(m.rank(delta)==2 and not np.any(m.mm(delta,N)),'rank-two update preserves old kernel')
    m.need(not np.any(m.mm(new,C)) and m.rank(new)==10,'complete abstract repair')
    new_kernel=m.null(new)
    m.need(new_kernel.shape[1]==6 and m.rank(new_kernel[:8])==m.rank(new_kernel[8:])==4,'repaired kernel projections')
    rank_one=m.mm(Y[:,:1],L[:1]);one=M^rank_one
    m.need(m.rank(rank_one)==1 and m.rank(m.mm(one,C))==1,'rank-one negative control leaves leakage')
    result=dict(status='PASS_OPTIMAL_ABSTRACT_RANK_TWO_REPAIR',original_rank=12,
        original_kernel_dimension=4,original_kernel_projection_ranks=[2,2],
        target_four_space_projection_ranks=[4,4],original_leakage_on_target_rank=2,
        minimum_update_rank=2,attained_update_rank=m.rank(delta),repaired_map_rank=m.rank(new),
        repaired_kernel_dimension=6,repaired_kernel_projection_ranks=[4,4],
        original_kernel_preserved=True,rank_one_control_residual_rank=1,
        coefficient_extensions=True,repetition_minimum_update_rank='2k',
        implementable_H_word_established=False,new_owner_or_cost_claim=False,new_complete_kappa=False)
    cert=dict(source_matrix=M.tolist(),source_kernel=N.tolist(),
        target_frame=C.tolist(),extra_directions=X.tolist(),left_inverse_annihilating_old_kernel=L.tolist(),
        rank_two_update=delta.tolist(),repaired_matrix=new.tolist(),rank_one_control=rank_one.tolist())
    pins={str(source.relative_to(repo)):hashlib.sha256(source.read_bytes()).hexdigest(),
          str((HERE.parent/'check.py').relative_to(repo)):hashlib.sha256((HERE.parent/'check.py').read_bytes()).hexdigest()}
    expected=HERE/'SOURCE-PINS.json'
    if expected.exists():m.need(pins==m.read(expected),'source pins')
    out.mkdir(parents=True,exist_ok=True)
    for name,value in [('RESULT',result),('CERTIFICATE',cert),('SOURCE-PINS',pins)]:
        (out/(name+'.json')).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    q=p.parse_args();main(q.repo.resolve(),q.out.resolve())
