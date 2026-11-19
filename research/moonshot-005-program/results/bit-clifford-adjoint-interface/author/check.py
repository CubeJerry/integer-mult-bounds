#!/usr/bin/env python3
"""Exact characteristic-two Clifford adjoint and endpoint-dual checks."""
import argparse,gzip,hashlib,json
from pathlib import Path
from algebra import require,identity,transpose,multiply,plus,tensor,matrix_rank,native

def flat(A):return sum(x<<(len(A)*i)for i,x in enumerate(A))
def comm(A,B):return plus(multiply(A,B),multiply(B,A))
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    base=a.repo/'research/moonshot-005-program/results';lp=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';bp=base/'bit-clifford-one-evaluation-gate/author/BASIS.json'
    raw=gzip.decompress(lp.read_bytes());require(hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    layout=json.loads(raw);gammas,nb=native(layout,json.loads(bp.read_text()))
    J=[1<<(15-i)for i in range(16)];JE=[1<<(255-i)for i in range(256)]
    require(multiply(J,J)==identity(16)and transpose(J)==J,'nondegenerate symmetric spinor pairing')
    require(all((row>>i&1)==0 for i,row in enumerate(J)),'alternating spinor pairing')
    def adj(M):return multiply(multiply(J,transpose(M)),J)
    require(all(adj(M)==M for M in gammas),'all root gammas self-adjoint')
    K=layout['A2'][370];i,j=K[:2];basis=[identity(16),gammas[i],gammas[j],multiply(gammas[i],gammas[j])]
    require(matrix_rank(list(map(flat,basis)))==4,'full native K algebra')
    one_constraints=[flat(comm(M,gammas[i]))for M in basis]
    two_constraints=[flat(comm(M,gammas[i]))|(flat(comm(M,gammas[j]))<<256)for M in basis]
    require(matrix_rank(one_constraints)==2,'one root centralizer has dimension2 in M2')
    require(matrix_rank(two_constraints)==3,'two generators have scalar common centralizer')
    scalar=identity(16);require(all(comm(scalar,x)==[0]*16 for x in basis),'scalar positive control')
    require(comm(gammas[j],gammas[i])==identity(16),'unrestricted local coefficient fails receiver covariance')
    # F(X)=B X e_t. In row-major matrix coordinates, the pairing on EndS
    # has the complement permutation JE. Verify the adjoint formula on
    # all64 basis maps and every matrix/spinor coordinate at once.
    formula_checks=0;ordinary_transpose_faults=0
    for B in basis:
        for t in range(16):
            F=[sum(((B[r]>>u)&1)<<(16*u+t)for u in range(16))for r in range(16)]
            exact=multiply(multiply(JE,transpose(F,256)),J)
            Bstar=adj(B);formula=[0]*256
            for r in range(16):formula[16*r+(15-t)]=Bstar[r]
            require(exact==formula,'F dagger rank-one formula')
            ordinary_transpose_faults+=exact!=transpose(F,256)
            formula_checks+=1
    require(ordinary_transpose_faults>0,'ordinary transpose is not the paired adjoint')
    # The adjoint reverses products, and transpose exchanges left/right
    # actions. Check a source coefficient where the distinction matters.
    require(adj(multiply(gammas[i],gammas[j]))==multiply(adj(gammas[j]),adj(gammas[i])),'adjoint reverses product')
    bad=[0]*16;bad[0]=1
    found=next((k for k,M in enumerate(gammas)if multiply(M,bad)!=multiply(bad,M)),None)
    require(found is not None,'noncommuting transpose control')
    result={'status':'PASS_CLIFFORD_DUAL_INTERFACE','field_scope':'every characteristic-two field',
      'root_self_adjoint_checks':len(gammas),'native_K':370,'K_roots':K,
      'paired_adjoint_basis_maps_checked':formula_checks,'ordinary_transpose_fault_count':ordinary_transpose_faults,
      'full_covariant_coefficient_dimension':64,'one_receiver_intertwining_dimension':32,
      'common_two_receiver_intertwining_dimension':16,'noncommuting_transpose_root':found,
      'scope':'Correct paired adjoint and necessary/sufficient algebraic mirrored-covariance condition; not a full native decoder.',
      'source_pins':[{'path':str(p.relative_to(a.repo)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in [lp,bp]],
      'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status']);print(json.dumps({k:result[k]for k in ['paired_adjoint_basis_maps_checked','ordinary_transpose_fault_count','one_receiver_intertwining_dimension','common_two_receiver_intertwining_dimension']},sort_keys=True))
if __name__=='__main__':main()
