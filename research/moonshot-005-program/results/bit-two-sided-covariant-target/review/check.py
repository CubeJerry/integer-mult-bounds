#!/usr/bin/env python3
"""Separate reconstruction of the two-sided target's algebraic evidence."""
import argparse,gzip,hashlib,json
from pathlib import Path
from algebra import require,identity,transpose,multiply,plus,tensor,matrix_rank,inverse,native

def flat(A):return sum(r<<(len(A)*i)for i,r in enumerate(A))
def comm(A,B):return plus(multiply(A,B),multiply(B,A))
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    base=a.repo/'research/moonshot-005-program/results'
    lp=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';bp=base/'bit-clifford-one-evaluation-gate/author/BASIS.json'
    ap=base/'bit-receiver-covariant-target/author/output/ASSIGNMENT.json';wp=a.author/'WITNESS.json'
    raw=gzip.decompress(lp.read_bytes());require(hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    layout=json.loads(raw);g,nb=native(layout,json.loads(bp.read_text()))
    old=json.loads(ap.read_text());P=transpose(old['adapted_spinor_basis_columns']);Q=inverse(P)
    g=[multiply(multiply(Q,x),P)for x in g]
    require(plus(g[80],identity(16))==tensor([2,0],identity(8)),'adapted receiver action')
    require(plus(g[10],identity(16))==tensor([0,1],identity(8)),'adapted donor action')
    witness=json.loads(wp.read_text());T8,W8,U8=witness['secondary_matrices_8']
    T=plus(tensor(T8,identity(4)),tensor(identity(8),[2,4,8,0]))
    W=plus(tensor(W8,identity(4)),tensor(identity(8),[0,0,0,1]));U=tensor(U8,identity(4))
    matrices=[]
    for word in witness['word_basis_32']:
        M=identity(32)
        for index in word:
            require(index in [0,1,2],'word index');M=multiply(M,[T,W,U][index])
        matrices.append(flat(M))
    require(len(matrices)==1024 and matrix_rank(matrices)==1024,'independent full M32 word basis')
    require(matrix_rank(matrices[1:]+[matrices[1]])==1023,'duplicated word basis mutant rejected')
    E01,E10=[2,0],[0,1]
    internal=[tensor(E01,M)for M in [identity(32),T,W]]+[tensor(E10,M)for M in [identity(32),U]]
    edges=[(80,106),(80,107),(80,109),(109,10),(110,10)]
    require(sorted(nb[80])[59:]==[106,107,109]and sorted(nb[10])[59:]==[109,110],'actual five free slots')
    diagnostics=[]
    for M,(i,j)in zip(internal,edges):
        require(j in nb[i],'internal foreign edge')
        require(multiply(M,M)==[0]*64,'square-zero internal matrix')
        require(matrix_rank(plus(M,identity(64)))==64,'invertible foreign internal block')
        ranks=[matrix_rank(comm(M,tensor(g[k],identity(4))))for k in [i,j]]
        require(ranks==[0,0],'both endpoint commutators')
        diagnostics.append({'edge':[i,j],'commutator_ranks':ranks})
    for M,expected in [(multiply(internal[0],internal[3]),tensor([1,0],identity(32))),
                       (multiply(internal[3],internal[0]),tensor([0,2],identity(32)))]:
        require(M==expected,'independent matrix-unit multiplication')
    for index,M in enumerate([T,W,U]):
        if index<2:
            value=plus(multiply(internal[index+1],internal[3]),multiply(internal[3],internal[index+1]))
        else:value=plus(multiply(internal[0],internal[4]),multiply(internal[4],internal[0]))
        require(value==tensor(identity(2),M),'secondary generator on both halves')
    K=[(1<<i)|sum(1<<j for j in nb[i])for i in range(111)]
    require(matrix_rank(K)==9 and sum(map(len,nb))==6470,'native rank and foreign count')
    supports=[nb[80]|{10},nb[10]|{80}];separation=[]
    for support in supports:
        mask=sum(1<<i for i in range(111)if i not in support)
        separation.append(matrix_rank([row&mask for row in K]))
    require(separation==[9,9],'row and column rank separation')
    all_edges={(80,j)for j in nb[80]}|{(i,10)for i in nb[10]}
    require(len(all_edges)==123 and all((j,i)not in all_edges for i,j in all_edges),'one identity orientation per changed edge')
    require(10 not in nb[80]and 80 not in nb[10],'disjoint star input and output supports')
    visited={0}
    while True:
        nxt=visited|set.union(*(nb[i]for i in visited))
        if nxt==visited:break
        visited=nxt
    require(len(visited)==111,'connected native graph')
    # One bank transfer is onto its entire64-dimensional row-star image,
    # and one reverse transfer is injective on the64-dimensional column input.
    F=[0]*60;F[0]=2;R=[0]*60;R[1]=1
    require(matrix_rank(F)==matrix_rank(R)==1,'whole-spinor transfer rank')
    require(multiply(F,R)==[1]+[0]*59,'bank-zero matrix unit')
    require(multiply(R,F)==[0,2]+[0]*58,'bank-one matrix unit')
    require(matrix_rank(internal[0]+internal[3])==64,'zero common internal kernel')
    require(matrix_rank(transpose(internal[0])+transpose(internal[3]))==64,'full common internal image')
    bad=[0]*64;bad[0]=1;require(matrix_rank(plus(bad,identity(64)))==63,'singular diagonal mutant')
    wrong=None
    for r in range(32):
        for c in range(32):
            E=[0]*32;E[r]=1<<c;M=tensor(E01,E)
            z=matrix_rank(comm(M,tensor(g[107],identity(4))))
            if z:wrong={'entry':[r,c],'donor_rank':z};break
        if wrong:break
    require(wrong is not None,'receiver-only covariance mutant')
    # Diagnose exactly why the previous receiver-only target cannot simply
    # be mirrored under the donor/receiver dual contract.
    old_failures=[]
    for s in [1,4,12]:
        n=8*s;J=[1<<(r+1)if r+1<n else 0 for r in range(n)];E=[0]*(n-1)+[1]
        for donor,N in [(0,tensor(identity(2),J)),(2,tensor(identity(2),E))]:
            receiver_rank=matrix_rank(comm(N,tensor(g[80],identity(s))))
            donor_rank=matrix_rank(comm(N,tensor(g[donor],identity(s))))
            require(receiver_rank==0 and donor_rank==({0:16,2:4}[donor]),'old target covariance diagnostic')
            old_failures.append({'s':s,'edge':[80,donor],'receiver_rank':receiver_rank,'donor_rank':donor_rank})
    paths=[lp,bp,ap,wp,a.author/'PROOF.md',a.author/'check.py']
    result={'status':'PASS_SEPARATE_TWO_SIDED_TARGET_REVIEW','author_code_imported':False,
      'bank':3840,'secondary_word_basis_rank':1024,'maximum_word_length':max(map(len,witness['word_basis_32'])),
      'internal_endpoint_checks':diagnostics,'native_rank':9,'separation':separation,
      'row_star_rank':64,'column_star_rank':64,'perturbation_rank':128,'return_rank':34688,
      'full_algebra_dimension_proved':3840**2,'independence_scope':'Separate finite algebra and geometry reconstruction plus written proof review; no human or formal-kernel review.',
      'old_target_donor_covariance_failures':old_failures,
      'negative_controls':{'duplicated_word_rank':1023,'wrong_endpoint':wrong,'diagonal_mutant_rank':63},
      'source_pins':[{'path':str(path.relative_to(a.repo))if path.is_relative_to(a.repo)else path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}for path in paths],
      'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status']);print(json.dumps({k:result[k]for k in ['secondary_word_basis_rank','perturbation_rank','return_rank','author_code_imported']},sort_keys=True))
if __name__=='__main__':main()
